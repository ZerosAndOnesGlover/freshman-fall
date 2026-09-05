// CS 211 Week 12.  The same computation, four languages.
// Naive recursive Fibonacci: no data structures, no I/O, no library calls --
// just function calls and addition, so what is measured is the language's
// call and arithmetic path rather than its standard library.
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
static long fib(long n) { return n < 2 ? n : fib(n-1) + fib(n-2); }
int main(int argc, char **argv) {
    long n = argc > 1 ? atol(argv[1]) : 30;
    struct timespec a, b;
    clock_gettime(CLOCK_MONOTONIC, &a);
    long r = fib(n);
    clock_gettime(CLOCK_MONOTONIC, &b);
    printf("  %-12s fib(%ld) = %-10ld %8.3f s\n", "C (gcc -O2)", n, r,
           (b.tv_sec-a.tv_sec) + (b.tv_nsec-a.tv_nsec)/1e9);
    return 0;
}
