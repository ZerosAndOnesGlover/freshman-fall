# PROG 101 · Programming I: Structured Programming in C
## Week 1 · Problem Set 1: Types, Representation, and Conversions

**Released:** Thursday 1 October 2026, 11:00 (after Week 1 Lecture 3) · Week 1
**Due:** Friday 9 October 2026, 17:00 · Week 2 — late penalty from 17:01
**Submission:** Commit to the Freshman Fall repo under `"$PROG101/week1/ps1"`; submit the commit hash on the course portal.
**Points:** 100 · **Expected time:** about 3–4 hours

---

## What this problem set uses

Weeks 0–1 only: the compilation pipeline, `gcc`, `make` and `printf` (Week 0), and this week's types,
`sizeof`, `const`, `<limits.h>` (Lecture 01), two's complement, overflow, promotion and the
signed/unsigned trap, division and modulo signs (Lecture 02), floating point, `<float.h>`, `<math.h>`'s
`fabs` and `isnan`, infinity, NaN, negative zero, and conversions (Lecture 03).

**Every program is a single straight-line `main`.** No `if`, loops, `switch` or `?:` (Week 2), no functions of
your own (Week 3), no arrays or pointers (Weeks 4–5), no structs (Week 7). Where a program needs to report
a true/false result, print the comparison itself: `printf("%d\n", a < b);` prints `1` or `0`.

---

## Problem 1: Integer Types and Their Limits (20 pts)

Create `limits.c`. Print one row per type — `signed char`, `unsigned char`, `short`, `unsigned short`,
`int`, `unsigned int`, `long`, `long long` — with its `sizeof` (use `%zu`) and its minimum and maximum from
`<limits.h>`. Then print `sizeof` for `float` and `double`. Line the columns up with field widths.

In `ps1_answers.md`:

1. *(4 pts)* For a two's-complement type of `n` bits, give the formulas for its minimum and maximum. Check
   them against your `int` and `short` rows.
2. *(4 pts)* Why is the magnitude of `INT_MIN` one larger than `INT_MAX`?
3. *(4 pts)* Which of your rows does the C standard guarantee, and which only happen to hold on this
   machine? (Lecture 01 §3.)

*(8 pts for the program: correct format specifiers, `-Wall -Wextra` clean.)*

---

## Problem 2: Two's Complement by Hand (20 pts)

Answer in `ps1_answers.md`, **showing the bits**. Use 8-bit values throughout.

1. *(4 pts)* Write `42`, `-42`, `127`, `-128` and `-1` in binary. Show `-42` both ways: invert-and-add-one,
   and as `256 − 42`.
2. *(4 pts)* Add `100 + 30` in 8-bit binary. What bit pattern results, and what value does it mean as
   `unsigned char` and as `signed char`?
3. *(4 pts)* What are `(unsigned char)-1`, `(signed char)200` and `(unsigned char)300`? Which of these
   conversions does the standard define exactly, and which is implementation-defined? (Lecture 03 §4.)
4. *(4 pts)* Why is negating `-128` in 8 bits a problem?
5. *(4 pts)* The largest `unsigned int` plus one is `0`. The largest `int` plus one is *undefined
   behaviour*. Explain the difference in one or two sentences each (Lecture 02 §3).

---

## Problem 3: Predict, Then Run (25 pts)

Create `predictions.c` containing these snippets in one `main`. **Write your prediction in a comment above
each before you run it**, then record the real output and a one-sentence explanation in `ps1_answers.md`.

```c
/* Snippet 1 */
int a = -1;
unsigned int b = 1;
printf("1: a < b is %d\n", a < b);

/* Snippet 2 */
char c = 200;              /* char may be signed on your system */
printf("2: %d\n", c);

/* Snippet 3 */
unsigned int u = 0;
u = u - 1;
printf("3: %u\n", u);

/* Snippet 4 */
double d = 1.0 / 3.0;
printf("4: %.20f\n", d);

/* Snippet 5 */
int x = (int)3.9;
int y = (int)-3.9;
printf("5: %d %d\n", x, y);

/* Snippet 6 */
int p = 010;               /* octal literal */
int q = 0x10;              /* hex literal */
printf("6: %d %d\n", p, q);

/* Snippet 7 */
printf("7: %d %d %d %d\n", 7 / 2, -7 / 2, 7 % 3, -7 % 3);

/* Snippet 8 */
unsigned char uc = 255;
uc = uc + 1;
printf("8: %d\n", uc);
```

Compile with `-Wall -Wextra`. One snippet draws a warning: which, and what is the warning telling you?

*(3 pts per snippet — prediction, output, explanation — plus 1 for the warning.)*

---

## Problem 4: Floating Point (20 pts)

Create `floats.c`, a straight-line program that prints:

1. `0.1 + 0.2` with `%.17g`, whether it `== 0.3`, and whether `fabs(sum - 0.3) < 1e-9`
2. `DBL_EPSILON` and `FLT_EPSILON` from `<float.h>`
3. `16777216.0f + 1.0f` printed with `%.1f`
4. `DBL_MAX * 2`
5. `0.0 / 0.0` (compute it from a variable holding `0.0`), whether it equals itself, and `isnan` of it
6. `-0.0 == 0.0`, `-0.0` printed with `%f`, and `1.0 / -0.0`

Link with `-lm`. In `ps1_answers.md`, explain items 1, 3, 5 and 6 in a sentence each (Lecture 03 §2–3).

---

## Problem 5: Overflow, Seen by the Sanitizer (15 pts)

Create `overflow.c`: set `unsigned int u = UINT_MAX;` and `int i = INT_MAX;`, and print `u + 1` and `i + 1`.

1. *(5 pts)* Build with `gcc -Wall -std=c11 -fsanitize=undefined -g` and run it. Paste the runtime report.
   Which line does it name, and why only that one?
2. *(5 pts)* Build again with `-O2` and no sanitizer. What prints? Why does "it printed a number" prove
   nothing (Lecture 02 §3)?
3. *(5 pts)* Lecture 02 shows `if (x + 1 < x)` as a broken overflow check. Without writing an `if`, explain
   in two sentences why the compiler may delete it, and what the correct precondition test is.

---

## Makefile

Use this `Makefile` (TAB-indented recipes). `-Werror` is left off so that Problem 3's deliberate
warning still builds.

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -g -std=c11

PROGRAMS = limits predictions floats overflow

all: $(PROGRAMS)

floats: floats.c
	$(CC) $(CFLAGS) -o $@ $< -lm

overflow: overflow.c
	$(CC) $(CFLAGS) -fsanitize=undefined -o $@ $<

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROGRAMS)

.PHONY: all clean
```

---

## Submission

- `limits.c`, `predictions.c`, `floats.c`, `overflow.c`, `Makefile`, `ps1_answers.md` in `"$PROG101/week1/ps1"`
- All four programs build with `make` and `-Wall -Wextra -std=c11` (Problem 3's one deliberate warning excepted)

## Grading

| Problem | Points |
|---|---|
| 1 Integer types and limits | 20 |
| 2 Two's complement by hand | 20 |
| 3 Predict, then run | 25 |
| 4 Floating point | 20 |
| 5 Overflow and the sanitizer | 15 |
| **Total** | **100** |

---

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
