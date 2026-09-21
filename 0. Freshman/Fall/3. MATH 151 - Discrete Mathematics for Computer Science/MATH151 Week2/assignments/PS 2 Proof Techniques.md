# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 2 — Proof Techniques
### Released: Friday 9 October 2026, 14:00 (after the Friday lecture) | Due: Friday 16 October 2026, 17:00 (Week 3)

---

> *Revised 2026-09-21.* The optional bonus section was removed to keep the set to 100 points of
> this week's material.

**Instructions:**
- Every proof must be written in complete mathematical prose. No pseudocode, no bullet points, no arrows.
- State explicitly which proof technique you are using at the start of each proof.
- When using contrapositive: state the contrapositive before proving it.
- When using contradiction: state your contradictory assumption explicitly.
- Show every step. Cite definitions when you apply them.
- Submit as a single PDF.

**Scoring:** 100 points total.

---

## Part A — Direct Proof (28 points)

**A1.** (4 pts each) Prove each theorem directly.

**(a)** If n is an odd integer, then n + 1 is even.

**(b)** If m is even and n is odd, then m + n is odd.

**(c)** If a | b and a | c, then a | (3b − 2c).

**(d)** The product of any two rational numbers is rational.

**(e)** If n = 4k + 1 for some integer k, then n² = 8m + 1 for some integer m.

**(f)** For any integer n, n² + n is even.
*(Hint: Consider the cases n even and n odd.)*

**(g)** If a | b, then a² | b².

---

**A2.** (4 pts) The following "proof" contains an error. Identify the exact error, explain why it is wrong, and write a correct proof.

**Flawed Claim:** If n is an integer and n² is divisible by 4, then n is divisible by 4.

**Flawed Proof:** Assume n² is divisible by 4. Then n² = 4k for some integer k. Therefore n = 2√k. Since n must be an integer and 2√k is an integer only if √k is an integer... [proof breaks down].

Actually, let me just say: n² = 4k means n² is even, so n is even (proved in class), so n = 2m. Then n² = 4m². So 4 | n² and n = 2m, hence 4 | n. ✗

---

## Part B — Proof by Contrapositive (24 points)

**B1.** (4 pts each) For each theorem: (i) write the contrapositive, (ii) prove the theorem using the contrapositive.

**(a)** For any integer n, if n² is odd, then n is odd.

**(b)** For any integers a and b, if ab is even, then a is even or b is even.

**(c)** For any real numbers x and y, if x + y is irrational, then x is irrational or y is irrational.

**(d)** For any integer n, if n is not divisible by 3, then n² is not divisible by 9.

---

**B2.** (4 pts) Decide whether to use direct proof or contrapositive for each. State your choice and briefly justify it. Do NOT write the full proof.

**(a)** For any integer n, if n³ is even, then n is even.

**(b)** For any integer n, if 5 | n, then 5 | n².

**(c)** For integers a, b: if a is odd and b is odd, then a + b is even.

**(d)** For any real x, if x² < x, then x < 1.

---

## Part C — Proof by Contradiction (28 points)

**C1.** (4 pts each) Prove by contradiction.

**(a)** √7 is irrational.

**(b)** √(2/3) is irrational.
*(Hint: Write √(2/3) = p/q and derive p² = (2/3)q². Multiply through carefully.)*

**(c)** log₃ 5 is irrational.

**(d)** There is no rational number r such that r² = 6.

**(e)** If n is an integer and n² is divisible by 5, then n is divisible by 5.
*(This is not obviously a contradiction proof — compare with the contrapositive approach. Choose one and justify your choice.)*

---

**C2.** (4 pts) Prove: There are infinitely many prime numbers of the form 4k + 3.

*Hint:* Adapt Euclid's proof. Note that the product of numbers of the form 4k + 1 is again of the form 4k + 1. So if you have a finite list of 4k+3 primes, construct a number that must have a 4k+3 prime factor not on the list.

*(This is harder than the standard Euclid proof — think carefully about how to construct N.)*

---

**C3.** (4 pts) The following "proof by contradiction" has a logical flaw. Identify the flaw precisely.

**Claim:** √4 is irrational.

**Flawed Proof:** Suppose √4 = p/q in lowest terms. Squaring: 4 = p²/q², so p² = 4q². Then p² is even, so p is even. Write p = 2k. Then 4k² = 4q², so k² = q². Thus q = ±k, and gcd(p,q) = gcd(2k,k) = k ≥ 1. If k > 1, this contradicts gcd(p,q) = 1. Therefore √4 is irrational. ✗

What exactly goes wrong? At what step does the proof fail? Why does the analogous argument for √2 not have this problem?

---

## Part D — Mixed and Applied (20 points)

**D1.** (4 pts) Prove the following theorem using whichever technique you judge most appropriate. Justify your choice of technique.

**Theorem.** For any integer n, n(n+1)(n+2) is divisible by 6.

*(Hint: Consider cases modulo 3. Every integer is of the form 3k, 3k+1, or 3k+2.)*

---

**D2.** (4 pts) Prove both directions of the following biconditional directly:

**Theorem.** An integer n is odd if and only if n² is odd.

*(You must prove both → and ←. For each direction, state which technique you are using.)*

---

**D3.** (4 pts) This problem concerns the relationship between contradiction and contrapositive.

**(a)** We know P → Q is equivalent to its contrapositive ¬Q → ¬P. Show that a proof of ¬Q → ¬P is *also* a proof by contradiction of P → Q. That is, explain how every contrapositive proof can be viewed as a special case of proof by contradiction.

**(b)** Conversely, can every proof by contradiction of P → Q be converted into a contrapositive proof? If yes, explain how. If no, give an example where contradiction is essential and contrapositive doesn't work cleanly.

---

**D4.** (4 pts) The following theorem has a subtle hypothesis requirement. Prove it, and explain why each hypothesis is necessary (i.e., what goes wrong if you drop any one of them):

**Theorem.** For integers a, b, c: if a | bc and gcd(a, b) = 1, then a | c.

*(This is Euclid's Lemma. You may use without proof: if gcd(a,b) = 1, then there exist integers x, y such that ax + by = 1. This is Bézout's Identity — proved in Week 4.)*

---

**D5.** (4 pts) Prove or disprove each of the following. If true, provide a proof; if false, provide a counterexample and explain why the statement is false.

**(a)** If a | (b + c), then a | b or a | c.

**(b)** If a | bc, then a | b or a | c.

**(c)** If p is prime and p | ab, then p | a or p | b.

*(The contrast between (b) and (c) is one of the most important distinctions in number theory.)*
