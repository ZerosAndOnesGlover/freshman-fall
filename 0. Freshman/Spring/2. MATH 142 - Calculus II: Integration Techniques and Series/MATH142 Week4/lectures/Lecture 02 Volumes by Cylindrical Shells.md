# MATH 142 · Calculus II
## Week 4 · Lecture 2 (Tuesday)
### Cylindrical Shells, and Choosing a Method

*“...certain things first became clear to me by a mechanical method, although they had to be demonstrated by geometry afterwards...”* — Archimedes, *The Method of Mechanical Theorems*

**Date:** Tuesday 16 February 2027 · 11:00–11:50 · Week 4

**Coursework:** 🔬 **Lab 3** Wed 17 Feb 15:00–16:50 · 📝 **PS 3** due Fri 19 Feb 17:00 · 📝 **PS 4** released Fri 19 Feb 12:00, due Fri 26 Feb 17:00 · 📊 **Quiz 5** Mon 22 Feb 11:00–11:15

---

**Reading:** Stewart §6.3 | Apostol Ch. 2 §2.12

---

## 1. Slicing the Other Way

Yesterday we sliced **perpendicular** to the axis of rotation, giving discs. Today we slice **parallel** to it.

Rotate the region under $y=f(x)$, $a\le x\le b$, about the **$y$-axis**. Take a thin vertical strip at position $x$, of width $\Delta x$ and height $f(x)$. Rotating *that strip* about the $y$-axis sweeps out a **thin cylindrical shell**: a tube of radius $x$, height $f(x)$, and wall thickness $\Delta x$.

**What is its volume?** Cut the tube down its side and unroll it. You get a flat sheet:

$$\underbrace{2\pi x}_{\text{circumference}} \times \underbrace{f(x)}_{\text{height}} \times \underbrace{\Delta x}_{\text{thickness}}$$

Summing and taking the limit:

$$\boxed{V = 2\pi\int_a^b x\,f(x)\,dx}$$

**Read the integrand as (circumference) × (height).** That reading survives every variation — a shifted axis, a region between two curves, slicing in $y$ — where a memorised formula does not.

$$V = 2\pi\int (\text{radius})\times(\text{height})\ d(\text{thickness})$$

---

## 2. The Same Answer, Two Ways

Yesterday's Example 6: the region bounded by $y=x^2$, $x=2$, $y=0$, rotated about the **$y$-axis**.

**By discs** (slicing in $y$) we got $8\pi$, after re-expressing the boundary as $x=\sqrt y$ and treating it as a washer against $x=2$.

**By shells**, radius $x$ and height $x^2$:

$$V = 2\pi\int_0^2 x\cdot x^2\,dx = 2\pi\int_0^2 x^3dx = 2\pi\cdot4 = \boxed{8\pi}$$

*Verified symbolically — both methods give $8\pi$.*

**Note what the shell method did not require:** no solving $y=x^2$ for $x$, no washer, no splitting. Same answer, a third of the work.

> **Agreement between the two methods is the standard check on a setup.** If you have time in an
> exam and the second method is quick, do it.

---

## 3. When Shells Are Clearly Better

### Example 1 — a region that is not a function of $y$

Rotate the region under $y=\sin x$, $0\le x\le\pi$, about the **$y$-axis**.

**By shells**, immediately:

$$V = 2\pi\int_0^\pi x\sin x\,dx = 2\pi\big[-x\cos x+\sin x\big]_0^\pi = 2\pi(\pi) = \boxed{2\pi^2}$$

*(the inner integral is $\pi$ — computed in Week 1, Lecture 1)*

*Verified symbolically: $2\pi^2 \approx 19.74$.*

**By discs this is genuinely unpleasant.** Slicing horizontally at height $y$, the region runs from $x=\arcsin y$ on the left to $x = \pi - \arcsin y$ on the right — **$\sin x$ is not one-to-one on $[0,\pi]$**, so a horizontal slice meets the curve twice and you need a washer with two different branches of the inverse:

$$V = \pi\int_0^1\Big[(\pi-\arcsin y)^2 - (\arcsin y)^2\Big]dy$$

It can be done, but it needs both branches, an expansion, and $\int(\arcsin y)\,dy$ and $\int(\arcsin y)^2dy$. **Shells took one line.**

### Example 2

Rotate the region under $y = e^{-x^2}$, $0\le x\le1$, about the **$y$-axis**.

$$V = 2\pi\int_0^1 xe^{-x^2}dx = 2\pi\left[-\frac{e^{-x^2}}{2}\right]_0^1 = \pi\big(1-e^{-1}\big)\approx\boxed{1.986}$$

*Verified symbolically: $\pi - \pi e^{-1}$.*

**The factor of $x$ from the shell's circumference is exactly what makes this a substitution.** Without it — as in $\int e^{-x^2}dx$ — there is no elementary antiderivative at all. **The geometry supplied the missing factor.**

### Example 3 — the torus

Rotate the disc of radius $a$ centred at $(R,0)$, with $R>a$, about the **$y$-axis**.

At position $x$, the vertical extent of the disc is $2\sqrt{a^2-(x-R)^2}$, so shells of radius $x$ and that height give

$$V = 2\pi\int_{R-a}^{R+a} x\cdot2\sqrt{a^2-(x-R)^2}\,dx = \boxed{2\pi^2a^2R}$$

*Verified symbolically.*

**A beautiful result:** the volume equals $(\pi a^2)\times(2\pi R)$ — the cross-sectional area times the distance travelled by its centre. That is **Pappus's theorem**, and this integral is a proof of it in this case.

---

## 4. Choosing Between Discs and Shells

Both methods always work. The question is which produces an integral you can evaluate.

| | Discs / Washers | Shells |
|---|---|---|
| Slice | ⊥ to the axis | ∥ to the axis |
| Rotating about the **$x$-axis**, region given as $y=f(x)$ | **integrate in $x$** ✓ natural | integrate in $y$ — needs the inverse |
| Rotating about the **$y$-axis**, region given as $y=f(x)$ | integrate in $y$ — needs the inverse | **integrate in $x$** ✓ natural |

> **The rule of thumb:**
> **If the axis is perpendicular to the variable your functions are written in, use shells.**
> **If it is parallel, use discs.**
>
> Equivalently: **choose the method that lets you avoid inverting the function.**

### The decision, in one question

> *Would slicing this way force me to solve $y=f(x)$ for $x$?*
> If yes, slice the other way.

**Exceptions exist** — sometimes the inverse is easy and the shell integral is not, as when $f$ is a simple power. But the rule is right far more often than not, and it costs thirty seconds to apply.

---

## 5. Shells About Other Axes

Same principle as yesterday: **the radius is a distance to the axis.**

| Axis | Shell radius |
|---|---|
| $y$-axis ($x=0$) | $x$ |
| $x = c$, with the region to the right | $x - c$ |
| $x = c$, with the region to the left | $c - x$ |
| $x$-axis ($y=0$), slicing in $y$ | $y$ |

### Example 4

Rotate the region under $y=x-x^2$ on $[0,1]$ about the $y$-axis:

$$V = 2\pi\int_0^1 x(x-x^2)\,dx = 2\pi\left(\frac13-\frac14\right) = 2\pi\cdot\frac{1}{12} = \boxed{\frac\pi6}$$

*Verified symbolically.*

**If instead the axis were $x=1$**, the radius becomes $1-x$ (the region lies to the *left* of the axis) and the integral is

$$2\pi\int_0^1(1-x)(x-x^2)\,dx = \frac\pi6$$

**— the same answer.** *(Verified symbolically.)*

That is not a coincidence and it is worth pausing on: **$y=x-x^2$ is symmetric about $x=\tfrac12$**, and the lines $x=0$ and $x=1$ are equidistant from that axis of symmetry. Reflecting the region maps one problem exactly onto the other.

**The height is unchanged; only the radius moved** — and here the two radii are mirror images.

> **Look for symmetry before computing.** It is the Week 0 habit, and it works on solids too.

---

## 6. A Region Between Two Curves

The shell's **height** is the vertical extent of the region at that $x$ — i.e. (upper curve) − (lower curve), exactly as in Week 0's area formula.

$$V = 2\pi\int_a^b x\Big[f(x)-g(x)\Big]dx$$

The torus in Example 3 was this, with the two curves being the top and bottom halves of the circle.

---

## 7. What To Take From This Lecture

1. **A shell unrolls into a sheet:** $2\pi\times(\text{radius})\times(\text{height})\times(\text{thickness})$.
2. **$V=2\pi\int x f(x)\,dx$** about the $y$-axis — but read it as circumference × height, not as a formula.
3. **Shells slice parallel to the axis; discs slice perpendicular.**
4. **Choose the method that avoids inverting the function.**
5. **The radius is a distance to the axis**; a shifted axis changes the radius, never the height.
6. **Two methods on the same solid is a free check.**

---

*Next: Wednesday — Arc Length and Surface Area, and Where Closed Forms Run Out*
