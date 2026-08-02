# MATH 141 — Calculus I
## Quiz 08 (Monday, Week 8 — Start of Class)
### Covers: Week 7 — Shape of a Graph, Curve Sketching, Applied Optimization

**Time:** 15 minutes | **Closed book, closed notes**
**Name:** _________________________________ | **Section:** _______

---

**Q1 (4 pts).** For $f(x) = x^4 - 6x^2$, find the intervals of concavity and all inflection points.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

**Q2 (4 pts).** For $f(x) = x^2e^{-x}$, find all critical numbers and classify each using the Second Derivative Test.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

**Q3 (4 pts).** For $f(x) = \dfrac{x}{x^2+1}$, find all vertical and horizontal asymptotes.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

**Q4 (4 pts).** An open-top box is formed from a square piece of cardboard with side $20$ cm by cutting equal squares of side $x$ from each corner and folding up the sides. Write the volume $V(x)$ as a function of $x$, and state the domain.

*(You do not need to solve for the maximum — just set up the function and domain.)*

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

**Q5 (4 pts).** True or False (no justification required, but be careful):

(a) _____ If $f''(c)=0$, then $f$ has an inflection point at $c$.

(b) _____ A function can cross its own horizontal asymptote.

(c) _____ In an applied optimization problem, a critical point must still be verified as a maximum or minimum.

(d) _____ A rational function's vertical asymptotes always occur where the denominator is zero.

---

*Total: 20 pts*

---
---

# Quiz 08 — ANSWER KEY (INSTRUCTOR ONLY)

---

**Q1.** $f'(x)=4x^3-12x$; $f''(x)=12x^2-12=12(x^2-1)$

Zero at $x=\pm1$. Sign: $+$ for $\lvert x\rvert>1$, $-$ for $\lvert x\rvert<1$.

**Concave up:** $(-\infty,-1)\cup(1,\infty)$. **Concave down:** $(-1,1)$.

**Inflection points:** $x=\pm1$, where $f(1)=1-6=-5$ and $f(-1)=-5$ ($f$ is even).

Points: $(1,-5)$ and $(-1,-5)$.

*(Verified numerically: $f''(0)=-12$, and $f''$ passes through zero at $x=\pm1$.)*

*Grading: 1 pt second derivative, 1 pt zeros of $f''$, 1 pt concavity intervals, 1 pt inflection **points** — the question asks for points, so an answer of "$x=\pm1$" with no $y$-values loses that mark.*

---

**Q2.** $f(x)=x^2e^{-x}$

$f'(x)=2xe^{-x}+x^2(-e^{-x})=e^{-x}(2x-x^2)=xe^{-x}(2-x)$

Critical numbers: $x=0$, $x=2$ (note $e^{-x}$ is never zero).

$f''(x)=-e^{-x}(2x-x^2)+e^{-x}(2-2x)=e^{-x}(x^2-4x+2)$

| $c$ | $f''(c)$ | Conclusion |
|---|---|---|
| $0$ | $e^0(2)=2>0$ | **local minimum** |
| $2$ | $e^{-2}(4-8+2)=-2e^{-2}<0$ | **local maximum** |

*(Verified numerically: $f'(0)=f'(2)=0$; $f''(0)=2.000000$, $f''(2)=-0.270671=-2e^{-2}$.)*

*Grading: 2 pts finding both critical numbers, 2 pts applying the Second Derivative Test to both.
A common error is cancelling $e^{-x}$ from $f'$ and losing $x=0$.*

---

**Q3.** $f(x)=\dfrac{x}{x^2+1}$

Vertical asymptotes: denominator $x^2+1\ge1$ is never zero — **no vertical asymptotes**.

Horizontal: $\displaystyle\lim_{x\to\pm\infty}\frac{x}{x^2+1}=\lim_{x\to\pm\infty}\frac{1/x}{1+1/x^2}=0$. **Horizontal asymptote $y=0$** (both directions).

*Grading: 2 pts correctly identifying that there is no VA, 2 pts correct HA. Students who assert a
vertical asymptote "wherever the denominator could vanish" without checking that it can are the
target of this question.*

---

**Q4.** Base side after folding: $20-2x$. Height: $x$.

$$V(x)=x(20-2x)^2$$

Domain: $0<x<10$

*Grading: 2 pts correct volume formula, 2 pts correct domain. The domain is the real content —
$x\le0$ and $x\ge10$ give no box at all. An answer of "$x>0$" earns 1 of the 2.*

---

**Q5.** *(1 pt each)*

(a) **False** — $f''(c)=0$ is necessary, not sufficient. For $f(x)=x^4$ at $c=0$, $f''(0)=0$ but the
curve is concave up on both sides, so there is no inflection. The **sign must change**.

(b) **True** — an asymptote governs behaviour only in the limit. $f(x)=\dfrac{x}{x^2+1}$ from Q3 has
horizontal asymptote $y=0$ and equals $0$ at $x=0$, crossing it exactly once.

(c) **True** — a critical point is a candidate. The Closed Interval Method, a derivative test, or a
physical argument must confirm it.

(d) **False** — only if the numerator is nonzero there. Otherwise the factor may cancel, giving a
removable discontinuity (a hole) rather than an asymptote.

*Items (a), (b) and (d) all test the same habit: a necessary condition is not a sufficient one.*
