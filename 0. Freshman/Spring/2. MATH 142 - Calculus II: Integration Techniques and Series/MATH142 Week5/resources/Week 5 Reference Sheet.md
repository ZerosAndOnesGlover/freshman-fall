# MATH 142 · Calculus II
## Week 5 · Reference Sheet
### Parametric Curves; Polar Coordinates

---

## Parametric Curves

$$x=x(t),\qquad y=y(t),\qquad t\in[\alpha,\beta]$$

A **path**, with a direction and a speed — not just a set of points. It can describe self-intersections, vertical tangents, cusps and closed curves, none of which $y=f(x)$ can.

### Standard parametrisations

| Curve | Parametrisation |
|---|---|
| $y=f(x)$ on $[a,b]$ | $x=t$, $y=f(t)$ |
| circle, centre $(h,k)$, radius $r$ | $x=h+r\cos t$, $y=k+r\sin t$ |
| ellipse | $x=h+a\cos t$, $y=k+b\sin t$ |
| segment $P\to Q$ | $P+t(Q-P)$, $t\in[0,1]$ |
| **cycloid** (radius $a$) | $x=a(t-\sin t)$, $y=a(1-\cos t)$ |
| **astroid** | $x=a\cos^3t$, $y=a\sin^3t$ |

**Eliminate the parameter** by solving-and-substituting, or with $\cos^2+\sin^2=1$. **Elimination loses the range and the orientation, and is often impossible.**

### Calculus

$$\frac{dy}{dx} = \frac{dy/dt}{dx/dt} \qquad\qquad \frac{d^2y}{dx^2} = \frac{\dfrac{d}{dt}\!\left(\dfrac{dy}{dx}\right)}{\dfrac{dx}{dt}}$$

> **$\dfrac{d^2y}{dx^2}$ is NOT $\dfrac{d^2y/dt^2}{d^2x/dt^2}$.**

| | Tangent |
|---|---|
| $dy/dt=0$, $dx/dt\ne0$ | horizontal |
| $dx/dt=0$, $dy/dt\ne0$ | **vertical** |
| both zero | inconclusive — often a cusp; take the limit |

$$\text{Area } = \int_\alpha^\beta y(t)\,x'(t)\,dt \qquad L = \int_\alpha^\beta\sqrt{\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2}dt$$

$$S = 2\pi\int_\alpha^\beta y(t)\sqrt{\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2}dt \quad\text{(about the }x\text{-axis)}$$

**Arc length is $\int(\text{speed})\,dt$ — distance travelled.** Tracing the circle twice gives $4\pi$. **Check the range traces the curve exactly once.**

---

## Polar Coordinates

$$x=r\cos\theta,\quad y=r\sin\theta \qquad\qquad r^2=x^2+y^2,\quad \tan\theta=\frac yx$$

**$\tan\theta=y/x$ needs a quadrant check** — $\arctan$ only returns $\left(-\frac\pi2,\frac\pi2\right)$.

**Not unique:** $(r,\theta)\sim(r,\theta+2\pi k)\sim(-r,\theta+\pi)$; the origin is $(0,\theta)$ for every $\theta$.

### Standard curves

| Equation | Curve |
|---|---|
| $r=a$ | circle at the origin |
| $r=2a\cos\theta$ | circle radius $a$, centre $(a,0)$ — **traced once on $\left[-\frac\pi2,\frac\pi2\right]$** |
| $r=a(1+\cos\theta)$ | cardioid |
| $r=a\cos n\theta$ | rose: $n$ petals if $n$ odd, $2n$ if even |
| $r=a\theta$ | Archimedean spiral |

**To convert to Cartesian, multiply by $r$:** $r=2a\cos\theta \Rightarrow r^2=2ar\cos\theta \Rightarrow x^2+y^2=2ax$.

### Area and arc length

$$\boxed{A = \frac12\int_\alpha^\beta r^2\,d\theta} \qquad\qquad \boxed{L = \int_\alpha^\beta\sqrt{r^2+\left(\frac{dr}{d\theta}\right)^2}\,d\theta}$$

**The $\frac12$ comes from the circular sector** ($\frac12r^2\Delta\theta$), not from anywhere else. Slice by **angle**, approximate by a **wedge**.

Between two curves: $A=\frac12\int\left[r_{\text{out}}^2-r_{\text{in}}^2\right]d\theta$ — **squares subtract.**

> **Finding the limits is harder than the integral.** Locate where $r=0$; check whether the curve is
> traced more than once. Integrating $r=2a\cos\theta$ over $[0,2\pi]$ gives **twice** the area.

---

## Verified Results

| Curve | Quantity | Value |
|---|---|---|
| Cycloid, one arch | arc length | $\boldsymbol{8a}$ |
| Cycloid, one arch | area under | $3\pi a^2$ |
| Cycloid, one arch | surface (about $x$-axis) | $\frac{64\pi a^2}{3}$ |
| Astroid | total arc length | $6a$ |
| Cardioid $r=1+\cos\theta$ | area | $\frac{3\pi}{2}$ |
| Cardioid $r=1+\cos\theta$ | perimeter | $\boldsymbol{8}$ |
| Rose $r=\cos2\theta$ | one petal | $\frac\pi8$ |
| Circle $r=2a\cos\theta$ | area | $\pi a^2$ |
| **Ellipse** $a\ne b$ | perimeter | **no closed form** |

*(all verified)*

### Why some collapse and some do not

The cycloid and cardioid both produce $\sqrt{2\pm2\cos\theta}$, and a **half-angle identity** turns it into a perfect square:

$$2-2\cos t = 4\sin^2\tfrac t2 \qquad\qquad 2+2\cos\theta = 4\cos^2\tfrac\theta2$$

**The square root disappears, and the integral is elementary.**

The ellipse gives $\sqrt{a^2\sin^2t+b^2\cos^2t}$, which is a **genuine quadratic in $\sin t$** when $a\ne b$ and admits no such collapse. It is an **elliptic integral** — the same obstruction as the arc length of $y=\sin x$ (Week 4).

> **The cycloid cannot even be written as $y=f(x)$, and has arc length exactly $8a$. The ellipse has
> been studied since 200 BC and has no formula for its perimeter. Tractability is not predictable
> from appearance.**

### What is used instead

Ramanujan (1914): $\;P\approx\pi\left[3(a+b)-\sqrt{(3a+b)(a+3b)}\right]$

Relative error: $3.7\times10^{-9}$ at $b/a=0.8$; $2.8\times10^{-6}$ at $b/a=0.5$; still only $0.34\%$ at $b/a=0.01$. *(Measured.)*

---

## Traps

1. **Range of the parameter** — traced once? Arc length measures *distance travelled*.
2. **Take absolute values of speed**, and split at sign changes. (The astroid integrates to **zero** otherwise.)
3. **$\frac{d^2y}{dx^2}$ is not a ratio of second derivatives.**
4. **The $\frac12$ in polar area.**
5. **Polar limits** — find where $r=0$.
6. **Polar coordinates are not unique**, so two curves can meet at a point their equations never jointly satisfy.

---

*MATH 142 · Week 5 · Reference Sheet*
