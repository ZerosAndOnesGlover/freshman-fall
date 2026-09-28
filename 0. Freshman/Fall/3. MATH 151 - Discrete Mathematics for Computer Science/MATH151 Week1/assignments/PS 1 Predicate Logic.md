# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 1 — Predicate Logic and Quantifiers
### Released: Friday 2 October 2026, 14:00 (after the Friday lecture) | Due: Friday 9 October 2026, 17:00 (Week 2)

---

**Instructions:**
- Show all work. Unsupported answers receive no credit.
- Always state the domain and define all predicates before writing a formula.
- When negating, push ¬ all the way inward — do not leave ¬∀ or ¬∃ in your final answer.
- Submit as a single PDF.

**Expected time:** about 3 hours. **Scoring:** 100 points total.

---

## Part A — Predicates and Domains (18 points)

**A1.** (9 pts) Let P(x) = "x² − 5x + 6 = 0". Evaluate P(x) for x ∈ {0, 1, 2, 3, 4, 6}.
- (a) List all x in the given set for which P(x) is true.
- (b) Is ∀x ∈ {0,1,2,3,4,6}, P(x) true? Justify.
- (c) Is ∃x ∈ {0,1,2,3,4,6}, P(x) true? Exhibit a witness.

---

**A2.** (9 pts) Let D(x, y) mean "x divides y" (there exists an integer k with y = kx). Domain: ℤ⁺.

Evaluate each as TRUE or FALSE with brief justification:
- (a) D(3, 12)
- (b) D(5, 13)
- (c) D(n, 0) for any n ∈ ℤ⁺ — *Hint: is 0 = k·n solvable?*

---

## Part B — Single Quantifiers (22 points)

**B1.** (12 pts) For each statement, determine its truth value over the given domain. If TRUE, briefly explain why. If FALSE, give a specific counterexample.

Domain: ℤ unless otherwise stated.

- (a) ∀x, x² > x
- (b) ∃x, x² = x
- (c) ∃x ∈ ℤ, x² = 2

---

**B2.** (10 pts) Translate each English statement into predicate logic. Define all predicates and state the domain.

- (a) "Some prime number is even."
- (b) "There is a real number that is not the square of any real number."

---

## Part C — Negation (25 points)

**C1.** (15 pts) Negate each statement, simplify fully (push ¬ all the way inward), and state whether the original statement or its negation is true. Domain: ℤ unless stated.

- (a) ∀x ∈ ℤ, ∃y ∈ ℤ, x + y = 0
- (b) ∃x ∈ ℝ, ∀y ∈ ℝ, x · y = y
- (c) ∀x (E(x) → ∃k, x = 2k) where E(x) = "x is even"

---

**C2.** (10 pts) The following are purported negations. Each contains an error. Identify the error and give the correct negation.

- (a) Statement: ∃x (P(x) ∧ Q(x)). Proposed negation: ∀x (¬P(x) ∧ ¬Q(x)).
- (b) Statement: ∀x (P(x) → Q(x)). Proposed negation: ∃x (P(x) → ¬Q(x)).

---

## Part D — Nested Quantifiers (20 points)

**D1.** (20 pts) Determine the truth value of each statement over the domain ℤ. Provide a proof sketch (for TRUE) or explicit counterexample (for FALSE).

- (a) ∀x ∃y (y > x)
- (b) ∃y ∀x (y > x)
- (c) ∀x ∃y (x · y = 1) — domain: ℤ
- (d) ∀x ∃y (x · y = 1) — domain: ℚ \ {0}

---

## Part E — Applications to CS (15 points)

**E1.** (15 pts) The following is the formal definition of Big-O notation:

f(n) = O(g(n)) iff ∃C ∈ ℝ⁺, ∃n₀ ∈ ℕ, ∀n ∈ ℕ, (n ≥ n₀ → f(n) ≤ C · g(n))

- (a) Write the negation: what does f(n) ≠ O(g(n)) mean formally?
- (b) Translate the negation into plain English.

---

*Submit as a single PDF. Show all work.*
