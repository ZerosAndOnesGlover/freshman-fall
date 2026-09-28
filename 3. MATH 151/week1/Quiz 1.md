---
assessment: Quiz 1
course: MATH 151
component: Quizzes
possible: 20
score: 20
status: graded
started: 2026-09-28
submitted: 2026-09-28
graded: 2026-09-28
source: "QUIZ 1 Propositional Logic.md"
---

# MATH 151 · Quiz 1
## Answer Sheet

**Assessment:** `QUIZ 1 Propositional Logic.md`
**Points available:** 20

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Answer

**Your answer:**

**Problem 1 (4 pts).** p = "The loop terminates", q = "The input is finite", r = "Memory is sufficient"

(a) (q ∧ r) → p

(b) p → r  *("p only if r" means p cannot be true unless r is, so p is the hypothesis)*

(c) ¬p ∧ q  *("but" is a conjunction)*

(d) p ↔ (q ∧ r)

**Problem 2 (6 pts).** (p → q) ∧ (¬p → r)

| p | q | r | p → q | ¬p | ¬p → r | (p → q) ∧ (¬p → r) |
|---|---|---|-------|-----|--------|---------------------|
| T | T | T | T | F | T | **T** |
| T | T | F | T | F | T | **T** |
| T | F | T | F | F | T | **F** |
| T | F | F | F | F | T | **F** |
| F | T | T | T | T | T | **T** |
| F | T | F | T | T | F | **F** |
| F | F | T | T | T | T | **T** |
| F | F | F | T | T | F | **F** |

**Classification:** contingency. It is true in some rows (e.g. TTT) and false in others (e.g. TFT), so it is neither a tautology nor a contradiction.

**Problem 3 (5 pts).** Prove ¬(p → q) ≡ p ∧ ¬q

| Step | Formula | Law |
|---|---|---|
| 1 | ¬(p → q) | given |
| 2 | ≡ ¬(¬p ∨ q) | conditional equivalence: p → q ≡ ¬p ∨ q |
| 3 | ≡ ¬¬p ∧ ¬q | De Morgan's law: ¬(A ∨ B) ≡ ¬A ∧ ¬B |
| 4 | ≡ p ∧ ¬q | double negation: ¬¬p ≡ p |

∴ ¬(p → q) ≡ p ∧ ¬q ∎

**Problem 4 (5 pts).**

(a) ¬((p ∨ ¬q) ∧ (¬p ∨ r))

- ≡ ¬(p ∨ ¬q) ∨ ¬(¬p ∨ r)  — De Morgan (¬(A ∧ B) ≡ ¬A ∨ ¬B)
- ≡ (¬p ∧ ¬¬q) ∨ (¬¬p ∧ ¬r)  — De Morgan (¬(A ∨ B) ≡ ¬A ∧ ¬B), applied to each disjunct
- ≡ **(¬p ∧ q) ∨ (p ∧ ¬r)**  — double negation

(b)

(i) (p ∨ q) ∧ (¬p ∧ ¬q) is a **contradiction**.

- ¬p ∧ ¬q ≡ ¬(p ∨ q) (De Morgan), so the formula is (p ∨ q) ∧ ¬(p ∨ q).
- That has the form A ∧ ¬A, which is F by the negation law, so it is false in every row.

(ii) (p → q) ∨ (q → p) is a **tautology**.

- ≡ (¬p ∨ q) ∨ (¬q ∨ p)  — conditional equivalence, twice
- ≡ (¬p ∨ p) ∨ (q ∨ ¬q)  — commutative and associative laws
- ≡ T ∨ T ≡ T  — negation law, then domination

It is true in every row. Intuitively, if q is true then p → q holds, and if q is false then q → p holds.

*Marks: 20 / 20*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | **20 / 20** |
| **Percent** | 100% |
| **Graded** | 2026-09-28 |

**Feedback:**

All four problems are correct, and every mark in the key's rubric is earned.

| Q | Rubric | Marks |
|---|---|---|
| P1 | (a) 1 · (b) 1 · (c) 1 · (d) 1 | 4 / 4 |
| P2 | p→q column 1 · ¬p column 1 · ¬p→r column 1 · final column 2 · classification 1 | 6 / 6 |
| P3 | conditional equivalence 1 · De Morgan 2 · double negation 1 · clean final form 1 | 5 / 5 |
| P4(a) | outer De Morgan 1 · inner De Morgan + double negation 1 | 2 / 2 |
| P4(b) | (i) classification + justification 1 · (ii) classification + justification 2 | 3 / 3 |

**The answers were checked independently, not only against the key.** Every cell of
the P2 table was recomputed and all eight rows agree in all four columns. P3's chain is
sound: the negation is pushed through the conditional, then De Morgan, then double negation.
P4(a) fully simplifies to (¬p ∧ q) ∨ (p ∧ ¬r). P4(b)(i) is (p ∨ q) ∧ ¬(p ∨ q) = A ∧ ¬A = F,
a contradiction; P4(b)(ii) reduces to (¬p ∨ p) ∨ (q ∨ ¬q) = T ∨ T = T, a tautology.

Two things in the working deserve credit beyond the rubric. P2 row 2 (p = T, q = T, r = F)
is exactly the "common error" row flagged in the key — when p is true, ¬p → r is vacuously
true, so r is irrelevant — and getting it right is what the question is really testing. P1(b)
records the reasoning behind "p only if r" = p → r, which is the trap (the converse is the
usual mistake), and P4(b)(ii) adds a genuine intuitive justification rather than just asserting
the classification.

**A process note, not charged against this score.** The quiz paper and the instructor key now
live in separate folders (`quiz/` vs `solutions_instructor/`), which answers the note recorded
on the MATH 141 Quiz 01 grade. The working still follows the key closely on P3 and P4(a), but
those derivations are nearly forced — there is essentially one standard order in which to apply
the laws. The parts where the answer has freedom (P1's annotations, P2's classification
examples, P4(b)(ii)'s reading of the tautology) contain reasoning not present in the key, which
is consistent with the work having been produced under quiz conditions.

*Graded against `QUIZ 1 Solutions.md` (instructor key, per-question rubric).*

