# MATH 141 · Calculus I
## Quiz 07 (Monday, Week 7 — Start of Class)

**Date:** Monday 9 November 2026 · 11:00–11:15 (start of Lecture 01) · Week 7
### Covers: Week 6 — Extrema, Rolle's Theorem, the MVT, L'Hôpital's Rule

**Time:** 15 minutes | **Closed book, closed notes**
**Name:** _________________________________ | **Section:** _______

---

**Q1 (4 pts).** Find all critical numbers of $f(x) = 2x^3 - 9x^2 + 12x - 3$.

&nbsp;

&nbsp;

&nbsp;

---

**Q2 (4 pts).** Use the Closed Interval Method to find the absolute max and min of $f(x) = x^3 - 3x + 1$ on $[-2, 2]$.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

**Q3 (4 pts).** Verify the Mean Value Theorem applies to $f(x) = x^2 - 4x$ on $[0, 5]$, then find the value of $c$ guaranteed by the theorem.

&nbsp;

&nbsp;

&nbsp;

---

**Q4 (4 pts).** Evaluate using L'Hôpital's Rule, stating the indeterminate form first:
$$\lim_{x\to0}\frac{e^{3x}-1}{x}$$

&nbsp;

&nbsp;

&nbsp;

---

**Q5 (4 pts).** Evaluate, stating the indeterminate form first:
$$\lim_{x\to\infty}\frac{\ln x}{\sqrt x}$$

&nbsp;

&nbsp;

&nbsp;

---

*Total: 20 pts*

---
---

# Quiz 07 — ANSWER KEY (INSTRUCTOR ONLY)

---

**Q1.** $f'(x)=6x^2-18x+12=6(x^2-3x+2)=6(x-1)(x-2)$

Critical numbers: $x=1, x=2$

*Grading: 2 pts factoring, 2 pts correct critical numbers*

---

**Q2.** $f'(x)=3x^2-3=0\implies x=\pm1$

$f(-2)=-8+6+1=-1$; $f(-1)=-1+3+1=3$; $f(1)=1-3+1=-1$; $f(2)=8-6+1=3$

**Max: 3 (at $x=-1$ and $x=2$). Min: $-1$ (at $x=-2$ and $x=1$).**

*Grading: 1 pt critical numbers, 2 pts evaluating all four points, 1 pt correct max/min identification*

*Note: both extremes are attained twice. Students who report only one location for each should not be penalised, but it is worth pointing out in review — the Closed Interval Method returns values, and a value can occur at several points.*

---

**Q3.** $f$ is a polynomial: continuous on $[0,5]$, differentiable on $(0,5)$. ✓ MVT applies.

$$\frac{f(5)-f(0)}{5-0}=\frac{(25-20)-0}{5}=\frac{5}{5}=1$$

$f'(x)=2x-4=1\implies x=5/2\in(0,5)$

$c=5/2$

*Grading: 1 pt verifying hypotheses, 1 pt computing average rate, 2 pts solving for $c$*

---

**Q4.** Form: $\dfrac{0}{0}$ (numerator $e^0-1=0$, denominator $0$).

L'Hôpital: $\displaystyle\lim_{x\to0}\frac{3e^{3x}}{1}=3e^0=\mathbf 3$

*(Verified numerically: the quotient is $3.0000045$ at $x=10^{-6}$.)*

*Grading: 1 pt identifying the form, 2 pts correct differentiation, 1 pt correct value. Differentiating with the quotient rule instead of applying L'Hôpital is a whole-question error — the rule differentiates numerator and denominator **separately**.*

---

**Q5.** Form: $\dfrac{\infty}{\infty}$.

L'Hôpital: $\displaystyle\lim_{x\to\infty}\frac{1/x}{1/(2\sqrt x)}=\lim_{x\to\infty}\frac{2\sqrt x}{x}=\lim_{x\to\infty}\frac{2}{\sqrt x}=\mathbf 0$

*(Verified numerically: $0.00184$ at $x=10^8$, $2.76\times10^{-5}$ at $x=10^{12}$ — the decay is genuine but slow, which is the point: logarithms lose to every positive power of $x$.)*

*Grading: 1 pt identifying the form, 2 pts differentiation and simplification, 1 pt correct limit.*

---

*Coverage note: this quiz is drawn entirely from Week 6 (extrema and the Closed Interval Method,
Rolle/MVT, L'Hôpital). Concavity, curve sketching, and applied optimization are **Week 7** material
and appear on Quiz 08.*
