# MATH 141 — Problem Set 12
## Comprehensive Revision (Optional, Ungraded)

**Released:** Week 12 · **Not submitted** — full solutions below
**Suggested time:** 3 hours, under exam conditions

> **Work this cold, timed, before reading the solutions.** Its value is entirely diagnostic: it tells
> you which topics you can do under pressure and which you only recognise. Reading the solutions
> first destroys that information.

---

## Part A — Limits and Continuity (20 pts)

**A1.** *(4)* Evaluate $\displaystyle\lim_{x\to\infty}\frac{3x^2-x}{2x^2+5}$ and
$\displaystyle\lim_{x\to\infty}\big(\sqrt{x^2+6x}-x\big)$.

**A2.** *(4)* Classify the discontinuity of $\dfrac{x^2-9}{x^2-3x}$ at $x=0$ and at $x=3$.

**A3.** *(6)* Show $x^3-x-2$ has a root in $[1,2]$. How many bisection steps to locate it within
$10^{-4}$?

**A4.** *(6)* Find $a,b$ making $f(x)=\begin{cases}x^2,&x\le1\\ax+b,&x>1\end{cases}$ differentiable
at $1$. State both conditions.

---

## Part B — Derivatives (25 pts)

**B1.** *(8)* Differentiate: (a) $(x^2+1)^5$ (b) $\dfrac{x}{\sqrt{x^2+1}}$ (c) $\ln(x^2+1)$
(d) $x^2\sin x$

**B2.** *(6)* For $s(t)=t^3-6t^2+9t$ on $[0,4]$: when is the particle at rest, and is it speeding up
or slowing down at $t=2$?

**B3.** *(5)* Find $\dfrac{d^{50}}{dx^{50}}\cos x$ and $\dfrac{d^{9}}{dx^{9}}x^6$.

**B4.** *(6)* Find the absolute extrema of $f(x)=x^3-3x$ on $[-2,2]$.

---

## Part C — Integrals (30 pts)

**C1.** *(8)* Evaluate: (a) $\int_1^4\sqrt x\,dx$ (b) $\int_0^{\pi/2}\cos x\,dx$
(c) $\int_0^1 2xe^{x^2}dx$ (d) $\int x\cos x\,dx$

**C2.** *(6)* Explain the error in $\int_{-2}^{2}x^{-2}dx=\left[-x^{-1}\right]_{-2}^{2}=-1$.

**C3.** *(8)* For $v(t)=t^2-4$ on $[0,4]$, find the displacement and the total distance.

**C4.** *(8)* Find $G'(x)$ for (a) $G=\int_0^{x^3}\cos t\,dt$ (b) $G=\int_x^{x^2}\ln t\,dt$.

---

## Part D — Applications (25 pts)

**D1.** *(8)* Area between $y=\sin x$ and $y=\cos x$ on $[0,\pi/2]$.

**D2.** *(9)* Volume from revolving the region between $y=\sqrt x$ and $y=x$ on $[0,1]$ about the
$x$-axis.

**D3.** *(8)* Volume from revolving $y=x^2$ on $[0,2]$ about the $y$-axis — **twice**, by shells and
by washers.

---

## Solutions

*Every numerical value verified.*

### Part A

**A1.** $\dfrac{3x^2-x}{2x^2+5}\to\mathbf{\tfrac32}$ (equal degrees, ratio of leading coefficients).

$\sqrt{x^2+6x}-x$: rationalise to $\dfrac{6x}{\sqrt{x^2+6x}+x}=\dfrac{6}{\sqrt{1+6/x}+1}\to\mathbf 3$.
*(Verified: $2.99999550$ at $x=10^6$.)*

**A2.** Factor: $\dfrac{(x-3)(x+3)}{x(x-3)}$.

**At $x=3$: removable** — cancels to $\tfrac{x+3}{x}\to 2$, a hole at $(3,2)$.
**At $x=0$: infinite** — numerator $\to3\ne0$, vertical asymptote.

*Both came from the same denominator and classify differently. Factor first.*

**A3.** $f(1)=-2<0<4=f(2)$ and $f$ is continuous (polynomial), so by the **IVT** a root exists in
$(1,2)$.

Bisection: width $1$, need $2^{-n}\le10^{-4}$, so $n\ge\log_2(10^4)=13.29$ → **14 iterations**.
*(13 leaves the bracket at $1.22\times10^{-4}$ — too wide.)*

*Verified root: $1.521379706805$.*

**A4.** **Continuity:** $1=a+b$. **Slopes:** $2=a$. So $\mathbf{a=2,\ b=-1}$.

*Matching only slopes leaves $b$ free and produces a jump — not even continuous.*

### Part B

**B1.** (a) $10x(x^2+1)^4$ (b) $\dfrac{1}{(x^2+1)^{3/2}}$ (c) $\dfrac{2x}{x^2+1}$
(d) $2x\sin x+x^2\cos x$

*All verified numerically to 8 decimal places.*

**B2.** $v(t)=3(t-1)(t-3)$, so **at rest at $t=1$ and $t=3$**.

At $t=2$: $v=-3$, $a=6(2)-12=0$ turning positive. Signs differ ⟹ **slowing down**.

**B3.** $\dfrac{d^{50}}{dx^{50}}\cos x=\mathbf{-\cos x}$ ($50\equiv2\bmod4$).
$\dfrac{d^{9}}{dx^{9}}x^6=\mathbf 0$ (since $9>6$).

**B4.** $f'=3x^2-3=0$ at $x=\pm1$. Evaluate at critical points **and endpoints**:

| $x$ | $-2$ | $-1$ | $1$ | $2$ |
|---|---|---|---|---|
| $f$ | $-2$ | $2$ | $-2$ | $2$ |

**Absolute max $2$** (at $x=-1$ and $x=2$); **absolute min $-2$** (at $x=-2$ and $x=1$).

*Forgetting the endpoints is the classic error.*

### Part C

**C1.** (a) $\left[\tfrac23x^{3/2}\right]_1^4=\mathbf{\tfrac{14}{3}}$ (b) $\mathbf 1$
(c) $u=x^2$: $\big[e^u\big]_0^1=\mathbf{e-1}$ (d) parts with $u=x$: $\mathbf{x\sin x+\cos x+C}$

*All verified.*

**C2.** The FTC requires $f$ **continuous on the whole interval**. $x^{-2}$ has an infinite
discontinuity at $x=0\in[-2,2]$, so the hypothesis fails.

**The tell:** $x^{-2}>0$ everywhere it is defined, so a negative answer is impossible. The integral
actually **diverges**.

**C3.** $v=(t-2)(t+2)$, negative on $[0,2)$, positive on $(2,4]$.

**Displacement** $=\int_0^4(t^2-4)dt=\tfrac{64}{3}-16=\mathbf{\tfrac{16}{3}}\approx5.333$.

**Distance:** split at $t=2$. First piece $\tfrac{16}{3}$, second piece $\tfrac{32}{3}$, total
$\mathbf{16}$. *(Verified $\int_0^4\lvert v\rvert dt=16.00000000$.)*

*Note the pieces are unequal — adding them, not mistaking one for the total, is where this is lost.*

**C4.** (a) $\cos(x^3)\cdot3x^2$ (b) $\ln(x^2)\cdot2x-\ln x=\mathbf{4x\ln x-\ln x}$

*(b) verified numerically at $x=1.5$ and $x=2$.*

### Part D

**D1.** Cross at $\pi/4$. $A=\mathbf{2(\sqrt2-1)}\approx0.8284$ *(verified)*.

Without the split the answer is **0** — verified — because the regions cancel.

**D2.** $\sqrt x$ is outer: $V=\pi\int_0^1(x-x^2)dx=\mathbf{\tfrac{\pi}{6}}\approx0.524$ *(verified)*.

*$\pi\int(\sqrt x-x)^2dx$ gives $\pi/30$ — wrong by a factor of 5.*

**D3.** **Shells:** $2\pi\int_0^2x^3dx=\mathbf{8\pi}$.
**Washers in $y$:** $\pi\int_0^4(4-y)dy=\mathbf{8\pi}$.

Both verified as $25.13274123$.

---

## Self-Diagnosis

| If you struggled with | Revise |
|---|---|
| A1, A2 | Weeks 1–2 |
| A3 | Week 2, Lecture 3 |
| A4, B1 | Weeks 3–4 |
| B2, B4 | Weeks 4, 6–7 |
| C1, C4 | Weeks 9–10 |
| C2 | Week 9, Lecture 2 — the continuity hypothesis |
| C3, D1 | The signed-vs-absolute thread |
| D2, D3 | Week 11 |

---

*MATH 141 · Week 12 · Problem Set 12 · © CSE Department*
