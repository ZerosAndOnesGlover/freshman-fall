/* pt2.c — a two-level x86 page table (10/10/12) whose page directory and
 * page tables live in simulated physical frames, with 4 MiB superpages and a small
 * TLB per CPU.
 *   gcc -O2 -Wall -Wextra -o pt2 pt2.c && ./pt2 < traces/basic.txt
 *
 * Commands, one per line; numbers in hex unless marked (dec); # starts a comment.
 *   map VA PA PERM             map one 4 KiB page; PERM is any of w u, or -
 *   mapr VA PA N(dec) PERM     map N pages from VA to PA
 *   mapbig VA PA PERM          map the 4 MiB superpage containing VA        (Q5)
 *   unmap VA  /  unmapr VA N(dec)
 *   read VA | write VA | uread VA | uwrite VA        translate one access and print it
 *   seq VA NBYTES(dec) STEP(dec)      uread VA, VA+STEP, ... below VA+NBYTES; print totals
 *   rand VA NPAGES(dec) COUNT(dec) SEED(dec)          uread COUNT random pages; print totals
 *   matrix VA N(dec) row|col   uread every element of an N x N array of 8-byte values
 *   cpu N(dec)                 later accesses use that CPU's TLB (0 or 1)
 *   flush                      empty the current CPU's TLB (a context switch without PCIDs)
 *   stats                      page-table frames in use, and each CPU's TLB hits and misses
 *   reset                      zero the TLB counters
 * Run with --no-shootdown to invalidate only the current CPU's TLB on unmap.
 * CS 202 Week 5, PS 5. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define NFRAMES   4096                   /* 16 MiB of simulated physical memory for tables */
#define PGSIZE    4096
#define PTE_P     0x001
#define PTE_W     0x002
#define PTE_U     0x004
#define PTE_PS    0x080                  /* in a directory entry: a 4 MiB superpage */
#define PDX(va)   (((va) >> 22) & 0x3FF)
#define PTX(va)   (((va) >> 12) & 0x3FF)
#define PTE_ADDR(e) ((e) & ~0xFFFu)
#define BIG_ADDR(e) ((e) & ~0x3FFFFFu)
#define TLBSIZE   8
#define NCPU      2

enum { OK, NOTPRESENT, NOTWRITABLE, NOTUSER };
static const char *why[] = { "", "FAULT not present", "FAULT not writable", "FAULT not user" };

/* ---------------------------------------------------------------- provided: frames */

static uint32_t frames[NFRAMES][1024];   /* each frame holds 1024 32-bit entries */
static int inuse[NFRAMES];
static int ptframes;                     /* frames now holding the directory or a table */
static uint32_t pgdir;                   /* physical address of the page directory */

/* A zeroed frame, by physical address. Frame 0 is never handed out. */
static uint32_t palloc(void)
{
    for (int f = 1; f < NFRAMES; f++)
        if (!inuse[f]) {
            inuse[f] = 1;
            memset(frames[f], 0, sizeof frames[f]);
            ptframes++;
            return (uint32_t)f * PGSIZE;
        }
    fprintf(stderr, "out of frames\n");
    exit(1);
}

static void pfree(uint32_t pa)
{
    inuse[pa / PGSIZE] = 0;
    ptframes--;
}

/* Entry IDX of the table in the frame at physical address PA. */
static uint32_t *entry(uint32_t pa, unsigned idx)
{
    return &frames[pa / PGSIZE][idx];
}

/* ---------------------------------------------------------------- provided: the TLB */

/* A cached translation. For a 4 KiB page, vpn is va >> 12; for a superpage (big = 1),
 * it is va >> 22. pte is the page-table entry, or for a superpage the directory entry. */
struct tlbent { int valid, big; uint32_t vpn, pte; unsigned long used; };
static struct tlbent tlb[NCPU][TLBSIZE];
static unsigned long now, hits[NCPU], misses[NCPU];
static int cpu;
static int shootdown = 1;

/* ---------------------------------------------------------------- Q1: the page table */

/* The address of VA's page-table entry. If VA's page table does not exist, allocate
 * one when ALLOC is set (directory entry: present, writable, user) and otherwise
 * return 0. Also return 0 if VA lies in a superpage. */
static uint32_t *walk(uint32_t va, int alloc)
{
    /* TODO (Q1) */
    (void)va;
    (void)alloc;
    return 0;
}

/* Map the page containing VA to the frame containing PA with PERM.
 * -1 if that page is already mapped, or lies in a superpage. */
static int map(uint32_t va, uint32_t pa, uint32_t perm)
{
    /* TODO (Q1) */
    (void)va;
    (void)pa;
    (void)perm;
    return -1;
}

/* ---------------------------------------------------------------- Q5: superpages */

/* Map the 4 MiB region containing VA to the 4 MiB of frames containing PA, with one
 * directory entry. -1 if the directory entry is already present (as a superpage or
 * because a page table exists there). */
static int map_big(uint32_t va, uint32_t pa, uint32_t perm)
{
    /* TODO (Q5) */
    (void)va;
    (void)pa;
    (void)perm;
    return -1;
}

/* ---------------------------------------------------------------- Q1 and Q4: unmapping */

/* Remove the 4 KiB page VPN from CPU C's TLB. */
static void tlb_invalidate(int c, uint32_t vpn)
{
    /* TODO (Q1) */
    (void)c;
    (void)vpn;
}

/* Unmap VA's 4 KiB page. -2 if VA lies in a superpage; -1 if the page was not mapped;
 * 1 if its page table became empty and was freed; 0 otherwise. Invalidate the
 * translation in every CPU's TLB, or only the current CPU's when shootdown is 0. */
static int unmap(uint32_t va)
{
    /* TODO (Q1) */
    (void)va;
    (void)walk;
    (void)entry;
    (void)pfree;
    (void)tlb_invalidate;
    return -1;
}

/* ---------------------------------------------------------------- Q1, Q3, Q5: translation */

/* Translate VA for a WRITE or not, from USER mode or not. Look in the current CPU's TLB
 * first; on a hit count it and use the cached entry. On a miss count it and walk: if
 * the directory entry is a superpage, that entry is the translation; otherwise read
 * the page-table entry. If present, cache it — in an invalid slot if there is one,
 * otherwise in place of the least recently used — then check permissions and set *PA. */
static int translate(uint32_t va, int write, int user, uint32_t *pa)
{
    /* TODO (Q1, Q3, Q5) */
    (void)va;
    (void)write;
    (void)user;
    (void)pa;
    (void)now;
    (void)shootdown;
    return NOTPRESENT;
}

/* ---------------------------------------------------------------- provided: the driver */

static uint32_t perms(const char *s)
{
    return (strchr(s, 'w') ? PTE_W : 0) | (strchr(s, 'u') ? PTE_U : 0);
}

static uint32_t xorshift(uint32_t *s)
{
    *s ^= *s << 13;
    *s ^= *s >> 17;
    *s ^= *s << 5;
    return *s;
}

static unsigned long bulk_faults;
static void bulk(uint32_t va)
{
    uint32_t pa;
    if (translate(va, 0, 1, &pa) != OK) bulk_faults++;
}

int main(int argc, char **argv)
{
    if (argc > 1 && !strcmp(argv[1], "--no-shootdown")) shootdown = 0;
    char line[256], cmd[32], s[16];
    uint32_t va, pa;
    unsigned long n, m, seed;
    pgdir = palloc();
    while (fgets(line, sizeof line, stdin)) {
        char *hash = strchr(line, '#');
        if (hash) *hash = 0;
        if (sscanf(line, "%31s", cmd) != 1) continue;
        if (!strcmp(cmd, "map") && sscanf(line, "%*s %x %x %15s", &va, &pa, s) == 3) {
            printf("map     %08x -> %08x%s\n", va, pa, map(va, pa, perms(s)) ? "  ERROR already mapped" : "");
        } else if (!strcmp(cmd, "mapr") && sscanf(line, "%*s %x %x %lu %15s", &va, &pa, &n, s) == 4) {
            unsigned long bad = 0;
            for (unsigned long i = 0; i < n; i++) bad += map(va + i * PGSIZE, pa + i * PGSIZE, perms(s)) != 0;
            printf("mapr    %08x -> %08x  %lu pages%s\n", va, pa, n, bad ? "  ERROR some already mapped" : "");
        } else if (!strcmp(cmd, "mapbig") && sscanf(line, "%*s %x %x %15s", &va, &pa, s) == 3) {
            printf("mapbig  %08x -> %08x%s\n", va, pa, map_big(va, pa, perms(s)) ? "  ERROR already mapped" : "");
        } else if (!strcmp(cmd, "unmap") && sscanf(line, "%*s %x", &va) == 1) {
            int r = unmap(va);
            printf("unmap   %08x%s\n", va, r == -2 ? "  ERROR in a superpage" : r < 0 ? "  ERROR not mapped" :
                                           r ? "  (page table freed)" : "");
        } else if (!strcmp(cmd, "unmapr") && sscanf(line, "%*s %x %lu", &va, &n) == 2) {
            unsigned long freed = 0, bad = 0;
            for (unsigned long i = 0; i < n; i++) {
                int r = unmap(va + i * PGSIZE);
                bad += r < 0;
                freed += r > 0;
            }
            printf("unmapr  %08x  %lu pages, %lu page tables freed%s\n", va, n, freed, bad ? "  ERROR some not mapped" : "");
        } else if ((!strcmp(cmd, "read") || !strcmp(cmd, "write") || !strcmp(cmd, "uread") || !strcmp(cmd, "uwrite")) &&
                   sscanf(line, "%*s %x", &va) == 1) {
            int r = translate(va, strstr(cmd, "write") != 0, cmd[0] == 'u', &pa);
            if (r == OK) printf("%-7s %08x -> %08x\n", cmd, va, pa);
            else printf("%-7s %08x    %s\n", cmd, va, why[r]);
        } else if (!strcmp(cmd, "seq") && sscanf(line, "%*s %x %lu %lu", &va, &n, &m) == 3 && m > 0) {
            bulk_faults = 0;
            unsigned long k = 0;
            for (unsigned long off = 0; off < n; off += m, k++) bulk(va + off);
            printf("seq     %08x  %lu bytes, step %lu: %lu accesses, %lu faults\n", va, n, m, k, bulk_faults);
        } else if (!strcmp(cmd, "rand") && sscanf(line, "%*s %x %lu %lu %lu", &va, &n, &m, &seed) == 4 && n > 0) {
            bulk_faults = 0;
            uint32_t st = (uint32_t)seed;
            for (unsigned long i = 0; i < m; i++) bulk(va + (xorshift(&st) % n) * PGSIZE + (xorshift(&st) & 0xFFF));
            printf("rand    %08x  %lu pages: %lu accesses, %lu faults\n", va, n, m, bulk_faults);
        } else if (!strcmp(cmd, "matrix") && sscanf(line, "%*s %x %lu %15s", &va, &n, s) == 3) {
            bulk_faults = 0;
            for (unsigned long i = 0; i < n; i++)
                for (unsigned long j = 0; j < n; j++)
                    bulk(va + (s[0] == 'r' ? i * n + j : j * n + i) * 8);
            printf("matrix  %08x  %lu x %lu, %s order: %lu accesses, %lu faults\n", va, n, n,
                   s[0] == 'r' ? "row" : "column", n * n, bulk_faults);
        } else if (!strcmp(cmd, "cpu") && sscanf(line, "%*s %d", &cpu) == 1 && cpu >= 0 && cpu < NCPU) {
            printf("cpu     %d\n", cpu);
        } else if (!strcmp(cmd, "flush")) {
            for (int i = 0; i < TLBSIZE; i++) tlb[cpu][i].valid = 0;
            printf("flush   cpu %d\n", cpu);
        } else if (!strcmp(cmd, "stats")) {
            printf("stats   page-table frames %d (%d KiB)", ptframes, ptframes * 4);
            for (int c = 0; c < NCPU; c++)
                if (hits[c] + misses[c])
                    printf("   cpu %d TLB %lu hits, %lu misses (%.2f%% hits)", c, hits[c], misses[c],
                           100.0 * hits[c] / (hits[c] + misses[c]));
            printf("\n");
        } else if (!strcmp(cmd, "reset")) {
            memset(hits, 0, sizeof hits);
            memset(misses, 0, sizeof misses);
            printf("reset\n");
        } else {
            printf("?       %s", line);
        }
    }
    return 0;
}
