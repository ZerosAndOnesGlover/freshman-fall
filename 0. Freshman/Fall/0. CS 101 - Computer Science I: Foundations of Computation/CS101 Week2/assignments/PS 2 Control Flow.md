# CS 101 · Problem Set 2
## Control Flow: Conditionals and Iteration

**Released:** Friday 9 October 2026, 10:00 (after L09) · Week 2
**Due:** Friday 16 October 2026, 17:00 · Week 3 — late penalty from 17:01
**Submission:** `ps2.py` (Part B) and your answer sheet (Part A) in `"$CS101/week2"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 3 hours

*(Revised 2026-09-26: cut from about four hours to three — A4, the √2 approximations, the
multiplication table and the perfect-number check were removed — and the answer key moved out of this
handout.)*

---

## What this problem set uses

Weeks 0–2: everything in PS 1, plus `if`/`elif`/`else` and De Morgan's laws (L07), `while` loops,
tracing and loop invariants, `break`/`continue`, nested loops (L08), `for` with `range`,
`enumerate`/`zip`, and lists built with `.append()` (L09).

**Not needed and not expected:** writing your own functions with `def` (Week 3), recursion
(Week 4), dictionaries (Week 8). Each Part B problem is a short script that reads input, loops, and prints.

---

## Part A: Written Questions (38 points)

### A1: Execution Tracing (12 points)

Trace this **by hand** — do not run it.

```python
n = 156
result = []
while n > 1:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    result.append(n)
```

**(a)** Build the state table for the first 6 iterations: iteration, `n` before the body,
`n % 2 == 0`, `n` after the body, and the last value appended.

**(b)** State a loop invariant: what is true at the start of every iteration?

**(c)** What does `result` hold when the loop ends? (L08 §9 names this sequence.)

### A2: Loop Invariant Proof (14 points)

```python
base = int(input("base: "))
exp = int(input("exp (≥ 0): "))
result = 1
i = 0
while i < exp:
    result *= base
    i += 1
print(result)
```

**(a)** State the loop invariant using `result`, `i`, `base` and `exp`.
**(b)** Show it holds before the first iteration.
**(c)** Show the body preserves it.
**(d)** Show that the invariant plus the exit condition means the program prints `base ** exp`.
**(e)** Why does the loop always terminate?

### A3: Conditional Logic (12 points)

**(a)** Simplify `not (x >= 0 and y >= 0 and z >= 0)` with De Morgan's laws, step by step.

**(b)** This code is meant to put the smallest of three numbers in `smallest`. Find the bug, give a
counterexample (specific `a`, `b`, `c`), and write a correct version.

```python
smallest = None
if a < b:
    if a < c:
        smallest = a
elif b < c:
    smallest = b
else:
    smallest = c
print(smallest)
```

---

## Part B: Python (`ps2.py`) (62 points)

Put all four programs in `ps2.py`, one after another, each introduced by a comment (`# --- B1 ---`).

### B1: Digit Analysis (18 points)

Read a positive integer `n`. **Using `while` loops with `% 10` and `// 10` — not `str()`** — print:

- the number of digits
- the digit sum and the digit product
- the largest digit
- the **digital root**: sum the digits repeatedly until one digit remains (9875 → 29 → 11 → 2)
- whether `n` is a palindrome (build the reversed number digit by digit and compare)

**Example for `9875`:**
```
Digits:        4
Digit sum:     29
Digit product: 2520
Largest digit: 9
Digital root:  2
Palindrome:    False
```

### B2: Fibonacci (10 points)

Read a count `n`. Build a list of the first `n` Fibonacci numbers with a `for` loop and print it. Write
the loop invariant as a comment. For `n = 8`: `[0, 1, 1, 2, 3, 5, 8, 13]`.

### B3: Patterns (14 points)

Read a size `n` and use nested loops (or string repetition inside one loop) to print:

**(a)** a right triangle (`n = 5`):
```
*
**
***
****
*****
```

**(b)** a diamond with half-height `n` (`n = 3`):
```
  *
 ***
*****
 ***
  *
```

### B4: Number Theory (20 points)

**(a)** Read two positive integers and print their GCD by Euclid's algorithm with a `while` loop:
replace `(a, b)` by `(b, a % b)` until `b` is 0. Then print the LCM, `a * b // gcd`.
`48, 18` → GCD 6, LCM 144.

**(b)** For each `n` in `[360, 13, 1001]`, build and print the list of its prime factors: start with
`f = 2`, divide `f` out while it divides, then move to `f + 1`, until nothing is left.
`360` → `[2, 2, 2, 3, 3, 5]`.

---

## Grading Rubric

| Problem | Points |
|---------|--------|
| A1 Tracing | 12 |
| A2 Invariant proof | 14 |
| A3 Conditionals | 12 |
| B1 Digit analysis | 18 |
| B2 Fibonacci | 10 |
| B3 Patterns | 14 |
| B4 Number theory | 20 |
| **Total** | **100** |

---

*CS 101 · Week 2 · Problem Set 2 · Due Friday 16 October 2026, 17:00 · © CSE Department*
