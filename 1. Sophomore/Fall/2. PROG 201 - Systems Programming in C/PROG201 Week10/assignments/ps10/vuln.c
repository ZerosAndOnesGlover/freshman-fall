/* PROG 201 -- the deliberately vulnerable ROP target.
 * Built  -fno-stack-protector -no-pie -z noexecstack, run under setarch -R.
 * Everything unsafe is unsafe on purpose; this binary only exists to be
 * attacked in the sandbox. */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/* The goal: call this with the right argument.  A plain jump is not enough --
 * you must control %rdi, which is what makes it a chain and not ret2win. */
void unlock(long key)
{
    if (key == 0xc0ffee) {
        puts("[unlock] correct key -- launching a shell");
        system("/bin/sh");
        _exit(0);
    }
    printf("[unlock] wrong key 0x%lx\n", key);
}

/* A gadget farm.  Real targets get their gadgets from libc; a hardened,
 * CET-compiled glibc has surprisingly few (see the build record), so this
 * teaching target supplies the two the chain needs.  Never reached by
 * ordinary control flow -- the `used` attribute stops the linker deleting it. */
__attribute__((used, naked)) void gadgets(void)
{
    __asm__ volatile(
        ".globl g_pop_rdi\n"
        "g_pop_rdi: pop %rdi; ret\n"
        ".globl g_ret\n"
        "g_ret: ret\n");
}

void vulnerable(void)
{
    char buf[64];
    puts("input> "); fflush(stdout);
    gets(buf);                          /* the bug */
    printf("you said: %s\n", buf);
}

int main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);
    vulnerable();
    puts("[main] returned normally");
    return 0;
}
