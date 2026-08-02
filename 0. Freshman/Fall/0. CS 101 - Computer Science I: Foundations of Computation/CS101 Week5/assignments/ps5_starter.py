#!/usr/bin/env python3
"""
ps5.py
CS 101 — Problem Set 5: Searching and Sorting Algorithms

Student: ____________________________
Date: ______________________________

Honor pledge: I wrote this code myself and understand every line.
Signed: ____________________________
"""

import random
import time


# ══════════════════════════════════════════════════════════════════════════════
# B1: Search Variants
# ══════════════════════════════════════════════════════════════════════════════

def find_first_and_last(lst, target):
    """
    Return (first_index, last_index) of target's occurrences in a sorted
    list with possible duplicates. Return (-1, -1) if not found.

    Time: O(log n) — two binary searches.

    Args:
        lst    (list): sorted list, may contain duplicates
        target:        value to find

    Returns:
        (int, int): (first_index, last_index), or (-1, -1) if absent

    Examples:
        find_first_and_last([1,2,2,2,3,4], 2)  → (1, 3)
        find_first_and_last([1,2,3], 5)         → (-1, -1)
    """
    def find_leftmost():
        lo, hi, result = 0, len(lst) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if lst[mid] == target:
                result = mid
                hi = mid - 1     # keep searching left
            elif lst[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return result

    def find_rightmost():
        lo, hi, result = 0, len(lst) - 1, -1
        # TODO: mirror find_leftmost, but keep searching RIGHT on a match
        return result

    first = find_leftmost()
    if first == -1:
        return (-1, -1)
    last = find_rightmost()
    return (first, last)


assert find_first_and_last([1,2,2,2,3,4], 2) == (1, 3)
assert find_first_and_last([1,2,3], 5)        == (-1, -1)
assert find_first_and_last([], 1)             == (-1, -1)
assert find_first_and_last([5,5,5,5], 5)      == (0, 3)


def count_occurrences(lst, target):
    """
    Count occurrences of target in a sorted list. O(log n).
    Use find_first_and_last.

    Examples:
        count_occurrences([1,2,2,2,3,4], 2) → 3
        count_occurrences([1,2,3], 9)        → 0
    """
    # TODO
    pass


assert count_occurrences([1,2,2,2,3,4], 2) == 3
assert count_occurrences([1,2,3], 9)        == 0
assert count_occurrences([], 1)             == 0


def search_rotated(lst, target):
    """
    Search for target in a rotated sorted list (e.g. [4,5,6,7,1,2,3]).
    O(log n) — do NOT un-rotate the list first.

    Key insight: at least one half of [lo, mid] or [mid, hi] is always
    properly sorted. Determine which half is sorted, then check if
    target lies within that sorted half's range to decide where to recurse.

    Examples:
        search_rotated([4,5,6,7,1,2,3], 5) → 1
        search_rotated([4,5,6,7,1,2,3], 8) → -1
        search_rotated([1], 1)              → 0
    """
    lo, hi = 0, len(lst) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if lst[mid] == target:
            return mid

        # TODO: determine which half [lo,mid] or [mid,hi] is sorted,
        # then check whether target lies in that half's range.
        # if lst[lo] <= lst[mid]:      # left half is sorted
        #     if lst[lo] <= target < lst[mid]:
        #         hi = mid - 1
        #     else:
        #         lo = mid + 1
        # else:                          # right half is sorted
        #     if lst[mid] < target <= lst[hi]:
        #         lo = mid + 1
        #     else:
        #         hi = mid - 1
        pass

    return -1


assert search_rotated([4,5,6,7,1,2,3], 5) == 1
assert search_rotated([4,5,6,7,1,2,3], 8) == -1
assert search_rotated([1], 1)              == 0
assert search_rotated([1], 2)              == -1
assert search_rotated([3,1,2], 1)          == 1


def find_peak(lst):
    """
    Find the index of any "peak" element (greater than its neighbors).
    O(log n) using binary search on the slope direction.

    Precondition: lst is non-empty. lst[-1] and lst[len(lst)] are
    treated as -infinity for boundary comparisons.

    Examples:
        find_peak([1,3,5,4,2]) → 2   (value 5)
        find_peak([1,2,3])     → 2   (value 3, boundary peak)
        find_peak([3,2,1])     → 0   (value 3, boundary peak)
        find_peak([1])         → 0
    """
    assert lst, "find_peak requires a non-empty list"
    lo, hi = 0, len(lst) - 1

    # TODO: binary search — move toward the larger neighbor
    # while lo < hi:
    #     mid = (lo + hi) // 2
    #     if lst[mid] < lst[mid + 1]:
    #         lo = mid + 1     # peak is to the right
    #     else:
    #         hi = mid          # peak is at mid or to the left
    # return lo
    pass


p = find_peak([1,3,5,4,2])
assert lst_val := [1,3,5,4,2][p]
assert [1,3,5,4,2][p] == 5
assert find_peak([1]) == 0
p2 = find_peak([1,2,3])
assert [1,2,3][p2] == 3


def sqrt_floor(n):
    """
    Return floor(sqrt(n)) using binary search on the answer.
    Do NOT use math.sqrt or ** 0.5.

    Args:
        n (int): non-negative integer

    Returns:
        int: largest integer g such that g*g <= n

    Examples:
        sqrt_floor(17) → 4   (4²=16≤17<25=5²)
        sqrt_floor(16) → 4
        sqrt_floor(0)  → 0
        sqrt_floor(1)  → 1
    """
    assert n >= 0
    if n < 2:
        return n

    lo, hi = 1, n
    # TODO: binary search for largest g with g*g <= n
    # Invariant: lo*lo <= n < (hi+1)*(hi+1)  (or similar — design your own precisely)
    pass


assert sqrt_floor(0)  == 0
assert sqrt_floor(1)  == 1
assert sqrt_floor(16) == 4
assert sqrt_floor(17) == 4
assert sqrt_floor(99) == 9
assert sqrt_floor(100)== 10

print("✓ B1: search variants")


# ══════════════════════════════════════════════════════════════════════════════
# B2: Custom Sorting Implementations
# ══════════════════════════════════════════════════════════════════════════════

def insertion_sort_by_key(lst, key):
    """
    Insertion sort that orders elements by key(element).

    Examples:
        insertion_sort_by_key(["hi","a","world"], key=len) → ["a","hi","world"]
    """
    lst = lst[:]
    # TODO: standard insertion sort, comparing key(lst[j]) vs key(item)
    pass


assert insertion_sort_by_key(["hi","a","world"], key=len) == ["a","hi","world"]
assert insertion_sort_by_key([3,1,2], key=lambda x: -x)   == [3,2,1]


def cocktail_sort(lst):
    """
    Bidirectional bubble sort. Alternately sweeps left-to-right and
    right-to-left, shrinking the unsorted region from both ends.

    Time: O(n²) worst case.

    Examples:
        cocktail_sort([5,2,8,1,9]) → [1,2,5,8,9]
    """
    lst = lst[:]
    lo, hi = 0, len(lst) - 1

    # TODO: while lo < hi:
    #   sweep left-to-right from lo to hi, swapping out-of-order pairs
    #   hi -= 1
    #   sweep right-to-left from hi to lo, swapping out-of-order pairs
    #   lo += 1
    #   (add early-exit if a full pass makes no swaps)
    pass


assert cocktail_sort([5,2,8,1,9]) == [1,2,5,8,9]
assert cocktail_sort([])          == []
assert cocktail_sort([1])         == [1]
assert cocktail_sort([3,3,1,1])   == [1,1,3,3]


def merge(left, right):
    """Standard stable merge of two sorted lists."""
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_k_sorted(lists):
    """
    Merge k already-sorted lists into one sorted list.
    Implementation: repeated pairwise merging.

    Complexity: O(nk) where n = total elements, k = number of lists
    (each of the k-1 merges touches up to n elements).
    NOTE: an optimal solution using a min-heap achieves O(n log k) — 
    described but not required here.

    Examples:
        merge_k_sorted([[1,4,7],[2,5,8],[3,6,9]]) → [1,2,3,4,5,6,7,8,9]
        merge_k_sorted([])                          → []
        merge_k_sorted([[1,2,3]])                   → [1,2,3]
    """
    if not lists:
        return []
    # TODO: fold merge() across all lists
    pass


assert merge_k_sorted([[1,4,7],[2,5,8],[3,6,9]]) == [1,2,3,4,5,6,7,8,9]
assert merge_k_sorted([])                          == []
assert merge_k_sorted([[1,2,3]])                   == [1,2,3]
assert merge_k_sorted([[],[1,2],[]])                == [1,2]


def quicksort_random_pivot(lst):
    """
    Quicksort using a randomly chosen pivot.
    Should avoid O(n²) worst case on already-sorted input.

    Examples:
        quicksort_random_pivot([5,2,8,1,9]) → [1,2,5,8,9]
    """
    if len(lst) <= 1:
        return lst[:]

    # TODO: pick pivot = random.choice(lst), partition, recurse
    pivot = random.choice(lst)
    less    = [x for x in lst if x < pivot]
    equal   = [x for x in lst if x == pivot]
    greater = [x for x in lst if x > pivot]

    return quicksort_random_pivot(less) + equal + quicksort_random_pivot(greater)


assert quicksort_random_pivot([5,2,8,1,9]) == [1,2,5,8,9]
assert quicksort_random_pivot([])           == []

# Verify it handles already-sorted input without crashing (worst case for naive pivot choice):
import sys
sys.setrecursionlimit(5000)
big_sorted = list(range(2000))
t0 = time.perf_counter()
result = quicksort_random_pivot(big_sorted)
elapsed = time.perf_counter() - t0
assert result == big_sorted
print(f"✓ quicksort_random_pivot on sorted n=2000: {elapsed*1000:.1f}ms (should be fast, not O(n²) slow)")


def top_k(lst, k):
    """
    Return the k largest elements of lst, in descending order,
    without fully sorting the list.

    Approach: partial selection sort — only find the top k via k
    passes of "find the max of the remaining elements."
    Complexity: O(n*k) — better than O(n log n) when k << n.

    Examples:
        top_k([5,2,8,1,9,3], 3) → [9,8,5]
        top_k([1,2,3], 5)        → [3,2,1]   (k > len: return all, sorted desc)
    """
    lst = lst[:]
    k = min(k, len(lst))
    result = []

    # TODO: k passes, each finding the max of the remaining unselected elements
    # (similar structure to selection sort, but only k passes and take the MAX)

    return result


assert top_k([5,2,8,1,9,3], 3) == [9,8,5]
assert top_k([1,2,3], 5)        == [3,2,1]
assert top_k([], 3)             == []

print("✓ B2: custom sorting implementations")


# ══════════════════════════════════════════════════════════════════════════════
# B3: Empirical Analysis
# ══════════════════════════════════════════════════════════════════════════════

def measure_growth(sort_func, sizes):
    """
    Time sort_func on random lists of each size in sizes.

    Args:
        sort_func: a function taking a list and returning a sorted list
                   (may return (list, stats) tuple — handle both cases)
        sizes:     list of input sizes to test

    Returns:
        list of (size, time_in_seconds) tuples
    """
    measurements = []
    for n in sizes:
        data = [random.randint(0, 1_000_000) for _ in range(n)]
        start = time.perf_counter()
        result = sort_func(data)
        elapsed = time.perf_counter() - start
        measurements.append((n, elapsed))
    return measurements


def estimate_complexity_class(measurements):
    """
    Estimate the complexity class from timing measurements at doubling sizes.

    For each consecutive pair (n1,t1), (n2,t2) where n2 ≈ 2*n1:
        ratio = t2 / t1
        O(n):        ratio ≈ 2
        O(n log n):  ratio ≈ 2 to 2.5 (slightly more than 2)
        O(n²):       ratio ≈ 4

    Args:
        measurements: list of (size, time) tuples, sizes should roughly double

    Returns:
        str: "O(n)", "O(n log n)", or "O(n²)" (best estimate)
    """
    if len(measurements) < 2:
        return "insufficient data"

    ratios = []
    for i in range(1, len(measurements)):
        n1, t1 = measurements[i-1]
        n2, t2 = measurements[i]
        if t1 > 0:
            ratios.append(t2 / t1)

    if not ratios:
        return "insufficient data"

    avg_ratio = sum(ratios) / len(ratios)

    # TODO: classify avg_ratio into one of the three complexity classes
    # avg_ratio close to 2   → "O(n)"
    # avg_ratio close to 2-3 → "O(n log n)"
    # avg_ratio close to 4   → "O(n²)"
    pass


# Demonstration:
def _sorted_wrapper(lst):
    return sorted(lst)

sizes = [500, 1000, 2000, 4000]

print("\nEmpirical complexity estimation:")
for name, func in [("timsort (builtin)", _sorted_wrapper)]:
    measurements = measure_growth(func, sizes)
    estimate = estimate_complexity_class(measurements)
    print(f"  {name}: {measurements} → estimated {estimate}")


print("✓ B3: empirical analysis")


# ══════════════════════════════════════════════════════════════════════════════
# B4: Event Scheduling
# ══════════════════════════════════════════════════════════════════════════════

def sort_by_end_time(events):
    """
    Sort events (list of (start, end) tuples) by end time, using merge_sort.
    Must call your own merge_sort logic, not Python's built-in sorted().

    Examples:
        sort_by_end_time([(1,4),(3,5),(0,6)]) → [(1,4),(3,5),(0,6)]
        (already sorted by end time in this example)
    """
    if len(events) <= 1:
        return events[:]

    # TODO: implement merge sort, comparing by events[i][1] (end time)
    mid   = len(events) // 2
    left  = sort_by_end_time(events[:mid])
    right = sort_by_end_time(events[mid:])

    # Custom merge comparing end times:
    result, i, j = [], 0, 0
    # TODO: merge left and right by end time (left[i][1] <= right[j][1])
    result.extend(left[i:])
    result.extend(right[j:])
    return result


test_events = [(3,5),(1,4),(0,6)]
sorted_events = sort_by_end_time(test_events)
assert [e[1] for e in sorted_events] == sorted(e[1] for e in test_events)


def max_non_overlapping(events):
    """
    Return the maximum set of non-overlapping events using the greedy
    "earliest end time first" algorithm.

    Algorithm:
        1. Sort events by end time (use sort_by_end_time)
        2. Greedily select each event whose start >= previous selected end

    Args:
        events (list of (start, end) tuples)

    Returns:
        list of selected (start, end) tuples, in order

    Example:
        events = [(1,4),(3,5),(0,6),(5,7),(3,8),(5,9),(6,10),(8,11),(8,12),(2,13),(12,14)]
        max_non_overlapping(events) → 4 events selected
    """
    if not events:
        return []

    sorted_events = sort_by_end_time(events)
    selected = [sorted_events[0]]

    # TODO: for each subsequent event, select if its start >= selected[-1][1]

    return selected


events = [(1,4),(3,5),(0,6),(5,7),(3,8),(5,9),(6,10),(8,11),(8,12),(2,13),(12,14)]
selected = max_non_overlapping(events)
assert len(selected) == 4, f"Expected 4 events, got {len(selected)}: {selected}"
# Verify no overlaps:
for i in range(len(selected) - 1):
    assert selected[i][1] <= selected[i+1][0], f"Overlap between {selected[i]} and {selected[i+1]}"
print(f"✓ max_non_overlapping: selected {selected}")


def binary_search_next_event(sorted_events, current_end_time):
    """
    Given events sorted by START time, find the index of the first event
    whose start time is >= current_end_time. O(log n).

    Args:
        sorted_events (list of (start,end) tuples): sorted by start time
        current_end_time (int): the time to search from

    Returns:
        int: index of first valid next event, or len(sorted_events) if none

    Examples:
        events_by_start = [(0,6),(1,4),(2,13),(3,5),(3,8),(5,7),(5,9),(6,10),(8,11),(8,12),(12,14)]
        binary_search_next_event(events_by_start, 7) → index of first event with start >= 7
    """
    lo, hi = 0, len(sorted_events)
    # TODO: binary search (bisect_left style) for first event with start >= current_end_time
    pass


events_by_start = sorted(events, key=lambda e: e[0])
idx = binary_search_next_event(events_by_start, 7)
assert events_by_start[idx][0] >= 7
if idx > 0:
    assert events_by_start[idx-1][0] < 7
print(f"✓ binary_search_next_event: found index {idx}")

print("✓ B4: event scheduling")


# ══════════════════════════════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("All ps5.py assertions passed.")
    print("=" * 50)
