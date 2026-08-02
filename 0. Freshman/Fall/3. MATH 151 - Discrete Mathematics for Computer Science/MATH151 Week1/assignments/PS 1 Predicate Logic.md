# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 1 — Predicate Logic and Quantifiers
### Released: Friday, Week 1 | Due: Friday, Week 2 (11:59 PM)

---

**Instructions:**
- Show all work. Unsupported answers receive no credit.
- Always state the domain and define all predicates before writing a formula.
- When negating, push ¬ all the way inward — do not leave ¬∀ or ¬∃ in your final answer.
- Submit as a single PDF.

**Scoring:** 100 points total.

---

## Part A — Predicates and Domains (16 points)

**A1.** (6 pts) Let P(x) = "x² − 5x + 6 = 0". Evaluate P(x) for x ∈ {0, 1, 2, 3, 4, 6}.
- (a) List all x in the given set for which P(x) is true.
- (b) Is ∀x ∈ {0,1,2,3,4,6}, P(x) true? Justify.
- (c) Is ∃x ∈ {0,1,2,3,4,6}, P(x) true? Exhibit a witness.

---

**A2.** (6 pts) Let D(x, y) mean "x divides y" (there exists an integer k with y = kx). Domain: ℤ⁺.

Evaluate each as TRUE or FALSE with brief justification:
- (a) D(3, 12)
- (b) D(5, 13)
- (c) D(1, n) for any n ∈ ℤ⁺
- (d) D(n, 0) for any n ∈ ℤ⁺ — *Hint: is 0 = k·n solvable?*
- (e) D(n, n) for any n ∈ ℤ⁺
- (f) D(n, 1) for n > 1

---

**A3.** (4 pts) Identify all free and bound variable occurrences in each formula. If a variable appears both free and bound, note both occurrences:
- (a) ∀x (P(x, y) ∧ Q(y, z))
- (b) ∃x P(x) ∧ ∀x Q(x)
- (c) ∀x ∃y (R(x, y) → S(y, z)) ∧ T(x)
- (d) ∃x (∀y P(x, y)) ∧ ∃y Q(x, y)

---

## Part B — Single Quantifiers (20 points)

**B1.** (8 pts) For each statement, determine its truth value over the given domain. If TRUE, briefly explain why. If FALSE, give a specific counterexample.

Domain: ℤ unless otherwise stated.

- (a) ∀x, x + 1 > x
- (b) ∀x, x² ≥ 0
- (c) ∀x, x² > x
- (d) ∃x, x² = x
- (e) ∃x ∈ ℝ, x² = 2
- (f) ∃x ∈ ℤ, x² = 2
- (g) ∀x ∈ ℚ, ∃y ∈ ℚ, y > x
- (h) ∀x ∈ ℝ, x = 0 ∨ x > 0 ∨ x < 0

---

**B2.** (6 pts) Translate each English statement into predicate logic. Define all predicates and state the domain.

- (a) "Some prime number is even."
- (b) "Not every real number is rational."
- (c) "Every algorithm either terminates or runs forever." *(Tautology? Or genuine constraint?)*
- (d) "There is a real number that is not the square of any real number."
- (e) "Every input to the function produces an output." *(Domain: all inputs)*
- (f) "No integer is both positive and negative."

---

**B3.** (6 pts) Translate each formula into English. Domain: ℝ. P(x) = "x is rational."

- (a) ∀x (x > 0 → ∃y, y² = x)
- (b) ∃x ∀y (x ≤ y)
- (c) ∀x ∀y (x < y → ∃z, x < z < y)
- (d) ∀x (P(x) → ∀y (P(y) → P(x + y)))
- (e) ∃x ¬P(x)
- (f) ¬∀x P(x)

For (e) and (f): are these equivalent? Determine which are true and which are false over ℝ.

---

## Part C — Negation (22 points)

**C1.** (10 pts) Negate each statement, simplify fully (push ¬ all the way inward), and state whether the original statement or its negation is true. Domain: ℤ unless stated.

- (a) ∀x, x² ≥ 0
- (b) ∃x, x + x = x
- (c) ∀x ∈ ℤ, ∃y ∈ ℤ, x + y = 0
- (d) ∃x ∈ ℝ, ∀y ∈ ℝ, x · y = y
- (e) ∀x (E(x) → ∃k, x = 2k) where E(x) = "x is even"

---

**C2.** (6 pts) For each English claim, write it in predicate logic, then negate it in predicate logic, then translate the negation back into English. The negation should be a natural English sentence, not just "it is not the case that..."

- (a) "Every student who passes the midterm passes the course."
- (b) "Some program can solve every instance of the halting problem."
- (c) "No two distinct real numbers have the same absolute value."

---

**C3.** (6 pts) The following are purported negations. Each contains an error. Identify the error and give the correct negation.

- (a) Statement: ∀x P(x). Proposed negation: ∀x ¬P(x).
- (b) Statement: ∃x (P(x) ∧ Q(x)). Proposed negation: ∀x (¬P(x) ∧ ¬Q(x)).
- (c) Statement: ∀x (P(x) → Q(x)). Proposed negation: ∃x (P(x) → ¬Q(x)).

---

## Part D — Nested Quantifiers (28 points)

**D1.** (10 pts) Determine the truth value of each statement over the domain ℤ. Provide a proof sketch (for TRUE) or explicit counterexample (for FALSE).

- (a) ∀x ∃y (y > x)
- (b) ∃y ∀x (y > x)
- (c) ∀x ∀y (x < y → ∃z, x < z < y)
- (d) ∀x ∃y (x + y = 0)
- (e) ∃x ∀y (x + y = 0)
- (f) ∀x ∀y ∃z (z = x + y)
- (g) ∃x ∃y (x² + y² = 5)
- (h) ∀x ∃y (x · y = 1) — domain: ℤ
- (i) ∀x ∃y (x · y = 1) — domain: ℚ \ {0}
- (j) ∃x ∀y ∀z (x = y + z)

---

**D2.** (8 pts) Negate each nested quantifier statement fully. Then evaluate whether the original is true or false.

- (a) ∀x ∀y (x + y = y + x)
- (b) ∃x ∀y (x ≤ y)
- (c) ∀x ∃y ∀z (z > y → z > x)
- (d) ∃x ∃y (x² + y² < 0)

---

**D3.** (10 pts) Express each definition or claim formally using nested quantifiers.

- (a) **Definition of function:** A relation f ⊆ A × B is a function if every element of A is related to exactly one element of B. (Use ∀ and ∃! or expand ∃! explicitly.)

- (b) **Injection (one-to-one):** f: ℤ → ℤ defined by f(x) = 2x. Write the injectivity definition as a quantified statement, then prove it is satisfied.

- (c) **Surjection (onto):** f: ℤ → ℤ defined by f(x) = 2x. Write the surjectivity definition, then show it fails by finding a y ∈ ℤ with no preimage.

- (d) **Sequence boundedness:** Define "the sequence a₁, a₂, a₃, … is bounded" using quantifiers. Then use your definition to show that the sequence aₙ = (−1)ⁿ is bounded.

- (e) **Density of ℚ in ℝ:** "Between any two distinct real numbers, there exists a rational number." Write this formally, then write its negation formally and translate the negation into English.

---

## Part E — Applications to CS (14 points)

**E1.** (6 pts) Express each program property in predicate logic. Define all predicates and domains.

- (a) *Type safety:* "Every well-typed program does not encounter a type error at runtime."
- (b) *Memory safety:* "Every memory access in the program accesses an address that was allocated and has not yet been freed."
- (c) *Termination:* "For every valid input, the program halts in a finite number of steps."

---

**E2.** (4 pts) The following is the formal definition of Big-O notation:

f(n) = O(g(n)) iff ∃C ∈ ℝ⁺, ∃n₀ ∈ ℕ, ∀n ∈ ℕ, (n ≥ n₀ → f(n) ≤ C · g(n))

- (a) Write the negation: what does f(n) ≠ O(g(n)) mean formally?
- (b) Translate the negation into plain English.
- (c) Identify the quantifier alternation pattern. Is this a ∀∃, ∃∀, ∃∃∀, or something else?

---

**E3.** (4 pts) Below is a flawed program specification. Identify the logical error by analyzing the quantifier structure.

> **Spec A:** ∀ requests r, ∃ server s, s processes r.
>
> **Spec B:** ∃ server s, ∀ requests r, s processes r.

- (a) Translate Spec A and Spec B into plain English.
- (b) Which spec is weaker? Which is stronger?
- (c) A load balancer distributes each request to some available server. Which spec does it satisfy?
- (d) A system with a single server that handles all requests satisfies which spec(s)?

---

## Bonus (8 points — optional)

**Bonus 1.** (4 pts) The ε-δ definition of continuity of f at point a:

∀ε > 0, ∃δ > 0, ∀x ∈ ℝ, (|x − a| < δ → |f(x) − f(a)| < ε)

The definition of **uniform continuity** of f on ℝ:

∀ε > 0, ∃δ > 0, ∀x ∈ ℝ, ∀y ∈ ℝ, (|x − y| < δ → |f(x) − f(y)| < ε)

- (a) What is the quantifier difference between the two definitions?
- (b) Show that uniform continuity implies pointwise continuity (at every point). Argue from the quantifier structure.
- (c) Write the negation of uniform continuity. What does a function that is NOT uniformly continuous look like? Describe it in English.

**Bonus 2.** (4 pts) Let P(x, y) = "x and y are friends" over the domain of people at a party.

Express each social property in predicate logic:
- (a) "Everyone has at least one friend at the party."
- (b) "There is someone who is friends with everyone."
- (c) "No one is friends with themselves."
- (d) "Friendship is symmetric: if x is friends with y, then y is friends with x."
- (e) If properties (c) and (d) both hold, show that the negation of (b) can be simplified. State the simplified form in English.

---

*Submit as a single PDF. Show all work.*
