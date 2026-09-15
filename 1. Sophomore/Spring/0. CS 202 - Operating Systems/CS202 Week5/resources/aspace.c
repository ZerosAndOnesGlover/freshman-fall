/* aspace.c — where a program's code, heap and stack are; how high user space goes;
 * and a stack address split into x86-64's page-table indices.
 *   gcc -O2 -Wall -Wextra -o aspace aspace.c && ./aspace && ./aspace
 * CS 202 Week 5, L16 §1 and §6. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
int main(void)
{
    int local; char *h = malloc(16);
    printf("text  %p\nheap  %p\nstack %p\n", (void *)main, (void *)h, (void *)&local);
    void *hi = mmap((void *)(1UL << 56), 4096, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    printf("mmap hint 2^56 -> %p\n", hi);
    void *fx = mmap((void *)(1UL << 47), 4096, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED_NOREPLACE, -1, 0);
    printf("MAP_FIXED at 2^47 -> %p\n", fx);
    void *fx2 = mmap((void *)((1UL << 47) - 4096), 4096, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED_NOREPLACE, -1, 0);
    printf("MAP_FIXED at 2^47-4096 -> %p\n", fx2);
    unsigned long v = (unsigned long)&local;
    printf("stack address fields: PGD %lu PUD %lu PMD %lu PTE %lu offset %lu\n",
           v >> 39 & 511, v >> 30 & 511, v >> 21 & 511, v >> 12 & 511, v & 4095);
    return 0;
}
