# MATH 151 · Discrete Mathematics for Computer Science
## Week 3 — Mathematical Induction: Weak and Strong

---

### Course Information

| Field | Detail |
|---|---|
| Course | MATH 151: Discrete Mathematics for Computer Science |
| Credits | 3 |
| Semester | Fall, Year 1 |
| Week | 3 of 12 |

---

### Week 3 Overview

Week 2 gave you three proof techniques for statements that hold at a fixed point or for all elements simultaneously. But many of the most important theorems in mathematics and computer science are about **sequences of claims** — one claim per natural number:

- "For all n ≥ 1, the sum 1 + 2 + … + n = n(n+1)/2"
- "For all n ≥ 0, 2ⁿ > n"
- "Every integer n ≥ 2 has a prime factorization"

These are universally quantified over ℕ, but there is no single algebraic manipulation that proves them for all n at once. The tool for such claims is **mathematical induction** — arguably the most important proof technique in computer science.

Induction is not a trick. It is the formal justification for recursion, for loop invariants, for the correctness of divide-and-conquer algorithms, and for the theory of recursive data structures. Every time you write a recursive function and argue it is correct, you are using induction.

**You will leave Week 3 able to:**
- Identify when a claim calls for an inductive proof
- Write complete weak induction proofs with a correct base case and inductive step
- State and apply the induction hypothesis with precision
- Recognize when strong induction is needed and apply it correctly
- Prove correctness of recursive definitions and algorithms by induction
- Identify and avoid the most common induction errors — especially circular reasoning and incorrect base cases

---

### Week 3 Contents

```
MATH151_Week3/
├── README.md
│
├── lectures/
│   ├── L09 Weak Induction.md            ← Lecture 9 (Monday 12 Oct)
│   ├── L10 Induction Applications.md    ← Lecture 10 (Thursday 15 Oct)
│   └── L11 Strong Induction.md          ← Lecture 11 (Friday 16 Oct)
│
├── assignments/
│   └── PS 3 Induction.md
│
├── lab/
│   └── LAB 3 Induction Workshop.md
│
├── quiz/
│   ├── QUIZ 3 Proof Techniques.md        ← Administered Monday (covers Week 2)
│   └── QUIZ 4 Preview.md
│
├── resources/
│   ├── Induction Template Reference.md
│   └── Common Summation Formulas.md
│
└── solutions_instructor/
    ├── QUIZ 3 Solutions.md
    ├── PS 3 Solutions.md
    └── LAB 3 Solutions.md
```

---

### Schedule at a Glance

| Day | Event | Topic |
|---|---|---|
| Monday 12 Oct, 13:00 | Quiz 3 (15 min) | Covers Week 2: direct proof, contrapositive, contradiction |
| Monday 12 Oct, 13:00 | Lecture 9 | Weak induction — principle, structure, summation formulas |
| Thursday 15 Oct, 13:00 | Lecture 10 | Induction applications — inequalities, divisibility, recursion |
| Friday 16 Oct, 13:00 | Lecture 11 | Strong induction — when and why, prime factorization, Fibonacci |
| Friday 16 Oct, 14:00 | PS 3 released | Due Friday 23 Oct, 17:00 |
| Wednesday 21 Oct, 15:00 (Week 4) | Lab 3 | Induction workshop: writing, debugging, and verifying proofs |

---

### Textbook Readings

| Text | Sections |
|---|---|
| Rosen, 8e | §5.1, §5.2, §5.3 |
| Epp, 5e | §5.1, §5.2, §5.3 |
| Levin, 3e | §2.1, §2.2 |

---

### The Connection Between Induction and Recursion

Induction and recursion are two sides of the same coin:

| Recursion | Induction |
|---|---|
| Define f(0) = base case | Prove P(0) = base case |
| Define f(n) in terms of f(n−1) | Prove P(n) assuming P(n−1) |
| Computes values for all n | Proves truth for all n |

A recursive function is correct precisely when the corresponding inductive proof goes through. This is why every CS student must master induction — it is the mathematical foundation of recursive programming.
