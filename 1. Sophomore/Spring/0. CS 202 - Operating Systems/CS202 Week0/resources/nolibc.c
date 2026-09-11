/* nolibc.c: a program with no C library at all, and two system calls made by hand.
 *
 *   gcc -O2 -static -nostdlib -fno-stack-protector -o nolibc nolibc.c
 *   strace ./nolibc
 */
__asm__(
    ".section .rodata\n"
    "msg:    .ascii \"hello, with no libc\\n\"\n"
    "        .set len, . - msg\n"
    ".text\n"
    ".globl _start\n"
    "_start:\n"
    "        mov  $1, %eax\n"          /* rax = 1: write(2)      */
    "        mov  $1, %edi\n"          /* rdi = fd 1             */
    "        lea  msg(%rip), %rsi\n"   /* rsi = buffer           */
    "        mov  $len, %edx\n"        /* rdx = length           */
    "        syscall\n"
    "        mov  $60, %eax\n"         /* rax = 60: exit(2)      */
    "        xor  %edi, %edi\n"        /* rdi = status 0         */
    "        syscall\n");
