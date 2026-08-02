#!/usr/bin/env python3
"""
ps4.py
CS 101 — Problem Set 4: Recursion

Student: ____________________________
Date: ______________________________

Honor pledge: I wrote this code myself and understand every line.
Signed: ____________________________
"""


# ══════════════════════════════════════════════════════════════════════════════
# B1: Recursive List Operations
# ══════════════════════════════════════════════════════════════════════════════

def recursive_min(lst):
    """
    Return the minimum value in a non-empty list, recursively.

    Base case:     single-element list → return that element
    Recursive case: min(lst) = min(lst[0], recursive_min(lst[1:]))

    === Correctness ===
    Base: min([x]) = x  ✓
    Step: min of n elements = min of first element vs. min of remaining n-1. ✓
    ===================

    Args:
        lst (list): non-empty list of comparable elements

    Returns:
        the minimum element

    Examples:
        recursive_min([3, 1, 4, 1, 5]) → 1
        recursive_min([7])             → 7
    """
    assert lst, "recursive_min requires a non-empty list"
    # TODO
    pass


assert recursive_min([3, 1, 4, 1, 5]) == 1
assert recursive_min([7])             == 7
assert recursive_min([-5, 0, 5])      == -5
assert recursive_min([1])             == 1


def count_if(lst, predicate, i=0):
    """
    Count elements in lst satisfying predicate, using index-based recursion.
    O(n) time — no slicing.

    Base case:     i == len(lst) → 0
    Recursive case: (1 if predicate(lst[i]) else 0) + count_if(lst, predicate, i+1)

    Args:
        lst       (list):     the list to search
        predicate (callable): function returning True/False
        i         (int):      current index (default 0)

    Returns:
        int: count of elements satisfying predicate

    Examples:
        count_if([1,2,3,4,5], lambda x: x % 2 == 0) → 2
        count_if([1,2,3], lambda x: x > 10)          → 0
    """
    # TODO: use index i, not slicing
    pass


assert count_if([1,2,3,4,5], lambda x: x % 2 == 0) == 2
assert count_if([1,2,3], lambda x: x > 10)          == 0
assert count_if([], lambda x: True)                  == 0
assert count_if(["a","bb","ccc"], lambda s: len(s) > 1) == 2


def flatten(lst):
    """
    Flatten an arbitrarily nested list structure into a flat list.

    Base case:     empty list → []
    Recursive case:
        if lst[0] is a list → flatten(lst[0]) + flatten(lst[1:])
        else                → [lst[0]] + flatten(lst[1:])

    === Correctness ===
    Base: flatten([]) = []  ✓
    Step: Assume flatten works for any shorter list.
          If first element is a list → flatten it, then append flat rest. ✓
          If first element is not a list → prepend it to flat rest. ✓
    ===================

    Examples:
        flatten([1,[2,[3]],4])     → [1,2,3,4]
        flatten([])                → []
        flatten([[[]]])            → []
    """
    # TODO
    pass


assert flatten([])                    == []
assert flatten([1,2,3])               == [1,2,3]
assert flatten([1,[2,[3]],4])         == [1,2,3,4]
assert flatten([[[]]])                == []
assert flatten([1,[2,[3,[4,[5]]]]])   == [1,2,3,4,5]


def all_pairs(lst, i=0):
    """
    Return all pairs (lst[i], lst[j]) where i < j, as a list of tuples.
    Use index i to avoid repeated slicing.

    Base case:     i >= len(lst)-1 → []
    Recursive case:
        pairs starting with lst[i]: [(lst[i], lst[j]) for j in range(i+1, len(lst))]
        + all_pairs(lst, i+1)

    Examples:
        all_pairs([1,2,3]) → [(1,2),(1,3),(2,3)]
        all_pairs([1])     → []
        all_pairs([])      → []
    """
    # TODO
    pass


assert all_pairs([])      == []
assert all_pairs([1])     == []
assert all_pairs([1,2])   == [(1,2)]
assert all_pairs([1,2,3]) == [(1,2),(1,3),(2,3)]
assert len(all_pairs([1,2,3,4])) == 6   # C(4,2) = 6


def zip_lists(lst1, lst2):
    """
    Zip two lists into a list of pairs. Stop at the shorter list.
    Do NOT use Python's built-in zip().

    Base case:     either list is empty → []
    Recursive case: [(lst1[0], lst2[0])] + zip_lists(lst1[1:], lst2[1:])

    Examples:
        zip_lists([1,2,3],[4,5,6]) → [(1,4),(2,5),(3,6)]
        zip_lists([1,2],[4,5,6])   → [(1,4),(2,5)]
        zip_lists([],[1,2])        → []
    """
    # TODO
    pass


assert zip_lists([1,2,3],[4,5,6])   == [(1,4),(2,5),(3,6)]
assert zip_lists([1,2],[4,5,6])     == [(1,4),(2,5)]
assert zip_lists([],[1,2])          == []
assert zip_lists([1,2,3],[])        == []


def deep_sum(lst):
    """
    Sum all numbers in a (possibly nested) list.

    Base case:     empty list → 0
    Recursive case:
        if lst[0] is a list → deep_sum(lst[0]) + deep_sum(lst[1:])
        else                → lst[0] + deep_sum(lst[1:])

    Examples:
        deep_sum([1,[2,[3]],4])  → 10
        deep_sum([])             → 0
        deep_sum([[1,2],[3,4]])  → 10
    """
    # TODO
    pass


assert deep_sum([])             == 0
assert deep_sum([1,2,3])        == 6
assert deep_sum([1,[2,[3]],4])  == 10
assert deep_sum([[1,2],[3,4]])  == 10


print("✓ B1: all list operations")


# ══════════════════════════════════════════════════════════════════════════════
# B2: Recursive String Operations
# ══════════════════════════════════════════════════════════════════════════════

def count_vowels(s, i=0):
    """
    Count vowels (aeiou, case-insensitive) in s using index-based recursion.
    No loops, no list comprehensions.

    Base case:     i == len(s) → 0
    Recursive case: (1 if s[i].lower() in 'aeiou' else 0) + count_vowels(s, i+1)

    Examples:
        count_vowels("hello")   → 2
        count_vowels("rhythm")  → 0
        count_vowels("")        → 0
    """
    # TODO
    pass


assert count_vowels("hello")   == 2
assert count_vowels("rhythm")  == 0
assert count_vowels("")        == 0
assert count_vowels("AEIOU")   == 5


def reverse_words(sentence):
    """
    Reverse the order of words in sentence.
    Implement recursively — no [::-1] on the word list.

    Base case:     0 or 1 words → return sentence unchanged
    Recursive case: last_word + ' ' + reverse_words(all_but_last)

    Examples:
        reverse_words("hello world foo") → "foo world hello"
        reverse_words("one")             → "one"
        reverse_words("")                → ""
    """
    words = sentence.split()
    if len(words) <= 1:
        return sentence

    # TODO: recursive structure on the word list
    pass


assert reverse_words("hello world foo") == "foo world hello"
assert reverse_words("one")             == "one"
assert reverse_words("")                == ""
assert reverse_words("a b")            == "b a"


def is_balanced(s, depth=0, i=0):
    """
    Return True if every '(' in s is matched by a ')'.
    Use a recursive depth counter.

    Base case:     i == len(s) → depth == 0
    Rules:
        '(' → recurse with depth+1
        ')' → if depth == 0: False (unmatched close)
               else recurse with depth-1
        other → recurse with same depth

    === Correctness ===
    depth tracks unmatched '(' seen so far.
    At end: depth==0 means all opens were closed.  ✓
    depth<0 means a ')' appeared before its '('.  ✓
    ===================

    Examples:
        is_balanced("(()())")  → True
        is_balanced("(()")     → False
        is_balanced(")")       → False
        is_balanced("")        → True
    """
    # TODO
    pass


assert is_balanced("(()())")  == True
assert is_balanced("(()")     == False
assert is_balanced(")")       == False
assert is_balanced("")        == True
assert is_balanced("()")      == True
assert is_balanced("((()))")  == True
assert is_balanced(")(")      == False


def interleave(s1, s2):
    """
    Interleave two strings character by character.
    If one is longer, append its remaining characters.

    Base case:     either string is empty → return the other
    Recursive case: s1[0] + s2[0] + interleave(s1[1:], s2[1:])
                    (if s2 is empty: s1[0] + interleave(s1[1:], ""))

    Examples:
        interleave("abc","def")   → "adbecf"
        interleave("ab","defg")   → "adbefg"
        interleave("","abc")      → "abc"
    """
    # TODO
    pass


assert interleave("abc","def")   == "adbecf"
assert interleave("ab","defg")   == "adbefg"
assert interleave("","abc")      == "abc"
assert interleave("abc","")      == "abc"
assert interleave("","")         == ""


def longest_run(s, i=0, current_run=0, best=0):
    """
    Return the length of the longest run of identical consecutive characters.

    Base case:     i == len(s) → best
    Recursive case:
        if i==0 or s[i] != s[i-1]: new run starts (current_run=1)
        else: current_run += 1
        best = max(best, current_run)
        recurse with i+1

    Examples:
        longest_run("aaabbbcccc") → 4
        longest_run("a")          → 1
        longest_run("")           → 0
    """
    # TODO
    pass


assert longest_run("aaabbbcccc") == 4
assert longest_run("a")          == 1
assert longest_run("")           == 0
assert longest_run("aabbaa")     == 2
assert longest_run("abcde")      == 1


print("✓ B2: all string operations")


# ══════════════════════════════════════════════════════════════════════════════
# B3: Divide and Conquer
# ══════════════════════════════════════════════════════════════════════════════

def fast_power(base, exp):
    """
    Compute base**exp in O(log exp) multiplications.
    See lab for full docstring.
    """
    assert isinstance(exp, int) and exp >= 0
    if exp == 0: return 1
    if exp % 2 == 0:
        half = fast_power(base, exp // 2)
        return half * half
    return base * fast_power(base, exp - 1)


def merge(left, right):
    """Merge two sorted lists. O(n)."""
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(lst):
    """Sort lst recursively. O(n log n)."""
    if len(lst) <= 1: return lst[:]
    mid = len(lst) // 2
    return merge(merge_sort(lst[:mid]), merge_sort(lst[mid:]))


def find_rotation_point(lst, lo=0, hi=None):
    """
    Find the index of the minimum element in a rotated sorted list.
    A rotated sorted list: [4,5,6,7,1,2,3] — rotated sorted ascending list.

    Time: O(log n).

    Base case:     lo == hi → return lo
    Key insight:   if lst[mid] > lst[hi], minimum is in right half.
                   else minimum is in left half (including mid).

    === Correctness ===
    Invariant: the minimum is always in lst[lo..hi].
    At each step: compare lst[mid] with lst[hi].
        lst[mid] > lst[hi]: rotation point is in (mid, hi] → lo = mid+1
        lst[mid] <= lst[hi]: rotation point is in [lo, mid] → hi = mid
    Terminates when lo == hi.  ✓
    ===================

    Examples:
        find_rotation_point([4,5,6,7,1,2,3]) → 4
        find_rotation_point([1,2,3,4,5])     → 0
        find_rotation_point([2,1])           → 1
    """
    if hi is None:
        hi = len(lst) - 1
    # TODO
    pass


assert find_rotation_point([4,5,6,7,1,2,3]) == 4
assert find_rotation_point([1,2,3,4,5])     == 0
assert find_rotation_point([2,1])           == 1
assert find_rotation_point([3,4,5,1,2])     == 3


def count_inversions(lst):
    """
    Count the number of inversions in lst: pairs (i,j) where i<j and lst[i]>lst[j].

    Naive O(n²) implementation: check all pairs.

    Examples:
        count_inversions([3,1,2]) → 2
        count_inversions([1,2,3]) → 0
        count_inversions([3,2,1]) → 3
    """
    count = 0
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] > lst[j]:
                count += 1
    return count


assert count_inversions([3,1,2]) == 2
assert count_inversions([1,2,3]) == 0
assert count_inversions([3,2,1]) == 3
assert count_inversions([])      == 0


def closest_pair_1d(lst):
    """
    Given a sorted list of numbers, return the pair with smallest difference.

    Base case:     len(lst) == 2 → return (lst[0], lst[1])
    Recursive case:
        best_rest = closest_pair_1d(lst[1:])
        local_pair = (lst[0], lst[1])
        return whichever pair has the smaller difference

    Time: O(n) — linear scan disguised as recursion.

    Examples:
        closest_pair_1d([1,3,6,10,15]) → (1,3)
        closest_pair_1d([1,2])         → (1,2)
    """
    assert len(lst) >= 2, "Need at least 2 elements"
    # TODO
    pass


assert closest_pair_1d([1,3,6,10,15]) == (1,3)
assert closest_pair_1d([1,2])         == (1,2)
assert closest_pair_1d([1,5,5,10])    == (5,5)


print("✓ B3: divide and conquer")


# ══════════════════════════════════════════════════════════════════════════════
# B4: Backtracking
# ══════════════════════════════════════════════════════════════════════════════

def subsets(lst):
    """
    Return all subsets of lst (power set) as a list of lists.

    Base case:     [] → [[]]   (one subset: the empty set)
    Recursive case:
        rest = subsets(lst[1:])
        return rest + [s + [lst[0]] for s in rest]
        (subsets without lst[0]) ∪ (same subsets with lst[0] prepended)

    Examples:
        subsets([])      → [[]]
        subsets([1])     → [[], [1]]
        subsets([1,2,3]) → 8 subsets
    """
    # TODO
    pass


assert subsets([])  == [[]]
assert len(subsets([1,2,3])) == 8
assert [] in subsets([1,2,3])
assert [1,2,3] in subsets([1,2,3])


def combinations(lst, k, start=0):
    """
    Return all k-element subsets of lst.
    Use index start to avoid revisiting elements.

    Base case:     k == 0 → [[]]
    Recursive case:
        for each element at index i >= start:
            CHOOSE lst[i]
            EXPLORE combinations(lst, k-1, i+1)
            for each sub-combo: prepend lst[i]

    Examples:
        combinations([1,2,3,4], 2) → [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
        combinations([1,2,3], 0)   → [[]]
        combinations([1,2,3], 3)   → [[1,2,3]]
    """
    if k == 0:
        return [[]]
    if start >= len(lst):
        return []
    # TODO: for loop with CHOOSE/EXPLORE pattern
    pass


assert combinations([1,2,3], 0)   == [[]]
assert combinations([1,2,3], 3)   == [[1,2,3]]
assert len(combinations([1,2,3,4], 2)) == 6
assert [1,3] in combinations([1,2,3,4], 2)


def sum_subsets(lst, target, i=0, current=None):
    """
    Return all subsets of lst that sum to target.

    Backtracking: at each index, CHOOSE to include lst[i] or not.
    EXPLORE both branches.

    Base case:     i == len(lst) → if sum(current)==target: [current[:]] else []
    Recursive case:
        without = sum_subsets(lst, target, i+1, current)
        current.append(lst[i])
        with_i  = sum_subsets(lst, target, i+1, current)
        current.pop()
        return without + with_i

    Examples:
        sum_subsets([2,4,6,8], 10) → [[2,8],[4,6]]  (order may vary)
        sum_subsets([1,2,3], 7)    → []
    """
    if current is None:
        current = []
    # TODO
    pass


result_10 = sum_subsets([2,4,6,8], 10)
assert len(result_10) == 2
assert sorted([2,8]) in [sorted(s) for s in result_10]
assert sorted([4,6]) in [sorted(s) for s in result_10]
assert sum_subsets([1,2,3], 7) == []


def word_break(s, words, memo=None):
    """
    Return True if s can be formed by concatenating words from the list.
    Add memoization to handle overlapping subproblems.

    Recurrence:
        word_break("") = True
        word_break(s) = any(word_break(s[len(w):]) for w in words if s.startswith(w))

    Examples:
        word_break("leetcode", ["leet","code"])           → True
        word_break("applepenapple", ["apple","pen"])      → True
        word_break("catsandog", ["cats","dog","sand","and","cat"]) → False
    """
    if memo is None:
        memo = {}
    if s in memo:
        return memo[s]
    if s == "":
        return True
    # TODO: try each word as a prefix; recurse on the rest
    pass


assert word_break("leetcode", ["leet","code"])           == True
assert word_break("applepenapple", ["apple","pen"])      == True
assert word_break("catsandog", ["cats","dog","sand","and","cat"]) == False
assert word_break("", ["a"])                             == True


def generate_parentheses(n, open_count=0, close_count=0, current="", result=None):
    """
    Generate all strings of n pairs of balanced parentheses.

    Rules:
        Can add '(' if open_count < n
        Can add ')' if close_count < open_count
        Done when open_count == close_count == n

    Examples:
        generate_parentheses(1) → ["()"]
        generate_parentheses(2) → ["(())", "()()"]
        generate_parentheses(3) → 5 strings
    """
    if result is None:
        result = []
    # TODO: base case + two branches (add '(' or add ')')
    pass


assert generate_parentheses(1) == ["()"]
assert len(generate_parentheses(2)) == 2
assert len(generate_parentheses(3)) == 5
assert "(())" in generate_parentheses(2)
assert "()()" in generate_parentheses(2)


print("✓ B4: backtracking")


# ══════════════════════════════════════════════════════════════════════════════
# B5: Memoization
# ══════════════════════════════════════════════════════════════════════════════

def fib_memo(n, memo=None):
    """Fibonacci with memoization. O(n)."""
    if memo is None: memo = {}
    if n in memo: return memo[n]
    if n <= 1: return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]


def catalan(n, memo=None):
    """
    Return the nth Catalan number.
    C(0)=1, C(1)=1, C(n)=sum(C(i)*C(n-1-i) for i in 0..n-1)

    Add memoization. Catalan numbers grow exponentially without it.

    Examples:
        catalan(0) → 1
        catalan(5) → 42
        catalan(10) → 16796
    """
    if memo is None: memo = {}
    if n in memo: return memo[n]
    # TODO
    pass


assert catalan(0)  == 1
assert catalan(1)  == 1
assert catalan(5)  == 42
assert catalan(10) == 16796


def count_paths(m, n, memo=None):
    """
    Count paths from top-left to bottom-right of an m×n grid,
    moving only right or down.

    Recurrence:
        count_paths(1, n) = 1  (only one path: go all right)
        count_paths(m, 1) = 1  (only one path: go all down)
        count_paths(m, n) = count_paths(m-1, n) + count_paths(m, n-1)

    Add memoization using (m, n) as the key.

    Examples:
        count_paths(1, 1) → 1
        count_paths(2, 2) → 2
        count_paths(3, 3) → 6
        count_paths(4, 4) → 20
    """
    if memo is None: memo = {}
    # TODO
    pass


assert count_paths(1,1) == 1
assert count_paths(2,2) == 2
assert count_paths(3,3) == 6
assert count_paths(4,4) == 20
assert count_paths(3,7) == 28


def min_coins(coins, amount, memo=None):
    """
    Return the minimum number of coins from `coins` to make `amount`.
    Return -1 if it is impossible.

    Recurrence:
        min_coins(0) = 0
        min_coins(amount) = 1 + min(min_coins(amount - c) for c in coins if c <= amount)
                          = -1 if no valid coin exists

    Add memoization.

    Examples:
        min_coins([1,5,10,25], 36)  → 3  (25+10+1)
        min_coins([2], 3)           → -1
        min_coins([1,2,5], 11)      → 3  (5+5+1)
    """
    if memo is None: memo = {}
    if amount in memo: return memo[amount]
    # TODO
    pass


assert min_coins([1,5,10,25], 36)  == 3
assert min_coins([2], 3)           == -1
assert min_coins([1,2,5], 11)      == 3
assert min_coins([1], 0)           == 0


def edit_distance(s1, s2, memo=None):
    """
    Return the minimum edit distance (Levenshtein) between s1 and s2.
    Operations: insert, delete, substitute — each costs 1.

    Recurrence:
        edit("", s2) = len(s2)  (insert all of s2)
        edit(s1, "") = len(s1)  (delete all of s1)
        edit(s1, s2):
            if s1[-1] == s2[-1]: edit(s1[:-1], s2[:-1])
            else: 1 + min(edit(s1[:-1], s2),      # delete from s1
                          edit(s1, s2[:-1]),        # insert into s1
                          edit(s1[:-1], s2[:-1]))   # substitute

    Add memoization using (s1, s2) as key.

    Examples:
        edit_distance("kitten", "sitting") → 3
        edit_distance("", "abc")           → 3
        edit_distance("abc", "abc")        → 0
    """
    if memo is None: memo = {}
    key = (s1, s2)
    if key in memo: return memo[key]
    # TODO
    pass


assert edit_distance("kitten", "sitting") == 3
assert edit_distance("", "abc")           == 3
assert edit_distance("abc", "abc")        == 0
assert edit_distance("abc", "")           == 3
assert edit_distance("saturday","sunday") == 3


print("✓ B5: memoization")


# ══════════════════════════════════════════════════════════════════════════════
# B6: Iterative Conversion
# ══════════════════════════════════════════════════════════════════════════════

def factorial_iterative(n):
    """Iterative factorial. O(n) time, O(1) space."""
    assert n >= 0
    # TODO: for loop
    pass


def factorial_recursive(n):
    if n == 0: return 1
    return n * factorial_recursive(n - 1)

for i in range(10):
    assert factorial_iterative(i) == factorial_recursive(i), f"Mismatch at {i}"
print("✓ factorial_iterative")


def binary_search_iter(lst, target):
    """
    Iterative binary search. O(log n).
    Convert the recursive version to a while loop.
    """
    lo, hi = 0, len(lst) - 1
    # TODO: while lo <= hi: ...
    pass


lst_s = [1, 3, 5, 7, 9, 11, 13]
assert binary_search_iter(lst_s, 7)  == 3
assert binary_search_iter(lst_s, 4)  == -1
assert binary_search_iter([], 5)     == -1
print("✓ binary_search_iter")


def flatten_iter(lst):
    """
    Iterative flatten using an explicit stack.
    O(n) time where n is the total number of non-list elements.

    Algorithm:
        stack = [lst]
        while stack:
            item = stack.pop()
            if isinstance(item, list): push each element of item onto stack (reversed)
            else: append to result
    """
    result = []
    stack  = [lst]
    # TODO
    return result


assert flatten_iter([])                  == []
assert flatten_iter([1,2,3])             == [1,2,3]
assert flatten_iter([1,[2,[3]],4])       == [1,2,3,4]
assert flatten_iter([1,[2,[3,[4,[5]]]]])  == [1,2,3,4,5]
print("✓ flatten_iter")


def merge_sort_bottom_up(lst):
    """
    Iterative (bottom-up) merge sort. O(n log n), no recursion.

    Algorithm:
        Start with sub-lists of width 1 (each element is a sorted sub-list).
        Repeatedly merge adjacent pairs, doubling the width each round.
        Stop when the width exceeds len(lst).

    Round 1: merge pairs of size 1 → sub-lists of size 2
    Round 2: merge pairs of size 2 → sub-lists of size 4
    ...
    Round k: merge pairs of size 2^(k-1) → sub-lists of size 2^k

    Example (n=6):
        [3,1,4,1,5,9]
        → [1,3][1,4][5,9]    (merge pairs of size 1)
        → [1,1,3,4][5,9]     (merge pairs of size 2)
        → [1,1,3,4,5,9]      (merge pairs of size 4)
    """
    if len(lst) <= 1:
        return lst[:]

    result = lst[:]
    width  = 1

    while width < len(result):
        new_result = []
        # Merge adjacent pairs of sub-lists of size `width`
        for i in range(0, len(result), 2 * width):
            left  = result[i : i + width]
            right = result[i + width : i + 2 * width]
            new_result.extend(merge(left, right))
        result = new_result
        width *= 2

    return result


import random
for _ in range(20):
    test = [random.randint(-100, 100) for _ in range(random.randint(0, 50))]
    assert merge_sort_bottom_up(test) == sorted(test), f"Failed on {test}"
print("✓ merge_sort_bottom_up")


# ══════════════════════════════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("All ps4.py assertions passed.")
    print("=" * 50)
