# MATH 151: Discrete Mathematics for Computer Science
## Week 9 — Recurrence Relations and Generating Functions

---

### Course Information

| Field | Detail |
|---|---|
| Course | MATH 151: Discrete Mathematics for Computer Science |
| Credits | 3 |
| Semester | Fall, Year 1 |
| Week | 9 of 12 |

---

### Week 9 Overview

Week 3 taught induction: prove a statement for $n$ by reducing to $n-1$. This week runs the same
machinery forwards — **define** a value for $n$ in terms of $n-1$ — and then asks the question
induction never does: *what is the answer in closed form?*

Monday is about **modelling**. Writing $T_n = 2T_{n-1}+1$ for the Tower of Hanoi is the hard part;
solving it is mechanical. Most of the marks in this material go to students who can turn a word
problem into a recurrence, so that is where the lecture spends its time.

Wednesday gives the **characteristic equation** — a complete method for linear, constant-coefficient,
homogeneous recurrences. It produces Binet's formula for Fibonacci, which is worth meeting once in
your life: every Fibonacci number is an integer, and the formula that generates them is built
entirely out of $\sqrt5$.

Friday introduces **generating functions**, which encode an entire sequence as the coefficients of a
single function. The technique looks like a party trick until you see that multiplying generating
functions models independent choice — at which point counting problems that need delicate case
analysis become routine algebra.

**A discipline for the week:** every closed form here is checked against iterated values. Deriving a
formula and verifying it numerically are different skills, and the second one catches the sign errors
that reading over your own work never will.

---

### Week 9 Contents

```
MATH151 Week9/
├── README.md
├── lectures/
│   ├── L27 Recurrence Relations.md          ← Lecture 28 (Monday)
│   ├── L28 Solving Linear Recurrences.md    ← Lecture 29 (Wednesday)
│   └── L29 Generating Functions.md          ← Lecture 30 (Friday)
├── assignments/
│   └── PS 9 Recurrences.md
├── lab/
│   └── LAB 9 Recurrence Workshop.md
├── quiz/
│   ├── QUIZ 9 Advanced Counting.md
│   └── QUIZ 10 Preview.md
├── resources/
│   ├── Recurrence Solving Reference.md
│   └── Generating Functions Reference.md
└── solutions_instructor/
    ├── LAB 9 Solutions.md
    ├── PS 9 Solutions.md
    └── QUIZ 9 Solutions.md
```

---

### Learning Objectives

By the end of Week 9 you should be able to:

- Model a counting or process problem as a recurrence **with correct initial conditions**
- Classify a recurrence by order, linearity, constant coefficients, and homogeneity
- Solve by iteration and prove the result by induction
- Apply the characteristic equation, handling distinct roots, repeated roots, and non-homogeneous terms
- Derive and use Binet's formula, and explain why $F_n$ is the nearest integer to $\varphi^n/\sqrt5$
- Derive the generating function of a recurrence and recover its coefficients
- Use products of generating functions to model independent choices and restrictions
- Verify every closed form numerically before trusting it

---

### Schedule at a Glance

| Day | Event | Topic |
|---|---|---|
| Monday | Quiz 9 (15 min) | Covers Week 8: Pigeonhole and Inclusion–Exclusion |
| Monday | Lecture 28 | Modelling with recurrences; solving by iteration |
| Wednesday | Lecture 29 | The characteristic equation; Binet's formula; non-homogeneous terms |
| Wednesday | Lab 9 | Recurrence workshop: model, solve, verify numerically |
| Friday | Lecture 30 | Generating functions; convolution and counting |
| Friday | PS 9 Released | Due Week 10 Friday |

---

### Textbook Readings

| Text | Sections |
|---|---|
| Rosen, 8e | §8.1 (Applications), §8.2 (Solving), §8.4 (Generating functions) |
| Epp, 5e | §5.6 (Recursive definitions), §5.8 (Second-order recurrences) |
| Levin, 3e | §2.4 (Solving recurrences), §5.1 (Generating functions) |

---

### Key Results

| | |
|---|---|
| Recurrence needs | the relation **and** initial conditions |
| Tower of Hanoi | $T_n = 2^n-1$ |
| Distinct roots $r_1\ne r_2$ | $a_n = Ar_1^n + Br_2^n$ |
| Double root $r$ | $a_n = (A+Bn)r^n$ |
| Non-homogeneous | homogeneous $+$ particular; fit the particular **first** |
| Binet | $F_n = (\varphi^n-\psi^n)/\sqrt5$, $\varphi = \frac{1+\sqrt5}{2}$ |
| $F_n$ for $n\ge1$ | nearest integer to $\varphi^n/\sqrt5$ — but fails in float64 from $n=71$ |
| Generating function | $G(x)=\sum a_nx^n$; formal, never evaluated |
| Fibonacci GF | $x/(1-x-x^2)$ — the reversed characteristic polynomial |
| Multiplication | convolves coefficients ⟹ models independent choice |
| Naive Fibonacci calls | $2F_{n+1}-1$; $2{,}692{,}537$ at $n=30$ |

---

### Recurrences in Computer Science

| Mathematical Concept | CS Application |
|---|---|
| Recurrence relation | The running time of every recursive algorithm |
| Solving by iteration | Deriving $\Theta(n\log n)$ for merge sort |
| Exponential recurrences | Why naive Fibonacci is unusable and memoisation is not optional |
| Evaluating a recurrence bottom-up | Dynamic programming, in its entirety |
| Generating functions | Average-case analysis: quicksort comparisons, random BST depth |
| Convolution of coefficients | Polynomial multiplication; the FFT computes it in $\Theta(n\log n)$ |
| Catalan numbers | Counting binary trees, balanced brackets, parse trees |

---

### Connections

**Back:** Week 3's induction is this week's method of proof — unrolling shows a pattern, induction
establishes it. Week 8's derangements satisfy both $D_n = (n-1)(D_{n-1}+D_{n-2})$ and
$D_n = nD_{n-1}+(-1)^n$, giving a second route to the same numbers. Week 7's binomial coefficients
reappear as generating-function coefficients.

**Forward:** Week 10's graph algorithms are analysed with recurrences. In CS 102, every divide-and-conquer
running time is a recurrence, and dynamic programming is nothing more than evaluating one in a
sensible order.

**Sideways:** CS 101's recursion week defines functions by self-reference; this week gives you the
tools to say how expensive that is.

---

*MATH 151 · Week 9 · © CSE Department*
