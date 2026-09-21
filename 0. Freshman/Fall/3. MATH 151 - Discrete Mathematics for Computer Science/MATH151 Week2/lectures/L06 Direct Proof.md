# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 6 (L06) — Direct Proof
### Monday, Week 2

**Date:** Monday 5 October 2026 · 13:00–13:50 · Week 2

---

> **Core Question:** How do we establish that a mathematical claim is true with absolute certainty, and what does a valid proof actually look like?

---

## 1. What Is a Proof?

A **proof** is a finite sequence of statements, each of which is either:
- A hypothesis (given assumption),
- An axiom (a foundational truth we accept without proof),
- Or a statement that follows by a valid rule of inference from earlier statements in the sequence.

The final statement in the sequence is the **conclusion** — the claim being proved.

**What a proof is NOT:**
- A sequence of examples (no matter how many)
- An argument that it "must be true" because it seems obvious
- A computation that works for specific values
- A picture or diagram (these can provide intuition but not proof)

**Why does this matter?** Because mathematics is the only discipline where claims can be established with absolute certainty. A physical experiment gives evidence; a mathematical proof gives truth. This distinction is the foundation of everything: every algorithm you trust, every cryptographic protocol you rely on, every program correctness argument — all rest on proof.

---

## 2. Essential Definitions

Before writing any proof, you must know the precise definitions of every term involved. Proofs in mathematics work entirely from definitions. "Even" is not "you know it when you see it" — it is a specific formal definition.

### Definition: Even Integer
An integer n is **even** if there exists an integer k such that n = 2k.

### Definition: Odd Integer
An integer n is **odd** if there exists an integer k such that n = 2k + 1.

### Definition: Divisibility
An integer a **divides** integer b (written a | b) if there exists an integer k such that b = ka.

Equivalently: a | b iff b/a is an integer.

**Note:** The definition uses ∃k ∈ ℤ — the k must be an *integer*, not just any real number.

**Examples:**
- 3 | 12 because 12 = 4 · 3 (k = 4) ✓
- 5 | 0 because 0 = 0 · 5 (k = 0) ✓
- 7 | 7 because 7 = 1 · 7 (k = 1) ✓
- 4 ∤ 10 because 10/4 = 2.5 ∉ ℤ ✗

### Definition: Rational Number
A real number r is **rational** if there exist integers p and q, with q ≠ 0, such that r = p/q.

### Definition: Prime
An integer p > 1 is **prime** if its only positive divisors are 1 and p.

### Definition: Composite
An integer n > 1 is **composite** if it is not prime — i.e., n = ab for some integers a, b with 1 < a < n and 1 < b < n.

---

## 3. The Structure of a Direct Proof

To prove P → Q by direct proof:

1. **Assume P** (the hypothesis). Write "Assume P" or "Suppose P."
2. **Apply definitions** to P — expand what P means formally.
3. **Perform valid algebraic/logical steps** to transform the expression.
4. **Arrive at Q** — show that Q holds from what you derived.
5. **Conclude.** Write "Therefore Q" or "Thus Q" or end with ∎.

The key discipline: every step must be justified. You may not introduce a new claim without either deriving it from previous steps or citing a known result.

---

## 4. Direct Proof — Worked Examples

### Example 1: Sum of Two Even Integers

**Theorem.** If m and n are even integers, then m + n is even.

**Proof.**
Assume m and n are even integers.
By definition of even, there exist integers j and k such that m = 2j and n = 2k.
Then:
$$m + n = 2j + 2k = 2(j + k)$$
Since j and k are integers, j + k is an integer. Let ℓ = j + k.
Then m + n = 2ℓ where ℓ is an integer.
By definition of even, m + n is even. ∎

**Anatomy of this proof:**
- Line 1: State the assumption (hypothesis)
- Line 2: Apply the definition of "even" to both m and n — introducing integer witnesses j and k
- Line 3–4: Algebraic manipulation — factor out 2
- Line 5: Identify the new integer witness ℓ
- Line 6: Apply the definition of "even" in the forward direction

Every step is explicit. Nothing is skipped.

---

### Example 2: Product of Two Odd Integers

**Theorem.** If m and n are odd integers, then mn is odd.

**Proof.**
Assume m and n are odd integers.
By definition, there exist integers j and k such that m = 2j + 1 and n = 2k + 1.
Then:
$$mn = (2j+1)(2k+1) = 4jk + 2j + 2k + 1 = 2(2jk + j + k) + 1$$
Since j and k are integers, 2jk + j + k is an integer. Let ℓ = 2jk + j + k.
Then mn = 2ℓ + 1 where ℓ is an integer.
By definition of odd, mn is odd. ∎

**Key technique:** After expanding, *group* the expression into the form 2(something) + 1, where "something" is verified to be an integer.

---

### Example 3: Divisibility is Transitive

**Theorem.** If a | b and b | c, then a | c.

**Proof.**
Assume a | b and b | c.
By definition of divisibility, there exist integers j and k such that b = ja and c = kb.
Substituting the first into the second:
$$c = kb = k(ja) = (kj)a$$
Since k and j are integers, kj is an integer. Let ℓ = kj.
Then c = ℓa where ℓ is an integer.
By definition of divisibility, a | c. ∎

---

### Example 4: A Statement About Rationals

**Theorem.** The sum of two rational numbers is rational.

**Proof.**
Let r and s be rational numbers.
By definition, there exist integers p, q, m, n with q ≠ 0 and n ≠ 0, such that r = p/q and s = m/n.
Then:
$$r + s = \frac{p}{q} + \frac{m}{n} = \frac{pn + qm}{qn}$$
Since p, q, m, n are integers: pn + qm is an integer and qn is an integer.
Since q ≠ 0 and n ≠ 0, we have qn ≠ 0.
Therefore r + s = (pn + qm)/(qn) is a ratio of integers with nonzero denominator.
By definition of rational, r + s is rational. ∎

**Note:** We needed to verify *both* that the numerator is an integer and that the denominator is a nonzero integer. Forgetting the denominator condition is a common incomplete proof.

---

### Example 5: A Divisibility Combination

**Theorem.** If a | b and a | c, then a | (mb + nc) for any integers m and n.

**Proof.**
Assume a | b and a | c, and let m, n be any integers.
By definition, there exist integers j and k such that b = ja and c = ka.
Then:
$$mb + nc = m(ja) + n(ka) = (mj + nk)a$$
Since m, j, n, k are integers, mj + nk is an integer. Let ℓ = mj + nk.
Then mb + nc = ℓa.
By definition, a | (mb + nc). ∎

This is a powerful result: divisibility is preserved under integer linear combinations. It is the foundation of the theory of the GCD.

---

## 5. Proof Writing Style

### Use Prose, Not Pseudocode

A proof is a piece of mathematical writing. It should read like a paragraph, not like a program.

**Poor (pseudocode style):**
```
1. m = 2j
2. n = 2k
3. m + n = 2j + 2k
4. = 2(j+k)
5. Let ℓ = j+k
6. m + n = 2ℓ ∴ even
```

**Good (mathematical prose):**
"By definition of even, m = 2j and n = 2k for some integers j and k. Then m + n = 2j + 2k = 2(j + k). Since j + k is an integer, m + n is even."

### Use Quantifiers Implicitly — But Precisely

When you write "let m = 2j for some integer j," you are asserting ∃j ∈ ℤ, m = 2j — you just write it in natural language. This is standard mathematical practice.

### Signal Your Steps

Use transition words to mark what you are doing:
- **"By definition of [term]..."** — unpacking a definition
- **"Then..." / "Therefore..." / "Thus..."** — logical consequence
- **"Since [fact], we have..."** — citing a reason
- **"Let [variable] = [expression]..."** — introducing a new name
- **"By assumption..."** — using a hypothesis
- **"Without loss of generality (WLOG)..."** — invoking symmetry

### End Clearly

End with **∎** (tombstone), **QED** (quod erat demonstrandum), or the phrase "This completes the proof."

---

## 6. Cases

Some theorems require splitting into cases. This is valid and common — you prove the conclusion holds in every possible case.

### Example: Product of an Even and Any Integer

**Theorem.** If n is an integer, then n(n+1) is even.

**Proof.**
We consider two cases based on the parity of n.

**Case 1: n is even.**
Then n = 2k for some integer k.
So n(n+1) = 2k(n+1) = 2[k(n+1)].
Since k(n+1) is an integer, n(n+1) is even.

**Case 2: n is odd.**
Then n+1 is even (since n odd means n+1 even — we prove this if needed, or cite it as a known fact).
So n+1 = 2k for some integer k.
Then n(n+1) = n · 2k = 2(nk).
Since nk is an integer, n(n+1) is even.

In both cases, n(n+1) is even. ∎

**Important discipline:** When using case analysis, you must ensure the cases are:
1. **Exhaustive** — every possibility is covered
2. **Correct** — each case is correctly handled

In this proof: every integer is either even or odd (exhaustive by definition). Both cases were handled. ∎

---

## 7. What Makes a Proof Invalid

### Error 1: Assuming the Conclusion

**Flawed "proof" that 2 is even:**
"Assume 2 is even. Then 2 = 2(1). So 2 is even." ✗

This is circular — it assumes what it's trying to prove.

**Correct proof:** By definition, 2 = 2 · 1, where 1 is an integer. So 2 is even. ✓

### Error 2: Proof by Example

"For n = 2: 2² − 2 = 2, which is even. For n = 4: 16 − 4 = 12, even. For n = 6: 36 − 6 = 30, even. Therefore n² − n is always even." ✗

Examples establish nothing for a universal statement — you would need infinitely many. This is the classic confusion of *induction* (next week) with *enumeration*.

### Error 3: Incorrect Algebra

"If n is odd, then n = 2k + 1. So n² = 2k² + 1." ✗

This is wrong: n² = (2k+1)² = 4k² + 4k + 1, not 2k² + 1.

### Error 4: Wrong Existential Witness

"If n is even, then n = 2k. So n + 1 = 2k + 1 = 2(k + ½). Therefore n+1 is even." ✗

Here k + ½ is not an integer, so this does not satisfy the definition of even.

### Error 5: Incomplete Case Analysis

"Prove that x² ≥ 0 for all real x. Proof: If x > 0, then x² > 0 ≥ 0. Done." ✗

This omits the cases x = 0 and x < 0.

---

## 8. The Connection to Quantifiers

Direct proofs of universally quantified statements have a precise structure from predicate logic:

To prove ∀x ∈ D, P(x) → Q(x):
- Let x be an arbitrary element of D (this is the "∀x" step)
- Assume P(x) (this is the hypothesis)
- Derive Q(x) (this is the goal)

The word "arbitrary" is critical. If you assume anything about x beyond its membership in D and the hypothesis P(x), your proof is only valid for those special x values, not all x.

---

## 9. Summary — Direct Proof Template

```
Theorem. [State the theorem clearly.]

Proof.
[Assume the hypothesis.]
[Apply definitions to expand the hypothesis into algebraic form.]
[Perform valid algebraic steps, citing reasons.]
[Show that the result matches the definition of the conclusion.]
[State the conclusion explicitly.]
∎
```

---

## 10. End-of-Lecture Exercises

1. Prove each theorem directly. Show every step.
   - (a) If n is an even integer, then n² is even.
   - (b) If n is an odd integer, then n² is odd.
   - (c) The product of two rational numbers is rational.
   - (d) If a | b and a | c, then a | (b − c).

2. Find the error in each flawed proof:

   **(a)** Claim: If n² is even, then n is even.
   Proof: Let n be any integer. If n² is even, then n² = 2k. So n = √(2k). Since 2k is even, n is the square root of an even number, which is even. ✗

   **(b)** Claim: The square of any rational is rational.
   Proof: Let r be rational. Then r = p/q. So r² = p²/q. Since p² and q are integers, r² is rational. ✗

   **(c)** Claim: If n is divisible by 6, then n is divisible by 3.
   Proof: 6 = 2 × 3. Since 3 divides 6 and 6 divides n, we're done. ✗ (What's missing?)

3. Prove: If n is an integer and 3 | n, then 3 | n².

4. Prove: For any integers a, b, c, if a | b, then a | bc.

5. **Writing exercise:** The following proof is logically correct but poorly written. Rewrite it in proper mathematical prose:
   "n odd → n=2k+1 → n+1=2k+2=2(k+1) → k+1 ∈ ℤ → n+1 even ✓"

---

*Next: Lecture 7 — Proof by Contrapositive*
