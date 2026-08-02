# MATH 151 · Week 1
## Quiz 1 Solutions — INSTRUCTOR ONLY

---

### Problem 1 — Translations (4 points)

p = "loop terminates", q = "input is finite", r = "memory is sufficient"

**(a)** "If the input is finite and memory is sufficient, then the loop terminates."
**Answer: (q ∧ r) → p** — 1 pt

**(b)** "The loop terminates only if memory is sufficient."
**Answer: p → r** — 1 pt

*Grading note:* "p only if r" = p → r. A common error is r → p (converse). Award 0 pts for converse.

**(c)** "The loop does not terminate, but the input is finite."
**Answer: ¬p ∧ q** — 1 pt

*Grading note:* "but" is logical AND. Full credit for ¬p ∧ q. Deduct 0.5 for ¬p ∨ q.

**(d)** "The loop terminates if and only if both the input is finite and memory is sufficient."
**Answer: p ↔ (q ∧ r)** — 1 pt

*Grading note:* Require the biconditional. p → (q ∧ r) or (q ∧ r) → p alone get 0.5 pt.

---

### Problem 2 — Truth Table (6 points)

Formula: (p → q) ∧ (¬p → r)

| p | q | r | p→q | ¬p | ¬p→r | Result |
|---|---|---|-----|-----|------|--------|
| T | T | T | T   | F   | T    | **T**  |
| T | T | F | T   | F   | T    | **T**  |
| T | F | T | F   | F   | T    | **F**  |
| T | F | F | F   | F   | T    | **F**  |
| F | T | T | T   | T   | T    | **T**  |
| F | T | F | T   | T   | F    | **F**  |
| F | F | T | T   | T   | T    | **T**  |
| F | F | F | T   | T   | F    | **F**  |

Classification: **Contingency** (some T, some F rows).

*Grading:* 1 pt per correct intermediate column (p→q, ¬p, ¬p→r) = 3 pts. 2 pts for correct final column. 1 pt for correct classification.

*Common errors:* Row 2 result — students sometimes write F because they see q=T, r=F, but r is irrelevant when p=T (making ¬p=F, so ¬p→r is vacuously T). Row 6: ¬p→r with ¬p=T, r=F gives F — some students write T.

---

### Problem 3 — Algebraic Proof (5 points)

**¬(p → q) ≡ p ∧ ¬q**

```
¬(p → q)
≡ ¬(¬p ∨ q)       [Conditional Equivalence: p→q ≡ ¬p∨q]        (1 pt)
≡ ¬(¬p) ∧ ¬q      [De Morgan's Law: ¬(A∨B) ≡ ¬A∧¬B]            (2 pts)
≡ p ∧ ¬q           [Double Negation: ¬¬p ≡ p]                    (1 pt)
```

*Grading:* 1 pt for correctly applying Conditional Equivalence as first step. 2 pts for correct De Morgan application. 1 pt for Double Negation. 1 pt for clean correct final form. Deduct 1 pt if laws are applied but not cited. Award 0 for truth table approach (problem specifies laws only).

---

### Problem 4 (5 points)

**(a)** (2 pts) ¬((p ∨ ¬q) ∧ (¬p ∨ r))

```
¬((p ∨ ¬q) ∧ (¬p ∨ r))
≡ ¬(p ∨ ¬q) ∨ ¬(¬p ∨ r)         [De Morgan: ¬(A∧B) ≡ ¬A∨¬B]
≡ (¬p ∧ ¬¬q) ∨ (¬¬p ∧ ¬r)       [De Morgan twice: ¬(A∨B) ≡ ¬A∧¬B]
≡ (¬p ∧ q) ∨ (p ∧ ¬r)            [Double Negation twice]
```

**Final answer: (¬p ∧ q) ∨ (p ∧ ¬r)**

*Grading:* 1 pt for correct outer De Morgan. 1 pt for correct inner De Morgans and Double Negation. Deduct 0.5 for each error in negation direction.

**(b)(i)** (1 pt) (p ∨ q) ∧ (¬p ∧ ¬q)

Note: ¬p ∧ ¬q ≡ ¬(p ∨ q) by De Morgan.

So this is (p ∨ q) ∧ ¬(p ∨ q) ≡ A ∧ ¬A ≡ **F**.

Classification: **Contradiction**

**(b)(ii)** (2 pts) (p → q) ∨ (q → p)

Using Conditional Equivalence:
= (¬p ∨ q) ∨ (¬q ∨ p)
= (¬p ∨ p) ∨ (q ∨ ¬q)     [Commutativity and Associativity]
= T ∨ T = **T**

Classification: **Tautology**

*Grading (b):* 1 pt each for correct classification. Full credit requires brief justification. "It looks like a tautology" with no work = 0.

---

### Grade Distribution (typical)

| Score Range | Interpretation |
|---|---|
| 18–20 | Mastered propositional logic |
| 14–17 | Solid; review conditional and De Morgan |
| 10–13 | Needs review of truth tables and laws |
| < 10 | Schedule office hours; re-read Lectures 0.1–0.3 |
