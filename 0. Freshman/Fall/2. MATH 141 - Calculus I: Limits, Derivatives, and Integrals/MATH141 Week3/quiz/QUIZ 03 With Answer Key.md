# MATH 141 — Calculus I
## Quiz 03 (Monday, Week 3 — Start of Class)
### Covers: Week 2 — Continuity, Types of Discontinuity, and the IVT

**Time:** 15 minutes | **Closed book, closed notes**
**Name:** _________________________________ | **Section:** _______

---

**Q1 (4 pts).** Let $f(x) = \begin{cases} x^2 + 1 & x \leq 1 \\ 3x - 1 & x > 1 \end{cases}$

Is $f$ continuous at $x = 1$? Use the three-part definition. Show all work.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

**Q2 (4 pts).** Classify the discontinuity at the stated point as removable, jump, infinite, or essential. One word each, but be sure it is the right one.

(a) $\dfrac{x^2-x-6}{x-3}$ at $x=3$ &nbsp;&nbsp;&nbsp; (b) $\dfrac{x+2}{x-3}$ at $x=3$

&nbsp;

&nbsp;

&nbsp;

---

**Q3 (4 pts).** For the function in Q2(a), write the continuous extension explicitly.

&nbsp;

&nbsp;

&nbsp;

---

**Q4 (4 pts).** Use the Intermediate Value Theorem to show that $f(x) = x^3 + 2x - 5$ has a root in the interval $(1, 2)$. State all hypotheses explicitly, and state what the IVT does **not** tell you.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

**Q5 (4 pts).** Starting from the bracket $[1,2]$ in Q4, carry out **two** steps of bisection on $f(x)=x^3+2x-5$. Report the bracket after each step.

&nbsp;

&nbsp;

&nbsp;

---

*Total: 20 pts*

---
---

# Quiz 03 — ANSWER KEY (INSTRUCTOR ONLY — DO NOT DISTRIBUTE)

---

**Q1.** Check three conditions:

1. $f(1) = 1^2+1 = 2$ ✓ (defined)
2. $\lim_{x\to1^-}f(x) = 1+1 = 2$; $\lim_{x\to1^+}f(x) = 3-1 = 2$. Both equal, so $\lim_{x\to1}f(x) = 2$ ✓ (limit exists)
3. $\lim_{x\to1}f(x) = 2 = f(1)$ ✓

All three conditions hold. **$f$ is continuous at $x=1$.**

*Grading: 1 pt each condition, 1 pt conclusion. Students who compute only the two one-sided limits
and stop have skipped condition 3 — which happens to hold here, but they did not check it.*

---

**Q2.** *(2 pts each)*

**(a) Removable.** $\dfrac{(x-3)(x+2)}{x-3}=x+2$ for $x\ne3$, so the limit is $5$ — it exists, but
$f(3)$ is undefined.

**(b) Infinite.** The numerator at $x=3$ is $5\ne0$ while the denominator vanishes, so the one-sided
limits are $\mp\infty$. Vertical asymptote.

*This pair is the point of the question: **both are $\tfrac{\text{something}}{0}$ at $x=3$**, and only
factoring distinguishes them. A student who answers "removable" to both has learned the wrong rule.*

---

**Q3.** $$\tilde f(x)=\begin{cases}\dfrac{x^2-x-6}{x-3},& x\ne3\\[6pt] 5,& x=3\end{cases}$$

Equivalently, $\tilde f(x)=x+2$ for all $x$.

*Grading: 2 pts for the value $5$, 2 pts for writing an actual piecewise definition (or the
equivalent single formula). "Define $f(3)=5$" alone earns 3 — the extension must be written down.*

---

**Q4.** $f(x)=x^3+2x-5$ is a polynomial, hence **continuous on $[1,2]$** — hypothesis 1.

$f(1)=1+2-5=-2<0$ and $f(2)=8+4-5=7>0$, so $0$ lies strictly between $f(1)$ and $f(2)$ — hypothesis 2.

By the IVT there exists $c\in(1,2)$ with $f(c)=0$. $\square$

**What the IVT does not tell you:** where the root is, how many roots there are, or any method of
finding one. It is a pure existence statement.

*(The root is in fact $1.328268855669$, and it is unique — but uniqueness needs $f'>0$, which is
Week 6, not the IVT.)*

*Grading: 1 pt continuity, 1 pt the two sign computations, 1 pt citing the IVT correctly, 1 pt the
"does not tell you" part. That last mark is the one most often lost.*

---

**Q5.** Verified trace:

| Step | Bracket in | Midpoint | $f(\text{mid})$ | Bracket out |
|---|---|---|---|---|
| 1 | $[1,2]$ | $1.5$ | $+1.375000$ | $[1,\;1.5]$ |
| 2 | $[1,1.5]$ | $1.25$ | $-0.546875$ | $[1.25,\;1.5]$ |

After two steps the root is bracketed in $[1.25,\,1.5]$, of width $0.25$.

*Grading: 2 pts per step (midpoint and the sign decision). The decision rule is what is being tested:
keep the half on which $f$ changes sign. A student who keeps $[1.5,2]$ at step 1 has the rule
backwards — $f(1.5)>0$ and $f(2)>0$, no sign change there.*
