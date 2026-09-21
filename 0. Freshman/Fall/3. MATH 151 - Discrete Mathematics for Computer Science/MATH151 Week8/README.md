# MATH 151 · Discrete Mathematics for Computer Science
## Week 8 — Advanced Counting: Pigeonhole Principle, Inclusion–Exclusion

---

### Course Information

| Field | Detail |
|---|---|
| Course | MATH 151: Discrete Mathematics for Computer Science |
| Credits | 3 |
| Semester | Fall, Year 1 |
| Week | 8 of 12 |

---

### Week 8 Overview

Week 7 gave you the machinery for counting when everything is neatly separated: independent stages
multiply, disjoint cases add. This week handles the two situations that machinery cannot touch.

The first is **overlap**. The addition rule requires disjointness, and most real categories are not
disjoint — developers who use both Python and C, integers divisible by both 2 and 3. The **Principle
of Inclusion–Exclusion** repairs this with an alternating sum, and its most useful corollary is the
complement habit: when a problem says "at least one", count the opposite.

The second is a change of question. Everything so far has asked *how many*. The **Pigeonhole
Principle** answers *must there be one* — and it does so with almost no machinery at all. Its power
is inversely proportional to its difficulty: the statement is obvious, and the applications
(hash collisions, the impossibility of universal lossless compression, two subsets with equal sums)
are not.

The two are easy to confuse and answer opposite questions. Lecture 26 (Friday) is devoted to telling them
apart, because that choice — not the arithmetic — is where marks and real problems are lost.

**A note on existence versus search.** Friday's subset-sum argument proves two subsets must share a
sum, using three lines and no computation. *Finding* them is NP-complete. Hold that contrast; it is
one of the deepest facts in computer science and you meet it here first.

---

### Week 8 Contents

```
MATH151 Week8/
├── README.md
├── lectures/
│   ├── L24 Pigeonhole Principle.md            ← Lecture 24 (Monday 16 Nov)
│   ├── L25 Inclusion Exclusion.md             ← Lecture 25 (Thursday 19 Nov)
│   └── L26 Advanced Counting Applications.md  ← Lecture 26 (Friday 20 Nov)
├── assignments/
│   └── PS 8 Advanced Counting.md
├── lab/
│   └── LAB 8 Advanced Counting Workshop.md
├── quiz/
│   ├── QUIZ 8 Counting.md
│   └── QUIZ 9 Preview.md
├── resources/
│   ├── Pigeonhole Patterns Reference.md
│   └── Inclusion Exclusion Reference.md
└── solutions_instructor/
    ├── LAB 8 Solutions.md
    ├── PS 8 Solutions.md
    └── QUIZ 8 Solutions.md
```

---

### Learning Objectives

By the end of Week 8 you should be able to:

- State the Pigeonhole Principle and its generalised form, and prove both
- **Construct** the pigeonholes for a problem that does not hand them to you
- Apply inclusion–exclusion to two, three, and $n$ sets
- Use the complement rule, including when the complement is itself a union
- Count surjections and derangements, and explain why neither has a simple closed form
- Decide, from the wording of a problem, which technique applies
- Explain why an existence proof can be easy while the corresponding search is intractable

---

### Schedule at a Glance

| Day | Event | Topic |
|---|---|---|
| Monday 16 Nov, 13:00 | Quiz 8 (15 min) | Covers Week 7: multiplication/addition rules, permutations, combinations, binomial theorem |
| Monday 16 Nov, 13:00 | Lecture 24 | The Pigeonhole Principle, basic and generalised |
| Thursday 19 Nov, 13:00 | Lecture 25 | The Principle of Inclusion–Exclusion; surjections; derangements |
| Friday 20 Nov, 13:00 | Lecture 26 | Choosing the right tool; complement counting; constructed pigeonholes |
| Friday 20 Nov, 14:00 | PS 8 released | Due Friday 27 Nov, 17:00 |
| Wednesday 25 Nov, 15:00 (Week 9) | Lab 8 | Advanced counting workshop: both techniques, plus brute-force verification |

---

### Textbook Readings

| Text | Sections |
|---|---|
| Rosen, 8e | §6.2 (Pigeonhole), §8.5–§8.6 (Inclusion–Exclusion) |
| Epp, 5e | §9.4 (Pigeonhole), §9.3 (Inclusion–Exclusion) |
| Levin, 3e | §1.6 (Advanced counting) |

---

### Key Results

| | |
|---|---|
| Pigeonhole | $n$ items in $m$ containers, $n>m$ ⟹ some container holds $\ge 2$ |
| Generalised Pigeonhole | some container holds $\ge \lceil n/m \rceil$ |
| Inclusion–Exclusion | alternating sum over all $2^n-1$ non-empty subsets |
| Intersections in divisibility | use $\mathrm{lcm}$, never the product |
| Complement rule | "at least one" = total $-$ none |
| Surjections | $\sum_k(-1)^k\binom nk (n-k)^m$ |
| Derangements | $D_n = n!\sum_k \frac{(-1)^k}{k!}$; nearest integer to $n!/e$ |
| $D_n/n!$ | $\to 1/e \approx 0.368$, stable to 3 dp from $n=6$ |
| Exactly $k$ fixed points | $\binom nk D_{n-k}$ |

---

### Advanced Counting in Computer Science

| Mathematical Concept | CS Application |
|---|---|
| Pigeonhole | Hash collisions are guaranteed once keys exceed buckets |
| Pigeonhole | No lossless compressor shrinks every input — $2^n$ strings, $2^n-1$ shorter ones |
| Generalised Pigeonhole | Worst-case bucket load; lower bounds on data structure performance |
| Inclusion–Exclusion | Query selectivity estimation for `WHERE a OR b OR c` |
| Bonferroni truncation | Approximate cardinality when $2^n$ terms are unaffordable |
| Inclusion–Exclusion sieve | Euler's totient $\varphi(n)$ — returns in Week 12 for RSA |
| Derangements | Randomised assignment where nobody may keep their own item |
| Existence vs search | Subset-sum: the collision is trivially proved, NP-complete to find |

---

### Connections

**Back:** Week 7's multiplication and addition rules are the skeleton — this week supplies the organs
for when the addition rule's disjointness fails. The binomial theorem's identity
$\sum_k(-1)^k\binom nk = 0$ is exactly what makes inclusion–exclusion's signs work. Week 5's
surjections get counted here for the first time.

**Forward:** Week 9's recurrence relations offer a different route to many of these counts, and
derangements satisfy the elegant recurrence $D_n = (n-1)(D_{n-1} + D_{n-2})$. Week 12's number theory
uses inclusion–exclusion for the totient function.

**Sideways:** CS 101's hash tables assume collisions happen; this week proves they must. Its Week 11
computability material and Lecture 26 (Friday)'s existence-versus-search contrast are the same idea seen from
two directions.

---

*MATH 151 · Week 8 · © CSE Department*
