# PROG 101 · Programming I: Structured Programming in C
## Week 3 · Problem Set 3: Functions, the Call Stack, and Structured Programming

**Released:** Friday 16 October 2026, 10:00 · Week 3 (after Thursday's Lecture 3)
**Due:** Friday 23 October 2026, 17:00 · Week 4 — late penalty from 17:01
**Submission:** Commit to the Freshman Fall repo under `"$PROG101/week3/ps3"`; submit the commit hash on the course portal.
**Total:** 100 points · **Expected time:** about 3 hours

*(Revised 2026-09-26: Lab 3, on Monday 19 October, already works the stack-frame addresses, the `swap`
address demonstration, the `static` counter, the `static`-helper link error and an `assert` firing. Those
items (old 1.2, 2.1, 2.3, 3.3, 4.2) are now only in the lab. Old 2.4 went too: it needed recursion, which
is Week 9. The answer key moved out of this handout.)*

**What this uses:** Weeks 0–3 — everything so far plus functions and pass-by-value, the call stack,
storage duration and scope, multi-file programs, headers and include guards, `static` linkage, `assert`,
and structured programming. To print where a local lives, use the idiom from Lecture 02 and Lab 3:
`printf("%p\n", (void *)&x);` — what `&` and `%p` really are is Week 5.
**Not needed:** arrays (Week 4), pointer parameters (Week 5), `malloc` (Week 6).

**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`

---

## Problem 1: Functions and Pass-by-Value (22 pts)

**1.1** *(10)* Explain the difference between a function **declaration** and a **definition**. Give an
example of a program that is valid with only a declaration visible, and say when the definition must
exist.

**1.2** *(12)* For each, state whether the caller can observe the change, and why:

(a) a function that assigns to its `int` parameter
(b) a function that assigns to a `static` local
(c) a function that assigns to a global
(d) a function that returns a value the caller assigns

---

## Problem 2: Scope and Storage Duration (10 pts)

Complete this table:

| Declaration | Scope | Storage duration | Initialised to |
|---|---|---|---|
| `int x;` inside a function | | | |
| `static int x;` inside a function | | | |
| `static int x;` at file level | | | |
| `int x;` at file level | | | |

---

## Problem 3: A Multi-File Program (40 pts)

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

**3.1** *(20)* Implement `stats.c`. Keep a count, a running sum, a running sum of squares, and the smallest
and largest values seen. Variance is `(Σx² − n·mean²) / (n − 1)`. Link with `-lm` for `sqrt`.

**3.2** *(6)* Write `stats.h` with a correct include guard. Explain what breaks without it.

**3.3** *(6)* Write `main.c` that feeds `2, 4, 4, 4, 5, 5, 7, 9` in with `stats_add` and prints every
statistic to 6 decimal places. Expected: mean `5.000000`, variance `4.571429`, stddev `2.138090`,
min `2.000000`, max `9.000000`.

**3.4** *(8)* Write a `Makefile` with correct dependencies so that touching `stats.h` rebuilds both
objects but touching `main.c` rebuilds only one. Demonstrate both cases.

---

## Problem 4: Contracts and Defensive Programming (14 pts)

**4.1** *(8)* State a **precondition** and a **postcondition** for `stats_mean`, and an **invariant** that
holds between calls (what is always true of `count`, `sum` and `sum_sq`). Add them as comments.

**4.2** *(6)* Assertions are for programmer errors, not user errors. Give one condition in your
`stats` library that **should** be an assertion and one that should **not**, and justify each.

---

## Problem 5: Structured Programming (14 pts)

**5.1** *(7)* State the Böhm–Jacopini theorem and explain what it claims about `goto`.

**5.2** *(7)* Rewrite this using only sequence, selection, and iteration:

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
| 1: Functions and pass-by-value | 22 | The most important rule in C |
| 2: Scope and storage duration | 10 | Where variables live and for how long |
| 3: Multi-file program | 40 | Header discipline, linkage, separate compilation |
| 4: Contracts | 14 | Assertions as executable documentation |
| 5: Structured programming | 14 | Why three control structures suffice |
| **Total** | **100** | |

**Automatic deductions:** any compiler warning (−3 each); a header without an include guard (−5).

---

*PROG 101 · Week 3 · Problem Set 3 · Due Friday 23 October 2026, 17:00 · © CSE Department*
