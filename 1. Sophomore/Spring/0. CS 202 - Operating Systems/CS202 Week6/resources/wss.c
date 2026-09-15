/* wss.c — a process's working set, measured on itself: write 1 to /proc/self/clear_refs
 * to clear every page's referenced bit, then read Referenced in /proc/self/smaps_rollup
 * after an interval of work.
 *   gcc -O2 -Wall -Wextra -o wss wss.c && ./wss
 * CS 202 Week 6, L21 §1. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
static long field(const char *key) { FILE *f = fopen("/proc/self/smaps_rollup", "r"); char l[256]; long v = -1; while (fgets(l, sizeof l, f)) if (!strncmp(l, key, strlen(key))) v = atol(l + strlen(key)); fclose(f); return v; }
static void clear(void) { int fd = open("/proc/self/clear_refs", O_WRONLY); if (fd < 0 || write(fd, "1", 1) != 1) perror("clear_refs"); close(fd); }
int main(void)
{
    size_t N = 256UL << 20;
    char *p = mmap(0, N, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    madvise(p, N, MADV_NOHUGEPAGE);
    memset(p, 1, N);
    printf("touched 256 MiB:            Rss %7ld kB  Referenced %7ld kB\n", field("Rss:"), field("Referenced:"));
    clear();
    printf("after clear_refs 1:         Rss %7ld kB  Referenced %7ld kB\n", field("Rss:"), field("Referenced:"));
    volatile unsigned long s = 0;
    for (size_t i = 0; i < (64UL << 20); i += 4096) s += p[i];
    printf("read the first 64 MiB:      Rss %7ld kB  Referenced %7ld kB\n", field("Rss:"), field("Referenced:"));
    clear();
    for (size_t i = 128UL << 20; i < (144UL << 20); i += 4096) p[i] = 2;
    printf("cleared, wrote 16 MiB:      Rss %7ld kB  Referenced %7ld kB\n", field("Rss:"), field("Referenced:"));
    (void)s;
    return 0;
}
