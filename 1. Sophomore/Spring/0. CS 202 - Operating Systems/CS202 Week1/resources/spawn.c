/* spawn.c: what does it cost to create and destroy a thread, and a process? */
#define _GNU_SOURCE
#include <pthread.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>
static double now(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return t.tv_sec+t.tv_nsec*1e-9; }
static void *nothing(void *a){ return a; }
int main(void)
{
    const int N = 20000;
    double best_t = 1e9, best_p = 1e9;
    for (int rep = 0; rep < 5; rep++) {
        double t0 = now();
        for (int i = 0; i < N; i++) { pthread_t t; pthread_create(&t, 0, nothing, 0); pthread_join(t, 0); }
        double dt = (now() - t0) / N * 1e6; if (dt < best_t) best_t = dt;
        t0 = now();
        for (int i = 0; i < N; i++) { pid_t p = fork(); if (p == 0) _exit(0); waitpid(p, 0, 0); }
        dt = (now() - t0) / N * 1e6; if (dt < best_p) best_p = dt;
    }
    printf("pthread_create + join : %6.1f us\n", best_t);
    printf("fork + _exit + waitpid: %6.1f us   (small parent)\n", best_p);
    printf("ratio: %.1fx\n", best_p / best_t);
    return 0;
}
