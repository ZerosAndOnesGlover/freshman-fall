/* bbuf.c: a one-slot bounded buffer, three ways to wait.
 *
 *   ./bbuf if2     separate "not empty" / "not full" CVs, but consumers use `if`
 *   ./bbuf while1  consumers and producers share ONE CV, with `while` and signal
 *   ./bbuf while2  separate CVs, `while` everywhere -- the correct version
 *
 * 1 producer, 3 consumers, 300,000 items. A watchdog reports if nothing
 * happens for two seconds.
 *
 * CS 202 Week 3, L12 §2-§3.
 */
#define _GNU_SOURCE
#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define ITEMS 300000
#define CONSUMERS 3

static int mode;                        /* 0 if2, 1 while1, 2 while2 */
static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t not_empty = PTHREAD_COND_INITIALIZER, not_full = PTHREAD_COND_INITIALIZER;
static int count;                       /* 0 or 1 */
static atomic_long consumed, empty_takes, progress;
static atomic_int finished;

static pthread_cond_t *cv_for_consumers(void) { return mode == 1 ? &not_full : &not_empty; }

static void *producer(void *arg)
{
    (void)arg;
    for (int i = 0; i < ITEMS; i++) {
        pthread_mutex_lock(&m);
        while (count == 1)
            pthread_cond_wait(&not_full, &m);
        count = 1;
        pthread_cond_signal(cv_for_consumers());
        pthread_mutex_unlock(&m);
        atomic_fetch_add(&progress, 1);
    }
    return 0;
}

static void *consumer(void *arg)
{
    (void)arg;
    while (!atomic_load(&finished)) {
        pthread_mutex_lock(&m);
        if (mode == 0) {
            if (count == 0)
                pthread_cond_wait(&not_empty, &m);
        } else {
            while (count == 0 && !atomic_load(&finished))
                pthread_cond_wait(cv_for_consumers(), &m);
        }
        if (count == 0) {                 /* woke up, and there is nothing there */
            atomic_fetch_add(&empty_takes, 1);
        } else {
            count = 0;
            atomic_fetch_add(&consumed, 1);
            pthread_cond_signal(&not_full);
        }
        pthread_mutex_unlock(&m);
        atomic_fetch_add(&progress, 1);
        if (atomic_load(&consumed) == ITEMS) atomic_store(&finished, 1);
    }
    return 0;
}

int main(int argc, char **argv)
{
    mode = argc > 1 && !strcmp(argv[1], "while1") ? 1 : argc > 1 && !strcmp(argv[1], "while2") ? 2 : 0;
    pthread_t p, c[CONSUMERS];
    pthread_create(&p, 0, producer, 0);
    for (int i = 0; i < CONSUMERS; i++) pthread_create(&c[i], 0, consumer, 0);
    long last = -1;
    for (int secs = 0; secs < 60; secs++) {
        sleep(2);
        long now = atomic_load(&progress);
        if (atomic_load(&consumed) == ITEMS) break;
        if (now == last) {
            printf("%-7s DEADLOCK: no progress for 2 s after %ld of %d items consumed (empty takes %ld)\n",
                   argc > 1 ? argv[1] : "if2", atomic_load(&consumed), ITEMS, atomic_load(&empty_takes));
            fflush(stdout);
            _exit(1);
        }
        last = now;
    }
    printf("%-7s consumed %ld of %d; woke to an empty buffer %ld times\n",
           argc > 1 ? argv[1] : "if2", atomic_load(&consumed), ITEMS, atomic_load(&empty_takes));
    fflush(stdout);
    _exit(0);
}
