# MATH 151 · Course Overview & Syllabus
## Discrete Mathematics for Computer Science

---

## Course Information

| | |
|---|---|
| **Credits** | 3 |
| **Meetings** | Mon/Wed/Fri, 50 minutes each |
| **Lab** | Wednesday 15:00–16:50. Lab N meets the Wednesday **after** Week N, so all three of the week's lectures come first (Lab 0: Wed 30 Sep 2026; Lab 12: Wed 23 Dec 2026) |
| **Semester** | Fall, Year 1 |
| **Prerequisites** | None |

---

## Course Description

Discrete mathematics is the mathematics of computer science. Unlike calculus — which deals with
continuous quantities — discrete mathematics studies objects that are finite or countably infinite:
integers, graphs, sets, sequences, proofs.

Every CS concept you will use has a discrete mathematics foundation. This course teaches you to think
like a mathematician: precisely, rigorously, and with **proof as the standard of truth**.

**What the course is really about.** Thirty-nine lectures across logic, proof, sets and functions,
counting, graphs and number theory look like five unrelated subjects. They are one subject: *how to
establish that something is true*. Induction proves universal claims; counterexamples refute them;
pigeonhole establishes existence; bijections establish equal size; invariants establish difference.
Each technique discharges that obligation for a different kind of claim.

---

## Required Textbooks

**1. Rosen, K. — Discrete Mathematics and Its Applications, 8th ed.** *(McGraw-Hill, 2018)*
The standard reference. Comprehensive and well-organised.

**2. Epp, S. — Discrete Mathematics with Applications, 5th ed.** *(Cengage, 2019)*
Clearer prose, more accessible proofs. An excellent complement to Rosen.

**3. Levin, O. — Discrete Mathematics: An Open Introduction, 3rd ed.**
Free at `discrete.openmathbooks.org`. Focused and excellent.

---

## Assessment Breakdown

| Component | Weight | Details |
|-----------|--------|---------|
| **Problem Sets (13)** | 40% | PS 0–12, released Friday 14:00, due the following Friday at 17:00 (PS 12: Wednesday 23 December 2026, 17:00). Each worth 100 points. **Lowest 1 dropped.** |
| **Weekly Quizzes (12)** | 15% | Quiz 1–12, first 15 minutes of Monday's lecture (13:00–13:15; 28 September – 14 December 2026). Each worth 20 points. Quiz *N* covers Week *N−1*. **Lowest 1 dropped.** |
| **Lab Sections (13)** | 15% | Lab 0–12, Wednesdays 15:00–16:50, each one week after its material. Graded on **completion** against the checkoff criteria, not on points. |
| **Final Exam** | 30% | Monday 21 December 2026, 08:00 (registry slot 08:00–10:00 — *the registry allows 120 minutes, not 3 hours; one of the two must change*). Comprehensive. One double-sided A4 sheet of handwritten notes. |

**Total:** 100%

> **A note on these weights.** The Year 1 curriculum document specifies this course's topics,
> textbooks and credit hours, but **not its assessment breakdown**. The division above is set by the
> department and is the one the Academic Registry gradebook implements. If the curriculum document
> is later revised to specify weights, that revision governs.

**Grading scale:** this course uses the **university-wide 13-band scale** defined in
[[UNIVERSITY POLICIES]] (Academic Registry) — A+ 97–100, A 93–96, A− 90–92, B+ 87–89, B 83–86,
B− 80–82, C+ 77–79, C 73–76, C− 70–72, D+ 67–69, D 63–66, D− 60–62, F below 60. The registry copy
governs if the two ever differ.

**Credit hours:** 3

---

## Weekly Schedule

| Week | Topic | Assessments |
|------|-------|-------------|
| 0 | Logic: propositions, connectives, truth tables, tautologies | PS 0, Lab 0 |
| 1 | Predicate logic, quantifiers, logical equivalences | PS 1, Lab 1, Quiz 1 |
| 2 | Proof techniques: direct, contradiction, contrapositive | PS 2, Lab 2, Quiz 2 |
| 3 | Proof by induction: weak and strong | PS 3, Lab 3, Quiz 3 |
| 4 | Sets: operations, power sets, Cartesian products | PS 4, Lab 4, Quiz 4 |
| 5 | Functions: injective, surjective, bijective; composition, inverse | PS 5, Lab 5, Quiz 5 |
| 6 | Relations: reflexive, symmetric, transitive; equivalence classes | PS 6, Lab 6, Quiz 6 |
| 7 | Counting: permutations, combinations, the multiplication rule | PS 7, Lab 7, Quiz 7 |
| 8 | Advanced counting: pigeonhole principle, inclusion–exclusion | PS 8, Lab 8, Quiz 8 |
| 9 | Recurrence relations and generating functions | PS 9, Lab 9, Quiz 9 |
| 10 | Graphs: terminology, representations, paths, connectivity | PS 10, Lab 10, Quiz 10 |
| 11 | Trees, spanning trees, graph algorithms (BFS/DFS) | PS 11, Lab 11, Quiz 11 |
| 12 | Number theory: divisibility, primes, modular arithmetic; review | PS 12, Lab 12, Quiz 12, **Final** |

**Lecture numbering.** Lectures are numbered continuously **L00–L38**, three per week: Week *N* owns
`L(3N)` through `L(3N+2)`. Week overviews refer to them 1-indexed as "Lecture 1"–"Lecture 39", so
prose "Lecture *k*" is file `L(k−1)`.

---

## Problem Set Policy

- **Released:** Friday after lecture
- **Due:** The following Friday at 23:59
- **Late policy:** 20% per day, nothing accepted after 3 days
- **Lowest grade dropped**
- **Format:** a single PDF; handwritten is fine if legible

## Lab Policy

Labs meet Wednesday 15:00–16:50 and are graded on **completion**: your TA signs off the checkoff
criteria printed at the end of each lab sheet. Work in pairs, but both partners submit.

Labs use Python 3 with **no external libraries**. Implementing the algorithms yourself is the point —
it is what makes the cost analysis concrete.

---

## Collaboration Policy

**Problem sets:** discuss approaches freely; all written work must be your own. If you cannot explain
a proof to a TA, you have not learned it.

**Labs:** collaboration encouraged.

**Exams:** no collaboration.

**AI tools:** using AI to generate submitted work is academic dishonesty. You may use it to *explain*
a concept. A course whose entire subject is *how to know something is true* is poorly served by
outsourcing the knowing.

---

## Why This Course Matters

This is the most directly useful mathematics course in Year 1.

Mathematical induction is how we prove recursive algorithms correct. Graph theory is the foundation
of networking, compilers, and social analysis. Modular arithmetic is the basis of cryptography — you
will implement RSA from nothing in Week 12. Set theory is the mathematical foundation of databases.
Logic is the foundation of circuit design, type systems, and formal verification.

But the most valuable thing here is not any single technique. It is the judgement to look at a
problem and estimate whether it is **easy or hard** — Euler circuits versus Hamilton cycles,
minimum spanning trees versus travelling salesman, multiplying primes versus factoring their product.
Those pairs look alike and differ by the whole distance between tractable and intractable.

**A proof that something cannot be done is worth as much as an algorithm, and it is cheaper.**

---

*MATH 151 · Course Overview & Syllabus · © CSE Department*
