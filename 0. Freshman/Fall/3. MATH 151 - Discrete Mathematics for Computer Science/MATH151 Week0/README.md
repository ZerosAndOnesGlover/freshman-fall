# MATH 151 Discrete Mathematics for Computer Science
## Week 0 Logic: Propositions, Connectives, Truth Tables, Tautologies

---

### Course Information

| Field | Detail |
|---|---|
| Course | MATH 151: Discrete Mathematics for Computer Science |
| Credits | 3 |
| Semester | Fall, Year 1 |
| Prerequisites | None |
| Week | 0 of 12 |

---

### Week 0 Overview

Week 0 introduces the **formal language of mathematics**: propositional logic. Before you can prove anything (about algorithms, data structures, or programs) you must have a precise vocabulary for making and combining claims. This week gives you that vocabulary from first principles.

**You will leave Week 0 able to:**
- Translate English statements into formal logical notation
- Compute truth values for arbitrarily complex compound propositions
- Recognize tautologies, contradictions, and contingencies
- Prove logical equivalences without truth tables (using laws)
- Connect propositional logic to Boolean circuit design (ECE 110) and `if` statements in code

---

### Week 0 Contents

```
MATH151_Week0/
├── README.md                         ← You are here
│
├── lectures/
│   ├── L00 Propositions and Connectives.md     ← Lecture 1 (Monday)
│   ├── L01 Truth Tables.md                     ← Lecture 2 (Thursday)
│   └── L02 Tautologies and Logical Laws.md     ← Lecture 3 (Friday)
│
├── assignments/
│   └── PS 0 Propositional Logic.md              ← Problem Set 0 (released Friday, due Week 1 Friday)
│
├── lab/
│   └── LAB 0 Truth Table Explorer.md            ← Lab instructions + exercises
│
├── quiz/
│   └── QUIZ 1 Preview.md                        ← Preview of Quiz 1 scope (held Week 1 Monday)
│
├── resources/
│   ├── notation_reference.md                   ← Symbol cheat sheet
│   └── logic_laws_reference.md                 ← All standard equivalences in one place
│
└── solutions_instructor/
    ├── PS 0 Solutions.md                         ← Full worked solutions (instructor only)
    └── LAB 0 Solutions.md                        ← Lab solution guide (instructor only)
```

---

### Schedule at a Glance

| Day       | Event         | Topic                                                                  |
| --------- | ------------- | ---------------------------------------------------------------------- |
| Monday    | Lecture 1     | Propositions, logical connectives, negation, conjunction, disjunction  |
| Thursday  | Lecture 2     | Conditional, biconditional, complete truth tables, operator precedence |
| Wednesday | Lab 0         | Truth table computation, logical translation exercises                 |
| Friday    | Lecture 3     | Tautologies, contradictions, logical equivalence, the standard laws    |
| Friday    | PS 0 Released | Full problem set, due next Friday                                      |

---

### Textbook Readings

| Text | Sections |
|---|---|
| Rosen — *Discrete Mathematics and Its Applications*, 8e | §1.1, §1.3 |
| Epp — *Discrete Mathematics with Applications*, 5e | §2.1, §2.2 |
| Levin — *Discrete Mathematics: An Open Introduction*, 3e | §0.2 (free at discrete.openmathbooks.org) |

---

### Connection to CS

Propositional logic is not abstract philosophy, it is the mathematical foundation of:

- **Boolean circuits** (ECE 110): AND/OR/NOT gates compute exactly the logical connectives you study here
- **Conditional statements in code**: `if (A && !B || C)` is a logical formula — its truth table determines program behavior
- **Type systems and formal verification**: program correctness proofs are written in logic
- **Database queries**: `WHERE age > 18 AND (city = 'Lagos' OR city = 'Abuja')` is propositional logic
- **SAT solvers**: industrial tools that check satisfiability of logical formulas with millions of variables
