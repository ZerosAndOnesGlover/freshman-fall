# CS 101 · Problem Set 6 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** The reference `ps6.py` below was run; every assert passes and the
> tables are its real output. Watch the **A4(c) trap**.

*(Revised 2026-09-26: old A2 and B2 were removed from the set. Old A3, A4 and B3 are now A2, A3 and B2.)*

### Part A — Formal Analysis (48 points)

**A1 Big-O Proofs (14 pts).**

**(a)** `4n³ + 2n² + 100 = O(n³)`. Take **c = 106, n₀ = 1**. For n ≥ 1: `n² ≤ n³` and `100 ≤ 100n³`, so `4n³ + 2n² + 100 ≤ 4n³ + 2n³ + 100n³ = 106n³`. ✓
*(Any valid pair is acceptable — e.g. c = 5, n₀ = 6 also works. Grade the verification, not the specific constants.)*

**(b)** `2n + 5 = O(n²)`. Take **c = 7, n₀ = 1**. For n ≥ 1: `2n ≤ 2n²` and `5 ≤ 5n²`, so `2n + 5 ≤ 7n²`. ✓ Big-O is an **upper** bound, not a tight one — a loose bound is still formally correct.

**(c)** Disprove `n² = O(n)`. Suppose constants `c > 0, n₀` exist with `n² ≤ cn` for all `n ≥ n₀`. Dividing by `n > 0` gives `n ≤ c` for all `n ≥ n₀`. But choosing `n = max(n₀, ⌊c⌋ + 1)` yields `n > c`, contradicting the inequality. No such constants exist. ∎

*Grading: 5 / 5 / 4 — constants stated and the inequality verified; (c) must be a proof by contradiction ("n² grows faster, obviously" earns 1).*

**A2 Recurrences (18 pts).** 5 / 5 / 4 / 4.

**(a)** `T(n) = T(n−1) + n, T(0) = 0`. Expanding: `T(n) = n + (n−1) + … + 1 = n(n+1)/2`. Induction: base `T(0)=0=0·1/2` ✓; step `T(k+1) = (k+1) + k(k+1)/2 = (k+1)(k+2)/2` ✓. → **Θ(n²)**.

**(b)** `T(n) = 3T(n/2) + n`. `a=3, b=2`, `n^(log₂3) = n^1.585`. Since `f(n) = n = O(n^(1.585−ε))`, this is **Case 1** → **Θ(n^log₂3) ≈ Θ(n^1.585)**.

**(c)** `T(n) = 4T(n/2) + n²`. `a=4, b=2`, `n^(log₂4) = n²`. `f(n) = n² = Θ(n²)` — they match → **Case 2** → **Θ(n² log n)**.

**(d)** `T(n) = 2T(n/2) + n²`. `a=2, b=2`, `n^(log₂2) = n`. `f(n) = n²` grows polynomially faster, and the regularity condition holds (`2(n/2)² = n²/2 ≤ ¾n²`) → **Case 3** → **Θ(n²)**.
*Comparison asked for in the prompt: (c) and (d) share the same combine cost `n²` but differ in `a`. In (c) the recursion exactly balances the combine work, so every level costs the same and a `log n` factor appears. In (d) the root dominates — the work shrinks geometrically down the tree, so the top level alone determines the answer. **The branching factor decides which term wins.***

**A3 Code Analysis (16 pts).** 4 pts each.

- **(a) `f(n)` — Θ(log n).** `i` is divided by 3 each pass, so the loop runs `log₃ n` times. Base of the log is a constant factor, hence `O(log n)`.
- **(b) `g(n)` — Θ(n³).** Three independent nested loops each running exactly n times.
- **(c) `h(lst)` — Θ(n log n). ⚠️ This is a trap.** The tempting answer is O(n²) from the `left × right` double loop. But trace it: the base case returns a list of length 1, so `len(left) = len(right) = 1` at *every* level, meaning the double loop always runs exactly **once**. (In fact `h` computes the sum of the list — `h([1..16])` returns `[136]`.) The real cost is the **slicing**: `lst[:mid]` and `lst[mid:]` copy O(n) per call, giving `T(n) = 2T(n/2) + O(n)` → **Θ(n log n)**.
- **(d) `k(n)` — Θ(n²).** The loop is O(n) and it recurses on `n−1`: `T(n) = T(n−1) + n` → `n(n+1)/2`.

*Grading note for (c): accept **Θ(n log n)** for full marks. Award 1 of 4 for a well-argued O(n²) that explicitly reasons about `len(left) × len(right)` but fails to notice the lists are singletons — the reasoning is sound, the premise isn't. Award 0 for an unjustified "O(n²), three loops". This item is worth flagging in the post-mortem: it rewards actually tracing the code over pattern-matching on loop nesting.*

---

### Part B — reference `ps6.py` (52 points)

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

# --- B2: Amortized cost of appends ---
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
doubling n=    1000: copies=    1023  copies/n=1.023
doubling n=   10000: copies=   16383  copies/n=1.638
doubling n=  100000: copies=  131071  copies/n=1.311
doubling n= 1000000: copies= 1048575  copies/n=1.049
plus one n=    1000: copies=  499500  copies/n=499.5
plus one n=    2000: copies= 1999000  copies/n=999.5
plus one n=    4000: copies= 7998000  copies/n=1999.5
plus one n=    8000: copies=31996000  copies/n=3999.5
```

**B1 (24, 8 each).** Θ(n³): the innermost test runs C(n, 3) ≈ n³/6 times in the worst case (no triple).
Θ(n³): n² entries × n products. Θ(n²): n(n−1)/2 pairs. *4 pts code (asserts pass), 4 pts bound + count.*

**B2 (28).** Doubling: copies = 1 + 2 + 4 + … < 2n, so under 2 per append for every `n` (the ratio wobbles
between 1 and 2 with how close `n` is to a power of two). Plus one: copies = 0 + 1 + … + (n−1) = n(n−1)/2,
so copies-per-append is (n−1)/2 — Θ(n) each. *(a) 12 — the asserts `simulate_appends(5, double) == 7` and
`simulate_appends(5, plus_one) == 10` must pass; (b) 8; (c) 8.*

---

*CS 101 · Week 6 · Problem Set 6 · Due Friday 13 November 2026, 17:00 · © CSE Department*
