# CS 101 · Lab 6
## Plotting Empirical Runtime vs. Theoretical Complexity

**Tuesday of Week 7 · Lab Section** — sat after this week's Wed–Fri lectures, and covers Week 6.
*Duration: 2 hours · Graded on completion (TA checkoff)*

---

## Objectives

By the end of this lab, you will:
- [ ] Analyze the theoretical complexity of 8 functions by hand
- [ ] Empirically measure their runtimes across increasing input sizes
- [ ] Fit a curve to the data and estimate the complexity exponent
- [ ] Compare your theoretical predictions against empirical results
- [ ] Diagnose and explain any discrepancies
- [ ] Practice formal Big-O proofs with specific constants

---

## Setup

```bash
cd "$CS101"        # set in ~/.bashrc -- see Lab 0
mkdir -p week6 && cd week6
pip install matplotlib numpy --user   # if not already installed
```

---

## Part 1: Theoretical Analysis (30 minutes)

Before running any code, analyze each function **by hand**. Write your answer in `LAB 6 Empirical vs Theoretical Complexity.md` **before** proceeding to Part 2.

For each function, state:
(a) The Big-O time complexity
(b) The reasoning (which rule from Wednesday's lecture applies)
(c) The recurrence relation, if the function is recursive

```python
# Function A
def func_a(n):
    total = 0
    for i in range(n):
        total += i
    return total

# Function B
def func_b(n):
    total = 0
    for i in range(n):
        for j in range(n):
            total += i * j
    return total

# Function C
def func_c(n):
    count = 0
    i = 1
    while i < n:
        count += 1
        i *= 2
    return count

# Function D
def func_d(lst):
    """lst has length n."""
    return sorted(lst)   # Python's Timsort

# Function E
def func_e(n):
    if n <= 1:
        return 1
    return func_e(n - 1) + func_e(n - 1)

# Function F
def func_f(n):
    if n <= 1:
        return n
    return func_f(n - 1) + func_f(n - 2)

# Function G
def func_g(lst):
    """lst has length n. Checks for any duplicate pair."""
    n = len(lst)
    for i in range(n):
        for j in range(i + 1, n):
            if lst[i] == lst[j]:
                return True
    return False

# Function H
def func_h(n):
    if n <= 1:
        return n
    return func_h(n // 2) + func_h(n // 2) + n
```

**Fill out this table in `LAB 6 Empirical vs Theoretical Complexity.md`:**

| Function | Big-O | Reasoning | Recurrence (if recursive) |
|----------|-------|-----------|----------------------------|
| A | | | |
| B | | | |
| C | | | |
| D | | | |
| E | | | |
| F | | | |
| G | | | |
| H | | | |

---

## Part 2: Empirical Measurement (40 minutes)

Create `benchmark_functions.py`.

```python
#!/usr/bin/env python3
"""
benchmark_functions.py
CS 101 — Week 6, Lab 6

Empirically measure the runtime of the 8 functions from Part 1.
"""

import time
import random
import sys

sys.setrecursionlimit(10000)


def func_a(n):
    total = 0
    for i in range(n):
        total += i
    return total


def func_b(n):
    total = 0
    for i in range(n):
        for j in range(n):
            total += i * j
    return total


def func_c(n):
    count = 0
    i = 1
    while i < n:
        count += 1
        i *= 2
    return count


def func_d(lst):
    return sorted(lst)


def func_e(n):
    if n <= 1:
        return 1
    return func_e(n - 1) + func_e(n - 1)


def func_f(n):
    if n <= 1:
        return n
    return func_f(n - 1) + func_f(n - 2)


def func_g(lst):
    n = len(lst)
    for i in range(n):
        for j in range(i + 1, n):
            if lst[i] == lst[j]:
                return True
    return False


def func_h(n):
    if n <= 1:
        return n
    return func_h(n // 2) + func_h(n // 2) + n


def time_it(func, arg, repeats=3):
    """Run func(arg) `repeats` times, return the minimum time (reduces noise)."""
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        func(arg)
        times.append(time.perf_counter() - start)
    return min(times)


def benchmark_numeric(func, sizes, name):
    """Benchmark a function that takes a single integer n."""
    print(f"\n--- {name} ---")
    results = []
    for n in sizes:
        elapsed = time_it(func, n)
        results.append((n, elapsed))
        print(f"  n={n:8}: {elapsed*1000:10.4f} ms")
    return results


def benchmark_list(func, sizes, name, sorted_input=False):
    """Benchmark a function that takes a list of length n."""
    print(f"\n--- {name} ---")
    results = []
    for n in sizes:
        if sorted_input:
            data = list(range(n))
        else:
            data = [random.randint(0, 1_000_000) for _ in range(n)]
        elapsed = time_it(func, data)
        results.append((n, elapsed))
        print(f"  n={n:8}: {elapsed*1000:10.4f} ms")
    return results


if __name__ == "__main__":
    import json

    all_results = {}

    # Functions A, B, C, H: numeric input. Use appropriately scaled sizes
    # since B is O(n^2) and E, F would explode for large n.
    all_results["func_a"] = benchmark_numeric(func_a, [1000, 10000, 100000, 1000000], "func_a — O(n)?")
    all_results["func_b"] = benchmark_numeric(func_b, [100, 200, 400, 800], "func_b — O(n^2)?")
    all_results["func_c"] = benchmark_numeric(func_c, [1000, 100000, 10000000, 1000000000], "func_c — O(log n)?")
    all_results["func_h"] = benchmark_numeric(func_h, [1000, 10000, 100000, 1000000], "func_h — O(n log n)?")

    # Function D, G: list input
    all_results["func_d"] = benchmark_list(func_d, [1000, 10000, 100000, 1000000], "func_d — O(n log n)?")
    all_results["func_g"] = benchmark_list(func_g, [100, 200, 400, 800], "func_g — O(n^2)?")

    # Functions E, F: EXPONENTIAL — use small sizes only!
    all_results["func_e"] = benchmark_numeric(func_e, [10, 15, 18, 20], "func_e — O(2^n)?")
    all_results["func_f"] = benchmark_numeric(func_f, [15, 20, 25, 28], "func_f — O(2^n)?")

    with open("benchmark_results.json", "w") as fp:
        json.dump(all_results, fp, indent=2)

    print("\nResults saved to benchmark_results.json")
```

**⚠️ Warning:** Do not run `func_e(30)` or `func_f(35)` — they will take an extremely long time. Stay within the suggested sizes.

Run: `python3 benchmark_functions.py`

---

## Part 3: Estimating the Complexity Exponent (30 minutes)

Create `analyze_growth.py`:

```python
#!/usr/bin/env python3
"""
analyze_growth.py
CS 101 — Week 6, Lab 6

Fit a curve to empirical measurements and estimate the complexity class.
"""

import json
import math


def estimate_polynomial_exponent(measurements):
    """
    Given (n, time) pairs, estimate k assuming T(n) ≈ c * n^k.

    Method: take log of both n and time, fit a line.
    slope of the line ≈ k.

    Returns the estimated exponent (float).
    """
    # Filter out any zero times (too fast to measure — avoid log(0))
    valid = [(n, t) for n, t in measurements if t > 0]
    if len(valid) < 2:
        return None

    log_ns    = [math.log(n) for n, t in valid]
    log_times = [math.log(t) for n, t in valid]

    # Simple linear regression: slope = covariance(x,y) / variance(x)
    n_points = len(valid)
    mean_x = sum(log_ns) / n_points
    mean_y = sum(log_times) / n_points

    numerator   = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_ns, log_times))
    denominator = sum((x - mean_x) ** 2 for x in log_ns)

    if denominator == 0:
        return None

    slope = numerator / denominator
    return slope


def estimate_exponential_base(measurements):
    """
    Given (n, time) pairs, estimate b assuming T(n) ≈ c * b^n.

    Method: take log of time only (not n), fit against n directly.
    slope of log(time) vs n ≈ log(b).

    Returns the estimated base b (float).
    """
    valid = [(n, t) for n, t in measurements if t > 0]
    if len(valid) < 2:
        return None

    ns        = [n for n, t in valid]
    log_times = [math.log(t) for n, t in valid]

    n_points = len(valid)
    mean_x = sum(ns) / n_points
    mean_y = sum(log_times) / n_points

    numerator   = sum((x - mean_x) * (y - mean_y) for x, y in zip(ns, log_times))
    denominator = sum((x - mean_x) ** 2 for x in ns)

    if denominator == 0:
        return None

    slope = numerator / denominator
    base_estimate = math.exp(slope)
    return base_estimate


if __name__ == "__main__":
    with open("benchmark_results.json") as f:
        results = json.load(f)

    print("=" * 60)
    print("POLYNOMIAL EXPONENT ESTIMATES (assumes T(n) ~ n^k)")
    print("=" * 60)
    for name in ["func_a", "func_b", "func_d", "func_g", "func_h"]:
        measurements = results[name]
        k = estimate_polynomial_exponent(measurements)
        print(f"  {name}: estimated exponent k ≈ {k:.2f}")

    print()
    print("=" * 60)
    print("LOGARITHMIC CHECK (func_c should show near-ZERO exponent")
    print("since O(log n) grows much slower than any power of n)")
    print("=" * 60)
    k_c = estimate_polynomial_exponent(results["func_c"])
    print(f"  func_c: estimated exponent k ≈ {k_c:.3f}  (expect close to 0)")

    print()
    print("=" * 60)
    print("EXPONENTIAL BASE ESTIMATES (assumes T(n) ~ b^n)")
    print("=" * 60)
    for name in ["func_e", "func_f"]:
        measurements = results[name]
        b = estimate_exponential_base(measurements)
        print(f"  {name}: estimated base b ≈ {b:.2f}  (expect ≈ 2.0 for func_e, ≈ 1.618 for func_f)")
```

Run: `python3 analyze_growth.py`

**Why func_f's base should be ≈1.618 (the golden ratio):** naive Fibonacci's recursion tree grows by a factor related to the golden ratio φ = (1+√5)/2 ≈ 1.618 at each level, not exactly 2 — this is a well-known refinement of the "O(2ⁿ)" bound (the *tight* bound is Θ(φⁿ), which is a smaller base than 2 but still exponential).

**Record in `LAB 6 Empirical vs Theoretical Complexity.md`:**
1. For each function, compare the theoretical Big-O (from Part 1) against the empirically estimated exponent. Do they match?
2. `func_c` should show an exponent close to 0 (since O(log n) is much slower-growing than any polynomial). Explain why fitting `log(n)` data to a `n^k` model gives a near-zero k.
3. Which function(s), if any, had a noticeable **mismatch** between theory and measurement? Investigate: is the theoretical analysis wrong, or is the empirical measurement affected by something (e.g., too few data points, timing noise, constant-factor effects at small n)?

---

## Part 4: Visualizing the Comparison (20 minutes)

Create `plot_comparison.py`:

```python
#!/usr/bin/env python3
"""
plot_comparison.py
CS 101 — Week 6, Lab 6

Overlay empirical measurements against theoretical curves.
"""

import json
import math
import matplotlib.pyplot as plt

with open("benchmark_results.json") as f:
    results = json.load(f)

# Compare func_b (should be O(n^2)) against theoretical n^2 curve:
measurements = results["func_b"]
ns    = [n for n, t in measurements]
times = [t for n, t in measurements]

# Normalize theoretical curve to match at the last data point:
c = times[-1] / (ns[-1] ** 2)
theoretical = [c * n**2 for n in ns]

plt.figure(figsize=(8, 6))
plt.plot(ns, times, 'o-', label="Empirical (func_b)")
plt.plot(ns, theoretical, '--', label="Theoretical O(n²)")
plt.xlabel("n")
plt.ylabel("Time (s)")
plt.title("func_b: Empirical vs Theoretical O(n²)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("func_b_comparison.png", dpi=100)
print("Saved func_b_comparison.png")

# Compare func_d (should be O(n log n)) against theoretical curve:
measurements_d = results["func_d"]
ns_d    = [n for n, t in measurements_d]
times_d = [t for n, t in measurements_d]

c_d = times_d[-1] / (ns_d[-1] * math.log2(ns_d[-1]))
theoretical_d = [c_d * n * math.log2(n) for n in ns_d]

plt.figure(figsize=(8, 6))
plt.plot(ns_d, times_d, 'o-', label="Empirical (func_d / Timsort)")
plt.plot(ns_d, theoretical_d, '--', label="Theoretical O(n log n)")
plt.xlabel("n")
plt.ylabel("Time (s)")
plt.title("func_d: Empirical vs Theoretical O(n log n)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("func_d_comparison.png", dpi=100)
print("Saved func_d_comparison.png")

plt.show()
```

**Record in `LAB 6 Empirical vs Theoretical Complexity.md`:** For each plot, describe how closely the empirical curve tracks the theoretical curve. Where do they diverge, and why might that be (hint: think about constant factors, Python interpreter overhead, and small-n effects)?

---

## Part 5: Formal Big-O Proofs (20 minutes)

Practice writing rigorous proofs. Work these on paper in `LAB 6 Empirical vs Theoretical Complexity.md`.

**Exercise 5.1:** Prove that `3n² + 5n + 2 = O(n²)` by finding specific constants c and n₀.

**Exercise 5.2:** Prove that `100n = O(n²)` by finding specific constants c and n₀. (This shows Big-O upper bounds are not tight — a smaller function can still be O of a larger one.)

**Exercise 5.3:** Prove that `n² = Ω(n)` by finding specific constants c and n₀. (This shows the reverse doesn't generally hold: a bigger function is a valid lower bound for a smaller one, but this seems backwards at first — think carefully about what Ω means and double check your direction.)

**Exercise 5.4:** Is `2ⁿ = O(n^100)`? Justify your answer without a formal proof — just explain the reasoning (this connects to the fact that exponential functions eventually exceed ANY polynomial, no matter how high the degree).

---

## Part 6: Commit and Reflection (10 minutes)

```bash
cd "$CS101/week6"
git add .
git commit -m "Week 6 Lab: empirical vs theoretical complexity analysis"
git push
```

### Reflection in `LAB 6 Empirical vs Theoretical Complexity.md`:

**Q1.** For `func_h` (the recursive function with two calls on n/2 plus O(n) combine work), what recurrence did you write in Part 1? Does the Master Theorem apply? What case, and what's the result?

**Q2.** The exponential functions (`func_e`, `func_f`) had to be tested on much smaller n than the polynomial ones. Explain, using actual numbers, why testing `func_e(40)` would be impractical (estimate the time it would take, given your measurements for smaller n).

**Q3.** Your empirical measurements always have some noise (timing variance). Why does the lab instruct you to take the minimum of several repeated runs, rather than the average or a single run?

**Q4.** Big-O analysis says `func_a` and `func_c` are both "fast" (O(n) and O(log n) respectively), but for large enough n, `func_c` will always eventually be faster. Using your data, at what n (roughly) does this become visible in your measurements? Does this match what the math predicts?

---

## TA Checkoff Criteria

Show your TA:
- [ ] `LAB 6 Empirical vs Theoretical Complexity.md` Part 1 table completed BEFORE running any code
- [ ] `benchmark_functions.py` output for all 8 functions
- [ ] `analyze_growth.py` output with exponent/base estimates
- [ ] Both comparison plots generated
- [ ] All 4 formal Big-O proofs in Part 5
- [ ] Reflection questions answered

---

## Bonus Challenges

**Bonus 1:** Extend `analyze_growth.py` to automatically classify each function into one of: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ) based on the estimated exponent/base, printing a best-guess label.

**Bonus 2:** Measure `func_f` (naive Fibonacci) and verify that the ratio of successive terms `T(n+1)/T(n)` approaches the golden ratio φ ≈ 1.618, not 2. Explain why the *tight* bound for Fibonacci is Θ(φⁿ) rather than the looser Θ(2ⁿ).

**Bonus 3:** Write a version of `func_g` (duplicate checker) that runs in O(n log n) instead of O(n²) by sorting first, then checking adjacent elements. Benchmark it against the original and confirm the improvement empirically.

---

*CS 101 · Week 6 · Lab 6 · © CSE Department*
