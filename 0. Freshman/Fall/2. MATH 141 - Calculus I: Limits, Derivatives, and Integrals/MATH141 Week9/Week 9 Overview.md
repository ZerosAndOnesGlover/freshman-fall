# MATH 141 · Week 9 Overview
## The Fundamental Theorem of Calculus

---

## This Week

Week 8 defined the definite integral as a limit of Riemann sums — correct, and almost unusable.
This week we prove that **differentiation and integration are inverse operations**, which turns an
intractable limit into an antiderivative evaluated twice.

| Day | Lecture | Topic |
|---|---|---|
| Monday 23 Nov | 1 | The Fundamental Theorem, Part 1 |
| Tuesday 24 Nov | 2 | FTC Part 2 and Evaluation |
| Wednesday 25 Nov | 3 | Accumulation and Functions Defined by Integrals |
| Friday 27 Nov, 15:00 | Lab 09 | Accumulation Functions and the FTC Numerically |

**Quiz 09** at the start of Monday 23 November 2026's lecture (11:00), covering Week 8.
**Problem Set 9** released Wednesday 25 November 2026, 12:00; due Wednesday 2 December 2026, 11:00 (Week 10).

---

## Learning Objectives

1. State both parts of the FTC with their hypotheses
2. Differentiate $\int_a^x f(t)\,dt$, including with variable limits and the chain rule
3. Evaluate definite integrals by antidifferentiation
4. Distinguish **displacement** from **total distance**
5. Explain why $\int_0^x e^{-t^2}dt$ defines a perfectly good function with no elementary formula
6. State and apply the Mean Value Theorem for Integrals

---

## Key Results

| | |
|---|---|
| **FTC 1** | $f$ continuous ⟹ $\dfrac{d}{dx}\displaystyle\int_a^x f(t)\,dt = f(x)$ |
| **FTC 2** | $F'=f$ on $[a,b]$ ⟹ $\displaystyle\int_a^b f = F(b)-F(a)$ |
| Chain rule form | $\dfrac{d}{dx}\displaystyle\int_{u(x)}^{v(x)}f = f(v)v' - f(u)u'$ |
| Displacement | $\displaystyle\int_a^b v\,dt$ |
| Total distance | $\displaystyle\int_a^b \lvert v\rvert\,dt$ |
| Average value | $\dfrac{1}{b-a}\displaystyle\int_a^b f$ |
| **MVT for integrals** | Some $c$ with $f(c) = $ the average value |

---

## Common Errors

| Error | Correction |
|---|---|
| $\frac{d}{dx}\int_a^{x^2}f = f(x^2)$ | Missing the chain factor $2x$ |
| Reporting displacement as distance | Split at the sign changes and integrate $\lvert v\rvert$ |
| Applying FTC 2 across a discontinuity | $\int_{-1}^{1}\frac{dx}{x^2}$ is **not** $-2$ |
| "No elementary antiderivative" ⟹ "no antiderivative" | FTC 1 constructs one for every continuous $f$ |
| Dropping $dt$ vs $dx$ | The variable of integration is bound; the limit variable is free |

---

## Connections

**Back:** FTC 1's proof runs on the **MVT for Integrals**, established in Week 8 — not on Week 6's MVT, which is a statement about derivatives and would be circular here.
Week 8's properties — additivity, orientation, bounds — are the tools of that proof.

**Forward:** Week 10 makes antidifferentiation practical (substitution, parts). Week 11 applies it to
areas and volumes. In CS 101 and MATH 341, `cumsum` and the trapezoid rule are FTC 1 in discrete
form; every ODE solver is FTC 2 run backwards.

---

*MATH 141 · Week 9 · © CSE Department*
