/* pmlab.c — watch four pages of one mapping through /proc/self/pagemap while
 * the kernel fills them on demand, shares them after fork, tracks writes, and
 * pages them out.
 *   gcc -O2 -Wall -Wextra -o pmlab pmlab.c
 *   ./pmlab demand | cow | dirty | pageout
 * Each line shows one flag set per page:  P present  S swapped  x exclusive  d soft-dirty
 * CS 202 Week 5, Lab 5. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/resource.h>
#include <sys/wait.h>

#define NPAGES 4

static int pm;
static char *m;

static long faults(void)
{
    struct rusage r;
    getrusage(RUSAGE_SELF, &r);
    return r.ru_minflt + r.ru_majflt;
}

volatile char sink;                     /* somewhere to put a byte we read */

/* Run STMT and report the page faults it took, with the four pages' flags. */
#define STEP(who, what, stmt) do { long f0_ = faults(); stmt; long f1_ = faults(); show(who, what, f1_ - f0_); } while (0)

static void show(const char *who, const char *what, long nfaults)
{
    printf("%-6s %-34s", who, what);
    for (int i = 0; i < NPAGES; i++) {
        uint64_t e = 0;
        if (pread(pm, &e, 8, ((uintptr_t)m / 4096 + i) * 8) != 8) perror("pread");
        printf("  %c%c%c", e >> 63 & 1 ? 'P' : e >> 62 & 1 ? 'S' : '-',
               e >> 56 & 1 ? 'x' : '.', e >> 55 & 1 ? 'd' : '.');
        if (e >> 63 & 1 && (e & ((1ULL << 55) - 1)))
            printf("(pfn %llx)", (unsigned long long)(e & ((1ULL << 55) - 1)));
    }
    printf("   faults %ld\n", nfaults);
    fflush(stdout);
}

int main(int argc, char **argv)
{
    const char *mode = argc > 1 ? argv[1] : "demand";
    if (strcmp(mode, "demand") && strcmp(mode, "cow") && strcmp(mode, "dirty") && strcmp(mode, "pageout")) {
        fprintf(stderr, "usage: %s demand|cow|dirty|pageout\n", argv[0]);
        return 1;
    }
    pm = open("/proc/self/pagemap", O_RDONLY);
    m = mmap(0, NPAGES * 4096, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (pm < 0 || m == MAP_FAILED) { perror("setup"); return 1; }
    madvise(m, NPAGES * 4096, MADV_NOHUGEPAGE);
    sink = 0;
    show("", "mapped, nothing touched", 0);

    if (!strcmp(mode, "demand")) {
        STEP("", "read page 0", sink = m[0]);
        STEP("", "wrote page 0", m[0] = 1);
        STEP("", "wrote page 1 (never read)", m[4096] = 1);
    } else if (!strcmp(mode, "cow")) {
        STEP("parent", "wrote all four", memset(m, 7, NPAGES * 4096));
        pid_t p = fork();
        if (p == 0) {
            sink = 1;                   /* take the child's own copy of sink's page first */
            show("child", "after fork", 0);
            STEP("child", "read page 0", sink = m[0]);
            STEP("child", "wrote page 1", m[1 * 4096] = 8);
            _exit(0);
        }
        waitpid(p, 0, 0);
        sink = 0;                       /* fork made sink's page copy-on-write for the parent too */
        STEP("parent", "child has exited; read page 1", sink = m[4096]);
        printf("parent's page 1 still holds %d\n", sink);
    } else if (!strcmp(mode, "dirty")) {
        STEP("", "wrote all four", memset(m, 7, NPAGES * 4096));
        int fd = open("/proc/self/clear_refs", O_WRONLY);
        if (fd < 0 || write(fd, "4", 1) != 1) perror("clear_refs");
        sink = 0;                       /* clear_refs write-protected every page we own, sink's */
        (void)faults();                 /* and the stack's included: take those faults now */
        show("", "wrote 4 to /proc/self/clear_refs", 0);
        STEP("", "read page 0", sink = m[0]);
        STEP("", "wrote page 2", m[2 * 4096] = 9);
        STEP("", "wrote page 2 again", m[2 * 4096] = 10);
    } else {
        for (int i = 0; i < NPAGES; i++) memset(m + i * 4096, 'a' + i, 4096);
        show("", "wrote 'a' 'b' 'c' 'd' into the four", 0);
        int r = 0;
        STEP("", "MADV_PAGEOUT on pages 0 and 1", r = madvise(m, 2 * 4096, MADV_PAGEOUT));
        if (r) perror("MADV_PAGEOUT");
        STEP("", "read page 0 back", sink = m[0]);
        printf("page 0 holds '%c'\n", sink);
    }
    return 0;
}
