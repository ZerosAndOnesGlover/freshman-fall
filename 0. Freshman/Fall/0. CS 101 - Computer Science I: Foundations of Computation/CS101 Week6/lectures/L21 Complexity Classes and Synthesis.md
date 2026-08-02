# CS 101 — Lecture 21 (Week 6, Lecture 3)
## Algorithm Analysis III: Complexity Classes in Depth, and Theory Meets Practice

**Week 6 · Friday**
*"An O(n²) algorithm on n = 1,000,000 inputs would require 10¹² operations — roughly 11 days at 10⁹ operations/second. An O(n log n) algorithm needs only 20,000,000 operations — under a second." — CS 101*

---

## 0. Synthesizing Weeks 0–6

Today closes the first half of the course. We connect algorithm analysis (Big-O, this week) back to everything you've built: recursion (Week 4), searching and sorting (Week 5), and the fundamental question that started the course (Week 0): what does it mean to compute something *efficiently*?

---

## 1. The Complexity Classes, One at a Time

### O(1) — Constant Time

Cost does not depend on input size at all.

```python
def get_first(lst):
    return lst[0]     # always exactly one operation, regardless of len(lst)

def is_even(n):
    return n % 2 == 0  # one modulo operation, regardless of n's magnitude*
```

*Technically, arithmetic on arbitrary-precision integers in Python is not truly O(1) for astronomically large numbers, but for all practical purposes and for this course, we treat basic arithmetic as O(1).

### O(log n) — Logarithmic Time

Cost grows very slowly — each "step" eliminates a constant fraction of the remaining problem.

```python
def binary_search(lst, target):
    lo, hi = 0, len(lst) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if lst[mid] == target: return mid
        elif lst[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1
```

**Intuition:** log₂(1,000,000) ≈ 20. Doubling the input size only adds **one more step**. This is why binary search on a billion-element array still takes only ~30 comparisons.

### O(n) — Linear Time

Cost grows directly proportional to input size — you must "touch" every element at least once.

```python
def find_max(lst):
    m = lst[0]
    for x in lst:
        if x > m: m = x
    return m
```

**Intuition:** this is the minimum possible complexity for any algorithm that must examine every element of its input (a lower bound, by an easy argument: if you don't look at some element, you can't know its value, so you can't guarantee correctness on all inputs).

### O(n log n) — Linearithmic Time

The complexity of "efficient" sorting and many divide-and-conquer algorithms.

```python
def merge_sort(lst):
    if len(lst) <= 1: return lst
    mid = len(lst) // 2
    return merge(merge_sort(lst[:mid]), merge_sort(lst[mid:]))
```

**Intuition:** you do O(log n) "rounds," each touching all n elements once. This is provably optimal for comparison-based sorting (Week 5's decision-tree lower bound).

### O(n²) — Quadratic Time

Typically arises from comparing every pair of elements, or nested loops over the same data.

```python
def has_duplicate(lst):
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] == lst[j]: return True
    return False
```

**Intuition:** C(n,2) = n(n-1)/2 pairs — quadratic. This is the complexity class where naive algorithms often start, and where careful algorithm design (hashing, sorting first) frequently finds an improvement.

### O(2ⁿ) — Exponential Time

Arises from trying all subsets, or naive recursive branching without memoization.

```python
def subsets(lst):
    if not lst: return [[]]
    rest = subsets(lst[1:])
    return rest + [[lst[0]] + s for s in rest]
```

**Intuition:** for n=30, 2³⁰ ≈ 1 billion — borderline feasible. For n=50, 2⁵⁰ ≈ 1 quadrillion — infeasible. Exponential algorithms only work for small n.

### O(n!) — Factorial Time

Arises from trying all permutations or orderings.

```python
def all_orderings(lst):
    if len(lst) <= 1: return [lst]
    result = []
    for i in range(len(lst)):
        rest = lst[:i] + lst[i+1:]
        for perm in all_orderings(rest):
            result.append([lst[i]] + perm)
    return result
```

**Intuition:** 10! ≈ 3.6 million (feasible). 15! ≈ 1.3 trillion (borderline). 20! ≈ 2.4 × 10¹⁸ (utterly infeasible). This is the complexity of brute-force solutions to problems like the Traveling Salesman Problem.

---

## 2. Visualizing Growth Rates — The Full Picture

```
Operations needed for n = 20:

O(1)        : 1
O(log n)    : 4       (log2(20) ≈ 4.3)
O(n)        : 20
O(n log n)  : 86
O(n²)       : 400
O(2ⁿ)       : 1,048,576
O(n!)       : 2,432,902,008,176,640,000
```

For n=20, a factorial algorithm already requires more operations than there are grains of sand on Earth's beaches (estimated at ~7.5 × 10¹⁸). This visceral comparison is why complexity class matters more than almost any other engineering decision.

---

## 3. Connecting Theory to Empirical Measurement

Recall Week 5's lab, where you benchmarked sorting algorithms and plotted runtime vs. input size on a log-log scale. Here is why that technique works, formally:

If `T(n) = c·n^k` for some constants c and k, then:
```
log(T(n)) = log(c) + k·log(n)
```

This is a **linear equation** in `log(T(n))` vs. `log(n)`, with **slope k**. On a log-log plot:
- O(n) algorithms produce a line with slope ≈ 1
- O(n²) algorithms produce a line with slope ≈ 2
- O(n log n) algorithms produce a line that is *almost* straight with slope ≈ 1, but curves very slightly upward due to the log n factor

**This is the mathematical justification for why log-log plots reveal complexity class** — the slope of the line directly estimates the exponent k in `n^k`.

```python
import numpy as np

# Given measurements (n, time) pairs:
ns    = [1000, 2000, 4000, 8000]
times = [0.05, 0.20, 0.81, 3.24]   # example: looks like O(n²) — quadruples each doubling

log_ns    = np.log(ns)
log_times = np.log(times)

# Linear regression slope ≈ the complexity exponent k
slope = np.polyfit(log_ns, log_times, 1)[0]
print(f"Estimated exponent: {slope:.2f}")   # Should print ≈ 2.0 for O(n²) data
```

This technique — fitting a line to log-log data to estimate the complexity exponent — is exactly what you did empirically in Lab 5, now grounded in the mathematics of Big-O.

---

## 4. Worst Case, Average Case, and Best Case — Formal Distinctions

Every algorithm can be analyzed under three different assumptions about the input:

**Worst case:** the input that makes the algorithm perform as badly as possible.
```python
# Quicksort worst case: already-sorted input with naive pivot choice → O(n²)
```

**Best case:** the input that makes the algorithm perform as well as possible.
```python
# Insertion sort best case: already-sorted input → O(n)
```

**Average case:** the expected performance over a probability distribution of inputs (usually "random" inputs, uniformly distributed).
```python
# Quicksort average case: random pivot choices tend to split roughly evenly → O(n log n)
```

**Why worst case is usually the most important guarantee:** in safety-critical or real-time systems (flight control, medical devices), you need a guarantee that holds *no matter what* — average-case performance is not good enough if there exists any input that causes catastrophic slowdown. This is why algorithms like merge sort (guaranteed O(n log n) worst case) are preferred over quicksort in contexts where worst-case guarantees matter, despite quicksort's typically better average-case constant factors.

---

## 5. The Limits of Big-O — What It Does NOT Tell You

Big-O is an **asymptotic** measure — it describes behavior as n → ∞. It deliberately ignores:

**1. Constant factors.**
An O(n) algorithm with a huge constant (say, 1000n) can be slower in practice than an O(n log n) algorithm with a small constant (say, 2n log n), for a wide range of practical n. Big-O alone doesn't tell you which is faster for your specific n.

**2. Lower-order terms.**
`n² + 1000n` is O(n²), but for small n, the `1000n` term dominates.

**3. Real hardware effects.**
Cache locality, memory allocation patterns, and branch prediction can make a "worse" Big-O algorithm faster in practice for realistic input sizes. (This is precisely why Timsort's hybrid insertion-sort-for-small-runs strategy works — pure asymptotic analysis would never suggest it, but empirical performance does.)

**The practical lesson:** Big-O tells you how an algorithm **scales**. It does not, by itself, tell you which algorithm is fastest for your specific, finite-sized problem. Use Big-O to guide algorithm choice for large n and to rule out algorithms that will not scale; use empirical benchmarking (as in Lab 5) to make final decisions for your actual workload.

---

## 6. A Complete Worked Analysis — Putting It All Together

Let's fully analyze a non-trivial function, using every tool from this week.

```python
def mystery(matrix):
    """
    matrix: an n x n grid of integers.
    """
    n = len(matrix)
    count = 0

    for i in range(n):                    # O(n)
        row_sorted = sorted(matrix[i])    # O(n log n) — Python's Timsort
        for j in range(len(row_sorted)):  # O(n)
            if binary_search_helper(row_sorted, matrix[i][j] * 2):  # O(log n)
                count += 1

    return count

def binary_search_helper(sorted_lst, target):
    lo, hi = 0, len(sorted_lst) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_lst[mid] == target: return True
        elif sorted_lst[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return False
```

**Step-by-step analysis:**
1. Outer loop: runs n times → factor of O(n)
2. Inside outer loop: `sorted(matrix[i])` sorts a row of n elements → O(n log n) — done once per outer iteration
3. Inner loop: runs n times → factor of O(n)
4. Inside inner loop: `binary_search_helper` on a list of size n → O(log n)

**Combining:**
```
Total = O(n) × [O(n log n) + O(n) × O(log n)]
      = O(n) × [O(n log n) + O(n log n)]
      = O(n) × O(n log n)
      = O(n² log n)
```

This is a realistic example of the kind of multi-step analysis you'll perform routinely once you reach CS 102 (Algorithms II) and beyond — breaking a function into pieces, analyzing each piece's contribution, and combining them according to the sequential/nested rules from Wednesday.

---

## 7. Why This Course Emphasized Complexity From the Start

Look back at how far you've come:
- **Week 0–1:** basic Python, types, expressions
- **Week 2:** conditionals and loops — the building blocks of any algorithm
- **Week 3:** functions — how to organize and name computation
- **Week 4:** recursion — a second way to express repetition, with its own complexity implications
- **Week 5:** searching and sorting — concrete algorithms where complexity differences are dramatic and measurable
- **Week 6 (today):** the formal mathematics that makes all of the above rigorous

This is not a coincidence of curriculum design. **Complexity analysis is the single most transferable skill in this course.** It applies to every algorithm you will ever write, in every language, on every kind of hardware, for the rest of your career. A program that is "correct but slow" fails in production exactly as often as a program with a logic bug — and complexity analysis is how you predict and prevent that failure *before* it happens.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Complexity class hierarchy | O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!) |
| Log-log plots | Slope of the line estimates the exponent k in n^k |
| Worst/average/best case | Different assumptions about input; worst case is the guarantee that matters most for critical systems |
| Big-O's limitations | Ignores constants, lower-order terms, and real hardware effects |
| Multi-step analysis | Break functions into pieces; combine via sequential (add) / nested (multiply) rules |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** You time an algorithm at n = 1000, 2000, and 4000 and get 16 ms, 70 ms, and 297 ms. Determine its complexity class from the data alone, and state the general method.

**2. (Explain.)** §4 distinguishes worst, average, and best case. For each algorithm below give all three, and identify the one where the distinction matters most in practice.

Linear search · Insertion sort · Quicksort · Merge sort · Hash table lookup

**3. (Build.)** Analyse this function completely: time, space, best case, worst case. Then improve it and state the new complexity.

```python
def has_duplicate(xs):
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            if xs[i] == xs[j]:
                return True
    return False
```

**4. (Stretch.)** §5 lists what Big-O does not tell you. Give three concrete situations in which an algorithm with a *worse* asymptotic complexity is the correct engineering choice, with a specific example for each.


### Answers

**1.** **Θ(n²).**

The method is to look at the **ratio between successive doublings**: 70/16 ≈ 4.4 and 297/70 ≈ 4.2. Both are close to 4, and 4 = 2².

The general rule — for input size doubling, the ratio T(2n)/T(n) identifies the class:

| Ratio | Class |
|---|---|
| ≈ 1 | Θ(1) |
| ≈ 1 + a small constant | Θ(log n) |
| ≈ 2 | Θ(n) |
| slightly above 2 | Θ(n log n) |
| ≈ 4 | Θ(n²) |
| ≈ 8 | Θ(n³) |
| ≈ T(n)² | Θ(2ⁿ) |

For a polynomial Θ(n^k), the ratio is 2^k, so **k = log₂(ratio)** — here log₂ 4.2 ≈ 2.07, confirming k = 2.

Two cautions. Θ(n) and Θ(n log n) are hard to separate empirically, since the log factor changes the ratio from 2.00 to about 2.1 at these sizes — well within measurement noise. And small n is dominated by constant overheads and cache effects, so ratios only stabilise once the input is large enough that the asymptotic term dominates. Always take at least three points, and doubt a conclusion drawn from two.

**2.** | Algorithm | Best | Average | Worst |
|---|---|---|---|
| Linear search | Θ(1) | Θ(n) | Θ(n) |
| Insertion sort | Θ(n) | Θ(n²) | Θ(n²) |
| Quicksort | Θ(n log n) | Θ(n log n) | **Θ(n²)** |
| Merge sort | Θ(n log n) | Θ(n log n) | Θ(n log n) |
| Hash lookup | Θ(1) | Θ(1) | **Θ(n)** |

**Hash table lookup** is where it matters most. The gap is the largest — constant versus linear — and unlike quicksort's, the worst case is reachable by an **adversary** rather than only by unlucky data. If an attacker can choose keys that all hash to one bucket, every lookup degrades to a linear scan of that chain, turning an O(1) operation into O(n) and a web request into a denial of service. That is the hash-flooding attack of L26 §6, and it is why Python randomises its string hash seed per process.

Quicksort's worst case is the runner-up and is defended differently — randomised pivots make it unreachable in expectation, and introsort's depth limit makes it unreachable at all.

Note that **merge sort is the only row with no gap**. That predictability is exactly why it is chosen for real-time and external sorting even though quicksort is usually faster.

**3.** **As written:** Θ(1) auxiliary space. Best case Θ(1) time — the first two elements match and it returns immediately. Worst case Θ(n²) — no duplicates exist, so both loops run to completion, doing n(n−1)/2 comparisons. Average case is also Θ(n²) for random data with few duplicates.

**Improved:**

```python
def has_duplicate(xs):
    seen = set()
    for x in xs:
        if x in seen:
            return True
        seen.add(x)
    return False
```

**Θ(n) time, Θ(n) space** — a direct space-for-time trade, and the master pattern of L27 §1. Or, in one line, `len(set(xs)) != len(xs)`, which is the same complexity but always scans everything rather than returning early.

Two caveats the Big-O does not show. The set version requires elements to be **hashable**, so it fails on a list of lists where the quadratic version works. And its Θ(n) is the *average* case — the worst case is Θ(n²) if every element collides, which is §5's point about what Big-O leaves out.

If the elements are sortable but not hashable, `sorted` then scan adjacent pairs gives Θ(n log n) time and Θ(n) space — the middle option, and the right one when hashing is unavailable.

**4.** **1. Small n, where constants dominate.** Insertion sort is Θ(n²) and merge sort Θ(n log n), but insertion sort is faster below roughly 10–64 elements because its per-element work is a comparison and a move, with no allocation and perfect cache locality. Every production sort — Timsort, introsort — switches to insertion sort for small subarrays for exactly this reason.

**2. Predictability matters more than average speed.** Quicksort beats merge sort on average, but merge sort's Θ(n log n) is a *guarantee*. In a real-time system — audio processing, flight control — an operation that is usually fast and occasionally quadratic is unacceptable; a slightly slower operation that is never slow is correct. The same reasoning drives the choice of a balanced tree over a hash table when tail latency is the metric.

**3. Memory or locality is the real constraint.** An O(n²) in-place algorithm can beat an O(n log n) one that allocates an O(n) buffer, if the data barely fits in memory and the allocation forces swapping. Relatedly, a linear scan of a contiguous array often beats a "faster" pointer-chasing structure: searching a 1000-element sorted array linearly can outrun a binary search over a linked list, because the array is one cache line after another and the list is a thousand random memory accesses.

The unifying point: Big-O describes **growth**, not **cost**. It tells you which algorithm wins as n → ∞, and says nothing about the n you actually have, the constant factor, the memory hierarchy, or the variance. Measure.



---

## Reading

- **CLRS, Ch. 3.1** — Asymptotic notation, formal definitions revisited
- Review ALL Week 0–5 material — **Midterm 1 is this week**, covering everything through today

---

*CS 101 · Week 6 · Lecture 21 (Fri) · © CSE Department*
