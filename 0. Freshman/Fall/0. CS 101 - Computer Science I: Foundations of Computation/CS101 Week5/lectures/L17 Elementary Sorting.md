# CS 101 · Lecture 17 (Week 5, Lecture 2)
## Elementary Sorting: Selection, Insertion, and Bubble Sort

**Week 5 · Thursday**
*"Sorting is the process by which chaos is transformed into structure — and that structure is what makes efficient search, deduplication, and analysis possible." — CS 101*

**Date:** Thursday 24 September 2026 · 09:00–09:50 · Week 5

---

## 0. Why Sorting Matters So Much

Sorting is arguably the single most-studied problem in computer science. Not because sorting itself is glamorous, but because:

1. **It enables binary search**: the O(log n) magic from Wednesday requires sorted data
2. **It reveals algorithmic thinking clearly**: the same problem, many approaches, wildly different efficiency
3. **It appears everywhere**: databases, search engines, compilers, graphics — anything that needs order

Today we cover the three classic **O(n²)** sorting algorithms. They are not the fastest (Friday covers O(n log n) approaches), but they are the clearest way to build intuition about what "sorting" actually requires.

---

## 1. Selection Sort: Repeatedly Find the Minimum

**Idea:** Find the minimum of the unsorted portion, swap it to the front. Repeat for the remaining unsorted portion.

```python
def selection_sort(lst):
    """
    Sort lst in place using selection sort.

    Loop invariant: after the ith iteration, lst[0..i] contains the
    i+1 smallest elements of the original list, in sorted order.

    Time complexity: O(n²) — always, regardless of input order
    Space complexity: O(1) — sorts in place

    Examples:
        selection_sort([5, 2, 8, 1, 9])  → [1, 2, 5, 8, 9]  (mutates lst)
    """
    n = len(lst)

    for i in range(n - 1):
        # Find the index of the minimum in lst[i:]
        min_idx = i
        for j in range(i + 1, n):
            if lst[j] < lst[min_idx]:
                min_idx = j

        # Swap the minimum into position i
        lst[i], lst[min_idx] = lst[min_idx], lst[i]

    return lst
```

**Trace for `[5, 2, 8, 1, 9]`:**
```
i=0: min in [5,2,8,1,9] is 1 at idx 3 → swap → [1,2,8,5,9]
i=1: min in [2,8,5,9]   is 2 at idx 1 → no swap needed → [1,2,8,5,9]
i=2: min in [8,5,9]     is 5 at idx 3 → swap → [1,2,5,8,9]
i=3: min in [8,9]       is 8 at idx 3 → no swap needed → [1,2,5,8,9]
Done: [1,2,5,8,9]
```

**Complexity analysis:** The outer loop runs n-1 times. The inner loop (finding the minimum) runs n-1, n-2, ..., 1 times. Total comparisons: (n-1) + (n-2) + ... + 1 = n(n-1)/2 = O(n²).

**Key property:** Selection sort makes exactly O(n) swaps (one per outer iteration) — this matters when swaps are expensive (e.g., large records) even though comparisons are O(n²).

---

## 2. Insertion Sort: Build the Sorted Portion One Element at a Time

**Idea:** Maintain a sorted prefix. Take the next element and insert it into the correct position within the sorted prefix.

```python
def insertion_sort(lst):
    """
    Sort lst in place using insertion sort.

    Loop invariant: after the ith iteration, lst[0..i] is sorted
    (though not necessarily containing the smallest i+1 elements —
    just the first i+1 elements of the original list, now in order).

    Time complexity:
        Worst case:   O(n²) — reverse-sorted input
        Best case:    O(n)  — already-sorted input!
        Average case: O(n²)
    Space complexity: O(1)

    Examples:
        insertion_sort([5, 2, 8, 1, 9])  → [1, 2, 5, 8, 9]
    """
    n = len(lst)

    for i in range(1, n):
        key = lst[i]           # the element to insert
        j = i - 1

        # Shift elements greater than key to the right
        while j >= 0 and lst[j] > key:
            lst[j + 1] = lst[j]
            j -= 1

        lst[j + 1] = key        # insert key in its correct position

    return lst
```

**Trace for `[5, 2, 8, 1, 9]`:**
```
i=1: key=2. Shift 5 right. Insert 2 at 0.  → [2,5,8,1,9]
i=2: key=8. 8 > lst[1]=5, no shift needed.  → [2,5,8,1,9]
i=3: key=1. Shift 8,5,2 right. Insert 1 at 0. → [1,2,5,8,9]
i=4: key=9. 9 > lst[3]=8, no shift needed.  → [1,2,5,8,9]
Done: [1,2,5,8,9]
```

**Why insertion sort is O(n) on nearly-sorted data:** if the data is already sorted, the `while` condition `lst[j] > key` is immediately False for every i — no shifting occurs, and the outer loop just scans through once: O(n).

**This matters in practice.** Real-world data is often nearly sorted (e.g., adding a few new records to an already-sorted database). Insertion sort's best-case behavior makes it genuinely useful — in fact, Python's built-in `sort()` (Timsort) uses insertion sort for small sub-arrays as part of a hybrid strategy, which we'll see Friday.

---

## 3. Bubble Sort: Repeatedly Swap Adjacent Out-of-Order Pairs

**Idea:** Repeatedly scan through the list, swapping any adjacent pair that is out of order. Each full pass "bubbles" the largest remaining element to its correct position at the end.

```python
def bubble_sort(lst):
    """
    Sort lst in place using bubble sort.

    Loop invariant: after the ith pass, the i largest elements are
    in their correct final positions at the end of the list.

    Time complexity:
        Worst case:   O(n²)
        Best case:    O(n)  — with the early-exit optimization below
    Space complexity: O(1)

    Examples:
        bubble_sort([5, 2, 8, 1, 9])  → [1, 2, 5, 8, 9]
    """
    n = len(lst)

    for i in range(n - 1):
        swapped = False

        # Each pass pushes the largest unsorted element to its place
        for j in range(n - 1 - i):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                swapped = True

        # Optimization: if no swaps occurred, the list is already sorted
        if not swapped:
            break

    return lst
```

**Trace for `[5, 2, 8, 1, 9]`:**
```
Pass 1: compare(5,2)→swap→[2,5,8,1,9]
        compare(5,8)→no swap
        compare(8,1)→swap→[2,5,1,8,9]
        compare(8,9)→no swap
        → [2,5,1,8,9]   (9 is now in final position)

Pass 2: compare(2,5)→no swap
        compare(5,1)→swap→[2,1,5,8,9]
        compare(5,8)→no swap
        → [2,1,5,8,9]   (8 now in final position)

Pass 3: compare(2,1)→swap→[1,2,5,8,9]
        compare(2,5)→no swap
        → [1,2,5,8,9]   (5 now in final position)

Pass 4: compare(1,2)→no swap
        No swaps → EARLY EXIT
Done: [1,2,5,8,9]
```

**The early-exit optimization is essential.** Without it, bubble sort always does n-1 passes, even on already-sorted data. With it, an already-sorted list is detected in a single pass: O(n).

---

## 4. Comparing the Three O(n²) Algorithms

| Algorithm | Worst Case | Best Case | Swaps | Stable? | In-place? |
|-----------|-----------|-----------|-------|---------|-----------|
| Selection sort | O(n²) | O(n²) | O(n) | No* | Yes |
| Insertion sort | O(n²) | O(n) | O(n²) | Yes | Yes |
| Bubble sort | O(n²) | O(n) | O(n²) | Yes | Yes |

*Selection sort is not stable by default — it can reorder equal elements. (A stable variant exists but is rarely used.)

**Stability** means: elements with equal keys retain their relative order after sorting. This matters when sorting records by one field but wanting to preserve order for ties (e.g., sorting students by grade, but keeping alphabetical order for students with the same grade — assuming the input was already alphabetical).

```python
# Demonstrating stability:
students = [("Bob", 85), ("Alice", 90), ("Carol", 85), ("Dave", 90)]
# Sort by grade only. A stable sort keeps Bob before Carol (both 85),
# and Alice before Dave (both 90), since that was their original order.
```

---

## 5. Why All Three Are O(n²): And Why That's Not Good Enough

For n = 1,000: n² = 1,000,000 operations — fast (milliseconds).
For n = 1,000,000: n² = 1,000,000,000,000 operations — roughly 15 minutes at a billion ops/sec.
For n = 1,000,000,000 (a billion records — a realistic database size): n² would take **decades**.

This is why O(n²) algorithms, despite being simple and correct, are **unusable at scale**. Friday's lecture introduces **merge sort** (which you partially built in Week 4) and its O(n log n) relatives, which handle a billion records in seconds.

**The asymptotic gap:**
```
n = 1,000,000:
    O(n²)      ≈ 10^12 operations  (way too slow)
    O(n log n) ≈ 2×10^7 operations (instant)
```

This is the difference between "wait a coffee break" and "wait 11 days" — for the *same* logical task, sorting the *same* data. This is why algorithm choice matters more than almost anything else in software performance.

---

## 6. Sorting Custom Objects: The `key` Parameter

Real sorting rarely sorts raw numbers — it sorts records by some attribute. Implementing this yourself teaches the underlying mechanism.

```python
def selection_sort_by_key(lst, key):
    """
    Selection sort that sorts by key(element) instead of element directly.

    Args:
        lst: list of any elements
        key: function extracting the comparison value from an element

    Examples:
        selection_sort_by_key(["hi","hello","a"], key=len)
            → ["a", "hi", "hello"]
    """
    n = len(lst)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if key(lst[j]) < key(lst[min_idx]):
                min_idx = j
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
    return lst


words = ["hello", "a", "world", "hi"]
selection_sort_by_key(words, key=len)
print(words)   # ['a', 'hi', 'hello', 'world']
```

Python's built-in `sorted()` and `list.sort()` both accept a `key` parameter that does exactly this, using a highly optimized O(n log n) algorithm underneath (covered Friday).

```python
students = [("Bob", 85), ("Alice", 90), ("Carol", 78)]
sorted_students = sorted(students, key=lambda s: s[1], reverse=True)
# [("Alice", 90), ("Bob", 85), ("Carol", 78)]
```

---

## 7. Counting Comparisons and Swaps: Empirical Verification

You can empirically verify the O(n²) behavior by counting operations directly:

```python
def selection_sort_counted(lst):
    """Selection sort that returns (sorted_list, comparisons, swaps)."""
    lst = lst[:]   # don't mutate the original
    n = len(lst)
    comparisons = 0
    swaps = 0

    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if lst[j] < lst[min_idx]:
                min_idx = j
        if min_idx != i:
            lst[i], lst[min_idx] = lst[min_idx], lst[i]
            swaps += 1

    return lst, comparisons, swaps


import random
for n in [10, 100, 1000]:
    data = [random.randint(0, 1000) for _ in range(n)]
    _, comparisons, swaps = selection_sort_counted(data)
    predicted = n * (n - 1) // 2
    print(f"n={n:5}: comparisons={comparisons:8} predicted={predicted:8} swaps={swaps}")
```

Running this confirms: comparisons always equal exactly n(n-1)/2, regardless of input order — selection sort's comparison count is **input-independent**, unlike insertion and bubble sort.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Selection sort | Find min, swap to front; O(n²) always; O(n) swaps |
| Insertion sort | Insert into sorted prefix; O(n²) worst, O(n) best (nearly-sorted data) |
| Bubble sort | Swap adjacent out-of-order pairs; O(n²) worst, O(n) best with early exit |
| Stability | Equal elements retain relative order — insertion and bubble are stable |
| O(n²) is too slow at scale | A billion records: hours to days vs. seconds for O(n log n) |
| `key` parameter | Sort by a derived value, not the raw element |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Instrument all three sorts to count comparisons on `[1,2,3,4,5]`, `[5,4,3,2,1]`, and `[3,1,4,1,5]`. Report the numbers and explain what the sorted-input row tells you.

**2. (Explain.)** Define sorting **stability** precisely, then predict both outputs and explain what the second one achieves.

```python
pairs = [("b", 1), ("a", 2), ("b", 0), ("a", 1)]
print(sorted(pairs, key=lambda p: p[0]))
print(sorted(sorted(pairs, key=lambda p: p[1]), key=lambda p: p[0]))
```

**3. (Build.)** Write insertion sort so it returns a new list without modifying its argument, and counts both comparisons and shifts. Then explain why counting *shifts* rather than *swaps* is the honest measure for this algorithm.

**4. (Stretch.)** All three sorts are Θ(n²), yet insertion sort is the one used inside real library sorts. Give two distinct properties that justify this, and name one input class on which insertion sort beats merge sort outright.


### Answers

**1.** | Input | Selection (comps) | Insertion (comps) |
|---|---|---|
| `[1,2,3,4,5]` sorted | 10 | **4** |
| `[5,4,3,2,1]` reversed | 10 | 10 |
| `[3,1,4,1,5]` random | 10 | 6 |

**Selection sort makes exactly 10 comparisons in every case** — and 10 = 5·4/2 = n(n−1)/2. It must scan the entire unsorted remainder to find the minimum, no matter what is in it, so its comparison count depends only on `n`. Its best case equals its worst case: Θ(n²) always.

**Insertion sort makes only 4 = n−1 comparisons on sorted input.** Each element is compared once with its predecessor, found to be in place, and left alone. This makes it **Θ(n) in the best case** and **adaptive**: its cost scales with how out of order the input already is (formally, with the number of inversions).

That adaptivity is why insertion sort is not merely a teaching example. Timsort — Python's actual sort — uses insertion sort on short runs and on nearly-sorted data precisely because of this row of the table. L18 §3 returns to it.

**2.** A sort is **stable** if elements comparing equal keep their original relative order.

First: `[('a', 2), ('a', 1), ('b', 1), ('b', 0)]`. The two `a`s appear as `('a', 2)` then `('a', 1)` — their order in the *input*, since the key ignores the second field. Python's `sorted` is guaranteed stable, so this is specified behaviour, not luck.

Second: `[('a', 1), ('a', 2), ('b', 0), ('b', 1)]`. This is a **multi-key sort by successive passes**: sort by the secondary key first, then by the primary key. Stability preserves the secondary ordering within each group of equal primary keys, so the result is sorted by letter, then by number within each letter.

The technique only works with a stable sort — with an unstable one the first pass would be destroyed. The alternative, `sorted(pairs, key=lambda p: (p[0], p[1]))`, does it in one pass with a tuple key and is usually clearer; the two-pass form earns its place when the keys sort in *opposite directions* and the values are not numbers you can negate.

Of the three elementary sorts, insertion and bubble are stable; **selection sort is not**, because its long-range swap can jump one equal element past another.

**3.**

```python
def insertion_sort(xs):
    a = list(xs)                 # do not mutate the caller's list
    comps = shifts = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if a[j] > key:
                a[j+1] = a[j]
                shifts += 1
                j -= 1
            else:
                break
        a[j+1] = key
    return a, comps, shifts
```

Insertion sort does not swap. It **holds one element aside** in `key`, slides the larger elements one position right, and drops the held element into the gap. Counting swaps would suggest three assignments per displaced element, when the algorithm actually performs one — a factor of three overstatement.

This is exactly why insertion sort beats bubble sort in practice despite both being Θ(n²) with the same comparison count: bubble sort really does swap, paying three moves for every inversion it fixes, while insertion sort pays one. Same asymptotic class, materially different constant.

The `break` matters too. Without it the inner loop would scan to the start of the array every time, destroying the Θ(n) best case that makes the algorithm adaptive at all.

**4.** **1. It is adaptive.** Its running time is Θ(n + d) where d is the number of inversions, so nearly sorted input costs nearly linear time. Merge sort does the same Θ(n log n) work regardless.

**2. Its constant factor is tiny.** It sorts **in place** (O(1) extra space, versus merge sort's O(n) buffer), accesses memory sequentially and locally — which is cache-friendly in a way merge sort's two read streams plus a write stream are not — and its inner loop is a comparison, a move, and a decrement. For small n, Θ(n²) with a small constant beats Θ(n log n) with a large one; the crossover in real implementations is typically somewhere between 10 and 64 elements.

It is also **stable** and **online** (it can sort a stream as elements arrive, which merge sort cannot).

The input class where it wins outright is **nearly sorted data** — say, an already-sorted log with a few late arrivals appended. Insertion sort finishes in close to Θ(n); merge sort still pays Θ(n log n).

Timsort exploits both properties at once: it scans for existing sorted runs, extends short ones with insertion sort, and merges the runs. On already-sorted input it is Θ(n), which you can measure — sorting a sorted list of 200,000 integers takes roughly an order of magnitude less time than sorting a shuffled one on the same machine.



---

## Reading

- **Guttag, Ch. 12.1–12.2** (or equivalent sorting chapter) — bubble sort, selection sort
- **CLRS, Ch. 2.1–2.2** — insertion sort with formal analysis (optional, recommended for the rigorous)

---

*CS 101 · Week 5 · Lecture 17 (Thu) · © CSE Department*
