/* int80.c: the same request, getpid, through two different doors.
 *
 *   gcc -O2 -Wall -Wextra -o int80 int80.c && ./int80
 *
 * CS 202 Week 0, L03 §5. */
#include <stdio.h>
#include <unistd.h>
long via_syscall(void), via_int80(void), via_int80_64num(void);
__asm__(".text\n"
        ".globl via_syscall, via_int80, via_int80_64num\n"
        "via_syscall:     mov $39, %eax; syscall;     ret\n"   /* x86-64 ABI: getpid = 39 */
        "via_int80:       mov $20, %eax; int $0x80;   ret\n"   /* i386 ABI:   getpid = 20 */
        "via_int80_64num: mov $39, %eax; int $0x80;   ret\n"); /* wrong table for the door */
int main(void)
{
    printf("getpid()                   = %d\n", getpid());
    printf("syscall, rax=39            = %ld\n", via_syscall());
    printf("int $0x80, eax=20          = %ld\n", via_int80());
    printf("int $0x80, eax=39          = %ld\n", via_int80_64num());
    return 0;
}
