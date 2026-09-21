# PROG 101 · Programming I: Structured Programming in C
## Week 3 · Problem Set 3: Functions, the Call Stack, and Structured Programming

**Released:** Friday 16 October 2026, 10:00 · Week 3 (after Thursday's Lecture 3)
**Due:** Friday 23 October 2026, 17:00 · Week 4 — late penalty from 17:01
**Submission:** Commit to the Freshman Fall repo under `"$PROG101/week3/ps3"`; submit the commit hash on the course portal.
**Total:** 100 points · **Expected time:** about 4 hours

**What this uses:** Weeks 0–3 — everything so far plus functions and pass-by-value, the call stack,
storage duration and scope, multi-file programs, headers and include guards, `static` linkage, `assert`,
and structured programming. To print where a local lives, use the idiom from Lecture 02 and Lab 3:
`printf("%p\n", (void *)&x);` — what `&` and `%p` really are is Week 5.
**Not needed:** arrays (Week 4), pointer parameters (Week 5), `malloc` (Week 6).

**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`

---

## Problem 1: Functions and Pass-by-Value (20 pts)

**1.1** *(6)* Explain the difference between a function **declaration** and a **definition**. Give an
example of a program that is valid with only a declaration visible, and say when the definition must
exist.

**1.2** *(6)* This function does not do what its name suggests:

```c
void swap(int a, int b) { int t = a; a = b; b = t; }
```

Demonstrate the failure with a `main` that prints the addresses of the caller's variables and of the
parameters. Explain the failure **using those addresses**. Do not attempt to fix it — the fix needs
Week 5.

**1.3** *(8)* For each, state whether the caller can observe the change, and why:

(a) a function that assigns to its `int` parameter
(b) a function that assigns to a `static` local
(c) a function that assigns to a global
(d) a function that returns a value the caller assigns

---

## Problem 2: The Call Stack, Scope, and Storage Duration (25 pts)

**2.1** *(8)* Write `frames.c` with four nested functions, each printing the address of one local.
Tabulate the addresses, state whether the stack grows up or down on your machine, and give the
distance between consecutive frames.

**2.2** *(6)* Complete this table:

| Declaration | Scope | Storage duration | Initialised to |
|---|---|---|---|
| `int x;` inside a function | | | |
| `static int x;` inside a function | | | |
| `static int x;` at file level | | | |
| `int x;` at file level | | | |

**2.3** *(6)* `counter()` below returns 1, 2, 3, 4 on successive calls while `automatic()` returns 1
every time. `n` is invisible outside both functions. State precisely what `static` changed.

```c
int counter(void)   { static int n = 0; return ++n; }
int automatic(void) {        int n = 0; return ++n; }
```

**2.4** *(5)* Stack depth is finite. Write a program that recurses without a base case, run it, and
report how it terminates and at roughly what depth. Then state why an infinite *loop* does not fail
the same way.

---

## Problem 3: A Multi-File Program (30 pts)

Build a **running statistics** library across translation units. Values are fed in one at a time, so
the library needs no arrays: it keeps its state in **file-level `static` variables** in `stats.c`
(Lecture 03 §3) — private to that file, alive for the whole run.

**`stats.h`** must declare exactly:

```c
void   stats_reset(void);
void   stats_add(double x);
int    stats_count(void);
double stats_mean(void);
double stats_variance(void);   /* sample variance, denominator n - 1 */
double stats_stddev(void);
double stats_min(void);
double stats_max(void);
```

**3.1** *(12)* Implement `stats.c`. Keep a count, a running sum, a running sum of squares, and the smallest
and largest values seen. Variance is `(Σx² − n·mean²) / (n − 1)`. Link with `-lm` for `sqrt`.

**3.2** *(4)* Write `stats.h` with a correct include guard. Explain what breaks without it.

**3.3** *(6)* Make at least one helper in `stats.c` `static` (e.g. `square`). Then write a separate file
that declares that helper and calls it. Compile and link; record the **exact** error and state which
build stage produced it.

**3.4** *(4)* Write `main.c` that feeds `2, 4, 4, 4, 5, 5, 7, 9` in with `stats_add` and prints every
statistic to 6 decimal places. Expected: mean `5.000000`, variance `4.571429`, stddev `2.138090`,
min `2.000000`, max `9.000000`.

**3.5** *(4)* Write a `Makefile` with correct dependencies so that touching `stats.h` rebuilds both
objects but touching `main.c` rebuilds only one. Demonstrate both cases.

---

## Problem 4: Contracts and Defensive Programming (15 pts)

**4.1** *(5)* State a **precondition** and a **postcondition** for `stats_mean`, and an **invariant** that
holds between calls (what is always true of `count`, `sum` and `sum_sq`). Add them as comments.

**4.2** *(5)* Add `assert` for the preconditions of `stats_mean` and `stats_variance`. Show one firing, and show
that `-DNDEBUG` removes it.

**4.3** *(5)* Assertions are for programmer errors, not user errors. Give one condition in your
`stats` library that **should** be an assertion and one that should **not**, and justify each.

---

## Problem 5: Structured Programming (10 pts)

**5.1** *(5)* State the Böhm–Jacopini theorem and explain what it claims about `goto`.

**5.2** *(5)* Rewrite this using only sequence, selection, and iteration:

```c
int i = 0;
int total = 0;
loop:
    if (i >= n) goto done;
    if (i % 3 == 0) goto skip;
    total += i;
skip:
    i++;
    goto loop;
done:
    printf("%d\n", total);
```

---

## Grading

| Problem | Points | Focus |
|---|---|---|
| 1: Functions and pass-by-value | 20 | The most important rule in C |
| 2: Call stack, scope, storage duration | 25 | Where variables live and for how long |
| 3: Multi-file program | 30 | Header discipline, linkage, separate compilation |
| 4: Contracts | 15 | Assertions as executable documentation |
| 5: Structured programming | 10 | Why three control structures suffice |
| **Total** | **100** | |

**Automatic deductions:** any compiler warning (−3 each); a header without an include guard (−5).

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Code built with gcc 13.3, `-Wall -Wextra -Werror -pedantic -std=c11`; outputs are real.

### Problem 1 (20)

1.1 A declaration gives a name and type (`double stats_mean(void);`); a definition also gives the body or
storage. A call compiles with only the declaration visible; the definition must exist by **link** time, or
the linker reports `undefined reference`. 1.2 The parameters `a`, `b` print different addresses from the
caller's variables — they are copies in `swap`'s own frame, so swapping them changes nothing the caller can
see. 1.3 (a) no — parameter is a copy; (b) not directly (it is invisible outside), but its value persists
into the next call; (c) yes — one object, file scope; (d) yes — through the returned value only.

### Problem 2 (25)

2.1 Nested frames print decreasing addresses on x86-64: the stack grows **down**; spacing is small and
constant for identical frames (16–32 bytes, compiler-dependent — Lecture 02 measured 16).
2.2 `int x;` in a function: block scope, automatic, **indeterminate**. `static int x;` in a function: block
scope, static duration, **0**. `static int x;` at file level: file scope, internal linkage, static, **0**.
`int x;` at file level: file scope, external linkage, static, **0**.
2.3 `static` changed the **storage duration** (one object for the whole run, initialised once), not the
scope. 2.4 It dies with a segmentation fault (stack overflow) after tens of thousands to a few hundred
thousand calls, depending on frame size and the 8 MB default stack; a loop reuses one frame, so it never
grows the stack.

### Problem 3 (30) — reference

`stats.h`:
```c
/* stats.h — running statistics over values fed in one at a time */
#ifndef STATS_H
#define STATS_H

void   stats_reset(void);
void   stats_add(double x);
int    stats_count(void);
double stats_mean(void);
double stats_variance(void);   /* sample variance, denominator n - 1 */
double stats_stddev(void);
double stats_min(void);
double stats_max(void);

#endif
```

`stats.c`:
```c
/* stats.c — the state lives in file-level statics: private to this file, alive for the whole run */
#include <assert.h>
#include <math.h>
#include "stats.h"

static int    count = 0;
static double sum = 0.0;
static double sum_sq = 0.0;
static double lowest = 0.0;
static double highest = 0.0;

static double square(double x) {       /* file-private helper (3.3) */
    return x * x;
}

void stats_reset(void) {
    count = 0;
    sum = 0.0;
    sum_sq = 0.0;
}

void stats_add(double x) {
    if (count == 0 || x < lowest) {
        lowest = x;
    }
    if (count == 0 || x > highest) {
        highest = x;
    }
    count++;
    sum += x;
    sum_sq += square(x);
}

int stats_count(void) {
    return count;
}

double stats_mean(void) {
    assert(count > 0);                  /* precondition: at least one value */
    return sum / count;
}

double stats_variance(void) {
    assert(count > 1);                  /* sample variance needs two values */
    double m = stats_mean();
    return (sum_sq - count * m * m) / (count - 1);
}

double stats_stddev(void) {
    return sqrt(stats_variance());
}

double stats_min(void) {
    assert(count > 0);
    return lowest;
}

double stats_max(void) {
    assert(count > 0);
    return highest;
}
```

`main.c`:
```c
#include <stdio.h>
#include "stats.h"

int main(void) {
    stats_add(2.0); stats_add(4.0); stats_add(4.0); stats_add(4.0);
    stats_add(5.0); stats_add(5.0); stats_add(7.0); stats_add(9.0);
    printf("count    %d\n", stats_count());
    printf("mean     %.6f\n", stats_mean());
    printf("variance %.6f\n", stats_variance());
    printf("stddev   %.6f\n", stats_stddev());
    printf("min      %.6f\n", stats_min());
    printf("max      %.6f\n", stats_max());
    return 0;
}
```

Output: `count 8`, `mean 5.000000`, `variance 4.571429`, `stddev 2.138090`, `min 2.000000`, `max 9.000000`
(matches Python's `statistics.variance`). 3.3, with `sneaky.c` declaring `double square(double);`:
`sneaky.c:(.text+0x15): undefined reference to 'square'` from **ld** — the **link** stage; `static` gave
`square` internal linkage, so no other file can see it. 3.5 `Makefile`:

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -pedantic -std=c11 -g

stats_demo: main.o stats.o
	$(CC) $(CFLAGS) -o $@ main.o stats.o -lm

main.o: main.c stats.h
	$(CC) $(CFLAGS) -c main.c

stats.o: stats.c stats.h
	$(CC) $(CFLAGS) -c stats.c

clean:
	rm -f stats_demo *.o

.PHONY: clean
```

`touch stats.h` → `main.c` and `stats.c` both recompile, then relink; `touch main.c` → only `main.c`.

### Problem 4 (15)

4.1 Pre: `count > 0`. Post: returns `sum / count`. Invariant: `count` values have been added since the last
reset, `sum` is their total and `sum_sq` the total of their squares. 4.2 `stats_mean()` with nothing added:
`stats.c:39: stats_mean: Assertion 'count > 0' failed.` then abort; with `-DNDEBUG` the check vanishes and
the division `0.0 / 0` returns NaN silently. 4.3 Assert: `count > 0` in `stats_mean` — calling it on an
empty set is a programmer error. Not an assert: a non-numeric value typed by a user — that is input to
validate and report, and it must still be handled in a `-DNDEBUG` build.

### Problem 5 (10)

5.1 Any algorithm can be written with sequence, selection and iteration alone; `goto` is never necessary.
5.2:
```c
int total = 0;
for (int i = 0; i < n; i++) {
    if (i % 3 == 0) {
        continue;
    }
    total += i;
}
printf("%d\n", total);
```
For `n = 10`: `1 + 2 + 4 + 5 + 7 + 8 = 27`, same as the `goto` version.

---

*PROG 101 · Week 3 · Problem Set 3 · Due Friday 23 October 2026, 17:00 · © CSE Department*
