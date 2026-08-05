# MATH 142 · Calculus II
## Week 4 · Reference Sheet
### Volumes of Revolution, Arc Length, Surface Area

---

## The Pattern

> **Slice. Approximate. Sum. Take the limit.**

| Quantity | Slice | Each piece ≈ | Formula |
|---|---|---|---|
| Volume, general | ⊥ to an axis | a slab of area $A(x)$ | $V=\int_a^b A(x)\,dx$ |
| Volume, discs | ⊥ to the axis of rotation | a disc | $V=\pi\int f^2\,dx$ |
| Volume, washers | ⊥ to the axis | an annulus | $V=\pi\int(R^2-r^2)\,dx$ |
| Volume, shells | ∥ to the axis | a thin tube | $V=2\pi\int (\text{rad})(\text{ht})\,dx$ |
| Arc length | short arcs | a straight chord | $L=\int\sqrt{1+(f')^2}\,dx$ |
| Surface area | bands | a frustum | $S=2\pi\int(\text{rad})\,ds$ |

**Learn the pattern, not the formulas.**

---

## Volumes of Revolution

### Discs and washers — slice perpendicular to the axis

$$V = \pi\int_a^b\big(f(x)\big)^2dx \qquad\qquad V = \pi\int_a^b\Big[R(x)^2-r(x)^2\Big]dx$$

> $$R^2-r^2 \qquad\textbf{never}\qquad (R-r)^2$$

### Shells — slice parallel to the axis

$$V = 2\pi\int_a^b x\,f(x)\,dx \qquad\text{about the } y\text{-axis}$$

Read it as $2\pi\int(\text{radius})\times(\text{height})\ d(\text{thickness})$ — a tube, unrolled into a sheet.

### Radii for shifted axes

| Axis | Radius of the curve |
|---|---|
| $y=0$ | $\lvert f(x)\rvert$ |
| $y=c$ | $\lvert f(x)-c\rvert$ |
| $x=0$ | $\lvert x\rvert$ |
| $x=c$ | $\lvert x-c\rvert$ |

**The radius is a distance to the axis. The height never changes when the axis moves.**

### Choosing a method

> **Choose the method that avoids inverting the function.**
> Axis ⊥ to the variable your functions are written in → **shells**.
> Axis ∥ to it → **discs**.

**Two methods on one solid is a free check.**

### Standard results, derived this week

| Solid | Volume |
|---|---|
| Sphere, radius $r$ | $\tfrac43\pi r^3$ |
| Cone, radius $r$, height $h$ | $\tfrac13\pi r^2h$ |
| Torus, tube radius $a$, centre radius $R$ | $2\pi^2a^2R$ |

*(all verified)* — the torus result is $(\pi a^2)\times(2\pi R)$, an instance of **Pappus's theorem**.

---

## Arc Length

$$\boxed{L = \int_a^b\sqrt{1+\big(f'(x)\big)^2}\,dx} \qquad\qquad L = \int_c^d\sqrt{1+\big(g'(y)\big)^2}\,dy$$

Pythagoras on a chord, in the limit. **The inscribed polygon converges at $O(1/n^2)$ and always underestimates** — a chord is shorter than its arc.

### Worked lengths

| Curve | Interval | Length | |
|---|---|---|---|
| $y=\tfrac23x^{3/2}$ | $[0,3]$ | $\tfrac{14}{3}$ | easy |
| $y=x^{3/2}$ | $[0,1]$ | $\dfrac{13\sqrt{13}-8}{27}\approx1.4397$ | easy |
| $y=x^2$ | $[0,1]$ | $\dfrac{\sqrt5}{2}+\dfrac{\operatorname{arcsinh}2}{4}\approx1.4789$ | trig substitution |
| $y=\ln(\cos x)$ | $[0,\tfrac\pi4]$ | $\ln(1+\sqrt2)\approx0.8814$ | becomes $\int\sec$ |
| $y=\cosh x$ | $[0,1]$ | $\sinh1\approx1.1752$ | uses $1+\sinh^2=\cosh^2$ |
| $y=e^x$ | $[0,1]$ | $\approx2.0035$ | **elementary**, via $u=e^x$ |
| $y=\sin x$ | $[0,\pi]$ | $\approx3.8202$ | **not elementary** — elliptic |

*(all verified)*

> **$\sqrt{1+(f')^2}$ is almost never elementary.** Textbook curves are chosen so that it is. The
> arc length of a *sine curve* — and equally the perimeter of an ellipse — has no closed form.

$\operatorname{arcsinh}u = \ln\!\big(u+\sqrt{u^2+1}\big)$, so $\tfrac{\operatorname{arcsinh}2}{4} = \tfrac14\ln(2+\sqrt5)$. **Both forms are correct.**

---

## Surface Area of Revolution

$$\boxed{S = 2\pi\int_a^b f(x)\sqrt{1+\big(f'(x)\big)^2}\,dx} \quad\text{about the } x\text{-axis}$$

$$S = 2\pi\int_a^b x\sqrt{1+\big(f'(x)\big)^2}\,dx \quad\text{about the } y\text{-axis}$$

**Radius × the arc length element $ds$ — not $dx$.** Each band is a *frustum*, not a cylinder; the slant is what a steep band's extra surface comes from.

### Standard results

| Surface | Area |
|---|---|
| Sphere, radius $r$ | $4\pi r^2$ |
| $y=\sqrt x$ on $[0,4]$ about the $x$-axis | $\dfrac{\pi(17\sqrt{17}-1)}{6}\approx36.177$ |
| $y=x^3$ on $[0,1]$ about the $x$-axis | $\dfrac{\pi(10\sqrt{10}-1)}{27}\approx3.5631$ |

*(all verified)*

**The sphere works because the two square roots cancel exactly**, leaving a constant integrand — Archimedes' theorem, and the reason equal parallel slices of a sphere have equal surface area.

**Combine radicals before integrating:** $\sqrt x\sqrt{1+\tfrac{1}{4x}} = \sqrt{x+\tfrac14}$.

---

## Gabriel's Horn (Lab 4)

Rotate $y=\dfrac1x$, $x\ge1$, about the $x$-axis:

$$V = \pi\int_1^\infty\frac{dx}{x^2} = \boldsymbol{\pi} \qquad\qquad S = 2\pi\int_1^\infty\frac1x\sqrt{1+\frac1{x^4}}\,dx = \boldsymbol{\infty}$$

*(both verified)*

- **Volume converges** by the $p$-test, $p=2>1$.
- **Surface diverges** by comparison: $\sqrt{1+x^{-4}}\ge1$, so the integrand is $\ge\frac1x$, and $\int_1^\infty\frac{dx}{x}$ diverges.

**Finite volume, infinite surface.** The two integrals land on opposite sides of the $p=1$ threshold.

**Truncated at $T$:** $V(T) = \pi\left(1-\tfrac1T\right)$, and $S(T)/(2\pi\ln T)\to1$.

| $T$ | $V(T)$ | $S(T)$ |
|---|---|---|
| $10^2$ | 3.1102 | 29.65 |
| $10^6$ | 3.14159 | 87.52 |

**$V$ visibly converges; $S$ grows like $2\pi\ln T$ and is not visibly anything** — Lab 3's lesson again.

**The paradox is not one:** "filling" needs a *volume*; "coating with thickness $d$" needs *area × $d$*. Beyond $x = 1/d$ the horn is narrower than the paint layer, so the two operations are not comparable.

---

## Checklist

1. **Draw the region and the axis.** Every recurring error is a missing picture.
2. **Radius = distance to the axis.**
3. **$R^2-r^2$.**
4. **Surface area uses $ds$, not $dx$.**
5. **Combine radicals before integrating.**
6. **Check for symmetry** — it works on solids too.
7. **Two methods agreeing is a free check.**

---

*MATH 142 · Week 4 · Reference Sheet*
