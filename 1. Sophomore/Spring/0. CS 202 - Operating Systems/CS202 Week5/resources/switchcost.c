/* switchcost.c — one byte passed back and forth over two pipes, between two
 * threads of one process (same page tables) or two processes (different page
 * tables), both pinned to one CPU so that every hand-off is a context switch.
 *   gcc -O2 -Wall -Wextra -pthread -o switchcost switchcost.c
 *   taskset -c 2 ./switchcost
 * CS 202 Week 5, L17 §3. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/wait.h>

#define ROUNDS 500000

static int ab[2], ba[2];

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

static void *echo(void *arg)
{
    (void)arg;
    char c;
    for (int i = 0; i < ROUNDS; i++) {
        if (read(ab[0], &c, 1) != 1) break;
        if (write(ba[1], &c, 1) != 1) break;
    }
    return 0;
}

static double drive(void)
{
    char c = 'x';
    double t0 = now();
    for (int i = 0; i < ROUNDS; i++) {
        if (write(ab[1], &c, 1) != 1 || read(ba[0], &c, 1) != 1) { perror("pipe"); exit(1); }
    }
    return (now() - t0) * 1e9 / ROUNDS / 2;     /* two switches per round */
}

int main(void)
{
    for (int rep = 0; rep < 3; rep++) {
        if (pipe(ab) || pipe(ba)) return 1;
        pthread_t t;
        pthread_create(&t, 0, echo, 0);
        double th = drive();
        pthread_join(t, 0);
        close(ab[0]); close(ab[1]); close(ba[0]); close(ba[1]);

        if (pipe(ab) || pipe(ba)) return 1;
        pid_t p = fork();
        if (p == 0) { echo(0); _exit(0); }
        double pr = drive();
        waitpid(p, 0, 0);
        close(ab[0]); close(ab[1]); close(ba[0]); close(ba[1]);

        printf("threads: %6.0f ns per switch   processes: %6.0f ns per switch\n", th, pr);
    }
    return 0;
}
