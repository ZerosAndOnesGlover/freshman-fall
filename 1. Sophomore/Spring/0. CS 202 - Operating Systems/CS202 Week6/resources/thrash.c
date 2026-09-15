/* thrash.c — fill SIZE MiB with data, then make random single-byte reads for SECONDS,
 * either uniformly over all of it or with most reads in a hot region, and report
 * throughput, page faults, and the memory pressure this process's cgroup recorded.
 * Run it under a memory limit smaller than SIZE:
 *   gcc -O2 -Wall -Wextra -o thrash thrash.c
 *   systemd-run --user --scope -p MemoryMax=192M ./thrash 256 4 uniform
 *   systemd-run --user --scope -p MemoryMax=192M ./thrash 256 4 hot
 * Keep runs short: systemd-oomd watches the pressure of your whole session.
 * CS 202 Week 6, L21 §2. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/mman.h>
#include <sys/resource.h>

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

/* "some" and "full" totals, in microseconds, from this cgroup's memory.pressure */
static void pressure(long long *some, long long *full)
{
    char path[512] = "/sys/fs/cgroup", cg[400] = "";
    FILE *f = fopen("/proc/self/cgroup", "r");
    if (f && fscanf(f, "0::%399s", cg) == 1) strncat(path, cg, sizeof path - strlen(path) - 20);
    if (f) fclose(f);
    strcat(path, "/memory.pressure");
    *some = *full = -1;
    f = fopen(path, "r");
    if (!f) return;
    char line[256];
    while (fgets(line, sizeof line, f)) {
        char *t = strstr(line, "total=");
        if (!t) continue;
        if (!strncmp(line, "some", 4)) *some = atoll(t + 6);
        if (!strncmp(line, "full", 4)) *full = atoll(t + 6);
    }
    fclose(f);
}

int main(int argc, char **argv)
{
    if (argc < 4) {
        fprintf(stderr, "usage: %s SIZE_MIB SECONDS uniform|hot\n", argv[0]);
        return 1;
    }
    size_t pages = (size_t)atol(argv[1]) * 256;
    double seconds = atof(argv[2]);
    int hot = !strcmp(argv[3], "hot");
    size_t hotpages = pages / 8;                      /* hot: 90% of reads in the first eighth */

    char *p = mmap(0, pages * 4096, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (p == MAP_FAILED) { perror("mmap"); return 1; }
    madvise(p, pages * 4096, MADV_NOHUGEPAGE);
    double t0 = now();
    for (size_t i = 0; i < pages; i++) memset(p + i * 4096, (int)(i % 251) + 1, 4096);
    double t1 = now();

    struct rusage r0, r1;
    long long s0, f0, s1, f1;
    getrusage(RUSAGE_SELF, &r0);
    pressure(&s0, &f0);
    unsigned long x = 88172645463325252UL, reads = 0, bad = 0;
    double t2 = now(), end = t2 + seconds;
    while (1) {
        for (int k = 0; k < 256; k++) {
            x ^= x << 13; x ^= x >> 7; x ^= x << 17;
            size_t pg = hot && (x >> 60) < 15 ? (x >> 8) % hotpages
                      : hot ? hotpages + (x >> 8) % (pages - hotpages)
                      : (x >> 8) % pages;
            bad += (unsigned char)p[pg * 4096 + (x & 4095)] != (unsigned char)((pg % 251) + 1);
            reads++;
        }
        if (now() >= end) break;
    }
    double t3 = now();
    getrusage(RUSAGE_SELF, &r1);
    pressure(&s1, &f1);
    printf("%4s MiB %-7s fill %6.2f s | %11.0f reads/s  major %7ld  minor %7ld  wrong %lu | pressure some %5.1f%% full %5.1f%%\n",
           argv[1], argv[3], t1 - t0, reads / (t3 - t2), r1.ru_majflt - r0.ru_majflt, r1.ru_minflt - r0.ru_minflt, bad,
           s0 < 0 ? -1.0 : 100.0 * (s1 - s0) / ((t3 - t2) * 1e6), f0 < 0 ? -1.0 : 100.0 * (f1 - f0) / ((t3 - t2) * 1e6));
    return 0;
}
