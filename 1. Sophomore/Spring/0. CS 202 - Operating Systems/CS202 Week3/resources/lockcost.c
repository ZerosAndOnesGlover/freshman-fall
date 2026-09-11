/* lockcost.c: what does an UNCONTENDED lock cost? One thread, no competition.
 *
 *   gcc -O2 -Wall -Wextra -pthread -o lockcost lockcost.c && ./lockcost
 *
 * CS 202 Week 3, L11 §1.
 */
#include "locks.h"
#include <stdio.h>
#include <time.h>

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }
#define N 50000000L
#define BENCH(label, body) do { \
    double best = 1e9; \
    for (int r = 0; r < 5; r++) { double t0 = now(); for (long i = 0; i < N; i++) { body; } double ns = (now() - t0) / N * 1e9; if (ns < best) best = ns; } \
    printf("%-44s %6.2f ns\n", label, best); } while (0)

int main(void)
{
    volatile long counter = 0;
    atomic_long acounter = 0;
    tas_lock tas = { ATOMIC_FLAG_INIT };
    cas_lock cas = { 0 };
    futex_lock fl = { 0 };
    pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
    pthread_spinlock_t ps; pthread_spin_init(&ps, 0);
    sem_t sem; sem_init(&sem, 0, 1);

    BENCH("no lock: counter++",                      counter++);
    BENCH("atomic_fetch_add (lock xadd)",            atomic_fetch_add(&acounter, 1));
    BENCH("test-and-set spinlock",                   tas_acquire(&tas); counter++; tas_release(&tas));
    BENCH("compare-and-swap spinlock",               cas_acquire(&cas); counter++; cas_release(&cas));
    BENCH("futex mutex (ours)",                      futex_acquire(&fl); counter++; futex_release(&fl));
    BENCH("pthread_spin_lock",                       pthread_spin_lock(&ps); counter++; pthread_spin_unlock(&ps));
    BENCH("pthread_mutex_lock",                      pthread_mutex_lock(&mu); counter++; pthread_mutex_unlock(&mu));
    BENCH("sem_wait / sem_post",                     sem_wait(&sem); counter++; sem_post(&sem));
    return (int)(counter & 0);
}
