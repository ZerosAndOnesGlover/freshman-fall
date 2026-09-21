# CS 101 · Week 6
## LAB 6 Solutions: INSTRUCTOR ONLY

> Lab sat Tuesday 10 November 2026. **All code below was executed; the counts are real output** and are
> exact — every student's instrumented file should print the same numbers.

---

## Part 1 — Predictions (30)

| Function | Bound | Reasoning | Recurrence |
|---|---|---|---|
| A | Θ(n) | one loop, n iterations | — |
| B | Θ(n²) | two nested loops of n | — |
| C | Θ(log n) | `i` doubles until it reaches n | — |
| D | Θ(n log n) | Timsort (L18 §3); Θ(n) on already-sorted input | — |
| E | Θ(2ⁿ) | two calls on n − 1 | T(n) = 2T(n−1) + 1 |
| F | Θ(φⁿ), φ ≈ 1.618 (O(2ⁿ) accepted in Part 1) | calls on n − 1 and n − 2 | T(n) = T(n−1) + T(n−2) + 1 |
| G | Θ(n²) worst case | pairs i < j; early exit on a duplicate | — |
| H | **Θ(n)** | two calls on n/2, **O(1)** extra work — `+ n` adds a number, it does not loop | T(n) = 2T(n/2) + O(1) → Master case 1 |

*Most students write T(n) = 2T(n/2) + n → Θ(n log n) for H. That is the trap Part 3 exposes; do not
deduct in Part 1 if Part 3 catches and explains it.* 3.75 per row.

---

## Part 2 — Reference `count_growth.py` (35)

```python
#!/usr/bin/env python3
"""
count_growth.py — CS 101 Lab 6 (Tuesday 10 November 2026)
Each function adds 1 to the global `ops` every time its innermost step runs.
"""
import math

ops = 0


def func_a(n):
    global ops
    total = 0
    for i in range(n):
        ops += 1
        total += i
    return total


def func_b(n):
    global ops
    total = 0
    for i in range(n):
        for j in range(n):
            ops += 1
            total += i * j
    return total


def func_c(n):
    global ops
    count = 0
    i = 1
    while i < n:
        ops += 1
        count += 1
        i *= 2
    return count


def func_e(n):
    global ops
    ops += 1
    if n <= 1:
        return 1
    return func_e(n - 1) + func_e(n - 1)


def func_f(n):
    global ops
    ops += 1
    if n <= 1:
        return n
    return func_f(n - 1) + func_f(n - 2)


def func_g(lst):
    global ops
    n = len(lst)
    for i in range(n):
        for j in range(i + 1, n):
            ops += 1
            if lst[i] == lst[j]:
                return True
    return False


def func_h(n):
    global ops
    ops += 1
    if n <= 1:
        return n
    return func_h(n // 2) + func_h(n // 2) + n


def count_ops(func, arg):
    """Reset ops, run func(arg), return how many steps it counted."""
    global ops
    ops = 0
    func(arg)
    return ops


if __name__ == "__main__":
    print("Polynomial-looking functions: steps at n and 2n, and k = log2(ratio)")
    for name, func, make_arg in [("A", func_a, lambda n: n), ("B", func_b, lambda n: n),
                                 ("C", func_c, lambda n: n), ("G", func_g, lambda n: list(range(n))),
                                 ("H", func_h, lambda n: n)]:
        row = f"  {name}:"
        previous = None
        for n in [256, 512, 1024, 2048]:
            steps = count_ops(func, make_arg(n))
            if previous is not None:
                row += f"  n={n}: {steps} (k={math.log2(steps / previous):.2f})"
            else:
                row += f"  n={n}: {steps}"
            previous = steps
        print(row)

    print("\nExponential-looking functions: ratio of steps from n to n+1")
    for name, func in [("E", func_e), ("F", func_f)]:
        row = f"  {name}:"
        previous = None
        for n in range(16, 21):
            steps = count_ops(func, n)
            row += f"  n={n}: {steps}" + ("" if previous is None else f" (x{steps / previous:.3f})")
            previous = steps
        print(row)
```

Output:

```
Polynomial-looking functions: steps at n and 2n, and k = log2(ratio)
  A:  n=256: 256  n=512: 512 (k=1.00)  n=1024: 1024 (k=1.00)  n=2048: 2048 (k=1.00)
  B:  n=256: 65536  n=512: 262144 (k=2.00)  n=1024: 1048576 (k=2.00)  n=2048: 4194304 (k=2.00)
  C:  n=256: 8  n=512: 9 (k=0.17)  n=1024: 10 (k=0.15)  n=2048: 11 (k=0.14)
  G:  n=256: 32640  n=512: 130816 (k=2.00)  n=1024: 523776 (k=2.00)  n=2048: 2096128 (k=2.00)
  H:  n=256: 511  n=512: 1023 (k=1.00)  n=1024: 2047 (k=1.00)  n=2048: 4095 (k=1.00)

Exponential-looking functions: ratio of steps from n to n+1
  E:  n=16: 65535  n=17: 131071 (x2.000)  n=18: 262143 (x2.000)  n=19: 524287 (x2.000)  n=20: 1048575 (x2.000)
  F:  n=16: 3193  n=17: 5167 (x1.618)  n=18: 8361 (x1.618)  n=19: 13529 (x1.618)  n=20: 21891 (x1.618)
```

A student whose counts differ has put `ops += 1` somewhere other than the innermost step (for E, F, H:
not at the top of the call). 5 per function (7 functions).

---

## Part 3 — Prediction vs. Count (20, 5 each)

1. Doubling `n` adds **one** step to C (8, 9, 10, 11): Θ(log n) grows by a constant per doubling, so
   `log₂(ratio)` → 0 rather than settling at a positive `k`.
2. `list(range(n))` has no duplicates, so the early return never fires: exactly `n(n−1)/2` pairs
   (32640 at 256). Any list with a duplicate at the front, e.g. `[1, 1, …]`, returns after one comparison.
3. H makes `2n − 1` calls with constant work each: Θ(n), `k = 1.00`. The `+ n` is one addition, not n.
4. φ, the golden ratio. F's calls grow ×1.618 per step, so it is Θ(φⁿ); it is also O(2ⁿ) because
   φ < 2, but that bound overestimates by (2/φ)ⁿ.

## Part 4 — Proofs (15)

5.1 `3n² + 5n + 2 ≤ 3n² + 5n² + 2n² = 10n²` for n ≥ 1 (c = 10, n₀ = 1). 5.2 `100n ≤ n²` for n ≥ 100
(c = 1, n₀ = 100). 5.3 `n² ≥ n` for n ≥ 1 (c = 1, n₀ = 1). 5.4 No: `2ⁿ / n¹⁰⁰` → ∞ (for instance at
n = 1024, 2¹⁰²⁴ vs 2¹⁰⁰⁰), so no constant c can bound it. *4/4/4/3.*

## Reflection (required, not scored)

Q1: E doubles per step: about 2⁴¹ ≈ 2.2 × 10¹² steps at n = 40 — roughly 37 minutes at 10⁹ steps/s
(and Python manages far fewer than 10⁹). Q2: counts are exact and machine-independent; they hide the
cost of each step (a dict lookup and an addition count the same) and memory effects.

---

*CS 101 · Week 6 · Lab 6 Solutions · Instructor only*
