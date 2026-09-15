/* pagesim reference — page replacement on a reference string, for a range of frame counts.
 *   gcc -O2 -Wall -Wextra -o pagesim pagesim.c
 *   ./pagesim [-t TICK] POLICY FRAMES... < TRACE     one hex page number per line
 *   POLICY: fifo | lru | clock | aging | aging2 | opt | all
 * Prints, for each frame count, the number of faults. Loading a page into an empty
 * frame counts as a fault. -t sets the aging policies' interval (default 8 references).
 * CS 202 Week 6, PS 6. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static unsigned long *refs;
static size_t nrefs;

/* ---------------------------------------------------------------- provided: a hash set of pages in memory */

#define HBITS 20
#define HSIZE (1u << HBITS)
struct slot { unsigned long page; int frame; };   /* frame -1: empty; -2: deleted */
static struct slot table[HSIZE];

static unsigned h(unsigned long page) { return (unsigned)((page * 0x9E3779B97F4A7C15ul) >> (64 - HBITS)); }

static void hclear(void) { for (unsigned i = 0; i < HSIZE; i++) table[i].frame = -1; }

/* The frame holding PAGE, or -1. */
static int hfind(unsigned long page)
{
    for (unsigned i = h(page);; i = (i + 1) & (HSIZE - 1)) {
        if (table[i].frame == -1) return -1;
        if (table[i].frame >= 0 && table[i].page == page) return table[i].frame;
    }
}

/* Record that PAGE is in FRAME. PAGE must not be present. */
static void hput(unsigned long page, int frame)
{
    unsigned i = h(page);
    while (table[i].frame >= 0) i = (i + 1) & (HSIZE - 1);
    table[i].page = page;
    table[i].frame = frame;
}

/* Forget PAGE. */
static void hdel(unsigned long page)
{
    for (unsigned i = h(page);; i = (i + 1) & (HSIZE - 1)) {
        if (table[i].frame == -1) return;
        if (table[i].frame >= 0 && table[i].page == page) { table[i].frame = -2; return; }
    }
}

static unsigned long *frame_page;                 /* which page each frame holds */

/* ---------------------------------------------------------------- provided: FIFO */

/* Evict the page that has been in memory longest. */
static unsigned long fifo(int nframes)
{
    unsigned long faults = 0;
    int used = 0, hand = 0;
    for (size_t t = 0; t < nrefs; t++) {
        if (hfind(refs[t]) >= 0) continue;
        faults++;
        int f;
        if (used < nframes) f = used++;
        else { f = hand; hand = (hand + 1) % nframes; hdel(frame_page[f]); }
        frame_page[f] = refs[t];
        hput(refs[t], f);
    }
    return faults;
}

/* ---------------------------------------------------------------- Q1: LRU */

/* Evict the page whose most recent reference is oldest. Fill empty frames in order. */
static unsigned long lru(int nframes)
{
    unsigned long faults = 0;
    int used = 0;
    size_t *last = calloc((size_t)nframes, sizeof *last);
    for (size_t t = 0; t < nrefs; t++) {
        int f = hfind(refs[t]);
        if (f >= 0) { last[f] = t; continue; }
        faults++;
        if (used < nframes) f = used++;
        else {
            f = 0;
            for (int i = 1; i < nframes; i++) if (last[i] < last[f]) f = i;
            hdel(frame_page[f]);
        }
        frame_page[f] = refs[t];
        last[f] = t;
        hput(refs[t], f);
    }
    free(last);
    return faults;
}

/* ---------------------------------------------------------------- Q1: Clock */

/* Frames in a circle, each with a reference bit set on every reference and on loading.
 * Empty frames are filled in order without moving the hand. Once all are full, a fault
 * moves the hand: a frame with its bit set has the bit cleared and is passed; the first
 * frame with its bit clear is evicted, and the hand stops on the frame after it. */
static unsigned long clock_policy(int nframes)
{
    unsigned long faults = 0;
    int used = 0, hand = 0;
    unsigned char *ref = calloc((size_t)nframes, 1);
    for (size_t t = 0; t < nrefs; t++) {
        int f = hfind(refs[t]);
        if (f >= 0) { ref[f] = 1; continue; }
        faults++;
        if (used < nframes) f = used++;
        else {
            while (ref[hand]) { ref[hand] = 0; hand = (hand + 1) % nframes; }
            f = hand;
            hand = (hand + 1) % nframes;
            hdel(frame_page[f]);
        }
        frame_page[f] = refs[t];
        ref[f] = 1;
        hput(refs[t], f);
    }
    free(ref);
    return faults;
}

/* ---------------------------------------------------------------- Q5: aging */

/* Each frame has an 8-bit counter and a reference bit, set on every reference and on
 * loading. Before processing reference t, if t > 0 and t is a multiple of TICK, every
 * occupied frame's counter is shifted right one place with its reference bit copied into
 * the top bit, and the bit is cleared. A new page's counter starts at 0. On a fault with
 * no empty frame, evict the frame with the smallest counter — the lowest-numbered frame
 * among equals. aging2 is identical except that it compares (reference bit, counter)
 * as one 9-bit number, the reference bit most significant. */
static int tick = 8;

static unsigned long aging_common(int nframes, int refbit_first)
{
    unsigned long faults = 0;
    int used = 0;
    unsigned char *counter = calloc((size_t)nframes, 1), *ref = calloc((size_t)nframes, 1);
    for (size_t t = 0; t < nrefs; t++) {
        if (t > 0 && t % (size_t)tick == 0)
            for (int i = 0; i < used; i++) {
                counter[i] = (unsigned char)(counter[i] >> 1 | ref[i] << 7);
                ref[i] = 0;
            }
        int f = hfind(refs[t]);
        if (f >= 0) { ref[f] = 1; continue; }
        faults++;
        if (used < nframes) f = used++;
        else {
            f = 0;
            for (int i = 1; i < nframes; i++) {
                int ki = refbit_first ? ref[i] << 8 | counter[i] : counter[i];
                int kf = refbit_first ? ref[f] << 8 | counter[f] : counter[f];
                if (ki < kf) f = i;
            }
            hdel(frame_page[f]);
        }
        frame_page[f] = refs[t];
        counter[f] = 0;
        ref[f] = 1;
        hput(refs[t], f);
    }
    free(counter);
    free(ref);
    return faults;
}

static unsigned long aging(int nframes) { return aging_common(nframes, 0); }
static unsigned long aging2(int nframes) { return aging_common(nframes, 1); }

/* ---------------------------------------------------------------- provided: OPT */

/* Evict the page whose next reference is furthest away (never counts as furthest).
 * next[t] is the index of the next reference to refs[t] after t, or nrefs. */
static size_t *next;

static void build_next(void)
{
    next = malloc(nrefs * sizeof *next);
    hclear();                                     /* here the table maps page -> latest index seen */
    for (size_t t = nrefs; t-- > 0;) {
        int f = hfind(refs[t]);
        next[t] = f >= 0 ? (size_t)f : nrefs;
        if (f >= 0) hdel(refs[t]);
        hput(refs[t], (int)t);
    }
}

static unsigned long opt(int nframes)
{
    unsigned long faults = 0;
    int used = 0;
    size_t *nextuse = malloc((size_t)nframes * sizeof *nextuse);
    for (size_t t = 0; t < nrefs; t++) {
        int f = hfind(refs[t]);
        if (f >= 0) { nextuse[f] = next[t]; continue; }
        faults++;
        if (used < nframes) f = used++;
        else {
            f = 0;
            for (int i = 1; i < nframes; i++) if (nextuse[i] > nextuse[f]) f = i;
            hdel(frame_page[f]);
        }
        frame_page[f] = refs[t];
        nextuse[f] = next[t];
        hput(refs[t], f);
    }
    free(nextuse);
    return faults;
}

/* ---------------------------------------------------------------- provided: the driver */

static const struct { const char *name; unsigned long (*run)(int); } policies[] = {
    { "fifo", fifo }, { "lru", lru }, { "clock", clock_policy },
    { "aging", aging }, { "aging2", aging2 }, { "opt", opt },
};
#define NPOLICIES (int)(sizeof policies / sizeof policies[0])

int main(int argc, char **argv)
{
    if (argc > 2 && !strcmp(argv[1], "-t")) {
        tick = atoi(argv[2]);
        argv += 2;
        argc -= 2;
    }
    int which = -2;                               /* -1: all */
    if (argc >= 2) {
        if (!strcmp(argv[1], "all")) which = -1;
        for (int i = 0; i < NPOLICIES; i++) if (!strcmp(argv[1], policies[i].name)) which = i;
    }
    if (argc < 3 || which == -2 || tick < 1) {
        fprintf(stderr, "usage: %s [-t TICK] fifo|lru|clock|aging|aging2|opt|all FRAMES... < TRACE\n", argv[0]);
        return 1;
    }
    int maxframes = 0;
    for (int i = 2; i < argc; i++) {
        int n = atoi(argv[i]);
        if (n < 1 || n > (int)(HSIZE / 4)) { fprintf(stderr, "frames must be 1..%u\n", HSIZE / 4); return 1; }
        if (n > maxframes) maxframes = n;
    }

    size_t cap = 1 << 20;
    refs = malloc(cap * sizeof *refs);
    unsigned long page;
    while (scanf("%lx", &page) == 1) {
        if (nrefs == cap) refs = realloc(refs, (cap *= 2) * sizeof *refs);
        refs[nrefs++] = page;
    }
    frame_page = malloc((size_t)maxframes * sizeof *frame_page);

    hclear();
    size_t distinct = 0;
    for (size_t t = 0; t < nrefs; t++) if (hfind(refs[t]) < 0) { hput(refs[t], 0); distinct++; }
    if (distinct > HSIZE / 4) { fprintf(stderr, "too many distinct pages (%zu)\n", distinct); return 1; }
    printf("%zu references, %zu distinct pages\n", nrefs, distinct);

    if (which == -1 || !strcmp(policies[which].name, "opt")) build_next();
    printf("%8s", "frames");
    for (int p = 0; p < NPOLICIES; p++) if (which == -1 || which == p) printf(" %8s", policies[p].name);
    printf("\n");
    for (int i = 2; i < argc; i++) {
        int n = atoi(argv[i]);
        printf("%8d", n);
        for (int p = 0; p < NPOLICIES; p++)
            if (which == -1 || which == p) { hclear(); printf(" %8lu", policies[p].run(n)); }
        printf("\n");
    }
    return 0;
}
