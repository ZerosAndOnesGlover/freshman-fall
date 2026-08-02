# MATH 151: Discrete Mathematics for Computer Science
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
│   ├── L21 Multiplication Addition Rules.md   ← Lecture 22 (Monday)
│   ├── L22 Permutations and Combinations.md   ← Lecture 23 (Thursday)
│   └── L23 Binomial Theorem.md                ← Lecture 24 (Friday)
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
│   ├── counting_formulas_reference.md
│   └── counting_decision_guide.md
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
| Monday | Quiz 7 (15 min) | Covers Week 6: relations, equivalence relations, partial orders |
| Monday | Lecture 22 | Multiplication Rule, Addition Rule, basic counting arguments |
| Thursday | Lecture 23 | Permutations, combinations, the four counting scenarios |
| Wednesday | Lab 7 | Counting workshop: problem classification, Python combinatorics |
| Friday | Lecture 24 | The Binomial Theorem, Pascal's Triangle, combinatorial identities |
| Friday | PS 7 Released | Due Week 8 Friday |

---

### Textbook Readings

| Text | Sections |
|---|---|
| Rosen, 8e | §6.1, §6.3, §6.4 |
| Epp, 5e | §9.1, §9.2, §9.3, §9.5 |
| Levin, 3e | §4.1, §4.2, §4.3 |

---

### Counting in Computer Science — A Preview

| Combinatorial Concept | CS Application |
|---|---|
| Multiplication Rule | Nested loops; total configuration space; brute-force search space size |
| Permutations | Password/key space analysis; sorting algorithm input space |
| Combinations | Subset selection; feature selection; hash table load analysis |
| Binomial coefficients | Dynamic programming (Pascal's Triangle recurrence); probability of exact outcomes |
| Pigeonhole (Week 8) + Counting | Complexity lower bounds; hash collision analysis |
