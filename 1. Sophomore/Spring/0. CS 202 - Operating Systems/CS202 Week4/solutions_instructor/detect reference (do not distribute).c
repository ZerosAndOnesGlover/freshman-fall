/* detect.c: deadlock detection with several instances of each resource.
 *
 *   gcc -O2 -Wall -Wextra -o detect detect.c && ./detect < state.txt
 *
 * Input: n m / Available (m) / Allocation (n x m) / Request (n x m).
 * Like the Banker's safety check, but using each process's CURRENT request
 * instead of its maximum remaining need: a process that holds nothing and wants
 * nothing is not deadlocked; one whose request can never be met is.
 */
#include <stdio.h>
#include <string.h>
#define MAXP 256
#define MAXR 32
static int n, m, avail[MAXR], alloc[MAXP][MAXR], req[MAXP][MAXR];
int main(void)
{
    if (scanf("%d %d", &n, &m) != 2) return 2;
    for (int j = 0; j < m; j++) if (scanf("%d", &avail[j]) != 1) return 2;
    for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) if (scanf("%d", &alloc[i][j]) != 1) return 2;
    for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) if (scanf("%d", &req[i][j]) != 1) return 2;
    int work[MAXR], finish[MAXP], order[MAXP], k = 0;
    memcpy(work, avail, sizeof(int) * m);
    for (int i = 0; i < n; i++) {
        int holds = 0;
        for (int j = 0; j < m; j++) holds |= alloc[i][j];
        finish[i] = !holds;                     /* holding nothing: cannot be part of a deadlock */
    }
    for (int progress = 1; progress; ) {
        progress = 0;
        for (int i = 0; i < n; i++) {
            if (finish[i]) continue;
            int ok = 1;
            for (int j = 0; j < m; j++) if (req[i][j] > work[j]) ok = 0;
            if (ok) {
                for (int j = 0; j < m; j++) work[j] += alloc[i][j];
                finish[i] = 1; order[k++] = i; progress = 1;
            }
        }
    }
    int dead = 0;
    for (int i = 0; i < n; i++) if (!finish[i]) dead++;
    if (!dead) {
        printf("no deadlock; the processes can finish in the order <");
        for (int i = 0; i < k; i++) printf("%sP%d", i ? ", " : "", order[i]);
        printf(">\n");
    } else {
        printf("DEADLOCKED:");
        for (int i = 0; i < n; i++) if (!finish[i]) printf(" P%d", i);
        printf("\n");
    }
    return dead ? 1 : 0;
}
