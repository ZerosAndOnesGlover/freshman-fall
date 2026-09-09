/* LAB 11 -- what does isolation cost to start? Times three creation paths,
 * averaged over many iterations: a plain fork, a bare clone, and a clone that
 * creates all six namespaces (a container). Compare the last to a VM's boot
 * (seconds) -- see L36.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <sched.h>
#include <signal.h>
#include <string.h>
#include <time.h>
#include <sys/wait.h>

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec / 1e9; }
static char stk[1 << 20];
static int c0(void *a) { (void)a; return 0; }

int main(void)
{
    int N = 2000; double t0;

    t0 = now();
    for (int i = 0; i < N; i++) { pid_t p = fork(); if (p == 0) _exit(0); waitpid(p, 0, 0); }
    printf("fork+wait                          : %6.1f us\n", (now() - t0) / N * 1e6);

    t0 = now();
    for (int i = 0; i < N; i++) { pid_t p = clone(c0, stk + sizeof stk, SIGCHLD, 0); waitpid(p, 0, 0); }
    printf("clone (no namespaces)              : %6.1f us\n", (now() - t0) / N * 1e6);

    N = 500;
    t0 = now();
    for (int i = 0; i < N; i++) {
        pid_t p = clone(c0, stk + sizeof stk,
                        CLONE_NEWUSER | CLONE_NEWPID | CLONE_NEWNET |
                        CLONE_NEWNS | CLONE_NEWUTS | CLONE_NEWIPC | SIGCHLD, 0);
        if (p < 0) { perror("clone"); break; }
        waitpid(p, 0, 0);
    }
    printf("clone + 6 namespaces (a container) : %6.1f us\n", (now() - t0) / N * 1e6);
    return 0;
}
