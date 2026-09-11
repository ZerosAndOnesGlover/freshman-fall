/* worker.c: something for pm to manage.
 *
 *   ./worker hog          spin on the CPU forever
 *   ./worker tick         wake up every millisecond, do nothing, sleep again
 *   ./worker mem <MiB>    allocate and touch that much memory, then sleep
 *   ./worker exit <n>     sleep one second, exit with status n
 *   ./worker crash        sleep one second, dereference NULL
 *
 * CS 202 PS 1. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: worker hog|tick|mem N|exit N|crash\n"); return 2; }
    if (!strcmp(argv[1], "hog"))  { volatile unsigned long x = 0; for (;;) x++; }
    if (!strcmp(argv[1], "tick")) { for (;;) usleep(1000); }
    if (!strcmp(argv[1], "mem") && argc > 2) {
        size_t n = strtoul(argv[2], 0, 10) << 20;
        char *p = malloc(n);
        if (!p) return 1;
        /* Touch every page. A plain memset of memory that is never read again
         * is a dead store, and GCC at -O2 deletes it -- so read one byte back
         * through a volatile, which forces the writes to happen. */
        for (size_t i = 0; i < n; i += 4096)
            p[i] = 1;
        volatile char check = p[n - 4096];
        (void)check;
        for (;;) pause();
    }
    if (!strcmp(argv[1], "exit") && argc > 2) { sleep(1); return atoi(argv[2]); }
    if (!strcmp(argv[1], "crash")) { sleep(1); volatile char *z = 0; return *z; }
    fprintf(stderr, "worker: unknown mode %s\n", argv[1]);
    return 2;
}
