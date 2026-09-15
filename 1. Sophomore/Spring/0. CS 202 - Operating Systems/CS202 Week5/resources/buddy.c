/* buddy.c — /proc/buddyinfo before and after touching 512 MiB of 4 KiB pages, and
 * after unmapping them; then 64 MiB paged out with MADV_PAGEOUT and read back.
 *   gcc -O2 -Wall -Wextra -o buddy buddy.c && ./buddy
 * CS 202 Week 5, L18 §6. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/mman.h>
#include <sys/resource.h>
static void buddy(const char *when)
{
    FILE *f = fopen("/proc/buddyinfo", "r"); char line[512];
    while (fgets(line, sizeof line, f)) if (strstr(line, "Normal") || strstr(line, "DMA32")) printf("%-22s %s", when, line + 7);
    fclose(f);
}
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }
int main(void)
{
    buddy("before");
    size_t N = 512UL << 20;
    char *p = mmap(0, N, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    madvise(p, N, MADV_NOHUGEPAGE);
    memset(p, 3, N);
    buddy("512 MiB touched");
    munmap(p, N);
    buddy("after munmap");

    /* major faults: page 64 MiB out, then read it back */
    size_t M = 64UL << 20;
    char *q = mmap(0, M, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    madvise(q, M, MADV_NOHUGEPAGE);
    for (size_t i = 0; i < M; i += 4096) q[i] = (char)(i >> 12) ^ 0x5a;   /* not zero pages, not identical */
    for (size_t i = 0; i < M; i++) if (i % 4096) q[i] = (char)i;
    double t0 = now();
    int r = madvise(q, M, MADV_PAGEOUT);
    double t1 = now();
    int pm = open("/proc/self/pagemap", O_RDONLY); uint64_t e; unsigned long sw = 0, pr = 0;
    for (size_t i = 0; i < M; i += 4096) { if (pread(pm, &e, 8, ((uintptr_t)q + i) / 4096 * 8) != 8) break; sw += e >> 62 & 1; pr += e >> 63 & 1; }
    printf("MADV_PAGEOUT %d in %.3f s: %lu swapped, %lu present\n", r, t1 - t0, sw, pr);
    struct rusage a, b; getrusage(RUSAGE_SELF, &a);
    unsigned long bad = 0;
    t0 = now();
    for (size_t i = 0; i < M; i += 4096) bad += q[i] != (char)((char)(i >> 12) ^ 0x5a);
    t1 = now();
    getrusage(RUSAGE_SELF, &b);
    printf("read back: %ld major, %ld minor faults in %.3f s (%.1f us per page), %lu wrong bytes\n",
           b.ru_majflt - a.ru_majflt, b.ru_minflt - a.ru_minflt, t1 - t0, (t1 - t0) * 1e6 / (M / 4096), bad);
    return 0;
}
