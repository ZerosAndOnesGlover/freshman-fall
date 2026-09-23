# MATH 142 · Calculus II
## Problem Set 9
### Topic: Power Series; Radius and Interval of Convergence
**Released:** Friday 26 March 2027, 12:00 · Week 9 (after Friday's Lecture 3)
**Due:** Friday 2 April 2027, 17:00 · Week 10 — late penalty from 17:01

---

> **"Find the interval of convergence" means: find $R$, then test BOTH endpoints, then report an
> interval with the correct brackets.** Stopping at the radius answers a different question and
> earns partial marks at best.
>
> **Solve $|x-a|<R$ explicitly.** Do not quote an interval centred at 0 for a series centred elsewhere.
>
> **At an endpoint, name the test you use.** It will be one of Weeks 7–8; the Ratio Test is
> guaranteed to be silent there.

---

## Part A — Radius of Convergence (5 pts each)

**A1.** $\displaystyle\sum_{n=1}^{\infty}\frac{n\,x^n}{3^n}$

**A2.** $\displaystyle\sum_{n=0}^{\infty}\frac{x^n}{(n!)^2}$

**A3.** $\displaystyle\sum_{n=0}^{\infty}\frac{(3n)!}{(n!)^3}\,x^n$

**A4.** $\displaystyle\sum_{n=1}^{\infty}\frac{x^{3n}}{n\,5^n}$

*Missing terms. Apply the Ratio Test to the terms as written, powers included.*

---

## Part B — Interval of Convergence (6 pts each)

*For each: find $R$, state the open interval, test **both** endpoints, and report the interval.*

**B1.** $\displaystyle\sum_{n=1}^{\infty}\frac{x^n}{\sqrt n}$

**B2.** $\displaystyle\sum_{n=1}^{\infty}\frac{(x-2)^n}{n\,3^n}$

**B3.** $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^n(x+1)^n}{n^2}$

**B4.** $\displaystyle\sum_{n=0}^{\infty}n!\,(x-1)^n$

**B5.** $\displaystyle\sum_{n=1}^{\infty}\frac{(2x-1)^n}{n}$

*Rewrite $2x-1$ in the form $2(x-a)$ first, and be careful what the radius is **in $x$**.*

---

## Part C — Building and Manipulating Series (6 pts each)

*For each, give the series in $\sum$ notation and state its radius.*

**C1.** $\dfrac{1}{1+3x}$

**C2.** $\dfrac{x}{1-x^2}$

**C3.** $\ln(1-x)$

*Obtain it by integrating a geometric series. Then determine its interval of convergence, including both endpoints, and compare with the interval for $\ln(1+x)$.*

**C4.** Find a closed form for $\displaystyle\sum_{n=1}^{\infty}n^2x^n$ on $|x|<1$.

*Start from $\sum nx^n = \frac{x}{(1-x)^2}$ and differentiate again.*

**C5.** Find a power series for $\displaystyle\int_0^x\frac{dt}{1+t^4}$, and state its radius.

*The integrand has an elementary antiderivative, but a very unpleasant one. The series takes two lines.*

---

## Part D — Concept (10 pts each)

**D1.** *(Why endpoints need separate work.)*

- (a) Show that applying the Ratio Test to $\sum c_n(x-a)^n$ at $|x-a|=R$ gives $L=1$, **whatever the coefficients are.** Hence explain why the test can never decide an endpoint.
- (b) Give four series, all with $R=1$ and centre 0, whose intervals are $(-1,1)$, $[-1,1)$, $(-1,1]$ and $[-1,1]$. Justify each endpoint.
- (c) What does (b) show about the relationship between the radius and the interval?

**D2.** *(Term-by-term operations.)*

- (a) State the theorem permitting term-by-term differentiation and integration of a power series, including what happens to the radius.
- (b) **Which property established in Lecture 1 §7 licenses these operations, and why is it needed?** Refer to the relevant Week 8 result.
- (c) Starting from $\frac{1}{1+t}=\sum(-1)^nt^n$, derive the series for $\ln(1+x)$ by integration. Then determine both endpoints of the new series and compare with the endpoints of the original.
- (d) Hence explain the sentence: *"integration tends to gain endpoints, differentiation tends to lose them."*

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Radius, including missing terms |
| B (5 × 6) | 30 | Full intervals, both endpoints, shifted centres |
| C (5 × 6) | 30 | Building series by substitution, differentiation, integration |
| D (2 × 10) | 20 | Why endpoints are separate; what licenses term-by-term work |
| **Total** | **100** | |

---

## Before You Submit

1. **Every Part B answer is an interval**, not a radius, with correct brackets.
2. **Every endpoint test is named.**
3. **Check B2, B3, B5 for the centre** — none of them is 0.
4. **Check A4 and B5** — in both, applying the coefficient formula blindly gives the wrong radius.

---

*MATH 142 · Week 9 · Problem Set 9*
