# MATH 142 · Calculus II
## Lab 00: Numerical Integration and the Error of a Rule
### Week 0 Lab Session

**Date:** Wednesday 27 January 2027 · 15:00–16:50 · Lab section (Week 1) — covers Week 0 (Lectures 1–3)

---

**Duration:** 2 hours
**Format:** Individual or pairs (pairs submit separate reports)
**Graded on:** completion + correctness — **100 points**, counts toward the 10% lab component
**Tools required:** Python 3 (no external packages needed for Parts A–D)

---

## Overview

Lecture 1 said the integral is a limit of Riemann sums, and that this is not merely a definition but **an algorithm** — the one a computer actually runs, because a machine cannot find an antiderivative.

This lab makes that concrete on an integral that *has* no elementary antiderivative:

$$\int_0^1 e^{-x^2}\,dx$$

You will implement three rules, measure how wrong each one is, and **discover the rate at which each converges** rather than being told it.

**The central question of the lab:** if you double the work, how much better does the answer get? That question — cost against accuracy — is the whole of numerical analysis, and it recurs in Week 10 when a Taylor series gives you a third way to compute this same number.

---

## The Exact Value

There is no elementary antiderivative, but the integral has a name:

$$\int_0^1 e^{-x^2}\,dx = \frac{\sqrt\pi}{2}\operatorname{erf}(1) = 0.746824132812427025\ldots$$

**Use this as ground truth.** Note what has happened: $\operatorname{erf}$ is *defined* as this integral, so naming it is not solving it. But the value is computable to any precision, and that is what we need.

---

## Setup

```python
import math

def f(x):
    return math.exp(-x*x)

EXACT = 0.7468241328124270254   # sqrt(pi)/2 * erf(1)
a, b = 0.0, 1.0
```

---

## Part A — Implement the Three Rules (25 pts)

Each rule splits $[a,b]$ into $n$ subintervals of width $h=\frac{b-a}{n}$.

**A1 (8 pts) — Trapezoid Rule.** Approximate each strip by a trapezoid:

$$T_n = h\left[\frac{f(x_0)}{2} + f(x_1) + f(x_2) + \cdots + f(x_{n-1}) + \frac{f(x_n)}{2}\right]$$

**A2 (8 pts) — Midpoint Rule.** Use a rectangle whose height is the value at the strip's centre:

$$M_n = h\sum_{i=0}^{n-1} f\!\left(a + \left(i+\tfrac12\right)h\right)$$

**A3 (9 pts) — Simpson's Rule.** Fit a parabola through each *pair* of strips ($n$ must be even):

$$S_n = \frac{h}{3}\Big[f(x_0) + 4f(x_1) + 2f(x_2) + 4f(x_3) + \cdots + 4f(x_{n-1}) + f(x_n)\Big]$$

*The coefficients alternate 4, 2, 4, 2, …, with 1 at each end. Getting this pattern right is most of the marks.*

**Verify each function** on the four integrals $\int_0^1 x^k\,dx = \tfrac{1}{k+1}$ for $k=1,2,3,4$, using $n=4$. Tabulate the error of each rule on each.

You should find that **all three rules are exact on $x$**, that Simpson remains exact on $x^2$ and $x^3$, and that **Simpson first shows an error at $x^4$**. Report your table and answer:

- (a) Why is every rule exact on a linear function?
- (b) Simpson's rule is built by fitting **parabolas**. Explain why it is nevertheless exact on the *cubic* $x^3$ — this is not an accident, and it is the reason Simpson's order is 4 rather than 3.

---

## Part B — Measure the Error (25 pts)

**B1 (15 pts).** For each rule and each $n \in \{2, 4, 8, 16, 32, 64, 128, 256\}$, compute the approximation and the **absolute error** $|{\text{approx}} - \text{EXACT}|$. Produce a table.

**B2 (10 pts).** For each rule, add a column giving the **ratio of consecutive errors**:

$$r_n = \frac{\text{error at } n}{\text{error at } 2n}$$

*This ratio is the entire point of the lab. Do not skip it.*

---

## Part C — Determine the Order (25 pts)

A method has **order $p$** if its error behaves like $E \approx Ch^p$ for small $h$. Doubling $n$ halves $h$, so

$$\frac{E(h)}{E(h/2)} \approx \frac{Ch^p}{C(h/2)^p} = 2^p$$

**The error ratio tells you the order directly.**

**C1 (9 pts).** From your ratios, state the order $p$ of each of the three rules. Justify each from your numbers, not from the textbook.

**C2 (8 pts).** For Simpson's rule, look at the ratio at **small $n$** and compare it with the ratio at **large $n$**. They are not the same. Explain what "the error behaves like $Ch^p$" actually claims, and why the claim is only visible for large $n$.

*This is the most important question in the lab. An asymptotic statement is a statement about a limit, and a limit says nothing about any particular $n$.*

**C3 (8 pts).** Suppose you need 10 correct decimal places.

- (a) Using your measured order and one of your data points, estimate the $n$ each rule would need.
- (b) Simpson costs about the same per point as the trapezoid rule. Given your answer to (a), quantify how much work Simpson saves.
- (c) Would you ever prefer the trapezoid rule? Give one circumstance.

---

## Part D — The Sign of the Error (15 pts)

So far you have used absolute errors. Now keep the sign.

**D1 (7 pts).** Tabulate the **signed** errors $T_n - \text{EXACT}$ and $M_n - \text{EXACT}$ for $n \in \{4, 16, 64, 256\}$. Which rule overestimates and which underestimates?

**D2 (8 pts).** Compute the ratio $\dfrac{T_n - \text{EXACT}}{M_n - \text{EXACT}}$ for each $n$. It converges to a specific simple number — report it.

Then explain geometrically why the two errors have opposite signs, using the concavity of $f$.

> **A warning about the textbook rule.** You may have met "the trapezoid rule overestimates for a concave-up function". Compute $f''(x)$ for $f(x)=e^{-x^2}$ and find where it changes sign. **The concavity is not constant on $[0,1]$.** Explain how your observed sign is consistent with this — which part of the interval wins, and why. A rule stated for constant concavity needs care when concavity varies.

---

## Part E — Reflection (10 pts)

**E1 (5 pts).** This lab computed a definite integral that has no elementary antiderivative, to many digits, without ever finding an antiderivative. In two or three sentences, say what this tells you about the relationship between *evaluating* an integral and *solving* it symbolically.

**E2 (5 pts).** The **midpoint rule** is literally a Riemann sum in the sense of Lecture 1 — a sum of $f(x_i^*)\Delta x$ with a particular choice of sample point.

**Simpson's rule is not.** Write out $S_n$ and identify what makes it different: what would the "$\Delta x$" attached to each sample point have to be, and why does that disqualify it? Say in one sentence what Simpson's rule is doing instead of sampling.

---

## What to Submit

A single document containing:

1. Your three implementations (Part A) and the verification on $x$ and $x^2$
2. The error table with ratios (Part B)
3. Your stated orders with justification (Part C)
4. The signed-error table and the concavity discussion (Part D)
5. Your answers to Part E

**Report the numbers you actually got.** If a ratio does not match what you expected, say so and investigate — a surprising measurement is a finding, not a mistake to hide. Marks are for measuring and interpreting honestly, not for matching a number in the back of a book.

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A | 25 | Correct implementation of all three rules |
| B | 25 | Error table and consecutive ratios |
| C | 25 | Empirical determination of order; asymptotics |
| D | 15 | Signed error, and concavity done carefully |
| E | 10 | Interpretation |
| **Total** | **100** | |

---

*Lab 00 is graded. It is also the easiest 100 points in the course — every answer is something you can compute and check yourself.*
