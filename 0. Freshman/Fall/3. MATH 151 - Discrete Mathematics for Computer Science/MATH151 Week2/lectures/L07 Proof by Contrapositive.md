# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 2.2 (L07) — Proof by Contrapositive
### Thursday, Week 2

**Date:** Thursday 8 October 2026 · 13:00–13:50 · Week 2

---

> **Core Question:** When is it easier to prove ¬Q → ¬P than P → Q, and why are they the same statement?

---

## 1. The Logical Foundation

Recall from Week 0: **P → Q ≡ ¬Q → ¬P** (the contrapositive). These two statements are logically equivalent — they have identical truth tables under every assignment.

This equivalence is not just a curiosity. It is a proof technique: when proving P → Q directly is difficult, we may instead prove ¬Q → ¬P, which establishes exactly the same result.

**When does this help?**

The contrapositive is useful when:
- The hypothesis P is weak or hard to work with algebraically
- The negation ¬Q is a strong, concrete condition that gives you something to work with
- The conclusion Q involves a universal claim that is hard to establish directly, but whose negation is a specific, workable condition

**The diagnostic test:** Look at the negation of the conclusion. If ¬Q gives you more algebraic structure than P does, use contrapositive.

---

## 2. The Structure of a Contrapositive Proof

To prove P → Q by contrapositive:

1. State that you are proving the contrapositive: ¬Q → ¬P.
2. **Assume ¬Q.**
3. Apply definitions and derive ¬P by a chain of valid steps.
4. Conclude: since ¬Q → ¬P, we have P → Q. ∎

---

## 3. Worked Examples

### Example 1: Even Square Implies Even Root

**Theorem.** If n² is even, then n is even.

**Why direct proof is hard:** If we assume n² is even, we know n² = 2k for some integer k. But it is not obvious how to extract information about n from this — taking a square root gives n = ±√(2k), which is not obviously useful.

**Why contrapositive works:** The contrapositive is "If n is not even (i.e., n is odd), then n² is not even (i.e., n² is odd)." Now the hypothesis is the strong, workable condition.

**Proof.**
We prove the contrapositive: if n is odd, then n² is odd.

Assume n is odd. By definition, n = 2k + 1 for some integer k.
Then:
$$n^2 = (2k+1)^2 = 4k^2 + 4k + 1 = 2(2k^2 + 2k) + 1$$
Since 2k² + 2k is an integer, n² = 2(2k² + 2k) + 1 has the form 2m + 1 for integer m.
By definition, n² is odd.

Since we proved (n odd → n² odd), the contrapositive gives us (n² even → n even). ∎

**Comment:** This is the prototype example for contrapositive. The direct direction (n² even → n even) is genuinely harder. Many students attempt a direct proof by writing "if n² = 2k then n = √(2k)" — but this does not show n is even, only that n = √(2k), which could be irrational. The contrapositive sidesteps this entirely.

---

### Example 2: Divisibility and Parity

**Theorem.** If n² is odd, then n is odd.

**Proof.**
Contrapositive: if n is even, then n² is even.

Assume n is even. Then n = 2k for some integer k.
Then n² = (2k)² = 4k² = 2(2k²).
Since 2k² is an integer, n² is even. ∎

---

### Example 3: A Number Theory Result

**Theorem.** For any integer n, if 3 ∤ n², then 3 ∤ n.

**Proof.**
Contrapositive: if 3 | n, then 3 | n².

Assume 3 | n. Then n = 3k for some integer k.
Then n² = 9k² = 3(3k²).
Since 3k² is an integer, 3 | n². ∎

---

### Example 4: A Two-Variable Statement

**Theorem.** For integers a and b, if ab is odd, then both a and b are odd.

**Why direct proof is awkward:** If ab is odd, we know ab = 2k + 1. But factoring 2k + 1 into a product ab that forces both factors to be odd is not straightforward.

**Contrapositive:** If a is even or b is even (i.e., ¬(a odd ∧ b odd) ≡ a even ∨ b even), then ab is even.

**Proof.**
We prove the contrapositive: if a is even or b is even, then ab is even.

**Case 1:** a is even. Then a = 2k for some integer k.
Then ab = (2k)b = 2(kb).
Since kb is an integer, ab is even.

**Case 2:** b is even. Then b = 2k for some integer k.
Then ab = a(2k) = 2(ak).
Since ak is an integer, ab is even.

In both cases, ab is even. Therefore, by contrapositive, if ab is odd then both a and b are odd. ∎

**Note on the negation:** The negation of "both a and b are odd" is "a is even **or** b is even" (De Morgan: ¬(P ∧ Q) ≡ ¬P ∨ ¬Q). This disjunction required a case split in the proof.

---

### Example 5: A Statement Involving Divisibility

**Theorem.** For any integer n, if n² is divisible by 3, then n is divisible by 3.

This is harder to prove directly. We use the contrapositive combined with the division algorithm.

**Fact (Division Algorithm):** Every integer n can be written uniquely as n = 3q + r where r ∈ {0, 1, 2}.

**Proof.**
Contrapositive: if 3 ∤ n, then 3 ∤ n².

Assume 3 ∤ n. By the division algorithm, n = 3q + r where r ∈ {1, 2} (since r = 0 would mean 3 | n).

**Case r = 1:** n = 3q + 1.
n² = (3q+1)² = 9q² + 6q + 1 = 3(3q² + 2q) + 1.
So n² = 3m + 1 where m = 3q² + 2q ∈ ℤ. Thus 3 ∤ n².

**Case r = 2:** n = 3q + 2.
n² = (3q+2)² = 9q² + 12q + 4 = 9q² + 12q + 3 + 1 = 3(3q² + 4q + 1) + 1.
So n² = 3m + 1 where m = 3q² + 4q + 1 ∈ ℤ. Thus 3 ∤ n².

In both cases, 3 ∤ n². By contrapositive, if 3 | n² then 3 | n. ∎

**This result is fundamental:** It is used in the proof that √3 is irrational (coming in Friday's lecture).

---

## 4. Contrapositive vs Direct — How to Choose

| Situation | Use direct proof | Use contrapositive |
|---|---|---|
| Hypothesis P is strong and algebraically rich | ✓ | |
| Hypothesis P gives explicit form (e.g., "n = 2k") | ✓ | |
| Conclusion Q involves ∃ (produce a witness) | ✓ | |
| Hypothesis P is weak ("n² is even") | | ✓ |
| Negation ¬Q is concrete and algebraically useful | | ✓ |
| Conclusion Q is a universal claim ("every factor of...") | | ✓ |
| Statement involves divisibility by a prime | often | ✓ |

**The mental check:** After reading the theorem, ask:
1. What does P give me to work with? Is it concrete and algebraic?
2. What does ¬Q give me to work with? Is it more concrete?

If ¬Q is richer than P, try contrapositive first.

---

## 5. Contrapositive in Logic and CS

**Type inference:** The type inference rule modus tollens is the logical contrapositive in action:
- If (expression has type A → B) and (expression does not have type B), then (the argument does not have type A).
- This is exactly: (P → Q) ∧ ¬Q → ¬P.

Type checkers run this inference continuously.

**Compiler optimizations:** If (code is reachable → some condition C holds) and (C does not hold), then (code is not reachable). The compiler uses this to eliminate dead code.

**Loop invariants:** Proving a loop terminates often uses the contrapositive: "if the loop has not terminated, then the loop variable has not yet reached the termination condition."

---

## 6. Common Errors in Contrapositive Proofs

### Error 1: Proving the Converse Instead

"To prove P → Q, I will prove Q → P instead." ✗

**The converse Q → P is NOT equivalent to P → Q.** The contrapositive is ¬Q → ¬P, not Q → P.

### Error 2: Negating Incorrectly

Theorem: "If n is divisible by 4, then n is divisible by 2."

Incorrect contrapositive: "If n is divisible by 2, then n is divisible by 4." ✗

This is the converse, not the contrapositive.

Correct contrapositive: "If n is **not** divisible by 2, then n is **not** divisible by 4." ✓

### Error 3: Forgetting to Negate Both Sides

When forming the contrapositive, you must negate BOTH the hypothesis and conclusion, and swap their roles.

- P → Q
- Contrapositive: ¬Q → ¬P (not P → ¬Q, not ¬Q → P)

---

## 7. End-of-Lecture Exercises

1. For each theorem, state the contrapositive, then prove the theorem using the contrapositive:
   - (a) For any integer n, if n² is even, then n is even.
   - (b) For any integer n, if n³ is odd, then n is odd.
   - (c) For any integers a and b, if a + b is odd, then a and b have opposite parity (one even, one odd).
   - (d) For any real numbers x and y, if x · y ≠ 0, then x ≠ 0 and y ≠ 0.

2. Identify whether direct proof or contrapositive is more natural for each. Do NOT prove them — just justify your choice:
   - (a) If the product of two integers is even, then at least one of them is even.
   - (b) If n is divisible by 6, then n is divisible by 2.
   - (c) If x is irrational, then x + 1 is irrational.
   - (d) If n² − 1 is even, then n is odd.

3. Find the error:

   **(a)** Claim: If n is not divisible by 3, then n² is not divisible by 3.
   "Proof by contrapositive": We prove: if n² is divisible by 3, then n is divisible by 3. Assume n² = 3k. Then n = √(3k) = √3 · √k. Since √3 is irrational, n is irrational, but we assumed n is an integer — contradiction. ✗

   **(b)** Claim: If n² is odd, then n is odd.
   "Proof": We take the contrapositive: if n is even, then n² is odd. Assume n = 2k. Then n² = 4k² = 2(2k²), which is even, not odd. ✗

4. **True or False?** "To prove P → Q, proving Q → P is sufficient." Explain precisely why or why not using the truth table for the conditional.

---

*Next: Lecture 2.3 — Proof by Contradiction*
