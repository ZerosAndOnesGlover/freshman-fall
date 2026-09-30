---
assessment: PS 1
course: MATH 151
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-09-30
submitted: 2026-09-30
graded: 2026-09-30
source: "PS 1 Predicate Logic.md"
---

# MATH 151 · PS 1
## Answer Sheet

**Assessment:** `PS 1 Predicate Logic.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Part A — Predicates and Domains  (18 points)

#### A1 (9 pts)

Let P(x) = "x² − 5x + 6 = 0". Evaluate P(x) for x ∈ {0, 1, 2, 3, 4, 6}.

**Question A1(a).** List all x in the given set for which P(x) is true.

**Answer.** Factor first: x² − 5x + 6 = (x − 2)(x − 3), so P(x) is true exactly when x = 2 or x = 3.

| x | x² − 5x + 6 | P(x) |
|---|---|---|
| 0 | 0 − 0 + 6 = 6 | F |
| 1 | 1 − 5 + 6 = 2 | F |
| 2 | 4 − 10 + 6 = 0 | **T** |
| 3 | 9 − 15 + 6 = 0 | **T** |
| 4 | 16 − 20 + 6 = 2 | F |
| 6 | 36 − 30 + 6 = 12 | F |

P(x) is true for **x ∈ {2, 3}**.

**Question A1(b).** Is ∀x ∈ {0,1,2,3,4,6}, P(x) true? Justify.

**Answer.** **FALSE.** A universal statement fails if a single element fails. Counterexample: x = 0 gives 6 ≠ 0, so P(0) is false.

**Question A1(c).** Is ∃x ∈ {0,1,2,3,4,6}, P(x) true? Exhibit a witness.

**Answer.** **TRUE.** Witness: x = 2, since 2² − 5·2 + 6 = 0. (x = 3 also works.)

#### A2 (9 pts)

Let D(x, y) mean "x divides y" (there exists an integer k with y = kx). Domain: ℤ⁺. Evaluate each as TRUE or FALSE with brief justification.

**Question A2(a).** D(3, 12)

**Answer.** **TRUE.** 12 = 4 · 3, so k = 4 works.

**Question A2(b).** D(5, 13)

**Answer.** **FALSE.** 5 · 2 = 10 < 13 < 15 = 5 · 3, so no integer k gives 5k = 13 (13 / 5 = 2.6 ∉ ℤ).

**Question A2(c).** D(n, 0) for any n ∈ ℤ⁺. *Hint: is 0 = k·n solvable?*

**Answer.** **TRUE** for every n ∈ ℤ⁺. 0 = 0 · n, so k = 0 works. The definition only asks for k ∈ ℤ, not k ∈ ℤ⁺, so k = 0 is allowed. Every positive integer divides 0.

*(Strictly, 0 ∉ ℤ⁺, so D(n, 0) uses a value outside the stated domain. Evaluating the defining condition directly still gives TRUE.)*

*Marks: 18 / 18*

---

### Part B — Single Quantifiers  (22 points)

#### B1 (12 pts)

For each statement, determine its truth value over the given domain. If TRUE, briefly explain why. If FALSE, give a specific counterexample. Domain: ℤ unless otherwise stated.

**Question B1(a).** ∀x, x² > x

**Answer.** **FALSE.** Counterexample: x = 0 gives 0² = 0, and 0 > 0 is false. (x = 1 also fails, since 1 > 1 is false.)

**Question B1(b).** ∃x, x² = x

**Answer.** **TRUE.** Witness: x = 0 (0² = 0) or x = 1 (1² = 1). In fact x² = x ⇔ x(x − 1) = 0 ⇔ x ∈ {0, 1}.

**Question B1(c).** ∃x ∈ ℤ, x² = 2

**Answer.** **FALSE.** An existential is refuted by showing *every* element fails, so one counterexample is not enough:
- if |x| ≤ 1, then x² ∈ {0, 1}, so x² ≤ 1 < 2;
- if |x| ≥ 2, then x² ≥ 4 > 2.

Every integer lands in one of these two cases, so no integer squares to 2. (The only real solutions are ±√2, which are not integers.)

#### B2 (10 pts)

Translate each English statement into predicate logic. Define all predicates and state the domain.

**Question B2(a).** "Some prime number is even."

**Answer.**
- Domain: ℤ⁺.
- Predicates: P(x) = "x is prime", E(x) = "x is even".
- Formula: **∃x (P(x) ∧ E(x))**
- ∃ pairs with ∧, not →. ∃x (P(x) → E(x)) would be true for any non-prime x, which is not what the sentence says. The statement is true, with witness x = 2.

**Question B2(b).** "There is a real number that is not the square of any real number."

**Answer.**
- Domain: ℝ for both variables.
- Predicate: S(x, y) = "x = y²" ("x is the square of y").
- Formula: **∃x ∀y ¬S(x, y)**, i.e. **∃x ∀y (x ≠ y²)**
- Equivalently ∃x ¬∃y (x = y²). The two are the same because ¬∃y ≡ ∀y ¬. The statement is true, with witness x = −1, since y² ≥ 0 > −1 for every real y.

*Marks: 22 / 22*

---

### Part C — Negation  (25 points)

#### C1 (15 pts)

Negate each statement, simplify fully (push ¬ all the way inward), and state whether the original statement or its negation is true. Domain: ℤ unless stated.

**Question C1(a).** ∀x ∈ ℤ, ∃y ∈ ℤ, x + y = 0

**Answer.**
- ¬∀x ∃y (x + y = 0)
- ≡ ∃x ¬∃y (x + y = 0)  — ¬∀ ≡ ∃¬
- ≡ **∃x ∈ ℤ, ∀y ∈ ℤ, x + y ≠ 0**  — ¬∃ ≡ ∀¬

The **original is true**. Given any integer x, choose y = −x ∈ ℤ, and then x + y = 0. So the negation is false.

**Question C1(b).** ∃x ∈ ℝ, ∀y ∈ ℝ, x · y = y

**Answer.**
- ¬∃x ∀y (x · y = y)
- ≡ ∀x ¬∀y (x · y = y)  — ¬∃ ≡ ∀¬
- ≡ **∀x ∈ ℝ, ∃y ∈ ℝ, x · y ≠ y**  — ¬∀ ≡ ∃¬

The **original is true**. Take x = 1: then 1 · y = y for every real y, because 1 is the multiplicative identity. So the negation is false.

**Question C1(c).** ∀x (E(x) → ∃k, x = 2k) where E(x) = "x is even"

**Answer.** Here x, k ∈ ℤ.
- ¬∀x (E(x) → ∃k (x = 2k))
- ≡ ∃x ¬(E(x) → ∃k (x = 2k))  — ¬∀ ≡ ∃¬
- ≡ ∃x (E(x) ∧ ¬∃k (x = 2k))  — ¬(A → B) ≡ A ∧ ¬B
- ≡ **∃x (E(x) ∧ ∀k (x ≠ 2k))**  — ¬∃ ≡ ∀¬

The **original is true**. "x is even" means by definition that x = 2k for some integer k, so every even x has such a k. The negation would need an even number that is not a multiple of 2, which is impossible.

#### C2 (10 pts)

The following are purported negations. Each contains an error. Identify the error and give the correct negation.

**Question C2(a).** Statement: ∃x (P(x) ∧ Q(x)). Proposed negation: ∀x (¬P(x) ∧ ¬Q(x)).

**Answer.** **Error:** the quantifier flip ∃ → ∀ is correct, but De Morgan's law was applied wrongly to the conjunction. ¬(P ∧ Q) ≡ ¬P **∨** ¬Q, not ¬P ∧ ¬Q.

**Correct negation:**
- ¬∃x (P(x) ∧ Q(x)) ≡ ∀x ¬(P(x) ∧ Q(x)) ≡ **∀x (¬P(x) ∨ ¬Q(x))**
- Equivalently: ∀x (P(x) → ¬Q(x)).

The proposed version is too strong. It says every x fails *both* P and Q. The true negation only needs every x to fail *at least one* of them. For example, if P(a) is true and Q(a) is false for every a, the original is false. The correct negation is then true, but the proposed one is false.

**Question C2(b).** Statement: ∀x (P(x) → Q(x)). Proposed negation: ∃x (P(x) → ¬Q(x)).

**Answer.** **Error:** the quantifier flip ∀ → ∃ is correct, but the negation of a conditional is not another conditional. ¬(P → Q) ≡ P **∧** ¬Q, not P → ¬Q.

**Correct negation:**
- ¬∀x (P(x) → Q(x)) ≡ ∃x ¬(P(x) → Q(x)) ≡ **∃x (P(x) ∧ ¬Q(x))**

A counterexample to "every P is a Q" is something that *is* a P and *is not* a Q. The proposed version fails as a negation because it can be true at the same time as the original. Take any x with P(x) false: then P(x) → ¬Q(x) is vacuously true, and P(x) → Q(x) is vacuously true as well. In a domain where P is false everywhere, both statements hold.

*Marks: 25 / 25*

---

### Part D — Nested Quantifiers  (20 points)

#### D1 (20 pts)

Determine the truth value of each statement over the domain ℤ. Provide a proof sketch (for TRUE) or explicit counterexample (for FALSE).

**Question D1(a).** ∀x ∃y (y > x)

**Answer.** **TRUE.**

*Proof sketch:* Let x ∈ ℤ be arbitrary. Choose y = x + 1 ∈ ℤ. Then y = x + 1 > x. Since x was arbitrary, the statement holds for every x. Here y is allowed to depend on x.

**Question D1(b).** ∃y ∀x (y > x)

**Answer.** **FALSE.**

*Counterexample:* The negation is ∀y ∃x (y ≤ x). Let y ∈ ℤ be any candidate and take x = y (or x = y + 1). Then y > x is false, so y fails. Every candidate y is defeated this way, so ℤ has no largest element.

The quantifiers in (a) and (b) are the same but in a different order. In (a), y may depend on x. In (b), a single y must work for all x at once, which is impossible.

**Question D1(c).** ∀x ∃y (x · y = 1) — domain: ℤ

**Answer.** **FALSE.**

*Counterexample:* x = 2. Then 2y = 1 forces y = 1/2 ∉ ℤ, so no integer y works. (x = 0 also fails, since 0 · y = 0 ≠ 1 for all y.) In fact only x = 1 and x = −1 have integer multiplicative inverses.

**Question D1(d).** ∀x ∃y (x · y = 1) — domain: ℚ \ {0}

**Answer.** **TRUE.**

*Proof sketch:* Let x ∈ ℚ \ {0}. Write x = p/q with p, q ∈ ℤ, q ≠ 0, and p ≠ 0 since x ≠ 0. Choose y = q/p.
- y ∈ ℚ because q, p ∈ ℤ and p ≠ 0.
- y ≠ 0 because q ≠ 0.
- x · y = (p/q)(q/p) = 1.

So y lies in the domain and works, and x was arbitrary. Removing 0 from the domain matters: 0 has no inverse, just as in (c).

*Marks: 20 / 20*

---

### Part E — Applications to CS  (15 points)

#### E1 (15 pts)

The following is the formal definition of Big-O notation:

f(n) = O(g(n)) iff ∃C ∈ ℝ⁺, ∃n₀ ∈ ℕ, ∀n ∈ ℕ, (n ≥ n₀ → f(n) ≤ C · g(n))

**Question E1(a).** Write the negation: what does f(n) ≠ O(g(n)) mean formally?

**Answer.** Negate the definition, pushing ¬ inward one step at a time:

- ¬ ∃C ∃n₀ ∀n (n ≥ n₀ → f(n) ≤ C · g(n))
- ≡ ∀C ¬ ∃n₀ ∀n (n ≥ n₀ → f(n) ≤ C · g(n))  — ¬∃ ≡ ∀¬
- ≡ ∀C ∀n₀ ¬ ∀n (n ≥ n₀ → f(n) ≤ C · g(n))  — ¬∃ ≡ ∀¬
- ≡ ∀C ∀n₀ ∃n ¬(n ≥ n₀ → f(n) ≤ C · g(n))  — ¬∀ ≡ ∃¬
- ≡ ∀C ∀n₀ ∃n (n ≥ n₀ ∧ ¬(f(n) ≤ C · g(n)))  — ¬(A → B) ≡ A ∧ ¬B
- ≡ ∀C ∀n₀ ∃n (n ≥ n₀ ∧ f(n) > C · g(n))  — ¬(a ≤ b) ≡ a > b

The domains stay attached to their variables:

**f(n) ≠ O(g(n)) iff ∀C ∈ ℝ⁺, ∀n₀ ∈ ℕ, ∃n ∈ ℕ, (n ≥ n₀ ∧ f(n) > C · g(n))**

**Question E1(b).** Translate the negation into plain English.

**Answer.** *However large a constant C you pick, and however far out a starting point n₀ you pick, there is always some n at or beyond n₀ where f(n) is bigger than C · g(n).*

In other words, no constant multiple of g eventually stays above f. f keeps escaping every bound of the form C · g(n). Because this holds for every n₀, it happens infinitely often.

*Example:* n² ≠ O(n). Given any C > 0 and n₀ ∈ ℕ, take n = max(n₀, ⌊C⌋ + 1). Then n ≥ n₀ and n > C, so n² = n · n > C · n.

*Marks: 15 / 15*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | **100 / 100** |
| **Percent** | 100% |
| **Graded** | 2026-09-30 |

**Feedback:**

Every part is correct and every mark in the allocation is earned. No instructor key for
`PS 1 Predicate Logic.md` is held in this repository, so the sheet was graded on its own
mathematical merits; the checks below are independent of any key.

| Q | Allocation | Marks |
|---|---|---|
| A1(a) | truth table 3 · answer {2,3} 1 | 4 / 4 |
| A1(b) | FALSE 1 · counterexample + justification 2 | 3 / 3 |
| A1(c) | TRUE 1 · witness 1 | 2 / 2 |
| A2(a) | TRUE 1 · k = 4 exhibited 1 | 2 / 2 |
| A2(b) | FALSE 1 · justification 2 | 3 / 3 |
| A2(c) | TRUE 1 · k = 0 2 · domain caveat 1 | 4 / 4 |
| B1(a) | FALSE 1 · counterexample 3 | 4 / 4 |
| B1(b) | TRUE 1 · witness 1 · full solution set 2 | 4 / 4 |
| B1(c) | FALSE 1 · exhaustive argument 3 | 4 / 4 |
| B2(a) | domain + predicates 2 · formula 2 · ∃ with ∧ not → 1 | 5 / 5 |
| B2(b) | domain + predicate 2 · formula 2 · equivalence + witness 1 | 5 / 5 |
| C1(a) | steps to ∃∀ with ≠ 3 · truth value + witness 2 | 5 / 5 |
| C1(b) | steps to ∀∃ 3 · truth value + witness 2 | 5 / 5 |
| C1(c) | steps through ¬(A→B) 3 · truth value 2 | 5 / 5 |
| C2(a) | error identified 2 · correct negation 2 · too-strong argument 1 | 5 / 5 |
| C2(b) | error identified 2 · correct negation 2 · vacuous-truth counter-argument 1 | 5 / 5 |
| D1(a) | TRUE 1 · proof with y = x + 1 4 | 5 / 5 |
| D1(b) | FALSE 1 · negation of the statement 2 · defeat of every candidate 2 | 5 / 5 |
| D1(c) | FALSE 1 · counterexample 3 · note on ±1 1 | 5 / 5 |
| D1(d) | TRUE 1 · construction y = q/p 2 · domain checks 2 | 5 / 5 |
| E1(a) | each negation step 6 · final formula with domains 3 | 9 / 9 |
| E1(b) | plain-English rendering 5 · example n² ≠ O(n) 1 | 6 / 6 |

**How the answers were checked.** A1's table was recomputed cell by cell: (0, 6), (1, 2),
(2, 0), (3, 0), (4, 2), (6, 12), matching the sheet exactly, and the factorization
(x − 2)(x − 3) is right. Both C2 corrections were verified by exhaustion over all eight
truth valuations of P and Q — ∀x(¬P ∨ ¬Q) is the exact negation of ∃x(P ∧ Q), and
∃x(P ∧ ¬Q) is the exact negation of ∀x(P → Q). E1(a)'s six-step chain was checked the same
way on a finite window with f = n², g = n, five values of C and five of n₀: the proposed
negation agrees with the negation of the definition in every case. B1(c)'s case split
(|x| ≤ 1 and |x| ≥ 2) genuinely covers ℤ, and C1's three truth values were confirmed by
exhibiting the stated witnesses. D1(d)'s construction is a genuine ℚ∖{0} argument, and it
correctly checks y ≠ 0 rather than only x · y = 1.

**Work worth noting beyond the rubric.** A2(c) is the sharpest item on the sheet. The hint
asks whether 0 = k·n is solvable, and the answer takes the decisive point: the definition
quantifies k over ℤ, not ℤ⁺, so k = 0 is admissible and D(n, 0) is true for every n. It
then adds the domain caveat that 0 ∉ ℤ⁺ under the stated domain, so the pair (n, 0) is not
formally admissible, and that the defining condition nevertheless evaluates to TRUE. A
minimal answer would have stopped at k = 0. B1(c) makes the same distinction in a different
place, stating that refuting an existential requires showing *every* element fails and
organising the proof as an exhaustive case split accordingly. C2(b)'s argument is also
better than the question asked: rather than just correcting ∃x(P → ¬Q), it shows why the
proposed form fails by exhibiting a valuation (P false everywhere) where the original and
its alleged negation are both true, which is the actual defining test for a negation.

**One presentational note, not charged against the score.** In D1(b) the sheet heads the
argument "Counterexample:" but then presents the *negation* ∀y∃x(y ≤ x) and shows it holds.
That is the correct and in fact stronger proof — no greatest integer — and the accompanying
comparison of (a) and (b) explains why the quantifier order matters. The label is loose
rather than the mathematics. Worth tightening in later sheets: for a ∀-statement, a
counterexample is a single violating instance, whereas showing the negation is a complete
argument, and the two should not share a heading.

---
