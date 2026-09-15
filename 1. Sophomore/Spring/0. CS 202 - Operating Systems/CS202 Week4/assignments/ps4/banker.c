/* banker.c: the Banker's algorithm -- safety check and request handling. CS 202 PS 4 Q1.
 *
 *   gcc -O2 -Wall -Wextra -o banker banker.c
 *   ./banker < state.txt
 *
 * Input:
 *   n m
 *   Available:  m integers
 *   Max:        n lines of m integers
 *   Allocation: n lines of m integers
 *   then any number of requests:  request <process> <m integers>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXP 1024
#define MAXR 64

static int n, m;
static int avail[MAXR], maxc[MAXP][MAXR], alloc[MAXP][MAXR];

static int need(int i, int j) __attribute__((unused));
static int need(int i, int j) { return maxc[i][j] - alloc[i][j]; }

/* Is the current state safe? If so, write one safe sequence into seq (seq may
 * be NULL). Scan processes in index order, repeatedly, finishing any process
 * whose Need fits in Work -- so that your safe sequence matches the expected
 * output. */
static int safe(int *seq)
{
    /* TODO (Q1) */
    (void)seq;
    return 0;
}

/* 1 granted; 0 must wait (not available); -1 would be unsafe; -2 exceeds its claim.
 * Check in that order: the claim first, then availability, then safety. A request
 * that would be unsafe must leave the state exactly as it was. */
static int request(int i, const int *req)
{
    /* TODO (Q1) */
    (void)i; (void)req;
    return 0;
}

static void print_state(void)
{
    int seq[MAXP];
    if (safe(seq)) {
        printf("state is SAFE; one safe sequence: <");
        for (int i = 0; i < n; i++) printf("%sP%d", i ? ", " : "", seq[i]);
        printf(">\n");
    } else {
        printf("state is UNSAFE\n");
    }
}

int main(void)
{
    if (scanf("%d %d", &n, &m) != 2 || n > MAXP || m > MAXR) return 2;
    for (int j = 0; j < m; j++) if (scanf("%d", &avail[j]) != 1) return 2;
    for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) if (scanf("%d", &maxc[i][j]) != 1) return 2;
    for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) if (scanf("%d", &alloc[i][j]) != 1) return 2;
    print_state();
    char word[16];
    while (scanf("%15s", word) == 1) {
        int i, req[MAXR];
        if (strcmp(word, "request") || scanf("%d", &i) != 1) break;
        for (int j = 0; j < m; j++) if (scanf("%d", &req[j]) != 1) return 2;
        printf("request P%d (", i);
        for (int j = 0; j < m; j++) printf("%s%d", j ? "," : "", req[j]);
        int r = request(i, req);
        printf("): %s\n", r == 1 ? "GRANTED" : r == 0 ? "WAIT: not available"
                         : r == -1 ? "DENIED: would be unsafe" : "ERROR: exceeds maximum claim");
        if (r == 1) {
            printf("  available now (");
            for (int j = 0; j < m; j++) printf("%s%d", j ? "," : "", avail[j]);
            printf(")  ");
            print_state();
        }
    }
    return 0;
}
