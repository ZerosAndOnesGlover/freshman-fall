/* philo3.c: five dining philosophers, four strategies, measured for throughput
 * and fairness. CS 202 PS 3 Q3.
 *
 *   gcc -O2 -Wall -Wextra -pthread -o philo3 philo3.c
 *   ./philo3 <naive|ordered|seats|waiter> [seconds]
 *
 * Each philosopher thinks (a short loop), picks up two forks, eats (a longer
 * loop), and puts them down, until time runs out. The program reports total
 * meals, meals per second, and the fewest and most meals eaten by any one
 * philosopher. If nobody eats for a whole second it reports a deadlock.
 */
#define _GNU_SOURCE
#include <pthread.h>
#include <semaphore.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define N 5
#define THINK_ITERS 20000
#define EAT_ITERS   50000

static enum { NAIVE, ORDERED, SEATS, WAITER } strategy;
static pthread_mutex_t fork_[N];
static long meals[N];
static atomic_int stop;
static atomic_long progress;

/* ---- the three strategies you implement ---- */

static sem_t seats __attribute__((unused));                                  /* SEATS: N - 1 */
static pthread_mutex_t waiter __attribute__((unused)) = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t forks_freed __attribute__((unused)) = PTHREAD_COND_INITIALIZER;
static int in_use[N] __attribute__((unused));                                /* WAITER: which forks are taken */

static int left(int i)  { return i; }
static int right(int i) { return (i + 1) % N; }

static void pick_up(int i)
{
    switch (strategy) {
    case NAIVE:
        pthread_mutex_lock(&fork_[left(i)]);
        pthread_mutex_lock(&fork_[right(i)]);
        break;
    case ORDERED:
        /* TODO (Q3): lock the lower-numbered of left(i) and right(i) first. */
        break;
    case SEATS:
        /* TODO (Q3): take a seat (the semaphore), then both forks. */
        break;
    case WAITER:
        /* TODO (Q3): under `waiter`, wait on `forks_freed` until both of this
         * philosopher's forks are free in `in_use`, then mark both taken. */
        break;
    }
}

static void put_down(int i)
{
    switch (strategy) {
    case NAIVE:
        pthread_mutex_unlock(&fork_[right(i)]);
        pthread_mutex_unlock(&fork_[left(i)]);
        break;
    case ORDERED:
        /* TODO (Q3) */
        break;
    case SEATS:
        /* TODO (Q3): both forks, then give up the seat. */
        break;
    case WAITER:
        /* TODO (Q3): mark both forks free, and wake everyone who might now eat. */
        break;
    }
}

/* ---- the harness ---- */

static void *philosopher(void *arg)
{
    int i = (int)(long)arg;
    while (!atomic_load(&stop)) {
        for (volatile long k = 0; k < THINK_ITERS; k++) ;
        pick_up(i);
        for (volatile long k = 0; k < EAT_ITERS; k++) ;
        meals[i]++;                                  /* only philosopher i writes meals[i] */
        atomic_fetch_add(&progress, 1);
        put_down(i);
    }
    return 0;
}

int main(int argc, char **argv)
{
    const char *names[] = { "naive", "ordered", "seats", "waiter" };
    for (int s = 0; s < 4; s++) if (argc > 1 && !strcmp(argv[1], names[s])) strategy = s;
    int seconds = argc > 2 ? atoi(argv[2]) : 3;
    for (int i = 0; i < N; i++) pthread_mutex_init(&fork_[i], 0);
    sem_init(&seats, 0, N - 1);

    pthread_t t[N];
    for (long i = 0; i < N; i++) pthread_create(&t[i], 0, philosopher, (void *)i);
    long last = -1;
    for (int s = 0; s < seconds; s++) {
        sleep(1);
        long p = atomic_load(&progress);
        if (p == last) {
            printf("%-8s DEADLOCK after %ld meals\n", names[strategy], p);
            fflush(stdout);
            _exit(1);
        }
        last = p;
    }
    atomic_store(&stop, 1);
    for (int i = 0; i < N; i++) pthread_join(t[i], 0);

    long total = 0, lo = meals[0], hi = meals[0];
    for (int i = 0; i < N; i++) {
        total += meals[i];
        if (meals[i] < lo) lo = meals[i];
        if (meals[i] > hi) hi = meals[i];
    }
    printf("%-8s %ld meals in %d s (%.0f/s); per philosopher: fewest %ld, most %ld, ratio %.2f  [",
           names[strategy], total, seconds, (double)total / seconds, lo, hi, (double)lo / hi);
    for (int i = 0; i < N; i++) printf("%s%ld", i ? " " : "", meals[i]);
    printf("]\n");
    return 0;
}
