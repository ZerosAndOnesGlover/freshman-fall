# MATH 141 — Calculus I
## Week 11 · Lecture 3 (Wednesday)
### Cylindrical Shells, and Accumulation Revisited

---

**Reading:** Stewart §6.3, §6.5 | Spivak Ch. 13

---

## When Slicing Goes Wrong

Revolve $y=x^2$ on $[0,2]$ about the **$y$-axis**.

Yesterday's method wants slices perpendicular to the axis — horizontal slices, integrated in $y$.
That means inverting to $x=\sqrt y$ and setting up a washer with outer radius $2$ and inner radius
$\sqrt y$. Workable here, but the inversion is often the hard part, and for a curve like
$y=x^3+x$ it is impossible in closed form.

The **shell method** slices *parallel* to the axis instead, and needs no inversion.

---

## 1. The Shell Method

Take a thin vertical strip of the region at position $x$, of width $\Delta x$ and height $f(x)$.
Revolving it about the $y$-axis sweeps out a thin **cylindrical shell**.

Unroll the shell: it is a rectangular sheet of

- **length** $=$ circumference $=2\pi x$
- **height** $=f(x)$
- **thickness** $=\Delta x$

So its volume is $2\pi x\,f(x)\,\Delta x$, and

$$\boxed{\;V=2\pi\int_a^b x\,f(x)\,dx\;}$$

**Read it as** $2\pi \int (\text{radius})(\text{height})\,d(\text{thickness})$ — which is how it
generalises.

### The example

$y=x^2$ on $[0,2]$ about the $y$-axis:

$$V=2\pi\int_0^2 x\cdot x^2\,dx=2\pi\int_0^2x^3dx=2\pi\left[\frac{x^4}{4}\right]_0^2=8\pi$$

Verified: $25.13274123 = 8\pi$ ✓

**Cross-check by washers in $y$:** outer radius $2$, inner radius $\sqrt y$, for $0\le y\le4$:

$$V=\pi\int_0^4\big[2^2-(\sqrt y)^2\big]dy=\pi\int_0^4(4-y)\,dy=8\pi$$

Verified: $25.13274123$ — **identical** ✓

Two genuinely different set-ups, the same answer. That agreement is worth doing once by hand: it is
the strongest evidence that the slicing principle is sound rather than a recipe.

---

## 2. Choosing Between Shells and Washers

| | Slices | Integrate in | Needs |
|---|---|---|---|
| **Disks/washers** | ⟂ to axis | the axis variable | $x$ as a function of $y$ (for a $y$-axis rotation) |
| **Shells** | ∥ to axis | the other variable | nothing extra |

**The practical rule:**

- Revolving about the **$y$-axis** with the region described by $y=f(x)$ → **shells** (no inversion).
- Revolving about the **$x$-axis** with $y=f(x)$ → **disks/washers**.
- If the inversion is easy, either works — and doing both is a free check.

**Radius about a shifted axis.** Revolving about $x=c$, the shell radius is $\lvert x-c\rvert$:

$$V=2\pi\int_a^b \lvert x-c\rvert\,f(x)\,dx$$

The commonest error is using $x$ when the axis is not $x=0$.

---

## 3. Accumulation Revisited

Weeks 9 and 11 are the same idea applied twice. The general pattern:

> **Slice, approximate each piece, sum, take the limit.**

| Quantity | Slice contributes | Integral |
|---|---|---|
| Area under a curve | $f(x)\Delta x$ | $\int f\,dx$ |
| Area between curves | $(f-g)\Delta x$ | $\int(f-g)dx$ |
| Volume by slicing | $A(x)\Delta x$ | $\int A\,dx$ |
| Volume by shells | $2\pi x f(x)\Delta x$ | $2\pi\int xf\,dx$ |
| Displacement | $v(t)\Delta t$ | $\int v\,dt$ |
| Net change | $F'(x)\Delta x$ | $\int F'dx$ |
| Average value | — | $\frac{1}{b-a}\int f$ |

**Every application in this course is the same construction.** Once you can identify what one thin
slice contributes, the integral writes itself. That recognition — not memorising the formulas — is
what transfers to MATH 142, to physics, and to everything after.

### Work: one more instance

A force $F(x)$ moving an object from $a$ to $b$ does work $W=\int_a^b F(x)\,dx$. Over a slice
$\Delta x$ the force is nearly constant, contributing $F(x)\Delta x$ — same construction, new units.

For a spring with $F(x)=kx$ (Hooke's law), stretching from $0$ to $d$:

$$W=\int_0^d kx\,dx=\frac{kd^2}{2}$$

You will meet this again in PHYS 141 as the elastic potential energy.

---

## 4. What Comes Next

Week 12 reviews the course and previews Taylor polynomials. Beyond that:

- **MATH 142** — arc length, surface area, improper integrals, sequences and series, and Taylor
  series in full.
- **PHYS 141** — work, centre of mass, moments, all built on today's slicing.
- **MATH 251** — probability densities, where $\int_a^b f = P(a\le X\le b)$ and the error function
  from Week 9 becomes central.
- **MATH 341** — what to do when no antiderivative exists: the numerical methods that produced every
  verified figure in these lectures.

---

## Summary

| Idea | Takeaway |
|---|---|
| **Shell method** | $V=2\pi\int_a^b x\,f(x)\,dx$ |
| Derivation | Unroll the shell: $2\pi x \times f(x) \times \Delta x$ |
| Verified | $y=x^2$ on $[0,2]$ about the $y$-axis gives $8\pi$ |
| Cross-check | Washers in $y$ give $8\pi$ too — different set-up, same answer |
| Shells vs washers | Shells slice **parallel** to the axis and need no inversion |
| $y$-axis + $y=f(x)$ | Use shells |
| $x$-axis + $y=f(x)$ | Use disks/washers |
| Shifted axis $x=c$ | Radius $\lvert x-c\rvert$ |
| **The one idea** | Slice → approximate → sum → limit. Every application is this |
| Work | $W=\int F\,dx$; spring gives $\tfrac12kd^2$ |

---

## Lecture 3 Exercises

**1.** Use shells to find the volume when $y=x^2$ on $[0,3]$ is revolved about the $y$-axis.

**2.** Use shells for the region under $y=\sqrt x$ on $[0,4]$ revolved about the $y$-axis.

**3.** The region under $y=x^2$ on $[0,2]$ is revolved about the $y$-axis. Compute the volume **both**
ways — shells and washers — and confirm they agree.

**4.** Find the work done stretching a spring with $k=200$ N/m from its natural length to $0.3$ m.

**5.** State, in one sentence each, what a single slice contributes for: area between curves, a
volume by disks, a volume by shells, and displacement. Then say what those four have in common.

### Answers

**1.** $V=2\pi\int_0^3 x\cdot x^2dx=2\pi\int_0^3x^3dx=2\pi\left[\dfrac{x^4}{4}\right]_0^3
=2\pi\cdot\dfrac{81}{4}=\mathbf{\dfrac{81\pi}{2}}\approx127.23$

**2.** $V=2\pi\int_0^4 x\sqrt x\,dx=2\pi\int_0^4x^{3/2}dx=2\pi\left[\dfrac{2}{5}x^{5/2}\right]_0^4
=2\pi\cdot\dfrac{2}{5}(32)=\mathbf{\dfrac{128\pi}{5}}\approx80.42$

**3.** **Shells:** $V=2\pi\int_0^2x\cdot x^2dx=2\pi\left[\dfrac{x^4}{4}\right]_0^2=2\pi(4)=8\pi$

**Washers in $y$:** the solid is the cylinder of radius $2$, height $4$, minus the region inside the
parabola. Outer radius $2$, inner radius $x=\sqrt y$, for $0\le y\le 4$:

$$V=\pi\int_0^4\big[4-y\big]dy=\pi\left[4y-\frac{y^2}{2}\right]_0^4=\pi(16-8)=8\pi$$

**They agree**, at $8\pi\approx25.133$. Verified numerically: both give $25.13274123$.

*The agreement is the point. If two correct methods disagreed, one set-up would be wrong — and
checking a hard volume by the other method is the most reliable error-detection available.*

**4.** $W=\displaystyle\int_0^{0.3}200x\,dx=200\left[\frac{x^2}{2}\right]_0^{0.3}=100(0.09)=\mathbf{9}$ joules.

*Equivalently $\tfrac12kd^2=\tfrac12(200)(0.09)=9$ J.*

**5.**

| Application | One slice contributes |
|---|---|
| Area between curves | A rectangle of height $(f-g)$ and width $\Delta x$ |
| Volume by disks | A disk of area $\pi f(x)^2$ and thickness $\Delta x$ |
| Volume by shells | A shell of circumference $2\pi x$, height $f(x)$, thickness $\Delta x$ |
| Displacement | A distance $v(t)\Delta t$ travelled in a short time |

**What they share:** each approximates a quantity over a thin slice by treating it as **constant
there**, sums the slices, and takes the limit as the slices shrink — which is precisely the
definition of the definite integral.

*The formulas differ only in what one slice contributes. Recognising that is the transferable skill;
memorising four formulas is not.*

---

*Next: Week 12, Monday — Review and Synthesis*
