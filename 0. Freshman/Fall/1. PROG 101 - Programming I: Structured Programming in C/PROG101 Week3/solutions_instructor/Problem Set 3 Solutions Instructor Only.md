# PROG 101 · Problem Set 3 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

*(Revised 2026-09-26: old 1.2, 2.1, 2.3, 2.4, 3.3 and 4.2 are no longer on the set — Lab 3 works most of them —
so their answers below can be ignored. Renumbered: 1.3 → 1.2, 2.2 → Problem 2, 3.4 → 3.3, 3.5 → 3.4, 4.3 → 4.2.
Marks: 1.1 10, 1.2 12, P2 10, 3.1 20, 3.2 6, 3.3 6, 3.4 8, 4.1 8, 4.2 6, 5.1 7, 5.2 7.)*

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
