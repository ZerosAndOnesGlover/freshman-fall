/* philo.c: five dining philosophers, three ways.
 *
 *   ./philo naive    pick up left fork, then right
 *   ./philo ordered  pick up the lower-numbered fork first
 *   ./philo seats    at most four philosophers may try at once (a semaphore)
 *
 * Runs until 200,000 meals have been eaten, or until nobody has eaten for a
 * second -- which is reported as a deadlock.
 *
 * CS 202 Week 3, L12 §6.
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
#define MEALS 200000
static pthread_mutex_t fork_[N];
static sem_t seats;
static int mode;
static atomic_long meals;

static void *philosopher(void *arg)
{
    int i = (int)(long)arg;
    int left = i, right = (i + 1) % N;
    int first = left, second = right;
    if (mode == 1 && first > second) { first = right; second = left; }
    while (atomic_load(&meals) < MEALS) {
        if (mode == 2) sem_wait(&seats);
        pthread_mutex_lock(&fork_[first]);
        pthread_mutex_lock(&fork_[second]);
        atomic_fetch_add(&meals, 1);            /* eat */
        pthread_mutex_unlock(&fork_[second]);
        pthread_mutex_unlock(&fork_[first]);
        if (mode == 2) sem_post(&seats);
    }
    return 0;
}

int main(int argc, char **argv)
{
    mode = argc > 1 && !strcmp(argv[1], "ordered") ? 1 : argc > 1 && !strcmp(argv[1], "seats") ? 2 : 0;
    for (int i = 0; i < N; i++) pthread_mutex_init(&fork_[i], 0);
    sem_init(&seats, 0, N - 1);
    pthread_t t[N];
    struct timespec a, b;
    clock_gettime(CLOCK_MONOTONIC, &a);
    for (long i = 0; i < N; i++) pthread_create(&t[i], 0, philosopher, (void *)i);
    long last = -1;
    for (;;) {
        usleep(1000000);
        long m = atomic_load(&meals);
        clock_gettime(CLOCK_MONOTONIC, &b);
        if (m >= MEALS) {
            printf("%-8s %d meals in %.2f s\n", argc > 1 ? argv[1] : "naive", MEALS, (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) * 1e-9);
            fflush(stdout);
    _exit(0);
        }
        if (m == last) {
            printf("%-8s DEADLOCK after %ld meals\n", argc > 1 ? argv[1] : "naive", m);
            fflush(stdout);
            _exit(1);
        }
        last = m;
    }
}
