# MATH 142 · Calculus II
## Problem Set 7
### Topic: Series — Geometric, Telescoping, Integral Test, Comparison
**Released:** Friday 12 March 2027, 12:00 · Week 7 (after Friday's Lecture 3)
**Due:** Friday 19 March 2027, 17:00 · Week 8 — late penalty from 17:01

---

> **Name your test, and verify its hypotheses.** From this week a verdict without a justified test is
> worth almost nothing. The Integral Test needs *positive, continuous, decreasing*; comparison needs
> *non-negative*. **Say that you checked.**
>
> **Never write "the terms go to zero, so it converges."** That is the standard error of the subject
> and it is worth zero marks. The $n$-th Term Test proves divergence only.
>
> **For comparisons, state the comparison series and verify the inequality or the limit.**

---

## Part A — Geometric and Telescoping (5 pts each)

**A1.** $\displaystyle\sum_{n=0}^{\infty}3\left(\frac25\right)^n$

**A2.** $\displaystyle\sum_{n=2}^{\infty}\left(-\frac13\right)^{n}$

*Note where the sum starts.*

**A3.** $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+3)}$

*Partial fractions first. Write out the first four and last four terms of $s_N$ before deciding what survives.*

**A4.** $\displaystyle\sum_{n=1}^{\infty}\ln\!\left(\frac{n+1}{n}\right)$

*The terms tend to 0. Find $s_N$ in closed form anyway, and hence decide convergence. Comment on what this shows about the $n$-th Term Test.*

---

## Part B — Integral Test and $p$-Series (6 pts each)

**B1.** $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^{3/2}}$ — converge or diverge? Justify.

**B2.** $\displaystyle\sum_{n=1}^{\infty}\frac{n}{n^2+1}$

*Verify all three hypotheses of the Integral Test before applying it.*

**B3.** $\displaystyle\sum_{n=2}^{\infty}\frac{1}{n(\ln n)^3}$

**B4.** $\displaystyle\sum_{n=1}^{\infty}ne^{-n^2}$

**B5.** *(Remainder estimate.)* For $\displaystyle\sum_{n=1}^\infty\frac{1}{n^3}$:

- (a) Use the Integral Test remainder bound to find how many terms guarantee an error below $10^{-3}$.
- (b) State the two-sided bound on $R_N$ for your $N$.
- (c) Estimate the sum using the **average** of those two bounds, and say why that should be better than $s_N$ alone.

---

## Part C — Comparison (6 pts each)

*Determine convergence or divergence. State the comparison series and justify.*

**C1.** $\displaystyle\sum_{n=1}^{\infty}\frac{n^2+1}{n^4+3}$

**C2.** $\displaystyle\sum_{n=2}^{\infty}\frac{1}{n-\ln n}$

**C3.** $\displaystyle\sum_{n=1}^{\infty}\frac{2+\cos n}{n^2}$

*Why can the Integral Test not be used here?*

**C4.** $\displaystyle\sum_{n=2}^{\infty}\frac{1}{n^{1+1/n}}$

*Careful. Consider $\lim n^{1/n}$ from Week 6, and use limit comparison against a series you know.*

**C5.** $\displaystyle\sum_{n=1}^{\infty}\frac{\arctan n}{n^2}$

---

## Part D — Concept (10 pts each)

**D1.** *(The $n$-th Term Test.)*

- (a) State it, in the form that is actually useful.
- (b) Prove it from the definition of a series. *(Two lines, using $a_n = s_n-s_{n-1}$.)*
- (c) Explain why it can **never** prove convergence, and give two different series with $a_n\to0$, one convergent and one divergent.
- (d) A4 above has terms tending to 0 and diverges. Explain how a student who only checked the $n$-th Term Test would have gone wrong, and what they should have done instead.

**D2.** *(Checking a machine.)* A numerical library, asked for $\displaystyle\sum_{n=1}^\infty\frac{\ln n}{n^2}$, reports

$$0.936715596751$$

You do not know the true value.

- (a) Compute the partial sum $s_N$ for $N=10^6$. *(You may use a computer; report the value.)*
- (b) Using **only** the definition of a series and the fact that all terms are positive, explain why (a) proves the library's answer is wrong.
- (c) Use the Integral Test remainder bound to estimate the true value from your $s_N$, and state your estimate.
- (d) Comment in two or three sentences: what general habit does this illustrate, and how does it relate to the CAS failures earlier in the course?

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Geometric, telescoping, and a trap |
| B (5 × 6) | 30 | Integral Test, hypotheses, remainder bounds |
| C (5 × 6) | 30 | Direct and limit comparison |
| D (2 × 10) | 20 | The $n$-th Term Test; checking a machine |
| **Total** | **100** | |

---

## Before You Submit

1. **Every test named, with hypotheses checked.**
2. **No occurrence of "terms go to zero, so it converges."**
3. **Every comparison states its comparison series** and the direction of the inequality.
4. **Check A4 and C4** — both are designed to catch a plausible wrong answer.

---

*MATH 142 · Week 7 · Problem Set 7*
