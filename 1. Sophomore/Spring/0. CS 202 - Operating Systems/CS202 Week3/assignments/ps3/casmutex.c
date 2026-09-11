/* casmutex.c: a mutex from compare-and-swap. CS 202 PS 3 Q1-Q2.
 *
 *   gcc -O2 -Wall -Wextra -pthread -o casmutex casmutex.c
 *   ./casmutex uncontended <kind> <ops>
 *   ./casmutex contended   <kind> <threads> <total> [critical-section loop]
 *
 * kinds: mine     your lock: spin briefly, then yield
 *        spin     your lock with yielding switched off
 *        pthread  pthread_mutex, for comparison
 *        broken   "if not held, set held" -- not atomic (Q2)
 */
#define _GNU_SOURCE
#include <pthread.h>
#include <sched.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define SPIN_LIMIT 100

typedef struct { atomic_int held; } cas_mutex;
static int yielding = 1;

void cas_mutex_lock(cas_mutex *m)
{
    /* TODO (Q1): test, then compare-and-swap 0 -> 1. While it fails, `pause`
     * for up to SPIN_LIMIT attempts, then sched_yield() between attempts --
     * unless `yielding` is 0, in which case keep pausing forever. */
    (void)m;
}

void cas_mutex_unlock(cas_mutex *m)
{
    /* TODO (Q1): one atomic store. */
    (void)m;
}

/* ---- Everything below is the provided harness. ---- */

typedef struct { int held; } broken_mutex;
static void broken_lock(broken_mutex *m)   { while (m->held) sched_yield(); m->held = 1; }
static void broken_unlock(broken_mutex *m) { m->held = 0; }

static enum { MINE, SPIN, PTHREAD, BROKEN } kind;
static cas_mutex cm;
static broken_mutex bm;
static pthread_mutex_t pm = PTHREAD_MUTEX_INITIALIZER;
static long counter, per_thread, cs_iters;

static void lock(void)
{
    switch (kind) { case MINE: case SPIN: cas_mutex_lock(&cm); break; case PTHREAD: pthread_mutex_lock(&pm); break; case BROKEN: broken_lock(&bm); break; }
}
static void unlock(void)
{
    switch (kind) { case MINE: case SPIN: cas_mutex_unlock(&cm); break; case PTHREAD: pthread_mutex_unlock(&pm); break; case BROKEN: broken_unlock(&bm); break; }
}

static void *work(void *arg)
{
    (void)arg;
    for (long i = 0; i < per_thread; i++) {
        lock();
        counter++;
        for (volatile long k = 0; k < cs_iters; k++) ;
        unlock();
    }
    return 0;
}

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }

int main(int argc, char **argv)
{
    if (argc < 4) { fprintf(stderr, "usage: see the comment at the top\n"); return 2; }
    const char *names[] = { "mine", "spin", "pthread", "broken" };
    for (int i = 0; i < 4; i++) if (!strcmp(argv[2], names[i])) kind = i;
    yielding = kind != SPIN;
    int threads = 1;
    long total;
    if (!strcmp(argv[1], "contended")) {
        threads = atoi(argv[3]);
        total = atol(argv[4]);
        cs_iters = argc > 5 ? atol(argv[5]) : 0;
    } else {
        total = atol(argv[3]);
    }
    per_thread = total / threads;
    pthread_t t[64];
    double best = 1e9;
    int reps = threads == 1 ? 5 : 1;
    for (int r = 0; r < reps; r++) {
        counter = 0;
        double t0 = now();
        for (int i = 0; i < threads; i++) pthread_create(&t[i], 0, work, 0);
        for (int i = 0; i < threads; i++) pthread_join(t[i], 0);
        double s = now() - t0;
        if (s < best) best = s;
    }
    printf("%-8s %s x%d: %.1f ns per lock+unlock, counter %ld of %ld%s\n", argv[2], argv[1], threads,
           best / (per_thread * threads) * 1e9, counter, per_thread * threads,
           counter == per_thread * threads ? "" : "  WRONG");
    return 0;
}
