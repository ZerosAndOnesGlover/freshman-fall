# MATH 141 · Problem Set 6 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Revised 2026-09-21 to match the 100-point set (Parts C–E on graph shape removed; L'Hôpital part added).*

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

**4. Applying L'Hôpital's Rule to a form that is not 0/0 or ∞/∞.** Check the form first, every time — including before each repeated application. For 0·∞, ∞−∞ and 1^∞, rewrite first; for 1^∞, remember to exponentiate at the end.

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

## Part C — L'Hôpital's Rule

*(All five limits and C2 checked with SymPy.)*

**C1(a).** Form $0/0$. $\dfrac{e^x-1}{2x}$ is still $0/0$; again: $\dfrac{e^x}{2}\to\dfrac12$. **Answer $\tfrac12$.**

**C1(b).** Form $\infty/\infty$. $\dfrac{1/x}{1/(2\sqrt{x})}=\dfrac{2}{\sqrt{x}}\to0$. **Answer $0$.**

**C1(c).** Form $0\cdot(-\infty)$. Write $\dfrac{\ln x}{1/x}$ ($-\infty/\infty$): $\dfrac{1/x}{-1/x^2}=-x\to0$. **Answer $0$.**

**C1(d).** Form $\infty-\infty$. Combine: $\dfrac{\sin x-x}{x\sin x}$ ($0/0$). Then
$\dfrac{\cos x-1}{\sin x+x\cos x}$ ($0/0$), then $\dfrac{-\sin x}{2\cos x-x\sin x}\to\dfrac{0}{2}=0$. **Answer $0$.**

**C1(e).** Form $1^\infty$. $\ln y=x\ln(1+3/x)=\dfrac{\ln(1+3/x)}{1/x}$ ($0/0$). Differentiating:
$\dfrac{\frac{-3/x^2}{1+3/x}}{-1/x^2}=\dfrac{3}{1+3/x}\to3$. So $y\to e^3$. **Answer $e^3$.**
Common error: stopping at $\ln y\to3$.

**C2.** One application gives $\lim(1+\cos x)$, which oscillates between 0 and 2 and does not exist.
L'Hôpital's Rule only says *if* $\lim f'/g'$ exists, then $\lim f/g$ equals it; when it does not exist the
rule says nothing. Directly: $\dfrac{x+\sin x}{x}=1+\dfrac{\sin x}{x}$ and $\left|\dfrac{\sin x}{x}\right|\le\dfrac1x\to0$
(Squeeze), so the limit is **$1$**.

---

## Part D — Conceptual and Proof

**D1.** $f(x)=x^3$. $f'(0)=0$ but $x=0$ is neither a local max nor min: for $x<0$, $f(x)<0=f(0)$; for $x>0$, $f(x)>0=f(0)$. The graph has a horizontal tangent at $(0,0)$ but keeps rising through it, so it is not an extremum. By definition, a local max requires $f(x)\leq f(0)$ for ALL $x$ near 0, but for $x>0$ we have $f(x)>f(0)$ — violating this.

**D2.** *Step 1 (non-decreasing).* For $x_1<x_2$, the MVT gives $f(x_2)-f(x_1)=f'(c)(x_2-x_1)\ge0$, so
$f(x_1)\le f(x_2)$.

*Step 2 (strict).* Suppose $f(x_1)=f(x_2)$ for some $x_1<x_2$. For any $x\in[x_1,x_2]$, Step 1 gives
$f(x_1)\le f(x)\le f(x_2)=f(x_1)$, so $f$ is constant on $[x_1,x_2]$ and $f'(x)=0$ at every point of
$(x_1,x_2)$ — infinitely many points, contradicting the hypothesis. Hence $f(x_1)<f(x_2)$. $\square$

*(The old key argued by "choosing a slightly different sub-interval", which is not a proof.)*

**D3.** Rolle's Theorem is a **special case** of the MVT (when $f(a)=f(b)$, the average rate of change is 0, so MVT gives $f'(c)=0$ — exactly Rolle's conclusion). However, in the standard development, Rolle's Theorem is proved FIRST (directly from the EVT and Fermat's Theorem), and then the MVT is proved USING Rolle's Theorem (via the auxiliary function $g(x)$ that subtracts the secant line). So logically: Rolle's Theorem is used as a tool to prove the more general MVT, even though MVT "contains" Rolle's Theorem as a special case.
