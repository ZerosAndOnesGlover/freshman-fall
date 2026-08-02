# CS 101 · Quiz 5
## Week 5, Wednesday — In-Class Assessment

**Duration:** 10 minutes (first 10 minutes of Wednesday lecture)
**Format:** Written — closed book, closed notes
**Covers:** Week 4 material: recursion, base cases, recursion trees, memoization

---

### Question 1 (2 points)

Identify the base case and the recursive case in this function. Then state whether all three laws of recursion are satisfied.

```python
def mystery(n):
    if n <= 1:
        return 1
    return n * mystery(n - 1)
```

Base case: _______________

Recursive case: _______________

All three laws satisfied? (circle one): YES / NO

If NO, which law is violated?

---

### Question 2 (2 points)

Draw the recursion tree for `mystery(4)` from Question 1 (you may write it linearly if easier: `mystery(4) → mystery(3) → ...`). What mathematical function does `mystery` compute?

Tree/chain:

Function computed: _______________

---

### Question 3 (2 points)

This function is exponential (O(2^n)) due to overlapping subproblems. Rewrite it to run in O(n) using memoization.

```python
def paths(n):
    """Number of ways to climb n stairs, taking 1 or 2 steps at a time."""
    if n <= 1:
        return 1
    return paths(n - 1) + paths(n - 2)
```

Memoized version:
```python



```

---

### Question 4 (2 points)

What is the time complexity of each? Write your answer as O(...).

**(a)** A recursive function with one recursive call, reducing n by 1 each time.
O(___)

**(b)** A recursive function with two recursive calls, each on n-1 (no memoization).
O(___)

**(c)** A recursive function with one recursive call on n/2 (halving).
O(___)

**(d)** A recursive function with two recursive calls, each on n/2, plus O(n) work to combine results.
O(___)

---

### Question 5 (2 points)

Why does this function run in O(n²) instead of O(n), despite looking like simple linear recursion? Identify the specific issue and describe the fix (you don't need to write code — just describe it).

```python
def last_element(lst):
    if len(lst) == 1:
        return lst[0]
    return last_element(lst[1:])
```

Why O(n²): _______________

Fix (describe): _______________

---

**Total: 10 points**

---

## Answer Key (Instructor Copy)

**Q1:**
Base case: `n <= 1` → return 1
Recursive case: `n * mystery(n-1)`
All three laws: YES — base case exists, n-1 makes progress toward it, and it calls itself.

**Q2:**
`mystery(4) → 4 * mystery(3) → 4 * (3 * mystery(2)) → 4 * 3 * (2 * mystery(1)) → 4*3*2*1 = 24`
Function computed: **factorial** (n!)

**Q3:**
```python
def paths(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return 1
    memo[n] = paths(n-1, memo) + paths(n-2, memo)
    return memo[n]
```

**Q4:**
(a) O(n)
(b) O(2^n)
(c) O(log n)
(d) O(n log n)

**Q5:**
Why O(n²): `lst[1:]` creates a new list of size n-1 each call — this slicing operation is O(n). With n recursive calls, each doing O(n) work for the slice, total work is O(n²).
Fix: pass an index into the original list instead of slicing (e.g., `last_element(lst, i=0)` incrementing `i`, or recursing with `i+1` and checking `i == len(lst)-1`), avoiding any list copying.

---

*CS 101 · Week 5 · Quiz 5 · © CSE Department*
