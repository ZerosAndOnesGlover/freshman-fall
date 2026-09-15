/* forkcost.c — time fork() and the child's first write to every page, for a parent
 * with 0 to 1 GiB of touched anonymous memory.
 *   gcc -O2 -Wall -Wextra -o forkcost forkcost.c && taskset -c 2 ./forkcost
 * CS 202 Week 5, L18 §4. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <sys/resource.h>

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }

int main(void)
{
    static const size_t sizes[] = { 0, 64, 256, 1024 };
    for (size_t k = 0; k < 4; k++) {
        size_t bytes = sizes[k] << 20;
        char *p = bytes ? mmap(0, bytes, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0) : 0;
        if (bytes) { madvise(p, bytes, MADV_NOHUGEPAGE); memset(p, 1, bytes); }
        int fds[2]; if (pipe(fds)) return 1;
        double t0 = now();
        pid_t c = fork();
        if (c == 0) {
            double t1 = now();
            struct rusage r0, r1; getrusage(RUSAGE_SELF, &r0);
            double w0 = now();
            for (size_t i = 0; i < bytes; i += 4096) p[i] = 2;
            double w1 = now();
            getrusage(RUSAGE_SELF, &r1);
            double v[3] = { t1 - t0, w1 - w0, (double)(r1.ru_minflt - r0.ru_minflt) };
            if (write(fds[1], v, sizeof v) != sizeof v) _exit(1);
            _exit(0);
        }
        double v[3];
        if (read(fds[0], v, sizeof v) != sizeof v) return 1;
        waitpid(c, 0, 0);
        printf("%5zu MiB touched: fork %8.3f ms   child writes every page: %8.1f ms, %7.0f faults, %6.0f ns per fault\n",
               sizes[k], v[0] * 1e3, v[1] * 1e3, v[2], v[2] ? v[1] * 1e9 / v[2] : 0);
        if (bytes) munmap(p, bytes);
        close(fds[0]); close(fds[1]);
    }
    return 0;
}
