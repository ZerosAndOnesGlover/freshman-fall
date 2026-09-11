/* ctxsw.c: what does one context switch cost?
 *
 *   gcc -O2 -Wall -Wextra -o ctxsw ctxsw.c && ./ctxsw
 *
 * Two processes pass one byte back and forth through two pipes, so every read
 * blocks and every write wakes the other side. The program counts the switches
 * that actually happened -- voluntary and involuntary, in both processes -- and
 * separately times the same write and read with no second process at all.
 * Subtracting the second from the first, and dividing by the switch count,
 * estimates one switch.
 *
 * The estimate assumes a write+read pair costs the same whether or not it
 * blocks. It does not quite: a blocking read and a waking write do more work.
 * So the per-switch figure is an upper bound on the switch alone.
 *
 * CS 202 Week 1, L05 §5. */
#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define ROUNDS 200000

static int a2b[2], b2a[2];

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

static void pin(int cpu)
{
    cpu_set_t s;
    CPU_ZERO(&s);
    CPU_SET(cpu, &s);
    sched_setaffinity(0, sizeof s, &s);
}

static double baseline(void)            /* ns per write+read pair, one process */
{
    double best = 1e18;
    char c = 'x';
    pin(2);
    for (int rep = 0; rep < 5; rep++) {
        if (pipe(a2b)) exit(1);
        double t0 = now();
        for (int i = 0; i < ROUNDS; i++)
            if (write(a2b[1], &c, 1) != 1 || read(a2b[0], &c, 1) != 1) exit(1);
        double ns = (now() - t0) / ROUNDS * 1e9;
        if (ns < best) best = ns;
        close(a2b[0]); close(a2b[1]);
    }
    return best;
}

static void pingpong(int cpu_b, double pair_ns)
{
    static long child_v, child_i;      /* RUSAGE_CHILDREN accumulates; keep the last totals */
    char c = 'x';
    double best = 1e18;
    long best_sw = 0;
    for (int rep = 0; rep < 5; rep++) {
        if (pipe(a2b) || pipe(b2a)) exit(1);
        struct rusage s0, s1, ch;
        getrusage(RUSAGE_SELF, &s0);
        double t0 = now();
        pid_t p = fork();
        if (p == 0) {
            pin(cpu_b);
            for (int i = 0; i < ROUNDS; i++)
                if (read(a2b[0], &c, 1) != 1 || write(b2a[1], &c, 1) != 1) _exit(1);
            _exit(0);
        }
        pin(2);
        for (int i = 0; i < ROUNDS; i++)
            if (write(a2b[1], &c, 1) != 1 || read(b2a[0], &c, 1) != 1) exit(1);
        waitpid(p, 0, 0);
        double elapsed = now() - t0;
        getrusage(RUSAGE_SELF, &s1);
        getrusage(RUSAGE_CHILDREN, &ch);
        long sw = (s1.ru_nvcsw - s0.ru_nvcsw) + (s1.ru_nivcsw - s0.ru_nivcsw)
                + (ch.ru_nvcsw - child_v) + (ch.ru_nivcsw - child_i);
        child_v = ch.ru_nvcsw;
        child_i = ch.ru_nivcsw;
        if (elapsed < best) { best = elapsed; best_sw = sw; }
        close(a2b[0]); close(a2b[1]); close(b2a[0]); close(b2a[1]);
    }
    double syscalls = 2.0 * ROUNDS * pair_ns * 1e-9;     /* two write+read pairs per round */
    printf("CPUs 2 and %d: %.3f s for %d rounds; %ld switches (%.2f per round); "
           "%.3f s of that is the calls; %.0f ns per switch\n",
           cpu_b, best, ROUNDS, best_sw, (double)best_sw / ROUNDS,
           syscalls, (best - syscalls) / best_sw * 1e9);
}

int main(void)
{
    double pair = baseline();
    printf("baseline: one write+read pair with no other process: %.0f ns\n", pair);
    pingpong(2, pair);                  /* both on CPU 2: every switch is on one CPU */
    pingpong(3, pair);                  /* CPU 2 and CPU 3: each side sleeps and is woken */
    return 0;
}
