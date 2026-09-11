/* lat.c: ask to wake up every millisecond, and measure how late the wake-up is,
 * while other processes compete for the same CPU.
 *
 *   gcc -O2 -Wall -Wextra -o lat lat.c
 *   ./lat           with the default 50-microsecond timer slack
 *   ./lat slack     with timer slack set to 1 ns
 *
 * CS 202 Week 2, L09 §6. */
#define _GNU_SOURCE
#include <sched.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/prctl.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define CPU 7
#define N 3000
static void pin(void){ cpu_set_t s; CPU_ZERO(&s); CPU_SET(CPU,&s); sched_setaffinity(0,sizeof s,&s); }
static int cmp(const void *a, const void *b){ long x=*(long*)a, y=*(long*)b; return (x>y)-(x<y); }

static void measure(const char *label, int hogs, int nice, int idle)
{
    pid_t pids[8];
    for (int i = 0; i < hogs; i++) {
        if ((pids[i] = fork()) == 0) {
            pin();
            if (idle) { struct sched_param sp = {0}; sched_setscheduler(0, SCHED_IDLE, &sp); }
            if (nice) setpriority(PRIO_PROCESS, 0, nice);
            volatile unsigned long x = 0; for (;;) x++;
        }
    }
    pin();
    usleep(200000);
    static long late[N];
    struct timespec next; clock_gettime(CLOCK_MONOTONIC, &next);
    for (int i = 0; i < N; i++) {
        next.tv_nsec += 1000000; if (next.tv_nsec >= 1000000000) { next.tv_nsec -= 1000000000; next.tv_sec++; }
        clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next, 0);
        struct timespec now; clock_gettime(CLOCK_MONOTONIC, &now);
        late[i] = (now.tv_sec - next.tv_sec) * 1000000000L + (now.tv_nsec - next.tv_nsec);
    }
    for (int i = 0; i < hogs; i++) { kill(pids[i], SIGKILL); waitpid(pids[i], 0, 0); }
    qsort(late, N, sizeof(long), cmp);
    printf("%-30s wake-up lateness: median %7.3f ms  p99 %7.3f ms  max %7.3f ms\n",
           label, late[N/2]/1e6, late[N*99/100]/1e6, late[N-1]/1e6);
}

int main(int argc, char **argv)
{
    (void)argv;
    if (argc > 1) { prctl(PR_SET_TIMERSLACK, 1UL); printf("timer slack set to %ld ns\n", (long)prctl(PR_GET_TIMERSLACK)); }
    measure("no competition", 0, 0, 0);
    measure("3 hogs, nice 0", 3, 0, 0);
    measure("3 hogs, nice 19", 3, 19, 0);
    measure("3 hogs, SCHED_IDLE", 3, 0, 1);
    return 0;
}
