# PROG 101 · Problem Set 1 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

*(Revised 2026-09-26: the set no longer asks Problem 2 item 4 (negating −128), or Problem 3's old snippets 4
(1.0/3.0), 6 (octal/hex) and 8 (`unsigned char` wrap). Old snippets 5 and 7 are now 4 and 5. Marks: P2 items
4/4/4/8, P3 4 per snippet + 1, P4 24 (4 per item).)*

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Every program below was compiled with gcc 13.3 on x86-64 Linux and
> run; the outputs are real.

### Problem 1

```c
/* limits.c — PS 1 Problem 1 */
#include <stdio.h>
#include <limits.h>

int main(void) {
    printf("%-15s %6s %22s %22s\n", "type", "bytes", "min", "max");
    printf("%-15s %6zu %22d %22d\n", "signed char", sizeof(signed char), SCHAR_MIN, SCHAR_MAX);
    printf("%-15s %6zu %22d %22u\n", "unsigned char", sizeof(unsigned char), 0, UCHAR_MAX);
    printf("%-15s %6zu %22d %22d\n", "short", sizeof(short), SHRT_MIN, SHRT_MAX);
    printf("%-15s %6zu %22d %22u\n", "unsigned short", sizeof(unsigned short), 0, USHRT_MAX);
    printf("%-15s %6zu %22d %22d\n", "int", sizeof(int), INT_MIN, INT_MAX);
    printf("%-15s %6zu %22d %22u\n", "unsigned int", sizeof(unsigned int), 0, UINT_MAX);
    printf("%-15s %6zu %22ld %22ld\n", "long", sizeof(long), LONG_MIN, LONG_MAX);
    printf("%-15s %6zu %22lld %22lld\n", "long long", sizeof(long long), LLONG_MIN, LLONG_MAX);
    printf("%-15s %6zu\n", "float", sizeof(float));
    printf("%-15s %6zu\n", "double", sizeof(double));
    return 0;
}
```

```
type             bytes                    min                    max
signed char          1                   -128                    127
unsigned char        1                      0                    255
short                2                 -32768                  32767
unsigned short       2                      0                  65535
int                  4            -2147483648             2147483647
unsigned int         4                      0             4294967295
long                 8   -9223372036854775808    9223372036854775807
long long            8   -9223372036854775808    9223372036854775807
float                4
double               8
```

1. Min `−2ⁿ⁻¹`, max `2ⁿ⁻¹ − 1`: `int` (n = 32) → −2147483648 … 2147483647; `short` (16) → −32768 … 32767.
2. Zero takes one of the non-negative patterns, so there is one more negative value than positive.
3. Guaranteed: `sizeof(char) == 1`, minimum ranges (`int` at least 16 bits, `long` at least 32), and the
   ordering `short ≤ int ≤ long ≤ long long`. Everything else (4-byte `int`, 8-byte `long`) is this
   platform (LP64); `long` is 4 bytes on 64-bit Windows.

### Problem 2

1. `42 = 00101010`; `−42 = 11010110` (invert `11010101`, add 1; also `256 − 42 = 214`);
   `127 = 01111111`; `−128 = 10000000`; `−1 = 11111111`.
2. `01100100 + 00011110 = 10000010` = **130** unsigned, **−126** as `signed char` (overflow of the signed range).
3. `(unsigned char)-1 = 255` and `(unsigned char)300 = 44` — conversion **to unsigned** is defined:
   reduce modulo 256. `(signed char)200` is **implementation-defined** (−56 here, with gcc).
4. `+128` does not exist in 8-bit signed; `−(−128)` wraps back to `−128` (the negation overflows).
5. Unsigned arithmetic is defined modulo 2ⁿ, so `UINT_MAX + 1 == 0` always. Signed overflow is undefined:
   the compiler may assume it never happens and optimise accordingly — any result, or none, is allowed.

### Problem 3

```
1: a < b is 0
2: -56
3: 4294967295
4: 0.33333333333333331483
5: 3 -3
6: 8 16
7: 3 -3 1 -1
8: 0
```

1: `−1` converts to `unsigned` (4294967295), so `a < b` is false (**0**). This is the `-Wsign-compare`
warning. 2: `char` is signed here; 200 becomes −56 (implementation-defined). 3: unsigned wraps to
`UINT_MAX`. 4: `1/3` has no exact binary value; digits after the 17th are the stored double's
approximation. 5: conversion truncates **toward zero**. 6: `010` is octal (8), `0x10` hex (16).
7: division truncates toward zero, and `%` takes the sign of the dividend (`−7 % 3 == −1`). 8: `uc + 1` is
computed as `int` 256 (promotion), then converted back to `unsigned char`: 0.

### Problem 4

```
0.1 + 0.2       = 0.30000000000000004
== 0.3?           0
|sum - 0.3| < 1e-9? 1
DBL_EPSILON     = 2.22045e-16
FLT_EPSILON     = 1.19209e-07
16777216f + 1   = 16777216.0
DBL_MAX * 2     = inf
0.0 / 0.0       = -nan; nan == nan is 0; isnan is 1
-0.0 == 0.0 is 1, printed as -0.000000, 1/-0.0 = -inf
```

1: neither 0.1 nor 0.2 is exact in binary; compare with a tolerance. 3: above 2²⁴ a `float` cannot
represent every integer, so `+1` rounds back. 5: NaN is unequal to everything, including itself; glibc
prints it as `-nan` here (the sign bit is set) — accept `nan` or `-nan`. 6: negative zero compares equal to
zero but keeps its sign, which shows in `1/−0.0 = −inf`.

### Problem 5

```
overflow.c:9:5: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
unsigned: UINT_MAX + 1 = 0
signed:   INT_MAX + 1  = -2147483648
```

Only the signed line is reported: unsigned wrap-around is defined behaviour, not an error. At `-O2` the
same numbers print here — but that is luck, not a guarantee; the standard allows anything. `x + 1 < x` can
only be true after an overflow, which a valid program never performs, so the compiler may treat it as
always false and remove it. The correct test is the precondition `x > INT_MAX - 1`.
