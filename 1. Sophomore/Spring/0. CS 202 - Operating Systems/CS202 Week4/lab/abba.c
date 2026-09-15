/* abba.c: two threads and two locks, taken in opposite orders.
 *
 *   gcc -O0 -g -Wall -Wextra -pthread -o abba abba.c
 *   ./abba [work] [exit|trap|wait]
 *
 * Thread 1 takes A then B; thread 2 takes B then A. `work` is a loop run while
 * holding the first lock. A watchdog reports a deadlock when no round has
 * completed for one second, prints what /proc says about each thread, and then
 * exits, raises SIGTRAP for a debugger, or waits forever.
 *
 * CS 202 Week 4, L13 §1 and §4-§5; Lab 4.
 */
#define _GNU_SOURCE
#include <dirent.h>
#include <pthread.h>
#include <signal.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

pthread_mutex_t A = PTHREAD_MUTEX_INITIALIZER, B = PTHREAD_MUTEX_INITIALIZER;
static atomic_long rounds;
static long work;

static void *one(void *arg)
{
    (void)arg;
    for (;;) {
        pthread_mutex_lock(&A);
        for (volatile long k = 0; k < work; k++) ;
        pthread_mutex_lock(&B);
        atomic_fetch_add(&rounds, 1);
        pthread_mutex_unlock(&B);
        pthread_mutex_unlock(&A);
    }
    return 0;
}

static void *two(void *arg)
{
    (void)arg;
    for (;;) {
        pthread_mutex_lock(&B);
        for (volatile long k = 0; k < work; k++) ;
        pthread_mutex_lock(&A);
        atomic_fetch_add(&rounds, 1);
        pthread_mutex_unlock(&A);
        pthread_mutex_unlock(&B);
    }
    return 0;
}

static void show_proc(void)
{
    DIR *d = opendir("/proc/self/task");
    struct dirent *e;
    while ((e = readdir(d))) {
        if (e->d_name[0] == '.') continue;
        char path[300], buf[256] = "", wchan[64] = "", sys[128] = "";
        FILE *f;
        snprintf(path, sizeof path, "/proc/self/task/%s/stat", e->d_name);
        if ((f = fopen(path, "r"))) { if (!fgets(buf, sizeof buf, f)) buf[0] = 0; fclose(f); }
        char *rp = strrchr(buf, ')');
        snprintf(path, sizeof path, "/proc/self/task/%s/wchan", e->d_name);
        if ((f = fopen(path, "r"))) { if (!fgets(wchan, sizeof wchan, f)) wchan[0] = 0; fclose(f); }
        snprintf(path, sizeof path, "/proc/self/task/%s/syscall", e->d_name);
        if ((f = fopen(path, "r"))) { if (!fgets(sys, sizeof sys, f)) sys[0] = 0; fclose(f); }
        sys[strcspn(sys, "\n")] = 0;
        printf("  task %s: state %c, wchan %-16s syscall %s\n", e->d_name, rp ? rp[2] : '?', wchan, sys);
    }
    closedir(d);
    printf("  &A = %p, &B = %p\n", (void *)&A, (void *)&B);
    printf("  A is owned by TID %d, B by TID %d\n", A.__data.__owner, B.__data.__owner);
}

int main(int argc, char **argv)
{
    work = argc > 1 ? atol(argv[1]) : 0;
    const char *then = argc > 2 ? argv[2] : "exit";
    pthread_t t1, t2;
    pthread_create(&t1, 0, one, 0);
    pthread_create(&t2, 0, two, 0);
    long last = -1;
    for (;;) {
        usleep(1000000);
        long r = atomic_load(&rounds);
        if (r == last) break;
        last = r;
    }
    printf("DEADLOCK after %ld rounds\n", last);
    show_proc();
    fflush(stdout);
    if (!strcmp(then, "trap")) raise(SIGTRAP);
    if (!strcmp(then, "wait")) for (;;) pause();
    _exit(1);
}
