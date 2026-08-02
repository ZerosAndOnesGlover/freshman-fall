#!/usr/bin/env python3
"""
ps8.py
CS 101 — Problem Set 8: Hash Tables, Dictionaries, and Sets

Student: ____________________________
Date: ______________________________

Honor pledge: I wrote this code myself and understand every line.
Signed: ____________________________
"""

from collections import defaultdict
import time


# ══════════════════════════════════════════════════════════════════════════════
# B1: Custom Hash Table Extensions
# ══════════════════════════════════════════════════════════════════════════════

class ChainedHashTable:
    """ChainedHashTable from lab, extended with dict-like methods for PS8."""

    def __init__(self, initial_size=8):
        self._size = initial_size
        self._buckets = [[] for _ in range(self._size)]
        self._count = 0
        self._max_load_factor = 0.75

    def _index(self, key, size=None):
        size = size if size is not None else self._size
        return hash(key) % size

    def load_factor(self):
        return self._count / self._size

    def _resize(self):
        old_buckets = self._buckets
        self._size *= 2
        self._buckets = [[] for _ in range(self._size)]
        for chain in old_buckets:
            for key, value in chain:
                idx = self._index(key)
                self._buckets[idx].append((key, value))

    def put(self, key, value):
        idx = self._index(key)
        chain = self._buckets[idx]
        for i, (k, v) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)
                return
        chain.append((key, value))
        self._count += 1
        if self.load_factor() > self._max_load_factor:
            self._resize()

    def get(self, key):
        idx = self._index(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        raise KeyError(key)

    def __len__(self):
        return self._count

    # ── New methods for PS8 ────────────────────────────────────────────────

    def keys(self):
        """Return a list of all keys. O(n)."""
        # TODO
        pass

    def values(self):
        """Return a list of all values. O(n)."""
        # TODO
        pass

    def items(self):
        """Return a list of (key, value) tuples. O(n)."""
        # TODO
        pass

    def update(self, other_dict):
        """Insert all key-value pairs from a Python dict. O(k) average."""
        # TODO
        pass

    def __contains__(self, key):
        """Enable `key in my_hash_table` syntax."""
        # TODO: try self.get(key) in a try/except, or reimplement the scan directly
        pass


cht = ChainedHashTable()
cht.put("a", 1)
cht.put("b", 2)
cht.put("c", 3)
assert sorted(cht.keys())   == ["a", "b", "c"]
assert sorted(cht.values()) == [1, 2, 3]
assert sorted(cht.items())  == [("a",1), ("b",2), ("c",3)]

cht.update({"d": 4, "e": 5})
assert len(cht) == 5
assert cht.get("d") == 4

assert ("a" in cht) == True
assert ("z" in cht) == False
print("✓ B1: ChainedHashTable extensions")


# ══════════════════════════════════════════════════════════════════════════════
# B2: Refactoring Earlier Algorithms With Dict/Set
# ══════════════════════════════════════════════════════════════════════════════

def has_duplicate_pair_fast(lst):
    """
    O(n) — using a set. (Compare to O(n^2) nested-loop version from earlier weeks.)

    Examples:
        has_duplicate_pair_fast([1,2,3,2])  → True
        has_duplicate_pair_fast([1,2,3])    → False
    """
    # TODO
    pass


assert has_duplicate_pair_fast([1,2,3,2]) == True
assert has_duplicate_pair_fast([1,2,3])   == False
print("✓ has_duplicate_pair_fast")


def word_frequency_fast(text):
    """
    O(n) — using a dict. (Week 3's version was O(n^2) with no dicts allowed.)

    Returns dict: word -> count (lowercase, whitespace-split).
    """
    # TODO
    pass


wf = word_frequency_fast("the cat sat on the mat the cat ran")
assert wf["the"] == 3
assert wf["cat"] == 2
print("✓ word_frequency_fast")


def is_anagram_fast(s1, s2):
    """
    O(n) — using frequency dicts. (Week 2's version forbade dicts/sets/sorting.)
    """
    # TODO
    pass


assert is_anagram_fast("listen", "silent") == True
assert is_anagram_fast("hello", "world")    == False
print("✓ is_anagram_fast")


def find_missing_number(nums):
    """
    Given a list of n distinct numbers from 0 to n (one is missing),
    find the missing number. O(n) using a set.

    (Alternative: sum(range(n+1)) - sum(nums) also works in O(n) with
    O(1) extra space — mention this in your understanding, but implement
    the set-based version here.)

    Examples:
        find_missing_number([3,0,1])     → 2
        find_missing_number([0,1])       → 2
        find_missing_number([9,6,4,2,3,5,7,0,1]) → 8
    """
    # TODO
    pass


assert find_missing_number([3,0,1]) == 2
assert find_missing_number([0,1])   == 2
assert find_missing_number([9,6,4,2,3,5,7,0,1]) == 8
print("✓ find_missing_number")


def longest_consecutive_sequence(nums):
    """
    Find the length of the longest run of consecutive integers
    (consecutive in VALUE, not necessarily adjacent in the list).
    O(n) using a set.

    Key trick: for each number, only start counting a sequence if
    (number - 1) is NOT in the set (i.e., this number is the start
    of a potential sequence). This ensures each sequence is only
    counted once, keeping the algorithm O(n) instead of O(n^2).

    Examples:
        longest_consecutive_sequence([100,4,200,1,3,2]) → 4  (1,2,3,4)
        longest_consecutive_sequence([])                  → 0
        longest_consecutive_sequence([1,2,0,1])           → 3  (0,1,2)
    """
    if not nums:
        return 0

    num_set = set(nums)
    longest = 0

    # TODO: for each num in num_set, if num-1 not in num_set (it's a
    # sequence start), count forward (num, num+1, num+2, ...) while
    # each is in num_set, tracking the length

    return longest


assert longest_consecutive_sequence([100,4,200,1,3,2]) == 4
assert longest_consecutive_sequence([])                 == 0
assert longest_consecutive_sequence([1,2,0,1])           == 3
print("✓ longest_consecutive_sequence")


def group_by_first_letter(words):
    """
    Group words by their first letter using defaultdict.
    Return a regular dict (not defaultdict) mapping letter -> list of words,
    preserving first-appearance order within each group.

    Examples:
        group_by_first_letter(["cat","car","dog","cow"])
        → {'c': ['cat','car','cow'], 'd': ['dog']}
    """
    groups = defaultdict(list)
    # TODO: populate groups
    return dict(groups)


g = group_by_first_letter(["cat","car","dog","cow"])
assert g == {'c': ['cat','car','cow'], 'd': ['dog']}
print("✓ group_by_first_letter")


# ══════════════════════════════════════════════════════════════════════════════
# B3: Two-Sum Family of Problems
# ══════════════════════════════════════════════════════════════════════════════

def two_sum(nums, target):
    """O(n) — return (i, j) indices of two numbers summing to target, or None."""
    # TODO
    pass


assert two_sum([2, 7, 11, 15], 9) == (0, 1)
assert two_sum([3, 2, 4], 6)       == (1, 2)
print("✓ two_sum")


def three_sum_zero(nums):
    """
    Return all UNIQUE triplets (as sorted tuples) summing to zero.

    Approach: sort nums, then for each index i, use two-pointer
    technique on the remainder to find pairs summing to -nums[i].
    Skip duplicate values to avoid duplicate triplets.

    Examples:
        three_sum_zero([-1,0,1,2,-1,-4]) → [(-1,-1,2), (-1,0,1)]  (order may vary)
    """
    nums = sorted(nums)
    n = len(nums)
    result = []

    for i in range(n):
        if i > 0 and nums[i] == nums[i-1]:
            continue   # skip duplicate "first" elements

        # TODO: two-pointer search in nums[i+1:] for pairs summing to -nums[i]
        # Remember to also skip duplicate values for lo/hi to avoid duplicate triplets

        pass

    return result


result = three_sum_zero([-1,0,1,2,-1,-4])
assert sorted(result) == sorted([(-1,-1,2), (-1,0,1)])
print("✓ three_sum_zero")


def two_sum_all_pairs(nums, target):
    """
    Return ALL pairs of indices (i,j) with i<j such that nums[i]+nums[j]==target.
    Handle repeated values correctly.

    Examples:
        two_sum_all_pairs([3,3,3], 6) → [(0,1),(0,2),(1,2)]
        two_sum_all_pairs([1,2,3,4], 100) → []
    """
    result = []
    # TODO: use a dict mapping value -> list of indices seen so far
    return result


pairs = two_sum_all_pairs([3,3,3], 6)
assert sorted(pairs) == [(0,1),(0,2),(1,2)]
assert two_sum_all_pairs([1,2,3,4], 100) == []
print("✓ two_sum_all_pairs")


def four_sum_count(A, B, C, D):
    """
    Count tuples (i,j,k,l) such that A[i]+B[j]+C[k]+D[l] == 0.
    O(n^2) using a dict of pairwise sums (naive would be O(n^4)).

    Algorithm:
        1. Compute all sums a+b for a in A, b in B; store counts in a dict. O(n^2)
        2. For each c in C, d in D, look up -(c+d) in that dict. O(n^2)

    Examples:
        four_sum_count([1,2],[-2,-1],[-1,2],[0,2]) → 2
    """
    ab_sums = defaultdict(int)
    # TODO: populate ab_sums with counts of all a+b combinations

    count = 0
    # TODO: for each c, d pair, look up -(c+d) in ab_sums and add its count

    return count


assert four_sum_count([1,2],[-2,-1],[-1,2],[0,2]) == 2
print("✓ four_sum_count")


# ══════════════════════════════════════════════════════════════════════════════
# B4: A Simple Memoization Decorator
# ══════════════════════════════════════════════════════════════════════════════

def memoize(func):
    """
    Decorator: cache results of func in a dict keyed by its single argument.
    Supports functions with exactly one hashable positional argument.
    """
    cache = {}

    def wrapper(x):
        # TODO: check cache, compute+store if missing, return result
        pass

    return wrapper


@memoize
def slow_square(x):
    time.sleep(0.01)
    return x * x

t0 = time.perf_counter(); slow_square(5); t1 = time.perf_counter()
t2 = time.perf_counter(); slow_square(5); t3 = time.perf_counter()
assert slow_square(5) == 25
assert (t3 - t2) < (t1 - t0) * 0.1, "Second call should be much faster (cached)"
print("✓ memoize")


def memoize_with_stats(func):
    """
    Like memoize, but the wrapped function exposes .cache_hits and
    .cache_misses as attributes.
    """
    cache = {}

    def wrapper(x):
        # TODO: check cache; on hit increment wrapper.cache_hits and return
        # cached value; on miss increment wrapper.cache_misses, compute,
        # store, and return
        pass

    wrapper.cache_hits = 0
    wrapper.cache_misses = 0
    return wrapper


@memoize_with_stats
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


result = fib(20)
assert result == 6765
print(f"✓ memoize_with_stats: fib(20)={result}, "
      f"hits={fib.cache_hits}, misses={fib.cache_misses}")
assert fib.cache_misses == 21, f"Expected 21 unique subproblems, got {fib.cache_misses}"


# ══════════════════════════════════════════════════════════════════════════════
# B5: Set Theory Applications
# ══════════════════════════════════════════════════════════════════════════════

def jaccard_similarity(set_a, set_b):
    """
    Return |A ∩ B| / |A ∪ B|.

    Examples:
        jaccard_similarity({1,2,3}, {2,3,4}) → 0.5
        jaccard_similarity(set(), set())     → handle this edge case (return 0.0 or 1.0? — document your choice)
    """
    # TODO
    pass


assert jaccard_similarity({1,2,3}, {2,3,4}) == 0.5
assert jaccard_similarity({1,2}, {1,2})     == 1.0
print("✓ jaccard_similarity")


def find_common_words(text1, text2):
    """
    Return the set of words appearing in BOTH texts (case-insensitive).
    Use set intersection.
    """
    # TODO
    pass


common = find_common_words("The Cat Sat", "the dog sat there")
assert common == {"the", "sat"}
print("✓ find_common_words")


def symmetric_difference_report(set_a, set_b, name_a="A", name_b="B"):
    """
    Print a formatted report: elements only in A, only in B, in both.
    Use set operations (not manual loops) to compute each category.
    """
    only_a = set_a - set_b
    only_b = set_b - set_a
    both    = set_a & set_b

    print(f"Only in {name_a}: {sorted(only_a)}")
    print(f"Only in {name_b}: {sorted(only_b)}")
    print(f"In both: {sorted(both)}")


symmetric_difference_report({1,2,3}, {2,3,4}, "Set1", "Set2")


def are_disjoint(set_a, set_b):
    """
    Return True if set_a and set_b share no elements.
    O(min(len(a), len(b))) — use set.isdisjoint(), which is more
    efficient than computing the full intersection because it can
    return False as soon as ONE common element is found, without
    building the entire intersection set.
    """
    # TODO
    pass


assert are_disjoint({1,2,3}, {4,5,6}) == True
assert are_disjoint({1,2,3}, {3,4,5}) == False
print("✓ are_disjoint")


# ══════════════════════════════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("All ps8.py assertions passed.")
    print("=" * 50)
