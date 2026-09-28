# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 2 — Proof Techniques
### Released: Friday 9 October 2026, 14:00 (after the Friday lecture) | Due: Friday 16 October 2026, 17:00 (Week 3)

---

**Instructions:**
- Every proof must be written in complete mathematical prose. No pseudocode, no bullet points, no arrows.
- State explicitly which proof technique you are using at the start of each proof.
- When using contrapositive: state the contrapositive before proving it.
- When using contradiction: state your contradictory assumption explicitly.
- Show every step. Cite definitions when you apply them.
- Submit as a single PDF.

**Expected time:** about 3 hours. **Scoring:** 100 points total.

---

## Part A — Direct Proof (36 points)

**A1.** (24 pts) Prove each theorem directly.

**(a)** If n is an odd integer, then n + 1 is even.

**(b)** If a | b and a | c, then a | (3b − 2c).

**(c)** For any integer n, n² + n is even.
*(Hint: Consider the cases n even and n odd.)*

---

**A2.** (12 pts) The following "proof" contains an error. Identify the exact error, explain why it is wrong, and write a correct proof.

**Flawed Claim:** If n is an integer and n² is divisible by 4, then n is divisible by 4.

**Flawed Proof:** Assume 4 | n², so n² = 4k for some integer k. Then n² is even, so n is even (proved in class), so n = 2m. Then n² = 4m². So 4 | n² and n = 2m, hence 4 | n. ✗

---

## Part B — Proof by Contrapositive (18 points)

**B1.** (18 pts) For each theorem: (i) write the contrapositive, (ii) prove the theorem using the contrapositive.

**(a)** For any integer n, if n² is odd, then n is odd.

**(b)** For any real numbers x and y, if x + y is irrational, then x is irrational or y is irrational.

---

## Part C — Proof by Contradiction (32 points)

**C1.** (18 pts) Prove by contradiction.

**(a)** √7 is irrational.

**(b)** If n is an integer and n² is divisible by 5, then n is divisible by 5.
*(This is not obviously a contradiction proof — compare with the contrapositive approach. Choose one and justify your choice.)*

---

**C2.** (14 pts) The following "proof by contradiction" has a logical flaw. Identify the flaw precisely.

**Claim:** √4 is irrational.

**Flawed Proof:** Suppose √4 = p/q in lowest terms. Squaring: 4 = p²/q², so p² = 4q². Then p² is even, so p is even. Write p = 2k. Then 4k² = 4q², so k² = q². Thus q = ±k, and gcd(p,q) = gcd(2k,k) = k ≥ 1. If k > 1, this contradicts gcd(p,q) = 1. Therefore √4 is irrational. ✗

What exactly goes wrong? At what step does the proof fail? Why does the analogous argument for √2 not have this problem?

---

## Part D — Mixed and Applied (14 points)

**D1.** (14 pts) Prove or disprove each of the following. If true, provide a proof; if false, provide a counterexample and explain why the statement is false.

**(a)** If a | (b + c), then a | b or a | c.

**(b)** If a | bc, then a | b or a | c.

*(Both are false in general. Week 12 shows that (b) becomes true when a is prime — one of the most important facts in number theory.)*
