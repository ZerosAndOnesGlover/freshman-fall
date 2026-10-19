---
assessment: Lab 3
course: MATH 141
component: Labs
possible: 100
score: 100
status: graded
started: 2026-10-16
submitted: 2026-10-19
graded: 2026-10-19
source: "LAB 03 Derivative Exploration.md"
---

# MATH 141 · Lab 3
## Answer Sheet

**Assessment:** `LAB 03 Derivative Exploration.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

The program used throughout is saved alongside this sheet as `lab03.py`.

---

### Question 1  (10 points)

**Your answer:**

Running `forward` for $f(x)=x^2$ at $a=2$:

| $h$ | slope $\dfrac{f(2+h)-f(2)}{h}$ |
|---|---|
| $1$ | $5.0$ |
| $0.1$ | $4.100000000000001$ |
| $0.01$ | $4.009999999999891$ |
| $-0.01$ | $3.9899999999999824$ |

The slopes approach **$4$** — from above when $h>0$ and from below when $h<0$.

From the definition:
$$\frac{(2+h)^2-4}{h}=\frac{4+4h+h^2-4}{h}=\frac{4h+h^2}{h}=4+h \xrightarrow[h\to0]{} 4.$$

The symbolic cancellation ($4+h\to4$) and the numerical trend are the same fact: the secant
slope differs from the tangent slope by exactly $h$.

*Marks: 10 / 10*

---

### Question 2  (10 points)

**Your answer:**

As the slider $h$ is dragged toward $0$ from either side, the secant line through $(2,4)$ and
$(2+h,\,(2+h)^2)$ rotates until it is indistinguishable from the **tangent line** at $(2,4)$.

Its slope tends to $4$, so the tangent line is
$$y = 4 + 4(x-2) \quad\Longleftrightarrow\quad y = 4x - 4.$$

The two-sided approach matters: for $h>0$ and $h<0$ the secant line approaches the same line,
which is why the two-sided limit — the derivative — exists.

*Marks: 10 / 10*

---

### Question 3  (8 points)

**Your answer:**

Reading $f(x)=x^3-3x$ straight off the graph:

- **Increasing** ($f'>0$): $x<-1$ and $x>1$.
- **Decreasing** ($f'<0$): $-1<x<1$.
- **Horizontal tangent** ($f'=0$): at about $x=-1$ and $x=1$ (the local maximum and minimum).

*Marks: 8 / 8*

---

### Question 4  (12 points)

**Your answer:**

From the definition, with $f(x)=x^3-3x$:
$$
\begin{aligned}
f'(x)&=\lim_{h\to0}\frac{(x+h)^3-3(x+h)-\big(x^3-3x\big)}{h}\\
&=\lim_{h\to0}\frac{x^3+3x^2h+3xh^2+h^3-3x-3h-x^3+3x}{h}\\
&=\lim_{h\to0}\frac{3x^2h+3xh^2+h^3-3h}{h}\\
&=\lim_{h\to0}\big(3x^2+3xh+h^2-3\big)=3x^2-3.
\end{aligned}
$$
Setting $f'(x)=0$: $3x^2-3=0\Rightarrow x^2=1\Rightarrow x=\pm1$ **exactly**.

Graphed together, the zeros of $f'$ sit directly below the turning points of $f$, and the sign of
$f'$ matches Question 3:

| On $f$ | On $f'$ |
|---|---|
| increasing | $f'>0$ (above the axis) |
| decreasing | $f'<0$ (below the axis) |
| turning point | $f'$ **crosses** zero |

So the graph-reading and the algebra agree.

*Marks: 12 / 12*

---

### Question 5  (10 points)

**Your answer:**

For $f(x)=|x|$ at $0$, the difference quotient is $\dfrac{|h|}{h}$:
$$\lim_{h\to0^-}\frac{|h|}{h}=-1,\qquad \lim_{h\to0^+}\frac{|h|}{h}=+1.$$

Both one-sided limits **exist and are finite**, but they **disagree**. Therefore the two-sided limit
does not exist and $f$ is **not differentiable at $0$**. This is a **corner**: as $h$ crosses zero the
secant slope flips between $+1$ and $-1$, and the graph has a sharp point at the origin.

*Marks: 10 / 10*

---

### Question 6  (10 points)

**Your answer:**

For $f(x)=x^{2/3}$ at $0$ the quotient is $\dfrac{h^{2/3}}{h}=h^{-1/3}$:
$$\lim_{h\to0^+}h^{-1/3}=+\infty,\qquad \lim_{h\to0^-}h^{-1/3}=-\infty.$$

The quotient is unbounded (and of opposite sign) on the two sides, so the limit fails to exist and
$x^{2/3}$ is **not differentiable at $0$**. In Desmos the graph comes down to the origin, turns and
goes back up with a sharp point; the tangent direction is **vertical**, so the tangent line itself has
no finite slope. This is a **cusp**.

*Marks: 10 / 10*

---

### Question 7  (10 points)

**Your answer:**

Here $f(x)=x^2$ for $x\le1$ and $f(x)=2x-1$ for $x>1$.

**Continuity at $1$:** $\displaystyle\lim_{x\to1^-}x^2=1$, $\displaystyle\lim_{x\to1^+}(2x-1)=1$, and
$f(1)=1^2=1$. All agree, so $f$ **is continuous at $1$**.

**One-sided derivatives at $1$** (using $f(1)=1$):

Left:
$$\lim_{h\to0^-}\frac{(1+h)^2-1}{h}=\lim_{h\to0^-}\frac{2h+h^2}{h}=\lim_{h\to0^-}(2+h)=2.$$

Right:
$$\lim_{h\to0^+}\frac{2(1+h)-1-1}{h}=\lim_{h\to0^+}\frac{2h}{h}=2.$$

The one-sided limits are equal, so $f$ **is differentiable at $1$**, with $f'(1)=2$.

Graphically the two pieces **join smoothly**: $y=2x-1$ is exactly the tangent line to $y=x^2$ at
$(1,1)$, so there is no corner. This is the subtle case — a piecewise join need not be a corner.

*Marks: 10 / 10*

---

### Question 8  (15 points)

**Your answer:**

With $f(x)=\sqrt{x}$ at $a=4$ (exact $f'(4)=\dfrac{1}{2\sqrt4}=0.25$), using forward and central
differences and errors $\big|\text{approx}-0.25\big|$:

| $h$ | Forward | Forward error | Central | Central error |
|---|---|---|---|---|
| $0.1$ | $0.2484567313$ | $1.543\times10^{-3}$ | $0.2500195366$ | $1.954\times10^{-5}$ |
| $0.01$ | $0.2498439450$ | $1.561\times10^{-4}$ | $0.2500001953$ | $1.953\times10^{-7}$ |
| $0.001$ | $0.2499843770$ | $1.562\times10^{-5}$ | $0.2500000020$ | $1.953\times10^{-9}$ |

**The central difference is far more accurate for the same $h$:** about $80$ times better at
$h=0.1$ and about $8000$ times better at $h=0.001$.

**Error scaling.** Each time $h$ shrinks by a factor of $10$:

- the **forward** error shrinks by a factor of $10$ (it is proportional to $h$);
- the **central** error shrinks by a factor of $100$ (it is proportional to $h^2$).

*Marks: 15 / 15*

---

### Question 9  (15 points)

**Your answer:**

With $h=10^{-15}$ the two formulas give:

| $h$ | Forward | Forward error | Central | Central error |
|---|---|---|---|---|
| $10^{-15}$ | $0.0$ | $0.25$ | $0.1110223025$ | $0.1389776975$ |

Both are badly wrong — the forward difference returns exactly $0.0$ and the central one is not even
close.

**What went wrong.** In floating point, `math.sqrt(4 + 1e-15)` rounds to exactly `2.0`, because
$4 + 10^{-15}$ is indistinguishable from $4$ at double precision. The numerator
$\sqrt{4+h}-\sqrt{4}$ is then a difference of two nearly equal numbers, so almost all significant
digits cancel — the **catastrophic cancellation** seen in Lab 01. Dividing this tiny, contaminated
numerator by a tiny $h$ magnifies whatever round-off survived, so the result carries no accuracy at
all.

**Is "make $h$ as small as possible" good advice?** No. There are two competing errors: the
*formula* error (forward $\sim h$, central $\sim h^2$), which shrinks as $h$ shrinks, and the
*round-off* error (forward and central both $\sim \varepsilon_{\text{mach}}/h$), which **grows** as $h$
shrinks. The total error is minimised at some intermediate $h$; driving $h$ to $10^{-15}$ lets
round-off dominate completely.

*Marks: 15 / 15*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-19 |

**Feedback:**
All nine questions correct and complete; all numerical values match the key.

- **Part 1 (Q1–Q2):** Forward-difference table reproduced exactly, approach to $4$ confirmed by
  simplification to $4+h$, and the secant identified with the tangent line $y=4x-4$.
- **Part 2 (Q3–Q4):** Monotonicity and turning points read correctly; $f'(x)=3x^2-3$ derived from the
  definition with the zeros $x=\pm1$ matching the turning points and the sign of $f'$.
- **Part 3 (Q5–Q7):** Corner, cusp and the smooth join each diagnosed with both one-sided quotients.
  Q7 correctly recognises the piecewise join as differentiable — the subtle case.
- **Part 4 (Q8–Q9):** Central vs forward accuracy and the $10\times$/$100\times$ error scaling are
  correct, and Q9 explains catastrophic cancellation and the sweet spot in $h$ rather than just
  reporting the wrong output.

No errors. Full marks.
