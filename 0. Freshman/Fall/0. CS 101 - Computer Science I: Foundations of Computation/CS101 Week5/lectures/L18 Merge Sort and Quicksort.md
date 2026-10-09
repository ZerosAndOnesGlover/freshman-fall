# CS 101 · Lecture 18 (Week 5, Lecture 3)
## Efficient Sorting: Merge Sort, Quicksort, and the Sorting Landscape

**Week 5 · Friday**

*“Due credit must be paid to the genius of the designers of ALGOL 60 who included recursion in their language and enabled me to describe my invention [Quicksort] so elegantly to the world.”* — C. A. R. Hoare, "The Emperor's Old Clothes", Turing Award Lecture (1980)

**Date:** Friday 30 October 2026 · 09:00–09:50 · Week 5

**Reading:** CLRS, Ch. 2.3 · CLRS, Ch. 7 · Python docs, "Sorting Techniques" HOWTO *(details at the end of the lecture)*

**Coursework:** 📝 **PS 4** due today 17:00 · 📝 **PS 5** released today 10:00, due Fri 6 Nov 17:00 · 📘 **Midterm 1** Mon 2 Nov 18:00–19:15 · 🔬 **Lab 5** Tue 3 Nov 15:00–16:50 · 📊 **Quiz 6** Wed 4 Nov 09:00–09:10

---

## 0. From O(n²) to O(n log n)

Thursday's three algorithms share a common bottleneck: they solve the problem by repeatedly examining pairs of elements in a way that scales `quadratically`. Today we study algorithms that exploit **divide-and-conquer** (which you learned in Week 4) to break this barrier.

---

## 1. Merge Sort: Full Review and Formal Analysis

You built merge sort in Week 4 as a recursion exercise. Now we analyze it rigorously as a sorting algorithm.

```python
def merge_sort(lst):
    """
    Sort lst using merge sort. Returns a NEW sorted list (not in place).

    Time complexity:  O(n log n) — ALL cases (best, worst, average)
    Space complexity: O(n) — auxiliary arrays for merging
    Stable:            Yes
    In-place:          No

    Divide: split the list into two halves.
    Conquer: recursively sort each half.
    Combine: merge the two sorted halves.
    """
    if len(lst) <= 1:
        return lst[:]

    mid   = len(lst) // 2
    left  = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])
    return merge(left, right)


def merge(left, right):
    """Merge two sorted lists into one sorted list. O(len(left)+len(right))."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:    # <= (not <) ensures stability
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Why `<=` and not `<` in the merge step?** When `left[i] == right[j]`, taking from `left` first preserves the original relative order of equal elements (since `left` came from an earlier position in the original array). This is precisely what makes merge sort **stable**.

### The Master Theorem: Formal Complexity Derivation

Merge sort's recurrence: `T(n) = 2·T(n/2) + O(n)`

- `2·T(n/2)`: two recursive calls, each on half the input
- `O(n)`: the cost of merging two sorted halves of total size n

**Solving the recurrence** (via recursion tree):

```
Level 0:  T(n)                          → work: O(n)
Level 1:  2 × T(n/2)                    → work: O(n)
Level 2:  4 × T(n/4)                    → work: O(n)
...
Level k:  2^k × T(n/2^k)                → work: O(n)
...
Level log₂n: n × T(1)                   → work: O(n)
```

Every level does O(n) total work (merging touches every element once per level). There are log₂n + 1 levels. Total: **O(n log n)**.

This is the **Master Theorem** in action — you'll formalize it fully in CS 102 (Algorithms II), but the recursion-tree argument above is a complete, rigorous derivation.

---

## 2. Quicksort: Partition-Based Sorting

Quicksort, invented by Tony Hoare in 1959, is (on average) the fastest general-purpose comparison sort in practice, despite having a worse worst-case complexity than merge sort.

**Idea:** Pick a **pivot** element. Partition the list into elements less than the pivot and elements greater than the pivot. Recursively sort each partition.

```python
def quicksort(lst):
    """
    Sort lst using quicksort. Returns a NEW sorted list.

    Time complexity:
        Average case: O(n log n)
        Worst case:   O(n²)  — occurs with poor pivot choices (e.g., already-sorted
                       data with a naive "always pick first element" strategy)
    Space complexity: O(log n) average (recursion stack), O(n) worst case
    Stable:            No (in this simple implementation)
    In-place:          No (this version) — in-place versions exist and are standard

    Divide: partition around a pivot.
    Conquer: recursively sort each partition.
    Combine: NONE needed — concatenation is trivial once partitions are sorted.
    """
    if len(lst) <= 1:
        return lst[:]

    pivot = lst[len(lst) // 2]     # choosing the middle element helps avoid worst case
    less    = [x for x in lst if x <  pivot]
    equal   = [x for x in lst if x == pivot]
    greater = [x for x in lst if x >  pivot]

    return quicksort(less) + equal + quicksort(greater)
```

**Trace for `[5, 2, 8, 1, 9, 3]`, pivot = middle element = 8:**
```
less = [5, 2, 1, 3]   (< 8)
equal = [8]
greater = [9]   (> 8)

quicksort([5,2,1,3]), pivot=1:
    less=[]  equal=[1]  greater=[5,2,3]
    quicksort([5,2,3]), pivot=2:
        less=[]  equal=[2]  greater=[5,3]
        quicksort([5,3]), pivot=3:
            less=[]  equal=[3]  greater=[5]
            → [3,5]
        → [2,3,5]
    → [1,2,3,5]
quicksort([9]) → [9]

Final: [1,2,3,5] + [8] + [9] = [1,2,3,5,8,9]
```

### Why Quicksort's Worst Case Is O(n²)

If the pivot is always the **smallest or largest** element (e.g., choosing the first element on already-sorted data), one partition is empty and the other has n-1 elements. This degenerates the recursion to:

```
T(n) = T(n-1) + T(0) + O(n) = T(n-1) + O(n)
```

Solving: T(n) = O(n) + O(n-1) + ... + O(1) = **O(n²)**.

**Mitigation strategies** (used in real implementations):
- **Random pivot selection** — makes worst case exponentially unlikely
- **Median-of-three** — pick the median of first, middle, last elements as pivot
- **Introsort** — switch to heapsort if recursion depth exceeds a threshold (used by C++'s `std::sort`)

### Why Quicksort Is Usually Faster Than Merge Sort in Practice

Despite the same average-case complexity O(n log n), quicksort typically **outperforms** merge sort on real hardware because:
1. It sorts **in-place** (standard implementations) — merge sort requires O(n) auxiliary space
2. It has better **cache locality** — partitioning works on contiguous memory
3. Its constant factors are smaller in practice

This is why quicksort (or hybrid variants) is the default in many language standard libraries — though not Python's, as we'll see next.

---

## 3. Python's Built-in Sort: Timsort

Python's `sorted()` and `list.sort()` use **`Timsort`**, invented by Tim Peters in 2002 specifically for Python (and later adopted by Java, Android, and `V8`/JavaScript).

**`Timsort`'s key insight:** real-world data often contains long runs of already-sorted (or reverse-sorted) subsequences. `Timsort`:
1. Identifies these natural "runs" in the data
2. Extends short runs using insertion sort (which is O(n) on nearly-sorted data — recall Thursday!)
3. Merges runs together using a merge-sort-like strategy, carefully choosing merge order to maintain efficiency

**Complexity:**
- Worst case: O(n log n): same guarantee as merge sort
- Best case: O(n): for already-sorted or reverse-sorted data
- Stable: Yes

```python
# Python's built-in sort — always prefer this in real code:
data = [5, 2, 8, 1, 9, 3]
sorted_data = sorted(data)          # returns a new list
data.sort()                          # sorts in place

# With a key function:
words = ["hello", "a", "world", "hi"]
sorted_by_length = sorted(words, key=len)

# Reverse order:
sorted_desc = sorted(data, reverse=True)

# Sorting complex objects:
students = [("Bob", 85), ("Alice", 90), ("Carol", 78)]
by_grade_desc = sorted(students, key=lambda s: s[1], reverse=True)
```

**The practical lesson:** you implement sorting algorithms in this course to understand *how* and *why* they work — but in production Python code, you should almost always use the built-in `sorted()`/`list.sort()`. They are implemented in C, extensively optimized, stable, and correctly handle edge cases you might miss.

---

## 4. The Complete Sorting Landscape

| Algorithm | Best | Average | Worst | Space | Stable | In-place |
|-----------|------|---------|-------|-------|--------|----------|
| Selection sort | O(n²) | O(n²) | O(n²) | O(1) | No | Yes |
| Insertion sort | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes |
| Bubble sort | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes |
| Merge sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | No |
| Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) | No | Yes |
| Timsort (Python) | O(n) | O(n log n) | O(n log n) | O(n) | Yes | No* |

*Timsort uses O(n) auxiliary space but is often described as "nearly in-place" due to its clever merging strategy.

---

## 5. The Fundamental Lower Bound: Why O(n log n) Is Optimal

**Claim:** Any comparison-based sorting algorithm requires Ω(n log n) comparisons in the worst case. No comparison sort can do better.

> **Scoped preview — where the proof's two borrowed facts come from.** The sketch below *states*
> both, but neither is taught in Year 1, so here is the justification.
>
> **`n!` orderings.** Pick any of `n` items first, then any of the remaining `n−1`, then `n−2`:
> `n × (n−1) × … × 1 = n!`. That is a **permutation count**; MATH 151 develops permutations
> properly in **Week 7**, two weeks after you need it here.
>
> **`log₂(n!) = Θ(n log n)`.** The sketch attributes this to **Stirling's approximation**, taught
> in **neither** MATH 151 nor MATH 141 at any point this year. You do not need it: at least half
> the factors of `n!` are ≥ `n/2`, so `n! ≥ (n/2)^(n/2)` and therefore
> `log₂(n!) ≥ (n/2)·log₂(n/2)`, which is already `Ω(n log n)` — enough to finish the proof.

**Proof sketch (decision tree argument):**
- Any comparison-based sort can be modeled as a binary decision tree: each internal node is a comparison, each leaf is a final sorted arrangement.
- There are n! possible orderings of n elements — the tree must have at least n! leaves.
- A binary tree with L leaves has depth at least log₂L.
- Therefore, the tree has depth at least log₂(n!) ≈ n log₂n - n log₂e (by Stirling's approximation).
- The depth of the tree is the worst-case number of comparisons.
- Therefore, any comparison sort requires **Ω(n log n)** comparisons in the worst case.

This is a beautiful result: it proves that merge sort, quicksort (average case), and Timsort are not just *good* — they are **asymptotically optimal**. No cleverness can produce a general-purpose comparison sort faster than O(n log n).

**The loophole — non-comparison sorts:** if you know more about your data (e.g., it's all integers in a bounded range), you can sort in O(n) using **counting sort** or **radix sort** — these don't use comparisons, so the lower bound doesn't apply. We'll study these in CS 102.

---

## 6. Choosing the Right Sort: A Decision Framework

```
Is the data nearly sorted, or small (n < ~50)?
    → Insertion sort (simple, fast in this case)

Do you need a stable sort with guaranteed O(n log n)?
    → Merge sort, or just use sorted()/list.sort() (Timsort)

Do you need in-place sorting and average-case speed matters most?
    → Quicksort (with randomized pivot)

Is your data integers in a small known range?
    → Counting sort / radix sort (O(n), beats the comparison lower bound)

Are you writing production Python code?
    → ALWAYS use sorted() or list.sort(). Do not hand-roll a sort.
```

---

## 7. A Complete Worked Example: Sorting Students by Multiple Criteria

```python
students = [
    {"name": "Alice",   "grade": 90, "age": 20},
    {"name": "Bob",     "grade": 85, "age": 22},
    {"name": "Charlie", "grade": 90, "age": 19},
    {"name": "Dave",    "grade": 85, "age": 21},
]

# Sort by grade descending, then by age ascending (for ties):
# Python's sort is STABLE, so we can sort by the secondary key first,
# then by the primary key — the secondary order is preserved for ties.

# Method 1: tuple key (cleanest)
result = sorted(students, key=lambda s: (-s["grade"], s["age"]))

# Method 2: two stable sorts (exploits stability explicitly)
result2 = sorted(students, key=lambda s: s["age"])               # secondary sort first
result2 = sorted(result2, key=lambda s: s["grade"], reverse=True) # primary sort second

for s in result:
    print(f"{s['name']:10} grade={s['grade']} age={s['age']}")

# Tracing the tuple key for the two students on 90:
# (-90, 20) and (-90, 19): the first components tie, so compare 20 vs 19 → 19 comes first
# Charlie (90, 19), Alice (90, 20), Bob (85, 22), Dave (85, 21)
```

This demonstrates that **stability is not just a theoretical property** — it directly enables a practical, elegant technique for multi-key sorting: sort by the least significant key first, then progressively by more significant keys, relying on stability to preserve the ordering of previous passes.

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Merge sort recurrence | T(n) = 2T(n/2) + O(n) → O(n log n) via recursion tree |
| Quicksort | Partition around pivot; O(n log n) average, O(n²) worst case |
| Pivot selection | Random or median-of-three avoids worst-case degradation |
| Timsort | Python's real sort; exploits natural runs; O(n) best case |
| Comparison sort lower bound | Ω(n log n) — provably optimal; decision tree argument |
| Non-comparison sorts | Counting/radix sort can beat O(n log n) for special data |
| Stability enables multi-key sort | Sort by least significant key first, then most significant |
| Production advice | Always use `sorted()`/`.sort()` — never hand-roll in real code |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Trace one Lomuto partition on `[3, 7, 8, 5, 2, 1, 9, 5]` with the last element as pivot. Give the array after partitioning and the returned pivot index.

```python
def partition(a, lo, hi):
    pivot = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i+1], a[hi] = a[hi], a[i+1]
    return i + 1
```

**2. (Explain.)** Quicksort is Θ(n log n) on average but Θ(n²) in the worst case. State the worst-case input for the "always pick the last element" pivot rule, explain why it is quadratic, and give two ways real implementations avoid it.

**3. (Build.)** Sort these records by score descending, then by name ascending, using a single `key`. Explain why the negation trick works here and when it does not.

```python
recs = [("bob", 3, 90), ("amy", 3, 90), ("cy", 1, 70)]
```

**4. (Stretch.)** §5 states that Ω(n log n) is a lower bound for comparison sorts. Sketch the decision-tree argument, then explain how counting sort achieves O(n) without contradicting it.


### Answers

**1.** Result: **`[3, 5, 2, 1, 5, 7, 9, 8]`**, returned index **4**, and `a[4]` is the pivot `5`. ✓

The invariant is what makes this readable: at the top of each `j` iteration, `a[lo..i]` holds everything seen so far that is **≤ pivot**, and `a[i+1..j-1]` holds everything **> pivot**. When `a[j] <= pivot`, `i` advances and the element is swapped into the small region, pushing one large element rightward. When `a[j] > pivot`, nothing moves — it is already in the right region.

The final swap places the pivot at `i+1`, exactly between the two regions, which is why the pivot is then in its **permanent sorted position** and never needs to be examined again.

Note the duplicate `5`: with `<=`, the earlier `5` lands left of the pivot. Using `<` would send equal elements right instead — and on an array of all-equal elements would produce maximally unbalanced partitions, an O(n²) blowup on an input that looks trivially easy. Handling of equal keys is not a detail in quicksort.

**2.** The worst case for last-element pivoting is an **already sorted (or reverse sorted) array** — which is precisely the input most likely to occur in practice, and what makes the naive rule dangerous rather than merely theoretical.

On sorted input the pivot is always the largest remaining element, so partitioning splits `n` elements into `n−1` and `0`. The recurrence becomes T(n) = T(n−1) + Θ(n), which unrolls to n + (n−1) + … + 1 = **Θ(n²)**. The recursion depth also becomes n, risking stack overflow. Compare a balanced split, which gives T(n) = 2T(n/2) + Θ(n) = Θ(n log n) — the depth is what changes, from log n to n.

Two standard defences:

1. **Randomised pivot** — choose uniformly at random from `[lo, hi]`. No fixed input is bad any more; the expected time is Θ(n log n) for *every* input, and an adversary who knows your code still cannot construct a slow case. This is the theoretically cleanest fix.
2. **Median-of-three** — take the median of `a[lo]`, `a[mid]`, `a[hi]`. Cheap, deterministic, and makes the sorted case optimal rather than worst. It can still be defeated by a crafted input, which is why production sorts (introsort, used by C++ `std::sort`) add a third layer: **track the recursion depth and switch to heapsort** past ~2 log n, guaranteeing Θ(n log n) unconditionally.

**3.**

```python
sorted(recs, key=lambda r: (-r[2], r[0]))
# [('amy', 3, 90), ('bob', 3, 90), ('cy', 1, 70)]
```

Tuple keys compare **lexicographically**: the first components are compared, and only on a tie does comparison move to the second. So `(-score, name)` sorts by descending score, then by ascending name within each score — `amy` before `bob`, both before `cy`.

Negating works because the key is **numeric**, and reversing the sign of a number reverses its order. It does **not** work for strings — there is no `-"amy"` — nor for dates, tuples, or any non-numeric key. For mixed directions on non-numeric keys, use the two-pass technique from L17, relying on stability:

```python
recs2 = sorted(recs, key=lambda r: r[0])                # secondary, ascending
recs2 = sorted(recs2, key=lambda r: r[2], reverse=True)  # primary, descending
```

One caution: `reverse=True` does not reverse the stability behaviour — it keeps equal elements in their original order rather than flipping them — which is exactly what makes the two-pass idiom correct. Also note negation fails for floats at one point: `-0.0` and `0.0` compare equal, so no ordering is disturbed, but if the key can be `NaN`, all bets are off in either approach.

**4.** **The argument.** A comparison sort's execution is a path down a binary decision tree: each internal node is one comparison with two outcomes, and each leaf is one specific permutation the algorithm might output. To sort correctly, the tree must have a leaf for **every** one of the n! possible input orderings — otherwise two distinct inputs would follow the same path and receive the same output, and one would be wrong.

A binary tree with L leaves has height at least log₂ L. So the height — the worst-case number of comparisons — is at least log₂(n!). By Stirling's approximation, log₂(n!) = Θ(n log n). Hence **Ω(n log n)**, for every comparison sort, forever.

**Why counting sort escapes.** It is not a comparison sort. It never asks "is a < b?"; it uses each key's *value* directly as an index into a tally array. That operation is outside the model the theorem quantifies over, so the bound does not apply.

The escape is not free. Counting sort is O(n + k) for keys in a range of size k, so it is linear only when k is O(n) — sorting 1,000 integers spread over the full 64-bit range would need a table of 2⁶⁴ entries. It also requires keys that *are* small integers, or that map to them, whereas comparison sorts need only a working `<`. Radix sort extends the idea to larger keys by processing digits, at O(d(n + b)) for d digits in base b.

This is the general shape of beating a lower bound: you never break the theorem, you leave its model.



---

## Reading

- **CLRS, Ch. 2.3** — Merge sort with formal recurrence analysis
- **CLRS, Ch. 7** — Quicksort (optional — deeper than needed for CS 101, but excellent)
- **Python docs, "Sorting Techniques" HOWTO** — https://docs.python.org/3/howto/sorting.html

---

*CS 101 · Week 5 · Lecture 18 (Fri) · © CSE Department*
