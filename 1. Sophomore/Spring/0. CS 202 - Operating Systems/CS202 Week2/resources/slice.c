/* slice.c: how long does a CPU hog actually run before it is preempted, and for
 * how long is it off the CPU? N hogs share one CPU; each watches the clock in a
 * tight loop and treats any jump over 100 microseconds as time it did not run.
 *
 *   gcc -O2 -Wall -Wextra -o slice slice.c && ./slice 2
 *
 * CS 202 Week 2, L08 §6. */
#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define CPU 7
#define SECONDS 3
#define MAXREC 20000

static long ns(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return t.tv_sec*1000000000L+t.tv_nsec; }
static int cmp(const void *a, const void *b){ long x=*(long*)a, y=*(long*)b; return (x>y)-(x<y); }

int main(int argc, char **argv)
{
    int n = argc > 1 ? atoi(argv[1]) : 2;
    long *runs = mmap(0, sizeof(long) * MAXREC * 2, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0);
    long *gaps = runs + MAXREC;
    for (int k = 0; k < n; k++) {
        if (fork() == 0) {
            cpu_set_t s; CPU_ZERO(&s); CPU_SET(CPU, &s); sched_setaffinity(0, sizeof s, &s);
            long start = ns(), last = start, run_start = start;
            int nr = 0;
            while (last - start < SECONDS * 1000000000L) {
                long t = ns();
                if (t - last > 100000) {                 /* we were off the CPU */
                    if (k == 0 && nr < MAXREC && run_start != start) { runs[nr] = last - run_start; gaps[nr] = t - last; nr++; }
                    run_start = t;
                }
                last = t;
            }
            if (k == 0) runs[MAXREC*2-1] = nr;
            _exit(0);
        }
    }
    while (wait(0) > 0) ;
    int nr = (int)runs[MAXREC*2-1];
    qsort(runs, nr, sizeof(long), cmp); qsort(gaps, nr, sizeof(long), cmp);
    printf("%d hogs on CPU %d: hog 0 was preempted %d times in %d s; run length median %.2f ms (p10 %.2f, p90 %.2f); time off CPU median %.2f ms (p90 %.2f)\n",
        n, CPU, nr, SECONDS, runs[nr/2]/1e6, runs[nr/10]/1e6, runs[nr*9/10]/1e6, gaps[nr/2]/1e6, gaps[nr*9/10]/1e6);
    return 0;
}
