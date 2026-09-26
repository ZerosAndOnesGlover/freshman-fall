# CS 101 · Problem Set 6
## Algorithm Analysis: Classifying and Proving Big-O Bounds

**Released:** Friday 6 November 2026, 10:00 (after L21) · Week 6
**Due:** Friday 13 November 2026, 17:00 · Week 7 — late penalty from 17:01
**Submission:** `ps6.py` (Part B) and your answer sheet (Part A) in `"$CS101/week6"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 3 hours

*(Revised 2026-09-26: cut from about four hours to three. The Ω/Θ proofs (A2 — Lab 6 Part 4 does formal
proofs) and the tribonacci call count (B2) were removed, and the answer key moved out of this handout.)*

---

## What this problem set uses

Weeks 0–6, above all this week's: the formal definitions of O, Ω and Θ and loop analysis (L19),
writing recurrences and solving them by recursion tree, substitution and the Master Theorem, and the
amortized preview (L20), and connecting counts to growth (L21).

**Not needed and not expected:** timing code or fitting curves (you count operations exactly instead),
classes (Week 7), dictionaries or memoization (Week 8).

---

## Part A: Formal Analysis (48 points)

### A1: Big-O Proofs (14 points)

State the constants `c` and `n₀` and verify the inequality.

**(a)** `4n³ + 2n² + 100 = O(n³)`.
**(b)** `2n + 5 = O(n²)` — a loose bound is still a valid one.
**(c)** Disprove `n² = O(n)`: suppose `c` and `n₀` exist and derive a contradiction.

### A2: Recurrences (18 points)

**(a)** `T(n) = T(n−1) + n`, `T(0) = 0` — by **substitution**: expand, spot the pattern, prove it by induction.
**(b)** `T(n) = 3T(n/2) + n` — by the **Master Theorem**: compute `n^(log_b a)` and name the case.
**(c)** `T(n) = 4T(n/2) + n²` — Master Theorem.
**(d)** `T(n) = 2T(n/2) + n²` — Master Theorem. Compare with (c): same combine cost, different `a`. Why do they land in different cases?

### A3: Code Analysis (16 points)

Give the Θ-bound and explain in one or two sentences. **Trace (c) on a small list before you answer.**

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

## Part B: Python (`ps6.py`) (52 points)

Each function needs a docstring whose first line states its Θ-bound, and at least two `assert` tests.

### B1: Classifying Real Code (24 points)

**(a)** `has_zero_triple(lst)` — `True` if three elements at distinct positions sum to 0, using three
nested loops over `i < j < k`. `[-1, 0, 1]` → `True`; `[1, 2, 3]` → `False`; `[0, 0]` → `False`.
**(b)** `matrix_multiply(A, B)` — the product of two `n × n` matrices stored as lists of rows.
`[[1, 2], [3, 4]] × [[5, 6], [7, 8]]` → `[[19, 22], [43, 50]]`.
**(c)** `count_inversions(lst)` — pairs `i < j` with `lst[i] > lst[j]`. `[3, 1, 2]` → `2`; `[4, 3, 2, 1]` → `6`.

For each, state the bound and justify it by counting how many times the innermost statement runs.

### B2: Amortized Cost of Appends (28 points)

L20 §5 previews why `list.append` is O(1) amortized. Simulate it without building a real array:

**(a)** `simulate_appends(n, grow)` — start with capacity 1 and size 0. For each of `n` appends: if the
array is full, add `size` to a running copy count (every stored item is copied) and set
`capacity = grow(capacity)`; then increase `size`. Return the total copies.
**(b)** Print copies and copies-per-append for `n` = 1,000 … 1,000,000 with **doubling**
(`lambda c: 2 * c`), and for `n` = 1,000, 2,000, 4,000, 8,000 with **plus one** (`lambda c: c + 1`).
**(c)** In a comment: why does doubling keep copies-per-append below 2, and why does growing by one make
each append cost Θ(n) amortized?

---

## Grading Rubric

| Problem | Points |
|---------|--------|
| A1 Big-O proofs | 14 |
| A2 Recurrences | 18 |
| A3 Code analysis | 16 |
| B1 Classifying code | 24 |
| B2 Amortized appends | 28 |
| **Total** | **100** |

---

*CS 101 · Week 6 · Problem Set 6 · Due Friday 13 November 2026, 17:00 · © CSE Department*
