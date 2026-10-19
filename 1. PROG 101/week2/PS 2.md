---
assessment: PS 2
course: PROG 101
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-09
submitted: 2026-10-15
graded: 2026-10-17
source: "Problem Set 2.md"
---

# PROG 101 · PS 2
## Answer Sheet

**Assessment:** `Problem Set 2.md`
**Points available:** 100

Code and the detailed write-up live in `1. PROG 101/week2/ps2/`: `flags.c`, `Makefile`,
`ps2_answers.md`. `flags.c` builds clean under `gcc -Wall -Wextra -Werror -pedantic -std=c11`.

---

### Problem 1 — Bit Manipulation  (45 points)

`flags.c` holds the permission set in one `unsigned int` with `PERM_READ (1u<<0)`, `PERM_WRITE (1u<<1)`,
`PERM_EXEC (1u<<2)`. Real output:

```
set READ     -> 1
set EXEC     -> 5
clear READ   -> 4
toggle WRITE -> 6
test WRITE   -> 1
test READ    -> 0
bits set     -> 2
as rwx       -> -wx
```

**1.1 / 1.2.** Set READ (`p|PERM_READ` → `0|1=1`), set EXEC (`1|4=5`), clear READ (`5&~1=4`), toggle
WRITE (`4^2=6`): the values after each step are **1, 5, 4, 6**, exactly as expected. Membership is
printed with `!= 0`, so the tests are **exactly `0` or `1`** (`WRITE -> 1`, `READ -> 0`), not the masked
value. A right-shifting loop counts the set bits → **2**. Rendered as letters → **`-wx`**.

**1.3.** The flags use `1u << n`, not `1 << n`. `1` is a *signed* `int`, and shifting a `1` into the
sign bit (as `1 << 31` does) is **undefined behaviour** (C11 §6.5.7). `1u` is *unsigned*, with 32 value
bits and no sign bit; its shifts are defined modulo 2³². So `1u << n` is well defined for every
`n` in `0..31`, while `1 << 31` is a latent UB bug — and permission flags are unsigned by nature.

Full details in `ps2_answers.md`.

*Marks: 45 / 45*

---

### Problem 2 — Undefined and Unspecified Behaviour  (25 points)

| # | Expression | Category | Why (one sentence) |
|---|---|---|---|
| (a) | `i = i++;` | **Undefined** | Two unsequenced modifications of `i` with no sequence point between them. |
| (b) | order of `f() + g();` | **Unspecified** | The evaluation order of `+`'s operands is unspecified — either order is allowed. |
| (c) | `INT_MAX + 1` | **Undefined** | Signed overflow has no defined result and the compiler may assume it never happens. |
| (d) | `-1 >> 1` | **Implementation-defined** | Right-shifting a negative value is left to the implementation, which must document it. |

**Evidence gathered:** (a) `warning: operation on 'i' may be undefined [-Wsequence-point]`;
(c) UBSan `runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'`;
(d) gcc gives `-1` (arithmetic shift) — its documented choice.

*Marks: 25 / 25*

---

### Problem 3 — `for` and `while`  (30 points)

**3.1** Equivalent `while` loop:

```c
int i = 0;
while (i < n) {
    if (i % 3 == 0) { i++; continue; }   /* increment before continue */
    total += i;
    i++;
}
```

Verified: for `n = 10` both forms give `total = 27` (indices 1, 2, 4, 5, 7, 8).

**3.2** The one case where they are **not** equivalent is when the body uses **`continue`**. A `for`
loop runs its increment *after the body and after any `continue`*; a naive `while` rewrite puts the
increment only at the end of the body, so a `continue` skips it. On the first iteration (`i = 0`,
`0 % 3 == 0`) the loop then never advances — an infinite loop. The fix duplicates the increment
before each `continue`, as in 3.1.

*Marks: 30 / 30*

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-17 |

**Feedback:**
Complete and correct. Problem 1 implements set/clear/toggle with the right masks, prints membership as
exactly `0`/`1`, counts bits with a shift loop, renders `-wx`, and matches all expected values
(1, 5, 4, 6); the `1u << n` justification correctly cites the signed-shift UB. Problem 2 classifies all
four cases correctly — undefined, unspecified, undefined, implementation-defined — with one-sentence
justifications and real tool evidence. Problem 3 gives an equivalent `while` rewrite and pinpoints the
`continue`/increment non-equivalence. `flags.c` compiles clean under `-Werror -pedantic` with no UBSan
reports.
