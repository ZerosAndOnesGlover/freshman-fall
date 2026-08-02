# CS 101 · Week 5 Reading Guide & Resources
## Searching and Sorting Algorithms

---

## Required Reading

### Guttag — Introduction to Computation and Programming Using Python

**Chapter 3.4 — Bisection Search**
Reread this now with a full week of recursion behind you. Notice how the bisection search for approximating a square root is structurally identical to binary search on a sorted array.

**Sorting chapter (Ch. 12 or equivalent in your edition)**
Read the sections on bubble sort, selection sort, insertion sort, and merge sort.

### Supplemental — CLRS (Introduction to Algorithms)

If you have access to CLRS (the reference text for this course):
- **Chapter 2** — Getting Started (insertion sort, formal loop invariant proof style — this is the gold standard for how to write invariant proofs)
- **Chapter 2.3** — Merge sort, with the recursion-tree method for solving recurrences

**What to focus on:** CLRS Chapter 2 demonstrates the exact style of correctness proof you should use in your own work — precise, using loop invariants, addressing initialization/maintenance/termination explicitly.

---

## Focused REPL / Experimentation Sessions

### Session A: Feeling the Difference Between O(n) and O(log n) (15 min)

```python
import time

def linear_search(lst, target):
    for i, v in enumerate(lst):
        if v == target:
            return i
    return -1

def binary_search(lst, target):
    lo, hi = 0, len(lst) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# Build a large sorted list and search for a worst-case target (not present):
n = 10_000_000
data = list(range(n))
target = -1   # guaranteed not found — worst case for both

t0 = time.perf_counter()
linear_search(data, target)
t1 = time.perf_counter()
print(f"Linear search on {n:,} elements: {(t1-t0)*1000:.2f} ms")

t0 = time.perf_counter()
binary_search(data, target)
t1 = time.perf_counter()
print(f"Binary search on {n:,} elements: {(t1-t0)*1000:.4f} ms")

# The ratio should be dramatic — often 10,000x or more.
```

### Session B: Watching Sort Algorithms Degrade (15 min)

```python
import time
import sys

def selection_sort(lst):
    lst = lst[:]
    n = len(lst)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if lst[j] < lst[min_idx]:
                min_idx = j
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
    return lst

def merge_sort(lst):
    if len(lst) <= 1:
        return lst[:]
    mid = len(lst) // 2
    left, right = merge_sort(lst[:mid]), merge_sort(lst[mid:])
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]

import random
for n in [500, 1000, 2000, 4000, 8000]:
    data = [random.randint(0, 100000) for _ in range(n)]

    t0 = time.perf_counter(); selection_sort(data); t1 = time.perf_counter()
    sel_time = (t1 - t0) * 1000

    t0 = time.perf_counter(); merge_sort(data); t1 = time.perf_counter()
    merge_time = (t1 - t0) * 1000

    print(f"n={n:5}: selection={sel_time:8.2f}ms  merge={merge_time:6.2f}ms  ratio={sel_time/merge_time:6.1f}x")

# Notice: as n doubles, selection sort's time roughly QUADRUPLES.
# Merge sort's time roughly DOUBLES (times a small log factor).
```

### Session C: Building Intuition for the Decision Tree Lower Bound (10 min)

```python
import math

# For n elements, there are n! possible orderings.
# A comparison sort's decision tree needs at least n! leaves.
# A binary tree with L leaves has depth >= log2(L).
# So worst-case comparisons >= log2(n!).

def stirling_estimate(n):
    """Estimate log2(n!) using Stirling's approximation."""
    if n <= 1:
        return 0
    return n * math.log2(n) - n * math.log2(math.e)

for n in [10, 100, 1000, 10000]:
    exact_log_factorial = math.log2(math.factorial(n)) if n <= 1000 else None
    estimate = stirling_estimate(n)
    n_log_n = n * math.log2(n)
    print(f"n={n:6}: log2(n!) ≈ {estimate:12.1f}   n*log2(n) = {n_log_n:12.1f}   ratio = {estimate/n_log_n:.3f}")

# Notice: log2(n!) is very close to n*log2(n) for large n.
# This confirms: the information-theoretic lower bound IS Theta(n log n).
```

---

## Conceptual Exercises (Paper and Pencil)

**Exercise 1:** Trace insertion sort on `[4, 2, 7, 1, 9, 3]`. Show the array state after each outer loop iteration (i = 1, 2, 3, 4, 5).

**Exercise 2:** For selection sort on an array of n elements, prove that the number of swaps is always exactly n-1 in the worst case, and could be as low as 0 (if already sorted, though comparisons are still O(n²)). Is this consistent with what you know about the algorithm?

**Exercise 3:** A classmate says "quicksort is always O(n log n) because that's its average case, and average case is what matters in practice." Write a two-sentence rebuttal explaining when the worst case actually occurs and why mitigation strategies (randomization) matter.

**Exercise 4:** Given the recurrence for quicksort's worst case, T(n) = T(n-1) + O(n), solve it by expansion (write out T(n) = T(n-1) + cn = T(n-2) + c(n-1) + cn = ... and sum the series).

---

## Algorithms Summary Table

| Algorithm | Time (Best/Avg/Worst) | Space | Stable | Key Idea |
|-----------|------------------------|-------|--------|----------|
| Linear search | O(1)/O(n)/O(n) | O(1) | N/A | Check every element in order |
| Binary search | O(1)/O(log n)/O(log n) | O(1) | N/A | Halve the search space (sorted data only) |
| Selection sort | O(n²)/O(n²)/O(n²) | O(1) | No | Find min, place at front, repeat |
| Insertion sort | O(n)/O(n²)/O(n²) | O(1) | Yes | Insert into sorted prefix |
| Bubble sort | O(n)/O(n²)/O(n²) | O(1) | Yes | Swap adjacent out-of-order pairs |
| Merge sort | O(n log n) all cases | O(n) | Yes | Divide, recursively sort, merge |
| Quicksort | O(n log n)/O(n log n)/O(n²) | O(log n) | No | Partition around pivot, recurse |
| Timsort (Python) | O(n)/O(n log n)/O(n log n) | O(n) | Yes | Hybrid: insertion sort + merge sort |

---

## Common Mistakes This Week

**Mistake 1: Off-by-one in binary search bounds**
```python
while lo < hi:    # WRONG if you need lo == hi to be checked
while lo <= hi:   # Usually correct — verify against your invariant
```

**Mistake 2: Forgetting binary search requires sorted data**
```python
binary_search([5, 2, 8, 1, 9], 8)   # UNDEFINED BEHAVIOR — data isn't sorted!
```
Always verify (or guarantee via precondition) that the input is sorted.

**Mistake 3: Comparing algorithms only by "Big-O" without considering constants**
For small n (say, n < 20), insertion sort often beats merge sort in practice due to lower constant overhead, despite the "worse" asymptotic complexity. This is why Timsort uses insertion sort for small sub-arrays.

**Mistake 4: Assuming quicksort is always O(n log n)**
```python
quicksort(sorted(range(10000)))  # Worst case with naive first-element pivot!
```
Use random or median-of-three pivot selection to avoid this.

**Mistake 5: Forgetting stability matters for multi-key sorts**
If you need to sort by (grade, then name for ties), sort by name first, then by grade — relying on a stable sort to preserve the name-order within grade groups.

---

## Week 5 Self-Test

1. What precondition does binary search require that linear search does not?
2. State the loop invariant for binary search.
3. Why is selection sort's comparison count always exactly n(n-1)/2, regardless of input order?
4. Why does insertion sort achieve O(n) on already-sorted data?
5. What is bubble sort's "early exit" optimization, and why does it matter?
6. Write the recurrence for merge sort's time complexity, and state its solution.
7. Why is quicksort's worst case O(n²), and what mitigates it in practice?
8. What is a stable sort? Give an example situation where stability matters.
9. What does Timsort do differently from pure merge sort?
10. State the theoretical lower bound for comparison-based sorting, and briefly explain the decision-tree argument that proves it.

*(Answers: 1. data must be sorted. 2. if target is in lst, it is in lst[lo..hi]. 3. the inner loop always runs a fixed number of times regardless of values. 4. no shifting needed since each new element is already in place. 5. skip remaining passes if no swaps occurred in the last pass — turns best case into O(n). 6. T(n)=2T(n/2)+O(n) → O(n log n). 7. degenerate pivot choice (e.g. always smallest/largest); randomized or median-of-three pivot mitigates. 8. equal elements retain relative order; matters for multi-key sorts. 9. exploits natural runs, uses insertion sort for small/already-ordered subsequences. 10. Ω(n log n); a decision tree with n! leaves needs depth ≥ log2(n!) ≈ n log n.)*

---

## Preview: Week 6

Week 6 covers **Algorithm Analysis: Big-O Notation** formally — the mathematical machinery behind everything you've been doing empirically this week (measuring runtimes, drawing recursion trees, counting operations).

**Also: Midterm 1 is this week**, covering Weeks 0–5 (everything up through today). Review:
- Types, expressions, operators (Week 1)
- Conditionals and loops (Week 2)
- Functions, scope, the call stack (Week 3)
- Recursion — the three laws, induction, recursion trees (Week 4)
- Searching and sorting (Week 5)

Start reviewing early. The midterm rewards deep understanding, not memorization — the same skills you've practiced in every lab and problem set so far.

---

*CS 101 · Week 5 · Reading Guide · © CSE Department*
