/* syscost.c: what does crossing into the kernel cost, compared with not crossing?
 *
 *   gcc -O2 -Wall -Wextra -o syscost syscost.c && ./syscost
 *
 * Pinned to one CPU; each figure is the best of seven runs, in nanoseconds per call. */
#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <sys/syscall.h>

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

__attribute__((noinline)) static long func(void) { return 42; }

#define BENCH(label, n, stmt) do {                                  \
    double best = 1e9;                                              \
    for (int rep = 0; rep < 7; rep++) {                             \
        double t0 = now();                                          \
        for (long i = 0; i < (n); i++) { stmt; }                    \
        double dt = (now() - t0) / (n) * 1e9;                       \
        if (dt < best) best = dt;                                   \
    }                                                               \
    printf("%-44s %9.2f ns\n", label, best);                        \
} while (0)

int main(void)
{
    cpu_set_t s;
    CPU_ZERO(&s);
    CPU_SET(3, &s);
    sched_setaffinity(0, sizeof s, &s);

    struct timespec ts;
    volatile long sink = 0;
    char c;

    BENCH("function call (noinline)",                 200000000L, sink = func());
    BENCH("clock_gettime  (vDSO, no trap)",            20000000L, clock_gettime(CLOCK_MONOTONIC, &ts));
    BENCH("getppid()      (glibc wrapper)",             5000000L, sink = getppid());
    BENCH("syscall(SYS_getppid)",                       5000000L, sink = syscall(SYS_getppid));
    BENCH("syscall(SYS_clock_gettime) (forced trap)",   5000000L, syscall(SYS_clock_gettime, CLOCK_MONOTONIC, &ts));
    BENCH("read(-1, ...)  (fails with EBADF)",          5000000L, sink = read(-1, &c, 1));
    BENCH("syscall(1000)  (no such call: ENOSYS)",      5000000L, sink = syscall(1000));
    return (int)(sink & 0);
}
