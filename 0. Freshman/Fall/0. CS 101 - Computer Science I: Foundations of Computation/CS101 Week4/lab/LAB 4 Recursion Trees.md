# CS 101 · Lab 4
## Recursion Tree Drawing and Implementation

**Date:** Tuesday 27 October 2026 · 15:00–16:50 · Lab Section (Week 5) — covers Week 4 (L13–L15)
*Duration: 2 hours · 100 points via TA checkoff, part of the Labs component (10%)*

**Tools used:** Weeks 0–4 only. No dictionaries (so no memo tables — Week 8), no timing modules,
no Big-O notation yet (Week 6): you count calls instead.

---

## Objectives

By the end of this lab, you will:
- [ ] Draw recursion trees by hand for at least 4 functions
- [ ] Count recursive calls and identify the complexity class from the tree
- [ ] Implement 6 recursive functions with complete correctness proofs
- [ ] Demonstrate the exponential blowup of naïve Fibonacci
- [ ] Fix the slicing anti-pattern with index-based recursion
- [ ] Implement merge sort and verify it on multiple inputs
- [ ] Implement a backtracking solver

---

## Setup

```bash
cd "$CS101"        # set in ~/.bashrc -- see Lab 0
mkdir -p week4 && cd week4
```

---

## Part 1: Recursion Tree Drawing (30 minutes)

Work on paper. For each function:
1. Draw the complete recursion tree for the given input
2. Label each node with the function call and its return value
3. Count total nodes (= total calls)
4. Say how the count grows when `n` grows

### Exercise 1.1: Linear Recursion

```python
def count_up(n):
    if n == 0:
        return 0
    return 1 + count_up(n - 1)
```

Draw the tree for `count_up(5)`.

**Answer in `LAB 4 Recursion Trees.md`:**
- How many nodes total?
- What is the depth of the tree?
- How does the number of calls grow as `n` grows by 1? As the list length doubles?

### Exercise 1.2: Binary Recursion (the expensive kind)

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
```

Draw the tree for `fib(5)`. (This is large — count carefully.)

**Answer:**
- How many nodes? (Count by hand or in levels)
- How many times is `fib(2)` computed?
- How many times is `fib(1)` computed?
- How does the number of calls grow as `n` grows by 1? As the list length doubles?

### Exercise 1.3: Divide and Conquer

```python
def binary_search(lst, target, lo, hi):
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if lst[mid] == target:
        return mid
    elif lst[mid] < target:
        return binary_search(lst, target, mid+1, hi)
    else:
        return binary_search(lst, target, lo, mid-1)
```

Draw the tree for `binary_search([1,2,3,4,5,6,7,8], 3, 0, 7)`.

**Answer:**
- How many nodes? (worst case, searching for a missing element)
- What is the maximum depth for a list of length 8? Of length 16? Of length n?
- How does the number of calls grow as `n` grows by 1? As the list length doubles?

### Exercise 1.4: Tree Recursion on a Real Tree

Given this binary tree:
```
        5
       / \
      3   8
     / \   \
    1   4   9
```

Draw the recursion tree for `tree_sum(root)` where:
```python
def tree_sum(node):
    if node is None:
        return 0
    return node.value + tree_sum(node.left) + tree_sum(node.right)
```

**Answer:**
- How many calls total (including the None calls)?
- For a tree with n nodes, how many None-calls are made? (Hint: binary tree property)
- How does the number of calls grow as `n` grows by 1? As the list length doubles?

---

## Part 2: Recursive Implementation (50 minutes)

Create `recursion_lab.py`. Implement each function with:
- A complete docstring (base case, recursive case, example)
- A correctness argument (base + inductive step in comments)
- At least 2 `assert` tests

```python
#!/usr/bin/env python3
"""
recursion_lab.py
CS 101 — Week 4, Lab 4

Recursive function implementations with correctness proofs.

Student: ____________________________
Date: ______________________________
"""


# ─── Exercise 2.1: Power with fast exponentiation ────────────────────────────

def fast_power(base, exp):
    """
    Compute base**exp using O(log exp) multiplications.

    Key insight: base^exp = (base^(exp//2))^2 if exp is even
                          = base * base^(exp-1)  if exp is odd

    This halves the problem when exp is even → O(log exp) depth.

    Base case:    fast_power(base, 0) = 1
    Recursive cases:
        exp even: fast_power(base, exp) = half * half
                  where half = fast_power(base, exp//2)
        exp odd:  fast_power(base, exp) = base * fast_power(base, exp-1)

    Correctness:
        Base: base^0 = 1 ✓
        Even: (base^(n/2))^2 = base^n ✓
        Odd:  base * base^(n-1) = base^n ✓

    Args:
        base (int or float): the base
        exp  (int):          non-negative exponent

    Examples:
        fast_power(2, 10)  → 1024
        fast_power(2, 0)   → 1
        fast_power(3, 4)   → 81
    """
    assert isinstance(exp, int) and exp >= 0

    if exp == 0:
        return 1
    if exp % 2 == 0:
        half = fast_power(base, exp // 2)
        return half * half
    return base * fast_power(base, exp - 1)


assert fast_power(2, 0)   == 1
assert fast_power(2, 10)  == 1024
assert fast_power(3, 4)   == 81
assert fast_power(2, 1)   == 2
assert fast_power(10, 3)  == 1000
print("✓ fast_power")


# ─── Exercise 2.2: Merge Sort ────────────────────────────────────────────────

def merge(left, right):
    """
    Merge two sorted lists into one sorted list.
    Time complexity: O(len(left) + len(right)).

    Base case: either list is empty → return the other.
    Recursive case: compare front elements, take the smaller.

    Loop invariant: result contains all elements from left[:i] and right[:j]
                    in sorted order.
    """
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(lst):
    """
    Return a new sorted list using the merge sort algorithm.
    Time complexity: O(n log n).  Space complexity: O(n).

    Base case: a list of 0 or 1 elements is sorted.
    Recursive case: sort each half, then merge.

    Correctness:
        Base: [] and [x] are trivially sorted. ✓
        Step: assume merge_sort correctly sorts any list of size < n.
              Both halves have size < n, so they are correctly sorted (IH).
              merge() of two sorted lists is sorted.
              Therefore merge_sort(lst) is sorted. ✓

    Examples:
        merge_sort([3, 1, 4, 1, 5, 9]) → [1, 1, 3, 4, 5, 9]
        merge_sort([])                  → []
        merge_sort([1])                 → [1]
    """
    if len(lst) <= 1:
        return lst[:]

    mid   = len(lst) // 2
    left  = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])
    return merge(left, right)


assert merge_sort([])          == []
assert merge_sort([1])         == [1]
assert merge_sort([3, 1, 2])   == [1, 2, 3]
assert merge_sort([5,4,3,2,1]) == [1, 2, 3, 4, 5]
assert merge_sort([3,3,1,1,2]) == [1, 1, 2, 3, 3]
print("✓ merge_sort")


# ─── Exercise 2.3: Binary Search (recursive, index-based) ─────────────────────

def binary_search(lst, target, lo=0, hi=None):
    """
    Search for target in sorted lst[lo..hi] (inclusive).
    Returns the index if found, -1 if not found.
    Time: O(log n).

    Loop invariant: if target is in lst, it is in lst[lo..hi].

    Base case: lo > hi → search space empty → return -1.
    Recursive cases:
        lst[mid] == target → return mid
        lst[mid] <  target → search right half (lo = mid+1)
        lst[mid] >  target → search left half  (hi = mid-1)

    Correctness:
        Invariant initially holds (searching entire list).
        Each branch maintains the invariant:
            - Right half: target > lst[mid], so it cannot be in lst[lo..mid].
            - Left half: target < lst[mid], so it cannot be in lst[mid..hi].
        At termination (lo > hi): search space is empty, target not present.
        If target was found (lst[mid]==target): correct index returned. ✓

    Examples:
        binary_search([1,3,5,7,9], 5)  → 2
        binary_search([1,3,5,7,9], 4)  → -1
        binary_search([], 1)            → -1
    """
    if hi is None:
        hi = len(lst) - 1

    if lo > hi:
        return -1

    mid = (lo + hi) // 2

    if lst[mid] == target:
        return mid
    elif lst[mid] < target:
        return binary_search(lst, target, mid + 1, hi)
    else:
        return binary_search(lst, target, lo, mid - 1)


lst = [1, 3, 5, 7, 9, 11, 13]
assert binary_search(lst, 7)   == 3
assert binary_search(lst, 1)   == 0
assert binary_search(lst, 13)  == 6
assert binary_search(lst, 4)   == -1
assert binary_search(lst, 14)  == -1
assert binary_search([], 5)    == -1
print("✓ binary_search")


# ─── Exercise 2.4: Counting Fibonacci calls ──────────────────────────────────

calls = 0

def fib_counted(n):
    """
    Naive Fibonacci that also counts how many times it is called.
    Base cases: fib(0) = 0, fib(1) = 1.  Recursive case: fib(n-1) + fib(n-2).
    """
    global calls
    calls += 1
    if n <= 1:
        return n
    return fib_counted(n - 1) + fib_counted(n - 2)


# TODO: for n in 5, 10, 15, 20, 25: reset calls to 0, call fib_counted(n),
#       and print n, the result, and calls. Record the table in your notes.
# Check: fib_counted(10) == 55 with 177 calls; fib_counted(20) == 6765 with 21891 calls.
# Question: roughly what factor does the call count grow by each time n rises by 5?

assert fib_counted(10) == 55
print("✓ fib_counted")


# ─── Exercise 2.5: Tower of Hanoi with move counter ──────────────────────────

def hanoi(n, source='A', destination='C', auxiliary='B', verbose=True):
    """
    Compute (and optionally print) the moves for the Tower of Hanoi puzzle.
    Returns the total number of moves.

    Formula: T(n) = 2^n - 1 moves.

    Base case: 1 disk → move directly, 1 move.
    Recursive case:
        1. Move n-1 disks from source to auxiliary (T(n-1) moves)
        2. Move largest disk from source to destination (1 move)
        3. Move n-1 disks from auxiliary to destination (T(n-1) moves)
        Total: 2*T(n-1) + 1 = 2^n - 1 ✓

    Args:
        n:           number of disks
        source:      name of source peg
        destination: name of destination peg
        auxiliary:   name of auxiliary peg
        verbose:     if True, print each move

    Returns:
        int: total number of moves

    Examples:
        hanoi(1) → 1 move
        hanoi(3) → 7 moves
        hanoi(10) → 1023 moves
    """
    if n == 1:
        if verbose:
            print(f"  Move disk 1 from {source} to {destination}")
        return 1

    moves  = hanoi(n-1, source, auxiliary, destination, verbose)
    if verbose:
        print(f"  Move disk {n} from {source} to {destination}")
    moves += 1
    moves += hanoi(n-1, auxiliary, destination, source, verbose)
    return moves


print("\nTower of Hanoi — n=3:")
moves = hanoi(3, verbose=True)
print(f"  Total moves: {moves}")

# Verify formula T(n) = 2^n - 1:
for n in range(1, 12):
    assert hanoi(n, verbose=False) == 2**n - 1, f"Formula fails at n={n}"
print("✓ hanoi — formula verified for n=1..11")


# ─── All tests summary ────────────────────────────────────────────────────────

print("\n🎉 All lab tests passed!")
```

---

## Part 3: The Slicing Anti-Pattern Fix (15 minutes)

Create `slicing_fix.py`. `lst[1:]` copies the rest of the list on every call, so a recursive sum over
n items copies about n²/2 elements in total; passing an index copies nothing (L15 §6).

```python
# slicing_fix.py
# Demonstrates the slicing anti-pattern and its index-based fix.

# VERSION 1: copies a new list slice on each recursive call
def sum_slow(lst):
    if not lst:
        return 0
    return lst[0] + sum_slow(lst[1:])   # lst[1:] copies len(lst) - 1 items


# VERSION 2: passes an index, no copying
def sum_fast(lst, i=0):
    if i == len(lst):
        return 0
    return lst[i] + sum_fast(lst, i + 1)   # no copy


# Verify both are correct:
test = list(range(1, 101))
assert sum_slow(test) == 5050
assert sum_fast(test) == 5050
print("Both versions correct.")

# Apply the same fix to reverse:
def reverse_slow(lst):
    """Copies a slice on every call."""
    if not lst:
        return []
    return reverse_slow(lst[1:]) + [lst[0]]

def reverse_fast(lst, i=None, result=None):
    """Walks an index down the list and accumulates into result."""
    if i is None:
        i = len(lst) - 1
    if result is None:
        result = []
    if i < 0:
        return result
    result.append(lst[i])
    return reverse_fast(lst, i - 1, result)

test = [1, 2, 3, 4, 5]
assert reverse_slow(test) == [5, 4, 3, 2, 1]
assert reverse_fast(test) == [5, 4, 3, 2, 1]
print("\n✓ reverse_fast matches reverse_slow")

# TODO: implement count_occurrences(lst, target, i=0) without slicing
# count_occurrences([1,2,3,2,1], 2) → 2
def count_occurrences(lst, target, i=0):
    """Count occurrences of target in lst using index-based recursion."""
    # TODO
    pass

assert count_occurrences([1,2,3,2,1], 2) == 2
assert count_occurrences([1,1,1], 1) == 3
assert count_occurrences([], 5) == 0
print("✓ count_occurrences")
```

---

## Part 4: Commit and Reflection (10 minutes)

```bash
cd "$CS101/week4"
git add .
git commit -m "CS 101 Lab 4: recursion trees, merge sort, binary search, Hanoi"
git push
```

### Reflection in `LAB 4 Recursion Trees.md`:

**Q1.** You drew the tree for `fib(5)` and counted how often each sub-problem is recomputed. Using your `fib_counted` table, explain in one paragraph why the call count explodes, and what idea (L14's closing section names it) would stop the recomputation.

**Q2.** The Tower of Hanoi takes 2^n - 1 moves. This is provably optimal — you cannot solve it in fewer moves. Using the recurrence T(n) = 2·T(n-1) + 1, prove by induction that T(n) = 2^n - 1.

**Q3.** For which of the following problems is recursion the *clearest* solution, and for which is iteration clearer? Justify each.
- (a) Computing the sum of integers from 1 to n
- (b) Traversing a binary tree in sorted order
- (c) Finding whether a string is a palindrome
- (d) Solving a maze

---

## TA Checkoff Criteria

| Part | Points | Show your TA |
|---|---|---|
| 1 | 30 | Four recursion trees drawn with the counts answered (Exercises 1.1–1.4) |
| 2 | 45 | `recursion_lab.py`: all tests pass; the `fib_counted` table recorded |
| 3 | 15 | `slicing_fix.py` runs; `count_occurrences` implemented |
| Reflection | 10 | Q1–Q3 answered in the notes |
| **Total** | **100** | Work committed (required) |

---

*CS 101 · Week 4 · Lab 4 · Tuesday 27 October 2026 · © CSE Department*
