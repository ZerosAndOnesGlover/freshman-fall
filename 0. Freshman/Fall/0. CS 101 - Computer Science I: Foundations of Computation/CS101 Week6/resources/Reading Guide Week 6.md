# CS 101 — Week 6 Reading Guide & Resources
## Algorithm Analysis: Big-O Notation

---

## Required Reading

### CLRS — Introduction to Algorithms (Primary reference for this week)

**Chapter 3 — Growth of Functions**
- §3.1 — Asymptotic notation (formal definitions of O, Ω, Θ, o, ω)
- §3.2 — Standard notations and common functions (logs, polynomials, exponentials, factorials)

This is the definitive formal treatment. Read it carefully — the definitions here are the ones used in every algorithms course you will ever take (CS 102, CS 301, and beyond).

**Chapter 4 — Divide-and-Conquer**
- §4.3–4.5 — The Master Method (formal statement and proof sketch of the Master Theorem)

### Guttag (if your edition covers complexity)

- Any section on "efficiency," "orders of growth," or "Big-O" — treat as a gentler, more Python-centric supplement to CLRS.

---

## Focused Practice Sessions

### Session A: Building Proof Intuition (20 min)

Work through these on paper, then check your reasoning against the lecture's worked examples.

**Practice 1:** Prove `7n + 3 = O(n)`.
- Try c=8. Solve: `7n+3 ≤ 8n` ⟺ `3 ≤ n`. So n₀=3, c=8. Verify: at n=3, `7(3)+3=24`, `8(3)=24`. 24≤24 ✓ (equality is fine — the definition uses ≤).

**Practice 2:** Prove `n² = Ω(n)`.
- Try c=1. `n² ≥ 1·n` ⟺ `n ≥ 1`. So n₀=1, c=1.
- This shows: a "bigger" function is always a valid Ω of a "smaller" one, in the direction that might feel counterintuitive at first — make sure you understand WHY: Ω is a LOWER bound, so saying n² is Ω(n) just means n² grows at least as fast as n, which is obviously true.

**Practice 3:** Is `n = O(1)`?
- Try to find c, n₀ such that `n ≤ c·1 = c` for all `n ≥ n₀`. This is impossible — no matter what constant c you pick, n eventually exceeds it. So `n ≠ O(1)`.

**Practice 4:** Is `log(n) = O(n)`?
- Yes. For all n≥1, `log(n) ≤ n` (verify: at n=1, log(1)=0≤1; and log(n) grows much slower than n for all n). So c=1, n₀=1 works.

### Session B: Recurrence Practice (20 min)

Solve each using the METHOD indicated.

```
1. T(n) = T(n/2) + O(1)               [Master Theorem]
   a=1, b=2, f(n)=O(1). n^(log_2 1) = n^0 = 1. f(n)=Θ(1) → Case 2.
   T(n) = Θ(log n)

2. T(n) = 4T(n/2) + O(n)              [Master Theorem]
   a=4, b=2, f(n)=O(n). n^(log_2 4) = n^2. f(n)=O(n) is polynomially SMALLER than n^2 → Case 1.
   T(n) = Θ(n²)

3. T(n) = T(n-1) + O(n)               [Substitution / expansion]
   Expand: T(n) = O(n) + O(n-1) + ... + O(1) = O(n²)   (arithmetic series)

4. T(n) = 2T(n-1) + O(1)              [Recursion tree — doesn't fit Master Theorem template]
   Tree: level k has 2^k nodes, depth n.
   Total = 2^0 + 2^1 + ... + 2^n = 2^(n+1) - 1 = O(2^n)
```

**Key skill check:** did you correctly identify that recurrence #3 and #4 do NOT fit the Master Theorem's `aT(n/b)+f(n)` template (since they involve n-1, not n/b)? This distinction is the single most common point of confusion this week.

### Session C: Empirical Verification in the REPL (15 min)

```python
import time

def measure(func, n, repeats=5):
    """Time func(n), taking the minimum over several repeats."""
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        func(n)
        times.append(time.perf_counter() - t0)
    return min(times)

def linear_work(n):
    total = 0
    for i in range(n):
        total += i
    return total

def quadratic_work(n):
    total = 0
    for i in range(n):
        for j in range(n):
            total += i + j
    return total

# Doubling test: as n doubles, how does time change?
print("Linear function — doubling n:")
prev_time = None
for n in [1000, 2000, 4000, 8000, 16000]:
    t = measure(linear_work, n)
    ratio = t / prev_time if prev_time else None
    print(f"  n={n:6}: {t*1000:8.3f}ms   ratio={ratio}")
    prev_time = t

print("\nQuadratic function — doubling n:")
prev_time = None
for n in [500, 1000, 2000, 4000]:
    t = measure(quadratic_work, n)
    ratio = t / prev_time if prev_time else None
    print(f"  n={n:6}: {t*1000:8.3f}ms   ratio={ratio}")
    prev_time = t

# Expected: linear ratios ≈ 2.0, quadratic ratios ≈ 4.0
```

---

## Conceptual Exercises (Paper and Pencil)

**Exercise 1:** Order these functions from slowest-growing to fastest-growing: `n²`, `log(n)`, `n!`, `n`, `n log n`, `2ⁿ`, `1`, `√n`.

**Exercise 2:** A function does exactly `f(n) = 100n + 5n log(n) + 2n²` operations. What is the TIGHT Big-Θ bound? (Hint: as n→∞, which term dominates?)

**Exercise 3:** For the recurrence `T(n) = 8T(n/2) + n²`, apply the Master Theorem. Compute `n^(log_2 8)` and compare to `f(n)=n²`. Which case applies? What is T(n)?

**Exercise 4:** True or false, with justification: "An algorithm with time complexity O(n) is always faster in practice than one with time complexity O(n²)." (Think about constant factors and the specific n you care about.)

---

## Key Formulas Reference Card

```
BIG-O DEFINITIONS
─────────────────
f(n) = O(g(n))  ⟺  ∃ c>0, n₀>0 : f(n) ≤ c·g(n) for all n ≥ n₀    (upper bound)
f(n) = Ω(g(n))  ⟺  ∃ c>0, n₀>0 : f(n) ≥ c·g(n) for all n ≥ n₀    (lower bound)
f(n) = Θ(g(n))  ⟺  f(n) = O(g(n)) AND f(n) = Ω(g(n))              (tight bound)

LOOP ANALYSIS RULES
───────────────────
Sequential loops:  O(f(n)) + O(g(n)) = O(max(f(n), g(n)))
Nested loops:      O(f(n)) × O(g(n))
Halving loops:     O(log n)
Function calls in loops: multiply loop count by the CALLED function's complexity

RECURRENCE SOLVING METHODS
───────────────────────────
1. Recursion tree: draw it, sum work per level across all levels
2. Substitution:   guess closed form, verify by induction
3. Master Theorem: for T(n) = aT(n/b) + f(n) ONLY
     compare f(n) to n^(log_b a):
       f(n) smaller  → T(n) = Θ(n^(log_b a))              [Case 1]
       f(n) equal    → T(n) = Θ(n^(log_b a) · log n)       [Case 2]
       f(n) larger   → T(n) = Θ(f(n))                       [Case 3]

COMMON COMPLEXITY CLASSES (increasing order)
──────────────────────────────────────────────
O(1) < O(log n) < O(√n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)
```

---

## Common Mistakes This Week

**Mistake 1: Confusing T(n-1) recurrences with T(n/2) recurrences**
```python
T(n) = 2T(n-1) + O(1)    # Exponential O(2^n) — NOT Master Theorem eligible!
T(n) = 2T(n/2) + O(1)    # Linear O(n) — Master Theorem Case 1
```
These look similar but have wildly different solutions. Always check: is the sub-problem size `n-c` (constant reduction) or `n/b` (proportional reduction)?

**Mistake 2: Forgetting that Big-O is an upper bound, not a description of tightness**
`5n = O(n²)` is TRUE (just not tight/useful). Don't assume "X = O(Y)" means "X grows exactly like Y" — that's what Θ is for.

**Mistake 3: Applying the Master Theorem when it doesn't fit**
The Master Theorem ONLY applies to `T(n) = aT(n/b) + f(n)` — constant number of equal-sized recursive sub-problems. Recurrences like Fibonacci's `T(n)=T(n-1)+T(n-2)` or unequal splits like `T(n)=T(n/3)+T(2n/3)+n` require different techniques (recursion tree, substitution).

**Mistake 4: Ignoring function call costs inside loops**
```python
for x in lst:              # O(n) iterations
    if is_prime(x):         # O(sqrt(x)) each — NOT O(1)!
        ...
# Total is NOT simply O(n) — must account for the per-call cost
```

**Mistake 5: Trusting Big-O alone to predict real-world speed for small/fixed n**
Big-O describes asymptotic behavior (as n→∞). For a fixed, small n, an algorithm with worse Big-O but smaller constants can easily be faster in practice. Always benchmark for your actual use case when it matters.

---

## Week 6 Self-Test

1. State the formal definition of `f(n) = O(g(n))`.
2. What's the difference between O, Ω, and Θ?
3. What is the rule for analyzing sequential loops? Nested loops?
4. Write the recurrence for binary search. Solve it.
5. Write the recurrence for merge sort. Solve it using the Master Theorem.
6. Why doesn't the Master Theorem apply to `T(n) = T(n-1) + T(n-2) + O(1)`?
7. What is amortized analysis? Give an example (from this week or Week 5).
8. If an algorithm's runtime data, plotted on a log-log scale, forms a line with slope ≈ 2, what is its likely complexity class?
9. Name one thing Big-O notation does NOT tell you about an algorithm's real-world performance.
10. A function has worst-case O(n²) but best-case O(n). Name an algorithm from Week 5 with this property, and describe the input that triggers each case.

*(Answers: 1. ∃c,n₀>0 s.t. f(n)≤c·g(n) for all n≥n₀. 2. O=upper bound, Ω=lower bound, Θ=tight bound (both). 3. sequential: add; nested: multiply. 4. T(n)=T(n/2)+O(1) → O(log n). 5. T(n)=2T(n/2)+O(n) → O(n log n) via Master Theorem Case 2. 6. sub-problems are n-1,n-2 (constant reduction), not n/b (proportional) — doesn't fit the template. 7. average cost per operation across a sequence, even if some individual operations are expensive; e.g. dynamic array doubling — O(1) amortized append despite occasional O(n) resizes. 8. O(n²). 9. constant factors / real hardware performance for specific, finite n. 10. insertion sort; worst case = reverse-sorted input, best case = already-sorted input.)*

---

## Preview: Week 7

Week 7 begins **Data Structures I: Lists, Stacks, and Queues** — the first of a multi-week sequence covering the fundamental building blocks used in every program you will ever write. You'll formally study Abstract Data Types (ADTs), implement linked lists from scratch, and analyze the complexity of every operation using exactly the tools you built this week.

Before Wednesday, think about: when you call `list.append()` in Python, what do you think happens internally? Does it always take the same amount of time, no matter how large the list is? (You already answered a version of this in Lab 6 / PS6's amortized analysis section — Week 7 will build directly on this.)

---

*CS 101 · Week 6 · Reading Guide · © CSE Department*
