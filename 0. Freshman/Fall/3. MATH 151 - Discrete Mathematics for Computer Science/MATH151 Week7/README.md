# MATH 151 · Discrete Mathematics for Computer Science
## Week 7 — Counting: Permutations, Combinations, and Counting Rules

---

### Course Information

| Field | Detail |
|---|---|
| Course | MATH 151: Discrete Mathematics for Computer Science |
| Credits | 3 |
| Semester | Fall, Year 1 |
| Week | 7 of 12 |

---

### Week 7 Overview

Weeks 0–6 built the language of logic, the technique of proof, and the structures of sets, functions, and relations. Week 7 turns to **counting** — the branch of discrete mathematics called **combinatorics**, which answers the deceptively simple question: *how many?*

Counting is not "just arithmetic." It requires identifying the right structure in a problem — is this a matter of order, or not? Are repeats allowed? Are we counting arrangements, selections, or distributions? Getting the classification right is the entire challenge; once classified correctly, the formulas are simple.

Counting underlies algorithm complexity analysis (how many operations, how many comparisons), probability theory (which requires counting favorable vs. total outcomes), cryptography (keyspace sizes), and the analysis of data structures (how many possible states, configurations, or trees).

**You will leave Week 7 able to:**
- Apply the Multiplication Rule and Addition Rule correctly, recognizing which applies
- Count permutations (ordered arrangements) with and without repetition
- Count combinations (unordered selections) and compute binomial coefficients
- Distinguish the four fundamental counting scenarios: permutations/combinations × with/without repetition
- Apply the Binomial Theorem and interpret Pascal's Triangle
- Solve multi-step counting problems by decomposing them into the correct sequence of rules

---

### Week 7 Contents

```
MATH151_Week7/
├── README.md
│
├── lectures/
│   ├── L21 Multiplication Addition Rules.md   ← Lecture 21 (Monday 9 Nov)
│   ├── L22 Permutations and Combinations.md   ← Lecture 22 (Thursday 12 Nov)
│   └── L23 Binomial Theorem.md                ← Lecture 23 (Friday 13 Nov)
│
├── assignments/
│   └── PS 7 Counting.md
│
├── lab/
│   └── LAB 7 Counting Workshop.md
│
├── quiz/
│   ├── QUIZ 7 Relations.md                     ← Administered Monday (covers Week 6)
│   └── QUIZ 8 Preview.md
│
├── resources/
│   ├── Counting Formulas Reference.md
│   └── Counting Decision Guide.md
│
└── solutions_instructor/
    ├── QUIZ 7 Solutions.md
    ├── PS 7 Solutions.md
    └── LAB 7 Solutions.md
```

---

### Schedule at a Glance

| Day | Event | Topic |
|---|---|---|
| Monday 9 Nov, 13:00 | Quiz 7 (15 min) | Covers Week 6: relations, equivalence relations, partial orders |
| Monday 9 Nov, 13:00 | Lecture 21 | Multiplication Rule, Addition Rule, basic counting arguments |
| Thursday 12 Nov, 13:00 | Lecture 22 | Permutations, combinations, the four counting scenarios |
| Friday 13 Nov, 13:00 | Lecture 23 | The Binomial Theorem, Pascal's Triangle, combinatorial identities |
| Friday 13 Nov, 14:00 | PS 7 released | Due Friday 20 Nov, 17:00 |
| Wednesday 18 Nov, 15:00 (Week 8) | Lab 7 | Counting workshop: problem classification, Python combinatorics |

---

### Textbook Readings

| Text | Sections |
|---|---|
| Rosen, 8e | §6.1, §6.3, §6.4 |
| Epp, 5e | §9.1, §9.2, §9.3, §9.5, §9.6, §9.7 |
| Levin, 3e | §1.1, §1.2, §1.3, §1.4 |

---

### Counting in Computer Science — A Preview

| Combinatorial Concept | CS Application |
|---|---|
| Multiplication Rule | Nested loops; total configuration space; brute-force search space size |
| Permutations | Password/key space analysis; sorting algorithm input space |
| Combinations | Subset selection; feature selection; hash table load analysis |
| Binomial coefficients | Dynamic programming (Pascal's Triangle recurrence); probability of exact outcomes |
| Pigeonhole (Week 8) + Counting | Complexity lower bounds; hash collision analysis |
