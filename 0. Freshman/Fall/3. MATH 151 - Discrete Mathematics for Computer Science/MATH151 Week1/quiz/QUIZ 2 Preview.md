# MATH 151 · Discrete Mathematics for Computer Science
## Quiz 2 — Scope Preview
### Quiz administered: Monday 5 October 2026, 13:00–13:15 (first 15 minutes of lecture) · Week 2

---

**Coverage:** Week 1 material only:
- Week 1: Predicate logic, quantifiers, nested quantifiers, negation of quantified statements

*(Week 2 material is not on this quiz — it is taught after the quiz.)*

---

## What You Must Know Cold for Week 1 Material

### 1. Predicates

- A predicate P(x) is a function from domain elements to {T, F}
- Evaluating P(a) for a specific value a
- Distinguishing free variables from bound variables

### 2. Quantifiers — Definitions

**∀x P(x):** True iff P(a) is true for **every** a in the domain. One false value → whole statement false.

**∃x P(x):** True iff P(a) is true for **at least one** a. One true value → whole statement true.

Know these cold — including how to prove/disprove each:
- Prove ∀: argue for arbitrary x (no assumptions about x beyond domain membership)
- Disprove ∀: give one counterexample
- Prove ∃: give one witness
- Disprove ∃: argue P(x) fails for every x

### 3. Translation Rules

These must be automatic:

| English | Logic |
|---|---|
| "Every A is B" | ∀x (A(x) → B(x)) |
| "Some A is B" | ∃x (A(x) ∧ B(x)) |
| "No A is B" | ∀x (A(x) → ¬B(x)) |
| "Not every A is B" | ∃x (A(x) ∧ ¬B(x)) |

**Critical rule:** ∀ with a restricted domain uses →. ∃ with a restricted domain uses ∧.

### 4. Negation Rules (must produce in < 30 seconds)

| Original | Negation |
|---|---|
| ∀x P(x) | ∃x ¬P(x) |
| ∃x P(x) | ∀x ¬P(x) |
| ∀x ∃y P(x,y) | ∃x ∀y ¬P(x,y) |
| ∃x ∀y P(x,y) | ∀x ∃y ¬P(x,y) |

Push ¬ all the way inward. Never leave ¬∀ or ¬∃ in a final answer.

### 5. Nested Quantifiers — Order Matters

Know that ∀x ∃y P(x,y) ≠ ∃y ∀x P(x,y) in general, and be able to explain why with an example.

Know the implication: ∃y ∀x P(x,y) → ∀x ∃y P(x,y) (but not vice versa).

---

## Sample Quiz 2 Problems

**Problem 1.** (4 pts) Let D(x) = "x is divisible by 3", P(x) = "x is prime." Domain: ℤ⁺.

Evaluate:
- (a) ∀x (P(x) → ¬D(x))
- (b) ∃x (P(x) ∧ D(x))

**Problem 2.** (4 pts) Negate and simplify fully. Indicate which (original or negation) is true:
- (a) ∀x ∈ ℝ, x² ≥ 0
- (b) ∃x ∈ ℤ, ∀y ∈ ℤ, x ≤ y

**Problem 3.** (4 pts) Determine the truth value. If FALSE, give a specific counterexample (explicit values of x and y):
- (a) ∀x ∈ ℤ, ∃y ∈ ℤ, y > x
- (b) ∃y ∈ ℤ, ∀x ∈ ℤ, y > x

**Problem 4.** (4 pts) Translate into predicate logic. State domain and predicates:
- "Every sorting algorithm that is correct produces a permutation of its input that is in non-decreasing order."

**Problem 5.** (4 pts) From Week 2 — proof technique question (see Week 2 materials).

---

## Study Recommendations

1. **Drill negation until automatic.** Given any quantified statement, be able to write its negation in under 30 seconds without thinking. Practice on PS1 problems.

2. **Practice the ∀→ vs ∃∧ rule.** Take 10 English sentences and translate each. Check whether you used → or ∧ correctly in each case.

3. **Work PS1 fully.** The problem set covers exactly what the quiz will test.

4. **Do Exercise 1.2 from Lab 1 by hand again.** Filling in the divisibility table by hand builds quantifier intuition.

5. **Know one concrete example of ∀∃ ≠ ∃∀.** The example "∀x ∃y (y > x) is true but ∃y ∀x (y > x) is false" over ℤ is the canonical one.
