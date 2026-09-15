/* faultcost.c — what mapping, first-touching and re-touching a gigabyte cost, in
 * time and in page-table memory; and the tables for 64 pages a gigabyte apart.
 *   gcc -O2 -Wall -Wextra -o faultcost faultcost.c && taskset -c 2 ./faultcost
 * CS 202 Week 5, L16 §7 and L18 §1. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/resource.h>

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }
static long minflt(void) { struct rusage r; getrusage(RUSAGE_SELF, &r); return r.ru_minflt; }
static long status_kb(const char *key)
{
    FILE *f = fopen("/proc/self/status", "r"); char line[256]; long v = -1;
    while (fgets(line, sizeof line, f)) if (!strncmp(line, key, strlen(key))) v = atol(line + strlen(key) + 1);
    fclose(f); return v;
}

int main(void)
{
    const size_t N = 1UL << 30;                     /* 1 GiB */
    printf("before mmap:        VmRSS %6ld kB  VmPTE %4ld kB\n", status_kb("VmRSS"), status_kb("VmPTE"));
    char *p = mmap(0, N, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    madvise(p, N, MADV_NOHUGEPAGE);
    printf("after 1 GiB mmap:   VmRSS %6ld kB  VmPTE %4ld kB  VmSize %ld kB\n", status_kb("VmRSS"), status_kb("VmPTE"), status_kb("VmSize"));
    long f0 = minflt(); double t0 = now();
    for (size_t i = 0; i < N; i += 4096) p[i] = 1;
    double t1 = now(); long f1 = minflt();
    printf("touch 262144 pages: %ld faults, %.3f s, %.0f ns per fault\n", f1 - f0, t1 - t0, (t1 - t0) * 1e9 / (f1 - f0));
    printf("after touching:     VmRSS %6ld kB  VmPTE %4ld kB\n", status_kb("VmRSS"), status_kb("VmPTE"));
    t0 = now();
    for (size_t i = 0; i < N; i += 4096) p[i] = 2;
    t1 = now();
    printf("second pass:        %ld faults, %.3f s, %.1f ns per page\n", minflt() - f1, t1 - t0, (t1 - t0) * 1e9 / (N / 4096));
    munmap(p, N);

    /* sparse: one page in every 1 GiB across 64 GiB of address space */
    const size_t S = 64UL << 30;
    char *q = mmap(0, S, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_NORESERVE, -1, 0);
    long pte0 = status_kb("VmPTE");
    for (size_t i = 0; i < S; i += 1UL << 30) q[i] = 1;
    printf("64 pages, 1 GiB apart:              VmPTE %ld -> %ld kB\n", pte0, status_kb("VmPTE"));
    return 0;
}
