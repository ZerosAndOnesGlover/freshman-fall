# MATH 141 · Calculus I
## Lab 10
### Substitution Pattern Recognition, Symmetry, and the Tabular Method for Integration by Parts

**Date:** Friday 4 December 2026 · 15:00–16:50 · Lab Section (Week 10) — covers Week 10 (Lectures 01–03)  
**Duration:** 2 hours | **Tools:** Desmos (its integral tool: type `int`), and the Lab 09 `midpoint_rule` in Python
**Expected time:** the session itself (6 questions), plus at most 30 minutes to tidy your answers
**Submission:** Written report due Monday 7 December 2026, 17:00 (Week 11)

> *Revised 2026-09-26.* Cut from five parts, about 20 questions and a reflection to 6 questions, in the week
> that also holds Midterm 2. Part 4 pointed to "Problem Set Part E2" for $\int x^2e^{-x}dx$, but PS 10 never
> asked that integral; the question is now self-contained. The "solve for $I$" check (Part 5) was removed.

---

## Lab Objectives

1. Spot the substitution in an integral quickly
2. Check a substitution result numerically and in Desmos
3. See symmetry cancel and double areas
4. Learn the tabular method for repeated integration by parts

---

## Part 1 — Substitution Pattern Recognition (15 min)

### Question 1 (15 points)

For each integral, **do not** solve it — just name the substitution $u=g(x)$ and check that $du$ (up to a
constant) appears in the integrand. Then fully solve any **two** of them.

| # | Integral | Your $u$ | Does $du$ appear? |
|---|----------|----------|-------------------|
| 1 | $\int x^4\sin(x^5)\,dx$ | | |
| 2 | $\int \dfrac{e^{\sqrt x}}{\sqrt x}\,dx$ | | |
| 3 | $\int \tan^5x\sec^2x\,dx$ | | |
| 4 | $\int \dfrac{x^2}{(x^3+1)^5}\,dx$ | | |
| 5 | $\int \cos x\, e^{\sin x}\,dx$ | | |
| 6 | $\int \dfrac{1}{x(\ln x)^3}\,dx$ | | |
| 7 | $\int \sqrt{\tan x}\sec^2x\,dx$ | | |
| 8 | $\int \dfrac{\arctan x}{1+x^2}\,dx$ | | |

---

## Part 2 — Checking a Substitution (20 min)

### Question 2 (20 points)

Evaluate $\displaystyle\int_0^2 x(x^2+1)^2\,dx$ by substitution, converting the limits. Then check it two ways:
`midpoint_rule(lambda x: x * (x**2 + 1)**2, 0, 2, 1000)` in Python, and Desmos's integral tool (type `int`,
then fill in the limits and integrand). Do all three agree to at least 3 decimal places?

---

## Part 3 — Symmetry (20 min)

### Question 3 (20 points)

**(a)** $f(x) = x^3 - 4x$. Show algebraically that $f$ is odd. In Desmos, compute $\int_{-3}^{0} f$ and $\int_{0}^{3} f$.
What is $\int_{-3}^{3} f$, and why could you have said so at once?

**(b)** $g(x) = x^4 - 5x^2 + 4$. Show that $g$ is even. In Desmos, compute $\int_0^{2.5} g$ and $\int_{-2.5}^{2.5} g$,
and check the second is exactly double the first.

---

## Part 4 — The Tabular Method (50 min)

When integration by parts must be applied several times, as in $\int x^3e^x\,dx$ or $\int x^2\cos x\,dx$, the
**tabular method** organizes the work. It is taught here, in the lab (Lecture 03 defers it to today).

### The Method

To integrate $\displaystyle\int P(x)\cdot f(x)\,dx$, where $P$ is a polynomial and $f$ is easy to integrate
repeatedly:

1. Make a two-column table. Left: $P(x)$ and its successive derivatives, down to $0$. Right: $f(x)$ and its
   successive antiderivatives, the same number of rows.
2. Give the rows alternating signs, starting with $+$: $+,-,+,-,\ldots$
3. Multiply diagonally (each row's left entry times the **next** row's right entry), apply that row's sign,
   and add up the products.

### Worked Example — $\int x^3e^x\,dx$

| Sign | $P(x)$ and derivatives | $f(x)$ and antiderivatives |
|------|--------------------------|------------------------------|
| $+$ | $x^3$ | $e^x$ |
| $-$ | $3x^2$ | $e^x$ |
| $+$ | $6x$ | $e^x$ |
| $-$ | $6$ | $e^x$ |
| $+$ | $0$ | $e^x$ |

$$\int x^3e^x\,dx = x^3e^x - 3x^2e^x+6xe^x-6e^x+C = e^x(x^3-3x^2+6x-6)+C$$

### Question 4 (10 points)

Differentiate the worked example's answer and confirm you get $x^3e^x$ back.

### Question 5 (15 points)

Use the tabular method to find $\displaystyle\int x^2\cos x\,dx$. Check your answer by differentiating.

### Question 6 (20 points)

Use the tabular method to find $\displaystyle\int x^2e^{-x}\,dx$, and check it by differentiating. Then explain why
the method works: connect the first two rows of your table to one use of $\int u\,dv = uv - \int v\,du$, and
say where the alternating signs come from.

---

## Lab Report Requirements

Include the Question 1 table with two worked integrals, your Python and Desmos checks for Question 2, the
Desmos values for Question 3, your three tables for Part 4, and answers to Questions 1–6.

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — Pattern recognition | 15 |
| Part 2 — Substitution checked | 20 |
| Part 3 — Symmetry | 20 |
| Part 4 — Tabular method | 45 |
| **Total** | **100** |
