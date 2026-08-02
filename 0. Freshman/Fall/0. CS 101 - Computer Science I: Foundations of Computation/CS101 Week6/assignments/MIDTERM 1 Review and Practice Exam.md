# CS 101 · Midterm 1 Review & Practice Exam
## Covers Weeks 0–5: Foundations Through Sorting Algorithms

**Midterm 1 Format:** 75 minutes, written, closed book. One handwritten cheat sheet (1 side of 8.5×11) allowed.
**Weight:** 15% of final grade

---

## How to Use This Document

This is not busywork — it is a diagnostic tool. Work through it **closed-book, timed**, exactly as you will experience the real exam. Then grade yourself honestly against the answer key at the end. Any section where you scored below 80%, go back and re-read that week's lecture notes before the actual exam.

**Suggested schedule:**
- Attempt the full practice exam in one sitting: 75 minutes, no notes, no computer
- Grade yourself against the answer key
- For every wrong or incomplete answer, identify which week's lecture covers it, and reread that lecture
- Redo only the problems you got wrong, without looking at the key this time

---

## Topics Covered (By Week)

| Week | Topics |
|------|--------|
| 0 | Computer science as a discipline, Turing Machines, Church-Turing Thesis, Halting Problem, Von Neumann architecture |
| 1 | Python types (int, float, bool, str, None), mutability, expressions, operator precedence, type conversion |
| 2 | Conditionals (if/elif/else), while loops, for loops, loop invariants, range/enumerate/zip |
| 3 | Functions, parameters vs arguments, scope (LEGB), the call stack, mutable default trap, closures |
| 4 | Recursion — three laws, induction proofs, recursion trees, memoization, Tower of Hanoi, backtracking |
| 5 | Linear/binary search, selection/insertion/bubble sort, merge sort, quicksort, stability |

---

## Section 1: Short Answer (30 points, ~2 min each)

**1.1** State the three laws of recursion.

**1.2** What is the Church-Turing Thesis? What does it imply about the relationship between a Turing Machine and a modern laptop?

**1.3** Explain the difference between `is` and `==` in Python. State the one situation where `is` is the *correct* choice.

**1.4** What does LEGB stand for? In what order does Python search these namespaces?

**1.5** Why does `0.1 + 0.2 == 0.3` evaluate to `False` in Python? What is the correct way to compare floats?

**1.6** State the loop invariant for binary search (in terms of `lo`, `hi`, and `target`).

**1.7** What is the "mutable default argument trap"? Show a broken example and its fix.

**1.8** What is memoization? Why does it change naive Fibonacci from O(2ⁿ) to O(n)?

**1.9** What makes a sorting algorithm "stable"? Name one stable and one unstable sort from this course.

**1.10** Why is insertion sort's best case O(n) despite its worst case being O(n²)? What input triggers the best case?

---

## Section 2: Code Tracing (20 points)

### 2.1 (8 points) Trace this code completely. Show the value of every variable at each step.

```python
def mystery(lst):
    if len(lst) <= 1:
        return lst
    mid = len(lst) // 2
    left = mystery(lst[:mid])
    right = mystery(lst[mid:])
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

print(mystery([5, 2, 8, 1]))
```

What does this function compute? What is the output?

### 2.2 (6 points) What is printed? Explain using the LEGB rule.

```python
x = "global"

def outer():
    x = "outer"
    def inner():
        nonlocal x
        x = "inner"
    inner()
    print(x)

outer()
print(x)
```

### 2.3 (6 points) Trace the call stack. How many total frames exist at the DEEPEST point of execution?

```python
def a(n):
    if n == 0:
        return 0
    return b(n - 1) + 1

def b(n):
    if n == 0:
        return 0
    return a(n - 1) + 1

print(a(4))
```

---

## Section 3: Algorithm Design (25 points)

### 3.1 (10 points) Implement `binary_search_count(lst, lo_val, hi_val)` that returns the count of elements in a sorted list `lst` that fall within the inclusive range `[lo_val, hi_val]`. Your solution must run in O(log n).

```python
def binary_search_count(lst, lo_val, hi_val):
    """
    Return the number of elements x in sorted lst with lo_val <= x <= hi_val.

    Examples:
        binary_search_count([1,3,5,7,9,11], 4, 9) → 2  (elements 5, 7)
    """
    # Your implementation here
```

### 3.2 (8 points) Write a recursive function `is_sorted(lst)` that returns True if `lst` is sorted in non-decreasing order. State the base case and recursive case explicitly.

### 3.3 (7 points) Given the recurrence `T(n) = 2T(n/2) + O(1)`, solve it using the recursion-tree method. Show the tree, work per level, and total. What algorithm has this recurrence?

---

## Section 4: Big-O Analysis (15 points)

### 4.1 (6 points) State the tightest Big-O for each function.

```python
# (a)
def f(n):
    total = 0
    for i in range(n):
        j = i
        while j > 0:
            j //= 2
            total += 1
    return total

# (b)
def g(n):
    if n <= 1:
        return 1
    return g(n // 2) + g(n // 2) + 1
```

### 4.2 (5 points) Prove that `2n² + 10n = O(n²)`. State your chosen constants c and n₀ and verify the inequality.

### 4.3 (4 points) A student says: "Merge sort is always faster than insertion sort because O(n log n) beats O(n²)." Under what specific circumstance is this statement FALSE? Give a concrete example.

---

## Section 5: Written Explanation (10 points)

Choose ONE of the following and write a complete, well-organized paragraph (5-8 sentences):

**Option A:** Explain why the Halting Problem is undecidable. Your explanation should reference the proof technique (diagonalization) without needing to reproduce every formal step.

**Option B:** Explain why quicksort's worst case is O(n²) despite its average case being O(n log n). Describe the specific input/pivot-choice combination that triggers the worst case, and one practical mitigation.

**Option C:** Explain the connection between mathematical induction and recursion. Use a specific example (any recursive function from the course) to illustrate how the base case and recursive case correspond to the base case and inductive step of an induction proof.

---

## Total: 100 points

---

# ANSWER KEY

## Section 1: Short Answer

**1.1** (a) Must have a base case. (b) Must make progress toward the base case with each call. (c) Must call itself.

**1.2** The Church-Turing Thesis states that any computation performable by any mechanical/algorithmic process can be performed by a Turing Machine. Implication: a laptop is computationally equivalent to a Turing Machine — it computes exactly the same class of functions, just faster and with more (but still finite) memory.

**1.3** `==` compares value equality (do two objects have the same value?). `is` compares object identity (are two names bound to the exact same object in memory?). The correct use of `is`: `x is None` (since `None` is a singleton — there is only one `None` object).

**1.4** Local → Enclosing → Global → Built-in. Python searches in that order, using the first match found.

**1.5** Because `0.1` and `0.2` cannot be represented exactly in binary floating-point (IEEE 754) — similar to how 1/3 cannot be represented exactly in decimal. Their sum's rounding error causes it to differ slightly from the stored representation of `0.3`. Correct comparison: `math.isclose(0.1+0.2, 0.3)`.

**1.6** "If target is present in lst, it is located within lst[lo..hi]."

**1.7** Default argument values are evaluated ONCE, at function definition time — not at each call. Using a mutable default (like `[]`) means all calls share the same object.
```python
def f(x, lst=[]):       # BROKEN
    lst.append(x)
    return lst

def f(x, lst=None):     # FIXED
    if lst is None:
        lst = []
    lst.append(x)
    return lst
```

**1.8** Memoization caches the result of each unique subproblem so it is computed only once. Naive Fibonacci recomputes the same subproblems exponentially many times (e.g., fib(n-2) is computed both directly and via fib(n-1)); memoization ensures each of the n distinct subproblems (fib(0) through fib(n)) is computed exactly once, reducing total work from O(2ⁿ) to O(n).

**1.9** A stable sort preserves the relative order of elements that compare equal. Stable: merge sort, insertion sort, bubble sort, Timsort. Unstable: selection sort, quicksort (standard implementation).

**1.10** On already-sorted input, the inner `while` loop condition (`lst[j] > key`) is immediately False for every element being inserted — no shifting is ever needed. The algorithm degenerates to a single linear scan: O(n).

## Section 2: Code Tracing

**2.1** This is **merge sort**. Trace: `mystery([5,2,8,1])` splits into `mystery([5,2])` and `mystery([8,1])`. `mystery([5,2])` splits into `[5]` and `[2]`, merges to `[2,5]`. `mystery([8,1])` splits into `[8]` and `[1]`, merges to `[1,8]`. Final merge of `[2,5]` and `[1,8]`: compare 2,1→take 1; compare 2,8→take 2; compare 5,8→take 5; append remaining 8. Result: `[1,2,5,8]`.

**2.2** Output:
```
inner
global
```
`inner()` uses `nonlocal x`, which modifies `outer`'s local `x` (the Enclosing scope relative to `inner`) — changing it from "outer" to "inner". So `print(x)` inside `outer` (after calling `inner()`) prints "inner". The global `x` is never touched by either function, so the final `print(x)` at module level prints "global".

**2.3** Trace: `a(4)` calls `b(3)` calls `a(2)` calls `b(1)` calls `a(0)` → returns 0. Then unwinds: `b(1)`→1, `a(2)`→2, `b(3)`→3, `a(4)`→4.
At the deepest point (`a(0)` executing), the stack has: `__main__` → `a(4)` → `b(3)` → `a(2)` → `b(1)` → `a(0)`. **6 total frames** (including the module-level frame).

## Section 3: Algorithm Design

**3.1**
```python
def binary_search_count(lst, lo_val, hi_val):
    def bisect_left(target):
        lo, hi = 0, len(lst)
        while lo < hi:
            mid = (lo + hi) // 2
            if lst[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def bisect_right(target):
        lo, hi = 0, len(lst)
        while lo < hi:
            mid = (lo + hi) // 2
            if lst[mid] <= target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    return bisect_right(hi_val) - bisect_left(lo_val)
```

**3.2**
```python
def is_sorted(lst):
    # Base case: 0 or 1 elements are trivially sorted
    if len(lst) <= 1:
        return True
    # Recursive case: first two elements in order AND rest of list sorted
    if lst[0] > lst[1]:
        return False
    return is_sorted(lst[1:])
```

**3.3**

For T(n) = 2T(n/2) + O(1), each level doubles the number of subproblems while each subproblem does
O(1) work:

```
Level 0: 1 * O(1) = O(1)
Level 1: 2 * O(1) = O(2)
Level 2: 4 * O(1) = O(4)
...
Level log2(n): n * O(1) = O(n)
```
Total = O(1) + O(2) + O(4) + ... + O(n) = O(2n) = **O(n)** (geometric series dominated by the last term).
This recurrence matches a simple binary tree traversal (visit every node once, O(1) work per node, total O(n) nodes).

## Section 4: Big-O Analysis

**4.1** (a) Outer loop O(n), inner loop halves each time → O(log n) per outer iteration → total **O(n log n)**.
(b) `T(n) = 2T(n/2) + O(1)` → by the same reasoning as 3.3 → **O(n)**.

**4.2** Choose c=3, n₀=5. Verify: `2n²+10n ≤ 3n²` ⟺ `10n ≤ n²` ⟺ `10 ≤ n`. Holds for n≥10, so use n₀=10 (or verify n₀=5 doesn't quite work: 10(5)=50 ≤ 25? No — must use n₀=10). Correct proof: c=3, n₀=10: for all n≥10, `2n²+10n ≤ 3n²`. ∎

**4.3** False when n is small — for small n (roughly n<20-50 depending on constants), insertion sort's lower constant factor and simplicity often make it faster in absolute terms despite the "worse" asymptotic class, because the O(n log n) vs O(n²) gap hasn't yet overcome the constant-factor difference. Example: sorting a 10-element list — insertion sort typically outperforms merge sort due to merge sort's recursive call overhead and auxiliary array allocation.

## Section 5: Written Explanation

**Option A (sample answer):** The Halting Problem asks whether a program HALT(P, I) can determine if any program P halts on input I. Turing's proof assumes such a HALT function exists, then constructs a new program D that takes a program M as input, runs HALT(M, M), and does the OPPOSITE of what HALT predicts (if HALT says M halts on M, D loops forever; if HALT says M loops, D halts). Now consider running D on itself: D(D). If HALT(D,D) says D halts, then by construction D loops forever on D — contradiction. If HALT(D,D) says D loops, then D halts on D — contradiction. Since both cases lead to contradiction, no such HALT function can exist. This is a diagonalization argument, structurally similar to Cantor's proof that the reals are uncountable.

---

*CS 101 · Midterm 1 Review & Practice Exam · © CSE Department*
