// CS 211 Week 9, Lab 9 Part B.  What ordering costs, and what it buys.
//
// N threads increment one shared counter M times each.  Five ways:
//
//   plain        a non-atomic ++.  A DATA RACE: undefined behaviour, and
//                the answer is wrong.
//   relaxed      atomic, but no ordering guarantee at all.
//   acq_rel      atomic with acquire/release ordering.
//   seq_cst      atomic with sequential consistency -- C11's default, and
//                what you get from `counter++` on an _Atomic.
//   mutex        a pthread mutex.
//
//   gcc -O2 -pthread -o orders orders.c && ./orders 4 1000000
//
// Two things to read: the ANSWER column and the time.  Only one row gets
// the answer wrong, and it is the fastest.
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdatomic.h>
#include <time.h>

static long nthreads, per_thread;

static long plain_counter;
static _Atomic long atomic_counter;
static long mutex_counter;
static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;

static void *w_plain(void *a) { (void)a;
    for (long i = 0; i < per_thread; i++) plain_counter++;
    return NULL; }

static void *w_relaxed(void *a) { (void)a;
    for (long i = 0; i < per_thread; i++)
        atomic_fetch_add_explicit(&atomic_counter, 1, memory_order_relaxed);
    return NULL; }

static void *w_acqrel(void *a) { (void)a;
    for (long i = 0; i < per_thread; i++)
        atomic_fetch_add_explicit(&atomic_counter, 1, memory_order_acq_rel);
    return NULL; }

static void *w_seqcst(void *a) { (void)a;
    for (long i = 0; i < per_thread; i++)
        atomic_fetch_add_explicit(&atomic_counter, 1, memory_order_seq_cst);
    return NULL; }

static void *w_mutex(void *a) { (void)a;
    for (long i = 0; i < per_thread; i++) {
        pthread_mutex_lock(&mu); mutex_counter++; pthread_mutex_unlock(&mu);
    }
    return NULL; }

static double run(void *(*fn)(void *), long *result) {
    plain_counter = mutex_counter = 0;
    atomic_store(&atomic_counter, 0);
    pthread_t *t = malloc(nthreads * sizeof *t);
    struct timespec a, b;
    clock_gettime(CLOCK_MONOTONIC, &a);
    for (long i = 0; i < nthreads; i++) pthread_create(&t[i], NULL, fn, NULL);
    for (long i = 0; i < nthreads; i++) pthread_join(t[i], NULL);
    clock_gettime(CLOCK_MONOTONIC, &b);
    free(t);
    if (fn == w_plain)      *result = plain_counter;
    else if (fn == w_mutex) *result = mutex_counter;
    else                    *result = atomic_load(&atomic_counter);
    return (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) / 1e9;
}

int main(int argc, char **argv) {
    nthreads   = argc > 1 ? atol(argv[1]) : 4;
    per_thread = argc > 2 ? atol(argv[2]) : 1000000;
    long want = nthreads * per_thread;

    printf("; ---- %ld threads x %ld increments; correct answer %ld ----\n",
           nthreads, per_thread, want);
    printf("  %-9s %14s %10s %9s  %s\n",
           "mode", "answer", "lost", "time", "");

    struct { const char *n; void *(*f)(void *); } modes[] = {
        {"plain",   w_plain},   {"relaxed", w_relaxed},
        {"acq_rel", w_acqrel},  {"seq_cst", w_seqcst},
        {"mutex",   w_mutex},
    };
    for (unsigned i = 0; i < sizeof modes / sizeof *modes; i++) {
        long got; double s = run(modes[i].f, &got);
        printf("  %-9s %14ld %9.2f%% %8.3fs  %s\n",
               modes[i].n, got, 100.0 * (want - got) / want, s,
               got == want ? "" : "<- WRONG");
    }
    return 0;
}
