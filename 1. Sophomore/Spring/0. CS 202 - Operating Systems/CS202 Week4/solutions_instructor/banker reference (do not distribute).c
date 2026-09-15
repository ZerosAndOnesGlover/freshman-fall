/* banker.c: the Banker's algorithm -- safety check and request handling.
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

static int need(int i, int j) { return maxc[i][j] - alloc[i][j]; }

/* Is the current state safe? If so, write one safe sequence into seq. O(n^2 m). */
static int safe(int *seq)
{
    int work[MAXR], finish[MAXP] = {0}, count = 0;
    memcpy(work, avail, sizeof(int) * m);
    for (int pass = 0; pass < n && count < n; pass++) {
        int progressed = 0;
        for (int i = 0; i < n; i++) {
            if (finish[i]) continue;
            int ok = 1;
            for (int j = 0; j < m && ok; j++)
                if (need(i, j) > work[j]) ok = 0;
            if (ok) {
                for (int j = 0; j < m; j++) work[j] += alloc[i][j];
                finish[i] = 1;
                if (seq) seq[count] = i;
                count++;
                progressed = 1;
            }
        }
        if (!progressed) break;
    }
    return count == n;
}

/* 1 granted; 0 must wait (not available); -1 would be unsafe; -2 exceeds its claim. */
static int request(int i, const int *req)
{
    for (int j = 0; j < m; j++) if (req[j] > need(i, j)) return -2;
    for (int j = 0; j < m; j++) if (req[j] > avail[j]) return 0;
    for (int j = 0; j < m; j++) { avail[j] -= req[j]; alloc[i][j] += req[j]; }
    if (safe(0)) return 1;
    for (int j = 0; j < m; j++) { avail[j] += req[j]; alloc[i][j] -= req[j]; }   /* roll back */
    return -1;
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
