# MATH 142 · Calculus II
## Lab 07: Partial Sums and the Rate of Convergence
### Week 7 Lab Session

**Date:** Wednesday 17 March 2027 · 15:00–16:50 · Lab section (Week 8) — covers Week 7 (Lectures 1–3)

---

**Duration:** 2 hours
**Format:** Individual or pairs (pairs submit separate reports)
**Graded on:** completion + correctness — **100 points**
**Tools required:** Python 3 with `mpmath` — only the calls in Lab 02's SymPy box and Lab 03's mpmath box

---

## Overview

Two series, both famous, both about as simple as a series can be:

$$\sum_{n=1}^\infty\frac1n \qquad\text{and}\qquad \sum_{n=1}^\infty\frac{1}{n^2}$$

**One diverges. One converges.** And in both cases, **the partial sums are nearly useless for finding that out** — the first diverges too slowly ever to be observed, and the second converges too slowly to be computed.

This lab measures both, and then fixes the second one using the Integral Test's remainder bound — turning a hopeless method into an excellent one with a single extra line.

---

## Part A — How Slowly the Harmonic Series Diverges (25 pts)

**A1 (8 pts).** Compute $H_N=\sum_{n=1}^N\frac1n$ for $N=10,\ 10^2,\ 10^4,\ 10^6$.

Tabulate $H_N$ alongside $\ln N+\gamma$, where $\gamma = 0.5772156649\ldots$ is the Euler–Mascheroni constant *(`mp.euler`)*.

**A2 (7 pts).** Add a column for the difference $H_N-(\ln N+\gamma)$.

- (a) What happens to it?
- (b) It behaves like $\frac{c}{N}$ for a simple constant $c$. **Determine $c$ from your data.**

**A3 (10 pts).** Using $H_N\approx\ln N+\gamma$, compute how many terms are needed for the partial sum to first exceed

$$S = 5,\ 10,\ 20,\ 50,\ 100$$

Present the results, and comment on the last two. *(For scale: roughly $10^{80}$ atoms are estimated to exist in the observable universe.)*

---

## Part B — How Slowly the Basel Series Converges (25 pts)

$$\sum_{n=1}^\infty\frac{1}{n^2} = \frac{\pi^2}{6} = 1.6449340668\ldots$$

**B1 (8 pts).** Compute $s_N$ for $N=10,\ 10^2,\ 10^3,\ 10^4$ and tabulate the error $\frac{\pi^2}{6}-s_N$.

**B2 (8 pts).** Add a column of $N\times\text{error}$. What does it converge to?

Hence state the order of convergence and how the error behaves in $N$.

**B3 (9 pts).**

- (a) From your answer to B2, how many terms are needed for 6 correct decimal places? For 10?
- (b) Compare with Lab 0's Simpson's rule (10 digits from 128 points) and Lab 6's Babylonian iteration (48 digits in 6 steps).
- (c) Is direct summation a practical way to compute $\frac{\pi^2}{6}$?

---

## Part C — The Integral Test Remainder, and a Free Improvement (30 pts)

For $\sum\frac{1}{n^2}$, the Integral Test gives

$$\int_{N+1}^{\infty}\frac{dx}{x^2} \;\le\; R_N \;\le\; \int_N^\infty\frac{dx}{x^2} \qquad\text{i.e.}\qquad \frac{1}{N+1}\le R_N\le\frac1N$$

**C1 (8 pts).** For $N=10,\ 100,\ 1000$, compute the true remainder $R_N = \frac{\pi^2}{6}-s_N$ and **verify both inequalities hold.** Present as a table.

**C2 (12 pts).** Now form the improved estimate using the **average** of the two bounds:

$$\widetilde S_N = s_N + \frac12\left(\frac{1}{N+1}+\frac1N\right)$$

Tabulate $\left|\frac{\pi^2}{6}-\widetilde S_N\right|$ for $N=10,\ 10^2,\ 10^3,\ 10^4$ alongside the raw error from B1.

**C3 (10 pts).** Add a column of consecutive error ratios for $\widetilde S_N$ as $N$ increases by a factor of 10.

- (a) What is the ratio, and hence the **order** of the improved method?
- (b) The raw method was order 1. State the improvement.
- (c) How many terms does $\widetilde S_N$ need for 10 correct digits? Compare with your B3(a) answer.
- (d) Comment: **the improvement cost one line of arithmetic and no extra terms.** Where did the extra accuracy come from?

---

## Part D — Reflection (20 pts)

**D1 (10 pts).** This lab contains a divergent series whose divergence cannot be observed, and a convergent series whose sum cannot be computed by summing it.

For each, state **what does settle the question**, and how much work it takes.

**D2 (10 pts).** Across seven labs the balance between exact and numerical methods has shifted repeatedly:

| Lab | Verdict |
|---|---|
| 0 | numerics won |
| 1 | numerics worked, far too slowly |
| 2 | numerics gave the value, not the proof |
| 3 | numerics could not answer at all |
| 4 | excellent on one half, useless on the other |
| 5 | numerics essential — no closed form exists |
| 6 | numerics superb, **because** exact analysis predicted it |
| **7** | **?** |

Fill in the entry, and identify which earlier lab this one most resembles.

*In your answer, address Part C specifically: an exact theorem (the Integral Test) was used to improve a numerical method. Which of the two deserves the credit?*

---

## What to Submit

1. The harmonic table with the difference column and the term counts (Part A)
2. The Basel table with $N\times$error (Part B)
3. The remainder verification, the improved estimate, and the order analysis (Part C)
4. Parts D1 and D2

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A | 25 | Logarithmic divergence, measured |
| B | 25 | Order-1 convergence, measured |
| C | 30 | Remainder bounds, and raising the order to 3 |
| D | 20 | What settles a convergence question |
| **Total** | **100** | |

---

*A theorem you proved on Tuesday, applied on Wednesday, makes a hopeless computation good. That is not a coincidence — it is what the theorems are for.*
