/* clocks.c — the clocks a program can read, their resolution, and how far the wall
 * clock drifts from the monotonic one while it runs.  CS 202 Week 11, L34 §4. */
#define _GNU_SOURCE
#include <stdio.h>
#include <time.h>
#include <unistd.h>
int main(void)
{
    struct { const char *name; clockid_t id; } cs[] = {
        { "CLOCK_REALTIME", CLOCK_REALTIME }, { "CLOCK_MONOTONIC", CLOCK_MONOTONIC },
        { "CLOCK_BOOTTIME", CLOCK_BOOTTIME }, { "CLOCK_MONOTONIC_RAW", CLOCK_MONOTONIC_RAW },
    };
    struct timespec r, t;
    for (unsigned i = 0; i < 4; i++) {
        clock_getres(cs[i].id, &r);
        clock_gettime(cs[i].id, &t);
        printf("%-22s resolution %ld ns, now %ld.%09ld\n", cs[i].name, r.tv_nsec, (long)t.tv_sec, r.tv_nsec ? t.tv_nsec : 0);
    }
    struct timespec r0, m0, r1, m1;
    clock_gettime(CLOCK_REALTIME, &r0); clock_gettime(CLOCK_MONOTONIC, &m0);
    sleep(2);
    clock_gettime(CLOCK_REALTIME, &r1); clock_gettime(CLOCK_MONOTONIC, &m1);
    double dr = (r1.tv_sec - r0.tv_sec) + (r1.tv_nsec - r0.tv_nsec) / 1e9;
    double dm = (m1.tv_sec - m0.tv_sec) + (m1.tv_nsec - m0.tv_nsec) / 1e9;
    printf("over a 2 s sleep: realtime advanced %.6f s, monotonic %.6f s, difference %.0f us\n",
           dr, dm, (dr - dm) * 1e6);
    return 0;
}
