# MATH 142 · Calculus II
## Lab 10: Taylor Approximation, and Week 0's Debt
### Week 10 Lab Session

**Date:** Wednesday 7 April 2027 · 15:00–16:50 · Lab section (Week 11) — covers Week 10 (Lectures 1–3)

---

**Duration:** 2 hours
**Format:** Individual or pairs (pairs submit separate reports)
**Graded on:** completion + correctness — **100 points**
**Tools required:** Python 3 with `sympy` and `mpmath` — only the calls in Lab 02's SymPy box and Lab 03's mpmath box

---

## Overview

**In Week 0 you were told this:**

> $e^{-x^2}$ is continuous, so it has an antiderivative — **and that antiderivative is not
> elementary** (Liouville, 1835).

**In Lab 0 you computed $\int_0^1 e^{-x^2}dx$ anyway**, numerically, with Simpson's rule: **128 function evaluations** for ten decimal places. The debrief ended with a promise:

> *In Week 10 you will compute the same integral to the same precision by adding **13 numbers**.*

**This lab collects that debt.** It also measures how good Taylor's error bounds actually are, and examines the function whose Taylor series lies about it.

---

## Part A — Taylor Polynomials and Their Errors (25 pts)

**A1 (10 pts).** For $f(x)=\sin x$ at $a=0$, build the Taylor polynomials $P_1,P_3,P_5,P_7,P_9$.

Tabulate the **true error** $|\sin x - P_n(x)|$ at $x = 0.5,\ 1.0,\ 2.0$.

**A2 (8 pts).** Add, for each entry, the **Lagrange bound** $\dfrac{|x|^{n+1}}{(n+1)!}$.

*(Justify why $M=1$ is valid here.)*

**Confirm the bound holds in every case**, and report the **ratio** bound/true-error.

**A3 (7 pts).** Comment on the ratios.

- (a) Is the bound tight or loose? By roughly what factor?
- (b) Why would a numerical library still use this bound rather than the true error?

---

## Part B — Where the Series Lies (20 pts)

Let

$$f(x)=\begin{cases}e^{-1/x^2}&x\ne0\\0&x=0\end{cases}$$

**B1 (8 pts).** Compute $f(x)$ and $\dfrac{f(x)}{x^{10}}$ at $x=0.5,\ 0.2,\ 0.1,\ 0.05$.

What happens to the second column?

**B2 (6 pts).** It is a fact that $f^{(n)}(0)=0$ for every $n$. **Write down the Maclaurin series of $f$**, state its radius of convergence, and state what function it converges to.

**B3 (6 pts).** Compute $f(1)$ and compare with the value of the Maclaurin series at $x=1$.

**At how many points does $f$ agree with its own Taylor series?** Explain what this shows about the necessity of the remainder in Taylor's theorem.

---

## Part C — Collecting Week 0's Debt (35 pts)

**C1 (8 pts).** Derive

$$\int_0^1 e^{-x^2}dx = \sum_{n=0}^\infty\frac{(-1)^n}{n!\,(2n+1)}$$

showing the substitution and the term-by-term integration.

**C2 (12 pts).** Compute the partial sums for $1$ to $16$ terms, tabulating the value and the error against

$$\frac{\sqrt\pi}{2}\operatorname{erf}(1) = 0.7468241328124270254\ldots$$

**Report the first $N$ for which the error falls below $5\times10^{-11}$.**

**C3 (8 pts).** Build the comparison table:

| method | evaluations/terms for 10 digits |
|---|---|
| Simpson's rule (Lab 0) | ? |
| Taylor series (this lab) | ? |

Comment on the ratio.

**C4 (7 pts).** Do the same for $\displaystyle\int_0^1\frac{\sin x}{x}\,dx$.

Derive the series, tabulate partial sums, and report how many terms give eleven correct digits.

*Note that the integrand is undefined at $x=0$ while the series is not — explain.*

---

## Part D — Reflection (20 pts)

**D1 (10 pts).** The derivation in C1 used, in order: a Taylor series equalling its function; term-by-term integration; and an error bound from the first omitted term.

**Name the theorem behind each**, and the week it came from.

**D2 (10 pts).** This is the last lab before the final. Across ten labs:

| Lab | Verdict |
|---|---|
| 0 | numerics won |
| 3 | numerics could not answer at all |
| 6 | numerics superb, because exact analysis predicted it |
| 7 | numerics failed; an exact theorem repaired it |
| 8 | numerics correct; the question was ill-posed |
| 9 | the boundary was invisible to computation |
| **10** | **?** |

Fill in the entry for this lab.

*In your answer, address this: Lab 0's Simpson's rule and Lab 10's Taylor series compute the same number to the same accuracy. **What does the Taylor method have that Simpson's does not?*** *(Consider what each can promise before it is run.)*

---

## What to Submit

1. The $\sin$ error/bound table with ratios (Part A)
2. The $e^{-1/x^2}$ computation and your answers to B2, B3 (Part B)
3. The derivation, the 16-row partial-sum table, and the comparison (Part C)
4. Parts D1 and D2

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A | 25 | Taylor polynomials and the Lagrange bound |
| B | 20 | The function that is not its own series |
| C | 35 | Week 0's debt, collected |
| D | 20 | What Taylor gives that numerics does not |
| **Total** | **100** | |

---

*Ten weeks ago you were told an integral could not be done. You did it numerically anyway, and were promised a better way. This is it.*
