/* livelock.c: two threads that each need locks A and B, and are too polite.
 *
 *   gcc -O2 -Wall -Wextra -pthread -o livelock livelock.c
 *   ./livelock <polite|yield|backoff|ordered> [seconds]
 *
 * polite:  take my first lock, TRY the second; if it is busy, release and retry at once
 * yield:   the same, but sched_yield() before retrying
 * backoff: the same, but sleep a random 0-99 microseconds before retrying
 * fixed:   the same, but always sleep exactly 50 microseconds
 * expo:    the same, but sleep a random time below a limit that starts at 1 us,
 *          doubles after each consecutive failure up to 1 ms, and resets on success
 * ordered: both threads take A then B, blocking -- no trying, no retrying
 */
#define _GNU_SOURCE
#include <pthread.h>
#include <sched.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static pthread_mutex_t A = PTHREAD_MUTEX_INITIALIZER, B = PTHREAD_MUTEX_INITIALIZER;
static atomic_int stop;
static int mode;                    /* 0 polite, 1 yield, 2 backoff, 3 ordered, 4 fixed, 5 expo */
static long rounds[2], fails[2];

static void *worker(void *arg)
{
    long me = (long)arg;
    pthread_mutex_t *first = me ? &B : &A, *second = me ? &A : &B;
    if (mode == 3) { first = &A; second = &B; }
    unsigned seed = 42 + me;
    unsigned limit = 1;
    while (!atomic_load(&stop)) {
        pthread_mutex_lock(first);
        for (volatile int k = 0; k < 200; k++) ;          /* a little work holding one lock */
        if (mode == 3) {
            pthread_mutex_lock(second);
        } else if (pthread_mutex_trylock(second) != 0) {
            pthread_mutex_unlock(first);
            fails[me]++;
            if (mode == 1) sched_yield();
            if (mode == 2) usleep(rand_r(&seed) % 100);
            if (mode == 4) usleep(50);
            if (mode == 5) { usleep(rand_r(&seed) % limit); if (limit < 1000) limit *= 2; }
            continue;
        }
        for (volatile int k = 0; k < 200; k++) ;          /* the work that needs both */
        rounds[me]++;
        limit = 1;
        pthread_mutex_unlock(second);
        pthread_mutex_unlock(first);
    }
    return 0;
}

int main(int argc, char **argv)
{
    const char *names[] = { "polite", "yield", "backoff", "ordered", "fixed", "expo" };
    for (int i = 0; i < 6; i++) if (argc > 1 && !strcmp(argv[1], names[i])) mode = i;
    int secs = argc > 2 ? atoi(argv[2]) : 3;
    pthread_t t[2];
    for (long i = 0; i < 2; i++) pthread_create(&t[i], 0, worker, (void *)i);
    sleep(secs);
    atomic_store(&stop, 1);
    pthread_join(t[0], 0);
    pthread_join(t[1], 0);
    long r = rounds[0] + rounds[1], f = fails[0] + fails[1];
    printf("%-8s %9ld rounds in %d s (%8.0f/s), %10ld failed attempts, %.2f failures per round\n",
           names[mode], r, secs, (double)r / secs, f, r ? (double)f / r : 0.0);
    return 0;
}
