# MATH 141 · Calculus I
## Problem Set 8
### Topic: Riemann Sums, the Definite Integral, and Its Properties
**Released:** Wednesday 18 November 2026, 12:00 (after Lecture 03) · Week 8
**Due:** Wednesday 25 November 2026, 11:00 (start of class) · Week 9 — late penalty after 11:00

**Total:** 100 points

---

## Part A — Sigma Notation and Riemann Sums (25 pts)

**A1.** *(6)* Evaluate using summation formulas:
- (a) $\displaystyle\sum_{i=1}^{8}(4i-3)$
- (b) $\displaystyle\sum_{i=1}^{5}(i^2+2i)$
- (c) $\displaystyle\sum_{i=1}^{n} \frac{2i}{n}$ — express your answer in terms of $n$ only

**A2.** *(6)* Estimate $\displaystyle\int_0^2 (x^2+1)\,dx$ using $n=4$ subintervals with:
- (a) Right endpoints ($R_4$) &nbsp; (b) Left endpoints ($L_4$) &nbsp; (c) Midpoints ($M_4$)

The exact value is $\tfrac{14}{3}$. Rank your three estimates by accuracy and explain the ordering
from the shape of the graph.

**A3.** *(7)* Set up the right-endpoint Riemann sum $R_n$ for $f(x) = 2x+1$ on $[1,3]$ as an explicit
function of $n$ (simplify $\Delta x$ and $x_i$, substitute, and use summation formulas to reach a
closed form). Then compute $\displaystyle\lim_{n\to\infty}R_n$ and verify it matches the geometric
(trapezoid) area.

**A4.** *(6)* A particle has velocity $v(t) = 2t+3$ (m/s) for $t\in[0,4]$. Estimate the distance
travelled using a midpoint sum with $n=4$. Then compute the exact area under the velocity graph
geometrically. Your two answers will agree exactly — explain why that is guaranteed here and not in
general.

---

## Part B — Properties of the Definite Integral (25 pts)

**B1.** *(7)* Evaluate using geometric area formulas only — no Riemann sums, no antiderivatives:
- (a) $\displaystyle\int_{-2}^{5} 4\,dx$
- (b) $\displaystyle\int_0^6 \left|x-3\right|dx$ *(sketch the region — it is two triangles)*
- (c) $\displaystyle\int_{-3}^{3}\sqrt{9-x^2}\,dx$

**B2.** *(6)* Given $\displaystyle\int_1^3 f = 4$, $\displaystyle\int_3^6 f = -2$,
$\displaystyle\int_1^6 g = 7$, find:
- (a) $\displaystyle\int_1^6 f$ &nbsp; (b) $\displaystyle\int_6^1 f$ &nbsp;
  (c) $\displaystyle\int_1^6 [3f-2g]$ &nbsp; (d) $\displaystyle\int_3^3 f$

**B3.** *(6)* Use the comparison property to find upper and lower bounds for
$\displaystyle\int_0^2 \frac{dx}{1+x^3}$ (find the maximum and minimum of the integrand on $[0,2]$
first). Comment on how tight your bounds are.

**B4.** *(6)* Find the average value of $f(x) = 3x^2 - 2$ on $[0,3]$. Then find every $c \in [0,3]$
guaranteed by the Mean Value Theorem for Integrals.

---

## Part C — Exact Areas from the Definition (20 pts)

**C1.** *(10)* Compute $\displaystyle\int_0^1 x^3\,dx$ **entirely from the definition** — set up $R_n$,
apply the summation formula $\sum i^3 = \left[\tfrac{n(n+1)}{2}\right]^2$, simplify, and take the
limit. Show every step.

**C2.** *(5)* Evaluate $R_{10}$, $R_{1000}$ and $R_{100000}$ for the sum in C1 and tabulate them
against the exact value. At what rate does the error shrink?

**C3.** *(5)* Explain why $R_n$, $L_n$ and $M_n$ all converge to the **same** number for a continuous
$f$, and why that fact is required for the definition of $\int_a^b f$ to make sense at all.

---

## Part D — Conceptual and Proof (30 pts)

**D1.** *(8)* State the definition of $\displaystyle\int_a^b f(x)\,dx$ as a limit of Riemann sums, and
explain what each of $\Delta x$, $x_i^*$, and the limit contributes. Why must the sample point
$x_i^*$ be *arbitrary* in the subinterval rather than fixed at an endpoint?

**D2.** *(8)* Explain what $\displaystyle\int_a^b f$ measures when $f$ is negative on part of
$[a,b]$. Give an explicit $f$ and interval for which the integral is $0$ but the region has positive
geometric area.

**D3.** *(7)* Explain why $\displaystyle\int_b^a f = -\int_a^b f$ is a **definition** rather than a
theorem, and what would break if we declined to adopt it.

**D4.** *(7)* Prove: if $f$ is an odd function continuous on $[-a,a]$, then
$\displaystyle\int_{-a}^{a}f(x)\,dx=0$. *(Split at $0$ and argue that odd symmetry makes the two
signed areas cancel; a Riemann-sum or geometric argument is expected here. Week 10's substitution
rule gives a slicker proof — you may revisit it then.)*

---

## Grading Summary

| Part | Points | Focus |
|------|--------|-------|
| A (4 problems) | 25 | Sigma notation, Riemann sums |
| B (4 problems) | 25 | Properties, comparison, average value |
| C (3 problems) | 20 | Exact area from the definition |
| D (4 problems) | 30 | Conceptual and proof |
| **Total** | **100** | |

> **The FTC is not on this problem set.** It arrives in Week 9, and Problem Set 9 is where you will
> evaluate integrals by antidifferentiation. Everything here is deliberately done the hard way —
> by sums, by geometry, or by bounds — because that is the only way to see what the FTC later
> spares you.

---

*MATH 141 · Week 8 · Problem Set 8 · © CSE Department*
