---
assessment: Lab 2
course: PROG 101
component: Labs
possible: 20
score: 20
status: graded
started: 2026-10-12
submitted: 2026-10-12
graded: 2026-10-12
source: "LAB 2 Operators Evaluation Control Flow.md"
---

# PROG 101 · Lab 2
## Answer Sheet — Operators, Evaluation Order, and Control Flow

**Assessment:** `LAB 2 Operators Evaluation Control Flow.md`
**Points available:** 20

Programs, `Makefile`, and the full write-up live in `1. PROG 101/week2/lab2/`:
`precedence.c`, `ub.c`, `overflow.c`, `shift.c`, `fallthrough.c`, `collatz.c`, `dowhile.c`,
`wordcount.c`, `Makefile`, `answers.md`.

Clean programs build with `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`; the demonstrative files
(Parts 1A/2) are built without `-Werror` and with `-fsanitize=undefined`, since their warnings/UB are
the exercise. All values are real.

---

## Part 1 — Precedence and What the Compiler Sees  (5 points)

**1A** (`a=6, b=3, c=2`) — predicted, then run:

| # | Expression | Actual | How C parsed it |
|---|---|---|---|
| 1 | `a & b == c` | `0` | `a & (b == c)` → `6 & 0` |
| 2 | `(a & b) == c` | `1` | `(6 & 3) == 2` |
| 3 | `1 << 2 + 3` | `32` | `1 << (2 + 3)` |
| 4 | `(1 << 2) + 3` | `7` | `4 + 3` |
| 5 | `a + b % c` | `7` | `a + (b % c)` |
| 6 | `~5` | `-6` | `~x == -x-1` |
| 7 | `5 ^ 3` | `6` | `0101 ^ 0011` |

Lines 1 and 2 differ (`0` vs `1`) purely due to precedence: `==` binds tighter than `&`.

**1B** Lines 1 and 3 warn (`-Wparentheses`): *"suggest parentheses around comparison in operand of
'&'"* and *"suggest parentheses around '+' inside '<<'"*. gcc warns where precedence is **widely
misremembered**, not everywhere it matters — `a + b % c` is unsurprising (`%` tighter than `+` matches
ordinary arithmetic), so it stays silent.

**1C** `-7/2 = -3`, `-7%2 = -1`, `7/-2 = -3`, `7%-2 = 1`. C99 rule: division truncates toward zero and
the sign of `%` follows the **dividend**. Identity: `(-3)(2)+(-1) = -7` ✓, `(-3)(-2)+1 = 7` ✓.

*Marks: 5 / 5*

---

## Part 2 — Undefined Behaviour, Caught  (5 points)

**2A** `warning: operation on 'i' may be undefined [-Wsequence-point]`. A **sequence point** is a point
where all prior side effects are complete and none of the following have started; `i = i++` writes `i`
twice with no sequence point between, so the line has **no defined meaning** (undefined, not merely
"compiler-dependent").

**2B** UBSan: `runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type
'int'`. Normal build printed `-2147483648`, with no guarantee.

**2C** UBSan: `runtime error: left shift of 1 by 31 places cannot be represented in type 'int'`.
`1 << 31` would set the sign bit of a signed `int` — undefined (C11 §6.5.7). The one-character fix is
`1u << 31` (unsigned, 32 value bits, defined mod 2³²).

**2D** UB imposes no requirement on the implementation, so printing the "expected" value is one
permitted outcome, not proof of correctness — a test only shows UB didn't manifest on *this* compiler,
flags, and input. Tools: **compiler warnings** (caught 2A statically) and **UBSan** (caught 2B/2C).

*Marks: 5 / 5*

---

## Part 3 — Control Flow  (6 points)

**3A**

```
n=1: one two three
n=2: two three
n=3: three
n=4: four
n=5: other
```

Under `-Wall -Wextra -Werror` it **fails**: `error: this statement may fall through
[-Werror=implicit-fallthrough=]` (one per falling-through arm). Fix: add a `/* fall through */` comment
to each arm — output unchanged, build passes. The warning objects only to fall-through you didn't
*declare*.

**3B** Trace (x = 27 → 82, 41, 124, 62, 31, 94, 47, 142 for iterations 1–8). **Final `steps = 111`**
(verified).

**3C** `do { iter++; } while (k < 10);` with `k = 100` prints **`1`** — the body ran despite the
condition being false on entry. Use it when the loop must run at least once to *produce* the value the
condition tests (e.g. input validation).

*Marks: 6 / 6*

---

## Part 4 — Word-Count State Machine  (4 points)

`wordcount.c` uses an `OUT_OF_WORD`/`IN_WORD` machine driven by `switch`, counting on the **transition**
into `IN_WORD`, with `int c` (not `char c`) so `EOF` is distinguishable. Verified against `wc`:

| Input | Mine | `wc` |
|---|---|---|
| `hello world\n` | `1 2 12` | `1 2 12` ✓ |
| empty | `0 0 0` | `0 0 0` ✓ |
| `   \n` | `1 0 4` | `1 0 4` ✓ |
| `a\n\n\nb\n` | `4 2 6` | `4 2 6` ✓ |

*Marks: 4 / 4*

---

## Grading Summary

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-10-12 |

**Feedback:**
Complete and correct. Part 1 predicts and verifies all seven expressions (lines 1 vs 2 differ), and
explains the two `-Wparentheses` warnings with the "surprising precedence" rule, plus the C99 division/
remainder sign rule and the identity check. Part 2 provokes and catches the sequence-point, signed-
overflow, and sign-bit-shift issues with verbatim tool output (compiler warning + UBSan) and explains
why testing can't rule out UB. Part 3 traces the Collatz loop correctly (`steps = 111`), documents the
fall-through intent so the `-Werror` build passes without changing output, and proves the `do-while`
one-pass behaviour. Part 4 matches `wc` on all four cases with the state-transition counting and `int c`
done right. `make` builds everything; only the deliberately-broken demos warn.
