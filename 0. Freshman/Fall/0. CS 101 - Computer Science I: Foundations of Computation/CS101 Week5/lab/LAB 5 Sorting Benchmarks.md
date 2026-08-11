# CS 101 · Lab 5
## Benchmarking Sorting Algorithms

**Tuesday of Week 6 · Lab Section** — sat after this week's Wed–Fri lectures, and covers Week 5.
*Duration: 2 hours · Graded on completion (TA checkoff)*

---

## Objectives

By the end of this lab, you will:
- [ ] Implement all 5 sorting algorithms from this week's lectures
- [ ] Empirically measure their runtime across input sizes from 10 to 100,000
- [ ] Plot runtime vs. input size and visually confirm O(n²) vs O(n log n) growth
- [ ] Measure best-case behavior (already-sorted data) for insertion sort and bubble sort
- [ ] Verify stability empirically
- [ ] Compare your implementations against Python's built-in `sorted()`

---

## Setup

```bash
cd ~/cs101
mkdir week5 && cd week5
pip install matplotlib --user   # if not already installed
```

---

## Part 1: Implement All Sorting Algorithms (30 minutes)

Create `sorting_algorithms.py` with all five algorithms from this week, each instrumented to count comparisons and swaps.

```python
#!/usr/bin/env python3
"""
sorting_algorithms.py
CS 101 — Week 5, Lab 5

All sorting algorithms instrumented with comparison/swap counters.
"""


class SortStats:
    """Tracks comparisons and swaps during a sort."""
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0

    def __repr__(self):
        return f"comparisons={self.comparisons}, swaps={self.swaps}"


def selection_sort(lst, stats=None):
    """Selection sort, instrumented."""
    if stats is None:
        stats = SortStats()
    lst = lst[:]
    n = len(lst)

    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            stats.comparisons += 1
            if lst[j] < lst[min_idx]:
                min_idx = j
        if min_idx != i:
            lst[i], lst[min_idx] = lst[min_idx], lst[i]
            stats.swaps += 1

    return lst, stats


def insertion_sort(lst, stats=None):
    """Insertion sort, instrumented."""
    if stats is None:
        stats = SortStats()
    lst = lst[:]
    n = len(lst)

    for i in range(1, n):
        key = lst[i]
        j = i - 1
        while j >= 0:
            stats.comparisons += 1
            if lst[j] > key:
                lst[j + 1] = lst[j]
                stats.swaps += 1
                j -= 1
            else:
                break
        lst[j + 1] = key

    return lst, stats


def bubble_sort(lst, stats=None):
    """Bubble sort with early-exit optimization, instrumented."""
    if stats is None:
        stats = SortStats()
    lst = lst[:]
    n = len(lst)

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            stats.comparisons += 1
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                stats.swaps += 1
                swapped = True
        if not swapped:
            break

    return lst, stats


def merge_sort(lst, stats=None):
    """Merge sort, instrumented."""
    if stats is None:
        stats = SortStats()

    if len(lst) <= 1:
        return lst[:], stats

    mid = len(lst) // 2
    left, _  = merge_sort(lst[:mid], stats)
    right, _ = merge_sort(lst[mid:], stats)
    merged   = _merge(left, right, stats)

    return merged, stats


def _merge(left, right, stats):
    """Merge helper for merge_sort."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        stats.comparisons += 1
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quicksort(lst, stats=None):
    """Quicksort (middle pivot), instrumented."""
    if stats is None:
        stats = SortStats()

    if len(lst) <= 1:
        return lst[:], stats

    pivot = lst[len(lst) // 2]
    less, equal, greater = [], [], []

    for x in lst:
        stats.comparisons += 1
        if x < pivot:
            less.append(x)
        elif x == pivot:
            equal.append(x)
        else:
            greater.append(x)

    sorted_less, _    = quicksort(less, stats)
    sorted_greater, _ = quicksort(greater, stats)

    return sorted_less + equal + sorted_greater, stats


def timsort_wrapper(lst, stats=None):
    """Wrapper around Python's built-in sort, for comparison purposes."""
    if stats is None:
        stats = SortStats()
    return sorted(lst), stats   # comparisons/swaps not tracked (C implementation)


ALGORITHMS = {
    "selection_sort": selection_sort,
    "insertion_sort": insertion_sort,
    "bubble_sort":    bubble_sort,
    "merge_sort":     merge_sort,
    "quicksort":      quicksort,
    "timsort":        timsort_wrapper,
}


def verify_all():
    """Verify all algorithms produce correct sorted output."""
    import random
    test_cases = [
        [],
        [1],
        [2, 1],
        [3, 1, 2],
        [5, 2, 8, 1, 9, 3],
        [1, 1, 1, 1],
        [random.randint(-100, 100) for _ in range(50)],
        list(range(20)),           # already sorted
        list(range(20, 0, -1)),    # reverse sorted
    ]

    for name, func in ALGORITHMS.items():
        for test in test_cases:
            result, _ = func(test)
            expected = sorted(test)
            assert result == expected, f"{name} FAILED on {test}: got {result}, expected {expected}"
        print(f"✓ {name} — all test cases passed")


if __name__ == "__main__":
    verify_all()
```

Run it: `python3 sorting_algorithms.py` — all six should pass.

---

## Part 2: Empirical Complexity Measurement (40 minutes)

Create `benchmark.py`.

```python
#!/usr/bin/env python3
"""
benchmark.py
CS 101 — Week 5, Lab 5

Empirically measure sorting algorithm performance across input sizes.
"""

import time
import random
import sys
from sorting_algorithms import ALGORITHMS, SortStats

sys.setrecursionlimit(10000)   # merge sort / quicksort recursion on large inputs


def time_sort(func, data):
    """Time a single sort call. Returns (elapsed_seconds, stats)."""
    start = time.perf_counter()
    result, stats = func(data)
    elapsed = time.perf_counter() - start
    return elapsed, stats


def benchmark_random(sizes, algorithms):
    """
    Benchmark each algorithm on random data of increasing size.
    Returns a dict: {algo_name: {size: (time, comparisons)}}
    """
    results = {name: {} for name in algorithms}

    for n in sizes:
        data = [random.randint(0, 1_000_000) for _ in range(n)]
        print(f"\n--- n = {n:,} ---")

        for name, func in algorithms.items():
            # Skip O(n²) algorithms for very large n (would take too long)
            if name in ("selection_sort", "bubble_sort", "insertion_sort") and n > 5000:
                print(f"  {name:16}: SKIPPED (too slow for n={n})")
                continue

            test_data = data[:]   # each algorithm gets an identical copy
            elapsed, stats = time_sort(func, test_data)
            results[name][n] = (elapsed, stats.comparisons)
            print(f"  {name:16}: {elapsed*1000:9.3f} ms   comparisons={stats.comparisons:>12,}")

    return results


if __name__ == "__main__":
    sizes = [10, 100, 1000, 5000, 20000, 100000]

    print("=" * 60)
    print("SORTING ALGORITHM BENCHMARK — Random Data")
    print("=" * 60)

    results = benchmark_random(sizes, ALGORITHMS)

    # Save results for plotting
    import json
    with open("benchmark_results.json", "w") as f:
        # Convert to JSON-serializable format
        serializable = {
            name: {str(k): v for k, v in sizes_dict.items()}
            for name, sizes_dict in results.items()
        }
        json.dump(serializable, f, indent=2)

    print("\nResults saved to benchmark_results.json")
```

Run it: `python3 benchmark.py`. This will take a few minutes for the largest sizes — that's expected and part of the lesson.

**Record in `LAB 5 Sorting Benchmarks.md`:**
1. At n=100,000, how much SLOWER is `merge_sort` than `timsort`? Why do you think this is, given both are O(n log n)?
2. Compute the ratio of comparisons between `selection_sort` at n=1000 and n=5000. Does it match the predicted n² scaling? (Predicted ratio: (5000/1000)² = 25)
3. Compute the ratio of comparisons between `merge_sort` at n=1000 and n=100000. Does it roughly match n log n scaling?

---

## Part 3: Plotting Runtime vs. Input Size (25 minutes)

Create `plot_results.py`:

```python
#!/usr/bin/env python3
"""
plot_results.py
CS 101 — Week 5, Lab 5

Visualize sorting algorithm performance.
"""

import json
import matplotlib.pyplot as plt

with open("benchmark_results.json") as f:
    results = json.load(f)

# Plot 1: Runtime vs. n (linear scale)
plt.figure(figsize=(10, 6))
for name, sizes_dict in results.items():
    ns = sorted(int(n) for n in sizes_dict.keys())
    times = [sizes_dict[str(n)][0] * 1000 for n in ns]   # convert to ms
    plt.plot(ns, times, marker='o', label=name)

plt.xlabel("Input size (n)")
plt.ylabel("Time (ms)")
plt.title("Sorting Algorithm Runtime vs Input Size")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("runtime_linear.png", dpi=100)
print("Saved runtime_linear.png")

# Plot 2: Runtime vs. n (log-log scale — reveals the complexity class)
plt.figure(figsize=(10, 6))
for name, sizes_dict in results.items():
    ns = sorted(int(n) for n in sizes_dict.keys())
    times = [sizes_dict[str(n)][0] * 1000 for n in ns]
    plt.loglog(ns, times, marker='o', label=name)

plt.xlabel("Input size (n) — log scale")
plt.ylabel("Time (ms) — log scale")
plt.title("Sorting Algorithm Runtime vs Input Size (log-log)")
plt.legend()
plt.grid(True, alpha=0.3, which="both")
plt.savefig("runtime_loglog.png", dpi=100)
print("Saved runtime_loglog.png")

# Plot 3: Comparisons vs. n
plt.figure(figsize=(10, 6))
for name, sizes_dict in results.items():
    ns = sorted(int(n) for n in sizes_dict.keys())
    comparisons = [sizes_dict[str(n)][1] for n in ns]
    plt.plot(ns, comparisons, marker='o', label=name)

plt.xlabel("Input size (n)")
plt.ylabel("Number of comparisons")
plt.title("Comparisons vs Input Size")
plt.legend()
plt.grid(True, alpha=0.3)
plt.yscale("log")
plt.savefig("comparisons.png", dpi=100)
print("Saved comparisons.png")

plt.show()
```

**Key insight to observe:** On the log-log plot, an O(n^k) algorithm appears as a **straight line with slope k**. This means:
- O(n²) algorithms (selection, bubble, insertion) → slope ≈ 2
- O(n log n) algorithms (merge sort, quicksort, timsort) → slope ≈ 1 (log n grows so slowly it barely bends the line)

**Record in `LAB 5 Sorting Benchmarks.md`:** Include your three plots (or describe them if you can't attach images) and estimate the slope of each algorithm's line on the log-log plot. Does it match the predicted complexity?

---

## Part 4: Best-Case Behavior (20 minutes)

Create `best_case_test.py` to verify the best-case claims from lecture.

```python
#!/usr/bin/env python3
"""
best_case_test.py
CS 101 — Week 5, Lab 5

Verify best-case O(n) behavior for insertion sort and bubble sort
on already-sorted data.
"""

from sorting_algorithms import selection_sort, insertion_sort, bubble_sort

def test_best_case(n):
    """Test all three O(n²) algorithms on already-sorted data of size n."""
    sorted_data = list(range(n))

    print(f"\n--- Already-sorted data, n={n} ---")
    for name, func in [
        ("selection_sort", selection_sort),
        ("insertion_sort", insertion_sort),
        ("bubble_sort",    bubble_sort),
    ]:
        result, stats = func(sorted_data)
        print(f"  {name:16}: comparisons={stats.comparisons:6}  swaps={stats.swaps:6}")


for n in [10, 100, 1000]:
    test_best_case(n)

print("\n" + "=" * 50)
print("ANALYSIS")
print("=" * 50)
print("""
For already-sorted data:
  - selection_sort:  comparisons should STILL be n(n-1)/2 (input-independent!)
  - insertion_sort:  comparisons should be ~n-1 (O(n) — best case!)
  - bubble_sort:     comparisons should be ~n-1 (O(n) — with early exit!)

Verify these match your output above.
""")

# Now test reverse-sorted (worst case for insertion and bubble):
def test_worst_case(n):
    reverse_data = list(range(n, 0, -1))
    print(f"\n--- Reverse-sorted data (worst case), n={n} ---")
    for name, func in [
        ("selection_sort", selection_sort),
        ("insertion_sort", insertion_sort),
        ("bubble_sort",    bubble_sort),
    ]:
        result, stats = func(reverse_data)
        print(f"  {name:16}: comparisons={stats.comparisons:6}  swaps={stats.swaps:6}")

for n in [10, 100, 1000]:
    test_worst_case(n)
```

**Record in `LAB 5 Sorting Benchmarks.md`:**
1. For selection_sort on sorted data of size n=1000, how many comparisons occurred? Does this match n(n-1)/2 exactly?
2. For insertion_sort on sorted data of size n=1000, how many comparisons? Is it close to n-1?
3. For insertion_sort on reverse-sorted data of size n=1000, how many comparisons? Is it close to n(n-1)/2 (the worst case)?
4. Explain in one sentence why selection sort's comparison count never changes regardless of input order, while insertion sort's does.

---

## Part 5: Verifying Stability (15 minutes)

Create `stability_test.py`:

```python
#!/usr/bin/env python3
"""
stability_test.py
CS 101 — Week 5, Lab 5

Empirically verify which sorting algorithms are stable.
"""

from sorting_algorithms import selection_sort, insertion_sort, bubble_sort, merge_sort, quicksort


def test_stability(sort_func, name):
    """
    Test stability using tagged elements: sort by first component only,
    and check if elements with equal first components keep their
    original relative order (indicated by the tag).
    """
    # Each element: (sort_key, original_index) — sort only by sort_key
    data = [(3, 'a'), (1, 'b'), (3, 'c'), (2, 'd'), (1, 'e'), (3, 'f')]

    # We need a version that sorts by the first element only
    class Wrapper:
        def __init__(self, key, tag):
            self.key = key
            self.tag = tag
        def __lt__(self, other):
            return self.key < other.key
        def __le__(self, other):
            return self.key <= other.key
        def __eq__(self, other):
            return self.key == other.key
        def __repr__(self):
            return f"({self.key},{self.tag})"

    wrapped = [Wrapper(k, t) for k, t in data]
    result, _ = sort_func(wrapped)

    # Check: for equal keys, do tags appear in original relative order?
    groups = {}
    for item in result:
        groups.setdefault(item.key, []).append(item.tag)

    original_groups = {}
    for k, t in data:
        original_groups.setdefault(k, []).append(t)

    is_stable = (groups == original_groups)
    print(f"{name:16}: {'STABLE' if is_stable else 'NOT STABLE'}  {result}")
    return is_stable


print("Testing stability (equal elements should keep original relative order):\n")
test_stability(selection_sort, "selection_sort")
test_stability(insertion_sort, "insertion_sort")
test_stability(bubble_sort,    "bubble_sort")
test_stability(merge_sort,     "merge_sort")
test_stability(quicksort,      "quicksort")

print("\nExpected results (from lecture):")
print("  selection_sort: NOT STABLE")
print("  insertion_sort: STABLE")
print("  bubble_sort:    STABLE")
print("  merge_sort:     STABLE")
print("  quicksort:      NOT STABLE")
```

**Record:** Did your empirical results match the lecture's predictions? If any didn't match, investigate why (it may depend on the specific tie-breaking implementation).

---

## Part 6: Commit and Reflection (10 minutes)

```bash
cd ~/cs101/week5
git add .
git commit -m "Week 5 Lab: sorting algorithm benchmarks, best-case analysis, stability tests"
git push
```

### Reflection in `LAB 5 Sorting Benchmarks.md`:

**Q1.** Your log-log plot should show O(n²) algorithms as steeper lines than O(n log n) algorithms. At approximately what input size did selection_sort become noticeably slower than merge_sort in your absolute (non-log) runtime plot?

**Q2.** Despite both being O(n log n) on average, quicksort is often faster than merge sort in practice. Name two reasons from lecture, and explain which one you think matters more for the sizes you tested.

**Q3.** You verified that insertion sort achieves O(n) on already-sorted data. Give a concrete real-world scenario where this property would make insertion sort the *right* choice over merge sort, despite merge sort's better worst-case guarantee.

**Q4.** The stability test used a `Wrapper` class with custom `__lt__`, `__le__`, `__eq__` methods. Why did the test need `__le__` specifically (not just `__lt__`)? Which sorting algorithm's correctness depends on this operator?

---

## TA Checkoff Criteria

Show your TA:
- [ ] `sorting_algorithms.py` — all 6 pass `verify_all()`
- [ ] `benchmark.py` output showing timing data for all sizes
- [ ] Three plots generated (`runtime_linear.png`, `runtime_loglog.png`, `comparisons.png`)
- [ ] `best_case_test.py` output with analysis in notes
- [ ] `stability_test.py` output matching (or explaining discrepancies from) predictions
- [ ] `LAB 5 Sorting Benchmarks.md` with all reflection questions answered

---

## Bonus Challenges

**Bonus 1 — Randomized quicksort:**
Modify `quicksort` to pick a **random** pivot instead of the middle element. Benchmark it against the middle-pivot version on already-sorted data (the middle-pivot version's worst case). Does randomization help?

**Bonus 2 — Adaptive insertion sort threshold:**
Real-world hybrid sorts (like Timsort) switch to insertion sort for small sub-arrays. Modify your `merge_sort` to use `insertion_sort` directly when the sub-array size is below some threshold (e.g., 16). Benchmark the hybrid version against pure merge sort. Does it help? At what threshold?

**Bonus 3 — Counting sort:**
Implement `counting_sort(lst, max_value)` for lists of non-negative integers bounded by `max_value`. It should run in O(n + max_value) time — faster than any comparison sort for suitable data. Benchmark it against `merge_sort` on a list of 100,000 integers in range [0, 1000).

---

*CS 101 · Week 5 · Lab 5 · © CSE Department*
