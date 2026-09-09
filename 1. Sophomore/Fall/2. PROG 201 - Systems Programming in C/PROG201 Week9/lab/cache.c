/* The memory hierarchy, measured from userspace. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec/1e9;}
#define KEEP(x) __asm__ volatile("" :: "r,m"(x) : "memory")

/* 1. working-set size: a pointer chase over a shuffled ring of N bytes.
 *    Dependent loads, so this measures LATENCY at each level. */
static double chase(size_t bytes, long iters)
{
    size_t n = bytes / sizeof(size_t);
    if (n < 2) return 0;
    size_t *a = aligned_alloc(64, n * sizeof *a);
    size_t *idx = malloc(n * sizeof *idx);
    for (size_t i = 0; i < n; i++) idx[i] = i;
    for (size_t i = n - 1; i > 0; i--) { size_t j = (size_t) rand() % (i + 1);
                                        size_t t = idx[i]; idx[i] = idx[j]; idx[j] = t; }
    for (size_t i = 0; i < n; i++) a[idx[i]] = idx[(i + 1) % n];   /* one cycle */
    size_t p = 0;
    double t0 = now();
    for (long i = 0; i < iters; i++) p = a[p];
    double dt = now() - t0;
    KEEP(p);
    free(a); free(idx);
    return dt / iters * 1e9;
}

/* 2. stride: touch one int every `stride` ints across a fixed buffer */
static double stride_scan(int *a, size_t n, size_t stride)
{
    long sum = 0;
    double t0 = now();
    for (size_t i = 0; i < n; i += stride) sum += a[i];
    double dt = now() - t0;
    KEEP(sum);
    return dt / (double)(n / stride) * 1e9;         /* ns per element touched */
}

int main(void)
{
    printf("=== latency against working-set size (random pointer chase) ===\n");
    printf("  %10s %12s\n", "size", "ns/access");
    size_t sizes[] = { 8<<10, 32<<10, 128<<10, 256<<10, 1<<20, 4<<20, 16<<20, 64<<20, 256u<<20 };
    for (unsigned i = 0; i < sizeof sizes/sizeof *sizes; i++) {
        double ns = chase(sizes[i], 3000000);
        if (sizes[i] >= (1u<<20)) printf("  %8zu MiB %12.2f\n", sizes[i]>>20, ns);
        else                      printf("  %8zu KiB %12.2f\n", sizes[i]>>10, ns);
    }

    printf("\n=== stride: 64 MiB of int, touching one every `stride` ===\n");
    size_t n = (64u<<20)/sizeof(int);
    int *a = aligned_alloc(64, n * sizeof *a);
    memset(a, 1, n * sizeof *a);
    printf("  %8s %10s %14s\n", "stride", "bytes", "ns/element");
    for (size_t s = 1; s <= 64; s *= 2) 
        printf("  %8zu %10zu %14.2f\n", s, s*sizeof(int), stride_scan(a, n, s));
    free(a);
    return 0;
}
