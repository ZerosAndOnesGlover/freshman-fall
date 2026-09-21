# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 0: Propositional Logic
### Released: Friday 25 September 2026, 14:00 (after the Friday lecture) | Due: Friday 2 October 2026, 17:00 (Week 1)

---

> *Revised 2026-09-21.* The optional bonus section was removed to keep the set to 100 points of
> this week's material.

**Instructions:**
- Show all work. Answers without justification receive no credit.
- For truth tables, use the systematic column-by-column method shown in lecture.
- For algebraic proofs, cite the law used at each step.
- Work must be submitted individually. Collaboration on approach is allowed; write-up must be your own.
- Submission: handwritten or typed PDF. LaTeX is encouraged but not required.

**Scoring:** 100 points total. Point values marked per problem.

---

## Part A: Propositions and Translation (20 points)

**A1.** (6 pts) For each sentence, state whether it is a proposition. If it is, give its truth value (or state that it is unknown).

(a) "Every prime number greater than 2 is odd."

(b) "This problem set is difficult or easy."

(c) "x² − 4 = 0"

(d) "There are infinitely many prime numbers." *(Hint: this was proved by Euclid.)*

(e) "The program in Listing A halts on all inputs." *(No listing is provided — this is about the nature of the claim.)*

(f) "Prove that 1 + 1 = 2."

---

**A2.** (8 pts) Let:
- p = "The network is connected."
- q = "The server is running."
- r = "The database is reachable."
- s = "The user can log in."

Translate each English statement into a logical formula. Then write the *negation* of the formula (in simplified form — push negations inward using De Morgan's Laws, not just "¬(...)").

(a) "The user can log in if and only if the network is connected and the server is running."

(b) "If the network is connected and the server is running, then the database is reachable and the user can log in."

(c) "The user cannot log in unless the network is connected."

(d) "It is not the case that both the server is running and the database is unreachable."

---

**A3.** (6 pts) Translate each logical formula into a clear English sentence (using the variables from A2), then determine its truth value assuming: p = T, q = T, r = F, s = F.

(a) (p ∧ q) → s

(b) ¬r → ¬s

(c) (p ↔ q) ∧ (r ↔ s)

---

## Part B: Truth Tables (28 points)

**B1.** (8 pts) Construct a complete truth table for each formula. Clearly label every intermediate column.

(a) (p → q) ∧ (q → p)

(b) ¬p ∨ (p ∧ q)

(c) (p ∨ q) → (p ∧ q)

(d) (p → q) → ((p → ¬q) → ¬p)

---

**B2.** (8 pts) Use your truth tables from B1 to answer:

(a) Which formulas in B1 are tautologies? Contradictions? Contingencies?

(b) Formula B1(a) is a well-known connective — which one?

(c) Formula B1(b) has a simple equivalent — which one? Prove the equivalence using laws (not truth tables).

---

**B3.** (6 pts) Without building a full truth table, determine the truth value of each formula under the given assignment. Show intermediate steps.

Assignment: p = T, q = F, r = T, s = F

(a) (p ∧ ¬q) → (r ∨ s)

(b) ¬(p ↔ r) ∨ (q ∧ ¬s)

(c) ((p → q) → r) ∧ (¬s ∨ q)

---

**B4.** (6 pts) How many rows does a truth table for a formula with variables p₁, p₂, ..., pₙ have? Given a formula with 5 variables:

(a) How many rows?

(b) In how many rows is the formula true if it is a tautology? A contradiction?

(c) If a 5-variable formula has exactly 1 row where it is true, is it a tautology, contradiction, or contingency? Give an example of such a formula.

---

## Part C: The Conditional (20 points)

**C1.** (8 pts) For each conditional, write (i) the converse, (ii) the inverse, (iii) the contrapositive. State which are logically equivalent to the original.

(a) "If a number is divisible by 4, then it is divisible by 2."

(b) "If the algorithm runs in O(n log n), then it is efficient enough for production."

(c) p → (q ∧ r)

(d) ¬p → ¬(q ∨ r)

---

**C2.** (6 pts) A conditional statement can be vacuously true. For each situation, explain whether the conditional is vacuously true, substantively true, or false.

(a) "If 2 is odd, then the moon is made of cheese." (Evaluate: p = F)

(b) "If you score 100 on every problem set, you will pass the course." (Evaluate: you scored 80 on PS0)

(c) "If x > 100, then x > 50." (Evaluate when x = 3; when x = 200)

---

**C3.** (6 pts) This problem explores the *paradoxes of material implication* — cases where the truth-table definition of → produces results that feel counterintuitive.

(a) Show that (p → q) ∨ (q → p) is a tautology. (Use a truth table or algebraic proof.) This means: for any two propositions p and q, either "p implies q" or "q implies p" — or both. Does this seem intuitively correct? Explain the tension between the logical result and our everyday understanding of "implies."

(b) Show that p → (q → p) is a tautology. This means: any true proposition is implied by any proposition. Explain what this means and why it is "paradoxical" from an everyday standpoint.

(c) In formal logic, these "paradoxes" are not actually problems — they arise from taking → to mean *material implication* (defined purely by truth values) rather than *causal* or *meaningful* implication. In 2–3 sentences, explain why the material conditional is still the right choice for formal mathematics, despite these counterintuitive results.

---

## Part D: Equivalence Laws and Normal Forms (32 points)

**D1.** (12 pts) Prove each equivalence using *only* the laws from Lecture 2 (L02, Friday) (no truth tables). Cite the law at each step.

(a) (p ∧ q) ∨ (p ∧ ¬q) ≡ p

(b) (p → q) ∧ (p → ¬q) ≡ ¬p

(c) ¬(p ↔ q) ≡ (p ∧ ¬q) ∨ (¬p ∧ q)

(d) (p ∨ q) ∧ (¬p ∨ r) → (q ∨ r) is a tautology.
*(Hint: Show the formula ≡ T. This is the resolution rule — foundational to automated theorem proving.)*

---

**D2.** (8 pts) Convert each formula to Conjunctive Normal Form (CNF). Show all steps.

(a) p → q

(b) p ↔ q

(c) ¬(p ∨ ¬q) → r

---

**D3.** (6 pts) Convert each formula to Disjunctive Normal Form (DNF) using the truth table method.

(a) p ∧ (q ∨ ¬r)

(b) (p ↔ q) — verify that your DNF matches your answer from D2(b) (they should give the same truth table).

---

**D4.** (6 pts) **Functional completeness.**

(a) Show that {¬, ∨} is functionally complete: express p ∧ q using only ¬ and ∨.

(b) Show that {¬, →} is functionally complete: express p ∨ q using only ¬ and →.
*(Hint: use the equivalence p → q ≡ ¬p ∨ q.)*

(c) The set {∧, ∨} is NOT functionally complete. What connective does it fail to express, and why?

---

*Submit as a single PDF. Show all work. Good luck.*
