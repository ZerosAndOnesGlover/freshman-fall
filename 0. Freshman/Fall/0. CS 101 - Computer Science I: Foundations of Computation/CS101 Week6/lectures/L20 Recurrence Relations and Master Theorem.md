# CS 101 · Lecture 20 (Week 6, Lecture 2)
## Algorithm Analysis II: Recurrence Relations and the Master Theorem

*“Simplicity does not precede complexity, but follows it.”* — Alan Perlis, "Epigrams on Programming" (1982), #31

**Week 6 · Thursday**

**Date:** Thursday 5 November 2026 · 09:00–09:50 · Week 6

**Reading:** CLRS, Ch. 4 · CLRS, Ch. 16 *(details at the end of the lecture)*

**Coursework:** 📝 **PS 5** due Fri 6 Nov 17:00 · 📝 **PS 6** released Fri 6 Nov 10:00, due Fri 13 Nov 17:00 · 🔬 **Lab 6** Tue 10 Nov 15:00–16:50 · 📊 **Quiz 7** Wed 11 Nov 09:00–09:10

---

## 0. Why Recursive Algorithms Need Different Tools

Wednesday's rules (add for sequential, multiply for nested) work perfectly for iterative loops. But recursive algorithms don't have "loops" in the same sense — they have **self-referential calls**. To analyze them, we write a **recurrence relation**: an equation defining the algorithm's cost in terms of the cost of smaller instances of itself.

You've been *building intuition* for this since Week 4 (recursion trees). Today we make it a formal, repeatable method.

---

## 1. Writing a Recurrence Relation

A recurrence relation has two parts:
1. **Base case:** the cost for the smallest input (usually a constant)
2. **Recursive case:** the cost in terms of smaller sub-problems, plus the cost of combining them

```python
def factorial(n):
    if n == 0:            # base case: O(1)
        return 1
    return n * factorial(n - 1)   # recursive case: O(1) work + T(n-1)
```

**Recurrence:** `T(n) = T(n-1) + O(1)`, `T(0) = O(1)`.

```python
def merge_sort(lst):
    if len(lst) <= 1:      # base case: O(1)
        return lst[:]
    mid = len(lst) // 2
    left  = merge_sort(lst[:mid])     # T(n/2)
    right = merge_sort(lst[mid:])     # T(n/2)
    return merge(left, right)          # O(n) to merge
```

**Recurrence:** `T(n) = 2T(n/2) + O(n)`, `T(1) = O(1)`.

---

## 2. Three Methods for Solving Recurrences

### Method 1: Recursion Tree (from Week 4 — the intuitive method)

Draw the tree, compute work per level, sum across all levels. You've done this already for merge sort:

```
Level 0: 1 problem of size n           → work: cn
Level 1: 2 problems of size n/2        → work: c(n/2) × 2 = cn
Level 2: 4 problems of size n/4        → work: c(n/4) × 4 = cn
...
Level log₂n: n problems of size 1      → work: c(1) × n = cn

Total: cn × (log₂n + 1 levels) = O(n log n)
```

### Method 2: Substitution (guess and verify)

Guess a closed-form solution, then prove it by induction.

**Example:** solve `T(n) = T(n-1) + n`, `T(0) = 0`.

**Guess:** T(n) = n(n+1)/2 (based on expanding a few terms).

**Verify by induction:**
- Base case: T(0) = 0(1)/2 = 0 ✓
- Inductive step: assume T(n-1) = (n-1)n/2. Then:
  ```
  T(n) = T(n-1) + n = (n-1)n/2 + n = [(n-1)n + 2n]/2 = [n² - n + 2n]/2 = (n² + n)/2 = n(n+1)/2 ✓
  ```

So `T(n) = n(n+1)/2 = O(n²)`.

### Method 3: The Master Theorem (the fast formula)

For recurrences of the form:
```
T(n) = a·T(n/b) + f(n)
```
where `a ≥ 1`, `b > 1`, and `f(n)` is the cost of the "combine" step:

**Compare `f(n)` against `n^(log_b a)`:**

| Case | Condition | Result |
|------|-----------|--------|
| 1 | f(n) = O(n^(log_b a - ε)) for some ε > 0 | T(n) = Θ(n^(log_b a)) |
| 2 | f(n) = Θ(n^(log_b a)) | T(n) = Θ(n^(log_b a) · log n) |
| 3 | f(n) = Ω(n^(log_b a + ε)) for some ε > 0, and regularity condition | T(n) = Θ(f(n)) |

**In plain language:**
- **Case 1:** the recursive calls dominate the cost → complexity determined by the "leaves" of the recursion
- **Case 2:** the recursive calls and the combine step are balanced → extra log n factor
- **Case 3:** the combine step dominates → complexity determined by the top-level cost

### Applying the Master Theorem to Merge Sort

`T(n) = 2T(n/2) + O(n)` → a=2, b=2, f(n)=n

Compute `n^(log_b a) = n^(log₂2) = n^1 = n`.

Compare `f(n) = n` against `n^1 = n`: **they're equal** → Case 2.

**Result:** `T(n) = Θ(n^1 · log n) = Θ(n log n)`. ✓ Matches our recursion-tree derivation exactly.

### Applying the Master Theorem to Binary Search

`T(n) = T(n/2) + O(1)` → a=1, b=2, f(n)=1

Compute `n^(log_b a) = n^(log₂1) = n^0 = 1`.

Compare `f(n) = 1` against `n^0 = 1`: **equal** → Case 2.

**Result:** `T(n) = Θ(1 · log n) = Θ(log n)`. ✓

### Applying the Master Theorem to Naive Fibonacci (Beyond the Theorem's Scope)

`T(n) = T(n-1) + T(n-2) + O(1)` — this is **not** of the form `a·T(n/b) + f(n)` because the sub-problems are `n-1` and `n-2`, not `n/b`. The Master Theorem does not apply here — you must use the recursion-tree method (Week 4) or substitution instead, which gives `T(n) = O(2ⁿ)`.

**Important limitation:** the Master Theorem only applies to recurrences with the specific "divide into equal-sized b pieces" structure. Not every recurrence fits this template — know when to use recursion trees instead.

---

## 3. Common Recurrences and Their Solutions — Reference Table

| Recurrence | Solution | Example Algorithm |
|------------|----------|---------------------|
| T(n) = T(n-1) + O(1) | O(n) | Linear recursion (factorial, sum) |
| T(n) = T(n-1) + O(n) | O(n²) | Insertion into a growing structure |
| T(n) = T(n/2) + O(1) | O(log n) | Binary search |
| T(n) = 2T(n/2) + O(1) | O(n) | Simple binary tree traversal |
| T(n) = 2T(n/2) + O(n) | O(n log n) | Merge sort |
| T(n) = 2T(n/2) + O(n²) | O(n²) | Combine step dominates |
| T(n) = T(n-1) + T(n-2) + O(1) | O(2ⁿ) | Naive Fibonacci |
| T(n) = 2T(n-1) + O(1) | O(2ⁿ) | Tower of Hanoi |

---

## 4. Analyzing Real Recursive Functions Step by Step

### Example: Fast Power

```python
def fast_power(base, exp):
    if exp == 0:
        return 1
    if exp % 2 == 0:
        half = fast_power(base, exp // 2)  # T(n/2)
        return half * half                  # O(1)
    return base * fast_power(base, exp - 1)  # T(n-1), O(1)
```

**Recurrence (even case):** `T(n) = T(n/2) + O(1)` → by Master Theorem (a=1, b=2, f(n)=O(1)): Case 2, `T(n) = O(log n)`.

The odd case `T(n) = T(n-1) + O(1)` only happens at most once per "level" (since after subtracting 1 from an odd number, it becomes even), so it doesn't change the overall O(log n) complexity — it just adds a constant number of extra steps per halving.

### Example: The Recursive Power Set

```python
def power_set(lst):
    if not lst:
        return [[]]
    rest = power_set(lst[:-1])           # T(n-1)
    with_last = [s + [lst[-1]] for s in rest]   # O(2^(n-1)) — proportional to len(rest)
    return rest + with_last               # O(2^(n-1))
```

**Recurrence:** `T(n) = T(n-1) + O(2^(n-1))`

This doesn't fit the Master Theorem form either. Expand it:
```
T(n) = T(n-1) + 2^(n-1)
     = T(n-2) + 2^(n-2) + 2^(n-1)
     = ...
     = T(0) + 2^0 + 2^1 + ... + 2^(n-1)
     = O(1) + (2^n - 1)
     = O(2^n)
```

This matches intuition: a power set of n elements has 2ⁿ subsets, so any algorithm producing all of them must take at least O(2ⁿ) time.

---

## 5. Amortized Analysis — A Preview

Sometimes a single operation looks expensive, but averaged over a sequence of operations, the cost is much lower. This is **amortized analysis** — a technique you'll formalize fully in CS 102, but worth previewing now.

**Example: Python list `.append()`**

Python lists are implemented as dynamic arrays. When the underlying array is full, appending requires:
1. Allocating a new, larger array (typically ~1.125–2× the size)
2. Copying all existing elements to the new array
3. Adding the new element

A single "resize" append is O(n). But this only happens occasionally — most appends are O(1) (just adding to unused capacity).

**Amortized analysis:** across n append operations, the total cost of all the resizing is O(n) (each element is copied O(1) times on average across all resizes, due to the geometric growth factor). So **each append is O(1) amortized**, even though a specific append might occasionally cost O(n).

```python
import time

lst = []
resize_times = []

for i in range(100_000):
    t0 = time.perf_counter()
    lst.append(i)
    t1 = time.perf_counter()
    resize_times.append((t1 - t0) * 1_000_000)   # microseconds

# Most appends are extremely fast; occasional ones (resizes) are visibly slower.
# But the AVERAGE cost per append remains O(1).
print(f"Average time per append: {sum(resize_times)/len(resize_times):.4f} μs")
print(f"Max time (a resize event): {max(resize_times):.4f} μs")
```

This is why `list.append()` is described as **O(1) amortized** — not O(1) worst-case for every single call, but O(1) on average across any sequence of calls.

---

## 6. Common Errors in Recurrence-Based Analysis

**Error 1: Misidentifying the recurrence structure**
```python
def bad_analysis(n):
    if n <= 1: return 1
    return bad_analysis(n-1) + bad_analysis(n-1)   # NOT T(n/2) — it's T(n-1) twice!
```
Recurrence: `T(n) = 2T(n-1) + O(1)` → this is **O(2ⁿ)**, not O(n log n). Confusing "n-1, called twice" with "n/2, called twice" is one of the most common analysis mistakes.

**Error 2: Forgetting the cost of the "combine" step**
```python
def bad_merge_sort(lst):
    if len(lst) <= 1: return lst
    mid = len(lst)//2
    left, right = bad_merge_sort(lst[:mid]), bad_merge_sort(lst[mid:])
    return sorted(left + right)   # This "combine" step is O(n log n), not O(n)!
```
If you use `sorted()` to combine instead of a proper O(n) merge, the recurrence becomes `T(n) = 2T(n/2) + O(n log n)`, which solves (by Master Theorem Case 3) to `O(n log²n)` — worse than proper merge sort!

**Error 3: Applying the Master Theorem to non-conforming recurrences**
The Master Theorem requires the specific form `T(n) = aT(n/b) + f(n)`. Recurrences like `T(n) = T(n-1) + T(n-2) + O(1)` (Fibonacci) or `T(n) = T(n-1) + O(2ⁿ)` (power set) do not fit — use recursion trees or substitution instead.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Recurrence relation | Base case + recursive case, expressing algorithm cost self-referentially |
| Recursion tree method | Draw tree, sum work per level across all levels |
| Substitution method | Guess closed form, prove by induction |
| Master Theorem | Fast formula for T(n)=aT(n/b)+f(n); compare f(n) to n^(log_b a) |
| Master Theorem limitation | Only applies to the specific "divide into b equal pieces" form |
| Amortized analysis | Average cost per operation across a sequence, even if some are expensive |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Write and solve the recurrence for each, using the Master Theorem where it applies.

```python
# A: binary search
def a(xs, t, lo, hi): ...  # one recursive call on half
# B: merge sort
def b(xs): ...                # two recursive calls on half, O(n) merge
# C:
def c(n):
    if n <= 1: return 1
    return c(n-1) + c(n-1)
```

**2. (Explain.)** State all three cases of the Master Theorem for T(n) = aT(n/b) + f(n), and give a recurrence that falls into each. Then give one that the theorem cannot solve at all, and say why.

**3. (Build.)** Derive the amortised cost of `append` on a dynamic array that doubles when full. Show why the answer is O(1) even though individual appends can cost Θ(n).

**4. (Stretch.)** §6 lists common errors. Each analysis below is wrong. Find the error in each.

**(a)** "`for i in range(n): xs.insert(0, i)` is O(n), because it is a single loop."

**(b)** "Quicksort's recurrence is T(n) = 2T(n/2) + Θ(n), so it is Θ(n log n)."

**(c)** "`s = ""` then `for c in text: s += c` is O(n), since each `+=` is one operation."


### Answers

**1.** **A:** T(n) = T(n/2) + Θ(1). Master Theorem with a = 1, b = 2, f(n) = Θ(1) = Θ(n⁰). Since n^(log_b a) = n^(log₂ 1) = n⁰ = 1 and f(n) = Θ(1), we are in **case 2**: T(n) = Θ(n⁰ log n) = **Θ(log n)**.

**B:** T(n) = 2T(n/2) + Θ(n). Here a = 2, b = 2, so n^(log₂ 2) = n, and f(n) = Θ(n) matches. **Case 2** again: T(n) = **Θ(n log n)**.

**C:** T(n) = 2T(n−1) + Θ(1). The Master Theorem **does not apply** — it requires the subproblem size to be n/b, a constant *division*, and this subtracts. Unroll instead: T(n) = 2T(n−1) + 1 = 4T(n−2) + 3 = 8T(n−3) + 7 = … = 2ⁿT(0) + 2ⁿ − 1, giving **Θ(2ⁿ)**. Note `c(n)` just computes 2ⁿ, exponentially slowly.

The lesson from C is the one worth carrying: **check the form before reaching for the theorem.** Divide-and-conquer recurrences (n/b) take the Master Theorem; decrease-and-conquer recurrences (n−b) are solved by unrolling, and they are usually exponential when a ≥ 2.

**2.** Compare f(n) against the **critical exponent** n^(log_b a):

- **Case 1** — f(n) = O(n^(log_b a − ε)) for some ε > 0. The leaves dominate: **T(n) = Θ(n^(log_b a))**. *Example:* T(n) = 4T(n/2) + n. Critical exponent n² beats f(n) = n, so T(n) = Θ(n²).
- **Case 2** — f(n) = Θ(n^(log_b a)). Every level costs the same: **T(n) = Θ(n^(log_b a) log n)**. *Example:* T(n) = 2T(n/2) + n gives Θ(n log n) — merge sort.
- **Case 3** — f(n) = Ω(n^(log_b a + ε)) **and** the regularity condition af(n/b) ≤ cf(n) for some c < 1 holds. The root dominates: **T(n) = Θ(f(n))**. *Example:* T(n) = 2T(n/2) + n² gives Θ(n²).

**Unsolvable example:** T(n) = 2T(n/2) + n/log n. The critical exponent is n. Here f(n) = n/log n is smaller than n, but not *polynomially* smaller — the gap is a logarithmic factor, not n^ε for any ε > 0. So it falls into the **gap between cases 1 and 2** that the theorem does not cover. (The true answer, Θ(n log log n), needs the recursion-tree method or the Akra–Bazzi theorem.)

Case 3's regularity condition is the part most often skipped. It rules out pathological f that oscillate; for the polynomial-times-polylog functions you will meet in this course it always holds, but the theorem is stated with it for a reason.

**3.** Consider n appends into an array starting at capacity 1. A resize copies every existing element, so a resize at size k costs k. Resizes happen at sizes 1, 2, 4, 8, …, up to the largest power of 2 below n. Total copying cost is

1 + 2 + 4 + … + 2^⌊log₂ n⌋ < 2n

— a geometric series whose sum is less than **twice its largest term**. Adding the n unit-cost insertions gives total < 3n for n operations, so the **amortised cost per append is O(1)**.

The essential point is that expensive operations are **geometrically rare**. Doubling means resize k happens once every 2^k appends, so the cost of copying is spread over exactly enough cheap operations to pay for it.

This is why the growth factor must be **multiplicative**. Growing by a *fixed* amount c gives resizes at c, 2c, 3c, … with total copying c + 2c + 3c + … ≈ n²/(2c) — an **arithmetic** series, giving O(n) amortised per append and O(n²) overall. CPython actually grows by about 1/8 rather than doubling (you can observe the capacity jumps with `sys.getsizeof`), trading a slightly larger constant for less wasted memory; any factor > 1 preserves the O(1) amortised bound.

Note *amortised* is not *average*: it is a worst-case guarantee over any sequence of n operations, with no probability involved.

**4.** **(a)** The body is not O(1). `insert(0, x)` shifts every existing element right, costing Θ(current length). The total is 0 + 1 + 2 + … + (n−1) = **Θ(n²)**. The error is *assuming a loop body is constant time because it is one line* — always check the cost of the operations inside, especially list, string, and `in` operations.

**(b)** That recurrence describes the **best case**, where the pivot splits evenly. Quicksort does not guarantee an even split; the worst case is T(n) = T(n−1) + Θ(n) = **Θ(n²)**. The error is *stating a recurrence that assumes the favourable case and reporting its solution as the complexity*. Quicksort's Θ(n log n) is an **average-case** result and needs a probabilistic argument over pivot choices, not a single recurrence.

**(c)** Strings are **immutable**, so `s += c` builds an entirely new string and copies the old contents — Θ(len(s)) each time. The total is again **Θ(n²)**. Use `"".join(chars)`, which is Θ(n). (CPython has an optimisation that sometimes extends a string in place when the refcount is 1, which can make this look linear in a microbenchmark; it is an implementation detail that silently stops applying, so never rely on it.)

All three share one root cause: **an operation assumed to be O(1) that is not.** When analysing, the first question is always what the primitive operations actually cost.



---

## Reading

- **CLRS, Ch. 4** — Divide-and-Conquer (the Master Method, formally — 4.3–4.5)
- **CLRS, Ch. 16** — Amortized Analysis (optional, for the ambitious — aggregate method, accounting method)

---

*CS 101 · Week 6 · Lecture 20 (Thu) · © CSE Department*
