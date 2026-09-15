/* tlbcost.c — nanoseconds per random byte read over working sets of growing size,
 * backed by 4 KiB pages (THP refused) or by 2 MiB pages (THP requested).
 *   gcc -O2 -Wall -Wextra -o tlbcost tlbcost.c && taskset -c 2 ./tlbcost
 * CS 202 Week 5, L16 §5. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <sys/mman.h>

#define READS 20000000UL   /* each read is the first byte of a random page */

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

static long anon_huge_kb(void)
{
    FILE *f = fopen("/proc/self/smaps_rollup", "r");
    char line[256];
    long v = -1;
    while (f && fgets(line, sizeof line, f))
        if (!strncmp(line, "AnonHugePages:", 14)) v = atol(line + 14);
    if (f) fclose(f);
    return v;
}

static double run(size_t bytes, int huge, long *hugekb)
{
    size_t align = 2UL << 20;
    char *raw = mmap(0, bytes + align, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (raw == MAP_FAILED) { perror("mmap"); exit(1); }
    char *p = (char *)(((uintptr_t)raw + align - 1) & ~(align - 1));
    madvise(p, bytes, huge ? MADV_HUGEPAGE : MADV_NOHUGEPAGE);
    for (size_t i = 0; i < bytes; i += 4096) p[i] = (char)(i >> 12 | 1);
    *hugekb = anon_huge_kb();

    uint64_t x = 88172645463325252ULL, sum = 0;
    double t0 = now();
    for (unsigned long r = 0; r < READS; r++) {
        x ^= x << 13; x ^= x >> 7; x ^= x << 17;
        sum += (unsigned char)p[(x % bytes) & ~4095UL];
    }
    double t1 = now();
    munmap(raw, bytes + align);
    if (sum == 0) printf("(checksum zero)\n");
    return (t1 - t0) * 1e9 / READS;
}

int main(void)
{
    printf("%10s  %14s  %14s  %12s\n", "working set", "4 KiB pages", "2 MiB pages", "THP backed");
    static const size_t sizes[] = { 1, 4, 16, 64, 256, 1024, 2048 };
    for (size_t k = 0; k < sizeof sizes / sizeof sizes[0]; k++) {
        size_t mb = sizes[k];
        long k4, k2;
        double a = run(mb << 20, 0, &k4);
        double b = run(mb << 20, 1, &k2);
        printf("%7zu MiB  %11.2f ns  %11.2f ns  %9ld kB\n", mb, a, b, k2);
    }
    return 0;
}
