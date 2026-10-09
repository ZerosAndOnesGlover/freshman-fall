# MATH 142 · Calculus II
## Week 5 · Lecture 3 (Friday)
### Polar Coordinates

*“Eadem mutata resurgo [Changed and yet the same, I rise again]”* — Jacob Bernoulli, the epitaph he chose for his gravestone (1705), beside a logarithmic spiral

**Date:** Friday 26 February 2027 · 11:00–11:50 · Week 5

**Coursework:** 📝 **PS 4** due today 17:00 · 📝 **PS 5** released today 12:00, due Fri 5 Mar 17:00 · 📊 **Quiz 6** Mon 1 Mar 11:00–11:15 · 📘 **Midterm 1** Wed 3 Mar 18:00–19:15 · 🔬 **Lab 5** Wed 3 Mar 15:00–16:50

---

**Reading:** Stewart §10.3–10.4 | Apostol Ch. 2 §2.15

---

## 1. A Second Way to Locate a Point

Cartesian coordinates say **how far right and how far up**. Polar coordinates say **how far away and in which direction**:

$$(r,\theta): \qquad r = \text{distance from the origin},\qquad \theta = \text{angle from the positive } x\text{-axis}$$

### Conversion

$$\boxed{x = r\cos\theta,\qquad y = r\sin\theta} \qquad\qquad \boxed{r^2 = x^2+y^2,\qquad \tan\theta = \frac yx}$$

> **Use $\tan\theta = y/x$ with care.** It cannot distinguish the second quadrant from the fourth —
> $\arctan$ returns values in $\left(-\tfrac\pi2,\tfrac\pi2\right)$ only. **Always check which quadrant
> the point is in.** (This is why every programming language has `atan2(y,x)` as well as `atan`.)

### Polar coordinates are not unique

The same point has infinitely many representations:

- $(r,\theta)$ and $(r,\theta+2\pi k)$ are the same point.
- $(-r,\theta)$ and $(r,\theta+\pi)$ are the same point — **negative $r$ means "go backwards".**
- **The origin is $(0,\theta)$ for every $\theta$.**

**This non-uniqueness is a genuine nuisance**, and it is the source of most polar errors: two curves can intersect at a point that their equations never simultaneously satisfy, because they arrive there with different $\theta$.

---

## 2. Polar Curves

A polar curve is $r = f(\theta)$: the distance from the origin, as a function of direction.

| Equation | Curve |
|---|---|
| $r = a$ | circle of radius $a$, centred at the origin |
| $\theta = \alpha$ | a ray from the origin |
| $r = 2a\cos\theta$ | circle of radius $a$ through the origin, centred at $(a,0)$ |
| $r = a(1+\cos\theta)$ | **cardioid** (heart-shaped) |
| $r = a\cos(n\theta)$ | **rose** — $n$ petals if $n$ odd, $2n$ if $n$ even |
| $r = a\theta$ | **Archimedean spiral** |

**Every polar curve is a parametric curve**, with $\theta$ as the parameter:

$$x(\theta) = f(\theta)\cos\theta,\qquad y(\theta) = f(\theta)\sin\theta$$

So nothing in this lecture is logically new — but the polar formulas are much simpler than pushing everything through yesterday's machinery.

### Example 1 — a circle in disguise

$r = 2a\cos\theta$. Multiply both sides by $r$:

$$r^2 = 2ar\cos\theta \implies x^2+y^2 = 2ax \implies (x-a)^2+y^2 = a^2$$

— a circle of radius $a$ centred at $(a,0)$. **Multiplying by $r$ is the standard trick**, because it turns $r^2$ into $x^2+y^2$ and $r\cos\theta$ into $x$.

**Note the range:** the whole circle is traced as $\theta$ runs over $\left[-\tfrac\pi2,\tfrac\pi2\right]$, *not* $[0,2\pi]$. Over the full range it is traced **twice**. This is the recurring polar trap.

---

## 3. Area in Polar Coordinates

**This formula is not $\int y\,dx$ in disguise, and the derivation matters.**

Slice the region **by angle**, not by $x$. A thin wedge from $\theta$ to $\theta+\Delta\theta$, bounded by $r=f(\theta)$, is approximately a **circular sector** of radius $f(\theta)$ and angle $\Delta\theta$.

**The area of a sector** of radius $r$ and angle $\Delta\theta$ is $\frac{\Delta\theta}{2\pi}$ of the whole disc:

$$\frac{\Delta\theta}{2\pi}\cdot\pi r^2 = \frac12 r^2\,\Delta\theta$$

Summing and taking the limit:

$$\boxed{A = \frac12\int_\alpha^\beta \big(f(\theta)\big)^2\,d\theta}$$

> **The $\tfrac12$ comes from the sector**, and there is no way to remember it reliably except by
> remembering that the slices are wedges. **Slice, approximate, sum, limit** — Week 0's pattern, with
> a sector as the approximating shape instead of a rectangle.

### Example 2 — the cardioid

$r = 1+\cos\theta$, traced once as $\theta$ runs over $[0,2\pi]$:

$$A = \frac12\int_0^{2\pi}(1+\cos\theta)^2d\theta = \frac12\int_0^{2\pi}\big(1+2\cos\theta+\cos^2\theta\big)d\theta$$

Over a full period, $\int\cos\theta=0$ and $\int\cos^2\theta = \pi$:

$$A = \frac12\big(2\pi+0+\pi\big) = \boxed{\frac{3\pi}{2}}$$

*Verified symbolically.*

### Example 3 — one petal of a rose

$r=\cos2\theta$. **This is where the limits are the whole problem.**

The petal centred on the positive $x$-axis is traced where $r\ge0$, i.e. where $\cos2\theta\ge0$, i.e. $2\theta\in\left[-\tfrac\pi2,\tfrac\pi2\right]$:

$$\theta\in\left[-\frac\pi4,\frac\pi4\right]$$

$$A = \frac12\int_{-\pi/4}^{\pi/4}\cos^2 2\theta\,d\theta = \boxed{\frac{\pi}{8}}$$

*Verified symbolically.*

**Since $\cos2\theta$ gives a 4-petalled rose, the total area is $4\cdot\frac\pi8 = \frac\pi2$.**

> **Getting the limits right is harder than the integral.** Integrating over $[0,2\pi]$ here gives
> $\frac\pi2$ — the *total* area, which is correct for the whole rose and four times too big for one
> petal. **Find where $r=0$ to locate the petal boundaries.**

### Example 4 — the circle again, as a check

$r=2a\cos\theta$ over $\left[-\tfrac\pi2,\tfrac\pi2\right]$:

$$A = \frac12\int_{-\pi/2}^{\pi/2}4a^2\cos^2\theta\,d\theta = \boxed{\pi a^2}$$

*Verified symbolically.* ✓ — the area of a disc of radius $a$, as it must be. **Integrating over $[0,2\pi]$ would give $2\pi a^2$**, double, because the circle is traced twice.

### Area between two polar curves

$$A = \frac12\int_\alpha^\beta\Big[r_{\text{outer}}^2 - r_{\text{inner}}^2\Big]d\theta$$

**Squares subtract** — the same structure as Week 4's washers, and the same warning: **not $(r_{\text{outer}}-r_{\text{inner}})^2$.**

**Finding $\alpha,\beta$ requires solving $r_1(\theta)=r_2(\theta)$** — and then checking for intersections at the origin, which that equation can miss (§1's non-uniqueness).

---

## 4. Arc Length in Polar

Treat the curve as parametric in $\theta$ and grind through yesterday's formula. With $x=r\cos\theta$, $y=r\sin\theta$ and $r=f(\theta)$:

$$\frac{dx}{d\theta} = r'\cos\theta - r\sin\theta,\qquad \frac{dy}{d\theta} = r'\sin\theta+r\cos\theta$$

Squaring and adding, the cross terms cancel and $\cos^2+\sin^2=1$ twice:

$$\left(\frac{dx}{d\theta}\right)^2+\left(\frac{dy}{d\theta}\right)^2 = r^2 + (r')^2$$

$$\boxed{L = \int_\alpha^\beta\sqrt{\big(f(\theta)\big)^2+\big(f'(\theta)\big)^2}\,d\theta}$$

**A pleasingly symmetric formula**, and much easier than converting to Cartesian.

### Example 5 — the cardioid's perimeter

$r=1+\cos\theta$, $r'=-\sin\theta$:

$$r^2+(r')^2 = (1+\cos\theta)^2+\sin^2\theta = 2+2\cos\theta$$

**The half-angle identity again:** $2+2\cos\theta = 4\cos^2\frac\theta2$, so the integrand is $2\left|\cos\frac\theta2\right|$.

$$L = \int_0^{2\pi}2\left|\cos\frac\theta2\right|d\theta = 4\int_0^{\pi}|\cos u|\,du = 4\cdot2 = \boxed{8}$$

*(substituting $u=\theta/2$)*

*Verified: the identity holds exactly, and numerical quadrature over $[0,\pi,2\pi]$ gives exactly $8.0$.*

**Exactly 8** — the same clean number as the cycloid's $8a$, and for the same reason: **a half-angle identity collapsed the square root.**

> **The absolute value is essential.** $\cos\frac\theta2$ is negative on $(\pi,2\pi)$. A CAS asked for
> this integral directly returns it **unevaluated**, exactly as in Week 0 with $\int_0^3|t^2-4|dt$.
> **Splitting at the sign change by hand gives 8 immediately.**

---

## 5. What To Take From This Lecture

1. **$x=r\cos\theta$, $y=r\sin\theta$**; and $\tan\theta=y/x$ needs a quadrant check.
2. **Polar coordinates are not unique**, and the origin has every angle.
3. **$A = \frac12\int r^2d\theta$ — and the $\frac12$ is from the sector.** Derive it, do not memorise it.
4. **Finding the limits is harder than the integral.** Locate where $r=0$, and check whether the curve is traced more than once.
5. **$L = \int\sqrt{r^2+(r')^2}\,d\theta$** — symmetric, and easier than converting.
6. **Half-angle identities are why the cardioid and cycloid have clean answers.**

---

## Looking Ahead

**This is the last lecture of the first half of the course.**

Weeks 0–5 have been about **integration and geometry** — evaluating, computing, measuring. You now have every technique this course will teach for finding a number.

**Week 6 changes the subject entirely.** We start with sequences, and from there the question is almost always *"does this converge?"* — the question you first met in Week 3, now asked of sums instead of integrals. The computations will get easier and the reasoning much harder.

**Midterm 1 is Wednesday 3 March, 18:00–19:15**, covering Weeks 0–4. **This week's material is examined on Midterm 2, not Midterm 1.**

---

*Next: Week 6, Monday — Sequences*
