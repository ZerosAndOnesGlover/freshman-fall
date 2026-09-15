/* banksim.c: random workloads, granted naively or by the Banker's algorithm. CS 202 PS 4 Q3.
 *
 *   gcc -O2 -Wall -Wextra -o banksim banksim.c && ./banksim
 *
 * P processes, R resource types, UNITS units of each. Every process declares a
 * random maximum claim, then repeatedly asks for one more unit of something it
 * still needs, and releases everything when its claim is met.
 *   naive:  grant if the unit is free
 *   banker: grant only if it is free AND the resulting state is safe
 * A run deadlocks when no unfinished process can be granted anything and none
 * has its claim met.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define P 6
#define R 3
#define UNITS 6
static int avail[R], maxc[P][R], alloc[P][R], done[P];

static int safe(void)
{
    /* TODO (Q3): your safety check from Q1, adapted: processes already done are
     * finished from the start, and a process's need is maxc - alloc. */
    return 1;
}

static int claim_met(int i) { for (int j = 0; j < R; j++) if (alloc[i][j] < maxc[i][j]) return 0; return 1; }
static void release_all(int i) { for (int j = 0; j < R; j++) { avail[j] += alloc[i][j]; alloc[i][j] = 0; } done[i] = 1; }

/* Returns 1 if every process finished, 0 on deadlock. */
static int run(int banker, long *grants, long *refusals)
{
    for (int j = 0; j < R; j++) avail[j] = UNITS;
    for (int i = 0; i < P; i++) { done[i] = 0; for (int j = 0; j < R; j++) { maxc[i][j] = rand() % (UNITS / 2 + 1); alloc[i][j] = 0; } }
    int finished = 0;
    *grants = *refusals = 0;
    for (int i = 0; i < P; i++) if (claim_met(i)) { release_all(i); finished++; }
    while (finished < P) {
        /* every (process, resource) pair that could be granted now */
        int ci[P * R], cj[P * R], nc = 0;
        for (int i = 0; i < P; i++) {
            if (done[i]) continue;
            for (int j = 0; j < R; j++) if (alloc[i][j] < maxc[i][j] && avail[j] > 0) { ci[nc] = i; cj[nc] = j; nc++; }
        }
        if (banker) {                       /* drop the ones that would be unsafe */
            int keep = 0;
            for (int c = 0; c < nc; c++) {
                avail[cj[c]]--; alloc[ci[c]][cj[c]]++;
                int ok = safe();
                avail[cj[c]]++; alloc[ci[c]][cj[c]]--;
                if (ok) { ci[keep] = ci[c]; cj[keep] = cj[c]; keep++; } else (*refusals)++;
            }
            nc = keep;
        }
        if (nc == 0) return 0;
        int c = rand() % nc;
        avail[cj[c]]--; alloc[ci[c]][cj[c]]++;
        (*grants)++;
        if (claim_met(ci[c])) { release_all(ci[c]); finished++; }
    }
    return 1;
}

int main(void)
{
    for (int banker = 0; banker <= 1; banker++) {
        srand(202);
        long runs = 10000, deadlocks = 0, grants = 0, refusals = 0, ok = 0;
        for (long r = 0; r < runs; r++) {
            long g, f;
            if (run(banker, &g, &f)) { ok++; grants += g; refusals += f; } else deadlocks++;
        }
        printf("%-7s %ld runs: %ld deadlocked (%.1f%%)", banker ? "banker" : "naive", runs, deadlocks, 100.0 * deadlocks / runs);
        if (banker) printf("; %.1f candidate grants per run refused as unsafe although the unit was free", (double)refusals / ok);
        printf("\n");
    }
    return 0;
}
