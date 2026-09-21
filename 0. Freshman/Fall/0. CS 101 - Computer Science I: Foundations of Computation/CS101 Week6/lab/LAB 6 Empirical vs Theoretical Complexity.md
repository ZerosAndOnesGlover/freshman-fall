# CS 101 · Lab 6
## Counting Work: Empirical vs. Theoretical Complexity

**Date:** Tuesday 10 November 2026 · 15:00–16:50 · Lab Section (Week 7) — covers Week 6 (L19–L21)
*Duration: 2 hours · 100 points via TA checkoff, part of the Labs component (10%)*

---

## Objectives

By the end of this lab, you will:
- [ ] Analyse eight functions by hand before running anything
- [ ] Instrument them to count their own steps
- [ ] Estimate each growth exponent from counts at `n` and `2n` (L21 §3's idea, with exact counts instead of timings)
- [ ] Explain every place where your prediction and the count disagree
- [ ] Write formal Big-O proofs with explicit constants

**Tools used:** Weeks 0–6 only — functions, loops, `global` (L11), `math.log2` (L06 §5). No timing, no
plotting libraries, no files: step counts are exact and repeatable, so the growth shows without noise.

---

## Setup

```bash
mkdir -p "$CS101/week6"
cd "$CS101/week6"
```

Copy `count_growth_starter.py` from this week's `lab/` folder to `"$CS101/week6"`, renamed `count_growth.py`.

---

## Part 1: Theoretical Analysis (30 minutes) — 30 points

Before running any code, analyze each function **by hand**. Write your answer in `LAB 6 Empirical vs Theoretical Complexity.md` **before** proceeding to Part 2.

For each function, state:
(a) The Big-O time complexity
(b) The reasoning (which rule from L19 §6 or L20 applies)
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

## Part 2: Counting Steps (35 minutes) — 35 points

`count_growth.py` holds every function from Part 1 except D (Timsort's steps happen inside C code you
cannot instrument) and a global `ops`.

1. In each function, add `global ops` and `ops += 1` at its **innermost step**: inside the innermost
   loop for A, B, C and G; at the top of each call for the recursive E, F and H.
2. Run it. The starter prints, for A, B, C, G and H, the step count at `n` = 256, 512, 1024, 2048 and
   `k = log₂(steps(2n) / steps(n))`; for E and F, the ratio `steps(n+1) / steps(n)` for `n` = 16 … 20.
3. Copy the output into your notes.

If a function's steps grow like `nᵏ`, doubling `n` multiplies them by `2ᵏ`, so `log₂` of the ratio is `k`.

---

## Part 3: Prediction vs. Count (20 minutes) — 20 points

For each function, put your Part 1 answer next to what the counts say. Then answer:

1. C's `k` is not a constant: it shrinks (0.17, 0.15, 0.14 …). Why does a Θ(log n) function never show
   a steady `k`, and what does the count do instead each time `n` doubles?
2. G has an early `return`. Why does the count still come out at exactly `n(n−1)/2` here? What input
   would make it far smaller?
3. **H is a trap.** Did your Part 1 recurrence match the counts? Look closely at what `+ n` costs.
4. E grows ×2 per step and F ×1.618. Name the constant for F, and explain why F's bound Θ(2ⁿ) is true but not tight.

---

## Part 4: Formal Big-O Proofs (15 minutes) — 15 points

Work these on paper and copy them into your notes.

**Exercise 5.1:** Prove that `3n² + 5n + 2 = O(n²)` by finding specific constants c and n₀.

**Exercise 5.2:** Prove that `100n = O(n²)` by finding specific constants c and n₀. (This shows Big-O upper bounds are not tight — a smaller function can still be O of a larger one.)

**Exercise 5.3:** Prove that `n² = Ω(n)` by finding specific constants c and n₀. (Ω is a **lower** bound: you need `n² ≥ c·n` for all `n ≥ n₀`.)

**Exercise 5.4:** Is `2ⁿ = O(n^100)`? Justify your answer without a formal proof — just explain the reasoning (this connects to the fact that exponential functions eventually exceed ANY polynomial, no matter how high the degree).

---

## Part 5: Commit and Reflection

```bash
cd "$CS101/week6"
git add .
git commit -m "CS 101 Lab 6: step counts vs predicted complexity"
git push
```

In your notes: **Q1.** Using your E counts, estimate how many steps `func_e(40)` would take, and at a
billion steps a second, how long. **Q2.** Why are exact step counts easier to reason about than timings,
and what do they hide that a stopwatch would show?

---

## TA Checkoff Criteria

| Part | Points | Show your TA |
|---|---|---|
| 1 | 30 | The eight-row table, filled in **before** Part 2 |
| 2 | 35 | Instrumented functions; the output matches the reference counts |
| 3 | 20 | Four questions answered from your counts |
| 4 | 15 | Four proofs / justifications |
| **Total** | **100** | Reflection answered and work committed (required) |

---

*CS 101 · Week 6 · Lab 6 · Tuesday 10 November 2026 · © CSE Department*
