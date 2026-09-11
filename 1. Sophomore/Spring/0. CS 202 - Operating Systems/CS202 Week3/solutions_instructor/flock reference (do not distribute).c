/* flock.c: three futex locks, measured. CS 202 Lab 3 -- REFERENCE SOLUTION.
 *
 *   gcc -O2 -Wall -Wextra -pthread -o flock flock.c
 *   ./flock uncontended <always2|buggy2|drepper3> <ops>
 *   ./flock contended   <always2|buggy2|drepper3> <threads> <total ops>
 *   ./flock eagain
 */
#define _GNU_SOURCE
#include <errno.h>
#include <linux/futex.h>
#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/syscall.h>
#include <time.h>
#include <unistd.h>

static atomic_int v;
static int waiters;                     /* buggy2 only: a plain int, updated without a lock */
static long counter, per_thread;
static int kind;                        /* 0 always2, 1 buggy2, 2 drepper3 */

static long fwait(int val) { return syscall(SYS_futex, &v, FUTEX_WAIT_PRIVATE, val, 0, 0, 0); }
static long fwake(int n)   { return syscall(SYS_futex, &v, FUTEX_WAKE_PRIVATE, n, 0, 0, 0); }

static void lock(void)
{
    if (kind == 2) {
        int c = 0;
        if (atomic_compare_exchange_strong(&v, &c, 1)) return;
        if (c != 2) c = atomic_exchange(&v, 2);
        while (c != 0) { fwait(2); c = atomic_exchange(&v, 2); }
        return;
    }
    while (atomic_exchange(&v, 1) != 0) {
        if (kind == 1) waiters++;
        fwait(1);
        if (kind == 1) waiters--;
    }
}

static void unlock(void)
{
    if (kind == 2) { if (atomic_exchange(&v, 0) == 2) fwake(1); return; }
    atomic_store(&v, 0);
    if (kind == 0 || waiters > 0) fwake(1);
}

static void *work(void *arg) { (void)arg; for (long i = 0; i < per_thread; i++) { lock(); counter++; unlock(); } return 0; }
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }

int main(int argc, char **argv)
{
    if (argc >= 2 && !strcmp(argv[1], "eagain")) {
        atomic_store(&v, 5);
        long r = fwait(7);              /* "sleep if the value is 7" -- it is 5 */
        printf("FUTEX_WAIT expecting 7 on a value of 5 returned %ld, errno %s: no sleep at all\n", r, strerrorname_np(errno));
        return 0;
    }
    if (argc < 4) { fprintf(stderr, "usage: see source\n"); return 2; }
    kind = !strcmp(argv[2], "always2") ? 0 : !strcmp(argv[2], "buggy2") ? 1 : 2;
    int threads = !strcmp(argv[1], "contended") ? atoi(argv[3]) : 1;
    long total = atol(argv[argc - 1]);
    per_thread = total / threads;
    pthread_t t[16];
    double t0 = now();
    if (threads == 1) work(0);
    else {
        for (int i = 0; i < threads; i++) pthread_create(&t[i], 0, work, 0);
        /* watchdog: if the counter stops moving for 2 s, somebody is asleep forever */
        long last = -1;
        for (;;) {
            usleep(200000);
            if (counter == per_thread * threads) break;
            static int still;
            if (counter == last) { if (++still == 10) {
                printf("%-8s HUNG: counter stuck at %ld of %ld for 2 s, lock value %d, waiters %d\n",
                       argv[2], counter, per_thread * threads, atomic_load(&v), waiters);
                fflush(stdout); _exit(3); } }
            else still = 0;
            last = counter;
        }
        for (int i = 0; i < threads; i++) pthread_join(t[i], 0);
    }
    double s = now() - t0;
    printf("%-8s %s x%d: %.1f ns per lock+unlock, counter %s\n", argv[2], argv[1], threads,
           s / (per_thread * threads) * 1e9, counter == per_thread * threads ? "correct" : "WRONG");
    return 0;
}
