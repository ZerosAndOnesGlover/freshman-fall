# MATH 142 · Calculus II
## Lab 12: Mixed Review and Self-Diagnosis
### Week 12 Lab Session

**Date:** Wednesday 21 April 2027 · 15:00–16:50 · Lab section (finals week — see the course audit) — covers Week 12 (Lectures 1–3)

---

**Duration:** 2 hours
**Format:** **Individual.** This one is not useful in pairs.
**Graded on:** completion + honesty — **100 points**
**Tools required:** Python 3 with `mpmath`, for Part B only — only the calls in Lab 02's SymPy box and Lab 03's mpmath box

---

## Overview

**Two hours, three parts, and the first one is timed.**

Part A is a mock exam section done **without notes**, and it is marked on completion and on the honesty of your self-assessment — **not on how many you got right.** Part B is the last computation of the course: one integral, attacked with every tool the term supplied, ending in a result that should alarm you slightly. Part C is where you write down what you actually need to revise.

> **The purpose of this lab is to make your revision list short and correct.** A student who
> discovers here that they cannot do endpoint tests has gained more than one who scores 100%.

---

## Part A — Timed Mock Section (30 pts)

> **Set a timer for 50 minutes. Close your notes. No CAS, no calculator.**
> **Stop when the timer goes**, even mid-problem, and mark where you stopped.

**A1 (6 pts).** $\displaystyle\int_0^{1}x^3\sqrt{1-x^2}\,dx$

**A2 (6 pts).** $\displaystyle\int\frac{x^2+1}{x(x-1)^2}\,dx$

**A3 (6 pts).** Determine convergence, with justification, for each:
$$\text{(a) }\sum_{n=1}^\infty\frac{n^2}{2^n} \qquad \text{(b) }\sum_{n=2}^\infty\frac{1}{n\ln n} \qquad \text{(c) }\sum_{n=1}^\infty\frac{(-1)^n n}{n^2+1}$$
*For (c), state whether the convergence is absolute or conditional.*

**A4 (6 pts).** Find the interval of convergence of $\displaystyle\sum_{n=0}^\infty\frac{(3x-1)^n}{n^2+1}$, **endpoints decided.**

**A5 (6 pts).** Solve $\displaystyle\frac{dy}{dx}=\frac{2x}{1+y^2}$, $y(0)=1$. **Leave it implicit and say why.**

### A6 (0 pts, but do it) — the self-mark

**After the timer, and only then**, work each problem again *with* your notes, and fill in:

| | Got it in time? | Got it with notes? | Which week? |
|---|---|---|---|
| A1 | | | |
| A2 | | | |
| A3a/b/c | | | |
| A4 | | | |
| A5 | | | |

**The interesting cell is "no / yes".** That is a fluency problem, not a knowledge problem, and it is fixed by doing problems, not by re-reading.

*Marking: 30 points for a complete, timed, honestly self-marked attempt. **Correctness is not marked.***

---

## Part B — One Integral, Every Tool (45 pts)

$$I=\int_0^\infty e^{-x^2}\,dx = \frac{\sqrt\pi}{2} = 0.886226925452758\ldots$$

**This integral has no elementary antiderivative** *(Week 10)*, **and its infinite range makes it improper** *(Week 3)*. We will compute it three ways.

### B1 (10 pts) — Kill the tail with a bound

**Prove**, for $T\ge1$:

$$\int_T^\infty e^{-x^2}dx \;\le\; \frac{e^{-T^2}}{2T}$$

*Hint: on $[T,\infty)$ we have $x\ge T$, so $e^{-x^2}\le\frac{x}{T}e^{-x^2}$, and the right side integrates exactly.*

**Then tabulate the bound for $T=1,\ldots,6$ and choose the smallest $T$ for which the tail is provably below $10^{-15}$.**

### B2 (12 pts) — Simpson's rule on the truncated integral

**Apply Simpson's rule to $\int_0^{4}e^{-x^2}dx$ for $n=4,8,16,32,64,128,256$**, and tabulate the error against the true value $0.886226911789569$, with the ratio of consecutive errors.

- **(a)** The first two ratios are enormous — over $1000$. **Explain why**, in terms of what Simpson's rule assumes about the function on each subinterval.
- **(b)** From which $n$ does the ratio settle near $16$? **What does that tell you about reading an order off two data points?**

### B3 (13 pts) — The Maclaurin series, and a warning

**From $e^{u}=\sum u^n/n!$** *(Week 10)*, derive

$$\int_0^Te^{-x^2}dx = \sum_{k=0}^\infty\frac{(-1)^kT^{2k+1}}{k!\,(2k+1)}$$

**This series converges for every $T$** — the Ratio Test gives an infinite radius. **Sum it in double precision** for $T=1,2,3,4,5,6$, and record for each: your value, the true value, the absolute error, and **the magnitude of the largest single term you added.**

- **(a)** At $T=1$ and $T=2$ the series is essentially perfect. At $T=6$ it is not. **Report the error at $T=6$.**
- **(b)** **What is the largest term at $T=6$, and how does it compare to the answer?**
- **(c)** The series is mathematically exact and convergent. **Name the failure**, using Tuesday's lecture.
- **(d)** Now compute the terms two ways — directly as `(-1)**k * T**(2*k+1)/(factorial(k)*(2*k+1))`, and by the recurrence $t_k=-t_{k-1}\cdot\frac{T^2}{k}\cdot\frac{2k-1}{2k+1}$. **Compare the two totals at $T=6$.** *Report what you find; do not assume they agree.*

### B4 (10 pts) — Put it together

**Combine B1 and B2:** Simpson on $[0,6]$ with $n=256$, plus the proven tail bound.

- **(a)** Report your value and its error against $\sqrt\pi/2$.
- **(b)** **You now have a number with a rigorous error bound.** Write the one sentence that justifies it, naming which part supplies the truncation error and which supplies the quadrature error.
- **(c)** The series of B3 and the quadrature of B2 approximate the same integral. **In one sentence each, say when you would use which.**

---

## Part C — The Revision List (25 pts)

### C1 (10 pts)

**From Part A's self-mark and PS 12's answer key**, list **every week you missed something in**, and for each write **one sentence** naming the specific gap. Not "series" — *"I do not test endpoints"*.

### C2 (8 pts)

**Across the whole term, name the three errors you have made most often.** Look at your returned problem sets, not at your memory of them.

**For each, write the check that would have caught it.** *(Examples from the term: a sign check on a positive integrand; a partial sum that cannot exceed its total; substituting a solution back into its equation; comparing two refinements.)*

### C3 (7 pts)

**In one paragraph: what will you do differently in the last week before the exam?**

**Answers of the form "revise more" earn nothing.** The answer should be a list of weeks and a number of problems.

---

## Marking Summary

| Part | Points |
|---|---|
| A — timed mock, honestly self-marked | 30 |
| B1 — tail bound | 10 |
| B2 — Simpson and its ratios | 12 |
| B3 — series and its failure | 13 |
| B4 — the combined answer | 10 |
| C — the revision list | 25 |
| **Total** | **100** |

---

## Submission

A single report. **Part A may be photographed handwritten** — it should be, since it was written under a timer. Parts B and C typed, with your code.

> **Part A is marked on completion and honesty. Part B is marked on correctness. Part C is marked on
> specificity.**

---

*MATH 142 · Week 12 · Lab 12 — the last one*
