/* philo3.c: five dining philosophers, four strategies, measured for throughput
 * and fairness. CS 202 PS 3 Q3 -- REFERENCE.
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

static sem_t seats;                                  /* SEATS: N - 1 */
static pthread_mutex_t waiter = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t forks_freed = PTHREAD_COND_INITIALIZER;
static int in_use[N];                                /* WAITER: which forks are taken */

static int left(int i)  { return i; }
static int right(int i) { return (i + 1) % N; }

static void pick_up(int i)
{
    switch (strategy) {
    case NAIVE:
        pthread_mutex_lock(&fork_[left(i)]);
        pthread_mutex_lock(&fork_[right(i)]);
        break;
    case ORDERED: {
        int lo = left(i) < right(i) ? left(i) : right(i);
        int hi = left(i) < right(i) ? right(i) : left(i);
        pthread_mutex_lock(&fork_[lo]);
        pthread_mutex_lock(&fork_[hi]);
        break;
    }
    case SEATS:
        sem_wait(&seats);
        pthread_mutex_lock(&fork_[left(i)]);
        pthread_mutex_lock(&fork_[right(i)]);
        break;
    case WAITER:
        pthread_mutex_lock(&waiter);
        while (in_use[left(i)] || in_use[right(i)])
            pthread_cond_wait(&forks_freed, &waiter);
        in_use[left(i)] = in_use[right(i)] = 1;
        pthread_mutex_unlock(&waiter);
        break;
    }
}

static void put_down(int i)
{
    switch (strategy) {
    case NAIVE: case ORDERED:
        pthread_mutex_unlock(&fork_[right(i)]);
        pthread_mutex_unlock(&fork_[left(i)]);
        break;
    case SEATS:
        pthread_mutex_unlock(&fork_[right(i)]);
        pthread_mutex_unlock(&fork_[left(i)]);
        sem_post(&seats);
        break;
    case WAITER:
        pthread_mutex_lock(&waiter);
        in_use[left(i)] = in_use[right(i)] = 0;
        pthread_cond_broadcast(&forks_freed);
        pthread_mutex_unlock(&waiter);
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
