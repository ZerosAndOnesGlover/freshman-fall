# MATH 141 — Week 11 Reference Sheet
## Applications of Integration

---

## The One Idea

> **Slice → approximate each slice as constant → sum → take the limit.**

Every formula below is this construction. Identify what one thin slice contributes and the integral
writes itself.

---

## Area

| Slicing | Formula |
|---|---|
| Vertical ($dx$) | $A=\displaystyle\int_a^b\big[\text{top}-\text{bottom}\big]dx$ |
| Horizontal ($dy$) | $A=\displaystyle\int_c^d\big[\text{right}-\text{left}\big]dy$ |

**Procedure:** sketch → find intersections → identify top/bottom → integrate.

**If the curves cross, split at every crossing.** Equivalently integrate $\lvert f-g\rvert$.

Verified failure: $\int_0^{\pi/2}(\sin x-\cos x)dx = \mathbf 0$, while the true area is
$2(\sqrt2-1)\approx0.8284$. **An area of zero for a non-empty region is always a missing split.**

**Choose $dy$** when the bounding curves would otherwise change partway — e.g. $x=y^2$ and $x=y+2$
needs one integral in $y$, two in $x$.

---

## Volume

**General:** $V=\displaystyle\int_a^b A(x)\,dx$, where $A(x)$ is the cross-sectional area.

| Method | Formula | Slices | Use when |
|---|---|---|---|
| **Disks** | $\pi\displaystyle\int f(x)^2dx$ | ⟂ to axis | region touches the axis |
| **Washers** | $\pi\displaystyle\int\big[R_o^2-R_i^2\big]dx$ | ⟂ to axis | there is a hole |
| **Shells** | $2\pi\displaystyle\int x\,f(x)\,dx$ | ∥ to axis | rotating about $y$ with $y=f(x)$ |

**Square first, then subtract:** $\int(R_o-R_i)^2 \ne \int(R_o^2-R_i^2)$. Verified: the wrong version
gives $\pi/30$ where the right one gives $\pi/6$ — off by a factor of **5**.

**Shifted axis:** the radius is the **distance** to the axis — $\lvert f(x)-c\rvert$ about $y=c$,
$\lvert x-c\rvert$ about $x=c$.

**Non-circular cross-sections:** only $A(x)$ changes.

| Shape of side $s$ | $A$ |
|---|---|
| Square | $s^2$ |
| Semicircle (diameter $s$) | $\tfrac{\pi}{8}s^2$ |
| Equilateral triangle | $\tfrac{\sqrt3}{4}s^2$ |

For a base bounded above and below, the side spans the **full** chord.

---

## Verified Results Worth Knowing

| Solid | Volume |
|---|---|
| $y=\sqrt x$ on $[0,4]$ about $x$-axis | $8\pi \approx 25.133$ |
| Cone, $y=\tfrac rh x$ on $[0,h]$ | $\tfrac13\pi r^2h$ |
| Sphere, $y=\sqrt{R^2-x^2}$ on $[-R,R]$ | $\tfrac43\pi R^3$ |
| Between $y=x$ and $y=x^2$ on $[0,1]$ about $x$-axis | $\tfrac{2\pi}{15}$ |
| $y=x^2$ on $[0,2]$ about $y$-axis | $8\pi$ — **by shells and by washers alike** |

---

## Other Applications

| Quantity | Integral |
|---|---|
| Displacement | $\displaystyle\int_a^b v(t)\,dt$ |
| Distance | $\displaystyle\int_a^b\lvert v(t)\rvert\,dt$ |
| Net change | $\displaystyle\int_a^b F'(x)\,dx=F(b)-F(a)$ |
| Accumulation | $F(x)=F(a)+\displaystyle\int_a^x F'(t)\,dt$ |
| Average value | $\dfrac{1}{b-a}\displaystyle\int_a^b f$ |
| Work | $\displaystyle\int_a^b F(x)\,dx$; linear spring $\tfrac12kd^2$ |

---

## Checking Your Answer

1. **Sketch.** Most errors are set-up errors.
2. **Sanity-check the sign.** Areas and volumes are positive.
3. **Compute it the other way** where possible — shells against washers. Two independent set-ups
   agreeing is the strongest check available.
4. **Verify numerically.** Simpson's rule in ten lines will confirm any integral in this course.

---

*MATH 141 · Week 11 · Reference · © CSE Department*
