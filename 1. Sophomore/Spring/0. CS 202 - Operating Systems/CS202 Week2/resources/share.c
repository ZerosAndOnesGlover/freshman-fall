/* share.c: two CPU hogs on one CPU. How does the scheduler divide the CPU when
 * one of them is nicer, or in a different scheduling class, or in a different
 * session?
 *
 *   gcc -O2 -Wall -Wextra -o share share.c && ./share
 *
 * CS 202 Week 2, L08 §4. */
#define _GNU_SOURCE
#include <errno.h>
#include <sched.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <unistd.h>

#define CPU 6
#define SECONDS 4

static void pin(void) { cpu_set_t s; CPU_ZERO(&s); CPU_SET(CPU, &s); sched_setaffinity(0, sizeof s, &s); }

static unsigned long cpu_ticks(pid_t p)
{
    char path[64], buf[1024];
    snprintf(path, sizeof path, "/proc/%d/stat", (int)p);
    FILE *f = fopen(path, "r"); if (!f) return 0;
    size_t n = fread(buf, 1, sizeof buf - 1, f); fclose(f); buf[n] = 0;
    char *q = strrchr(buf, ')'); unsigned long ut, st;
    if (!q || sscanf(q + 2, "%*c %*d %*d %*d %*d %*d %*u %*u %*u %*u %*u %lu %lu", &ut, &st) != 2) return 0;
    return ut + st;
}

enum how { NICE, IDLE, BATCH, NICE_NEW_SESSION };

static pid_t hog(enum how how, int nice)
{
    int pfd[2]; if (pipe(pfd)) exit(1);
    pid_t p = fork();
    if (p == 0) {
        close(pfd[0]);
        pin();
        if (how == NICE_NEW_SESSION && setsid() < 0) perror("setsid");
        if (how == IDLE)  { struct sched_param sp = {0}; if (sched_setscheduler(0, SCHED_IDLE, &sp)) perror("SCHED_IDLE"); }
        if (how == BATCH) { struct sched_param sp = {0}; if (sched_setscheduler(0, SCHED_BATCH, &sp)) perror("SCHED_BATCH"); }
        if (nice && setpriority(PRIO_PROCESS, 0, nice)) perror("setpriority");
        if (write(pfd[1], "x", 1) != 1) _exit(1);
        close(pfd[1]);
        volatile unsigned long x = 0;
        for (;;) x++;
    }
    close(pfd[1]);
    char c; if (read(pfd[0], &c, 1) != 1) exit(1);
    close(pfd[0]);
    return p;
}

static void trial(const char *label, enum how how_b, int nice_b, double expect)
{
    pid_t a = hog(NICE, 0);
    pid_t b = hog(how_b, nice_b);
    unsigned long a0 = cpu_ticks(a), b0 = cpu_ticks(b);
    sleep(SECONDS);
    unsigned long a1 = cpu_ticks(a), b1 = cpu_ticks(b);
    kill(a, SIGKILL); kill(b, SIGKILL); waitpid(a, 0, 0); waitpid(b, 0, 0);
    double da = a1 - a0, db = b1 - b0, tot = da + db;
    printf("%-34s  A %5.1f%%  B %5.1f%%   (A:B = %6.2f)   weights predict B %5.1f%%\n",
           label, 100 * da / tot, 100 * db / tot, db ? da / db : 0.0, expect);
}

int main(void)
{
    /* Linux's nice-to-weight table: nice 0 = 1024, each step about 1.25x. */
    const struct { int nice; int w; } W[] = { {0,1024}, {1,820}, {5,335}, {10,110}, {19,15} };
    for (size_t i = 0; i < sizeof W / sizeof W[0]; i++) {
        char label[64];
        snprintf(label, sizeof label, "B nice %d, same session", W[i].nice);
        trial(label, NICE, W[i].nice, 100.0 * W[i].w / (1024 + W[i].w));
    }
    trial("B SCHED_BATCH, nice 0", BATCH, 0, 50.0);
    trial("B SCHED_IDLE", IDLE, 0, 100.0 * 3 / (1024 + 3));
    trial("B nice 10, in its own session", NICE_NEW_SESSION, 10, 100.0 * 110 / 1134);
    trial("B nice 19, in its own session", NICE_NEW_SESSION, 19, 100.0 * 15 / 1039);
    return 0;
}
