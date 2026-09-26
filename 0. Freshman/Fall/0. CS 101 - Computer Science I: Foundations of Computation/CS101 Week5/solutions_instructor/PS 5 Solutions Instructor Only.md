# CS 101 · Problem Set 5 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** The reference `ps5.py` below was run; every assert passes and
> the B3 table is the real output.

### A1 (14)

(a) `binary_search_v2(lst, target, mid, hi)` — with an exclusive `hi`, `mid` has already been
checked, so the left bound must become `mid + 1`. When `hi = lo + 1`, `mid == lo` and the call repeats
unchanged. *(4)* (b) `binary_search_v2([1, 3], 2, 0, 2)`: `mid = 1`, `3 > 2` → `(0, 1)`; `mid = 0`,
`1 < 2` → `(0, 1)` again, forever → `RecursionError`. *(4)* (c) Change that call to
`binary_search_v2(lst, target, mid + 1, hi)`. *(3)* (d) If `target` is in `lst`, its index is in
`[lo, hi)`, and `hi − lo` strictly decreases on every call. *(3)*

### A2 (12, 3 each)

(a) `sorted()` (or merge sort) — O(n log n) once; stability is free. (b) Insertion sort — nearly-sorted,
tiny data; each insertion is a short shift. (c) Linear search — sorting first costs more than one scan.
(d) Binary search — ~20 comparisons per query, and the sort cost is already paid.

### A3 (18, 6 each)

(a) True for small `n` (tens of items): insertion sort has almost no overhead per step and is linear on
nearly-sorted data, while merge sort pays for recursion and copying. Timsort sorts short runs with
insertion sort and merges them. *(6)* (b) Level `k` has `2ᵏ` sub-problems of size `n/2ᵏ`: **n work per
level**, `log₂ n` levels + the leaves → about `n log₂ n`. *(6)* (c) A comparison sort's run is a path in a
binary decision tree; it must have a leaf for each of the `n!` orderings, so its height is at least
`log₂(n!) ≈ n log₂ n`. It says nothing about any particular algorithm — only that each comparison gives one
bit. *(6)*

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

print("all asserts passed")
```

**Marking.** B1: 11 / 6 / 11 (the 2000-value test is required for full marks on (c)). B2: 10 / 9 / 9 —
`insertion_sort_by_key` must pass the stability assert. Missing invariant/base-case
docstring or fewer than three asserts: −1 per function (max −5).

---

*CS 101 · Week 5 · Problem Set 5 · Due Friday 6 November 2026, 17:00 · © CSE Department*
