# CS 101 · Problem Set 6
## Algorithm Analysis: Classifying and Proving Big-O Bounds

**Released:** Friday 6 November 2026, 10:00 (after L21) · Week 6
**Due:** Friday 13 November 2026, 17:00 · Week 7 — late penalty from 17:01
**Submission:** `ps6.py` (Part B) and your answer sheet (Part A) in `"$CS101/week6"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 4 hours

---

## What this problem set uses

Weeks 0–6, above all this week's: the formal definitions of O, Ω and Θ and loop analysis (L19),
writing recurrences and solving them by recursion tree, substitution and the Master Theorem, and the
amortized preview (L20), and connecting counts to growth (L21).

**Not needed and not expected:** timing code or fitting curves (you count operations exactly instead),
classes (Week 7), dictionaries or memoization (Week 8).

---

## Part A: Formal Analysis (50 points)

### A1: Big-O Proofs (12 points)

State the constants `c` and `n₀` and verify the inequality.

**(a)** `4n³ + 2n² + 100 = O(n³)`.
**(b)** `2n + 5 = O(n²)` — a loose bound is still a valid one.
**(c)** Disprove `n² = O(n)`: suppose `c` and `n₀` exist and derive a contradiction.

### A2: Big-Ω and Big-Θ (10 points)

**(a)** Prove `n² − 10n = Ω(n²)` (find `c` and `n₀`).
**(b)** Prove `4n³ + 2n² + 100 = Θ(n³)`, using A1(a) for the upper bound.
**(c)** True or false, with justification: "If `f(n) = O(g(n))` then `g(n) = Ω(f(n))`."

### A3: Recurrences (16 points)

**(a)** `T(n) = T(n−1) + n`, `T(0) = 0` — by **substitution**: expand, spot the pattern, prove it by induction.
**(b)** `T(n) = 3T(n/2) + n` — by the **Master Theorem**: compute `n^(log_b a)` and name the case.
**(c)** `T(n) = 4T(n/2) + n²` — Master Theorem.
**(d)** `T(n) = 2T(n/2) + n²` — Master Theorem. Compare with (c): same combine cost, different `a`. Why do they land in different cases?

### A4: Code Analysis (12 points)

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

## Part B: Python (`ps6.py`) (50 points)

Each function needs a docstring whose first line states its Θ-bound, and at least two `assert` tests.

### B1: Classifying Real Code (18 points)

**(a)** `has_zero_triple(lst)` — `True` if three elements at distinct positions sum to 0, using three
nested loops over `i < j < k`. `[-1, 0, 1]` → `True`; `[1, 2, 3]` → `False`; `[0, 0]` → `False`.
**(b)** `matrix_multiply(A, B)` — the product of two `n × n` matrices stored as lists of rows.
`[[1, 2], [3, 4]] × [[5, 6], [7, 8]]` → `[[19, 22], [43, 50]]`.
**(c)** `count_inversions(lst)` — pairs `i < j` with `lst[i] > lst[j]`. `[3, 1, 2]` → `2`; `[4, 3, 2, 1]` → `6`.

For each, state the bound and justify it by counting how many times the innermost statement runs.

### B2: A Recurrence in Code (14 points)

**(a)** `tribonacci(n)`: `T(0) = T(1) = 0`, `T(2) = 1`, `T(n) = T(n−1) + T(n−2) + T(n−3)`, naive,
counting its calls in a global `calls` (as in Lab 4). First ten values: `0 0 1 1 2 4 7 13 24 44`.
**(b)** Write the recurrence `C(n)` for the **number of calls**, and `predicted_calls(n)` that computes it
with a loop. Assert that it matches the measured count for `n` = 10, 12, …, 20, and print a table with the
ratio between successive rows.
**(c)** In a comment: the ratio settles near 3.38 per two steps. What growth per step does that imply,
and why can't the Master Theorem solve this recurrence?

### B3: Amortized Cost of Appends (18 points)

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
| A1 Big-O proofs | 12 |
| A2 Big-Ω and Big-Θ | 10 |
| A3 Recurrences | 16 |
| A4 Code analysis | 12 |
| B1 Classifying code | 18 |
| B2 A recurrence in code | 14 |
| B3 Amortized appends | 18 |
| **Total** | **100** |

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** The reference `ps6.py` below was run; every assert passes and the
> tables are its real output. Watch the **A4(c) trap**.

### Part A — Formal Analysis (50 points)

**A1 Big-O Proofs (12 pts).**

**(a)** `4n³ + 2n² + 100 = O(n³)`. Take **c = 106, n₀ = 1**. For n ≥ 1: `n² ≤ n³` and `100 ≤ 100n³`, so `4n³ + 2n² + 100 ≤ 4n³ + 2n³ + 100n³ = 106n³`. ✓
*(Any valid pair is acceptable — e.g. c = 5, n₀ = 6 also works. Grade the verification, not the specific constants.)*

**(b)** `2n + 5 = O(n²)`. Take **c = 7, n₀ = 1**. For n ≥ 1: `2n ≤ 2n²` and `5 ≤ 5n²`, so `2n + 5 ≤ 7n²`. ✓ Big-O is an **upper** bound, not a tight one — a loose bound is still formally correct.

**(c)** Disprove `n² = O(n)`. Suppose constants `c > 0, n₀` exist with `n² ≤ cn` for all `n ≥ n₀`. Dividing by `n > 0` gives `n ≤ c` for all `n ≥ n₀`. But choosing `n = max(n₀, ⌊c⌋ + 1)` yields `n > c`, contradicting the inequality. No such constants exist. ∎

*Grading: 4 pts each — constants stated and the inequality verified; (c) must be a proof by contradiction ("n² grows faster, obviously" earns 1).*

**A2 Big-Ω / Big-Θ (10 pts).** (a) 4, (b) 3, (c) 3.

**(a)** `n² − 10n = Ω(n²)`. Take **c = ½, n₀ = 20**. For n ≥ 20: `10n ≤ ½n²` (since `n ≥ 20` ⟹ `20n ≤ n²`), so `n² − 10n ≥ n² − ½n² = ½n²`. ✓

**(b)** `4n³ + 2n² + 100 = Θ(n³)`. Upper bound from A1(a) (c = 106). Lower bound: for n ≥ 1, `4n³ + 2n² + 100 ≥ 4n³`, so c = 4 works. Since it is both `O(n³)` and `Ω(n³)`, it is `Θ(n³)`. ∎

**(c)** **True.** `f = O(g)` means `∃ c, n₀ : f(n) ≤ c·g(n)` for `n ≥ n₀`. Rearranging, `g(n) ≥ (1/c)·f(n)`, which is exactly the definition of `g = Ω(f)` with constant `1/c` (valid since `c > 0`). The relationship is genuinely symmetric — O and Ω are transposes of one another.

**A3 Recurrences (16 pts).** 4 pts each.

**(a)** `T(n) = T(n−1) + n, T(0) = 0`. Expanding: `T(n) = n + (n−1) + … + 1 = n(n+1)/2`. Induction: base `T(0)=0=0·1/2` ✓; step `T(k+1) = (k+1) + k(k+1)/2 = (k+1)(k+2)/2` ✓. → **Θ(n²)**.

**(b)** `T(n) = 3T(n/2) + n`. `a=3, b=2`, `n^(log₂3) = n^1.585`. Since `f(n) = n = O(n^(1.585−ε))`, this is **Case 1** → **Θ(n^log₂3) ≈ Θ(n^1.585)**.

**(c)** `T(n) = 4T(n/2) + n²`. `a=4, b=2`, `n^(log₂4) = n²`. `f(n) = n² = Θ(n²)` — they match → **Case 2** → **Θ(n² log n)**.

**(d)** `T(n) = 2T(n/2) + n²`. `a=2, b=2`, `n^(log₂2) = n`. `f(n) = n²` grows polynomially faster, and the regularity condition holds (`2(n/2)² = n²/2 ≤ ¾n²`) → **Case 3** → **Θ(n²)**.
*Comparison asked for in the prompt: (c) and (d) share the same combine cost `n²` but differ in `a`. In (c) the recursion exactly balances the combine work, so every level costs the same and a `log n` factor appears. In (d) the root dominates — the work shrinks geometrically down the tree, so the top level alone determines the answer. **The branching factor decides which term wins.***

**A4 Code Analysis (12 pts).** 3 pts each.

- **(a) `f(n)` — Θ(log n).** `i` is divided by 3 each pass, so the loop runs `log₃ n` times. Base of the log is a constant factor, hence `O(log n)`.
- **(b) `g(n)` — Θ(n³).** Three independent nested loops each running exactly n times.
- **(c) `h(lst)` — Θ(n log n). ⚠️ This is a trap.** The tempting answer is O(n²) from the `left × right` double loop. But trace it: the base case returns a list of length 1, so `len(left) = len(right) = 1` at *every* level, meaning the double loop always runs exactly **once**. (In fact `h` computes the sum of the list — `h([1..16])` returns `[136]`.) The real cost is the **slicing**: `lst[:mid]` and `lst[mid:]` copy O(n) per call, giving `T(n) = 2T(n/2) + O(n)` → **Θ(n log n)**.
- **(d) `k(n)` — Θ(n²).** The loop is O(n) and it recurses on `n−1`: `T(n) = T(n−1) + n` → `n(n+1)/2`.

*Grading note for (c): accept **Θ(n log n)** for full marks. Award 1 of 3 for a well-argued O(n²) that explicitly reasons about `len(left) × len(right)` but fails to notice the lists are singletons — the reasoning is sound, the premise isn't. Award 0 for an unjustified "O(n²), three loops". This item is worth flagging in the post-mortem: it rewards actually tracing the code over pattern-matching on loop nesting.*

---

### Part B — reference `ps6.py` (50 points)

```python
# --- B1: Classifying real code ---
def has_zero_triple(lst):
    """True if three elements at distinct positions sum to 0.  O(n^3): three nested loops over i < j < k."""
    n = len(lst)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if lst[i] + lst[j] + lst[k] == 0:
                    return True
    return False

def matrix_multiply(A, B):
    """Product of two n x n matrices (lists of lists).  O(n^3): n^2 entries, each a sum of n products."""
    n = len(A)
    C = []
    for i in range(n):
        row = []
        for j in range(n):
            total = 0
            for k in range(n):
                total += A[i][k] * B[k][j]
            row.append(total)
        C.append(row)
    return C

def count_inversions(lst):
    """Number of pairs i < j with lst[i] > lst[j].  O(n^2): n(n-1)/2 pairs checked."""
    count = 0
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] > lst[j]:
                count += 1
    return count

assert has_zero_triple([-1, 0, 1]) and has_zero_triple([3, -7, 4, 10]) and not has_zero_triple([1, 2, 3]) and not has_zero_triple([0, 0])
assert matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]
assert matrix_multiply([[2]], [[3]]) == [[6]]
assert count_inversions([3, 1, 2]) == 2 and count_inversions([1, 2, 3]) == 0 and count_inversions([4, 3, 2, 1]) == 6

# --- B2: A recurrence in code ---
calls = 0

def tribonacci(n):
    """T(0)=0, T(1)=0, T(2)=1, T(n)=T(n-1)+T(n-2)+T(n-3). Naive; counts its calls in the global `calls`."""
    global calls
    calls += 1
    if n < 2:
        return 0
    if n == 2:
        return 1
    return tribonacci(n - 1) + tribonacci(n - 2) + tribonacci(n - 3)

def predicted_calls(n):
    """C(n) = 1 for n <= 2, else 1 + C(n-1) + C(n-2) + C(n-3) — computed with a loop."""
    c = [1, 1, 1]
    for k in range(3, n + 1):
        c.append(1 + c[k - 1] + c[k - 2] + c[k - 3])
    return c[n]

assert [tribonacci(k) for k in range(10)] == [0, 0, 1, 1, 2, 4, 7, 13, 24, 44]
print(f"{'n':>3} {'T(n)':>7} {'calls':>8} {'predicted':>10} {'ratio':>6}")
previous = None
for n in [10, 12, 14, 16, 18, 20]:
    calls = 0
    value = tribonacci(n)
    assert calls == predicted_calls(n)
    ratio = "" if previous is None else f"{calls / previous:.2f}"
    print(f"{n:>3} {value:>7} {calls:>8} {predicted_calls(n):>10} {ratio:>6}")
    previous = calls

# --- B3: Amortized cost of appends ---
def simulate_appends(n, grow):
    """Append n items to an array that starts with capacity 1. When full, the capacity becomes grow(capacity)
    and every stored item is copied. Returns the total number of copies."""
    capacity = 1
    size = 0
    copies = 0
    for _ in range(n):
        if size == capacity:
            copies += size
            capacity = grow(capacity)
        size += 1
    return copies

double = lambda c: 2 * c
plus_one = lambda c: c + 1
for n in [1000, 10000, 100000, 1000000]:
    c = simulate_appends(n, double)
    print(f"doubling n={n:>8}: copies={c:>8}  copies/n={c / n:.3f}")
for n in [1000, 2000, 4000, 8000]:
    c = simulate_appends(n, plus_one)
    print(f"plus one n={n:>8}: copies={c:>8}  copies/n={c / n:.1f}")
assert simulate_appends(1, double) == 0 and simulate_appends(5, double) == 1 + 2 + 4
assert simulate_appends(5, plus_one) == 1 + 2 + 3 + 4
print("all asserts passed")
```

Output:

```
  n    T(n)    calls  predicted  ratio
 10      81      289        289
 12     274      979        979   3.39
 14     927     3313       3313   3.38
 16    3136    11209      11209   3.38
 18   10609    37921      37921   3.38
 20   35890   128287     128287   3.38
doubling n=    1000: copies=    1023  copies/n=1.023
doubling n=   10000: copies=   16383  copies/n=1.638
doubling n=  100000: copies=  131071  copies/n=1.311
doubling n= 1000000: copies= 1048575  copies/n=1.049
plus one n=    1000: copies=  499500  copies/n=499.5
plus one n=    2000: copies= 1999000  copies/n=999.5
plus one n=    4000: copies= 7998000  copies/n=1999.5
plus one n=    8000: copies=31996000  copies/n=3999.5
```

**B1 (18, 6 each).** Θ(n³): the innermost test runs C(n, 3) ≈ n³/6 times in the worst case (no triple).
Θ(n³): n² entries × n products. Θ(n²): n(n−1)/2 pairs. *3 pts code (asserts pass), 3 pts bound + count.*

**B2 (14).** `C(n) = 1 + C(n−1) + C(n−2) + C(n−3)`, `C(0) = C(1) = C(2) = 1`. (c) 3.38 per two steps is
≈ 1.839 per step (√3.38): the calls grow like 1.839ⁿ — exponential. The Master Theorem needs sub-problems
of size `n/b`; these are `n − 1`, `n − 2`, `n − 3`, which shrink by subtraction, not division.
*(a) 4, (b) 6, (c) 4.*

**B3 (18).** Doubling: copies = 1 + 2 + 4 + … < 2n, so under 2 per append for every `n` (the ratio wobbles
between 1 and 2 with how close `n` is to a power of two). Plus one: copies = 0 + 1 + … + (n−1) = n(n−1)/2,
so copies-per-append is (n−1)/2 — Θ(n) each. *(a) 8 — the asserts `simulate_appends(5, double) == 7` and
`simulate_appends(5, plus_one) == 10` must pass; (b) 5; (c) 5.*

---

*CS 101 · Week 6 · Problem Set 6 · Due Friday 13 November 2026, 17:00 · © CSE Department*
