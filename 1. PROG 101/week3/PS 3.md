---
assessment: PS 3
course: PROG 101
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-16
submitted: 2026-10-19
graded: 2026-10-19
source: "Problem Set 3.md"
---

# PROG 101 · PS 3
## Answer Sheet

**Assessment:** `Problem Set 3.md`
**Points available:** 100

Code and the detailed write-up live in `1. PROG 101/week3/ps3/`: `stats.h`, `stats.c`, `main.c`,
`Makefile`, `ps3_answers.md`.

Built with `gcc 15.2.0`, `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`. All outputs are real.

---

## Problem 1 — Functions and Pass-by-Value  (22 points)

**1.1** *(10)* A **declaration** names a thing and gives its type — a promise, no code; a **definition**
supplies the body (functions) or the storage (objects). A program is valid with only a declaration
visible at the point of use (as in `main.c` with `stats.h`): the compiler emits the call and type-checks
the arguments. The **definition must exist by link time** — if it never does, compilation succeeds but
the link fails with `undefined reference`.

**1.2** *(12)*

| Case | Observable? | Why |
|---|---|---|
| (a) assigns to an `int` parameter | **No** | The parameter is a copy in the callee's frame; the caller's variable is untouched. |
| (b) assigns to a `static` local | **Indirectly** — its value persists into the next call | The name is invisible outside, but the object lives for the whole run. |
| (c) assigns to a global | **Yes** | One file-scope object; everyone sees the change. |
| (d) returns a value the caller assigns | **Yes** | The change travels back through the returned value only. |

*Marks: 22 / 22*

---

## Problem 2 — Scope and Storage Duration  (10 points)

| Declaration | Scope | Storage duration | Initialised to |
|---|---|---|---|
| `int x;` inside a function | block | automatic | **indeterminate** (garbage) |
| `static int x;` inside a function | block | static (whole run) | **0** |
| `static int x;` at file level | file (internal linkage) | static | **0** |
| `int x;` at file level | file (external linkage) | static | **0** |

Block-scope `static` changes the **storage duration** (not scope); file-scope `static` changes the
**linkage** (internal). Static-duration objects are zero-initialised before `main`.

*Marks: 10 / 10*

---

## Problem 3 — A Multi-File Program  (40 points)

**3.1** *(20)* `stats.c` keeps `count`, `sum`, `sum_sq`, `lowest`, `highest` as **file-level `static`**
state, plus a file-private `square` helper. Variance uses `(Σx² − n·mean²)/(n − 1)`; linked with `-lm`.

**3.2** *(6)* `stats.h` has a correct include guard (`#ifndef STATS_H / #define STATS_H / … / #endif`).
Without it, a second inclusion re-processes every declaration; for anything with a *definition*
(`struct`, `enum`, `static inline` function, object-like macro) that is a hard `redefinition` error.
Demonstrated: a header defining `struct point` included twice gives `error: redefinition of 'struct point'`;
with the guard it compiles clean.

**3.3** *(6)* `main.c` feeds `2, 4, 4, 4, 5, 5, 7, 9` one at a time (no arrays) and prints 6 dp:

```
count    8
mean     5.000000
variance 4.571429
stddev   2.138090
min      2.000000
max      9.000000
```

Matches the expected values exactly.

**3.4** *(8)* The `Makefile` lists `stats.h` as a prerequisite of **both** objects. Demonstrated:

* `touch stats.h; make` → **both** `main.c` and `stats.c` recompile, then relink.
* `touch main.c; make` → **only** `main.o` recompiles, then relink.
* unchanged → `make: 'stats' is up to date.`

*Marks: 40 / 40*

---

## Problem 4 — Contracts and Defensive Programming  (14 points)

**4.1** *(8)* For `stats_mean`: **precondition** `count > 0`; **postcondition** returns `sum / count`.
**Invariant between calls:** `count` values added since reset, `sum` their total, `sum_sq` the total of
their squares — so `mean == sum / count`, and `lowest ≤ mean ≤ highest`. Added as comments in `stats.c`.

**4.2** *(6)* **Assertion:** `count > 0` in `stats_mean` (and `count > 1` in `stats_variance`) — asking
for the mean of an empty set is a **programmer error** with no sensible recovery. **Not an assertion:**
a non-numeric value typed by a **user** at runtime — that is an expected condition needing real error
handling, and it must still work in a `-DNDEBUG` build. (Never put a side effect inside `assert`.)

*Marks: 14 / 14*

---

## Problem 5 — Structured Programming  (14 points)

**5.1** *(7)* **Böhm–Jacopini theorem:** every computable function can be expressed with only **sequence,
selection, and iteration**. Consequence: unrestricted `goto` is **never necessary** — any `goto` program
can be rewritten with those three structures, the basis of structured programming.

**5.2** *(7)* Rewritten with only sequence, selection, iteration:

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

Verified for `n = 10`: both the `goto` original and the rewrite print `27`
(`1 + 2 + 4 + 5 + 7 + 8`).

*Marks: 14 / 14*

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-19 |

**Feedback:**
Complete and correct across all five problems. Problem 1 separates declaration (promise, no code) from
definition (body/storage) and pins the definition to link time; the pass-by-value table is right on all
four cases, including the subtle "static local is not directly observable but persists". Problem 2's
table is correct, including the block-scope-static-changes-duration vs file-scope-static-changes-linkage
distinction and zero-initialisation. Problem 3 builds a clean multi-file library: `stats.h` has a proper
include guard with a demonstrated failure mode, `stats.c` uses file-level `static` state, `main.c` avoids
arrays (Week 4) and hits every expected value to 6 dp, and the `Makefile` has correct header dependencies
with both `touch` cases demonstrated. Problem 4 states a real precondition/postcondition/invariant and
correctly separates programmer-error assertions from user-input error handling. Problem 5 states
Böhm–Jacopini accurately and rewrites the `goto` loop with `for` + `continue`, verified against the
original. No compiler warnings; header guard present.
