# MATH 141 — Problem Set 6 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

---


## Marking Scheme

Point values are printed per problem on the problem set. Within each problem, split the marks:

- **Method (≈60%).** Correct technique named and set up: the right rule or theorem, hypotheses checked where the theorem requires it, and the symbolic work shown before any numerical evaluation.
- **Execution (≈40%).** Correct algebra and simplification, correct final form, and any domain restrictions or constants of integration stated.

A bare answer with no working earns at most the execution marks — and in proof problems ("show that", "prove"), no marks at all, since the reasoning *is* the deliverable.

**Carry-through.** Penalise a given error once. If the student proceeds correctly from their own wrong intermediate value, award the downstream marks in full.

**Equivalent forms.** Accept any algebraically equivalent answer — factored or expanded, and trigonometric identities applied or not — unless the problem explicitly demands a particular form.

### Common errors in this problem set

**1. Only checking where f′ = 0.** Critical points also occur where f′ is **undefined** but f is defined. Corners and cusps are routinely missed.

**2. Omitting endpoints for absolute extrema.** On a closed interval the absolute extrema may occur at endpoints. The Closed Interval Method requires evaluating f at critical points *and* both endpoints.

**3. Applying the MVT/Rolle without verifying hypotheses.** Continuity on [a,b] and differentiability on (a,b) must both be checked. |x| on [−1,1] is the standard counterexample.

**4. Treating an inconclusive second-derivative test as 'no extremum'.** f″(c) = 0 tells you nothing. Fall back to the first-derivative sign test — x⁴ at 0 is a minimum despite f″(0) = 0.

---

## Part A — Absolute Extrema

**A1(a).** $f'(x)=3x^2-12x+9=3(x-1)(x-3)$. Critical numbers: $x=1,3$.

**A1(b).** $g'(x)=\dfrac{1\cdot(x^2+3)-(x-1)(2x)}{(x^2+3)^2}=\dfrac{x^2+3-2x^2+2x}{(x^2+3)^2}=\dfrac{-x^2+2x+3}{(x^2+3)^2}=\dfrac{-(x-3)(x+1)}{(x^2+3)^2}$

Critical numbers: $x=3,-1$.

**A1(c).** $h(x)=x^{1/3}(x+4)=x^{4/3}+4x^{1/3}$

$h'(x)=\dfrac43x^{1/3}+\dfrac43x^{-2/3}=\dfrac43x^{-2/3}(x+1)$

Critical numbers: $x=-1$ (where $h'=0$) and $x=0$ (where $h'$ undefined).

**A1(d).** $k'(x)=-2\sin x+1=0 \implies \sin x=1/2 \implies x=\pi/6, 5\pi/6$ in $[0,2\pi]$.

---

## Part A2

**A2(a).** $f(x)=x^3-3x+1$ on $[-2,3]$.

$f'(x)=3x^2-3=0 \implies x=\pm1$.

$f(-2)=-8+6+1=-1$; $f(-1)=-1+3+1=3$; $f(1)=1-3+1=-1$; $f(3)=27-9+1=19$.

**Max: 19 at $x=3$. Min: $-1$ at $x=-2$ and $x=1$.**

**A2(b).** $f(x)=\dfrac{x}{x^2+4}$ on $[0,4]$.

$f'(x)=\dfrac{(x^2+4)-x(2x)}{(x^2+4)^2}=\dfrac{4-x^2}{(x^2+4)^2}=0\implies x=\pm2$. Only $x=2\in[0,4]$.

$f(0)=0$; $f(2)=2/8=0.25$; $f(4)=4/20=0.2$.

**Max: 0.25 at $x=2$. Min: 0 at $x=0$.**

**A2(c).** $f(x)=x-2\sin x$ on $[0,2\pi]$.

$f'(x)=1-2\cos x=0\implies\cos x=1/2\implies x=\pi/3,5\pi/3$.

$f(0)=0$; $f(\pi/3)=\pi/3-2(\sqrt3/2)=\pi/3-\sqrt3\approx-0.685$; $f(5\pi/3)=5\pi/3-2(-\sqrt3/2)=5\pi/3+\sqrt3\approx6.964$; $f(2\pi)=2\pi\approx6.283$.

**Max: $5\pi/3+\sqrt3\approx6.964$ at $x=5\pi/3$. Min: $\pi/3-\sqrt3\approx-0.685$ at $x=\pi/3$.**

---

**A3.** Candidates: $f(0)=4$, $f(5)=4$, $f(2)=9$, $f(4)=1$.

**Absolute max: 9 at $x=2$. Absolute min: 1 at $x=4$.**

This is guaranteed by the **Extreme Value Theorem** (assuming $f$ is continuous on the closed interval $[0,5]$, which is given).

---

## Part B — Rolle's Theorem and MVT

**B1(a).** $f(x)=x^2-2x$; continuous & differentiable everywhere (polynomial). $f(0)=0$, $f(2)=0$ ✓. Applies.

$f'(x)=2x-2=0\implies x=1\in(0,2)$. $c=1$.

**B1(b).** $f(x)=1-x^{2/3}$; $f'(x)=-\dfrac23x^{-1/3}$, undefined at $x=0\in(-1,1)$. **Rolle's Theorem does NOT apply** — differentiability on the open interval fails.

**B1(c).** $f(x)=\tan x$ on $[0,\pi]$; discontinuous at $x=\pi/2\in(0,\pi)$ (vertical asymptote). **Does NOT apply** — continuity on $[0,\pi]$ fails.

---

**B2(a).** $f(x)=x^3+x-1$; polynomial, continuous & differentiable everywhere. Applies on $[0,2]$.

$\dfrac{f(2)-f(0)}{2-0}=\dfrac{9-(-1)}{2}=5$

$f'(x)=3x^2+1=5\implies x^2=4/3\implies x=2/\sqrt3\approx1.155\in(0,2)$. $c=2/\sqrt3$.

**B2(b).** $f(x)=\sqrt{x+1}$; continuous on $[0,3]$, differentiable on $(0,3)$ (note: even at $x=-1$ boundary isn't in our interval, so fine). Applies.

$\dfrac{f(3)-f(0)}{3}=\dfrac{2-1}{3}=\dfrac13$

$f'(x)=\dfrac{1}{2\sqrt{x+1}}=\dfrac13\implies\sqrt{x+1}=1.5\implies x+1=2.25\implies x=1.25\in(0,3)$. $c=1.25$.

---

**B3.** $f(x)=x^5+2x-3$ is a polynomial (continuous, differentiable everywhere).

Existence: $f(0)=-3<0$, $f(1)=1+2-3=0$. Actually $f(1)=0$ exactly — so $x=1$ IS a root.

Let's verify uniqueness: $f'(x)=5x^4+2>0$ always (since $5x^4\geq0$ and $+2$). So $f'$ never zero.

If there were two roots $a<b$, Rolle's Theorem would guarantee $f'(c)=0$ for some $c\in(a,b)$ — contradiction. So **at most one root**. Combined with $f(1)=0$: **exactly one real root, at $x=1$.**

---

**B4.** Let $s(t)$ = position along the road, $t\in[0,1.5]$ hours, with $s(0)=0$, $s(1.5)=45$ km.

Assuming the cyclist's position is continuous (physical motion) and differentiable (velocity well-defined, no instantaneous jumps) — reasonable physical assumptions — the MVT applies:

$$\exists\,c\in(0,1.5): s'(c)=\frac{45-0}{1.5-0}=30\text{ km/h}$$

So at some instant, the cyclist's instantaneous speed was exactly 30 km/h. $\square$

---

**B5.** Fix $x<y$. Apply MVT to $f(t)=\sin t$ on $[x,y]$: $f$ is continuous and differentiable everywhere.

$$\exists\,c\in(x,y): \frac{\sin y-\sin x}{y-x}=\cos c$$

Since $|\cos c|\leq1$:

$$\left|\frac{\sin y-\sin x}{y-x}\right|\leq1 \implies |\sin y-\sin x|\leq|y-x| \quad\square$$

*(This is a Lipschitz continuity result — $\sin$ is 1-Lipschitz.)*

---

## Part C — Shape of a Graph

**C1.** $f(x)=x^3-3x^2-9x+5$

$f'(x)=3x^2-6x-9=3(x-3)(x+1)$. Critical: $x=-1,3$.

Sign of $f'$: $+$ on $(-\infty,-1)$, $-$ on $(-1,3)$, $+$ on $(3,\infty)$.

**Increasing:** $(-\infty,-1)\cup(3,\infty)$. **Decreasing:** $(-1,3)$.

$x=-1$: local max, $f(-1)=-1-3+9+5=10$. $x=3$: local min, $f(3)=27-27-27+5=-22$.

$f''(x)=6x-6=0\implies x=1$. Sign: $-$ for $x<1$, $+$ for $x>1$.

**Concave down** on $(-\infty,1)$, **concave up** on $(1,\infty)$.

$f(1)=1-3-9+5=-6$, so the **inflection point is $(1,-6)$**.

> **Marking note.** Substituting $x=1$ into $f$ is where sign errors cluster — evaluating the two
> negative terms as positive gives $-1-3+9+5=10$ and a badly wrong point. Since $x=1$ makes every
> power equal 1, the value is just the sum of the coefficients: $1-3-9+5=-6$. That is the fastest
> check available, and worth teaching.

---

**C2.** $f(x)=3x^4-4x^3$

$f'(x)=12x^3-12x^2=12x^2(x-1)$. Critical: $x=0,1$.

Sign: $-$ on $(-\infty,0)$, $-$ on $(0,1)$, $+$ on $(1,\infty)$ (since $x^2\geq0$ always, sign driven by $(x-1)$; at $x=0$ no sign change).

**Decreasing** $(-\infty,1)$, **increasing** $(1,\infty)$. $x=0$: not an extremum (no sign change). $x=1$: local min, $f(1)=3-4=-1$.

$f''(x)=36x^2-24x=12x(3x-2)$. Zero at $x=0,2/3$.

Sign: $+$ on $(-\infty,0)$, $-$ on $(0,2/3)$, $+$ on $(2/3,\infty)$.

Inflection points at $x=0$ ($f(0)=0$) and $x=2/3$ ($f(2/3)=3(16/81)-4(8/27)=48/81-32/27=16/27-32/27=-16/27$).

---

**C3.** $f(x)=\dfrac{x^2}{x^2+3}$

$f'(x)=\dfrac{2x(x^2+3)-x^2(2x)}{(x^2+3)^2}=\dfrac{2x^3+6x-2x^3}{(x^2+3)^2}=\dfrac{6x}{(x^2+3)^2}$

Critical: $x=0$. Sign: $-$ for $x<0$, $+$ for $x>0$.

**Decreasing** $(-\infty,0)$, **increasing** $(0,\infty)$. Local min at $x=0$, $f(0)=0$.

$f''(x)$: differentiate $\dfrac{6x}{(x^2+3)^2}$ using quotient rule:

$f''(x)=\dfrac{6(x^2+3)^2-6x\cdot2(x^2+3)(2x)}{(x^2+3)^4}=\dfrac{6(x^2+3)-24x^2}{(x^2+3)^3}=\dfrac{6x^2+18-24x^2}{(x^2+3)^3}=\dfrac{18-18x^2}{(x^2+3)^3}=\dfrac{18(1-x^2)}{(x^2+3)^3}$

Zero at $x=\pm1$. Sign: $-$ for $x<-1$, $+$ for $-1<x<1$, $-$ for $x>1$.

**Concave down** $(-\infty,-1)$, **up** $(-1,1)$, **down** $(1,\infty)$. Inflection at $x=\pm1$: $f(\pm1)=1/4$.

---

**C4.** $f(x)=xe^{-x^2}$

$f'(x)=e^{-x^2}+x(-2x)e^{-x^2}=e^{-x^2}(1-2x^2)$

Critical: $1-2x^2=0\implies x=\pm1/\sqrt2$.

Sign of $f'$ (since $e^{-x^2}>0$ always, sign follows $1-2x^2$): $-$ for $x<-1/\sqrt2$, $+$ for $-1/\sqrt2<x<1/\sqrt2$, $-$ for $x>1/\sqrt2$.

**Decreasing** $(-\infty,-1/\sqrt2)$, **increasing** $(-1/\sqrt2,1/\sqrt2)$, **decreasing** $(1/\sqrt2,\infty)$.

$x=-1/\sqrt2$: local min. $x=1/\sqrt2$: local max.

$f''(x)=-2xe^{-x^2}(1-2x^2)+e^{-x^2}(-4x)=e^{-x^2}[-2x(1-2x^2)-4x]=e^{-x^2}[-2x+4x^3-4x]=e^{-x^2}(4x^3-6x)=2xe^{-x^2}(2x^2-3)$

Zero at $x=0,\pm\sqrt{3/2}$.

Sign analysis gives concavity changes at all three — three inflection points.

---

**C5.** $f(x)=x-2\sin x$ on $[0,2\pi]$

$f'(x)=1-2\cos x=0\implies\cos x=1/2\implies x=\pi/3,5\pi/3$

Sign: at $x=0$: $f'(0)=1-2=-1<0$. Between $\pi/3$ and $5\pi/3$: at $x=\pi$, $f'(\pi)=1-2(-1)=3>0$. Beyond $5\pi/3$: at $x=2\pi$, $f'=1-2=-1<0$.

**Decreasing** $(0,\pi/3)$, **increasing** $(\pi/3,5\pi/3)$, **decreasing** $(5\pi/3,2\pi)$.

$x=\pi/3$: local min. $x=5\pi/3$: local max.

$f''(x)=2\sin x=0\implies x=0,\pi,2\pi$ in $[0,2\pi]$.

Sign: $+$ on $(0,\pi)$, $-$ on $(\pi,2\pi)$. Inflection at $x=\pi$ (interior point).

---

## Part D — Second Derivative Test

**D1(a).** $f(x)=x^4-4x^2$; $f'(x)=4x^3-8x=4x(x^2-2)$. Critical: $x=0,\pm\sqrt2$.

$f''(x)=12x^2-8$.

$f''(0)=-8<0$: local max. $f''(\pm\sqrt2)=24-8=16>0$: local min at both.

**D1(b).** $f(x)=x^5$; $f'(x)=5x^4=0\implies x=0$. $f''(x)=20x^3$; $f''(0)=0$ — **inconclusive**.

First Derivative Test: $f'(x)=5x^4\geq0$ always, never negative. No sign change (positive on both sides). **Not an extremum** (inflection with horizontal tangent).

**D1(c).** $f(x)=x^3-3x^2+3x-1=(x-1)^3$; $f'(x)=3x^2-6x+3=3(x-1)^2=0\implies x=1$.

$f''(x)=6x-6$; $f''(1)=0$ — **inconclusive**.

First Derivative Test: $f'(x)=3(x-1)^2\geq0$ always. No sign change. **Not an extremum.**

---

**D2.** Example: $f(x)=x^4$. $f'(x)=4x^3$, $f'(0)=0$. $f''(x)=12x^2$, $f''(0)=0$.

First Derivative Test: $f'(x)=4x^3<0$ for $x<0$, $>0$ for $x>0$ — sign change negative to positive: **local minimum at $x=0$.** ✓

---

## Part E

**E1.** Sketch: decreasing then increasing pattern with max at $x=-1$ (value 4), min at $x=3$ (value $-2$), concave down until $x=1$, concave up after. Point $(1,1)$ is the inflection point (roughly midway in value between the extrema, consistent with concavity switch inside the decreasing interval).

**E2.** $g'(x)=(x-1)^2(x-3)$

(a) Critical numbers: $x=1,3$.

(b) Sign of $g'$: $(x-1)^2\geq0$ always; sign driven by $(x-3)$. Negative for $x<3$ (except possibly at $x=1$ where it's zero), positive for $x>3$.

**Decreasing** on $(-\infty,1)\cup(1,3)$ [effectively $(-\infty,3)$ with a flat point at $x=1$], **increasing** on $(3,\infty)$.

(c) $x=1$: no sign change (negative both sides) — **not an extremum**. $x=3$: negative to positive — **local minimum**.

(d) $g''(x)=2(x-1)(x-3)+(x-1)^2=(x-1)[2(x-3)+(x-1)]=(x-1)(3x-7)$

Zero at $x=1, 7/3$. Sign: $+$ for $x<1$, $-$ for $1<x<7/3$, $+$ for $x>7/3$.

**Concave up** $(-\infty,1)\cup(7/3,\infty)$, **concave down** $(1,7/3)$.

---

**E3.** $f(x)=\dfrac{x^2-1}{x^2+1}$

**Domain:** $\mathbb{R}$ (denominator never zero).

**Symmetry:** $f(-x)=f(x)$ — even function, symmetric about $y$-axis.

**Intercepts:** $f(0)=-1$. $x$-intercepts: $x^2-1=0\implies x=\pm1$.

**Derivative:** $f'(x)=\dfrac{2x(x^2+1)-(x^2-1)(2x)}{(x^2+1)^2}=\dfrac{2x[(x^2+1)-(x^2-1)]}{(x^2+1)^2}=\dfrac{4x}{(x^2+1)^2}$

Critical: $x=0$. **Decreasing** $(-\infty,0)$, **increasing** $(0,\infty)$. Local (and absolute) min at $x=0$: $f(0)=-1$.

**Second derivative:** $f''(x)=\dfrac{4(x^2+1)^2-4x\cdot2(x^2+1)(2x)}{(x^2+1)^4}=\dfrac{4(x^2+1)-16x^2}{(x^2+1)^3}=\dfrac{4-12x^2}{(x^2+1)^3}$

Zero at $x=\pm1/\sqrt3$. **Concave up** $(-1/\sqrt3,1/\sqrt3)$, **concave down** elsewhere. Inflection at $x=\pm1/\sqrt3$: $f(\pm1/\sqrt3)=\dfrac{1/3-1}{1/3+1}=\dfrac{-2/3}{4/3}=-\dfrac12$.

**Asymptote:** as $x\to\pm\infty$, $f(x)\to1$. Horizontal asymptote $y=1$.

---

## Part F

**F1.** $f(x)=x^3$. $f'(0)=0$ but $x=0$ is neither a local max nor min: for $x<0$, $f(x)<0=f(0)$; for $x>0$, $f(x)>0=f(0)$. The function passes through $(0,0)$ without turning — it's an inflection point with horizontal tangent, not an extremum. By definition, a local max requires $f(x)\leq f(0)$ for ALL $x$ near 0, but for $x>0$ we have $f(x)>f(0)$ — violating this.

**F2.** Take any $x_1<x_2$. By MVT on $[x_1,x_2]$: $f(x_2)-f(x_1)=f'(c)(x_2-x_1)$ for some $c\in(x_1,x_2)$.

If $f'(c)>0$: done, $f(x_2)>f(x_1)$.

If $f'(c)=0$: since $f'=0$ at only finitely many points, we can choose a slightly different sub-interval avoiding that point (or apply MVT to a nearby sub-interval within $[x_1,x_2]$ where $f'\neq0$ somewhere, since $f'\geq0$ everywhere and can't be identically zero on any sub-interval by the finiteness assumption). This guarantees $f(x_2)>f(x_1)$ strictly. Hence $f$ is strictly increasing. $\square$

**F3.** Rolle's Theorem is a **special case** of the MVT (when $f(a)=f(b)$, the average rate of change is 0, so MVT gives $f'(c)=0$ — exactly Rolle's conclusion). However, in the standard development, Rolle's Theorem is proved FIRST (directly from the EVT and Fermat's Theorem), and then the MVT is proved USING Rolle's Theorem (via the auxiliary function $g(x)$ that subtracts the secant line). So logically: Rolle's Theorem is used as a tool to prove the more general MVT, even though MVT "contains" Rolle's Theorem as a special case.

**F4 (Bonus).** $f(t)=e^t-1-t$. $f(0)=1-1-0=0$.

$f'(t)=e^t-1$. For $t\geq0$: $e^t\geq1$ (since $e^t$ is increasing and $e^0=1$), so $f'(t)\geq0$ for $t\geq0$.

By the I/D Test (MVT Corollary 3), $f$ is non-decreasing on $[0,\infty)$. Since $f(0)=0$ and $f$ is non-decreasing, $f(t)\geq f(0)=0$ for all $t\geq0$.

Therefore $e^t-1-t\geq0 \implies e^t\geq1+t$ for all $t\geq0$. $\square$
