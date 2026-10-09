# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 9 (L09) — Mathematical Induction: The Principle and Basic Applications
### Monday, Week 3

*“I may as well say at once that I do not distinguish between inference and deduction. What is called induction appears to me to be either disguised deduction or a mere method of making plausible guesses.”* — Bertrand Russell, *The Principles of Mathematics* (1903), ch. II

**Date:** Monday 12 October 2026 · 13:00–13:50 · Week 3

**Reading:** Rosen, 8e §5.1 · Epp, 5e §5.2 · Levin, 3e §2.5 *(details at the end of the lecture)*

**Coursework:** 📊 **Quiz 3** today 13:00–13:15 · 🔬 **Lab 2** Wed 14 Oct 15:00–16:50 · 📝 **PS 2** due Fri 16 Oct 17:00 · 📝 **PS 3** released Fri 16 Oct 14:00, due Fri 23 Oct 17:00

---

> **Core Question:** How do we prove a claim holds for every natural number — not just finitely many — with a finite proof?

---

## 1. The Problem with Universal Proofs Over ℕ

Consider the claim: "For all n ≥ 1, 1 + 2 + 3 + … + n = n(n+1)/2."

We cannot verify this for all n by checking cases — there are infinitely many. We need a fundamentally different argument: one that establishes the claim for ALL n simultaneously with a finite proof.

**The key insight:** If we can show:
1. The claim holds for the smallest case (n = 1), AND
2. Whenever the claim holds for some n, it also holds for n+1,

then the claim holds for all n ≥ 1. Why? Because (1) gives us n=1; then (2) gives n=2; then (2) again gives n=3; and so on — every natural number is eventually reached.

This is the Principle of Mathematical Induction.

---

## 2. The Principle of Mathematical Induction (Weak Form)

**Theorem (Principle of Mathematical Induction).** Let P(n) be a predicate over the natural numbers. If:
1. **Base case:** P(n₀) is true for some starting value n₀, AND
2. **Inductive step:** For all k ≥ n₀, P(k) → P(k+1),

then P(n) is true for all n ≥ n₀.

**Notation:**
- n₀ is the **base case** — typically 0 or 1, but can be any integer
- The assumption P(k) in the inductive step is called the **induction hypothesis (IH)**
- The goal of the inductive step is to prove P(k+1) using P(k)

**Why is this valid?** The Principle of Mathematical Induction is an axiom of the natural numbers (Peano's fifth axiom). It is equivalent to the **Well-Ordering Principle**: every nonempty subset of ℕ has a least element. We will use both formulations.

---

## 3. The Structure of an Induction Proof

Every induction proof has exactly this structure:

```
Proof. By mathematical induction on n.

Base case: [n = n₀]
  [Verify P(n₀) directly — typically a simple computation.]

Inductive step:
  Let k ≥ n₀ be arbitrary. Assume P(k). [This is the induction hypothesis.]
  [We must prove P(k+1).]
  [Derive P(k+1) using P(k) and algebraic steps.]
  [Conclude P(k+1) holds.]

By the principle of mathematical induction, P(n) holds for all n ≥ n₀.  ∎
```

**Critical discipline:** In the inductive step, you must use the induction hypothesis. If your proof of P(k+1) doesn't use P(k) anywhere, something is wrong.

---

## 4. Worked Examples — Summation Formulas

### Example 1: Gauss's Formula

**Theorem.** For all n ≥ 1:
$$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$

**Proof.** By mathematical induction on n.

**Base case (n = 1):**
Left side: $\sum_{i=1}^{1} i = 1$.
Right side: $\frac{1 \cdot 2}{2} = 1$.
Both sides equal 1. ✓

**Inductive step:**
Let k ≥ 1 be arbitrary. Assume $\sum_{i=1}^{k} i = \frac{k(k+1)}{2}$. [IH]

We must prove $\sum_{i=1}^{k+1} i = \frac{(k+1)(k+2)}{2}$.

$$\sum_{i=1}^{k+1} i = \left(\sum_{i=1}^{k} i\right) + (k+1)$$

$$= \frac{k(k+1)}{2} + (k+1) \quad \text{[by IH]}$$

$$= (k+1)\left(\frac{k}{2} + 1\right)$$

$$= (k+1) \cdot \frac{k+2}{2}$$

$$= \frac{(k+1)(k+2)}{2}$$

This is exactly $\frac{(k+1)((k+1)+1)}{2}$, which is P(k+1). ✓

By the principle of mathematical induction, the formula holds for all n ≥ 1. ∎

**Key move:** We split the sum $\sum_{i=1}^{k+1}$ into $\sum_{i=1}^{k}$ plus the last term $(k+1)$. This lets us apply the IH to $\sum_{i=1}^{k}$. This "peel off the last term" technique is the most common move in induction on sums.

---

### Example 2: Sum of Squares

**Theorem.** For all n ≥ 1:
$$\sum_{i=1}^{n} i^2 = \frac{n(n+1)(2n+1)}{6}$$

**Proof.** By mathematical induction on n.

**Base case (n = 1):**
Left: $1^2 = 1$. Right: $\frac{1 \cdot 2 \cdot 3}{6} = 1$. ✓

**Inductive step:**
Assume $\sum_{i=1}^{k} i^2 = \frac{k(k+1)(2k+1)}{6}$. [IH]

Goal: show $\sum_{i=1}^{k+1} i^2 = \frac{(k+1)(k+2)(2k+3)}{6}$.

$$\sum_{i=1}^{k+1} i^2 = \sum_{i=1}^{k} i^2 + (k+1)^2 = \frac{k(k+1)(2k+1)}{6} + (k+1)^2 \quad \text{[IH]}$$

$$= (k+1)\left[\frac{k(2k+1)}{6} + (k+1)\right] = (k+1) \cdot \frac{k(2k+1) + 6(k+1)}{6}$$

$$= (k+1) \cdot \frac{2k^2 + k + 6k + 6}{6} = (k+1) \cdot \frac{2k^2 + 7k + 6}{6}$$

$$= (k+1) \cdot \frac{(k+2)(2k+3)}{6} = \frac{(k+1)(k+2)(2k+3)}{6}$$

This equals $\frac{(k+1)((k+1)+1)(2(k+1)+1)}{6}$. ✓

By induction, the formula holds for all n ≥ 1. ∎

---

### Example 3: Geometric Series

**Theorem.** For all n ≥ 0 and r ≠ 1:
$$\sum_{i=0}^{n} r^i = \frac{r^{n+1} - 1}{r - 1}$$

**Proof.** By mathematical induction on n.

**Base case (n = 0):**
Left: $r^0 = 1$. Right: $\frac{r^1 - 1}{r - 1} = \frac{r-1}{r-1} = 1$. ✓

**Inductive step:**
Assume $\sum_{i=0}^{k} r^i = \frac{r^{k+1}-1}{r-1}$. [IH]

$$\sum_{i=0}^{k+1} r^i = \left(\sum_{i=0}^{k} r^i\right) + r^{k+1} = \frac{r^{k+1}-1}{r-1} + r^{k+1}$$

$$= \frac{r^{k+1}-1 + r^{k+1}(r-1)}{r-1} = \frac{r^{k+1} - 1 + r^{k+2} - r^{k+1}}{r-1} = \frac{r^{k+2} - 1}{r-1}$$

This is $\frac{r^{(k+1)+1}-1}{r-1}$. ✓ ∎

---

## 5. Worked Examples — Divisibility

### Example 4: Divisibility by 3

**Theorem.** For all n ≥ 0, $3 \mid (4^n - 1)$.

**Proof.** By mathematical induction on n.

**Base case (n = 0):**
$4^0 - 1 = 0$. Since $0 = 3 \cdot 0$, we have $3 \mid 0$. ✓

**Inductive step:**
Assume $3 \mid (4^k - 1)$. Then $4^k - 1 = 3m$ for some $m \in \mathbb{Z}$, so $4^k = 3m + 1$.

$$4^{k+1} - 1 = 4 \cdot 4^k - 1 = 4(3m+1) - 1 = 12m + 4 - 1 = 12m + 3 = 3(4m+1)$$

Since $4m+1 \in \mathbb{Z}$, we have $3 \mid (4^{k+1}-1)$. ✓

By induction, $3 \mid (4^n - 1)$ for all $n \geq 0$. ∎

---

## 6. The Well-Ordering Principle

**Theorem (Well-Ordering Principle).** Every nonempty subset S of ℕ has a smallest element.

This seems obvious but is actually equivalent to the Principle of Mathematical Induction — each can be derived from the other.

**Using WOP to prove a claim:**
1. Suppose the claim fails for some n.
2. Let S = {n ∈ ℕ : P(n) is false}.
3. Since S is nonempty, it has a least element m (by WOP).
4. Show this leads to a contradiction — typically, P(m) fails but P(m−1) holds, yet the inductive step would then force P(m) to hold.

WOP underlies the existence half of unique prime factorisation in Week 12, and it is the principle behind every "take a smallest counterexample" argument.

---

## 7. Why the Base Case Matters — A Famous False Proof

**"Theorem" (FALSE):** All horses are the same color.

**"Proof" by induction:** Let P(n) = "in any set of n horses, all horses have the same color."

**Base case (n = 1):** In any set of 1 horse, all horses trivially have the same color. ✓

**Inductive step:** Assume P(k): in any set of k horses, all are the same color. Consider any set of k+1 horses: {h₁, h₂, …, h_{k+1}}.

By P(k) applied to {h₁, …, h_k}: all of h₁, …, h_k are the same color.
By P(k) applied to {h₂, …, h_{k+1}}: all of h₂, …, h_{k+1} are the same color.

Since h₂ is in both groups, both groups share the same color. Therefore all k+1 horses have the same color. ✓

This gives P(n) for all n by induction. But the conclusion is clearly false! What went wrong?

**The error:** The inductive step fails when k = 1. With k+1 = 2 horses {h₁, h₂}: the first group is {h₁} and the second group is {h₂}. These two groups share NO horses in common — there is no h₂ "in both groups" to link them. The overlap argument requires the groups to have at least one element in common, which requires k ≥ 2, meaning k+1 ≥ 3. So the step fails for k = 1 (the step from n=1 to n=2), and the induction breaks.

**Lesson:** The base case and the inductive step must together cover all n. If the inductive step silently requires k ≥ 2 but the base case only establishes n = 1, there is a gap at n = 2 that makes the whole argument invalid.

---

## 8. What to Do When the Formula Is Unknown

Sometimes you need to guess the formula before proving it. Techniques:

1. **Compute small cases:** Calculate P(1), P(2), P(3), P(4). Look for a pattern.
2. **Finite differences:** If P(n) is a sum, the terms tell you the degree of the formula.
3. **OEIS:** The Online Encyclopedia of Integer Sequences (oeis.org) — enter the first few values.

**Example:** What is $\sum_{i=1}^{n} (2i-1)$?

Compute: n=1: 1. n=2: 1+3=4. n=3: 1+3+5=9. n=4: 1+3+5+7=16.

Pattern: 1, 4, 9, 16 — these are perfect squares! Conjecture: $\sum_{i=1}^{n} (2i-1) = n^2$.

Then prove by induction.

---

## 9. Summary — Weak Induction Template

```
Claim: P(n) holds for all n ≥ n₀.

Proof. By mathematical induction on n.

Base case (n = n₀): [Verify P(n₀) by direct computation.] ✓

Inductive step: Let k ≥ n₀ be arbitrary. 
  Assume P(k): [State the IH explicitly].
  We prove P(k+1): [State what needs to be shown].
  
  [Start from the left side of P(k+1).]
  [Write it in terms of a sub-expression to which P(k) applies.]
  [Apply the IH.]
  [Simplify to obtain the right side of P(k+1).]
  
  Therefore P(k+1) holds.

By the Principle of Mathematical Induction, P(n) holds for all n ≥ n₀. ∎
```

---

## 10. End-of-Lecture Exercises

1. Prove by induction:
   - (a) $\sum_{i=1}^{n} i^3 = \left[\frac{n(n+1)}{2}\right]^2$ for all $n \geq 1$.
   - (b) $\sum_{i=0}^{n} 2^i = 2^{n+1} - 1$ for all $n \geq 0$.
   - (c) $\sum_{i=1}^{n} (2i-1) = n^2$ for all $n \geq 1$.

2. Prove by induction: $6 \mid (n^3 - n)$ for all $n \geq 0$.

3. Find the error: The following "proof" shows $\sum_{i=1}^{n} i = \frac{n^2+n+2}{2}$.

   "Proof": For n=1: $\frac{1+1+2}{2} = 2 \neq 1$. [Base case FAILS — so this is wrong, but pretend a student didn't check and proceeded with the inductive step anyway.] Inductive step: Assume $\sum_{i=1}^{k} i = \frac{k^2+k+2}{2}$. Then $\sum_{i=1}^{k+1} i = \frac{k^2+k+2}{2} + (k+1) = \frac{k^2+k+2+2k+2}{2} = \frac{k^2+3k+4}{2} = \frac{(k+1)^2+(k+1)+2}{2}$. ✓

   The inductive step works perfectly. What does this illustrate about the relationship between the base case and inductive step?

4. Conjecture and prove a closed-form formula for $\sum_{i=1}^{n} \frac{1}{i(i+1)}$.

   *Hint:* Partial fractions — $\frac{1}{i(i+1)} = \frac{1}{i} - \frac{1}{i+1}$.

---

## Reading

- **Rosen, 8e §5.1** — Mathematical induction
- **Epp, 5e §5.2** — Mathematical induction I: proving formulas
- **Levin, 3e §2.5** — Induction

*Next: Lecture 10 — Induction Applications: Inequalities, Recursion, and Algorithm Correctness*
