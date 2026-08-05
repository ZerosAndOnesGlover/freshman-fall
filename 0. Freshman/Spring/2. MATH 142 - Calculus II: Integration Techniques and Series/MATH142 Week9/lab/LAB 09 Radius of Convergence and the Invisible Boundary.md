# MATH 142 · Calculus II
## Lab 09: Radius of Convergence, and the Invisible Boundary
### Week 9 Lab Session

---

**Duration:** 2 hours
**Format:** Individual or pairs (pairs submit separate reports)
**Graded on:** completion + correctness — **100 points**
**Tools required:** Python 3 with `sympy` and `mpmath`

---

## Overview

A power series has a **sharp** boundary: it converges for $|x|<R$ and diverges for $|x|>R$, with nothing in between.

**This lab asks whether you could find that boundary by computing.** The answer is the one Lab 3 gave for improper integrals and Lab 7 gave for the harmonic series — **no** — and this time the failure is even starker, because the boundary is a single exact number that the Ratio Test produces in one line.

**Part D** then turns the theory to use: integrating a series term by term to obtain $\pi$, and measuring exactly how much the choice of evaluation point costs.

---

## Part A — Radii, Symbolically (20 pts)

**A1 (12 pts).** For each series, find the radius of convergence **by hand** using the Ratio Test, then confirm with `sympy` by computing $\lim\left|\frac{c_{n+1}}{c_n}\right|$.

| | Series |
|---|---|
| (i) | $\sum\dfrac{x^n}{n}$ |
| (ii) | $\sum\dfrac{x^n}{n!}$ |
| (iii) | $\sum n!\,x^n$ |
| (iv) | $\sum\dfrac{n^n}{n!}x^n$ |
| (v) | $\sum\dfrac{(3n)!}{(n!)^3}x^n$ |

**A2 (8 pts).** Two of the above have radii that are not "nice" numbers like 1, 0 or $\infty$.

Identify them, report the radii exactly, and say which **Week 6 limit** produces each.

---

## Part B — Can You See the Boundary? (30 pts)

Take $\displaystyle\sum_{n\ge1}\frac{x^n}{n}$, which has $R=1$.

**B1 (12 pts).** Compute the partial sum $s_{200}$ at

$$x = 0.9,\quad 0.99,\quad 1.0,\quad 1.01,\quad 1.1$$

Tabulate the results. **Mark which values of $x$ are inside the radius and which are outside.**

**B2 (10 pts).** Look at the three middle values ($0.99$, $1.0$, $1.01$).

- (a) Report the three partial sums.
- (b) **Which of these three converge and which diverge?**
- (c) Could you tell from the three numbers alone? Explain.

**B3 (8 pts).** Now compute $s_N$ at $x=1.01$ for $N = 200,\ 1000,\ 5000$.

At what point does the divergence become unmistakable? Comment on how this compares with $x=1.1$.

---

## Part C — The Cost of Being Near the Boundary (25 pts)

Inside the radius the series converges — but not equally fast everywhere.

**C1 (12 pts).** For $\sum\frac{x^n}{n}$, whose sum is $-\ln(1-x)$, find the number of terms $N$ needed for the partial sum to be within $10^{-10}$ of the true value, at

$$x = 0.5,\quad 0.9,\quad 0.99,\quad 0.999$$

Tabulate $x$, the true value, and $N$.

**C2 (8 pts).** The counts grow rapidly. **Show that $N$ behaves roughly like $\dfrac{C}{1-x}$** and estimate $C$ from your data.

*(Hint: the error after $N$ terms is roughly $\frac{x^{N}}{N(1-x)}$; the dominant factor is $x^N$, so $N\approx\frac{\ln(\text{tolerance})}{\ln x}$, and $\ln x\approx-(1-x)$ near 1.)*

**C3 (5 pts).** What happens at $x=1$ exactly? Relate your answer to the interval of convergence.

---

## Part D — Getting $\pi$ From a Series (25 pts)

Lecture 3 derived

$$\arctan x = \sum_{n=0}^\infty\frac{(-1)^nx^{2n+1}}{2n+1}$$

**D1 (8 pts).** Verify this against `sympy`'s expansion of $\arctan x$ to at least the $x^9$ term.

**D2 (9 pts).** Setting $x=1$ gives the Leibniz–Gregory series $\frac\pi4 = 1-\frac13+\frac15-\cdots$.

Compute the error $\left|\frac\pi4 - s_N\right|$ for $N=10,\ 100,\ 1000$, and confirm it is consistent with the **alternating series bound** $\frac{1}{2N+1}$ from Week 8.

**How many terms would 10 correct digits require?**

**D3 (8 pts).** Now use $x=\frac{1}{\sqrt3}$ instead, where

$$\arctan\frac{1}{\sqrt3} = \frac\pi6$$

Compute the number of terms needed for $10^{-10}$ accuracy at this $x$, and compare with your D2 answer.

**Explain the difference in terms of the radius of convergence**, referring to Part C.

---

## Part E — Reflection (Answer within Part D's allocation)

*No separate marks — but address this in your D3 discussion:*

Across Labs 3, 7 and 9, a finite computation has failed to locate a convergence boundary three times, in three different settings. **State the common reason in one sentence.**

---

## What to Submit

1. The radii, by hand and confirmed (Part A)
2. The boundary table and your answers to B2, B3 (Part B)
3. The term-count table and the $\frac{C}{1-x}$ estimate (Part C)
4. The $\arctan$ verification, both evaluation points, and the comparison (Part D)

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A | 20 | Radii by Ratio Test, including two unusual ones |
| B | 30 | The boundary is exact and numerically invisible |
| C | 25 | Cost of evaluating near the radius |
| D | 25 | Term-by-term integration, and where to evaluate |
| **Total** | **100** | |

---

*The Ratio Test locates the boundary exactly, in one line, for every series in Part A. Two hundred terms of arithmetic cannot locate it at all. That contrast is the lab.*
