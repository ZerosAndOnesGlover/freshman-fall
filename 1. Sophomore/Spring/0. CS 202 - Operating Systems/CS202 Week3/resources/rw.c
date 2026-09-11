/* rw.c: seven readers who never stop reading, and one writer who wants in
 * every 10 ms. How long does the writer wait?
 *
 *   ./rw default | ./rw writer
 *
 * CS 202 Week 3, L12 §7.
 */
#define _GNU_SOURCE
#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

static pthread_rwlock_t rw;
static atomic_int stop;
static double now(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return t.tv_sec+t.tv_nsec*1e-9; }
static int cmp(const void *a, const void *b){ double x=*(double*)a, y=*(double*)b; return (x>y)-(x<y); }

static void *reader(void *arg)
{
    (void)arg;
    while (!atomic_load(&stop)) {
        pthread_rwlock_rdlock(&rw);
        usleep(100);                    /* read for ~100 microseconds */
        pthread_rwlock_unlock(&rw);
    }
    return 0;
}

int main(int argc, char **argv)
{
    pthread_rwlockattr_t a; pthread_rwlockattr_init(&a);
    if (argc > 1 && !strcmp(argv[1], "writer"))
        pthread_rwlockattr_setkind_np(&a, PTHREAD_RWLOCK_PREFER_WRITER_NONRECURSIVE_NP);
    pthread_rwlock_init(&rw, &a);
    pthread_t t[7];
    for (int i = 0; i < 7; i++) pthread_create(&t[i], 0, reader, 0);
    double waits[400]; int n = 0, timeouts = 0;
    double end = now() + 4;
    while (now() < end && n < 400) {
        usleep(10000);
        double t0 = now();
        struct timespec dl; clock_gettime(CLOCK_REALTIME, &dl); dl.tv_sec += 1;
        if (pthread_rwlock_timedwrlock(&rw, &dl) != 0) { timeouts++; continue; }
        waits[n++] = (now() - t0) * 1e3;
        pthread_rwlock_unlock(&rw);
    }
    atomic_store(&stop, 1);
    for (int i = 0; i < 7; i++) pthread_join(t[i], 0);
    if (n) qsort(waits, n, sizeof(double), cmp);
    printf("%-8s writer got the lock %d times in 4 s, gave up after 1 s %d times; wait median %.3f ms, max %.3f ms\n",
           argc > 1 ? argv[1] : "default", n, timeouts, n ? waits[n/2] : 0.0, n ? waits[n-1] : 0.0);
    return 0;
}
