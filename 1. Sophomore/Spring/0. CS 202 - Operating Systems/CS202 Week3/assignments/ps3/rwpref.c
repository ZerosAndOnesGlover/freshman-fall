/* rwpref.c: a writer-preferring reader-writer lock from one mutex and two
 * condition variables, against glibc's. CS 202 PS 3 Q4.
 *
 *   gcc -O2 -Wall -Wextra -pthread -o rwpref rwpref.c
 *   ./rwpref <mine|glibc|glibc-writer>
 *
 * Seven readers read continuously (each holds the read lock ~100 us), and one
 * writer wants the lock every 10 ms for four seconds, giving up after one
 * second of waiting. Reports the writer's successes and waits, and how many
 * read sections the readers completed.
 */
#define _GNU_SOURCE
#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

/* ---- your lock ---- */

typedef struct {
    pthread_mutex_t m;
    pthread_cond_t readers_ok, writer_ok;
    int readers;            /* holding the read lock */
    int writer;             /* 1 if a writer holds it */
    int waiting_writers;    /* writers waiting -- this is the preference */
} my_rwlock;

static void my_rdlock(my_rwlock *l)
{
    /* TODO (Q4): wait on readers_ok while a writer holds the lock OR any writer
     * is waiting; then count yourself as a reader. */
    (void)l;
}

static void my_rdunlock(my_rwlock *l)
{
    /* TODO (Q4): stop counting yourself; if you were the last reader, let a
     * writer know. */
    (void)l;
}

/* Returns 0 on success, -1 if it gave up at the deadline. */
static int my_wrlock_until(my_rwlock *l, const struct timespec *deadline)
{
    /* TODO (Q4): register as a waiting writer; wait on writer_ok (with
     * pthread_cond_timedwait and `deadline`) while a writer or any reader holds
     * the lock; unregister; on success take the lock. If you gave up and no
     * other writer is waiting, readers you were holding back must be woken. */
    (void)l; (void)deadline;
    return -1;
}

static void my_wrunlock(my_rwlock *l)
{
    /* TODO (Q4): release; prefer a waiting writer, otherwise wake all readers. */
    (void)l;
}

/* ---- the harness ---- */

static enum { MINE, GLIBC, GLIBC_WRITER } kind;
static my_rwlock mine = { PTHREAD_MUTEX_INITIALIZER, PTHREAD_COND_INITIALIZER, PTHREAD_COND_INITIALIZER, 0, 0, 0 };
static pthread_rwlock_t theirs;
static atomic_int stop;
static atomic_long reads;

static void rd(void)   { if (kind == MINE) my_rdlock(&mine);   else pthread_rwlock_rdlock(&theirs); }
static void rdun(void) { if (kind == MINE) my_rdunlock(&mine); else pthread_rwlock_unlock(&theirs); }

static void *reader(void *arg)
{
    (void)arg;
    while (!atomic_load(&stop)) {
        rd();
        usleep(100);
        rdun();
        atomic_fetch_add(&reads, 1);
    }
    return 0;
}

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }
static int cmp(const void *a, const void *b) { double x = *(double *)a, y = *(double *)b; return (x > y) - (x < y); }

int main(int argc, char **argv)
{
    const char *names[] = { "mine", "glibc", "glibc-writer" };
    for (int i = 0; i < 3; i++) if (argc > 1 && !strcmp(argv[1], names[i])) kind = i;
    pthread_rwlockattr_t a;
    pthread_rwlockattr_init(&a);
    if (kind == GLIBC_WRITER)
        pthread_rwlockattr_setkind_np(&a, PTHREAD_RWLOCK_PREFER_WRITER_NONRECURSIVE_NP);
    pthread_rwlock_init(&theirs, &a);

    pthread_t t[7];
    for (int i = 0; i < 7; i++) pthread_create(&t[i], 0, reader, 0);
    double waits[500];
    int n = 0, gave_up = 0;
    double end = now() + 4;
    while (now() < end && n < 500) {
        usleep(10000);
        double t0 = now();
        struct timespec dl;
        clock_gettime(CLOCK_REALTIME, &dl);
        dl.tv_sec += 1;
        int ok;
        if (kind == MINE) ok = my_wrlock_until(&mine, &dl) == 0;
        else ok = pthread_rwlock_timedwrlock(&theirs, &dl) == 0;
        if (!ok) { gave_up++; continue; }
        waits[n++] = (now() - t0) * 1e3;
        if (kind == MINE) my_wrunlock(&mine); else pthread_rwlock_unlock(&theirs);
    }
    atomic_store(&stop, 1);
    for (int i = 0; i < 7; i++) pthread_join(t[i], 0);
    if (n) qsort(waits, n, sizeof(double), cmp);
    printf("%-13s writer: %3d acquisitions, gave up %d; wait median %.3f ms, max %.3f ms; readers completed %ld reads\n",
           names[kind], n, gave_up, n ? waits[n / 2] : 0.0, n ? waits[n - 1] : 0.0, atomic_load(&reads));
    return 0;
}
