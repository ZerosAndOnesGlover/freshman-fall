#!/usr/bin/env python3
"""
ps6.py
CS 101 — Problem Set 6: Algorithm Analysis

Student: ____________________________
Date: ______________________________

Honor pledge: I wrote this code myself and understand every line.
Signed: ____________________________
"""

import math
import time
import random


# ══════════════════════════════════════════════════════════════════════════════
# B1: Empirical Complexity Verification Tool
# ══════════════════════════════════════════════════════════════════════════════

def time_function(func, arg_generator, sizes):
    """
    Time func on inputs of increasing size.

    Args:
        func:          function taking one argument
        arg_generator: function that takes n and returns an appropriate argument
        sizes:         list of sizes to test

    Returns:
        list of (n, time_in_seconds) tuples

    Example:
        time_function(sum, lambda n: list(range(n)), [100, 1000, 10000])
    """
    measurements = []
    # TODO: for each n in sizes:
    #   arg = arg_generator(n)
    #   time it (use time.perf_counter(), consider running func multiple times
    #   and taking the min to reduce noise)
    #   append (n, elapsed) to measurements
    return measurements


def fit_power_law(measurements):
    """
    Fit T(n) = c * n^k to the measurements using log-log linear regression.

    Returns:
        (c, k): estimated constant and exponent

    Method:
        log(T) = log(c) + k*log(n)  — linear regression on (log(n), log(T))
        slope = k, intercept = log(c)
    """
    valid = [(n, t) for n, t in measurements if t > 0]
    if len(valid) < 2:
        return None, None

    log_ns    = [math.log(n) for n, t in valid]
    log_times = [math.log(t) for n, t in valid]

    mean_x = sum(log_ns) / len(log_ns)
    mean_y = sum(log_times) / len(log_times)

    numerator   = sum((x - mean_x) * (y - mean_y) for x, y in zip(log_ns, log_times))
    denominator = sum((x - mean_x) ** 2 for x in log_ns)

    if denominator == 0:
        return None, None

    k = numerator / denominator
    log_c = mean_y - k * mean_x
    c = math.exp(log_c)

    return c, k


def predict_time(c, k, n):
    """
    Predict T(n) using fitted parameters c, k from fit_power_law.

    Returns:
        float: predicted time = c * n^k
    """
    # TODO
    pass


def classify(k):
    """
    Map an estimated exponent k to a complexity class string.

    Suggested thresholds:
        k < 0.3         → "O(log n)"
        0.3 <= k < 0.7  → "O(sqrt(n))"  (rare, but possible)
        0.7 <= k < 1.3  → "O(n)"
        1.3 <= k < 1.8  → "O(n log n)"
        1.8 <= k < 2.5  → "O(n^2)"
        2.5 <= k < 3.5  → "O(n^3)"
        k >= 3.5        → "O(n^k) — high degree polynomial"

    Returns:
        str
    """
    # TODO
    pass


# Demonstration:
def _example_quadratic(n):
    total = 0
    for i in range(n):
        for j in range(n):
            total += 1
    return total

measurements = time_function(_example_quadratic, lambda n: n, [50, 100, 200, 400])
c, k = fit_power_law(measurements)
if k is not None:
    print(f"Quadratic test function: estimated k = {k:.2f} → {classify(k)}")
    predicted = predict_time(c, k, 800)
    print(f"Predicted time at n=800: {predicted*1000:.2f} ms")


print("✓ B1: empirical complexity tool built")


# ══════════════════════════════════════════════════════════════════════════════
# B2: Complexity Classification Exercises
# ══════════════════════════════════════════════════════════════════════════════

def all_triples_sum_to_zero(lst):
    """
    O(n^3) — three nested loops over all distinct triples.

    Return True if any three DISTINCT indices i<j<k have lst[i]+lst[j]+lst[k]==0.

    Examples:
        all_triples_sum_to_zero([1, -2, 1, 0, 5]) → True   (1 + -2 + 1 = 0)
        all_triples_sum_to_zero([1, 2, 3])          → False
    """
    n = len(lst)
    # TODO: three nested loops
    return False


assert all_triples_sum_to_zero([1, -2, 1, 0, 5]) == True
assert all_triples_sum_to_zero([1, 2, 3])          == False
assert all_triples_sum_to_zero([0, 0, 0])           == True


def all_triples_sum_to_zero_fast(lst):
    """
    O(n^2) — sort first, then for each element use two pointers on the rest.

    Same behavior as all_triples_sum_to_zero but faster.

    Algorithm:
        sorted_lst = sorted(lst)
        for i in range(n):
            target = -sorted_lst[i]
            lo, hi = i+1, n-1
            while lo < hi:
                s = sorted_lst[lo] + sorted_lst[hi]
                if s == target: return True
                elif s < target: lo += 1
                else: hi -= 1
        return False
    """
    n = len(lst)
    sorted_lst = sorted(lst)
    # TODO: implement the two-pointer algorithm described above
    return False


assert all_triples_sum_to_zero_fast([1, -2, 1, 0, 5]) == True
assert all_triples_sum_to_zero_fast([1, 2, 3])          == False
assert all_triples_sum_to_zero_fast([0, 0, 0])           == True
# Cross-verify against the slow version on random data:
for _ in range(20):
    test = [random.randint(-10, 10) for _ in range(random.randint(3, 15))]
    assert all_triples_sum_to_zero(test) == all_triples_sum_to_zero_fast(test), f"Mismatch on {test}"
print("✓ all_triples_sum_to_zero (both versions agree)")


def matrix_multiply(A, B):
    """
    O(n^3) — naive matrix multiplication for n x n matrices.

    Args:
        A, B: lists of lists (n x n matrices)

    Returns:
        list of lists: the product A @ B

    Reasoning for O(n^3): computing each of the n^2 output entries
    requires summing n products — n^2 * n = n^3.

    Examples:
        matrix_multiply([[1,2],[3,4]], [[5,6],[7,8]]) → [[19,22],[43,50]]
    """
    n = len(A)
    result = [[0] * n for _ in range(n)]
    # TODO: three nested loops (i, j, k)
    return result


assert matrix_multiply([[1,2],[3,4]], [[5,6],[7,8]]) == [[19,22],[43,50]]
assert matrix_multiply([[1]], [[1]]) == [[1]]
print("✓ matrix_multiply")


def count_inversions_On2(lst):
    """
    O(n^2) — count pairs (i,j) with i<j and lst[i]>lst[j], via nested loops.
    """
    count = 0
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] > lst[j]:
                count += 1
    return count


def count_inversions_Onlogn(lst):
    """
    O(n log n) — count inversions using a modified merge sort.

    Key insight: during the merge step, if we take an element from `right`
    before all elements of `left` have been consumed, that right-element
    forms an inversion with EVERY remaining element in `left` (since left
    is sorted and all those elements are larger, appearing earlier in
    the original array — i<j and lst[i]>lst[j]).

    Returns:
        int: total inversion count

    Examples:
        count_inversions_Onlogn([3, 1, 2]) → 2
        count_inversions_Onlogn([1, 2, 3]) → 0
    """
    def sort_and_count(arr):
        """Return (sorted_array, inversion_count)."""
        if len(arr) <= 1:
            return arr, 0

        mid = len(arr) // 2
        left, left_count   = sort_and_count(arr[:mid])
        right, right_count = sort_and_count(arr[mid:])

        merged = []
        i = j = 0
        cross_count = 0

        # TODO: standard merge, but whenever you take from `right` before
        # `left` is exhausted, add (len(left) - i) to cross_count
        # (all remaining elements in left form inversions with right[j])

        merged.extend(left[i:])
        merged.extend(right[j:])

        total_count = left_count + right_count + cross_count
        return merged, total_count

    _, total = sort_and_count(lst)
    return total


assert count_inversions_On2([3, 1, 2]) == 2
assert count_inversions_On2([1, 2, 3]) == 0
assert count_inversions_Onlogn([3, 1, 2]) == 2
assert count_inversions_Onlogn([1, 2, 3]) == 0
assert count_inversions_Onlogn([5,4,3,2,1]) == 10   # all pairs inverted: C(5,2)=10

# Cross-verify on random data:
for _ in range(30):
    test = [random.randint(0, 100) for _ in range(random.randint(0, 30))]
    assert count_inversions_On2(test) == count_inversions_Onlogn(test), f"Mismatch on {test}"
print("✓ count_inversions (both versions agree)")

# Benchmark comparison:
print("\nBenchmarking inversion counting:")
for n in [500, 1000, 2000]:
    data = [random.randint(0, 10000) for _ in range(n)]
    t0 = time.perf_counter(); count_inversions_On2(data); t1 = time.perf_counter()
    t2 = time.perf_counter(); count_inversions_Onlogn(data); t3 = time.perf_counter()
    print(f"  n={n:5}: O(n²)={  (t1-t0)*1000:8.2f}ms   O(n log n)={(t3-t2)*1000:6.2f}ms")


# ══════════════════════════════════════════════════════════════════════════════
# B3: Recursion Complexity Deep Dive
# ══════════════════════════════════════════════════════════════════════════════

def tribonacci(n):
    """
    Naive tribonacci: T(0)=0, T(1)=0, T(2)=1, T(n)=T(n-1)+T(n-2)+T(n-3).

    === Recurrence ===
    T(n) = T(n-1) + T(n-2) + T(n-3) + O(1)
    This is exponential (similar structure to Fibonacci but with THREE
    recursive calls instead of two) — informally, the branching factor
    per level is 3 in the worst analysis, though the TIGHT growth rate
    is governed by the "tribonacci constant" ≈ 1.839 (the real root of
    x^3 = x^2 + x + 1), analogous to how Fibonacci's tight rate is the
    golden ratio φ ≈ 1.618, not 2.
    ===================

    Examples:
        tribonacci(0) → 0
        tribonacci(2) → 1
        tribonacci(6) → 7   (0,0,1,1,2,4,7,...)
    """
    if n == 0 or n == 1:
        return 0
    if n == 2:
        return 1
    # TODO: naive recursive case
    pass


assert tribonacci(0) == 0
assert tribonacci(1) == 0
assert tribonacci(2) == 1
assert tribonacci(6) == 7


def tribonacci_memo(n, memo=None):
    """
    Memoized tribonacci. O(n) time.

    Examples:
        tribonacci_memo(20) should be fast (naive would be slow-ish)
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n == 0 or n == 1:
        return 0
    if n == 2:
        return 1
    # TODO: memoized recursive case
    pass


for i in range(10):
    assert tribonacci(i) == tribonacci_memo(i), f"Mismatch at n={i}"
print("✓ tribonacci / tribonacci_memo agree")

t0 = time.perf_counter(); tribonacci(24); t1 = time.perf_counter()
t2 = time.perf_counter(); tribonacci_memo(500); t3 = time.perf_counter()
print(f"  tribonacci(24) naive: {(t1-t0)*1000:.1f}ms   tribonacci_memo(500): {(t3-t2)*1000:.3f}ms")


def karatsuba_multiply(x, y):
    """
    Multiply two non-negative integers using Karatsuba's algorithm.

    === Recurrence ===
    T(n) = 3T(n/2) + O(n)
    By Master Theorem: a=3, b=2, f(n)=O(n)
    n^(log_b a) = n^(log2(3)) ≈ n^1.585
    Compare f(n)=n against n^1.585: f(n) is smaller → Case 1
    Result: T(n) = Θ(n^log2(3)) ≈ Θ(n^1.585)
    This beats naive O(n^2) multiplication for large n.
    ===================

    Algorithm (for numbers with the same number of digits, padded with
    leading zeros if needed):
        Split x into x_high, x_low (each roughly half the digits)
        Split y into y_high, y_low
        z2 = x_high * y_high            (recursive)
        z0 = x_low  * y_low             (recursive)
        z1 = (x_high+x_low)*(y_high+y_low) - z2 - z0   (recursive, 1 more mult)
        result = z2 * 10^n + z1 * 10^(n/2) + z0

    Args:
        x, y (int): non-negative integers

    Returns:
        int: x * y

    Examples:
        karatsuba_multiply(1234, 5678) → 7006652
        karatsuba_multiply(0, 100)     → 0
        karatsuba_multiply(9, 9)       → 81
    """
    # Base case: small numbers, multiply directly
    if x < 10 or y < 10:
        return x * y

    # Determine the number of digits (use the larger of the two)
    n = max(len(str(x)), len(str(y)))
    half = n // 2

    # Split x and y
    x_high, x_low = divmod(x, 10 ** half)
    y_high, y_low = divmod(y, 10 ** half)

    # TODO: recursive calls for z2, z0, z1 (per algorithm above)
    z2 = None  # x_high * y_high
    z0 = None  # x_low * y_low
    z1 = None  # (x_high+x_low)*(y_high+y_low) - z2 - z0

    return z2 * 10**(2*half) + z1 * 10**half + z0


assert karatsuba_multiply(1234, 5678) == 1234 * 5678
assert karatsuba_multiply(0, 100)      == 0
assert karatsuba_multiply(9, 9)        == 81
assert karatsuba_multiply(123456789, 987654321) == 123456789 * 987654321
print("✓ karatsuba_multiply")


def closest_pair_2d(points):
    """
    Find the pair of points with minimum Euclidean distance.
    Uses the classic divide-and-conquer algorithm.

    === Recurrence ===
    T(n) = 2T(n/2) + O(n)   (the strip check is O(n) given points
                              sorted by y within the strip)
    By Master Theorem (a=2,b=2,f(n)=n): Case 2 → T(n) = Θ(n log n)
    Compare to naive O(n^2) all-pairs check.
    ===================

    Args:
        points: list of (x, y) tuples, len(points) >= 2

    Returns:
        (point1, point2): the closest pair

    Examples:
        closest_pair_2d([(0,0), (3,4), (1,1)]) → ((0,0),(1,1))  distance sqrt(2)
    """
    def dist(p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def brute_force(pts):
        """Base case for small point sets — O(k^2) for small k."""
        best_pair = None
        best_dist = float('inf')
        for i in range(len(pts)):
            for j in range(i+1, len(pts)):
                d = dist(pts[i], pts[j])
                if d < best_dist:
                    best_dist = d
                    best_pair = (pts[i], pts[j])
        return best_pair, best_dist

    def solve(pts_sorted_x):
        if len(pts_sorted_x) <= 3:
            return brute_force(pts_sorted_x)

        mid = len(pts_sorted_x) // 2
        midpoint = pts_sorted_x[mid]

        left_pair, left_dist   = solve(pts_sorted_x[:mid])
        right_pair, right_dist = solve(pts_sorted_x[mid:])

        if left_dist < right_dist:
            best_pair, best_dist = left_pair, left_dist
        else:
            best_pair, best_dist = right_pair, right_dist

        # TODO: check the "strip" of points within best_dist of the midline
        # strip = [p for p in pts_sorted_x if abs(p[0] - midpoint[0]) < best_dist]
        # strip.sort(key=lambda p: p[1])
        # For each point in strip, only need to check the next few points
        # (a well-known geometric argument bounds this to a constant number)
        # Update best_pair, best_dist if a closer cross-strip pair is found

        return best_pair, best_dist

    assert len(points) >= 2, "Need at least 2 points"
    pts_sorted_x = sorted(points, key=lambda p: p[0])
    pair, _ = solve(pts_sorted_x)
    return pair


result = closest_pair_2d([(0,0), (3,4), (1,1)])
assert set(result) == {(0,0), (1,1)}, f"Expected (0,0) and (1,1), got {result}"
print("✓ closest_pair_2d")


# ══════════════════════════════════════════════════════════════════════════════
# B4: Amortized Analysis in Practice
# ══════════════════════════════════════════════════════════════════════════════

class DynamicArray:
    """
    A simple dynamic array that doubles capacity when full.
    Tracks total element copies for amortized analysis.
    """
    def __init__(self):
        self._capacity = 1
        self._size = 0
        self._array = [None] * self._capacity
        self.total_copies = 0    # instrumentation

    def __len__(self):
        return self._size

    def __getitem__(self, i):
        if i < 0 or i >= self._size:
            raise IndexError("index out of range")
        return self._array[i]

    def append(self, value):
        """
        Add value to the end. If the array is full, double capacity first
        (copying all existing elements to the new array).
        """
        if self._size == self._capacity:
            # TODO: resize — double capacity, copy all elements,
            # incrementing self.total_copies for EACH element copied
            new_capacity = self._capacity * 2
            new_array = [None] * new_capacity
            # TODO: copy loop
            self._array = new_array
            self._capacity = new_capacity

        self._array[self._size] = value
        self._size += 1


def measure_amortized_cost(n):
    """
    Create a DynamicArray, append n elements, return total_copies / n.

    This ratio should stay roughly bounded (a small constant) as n grows,
    demonstrating O(1) amortized cost per append.
    """
    arr = DynamicArray()
    for i in range(n):
        arr.append(i)
    return arr.total_copies / n


for n in [1000, 10000, 100000, 1000000]:
    ratio = measure_amortized_cost(n)
    print(f"  n={n:8}: amortized copies per append ≈ {ratio:.4f}")

print("✓ B4: amortized analysis")


# ══════════════════════════════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("All ps6.py assertions passed.")
    print("=" * 50)
