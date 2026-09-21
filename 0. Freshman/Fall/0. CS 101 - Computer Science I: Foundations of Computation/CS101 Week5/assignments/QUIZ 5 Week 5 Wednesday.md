# CS 101 · Quiz 5
## Week 5, Wednesday — In-Class Assessment

**Date:** Wednesday 28 October 2026 · 09:00–09:10 (start of L16) · Week 5
**Duration:** 10 minutes (first 10 minutes of Wednesday lecture)
**Format:** Written — closed book, closed notes
**Covers:** Week 4 material: recursion, base cases, recursion trees, recursion to iteration

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

This function recomputes the same sub-problems many times. Rewrite it as a **loop** (L14 §5) that does only `n` steps.

```python
def paths(n):
    """Number of ways to climb n stairs, taking 1 or 2 steps at a time."""
    if n <= 1:
        return 1
    return paths(n - 1) + paths(n - 2)
```

Iterative version:
```python



```

---

### Question 4 (2 points)

Roughly how many calls does each make for input `n`? Choose from: `n`, `log₂ n`, `2ⁿ`, and (for total work) `n log₂ n`.

**(a)** A recursive function with one recursive call, reducing n by 1 each time.
________

**(b)** A recursive function with two recursive calls, each on n-1 (no memoization).
________

**(c)** A recursive function with one recursive call on n/2 (halving).
________

**(d)** A recursive function with two recursive calls, each on n/2, plus O(n) work to combine results.
________

---

### Question 5 (2 points)

This makes only `n` calls, yet copies about `n²/2` list elements in total. Why? Identify the specific issue and describe the fix (you don't need to write code — just describe it).

```python
def last_element(lst):
    if len(lst) == 1:
        return lst[0]
    return last_element(lst[1:])
```

Why so much copying: _______________

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
def paths(n):
    a, b = 1, 1          # paths(0), paths(1)
    for _ in range(n - 1):
        a, b = b, a + b
    return b
```
Check: `paths(1) = 1`, `paths(2) = 2`, `paths(5) = 8`. Accept any loop that keeps the last two values.

**Q4:**
(a) `n` (b) about `2ⁿ` (c) about `log₂ n` (d) `n log₂ n` total work (merge sort's shape)

**Q5:**
Why: `lst[1:]` copies the rest of the list on every call: (n−1) + (n−2) + … + 1 ≈ n²/2 copies.
Fix: pass an index into the original list instead of slicing (e.g., `last_element(lst, i=0)` incrementing `i`, or recursing with `i+1` and checking `i == len(lst)-1`), avoiding any list copying.

---

*CS 101 · Week 5 · Quiz 5 · © CSE Department*
