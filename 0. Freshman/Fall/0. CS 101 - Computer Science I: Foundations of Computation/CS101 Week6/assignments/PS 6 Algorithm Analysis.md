# CS 101 · Problem Set 6
## Algorithm Analysis: Classifying and Proving Big-O Bounds

**Released:** Friday, Week 6
**Due:** Friday, Week 7 at 11:59 PM
**Submission:** Upload `ps6.py` and `PS 6 Algorithm Analysis.md`
**Weight:** Part of the 30% Problem Sets grade

**Note:** This problem set is intentionally proof-heavy and analysis-focused rather than implementation-heavy — it consolidates the formal reasoning skills from this week, which underpin every algorithms course you'll take from here forward.

---

## Overview

This problem set covers:
- Formal proofs of O(), Ω(), Θ() using the epsilon-n₀ definitions
- Analyzing loops (sequential, nested, triangular, halving)
- Writing and solving recurrence relations (recursion tree, substitution, Master Theorem)
- Classifying real code by complexity class
- Amortized analysis
- Empirical verification of theoretical predictions

---

## Part A: Formal Proofs (`PS 6 Algorithm Analysis.md`)

### A1: Big-O Proofs (10 points)

For each claim, write a complete formal proof: state the constants c and n₀ you choose, then verify the inequality holds.

**(a)** Prove `4n³ + 2n² + 100 = O(n³)`.

**(b)** Prove `n log n + n = O(n log n)`.

**(c)** Prove `2n + 5 = O(n²)`. (This shows a smaller-order function is still a valid — if loose — upper bound.)

**(d)** Disprove `n² = O(n)`. That is, show that NO constants c and n₀ can satisfy the definition. (Hint: assume such c, n₀ exist and derive a contradiction by considering n > c.)

---

### A2: Big-Ω and Big-Θ Proofs (8 points)

**(a)** Prove `n² - 10n = Ω(n²)` for n ≥ 20. (Find c and n₀.)

**(b)** Using your results from A1(a) and A2 (adapting as needed), prove `4n³ + 2n² + 100 = Θ(n³)`.

**(c)** Is `n = Ω(n²)`? Justify your answer (either prove it or disprove it as in A1d).

**(d)** True or False, with justification: "If f(n) = O(g(n)), then g(n) = Ω(f(n))." (This is asking you to verify the symmetric relationship between O and Ω.)

---

### A3: Recurrence Relations (10 points)

For each recurrence, solve it using the **method indicated** and show your work.

**(a)** `T(n) = T(n-1) + n`, `T(0) = 0`. Solve by **expansion/substitution** (write out several terms, spot the pattern, prove by induction).

**(b)** `T(n) = 3T(n/2) + n`. Solve using the **Master Theorem**. Show the calculation of `n^(log_b a)` and identify which case applies.

**(c)** `T(n) = 4T(n/2) + n²`. Solve using the **Master Theorem**. Show your work.

**(d)** `T(n) = 2T(n/2) + n²`. Solve using the **Master Theorem**. Show your work. (Compare your answer to part (c) — same coefficient 'a' and different combine cost, or vice versa. Which case do you land in for each, and why does it matter?)

**(e)** `T(n) = T(n/3) + T(2n/3) + n`. This does NOT fit the standard Master Theorem template (unequal split sizes). Solve using a **recursion tree**, being careful about the tree's depth (hint: the tree is unbalanced — the n/3 side terminates faster than the 2n/3 side; find the depth of the LONGEST path).

---

### A4: Code Analysis (8 points)

For each function, state the exact Big-O time complexity and explain your reasoning in 1-2 sentences.

```python
# (a)
def f(n):
    i = n
    count = 0
    while i > 1:
        i = i // 3
        count += 1
    return count

# (b)
def g(n):
    total = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                total += 1
    return total

# (c)
def h(lst):
    n = len(lst)
    if n <= 1:
        return lst
    mid = n // 2
    left = h(lst[:mid])
    right = h(lst[mid:])
    combined = []
    for x in left:
        for y in right:
            combined.append(x + y)
    return combined

# (d)
def k(n):
    if n <= 0:
        return 0
    result = 0
    for i in range(n):
        result += i
    return result + k(n - 1)
```

---

## Part B: Python Implementation (`ps6.py`)

### B1: Empirical Complexity Verification Tool (14 points)

Build a reusable tool that empirically classifies a function's complexity.

**(a)** `time_function(func, arg_generator, sizes)` — for each `n` in `sizes`, generate the argument using `arg_generator(n)`, time `func(argument)`, and return a list of `(n, time)` pairs.

**(b)** `fit_power_law(measurements)` — given `(n, time)` pairs, use log-log linear regression (from lab) to estimate the exponent k assuming `T(n) = c * n^k`. Return `(c, k)` — both the estimated constant and exponent.

**(c)** `predict_time(c, k, n)` — given fitted parameters, predict the time for a new value of n. Use this to predict `T(n)` for an n **larger** than any you actually measured, and compare against a real measurement at that n to check the prediction's accuracy.

**(d)** `classify(k)` — map an estimated exponent to a human-readable string: "O(1)", "O(log n)"(k≈0), "O(n)"(k≈1), "O(n log n)"(k≈1.1-1.5, use judgment), "O(n²)"(k≈2), "O(n³)"(k≈3), or "unknown" if it doesn't cleanly match.

**(e)** Apply your tool to at least 4 functions of your choice (some from lecture, some you write yourself) and print a table: function name | measured exponent | classification | matches theoretical prediction? (yes/no)

---

### B2: Complexity Classification Exercises (16 points)

Implement each function AND determine its complexity. Write the complexity as a comment above each function.

**(a)** `all_triples_sum_to_zero(lst)` — return True if any three DISTINCT elements sum to zero. Naive O(n³) implementation (three nested loops).

**(b)** `all_triples_sum_to_zero_fast(lst)` — same problem, but O(n²): sort first, then for each element, use a two-pointer technique on the remainder to find a pair summing to its negation.

**(c)** `matrix_multiply(A, B)` — naive matrix multiplication for two n×n matrices (represented as lists of lists). State why this is O(n³).

**(d)** `count_inversions_On2(lst)` — O(n²) inversion counting (nested loops, from PS5 if you recall it).

**(e)** `count_inversions_Onlogn(lst)` — O(n log n) inversion counting using a modified merge sort: during the merge step, whenever an element from the right list is taken before an element from the left list, all *remaining* elements in the left list form inversions with it — count them all at once.

**(f)** Benchmark (d) and (e) on the same random inputs of increasing size and verify empirically that (e) scales better, printing your results.

---

### B3: Recursion Complexity Deep Dive (12 points)

For each function: (i) write its recurrence relation as a comment, (ii) solve it (state the method used), (iii) implement it, (iv) verify with tests.

**(a)** `tribonacci(n)` — like Fibonacci but summing the previous THREE terms: T(0)=0, T(1)=0, T(2)=1, T(n)=T(n-1)+T(n-2)+T(n-3). Implement naively (no memoization) and state its complexity (it will not have a simple closed form via Master Theorem — argue informally that it's exponential, similar to Fibonacci but with a different growth base).

**(b)** `tribonacci_memo(n)` — memoized version. State the improved complexity.

**(c)** `karatsuba_multiply(x, y)` — multiply two n-digit numbers using Karatsuba's divide-and-conquer algorithm (see Week 4 PS4 Challenge C1 if you attempted it, or implement fresh here). Recurrence: `T(n) = 3T(n/2) + O(n)`. Solve using the Master Theorem and state the resulting complexity class. Compare against naive O(n²) multiplication.

**(d)** `closest_pair_2d(points)` — given a list of 2D points, find the pair with minimum Euclidean distance, using the classic divide-and-conquer algorithm: sort by x-coordinate, split in half, recursively solve each half, then check a narrow "strip" near the dividing line for closer cross-boundary pairs. Recurrence: `T(n) = 2T(n/2) + O(n)` (the strip-check is linear if points are also sorted by y). State the resulting complexity and compare to the naive O(n²) all-pairs approach.

---

### B4: Amortized Analysis in Practice (10 points)

**(a)** `DynamicArray` class — implement a simple dynamic array that doubles its capacity when full (similar to how Python lists work internally). Track and expose the total number of element copies performed across all `append` calls.
- Methods: `append(value)`, `__getitem__(i)`, `__len__()`

**(b)** `measure_amortized_cost(n)` — create a `DynamicArray`, append n elements, and return `total_copies / n` (the amortized number of copy-operations per append). Verify this stays bounded (roughly constant) as n grows, even though individual `append` calls occasionally trigger an O(current_size) resize.

**(c)** Run `measure_amortized_cost` for n = 1000, 10000, 100000, 1000000 and print the results. Confirm the ratio stays roughly constant (bounded by a small constant, typically less than 3 for a doubling strategy), demonstrating O(1) amortized cost per append.

**(d)** In `PS 6 Algorithm Analysis.md`, explain in your own words (3-4 sentences) why a resize factor of exactly 1.0 (i.e., growing the array by a fixed amount like +1 each time it's full) would make appends O(n) amortized instead of O(1) amortized. This is why real dynamic arrays always grow **multiplicatively** (doubling, or by a factor like 1.5×), never by a fixed additive amount.

---

## Grading Rubric

| Problem | Points | Key Criteria |
|---------|--------|--------------|
| A1 Big-O proofs | 10 | Correct constants, valid inequality verification for all 4 |
| A2 Big-Ω/Θ proofs | 8 | Correct constants; correct True/False with justification |
| A3 Recurrences | 10 | Correct method used as specified; correct final answer for all 5 |
| A4 Code analysis | 8 | Correct Big-O and valid reasoning for all 4 |
| B1 Empirical tool | 14 | All 5 parts functional; sensible classification |
| B2 Classification exercises | 16 | All 6 correct; complexity comments accurate; (e) genuinely faster than (d) |
| B3 Recursion deep dive | 12 | All 4 correct; recurrences and solutions accurate |
| B4 Amortized analysis | 10 | Correct DynamicArray; ratio stays bounded; explanation correct |
| **Total** | **88** | |
| Proof rigor/clarity | up to 5 bonus | |

---

## Part C: Challenge Problems (Ungraded)

**C1: Strassen's Algorithm**
Naive matrix multiplication is O(n³). Strassen's algorithm (1969) achieves O(n^log₂7) ≈ O(n^2.807) using a clever 7-multiplication (instead of 8) divide-and-conquer scheme. Research and implement Strassen's algorithm for matrices of size 2^k × 2^k. Verify correctness against naive multiplication, and benchmark the crossover point where Strassen's becomes faster in practice (accounting for its larger constant factor).

**C2: The Master Theorem's Fourth Case**
The version of the Master Theorem presented in lecture has a technical "regularity condition" for Case 3 that we glossed over. Research the precise regularity condition (`a·f(n/b) ≤ c·f(n)` for some c<1) and construct a recurrence where Case 3's polynomial-difference condition holds BUT the regularity condition fails — showing the Master Theorem does not apply even though it looks like it should.

**C3: Competitive Analysis**
Research "competitive analysis" for online algorithms (algorithms that must make decisions without knowing future input, like the ski-rental problem or paging/caching algorithms). Write a 300-word summary connecting this to amortized analysis — how are they similar, and how do they differ?

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading Rubric above (88 points).
> No errata found — but see the **A4(c) trap** below, which most students (and most graders) will get wrong.

---

### Part A — Formal Proofs (36 points)

**A1 Big-O Proofs (10 pts).**

**(a)** `4n³ + 2n² + 100 = O(n³)`. Take **c = 106, n₀ = 1**. For n ≥ 1: `n² ≤ n³` and `100 ≤ 100n³`, so `4n³ + 2n² + 100 ≤ 4n³ + 2n³ + 100n³ = 106n³`. ✓
*(Any valid pair is acceptable — e.g. c = 5, n₀ = 6 also works. Grade the verification, not the specific constants.)*

**(b)** `n log n + n = O(n log n)`. Take **c = 2, n₀ = 2**. For n ≥ 2, `log₂ n ≥ 1`, so `n ≤ n log n`, giving `n log n + n ≤ 2n log n`. ✓
*The `n₀ = 2` matters: at n = 1, `log₂ 1 = 0` so `n log n = 0` while `n = 1`, and no constant works. Deduct 1 if the student uses n₀ = 1.*

**(c)** `2n + 5 = O(n²)`. Take **c = 7, n₀ = 1**. For n ≥ 1: `2n ≤ 2n²` and `5 ≤ 5n²`, so `2n + 5 ≤ 7n²`. ✓ Big-O is an **upper** bound, not a tight one — a loose bound is still formally correct.

**(d)** Disprove `n² = O(n)`. Suppose constants `c > 0, n₀` exist with `n² ≤ cn` for all `n ≥ n₀`. Dividing by `n > 0` gives `n ≤ c` for all `n ≥ n₀`. But choosing `n = max(n₀, ⌊c⌋ + 1)` yields `n > c`, contradicting the inequality. No such constants exist. ∎

*Grading: 2 pts each (a)(b)(c) — 1 for stating constants, 1 for verifying the inequality. 4 pts (d) — a proof by contradiction is required; "n² grows faster, obviously" earns 1.*

**A2 Big-Ω / Big-Θ (8 pts).** 2 pts each.

**(a)** `n² − 10n = Ω(n²)`. Take **c = ½, n₀ = 20**. For n ≥ 20: `10n ≤ ½n²` (since `n ≥ 20` ⟹ `20n ≤ n²`), so `n² − 10n ≥ n² − ½n² = ½n²`. ✓

**(b)** `4n³ + 2n² + 100 = Θ(n³)`. Upper bound from A1(a) (c = 106). Lower bound: for n ≥ 1, `4n³ + 2n² + 100 ≥ 4n³`, so c = 4 works. Since it is both `O(n³)` and `Ω(n³)`, it is `Θ(n³)`. ∎

**(c)** **No.** `n = Ω(n²)` would require `n ≥ cn²` for all large n, i.e. `1 ≥ cn` — but `n` grows without bound, so for `n > 1/c` this fails. Same contradiction structure as A1(d).

**(d)** **True.** `f = O(g)` means `∃ c, n₀ : f(n) ≤ c·g(n)` for `n ≥ n₀`. Rearranging, `g(n) ≥ (1/c)·f(n)`, which is exactly the definition of `g = Ω(f)` with constant `1/c` (valid since `c > 0`). The relationship is genuinely symmetric — O and Ω are transposes of one another.

**A3 Recurrences (10 pts).** 2 pts each.

**(a)** `T(n) = T(n−1) + n, T(0) = 0`. Expanding: `T(n) = n + (n−1) + … + 1 = n(n+1)/2`. Induction: base `T(0)=0=0·1/2` ✓; step `T(k+1) = (k+1) + k(k+1)/2 = (k+1)(k+2)/2` ✓. → **Θ(n²)**.

**(b)** `T(n) = 3T(n/2) + n`. `a=3, b=2`, `n^(log₂3) = n^1.585`. Since `f(n) = n = O(n^(1.585−ε))`, this is **Case 1** → **Θ(n^log₂3) ≈ Θ(n^1.585)**.

**(c)** `T(n) = 4T(n/2) + n²`. `a=4, b=2`, `n^(log₂4) = n²`. `f(n) = n² = Θ(n²)` — they match → **Case 2** → **Θ(n² log n)**.

**(d)** `T(n) = 2T(n/2) + n²`. `a=2, b=2`, `n^(log₂2) = n`. `f(n) = n²` grows polynomially faster, and the regularity condition holds (`2(n/2)² = n²/2 ≤ ¾n²`) → **Case 3** → **Θ(n²)**.
*Comparison asked for in the prompt: (c) and (d) share the same combine cost `n²` but differ in `a`. In (c) the recursion exactly balances the combine work, so every level costs the same and a `log n` factor appears. In (d) the root dominates — the work shrinks geometrically down the tree, so the top level alone determines the answer. **The branching factor decides which term wins.***

**(e)** `T(n) = T(n/3) + T(2n/3) + n`. Every level sums to `n` (the fractions partition the input). The tree is unbalanced: the shallowest path shrinks by ⅓ each step (depth `log₃ n`), the **longest** path shrinks by ⅔ (depth `log_{3/2} n`). Total work ≤ `n · log_{3/2} n` → **Θ(n log n)**.
*Grading: award full marks for `Θ(n log n)` with the longest-path depth identified; deduct 1 if the student uses `log₃ n` (the short path) and thus understates the depth.*

**A4 Code Analysis (8 pts).** 2 pts each.

- **(a) `f(n)` — Θ(log n).** `i` is divided by 3 each pass, so the loop runs `log₃ n` times. Base of the log is a constant factor, hence `O(log n)`.
- **(b) `g(n)` — Θ(n³).** Three independent nested loops each running exactly n times.
- **(c) `h(lst)` — Θ(n log n). ⚠️ This is a trap.** The tempting answer is O(n²) from the `left × right` double loop. But trace it: the base case returns a list of length 1, so `len(left) = len(right) = 1` at *every* level, meaning the double loop always runs exactly **once**. (In fact `h` computes the sum of the list — `h([1..16])` returns `[136]`.) The real cost is the **slicing**: `lst[:mid]` and `lst[mid:]` copy O(n) per call, giving `T(n) = 2T(n/2) + O(n)` → **Θ(n log n)**.
- **(d) `k(n)` — Θ(n²).** The loop is O(n) and it recurses on `n−1`: `T(n) = T(n−1) + n` → `n(n+1)/2`.

*Grading note for (c): accept **Θ(n log n)** for full marks. Award 1 of 2 for a well-argued O(n²) that explicitly reasons about `len(left) × len(right)` but fails to notice the lists are singletons — the reasoning is sound, the premise isn't. Award 0 for an unjustified "O(n²), three loops". This item is worth flagging in the post-mortem: it rewards actually tracing the code over pattern-matching on loop nesting.*

---

### Part B — Coding (52 points)

**B1 Empirical Complexity Tool (14 pts).** 3 pts (a), 4 pts (b), 2 pts (c), 2 pts (d), 3 pts (e).
*Log-log regression: `log T = log c + k log n`, so a least-squares fit of `log T` against `log n` gives slope `k` and intercept `log c`. Grade (b) on the fit being genuine regression, not a two-point slope. For (c), the extrapolation check is the graded artifact — a prediction within ~2× of measurement is a pass at these timescales.*
*Expect the measured exponent for `O(n log n)` to land near 1.05–1.2 for reachable n, **not** 1.1–1.5 as the prompt's band suggests. Do not penalise a student whose merge-sort fit reads 1.08 and who classifies it correctly with justification — the log factor is nearly invisible to a power-law fit over two decades.*

**B2 Classification Exercises (16 pts).** ~2.7 pts each.

```python
def all_triples_sum_to_zero_fast(lst):          # O(n^2) after the O(n log n) sort
    a = sorted(lst)
    for i in range(len(a) - 2):
        lo, hi = i + 1, len(a) - 1
        while lo < hi:
            s = a[i] + a[lo] + a[hi]
            if s == 0:  return True
            elif s < 0: lo += 1                  # need a larger sum
            else:       hi -= 1
    return False

def count_inversions_Onlogn(lst):
    def sc(a):
        if len(a) <= 1: return a, 0
        m = len(a) // 2
        L, x = sc(a[:m]); R, y = sc(a[m:])
        out, inv, i, j = [], x + y, 0, 0
        while i < len(L) and j < len(R):
            if L[i] <= R[j]: out.append(L[i]); i += 1
            else:
                out.append(R[j]); j += 1
                inv += len(L) - i                # all remaining L elements invert with R[j]
        return out + L[i:] + R[j:], inv
    return sc(lst)[1]
```

*The `inv += len(L) - i` line is the whole point of (e) — it counts a block of inversions in O(1) instead of one at a time. Deduct 3 if the student merges correctly but counts inversions by an inner loop (that is still O(n²)).*
*(c) is O(n³) because the result has n² entries and each requires an n-term dot product. (f) must show actual timings; verify (e) genuinely wins at n ≥ 2000 — below that the constants can mask the difference.*

**B3 Recursion Deep Dive (12 pts).** 3 pts each.
- **(a) `tribonacci`** — `T(n) = T(n−1)+T(n−2)+T(n−3)+O(1)`, exponential. The growth base is the real root of `x³ = x² + x + 1`, the **tribonacci constant ≈ 1.8393**, so `Θ(1.8393ⁿ)`. This grows **faster** than naive Fibonacci (`φ ≈ 1.6180`) because each call spawns three branches instead of two. Verified empirically: successive call counts for n = 10…20 give ratios converging to 1.8393. Accept any argument that it is exponential with a base strictly between φ and 2; the exact constant is bonus-worthy, not required.
- **(b) `tribonacci_memo`** — each of n subproblems solved once → **Θ(n)** time, Θ(n) space.
- **(c) `karatsuba`** — `T(n) = 3T(n/2) + O(n)`; Master Case 1 → **Θ(n^log₂3) ≈ Θ(n^1.585)**, beating naive `Θ(n²)`. Note this is *the same recurrence as A3(b)* — call that out if the student doesn't.
- **(d) `closest_pair_2d`** — `T(n) = 2T(n/2) + O(n)` → **Θ(n log n)** vs naive `Θ(n²)`. The subtle correctness fact: only **7 subsequent points** in the y-sorted strip need checking per point, which is what keeps the strip scan linear.

**B4 Amortized Analysis (10 pts).** Verified with a doubling implementation:

| n | total copies | copies / append |
|---|---|---|
| 1,000 | 1,023 | 1.02 |
| 10,000 | 16,383 | 1.64 |
| 100,000 | 131,071 | 1.31 |
| 1,000,000 | 1,048,575 | 1.05 |

The ratio oscillates between roughly 1.0 and 2.0 depending on where `n` sits relative to the next power of two, but never grows with `n` — that boundedness *is* the O(1) amortized result. Total copies before reaching size n is `1 + 2 + 4 + … < 2n`.

**(d)** With additive growth (+1 each resize), a resize happens on **every** append, copying the entire array: total copies `= 0 + 1 + 2 + … + (n−1) = n(n−1)/2`, so amortized cost is `(n−1)/2 = Θ(n)` per append. Measured: 499.5 copies/append at n = 1,000 and 4,999.5 at n = 10,000 — the ratio scales linearly with n, exactly as predicted. Multiplicative growth works because the *number* of resizes drops to `log₂ n` while the copy cost forms a geometric series summing to `O(n)`.

*Grading: 4 pts (a), 2 pts (b), 2 pts (c) — must show the ratio across several n — 2 pts (d). Accept ratios anywhere in 1.0–2.0; a student reporting a constant near 2.0 has likely counted the write as a copy, which is fine if stated.*
*Common misconception in (d): "it's O(n) because each resize is O(n)". Incomplete — doubling *also* has O(n) resizes. The distinguishing fact is **how many** resizes occur: `n` versus `log n`.*

---

*CS 101 · Week 6 · Problem Set 6 · Due Friday Week 7 · © CSE Department*
