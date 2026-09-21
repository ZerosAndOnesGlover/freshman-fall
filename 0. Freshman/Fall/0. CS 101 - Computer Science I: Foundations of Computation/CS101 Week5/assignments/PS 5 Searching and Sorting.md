# CS 101 · Problem Set 5
## Searching and Sorting Algorithms

**Released:** Friday 30 October 2026, 10:00 (after L18) · Week 5
**Due:** Friday 6 November 2026, 17:00 · Week 6 — late penalty from 17:01
**Submission:** `ps5.py` (Part B) and your answer sheet (Part A) in `"$CS101/week5"`, committed to the Freshman Fall repo.
**Points:** 100 · Part of the 30% Problem Sets grade (lowest one dropped)
**Expected time:** about 4 hours
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

## Part A: Written (40 points)

### A1: A Binary Search Bug (10 points)

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

### A2: Choosing an Algorithm (8 points)

Choose from linear search, binary search, insertion sort, merge sort, or Python's `sorted()`, and
justify in one or two sentences (L18 §6's decision framework):

**(a)** 50 million records to sort by ID once. **(b)** ~20 items kept sorted while a few are inserted
each second. **(c)** One lookup in an unsorted list of 30 items. **(d)** Thousands of membership
queries per second against a sorted list of a million values.

### A3: Analysis (12 points)

**(a)** "Insertion sort is always faster than merge sort on tiny inputs." When is this true, and why
does Python's Timsort (L18 §3) use insertion sort inside?
**(b)** Draw the recursion tree for `T(n) = 2T(n/2) + n` (merge sort, L18 §1): the work at each level,
the number of levels, and the total.
**(c)** In your own words, why does the decision-tree argument (L18 §5) show that **every**
comparison sort needs about `n log₂ n` comparisons in the worst case?

### A4: Stability (10 points)

**(a)** Give concrete data showing why stability matters: a list of `(last_name, first_name)` pairs
already in first-name order, then sorted by last name only.
**(b)** In your `insertion_sort_by_key` (B2), what would happen to stability if the inner test were
`key(result[j]) >= key(item)` instead of `>`? Show it on `["bb", "a", "cc", "d"]` with `key=len`.

---

## Part B: Python (`ps5.py`) (60 points)

### B1: Search Variants (20 points)

**(a)** `find_first(lst, target)` and `find_last(lst, target)` — the index of the first / last
occurrence in a **sorted** list, or `-1`, in O(log n): when you find the target, record it and keep
searching left (or right) — L16 §6.
`[1, 2, 2, 2, 3, 4]`, `2` → first `1`, last `3`.

**(b)** `count_occurrences(lst, target)` — using (a). `[1, 2, 2, 2, 3, 4]`, `2` → `3`.

**(c)** `sqrt_floor(n)` — `⌊√n⌋` by binary search on the answer (L16 §8), without `math.sqrt` or `** 0.5`.
`17` → `4`, `16` → `4`, `0` → `0`. Test it for every `n` below 2000 against the definition
`r*r <= n < (r+1)*(r+1)`.

### B2: Sorting (20 points)

Each returns a **new** list.

**(a)** `insertion_sort_by_key(lst, key)` — stable insertion sort by `key(x)`.
`(["hi", "a", "world"], len)` → `["a", "hi", "world"]`; `(["bb", "a", "cc", "d"], len)` → `["a", "d", "bb", "cc"]`.

**(b)** `merge_k_sorted(lists)` — merge k sorted lists by merging the result so far with each list in
turn (reuse the `merge` from L14/L18). `[[1, 4, 7], [2, 5, 8], [3, 6, 9]]` → `[1, …, 9]`.

**(c)** `top_k(lst, k)` — the `k` largest in descending order **without sorting the whole list**: run
`k` passes of selection (find the largest remaining, take it out). `([5, 2, 8, 1, 9, 3], 3)` → `[9, 8, 5]`.

### B3: Counting Comparisons (20 points)

Following L17 §7:

**(a)** `selection_sort_count(lst)` and `insertion_sort_count(lst)` — each returns
`(sorted_copy, comparisons)`, counting every comparison between two elements.

**(b)** For `n` = 100, 200, 400, run both on an already-sorted list and a reversed list, and print a table:

```
    n     input  selection  insertion
  100    sorted       4950         99
  ...
```

**(c)** In a comment, explain: why selection sort's count does not depend on the input order; why
insertion sort's does; and what happens to each count when `n` doubles.

---

## Grading Rubric

| Problem | Points |
|---------|--------|
| A1 Binary search bug | 10 |
| A2 Choosing an algorithm | 8 |
| A3 Analysis | 12 |
| A4 Stability | 10 |
| B1 Search variants | 20 |
| B2 Sorting | 20 |
| B3 Counting comparisons | 20 |
| **Total** | **100** |

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** The reference `ps5.py` below was run; every assert passes and
> the B3 table is the real output.

### A1 (10)

(a) `binary_search_v2(lst, target, mid, hi)` — with an exclusive `hi`, `mid` has already been
checked, so the left bound must become `mid + 1`. When `hi = lo + 1`, `mid == lo` and the call repeats
unchanged. *(3)* (b) `binary_search_v2([1, 3], 2, 0, 2)`: `mid = 1`, `3 > 2` → `(0, 1)`; `mid = 0`,
`1 < 2` → `(0, 1)` again, forever → `RecursionError`. *(3)* (c) Change that call to
`binary_search_v2(lst, target, mid + 1, hi)`. *(2)* (d) If `target` is in `lst`, its index is in
`[lo, hi)`, and `hi − lo` strictly decreases on every call. *(2)*

### A2 (8, 2 each)

(a) `sorted()` (or merge sort) — O(n log n) once; stability is free. (b) Insertion sort — nearly-sorted,
tiny data; each insertion is a short shift. (c) Linear search — sorting first costs more than one scan.
(d) Binary search — ~20 comparisons per query, and the sort cost is already paid.

### A3 (12)

(a) True for small `n` (tens of items): insertion sort has almost no overhead per step and is linear on
nearly-sorted data, while merge sort pays for recursion and copying. Timsort sorts short runs with
insertion sort and merges them. *(4)* (b) Level `k` has `2ᵏ` sub-problems of size `n/2ᵏ`: **n work per
level**, `log₂ n` levels + the leaves → about `n log₂ n`. *(4)* (c) A comparison sort's run is a path in a
binary decision tree; it must have a leaf for each of the `n!` orderings, so its height is at least
`log₂(n!) ≈ n log₂ n`. It says nothing about any particular algorithm — only that each comparison gives one
bit. *(4)*

### A4 (10)

(a) E.g. `[("Smith", "Ann"), ("Jones", "Bob"), ("Smith", "Cal")]`: a stable sort by last name gives
Jones Bob, Smith Ann, Smith Cal — the Smiths stay in first-name order; an unstable one may give Smith
Cal before Smith Ann. *(5)* (b) With `>=`, equal keys are shifted past each other: `"d"` moves in front
of `"a"` and `"cc"` in front of `"bb"`, giving `["d", "a", "cc", "bb"]` — **not stable**. *(5)*

### Part B — reference `ps5.py`

```python
# --- B1: Search variants ---
def find_first(lst, target):
    """Index of the first occurrence of target in sorted lst, or -1. O(log n).
    Invariant: if target is present, its first index is in [lo, hi]; answer holds the best index found so far."""
    lo, hi = 0, len(lst) - 1
    answer = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if lst[mid] == target:
            answer = mid
            hi = mid - 1          # keep looking left
        elif lst[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return answer

def find_last(lst, target):
    """Index of the last occurrence of target in sorted lst, or -1. O(log n)."""
    lo, hi = 0, len(lst) - 1
    answer = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if lst[mid] == target:
            answer = mid
            lo = mid + 1          # keep looking right
        elif lst[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return answer

def count_occurrences(lst, target):
    """How many times target occurs in sorted lst, using find_first and find_last. O(log n)."""
    first = find_first(lst, target)
    if first == -1:
        return 0
    return find_last(lst, target) - first + 1

def sqrt_floor(n):
    """floor(sqrt(n)) for n >= 0 by binary search on the answer (L16 §8)."""
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi + 1) // 2      # round up so the range always shrinks
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo

assert find_first([1, 2, 2, 2, 3, 4], 2) == 1 and find_last([1, 2, 2, 2, 3, 4], 2) == 3
assert find_first([1, 2, 3], 5) == -1 and find_last([], 1) == -1
assert count_occurrences([1, 2, 2, 2, 3, 4], 2) == 3 and count_occurrences([1, 2, 3], 5) == 0
assert count_occurrences([7, 7, 7], 7) == 3
assert sqrt_floor(17) == 4 and sqrt_floor(16) == 4 and sqrt_floor(0) == 0 and sqrt_floor(1) == 1
for k in range(2000):
    assert sqrt_floor(k) ** 2 <= k < (sqrt_floor(k) + 1) ** 2

# --- B2: Sorting ---
def insertion_sort_by_key(lst, key):
    """New list sorted by key(x), stable. Invariant: result[:i] is sorted by key."""
    result = lst[:]
    for i in range(1, len(result)):
        item = result[i]
        j = i - 1
        while j >= 0 and key(result[j]) > key(item):   # strict > keeps equal keys in order: stable
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = item
    return result

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]

def merge_k_sorted(lists):
    """Merge k sorted lists by repeated pairwise merging."""
    result = []
    for lst in lists:
        result = merge(result, lst)
    return result

def top_k(lst, k):
    """The k largest elements in descending order, by k passes of selection (no full sort)."""
    work = lst[:]
    result = []
    for _ in range(min(k, len(work))):
        best = 0
        for i in range(1, len(work)):
            if work[i] > work[best]:
                best = i
        result.append(work[best])
        work[best], work[-1] = work[-1], work[best]
        work.pop()
    return result

assert insertion_sort_by_key(["hi", "a", "world"], len) == ["a", "hi", "world"]
assert insertion_sort_by_key(["bb", "a", "cc", "d"], len) == ["a", "d", "bb", "cc"]   # stable
assert insertion_sort_by_key([], len) == []
assert merge_k_sorted([[1, 4, 7], [2, 5, 8], [3, 6, 9]]) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
assert merge_k_sorted([]) == [] and merge_k_sorted([[], [1]]) == [1]
assert top_k([5, 2, 8, 1, 9, 3], 3) == [9, 8, 5] and top_k([1], 5) == [1] and top_k([], 2) == []

# --- B3: Counting comparisons ---
def selection_sort_count(lst):
    """(sorted copy, number of element comparisons)."""
    a = lst[:]
    comparisons = 0
    for i in range(len(a)):
        smallest = i
        for j in range(i + 1, len(a)):
            comparisons += 1
            if a[j] < a[smallest]:
                smallest = j
        a[i], a[smallest] = a[smallest], a[i]
    return a, comparisons

def insertion_sort_count(lst):
    """(sorted copy, number of element comparisons)."""
    a = lst[:]
    comparisons = 0
    for i in range(1, len(a)):
        item = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > item:
                a[j + 1] = a[j]
                j -= 1
            else:
                break
        a[j + 1] = item
    return a, comparisons

print(f"{'n':>5} {'input':>9} {'selection':>10} {'insertion':>10}")
for n in [100, 200, 400]:
    for name, data in [("sorted", list(range(n))), ("reversed", list(range(n, 0, -1)))]:
        s_sorted, s_count = selection_sort_count(data)
        i_sorted, i_count = insertion_sort_count(data)
        assert s_sorted == i_sorted == sorted(data)
        print(f"{n:>5} {name:>9} {s_count:>10} {i_count:>10}")
print("all asserts passed")
```

Output of B3:

```
    n     input  selection  insertion
  100    sorted       4950         99
  100  reversed       4950       4950
  200    sorted      19900        199
  200  reversed      19900      19900
  400    sorted      79800        399
  400  reversed      79800      79800
```

(c) Selection sort always scans the whole unsorted part: `n(n−1)/2` comparisons whatever the order.
Insertion sort stops each inner loop as soon as it finds a smaller element: `n − 1` on sorted input,
`n(n−1)/2` on reversed. Doubling `n` about **quadruples** the quadratic counts and **doubles** the
linear one.

**Marking.** B1: 8 / 4 / 8 (the 2000-value test is required for full marks on (c)). B2: 8 / 6 / 6 —
`insertion_sort_by_key` must pass the stability assert. B3: 10 / 6 / 4. Missing invariant/base-case
docstring or fewer than three asserts: −1 per function (max −5).

---

*CS 101 · Week 5 · Problem Set 5 · Due Friday 6 November 2026, 17:00 · © CSE Department*
