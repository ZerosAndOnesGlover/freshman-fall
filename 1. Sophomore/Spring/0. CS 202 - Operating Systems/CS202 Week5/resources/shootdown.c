/* shootdown.c — what unmapping costs when another thread of the same process
 * is running on another CPU, and how many TLB-shootdown interrupts it sends.
 *   gcc -O2 -Wall -Wextra -pthread -o shootdown shootdown.c
 *   taskset -c 2,3 ./shootdown 0      # no other thread
 *   taskset -c 2,3 ./shootdown 1      # one other thread, busy on CPU 3
 *   taskset -c 2,3 ./shootdown 2      # one other thread, asleep
 * CS 202 Week 5, L17 §5. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sched.h>
#include <unistd.h>
#include <pthread.h>
#include <stdatomic.h>
#include <sys/mman.h>

#define ROUNDS 200000

static atomic_int stop;

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

static long tlb_total(void)
{
    FILE *f = fopen("/proc/interrupts", "r");
    char line[4096];
    long total = 0;
    while (fgets(line, sizeof line, f)) {
        char *s = line;
        while (*s == ' ') s++;
        if (strncmp(s, "TLB:", 4)) continue;
        s += 4;
        char *end;
        for (;;) {
            long v = strtol(s, &end, 10);
            if (end == s) break;
            total += v;
            s = end;
        }
    }
    fclose(f);
    return total;
}

static void pin(int cpu)
{
    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(cpu, &set);
    pthread_setaffinity_np(pthread_self(), sizeof set, &set);
}

static void *busy(void *arg)
{
    (void)arg;
    pin(3);
    volatile unsigned long n = 0;
    while (!atomic_load(&stop)) n++;
    return 0;
}

static void *sleepy(void *arg)
{
    (void)arg;
    pin(3);
    while (!atomic_load(&stop)) usleep(100000);
    return 0;
}

int main(int argc, char **argv)
{
    int mode = argc > 1 ? atoi(argv[1]) : 0;
    pthread_t t;
    pin(2);
    if (mode == 1) pthread_create(&t, 0, busy, 0);
    if (mode == 2) pthread_create(&t, 0, sleepy, 0);
    usleep(200000);

    long i0 = tlb_total();
    double t0 = now();
    for (int r = 0; r < ROUNDS; r++) {
        char *p = mmap(0, 4096, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
        p[0] = 1;                       /* fault it in, so there is a translation to flush */
        munmap(p, 4096);
    }
    double t1 = now();
    long i1 = tlb_total();

    atomic_store(&stop, 1);
    if (mode) pthread_join(t, 0);
    printf("%-26s %8.0f ns per mmap+touch+munmap   TLB shootdown interrupts: %ld (%.2f per round)\n",
           mode == 0 ? "single thread" : mode == 1 ? "second thread busy" : "second thread asleep",
           (t1 - t0) * 1e9 / ROUNDS, i1 - i0, (double)(i1 - i0) / ROUNDS);
    return 0;
}
