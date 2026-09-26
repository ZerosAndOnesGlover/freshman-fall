# MATH 141 · Problem Set 6 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Revised 2026-09-26 to match the 8-problem, 12-part set; items are numbered as in the new set.*

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
## Problem 1 — Critical Numbers (12)

**(a)** $g'(x)=\dfrac{1\cdot(x^2+3)-(x-1)(2x)}{(x^2+3)^2}=\dfrac{x^2+3-2x^2+2x}{(x^2+3)^2}=\dfrac{-x^2+2x+3}{(x^2+3)^2}=\dfrac{-(x-3)(x+1)}{(x^2+3)^2}$

Critical numbers: $x=3,-1$.

**(b)** $h(x)=x^{1/3}(x+4)=x^{4/3}+4x^{1/3}$

$h'(x)=\dfrac43x^{1/3}+\dfrac43x^{-2/3}=\dfrac43x^{-2/3}(x+1)$

Critical numbers: $x=-1$ (where $h'=0$) and $x=0$ (where $h'$ undefined).

---

## Problem 2 — The Closed Interval Method (16)

**(a)** $f(x)=x^3-3x+1$ on $[-2,3]$.

$f'(x)=3x^2-3=0 \implies x=\pm1$.

$f(-2)=-8+6+1=-1$; $f(-1)=-1+3+1=3$; $f(1)=1-3+1=-1$; $f(3)=27-9+1=19$.

**Max: 19 at $x=3$. Min: $-1$ at $x=-2$ and $x=1$.**

**(b)** $f(x)=x-2\sin x$ on $[0,2\pi]$.

$f'(x)=1-2\cos x=0\implies\cos x=1/2\implies x=\pi/3,5\pi/3$.

$f(0)=0$; $f(\pi/3)=\pi/3-2(\sqrt3/2)=\pi/3-\sqrt3\approx-0.685$; $f(5\pi/3)=5\pi/3-2(-\sqrt3/2)=5\pi/3+\sqrt3\approx6.964$; $f(2\pi)=2\pi\approx6.283$.

**Max: $5\pi/3+\sqrt3\approx6.964$ at $x=5\pi/3$. Min: $\pi/3-\sqrt3\approx-0.685$ at $x=\pi/3$.**

---

## Problem 3 — Exactly One Root (8)

$f(x)=x^5+2x-3$ is a polynomial (continuous, differentiable everywhere).

Existence: $f(0)=-3<0$, $f(1)=1+2-3=0$. Actually $f(1)=0$ exactly — so $x=1$ IS a root.

Let's verify uniqueness: $f'(x)=5x^4+2>0$ always (since $5x^4\geq0$ and $+2$). So $f'$ never zero.

If there were two roots $a<b$, Rolle's Theorem would guarantee $f'(c)=0$ for some $c\in(a,b)$ — contradiction. So **at most one root**. Combined with $f(1)=0$: **exactly one real root, at $x=1$.**

---

## Problem 4 — The MVT (10)

$f(x)=\sqrt{x+1}$; continuous on $[0,3]$, differentiable on $(0,3)$ (note: even at $x=-1$ boundary isn't in our interval, so fine). Applies.

$\dfrac{f(3)-f(0)}{3}=\dfrac{2-1}{3}=\dfrac13$

$f'(x)=\dfrac{1}{2\sqrt{x+1}}=\dfrac13\implies\sqrt{x+1}=1.5\implies x+1=2.25\implies x=1.25\in(0,3)$. $c=1.25$.

---

## Problem 5 — The Cyclist (10)

Let $s(t)$ = position along the road, $t\in[0,1.5]$ hours, with $s(0)=0$, $s(1.5)=45$ km.

Assuming the cyclist's position is continuous (physical motion) and differentiable (velocity well-defined, no instantaneous jumps) — reasonable physical assumptions — the MVT applies:

$$\exists\,c\in(0,1.5): s'(c)=\frac{45-0}{1.5-0}=30\text{ km/h}$$

So at some instant, the cyclist's instantaneous speed was exactly 30 km/h. $\square$

---

## Problem 6 — An Inequality from the MVT (10)

Fix $x<y$. Apply MVT to $f(t)=\sin t$ on $[x,y]$: $f$ is continuous and differentiable everywhere.

$$\exists\,c\in(x,y): \frac{\sin y-\sin x}{y-x}=\cos c$$

Since $|\cos c|\leq1$:

$$\left|\frac{\sin y-\sin x}{y-x}\right|\leq1 \implies |\sin y-\sin x|\leq|y-x| \quad\square$$

*(This is a Lipschitz continuity result — $\sin$ is 1-Lipschitz.)*

---

## Problem 7 — L'Hôpital's Rule (24)

**(a)** Form $0/0$. $\dfrac{e^x-1}{2x}$ is still $0/0$; again: $\dfrac{e^x}{2}\to\dfrac12$. **Answer $\tfrac12$.**

**(b)** Form $0\cdot(-\infty)$. Write $\dfrac{\ln x}{1/x}$ ($-\infty/\infty$): $\dfrac{1/x}{-1/x^2}=-x\to0$. **Answer $0$.**

**(c)** Form $1^\infty$. $\ln y=x\ln(1+3/x)=\dfrac{\ln(1+3/x)}{1/x}$ ($0/0$). Differentiating:
$\dfrac{\frac{-3/x^2}{1+3/x}}{-1/x^2}=\dfrac{3}{1+3/x}\to3$. So $y\to e^3$. **Answer $e^3$.**
Common error: stopping at $\ln y\to3$.

---

## Problem 8 — A Zero Derivative (10)

$f(x)=x^3$. $f'(0)=0$ but $x=0$ is neither a local max nor min: for $x<0$, $f(x)<0=f(0)$; for $x>0$, $f(x)>0=f(0)$. The graph has a horizontal tangent at $(0,0)$ but keeps rising through it, so it is not an extremum. By definition, a local max requires $f(x)\leq f(0)$ for ALL $x$ near 0, but for $x>0$ we have $f(x)>f(0)$ — violating this.

---

*MATH 141 · Week 6 · Problem Set 6 Solutions · © CSE Department*
