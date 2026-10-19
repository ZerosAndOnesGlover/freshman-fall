---
assessment: PS 2
course: CS 101
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-13
submitted: 2026-10-16
graded: 2026-10-19
source: "PS 2 Control Flow.md"
---

# CS 101 · PS 2
## Answer Sheet

**Assessment:** `PS 2 Control Flow.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### A1 — Execution Tracing  (12 points)

**Your answer:**

**(a)** State table (traced by hand):

| Iter | `n` before | `n % 2 == 0` | `n` after | appended |
|------|-----------|--------------|-----------|----------|
| 1 | 156 | True  | 78  | 78  |
| 2 | 78  | True  | 39  | 39  |
| 3 | 39  | False | 118 | 118 |
| 4 | 118 | True  | 59  | 59  |
| 5 | 59  | False | 178 | 178 |
| 6 | 178 | True  | 89  | 89  |

**(b)** At the start of every iteration, `n > 1`, and `result` holds — in order — every value `n` has
taken after the seed `156` (the terms produced so far).

**(c)** When the loop ends, `result` holds the **Collatz (hailstone) sequence** of 156 *without the
seed*: 36 values ending at 1, peaking at 304. (Whether every start reaches 1 is the open Collatz
conjecture, but 156 does.)

_Marks: 12 / 12_

---

### A2 — Loop Invariant Proof  (14 points)

**Your answer:**

**(a)** Invariant: `result == base ** i` **and** `0 <= i <= exp`.

**(b) Initialisation.** Before the first iteration `result = 1` and `i = 0`, so
`result == base ** 0` (which is 1) and `0 <= 0 <= exp` (since `exp ≥ 0`). Holds.

**(c) Preservation.** Assume the invariant holds at the top of an iteration, i.e. `result == base ** i`.
The body executes `result *= base` → `base ** i * base = base ** (i + 1)`, then `i += 1` → `i + 1`.
Since `i < exp` was true, `i + 1 <= exp`, so `0 <= i + 1 <= exp`. The invariant holds again.

**(d) Conclusion.** The loop exits when `i < exp` is false, i.e. `i >= exp`. Combined with the
invariant's `i <= exp` we get `i == exp`, so `result == base ** exp` — exactly what the program
prints.

**(e) Termination.** `exp - i` is a non-negative integer that decreases by exactly 1 each iteration,
so it reaches 0 after `exp` iterations and the loop stops.

_Marks: 14 / 14_

---

### A3 — Conditional Logic  (12 points)

**Your answer:**

**(a)** Step by step with De Morgan's law `not (P and Q and R) ≡ not P or not Q or not R`:

```
not (x >= 0 and y >= 0 and z >= 0)
= not (x >= 0) or not (y >= 0) or not (z >= 0)
= x < 0 or y < 0 or z < 0
```

**(b) Bug.** The `elif`/`else` are attached to the **outer** `if a < b` (wrong indentation). If
`a < b` is true but `a < c` is *not*, no branch assigns anything, so `smallest` is never set.

**Counterexample:** `a, b, c = 2, 3, 1`. Here `a < b` is true, but `a < c` (2 < 1) is false, so the
outer `if`'s `elif`/`else` are skipped and the program prints `None`, although the answer is `1`.

**Correct version:**

```python
if a <= b and a <= c:
    smallest = a
elif b <= c:
    smallest = b
else:
    smallest = c
```

_Marks: 12 / 12_

---

### B1 — Digit Analysis  (18 points)

**Your answer:**

All four Part B programs are in `ps2.py` (submitted in `0. CS 101/week2/`). B1 uses `while` loops
with `% 10` and `// 10` only — no `str()`:

```python
n = int(input("Positive integer: "))
count = 0
digit_sum = 0
digit_product = 1
largest = 0
m = n
while m > 0:
    d = m % 10
    count += 1
    digit_sum += d
    digit_product *= d
    if d > largest:
        largest = d
    m //= 10

# digital root: repeatedly sum the digits until a single digit is left
root = digit_sum
while root >= 10:
    s = 0
    while root > 0:
        s += root % 10
        root //= 10
    root = s

# palindrome: build the reversed number one digit at a time and compare with n
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

Output for `9875`:

```
Digits:        4
Digit sum:     29
Digit product: 2520
Largest digit: 9
Digital root:  2
Palindrome:    False
```

Also verified: `1234` → 4, 10, 24, 4, 1, False; `12321` → 5, 9, 12, 3, 9, True; `7` → 1, 7, 7, 7, 7, True.

_Marks: 18 / 18_

---

### B2 — Fibonacci  (10 points)

**Your answer:**

```python
n = int(input("How many terms? "))
fibs = []
a, b = 0, 1
for i in range(n):
    # invariant: fibs holds F(0)..F(i-1); a == F(i), b == F(i+1)
    fibs.append(a)
    a, b = b, a + b
print(fibs)
```

**Loop invariant:** at the start of iteration `i`, `fibs` holds `F(0) … F(i-1)`, with `a == F(i)` and
`b == F(i+1)`.

Output for `n = 8`: `[0, 1, 1, 2, 3, 5, 8, 13]`.

_Marks: 10 / 10_

---

### B3 — Patterns  (14 points)

**Your answer:**

```python
n = int(input("Size: "))
# (a) right triangle
for row in range(1, n + 1):
    print("*" * row)
# (b) diamond with half-height n: growing top half, then shrinking bottom half
for row in range(1, n + 1):
    print(" " * (n - row) + "*" * (2 * row - 1))
for row in range(n - 1, 0, -1):
    print(" " * (n - row) + "*" * (2 * row - 1))
```

**(a)** For `n = 5`:

```
*
**
***
****
*****
```

**(b)** For `n = 3`:

```
  *
 ***
*****
 ***
  *
```

_Marks: 14 / 14_

---

### B4 — Number Theory  (20 points)

**Your answer:**

```python
a = int(input("a: "))
b = int(input("b: "))
x, y = a, b
while y != 0:
    x, y = y, x % y
print(f"gcd({a}, {b}) = {x}")
print(f"lcm({a}, {b}) = {a * b // x}")

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

**(a)** Output for `a = 48`, `b = 18`:

```
gcd(48, 18) = 6
lcm(48, 18) = 144
```

(Also `1071, 462` → 21 and 23562.)

**(b)** Output:

```
360 [2, 2, 2, 3, 3, 5]
13 [13]
1001 [7, 11, 13]
```

_Marks: 20 / 20_

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-19 |

**Feedback:**
Full marks. A1's table is correct for all six iterations, the invariant names both `n > 1` and what
`result` accumulates, and the sequence is correctly identified as the Collatz/hailstone sequence of
156 (36 terms, no seed). A2 separates the invariant from the postcondition and proves
init/preserve/conclude plus termination via the strictly decreasing `exp - i`. A3 applies De Morgan
correctly and diagnoses the mis-indented `elif`/`else` with the exact counterexample `2, 3, 1` and a
correct fix.

Part B runs exactly as specified: B1 uses `% 10`/`// 10` throughout (no `str()`), with correct
digital-root and reversed-number loops; B2 builds the list with a `for` loop and a correct invariant
comment; B3's triangle and diamond match the examples for `n = 5` and `n = 3`; B4's Euclid loop,
LCM, and prime-factorisation all produce the specified output (`48,18` → 6/144; `360, 13, 1001` →
the listed factor lists).
