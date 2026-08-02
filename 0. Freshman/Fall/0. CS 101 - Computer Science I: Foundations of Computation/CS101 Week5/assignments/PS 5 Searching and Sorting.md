# CS 101 — Problem Set 5
## Searching and Sorting Algorithms

**Released:** Friday, Week 5
**Due:** Friday, Week 6 at 11:59 PM
**Submission:** Upload `ps5.py` and `PS 5 Searching and Sorting.md`
**Weight:** Part of the 30% Problem Sets grade

**Note:** Midterm 1 is next week (Week 6, covers Weeks 0–5). This problem set doubles as review — work through it carefully.

---

## Overview

This problem set covers:
- Linear and binary search, including variants (bisect_left, first occurrence)
- Binary search on the answer (searching a monotonic predicate)
- Selection, insertion, and bubble sort with correctness arguments
- Merge sort and quicksort, including stability analysis
- Empirical complexity measurement and interpretation
- Choosing the right algorithm for a given situation

**Every algorithm implementation must have:**
- A complete docstring with time/space complexity
- A correctness argument (loop invariant or inductive proof)
- At least 3 `assert` tests including edge cases (empty list, single element, duplicates)

---

## Part A: Written Questions (`PS 5 Searching and Sorting.md`)

### A1: Binary Search Correctness (8 points)

Consider this binary search variant:

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

**(a)** This implementation has a bug related to the boundary update. Identify it precisely (which line, and why it's wrong).

**(b)** Construct a specific input (a list and a target) that triggers an infinite loop (or `RecursionError`) due to this bug.

**(c)** Write the corrected version.

**(d)** State the loop invariant for the corrected version.

---

### A2: Algorithm Selection (8 points)

For each scenario, choose the best algorithm (from: linear search, binary search, selection sort, insertion sort, bubble sort, merge sort, quicksort, Python's built-in `sorted()`) and justify your choice in 1-2 sentences.

**(a)** You have a list of 50 million customer records that must be sorted by customer ID exactly once, then never modified again.

**(b)** You have a list of ~20 elements that is updated frequently (a few insertions per second) and must remain sorted after each insertion.

**(c)** You need to find whether a specific value exists in an unsorted list of 30 items, and you will only do this search once.

**(d)** You need to repeatedly check membership in a large sorted list of one million values, performing thousands of queries per second.

---

### A3: Complexity Analysis (8 points)

**(a)** A student claims: "Insertion sort is always faster than merge sort because merge sort has O(n log n) overhead even for tiny inputs." Evaluate this claim. Is it ever true? Under what specific circumstances?

**(b)** Given the recurrence T(n) = 2T(n/2) + n, solve it using the recursion-tree method (show the tree, the work per level, and the total).

**(c)** A sorting algorithm has the recurrence T(n) = T(n-1) + n (one recursive call on a slightly smaller problem, plus O(n) work). Solve this recurrence. What does this pattern resemble from an algorithm you've seen this week?

**(d)** Explain, in your own words, why the decision-tree argument proves that Ω(n log n) comparisons are necessary for ANY comparison-based sort — even one that hasn't been invented yet.

---

### A4: Stability (4 points)

**(a)** Give a concrete example (with actual data) showing why stability matters when sorting a list of `(last_name, first_name)` tuples by `last_name` only, when the input was previously sorted by `first_name`.

**(b)** Is the following sort stable? Justify your answer by tracing through a small example with duplicate keys.

```python
def mystery_sort(lst):
    if len(lst) <= 1:
        return lst[:]
    pivot = lst[0]
    less  = [x for x in lst[1:] if x < pivot]
    equal = [x for x in lst if x == pivot]
    greater = [x for x in lst[1:] if x > pivot]
    return mystery_sort(less) + equal + mystery_sort(greater)
```

---

## Part B: Python Implementation (`ps5.py`)

### B1: Search Variants (12 points)

**(a)** `find_first_and_last(lst, target)` — for a sorted list with duplicates, return `(first_index, last_index)` of target's occurrences, or `(-1, -1)` if not found. Must run in O(log n).
- `find_first_and_last([1,2,2,2,3,4], 2)` → `(1, 3)`
- `find_first_and_last([1,2,3], 5)` → `(-1, -1)`

**(b)** `count_occurrences(lst, target)` — count occurrences of target in a sorted list. Use `find_first_and_last`. O(log n).
- `count_occurrences([1,2,2,2,3,4], 2)` → `3`

**(c)** `search_rotated(lst, target)` — search for target in a rotated sorted list (e.g., `[4,5,6,7,1,2,3]`) in O(log n), without first "un-rotating" it.
- `search_rotated([4,5,6,7,1,2,3], 5)` → `1`
- `search_rotated([4,5,6,7,1,2,3], 8)` → `-1`

**(d)** `find_peak(lst)` — a "peak" is an element greater than both neighbors (or greater than its only neighbor at the boundary). Find any one peak's index in O(log n) using binary search on the direction of the slope.
- `find_peak([1,3,5,4,2])` → `2` (value 5, greater than neighbors)
- Multiple peaks may exist; any valid index is acceptable.

**(e)** `sqrt_floor(n)` — return floor(sqrt(n)) for non-negative integer n, using binary search on the answer (not `math.sqrt` or `**0.5`).
- `sqrt_floor(17)` → `4` (since 4²=16≤17<25=5²)
- `sqrt_floor(16)` → `4`
- `sqrt_floor(0)` → `0`

---

### B2: Custom Sorting Implementations (14 points)

Implement each with full docstrings and correctness arguments. Each function must return a **new** sorted list (not mutate the input), unless stated otherwise.

**(a)** `insertion_sort_by_key(lst, key)` — insertion sort that sorts by `key(element)`.
- `insertion_sort_by_key(["hi","a","world"], key=len)` → `["a","hi","world"]`

**(b)** `cocktail_sort(lst)` — bidirectional bubble sort: alternately sweep left-to-right and right-to-left, shrinking the unsorted region from both ends each pass.
- Time: O(n²) worst case, but converges faster than bubble sort for certain patterns (e.g., a few small elements near the end).

**(c)** `merge_k_sorted(lists)` — merge k already-sorted lists into one sorted list.
- `merge_k_sorted([[1,4,7],[2,5,8],[3,6,9]])` → `[1,2,3,4,5,6,7,8,9]`
- Implement using repeated pairwise merging (merge lists[0] with lists[1], then with lists[2], etc.) — analyze why this is O(nk) rather than optimal O(n log k), where n is total elements and k is number of lists.

**(d)** `quicksort_random_pivot(lst)` — quicksort using a **randomly chosen** pivot instead of the middle element.
- Verify empirically (in your test code) that this avoids the O(n²) worst case on already-sorted input, by running it on `list(range(2000))` and confirming it completes quickly.

**(e)** `top_k(lst, k)` — return the k largest elements from lst, in descending order, WITHOUT fully sorting the list. Aim for better than O(n log n) if possible (partial selection sort or a heap-based approach are both acceptable — describe your approach's complexity in the docstring).
- `top_k([5,2,8,1,9,3], 3)` → `[9,8,5]`

---

### B3: Empirical Analysis (10 points)

**(a)** Write `measure_growth(sort_func, sizes)` that times `sort_func` on random lists of each size in `sizes`, and returns a list of `(size, time)` tuples.

**(b)** Write `estimate_complexity_class(measurements)` that takes the output of `measure_growth` and estimates whether the algorithm's growth is closer to O(n), O(n log n), or O(n²), by computing the ratio of times between consecutive size doublings and comparing against theoretical predictions:
- O(n): doubling n → time roughly doubles (ratio ≈ 2)
- O(n log n): doubling n → time increases by a bit more than 2x (ratio ≈ 2 to 2.5 for reasonable n)
- O(n²): doubling n → time roughly quadruples (ratio ≈ 4)

Return the estimated complexity class as a string.

**(c)** Run `estimate_complexity_class` on `selection_sort`, `merge_sort`, and Python's `sorted()`. Print a report showing the sizes, times, ratios, and estimated class for each. Include this report's output in your written submission.

---

### B4: Real-World Application — Event Scheduling (14 points)

You are given a list of events, each with a start time and end time (as integers representing minutes). Implement a scheduler that finds the maximum number of non-overlapping events that can be attended (the classic "activity selection problem").

```python
events = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 8), (5, 9), (6, 10), (8, 11), (8, 12), (2, 13), (12, 14)]
```

**(a)** `sort_by_end_time(events)` — sort events by end time using merge sort (call your Week 5 implementation, don't use built-in `sorted`). Return the sorted list.

**(b)** `max_non_overlapping(events)` — using the greedy algorithm (sort by end time, then greedily select each event that doesn't overlap the previously selected one), return the maximum set of non-overlapping events.
- For the events above: expected result has 4 events (e.g., (1,4), (5,7), (8,11) or (8,12), (12,14) — verify the exact count is 4)

**(c)** `binary_search_next_event(sorted_events, current_end_time)` — given events sorted by start time, use binary search to find the index of the first event whose start time is >= `current_end_time`. This is useful for an O(n log n) version of the scheduling algorithm (rather than a linear scan).

**(d)** Write a short paragraph (in `PS 5 Searching and Sorting.md`) explaining why sorting by end time (not start time) is the correct greedy strategy for this problem, and give a counterexample showing that sorting by start time can produce a suboptimal answer.

---

## Grading Rubric

| Problem | Points | Key Criteria |
|---------|--------|--------------|
| A1 Binary search bug | 8 | Correct bug identification, infinite loop example, correct fix, invariant |
| A2 Algorithm selection | 8 | Correct choice + valid justification for all 4 |
| A3 Complexity analysis | 8 | Correct recurrence solutions, valid decision-tree explanation |
| A4 Stability | 4 | Correct example, correct stability determination with trace |
| B1 Search variants | 12 | All 5 correct, correct complexity |
| B2 Custom sorting | 14 | All 5 correct, correctness arguments present |
| B3 Empirical analysis | 10 | Correct measurement, sensible complexity estimation, clear report |
| B4 Event scheduling | 14 | All 4 correct, correct greedy proof/counterexample |
| **Total** | **78** | |
| Docstring/proof quality | up to 5 bonus | |

---

## Part C: Challenge Problems (Ungraded)

**C1: Median of Two Sorted Arrays**
Given two sorted arrays of sizes m and n, find the median of the combined array in O(log(min(m,n))) time — without merging them. This is a classic hard interview problem; research the binary-search-based approach.

**C2: External Sort**
Design (in pseudocode, not full implementation) an algorithm to sort a file containing 100 GB of integers using only 1 GB of RAM. This is called "external sorting" and is the foundation of how databases sort data larger than memory. Hint: think about merge sort's merge step, applied across disk-based chunks.

**C3: Radix Sort**
Implement `radix_sort(lst)` for non-negative integers, sorting by digit from least significant to most significant using a stable sort (like counting sort) as a subroutine at each digit position. This achieves O(d·n) time where d is the number of digits — beating the comparison sort lower bound for suitable data.

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading Rubric above (78 points).
> No errata found in this problem set — all stated example values verified correct.

---

### Part A — Written (28 points)

**A1 Binary Search Correctness (8 pts).**

**(a)** The bug is on the `lst[mid] < target` branch: `return binary_search_v2(lst, target, mid, hi)`. It passes **`mid`**, not `mid + 1`. Since `mid = (lo + hi) // 2` floors, when `hi == lo + 1` we get `mid == lo`, so the recursive call receives the *identical* `(lo, hi)` pair and the interval never shrinks. The `else` branch is fine — passing `mid` as the new `hi` does strictly shrink, because `mid < hi` always.

**(b)** Verified counterexamples — each recurses forever:

| List | Target | Why |
|---|---|---|
| `[1, 3]` | `2` | `(0,2)`→mid 1, `3>2`→`(0,1)`→mid 0, `1<2`→`(0,1)` — stuck |
| `[1, 2, 3]` | `4` | narrows to `(2,3)`→mid 2, `3<4`→`(2,3)` — stuck |
| `[1, 3, 5]` | `4` | narrows to `(1,2)`→mid 1, `3<4`→`(1,2)` — stuck |

Note the target need not be absent in general, but in all three above it is — the failure is reaching a width-1 window whose single element is *less than* the target.

**(c)**

```python
def binary_search_v2(lst, target, lo, hi):
    if lo >= hi: return -1
    mid = (lo + hi) // 2
    if lst[mid] == target:  return mid
    elif lst[mid] < target: return binary_search_v2(lst, target, mid + 1, hi)   # FIX
    else:                   return binary_search_v2(lst, target, lo, mid)
```

**(d)** Invariant: *if `target` occurs anywhere in the original list, its index lies in `[lo, hi)`.* Initialization holds with `lo=0, hi=len(lst)`. Each branch preserves it (everything at or below `mid` is `< target`, or everything at or above `mid` is `> target`). At exit `lo >= hi` means the window is empty, so `target` is absent — hence `-1` is correct.

*Grading: 3 pts (a) — must name the line **and** explain why flooring makes it stick. 2 pts (b) — the example must actually loop; verify it. 2 pts (c). 1 pt (d).*
*Common error: "the bug is using `//` instead of `/`". That is wrong — integer division is required; the defect is the missing `+1`.*

**A2 Algorithm Selection (8 pts).** 2 pts each — grade the justification, not the label.
- **(a) Merge sort (or built-in `sorted()`).** Sorted once, never re-sorted, and 50M records means a guaranteed O(n log n) matters; merge sort's predictable worst case (and natural fit for external/on-disk sorting at this scale) beats quicksort's O(n²) tail risk.
- **(b) Insertion sort.** For n ≈ 20 already-nearly-sorted data, insertion sort is O(n) per insertion in practice and has minimal constant overhead. Re-running an O(n log n) sort after every insertion is wasted work.
- **(c) Linear search.** The list is *unsorted* and queried *once* — sorting first would cost O(n log n) to enable an O(log n) query, which is strictly worse than one O(n) scan.
- **(d) Binary search.** Already sorted, many queries: pay nothing extra and get O(log n) per query. (A hash set is even faster at O(1), but the question restricts to the listed options — mention as bonus.)

**A3 Complexity Analysis (8 pts).** 2 pts each.

**(a)** The claim is **partially true**. Insertion sort beats merge sort on *small* inputs (typically n ≲ 10–50) because its constant factors are tiny and it has no allocation/recursion overhead; it is also O(n) on nearly-sorted input, beating merge sort's Θ(n log n) *best* case. But "always faster" is false — asymptotics dominate as n grows. This is precisely why real hybrid sorts (Timsort, introsort) switch to insertion sort below a threshold.

**(b)** `T(n) = 2T(n/2) + n` by recursion tree: level `i` has `2ⁱ` nodes each doing `n/2ⁱ` work, so **every level does exactly `n` work**. Depth is `log₂ n`. Total = `n · log₂ n` → **Θ(n log n)**.

**(c)** `T(n) = T(n−1) + n` unrolls to `n + (n−1) + (n−2) + … + 1 = n(n+1)/2` → **Θ(n²)**. This is the shape of **selection sort / insertion sort worst case** — one element placed per pass, with a linear scan each time.

**(d)** Any comparison sort is a decision tree: internal nodes are comparisons, each with 2 outcomes; leaves are the possible output permutations. There are `n!` permutations, so the tree needs ≥ `n!` leaves. A binary tree of height `h` has ≤ `2^h` leaves, so `2^h ≥ n!` → `h ≥ log₂(n!)`. By Stirling, `log₂(n!) = Θ(n log n)`. Height = worst-case comparisons, so **every** comparison-based sort needs Ω(n log n) comparisons — the argument constrains the *model*, not any particular algorithm, which is why it covers algorithms not yet invented. (It does **not** apply to counting/radix sort, which don't compare elements.)

**A4 Stability (4 pts).**

**(a)** Input previously sorted by first name: `[("Smith","Ann"), ("Jones","Bob"), ("Smith","Carl")]`. Sorting by **last name only**: a *stable* sort gives `[("Jones","Bob"), ("Smith","Ann"), ("Smith","Carl")]` — the two Smiths remain in first-name order, so the data is now sorted by last-then-first "for free". An unstable sort may emit `Carl` before `Ann`, destroying the earlier ordering. This is how multi-key sorting is built: sort by the least significant key first, then stably by the more significant one.

**(b)** **Yes, `mystery_sort` is stable.** Traced with tagged equal keys `[2a, 1x, 2b, 1y, 2c]` (subscripts mark original position):

- pivot `= 2a`. `less = [1x, 1y]` (scanned from `lst[1:]`, order preserved), `equal = [2a, 2b, 2c]` (scanned across the **whole** list, so original order preserved), `greater = []`.
- Recursing on `less` yields `[1x, 1y]`.
- Result: **`[1x, 1y, 2a, 2b, 2c]`** — every group of equal keys retains its input order.

Stability holds because all three sublists are built by list comprehensions that traverse left-to-right, and `equal` scans the original list rather than reordering. (Caveat worth noting for bonus: it is *not* in-place — it allocates O(n) per level, unlike a classic Lomuto/Hoare quicksort, which **is** unstable.)

*Grading: 2 pts (a) with concrete data showing the difference. 2 pts (b) — the answer "stable" alone earns 1; the trace with duplicate keys is required for the second point.*

---

### Part B — Coding (50 points)

**B1 Search Variants (12 pts).** All verified.

```python
def find_first_and_last(lst, target):
    def bound(left):                       # left=True -> first index; else one past last
        lo, hi = 0, len(lst)
        while lo < hi:
            m = (lo + hi) // 2
            if lst[m] < target or (not left and lst[m] == target): lo = m + 1
            else: hi = m
        return lo
    first = bound(True)
    if first == len(lst) or lst[first] != target: return (-1, -1)
    return (first, bound(False) - 1)

def search_rotated(lst, target):
    lo, hi = 0, len(lst) - 1
    while lo <= hi:
        m = (lo + hi) // 2
        if lst[m] == target: return m
        if lst[lo] <= lst[m]:                       # left half is sorted
            if lst[lo] <= target < lst[m]: hi = m - 1
            else: lo = m + 1
        else:                                        # right half is sorted
            if lst[m] < target <= lst[hi]: lo = m + 1
            else: hi = m - 1
    return -1

def find_peak(lst):
    lo, hi = 0, len(lst) - 1
    while lo < hi:
        m = (lo + hi) // 2
        if lst[m] < lst[m + 1]: lo = m + 1            # ascending -> peak is right
        else: hi = m                                  # descending -> peak is at or left
    return lo

def sqrt_floor(n):
    if n < 2: return n
    lo, hi, ans = 1, n, 1
    while lo <= hi:
        m = (lo + hi) // 2
        if m * m <= n: ans, lo = m, m + 1
        else: hi = m - 1
    return ans
```

Verified: `(1,3)`; `(-1,-1)`; `search_rotated(...,5)=1`, `(...,8)=-1`; `find_peak([1,3,5,4,2])=2`; `sqrt_floor` on `17,16,0,1,99` → `4,4,0,1,9`.

*Grading: 3 pts (a), 1 pt (b) — must **call** (a), not re-scan — 3 pts (c), 3 pts (d), 2 pts (e).*
*Deduct 2 on (b) if implemented as a linear count: the spec requires O(log n) and the whole point is reuse. On (e), reject any use of `math.sqrt`/`** 0.5`, and check `sqrt_floor(0)` and `sqrt_floor(1)` — the `n < 2` guard is where most submissions crash or loop.*

**B2 Custom Sorting (14 pts).** 3 pts each for (a)–(d), 2 pts (e).

```python
def merge_k_sorted(lists):
    out = []
    for lst in lists: out = merge(out, lst)      # repeated pairwise merge
    return out
```

*(c) analysis (required): merging accumulator-with-next k times, where the accumulator grows to n, costs `O(n)` per merge and there are `k` merges → **O(nk)**. The optimal approach pairs lists tournament-style (or uses a k-way heap), giving **O(n log k)**. Award the analysis point only if the student explains **why** the accumulator's growth is the cost driver.*
*(d) The empirical check on `list(range(2000))` is the graded artifact — a middle-element pivot is fine on sorted input too, so make sure they tested with random pivot and reported timing. A student who only asserts correctness without the timing evidence loses 1.*
*(e) `top_k` must beat a full sort: partial selection is `O(nk)`, a min-heap of size k is `O(n log k)`. Either earns full marks **with** the complexity stated in the docstring; a `sorted(lst)[-k:]` earns 0 — it is exactly what the problem forbids.*

**B3 Empirical Analysis (10 pts).** 3 pts (a), 4 pts (b), 3 pts (c).

*Expect ratios near 4 for selection sort, near 2.1–2.3 for merge sort and `sorted()`. Grade (b) on whether the classification bands are defensible and the code actually doubles sizes; grade (c) on whether the report is present with real numbers — this is the one place students commonly submit code but no output.*
*Timing caution to accept in student write-ups: at small n the measurements are dominated by interpreter overhead and are unreliable; `sorted()` on random data may look sub-linear because Timsort exploits existing runs. A student who notices and explains this deserves bonus credit.*

**B4 Event Scheduling (14 pts).** Verified on the supplied event list.

**(b)** Greedy by end time selects **`[(1,4), (5,7), (8,11), (12,14)]` — 4 events**, matching the spec.

**(d)** Sorting by **start time** on the *same* input greedily selects `[(0,6), (6,10), (12,14)]` — only **3 events**. That is the required counterexample, and it comes straight from the assignment's own data: `(0,6)` starts earliest but occupies a long span, blocking `(1,4)` and `(5,7)`.

**Why end time is correct:** among all events compatible with what's already chosen, the one finishing earliest leaves the maximum remaining time for everything after it. Formally, by an exchange argument — take any optimal schedule; if its first event doesn't finish earliest, swap in the earliest-finishing compatible event. The result is still valid (it ends no later, so it cannot conflict with the rest) and has the same size. Induct on the remainder: the greedy choice is always extendable to an optimum.

*Grading: 3 pts (a) — must call their own merge sort, not `sorted()`. 4 pts (b) — the count must be 4. 3 pts (c). 4 pts (d) — 2 for the exchange-argument intuition, 2 for a **concrete** counterexample with the two counts shown.*
*Note on (b): comparing `start > last_end` (strict) instead of `start >= last_end` wrongly rejects an event beginning exactly when the previous one ends. **This dataset does not expose the bug** — the greedy path `(1,4)→(5,7)→(8,11)→(12,14)` never touches at a boundary, so both versions return 4. If you want to test for it, add a probe case such as `[(1,4), (4,7), (7,10)]`: correct (`>=`) selects all 3, the strict version selects only 2. Worth adding to the marking script, since a submission can score full marks here while carrying the defect.*

---

*CS 101 · Week 5 · Problem Set 5 · Due Friday Week 6 · © CSE Department*
