/* bankbench.c: how does the Banker's safety check's cost grow with n and m?
 *
 * Worst case by construction: every resource except the last is plentiful, so
 * each check scans all m resources; and processes can finish only one at a
 * time, in reverse of the scan order, so every pass finds exactly one.
 */
#include <stdio.h>
#include <string.h>
#include <time.h>
#define MAXP 4096
#define MAXR 64
static int n, m, avail[MAXR], need_[MAXP][MAXR], alloc[MAXP][MAXR], finish[MAXP];
static int safe(void)
{
    int work[MAXR], count = 0;
    memset(finish, 0, sizeof(int) * n);
    memcpy(work, avail, sizeof(int) * m);
    for (int pass = 0; pass < n && count < n; pass++) {
        int progressed = 0;
        for (int i = n - 1; i >= 0; i--) {
            if (finish[i]) continue;
            int ok = 1;
            for (int j = 0; j < m && ok; j++) if (need_[i][j] > work[j]) ok = 0;
            if (ok) { for (int j = 0; j < m; j++) work[j] += alloc[i][j]; finish[i] = 1; count++; progressed = 1; break; }
        }
        if (!progressed) break;
    }
    return count == n;
}
int main(void)
{
    const int ns[] = { 100, 200, 400, 800, 1600, 3200 };
    for (int mi = 0; mi < 2; mi++) {
        m = mi ? 32 : 4;
        for (int k = 0; k < 6; k++) {
            n = ns[k];
            for (int j = 0; j < m; j++) avail[j] = 1;
            for (int i = 0; i < n; i++)
                for (int j = 0; j < m; j++) { alloc[i][j] = 1; need_[i][j] = (j < m - 1) ? 0 : 1 + i; }
            struct timespec a, b;
            clock_gettime(CLOCK_MONOTONIC, &a);
            int s = safe();
            clock_gettime(CLOCK_MONOTONIC, &b);
            printf("n=%5d m=%2d: safe=%d  %8.3f ms\n", n, m, s, ((b.tv_sec - a.tv_sec) * 1e9 + (b.tv_nsec - a.tv_nsec)) / 1e6);
        }
    }
    return 0;
}
