# MATH 151 · Discrete Mathematics for Computer Science
## Quiz 3 — Scope Preview
### Quiz administered: Monday 12 October 2026, 13:00–13:15 (first 15 minutes of lecture) · Week 3

---

**Coverage:** Week 2 material only:
- Week 2: Proof techniques — direct proof, contrapositive, contradiction

*(Week 3 material is not on this quiz — it is taught after the quiz.)*

---

## What You Must Know Cold for Week 2 Material

### 1. Core Definitions (produce instantly from memory)

| Term | Definition |
|---|---|
| n is even | ∃k ∈ ℤ, n = 2k |
| n is odd | ∃k ∈ ℤ, n = 2k + 1 |
| a divides b | ∃k ∈ ℤ, b = ka |
| r is rational | ∃p, q ∈ ℤ, q ≠ 0, r = p/q |
| n is prime | n > 1 and only positive divisors are 1 and n |

### 2. Proof Structures

**Direct proof of P → Q:**
- Assume P
- Apply definitions, algebra
- Conclude Q

**Contrapositive of P → Q:**
- State: we prove ¬Q → ¬P
- Assume ¬Q
- Derive ¬P
- Conclude P → Q by contrapositive equivalence

**Contradiction proof of claim C:**
- State: assume ¬C
- Derive a statement R and its negation ¬R
- Conclude ¬C is false, so C holds

### 3. Technique Selection

Know which technique to choose:
- Direct: when P gives explicit algebraic form (n = 2k, b = ka)
- Contrapositive: when ¬Q is stronger/more concrete than P
- Contradiction: when the claim is not an implication, or when "no solution exists," or for irrationality

### 4. Classic Results (know these proofs)

- Sum of two even integers is even (direct)
- Product of two odd integers is odd (direct)
- If n² is even then n is even (contrapositive)
- √2 is irrational (contradiction)
- There are infinitely many primes (contradiction)

---

## Sample Quiz 3 Problems (Week 2 portion)

**Problem 1.** (4 pts) Prove directly: If a | b and b | c, then a² | b²c.

**Problem 2.** (4 pts) Prove by contrapositive: For integers a, b, if ab is odd, then a is odd and b is odd.

**Problem 3.** (4 pts) Prove by contradiction: √10 is irrational.

**Problem 4.** (4 pts) Find the error in this proof:
*Claim: If n² is even, then n is even.*
*"Proof": Suppose n² is even. Then n² = 2k. So n = √(2k) = √2 · √k. Since √2 is irrational and the product of an irrational with √k is irrational unless k = 0, we have n = 0, which is even. ✗*

**Problem 5.** (4 pts) From Week 3 — induction problem (see Week 3 materials).

---

## Study Recommendations

1. **Know the definitions verbatim.** Every proof begins by expanding a definition. If you write "n is even so n = 2k + 1" you will lose marks. Even → 2k. Odd → 2k+1.

2. **Write out the contrapositive before proving it.** State ¬Q → ¬P in words, then prove it. Do not just say "by contrapositive" and immediately dive in.

3. **Practice the √2 proof from memory.** It has five distinct steps; know each one and why it is needed.

4. **Do PS2 in full.** Every proof type on the quiz appears on PS2.

5. **Know what makes a proof invalid.** Quiz problems regularly ask you to find errors. The most common: assuming the conclusion, dividing by zero, incorrect negation, not verifying gcd conditions.
