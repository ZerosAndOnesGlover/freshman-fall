# MATH 142 · Calculus II
## Week 5 · Lecture 2 (Tuesday)
### Calculus with Parametric Curves

---

**Reading:** Stewart §10.2 | Apostol Ch. 2 §2.14

---

## 1. The Slope

The curve has a tangent even where it is not a graph. What is $\dfrac{dy}{dx}$ when both $x$ and $y$ are functions of $t$?

**The chain rule.** Treating $y$ as a function of $x$ and $x$ as a function of $t$:

$$\frac{dy}{dt} = \frac{dy}{dx}\cdot\frac{dx}{dt} \implies \boxed{\frac{dy}{dx} = \frac{dy/dt}{dx/dt}\qquad\text{provided } \frac{dx}{dt}\neq0}$$

**The $dt$'s cancel** — which is exactly why Leibniz notation is worth the trouble.

### Horizontal and vertical tangents

| Condition | Tangent |
|---|---|
| $\dfrac{dy}{dt}=0$ and $\dfrac{dx}{dt}\neq0$ | **horizontal** |
| $\dfrac{dx}{dt}=0$ and $\dfrac{dy}{dt}\neq0$ | **vertical** |
| **both zero** | inconclusive — often a **cusp**; examine further |

> **The vertical case is the payoff.** For $y=f(x)$, a vertical tangent means $f'$ does not exist and
> the description breaks down. Parametrically it is simply the case $\frac{dx}{dt}=0$ — a perfectly
> ordinary point of the motion where the horizontal velocity is momentarily zero. **The curve was
> never the problem; the description was.**

### Example 1 — the cycloid

$$x=a(t-\sin t),\qquad y = a(1-\cos t)$$

$$\frac{dx}{dt} = a(1-\cos t),\qquad \frac{dy}{dt} = a\sin t$$

$$\frac{dy}{dx} = \frac{a\sin t}{a(1-\cos t)} = \frac{\sin t}{1-\cos t} = \boxed{\cot\frac t2}$$

**The simplification uses half-angle identities:** $\sin t = 2\sin\frac t2\cos\frac t2$ and $1-\cos t = 2\sin^2\frac t2$, so the ratio is $\frac{\cos(t/2)}{\sin(t/2)}$.

*Verified: the identity holds exactly (checked symbolically after rewriting in $\tan$, and numerically at $t=0.7,\ 1.9,\ 3.0$ to 16 significant figures).*

*(A CAS asked to `simplify` this difference returns a non-zero mess — the half-angle rewrite must be requested explicitly. **Fifth week running: the machine is a check, not an oracle.**)*

**Reading off the geometry:**

- At $t=\pi$ (the top of the arch): $\cot\frac\pi2 = 0$ — **horizontal tangent** ✓ *(verified)*
- As $t\to0^+$: $\cot\frac t2\to+\infty$ — **vertical tangent** ✓ *(verified)*

That last point is the **cusp** where the wheel touches the ground. Both $\frac{dx}{dt}$ and $\frac{dy}{dt}$ vanish at $t=0$, so the table above says "inconclusive" — and the limit resolves it.

---

## 2. The Second Derivative

$\dfrac{d^2y}{dx^2}$ is **not** $\dfrac{d^2y/dt^2}{d^2x/dt^2}$. That is a common and costly error.

Apply the rule from §1 to the function $\frac{dy}{dx}$:

$$\boxed{\frac{d^2y}{dx^2} = \frac{\dfrac{d}{dt}\!\left(\dfrac{dy}{dx}\right)}{\dfrac{dx}{dt}}}$$

**Differentiate the slope with respect to $t$, then divide by $\frac{dx}{dt}$ again.**

### Example 2

For the cycloid, $\frac{dy}{dx} = \cot\frac t2$, so $\frac{d}{dt}\left(\cot\frac t2\right) = -\frac12\csc^2\frac t2$, and

$$\frac{d^2y}{dx^2} = \frac{-\frac12\csc^2\frac t2}{a(1-\cos t)} = \frac{-\frac12\csc^2\frac t2}{2a\sin^2\frac t2} = -\frac{1}{4a\sin^4\frac t2}$$

*Verified symbolically: the CAS gives $-\dfrac{1}{a(1-\cos t)^2}$, which is the same thing since $1-\cos t = 2\sin^2\frac t2$.*

**It is negative everywhere**, so the arch is **concave down** throughout — which matches the picture.

---

## 3. Area Under a Parametric Curve

The area under $y=f(x)$ from $x=a$ to $x=b$ is $\int_a^b y\,dx$. Substituting $x=x(t)$, $dx = x'(t)\,dt$:

$$\boxed{A = \int_{\alpha}^{\beta} y(t)\,x'(t)\,dt}$$

**This is just substitution** (Week 0), applied in the direction that introduces a parameter rather than removing one.

> **Watch the orientation.** The limits $\alpha,\beta$ must correspond to $x=a,b$ **in that order.**
> If the curve is traced right-to-left, $x'(t)<0$ and the integral comes out negative — take the
> absolute value, or swap the limits.

### Example 3 — area under one arch of the cycloid

As $t$ runs $0\to2\pi$, $x$ runs $0\to2\pi a$ (left to right ✓).

$$A = \int_0^{2\pi} a(1-\cos t)\cdot a(1-\cos t)\,dt = a^2\int_0^{2\pi}(1-\cos t)^2dt$$

Expanding: $(1-\cos t)^2 = 1-2\cos t+\cos^2t$, and over a full period $\int\cos t = 0$ while $\int\cos^2 t = \pi$:

$$A = a^2\big(2\pi - 0 + \pi\big) = \boxed{3\pi a^2}$$

*Verified symbolically.*

**A beautiful result: exactly three times the area of the rolling circle** ($\pi a^2$). Galileo weighed cut-out cycloid arches against cut-out circles trying to establish this ratio experimentally, and got about 3 — but could not prove it. Roberval proved it in 1634.

---

## 4. Arc Length

Week 4 derived $L=\int\sqrt{1+(f')^2}\,dx$ by replacing arcs with chords. **The same derivation, in parametric form**, gives a more symmetric formula. A chord over $\Delta t$ has length

$$\sqrt{(\Delta x)^2+(\Delta y)^2} = \sqrt{\left(\frac{\Delta x}{\Delta t}\right)^2+\left(\frac{\Delta y}{\Delta t}\right)^2}\;\Delta t$$

so

$$\boxed{L = \int_\alpha^\beta\sqrt{\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2}\,dt}$$

**Read it as $\int(\text{speed})\,dt$** — the integral of speed over time is distance travelled, which is Week 0's net-change principle applied to motion.

> **This is why the range matters.** Tracing the circle twice gives $L=4\pi$: the formula measures
> **distance travelled**, not the length of the point set. Both are legitimate; know which you want.

### Example 4 — the circle

$x=\cos t$, $y=\sin t$: speed $=\sqrt{\sin^2t+\cos^2t}=1$, so $L = \int_0^{2\pi}1\,dt = 2\pi$ ✓ *(verified)*.

### Example 5 — the cycloid, and why it comes out clean

$$\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2 = a^2(1-\cos t)^2 + a^2\sin^2 t = a^2\big(2-2\cos t\big)$$

Now the half-angle identity again: $2-2\cos t = 4\sin^2\frac t2$, so the speed is

$$\sqrt{4a^2\sin^2\tfrac t2} = 2a\left|\sin\tfrac t2\right| = 2a\sin\tfrac t2 \qquad (t\in[0,2\pi])$$

**The square root disappears completely.** Hence

$$L = \int_0^{2\pi}2a\sin\frac t2\,dt = 2a\Big[-2\cos\tfrac t2\Big]_0^{2\pi} = 2a(2+2) = \boxed{8a}$$

*Verified symbolically, and numerically ($a=1$ gives exactly $8.0$).*

**Eight times the radius, exactly** — no $\pi$, no roots.

**Christopher Wren** — the architect of St Paul's — found this in **1658**, and stated it in the form that is easier to remember: **the arch is four times the diameter of the rolling circle.** ($4\times 2a = 8a$.) It was among the first curves other than the circle whose length was ever computed exactly.

### Example 6 — the astroid

$x=a\cos^3t$, $y=a\sin^3t$. Here

$$\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2 = 9a^2\cos^2t\sin^2t$$

*(verified)*, so the speed is $3a|\cos t\sin t|$, and by symmetry over the four quadrants

$$L = 4\int_0^{\pi/2}3a\cos t\sin t\,dt = 4\cdot\frac{3a}{2} = \boxed{6a}$$

*Verified symbolically.*

**The absolute value is essential.** Integrating $3a\cos t\sin t$ straight over $[0,2\pi]$ gives **zero**, because the integrand is negative on two quadrants. **Splitting at the sign changes is Week 0's rule, still binding.**

### Example 7 — the ellipse, which has no closed form

$x=a\cos t$, $y=b\sin t$:

$$L = \int_0^{2\pi}\sqrt{a^2\sin^2t+b^2\cos^2t}\,dt$$

**When $a\neq b$ this cannot be evaluated in elementary terms.** *(Verified: a CAS returns it unevaluated.)* It is an **elliptic integral** — and it is where the name comes from.

For $a=2$, $b=1$ the perimeter is $9.68844822054768$. *(Verified: numerical quadrature agrees with the standard elliptic-integral function to 15 significant figures.)*

> **The contrast is the lesson of the week.** The **cycloid** — a curve you cannot even write as
> $y=f(x)$ — has arc length exactly $8a$. The **ellipse** — two lines of trigonometry, known since
> antiquity — has a perimeter no finite formula can express.
>
> **Which curves are tractable is not predictable from how they look.**

---

## 5. Surface Area

Rotating a parametric curve about the $x$-axis, the same reasoning as Week 4 gives

$$\boxed{S = 2\pi\int_\alpha^\beta y(t)\sqrt{\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2}\,dt}$$

**Radius $\times$ arc length element** — the arc length element is now the parametric one.

### Example 8

Rotating one arch of the cycloid about the $x$-axis:

$$S = 2\pi\int_0^{2\pi}a(1-\cos t)\cdot2a\sin\frac t2\,dt = \boxed{\frac{64\pi a^2}{3}}$$

*Verified symbolically.*

---

## 6. What To Take From This Lecture

1. **$\dfrac{dy}{dx} = \dfrac{dy/dt}{dx/dt}$** — the chain rule, with the $dt$'s cancelling.
2. **$\dfrac{dx}{dt}=0$ is a vertical tangent**, not a breakdown.
3. **$\dfrac{d^2y}{dx^2}$ is $\dfrac{d}{dt}\!\left(\dfrac{dy}{dx}\right)\Big/\dfrac{dx}{dt}$** — *not* a ratio of second derivatives.
4. **Area: $\int y\,x'\,dt$. Arc length: $\int(\text{speed})\,dt$. Surface: $2\pi\int y\,(\text{speed})\,dt$.**
5. **Half-angle identities collapse the square roots** in the cycloid and cardioid. That is why those have closed forms and the ellipse does not.
6. **Take absolute values of speed, and split at sign changes.**

---

*Next: Wednesday — Polar Coordinates*
