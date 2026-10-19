# CS 101 · Lab 2 — Notes

**Lab:** Tracing, Print-Debugging, and Loop Invariants · Tuesday 13 October 2026
**Student:** Adebayo Glover

Deliverables in `0. CS 101/week2/`: `debug_exercise.py` (Part 2, fixed), `loops.py` (Parts 3–4),
and this file.

---

## Part 1 — Tracing by Hand (20)

### Exercise 1.1 (10)

```python
n = 5
result = 0      # <-- bug
i = 1
while i <= n:
    result *= i
    i += 1
print(result)
```

Trace of three iterations:

| iteration | `i` before | `result` before | `result *= i` | `i` after |
|-----------|-----------|-----------------|---------------|-----------|
| 1 | 1 | 0 | 0 | 2 |
| 2 | 2 | 0 | 0 | 3 |
| 3 | 3 | 0 | 0 | 4 |

Once `result` is `0` it stays `0` forever, so the program prints `0`, not `120`.

**Invariant:** `result == (i - 1)!` at the top of each iteration. At `i = 1` this demands
`result == 0! == 1`, but the code starts with `result = 0`. **Fix:** `result = 1` → prints `120`.

### Exercise 1.2 (10)

One row per inner-loop step:

| `i` | `j` | `total` before | `total += j` |
|-----|-----|----------------|--------------|
| 1 | 1 | 0  | 1  |
| 2 | 1 | 1  | 2  |
| 2 | 2 | 2  | 4  |
| 3 | 1 | 4  | 5  |
| 3 | 2 | 5  | 7  |
| 3 | 3 | 7  | 10 |
| 4 | 1 | 10 | 11 |
| 4 | 2 | 11 | 13 |
| 4 | 3 | 13 | 16 |
| 4 | 4 | 16 | 20 |

**Printed:** `20`. For each `i`, the inner loop adds `1 + 2 + … + i` — the `i`-th triangular number.
The running totals after each outer iteration are **1, 3, 6, 10**, so `total` is the sum of the first
four triangular numbers: `1 + 3 + 6 + 10 = 20`.

---

## Part 2 — Print-Debugging (30)

For each bug: a `print` was placed inside the loop, the run was read, the wrong line identified, the
fix applied, and the debug `print` removed. Final code is in `debug_exercise.py`.

| Bug | Debug print showed | Wrong line | What was meant | Fix | Buggy → fixed |
|-----|--------------------|------------|----------------|-----|----------------|
| 1 | `total` jumping to each odd number (`1, 3, 5, …`) | `total = i` | *add* each odd number to the running total | `total += i` | `99` → `2500` |
| 2 | `is_prime` becoming `True` at `d = 3` for `n = 9` | `is_prime = True` (inside `if n % d == 0`) | a divisor means the number is **not** prime | `is_prime = False` | `9 True` → `9 False` |
| 3 | `count` stuck at `0` although `ch == "a"` matched | `count + 1` | increment `count` (assign the result) | `count += 1` | `0` → `3` |
| 4 | `largest` stuck at `0` (every `v` is negative) | `largest = 0` | start from a value actually in the list | `largest = values[0]` | `0` → `-1` |
| 5 | `IndexError` on the first step (`word[5]`) | `i = len(word)` | the last valid index is `len - 1` | `i = len(word) - 1` | `IndexError` → `olleh` |

Final output of `debug_exercise.py`:

```
bug 1: 2500
bug 2: 9 False
bug 3: 3
bug 4: -1
bug 5: olleh
```

---

## Part 5 — Reflection

### Q1. Classify each of the five bugs

| Bug | Class |
|-----|-------|
| 1 | wrong **accumulation** (`=` instead of `+=`) |
| 2 | wrong **update** (set the flag the wrong way) |
| 3 | wrong **update** (`count + 1` discards the result) |
| 4 | wrong **initialisation** (`largest = 0`) |
| 5 | wrong **condition/bound** (`i` starts past the last index) |

### Q2. Bug 4's `largest` started at `0`

The invariant *"`largest` is the largest value seen so far"* was false before the loop: `0` had never
been seen, yet it was treated as the running maximum. For a list whose values are all negative
(`[-1, -5, -3]`) that is larger than every real value, so nothing ever updates and `0` is printed.
Starting from `values[0]` makes the invariant true before the first iteration (the first value *is*
the largest seen so far) and restores the correct result, `-1`.
