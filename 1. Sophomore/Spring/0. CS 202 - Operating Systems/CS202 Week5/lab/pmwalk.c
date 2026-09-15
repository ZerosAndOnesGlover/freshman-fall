/* pmwalk.c — for each mapping of a process, count its pages by what
 * /proc/PID/pagemap says about them.
 *   gcc -O2 -Wall -Wextra -o pmwalk pmwalk.c
 *   ./pmwalk            # this process
 *   ./pmwalk PID        # another process you own
 * CS 202 Week 5, Lab 5. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

#define PM_PRESENT   (1ULL << 63)
#define PM_SWAPPED   (1ULL << 62)
#define PM_FILE      (1ULL << 61)
#define PM_EXCLUSIVE (1ULL << 56)
#define PM_SOFTDIRTY (1ULL << 55)
#define PM_PFN       ((1ULL << 55) - 1)

int main(int argc, char **argv)
{
    char path[64];
    const char *pid = argc > 1 ? argv[1] : "self";
    snprintf(path, sizeof path, "/proc/%s/maps", pid);
    FILE *maps = fopen(path, "r");
    snprintf(path, sizeof path, "/proc/%s/pagemap", pid);
    int pm = open(path, O_RDONLY);
    if (!maps || pm < 0) { perror(path); return 1; }

    printf("%-12s %8s %8s %8s %8s %8s  %s\n", "start", "pages", "present", "swapped", "exclusv", "nonzero", "mapping");
    char line[512];
    unsigned long pfns = 0;
    while (fgets(line, sizeof line, maps)) {
        unsigned long lo, hi;
        char name[256] = "";
        if (sscanf(line, "%lx-%lx %*s %*s %*s %*s %255[^\n]", &lo, &hi, name) < 2) continue;
        if (lo >= 0x800000000000UL) continue;                   /* [vsyscall]: no pagemap entry */
        unsigned long n = (hi - lo) / 4096, p = 0, s = 0, x = 0, z = 0;
        uint64_t buf[512];
        for (unsigned long i = 0; i < n; i += 512) {
            size_t want = n - i < 512 ? n - i : 512;
            ssize_t got = pread(pm, buf, want * 8, (off_t)((lo / 4096 + i) * 8));
            if (got <= 0) break;
            for (ssize_t k = 0; k < got / 8; k++) {
                p += !!(buf[k] & PM_PRESENT);
                s += !!(buf[k] & PM_SWAPPED);
                x += !!(buf[k] & PM_EXCLUSIVE);
                z += (buf[k] & PM_PRESENT) && (buf[k] & PM_PFN);
            }
        }
        pfns += z;
        char *base = strrchr(name, '/');
        printf("%012lx %8lu %8lu %8lu %8lu %8lu  %s\n", lo, n, p, s, x, z, base ? base + 1 : name);
    }
    printf("present pages with a nonzero frame number: %lu\n", pfns);
    return 0;
}
