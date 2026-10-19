---
assessment: Quiz 03
course: MATH 141
component: Quizzes
possible: 20
score: 20
status: graded
started: 2026-10-19
submitted: 2026-10-19
graded: 2026-10-19
source: "QUIZ 03 With Answer Key.md"
---

# MATH 141 · Quiz 03
## Answer Sheet

**Assessment:** `QUIZ 03 With Answer Key.md`
**Points available:** 20

---

**Q1 (4 pts). Is $f$ continuous at $x=1$?**
$$f(x)=\begin{cases}x^2+1,&x\le1\\ 3x-1,&x>1\end{cases}$$

Check the three conditions of continuity at $a=1$:

1. **Defined:** $f(1)=1^2+1=2$. ✓
2. **Limit exists:** $\displaystyle\lim_{x\to1^-}f(x)=1+1=2$ and $\displaystyle\lim_{x\to1^+}f(x)=3-1=2$. The one-sided limits agree, so $\displaystyle\lim_{x\to1}f(x)=2$. ✓
3. **They match:** $\displaystyle\lim_{x\to1}f(x)=2=f(1)$. ✓

All three conditions hold, so $f$ **is continuous at $x=1$**.

**Answer:** Continuous at $x=1$.

*Marks: 4 / 4*

---

**Q2 (4 pts). Classify the discontinuity at $x=3$.**

(a) $\dfrac{x^2-x-6}{x-3}$: factor the numerator, $x^2-x-6=(x-3)(x+2)$, so the function equals $x+2$
for $x\neq3$ and has limit $5$. The limit exists but $f(3)$ is undefined — **removable**.

(b) $\dfrac{x+2}{x-3}$: at $x=3$ the numerator is $5\neq0$ while the denominator vanishes, so the
one-sided limits are $\mp\infty$ — a vertical asymptote, **infinite**.

**Answer:** (a) Removable; (b) Infinite.

*Marks: 4 / 4*

---

**Q3 (4 pts). Continuous extension of Q2(a).**

The continuous extension removes the hole by defining $f(3)$ to be the limit, $5$:
$$\tilde f(x)=\begin{cases}\dfrac{x^2-x-6}{x-3},&x\neq3\\[6pt] 5,&x=3.\end{cases}$$
Equivalently, $\tilde f(x)=x+2$ for all $x$.

**Answer:** $\tilde f(x)=\begin{cases}\dfrac{x^2-x-6}{x-3},&x\neq3\\ 5,&x=3\end{cases}$

*Marks: 4 / 4*

---

**Q4 (4 pts). IVT for $f(x)=x^3+2x-5$ on $(1,2)$.**

**Hypotheses.** (1) $f$ is a polynomial, hence **continuous on the closed interval $[1,2]$**.
(2) $f(1)=1+2-5=-2<0$ and $f(2)=8+4-5=7>0$, so $f(1)$ and $f(2)$ have opposite signs and $0$ lies
strictly between them.

**Conclusion.** By the IVT there exists $c\in(1,2)$ with $f(c)=0$ — a root in $(1,2)$.

**What the IVT does not tell you:** *where* the root is, *how many* roots there are, or *how* to find
one. It is a pure existence statement.

**Answer:** Root exists in $(1,2)$; IVT gives existence only, not location or number.

*Marks: 4 / 4*

---

**Q5 (4 pts). Two bisection steps on $[1,2]$, $f(x)=x^3+2x-5$.**

| Step | Bracket in | Midpoint | $f(\text{mid})$ | Bracket out |
|---|---|---|---|---|
| 1 | $[1,2]$ | $1.5$ | $+1.375000$ | $[1,\,1.5]$ |
| 2 | $[1,1.5]$ | $1.25$ | $-0.546875$ | $[1.25,\,1.5]$ |

After two steps the root is bracketed in $[1.25,\,1.5]$, of width $0.25$.

**Answer:** $[1.25,\,1.5]$

*Marks: 4 / 4*

---

## Grading Summary

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-10-19 |

**Feedback:**
All correct per answer key.

- **Q1:** All three continuity conditions checked explicitly, including the value $f(1)=2$, with the
  correct conclusion.
- **Q2:** Both $\frac{\text{something}}{0}$ cases at $x=3$ distinguished correctly — removable
  (limit exists, point missing) vs infinite (vertical asymptote) — the point being tested.
- **Q3:** Continuous extension written as an actual piecewise definition with value $5$, not merely
  "define $f(3)=5$".
- **Q4:** Continuity hypothesis and the two sign computations stated, IVT cited correctly, and the
  existence-only limitation given.
- **Q5:** Both bisection steps shown with the correct sign decisions, ending in $[1.25,\,1.5]$.
