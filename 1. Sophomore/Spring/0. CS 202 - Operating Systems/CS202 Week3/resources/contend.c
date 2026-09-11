/* contend.c: T threads share one counter behind one lock. Total increments fixed.
 *
 *   gcc -O2 -Wall -Wextra -pthread -o contend contend.c
 *   ./contend <none|local|atomic|tas|ttas|cas|spin|futex|mutex> <threads> <total> [cs loop]
 *
 * CS 202 Week 3, L10 §7, L11 §5-§6.
 */
#include "locks.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static enum { NONE, ATOMIC, TAS, CAS, FUTEX, MUTEX, SPIN, TTAS, LOCAL } kind;
static long cs_iters;                   /* extra work inside the critical section */
static ttas_lock ttas;
struct padded { long v; char pad[56]; };
static struct padded local[64];
static long per_thread;
static long counter;
static atomic_long acounter;
static tas_lock tas = { ATOMIC_FLAG_INIT };
static cas_lock cas;
static futex_lock fl;
static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
static pthread_spinlock_t ps;

static inline void cs(void) { counter++; for (volatile long k = 0; k < cs_iters; k++) ; }

static void *work(void *arg)
{
    long me = (long)arg;
    for (long i = 0; i < per_thread; i++) {
        switch (kind) {
        case LOCAL:  local[me].v++; break;
        case TTAS:   ttas_acquire(&ttas); cs(); ttas_release(&ttas); break;
        case NONE:   counter++; break;
        case ATOMIC: atomic_fetch_add(&acounter, 1); break;
        case TAS:    tas_acquire(&tas); cs(); tas_release(&tas); break;
        case CAS:    cas_acquire(&cas); cs(); cas_release(&cas); break;
        case FUTEX:  futex_acquire(&fl); cs(); futex_release(&fl); break;
        case MUTEX:  pthread_mutex_lock(&mu); cs(); pthread_mutex_unlock(&mu); break;
        case SPIN:   pthread_spin_lock(&ps); cs(); pthread_spin_unlock(&ps); break;
        }
    }
    return 0;
}

int main(int argc, char **argv)
{
    if (argc < 4) { fprintf(stderr, "usage: contend <kind> <threads> <total> [critical-section loop]\n"); return 2; }
    const char *names[] = { "none", "atomic", "tas", "cas", "futex", "mutex", "spin", "ttas", "local" };
    for (int i = 0; i < 9; i++) if (!strcmp(argv[1], names[i])) kind = i;
    cs_iters = argc > 4 ? atol(argv[4]) : 0;
    int n = atoi(argv[2]);
    long total = atol(argv[3]);
    per_thread = total / n;
    pthread_spin_init(&ps, 0);
    pthread_t t[64];
    struct timespec a, b;
    clock_gettime(CLOCK_MONOTONIC, &a);
    for (long i = 0; i < n; i++) pthread_create(&t[i], 0, work, (void *)i);
    for (int i = 0; i < n; i++) pthread_join(t[i], 0);
    clock_gettime(CLOCK_MONOTONIC, &b);
    double s = (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) * 1e-9;
    long got = kind == ATOMIC ? acounter : counter;
    if (kind == LOCAL) { got = 0; for (int i = 0; i < n; i++) got += local[i].v; }
    printf("%-6s %d threads: %.3f s, %.1f ns per increment, counter %s\n",
           names[kind], n, s, s / (per_thread * n) * 1e9, got == per_thread * n ? "correct" : "WRONG");
    return 0;
}
