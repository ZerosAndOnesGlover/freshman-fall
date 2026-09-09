/* LAB 11 -- a memory hog. Allocates AND touches memory forever (touching
 * forces the kernel to commit each page, so it counts against memory.current).
 * Run it under a cgroup memory cap and watch the cgroup-local OOM killer:
 *   systemd-run --user --scope -p MemoryMax=100M -p MemorySwapMax=0 ./hog
 *   echo $?     # 137 = 128 + SIGKILL(9)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    size_t step = 8 << 20;   /* 8 MiB at a time */
    size_t total = 0;
    for (;;) {
        char *p = malloc(step);
        if (!p) { printf("malloc failed at %zu MiB\n", total >> 20); return 1; }
        memset(p, 1, step);          /* touch: commit the pages */
        total += step;
        if ((total >> 20) % 64 == 0) { printf("touched %zu MiB\n", total >> 20); fflush(stdout); }
        if (total > (2UL << 30)) return 0;   /* stop at 2 GiB if never capped */
    }
}
