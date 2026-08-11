# CS 101 · Lab 4
## Recursion Tree Drawing and Implementation

**Tuesday of Week 5 · Lab Section** — sat after this week's Wed–Fri lectures, and covers Week 4.
*Duration: 2 hours · Graded on completion (TA checkoff)*

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
cd ~/cs101
mkdir week4 && cd week4
```

---

## Part 1: Recursion Tree Drawing (30 minutes)

Work on paper. For each function:
1. Draw the complete recursion tree for the given input
2. Label each node with the function call and its return value
3. Count total nodes (= total calls)
4. State the big-O complexity

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
- O(___)

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
- O(___)

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
- O(___)

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
- O(___)

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


# ─── Exercise 2.4: Fibonacci with memoization ─────────────────────────────────

def fib_naive(n):
    """Naive Fibonacci — O(2^n). Do not call with n > 35."""
    if n <= 1:
        return n
    return fib_naive(n-1) + fib_naive(n-2)


def fib_memo(n, memo=None):
    """
    Fibonacci with memoization — O(n).

    Key: store computed results in memo dict to avoid recomputation.
    Each subproblem is solved exactly once.

    Base cases: fib(0) = 0, fib(1) = 1.
    Recursive case: fib(n) = fib(n-1) + fib(n-2).
    Memoization: before computing, check if result already in memo.

    Examples:
        fib_memo(10) → 55
        fib_memo(50) → 12586269025  (fast! naive would take hours)
    """
    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n <= 1:
        return n

    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]


# Correctness tests:
assert fib_memo(0)  == 0
assert fib_memo(1)  == 1
assert fib_memo(10) == 55
assert fib_memo(20) == 6765
assert fib_memo(50) == 12586269025

# Verify memoized matches naive (for small n):
for i in range(15):
    assert fib_naive(i) == fib_memo(i), f"Mismatch at n={i}"
print("✓ fib_memo (matches naive for n=0..14)")

# Performance comparison:
import time

t0 = time.time(); fib_naive(30); t1 = time.time()
t2 = time.time(); fib_memo(30);  t3 = time.time()

print(f"  fib_naive(30): {(t1-t0)*1000:.1f} ms")
print(f"  fib_memo(30):  {(t3-t2)*1000:.3f} ms")
print(f"  Speedup: ~{(t1-t0)/(t3-t2+1e-9):.0f}x")


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


# ─── Exercise 2.6: Permutations ──────────────────────────────────────────────

def permutations(lst):
    """
    Return all permutations of lst as a list of lists.
    Uses the choose-explore-unchoose (backtracking) pattern.

    Base case: 0 or 1 elements → only one permutation.
    Recursive case: for each element as the first, permute the rest.

    Total permutations: n! (verified by len(permutations(range(n))) == factorial(n))

    Examples:
        permutations([1,2])     → [[1,2],[2,1]]
        permutations([1,2,3])   → 6 permutations
        permutations([])        → [[]]
    """
    if len(lst) <= 1:
        return [lst[:]]

    result = []
    lst = lst[:]    # work on a copy to avoid modifying caller's list

    for i in range(len(lst)):
        # CHOOSE: swap element i to the front
        lst[0], lst[i] = lst[i], lst[0]

        # EXPLORE: get all permutations of the rest
        for perm in permutations(lst[1:]):
            result.append([lst[0]] + perm)

        # UNCHOOSE: restore the swap
        lst[0], lst[i] = lst[i], lst[0]

    return result


perms_3 = permutations([1, 2, 3])
assert len(perms_3) == 6
assert sorted(perms_3) == sorted([
    [1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]
])
assert permutations([]) == [[]]
assert permutations([1]) == [[1]]
print("✓ permutations")


# ─── All tests summary ────────────────────────────────────────────────────────

print("\n🎉 All lab tests passed!")
```

---

## Part 3: The Slicing Anti-Pattern Fix (15 minutes)

Create `slicing_fix.py`. Demonstrate and fix the O(n²) slicing problem.

```python
# slicing_fix.py
# Demonstrates the O(n^2) slicing anti-pattern and its O(n) fix.

import time

# VERSION 1: O(n^2) — creates a new list slice each recursive call
def sum_slow(lst):
    if not lst:
        return 0
    return lst[0] + sum_slow(lst[1:])   # lst[1:] = O(n) each time!


# VERSION 2: O(n) — passes index, no slice creation
def sum_fast(lst, i=0):
    if i == len(lst):
        return 0
    return lst[i] + sum_fast(lst, i + 1)   # O(1) per call


# Verify both are correct:
test = list(range(1, 101))
assert sum_slow(test) == sum(test) == 5050
assert sum_fast(test) == sum(test) == 5050
print("Both versions correct.")

# Benchmark (use a larger list for visible difference):
import sys
sys.setrecursionlimit(5000)   # temporarily increase for this benchmark

n = 900   # stay under limit
big = list(range(n))

t0 = time.perf_counter(); sum_slow(big); t1 = time.perf_counter()
t2 = time.perf_counter(); sum_fast(big); t3 = time.perf_counter()

print(f"\nFor n={n}:")
print(f"  sum_slow (O(n²) slicing): {(t1-t0)*1000:.2f} ms")
print(f"  sum_fast (O(n) index):    {(t3-t2)*1000:.2f} ms")
print(f"  Ratio: {(t1-t0)/(t3-t2+1e-9):.1f}x slower")

# Apply the same fix to reverse:
def reverse_slow(lst):
    """O(n^2) due to slicing."""
    if not lst:
        return []
    return reverse_slow(lst[1:]) + [lst[0]]

def reverse_fast(lst, i=None, result=None):
    """O(n) — accumulates into result list."""
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

## Part 4: Backtracking — N-Queens (15 minutes)

The N-Queens problem: place N queens on an N×N chessboard so no two queens attack each other (no two in the same row, column, or diagonal).

```python
# n_queens.py

def is_safe(board, row, col):
    """
    Return True if placing a queen at (row, col) is safe,
    given queens already placed in rows 0..row-1.

    board[r] = column of queen in row r.
    Check: no queen in same column, or either diagonal.
    """
    for r in range(row):
        c = board[r]
        if c == col:                  # same column
            return False
        if abs(c - col) == abs(r - row):  # same diagonal
            return False
    return True


def solve_nqueens(n, row=0, board=None, solutions=None):
    """
    Find all solutions to the N-Queens problem.

    board: list of length n where board[r] = column of queen in row r.
    solutions: accumulates all valid complete boards.

    Backtracking pattern:
        For each column in this row:
            CHOOSE: place queen at (row, col)
            EXPLORE: recursively solve remaining rows
            UNCHOOSE: (implicit — board[row] is overwritten next iteration)

    Returns:
        list of boards (each board is a list of column indices)
    """
    if board is None:
        board = [0] * n
    if solutions is None:
        solutions = []

    # Base case: all rows filled → valid solution found
    if row == n:
        solutions.append(board[:])   # append a copy
        return solutions

    for col in range(n):
        if is_safe(board, row, col):
            board[row] = col                              # CHOOSE
            solve_nqueens(n, row + 1, board, solutions)  # EXPLORE
            # UNCHOOSE: board[row] overwritten on next iteration

    return solutions


def print_board(board):
    """Print an N-Queens solution as a grid."""
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            line += "Q " if board[row] == col else ". "
        print(" ", line)
    print()


# Solve and display:
for n in [4, 5, 6, 8]:
    solutions = solve_nqueens(n)
    print(f"N={n}: {len(solutions)} solutions")

print("\nOne solution for N=8:")
print_board(solve_nqueens(8)[0])

# Known solution counts:
assert len(solve_nqueens(4)) == 2
assert len(solve_nqueens(5)) == 10
assert len(solve_nqueens(8)) == 92
print("✓ n_queens solution counts verified")
```

**Answer in `LAB 4 Recursion Trees.md`:**
1. For N=8, how many boards does the solver examine before finding all 92 solutions? (Add a counter.)
2. The `is_safe` check is O(row). What is the total work done for an N=8 board? Estimate.
3. Draw the recursion tree structure for N=4 (don't draw all branches — show the shape).

---

## Part 5: Commit and Reflection (10 minutes)

```bash
cd ~/cs101/week4
git add .
git commit -m "Week 4 Lab: recursion trees, merge sort, binary search, Hanoi, N-Queens"
git push
```

### Reflection in `LAB 4 Recursion Trees.md`:

**Q1.** You drew the recursion tree for `fib(5)` and counted how many times each sub-problem was recomputed. Explain in one paragraph why memoization fixes this, and state the time complexity of memoized Fibonacci.

**Q2.** The Tower of Hanoi takes 2^n - 1 moves. This is provably optimal — you cannot solve it in fewer moves. Using the recurrence T(n) = 2·T(n-1) + 1, prove by induction that T(n) = 2^n - 1.

**Q3.** In the N-Queens backtracking solver, the UNCHOOSE step is implicit (the board is overwritten on the next iteration). Would it still work correctly if you explicitly added `board[row] = -1` after the recursive call? Why or why not?

**Q4.** For which of the following problems is recursion the *clearest* solution, and for which is iteration clearer? Justify each.
- (a) Computing the sum of integers from 1 to n
- (b) Traversing a binary tree in sorted order
- (c) Finding whether a string is a palindrome
- (d) Solving a maze

---

## TA Checkoff Criteria

Show your TA:
- [ ] `LAB 4 Recursion Trees.md` with 4 recursion trees drawn (Parts 1.1–1.4)
- [ ] `recursion_lab.py` with all tests passing (6 functions)
- [ ] `slicing_fix.py` with benchmark output and `count_occurrences` implemented
- [ ] `n_queens.py` running with correct solution counts
- [ ] `LAB 4 Recursion Trees.md` reflection questions answered

---

## Bonus Challenges

**Bonus 1 — Sudoku solver:**
Extend the backtracking pattern to solve Sudoku. Represent the board as a 9×9 list of lists (0 = empty). Use `is_valid(board, row, col, num)` to check placement validity, then backtrack.

**Bonus 2 — Memoized power set:**
The power set of size n has 2^n subsets. Can memoization help? Why or why not? (Think about what subproblems overlap.)

**Bonus 3 — Ackermann function:**
Implement the Ackermann function:
- A(0, n) = n + 1
- A(m, 0) = A(m-1, 1)
- A(m, n) = A(m-1, A(m, n-1))

Try `A(3, 4)`. What is the depth of the recursion tree? Why does `sys.setrecursionlimit` need to be very high?

---

*CS 101 · Week 4 · Lab 4 · © CSE Department*
