/* gentrace.c — a page reference string with locality: PHASES phases of LENGTH references
 * each; in every phase a working set of WSS pages is drawn from TOTAL pages, and each
 * reference is to the working set with probability P percent, otherwise to any page.
 *   gcc -O2 -Wall -Wextra -o gentrace gentrace.c
 *   ./gentrace TOTAL WSS P PHASES LENGTH SEED > trace.txt
 * CS 202 Week 6, PS 6. */
#include <stdio.h>
#include <stdlib.h>

static unsigned long state;
static unsigned long rnd(void)
{
    state ^= state << 13;
    state ^= state >> 7;
    state ^= state << 17;
    return state;
}

int main(int argc, char **argv)
{
    if (argc != 7) {
        fprintf(stderr, "usage: %s TOTAL WSS P PHASES LENGTH SEED\n", argv[0]);
        return 1;
    }
    unsigned long total = strtoul(argv[1], 0, 10), wss = strtoul(argv[2], 0, 10);
    unsigned long p = strtoul(argv[3], 0, 10), phases = strtoul(argv[4], 0, 10);
    unsigned long length = strtoul(argv[5], 0, 10);
    state = strtoul(argv[6], 0, 10) * 2654435761UL + 1;
    if (!total || !wss || wss > total || p > 100) {
        fprintf(stderr, "need 0 < WSS <= TOTAL and P <= 100\n");
        return 1;
    }
    unsigned long *ws = malloc(wss * sizeof *ws);
    for (unsigned long ph = 0; ph < phases; ph++) {
        unsigned long start = rnd() % total;             /* a contiguous run of pages, wrapping */
        for (unsigned long i = 0; i < wss; i++) ws[i] = (start + i) % total;
        for (unsigned long r = 0; r < length; r++) {
            unsigned long page = rnd() % 100 < p ? ws[rnd() % wss] : rnd() % total;
            printf("%lx\n", page);
        }
    }
    free(ws);
    return 0;
}
