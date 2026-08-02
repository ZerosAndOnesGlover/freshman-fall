#!/usr/bin/env python3
"""
sorting_algorithms.py
CS 101 — Week 5, Lab 5 Starter

All sorting algorithms instrumented with comparison/swap counters.
Implement each function, then run verify_all() to check correctness.

Student: ____________________________
Date: ______________________________
"""


class SortStats:
    """Tracks comparisons and swaps during a sort."""
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0

    def __repr__(self):
        return f"comparisons={self.comparisons}, swaps={self.swaps}"


def selection_sort(lst, stats=None):
    """
    Selection sort, instrumented with comparison/swap counting.

    Loop invariant: after the ith iteration, lst[0..i] contains the
    i+1 smallest elements of the original list, in sorted order.

    Time: O(n²) always. Swaps: O(n).

    Returns:
        (sorted_list, stats)
    """
    if stats is None:
        stats = SortStats()
    lst = lst[:]   # don't mutate caller's list
    n = len(lst)

    # TODO: implement selection sort
    # For each i from 0 to n-2:
    #   find min_idx in lst[i:]  (increment stats.comparisons for each comparison)
    #   if min_idx != i: swap and increment stats.swaps

    return lst, stats


def insertion_sort(lst, stats=None):
    """
    Insertion sort, instrumented.

    Loop invariant: after the ith iteration, lst[0..i] is sorted.

    Time: O(n) best case (sorted input), O(n²) worst case.

    Returns:
        (sorted_list, stats)
    """
    if stats is None:
        stats = SortStats()
    lst = lst[:]
    n = len(lst)

    # TODO: implement insertion sort
    # For each i from 1 to n-1:
    #   key = lst[i]
    #   shift elements > key rightward (count each comparison AND each shift as a "swap")
    #   insert key in its place

    return lst, stats


def bubble_sort(lst, stats=None):
    """
    Bubble sort with early-exit optimization, instrumented.

    Loop invariant: after the ith pass, the i largest elements
    are in their correct final positions.

    Time: O(n) best case (with early exit), O(n²) worst case.

    Returns:
        (sorted_list, stats)
    """
    if stats is None:
        stats = SortStats()
    lst = lst[:]
    n = len(lst)

    # TODO: implement bubble sort with early exit
    # For each pass i from 0 to n-2:
    #   swapped = False
    #   for j from 0 to n-2-i:
    #     compare lst[j], lst[j+1] (count comparison)
    #     if out of order: swap, count swap, swapped = True
    #   if not swapped: break

    return lst, stats


def _merge(left, right, stats):
    """
    Merge two sorted lists into one sorted list. O(len(left)+len(right)).
    Uses <= (not <) to ensure stability.
    """
    result = []
    i = j = 0

    # TODO: standard merge, incrementing stats.comparisons for each comparison
    # Use left[i] <= right[j] (not <) for stability!

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(lst, stats=None):
    """
    Merge sort, instrumented.

    Time: O(n log n) all cases. Space: O(n). Stable: Yes.

    Returns:
        (sorted_list, stats)
    """
    if stats is None:
        stats = SortStats()

    if len(lst) <= 1:
        return lst[:], stats

    # TODO: divide, recurse on each half, combine with _merge
    mid = len(lst) // 2
    left, _  = merge_sort(lst[:mid], stats)
    right, _ = merge_sort(lst[mid:], stats)
    merged   = _merge(left, right, stats)

    return merged, stats


def quicksort(lst, stats=None):
    """
    Quicksort with middle-element pivot, instrumented.

    Time: O(n log n) average, O(n²) worst case (e.g. sorted input
    with poor pivot choice — middle pivot mitigates but doesn't eliminate this).
    Stable: No.

    Returns:
        (sorted_list, stats)
    """
    if stats is None:
        stats = SortStats()

    if len(lst) <= 1:
        return lst[:], stats

    pivot = lst[len(lst) // 2]
    less, equal, greater = [], [], []

    # TODO: partition lst into less/equal/greater relative to pivot
    # Increment stats.comparisons for each element examined

    sorted_less, _    = quicksort(less, stats)
    sorted_greater, _ = quicksort(greater, stats)

    return sorted_less + equal + sorted_greater, stats


def timsort_wrapper(lst, stats=None):
    """Wrapper around Python's built-in sort, for benchmark comparison."""
    if stats is None:
        stats = SortStats()
    return sorted(lst), stats


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
            assert result == expected, (
                f"{name} FAILED on {test}: got {result}, expected {expected}"
            )
        print(f"✓ {name} — all test cases passed")

    print("\n🎉 All sorting algorithms verified correct!")


if __name__ == "__main__":
    verify_all()
