# CS 101 · Lecture 19 (Week 6, Lecture 1)
## Algorithm Analysis I: Big-O, Big-Ω, and Big-Θ — Formal Definitions

**Week 6 · Wednesday**
*"Big-O notation captures the essential shape of how an algorithm scales, discarding constants and lower-order terms." — CS 101*

**Date:** Wednesday 4 November 2026 · 09:00–09:50 · Week 6

---

## 0. Why We Need Formal Notation

For five weeks, you have been reasoning informally about efficiency: "this is O(n²)," "this is exponential," "this halves the search space." Today we make that language **precise and provable** — not just useful intuition, but mathematics with definitions, theorems, and proofs.

This matters because informal reasoning eventually breaks down. Is an algorithm that does `3n² + 100n + 5` operations "quadratic"? Is one doing `n² / 1000` operations "fast"? Without formal definitions, these questions have no rigorous answer. With them, every such question becomes a precise, checkable claim.

---

## 1. The Problem With Counting Exact Operations

Consider two algorithms solving the same problem:

**Algorithm A:** does exactly `5n + 12` operations.
**Algorithm B:** does exactly `n² + 3` operations.

For small n (say n=3): A does 27 operations, B does 12. B looks faster!
For n=10: A does 62, B does 103. A is now faster.
For n=1000: A does 5012, B does 1,000,003. A is dramatically faster.
For n=1,000,000: A does 5,000,012. B does 1,000,000,000,003 — a trillion.

**The exact constants (5, 12, 3) become irrelevant as n grows.** What matters is the **rate of growth** — the shape of the function, not its exact value at any point. This is precisely what Big-O captures.

---

## 2. Formal Definition of Big-O

**Definition:** We say f(n) = O(g(n)) if there exist positive constants c and n₀ such that:

```
f(n) ≤ c · g(n)   for all n ≥ n₀
```

In words: f(n) is **at most** a constant multiple of g(n), for all sufficiently large n.

**What this means intuitively:** g(n) is an **upper bound** on f(n)'s growth rate. Big-O describes the **worst-case ceiling** — f grows no faster than g (up to a constant factor).

### Worked Proof: Show that `5n + 12 = O(n)`

We need to find constants c and n₀ such that `5n + 12 ≤ c·n` for all `n ≥ n₀`.

Try c = 6:
```
5n + 12 ≤ 6n
12 ≤ n
```
This holds whenever `n ≥ 12`. So choose `n₀ = 12`, `c = 6`.

**Proof:** For all n ≥ 12: `5n + 12 ≤ 6n`. Therefore, by definition, `5n + 12 = O(n)`. ∎

### Worked Proof: Show that `n² + 3n = O(n²)`

Try c = 2:
```
n² + 3n ≤ 2n²
3n ≤ n²
3 ≤ n
```
This holds whenever n ≥ 3. So choose n₀ = 3, c = 2.

**Proof:** For all n ≥ 3: `n² + 3n ≤ 2n²`. Therefore `n² + 3n = O(n²)`. ∎

### Common Mistake: Big-O Is an Upper Bound, Not a Tight Description

`5n + 12 = O(n)` is true. But `5n + 12 = O(n²)` is **also true** — because n² is also an upper bound (any function growing as fast or faster than n grows no faster than n² as well)!

```
5n + 12 ≤ c·n²  for c=1, n₀=6:  5(6)+12=42 ≤ 36? NO. Try n₀=17: 5(17)+12=97 ≤ 289? YES.
```

Big-O only claims an upper bound — it does not claim the bound is the *tightest possible* one. This is why we need Big-Ω and Big-Θ.

---

## 3. Formal Definition of Big-Ω (Big-Omega)

**Definition:** We say f(n) = Ω(g(n)) if there exist positive constants c and n₀ such that:

```
f(n) ≥ c · g(n)   for all n ≥ n₀
```

In words: g(n) is a **lower bound** on f(n)'s growth rate. f grows **at least** as fast as g (up to a constant factor).

### Worked Proof: Show that `n² + 3n = Ω(n²)`

Try c = 1:
```
n² + 3n ≥ 1·n²
3n ≥ 0
```
This holds for all n ≥ 0. So choose n₀ = 0, c = 1.

**Proof:** For all n ≥ 0: `n² + 3n ≥ n²`. Therefore `n² + 3n = Ω(n²)`. ∎

**Big-Ω describes the best-case floor.** It says: no matter what, this algorithm cannot do better than this growth rate.

---

## 4. Formal Definition of Big-Θ (Big-Theta)

**Definition:** We say f(n) = Θ(g(n)) if f(n) = O(g(n)) **AND** f(n) = Ω(g(n)).

Equivalently: there exist positive constants c₁, c₂, and n₀ such that:

```
c₁ · g(n) ≤ f(n) ≤ c₂ · g(n)   for all n ≥ n₀
```

**Big-Θ is the tight bound** — it says f(n) grows *exactly* at the rate of g(n), both from above and below (up to constant factors). This is the strongest and most informative statement.

### Worked Proof: Show that `n² + 3n = Θ(n²)`

We already proved `n² + 3n = O(n²)` (Section 2) and `n² + 3n = Ω(n²)` (Section 3).

By definition, `n² + 3n = Θ(n²)`. ∎

**In casual conversation, people often say "Big-O" when they mean "Big-Θ."** When we say "merge sort is O(n log n)," we usually mean it is Θ(n log n) — both an upper AND lower bound. Being aware of this distinction matters in formal contexts (like CS 301, Theory of Computation), but for this course, we'll follow the common convention of using O() to describe tight bounds when the context makes clear that's what we mean.

---

## 5. The Complete Hierarchy of Complexity Classes

Ranked from fastest-growing to slowest-growing (as n → ∞):

| Notation | Name | Example Algorithm | n=10 | n=1,000 | n=1,000,000 |
|----------|------|-------------------|------|---------|--------------|
| O(1) | Constant | Array index access | 1 | 1 | 1 |
| O(log n) | Logarithmic | Binary search | 3 | 10 | 20 |
| O(n) | Linear | Linear search | 10 | 1,000 | 1,000,000 |
| O(n log n) | Linearithmic | Merge sort | 33 | 9,966 | 2×10⁷ |
| O(n²) | Quadratic | Selection sort | 100 | 10⁶ | 10¹² |
| O(n³) | Cubic | Naive matrix multiply | 1,000 | 10⁹ | 10¹⁸ |
| O(2ⁿ) | Exponential | Naive Fibonacci | 1,024 | astronomical | impossible |
| O(n!) | Factorial | Brute-force TSP | 3.6M | impossible | impossible |

**The critical lesson:** for n=1,000,000, the difference between O(n log n) (≈20 million operations, instant) and O(n²) (≈10¹² operations, hours) is not a minor inefficiency — it is the difference between a working system and a broken one.

---

## 6. Analyzing Loops — The Systematic Method

### Rule 1: Sequential statements — add complexities

```python
def f(n):
    for i in range(n):      # O(n)
        print(i)
    for j in range(n):      # O(n)
        print(j)
    # Total: O(n) + O(n) = O(n)  (constants drop out)
```

### Rule 2: Nested loops — multiply complexities

```python
def f(n):
    for i in range(n):       # O(n) outer
        for j in range(n):   # O(n) inner
            print(i, j)
    # Total: O(n) × O(n) = O(n²)
```

### Rule 3: Loop bounds that depend on input size determine the count directly

```python
def f(n):
    for i in range(n):
        for j in range(i):    # inner loop runs i times, not n times
            print(i, j)
    # Total iterations: 0 + 1 + 2 + ... + (n-1) = n(n-1)/2 = O(n²)
    # Still quadratic! Even though the inner loop is "shorter" on average.
```

### Rule 4: Loops that shrink geometrically → logarithmic

```python
def f(n):
    while n > 1:
        n = n // 2      # halves each time
        print(n)
    # Total iterations: log2(n) = O(log n)
```

### Rule 5: Function calls inside loops — multiply by the call's complexity

```python
def is_prime(n):          # O(sqrt(n))
    ...

def count_primes(numbers):
    count = 0
    for x in numbers:      # O(n) where n = len(numbers)
        if is_prime(x):    # O(sqrt(x)) per call
            count += 1
    # Total: O(n * sqrt(max_value)) — NOT simply O(n)!
```

**This is a critical and commonly-missed error:** if you call a function with its own non-constant complexity inside a loop, you must multiply, not just count the loop iterations.

---

## 7. Worked Complexity Analysis — Complete Examples

### Example 1:

```python
def example_1(lst):
    total = 0
    for x in lst:              # O(n)
        total += x
    return total
```
**Analysis:** single loop over n elements, O(1) work per iteration. **O(n).**

### Example 2:

```python
def example_2(lst):
    n = len(lst)
    for i in range(n):          # O(n)
        for j in range(n):      # O(n)
            if lst[i] == lst[j]:
                print("match")
    # O(n) * O(n) = O(n²)
```

### Example 3:

```python
def example_3(lst):
    n = len(lst)
    for i in range(n):           # O(n)
        for j in range(i, n):    # runs (n-i) times
            print(lst[i], lst[j])
    # Total iterations: n + (n-1) + (n-2) + ... + 1 = n(n+1)/2 = O(n²)
    # Still O(n²) even though the inner loop is "triangular"!
```

### Example 4:

```python
def example_4(lst):
    n = len(lst)
    i = 1
    while i < n:               # i doubles each iteration
        print(lst[i])
        i *= 2
    # Total iterations: log2(n)  →  O(log n)
```

### Example 5 — combining rules:

```python
def example_5(matrix):
    """matrix is an n x n grid."""
    n = len(matrix)
    total = 0
    for i in range(n):              # O(n)
        for j in range(n):          # O(n)
            for k in range(j):      # runs up to n times (triangular, still O(n))
                total += matrix[i][j]
    # O(n) * O(n) * O(n) = O(n³)
```

---

## 8. Space Complexity — Not Just Time

We've focused on **time complexity** (number of operations), but **space complexity** (amount of extra memory used) matters equally.

```python
def sum_list(lst):
    """O(n) time, O(1) space — no extra memory proportional to input."""
    total = 0
    for x in lst:
        total += x
    return total

def duplicate_list(lst):
    """O(n) time, O(n) space — creates a new list of size n."""
    return lst[:]

def merge_sort(lst):
    """O(n log n) time, O(n) space — auxiliary arrays for merging."""
    ...

def selection_sort(lst):
    """O(n²) time, O(1) space — sorts in place, no extra arrays."""
    ...
```

**Space-time tradeoffs** appear constantly: memoization (Week 4) trades O(n) extra space for exponential time savings. This tradeoff — spend memory to save time, or vice versa — is one of the most important decisions in algorithm design, and we'll see it repeatedly in CS 102 (dynamic programming) and beyond.

---

## Summary

| Notation | Meaning | Analogy |
|----------|---------|---------|
| O(g(n)) | f grows **no faster** than g (upper bound) | "at most" |
| Ω(g(n)) | f grows **at least as fast** as g (lower bound) | "at least" |
| Θ(g(n)) | f grows **exactly** as fast as g (tight bound) | "exactly" |

| Rule | Effect |
|------|--------|
| Sequential loops | Add complexities |
| Nested loops | Multiply complexities |
| Halving loops | Logarithmic |
| Function calls with non-constant complexity | Multiply, don't just count iterations |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Give a tight Θ bound for each, and state the exact count where the notation hides something interesting.

```python
# A
for i in range(n):
    for j in range(n):
        work()

# B
for i in range(n):
    for j in range(i):
        work()

# C
i = 1
while i < n:
    work()
    i *= 2

# D
for i in range(n):
    j = 1
    while j < n:
        work()
        j *= 2
```

**2. (Explain.)** Prove from the formal definition in §2 that 3n² + 100n + 7 is O(n²). Give explicit c and n₀. Then explain why the statement "3n² + 100n + 7 is O(n³)" is also true, and why it is nevertheless a worse answer.

**3. (Build.)** Analyse this function's time **and space** complexity, and explain why the two differ.

```python
def pairs(xs):
    out = []
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            if xs[i] + xs[j] == 0:
                out.append((xs[i], xs[j]))
    return out
```

**4. (Stretch.)** Rank these by growth rate, slowest-growing first, and identify the two that are in the same Θ class.

`n log n`, `2ⁿ`, `n!`, `log(n!)`, `n²`, `√n`, `n^1.5`, `log₂ n`, `n log₄ n`


### Answers

**1.** A: **Θ(n²)**, exactly n² calls.

B: **Θ(n²)**, exactly n(n−1)/2 calls. Same class as A with **half the constant** — Big-Θ deliberately discards that factor, which is why two algorithms in the same class can still differ by 2× in practice.

C: **Θ(log n)**, exactly ⌊log₂(n−1)⌋ + 1 calls. `i` doubles, so it reaches n after log₂ n steps. Any loop whose counter is *multiplied* rather than incremented is logarithmic, and the base of the logarithm changes only the constant — which is why nobody writes the base.

D: **Θ(n log n)**. The outer loop runs n times and the inner loop is independent of `i`, so the counts multiply.

The systematic method from §6: work outward, and **multiply** when an inner loop's bound is independent of the outer variable, **sum** when it is not. B is the case where you must sum — writing it as n × n because "the inner loop runs up to n times" gives the right Θ by luck and the wrong count.

**2.** **Definition.** f(n) is O(g(n)) iff there exist constants c > 0 and n₀ ≥ 0 such that f(n) ≤ c·g(n) for all n ≥ n₀.

**Proof.** Take n₀ = 1. For every n ≥ 1 we have n ≤ n² and 1 ≤ n², so

3n² + 100n + 7 ≤ 3n² + 100n² + 7n² = 110n².

So **c = 110, n₀ = 1** witnesses the claim. ∎ (The constants are not unique — c = 4 with n₀ = 101 also works, and is tighter. Any valid pair proves it.)

**O(n³) is also true**, because n² ≤ n³ for n ≥ 1, so the same inequality chain gives 3n² + 100n + 7 ≤ 110n³. Big-O is an **upper bound**, not an exact description — it is `≤`, not `=`. Every O(n²) function is also O(n³), O(n⁴), and O(2ⁿ).

It is a worse answer because it is **loose**: it discards information you have. The precise tool is Big-Θ, which requires matching upper *and* lower bounds — and 3n² + 100n + 7 is Θ(n²) but **not** Θ(n³). When someone says an algorithm "is O(n²)" and means it is tight, they are speaking informally; say Θ when you mean Θ.

**3.** **Time: Θ(n²).** The loops run n(n−1)/2 times regardless of the data, and the body is O(1).

**Space: O(n²) worst case, O(1) auxiliary in the best case.** The distinction is the point. The function allocates no scratch space — everything it holds is the output list. On input `[1, -1, 1, -1, ...]` roughly n²/4 pairs sum to zero, so `out` grows quadratically. On input `[1, 2, 3, ...]` nothing matches and `out` stays empty.

Time and space differ because **time counts work done, space counts data retained.** A Θ(n²) loop that keeps nothing is Θ(1) space; a Θ(n) loop that copies its input is Θ(n) space.

Two conventions worth stating explicitly. Complexity is measured in **auxiliary** space — the input itself is not counted, or every algorithm would be Ω(n). And output size is usually excluded too when the output *is* the answer, since you cannot produce n² pairs in less than n² space. Under that convention this function is **O(1) auxiliary space**, which is the more informative statement.

Incidentally, a dict makes this Θ(n) time — see L27 §5.

**4.** **log₂ n < √n < n log n ≈ n log₄ n ≈ log(n!) < n^1.5 < n² < 2ⁿ < n!**

The two — really three — in the same class: **n log n, n log₄ n, and log(n!) are all Θ(n log n)**.

- `n log₄ n = n·(log₂ n)/(log₂ 4) = (n log₂ n)/2`. Changing the base of a logarithm multiplies by a constant, and constants vanish. This is why the base is never written.
- `log(n!)` = Θ(n log n) by Stirling's approximation, which is exactly the fact behind the comparison-sort lower bound in L18 §5.

Two rankings people get wrong: **√n < n log n** — a common error is to place √n above logarithmic-ish terms without noticing √n = n^0.5 grows polynomially while log n does not. And **n^1.5 sits strictly between n log n and n²**, since log n grows slower than any positive power of n.

The general facts worth memorising: any power of log beats any positive power of n; any polynomial beats any exponential with base > 1; and n! beats 2ⁿ (n! has n factors averaging ~n/2, versus n factors of 2).



---

## Reading

- **CLRS, Ch. 3** — Growth of Functions (the definitive formal treatment; read 3.1–3.2)
- **Guttag, Ch. 6.1–6.2** — Complexity introduction (if covered in your edition)

---

*CS 101 · Week 6 · Lecture 19 (Wed) · © CSE Department*
