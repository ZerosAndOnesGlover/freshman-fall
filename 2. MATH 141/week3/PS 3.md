---
assessment: PS 3
course: MATH 141
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-22
submitted: 2026-10-22
graded: 2026-10-22
source: "Problem Set 3.md"
---

# MATH 141 · PS 3
## Answer Sheet

**Assessment:** `Problem Set 3.md`
**Points available:** 100

---

### Problem 1 — Derivatives from the Definition  (24 points)

**Your answer:**

**(a)** $f(x)=4x^2-3x+1$.

$$\frac{f(x+h)-f(x)}{h}
=\frac{\bigl[4(x+h)^2-3(x+h)+1\bigr]-(4x^2-3x+1)}{h}$$
$$=\frac{4(x^2+2xh+h^2)-3x-3h+1-4x^2+3x-1}{h}
=\frac{8xh+4h^2-3h}{h}=8x+4h-3.$$
Letting $h\to0$,
$$\boxed{f'(x)=8x-3}.$$

**(b)** $f(x)=\dfrac{1}{2x+3}$, with $x\neq-\tfrac32$.

$$\frac{f(x+h)-f(x)}{h}
=\frac{1}{h}\left(\frac{1}{2(x+h)+3}-\frac{1}{2x+3}\right)
=\frac{(2x+3)-(2x+2h+3)}{h\,(2x+2h+3)(2x+3)}$$
$$=\frac{-2h}{h\,(2x+2h+3)(2x+3)}
=\frac{-2}{(2x+2h+3)(2x+3)}.$$
Letting $h\to0$,
$$\boxed{f'(x)=\frac{-2}{(2x+3)^2}},\qquad x\neq-\tfrac32.$$

**(c)** $f(x)=\sqrt{x+4}$, with $x>-4$. Rationalise the numerator:
$$\frac{f(x+h)-f(x)}{h}
=\frac{\sqrt{x+h+4}-\sqrt{x+4}}{h}\cdot
\frac{\sqrt{x+h+4}+\sqrt{x+4}}{\sqrt{x+h+4}+\sqrt{x+4}}$$
$$=\frac{(x+h+4)-(x+4)}{h\left(\sqrt{x+h+4}+\sqrt{x+4}\right)}
=\frac{h}{h\left(\sqrt{x+h+4}+\sqrt{x+4}\right)}
=\frac{1}{\sqrt{x+h+4}+\sqrt{x+4}}.$$
Letting $h\to0$,
$$\boxed{f'(x)=\frac{1}{2\sqrt{x+4}}},\qquad x>-4.$$

*Marks: 24 / 24*

---

### Problem 2 — Working Backwards  (10 points)

**Your answer:**

**(a)** Given $f(x+h)-f(x)=3x^2h+3xh^2+h^3$, the difference quotient is
$$\frac{f(x+h)-f(x)}{h}=\frac{3x^2h+3xh^2+h^3}{h}=3x^2+3xh+h^2.$$
Letting $h\to0$,
$$\boxed{f'(x)=3x^2}.$$

**(b)** The identity
$$(x+h)^3-x^3=3x^2h+3xh^2+h^3$$
has exactly the stated form, so $\boxed{f(x)=x^3}$ works. More generally any $f(x)=x^3+C$ works, since
the constant cancels in $f(x+h)-f(x)$.

*Marks: 10 / 10*

---

### Problem 3 — A Tangent Line  (12 points)

**Your answer:**

First compute $f'(x)$ from the definition for $f(x)=x^3$:
$$\frac{(x+h)^3-x^3}{h}
=\frac{x^3+3x^2h+3xh^2+h^3-x^3}{h}
=3x^2+3xh+h^2\;\longrightarrow\;3x^2,$$
so $f'(x)=3x^2$.

At $x=2$: the point of tangency is $(2,f(2))=(2,8)$, and the slope is
$$f'(2)=3(2)^2=12.$$
The tangent line is therefore
$$y-8=12(x-2)
\quad\Longrightarrow\quad
\boxed{y=12x-16}.$$

*Marks: 12 / 12*

---

### Problem 4 — A Tangent Through a Point  (8 points)

**Your answer:**

The point of tangency is $(1,f(1))=(1,4)$, and the tangent line also passes through $(4,10)$. A line
through these two points has slope
$$m=\frac{10-4}{4-1}=\frac{6}{3}=2.$$
The slope of the tangent at $x=1$ is by definition $f'(1)$, so
$$\boxed{f'(1)=2}.$$

*Marks: 8 / 8*

---

### Problem 5 — Velocity  (15 points)

**Your answer:**

Let $s(t)=t^2-6t+5$ metres, $t\ge0$ seconds.

**(a)** From the definition,
$$\frac{s(t+h)-s(t)}{h}
=\frac{\bigl[(t+h)^2-6(t+h)+5\bigr]-(t^2-6t+5)}{h}$$
$$=\frac{t^2+2th+h^2-6t-6h+5-t^2+6t-5}{h}
=\frac{2th+h^2-6h}{h}=2t+h-6.$$
Letting $h\to0$,
$$\boxed{v(t)=s'(t)=2t-6\ \text{m/s}}.$$

**(b)** The particle is at rest when $v(t)=0$:
$$2t-6=0\;\Longrightarrow\;t=3\ \text{s}.$$
Its position then is
$$s(3)=3^2-6(3)+5=9-18+5=-4\ \text{m}.$$
So it is at rest at $t=3$ s, at position $\boxed{-4\ \text{m}}$ (4 m in the negative direction from the
origin).

**(c)** Moving in the positive direction when $v(t)>0$:
$$2t-6>0\;\Longrightarrow\;t>3.$$
So the particle moves in the positive direction for $\boxed{t>3\ \text{s}}$ (and in the negative
direction for $0\le t<3$).

*Marks: 15 / 15*

---

### Problem 6 — Differentiability vs Continuity  (16 points)

**Your answer:**

**(a)** $f(x)=|x|$ at $x=0$.

*Continuity.* $\displaystyle\lim_{x\to0}|x|=0=f(0)$, so $f$ is **continuous** at $0$.

*Differentiability.* The difference quotient at $0$ is
$$\frac{f(0+h)-f(0)}{h}=\frac{|h|-0}{h}=\frac{|h|}{h}.$$
For $h>0$ this equals $1$; for $h<0$ it equals $-1$. Hence
$$\lim_{h\to0^-}\frac{|h|}{h}=-1,\qquad
\lim_{h\to0^+}\frac{|h|}{h}=1,$$
and the two one-sided limits differ, so the limit does not exist. Therefore $f$ is **not
differentiable** at $0$ (a corner).

**(b)** $f(x)=x|x|$ at $x=0$.

*Continuity.* Since $|x|\to0$ and $x\to0$ as $x\to0$, we have $x|x|\to0=f(0)$, so $f$ is
**continuous** at $0$.

*Differentiability.* At $0$,
$$\frac{f(0+h)-f(0)}{h}=\frac{h|h|-0}{h}=|h|.$$
As $h\to0$, $|h|\to0$, so the limit exists and equals $0$. Hence $f$ is **differentiable** at $0$, with
$$\boxed{f'(0)=0}.$$

*Marks: 16 / 16*

---

### Problem 7 — What "Slope at a Point" Means  (15 points)

**Your answer:**

The slope of a curve at a single point is not defined by two distinct points, so it is defined as a
**limit of secant slopes**. Take the fixed point $(3,9)$ on $y=x^2$ and a nearby point
$(3+h,(3+h)^2)$. The secant through them has slope
$$\frac{(3+h)^2-9}{(3+h)-3}=\frac{(3+h)^2-9}{h}.$$
As $h\to0$, the second point approaches $(3,9)$ along the curve, and the secant lines approach the
tangent line. The slope of the tangent at $x=3$ is therefore *defined* to be the limit of these secant
slopes:
$$\lim_{h\to0}\frac{(3+h)^2-9}{h}.$$
Saying "the slope at $x=3$ is $6$" is exactly the assertion that this limit equals $6$.

**Verification.** Expanding,
$$\frac{(3+h)^2-9}{h}=\frac{9+6h+h^2-9}{h}=\frac{6h+h^2}{h}=6+h\qquad(h\neq0).$$
Hence
$$\lim_{h\to0}\frac{(3+h)^2-9}{h}=\lim_{h\to0}(6+h)=6,$$
as claimed. (Equivalently, $f'(x)=2x$ from the definition, so $f'(3)=6$.)

*Marks: 15 / 15*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-22 |

**Feedback:**
All seven problems complete and correct, and every derivative is computed **from the limit definition**
rather than by rule, as the set requires.

- **P1:** All three difference quotients are set up and simplified correctly; the rationalisation in (c)
  is done properly, and domain restrictions ($x\neq-3/2$; $x>-4$) are stated.
- **P2:** The quotient simplifies to $3x^2+3xh+h^2$ and the limit is $3x^2$; $f(x)=x^3$ is identified,
  with the additive-constant freedom noted.
- **P3:** Expansion of $(x+h)^3$ is correct; tangent uses $f(2)=8$ and $f'(2)=12$, giving $y=12x-16$.
- **P4:** Correctly recognises the point of tangency $(1,4)$ and computes the two-point slope $2$.
- **P5:** Velocity from the definition is $2t-6$; rest at $t=3$ with $s(3)=-4$ m; positive motion for
  $t>3$, with the direction split stated.
- **P6:** Both continuity checks are explicit; $|x|$ is shown non-differentiable via the two one-sided
  limits $-1$ and $+1$, and $x|x|$ differentiable with $f'(0)=0$ via $|h|\to0$.
- **P7:** The secant-limit definition is explained precisely before the algebra, and the limit is
  evaluated correctly.
