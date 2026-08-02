# MATH 141 — Calculus I
## Quiz 05 (Monday, Week 5 — Start of Class)
### Covers: Week 4 — Differentiation Rules, the Chain Rule, Higher Derivatives and Rates
*(Q1 revisits Week 3's limit definition deliberately — the rules are shortcuts for it, not replacements.)*

**Time:** 15 minutes | **Closed book, closed notes**
**Name:** _________________________________ | **Section:** _______

---

**Q1 (4 pts).** Using the limit definition of the derivative, find $f'(x)$ for $f(x) = x^2 + 3x$.

Do NOT use differentiation rules.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

**Q2 (4 pts).** Differentiate. State every rule used.

$$y = \frac{x^3 - 2x}{x^2 + 1}$$

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

**Q3 (4 pts).** Differentiate using the chain rule:

$$y = \sin^4(3x^2)$$

Identify the outer, middle, and inner functions before differentiating.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

**Q4 (4 pts).** Find the equation of the tangent line to $y = e^{x^2}$ at $x = 1$.

&nbsp;

&nbsp;

&nbsp;

---

**Q5 (4 pts).** A particle has position $s(t) = t^3 - 6t^2 + 9t$ (meters, $t \geq 0$ in seconds).

(a) Find the velocity $v(t)$.

(b) At what time(s) is the particle at rest?

&nbsp;

&nbsp;

&nbsp;

---

*Total: 20 pts*

---
---

# Quiz 05 — ANSWER KEY (INSTRUCTOR ONLY)

---

**Q1.** $f(x)=x^2+3x$

$$\frac{f(x+h)-f(x)}{h}=\frac{(x+h)^2+3(x+h)-(x^2+3x)}{h}=\frac{x^2+2xh+h^2+3x+3h-x^2-3x}{h}=\frac{2xh+h^2+3h}{h}=2x+h+3$$

$f'(x)=\lim_{h\to0}(2x+h+3)=\boxed{2x+3}$

*Grading: 2 pts expanding, 1 pt simplifying/canceling, 1 pt taking limit*

---

**Q2.** Quotient rule:

$$y'=\frac{(3x^2-2)(x^2+1)-(x^3-2x)(2x)}{(x^2+1)^2}=\frac{3x^4+3x^2-2x^2-2-2x^4+4x^2}{(x^2+1)^2}=\frac{x^4+5x^2-2}{(x^2+1)^2}$$

*Grading: 2 pts applying quotient rule correctly, 1 pt numerator expansion, 1 pt simplification*

---

**Q3.** $y=[\sin(3x^2)]^4$

- Outer: $u^4$
- Middle: $\sin(v)$
- Inner: $3x^2$

$$y'=4\sin^3(3x^2)\cdot\cos(3x^2)\cdot6x=\boxed{24x\sin^3(3x^2)\cos(3x^2)}$$

*Grading: 1 pt identifying layers, 1 pt first chain rule, 1 pt second chain rule, 1 pt correct final form*

---

**Q4.** $y=e^{x^2}$; $y'=2xe^{x^2}$.

At $x=1$: $y(1)=e^1=e$, $y'(1)=2(1)e^1=2e$.

Tangent line: $y-e=2e(x-1)$, i.e., $\boxed{y=2ex-e}$

*Grading: 1 pt derivative, 1 pt evaluating $y(1)$, 1 pt evaluating $y'(1)$, 1 pt tangent line equation*

---

**Q5.**
(a) $v(t)=s'(t)=3t^2-12t+9=3(t^2-4t+3)=3(t-1)(t-3)$

(b) At rest when $v(t)=0$: $t=1$ s and $t=3$ s.

*Grading: 2 pts (a), 2 pts (b)*
