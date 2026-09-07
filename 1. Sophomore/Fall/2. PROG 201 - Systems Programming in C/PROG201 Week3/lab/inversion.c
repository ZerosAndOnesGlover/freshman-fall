/* PROG 201 -- Lab 3: priority inversion, and what actually fixes it.
 *
 * Three threads pinned to ONE cpu:
 *   L (low)     nice 19, takes the lock and does a fixed amount of work
 *   M (medium)  nice 0,  burns cpu and never touches the lock
 *   H (high)    nice 0,  wants the lock, and times how long it waits
 *
 *   make
 *   ./inversion                    baseline: L and H only
 *   ./inversion m                  add the burners      <- the bug
 *   ./inversion m pi               ... with PTHREAD_PRIO_INHERIT
 *   ./inversion m nice0            ... with L at nice 0
 *   ./inversion m chunks=100       ... with a chunked critical section
 *
 * WARNING: `./inversion m` takes about a hundred seconds.  That is the point.
 * Start it, then read section 3 of the lab sheet while it runs.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sched.h>
#include <time.h>
#include <sys/resource.h>

#define WORK_UNITS 3000

static pthread_mutex_t lock;
static volatile int    stop;          /* tells the burners to finish        */
static volatile int    low_has_lock;  /* H waits for this before it starts  */
static int             low_nice = 19;
static int             chunks   = 1;

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec / 1e9;
}

/* All three threads run on cpu 0.  Without this there is no contention on an
 * eight-cpu machine and there is nothing to see. */
static void pin(void)
{
    cpu_set_t s;
    CPU_ZERO(&s);
    CPU_SET(0, &s);
    if (pthread_setaffinity_np(pthread_self(), sizeof s, &s) != 0)
        perror("setaffinity");
}

/* A fixed amount of WORK, not a fixed amount of time.  Starve the thread
 * doing this and it takes longer in wall-clock terms -- which is the entire
 * phenomenon.  If you rewrite this as a sleep or a timed loop, the lab
 * measures nothing. */
static void work(long units)
{
    volatile unsigned long x = 0;
    for (long u = 0; u < units; u++)
        for (int i = 0; i < 100000; i++) x++;
}

/* TODO 1.  The low-priority thread.
 *
 *   pin();
 *   setpriority(PRIO_PROCESS, 0, low_nice);
 *   then, `chunks` times:
 *       take the lock, set low_has_lock, do WORK_UNITS/chunks of work,
 *       release the lock.
 *
 * With chunks == 1 that is one long critical section, which is the bug.
 * Part D uses a larger number. */
static void *low(void *arg)
{
    (void) arg;
    pin();
    return NULL;
}

/* TODO 2.  The high-priority thread.
 *
 *   pin();
 *   setpriority(PRIO_PROCESS, 0, 0);
 *   spin on sched_yield() until low_has_lock -- otherwise H may take the
 *       lock first and measure nothing;
 *   then time pthread_mutex_lock, store the wait through `arg`, and unlock.
 *
 * `arg` is a double *. */
static void *high(void *arg)
{
    (void) arg;
    pin();
    return NULL;
}

/* TODO 3.  The medium thread.  nice 0, never touches the lock, burns cpu in a
 * loop until `stop` is set.  Three of these are created. */
static void *medium(void *arg)
{
    (void) arg;
    pin();
    return NULL;
}

int main(int argc, char **argv)
{
    int with_m = 0, pi = 0;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "m"))          with_m = 1;
        if (!strcmp(argv[i], "pi"))         pi = 1;
        if (!strcmp(argv[i], "nice0"))      low_nice = 0;
        if (!strncmp(argv[i], "chunks=", 7)) chunks = atoi(argv[i] + 7);
    }

    /* Calibration: how long is WORK_UNITS on this machine, uncontended?
     * Every number the lab asks for is a multiple of this one. */
    double t0 = now();
    work(WORK_UNITS / 10);
    printf("calibration: %ld work units take %.3f s alone\n",
           (long) WORK_UNITS, (now() - t0) * 10);

    pthread_mutexattr_t a;
    pthread_mutexattr_init(&a);
    /* TODO 4.  When `pi` is set, ask for PTHREAD_PRIO_INHERIT here, and
     * report it if the call fails.  Then read what it actually did. */
    if (pthread_mutex_init(&lock, &a) != 0) { perror("mutex_init"); return 1; }

    pthread_t tl, tm[3], th;
    double waited = -1;

    pthread_create(&tl, NULL, low, NULL);
    if (with_m) for (int i = 0; i < 3; i++) pthread_create(&tm[i], NULL, medium, NULL);
    pthread_create(&th, NULL, high, &waited);

    pthread_join(th, NULL);
    pthread_join(tl, NULL);
    stop = 1;
    if (with_m) for (int i = 0; i < 3; i++) pthread_join(tm[i], NULL);

    char label[80];
    snprintf(label, sizeof label, "%s%s, L at nice %d, %d chunk%s",
             with_m ? "3 burners" : "no burners", pi ? " + PRIO_INHERIT" : "",
             low_nice, chunks, chunks == 1 ? "" : "s");
    printf("%-48s high waited %8.3f s\n", label, waited);
    return 0;
}
