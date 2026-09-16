#define _GNU_SOURCE
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/kvm.h>
int main(void)
{
    int fd = open("/dev/kvm", O_RDWR);
    if (fd < 0) { perror("/dev/kvm"); return 1; }
    printf("KVM_GET_API_VERSION      %d\n", ioctl(fd, KVM_GET_API_VERSION, 0));
    printf("KVM_GET_VCPU_MMAP_SIZE   %d bytes\n", ioctl(fd, KVM_GET_VCPU_MMAP_SIZE, 0));
    struct { const char *name; int cap; } caps[] = {
        { "NR_VCPUS", KVM_CAP_NR_VCPUS }, { "MAX_VCPUS", KVM_CAP_MAX_VCPUS },
        { "NR_MEMSLOTS", KVM_CAP_NR_MEMSLOTS }, { "USER_MEMORY", KVM_CAP_USER_MEMORY },
        { "SET_TSS_ADDR", KVM_CAP_SET_TSS_ADDR }, { "IMMEDIATE_EXIT", KVM_CAP_IMMEDIATE_EXIT },
        { "IRQCHIP", KVM_CAP_IRQCHIP }, { "COALESCED_MMIO", KVM_CAP_COALESCED_MMIO },
    };
    for (unsigned i = 0; i < sizeof caps / sizeof caps[0]; i++)
        printf("KVM_CAP_%-18s %d\n", caps[i].name, ioctl(fd, KVM_CHECK_EXTENSION, caps[i].cap));
    int vm = ioctl(fd, KVM_CREATE_VM, 0);
    printf("KVM_CREATE_VM            %d %s\n", vm, vm < 0 ? "(failed)" : "(a VM file descriptor)");
    close(vm); close(fd);
    return 0;
}
