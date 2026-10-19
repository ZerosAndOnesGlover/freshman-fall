---
assessment: PS 1
course: MATH 141
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-01
submitted: 2026-10-07
graded: 2026-10-09
source: "Problem Set 1.md"
---

# MATH 141 · PS 1
## Answer Sheet

**Assessment:** `Problem Set 1.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Problem 1 — Algebraic Limits  (18 points)

**Your answer:**

**(a)** $\displaystyle\lim_{x \to -2} \frac{x^2 + 5x + 6}{x^2 - x - 6}$

Factor numerator and denominator (both are $0$ at $x = -2$, so $(x+2)$ is a common factor):

$$= \lim_{x \to -2} \frac{(x+2)(x+3)}{(x+2)(x-3)} = \lim_{x \to -2} \frac{x+3}{x-3} = \frac{-2+3}{-2-3} = -\frac{1}{5}.$$

The cancellation is valid because $x \neq -2$ in the limit process. **Answer:** $\boxed{-\tfrac{1}{5}}$

**(b)** $\displaystyle\lim_{x \to 0} \frac{\sqrt{4+x}-2}{x}$ — rationalize the numerator by $\dfrac{\sqrt{4+x}+2}{\sqrt{4+x}+2}$:

$$= \lim_{x \to 0} \frac{(4+x)-4}{x(\sqrt{4+x}+2)} = \lim_{x \to 0} \frac{x}{x(\sqrt{4+x}+2)} = \lim_{x \to 0} \frac{1}{\sqrt{4+x}+2} = \frac{1}{\sqrt{4}+2} = \frac{1}{4}.$$

The final function is continuous at $0$, so substitution is now valid. **Answer:** $\boxed{\tfrac{1}{4}}$

**(c)** For $x < 1$, $|x-1| = -(x-1)$, so $\dfrac{|x-1|}{x-1} = -1$; hence $\displaystyle\lim_{x\to1^-}\frac{|x-1|}{x-1} = -1$.

For $x > 1$, $|x-1| = x-1$, so $\dfrac{|x-1|}{x-1} = 1$; hence $\displaystyle\lim_{x\to1^+}\frac{|x-1|}{x-1} = 1$.

Since the one-sided limits differ ($-1 \neq 1$), the two-sided limit **does not exist**. **Answer:** $\boxed{-1,\; 1;\ \text{two-sided limit DNE}}$

*Marks: 18 / 18*

---

### Problem 2 — Limits at Infinity  (12 points)

**Your answer:**

**(a)** Divide numerator and denominator by the highest power $x^4$:

$$\lim_{x \to \infty} \frac{6x^4 - 3x^2 + 7}{2x^4 + x^3 - 5} = \lim_{x \to \infty} \frac{6 - 3/x^2 + 7/x^4}{2 + 1/x - 5/x^4} = \frac{6 - 0 + 0}{2 + 0 - 0} = 3.$$

(Equal degrees ⇒ ratio of leading coefficients.) **Answer:** $\boxed{3}$

**(b)** Multiply by $\dfrac{\sqrt{x^2+x}+x}{\sqrt{x^2+x}+x}$:

$$\lim_{x \to \infty}\left(\sqrt{x^2+x}-x\right) = \lim_{x \to \infty} \frac{(x^2+x)-x^2}{\sqrt{x^2+x}+x} = \lim_{x \to \infty} \frac{x}{\sqrt{x^2+x}+x}.$$

Divide numerator and denominator by $x$ (positive for large $x$):

$$= \lim_{x \to \infty} \frac{1}{\sqrt{1 + 1/x} + 1} = \frac{1}{\sqrt{1+0}+1} = \frac{1}{2}.$$

**Answer:** $\boxed{\tfrac{1}{2}}$

*Marks: 12 / 12*

---

### Problem 3 — The Squeeze Theorem  (10 points)

**Your answer:**

The bounding functions come from $-1 \le \cos\theta \le 1$ for every real $\theta$. Taking $\theta = 1/x^2$
(for $x \neq 0$) and multiplying through by $x^2 > 0$:

$$-x^2 \;\le\; x^2\cos\!\left(\frac{1}{x^2}\right) \;\le\; x^2.$$

The outer functions both tend to $0$:

$$\lim_{x\to0}\left(-x^2\right) = 0 = \lim_{x\to0} x^2.$$

Both bounds are equal, so by the **Squeeze Theorem** the middle function is forced to the same limit.
**Answer:** $\boxed{0}$

*Marks: 10 / 10*

---

### Problem 4 — Trigonometric Limits  (12 points)

**Your answer:**

**(a)** Force the special limit $\dfrac{\sin u}{u}\to 1$ by multiplying and dividing by $7x$:

$$\lim_{x\to0}\frac{\sin 7x}{4x} = \frac{7}{4}\lim_{x\to0}\frac{\sin 7x}{7x} = \frac{7}{4}\cdot 1 = \frac{7}{4}.$$

(As $x\to0$, $u = 7x\to0$, so $\frac{\sin 7x}{7x}\to1$.) **Answer:** $\boxed{\tfrac{7}{4}}$

**(b)** Write $\tan 5x = \dfrac{\sin 5x}{\cos 5x}$ and regroup into known limits:

$$\lim_{x\to0}\frac{\tan 5x}{\sin 2x} = \lim_{x\to0}\frac{\sin 5x}{\cos 5x \cdot \sin 2x}
= \lim_{x\to0}\left[\frac{\sin 5x}{5x}\cdot\frac{2x}{\sin 2x}\cdot\frac{5x}{2x\cos 5x}\right].$$

The first two factors tend to $1$ and the third to $\dfrac{5}{2\cdot 1} = \dfrac{5}{2}$:

$$= 1 \cdot 1 \cdot \frac{5}{2} = \frac{5}{2}.$$

**Answer:** $\boxed{\tfrac{5}{2}}$

*Marks: 12 / 12*

---

### Problem 5 — Making a Limit Exist  (12 points)

**Your answer:**

Compute the one-sided limits at $x = 2$. For the left piece ($x < 2$):

$$\lim_{x\to2^-} g(x) = \lim_{x\to2^-}(ax+3) = 2a + 3.$$

For the right piece ($x \ge 2$):

$$\lim_{x\to2^+} g(x) = \lim_{x\to2^+}(x^2 - a) = 4 - a.$$

The two-sided limit exists exactly when the one-sided limits agree:

$$2a + 3 = 4 - a \;\Longrightarrow\; 3a = 1 \;\Longrightarrow\; a = \frac{1}{3}.$$

For this $a$, the limit is $\displaystyle\lim_{x\to2}g(x) = 2\cdot\tfrac{1}{3} + 3 = \tfrac{11}{3}$.

For every other $a$ the one-sided limits differ, so the limit does not exist.
**Answer:** $\boxed{a = \tfrac{1}{3},\quad \lim_{x\to2}g(x) = \tfrac{11}{3}}$

*Marks: 12 / 12*

---

### Problem 6 — An ε-δ Proof, Linear  (12 points)

**Your answer:**

*Scratch work:* $\big|(3x-7) - 8\big| = |3x - 15| = 3|x-5|$. We need $3|x-5| < \varepsilon$, which holds if
$|x - 5| < \varepsilon/3$. So take $\delta = \varepsilon/3$.

*Proof.* Given $\varepsilon > 0$, let $\delta = \dfrac{\varepsilon}{3} > 0$. Suppose $0 < |x - 5| < \delta$. Then

$$\big|(3x-7) - 8\big| = |3x - 15| = 3|x - 5| < 3\delta = 3\cdot\frac{\varepsilon}{3} = \varepsilon.$$

Since for every $\varepsilon > 0$ such a $\delta$ exists, $\displaystyle\lim_{x\to5}(3x-7) = 8$. $\blacksquare$

*Marks: 12 / 12*

---

### Problem 7 — An ε-δ Proof, Quadratic  (14 points)

**Your answer:**

*Scratch work:* $|x^2 - 9| = |x-3|\,|x+3|$. Restrict $\delta \le 1$ first: then $|x-3| < 1$ gives
$2 < x < 4$, so $5 < x + 3 < 7$ and hence $|x+3| < 7$. We need $|x-3|\cdot 7 < \varepsilon$, i.e.
$|x - 3| < \varepsilon/7$. So take $\delta = \min\!\left(1, \dfrac{\varepsilon}{7}\right)$.

*Proof.* Given $\varepsilon > 0$, let $\delta = \min\!\left(1, \dfrac{\varepsilon}{7}\right) > 0$. Suppose
$0 < |x - 3| < \delta$. Since $\delta \le 1$, we have $|x-3| < 1$, so $2 < x < 4$ and therefore
$5 < x + 3 < 7$, giving $|x + 3| < 7$. Then

$$|x^2 - 9| = |x-3|\,|x+3| < \delta \cdot 7 \le \frac{\varepsilon}{7}\cdot 7 = \varepsilon,$$

using $\delta \le \varepsilon/7$. Hence $\displaystyle\lim_{x\to3}x^2 = 9$. $\blacksquare$

*Marks: 14 / 14*

---

### Problem 8 — What a Limit Ignores  (10 points)

**Your answer:**

The student is **not** correct. $\displaystyle\lim_{x\to2}f(x)$ describes the values $f(x)$ takes for
$x$ **near** $2$ but with $x \neq 2$ — the limit ignores $f(2)$ entirely. A limit depends only on the
behaviour of $f$ on a punctured neighbourhood of $2$; the value at the point is irrelevant. (Whether
$f$ is continuous at $2$ is exactly the extra condition that $f(2)$ also exists *and* equals the limit.)

Counterexample:

$$f(x) = \begin{cases} x & x \neq 2 \\ 5 & x = 2 \end{cases}$$

Here $f(2) = 5$, but for $x$ near $2$ with $x \neq 2$, $f(x) = x \to 2$. So $\displaystyle\lim_{x\to2}f(x) = 2 \neq 5$.

*Marks: 10 / 10*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-09 |

**Feedback:**
All 8 problems correct and fully justified.

- **P1:** Both algebraic limits factored/rationalized correctly, and the removable factors explicitly
  cancelled with the reason ($x \neq -2$); the absolute-value one-sided limits are computed and the
  non-existence of the two-sided limit stated.
- **P2:** Highest-degree division for (a); conjugate for (b) with the correct division by $x > 0$ and
  the resulting $1/2$.
- **P3:** Bounding functions stated, both outer limits verified equal to $0$, Squeeze Theorem invoked.
- **P4:** Special limit forced correctly; (b) regrouped into $\sin u/u$ factors, giving $5/2$.
- **P5:** Both one-sided limits in terms of $a$, equation solved, $a = 1/3$ and limit value $11/3$; noted
  that all other $a$ give DNE.
- **P6–P7:** ε-δ proofs follow the required structure — begin "Given $\varepsilon > 0$", state $\delta$
  ($\varepsilon/3$; $\min(1,\varepsilon/7)$), verify the implication, quantifier order correct.
- **P8:** Correct verdict, clear statement of what the limit depends on, valid piecewise counterexample.

No errors. Full marks.
