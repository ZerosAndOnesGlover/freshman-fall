# MATH 141 — Calculus I
## Week 11 · Lecture 1 (Monday)
### Area Between Curves

---

**Reading:** Stewart §6.1 | Spivak Ch. 13

---

## From Area Under to Area Between

Week 8 interpreted $\int_a^b f$ as signed area between the curve and the $x$-axis. The generalisation
is immediate: replace the axis with another curve.

> **Definition.** If $f(x)\ge g(x)$ on $[a,b]$, the area of the region between them is
> $$A=\int_a^b\big[f(x)-g(x)\big]\,dx$$

The integrand is **(top) − (bottom)**, so it is non-negative and the result is a genuine area, not a
signed quantity. Setting $g=0$ recovers the Week 8 case.

**The Riemann-sum picture:** slice the region vertically into rectangles of width $\Delta x$ and
height $f(x_i^*)-g(x_i^*)$. Sum and take the limit.

---

## 1. The Standard Procedure

1. **Sketch.** Not optional — it determines which curve is on top and where the limits are.
2. **Find the intersections** by solving $f(x)=g(x)$. These are usually the limits of integration.
3. **Identify top and bottom** on each subinterval.
4. **Integrate** (top − bottom).

### Example: $y=x$ and $y=x^2$

They meet where $x=x^2$, i.e. $x=0$ and $x=1$. On $(0,1)$, $x > x^2$, so the line is on top:

$$A=\int_0^1(x-x^2)\,dx=\left[\frac{x^2}{2}-\frac{x^3}{3}\right]_0^1=\frac12-\frac13=\frac16$$

Verified: $0.1666666667$ ✓

### Example: $y=x^2$ and $y=2-x^2$

Intersections: $x^2=2-x^2 \Rightarrow x^2=1 \Rightarrow x=\pm1$. The downward parabola is on top:

$$A=\int_{-1}^{1}\big[(2-x^2)-x^2\big]dx=\int_{-1}^{1}(2-2x^2)\,dx=\frac83$$

Verified: $2.6666666667$ ✓

*(The integrand is **even**, so this is $2\int_0^1(2-2x^2)dx$ — Week 8's symmetry property saving
half the work.)*

---

## 2. When the Curves Cross

This is where marks are lost.

If $f$ and $g$ **swap places** inside $[a,b]$, a single integral of $f-g$ **cancels** the two
regions against each other and gives the wrong answer.

### The demonstration

$y=\sin x$ and $y=\cos x$ on $[0,\pi/2]$. They cross at $x=\pi/4$.

**Naive** (one integral, no split):

$$\int_0^{\pi/2}(\sin x-\cos x)\,dx = 0$$

Verified: $-0.0000000000$. **The area is not zero** — the region plainly has positive area. The two
halves cancelled exactly.

**Correct** (split at the crossing, taking top − bottom on each piece):

$$A=\int_0^{\pi/4}(\cos x-\sin x)\,dx+\int_{\pi/4}^{\pi/2}(\sin x-\cos x)\,dx$$

Verified: $0.8284271247$, which is exactly $2(\sqrt2-1)$ ✓

> **The rule.** Find **every** intersection in the interval, split there, and determine which curve
> is on top **on each piece separately**. Equivalently, integrate $\lvert f-g\rvert$ — the absolute
> value is doing the same job the split does.

This is Week 9's displacement-versus-distance distinction in geometric dress: $\int(f-g)$ is a signed
net quantity; $\int\lvert f-g\rvert$ is the area.

---

## 3. Integrating With Respect to $y$

Some regions are far easier described by horizontal slices. If the region is bounded on the right by
$x=r(y)$ and on the left by $x=\ell(y)$ for $c\le y\le d$:

$$A=\int_c^d\big[r(y)-\ell(y)\big]\,dy$$

**(right) − (left)**, sliced horizontally.

**When to switch.** If solving for $x$ in terms of $y$ is easier, or if a vertical slice would change
which curve bounds it partway up, use $dy$. The region bounded by $x=y^2$ and $x=y+2$ is a good
example: in $x$ it needs two integrals, in $y$ it needs one.

Intersections: $y^2=y+2 \Rightarrow y^2-y-2=0 \Rightarrow (y-2)(y+1)=0$, so $y=-1,2$.

$$A=\int_{-1}^{2}\big[(y+2)-y^2\big]dy=\left[\frac{y^2}{2}+2y-\frac{y^3}{3}\right]_{-1}^{2}=\frac{9}{2}$$

---

## Summary

| Idea | Takeaway |
|---|---|
| Area between curves | $\int_a^b(\text{top}-\text{bottom})\,dx$ |
| Limits | Usually the intersections; solve $f=g$ |
| **Sketch first** | It decides top/bottom and the limits |
| **Crossing curves** | Split at every crossing — verified: naive gives $0$ instead of $0.8284$ |
| Equivalently | $\int\lvert f-g\rvert$ |
| Horizontal slices | $\int_c^d(\text{right}-\text{left})\,dy$ |
| When to use $dy$ | When it avoids splitting, or when $x=g(y)$ is simpler |
| Symmetry | Even integrand on a symmetric interval halves the work |

---

## Lecture 1 Exercises

**1.** Find the area between $y=x^2$ and $y=x^3$ on $[0,1]$.

**2.** Find the area enclosed by $y=x^2-4$ and $y=4-x^2$.

**3.** Find the area between $y=\sin x$ and $y=\cos x$ on $[0,\pi/2]$, showing the split explicitly.

**4.** Find the area bounded by $x=y^2$ and $x=y+2$, integrating with respect to $y$. Explain why
$dy$ is easier here than $dx$.

### Answers

**1.** On $(0,1)$, $x^2 > x^3$ (since $x<1$), so $x^2$ is on top:

$$A=\int_0^1(x^2-x^3)dx=\left[\frac{x^3}{3}-\frac{x^4}{4}\right]_0^1=\frac13-\frac14=\mathbf{\frac{1}{12}}$$

*The common error is assuming $x^3>x^2$ because the exponent is larger — true for $x>1$, false on
$(0,1)$. Sketching prevents it.*

**2.** Intersections: $x^2-4=4-x^2 \Rightarrow 2x^2=8 \Rightarrow x=\pm2$. On $(-2,2)$ the upward
parabola $x^2-4$ is **below**:

$$A=\int_{-2}^{2}\big[(4-x^2)-(x^2-4)\big]dx=\int_{-2}^{2}(8-2x^2)dx$$

The integrand is even, so this is $2\int_0^2(8-2x^2)dx=2\left[8x-\tfrac{2x^3}{3}\right]_0^2
=2\left(16-\tfrac{16}{3}\right)=\mathbf{\dfrac{64}{3}}\approx21.33$

**3.** The curves cross where $\sin x=\cos x$, i.e. $x=\pi/4$.

On $[0,\pi/4]$, $\cos x>\sin x$. On $[\pi/4,\pi/2]$, $\sin x>\cos x$.

$$A=\int_0^{\pi/4}(\cos x-\sin x)dx+\int_{\pi/4}^{\pi/2}(\sin x-\cos x)dx$$

$$=\big[\sin x+\cos x\big]_0^{\pi/4}+\big[-\cos x-\sin x\big]_{\pi/4}^{\pi/2}
=(\sqrt2-1)+(\sqrt2-1)=\mathbf{2(\sqrt2-1)}\approx0.8284$$

Verified: $0.8284271247$.

**Without the split** the answer is $0$ — verified — because the two equal regions cancel. *This is
the single most important warning of the lecture, and it is worth stating that a computed area of
zero for a visibly non-empty region is always a missing split.*

**4.** Intersections: $y^2=y+2 \Rightarrow (y-2)(y+1)=0 \Rightarrow y=-1,\,2$.

For $-1<y<2$ the line $x=y+2$ is to the **right** of the parabola $x=y^2$:

$$A=\int_{-1}^{2}\big[(y+2)-y^2\big]dy=\left[\frac{y^2}{2}+2y-\frac{y^3}{3}\right]_{-1}^{2}$$

$$=\left(2+4-\frac83\right)-\left(\frac12-2+\frac13\right)=\frac{10}{3}-\left(-\frac76\right)=\mathbf{\frac92}=4.5$$

**Why $dy$ is easier.** In terms of $x$, the region's **lower boundary changes**: for $0\le x\le1$ it
is the lower branch $y=-\sqrt x$, but for $1\le x\le4$ it is the line $y=x-2$. That forces **two**
integrals. Slicing horizontally, the right boundary is the line and the left is the parabola
throughout — **one** integral, no split.

*The general principle: choose the slicing direction in which the bounding curves do not change.*

---

*Next: Tuesday — Volumes by Slicing: Disks and Washers*
