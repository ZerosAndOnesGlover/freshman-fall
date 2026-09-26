# CS 101 · Problem Set 2 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

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

### A2 (14)

(a) `result == base ** i` and `0 <= i <= exp`. (b) Before the loop `result = 1`, `i = 0`, and `base ** 0 == 1`.
(c) If `result == base ** i` at the top, the body gives `result * base == base ** (i + 1)` and `i + 1`.
(d) The loop stops when `i < exp` is false; since `i` starts at 0 ≤ `exp` and rises by exactly 1, `i == exp`,
so `result == base ** exp`. (e) `exp - i` is a non-negative integer that drops by 1 each iteration.
*3/3/3/3/2. Stating `result == base ** exp` as the invariant earns 0 for (a) — that is the postcondition.*

### A3 (12)

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
*(3 bug, 3 counterexample, 2 fix.) Any correct version is fine.*

### B1 (18)

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
*3 per quantity except palindrome (3). Using `str(n)` for the digits earns half.*

### B2 (10)

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

`n = 8` → `[0, 1, 1, 2, 3, 5, 8, 13]`.
*8 for the list, 2 for a correct invariant comment.*

### B3 (14)

```python
n = int(input("Size: "))
for row in range(1, n + 1):
    print("*" * row)
for row in range(1, n + 1):
    print(" " * (n - row) + "*" * (2 * row - 1))
for row in range(n - 1, 0, -1):
    print(" " * (n - row) + "*" * (2 * row - 1))
```
Output matches the examples exactly for `n = 5` (triangle) and `n = 3` (diamond).
*6 / 8.*

### B4 (20)

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

Verified: `48, 18` → 6 and 144; `1071, 462` → 21 and 23562.
`360` → `[2, 2, 2, 3, 3, 5]`, `13` → `[13]`, `1001` → `[7, 11, 13]`.
*(a) 10, (b) 10.*

---

*CS 101 · Week 2 · Problem Set 2 · Due Friday 16 October 2026, 17:00 · © CSE Department*
