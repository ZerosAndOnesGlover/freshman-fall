/* PROG 201 -- Lab 9: the roofline model, measured on your own machine.
 *
 *   make
 *   ./roof
 *
 * Two ceilings and a set of kernels.  The kernels are provided; the ceilings
 * are TODO 1 and TODO 2, and getting the first one right is the lab.
 *
 * KEEP() below is not decoration.  Remove it from any loop and gcc deletes
 * the loop, and the loop then runs in zero seconds -- see section 4 of the
 * lab sheet, and L30 section 5.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>

static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec/1e9;}

/* Tell the compiler a value has escaped, so it cannot delete the code that
 * produced it.  This is what every benchmarking library calls DoNotOptimize,
 * and without it half of section 1 of the lab measures nothing. */
#define KEEP(x) __asm__ volatile("" :: "r,m"(x) : "memory")

/* TODO 1.  Ceiling one: memory bandwidth.
 *
 * Stream a buffer far larger than the last-level cache and report the best
 * GB/s over `reps` runs.  The buffer is allocated and touched for you.
 *
 * The obvious loop is
 *
 *     for (size_t i = 0; i < n; i++) s += a[i];
 *
 * and it is WRONG for this purpose.  Write it that way first, note the
 * number, then read section 3 of the lab sheet and fix it.  Q2 asks for both
 * numbers, so do not skip the wrong one.
 *
 * Report bytes/seconds/1e9, and KEEP() every accumulator.
 */
static double bandwidth(size_t bytes, int reps)
{
    double *a = aligned_alloc(64, bytes);
    memset(a, 1, bytes);
    size_t n = bytes / sizeof *a;
    (void) n; (void) reps;
    free(a);
    return 1.0;                          /* TODO 1 */
}

/* TODO 2.  Ceiling two: arithmetic peak.
 *
 * Do fused multiply-adds and nothing else -- no array, no memory traffic at
 * all.  Use EIGHT independent accumulators for the same reason as TODO 1: one
 * chain measures FMA latency, several measure throughput.
 *
 *     a0 = a0*k + 1.0;  a1 = a1*k + 1.0;  ...
 *
 * Each FMA is 2 flops.  Report the best GFLOP/s over `reps` runs, and KEEP()
 * every accumulator.
 */
static double flops(long iters, int reps)
{
    (void) iters; (void) reps;
    return 1.0;                          /* TODO 2 */
}

/* --- kernels with different arithmetic intensity --- */
struct result { const char *name; double ai; double gflops; double gbs; };

static struct result k_copy(double *a, double *b, size_t n)
{   /* 0 flops, 16 bytes moved per element */
    double t0 = now();
    for (size_t i = 0; i < n; i++) b[i] = a[i];
    double dt = now() - t0;
    KEEP(b);
    return (struct result){ "copy", 0.0, 0.0, n * 16.0 / dt / 1e9 };
}

static struct result k_sum(double *a, size_t n)
{   /* 1 flop per 8 bytes -> AI = 0.125 */
    double s = 0;
    double t0 = now();
    for (size_t i = 0; i < n; i++) s += a[i];
    double dt = now() - t0;
    KEEP(s);
    return (struct result){ "sum (1 acc)", 1.0/8.0, n / dt / 1e9, n * 8.0 / dt / 1e9 };
}

static struct result k_axpy(double *a, double *b, size_t n)
{   /* 2 flops per 24 bytes (read a, read b, write b) -> AI = 0.083 */
    double t0 = now();
    for (size_t i = 0; i < n; i++) b[i] = 2.5 * a[i] + b[i];
    double dt = now() - t0;
    KEEP(b);
    return (struct result){ "axpy", 2.0/24.0, n * 2.0 / dt / 1e9, n * 24.0 / dt / 1e9 };
}

static struct result k_poly(double *a, size_t n, int deg)
{   /* deg*2 flops per 8 bytes -- turn the dial */
    double s = 0;
    double t0 = now();
    for (size_t i = 0; i < n; i++) {
        double x = a[i], p = 1.0;
        for (int d = 0; d < deg; d++) p = p * x + (double) d;
        s += p;
    }
    double dt = now() - t0;
    KEEP(s);
    static char name[8][32];
    static int slot;
    int me = slot++ & 7;
    snprintf(name[me], sizeof name[me], "poly(deg %d)", deg);
    return (struct result){ name[me], deg * 2.0 / 8.0, n * deg * 2.0 / dt / 1e9, n * 8.0 / dt / 1e9 };
}

/* the same arithmetic intensity, but four independent dependency chains */
static struct result k_poly4(double *a, size_t n, int deg)
{
    double s = 0;
    double t0 = now();
    for (size_t i = 0; i + 3 < n; i += 4) {
        double x0=a[i], x1=a[i+1], x2=a[i+2], x3=a[i+3];
        double p0=1, p1=1, p2=1, p3=1;
        for (int d = 0; d < deg; d++) {
            p0 = p0*x0 + (double) d; p1 = p1*x1 + (double) d;
            p2 = p2*x2 + (double) d; p3 = p3*x3 + (double) d;
        }
        s += p0 + p1 + p2 + p3;
    }
    double dt = now() - t0;
    KEEP(s);
    static char nm[8][32];
    static int slot4;
    int me = slot4++ & 7;
    snprintf(nm[me], sizeof nm[me], "poly4(deg %d)", deg);
    return (struct result){ nm[me], deg * 2.0 / 8.0, n * deg * 2.0 / dt / 1e9, n * 8.0 / dt / 1e9 };
}

int main(void)
{
    size_t bytes = 256u << 20;               /* 256 MiB: far past any cache */
    printf("=== the two ceilings ===\n");
    double bw = bandwidth(bytes, 3);
    double pk = flops(50000000, 3);
    printf("  memory bandwidth   %8.2f GB/s   (256 MiB streaming read)\n", bw);
    printf("  arithmetic peak    %8.2f GFLOP/s (independent FMAs, no memory)\n", pk);
    printf("  ridge point        %8.2f flops/byte\n\n", pk / bw);

    size_t n = bytes / sizeof(double);
    double *a = aligned_alloc(64, bytes), *b = aligned_alloc(64, bytes);
    for (size_t i = 0; i < n; i++) { a[i] = 1.0 + i * 1e-9; b[i] = 2.0; }

    printf("=== kernels ===\n");
    printf("  %-14s %10s %12s %12s %10s\n", "kernel", "AI", "GFLOP/s", "GB/s", "% of roof");
    struct result rs[10];
    int k = 0;
    rs[k++] = k_sum(a, n);
    rs[k++] = k_axpy(a, b, n);
    rs[k++] = k_copy(a, b, n);
    rs[k++] = k_poly (a, n / 16, 16);
    rs[k++] = k_poly4(a, n / 16, 16);
    rs[k++] = k_poly (a, n / 16, 64);
    rs[k++] = k_poly4(a, n / 16, 64);
    for (int i = 0; i < k; i++) {
        double roof = rs[i].ai * bw < pk ? rs[i].ai * bw : pk;
        printf("  %-14s %10.3f %12.2f %12.2f %9.0f%%\n",
               rs[i].name, rs[i].ai, rs[i].gflops, rs[i].gbs,
               roof > 0 ? 100.0 * rs[i].gflops / roof : 0.0);
    }
    free(a); free(b);
    return 0;
}
