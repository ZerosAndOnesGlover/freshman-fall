/* PROG 202 · Week 0 · L01 §3
 * What purity buys a compiler, in C, where it has to be proved.
 *
 *   gcc -O2 -Wall -Wextra -o cse cse.c
 *   ./cse a 1000000000     pure_sum   once    0.44 s
 *   ./cse b 1000000000     pure_sum   twice   0.44 s   <- GCC ran the loop once
 *   ./cse c 1000000000     impure_sum once    0.44 s
 *   ./cse d 1000000000     impure_sum twice   0.88 s   <- and here it could not
 *
 * The two functions have byte-identical arithmetic.  impure_sum has one extra
 * line, `calls++`, incrementing a global that nothing in this program reads.
 * That line costs 0.44 seconds, because it makes two calls distinguishable
 * from one.  Making `calls` static does NOT win the optimisation back (0.89 s
 * measured): GCC's analysis is conservative.  GHC never has to do this
 * analysis, because there is no way to write the line -- see cse.hs.
 */
#include <stdio.h>
#include <stdlib.h>

long calls = 0;

/* Pure: no globals, no I/O.  GCC can see the whole body. */
__attribute__((noinline))
long pure_sum(long n) { long s = 0; for (long i = 1; i <= n; i++) s += i; return s; }

/* Identical arithmetic, plus one observable write. */
__attribute__((noinline))
long impure_sum(long n) { long s = 0; for (long i = 1; i <= n; i++) s += i; calls++; return s; }

int main(int argc, char **argv) {
    (void)argc;
    long n = atol(argv[2]);
    long r;
    switch (argv[1][0]) {
      case 'a': r = pure_sum(n);                 break;  /* pure,   once  */
      case 'b': r = pure_sum(n)   + pure_sum(n);  break;  /* pure,   twice */
      case 'c': r = impure_sum(n);               break;  /* impure, once  */
      default : r = impure_sum(n) + impure_sum(n); break; /* impure, twice */
    }
    printf("%ld\n", r);
    return 0;
}
