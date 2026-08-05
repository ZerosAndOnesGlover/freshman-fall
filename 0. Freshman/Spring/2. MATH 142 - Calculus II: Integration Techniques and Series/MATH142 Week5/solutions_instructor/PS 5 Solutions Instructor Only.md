# MATH 142 · Calculus II
## Problem Set 5 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every value verified symbolically.

> **Marking philosophy.** This week the **limits of integration are the assessment.** A correct
> integrand over the wrong range is the characteristic error, and it produces a plausible number —
> often exactly twice or four times the right one. **Check ranges before checking arithmetic.**

---

## Part A — Parametric Curves (5 pts each)

### A1 (5) — $x=3\cos t$, $y=2\sin t$

$\frac x3=\cos t$, $\frac y2=\sin t$, so

$$\boxed{\frac{x^2}{9}+\frac{y^2}{4}=1}$$

— an ellipse with semi-axes 3 and 2. **Traced anticlockwise**, starting at $(3,0)$ when $t=0$, exactly once over $[0,2\pi]$.

*Marking: 3 for the equation, **2 for orientation and starting point** (the question asked).*

### A2 (5) — $x=t^2-2t$, $y=t+1$

From the second, $t=y-1$. Substituting:

$$x = (y-1)^2-2(y-1) = y^2-4y+3$$

$$\boxed{x = y^2-4y+3}$$

— a parabola opening in the $+x$ direction, vertex at $(-1,2)$.

*Marking: 5. Solving from the $y$ equation is the point; students who tried the quadratic in $t$ from the $x$ equation get there too but with a square root and a branch problem — award full marks but note the easier route.*

### A3 (5) — $x=e^t$, $y=e^{2t}$

$y = (e^t)^2 = x^2$. **But** $x=e^t>0$ always, so

$$\boxed{y=x^2,\quad \textbf{restricted to } x>0}$$

*Marking: 3 for $y=x^2$, **2 for the restriction $x>0$.** This is the "elimination loses information" point from Lecture 1 §4, and it was flagged in the question.*

### A4 (5) — self-intersection of $x=t^3-3t$, $y=t^2-1$

**Same $y$:** $t_1^2 = t_2^2$ with $t_1\ne t_2$ forces $t_2=-t_1$.

**Same $x$:** $t_1^3-3t_1 = -t_1^3+3t_1 \implies 2t_1^3 = 6t_1 \implies t_1(t_1^2-3)=0$.

$t_1=0$ gives $t_2=0$ — not distinct. So $t_1=\sqrt3$, $t_2=-\sqrt3$, and

$$x = 3\sqrt3-3\sqrt3 = 0,\qquad y = 3-1=2$$

$$\boxed{t=\pm\sqrt3, \text{ crossing at } (0,2)}$$

*Verified symbolically.*

*Marking: 2 for using $y$ to get $t_2=-t_1$, 2 for solving, 1 for the point. **Discarding $t=0$ must be explicit** — it solves the equations but is not a crossing.*

---

## Part B — Calculus with Parametric Curves (6 pts each)

### B1 (6) — $\frac{dy}{dx}$ at $t=2$ for $(t^2,\ t^3-3t)$

$$\frac{dy}{dx} = \frac{3t^2-3}{2t}\Bigg|_{t=2} = \frac{12-3}{4} = \boxed{\frac94}$$

*Verified symbolically.*

### B2 (6) — tangents of $x=t^2-t$, $y=t^3-3t$

**Horizontal** ($\frac{dy}{dt}=3t^2-3=0$): $\boxed{t=\pm1}$

**Vertical** ($\frac{dx}{dt}=2t-1=0$): $\boxed{t=\tfrac12}$

*Verified symbolically.*

**Neither set overlaps**, so no cusp arises and both classifications stand. *A student who checked that is doing it properly — award a comment.*

*Marking: 3 + 3. **Deduct 2 for swapping the two conditions**, which is the standard error.*

### B3 (6) — arc length of $(t^2,\ t^3)$ on $[0,1]$

Speed $=\sqrt{4t^2+9t^4} = t\sqrt{4+9t^2}$ (positive on $[0,1]$):

$$L = \int_0^1 t\sqrt{4+9t^2}\,dt = \frac{1}{27}\Big[(4+9t^2)^{3/2}\Big]_0^1 = \boxed{\frac{13\sqrt{13}-8}{27}}\approx1.4397$$

*Verified symbolically.*

**The relationship to Week 4:** eliminating the parameter gives $y^2=x^3$, i.e. $y=x^{3/2}$ — and $t\in[0,1]$ corresponds to $x\in[0,1]$. **It is the same curve over the same interval, so the lengths must agree**, and Week 4's answer was $\frac{13\sqrt{13}-8}{27}$. *(Verified: identical.)*

*Marking: 4 for the length, **2 for the explanation.** The explanation must identify the curve as $y=x^{3/2}$ and check the interval corresponds — "they look the same" earns 1.*

### B4 (6) — area under one cycloid arch ($a=1$)

$$A = \int_0^{2\pi}(1-\cos t)(1-\cos t)\,dt = \int_0^{2\pi}\big(1-2\cos t+\cos^2t\big)dt = 2\pi-0+\pi = \boxed{3\pi}$$

*Verified symbolically.*

*Marking: 2 setup, 4 evaluation. **$\int_0^{2\pi}\cos^2 = \pi$, not $2\pi$** — the standard slip.*

### B5 (6) — astroid first-quadrant arc, surface about the $x$-axis

Speed $=3a|\cos t\sin t| = 3a\cos t\sin t$ on $\left[0,\tfrac\pi2\right]$ (both factors non-negative).

$$S = 2\pi\int_0^{\pi/2} a\sin^3t\cdot3a\cos t\sin t\,dt = 6\pi a^2\int_0^{\pi/2}\sin^4t\cos t\,dt = 6\pi a^2\cdot\frac15$$

$$\boxed{S = \frac{6\pi a^2}{5}}$$

*Verified symbolically.*

*Marking: 2 speed, 2 setup, 2 evaluation. **Note the absolute value is harmless here** because the range is the first quadrant — say so, because it is *not* harmless over the full curve (see the astroid arc length in Lecture 2, Example 6).*

---

## Part C — Polar Coordinates (6 pts each)

### C1 (6) — area of $r=1-\sin\theta$

$$A = \frac12\int_0^{2\pi}(1-\sin\theta)^2d\theta = \frac12\int_0^{2\pi}\big(1-2\sin\theta+\sin^2\theta\big)d\theta = \frac12\big(2\pi-0+\pi\big) = \boxed{\frac{3\pi}{2}}$$

*Verified symbolically.*

**Same as the cardioid $r=1+\cos\theta$** — it is the same curve rotated, so the area must match. *A free check worth mentioning.*

### C2 (6) — one petal of $r=2\sin3\theta$

**Finding the range is the problem.** $r=0$ when $\sin3\theta=0$, i.e. $\theta = 0,\tfrac\pi3,\tfrac{2\pi}3,\ldots$ **The petal is traced as $\theta$ runs from $0$ to $\tfrac\pi3$** — the curve leaves the origin and returns to it.

$$A = \frac12\int_0^{\pi/3}4\sin^23\theta\,d\theta = 2\int_0^{\pi/3}\sin^23\theta\,d\theta = 2\cdot\frac\pi6 = \boxed{\frac\pi3}$$

*Verified symbolically. $\approx1.047$.*

*Marking: **3 of the 6 for the range, justified by $r=0$.** Integrating over $[0,2\pi]$ gives $2\pi$ — six times too much, since $r=2\sin3\theta$ is a 3-petalled rose traced twice. **A student reporting $2\pi$ has made exactly the error the question was set to catch.***

### C3 (6) — arc length of $r=\theta$ on $[0,\pi]$

$r'=1$, so $\sqrt{r^2+(r')^2} = \sqrt{\theta^2+1}$:

$$L = \int_0^\pi\sqrt{\theta^2+1}\,d\theta$$

This is the **trigonometric substitution** $\theta=\tan\phi$ from Week 2, giving $\int\sec^3$:

$$L = \frac{\pi\sqrt{1+\pi^2}}{2}+\frac{\operatorname{arcsinh}\pi}{2} \approx \boxed{6.110}$$

*Verified symbolically.*

*(Equivalently $\frac12\left[\pi\sqrt{1+\pi^2}+\ln\left(\pi+\sqrt{1+\pi^2}\right)\right]$ — both forms correct.)*

*Marking: 2 for the integrand, 4 for the evaluation. **Accept the $\ln$ form.***

### C4 (6) — $r=2a\cos\theta$, traced once

$r\ge0$ requires $\cos\theta\ge0$, i.e. $\boxed{\theta\in\left[-\tfrac\pi2,\tfrac\pi2\right]}$ — over which the full circle is traced exactly once.

**Over that range:**

$$A = \frac12\int_{-\pi/2}^{\pi/2}4a^2\cos^2\theta\,d\theta = 2a^2\cdot\frac\pi2\cdot\ldots = \boxed{\pi a^2}$$ ✓

**Over $[0,2\pi]$:** $\;A = 2\pi a^2$ — **exactly double.**

**The discrepancy:** on $\left(\tfrac\pi2,\tfrac{3\pi}2\right)$ we have $r<0$, and a negative $r$ traces *the same circle again* (since $(-r,\theta)=(r,\theta+\pi)$). **The formula $\frac12\int r^2$ has no way to notice** — $r^2$ is positive either way — so it counts every point twice.

*Verified symbolically: $\pi a^2$ and $2\pi a^2$.*

*Marking: 2 range, 2 both values, **2 for the explanation.** The explanation must invoke negative $r$ retracing the curve; "it goes round twice" without saying why earns 1.*

### C5 (6) — $r=4\sin\theta$

Multiply by $r$: $r^2 = 4r\sin\theta$, so $x^2+y^2=4y$, i.e.

$$\boxed{x^2+(y-2)^2 = 4}$$

— a **circle of radius 2 centred at $(0,2)$**, passing through the origin.

*Verified: the expansion matches.*

*Marking: 3 for the conversion, 2 for completing the square, 1 for identifying it. **The "multiply by $r$" step** is the technique.*

---

## Part D — Concept (10 pts each)

### D1 (10) — where the $\frac12$ comes from

**(a)** Slice the region **by angle**. A wedge from $\theta$ to $\theta+\Delta\theta$ is approximately a **circular sector** of radius $r=f(\theta)$ and angle $\Delta\theta$. Its area is the fraction $\frac{\Delta\theta}{2\pi}$ of the disc $\pi r^2$:

$$\frac{\Delta\theta}{2\pi}\cdot\pi r^2 = \frac12 r^2\Delta\theta$$

**The $\frac12$ is the sector's.** Summing and taking $\Delta\theta\to0$ gives $A=\frac12\int r^2d\theta$.

**(b)** The two are **different families of slices**. $\int y\,dx$ slices into **vertical rectangles**; $\frac12\int r^2d\theta$ slices into **wedges from the origin**. Both compute area, but they are different decompositions, and only the second has a factor of $\frac12$ because only the second uses sectors.

*(A student may correctly note that $\int y\,dx$ **can** be pushed through with $x=r\cos\theta$ and does give the right answer — but it produces a different integrand, and it is far more work. Award full marks and a comment.)*

**(c)** For $r\le a$: $A = \frac12\int_0^{2\pi}a^2d\theta = \frac12 a^2\cdot2\pi = \boxed{\pi a^2}$ ✓

*Marking: 5 + 3 + 2. **(a) must identify the sector explicitly.** Quoting the formula earns 1 of the 5.*

### D2 (10) — which curves have closed forms

**(a)** For the cycloid,

$$\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2 = a^2(1-\cos t)^2+a^2\sin^2t = a^2(2-2\cos t)$$

**The step where the root disappears:** $2-2\cos t = 4\sin^2\frac t2$, so the speed is $2a\left|\sin\frac t2\right| = 2a\sin\frac t2$ on $[0,2\pi]$.

$$L = \int_0^{2\pi}2a\sin\frac t2\,dt = \boxed{8a}$$

**(b)** $\displaystyle P = \int_0^{2\pi}\sqrt{a^2\sin^2t+b^2\cos^2t}\,dt$.

**(c)** The difference is **whether the expression under the root is a perfect square.**

- Cycloid: $2-2\cos t$ is, by a **half-angle identity**, exactly $4\sin^2\frac t2$ — a square of an elementary function, so the root cancels.
- Ellipse: $a^2\sin^2t+b^2\cos^2t = b^2 + (a^2-b^2)\sin^2 t$ is a **genuine quadratic in $\sin t$**, and when $a\ne b$ it is not a perfect square. No identity collapses it; the integral is **elliptic** and provably non-elementary.

**When $a=b$ the quadratic degenerates to the constant $a^2$**, the root becomes $a$, and the integral gives $2\pi a$ — which is why the circle is the only case that works.

**(d)** The cycloid is the harder-*looking* object by every superficial measure — no Cartesian equation, unknown before the 17th century, defined by a rolling motion — and it has an arc length of exactly $8a$. The ellipse is a conic section known for two thousand years, with area $\pi ab$, and its perimeter has no closed form at all.

**Which problems are tractable is a fact about the algebra of the resulting integrand, not about how complicated the object looks.** This is the same lesson as PS 4 C5, where $\int\sqrt{1+e^{2x}}$ looked hopeless and was elementary.

*Marking: 3 + 1 + 4 + 2. **(c) is the discriminating part** and must contrast "perfect square via an identity" with "genuine quadratic". "One is harder" earns 1 of the 4.*

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Parametrisation, elimination, self-intersection |
| B (5 × 6) | 30 | Slopes, tangents, arc length, area, surface |
| C (5 × 6) | 30 | Polar area, arc length, limits |
| D (2 × 10) | 20 | The sector derivation; tractability |
| **Total** | **100** | |

---

## Diagnostic Notes

| Question | Weakness | Bites in |
|---|---|---|
| **C2 / C4** | Integrating over the wrong range | Midterm 2 |
| **A3** | Not stating the restriction after elimination | Week 9 (intervals of convergence) |
| **B2** | Swapping the horizontal/vertical conditions | Midterm 2 |
| **D1(a)** | Memorising $\frac12$ rather than deriving it | Midterm 2 |

**Midterm 1 was this week and covered Weeks 0–4.** Once marked, the most useful feedback is a per-topic breakdown rather than a single score — **Week 6 begins a completely different subject**, and a student weak on integration technique will not be rescued by the change but will be able to keep up if they patch it now.

---

*MATH 142 · Week 5 · PS 5 Solutions · Instructor Only*
