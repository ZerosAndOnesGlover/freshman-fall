# PROG 101 · Programming I: Structured Programming in C
## Week 2 · Problem Set 2: Operators, Evaluation Order, and Control Flow

**Released:** Friday 9 October 2026, 10:00 · Week 2 (after Thursday's Lecture 3)
**Due:** Friday 16 October 2026, 17:00 · Week 3 — late penalty from 17:01
**Submission:** Commit to the Freshman Fall repo under `"$PROG101/week2/ps2"`; submit the commit hash on the course portal.
**Total:** 100 points · **Expected time:** about 3 hours

*(Revised 2026-09-26: Lab 2, on Monday 12 October, already works the precedence gallery and `-7 / 2`
identity (old Problem 1), the `i = i++` warning and "testing proves nothing" (old 3.2–3.3), and the Collatz
trace (old 4.1). Those items are now only in the lab; this set keeps the rest. The answer key moved out of
this handout.)*

**What this uses:** Weeks 0–2 — `#define` (Week 0), types and conversions (Week 1), and this week's operators
and bit manipulation, evaluation order and undefined behaviour, `if`/`switch`/loops and `getchar`.
**Not needed:** functions of your own (Week 3) — every program is one `main`; `enum` (Week 7).

**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11`

---

## Problem 1: Bit Manipulation (45 pts)

Write `flags.c`: a file-permission set held in one `unsigned int`, all in `main`.

```c
#define PERM_READ  (1u << 0)
#define PERM_WRITE (1u << 1)
#define PERM_EXEC  (1u << 2)
```

**1.1** *(25)* Starting from `unsigned p = 0;`, use one expression each to **set** READ, **set** EXEC,
**clear** READ, and **toggle** WRITE, printing `p` after every step. Then print whether WRITE and READ are
set as **exactly `0` or `1`** (not the masked value), count the set bits with a loop that shifts `p`
right, and print `p` as `rwx`-style letters (`-wx` for 6).

**1.2** *(10)* Expected values after each step: `1, 5, 4, 6`; tests `1` and `0`; count `2`; `-wx`. Show
your output matches.

**1.3** *(10)* Explain why the flags use `1u << n` rather than `1 << n`, referring to Lecture 1's
material on shifting into the sign bit.

---

## Problem 2: Undefined and Unspecified Behaviour (25 pts)

Classify each as **well defined**, **unspecified**, **implementation-defined**, or **undefined**, and justify in
one sentence. *(6, 6, 6, 7)*

(a) `i = i++;`
(b) `f() + g();` — which of `f`, `g` runs first
(c) `INT_MAX + 1`
(d) `-1 >> 1`

---

## Problem 3: `for` and `while` (30 pts)

**3.1** *(20)* Rewrite this `for` loop as an equivalent `while` loop.

```c
for (int i = 0; i < n; i++) { if (i % 3 == 0) continue; total += i; }
```

**3.2** *(10)* Explain the one case where the two are **not** equivalent.

---

## Grading

| Problem | Points | Focus |
|---|---|---|
| 1: Bit manipulation | 45 | Masks, flags, unsigned discipline |
| 2: Undefined behaviour | 25 | The four categories |
| 3: Control flow | 30 | `for`/`while` equivalence |
| **Total** | **100** | |

**Automatic deductions:** any compiler warning (−3 each); any UBSan report in code not deliberately
broken (−5 each).

---

*PROG 101 · Week 2 · Problem Set 2 · Due Friday 16 October 2026, 17:00 · © CSE Department*
