# MATH 142 · Calculus II
## Problem Set 10
### Topic: Taylor and Maclaurin Series; Remainders; Applications
**Released:** Friday 2 April 2027, 12:00 · Week 10 (after Friday's Lecture 3)
**Due:** Friday 9 April 2027, 17:00 · Week 11 — late penalty from 17:01

---

> **Manipulate, do not differentiate.** Every series in Part A comes from substituting into or
> multiplying a standard one. Computing $f^{(8)}(0)$ by hand is not a method.
>
> **State the radius** for every series you produce.
>
> **For every error bound, say which bound you used** — Lagrange or the alternating estimate — and
> over what interval it holds.

---

## Part A — Building Series (5 pts each)

*Give the general term in $\sum$ notation and state the radius.*

**A1.** Maclaurin series for $e^{3x}$.

**A2.** Maclaurin series for $x^2\sin x$.

**A3.** Maclaurin series for $\dfrac{1}{1+x^3}$.

**A4.** Taylor series for $\ln x$ **centred at $a=1$**.

*Either differentiate directly, or write $\ln x = \ln(1+(x-1))$ and use the standard series.*

---

## Part B — Remainders and Error Bounds (6 pts each)

**B1.** Let $P_3$ be the degree-3 Maclaurin polynomial for $e^x$.

- (a) Write $P_3$.
- (b) Use the Lagrange remainder to bound $|R_3(x)|$ for $x\in[0,1]$. **State the $M$ you used and why it is valid on that interval.**
- (c) Compute the actual error at $x=1$ and compare.

**B2.** How many terms of the Maclaurin series for $\cos x$ guarantee $|R_n(0.3)|<10^{-8}$?

*Give the degree $n$, and then say how many **nonzero** terms that is.*

**B3.** Use the binomial series to write the degree-3 Maclaurin polynomial for $\sqrt{1+x}$, and use it to estimate $\sqrt{1.1}$. Compare with the true value.

**B4.** Estimate $\sin(0.2)$ using terms up to $x^3$, and bound the error using the **alternating series estimate**. Compare the bound with the true error.

**B5.** Let $f(x)=e^{-1/x^2}$ for $x\ne0$ and $f(0)=0.

- (a) Compute $f(0.5)$, $f(0.2)$, $f(0.1)$ and in each case the ratio $\dfrac{f(x)}{x^{10}}$.
- (b) What do your numbers suggest about $\lim_{x\to0}\dfrac{f(x)}{x^k}$ for a fixed $k$?
- (c) Given that every derivative of $f$ at 0 is zero, write down the Maclaurin series of $f$ and state where it converges and to what.
- (d) **Explain why this does not contradict Taylor's theorem.**

---

## Part C — Applications (6 pts each)

**C1.** $\displaystyle\lim_{x\to0}\frac{e^x-1-x-\frac{x^2}{2}}{x^3}$, by series.

**C2.** Find a series for $\displaystyle\int_0^{1/2}e^{-x^2}dx$ and compute it to four terms.

**Bound the error** using the alternating estimate.

**C3.** Find a series for $\displaystyle\int_0^1\frac{1-\cos x}{x^2}\,dx$ and evaluate it to four terms.

*Note that the integrand is not defined at $x=0$; explain why the series is nevertheless well behaved there.*

**C4.** Use the binomial series for $(1+x)^{1/3}$ to estimate $\sqrt[3]{1.03}$ to three terms, and compare with the true value.

**C5.** Let $f(x)=x^2e^{x^3}$. Find $f^{(8)}(0)$ **without differentiating**.

*Hint: find the coefficient of $x^8$ in the Maclaurin series and use $c_n = \frac{f^{(n)}(0)}{n!}$.*

---

## Part D — Concept (10 pts each)

**D1.** *(Does the series equal the function?)*

- (a) State Taylor's theorem with the Lagrange remainder.
- (b) State precisely the condition under which $f$ equals its Taylor series on an interval.
- (c) Prove that $\sin x$ equals its Maclaurin series **for every real $x$**, using the remainder bound and a Week 6 fact.
- (d) Explain how the function in B5 is consistent with (b) — i.e. which quantity fails to tend to zero.

**D2.** *(Week 0's debt.)* The course opened by observing that $e^{-x^2}$ has no elementary antiderivative.

- (a) Derive the series for $\int_0^1 e^{-x^2}dx$.
- (b) Determine how many terms give an error below $5\times10^{-11}$, using the alternating estimate.
- (c) In Lab 0 you computed the same integral by Simpson's rule, needing 128 function evaluations for the same accuracy. **Compare, and comment.**
- (d) **List the four theorems from Weeks 8, 9 and 10 that make the derivation in (a) legitimate**, saying what each one licenses.

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Building series by manipulation |
| B (5 × 6) | 30 | Lagrange and alternating bounds; the counterexample |
| C (5 × 6) | 30 | Limits, non-elementary integrals, coefficient extraction |
| D (2 × 10) | 20 | When a series equals its function; Week 0's debt |
| **Total** | **100** | |

---

## Before You Submit

1. **Every series has its radius stated.**
2. **No Taylor coefficient was computed by repeated differentiation** except where asked.
3. **Every error bound names its type and its interval.**
4. **D2(d) lists four theorems**, not a vague appeal to "the theory".

---

*MATH 142 · Week 10 · Problem Set 10*
