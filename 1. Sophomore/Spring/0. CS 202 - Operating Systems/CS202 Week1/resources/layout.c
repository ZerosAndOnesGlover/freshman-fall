/* layout.c: where each kind of memory lives in this process's address space. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/auxv.h>
#include <unistd.h>

int initialised = 42;          /* .data */
int uninitialised;             /* .bss  */
const char *literal = "hello"; /* the pointer is in .data; the string in .rodata */

int main(void)
{
    int local = 0;
    char *small = malloc(64);
    char *large = malloc(64 << 20);
    printf("%-26s %18p\n", "main (text)", (void *)main);
    printf("%-26s %18p\n", "string literal (rodata)", (void *)literal);
    printf("%-26s %18p\n", "initialised global (data)", (void *)&initialised);
    printf("%-26s %18p\n", "uninitialised global (bss)", (void *)&uninitialised);
    printf("%-26s %18p\n", "malloc(64) (heap)", (void *)small);
    printf("%-26s %18p\n", "malloc(64 MiB) (mmap)", (void *)large);
    printf("%-26s %18p\n", "printf (libc)", (void *)printf);
    printf("%-26s %18p\n", "vDSO", (void *)getauxval(AT_SYSINFO_EHDR));
    printf("%-26s %18p\n", "local variable (stack)", (void *)&local);
    if (getenv("MAPS")) {
        char cmd[64];
        snprintf(cmd, sizeof cmd, "cat /proc/%d/maps", (int)getpid());
        fflush(stdout);
        if (system(cmd) != 0) return 1;
    }
    free(small); free(large);
    return local;
}
