# MATH 142 · Calculus II
## Week 4 · Lecture 1 (Monday)
### Volumes by Discs and Washers

**Date:** Monday 8 February 2027 · 11:00–11:50 · Week 4

---

**Reading:** Stewart §6.2 | Apostol Ch. 2 §2.11
**Quiz 04** — this Monday, **covers Week 3** (improper integrals, comparison tests)

---

## 1. Volume by Slicing — The General Principle

Before any formula, the general statement. Suppose a solid lies between $x=a$ and $x=b$, and let $A(x)$ be **the area of its cross-section at position $x$**, taken perpendicular to the $x$-axis.

**Slice, approximate, sum, limit:** a slab of thickness $\Delta x$ at position $x$ is approximately a cylinder of cross-section $A(x)$ and height $\Delta x$, so its volume is about $A(x)\,\Delta x$. Summing and taking the limit:

$$\boxed{V = \int_a^b A(x)\,dx}$$

**Everything today is this one formula.** The only question is what $A(x)$ is.

---

## 2. The Disc Method

Rotate the region under $y=f(x)$, from $x=a$ to $x=b$, about the **$x$-axis**.

The cross-section at $x$ is a **disc of radius $f(x)$**, so $A(x)=\pi\big(f(x)\big)^2$:

$$\boxed{V = \pi\int_a^b\big(f(x)\big)^2\,dx}$$

### Example 1 — the volume of a sphere

A sphere of radius $r$ is obtained by rotating $y=\sqrt{r^2-x^2}$, $-r\le x\le r$, about the $x$-axis.

$$V = \pi\int_{-r}^{r}\big(r^2-x^2\big)dx = \pi\left[r^2x - \frac{x^3}{3}\right]_{-r}^{r} = \pi\left(\frac{2r^3\cdot 2}{3}\right)$$

Carefully: $\left(r^3-\frac{r^3}{3}\right)-\left(-r^3+\frac{r^3}{3}\right) = \frac{2r^3}{3}+\frac{2r^3}{3} = \frac{4r^3}{3}$.

$$\boxed{V = \frac43\pi r^3}$$

*Verified symbolically.*

**This is the formula you were given in school, derived.** Archimedes obtained it around 250 BC by a method essentially equivalent to this one — and considered it his finest result.

### Example 2 — the volume of a cone

A cone of radius $r$ and height $h$: rotate the line $y = \frac{r}{h}x$ from $x=0$ to $x=h$.

$$V = \pi\int_0^h\frac{r^2}{h^2}x^2\,dx = \frac{\pi r^2}{h^2}\cdot\frac{h^3}{3} = \boxed{\frac13\pi r^2h}$$

*Verified symbolically.*

**The famous $\frac13$** is nothing more than $\int x^2 = \frac{x^3}{3}$.

### Example 3

Rotate $y=x^2$ on $[0,2]$ about the $x$-axis.

$$V = \pi\int_0^2 x^4\,dx = \pi\left[\frac{x^5}{5}\right]_0^2 = \boxed{\frac{32\pi}{5}}$$

*Verified symbolically.*

---

## 3. The Washer Method

If the region does not touch the axis, the cross-section is an **annulus** ("washer") — a disc with a hole.

With **outer** radius $R(x)$ and **inner** radius $r(x)$:

$$A(x) = \pi R(x)^2 - \pi r(x)^2 \implies \boxed{V = \pi\int_a^b\Big[R(x)^2 - r(x)^2\Big]dx}$$

### The error that costs the most marks

$$\pi\int\big(R-r\big)^2 dx \qquad\textbf{is wrong}$$

**Squares subtract; they do not subtract before squaring.** $R^2-r^2 \neq (R-r)^2$. Write the two radii separately, square each, then subtract.

### Example 4

The region between $y=x$ and $y=x^2$ on $[0,1]$, rotated about the $x$-axis.

On $(0,1)$, $x>x^2$, so $y=x$ is the **outer** boundary: $R(x)=x$, $r(x)=x^2$.

$$V = \pi\int_0^1\big(x^2 - x^4\big)dx = \pi\left(\frac13-\frac15\right) = \pi\cdot\frac{2}{15} = \boxed{\frac{2\pi}{15}}$$

*Verified symbolically.*

**Check the radii by picture, not by algebra.** "Outer" means *further from the axis of rotation*, which is not always the larger function — it depends where the axis is.

---

## 4. Rotating About Other Lines

This is where most errors live. **The radius is the distance from the curve to the axis of rotation**, not the value of the function.

| Axis of rotation | Radius of the curve $y=f(x)$ |
|---|---|
| the $x$-axis ($y=0$) | $\lvert f(x)\rvert$ |
| $y = c$ | $\lvert f(x) - c\rvert$ |
| the $y$-axis ($x=0$) | $\lvert x\rvert$ *(slicing in $y$)* |
| $x = c$ | $\lvert x - c\rvert$ |

### Example 5

Rotate the region under $y=x^2$ on $[0,1]$ about the line $y=-1$.

Every distance increases by 1. The outer radius is $x^2+1$ (curve to axis) and the inner radius is $1$ (the $x$-axis to the axis of rotation — the region's lower boundary):

$$V = \pi\int_0^1\Big[(x^2+1)^2 - 1^2\Big]dx = \pi\int_0^1\big(x^4+2x^2\big)dx = \pi\left(\frac15+\frac23\right) = \frac{13\pi}{15}$$

**Draw the picture.** Deciding which radius is outer, and remembering the hole exists at all, is a geometric question, and an algebraic approach to it fails silently.

---

## 5. Slicing in $y$ Instead

Rotating about the **$y$-axis**, the natural slices are horizontal, and everything must be expressed as a function of $y$:

$$V = \pi\int_c^d\big(g(y)\big)^2dy \qquad\text{where } x = g(y)$$

### Example 6

Rotate the region bounded by $y=x^2$, $x=2$ and $y=0$ about the **$y$-axis**.

Slicing horizontally at height $y$: the solid runs from $x=\sqrt y$ out to $x=2$, so it is a washer with $R=2$, $r=\sqrt y$, for $y\in[0,4]$:

$$V = \pi\int_0^4\Big[4 - y\Big]dy = \pi\left[4y-\frac{y^2}{2}\right]_0^4 = \pi(16-8) = \boxed{8\pi}$$

*Verified symbolically.*

**We will get $8\pi$ again tomorrow by a completely different method** — cylindrical shells, which handles this problem without ever solving $y=x^2$ for $x$. Agreement between the two is the standard check that a setup is right.

---

## 6. The Procedure

1. **Draw the region** and the axis of rotation.
2. **Decide the slicing direction** — perpendicular to the axis, for this method.
3. **Draw one representative slice** and identify it as a disc or a washer.
4. **Write the radius/radii as distances to the axis**, in the slicing variable.
5. **Integrate** $A$ over the range of that variable.

> **Step 1 is not optional.** Every recurring error in this material — wrong radius, missing hole,
> outer and inner swapped — is a picture that was not drawn.

---

## 7. What To Take From This Lecture

1. **$V = \int A(x)\,dx$** — one formula; the work is finding $A$.
2. **Disc:** $A = \pi f^2$. **Washer:** $A = \pi(R^2-r^2)$.
3. **$R^2 - r^2$, never $(R-r)^2$.**
4. **The radius is a distance to the axis**, so a shifted axis shifts every radius.
5. **Rotating about the $y$-axis means slicing in $y$** — and re-expressing everything in $y$.
6. **Draw the picture.**

---

*Next: Tuesday — Cylindrical Shells, and When Discs Will Not Work*
