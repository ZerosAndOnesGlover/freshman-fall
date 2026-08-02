# CS 101 · Quiz 7
## Week 7, Wednesday — In-Class Assessment

**Duration:** 10 minutes (first 10 minutes of Wednesday lecture)
**Format:** Written — closed book, closed notes
**Covers:** Week 6 material: Big-O, recurrences, Master Theorem, amortized analysis

---

### Question 1 (2 points)

State the formal definition of `f(n) = O(g(n))`. Your answer must include the quantifiers (∃, ∀) and the inequality.

---

### Question 2 (2 points)

What is the tightest Big-O for this function? Show the loop structure that justifies your answer.

```python
def f(n):
    total = 0
    for i in range(n):
        for j in range(i):
            total += 1
    return total
```

Big-O: ___________

Justification:

---

### Question 3 (2 points)

Solve this recurrence using the Master Theorem. Show `a`, `b`, `f(n)`, the comparison, and which case applies.

```
T(n) = 4T(n/2) + O(n)
```

a = ___  b = ___  f(n) = ___
n^(log_b a) = ___
Case: ___
T(n) = O(___)

---

### Question 4 (2 points)

Why does the Master Theorem NOT apply to this recurrence? What method would you use instead?

```
T(n) = T(n-1) + T(n-2) + O(1)
```

---

### Question 5 (2 points)

What is "amortized analysis"? Give the canonical example from this week's material, and state the amortized complexity of the relevant operation.

---

**Total: 10 points**

---

## Answer Key (Instructor Copy)

**Q1:** `f(n) = O(g(n))` if and only if there exist positive constants `c` and `n₀` such that `f(n) ≤ c·g(n)` for all `n ≥ n₀`.

**Q2:** Big-O: **O(n²)**
Justification: outer loop runs n times; inner loop runs i times for each i from 0 to n-1. Total iterations = 0+1+2+...+(n-1) = n(n-1)/2 = O(n²). Even though the inner loop is "triangular" (shorter on average than n), the sum is still quadratic.

**Q3:**
a=4, b=2, f(n)=O(n)
n^(log_2 4) = n²
Compare f(n)=n to n²: f(n) is polynomially smaller → **Case 1**
T(n) = **Θ(n²)**

**Q4:** The Master Theorem only applies to recurrences of the form `T(n) = a·T(n/b) + f(n)` — a constant number of sub-problems, each a *fraction* (n/b) of the original size. This recurrence has sub-problems of size `n-1` and `n-2` (constant reduction, not proportional reduction), so it does not fit the template. Use the **recursion tree method** (or substitution) instead — this recurrence (naive Fibonacci) solves to O(2ⁿ).

**Q5:** Amortized analysis computes the average cost per operation across a sequence of operations, even though individual operations may occasionally be expensive. Canonical example: Python's dynamic array (`list.append()`). Most appends are O(1) (writing into unused capacity), but occasionally the array must be resized (O(n), copying all elements to a larger array). Because resizes happen exponentially rarely (doubling strategy), the amortized cost of `append()` is **O(1)**.

---

*CS 101 · Week 7 · Quiz 7 · © CSE Department*
