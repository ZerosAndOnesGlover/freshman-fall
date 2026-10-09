# MATH 151 · Discrete Mathematics for Computer Science
## Week 2 — Proof Techniques: Direct Proof, Contradiction, Contrapositive

---

### Course Information

| Field | Detail |
|---|---|
| Course | MATH 151: Discrete Mathematics for Computer Science |
| Credits | 3 |
| Semester | Fall, Year 1 |
| Week | 2 of 12 |

---

### Week 2 Overview

Weeks 0 and 1 built the *language* of mathematics — propositional logic and predicate logic. Week 2 begins the *practice* of mathematics: **proof**.

A proof is a finite sequence of logically valid steps that establishes the truth of a claim beyond all doubt. Not "very likely true," not "true in all cases I tested," not "intuitively obvious" — but *necessarily* true, with every step justified by a rule of inference or a previously established fact.

This week introduces the three most fundamental proof strategies:

- **Direct proof** — assume the hypothesis, derive the conclusion by a chain of valid steps
- **Proof by contrapositive** — prove ¬Q → ¬P instead of P → Q, using their logical equivalence
- **Proof by contradiction** — assume the negation of what you want to prove, derive a contradiction, conclude the original must be true

These three techniques — together with induction (Week 3) — are sufficient to prove nearly everything in undergraduate mathematics.

**You will leave Week 2 able to:**
- Read a mathematical claim and identify which proof strategy is most natural
- Write direct proofs of statements about integers, divisibility, and parity
- Write proofs by contrapositive when the hypothesis is weak and the negation of the conclusion is strong
- Write proofs by contradiction for existence claims and irrationality results
- Recognize and avoid the most common proof errors: assuming the conclusion, circular reasoning, incomplete case analysis
- Write proofs in correct mathematical prose — not pseudocode, not bullet points

---

### Week 2 Contents

```
MATH151_Week2/
├── README.md
│
├── lectures/
│   ├── L06 Direct Proof.md              ← Lecture 6 (Monday 5 Oct)
│   ├── L07 Proof by Contrapositive.md   ← Lecture 7 (Thursday 8 Oct)
│   └── L08 Proof by Contradiction.md    ← Lecture 8 (Friday 9 Oct)
│
├── assignments/
│   └── PS 2 Proof Techniques.md
│
├── lab/
│   └── LAB 2 Proof Workshop.md
│
├── quiz/
│   ├── QUIZ 2 Predicate Logic.md         ← Administered Monday (covers Week 1)
│   └── QUIZ 3 Preview.md
│
├── resources/
│   ├── Proof Writing Guide.md
│   └── Proof Strategies Reference.md
│
└── solutions_instructor/
    ├── QUIZ 2 Solutions.md
    ├── PS 2 Solutions.md
    └── LAB 2 Solutions.md
```

---

### Schedule at a Glance

| Day | Event | Topic |
|---|---|---|
| Monday 5 Oct, 13:00 | Quiz 2 (15 min) | Covers Week 1: predicate logic, quantifiers, negation |
| Monday 5 Oct, 13:00 | Lecture 6 | Direct proof — definitions, even/odd, divisibility |
| Thursday 8 Oct, 13:00 | Lecture 7 | Proof by contrapositive — when and how |
| Friday 9 Oct, 13:00 | Lecture 8 | Proof by contradiction — irrationality, infinitude of primes |
| Friday 9 Oct, 14:00 | PS 2 released | Due Friday 16 Oct, 17:00 |
| Wednesday 14 Oct, 15:00 (Week 3) | Lab 2 | Proof workshop: writing, critiquing, fixing proofs |

---

### Textbook Readings

| Text | Sections |
|---|---|
| Rosen, 8e | §1.7, §1.8 |
| Epp, 5e | §4.1, §4.2, §4.7, §4.8 |
| Levin, 3e | §3.2 |

---

### The Logical Structure of a Proof

Every theorem has the form **P → Q**: given hypotheses P, conclude Q. The three techniques differ in *which* implication they actually prove:

| Technique | What you prove | Logical basis |
|---|---|---|
| Direct | P → Q | Directly |
| Contrapositive | ¬Q → ¬P | Equivalent to P → Q |
| Contradiction | ¬(P→Q) → contradiction | Shows ¬(P→Q) is false, so P→Q is true |

All three establish the same result — P → Q — by different routes.
