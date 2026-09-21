# MATH 141 · Problem Set 2 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-21 out of the student handout, where it had been printed below the questions.*

---

### Part A

**A1.** (i) $f(a)$ is defined; (ii) $\lim_{x\to a}f(x)$ exists; (iii) they are equal.

Failures: (i) $\frac1x$ at $0$; (ii) $\frac{\lvert x\rvert}{x}$ at $0$; (iii) $f(x)=x$ for $x\ne0$
with $f(0)=5$.

**A2.** (a) All $x\ne\pm2$. (b) $[3,\infty)$ — right-continuous at $3$. (c) All $x\ne0$; the
discontinuity at $0$ is **removable**, with limit $1$.

**A3.** $\dfrac{(x-3)(x+3)}{x-3}=x+3\to6$, so $k=\mathbf 6$.

**A4.** Given $\varepsilon>0$, take $\delta=\varepsilon$. Then $\lvert x-0\rvert<\delta$ implies
$\big\lvert\,\lvert x\rvert-0\,\big\rvert=\lvert x\rvert<\varepsilon$. ∎

*The point is that $\lvert x\rvert$ is continuous everywhere despite not being differentiable at $0$
— which Week 3 will use.*

### Part B

**B1.** *(3 each)*

| | Type | Reason |
|---|---|---|
| (a) | **Removable** | Cancels to $x+2\to4$ |
| (b) | **Infinite** | Numerator $\to4\ne0$ |
| (c) | **Jump** | One-sided limits $-1$ and $+1$ |
| (d) | **Essential** | Oscillates between $\pm1$ |

*(a) and (b) are the discriminating pair — both have a vanishing denominator.*

**B2.** $\dfrac{(x-3)(x+3)}{x(x-3)}$. **At $3$: removable** (limit $2$). **At $0$: infinite**.

*Verified: $f\to2$ from both sides at $3$; $f\to\mp\infty$ at $0$.*

**B3.** $f(x)=\frac1x$ — **not defined at $0$**, so the first condition fails, and no value at $0$
would help since the limit is $+\infty$.

*Reject $f(x)=x$ restricted to $(0,1)$ — it extends continuously, so the failure is an artefact of
the domain.*

### Part C

**C1.** $f(1)=-2<0<4=f(2)$; $f$ is a polynomial, hence continuous. By the IVT a root exists in
$(1,2)$.

**Does tell you:** at least one root exists.
**Does not:** where it is, how many there are, or how to find one.

*(The actual root is $1.521379706805$; uniqueness needs $f'>0$, which is Week 6.)*

**C2.** $g(x)=\cos x-x$ is continuous; $g(0)=1>0$ and $g(1)=\cos 1-1\approx-0.4597<0$. IVT gives a
solution in $(0,1)$.

*(Verified: $c\approx0.739085133$.)*

**C3.** Verified trace:

| Step | Bracket | Midpoint | $f(\text{mid})$ |
|---|---|---|---|
| 1 | $[1.000000,2.000000]$ | $1.500000$ | $-0.125000$ |
| 2 | $[1.500000,2.000000]$ | $1.750000$ | $+1.609375$ |
| 3 | $[1.500000,1.750000]$ | $1.625000$ | $+0.666016$ |
| 4 | $[1.500000,1.625000]$ | $1.562500$ | $+0.252197$ |

**C4.** Width $1$; need $2^{-n}\le10^{-4}$, so $n\ge\log_2(10^4)=13.29$ → **14 steps**.

*13 leaves the bracket at $1.221\times10^{-4}$ — verified too wide. **Round up.***

**C5.** Any jump function straddling zero, e.g. $-1$ for $x<\tfrac12$ and $+1$ for $x\ge\tfrac12$.
**Continuity fails.**

### Part D

**D1.** Take $f(x)=x^2-2$ on $[1,2]$ over $\mathbb{Q}$ only. $f$ is continuous, $f(1)=-1<0<2=f(2)$,
yet no **rational** $c$ has $c^2=2$ — $\sqrt2$ is irrational.

So the conclusion fails while every hypothesis holds. What rescues it over $\mathbb{R}$ is
**completeness** — the reals have no gaps, formalised by the least-upper-bound axiom.

*This is why the IVT needs a proof rather than a picture: the picture is equally convincing over
$\mathbb{Q}$, where the theorem is false. Full marks require naming completeness.*

**D2.** $f(x)=\sin(1/x)$ for $x\ne0$ with $f(0)=0$, on $[-1,1]$.

On **any** interval containing $0$, $f$ takes every value in $[-1,1]$ — infinitely often, since
$1/x$ runs through unboundedly many periods. So the intermediate-value *property* holds.

But $f$ is **discontinuous at $0$**: no one-sided limit exists, because the oscillation never
settles. Verified: at $x=1/(k\pi/2)$ for $k=1,3,5,\dots$ the values alternate exactly $+1,-1,+1,\dots$

**Therefore "takes all intermediate values" does not imply continuity.** The implication runs one way
only.

*(Functions with the intermediate-value property are called **Darboux functions**; every derivative
is one, even when discontinuous — which connects to Week 3's $x^2\sin(1/x)$.)*

---

*MATH 141 · Week 2 · Problem Set 2 · © CSE Department*
