#!/usr/bin/env python3
"""
recursion_lab.py
CS 101 — Week 4, Lab 4 Starter

Recursive implementations with correctness arguments.
All functions: docstring with base case + inductive step, assert tests.

Student: ____________________________
Date: ______________________________
"""

import time
import sys


# ─── Exercise 2.1: Fast Power ─────────────────────────────────────────────────

def fast_power(base, exp):
    """
    Compute base**exp using O(log exp) multiplications.

    Key insight:
        base^exp = (base^(exp//2))^2      if exp is even
        base^exp = base * base^(exp-1)    if exp is odd
        base^0   = 1                       base case

    === Correctness ===
    Base:    fast_power(base, 0) = 1 = base^0  ✓
    Even:    (base^(n/2))^2 = base^n  ✓
    Odd:     base * base^(n-1) = base^n  ✓
    ===================

    Args:
        base (int or float): the base
        exp  (int):          non-negative exponent

    Returns:
        base**exp

    Examples:
        fast_power(2, 10)  → 1024
        fast_power(2, 0)   → 1
        fast_power(3, 4)   → 81
    """
    assert isinstance(exp, int) and exp >= 0, f"exp must be a non-negative int, got {exp}"

    # TODO: implement
    # if exp == 0: return 1
    # if exp % 2 == 0: half = fast_power(...); return half * half
    # else: return base * fast_power(base, exp - 1)
    pass


assert fast_power(2, 0)   == 1,    f"fast_power(2,0): {fast_power(2,0)}"
assert fast_power(2, 1)   == 2,    f"fast_power(2,1): {fast_power(2,1)}"
assert fast_power(2, 10)  == 1024, f"fast_power(2,10): {fast_power(2,10)}"
assert fast_power(3, 4)   == 81,   f"fast_power(3,4): {fast_power(3,4)}"
assert fast_power(10, 3)  == 1000, f"fast_power(10,3): {fast_power(10,3)}"
# Verify matches built-in:
for b in [2, 3, 5, 7]:
    for e in range(15):
        assert fast_power(b, e) == b**e, f"Mismatch at {b}**{e}"
print("✓ fast_power")


# ─── Exercise 2.2: Merge Sort ─────────────────────────────────────────────────

def merge(left, right):
    """
    Merge two sorted lists into one sorted list.
    Time: O(len(left) + len(right)).

    Maintain two indices i, j into left and right.
    At each step, append the smaller front element and advance that index.
    After one list is exhausted, append the rest of the other.

    === Loop Invariant ===
    result contains all elements from left[:i] and right[:j] in sorted order.
    ======================
    """
    result = []
    i = j = 0

    # TODO: while loop comparing left[i] and right[j]
    # After loop: extend result with leftover elements

    return result


def merge_sort(lst):
    """
    Sort lst and return a new sorted list using merge sort.
    Time: O(n log n).  Space: O(n).

    === Correctness ===
    Base:  [] and [x] are trivially sorted.  ✓
    Step:  Assume merge_sort correctly sorts any list of size < n (IH).
           Left half (size ≤ n//2 < n) → sorted by IH.
           Right half (size ≤ n//2 < n) → sorted by IH.
           merge() of two sorted lists → sorted list.
           Therefore merge_sort(lst) is sorted.  ✓
    ===================

    Examples:
        merge_sort([3, 1, 4, 1, 5]) → [1, 1, 3, 4, 5]
        merge_sort([])              → []
        merge_sort([1])             → [1]
    """
    # TODO: base case + divide + conquer + combine
    pass


assert merge_sort([])            == [],          "empty"
assert merge_sort([1])           == [1],         "single"
assert merge_sort([3, 1, 2])     == [1, 2, 3],   "three"
assert merge_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5], "reverse"
assert merge_sort([3, 3, 1, 1])  == [1, 1, 3, 3], "duplicates"
# Stability check: equal elements keep relative order
pairs = [(1, 'b'), (1, 'a'), (2, 'c')]
# Note: merge_sort compares by full tuple; this is a general correctness check
assert merge_sort([5, 2, 8, 1, 9]) == [1, 2, 5, 8, 9]
print("✓ merge_sort")


# ─── Exercise 2.3: Binary Search ──────────────────────────────────────────────

def binary_search(lst, target, lo=0, hi=None):
    """
    Return index of target in sorted lst[lo..hi], or -1 if not found.
    Time: O(log n).

    === Loop Invariant (restated as recursive invariant) ===
    If target is in lst, it is in lst[lo..hi].
    =========================================================

    === Correctness ===
    Base:  lo > hi → search space empty → return -1.  ✓
    Step:  Invariant is maintained by each branch:
           lst[mid] < target → target not in lst[lo..mid]   → search right  ✓
           lst[mid] > target → target not in lst[mid..hi]   → search left   ✓
           lst[mid] == target → found at mid                → return mid     ✓
    ===================

    Examples:
        binary_search([1, 3, 5, 7, 9], 5)  → 2
        binary_search([1, 3, 5, 7, 9], 4)  → -1
        binary_search([], 1)                → -1
    """
    if hi is None:
        hi = len(lst) - 1

    # TODO: base case + three-way branch
    pass


lst9 = [1, 3, 5, 7, 9, 11, 13]
assert binary_search(lst9, 7)   == 3,  f"found 7: {binary_search(lst9,7)}"
assert binary_search(lst9, 1)   == 0,  f"found 1: {binary_search(lst9,1)}"
assert binary_search(lst9, 13)  == 6,  f"found 13: {binary_search(lst9,13)}"
assert binary_search(lst9, 4)   == -1, f"missing 4"
assert binary_search(lst9, 0)   == -1, f"missing 0 (below range)"
assert binary_search(lst9, 15)  == -1, f"missing 15 (above range)"
assert binary_search([], 5)     == -1, f"empty list"
print("✓ binary_search")


# ─── Exercise 2.4: Fibonacci with memoization ─────────────────────────────────

def fib_naive(n):
    """Naive Fibonacci — O(2^n). Only use for n ≤ 30."""
    if n <= 1:
        return n
    return fib_naive(n-1) + fib_naive(n-2)


def fib_memo(n, memo=None):
    """
    Fibonacci with top-down memoization. O(n) time, O(n) space.

    Store computed results in memo dict to avoid recomputation.
    Each of the n distinct subproblems is solved exactly once.

    === Correctness ===
    Same as fib_naive (memoization doesn't change the result, only speed).
    Each fib_memo(k) returns fib(k) by induction:
        Base: fib_memo(0)=0, fib_memo(1)=1  ✓
        Step: fib_memo(n) = fib_memo(n-1) + fib_memo(n-2)
                          = fib(n-1) + fib(n-2) (IH)
                          = fib(n)  ✓
    ===================

    Examples:
        fib_memo(10) → 55
        fib_memo(50) → 12586269025
    """
    if memo is None:
        memo = {}

    # TODO:
    # 1. Check if n is in memo → return memo[n]
    # 2. Base cases: n <= 1 → return n
    # 3. Compute, store in memo[n], return
    pass


# Correctness:
for i in range(15):
    assert fib_naive(i) == fib_memo(i), f"Mismatch at n={i}"
assert fib_memo(50) == 12586269025

# Performance:
t0 = time.perf_counter(); fib_naive(30); t1 = time.perf_counter()
t2 = time.perf_counter(); fib_memo(300); t3 = time.perf_counter()
print(f"✓ fib_memo — naive(30): {(t1-t0)*1000:.1f}ms  memo(300): {(t3-t2)*1000:.3f}ms")


# ─── Exercise 2.5: Tower of Hanoi ─────────────────────────────────────────────

def hanoi(n, source='A', destination='C', auxiliary='B', verbose=False):
    """
    Print the moves for the Tower of Hanoi puzzle with n disks.
    Returns the total number of moves.

    Formula: T(n) = 2^n - 1.

    === Recurrence ===
    T(1) = 1
    T(n) = T(n-1) + 1 + T(n-1) = 2·T(n-1) + 1

    === Proof by induction that T(n) = 2^n - 1 ===
    Base: T(1) = 1 = 2^1 - 1  ✓
    Step: T(n) = 2·T(n-1) + 1
               = 2·(2^(n-1) - 1) + 1   (by IH)
               = 2^n - 2 + 1
               = 2^n - 1  ✓
    ================================================

    Args:
        n:           number of disks (positive integer)
        source:      name of source peg
        destination: name of destination peg
        auxiliary:   name of auxiliary peg
        verbose:     if True, print each move

    Returns:
        int: total moves (= 2^n - 1)
    """
    # TODO:
    # Base case: n == 1 → one move, return 1
    # Recursive:
    #   moves  = hanoi(n-1, source, auxiliary, destination, verbose)
    #   if verbose: print the big disk move
    #   moves += 1
    #   moves += hanoi(n-1, auxiliary, destination, source, verbose)
    #   return moves
    pass


# Verify formula:
for n in range(1, 12):
    assert hanoi(n, verbose=False) == 2**n - 1, f"Formula wrong at n={n}"
print("✓ hanoi — 2^n - 1 formula verified for n=1..11")

print("\nHanoi n=3 moves:")
hanoi(3, verbose=True)


# ─── Exercise 2.6: Permutations ───────────────────────────────────────────────

def permutations(lst):
    """
    Return all permutations of lst as a list of lists.
    Uses choose-explore-unchoose (backtracking).

    Total: n! permutations for a list of n elements.

    === Correctness ===
    Base: permutations([]) = [[]], permutations([x]) = [[x]]  ✓
    Step: Every permutation of lst starts with some element lst[i].
          For each i: put lst[i] first (swap), recurse on the rest (n-1)!
          perms, then restore swap (unchoose).
          Total: n * (n-1)! = n! permutations.  ✓
    ===================

    Examples:
        permutations([])      → [[]]
        permutations([1])     → [[1]]
        permutations([1,2])   → [[1,2],[2,1]]
        permutations([1,2,3]) → 6 permutations
    """
    if len(lst) <= 1:
        return [lst[:]]

    result = []
    lst = lst[:]    # work on a copy

    for i in range(len(lst)):
        # TODO: CHOOSE, EXPLORE, UNCHOOSE
        pass

    return result


assert permutations([]) == [[]]
assert permutations([1]) == [[1]]
assert len(permutations([1, 2, 3])) == 6
assert sorted(permutations([1, 2])) == [[1, 2], [2, 1]]
# Verify all unique:
p3 = permutations([1, 2, 3])
assert len(set(map(tuple, p3))) == 6, "All permutations should be unique"
print("✓ permutations")


# ─── Summary ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("All tests passed!")
    print("=" * 50)
