/* oomscore.c — /proc/self/oom_score as this process changes its oom_score_adj, and as
 * it touches one, two and three GiB. Needs 3 GiB free: run it alone.
 *   gcc -O2 -Wall -Wextra -o oomscore oomscore.c && ./oomscore
 * CS 202 Week 6, L21 §5 and Lab 6 Part E. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
static long rd(const char *p) { FILE *f = fopen(p, "r"); long v = -99999; if (f) { if (fscanf(f, "%ld", &v) != 1) v = -99998; fclose(f); } return v; }
static int setadj(int a) { FILE *f = fopen("/proc/self/oom_score_adj", "w"); if (!f) return -1; int r = fprintf(f, "%d", a); return fclose(f) == 0 && r > 0 ? 0 : -1; }
static long rss_kb(void) { FILE *f = fopen("/proc/self/status", "r"); char l[256]; long v = -1; while (fgets(l, sizeof l, f)) if (!strncmp(l, "VmRSS:", 6)) v = atol(l + 6); fclose(f); return v; }
int main(void)
{
    long total_kb = 0; FILE *m = fopen("/proc/meminfo", "r"); char l[256];
    long mem = 0, swap = 0;
    while (fgets(l, sizeof l, m)) { if (!strncmp(l, "MemTotal:", 9)) mem = atol(l + 9); if (!strncmp(l, "SwapTotal:", 10)) swap = atol(l + 10); }
    fclose(m); total_kb = mem + swap;
    printf("MemTotal %ld kB + SwapTotal %ld kB = %ld kB\n", mem, swap, total_kb);
    printf("inherited adj %ld, score %ld\n", rd("/proc/self/oom_score_adj"), rd("/proc/self/oom_score"));
    static const int adjs[] = { 1000, 500, 200, 100, 0, -1, -100 };
    for (int i = 0; i < 7; i++) {
        int r = setadj(adjs[i]);
        printf("  set adj %5d: %-8s adj now %5ld  score %5ld\n", adjs[i], r ? "REFUSED" : "ok", rd("/proc/self/oom_score_adj"), rd("/proc/self/oom_score"));
    }
    setadj(0);
    for (int gb = 0; gb <= 3; gb++) {
        if (gb) { char *p = mmap(0, 1UL << 30, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0); memset(p, 1, 1UL << 30); }
        printf("  adj 0, RSS %8ld kB (%.1f%% of RAM+swap): score %ld\n", rss_kb(), 100.0 * rss_kb() / total_kb, rd("/proc/self/oom_score"));
    }
    setadj(300);
    printf("  adj 300, RSS %8ld kB: score %ld\n", rss_kb(), rd("/proc/self/oom_score"));
    return 0;
}
