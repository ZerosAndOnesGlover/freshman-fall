# MATH 151 · Discrete Mathematics for Computer Science
## Week 5 — Functions: Injective, Surjective, Bijective; Composition, Inverse

---

### Course Information

| Field | Detail |
|---|---|
| Course | MATH 151: Discrete Mathematics for Computer Science |
| Credits | 3 |
| Semester | Fall, Year 1 |
| Week | 5 of 12 |

---

### Week 5 Overview

Week 4 built the Cartesian product $A \times B$ — the set of all ordered pairs. This week specializes that construction to the single most important mathematical object in all of computer science: the **function**.

A function is not "a formula" or "a piece of code that returns a value" — it is a precise mathematical object: a special kind of relation. Understanding functions formally, as subsets of $A \times B$ satisfying specific properties, is what lets you prove things about hash functions, encryption schemes, compiler transformations, and every recursive definition you have ever written.

This week formalizes:
- What a function actually *is*, set-theoretically
- **Injective** (one-to-one), **surjective** (onto), and **bijective** functions — and how to prove or disprove each property
- **Composition** of functions — building new functions from old ones
- **Inverse functions** — precisely when they exist, and why
- **Bijections and cardinality** — what it means for two sets to be "the same size", and why that idea survives into the infinite

**You will leave Week 5 able to:**
- State the formal definition of a function as a special relation
- Prove a function is injective, surjective, or bijective using the quantifier techniques from Week 1
- Disprove these properties with explicit counterexamples
- Compute and reason about function composition, including proving composition properties
- Determine precisely when a function has an inverse, and construct that inverse
- Use bijections to prove two finite sets have equal size, and state what changes for infinite sets

---

### Week 5 Contents

```
MATH151_Week5/
├── README.md
│
├── lectures/
│   ├── L15 Functions and Properties.md      ← Lecture 16 (Monday)
│   ├── L16 Composition and Inverses.md      ← Lecture 17 (Thursday)
│   └── L17 Bijections and Cardinality.md    ← Lecture 18 (Friday)
│
├── assignments/
│   └── PS 5 Functions.md
│
├── lab/
│   └── LAB 5 Function Workshop.md
│
├── quiz/
│   ├── QUIZ 5 Sets.md                        ← Administered Monday (covers Week 4)
│   └── QUIZ 6 Preview.md
│
├── resources/
│   ├── Function Properties Reference.md
│   └── Cardinality Reference.md
│
└── solutions_instructor/
    ├── QUIZ 5 Solutions.md
    ├── PS 5 Solutions.md
    └── LAB 5 Solutions.md
```

---

### Schedule at a Glance

| Day | Event | Topic |
|---|---|---|
| Monday | Quiz 5 (15 min) | Covers Week 4: sets, identities, power sets, products |
| Monday | Lecture 16 | Functions as relations; injective, surjective, bijective |
| Thursday | Lecture 17 | Composition of functions; inverse functions |
| Wednesday | Lab 5 | Function workshop: proofs, composition, Python function analysis |
| Friday | Lecture 18 | Bijections, cardinality, and counting with functions |
| Friday | PS 5 Released | Due Week 6 Friday |

---

### Textbook Readings

| Text | Sections |
|---|---|
| Rosen, 8e | §2.3, §2.5 (Cardinality) |
| Epp, 5e | §7.1, §7.2, §7.3, §7.4 (Cardinality) |
| Levin, 3e | §1.8, §1.9 |

---

### Functions in Computer Science — A Preview

| Mathematical Concept | CS Application |
|---|---|
| Function $f: A \to B$ | Any deterministic computation from input type to output type |
| Injective function | Hash functions with no collisions (ideal); encryption (must be invertible) |
| Surjective function | Every possible output is achievable — coverage/completeness |
| Bijective function | Perfect hashing; lossless encoding; invertible transformations |
| Composition $g \circ f$ | Function pipelines; the Unix pipe; chained transformations |
| Inverse function | Decryption; decompression; undo operations |
| Bijection | Perfect hashing; lossless encoding; a proof that two datasets have equal size without counting either |
