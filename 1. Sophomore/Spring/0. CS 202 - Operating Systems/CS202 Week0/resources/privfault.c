/* privfault.c: execute one instruction per child process, in ring 3, and
 * report what the kernel did about it.
 *
 *   gcc -O2 -Wall -Wextra -o privfault privfault.c && ./privfault
 *
 * CS 202 Week 0, L02 §3. */
#define _GNU_SOURCE
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

void do_cli(void), do_hlt(void), do_in(void), do_out(void), do_rdmsr(void),
     do_cr3(void), do_sgdt(void), do_rdtsc(void), do_cpuid(void);
unsigned long get_cs(void);
extern unsigned char gdtr[10];

__asm__(
    ".text\n"
    ".globl do_cli, do_hlt, do_in, do_out, do_rdmsr, do_cr3, do_sgdt, do_rdtsc, do_cpuid, get_cs\n"
    "do_cli:   cli; ret\n"
    "do_hlt:   hlt; ret\n"
    "do_in:    mov $0x3f8, %dx; inb (%dx), %al; ret\n"
    "do_out:   mov $0x3f8, %dx; mov $72, %al; outb %al, (%dx); ret\n"
    "do_rdmsr: mov $0x10, %ecx; rdmsr; ret\n"
    "do_cr3:   mov %cr3, %rax; ret\n"
    "do_sgdt:  sgdt gdtr(%rip); ret\n"
    "do_rdtsc: rdtsc; ret\n"
    "do_cpuid: push %rbx; xor %eax, %eax; cpuid; pop %rbx; ret\n"
    "get_cs:   xor %eax, %eax; mov %cs, %ax; ret\n"
    ".data\n"
    ".globl gdtr\n"
    "gdtr: .zero 10\n"
    ".text\n");

static const struct { const char *name; void (*fn)(void); } tests[] = {
    { "cli      disable interrupts",   do_cli   },
    { "hlt      halt the CPU",         do_hlt   },
    { "inb      read I/O port 0x3f8",  do_in    },
    { "outb     write I/O port 0x3f8", do_out   },
    { "rdmsr    read the TSC MSR",     do_rdmsr },
    { "mov cr3  read page-table root", do_cr3   },
    { "sgdt     read the GDT register", do_sgdt },
    { "rdtsc    read the timestamp",   do_rdtsc },
    { "cpuid    identify the CPU",     do_cpuid },
};

int main(void)
{
    printf("CS = 0x%lx, so CPL = %lu\n\n", get_cs(), get_cs() & 3);
    for (size_t i = 0; i < sizeof tests / sizeof tests[0]; i++) {
        fflush(stdout);                      /* PROG 201 L01 §6: flush before fork */
        pid_t p = fork();
        if (p == 0) {
            tests[i].fn();                   /* if this faults, nothing below runs */
            printf("%-34s -> ran", tests[i].name);
            if (tests[i].fn == do_sgdt) {
                unsigned long base;
                memcpy(&base, gdtr + 2, sizeof base);
                printf(", GDT base = 0x%lx", base);
            }
            printf("\n");
            fflush(stdout);
            _exit(0);
        }
        int st;
        waitpid(p, &st, 0);
        if (WIFSIGNALED(st))
            printf("%-34s -> killed by SIG%s\n", tests[i].name, sigabbrev_np(WTERMSIG(st)));
    }
    return 0;
}
