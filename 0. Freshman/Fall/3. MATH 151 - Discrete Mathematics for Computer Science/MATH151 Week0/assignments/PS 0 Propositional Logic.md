# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 0: Propositional Logic
### Released: Friday 25 September 2026, 14:00 (after the Friday lecture) | Due: Friday 2 October 2026, 17:00 (Week 1)

---

> *Revised 2026-09-21.* The optional bonus section was removed to keep the set to 100 points of
> this week's material.
>
> *Revised 2026-09-26.* Cut from 14 problems and about 50 parts to 7 problems and 20 short parts, to fit
> about three hours. Kept: one or two items of each skill. Removed: the assignment-evaluation drill, the
> truth-table row-count questions, vacuous truth, the material-implication essay, the resolution tautology
> and the {∧, ∨} completeness question.

**Instructions:**
- Show all work. Answers without justification receive no credit.
- For truth tables, use the systematic column-by-column method shown in lecture.
- For algebraic proofs, cite the law used at each step.
- Work must be submitted individually. Collaboration on approach is allowed; write-up must be your own.
- Submission: handwritten or typed PDF. LaTeX is encouraged but not required.

**Expected time:** about 3 hours. **Scoring:** 100 points total. Point values marked per problem.

---

## Problem 1: Propositions (9 points)

For each sentence, state whether it is a proposition. If it is, give its truth value (or state that it is
unknown). *(3 pts each)*

(a) "Every prime number greater than 2 is odd."

(b) "x² − 4 = 0"

(c) "Prove that 1 + 1 = 2."

---

## Problem 2: Translation and Negation (12 points)

Let:
- p = "The network is connected."
- q = "The server is running."
- r = "The database is reachable."
- s = "The user can log in."

Translate each English statement into a logical formula. Then write the *negation* of the formula (in
simplified form — push negations inward using De Morgan's Laws, not just "¬(...)"). *(4 pts each)*

(a) "The user can log in if and only if the network is connected and the server is running."

(b) "If the network is connected and the server is running, then the database is reachable and the user can log in."

(c) "The user cannot log in unless the network is connected."

---

## Problem 3: Truth Tables (18 points)

Construct a complete truth table for each formula. Clearly label every intermediate column. *(4 pts each)*

(a) (p → q) ∧ (q → p)

(b) (p ∨ q) → (p ∧ q)

(c) (p → q) → ((p → ¬q) → ¬p)

(d) Which of the three are tautologies, contradictions, or contingencies? Which well-known connective is
(a)? *(6 pts)*

---

## Problem 4: Converse, Inverse, Contrapositive (12 points)

For each conditional, write (i) the converse, (ii) the inverse, (iii) the contrapositive. State which are
logically equivalent to the original. *(6 pts each)*

(a) "If a number is divisible by 4, then it is divisible by 2."

(b) p → (q ∧ r)

---

## Problem 5: Proofs by Laws (21 points)

Prove each equivalence using *only* the laws from Lecture 2 (L02, Friday) — no truth tables. Cite the law
at each step. *(7 pts each)*

(a) (p ∧ q) ∨ (p ∧ ¬q) ≡ p

(b) (p → q) ∧ (p → ¬q) ≡ ¬p

(c) ¬(p ↔ q) ≡ (p ∧ ¬q) ∨ (¬p ∧ q)

---

## Problem 6: Normal Forms (16 points)

(a) Convert p → q to Conjunctive Normal Form (CNF). *(4 pts)*

(b) Convert p ↔ q to CNF. Show all steps. *(6 pts)*

(c) Convert p ∧ (q ∨ ¬r) to Disjunctive Normal Form (DNF) using the truth table method. *(6 pts)*

---

## Problem 7: Functional Completeness (12 points)

(a) Show that {¬, ∨} is functionally complete: express p ∧ q using only ¬ and ∨. *(6 pts)*

(b) Show that {¬, →} is functionally complete: express p ∨ q using only ¬ and →. *(6 pts)*
*(Hint: use the equivalence p → q ≡ ¬p ∨ q.)*

---

*Submit as a single PDF. Show all work. Good luck.*
