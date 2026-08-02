# MATH 151: Discrete Mathematics for Computer Science
## Week 4 — Sets: Operations, Power Sets, Cartesian Products

---

### Course Information

| Field | Detail |
|---|---|
| Course | MATH 151: Discrete Mathematics for Computer Science |
| Credits | 3 |
| Semester | Fall, Year 1 |
| Week | 4 of 12 |

---

### Week 4 Overview

Weeks 0–3 built the machinery of logic and proof. Week 4 begins the study of **discrete structures** — starting with the most fundamental one: the **set**.

Sets are the universal building material of mathematics. Every mathematical object — numbers, functions, relations, graphs, even logic itself — can be built from sets. In computer science, sets underlie data structures (hash sets, the relational model of databases), type theory (types as sets of values), and formal language theory (languages as sets of strings).

This week develops set theory rigorously: the operations that combine sets, the algebraic laws they obey, the power set (the set of all subsets), and the Cartesian product (the foundation of relations and functions, covered in Week 5).

**You will leave Week 4 able to:**
- State precise set-builder definitions and translate between set notation and predicate logic
- Compute unions, intersections, differences, complements, and symmetric differences
- Prove set identities using element-chasing arguments and using the algebra of sets
- Construct and reason about power sets, including their size
- Construct Cartesian products and understand their role in defining relations
- Apply the Principle of Inclusion-Exclusion to compute the size of unions

---

### Week 4 Contents

```
MATH151_Week4/
├── README.md
│
├── lectures/
│   ├── L12 Sets and Operations.md         ← Lecture 13 (Monday)
│   ├── L13 Set Identities and Proofs.md   ← Lecture 14 (Thursday)
│   └── L14 Power Sets and Products.md     ← Lecture 15 (Friday)
│
├── assignments/
│   └── PS 4 Sets.md
│
├── lab/
│   └── LAB 4 Set Workshop.md
│
├── quiz/
│   ├── QUIZ 4 Induction.md                 ← Administered Monday (covers Week 3)
│   └── QUIZ 5 Preview.md
│
├── resources/
│   ├── set_notation_reference.md
│   └── set_identities_reference.md
│
└── solutions_instructor/
    ├── QUIZ 4 Solutions.md
    ├── PS 4 Solutions.md
    └── LAB 4 Solutions.md
```

---

### Schedule at a Glance

| Day | Event | Topic |
|---|---|---|
| Monday | Quiz 4 (15 min) | Covers Week 3: weak and strong induction |
| Monday | Lecture 13 | Sets, set-builder notation, operations (∪, ∩, −, complement) |
| Thursday | Lecture 14 | Set identities, element-chasing proofs, algebra of sets |
| Wednesday | Lab 4 | Set workshop: proofs, Venn diagrams, Python set operations |
| Friday | Lecture 15 | Power sets, Cartesian products, Inclusion-Exclusion |
| Friday | PS 4 Released | Due Week 5 Friday |

---

### Textbook Readings

| Text | Sections |
|---|---|
| Rosen, 8e | §2.1, §2.2 |
| Epp, 5e | §6.1, §6.2, §6.3 |
| Levin, 3e | §1.6, §1.7 |

---

### Why Sets Matter for Computer Science

| Set Concept | CS Application |
|---|---|
| Set membership | Hash sets, `in` operator, database WHERE clauses |
| Union, intersection | SQL UNION, INTERSECT; set-based query optimization |
| Power set | Feature flag combinations; subset-sum and knapsack problems |
| Cartesian product | Relational database joins; the foundation of relations (Week 5) |
| Set cardinality | Counting problems; Inclusion-Exclusion in probability and combinatorics |
| Empty set | Base cases in recursive definitions; null/None handling |
