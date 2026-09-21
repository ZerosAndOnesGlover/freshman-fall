# MATH 151 · Discrete Mathematics for Computer Science
## Week 6 — Relations: Reflexive, Symmetric, Transitive; Equivalence Classes

---

### Course Information

| Field | Detail |
|---|---|
| Course | MATH 151: Discrete Mathematics for Computer Science |
| Credits | 3 |
| Semester | Fall, Year 1 |
| Week | 6 of 12 |

---

### Week 6 Overview

Week 5 studied functions — a special kind of relation where each input has exactly one output. This week studies **relations** in full generality: arbitrary subsets of $A \times B$, with no restriction on how many outputs an input may have.

Relations are the mathematical foundation of:
- **Databases** — a relational table IS a relation in the formal sense
- **Graphs** — a graph is a relation on the vertex set
- **Equivalence and equality** — every notion of "these two things are the same in some sense" is a relation with specific properties
- **Ordering** — "less than," "divides," "is a subset of" are all relations, and the ones with the right properties give you a coherent notion of order

This week develops the three fundamental properties a relation can have — **reflexive**, **symmetric**, **transitive** — and the two most important combinations: **equivalence relations** (which partition a set into classes) and **partial orders** (which structure a set hierarchically).

**You will leave Week 6 able to:**
- Formally define a relation and represent it as a set of pairs, a directed graph, or a matrix
- Test and prove whether a relation is reflexive, symmetric, antisymmetric, or transitive
- Prove that a given relation is an equivalence relation, and compute its equivalence classes
- Understand and apply the Fundamental Theorem of Equivalence Relations (relations ↔ partitions)
- Recognize partial orders and construct Hasse diagrams
- Connect relations directly to database theory, graph theory, and type systems

---

### Week 6 Contents

```
MATH151_Week6/
├── README.md
│
├── lectures/
│   ├── L18 Relations and Properties.md       ← Lecture 18 (Monday 2 Nov)
│   ├── L19 Equivalence Relations.md          ← Lecture 19 (Thursday 5 Nov)
│   └── L20 Partial Orders.md                 ← Lecture 20 (Friday 6 Nov)
│
├── assignments/
│   └── PS 6 Relations.md
│
├── lab/
│   └── LAB 6 Relations Workshop.md
│
├── quiz/
│   ├── QUIZ 6 Functions.md                    ← Administered Monday (covers Week 5)
│   └── QUIZ 7 Preview.md
│
├── resources/
│   ├── Relation Properties Reference.md
│   └── Hasse Diagram Reference.md
│
└── solutions_instructor/
    ├── QUIZ 6 Solutions.md
    ├── PS 6 Solutions.md
    └── LAB 6 Solutions.md
```

---

### Schedule at a Glance

| Day | Event | Topic |
|---|---|---|
| Monday 2 Nov, 13:00 | Quiz 6 (15 min) | Covers Week 5: functions, composition, inverses, cardinality |
| Monday 2 Nov, 13:00 | Lecture 18 | Relations, representations, reflexive/symmetric/antisymmetric/transitive |
| Thursday 5 Nov, 13:00 | Lecture 19 | Equivalence relations, equivalence classes, the Fundamental Theorem |
| Friday 6 Nov, 13:00 | Lecture 20 | Partial orders, Hasse diagrams, total orders, topological sort |
| Friday 6 Nov, 14:00 | PS 6 released | Due Friday 13 Nov, 17:00 |
| Wednesday 11 Nov, 15:00 (Week 7) | Lab 6 | Relations workshop: proofs, digraphs, Python relation checker |

---

### Textbook Readings

| Text | Sections |
|---|---|
| Rosen, 8e | §9.1, §9.5, §9.6 |
| Epp, 5e | §8.2, §8.3, §8.4 |
| Levin, 3e | §5.1, §5.2, §5.3 |

---

### Relations in Computer Science — A Preview

| Mathematical Concept | CS Application |
|---|---|
| Relation $R \subseteq A\times B$ | Database table; edge set of a graph |
| Reflexive | "≤" reflexivity; self-loops in graphs |
| Symmetric | Undirected graph edges; "is friends with" |
| Antisymmetric | Partial orders; "is a subtype of" |
| Transitive | Reachability; type inheritance chains |
| Equivalence relation | Equivalence classes = partitioning data (e.g., grouping by key) |
| Partial order | Dependency graphs; version compatibility; topological sort |
