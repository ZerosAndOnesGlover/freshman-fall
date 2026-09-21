# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 3.2 (L10) — Induction Applications: Inequalities, Divisibility, and Recursion
### Thursday, Week 3

**Date:** Thursday 15 October 2026 · 13:00–13:50 · Week 3

---

> **Core Question:** How does induction extend beyond summation formulas to inequalities, recursive definitions, and algorithm correctness?

---

## 1. Inequalities by Induction

Induction on inequalities requires a different technique from summation formulas. Instead of computing both sides and checking equality, you must manipulate the inequality carefully — using the induction hypothesis as a bound.

**Key technique:** In the inductive step, when proving P(k+1) from P(k), you will have an inequality P(k) as your IH. To prove P(k+1):
1. Write the expression in P(k+1) in terms of an expression in P(k).
2. Apply the IH to get a bound.
3. Show that this bound is sufficient.

---

### Example 1: Exponential vs Polynomial

**Theorem.** For all n ≥ 1, $2^n > n$.

**Proof.** By mathematical induction on n.

**Base case (n = 1):** $2^1 = 2 > 1$. ✓

**Inductive step:**
Let k ≥ 1 be arbitrary. Assume $2^k > k$. [IH]
We must show $2^{k+1} > k+1$.

$$2^{k+1} = 2 \cdot 2^k > 2k \quad \text{[IH: } 2^k > k\text{, multiply both sides by 2]}$$

Now we need $2k \geq k+1$, i.e., $k \geq 1$, which holds since $k \geq 1$.

Therefore $2^{k+1} > 2k \geq k+1$. ✓

By induction, $2^n > n$ for all $n \geq 1$. ∎

**Anatomy of the technique:** We wrote $2^{k+1} = 2 \cdot 2^k$, applied IH to replace $2^k > k$, then showed $2k \geq k+1$ from $k \geq 1$. The chain of inequalities $2^{k+1} > 2k \geq k+1$ gives the result.

---

### Example 2: A Tighter Inequality

**Theorem.** For all n ≥ 4, $2^n > n^2$.

Note the base case starts at n = 4 (the formula fails for n = 1, 2, 3).

**Proof.** By mathematical induction on n, starting from n = 4.

**Base case (n = 4):** $2^4 = 16 > 16 = 4^2$? No — $16 \not> 16$. The claim uses $>$, not $\geq$.

Check again: $2^4 = 16$ and $4^2 = 16$. So $16 \not> 16$. **The claim is false for n = 4!**

**Correction:** The correct statement is $2^n \geq n^2$ for $n = 4$, and $2^n > n^2$ for $n \geq 5$.

Let us prove: For all n ≥ 5, $2^n > n^2$.

**Base case (n = 5):** $2^5 = 32 > 25 = 5^2$. ✓

**Inductive step:**
Assume $2^k > k^2$ for some $k \geq 5$. [IH]
Goal: $2^{k+1} > (k+1)^2$.

$$2^{k+1} = 2 \cdot 2^k > 2k^2 \quad \text{[IH]}$$

We need to show $2k^2 \geq (k+1)^2 = k^2 + 2k + 1$, i.e., $k^2 - 2k - 1 \geq 0$, i.e., $(k-1)^2 \geq 2$.

For $k \geq 5$: $(k-1)^2 \geq 4^2 = 16 > 2$. ✓

Therefore $2^{k+1} > 2k^2 \geq (k+1)^2$. ✓

By induction, $2^n > n^2$ for all $n \geq 5$. ∎

**Lesson:** Always verify your base case before claiming a theorem. The specific starting value matters.

---

### Example 3: Bernoulli's Inequality

**Theorem.** For all $n \geq 1$ and $x \geq -1$: $(1+x)^n \geq 1 + nx$.

**Proof.** By mathematical induction on n (treating x as a fixed parameter with $x \geq -1$).

**Base case (n = 1):** $(1+x)^1 = 1+x \geq 1+1\cdot x$. ✓ (equality)

**Inductive step:**
Assume $(1+x)^k \geq 1+kx$. [IH]

$$(1+x)^{k+1} = (1+x)^k \cdot (1+x) \geq (1+kx)(1+x) \quad \text{[IH, using } 1+x \geq 0\text{]}$$

$$= 1 + x + kx + kx^2 = 1 + (k+1)x + kx^2 \geq 1 + (k+1)x$$

The last step uses $kx^2 \geq 0$, which holds since $k \geq 1$ and $x^2 \geq 0$.

Therefore $(1+x)^{k+1} \geq 1 + (k+1)x$. ✓ ∎

**Note:** When multiplying an inequality by $(1+x)$, we used $1+x \geq 0$ (which holds since $x \geq -1$). If $1+x$ could be negative, multiplying would flip the inequality. Always check the sign when multiplying inequalities.

---

## 2. Divisibility by Induction

### Example 4

**Theorem.** For all n ≥ 0, $5 \mid (8^n - 3^n)$.

**Proof.** By induction on n.

**Base case (n = 0):** $8^0 - 3^0 = 1 - 1 = 0 = 5 \cdot 0$. So $5 \mid 0$. ✓

**Inductive step:**
Assume $5 \mid (8^k - 3^k)$. Then $8^k - 3^k = 5m$ for some $m \in \mathbb{Z}$, so $8^k = 3^k + 5m$.

$$8^{k+1} - 3^{k+1} = 8 \cdot 8^k - 3 \cdot 3^k$$

$$= 8(3^k + 5m) - 3 \cdot 3^k \quad \text{[substituting } 8^k = 3^k + 5m\text{]}$$

$$= 8 \cdot 3^k + 40m - 3 \cdot 3^k = 5 \cdot 3^k + 40m = 5(3^k + 8m)$$

Since $3^k + 8m \in \mathbb{Z}$, $5 \mid (8^{k+1} - 3^{k+1})$. ✓ ∎

**The key technique:** Express $8^{k+1}$ in terms of $8^k$ (via $8^{k+1} = 8 \cdot 8^k$), then use the IH to substitute for $8^k$.

---

### Example 5: A General Pattern

**Theorem.** For all n ≥ 1, $(a - b) \mid (a^n - b^n)$ for any integers a, b.

**Proof.** By induction on n.

**Base case (n = 1):** $a^1 - b^1 = a - b = 1 \cdot (a-b)$. So $(a-b) \mid (a-b)$. ✓

**Inductive step:**
Assume $(a-b) \mid (a^k - b^k)$.

$$a^{k+1} - b^{k+1} = a^{k+1} - ab^k + ab^k - b^{k+1}$$
$$= a(a^k - b^k) + b^k(a - b)$$

By IH, $(a-b) \mid (a^k - b^k)$, so $(a-b) \mid a(a^k - b^k)$.
Also $(a-b) \mid b^k(a-b)$ trivially.
Therefore $(a-b) \mid [a(a^k - b^k) + b^k(a-b)] = a^{k+1} - b^{k+1}$. ✓ ∎

---

## 3. Induction on Recursive Definitions

One of the most powerful applications of induction is proving properties of recursively defined sequences.

### Example 6: Fibonacci Sequence

**Definition.** The Fibonacci sequence is defined by:
$$F_1 = 1, \quad F_2 = 1, \quad F_n = F_{n-1} + F_{n-2} \text{ for } n \geq 3$$

**Theorem.** For all n ≥ 1, $F_n < 2^n$.

**Proof.** This requires proving two base cases since the recursive definition uses two prior values.

**Base cases:**
- n = 1: $F_1 = 1 < 2 = 2^1$. ✓
- n = 2: $F_2 = 1 < 4 = 2^2$. ✓

**Inductive step:**
Assume $F_k < 2^k$ and $F_{k-1} < 2^{k-1}$ for some $k \geq 2$. [IH — two hypotheses]

$$F_{k+1} = F_k + F_{k-1} < 2^k + 2^{k-1} = 2^{k-1}(2 + 1) = 3 \cdot 2^{k-1} < 4 \cdot 2^{k-1} = 2^{k+1}$$

So $F_{k+1} < 2^{k+1}$. ✓ ∎

**Note:** This is a preview of **strong induction** — the inductive step used both $F_k$ and $F_{k-1}$, requiring two induction hypotheses. We treat this more carefully in Friday's lecture.

---

## 4. Proving Algorithm Correctness by Induction

Induction is the rigorous tool for proving recursive algorithms correct. The structure maps perfectly:

| Algorithm Component | Induction Component |
|---|---|
| Base case of recursion | Base case of induction |
| Recursive call on smaller input | Induction hypothesis |
| Algorithm's work after recursive call | Inductive step |

### Example 7: Recursive Factorial

**Algorithm:**
```python
def factorial(n):
    if n == 0:
        return 1          # base case
    else:
        return n * factorial(n-1)   # recursive case
```

**Claim:** `factorial(n)` returns n! for all n ≥ 0.

**Proof.** By induction on n.

**Base case (n = 0):** `factorial(0)` returns 1 = 0!. ✓

**Inductive step:**
Assume `factorial(k)` returns k! for some k ≥ 0. [IH]

Consider `factorial(k+1)`:
- The `else` branch executes (since k+1 ≥ 1 > 0)
- It computes `(k+1) * factorial(k)`
- By IH, `factorial(k)` returns k!
- So the result is `(k+1) * k! = (k+1)!`

Therefore `factorial(k+1)` returns (k+1)!. ✓

By induction, `factorial(n)` returns n! for all n ≥ 0. ∎

---

### Example 8: Binary Search Correctness (Proof Sketch)

**Claim:** If `arr` is sorted and `target ∈ arr`, then `binary_search(arr, target)` returns an index i with `arr[i] = target`.

**Proof sketch by induction on the size of the search space n = hi − lo + 1.**

**Base case (n = 1):** Only one element. Either it equals target (return its index) or target ∉ arr (but we assumed target ∈ arr, contradiction). ✓

**Inductive step:** Assume binary search is correct on any sorted subarray of size < k. Given a subarray of size k:
- Compute mid. 
- If `arr[mid] = target`: return mid. ✓
- If `arr[mid] < target`: recurse on right half (size < k). By IH, correct. ✓
- If `arr[mid] > target`: recurse on left half (size < k). By IH, correct. ✓ ∎

---

## 5. Two Common Induction Errors

### Error 1: Using the Conclusion in the Inductive Step

**Flawed "proof"** that $n^2 + n + 41$ is prime for all n ≥ 0:

"Inductive step: Assume $k^2 + k + 41$ is prime. Then... [no valid argument follows, so the student assumes $(k+1)^2 + (k+1) + 41$ is also prime because it has the same form.]"

This is circular — assuming the conclusion.

**Truth:** $n^2 + n + 41$ is prime for $n = 0, 1, \ldots, 39$ but $40^2 + 40 + 41 = 41^2$, which is composite.

### Error 2: Wrong Inductive Step Direction

When asked to prove P(k) → P(k+1), students sometimes prove P(k+1) → P(k) (the wrong direction).

**Example:** "Prove $2^n > n$ for all n ≥ 1."

Wrong: "Assume $2^{k+1} > k+1$. Then $2^k > k$." (This proves the step backwards — you assumed what you're trying to prove and derived what you're allowed to assume.)

Right: "Assume $2^k > k$. Then $2^{k+1} = 2 \cdot 2^k > 2k \geq k+1$."

---

## 6. End-of-Lecture Exercises

1. Prove by induction:
   - (a) For all n ≥ 1, $3^n \geq 1 + 2n$.
   - (b) For all n ≥ 0, $4^n - 1$ is divisible by 3.
   - (c) For all n ≥ 1, $n! \geq 2^{n-1}$.

2. Let the sequence $a_n$ be defined by $a_1 = 3$ and $a_n = 2a_{n-1} + 1$ for $n \geq 2$. Conjecture a closed form for $a_n$, then prove it by induction.

3. Prove by induction that the recursive algorithm for computing the sum of an array is correct:
```python
def array_sum(arr, n):
    if n == 0:
        return 0
    else:
        return arr[n-1] + array_sum(arr, n-1)
```
**Claim:** `array_sum(arr, n)` returns $\sum_{i=0}^{n-1} \text{arr}[i]$ for all $n \geq 0$.

4. **Telescoping:** Prove that $\sum_{i=1}^{n} \frac{1}{i(i+1)} = \frac{n}{n+1}$ by induction. *(Compare to the pattern you found in Exercise 4 from Lecture 3.1.)*

5. Find the error: "Proof that all integers are equal: P(n) = 'in any set of n integers, all are equal.' Base: P(1) trivially true. Inductive step: given n+1 integers $a_1,\ldots,a_{n+1}$, by P(n) applied to $\{a_1,\ldots,a_n\}$: $a_1=\ldots=a_n$. By P(n) applied to $\{a_2,\ldots,a_{n+1}\}$: $a_2=\ldots=a_{n+1}$. Since $a_2$ is in both groups, all are equal." *(Same error as the horses — find it.)*

---

*Next: Lecture 3.3 — Strong Induction and the Well-Ordering Principle*
