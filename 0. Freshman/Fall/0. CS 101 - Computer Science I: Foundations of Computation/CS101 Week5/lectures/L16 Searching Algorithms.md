# CS 101 · Lecture 16 (Week 5, Lecture 1)
## Searching Algorithms: Linear and Binary Search

**Week 5 · Wednesday**
*"Why does binary search work on sorted arrays? Because sorting imposes order — a global structure — on data, and binary search exploits that structure to eliminate half the search space with each comparison." — CS 101*

**Date:** Wednesday 28 October 2026 · 09:00–09:50 · Week 5

---

## 0. From Recursion to Algorithms

Week 4 gave you recursion as a tool. This week we use that tool — and iteration — to study **algorithms** formally for the first time: precise procedures with provable properties, analyzed for correctness and efficiency.

We start with searching because it is the simplest setting in which the central idea of this course appears: **the same problem can be solved with wildly different efficiency, depending on what structure you exploit.**

---

## 1. The Searching Problem: Formal Statement

**Input:** A collection of n elements, and a target value.
**Output:** The location (index) of the target in the collection, or an indication that it is not present.

This sounds trivial. It is not — the *efficiency* of solving it depends entirely on what you know about the collection's structure.

---

## 2. Linear Search: The Baseline

**Linear search** checks each element in order until it finds the target or exhausts the collection.

```python
def linear_search(lst, target):
    """
    Search for target in lst by checking every element in order.

    Args:
        lst:    a list of any comparable elements (no ordering required)
        target: the value to find

    Returns:
        int: index of target, or -1 if not found

    Time complexity: O(n) — worst case checks every element
    Space complexity: O(1)

    Precondition: NONE — works on unsorted data.

    Examples:
        linear_search([4, 2, 7, 1, 9], 7)  → 2
        linear_search([4, 2, 7, 1, 9], 5)  → -1
    """
    for i, value in enumerate(lst):
        if value == target:
            return i
    return -1
```

**Why is this the best you can do on unsorted data?** Because without any structural knowledge, the target could be anywhere — you have no basis for skipping any element. In the worst case (target is last, or absent), you must check all n elements.

**Formal lower bound:** Any correct search algorithm on unordered data requires Ω(n) comparisons in the worst case. This is not an implementation limitation — it is a mathematical fact about the problem.

---

## 3. Binary Search: Exploiting Order

If the collection is **sorted**, you gain enormous power: comparing against the middle element tells you which half the target must be in (if present), eliminating the other half entirely.

```python
def binary_search(lst, target):
    """
    Search for target in a SORTED lst using binary search.

    Args:
        lst:    a list sorted in ascending order
        target: the value to find

    Returns:
        int: index of target, or -1 if not found

    Precondition: lst must be sorted in ascending order.

    Time complexity: O(log n)
    Space complexity: O(1) — iterative version

    Examples:
        binary_search([1,3,5,7,9,11], 7)  → 3
        binary_search([1,3,5,7,9,11], 4)  → -1
    """
    lo, hi = 0, len(lst) - 1

    # Loop invariant: if target is in lst, it is in lst[lo..hi]
    while lo <= hi:
        mid = (lo + hi) // 2
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            lo = mid + 1     # target must be in the right half
        else:
            hi = mid - 1     # target must be in the left half

    return -1   # lo > hi: search space exhausted, target not present
```

**Why this is correct:** The loop invariant — "if target is in lst, it is in lst[lo..hi]" — holds at the start, is preserved by every branch, and (combined with the exit condition `lo > hi`) proves correctness. We proved this formally in Week 4.

**Why O(log n)?** Each iteration halves the search space: n → n/2 → n/4 → ... → 1. The number of halvings needed is log₂n. For n = 1,000,000: at most 20 comparisons. For n = 1,000,000,000: at most 30 comparisons.

---

## 4. The Off-By-One Trap: Why Binary Search Is Notoriously Hard to Get Right

Jon Bentley's famous observation (*Programming Pearls*): when he asked professional programmers to implement binary search, the vast majority had bugs — usually off-by-one errors in the boundary conditions.

**Common bugs:**

```python
# BUG 1: Using < instead of <=
while lo < hi:              # WRONG — misses the case lo == hi
    ...

# BUG 2: mid+1 / mid-1 confusion
lo = mid       # WRONG — can cause infinite loop if lo becomes stuck at mid
hi = mid       # WRONG — same issue

# BUG 3: Integer overflow (in languages with fixed-size integers)
mid = (lo + hi) // 2    # in C/Java: lo+hi can overflow for huge arrays
# Fix (used in Java's real implementation):
mid = lo + (hi - lo) // 2   # avoids overflow — not an issue in Python (arbitrary precision ints)
```

**The discipline that prevents these bugs:** always state the loop invariant explicitly, and verify that every branch preserves it. This is not academic — it is the actual engineering practice that prevents bugs in production search code.

---

## 5. Comparing Linear and Binary Search

|                  | Linear Search                           | Binary Search                           |
| ---------------- | --------------------------------------- | --------------------------------------- |
| Precondition     | None                                    | Data must be sorted                     |
| Time complexity  | O(n)                                    | O(log n)                                |
| Space complexity | O(1)                                    | O(1) iterative, O(log n) recursive      |
| Best for         | Unsorted data, small n, one-time search | Sorted data, large n, repeated searches |

**The crucial tradeoff:** if you need to search once, sorting first (which costs O(n log n)) to then binary search (O(log n)) is *slower overall* than a single linear search (O(n)). Binary search pays off when you search **many times** on the same sorted data — the sorting cost is amortized across all the searches.

```python
# When linear search wins:
data = get_data()               # unsorted, O(n) to sort
result = linear_search(data, x)  # O(n) — total: O(n)

# When binary search wins:
data = sorted(get_data())        # O(n log n) once
for x in many_queries:            # searching m times
    result = binary_search(data, x)  # O(log n) each
# Total: O(n log n) + O(m log n) — wins when m is large
```

---

## 6. Variants of Binary Search

### Finding the first occurrence (with duplicates)

```python
def binary_search_leftmost(lst, target):
    """
    Return the index of the FIRST occurrence of target in a sorted list
    (which may contain duplicates). Return -1 if not found.

    Examples:
        binary_search_leftmost([1,2,2,2,3,4], 2)  → 1  (first 2, not just any 2)
    """
    lo, hi = 0, len(lst) - 1
    result = -1

    while lo <= hi:
        mid = (lo + hi) // 2
        if lst[mid] == target:
            result = mid       # record this match...
            hi = mid - 1       # ...but keep searching LEFT for an earlier one
        elif lst[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return result
```

### Finding the insertion point (bisect)

```python
def bisect_left(lst, target):
    """
    Return the index where target should be inserted to keep lst sorted,
    inserting before any existing equal elements.

    Examples:
        bisect_left([1,3,5,7], 4)  → 2  (insert 4 between index 1 and 2)
        bisect_left([1,3,5,7], 3)  → 1  (insert before the existing 3)
    """
    lo, hi = 0, len(lst)

    while lo < hi:
        mid = (lo + hi) // 2
        if lst[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
```

Python's standard library provides this: `bisect.bisect_left(lst, target)`. It is used constantly in real code — e.g., maintaining a sorted list while inserting new elements in O(log n) search + O(n) insertion time.

---

## 7. Searching in 2D and Beyond: A Preview

Binary search generalizes beyond flat sorted arrays.

**Searching a row-and-column sorted matrix:**
```python
def search_matrix(matrix, target):
    """
    Search a matrix where each row and column is sorted in ascending order.
    Start from the top-right corner: if current > target, move left;
    if current < target, move down.

    Time: O(rows + cols) — not O(log n), but much better than O(rows*cols).
    """
    if not matrix or not matrix[0]:
        return False

    row, col = 0, len(matrix[0]) - 1

    while row < len(matrix) and col >= 0:
        current = matrix[row][col]
        if current == target:
            return True
        elif current > target:
            col -= 1     # eliminate this column
        else:
            row += 1     # eliminate this row

    return False
```

This is not binary search, but it uses the same underlying idea: **exploit structure to eliminate large portions of the search space with each comparison.**

---

## 8. Searching Over a Function: Binary Search on the Answer

A powerful generalization: binary search doesn't require an array. It works on **any monotonic predicate** — a Boolean function that is False, then True (or vice versa), as some parameter increases.

```python
def sqrt_binary_search(x, tolerance=1e-9):
    """
    Compute sqrt(x) using binary search on the answer.

    We search for the largest value g such that g*g <= x.
    """
    if x < 0:
        raise ValueError("Cannot take sqrt of a negative number")
    if x == 0:
        return 0.0

    lo, hi = 0.0, max(1.0, x)

    while hi - lo > tolerance:
        mid = (lo + hi) / 2
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid

    return lo


assert abs(sqrt_binary_search(4)  - 2.0)      < 1e-6
assert abs(sqrt_binary_search(2)  - 2**0.5)   < 1e-6
assert abs(sqrt_binary_search(100) - 10.0)    < 1e-6
```

This pattern — "binary search on the answer" — is one of the most powerful and underused techniques in algorithm design. Any time you can phrase a problem as "find the smallest/largest value satisfying property P, where P is monotonic," binary search applies, even without an explicit sorted array.

---

## 9. Summary

| Concept | Key Point |
|---------|-----------|
| Linear search | O(n); no precondition; optimal for unsorted data |
| Binary search | O(log n); requires sorted data; halves search space each step |
| Loop invariant | "If target is in lst, it is in lst[lo..hi]" — proves correctness |
| Off-by-one bugs | The most common source of binary search errors — verify invariant explicitly |
| Sort-then-search tradeoff | Only pays off when searching many times on the same data |
| bisect_left | Finds insertion point; Python's `bisect` module implements this |
| Binary search on the answer | Generalizes to any monotonic predicate, not just sorted arrays |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** This binary search has an off-by-one bug. Find the input that breaks it, then state the loop invariant the correct version maintains.

```python
def search(xs, target):
    lo, hi = 0, len(xs) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if xs[mid] == target:
            return mid
        elif xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

**2. (Explain.)** Given `a = [1, 2, 2, 2, 5]`, give the values of `bisect_left(a, 2)`, `bisect_right(a, 2)`, `bisect_left(a, 3)`, and `bisect_left(a, 0)`. Then give a one-line expression for how many times `2` occurs.

**3. (Build.)** Use binary search on the answer (§8) to write `min_capacity(weights, days)`: the smallest ship capacity that lets you ship the packages, in order, within `days` days. State the monotonic predicate you are searching over.

**4. (Stretch.)** §4 mentions that `mid = (lo + hi) // 2` can overflow in languages with fixed-size integers — a bug that sat undetected in Java's standard library for nine years. Explain the failure, give the standard fix, and say why Python is immune.


### Answers

**1.** The bug is `while lo < hi` — it must be `while lo <= hi`. Any input where the target sits in a **one-element** final range fails: `search([1, 2, 3], 3)` returns `-1`, and so does `search([5], 5)`.

Trace `search([5], 5)`: `lo = 0`, `hi = 0`, the condition `0 < 0` is false, the loop never runs, and the function reports not-found without ever examining the only element.

**Invariant:** *if `target` is present in `xs`, it lies within `xs[lo..hi]` inclusive.* Initialisation holds because `[0 .. len-1]` is the whole list. Maintenance holds because the list is sorted: when `xs[mid] < target`, everything at or below `mid` is too small, so discarding through `mid` cannot discard the target.

The exit condition is what exposes the bug. With `lo <= hi`, the loop ends when `lo > hi`, i.e. the range is genuinely **empty**, and the invariant then says the target is absent — a valid conclusion. With `lo < hi`, the loop ends when `lo == hi`, a range still holding **one unexamined element**, and concluding "absent" is unjustified. Whenever a binary search is wrong, compare its exit condition against the invariant like this; the answer is always there.

**2.** `1`, `4`, `4`, `0`. Occurrence count: `bisect_right(a, x) - bisect_left(a, x)` — here `4 - 1 = 3`.

`bisect_left` returns the index of the **first** position where the value could be inserted keeping the list sorted — for a present value, the index of its first occurrence. `bisect_right` returns the **last** such position, one past its final occurrence. Together they bracket the run.

`bisect_left(a, 3)` is `4` even though `3` is absent: it is the insertion point, between the `2`s and the `5`. This is what makes bisect more useful than a plain "find" — the answer is meaningful whether or not the target exists, which is why it underlies range queries, "find the closest value", and scheduling by timestamp.

`bisect_left(a, 0)` is `0`, the insertion point before everything. To turn either into a membership test you must check the boundary yourself: `i = bisect_left(a, x); found = i < len(a) and a[i] == x`. Forgetting the `i < len(a)` guard when the target exceeds everything in the list is the standard bisect bug.

**3.**

```python
def min_capacity(weights, days):
    def days_needed(cap):
        d, load = 1, 0
        for w in weights:
            if load + w > cap:
                d += 1
                load = 0
            load += w
        return d

    lo, hi = max(weights), sum(weights)   # both feasible bounds
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(mid) <= days:
            hi = mid            # feasible: try smaller
        else:
            lo = mid + 1
    return lo
```

**Predicate:** `feasible(cap)` = "a ship of capacity `cap` can deliver everything within `days` days". It is **monotonic**: if a capacity works, every larger capacity works too. So the predicate's values form `False False … False True True … True`, and binary search finds the boundary.

That monotonicity is the entire requirement — the array being searched is *conceptual*, never materialised, and "sorted" means only that the predicate flips once. The bounds must be chosen so the answer is inside: `max(weights)` because no ship smaller than the heaviest package can ever load it, and `sum(weights)` because that capacity always finishes in one day.

Note this loop uses `while lo < hi` with `hi = mid` — correct here, because the invariant is different: `hi` stays *feasible* rather than being excluded. Binary search variants differ in exactly this way, and the invariant is what tells you which form you need.

**4.** In a language with 32-bit signed `int`, `lo + hi` can exceed 2³¹ − 1 when both indices are large — roughly, when the array has more than about a billion elements. The sum wraps to a **negative** number, the division yields a negative `mid`, and the next array access throws `ArrayIndexOutOfBoundsException`. The bug was in `java.util.Arrays.binarySearch` from 1997 and was publicly diagnosed by Joshua Bloch in 2006; the same code had been copied into countless textbooks, including from Bentley's *Programming Pearls*.

The standard fix computes the **offset** rather than the sum:

```
mid = lo + (hi - lo) // 2
```

`hi - lo` is at most the array length and cannot overflow, and adding it back to `lo` stays in range. (In Java one can also write `(lo + hi) >>> 1`, using the unsigned right shift to reinterpret the wrapped bit pattern correctly — clever, but the subtraction form is clearer and portable.)

Python is immune because its integers are **arbitrary precision** — `lo + hi` simply grows to whatever size it needs, and there is no wraparound to trigger. This is a case where Python's slower integer representation buys a real correctness guarantee. Write `lo + (hi - lo) // 2` anyway: you will write binary search in C in PROG 101, where the bug is live.



---

## Reading

- **Guttag, Ch. 3.4** — Bisection Search (primary)
- **CLRS, Ch. 2** — brief mention of search as a warm-up to sorting (optional, for the ambitious)

---

*CS 101 · Week 5 · Lecture 16 (Wed) · © CSE Department*
