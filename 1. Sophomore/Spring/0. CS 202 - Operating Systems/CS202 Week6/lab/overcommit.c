/* overcommit.c — which single anonymous mappings heuristic overcommit refuses, how much
 * it accepts in pieces, and, with any argument, how far malloc gets under RLIMIT_AS.
 *   gcc -O2 -Wall -Wextra -o overcommit overcommit.c
 *   ./overcommit                     ( ulimit -v 262144; ./overcommit limit )
 * CS 202 Week 6, L21 §4 and Lab 6 Parts B and C. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/resource.h>
static void meminfo(void) { FILE *f = fopen("/proc/meminfo", "r"); char l[256]; while (fgets(l, sizeof l, f)) if (strstr(l, "Commit")) printf("    %s", l); fclose(f); }
int main(int argc, char **argv)
{
    if (argc > 1 && argv[1][0]) {                        /* malloc until refused, under whatever RLIMIT_AS the shell set */
        struct rlimit rl; getrlimit(RLIMIT_AS, &rl);
        size_t n = 0; char *p;
        while ((p = malloc(1 << 20))) { p[0] = 1; n++; if (n > 100000) break; }
        printf("RLIMIT_AS %ld kB: malloc(1 MiB) succeeded %zu times, then errno %s\n", (long)(rl.rlim_cur / 1024), n, strerror(errno));
        return 0;
    }
    meminfo();
    static const int gib[] = { 4, 8, 11, 12, 16, 64, 1024 };
    for (int i = 0; i < 7; i++) {
        size_t sz = (size_t)gib[i] << 30;
        void *a = mmap(0, sz, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
        int e1 = errno;
        void *b = mmap(0, sz, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_NORESERVE, -1, 0);
        void *c = malloc(sz);
        printf("  %5d GiB: mmap %-8s  mmap NORESERVE %-8s  malloc %s\n", gib[i],
               a == MAP_FAILED ? strerror(e1) : "ok", b == MAP_FAILED ? "refused" : "ok", c ? "ok" : "refused");
        if (a != MAP_FAILED) munmap(a, sz);
        if (b != MAP_FAILED) munmap(b, sz);
        free(c);
    }
    /* many mappings that together exceed everything */
    size_t got = 0;
    for (int i = 0; i < 1000; i++) {
        if (mmap(0, 8UL << 30, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0) == MAP_FAILED) break;
        got += 8;
    }
    printf("  8 GiB mappings, kept: %zu GiB mapped before a refusal (or 8000 = none)\n", got);
    meminfo();
    return 0;
}
