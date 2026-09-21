# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 3.3 (L11) — Strong Induction and the Well-Ordering Principle
### Friday, Week 3

**Date:** Friday 16 October 2026 · 13:00–13:50 · Week 3

---

> **Core Question:** When is the ordinary induction hypothesis P(k) not enough, and how do we harness all of P(1), P(2), …, P(k) simultaneously?

---

## 1. The Limitation of Weak Induction

Weak induction assumes P(k) to prove P(k+1). This works perfectly when P(k+1) can be reduced to P(k) in one step. But some problems are structured differently:

- **Fibonacci:** $F_{n} = F_{n-1} + F_{n-2}$ — each term depends on the *two* previous terms
- **Prime factorization:** to factor n, you factor numbers smaller than n (not necessarily n−1)
- **Recursive algorithms on arbitrary sub-problems:** the recursive call may not always be on input n−1

In these cases, weak induction — which only gives you P(k) — is insufficient. We need P(k), P(k−1), …, P(1) simultaneously.

---

## 2. The Principle of Strong Induction

**Theorem (Strong Induction).** Let P(n) be a predicate over ℕ. If:
1. **Base case(s):** P(n₀), P(n₀+1), …, P(n₀+j) are true for some j ≥ 0, AND
2. **Inductive step:** For all k ≥ n₀ + j, if P(n₀), P(n₀+1), …, P(k) all hold, then P(k+1) holds,

then P(n) holds for all n ≥ n₀.

**The induction hypothesis in strong induction:** "P(m) holds for all m with n₀ ≤ m ≤ k."

This is a much richer IH — instead of just P(k), you may assume the entire history P(n₀) through P(k).

**Is strong induction "stronger" than weak induction?**

No — they are logically equivalent. Any theorem provable by strong induction is provable by weak induction (just modify the predicate), and vice versa. Strong induction is not more powerful in the logical sense; it is simply more *convenient* for certain problems.

---

## 3. How Many Base Cases?

If the inductive step uses P(k), P(k−1), …, P(k−j+1) to prove P(k+1), then you need at least j base cases.

- Weak induction (uses P(k) only): 1 base case
- Fibonacci-style recursion (uses P(k) and P(k−1)): **2 base cases**
- A recursion that jumps back up to 3 steps: **3 base cases**

**Rule:** You need as many base cases as the maximum "lookback" in your inductive step.

---

## 4. Worked Examples

### Example 1: Prime Factorization

**Theorem.** Every integer n ≥ 2 can be written as a product of primes.

(This is half of the Fundamental Theorem of Arithmetic — the existence part.)

**Why weak induction fails:** If n is composite, n = ab with 2 ≤ a, b < n. We need to use the fact that a and b (which could be anything from 2 to n−1) have prime factorizations — not just n−1.

**Proof.** By strong induction on n.

**Base case (n = 2):** 2 is itself prime, so 2 = 2 is a product of primes (a product with one factor). ✓

**Inductive step:**
Let k ≥ 2 be arbitrary. Assume every integer m with 2 ≤ m ≤ k has a prime factorization. [Strong IH]

We must show k+1 has a prime factorization.

**Case 1:** k+1 is prime. Then k+1 is itself a product of primes (one factor). ✓

**Case 2:** k+1 is composite. Then k+1 = ab for some integers a, b with 2 ≤ a ≤ b < k+1.

Since 2 ≤ a ≤ k and 2 ≤ b ≤ k, both a and b satisfy the strong IH.
By IH: a = p₁p₂…pᵣ and b = q₁q₂…qₛ for primes pᵢ, qⱼ.
Therefore k+1 = ab = p₁p₂…pᵣq₁q₂…qₛ, a product of primes. ✓

By strong induction, every integer n ≥ 2 has a prime factorization. ∎

**Why strong induction was essential:** In Case 2, a and b could be anywhere in [2, k]. Weak induction would only give us P(k) = the factorization of k, which doesn't help with arbitrary a, b.

---

### Example 2: Fibonacci Upper Bound

**Theorem.** For all n ≥ 1, $F_n \leq 2^{n-1}$.

(F₁ = 1, F₂ = 1, Fₙ = Fₙ₋₁ + Fₙ₋₂ for n ≥ 3.)

**Proof.** By strong induction.

**Base cases:**
- n = 1: $F_1 = 1 \leq 1 = 2^0$. ✓
- n = 2: $F_2 = 1 \leq 2 = 2^1$. ✓

**Inductive step:**
Let k ≥ 2. Assume $F_m \leq 2^{m-1}$ for all m with 1 ≤ m ≤ k. [Strong IH]

$$F_{k+1} = F_k + F_{k-1} \leq 2^{k-1} + 2^{k-2} \quad \text{[Strong IH applied to } m=k \text{ and } m=k-1\text{]}$$

$$= 2^{k-2}(2 + 1) = 3 \cdot 2^{k-2} \leq 4 \cdot 2^{k-2} = 2^k$$

So $F_{k+1} \leq 2^k = 2^{(k+1)-1}$. ✓ ∎

---

### Example 3: Postage Stamps (Classic)

**Theorem.** Every integer n ≥ 8 can be expressed as $3a + 5b$ for non-negative integers a and b.

(You have unlimited 3-cent and 5-cent stamps; you can make any postage ≥ 8 cents.)

**Why we need strong induction:** Making postage of n+1 cents doesn't directly reduce to n cents — you might need to change which stamps you use entirely. But n−2 or n−3 might be directly useful.

**Proof.** By strong induction on n.

**Base cases:**
- n = 8: $8 = 3 + 5 = 3(1) + 5(1)$. ✓
- n = 9: $9 = 3 \cdot 3 = 3(3) + 5(0)$. ✓
- n = 10: $10 = 5 \cdot 2 = 3(0) + 5(2)$. ✓

**Inductive step:**
Let k ≥ 10. Assume every integer m with 8 ≤ m ≤ k can be expressed as $3a + 5b$. [Strong IH]

Consider k+1. Since k ≥ 10, we have k+1 ≥ 11 > 8, so k+1−3 = k−2 ≥ 8.

By the strong IH applied to m = k−2: $k-2 = 3a + 5b$ for some non-negative integers a, b.

Therefore: $k+1 = (k-2) + 3 = 3a + 5b + 3 = 3(a+1) + 5b$.

Since a+1 ≥ 1 ≥ 0 and b ≥ 0, this is a valid representation. ✓

By strong induction, every integer n ≥ 8 can be expressed as $3a + 5b$. ∎

**The strategy:** To prove P(k+1), we looked back at P(k−2) (not P(k)) because adding 3 to a representation of k−2 gives a representation of k+1. The strong IH let us reach back three steps.

---

### Example 4: Recursive Algorithm with Halving

**Claim:** The following algorithm computes $2^n$ correctly for all $n \geq 0$.

```python
def power_of_two(n):
    if n == 0:
        return 1
    elif n % 2 == 0:              # n is even
        half = power_of_two(n // 2)
        return half * half
    else:                          # n is odd
        return 2 * power_of_two(n - 1)
```

**Proof.** By strong induction on n.

**Base case (n = 0):** `power_of_two(0)` returns 1 = $2^0$. ✓

**Inductive step:**
Let k ≥ 0. Assume `power_of_two(m)` returns $2^m$ for all m with 0 ≤ m ≤ k. [Strong IH]

Consider `power_of_two(k+1)`.

**Case 1: k+1 is even.** Let k+1 = 2t, so t = (k+1)/2 ≤ k (since k+1 ≥ 2 means t ≤ k).
The function computes `half = power_of_two(t)`.
By Strong IH (since t ≤ k): `half` = $2^t$.
Returns `half * half` = $(2^t)^2 = 2^{2t} = 2^{k+1}$. ✓

**Case 2: k+1 is odd.** k+1−1 = k ≤ k.
The function computes `2 * power_of_two(k)`.
By Strong IH: `power_of_two(k)` = $2^k$.
Returns $2 \cdot 2^k = 2^{k+1}$. ✓

By strong induction, `power_of_two(n)` returns $2^n$ for all n ≥ 0. ∎

**Why strong induction was needed:** In Case 1, the recursive call is on t = (k+1)/2, which is much smaller than k. Weak induction would only give us the correctness at k, not at t.

---

## 5. Well-Ordering Principle — Proof Technique

The Well-Ordering Principle (WOP) states that every nonempty subset of ℕ has a least element. It is equivalent to strong induction and provides another proof structure.

**Template for WOP proofs:**
1. Suppose claim P(n) is false for some n.
2. Let S = {n ∈ ℕ : P(n) is false} — nonempty by assumption.
3. By WOP, S has a least element m.
4. Derive a contradiction — either:
   - Show P(m) actually holds (contradicting m ∈ S), or
   - Show P(m) implies some m' < m is also in S (contradicting m being least)

### Example: WOP Proof of Irrationality of √2

We already proved this by contradiction. Here is an alternative using WOP (infinite descent).

**Proof.** Suppose $\sqrt{2} = p/q$ for positive integers p and q. Consider the set:

$S = \{q \in \mathbb{Z}^+ : \sqrt{2} = p/q \text{ for some } p \in \mathbb{Z}^+\}$

S is nonempty by assumption. By WOP, S has a smallest element q₀. Let $\sqrt{2} = p_0/q_0$.

Then $p_0 = \sqrt{2} \cdot q_0$ and $p_0^2 = 2q_0^2$, so $p_0^2$ is even, hence $p_0$ is even. Write $p_0 = 2r$.

Then $4r^2 = 2q_0^2$, so $q_0^2 = 2r^2$, so $q_0$ is even. Write $q_0 = 2s$.

Then $\sqrt{2} = p_0/q_0 = 2r/2s = r/s$, so $s \in S$.

But $s = q_0/2 < q_0$, contradicting the minimality of $q_0$. ∎

---

## 6. Choosing Between Weak and Strong Induction

| Use Weak Induction When | Use Strong Induction When |
|---|---|
| P(k+1) depends only on P(k) | P(k+1) depends on P(j) for multiple j ≤ k |
| Recurrence is f(n) = g(f(n−1)) | Recurrence uses f(n−1), f(n−2), …, f(n−j) |
| Recursive algorithm always recurses on n−1 | Recursive algorithm recurses on arbitrary smaller input |
| Summation/product formulas | Prime factorization, Fibonacci-like sequences |
| Simple divisibility | Coin problems, postage problems |

---

## 7. Summary — Strong Induction Template

```
Claim: P(n) holds for all n ≥ n₀.

Proof. By strong mathematical induction on n.

Base case(s): Verify P(n₀), P(n₀+1), ..., P(n₀+j) directly.

Inductive step: Let k ≥ n₀ + j be arbitrary.
  Assume P(m) holds for all m with n₀ ≤ m ≤ k. [Strong IH]
  We prove P(k+1).
  
  [Express P(k+1) in terms of P(m) for some m ≤ k.]
  [Apply the Strong IH to those m values.]
  [Derive P(k+1).]

By the Principle of Strong Induction, P(n) holds for all n ≥ n₀. ∎
```

---

## 8. End-of-Lecture Exercises

1. Prove by strong induction:
   - (a) Every integer $n \geq 2$ is either prime or a product of primes (restating the theorem from this lecture — write a complete clean proof).
   - (b) Every integer $n \geq 12$ can be expressed as $4a + 5b$ for non-negative integers $a, b$.
   - (c) The sequence defined by $a_1 = 1, a_2 = 3, a_n = a_{n-1} + 2a_{n-2}$ satisfies $a_n \leq 3^{n-1}$ for all $n \geq 1$.

2. Prove by strong induction: For all $n \geq 1$, $F_n \geq \phi^{n-2}$ where $\phi = (1+\sqrt{5})/2 \approx 1.618$ (the golden ratio).
   *Hint:* You will need the identity $\phi^2 = \phi + 1$.

3. Determine whether weak or strong induction is needed for each. Justify your answer without writing the full proof:
   - (a) For all $n \geq 1$, $\sum_{i=1}^{n} i = n(n+1)/2$.
   - (b) Every $n \geq 2$ has a unique prime factorization (uniqueness part).
   - (c) The sequence $a_n = 3a_{n-1} - 2a_{n-2}$ with $a_1=1, a_2=3$ satisfies $a_n = 2^{n-1} + (-1)^n \cdot 0$... compute a formula and decide.
   - (d) The number of regions created by n lines in general position in the plane is $1 + n + \binom{n}{2}$.

4. **CS application:** Prove by strong induction that merge sort (which splits an array of size n into two halves, sorts each recursively, then merges) correctly sorts any array of size n ≥ 1.
   *State the induction hypothesis clearly. You may assume the merge step is correct.*

5. Use the Well-Ordering Principle to prove: there is no infinite strictly decreasing sequence of natural numbers $n_1 > n_2 > n_3 > \ldots$

---

*Week 3 complete. Week 4: Sets — Operations, Power Sets, Cartesian Products, and Set Proofs.*
