# CS 101 · Problem Set 5
## Searching and Sorting Algorithms

**Released:** Friday 30 October 2026, 10:00 (after L18) · Week 5
**Due:** Friday 6 November 2026, 17:00 · Week 6 — late penalty from 17:01
**Submission:** `ps5.py` (Part B) and your answer sheet (Part A) in `"$CS101/week5"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 3 hours

*(Revised 2026-09-26: A4 (stability) and B3 (counting comparisons) repeated Lab 5 Parts 4 and 1–2; they
are now only in the lab. The answer key moved out of this handout.)*
**Note:** Midterm 1 is Monday 2 November (Weeks 0–5). Parts A and B1 double as revision — do them first.

---

## What this problem set uses

Weeks 0–5: linear and binary search and their variants, including binary search on the answer
(L16), selection/insertion/bubble sort, the `key` parameter, stability, and counting comparisons
(L17), merge sort and its recursion-tree analysis, quicksort, and the comparison lower bound (L18).

**Not needed and not expected:** timing with `time` (you count comparisons instead, as L17 §7 does),
greedy algorithms, heaps, and the formal Big-O definitions of Week 6.

Every Part B function needs a docstring with its loop invariant or base/recursive case, and at least
three `assert` tests covering an empty list, one element, and duplicates where they make sense.

---

## Part A: Written (44 points)

### A1: A Binary Search Bug (14 points)

```python
def binary_search_v2(lst, target, lo, hi):
    if lo >= hi:
        return -1
    mid = (lo + hi) // 2
    if lst[mid] == target:
        return mid
    elif lst[mid] < target:
        return binary_search_v2(lst, target, mid, hi)
    else:
        return binary_search_v2(lst, target, lo, mid)
```

Here `hi` is **exclusive** (the search range is `lst[lo:hi]`).

**(a)** Which line is wrong, and why? (L16 §4 on off-by-one traps.)
**(b)** Give a list and target that cause a `RecursionError`, and show the repeating call.
**(c)** Write the corrected version.
**(d)** State the invariant the corrected version maintains.

### A2: Choosing an Algorithm (12 points)

Choose from linear search, binary search, insertion sort, merge sort, or Python's `sorted()`, and
justify in one or two sentences (L18 §6's decision framework):

**(a)** 50 million records to sort by ID once. **(b)** ~20 items kept sorted while a few are inserted
each second. **(c)** One lookup in an unsorted list of 30 items. **(d)** Thousands of membership
queries per second against a sorted list of a million values.

### A3: Analysis (18 points)

**(a)** "Insertion sort is always faster than merge sort on tiny inputs." When is this true, and why
does Python's Timsort (L18 §3) use insertion sort inside?
**(b)** Draw the recursion tree for `T(n) = 2T(n/2) + n` (merge sort, L18 §1): the work at each level,
the number of levels, and the total.
**(c)** In your own words, why does the decision-tree argument (L18 §5) show that **every**
comparison sort needs about `n log₂ n` comparisons in the worst case?

---

## Part B: Python (`ps5.py`) (56 points)

### B1: Search Variants (28 points)

**(a)** `find_first(lst, target)` and `find_last(lst, target)` — the index of the first / last
occurrence in a **sorted** list, or `-1`, in O(log n): when you find the target, record it and keep
searching left (or right) — L16 §6.
`[1, 2, 2, 2, 3, 4]`, `2` → first `1`, last `3`.

**(b)** `count_occurrences(lst, target)` — using (a). `[1, 2, 2, 2, 3, 4]`, `2` → `3`.

**(c)** `sqrt_floor(n)` — `⌊√n⌋` by binary search on the answer (L16 §8), without `math.sqrt` or `** 0.5`.
`17` → `4`, `16` → `4`, `0` → `0`. Test it for every `n` below 2000 against the definition
`r*r <= n < (r+1)*(r+1)`.

### B2: Sorting (28 points)

Each returns a **new** list.

**(a)** `insertion_sort_by_key(lst, key)` — stable insertion sort by `key(x)`.
`(["hi", "a", "world"], len)` → `["a", "hi", "world"]`; `(["bb", "a", "cc", "d"], len)` → `["a", "d", "bb", "cc"]`.

**(b)** `merge_k_sorted(lists)` — merge k sorted lists by merging the result so far with each list in
turn (reuse the `merge` from L14/L18). `[[1, 4, 7], [2, 5, 8], [3, 6, 9]]` → `[1, …, 9]`.

**(c)** `top_k(lst, k)` — the `k` largest in descending order **without sorting the whole list**: run
`k` passes of selection (find the largest remaining, take it out). `([5, 2, 8, 1, 9, 3], 3)` → `[9, 8, 5]`.

---

## Grading Rubric

| Problem | Points |
|---------|--------|
| A1 Binary search bug | 14 |
| A2 Choosing an algorithm | 12 |
| A3 Analysis | 18 |
| B1 Search variants | 28 |
| B2 Sorting | 28 |
| **Total** | **100** |

---

*CS 101 · Week 5 · Problem Set 5 · Due Friday 6 November 2026, 17:00 · © CSE Department*
