# MATH 141 · Calculus I
## Problem Set 8
### Topic: Riemann Sums, the Definite Integral, and Its Properties
**Released:** Wednesday 18 November 2026, 12:00 (after Lecture 03) · Week 8
**Due:** Wednesday 25 November 2026, 11:00 (start of class) · Week 9 — late penalty after 11:00
**Expected time:** about 3 hours — 8 problems, 10 parts
**Total:** 100 points

*(Revised 2026-09-26: cut from 15 problems and about 27 parts to 8 problems and 10 parts, to fit about
three hours. Dropped: the second sigma sum, the midpoint velocity sum, the property arithmetic, the
$R_n$ table (Lab 08 builds the same table), the convergence and definition essays, the orientation
convention and the odd-function proof.)*

---

## Problem 1: Sigma Notation (8 points)

Evaluate using summation formulas. *(4 pts each)*

**(a)** $\displaystyle\sum_{i=1}^{8}(4i-3)$

**(b)** $\displaystyle\sum_{i=1}^{n} \frac{2i}{n}$ — express your answer in terms of $n$ only

---

## Problem 2: Left, Right and Midpoint Sums (14 points)

Estimate $\displaystyle\int_0^2 (x^2+1)\,dx$ using $n=4$ subintervals with right endpoints ($R_4$), left
endpoints ($L_4$) and midpoints ($M_4$). The exact value is $\tfrac{14}{3}$. Rank your three estimates by
accuracy and explain the ordering from the shape of the graph.

---

## Problem 3: A Riemann Sum in Closed Form (14 points)

Set up the right-endpoint Riemann sum $R_n$ for $f(x) = 2x+1$ on $[1,3]$ as an explicit function of $n$
(simplify $\Delta x$ and $x_i$, substitute, and use summation formulas to reach a closed form). Then compute
$\displaystyle\lim_{n\to\infty}R_n$ and check it against the geometric (trapezoid) area.

---

## Problem 4: Integrals from Geometry (14 points)

Evaluate using area formulas only — no Riemann sums. *(7 pts each)*

**(a)** $\displaystyle\int_0^6 \left|x-3\right|dx$ *(sketch the region — it is two triangles)*

**(b)** $\displaystyle\int_{-3}^{3}\sqrt{9-x^2}\,dx$

---

## Problem 5: Bounding an Integral (12 points)

Use the comparison property to find upper and lower bounds for $\displaystyle\int_0^2 \frac{dx}{1+x^3}$.
First show the integrand is monotone on $[0,2]$ and find its maximum and minimum there. Comment on how
tight your bounds are.

---

## Problem 6: Average Value (12 points)

Find the average value of $f(x) = 2x + 1$ on $[0,4]$, computing the integral from geometry. Then find every
$c \in [0,4]$ guaranteed by the Mean Value Theorem for Integrals.

---

## Problem 7: An Exact Area from the Definition (16 points)

Compute $\displaystyle\int_0^1 x^3\,dx$ **entirely from the definition**: set up $R_n$, apply the summation
formula $\sum i^3 = \left[\tfrac{n(n+1)}{2}\right]^2$, simplify, and take the limit. Show every step.

---

## Problem 8: Signed Area (10 points)

Explain what $\displaystyle\int_a^b f$ measures when $f$ is negative on part of $[a,b]$. Give an explicit $f$
and interval for which the integral is $0$ but the region has positive geometric area.

---

> **The FTC is not on this problem set.** It arrives in Week 9, and Problem Set 9 is where you will
> evaluate integrals by antidifferentiation. Everything here is deliberately done the hard way —
> by sums, by geometry, or by bounds — because that is the only way to see what the FTC later
> spares you.

---

*MATH 141 · Week 8 · Problem Set 8 · © CSE Department*
