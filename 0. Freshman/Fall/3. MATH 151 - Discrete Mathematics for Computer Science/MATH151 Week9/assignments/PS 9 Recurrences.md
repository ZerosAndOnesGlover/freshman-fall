# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 9: Recurrence Relations and Generating Functions
### Released: Friday 27 November 2026, 14:00 (after the Friday lecture) | Due: Friday 4 December 2026, 17:00 (Week 10)

---

> *Revised 2026-09-21.* The optional bonus section was removed to keep the set to 100 points of
> this week's material.

**Instructions:**
- Every closed form must be **checked against at least three iterated values**. Show the check.
- State initial conditions explicitly whenever you write a recurrence.
- Show all work. Submit as a single PDF.

**Scoring:** 100 points total.

---

## Part A — Modelling with Recurrences (24 points)

**A1.** *(6 pts)* Write a recurrence with initial conditions for the number of length-$n$ bit strings
containing **no two consecutive 1s**. Compute the first six values and identify the sequence.

**A2.** *(6 pts)* A country issues 3¢ and 5¢ stamps. Write a recurrence for the number of ways to
make $n$ cents when **order matters**, state the initial conditions carefully, and compute the first
eight values.

**A3.** *(6 pts)* Write and solve, by iteration, the recurrence for the number of regions a plane is
divided into by $n$ lines in general position (no two parallel, no three concurrent).

**A4.** *(6 pts)* Classify each by order, linearity, whether the coefficients are constant, and
whether it is homogeneous:

(a) $a_n = 3a_{n-1} - a_{n-3}$ &nbsp;&nbsp; (b) $a_n = n\,a_{n-1}$ &nbsp;&nbsp;
(c) $a_n = a_{n-1}^2$ &nbsp;&nbsp; (d) $a_n = a_{n-1} + a_{n-2} + n^2$

---

## Part B — Solving by Iteration (16 points)

**B1.** *(5 pts)* Solve $a_n = a_{n-1} + n$, $a_0 = 0$, by unrolling. Identify the resulting sequence
and prove your closed form by induction.

**B2.** *(5 pts)* Solve $T_n = 2T_{n-1}+1$ with $T_0 = 1$ (note: **not** $T_0 = 0$). How does the
closed form differ from the Tower of Hanoi solution, and why?

**B3.** *(6 pts)* Solve $a_n = 3a_{n-1} + 2$, $a_0 = 4$, by iteration, then verify with the
characteristic-equation method.

---

## Part C — The Characteristic Equation (30 points)

**C1.** *(6 pts)* Solve $a_n = 7a_{n-1} - 12a_{n-2}$, $a_0 = 2$, $a_1 = 5$.

**C2.** *(6 pts)* Solve $a_n = 4a_{n-1} - 4a_{n-2}$, $a_0 = 1$, $a_1 = 6$. State which case applies
and why.

**C3.** *(6 pts)* Solve $a_n = a_{n-1} + 2a_{n-2}$, $a_0 = 2$, $a_1 = 7$.

**C4.** *(6 pts)* Use Binet's formula to compute $F_{20}$ exactly. Then explain why $F_n$ is the
nearest integer to $\varphi^n/\sqrt5$ for $n \ge 1$.

**C5.** *(6 pts)* Solve the non-homogeneous $a_n = 3a_{n-1} + 2^n$, $a_0 = 1$. State why the
particular guess $C\,2^n$ is legitimate here.

---

## Part D — Generating Functions (30 points)

**D1.** *(5 pts)* Write the first six coefficients of $\dfrac{1}{1-3x}$ and identify the sequence.

**D2.** *(6 pts)* Derive the generating function for $a_n = a_{n-1} + 2a_{n-2}$, $a_0 = 2$,
$a_1 = 7$. Expand it to six terms and confirm the coefficients match your answer to C3.

**D3.** *(7 pts)* Write the generating function for making $n$ cents from 1¢, 2¢, and 5¢ coins.
Find the coefficient of $x^{10}$ and **verify it by listing every combination**.

**D4.** *(6 pts)* Write the generating function for selecting $n$ objects from four types using **at
most 3 of each type**, and compute the coefficient of $x^5$.

**D5.** *(6 pts)* Explain what "formal power series" means and why convergence is irrelevant to
everything done in this part. Give one operation that is legitimate on formal series.

---

## Grading

| Part | Topic | Points |
|---|---|---|
| A | Modelling with recurrences | 24 |
| B | Solving by iteration | 16 |
| C | The characteristic equation | 30 |
| D | Generating functions | 30 |
| **Total** | | **100** |
