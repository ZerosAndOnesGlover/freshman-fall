---
assessment: Quiz 04
course: MATH 141
component: Quizzes
possible: 20
score: 20
status: graded
started: 2026-10-19
submitted: 2026-10-19
graded: 2026-10-19
source: "QUIZ 04 With Answer Key.md"
---

# MATH 141 · Quiz 04
## Answer Sheet

**Assessment:** `QUIZ 04 With Answer Key.md`
**Points available:** 20

---

## Section A — Short Answer (2 pts each)

**A1.** The limit definition of the derivative as a function is
$$f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h},$$
defined wherever this two-sided limit exists.

*(1 pt for the difference quotient, 1 pt for noting the limit must exist / the domain caveat.)*

**A2.** For $f(x)=x^2-3x$:
$$\lim_{h\to0}\frac{(x+h)^2-3(x+h)-(x^2-3x)}{h}=\lim_{h\to0}\frac{2xh+h^2-3h}{h}=\lim_{h\to0}(2x+h-3)=2x-3.$$

**Answer:** $f'(x)=2x-3$

**A3.** $\operatorname{dom}(f)=[0,\infty)$ but $\operatorname{dom}(f')=(0,\infty)$, because
$f'(x)=\dfrac{1}{2\sqrt{x}}$.

They differ at $x=0$: there the difference quotient is
$\dfrac{\sqrt{h}}{h}=\dfrac{1}{\sqrt{h}}\to+\infty$, so the tangent is **vertical** and no finite
derivative exists — even though $f$ is continuous at $0$.

**A4.** **Differentiable at $a$ $\Rightarrow$ continuous at $a$.** The **converse is false**: a
function can be continuous but not differentiable (e.g. a corner).

**A5.** $f(x)=|x|$ is continuous at $0$ but not differentiable there — a **corner**: the one-sided
derivatives are $+1$ and $-1$, finite but unequal.
*(Also acceptable: $x^{2/3}$ — a cusp, or $x^{1/3}$ — a vertical tangent, provided the type is named.)*

*Marks: 10 / 10*

---

## Section B — Longer (5 pts each)

**B1.** Differentiability at the stated point:

**(a) $f(x)=|x-2|$ at $x=2$: not differentiable.** The one-sided difference quotients are
$$\frac{|2+h-2|}{h}=\frac{|h|}{h}=+1\;(h>0),\qquad -1\;(h<0).$$
Both are finite but unequal, so the two-sided limit does not exist. This is a **corner**.

**(b) $f(x)=x^{1/3}$ at $x=0$: not differentiable.** The difference quotient is
$$\frac{h^{1/3}}{h}=h^{-2/3},$$
which diverges to $+\infty$ from **both** sides. The function is continuous at $0$ but has a
**vertical tangent** — no finite slope. ($+\infty$ is not a derivative.)

**Answer:** Neither is differentiable: (a) corner, (b) vertical tangent.

*Marks: 5 / 5*

---

**B2.** Find $a,b$ making $f(x)=\begin{cases}x^2,&x\le1\\ ax+b,&x>1\end{cases}$ differentiable at $x=1$.

Two conditions are needed.

**1. Continuity** (necessary, since differentiability implies continuity): the pieces must meet at
$x=1$, so
$$1^2=a(1)+b \;\Longrightarrow\; a+b=1.$$

**2. Matching slopes** (the derivative itself must exist, so the one-sided derivatives agree). Left
piece: $(x^2)'=2x$, giving $2$ at $x=1$. Right piece: $(ax+b)'=a$. Hence $a=2$.

Then $a+b=1$ gives $b=1-2=-1$.

**Answer:** $a=2,\ b=-1$.

*Marks: 5 / 5*

---

## Grading Summary

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-10-19 |

**Feedback:**
All correct per answer key.

- **A1:** Quotient correct with the domain/existence caveat.
- **A2:** Expansion and cancellation carried out correctly to $2x-3$.
- **A3:** Domains stated with the vertical-tangent reason for the difference at $0$.
- **A4:** Implication and the failure of its converse both given.
- **A5:** Corner named with the unequal one-sided derivatives.
- **B1:** Both cases diagnosed from the one-sided quotients, with corner and vertical tangent named;
  correctly rejects "$+\infty$" as a derivative.
- **B2:** Both the continuity and slope-matching conditions used, yielding $a=2,\ b=-1$.
