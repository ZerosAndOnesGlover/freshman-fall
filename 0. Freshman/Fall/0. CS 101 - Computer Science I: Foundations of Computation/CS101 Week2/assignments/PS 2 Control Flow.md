# CS 101 · Problem Set 2
## Control Flow: Conditionals and Iteration

**Released:** Friday 9 October 2026, 10:00 (after L09) · Week 2
**Due:** Friday 16 October 2026, 17:00 · Week 3 — late penalty from 17:01
**Submission:** `ps2.py` (Part B) and your answer sheet (Part A) in `"$CS101/week2"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 4 hours

---

## What this problem set uses

Weeks 0–2: everything in PS 1, plus `if`/`elif`/`else` and De Morgan's laws (L07), `while` loops,
tracing and loop invariants, `break`/`continue`, nested loops (L08), `for` with `range`,
`enumerate`/`zip`, and lists built with `.append()` (L09).

**Not needed and not expected:** writing your own functions with `def` (Week 3), recursion
(Week 4), dictionaries (Week 8). Each Part B problem is a short script that reads input, loops, and prints.

---

## Part A: Written Questions (40 points)

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

### A2: Loop Invariant Proof (12 points)

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

### A3: Conditional Logic (10 points)

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

### A4: `for` vs `while` (6 points)

For each task, say which loop fits better and why:

**(a)** Printing each character of a string with its position.
**(b)** Asking the user for a number until they type a valid one.
**(c)** Computing the 100th Fibonacci number.

---

## Part B: Python (`ps2.py`) (60 points)

Put all four programs in `ps2.py`, one after another, each introduced by a comment (`# --- B1 ---`).

### B1: Digit Analysis (16 points)

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

### B2: Sequences (14 points)

Read a count `n`.

**(a)** Build a list of the first `n` Fibonacci numbers with a `for` loop and print it. Write the loop
invariant as a comment. For `n = 8`: `[0, 1, 1, 2, 3, 5, 8, 13]`.

**(b)** Print the first `n` approximations of √2: start with `p = 1, q = 1`; each step the next pair
is `p + 2q, p + q`. Print each as a fraction, its value to 6 decimals, and its error
`abs(p / q - 2 ** 0.5)`. For `n = 5` the fractions are `1/1, 3/2, 7/5, 17/12, 41/29`.

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

**(c)** an `n × n` multiplication table, each entry in width 5 (`:5d`). For `n = 5`:
```
    1    2    3    4    5
    2    4    6    8   10
    3    6    9   12   15
    4    8   12   16   20
    5   10   15   20   25
```

### B4: Number Theory (16 points)

**(a)** Read two positive integers and print their GCD by Euclid's algorithm with a `while` loop:
replace `(a, b)` by `(b, a % b)` until `b` is 0. Then print the LCM, `a * b // gcd`.
`48, 18` → GCD 6, LCM 144.

**(b)** For each `n` in `[6, 12, 28, 496, 500]`, print whether it is **perfect** — equal to the sum of
its divisors below itself (6 = 1 + 2 + 3). Only divisors up to `n // 2` need checking.

**(c)** For each `n` in `[360, 13, 1001]`, build and print the list of its prime factors: start with
`f = 2`, divide `f` out while it divides, then move to `f + 1`, until nothing is left.
`360` → `[2, 2, 2, 3, 3, 5]`.

---

## Grading Rubric

| Problem | Points |
|---------|--------|
| A1 Tracing | 12 |
| A2 Invariant proof | 12 |
| A3 Conditionals | 10 |
| A4 for vs while | 6 |
| B1 Digit analysis | 16 |
| B2 Sequences | 14 |
| B3 Patterns | 14 |
| B4 Number theory | 16 |
| **Total** | **100** |

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** All code below was run; outputs are real.

### A1 (12)

| Iter | `n` before | even? | `n` after | appended |
|---|---|---|---|---|
| 1 | 156 | True | 78 | 78 |
| 2 | 78 | True | 39 | 39 |
| 3 | 39 | False | 118 | 118 |
| 4 | 118 | True | 59 | 59 |
| 5 | 59 | False | 178 | 178 |
| 6 | 178 | True | 89 | 89 |

(b) At the start of every iteration `n > 1`, and `result` holds, in order, every value `n` has taken
after 156. (c) The **Collatz (hailstone) sequence** of 156 without the seed: 36 values, ending at 1,
peaking at 304.
*6 pts table (1 per row), 4 pts invariant (must mention both `n > 1` and what `result` holds), 2 pts naming it.
Termination for every starting `n` is the open Collatz conjecture — a student who claims to have proved it has made an error.*

### A2 (12)

(a) `result == base ** i` and `0 <= i <= exp`. (b) Before the loop `result = 1`, `i = 0`, and `base ** 0 == 1`.
(c) If `result == base ** i` at the top, the body gives `result * base == base ** (i + 1)` and `i + 1`.
(d) The loop stops when `i < exp` is false; since `i` starts at 0 ≤ `exp` and rises by exactly 1, `i == exp`,
so `result == base ** exp`. (e) `exp - i` is a non-negative integer that drops by 1 each iteration.
*3/2/2/3/2. Stating `result == base ** exp` as the invariant earns 0 for (a) — that is the postcondition.*

### A3 (10)

(a) `not(x >= 0) or not(y >= 0) or not(z >= 0)` → **`x < 0 or y < 0 or z < 0`**. *(4)*

(b) The `elif`/`else` belong to the **outer** `if`. When `a < b` is true but `a < c` is false, nothing
is assigned. **Counterexample `a, b, c = 2, 3, 1`** prints `None`; the answer is `1`. Correct version:

```python
if a <= b and a <= c:
    smallest = a
elif b <= c:
    smallest = b
else:
    smallest = c
```
*(2 bug, 2 counterexample, 2 fix.) Any correct version is fine.*

### A4 (6)

(a) `for` — a known sequence (`for i, ch in enumerate(s)`). (b) `while` — the number of tries is not
known in advance (`while True:` … `break`). (c) `for i in range(100)` — the count is fixed.
*2 each: choice plus the reason (known vs unknown number of iterations).*

### B1 (16)

```python
n = int(input("Positive integer: "))
digit_sum = 0
digit_product = 1
count = 0
largest = 0
m = n
while m > 0:
    d = m % 10
    digit_sum += d
    digit_product *= d
    count += 1
    if d > largest:
        largest = d
    m //= 10
root = digit_sum
while root >= 10:
    s = 0
    while root > 0:
        s += root % 10
        root //= 10
    root = s
reversed_n = 0
m = n
while m > 0:
    reversed_n = reversed_n * 10 + m % 10
    m //= 10
print(f"Digits:        {count}")
print(f"Digit sum:     {digit_sum}")
print(f"Digit product: {digit_product}")
print(f"Largest digit: {largest}")
print(f"Digital root:  {root}")
print(f"Palindrome:    {reversed_n == n}")
```

Verified: `9875` → 4, 29, 2520, 9, 2, False. `1234` → 4, 10, 24, 4, 1, False. `12321` → 5, 9, 12, 3, 9, True. `7` → 1, 7, 7, 7, 7, True.
*3 per quantity except palindrome (1). Using `str(n)` for the digits earns half.*

### B2 (14)

```python
n = int(input("How many terms? "))
fibs = []
a, b = 0, 1
for i in range(n):
    # invariant: fibs holds F(0)..F(i-1); a == F(i), b == F(i+1)
    fibs.append(a)
    a, b = b, a + b
print(fibs)

p, q = 1, 1
for k in range(n):
    print(f"{p}/{q} = {p / q:.6f}   error {abs(p / q - 2 ** 0.5):.1e}")
    p, q = p + 2 * q, p + q
```

`n = 8` → `[0, 1, 1, 2, 3, 5, 8, 13]`; fractions `1/1 3/2 7/5 17/12 41/29 99/70 239/169 577/408`,
the last `1.414216` with error `2.1e-06` — the error shrinks by about 6× per step.
*(a) 8 including 2 for a correct invariant comment; (b) 6.*

### B3 (14)

```python
n = int(input("Size: "))
for row in range(1, n + 1):
    print("*" * row)
for row in range(1, n + 1):
    print(" " * (n - row) + "*" * (2 * row - 1))
for row in range(n - 1, 0, -1):
    print(" " * (n - row) + "*" * (2 * row - 1))
for i in range(1, n + 1):
    line = ""
    for j in range(1, n + 1):
        line += f"{i * j:5d}"
    print(line)
```
Output matches the examples exactly for `n = 5` (triangle, table) and `n = 3` (diamond).
*4 / 5 / 5.*

### B4 (16)

```python
a = int(input("a: "))
b = int(input("b: "))
x, y = a, b
while y != 0:
    x, y = y, x % y
print(f"gcd({a}, {b}) = {x}")
print(f"lcm({a}, {b}) = {a * b // x}")

for n in [6, 12, 28, 496, 500]:
    total = 0
    for d in range(1, n // 2 + 1):
        if n % d == 0:
            total += d
    print(n, "perfect" if total == n else "not perfect")

for n in [360, 13, 1001]:
    factors = []
    m = n
    f = 2
    while m > 1:
        while m % f == 0:
            factors.append(f)
            m //= f
        f += 1
    print(n, factors)
```

Verified: `48, 18` → 6 and 144; `1071, 462` → 21 and 23562. 6, 28, 496 perfect; 12, 500 not.
`360` → `[2, 2, 2, 3, 3, 5]`, `13` → `[13]`, `1001` → `[7, 11, 13]`.
*(a) 6, (b) 5, (c) 5.*

---

*CS 101 · Week 2 · Problem Set 2 · Due Friday 16 October 2026, 17:00 · © CSE Department*
