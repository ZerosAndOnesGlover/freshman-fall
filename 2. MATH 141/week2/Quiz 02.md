---
assessment: Quiz 02
course: MATH 141
component: Quizzes
possible: 20
score: 20
status: graded
started: 2026-10-08
submitted: 2026-10-08
graded: 2026-10-08
source: "QUIZ 02 With Answer Key.md"
---

# MATH 141 · Quiz 02
## Answer Sheet

**Assessment:** `QUIZ 02 With Answer Key.md`
**Points available:** 20

---

## Section A — Short Answer (2 pts each)

**A1.** For every $\varepsilon>0$ there exists $\delta>0$ such that
$$0 < |x-a| < \delta \implies |f(x)-L| < \varepsilon.$$
*(1 pt for quantifiers in order ∀ε∃δ, 1 pt for $0<|x-a|$.)*

**A2.** $\displaystyle\lim_{x\to\infty}\frac{3x^2+2x}{x^2-5} = 3$. Divide numerator and denominator by $x^2$ (highest power in denominator): $\frac{3+2/x}{1-5/x^2}\to \frac{3}{1}=3$. Equal degrees ⇒ ratio of leading coefficients.

**A3.** $\lim_{x\to0^+}\frac{1}{x}=+\infty$, $\lim_{x\to0^-}\frac{1}{x}=-\infty$. Since the one-sided limits disagree, $\lim_{x\to0}\frac{1}{x}$ does **not** exist.

**A4.** For $1/x^2$, both one-sided limits are $+\infty$ (they agree), so it is meaningful to write $\lim_{x\to0}\frac{1}{x^2}=+\infty$ as a two-sided statement describing the unbounded behavior. For $1/x$, the one-sided limits differ in sign ($+\infty$ vs $-\infty$), so no single two-sided statement is correct; we do not write $\lim_{x\to0}\frac{1}{x}=\infty$. Note $\infty$ is not a real number in either case.

**A5.** Three indeterminate forms: $\frac{0}{0}$, $\frac{\infty}{\infty}$, $\infty-\infty$ (also acceptable: $0\cdot\infty$, $1^\infty$, $0^0$, $\infty^0$). "Indeterminate" means the form alone does **not** determine the limit — functions with the same indeterminate form can have different limits.

*Marks: ___ / 10*

---

## Section B — Longer (5 pts each)

**B1.** Evaluate $\displaystyle\lim_{x\to\infty}\big(\sqrt{x^2+1}-x\big)$.

Rationalize:
$$\sqrt{x^2+1}-x=\frac{(\sqrt{x^2+1}-x)(\sqrt{x^2+1}+x)}{\sqrt{x^2+1}+x}=\frac{x^2+1-x^2}{\sqrt{x^2+1}+x}=\frac{1}{\sqrt{x^2+1}+x}.$$
As $x\to+\infty$, $\sqrt{x^2+1}\sim x$ so denominator $\sim 2x\to+\infty$; thus the limit is $0$.

**Answer:** $0$

*Marks: ___ / 5*

**B2.** Find all horizontal and vertical asymptotes of $f(x)=\dfrac{3x^2+2x}{x^2-5}$.

**Horizontal asymptote:** From A2, $\lim_{x\to\pm\infty}f(x)=3$ (equal degrees, ratio of leading coefficients), so $y=3$ is the horizontal asymptote (in both directions).

**Vertical asymptotes:** Denominator zero at $x^2-5=0 \implies x=\pm\sqrt{5}$. Numerator at $x=\sqrt{5}$: $3(5)+2\sqrt{5}=15+2\sqrt{5}\neq 0$; at $x=-\sqrt{5}$: $3(5)+2(-\sqrt{5})=15-2\sqrt{5}\neq 0$. Thus vertical asymptotes at $x=\sqrt{5}$ and $x=-\sqrt{5}$.

**Answer:** HA: $y=3$; VA: $x=\pm\sqrt{5}$

*Marks: ___ / 5*

---

## Grading Summary

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-10-08 |

**Feedback:**
All correct per answer key. ε-δ stated precisely with correct quantifier order and $0<|x-a|$. Limit at infinity handled via highest-degree division; one-sided infinite limits compared correctly. The distinction for $1/x^2$ vs $1/x$ (agreement vs disagreement of one-sided infinities) is clear. Rationalization for $\sqrt{x^2+1}-x$ shown. Asymptotes identified with the required check that numerator is nonzero at vertical asymptotes. No errors.
