# CS 101 Week 4 Reading Guide & Resources
## Recursion: Thinking in Self-Reference

---

## Required Reading

### Guttag — Introduction to Computation and Programming Using Python

**Chapter 4.3 — Recursion**
The primary treatment of recursion in the course text. Read the entire section, paying close attention to:
- The formal definition of a recursive function
- How Python resolves recursive calls using the call stack
- The examples: factorial, Fibonacci, palindrome checking

**Chapter 3.4 — Bisection Search**
Connects recursion to a practical search algorithm. The bisection search for a square root approximation is a clean example of divide-and-conquer thinking applied to numerical methods.

**Chapter 5 (partial) — Structured Types**
Read §5.1–5.3 on lists. Understanding lists deeply — as mutable sequences that can contain other lists — is the foundation for recursive list processing and data structures in Weeks 7–8.

---

## Focused REPL Sessions

### Session A: Recursion vs. The Stack (20 min)

Open Python Tutor (https://pythontutor.com) for every example. Step through each one completely.

```python
# 1. Count frames at the deepest point
def f(n):
    if n == 0:
        return 0        # ← PUT A BREAKPOINT HERE (in Python Tutor)
    return 1 + f(n-1)

f(5)
# How many frames when n==0? ___

# 2. Two recursive calls — watch the tree unfold
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

fib(4)
# Step through: notice fib(2) is computed twice. At what point?

# 3. What happens to local variables after return?
def triple(x):
    local_var = x * 3
    return local_var

result = triple(7)
# After triple returns: does local_var still exist? Test:
try:
    print(local_var)
except NameError as e:
    print(f"Correct: {e}")

# 4. Recursion limit — feel the wall
import sys
print(sys.getrecursionlimit())   # 1000

def count(n):
    return 1 + count(n+1)

try:
    count(0)
except RecursionError:
    print("RecursionError hit!")
```

### Session B: The Memoization Transformation (20 min)

```python
import time

# Step 1: Measure naive Fibonacci
def fib_naive(n):
    if n <= 1: return n
    return fib_naive(n-1) + fib_naive(n-2)

for n in [10, 20, 30, 35]:
    t0 = time.perf_counter()
    result = fib_naive(n)
    t1 = time.perf_counter()
    print(f"fib_naive({n:2}) = {result:>12}  time: {(t1-t0)*1000:8.2f}ms")

# Step 2: Add memoization
def fib_memo(n, memo=None):
    if memo is None: memo = {}
    if n in memo: return memo[n]
    if n <= 1: return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

for n in [10, 50, 100, 500]:
    t0 = time.perf_counter()
    result = fib_memo(n)
    t1 = time.perf_counter()
    print(f"fib_memo({n:3}) = {result:>30}  time: {(t1-t0)*1000:8.4f}ms")

# Step 3: How many unique subproblems does fib_memo(n) solve?
# Answer: exactly n+1 (fib(0), fib(1), ..., fib(n))
# Verify by counting memo entries after a call:
memo = {}
fib_memo(20, memo)
print(f"Unique subproblems solved: {len(memo)}")   # Should be 20
```

### Session C: Recursion Design Practice (15 min)

For each problem, write the recursive solution step-by-step:
1. Identify the base case(s)
2. Identify the recursive case (what is the "smaller problem"?)
3. Write the code
4. Verify with at least 3 test cases

```python
# Problem 1: sum of digits (without loops or string conversion)
# Base case: n < 10 → n itself is the only digit
# Recursive: last digit (n%10) + sum_digits(n//10)
def sum_digits(n):
    # TODO
    pass

assert sum_digits(0)    == 0
assert sum_digits(9)    == 9
assert sum_digits(123)  == 6
assert sum_digits(9999) == 36

# Problem 2: count occurrences (without loops)
# count_occ([1,2,1,3,1], 1) → 3
def count_occ(lst, target, i=0):
    # TODO
    pass

assert count_occ([1,2,1,3,1], 1) == 3
assert count_occ([], 5)          == 0

# Problem 3: is_sorted (without loops)
# is_sorted([1,2,3,4]) → True
# is_sorted([1,3,2,4]) → False
def is_sorted(lst):
    # TODO: base cases (0 or 1 elements), recursive case
    pass

assert is_sorted([])        == True
assert is_sorted([1])       == True
assert is_sorted([1,2,3])   == True
assert is_sorted([1,3,2])   == False
```

---

## Conceptual Exercises (Paper and Pencil)

Work all of these without Python. Verify afterward.

**Exercise 1:** The Towers of Hanoi

The recurrence for the number of moves is T(n) = 2·T(n-1) + 1, T(1) = 1.

(a) Compute T(1), T(2), T(3), T(4), T(5) manually.
(b) Guess a closed-form formula from the pattern.
(c) Prove your formula by induction.

**Exercise 2:** Recursion tree node count

For `fib(n)`, let C(n) = total number of calls made (including the initial call).

(a) Compute C(0), C(1), C(2), C(3), C(4), C(5).
(b) Find the pattern: C(n) relates to which well-known sequence?
(c) Prove your answer by induction.

**Exercise 3:** Correctness proof

Prove that this function returns the number of elements in lst greater than x:

```python
def count_greater(lst, x, i=0):
    if i == len(lst):
        return 0
    return (1 if lst[i] > x else 0) + count_greater(lst, x, i+1)
```

Write the base case proof and the inductive step.

**Exercise 4:** Three Laws Check

For each function, identify whether the three laws are all satisfied:

(a) `def f(n): return f(n+1)` — Which law is violated?

(b) `def g(n): if n==0: return 0; return g(n-2)` — Is there a problem? For which inputs?

(c) `def h(lst): if not lst: return []; return [lst[-1]] + h(lst[:-1])` — All laws satisfied? What does it compute?

---

## Key Algorithms This Week

### Merge Sort — O(n log n)

```
merge_sort(lst):
    if len(lst) <= 1: return lst
    mid = len(lst)//2
    return merge(merge_sort(lst[:mid]), merge_sort(lst[mid:]))
```

| Property | Value |
|----------|-------|
| Time complexity | O(n log n) — all cases |
| Space complexity | O(n) — auxiliary space for merging |
| Stable? | Yes — equal elements maintain relative order |
| In-place? | No — requires O(n) extra space |
| Divide-and-conquer? | Yes — split in half each time |
| Optimal? | Yes — no comparison sort beats O(n log n) |

### Binary Search — O(log n)

```
binary_search(lst, target, lo, hi):
    if lo > hi: return -1
    mid = (lo+hi)//2
    if lst[mid]==target: return mid
    if lst[mid]<target:  return binary_search(lst, target, mid+1, hi)
    else:                return binary_search(lst, target, lo, mid-1)
```

| Property | Value |
|----------|-------|
| Time complexity | O(log n) |
| Space complexity | O(log n) recursive, O(1) iterative |
| Requirement | List must be sorted |
| Each call | Eliminates half the remaining search space |

### Fast Power — O(log n)

```
fast_power(b, n):
    if n==0: return 1
    if n%2==0: half=fast_power(b,n//2); return half*half
    else: return b*fast_power(b,n-1)
```

| Property | Value |
|----------|-------|
| Time | O(log n) multiplications |
| vs naive | Naive b*b*b*...*b = n-1 multiplications = O(n) |
| Trick | Squaring halves the exponent — like binary search on the exponent |

---

## Common Mistakes This Week

**Mistake 1: Missing base case**
```python
def bad(n):
    return bad(n-1) + 1   # RecursionError — never stops
```
Always write the base case first. Test it explicitly.

**Mistake 2: Not making progress**
```python
def bad(n):
    if n == 0: return 0
    return bad(n) + 1    # calls bad(n), not bad(n-1) — infinite recursion
```
The recursive call must receive a strictly smaller input.

**Mistake 3: O(n²) slicing in recursive list functions**
```python
def my_sum(lst):
    if not lst: return 0
    return lst[0] + my_sum(lst[1:])   # lst[1:] = O(n) → total O(n²)
```
Fix: pass an index instead.
```python
def my_sum(lst, i=0):
    if i == len(lst): return 0
    return lst[i] + my_sum(lst, i+1)  # O(1) per call → total O(n)
```

**Mistake 4: Mutable default in recursive helper**
```python
def collect(n, result=[]):   # WRONG — shared across calls!
    if n == 0: return result
    result.append(n)
    return collect(n-1, result)
```
Fix: `result=None`, then `if result is None: result = []` at the start.

**Mistake 5: Confusing `return` with `print` in recursion**
```python
def factorial(n):
    if n == 0:
        print(1)   # WRONG — prints, doesn't return
    print(n * factorial(n-1))  # multiplies by None!
```
Recursive functions must `return` values, not just `print` them.

**Mistake 6: Exponential recursion without memoization**
```python
fib(40)   # Takes ~30 seconds — over 300 million calls
fib(50)   # Effectively never terminates
```
Any function with two recursive calls on n-1 and n-2 is O(2^n). Add memoization or convert to dynamic programming.

---

## Week 4 Self-Test

Without notes, answer these:

1. State the three laws of recursion.
2. What is the base case and recursive case for `factorial`?
3. Why is naïve `fib(n)` O(2^n)?
4. How does memoization reduce `fib(n)` from O(2^n) to O(n)?
5. What is the recursion tree for merge sort? What is its depth? Total nodes?
6. Why does `merge_sort` run in O(n log n)?
7. How many comparisons does binary search make on a list of 1,024 elements?
8. What is the `fast_power` trick for even exponents?
9. What is the "choose-explore-unchoose" pattern? Give an example.
10. What is Python's default recursion limit? What error is raised when exceeded?

*(Answers: 1. base case, progress toward base, self-call. 2. n=0→1; n→n*f(n-1). 3. Two calls per level, each at n-1 and n-2 — tree grows exponentially. 4. Each of n subproblems solved once. 5. Binary tree; log₂n depth; 2n-1 nodes. 6. O(n) work per level × O(log n) levels. 7. At most 10 (log₂1024=10). 8. half=fast_power(b,n//2); return half*half — one call instead of n/2 calls. 9. Try option, recurse, undo if failure; e.g., permutations. 10. 1000; RecursionError.)*

---

## Preview: Week 5

Week 5 covers **searching and sorting algorithms** in depth:
- Linear search vs binary search — complexity comparison
- Selection sort, insertion sort, bubble sort — O(n²) algorithms
- Merge sort (from this week) vs quicksort — O(n log n)
- Sorting stability, best/worst/average case analysis
- Introduction to Big-O notation (preview of Week 6)

The recursion you learned this week is the foundation: merge sort is recursive divide-and-conquer, and binary search is recursive halving. Week 5 goes wider — covering the full landscape of sorting algorithms and why the differences matter.

---

*CS 101 · Week 4 · Reading Guide · © CSE Department*
