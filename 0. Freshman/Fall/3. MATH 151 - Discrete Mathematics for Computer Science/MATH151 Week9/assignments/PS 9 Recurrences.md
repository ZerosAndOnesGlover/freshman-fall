# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 9: Recurrence Relations and Generating Functions
### Released: Friday 27 November 2026, 14:00 (after the Friday lecture) | Due: Friday 4 December 2026, 17:00 (Week 10)

---

**Instructions:**
- Every closed form must be **checked against at least three iterated values**. Show the check.
- State initial conditions explicitly whenever you write a recurrence.
- Show all work. Submit as a single PDF.

**Expected time:** about 3 hours. **Scoring:** 100 points total.

---

## Part A — Classifying Recurrences (12 points)

**A1.** *(3 pts each)* Classify each by order, linearity, whether the coefficients are constant, and
whether it is homogeneous:

(a) $a_n = 3a_{n-1} - a_{n-3}$ &nbsp;&nbsp; (b) $a_n = n\,a_{n-1}$ &nbsp;&nbsp;
(c) $a_n = a_{n-1}^2$ &nbsp;&nbsp; (d) $a_n = a_{n-1} + a_{n-2} + n^2$

---

## Part B — Solving by Iteration (24 points)

**B1.** *(12 pts)* Solve $a_n = a_{n-1} + n$, $a_0 = 0$, by unrolling. Identify the resulting sequence
and prove your closed form by induction.

**B2.** *(12 pts)* Solve $T_n = 2T_{n-1}+1$ with $T_0 = 1$ (note: **not** $T_0 = 0$). How does the
closed form differ from the Tower of Hanoi solution, and why?

---

## Part C — The Characteristic Equation (28 points)

**C1.** *(12 pts)* Solve $a_n = a_{n-1} + 2a_{n-2}$, $a_0 = 2$, $a_1 = 7$.

**C2.** *(16 pts)* Solve the non-homogeneous $a_n = 3a_{n-1} + 2^n$, $a_0 = 1$. State why the
particular guess $C\,2^n$ is legitimate here.

---

## Part D — Generating Functions (36 points)

**D1.** *(8 pts)* Write the first six coefficients of $\dfrac{1}{1-3x}$ and identify the sequence.

**D2.** *(16 pts)* Derive the generating function for $a_n = a_{n-1} + 2a_{n-2}$, $a_0 = 2$,
$a_1 = 7$. Expand it to six terms and confirm the coefficients match your answer to C1.

**D3.** *(12 pts)* Explain what "formal power series" means and why convergence is irrelevant to
everything done in this part. Give one operation that is legitimate on formal series.

---

## Grading

| Part | Topic | Points |
|---|---|---|
| A | Classifying recurrences | 12 |
| B | Solving by iteration | 24 |
| C | The characteristic equation | 28 |
| D | Generating functions | 36 |
| **Total** | | **100** |
