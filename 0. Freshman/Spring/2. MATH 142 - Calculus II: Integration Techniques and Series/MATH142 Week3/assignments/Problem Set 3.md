# MATH 142 · Calculus II
## Problem Set 3
### Topic: Improper Integrals; Comparison Tests
**Released:** Friday 12 February 2027, 12:00 · Week 3 (after Friday's Lecture 3)
**Due:** Friday 19 February 2027, 17:00 · Week 4 — late penalty from 17:01

---

> **Write the limit.** Every improper integral must be set up as a limit before you evaluate
> anything. An answer obtained by substituting $\infty$ into an antiderivative earns no marks even
> when the number is right — the limit notation *is* the argument.
>
> **Before evaluating any definite integral, check the integrand for singularities** — at both
> endpoints and everywhere inside. Two problems below are improper in ways that are not announced.
>
> **For comparison problems, state the comparison function and verify the inequality or the limit.**
> "It behaves like $1/x^2$" is a starting point, not an answer.

---

## Part A — Type I: Infinite Intervals (5 pts each)

**A1.** $\displaystyle\int_1^\infty\frac{dx}{x^3}$

**A2.** $\displaystyle\int_0^\infty e^{-3x}\,dx$

**A3.** $\displaystyle\int_0^\infty xe^{-x^2}\,dx$

**A4.** $\displaystyle\int_2^\infty\frac{dx}{x^2-1}$

*Partial fractions first (Week 2). Watch what happens to the two logarithms separately as $T\to\infty$, and explain why their difference behaves better than either.*

---

## Part B — Type II: Unbounded Integrands (6 pts each)

**B1.** $\displaystyle\int_0^1\frac{dx}{x^{1/3}}$

**B2.** $\displaystyle\int_0^4\frac{dx}{\sqrt{4-x}}$

**B3.** $\displaystyle\int_0^1 x\ln x\,dx$

*You will need $\lim_{t\to0^+}t^2\ln t$. Justify it.*

**B4.** $\displaystyle\int_{-1}^{1}\frac{dx}{x^{2/3}}$

*Use the real cube root, so $x^{2/3} = \left(\sqrt[3]{x}\right)^2 \ge 0$.*

**B5.** $\displaystyle\int_0^2\frac{dx}{(x-1)^2}$

*Two of B4 and B5 have an interior singularity. Both must be split; only one converges.*

---

## Part C — Comparison (6 pts each)

*For each, determine convergence or divergence. **Do not evaluate.** State your comparison function and justify the comparison.*

**C1.** $\displaystyle\int_1^\infty\frac{dx}{x^3+5}$

**C2.** $\displaystyle\int_1^\infty\frac{2+\cos x}{\sqrt x}\,dx$

**C3.** $\displaystyle\int_1^\infty\frac{x}{x^3+1}\,dx$

**C4.** $\displaystyle\int_2^\infty\frac{dx}{\sqrt{x^3-1}}$

*Direct comparison with $x^{-3/2}$ points the wrong way here. Either fix it, or use limit comparison — and say which you did and why.*

**C5.** $\displaystyle\int_0^1\frac{\sin x}{x^{3/2}}\,dx$

*This is Type II. Compare near the singularity, and use a standard fact about $\sin x$ for small $x$.*

---

## Part D — Concept (10 pts each)

**D1.** *(The two $p$-tests.)*

- (a) State both: for which $p$ does $\int_1^\infty x^{-p}dx$ converge, and for which does $\int_0^1x^{-p}dx$ converge?
- (b) The inequalities point in opposite directions. **Explain why**, in terms of what the function must do near each kind of bad point. Do not just restate the tests.
- (c) Both tests exclude $p=1$. Show by direct computation that $\int_1^\infty\frac{dx}{x}$ and $\int_0^1\frac{dx}{x}$ both diverge, and identify the function of $T$ (resp. $t$) that fails to converge in each case.
- (d) Deduce that $\int_0^\infty\frac{dx}{x^p}$ **diverges for every** $p>0$, and explain the deduction in one sentence.

**D2.** *(A confident, wrong answer.)* A student evaluates

$$\int_{-1}^{1}\frac{dx}{x^2} = \left[-\frac1x\right]_{-1}^{1} = (-1)-(1) = -2$$

- (a) Give a one-line reason, requiring no calculation at all, that $-2$ cannot be correct.
- (b) Identify precisely which hypothesis of the Fundamental Theorem of Calculus (Part 2) fails here.
- (c) Evaluate the integral correctly, showing the split and treating each piece as improper.
- (d) The error announced itself because the wrong answer had an impossible **sign**. Construct — or describe — a definite integral with an interior singularity where the same careless method produces a **positive** wrong answer, so that nothing looks amiss. Say what this tells you about how to work.

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Type I; setting up the limit |
| B (5 × 6) | 30 | Type II; endpoint and interior singularities |
| C (5 × 6) | 30 | Direct and limit comparison |
| D (2 × 10) | 20 | The $p$-tests; a diagnostic error |
| **Total** | **100** | |

---

## Before You Submit

1. **Every improper integral written as a limit**, with the limit variable named.
2. **Every singularity found and split at** — check B4, B5, C5 especially.
3. **Every comparison states its comparison function** and verifies the inequality or the limit.
4. **No comparison problem in Part C was evaluated.** If you found a value, you did more work than was asked and probably could not have — check whether an antiderivative even exists.

---

*MATH 142 · Week 3 · Problem Set 3*
