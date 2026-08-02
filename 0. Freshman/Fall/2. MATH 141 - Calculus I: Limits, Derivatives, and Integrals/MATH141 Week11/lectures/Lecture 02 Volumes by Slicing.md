# MATH 141 — Calculus I
## Week 11 · Lecture 2 (Tuesday)
### Volumes by Slicing: Disks and Washers

---

**Reading:** Stewart §6.2 | Spivak Ch. 13

---

## The General Principle

Yesterday sliced a plane region into rectangles. Today slices a solid into **thin slabs**.

> If a solid extends from $x=a$ to $x=b$, and the cross-section perpendicular to the $x$-axis at
> position $x$ has area $A(x)$, then
> $$V=\int_a^b A(x)\,dx$$

A slab of thickness $\Delta x$ at position $x$ has volume $\approx A(x)\Delta x$. Sum and pass to the
limit. **Everything today is a special case of this one formula** — the work is always finding
$A(x)$.

---

## 1. The Disk Method

Revolve the region under $y=f(x)$ about the **$x$-axis**. Each cross-section is a **disk** of radius
$f(x)$:

$$A(x)=\pi\big[f(x)\big]^2 \qquad\Longrightarrow\qquad V=\pi\int_a^b\big[f(x)\big]^2dx$$

### Example: $y=\sqrt x$ on $[0,4]$

$$V=\pi\int_0^4(\sqrt x)^2dx=\pi\int_0^4 x\,dx=\pi\left[\frac{x^2}{2}\right]_0^4=8\pi$$

Verified: $25.1327412287 = 8\pi$ ✓

### Deriving the classics

**The cone.** Revolve $y=x$ on $[0,3]$:

$$V=\pi\int_0^3x^2dx=\pi\left[\frac{x^3}{3}\right]_0^3=9\pi$$

Verified: $28.27433388 = 9\pi$, matching $\tfrac13\pi r^2h$ with $r=h=3$ ✓

**The sphere.** Revolve $y=\sqrt{R^2-x^2}$ on $[-R,R]$:

$$V=\pi\int_{-R}^{R}(R^2-x^2)dx=\pi\left[R^2x-\frac{x^3}{3}\right]_{-R}^{R}=\frac{4}{3}\pi R^3$$

Verified for $R=3$: $113.09733553 = \tfrac43\pi(27)$ ✓

> **Worth pausing on.** The volume of a sphere was known to Archimedes, who obtained it by an
> ingenious argument with a cylinder and a cone. With the FTC it is a two-line computation. That gap
> — a lifetime's insight reduced to a routine exercise — is what calculus bought.

---

## 2. The Washer Method

If the region does not touch the axis of revolution, each slice is a disk with a hole — an
**annulus**, or washer:

$$A(x)=\pi\Big[R_{\text{outer}}(x)^2-R_{\text{inner}}(x)^2\Big]$$

$$V=\pi\int_a^b\Big[R_{\text{out}}^2-R_{\text{in}}^2\Big]dx$$

### Example: between $y=x$ and $y=x^2$ on $[0,1]$, about the $x$-axis

On $(0,1)$ the line is above the parabola, so the line traces the **outer** radius:

$$V=\pi\int_0^1\big[x^2-(x^2)^2\big]dx=\pi\int_0^1(x^2-x^4)dx=\pi\left[\frac{x^3}{3}-\frac{x^5}{5}\right]_0^1=\frac{2\pi}{15}$$

Verified: $0.4188790205 = \tfrac{2\pi}{15}$ ✓

### The error that dominates this topic

$$\int\big[R_{\text{out}}-R_{\text{in}}\big]^2dx \quad\ne\quad \int\big[R_{\text{out}}^2-R_{\text{in}}^2\big]dx$$

**Square each radius first, then subtract.** The washer's area is a difference of *areas*, not the
square of a difference of *radii*. Check with numbers: $R_{\text{out}}=2$, $R_{\text{in}}=1$ gives
$\pi(4-1)=3\pi$, not $\pi(2-1)^2=\pi$.

### Revolving about a line other than an axis

If the axis is $y=c$, the radius is the **distance** from the curve to that line:

$$R(x)=\lvert f(x)-c\rvert$$

Everything else is unchanged. The commonest mistake is using $f(x)$ itself and forgetting the shift.

---

## 3. Slicing Without Revolving

The formula $V=\int A(x)\,dx$ needs no rotational symmetry at all.

**Example.** A solid has base the region between $y=x^2$ and $y=4$, and every cross-section
perpendicular to the $x$-axis is a **square**. The base of each square runs from the parabola to the
line, so its side is $4-x^2$:

$$A(x)=(4-x^2)^2 \qquad V=\int_{-2}^{2}(4-x^2)^2dx$$

$$=\int_{-2}^{2}(16-8x^2+x^4)dx = 2\left[16x-\frac{8x^3}{3}+\frac{x^5}{5}\right]_0^2=\frac{512}{15}$$

*(Even integrand on a symmetric interval — Week 8 again.)*

**Semicircular cross-sections** would give $A(x)=\tfrac{\pi}{2}\left(\tfrac{4-x^2}{2}\right)^2$;
**equilateral triangles**, $A(x)=\tfrac{\sqrt3}{4}(4-x^2)^2$. Only $A(x)$ changes.

---

## 4. Choosing $dx$ or $dy$

| Revolving about | Natural slicing |
|---|---|
| $x$-axis (or $y=c$) | $dx$ — slices perpendicular to $x$ |
| $y$-axis (or $x=c$) | $dy$ — slices perpendicular to $y$ |

Revolving about the $y$-axis with disks requires expressing $x$ as a function of $y$. If that
inversion is awkward, tomorrow's **shell method** avoids it entirely.

---

## Summary

| Idea | Takeaway |
|---|---|
| **General principle** | $V=\int_a^b A(x)\,dx$ — everything else is finding $A(x)$ |
| Disk | $A=\pi f(x)^2$; $V=\pi\int f^2dx$ |
| Cone from $y=x$ on $[0,3]$ | $9\pi$ — verified |
| Sphere from $y=\sqrt{R^2-x^2}$ | $\tfrac43\pi R^3$ — verified at $R=3$ |
| Washer | $V=\pi\int\big[R_{\text{out}}^2-R_{\text{in}}^2\big]dx$ |
| **Square first, then subtract** | $\int(R_o-R_i)^2 \ne \int(R_o^2-R_i^2)$ |
| Axis $y=c$ | Radius is $\lvert f(x)-c\rvert$ |
| Non-circular slices | Only $A(x)$ changes; the method does not |
| Slicing direction | Perpendicular to the axis of revolution |

---

## Lecture 2 Exercises

**1.** Find the volume when $y=x^2$ on $[0,2]$ is revolved about the $x$-axis.

**2.** Find the volume when the region between $y=\sqrt x$ and $y=x$ on $[0,1]$ is revolved about the
$x$-axis.

**3.** Derive the volume of a cone of radius $r$ and height $h$ by revolving a suitable line.

**4.** A solid has base the disk $x^2+y^2\le4$, and cross-sections perpendicular to the $x$-axis are
squares. Find its volume.

**5.** A student computes the washer volume for Exercise 2 as
$\pi\int_0^1(\sqrt x-x)^2dx$. Explain the error and give the correct integral.

### Answers

**1.** $V=\pi\int_0^2(x^2)^2dx=\pi\int_0^2x^4dx=\pi\left[\dfrac{x^5}{5}\right]_0^2=\mathbf{\dfrac{32\pi}{5}}\approx20.11$

**2.** On $(0,1)$, $\sqrt x > x$, so $\sqrt x$ is the **outer** radius:

$$V=\pi\int_0^1\big[(\sqrt x)^2-x^2\big]dx=\pi\int_0^1(x-x^2)dx=\pi\left[\frac{x^2}{2}-\frac{x^3}{3}\right]_0^1=\mathbf{\frac{\pi}{6}}\approx0.524$$

**3.** Revolve $y=\dfrac{r}{h}x$ on $[0,h]$ about the $x$-axis:

$$V=\pi\int_0^h\left(\frac{r}{h}x\right)^2dx=\frac{\pi r^2}{h^2}\left[\frac{x^3}{3}\right]_0^h=\frac{\pi r^2}{h^2}\cdot\frac{h^3}{3}=\mathbf{\frac13\pi r^2h}$$

*Verified for $r=h=3$: $9\pi = 28.27433388$ ✓. The line must pass through the origin with slope
$r/h$ so that it reaches height $r$ exactly at $x=h$.*

**4.** At position $x$, the disk's vertical extent runs from $-\sqrt{4-x^2}$ to $+\sqrt{4-x^2}$, so
the square's side is $s(x)=2\sqrt{4-x^2}$ and

$$A(x)=s^2=4(4-x^2)$$

$$V=\int_{-2}^{2}4(4-x^2)dx=4\cdot2\int_0^2(4-x^2)dx=8\left[4x-\frac{x^3}{3}\right]_0^2=8\cdot\frac{16}{3}=\mathbf{\frac{128}{3}}\approx42.67$$

*The trap is taking the side to be $\sqrt{4-x^2}$ rather than $2\sqrt{4-x^2}$ — the square spans the
**full** chord, both above and below the axis.*

**5.** The error is **squaring the difference instead of differencing the squares**.

The washer's cross-sectional area is
$\pi R_{\text{out}}^2-\pi R_{\text{in}}^2 = \pi\big(R_o^2-R_i^2\big)$ — a difference of two circular
areas. Writing $\pi(R_o-R_i)^2$ computes the area of a circle whose radius is the *gap between* the
two radii, which is a different and geometrically meaningless quantity.

**Correct:** $\displaystyle V=\pi\int_0^1\big[(\sqrt x)^2-x^2\big]dx=\pi\int_0^1(x-x^2)dx=\frac{\pi}{6}$

**The student's version** gives $\pi\int_0^1(x-2x^{3/2}+x^2)dx=\pi\left(\tfrac12-\tfrac45+\tfrac13\right)=\tfrac{\pi}{30}$
— a fifth of the correct answer, and wrong.

*Numerical check: correct $\pi/6 \approx 0.5236$; the erroneous version $\pi/30 \approx 0.1047$.*

---

*Next: Wednesday — Volumes by Cylindrical Shells, and Accumulation Revisited*
