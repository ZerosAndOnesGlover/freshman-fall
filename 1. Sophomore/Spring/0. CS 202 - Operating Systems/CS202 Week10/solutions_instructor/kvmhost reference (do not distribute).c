/* kvmhost.c — a hypervisor in one file: create a virtual machine through /dev/kvm,
 * give it a megabyte of memory and one virtual CPU in 16-bit real mode, and run a
 * guest that talks to the outside world by writing to an I/O port.
 *
 *   gcc -O2 -Wall -Wextra -o kvmhost kvmhost.c
 *   ./kvmhost hello        the guest prints a string through port 0x3f8 and halts
 *   ./kvmhost exits N      N port-I/O exits: the cost of an exit that reaches this process
 *   ./kvmhost cpuid N      N cpuid instructions: an exit KVM handles without leaving the kernel
 *   ./kvmhost mmio         the guest writes to unmapped memory: an MMIO exit
 *
 * CS 202 Week 10, L31-L33 and PS 10. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <linux/kvm.h>
#include <errno.h>

#define GUEST_MEM  (64 << 10)         /* 64 KiB of guest physical memory: everything above is unmapped */
#define CODE_ADDR  0x1000             /* where the guest's code is placed */
#define DATA_ADDR  0x2000             /* and its string */

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

/* 16-bit real-mode guests, assembled by hand. */
static const unsigned char guest_hello[] = {
    0xbe, 0x00, 0x20,             /* mov si, 0x2000     */
    0xba, 0xf8, 0x03,             /* mov dx, 0x3f8      */
    0xac,                         /* lodsb              */
    0x3c, 0x00,                   /* cmp al, 0          */
    0x74, 0x03,                   /* je  done           */
    0xee,                         /* out dx, al         */
    0xeb, 0xf8,                   /* jmp back to lodsb  */
    0xf4,                         /* done: hlt          */
};

static const unsigned char guest_exits[] = {
    0xba, 0xf8, 0x03,             /* mov dx, 0x3f8      */
    0xee,                         /* out dx, al         */
    0xeb, 0xfd,                   /* jmp back to out — forever; the host stops it */
};

/* cpuid always leaves the guest, but KVM answers it inside the kernel: the hypervisor
 * process never runs. Counted by the guest, in cx, so one KVM_RUN covers all of them —
 * and cx must be saved around cpuid, which returns part of the vendor string in ecx. */
static const unsigned char guest_cpuid[] = {
    0x51,                         /* push cx            */
    0x31, 0xc0,                   /* xor ax, ax         */
    0x0f, 0xa2,                   /* cpuid              */
    0x59,                         /* pop cx             */
    0xe2, 0xf8,                   /* loop back to push  */
    0xf4,                         /* hlt                */
};

static const unsigned char guest_mmio[] = {
    0xb8, 0x00, 0x80,             /* mov ax, 0x8000     */
    0x8e, 0xc0,                   /* mov es, ax         */
    0x26, 0xc6, 0x06, 0x00, 0x00, 0x2a,   /* mov byte [es:0], 0x2a  — 0x80000, unmapped */
    0xf4,                         /* hlt                */
};

int main(int argc, char **argv)
{
    const char *mode = argc > 1 ? argv[1] : "hello";
    unsigned long count = argc > 2 ? strtoul(argv[2], 0, 10) : 100000;

    int kvm = open("/dev/kvm", O_RDWR | O_CLOEXEC);
    if (kvm < 0) { perror("/dev/kvm"); return 1; }
    if (ioctl(kvm, KVM_GET_API_VERSION, 0) != 12) { fprintf(stderr, "unexpected KVM API version\n"); return 1; }

    int vmfd = ioctl(kvm, KVM_CREATE_VM, 0);
    if (vmfd < 0) { perror("KVM_CREATE_VM"); return 1; }

    /* Guest physical memory is just a mapping in this process. */
    void *mem = mmap(0, GUEST_MEM, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    if (mem == MAP_FAILED) { perror("mmap"); return 1; }
    struct kvm_userspace_memory_region region = {
        .slot = 0, .guest_phys_addr = 0, .memory_size = GUEST_MEM,
        .userspace_addr = (unsigned long)mem,
    };
    if (ioctl(vmfd, KVM_SET_USER_MEMORY_REGION, &region) < 0) { perror("KVM_SET_USER_MEMORY_REGION"); return 1; }

    const unsigned char *code = guest_hello;
    size_t codelen = sizeof guest_hello;
    if (!strcmp(mode, "exits")) { code = guest_exits; codelen = sizeof guest_exits; }
    else if (!strcmp(mode, "cpuid")) { code = guest_cpuid; codelen = sizeof guest_cpuid; }
    else if (!strcmp(mode, "mmio")) { code = guest_mmio; codelen = sizeof guest_mmio; }
    memcpy((char *)mem + CODE_ADDR, code, codelen);
    strcpy((char *)mem + DATA_ADDR, "Hello from the guest\n");

    int vcpufd = ioctl(vmfd, KVM_CREATE_VCPU, 0);
    if (vcpufd < 0) { perror("KVM_CREATE_VCPU"); return 1; }
    int runsize = ioctl(kvm, KVM_GET_VCPU_MMAP_SIZE, 0);
    struct kvm_run *run = mmap(0, runsize, PROT_READ | PROT_WRITE, MAP_SHARED, vcpufd, 0);
    if (run == MAP_FAILED) { perror("mmap kvm_run"); return 1; }

    /* Real mode: a flat 16-bit code segment at 0, starting at CODE_ADDR. */
    struct kvm_sregs sregs;
    if (ioctl(vcpufd, KVM_GET_SREGS, &sregs) < 0) { perror("KVM_GET_SREGS"); return 1; }
    sregs.cs.base = 0;
    sregs.cs.selector = 0;
    if (ioctl(vcpufd, KVM_SET_SREGS, &sregs) < 0) { perror("KVM_SET_SREGS"); return 1; }

    if (!strcmp(mode, "cpuid") && count > 65535) count = 65535;   /* cx is 16 bits in real mode */
    struct kvm_regs regs = { .rip = CODE_ADDR, .rflags = 0x2, .rax = 'A', .rcx = count, .rsp = 0x8000 };
    if (ioctl(vcpufd, KVM_SET_REGS, &regs) < 0) { perror("KVM_SET_REGS"); return 1; }

    unsigned long io_exits = 0, mmio_exits = 0, other = 0;
    double t0 = now();
    for (;;) {
        if (ioctl(vcpufd, KVM_RUN, 0) < 0) {
            if (errno == EINTR) continue;     /* a signal arrived; re-enter the guest */
            perror("KVM_RUN");
            return 1;
        }
        if (run->exit_reason == KVM_EXIT_IO) {
            io_exits++;
            if (!strcmp(mode, "hello"))
                putchar(*((char *)run + run->io.data_offset));
            if (!strcmp(mode, "exits") && io_exits >= count)
                break;                          /* the guest loops forever; we stop entering it */
        } else if (run->exit_reason == KVM_EXIT_MMIO) {
            mmio_exits++;
            printf("MMIO exit: %s %u byte(s) at guest physical 0x%llx, data 0x%02x\n",
                   run->mmio.is_write ? "write of" : "read of", run->mmio.len,
                   (unsigned long long)run->mmio.phys_addr, run->mmio.data[0]);
        } else if (run->exit_reason == KVM_EXIT_HLT) {
            break;
        } else {
            other++;
            fprintf(stderr, "unhandled exit_reason %u\n", run->exit_reason);
            break;
        }
    }
    double t1 = now();

    if (!strcmp(mode, "exits"))
        printf("%lu port-I/O exits in %.4f s = %.0f ns per exit\n", io_exits, t1 - t0,
               (t1 - t0) * 1e9 / (io_exits ? io_exits : 1));
    else if (!strcmp(mode, "cpuid"))
        printf("%lu cpuid instructions in %.4f s = %.0f ns each, in one KVM_RUN\n", count, t1 - t0,
               (t1 - t0) * 1e9 / count);
    else
        printf("guest halted after %lu I/O exits, %lu MMIO exits, %lu other, in %.4f s\n",
               io_exits, mmio_exits, other, t1 - t0);
    return 0;
}
