# MATH 141 — Week 9 Reference Sheet
## The Fundamental Theorem of Calculus

---

## FTC Part 1 — Differentiating an Integral

> $f$ **continuous** on $[a,b]$, $\displaystyle A(x)=\int_a^x f(t)\,dt$ ⟹ $A'(x)=f(x)$.

Every continuous function **has** an antiderivative — FTC 1 constructs it. Whether that
antiderivative can be written with elementary symbols is a separate, much narrower question.

### With variable limits

$$\frac{d}{dx}\int_{u(x)}^{v(x)}f(t)\,dt = f\big(v(x)\big)v'(x) - f\big(u(x)\big)u'(x)$$

| Form | Derivative |
|---|---|
| $\int_a^x f$ | $f(x)$ |
| $\int_a^{u(x)} f$ | $f(u)\,u'$ |
| $\int_{u(x)}^{b} f$ | $-f(u)\,u'$ |
| $\int_{u(x)}^{v(x)} f$ | $f(v)v' - f(u)u'$ |

Verified: for $G(x)=\int_{x^2}^{x^3}\sin t\,dt$, the formula and a numerical derivative agree at
$x=1.3$ to seven decimals ($1.5264599$).

---

## FTC Part 2 — Evaluating an Integral

> $F'=f$ on $[a,b]$, $f$ continuous ⟹ $\displaystyle\int_a^b f(x)\,dx = F(b)-F(a)$.

$$\int_a^b F'(x)\,dx = F(b)-F(a) \qquad \textbf{the integral of a rate is the net change}$$

**The hypothesis is not decoration.** $\int_{-1}^{1}x^{-2}dx$ "evaluates" to $-2$ if you ignore the
discontinuity at $0$ — a negative number for a positive integrand. The integral in fact diverges.

**Antiderivatives to know cold:**

| $f$ | $F$ | | $f$ | $F$ |
|---|---|---|---|---|
| $x^n\ (n\ne-1)$ | $\dfrac{x^{n+1}}{n+1}$ | | $\sin x$ | $-\cos x$ |
| $\dfrac1x$ | $\ln\lvert x\rvert$ | | $\cos x$ | $\sin x$ |
| $e^x$ | $e^x$ | | $\sec^2x$ | $\tan x$ |

---

## Motion

| Quantity | Formula |
|---|---|
| Displacement | $\displaystyle\int_a^b v\,dt$ |
| **Total distance** | $\displaystyle\int_a^b \lvert v\rvert\,dt$ |
| Position | $\displaystyle s(t)=s(a)+\int_a^t v$ |

To get distance: **find where $v=0$, split there, integrate each piece, add the absolute values.**

Worked and verified, $v=t^2-4$ on $[0,4]$:

$$\text{displacement}=\tfrac{16}{3}\approx5.333 \qquad \text{distance}=\tfrac{16}{3}+\tfrac{32}{3}=\mathbf{16}$$

---

## Average Value and the MVT for Integrals

$$f_{\text{avg}}=\frac{1}{b-a}\int_a^b f(x)\,dx$$

> **MVT for integrals.** $f$ continuous on $[a,b]$ ⟹ some $c\in[a,b]$ with $f(c)=f_{\text{avg}}$.

A continuous function attains its own average. This is the engine of FTC 1's proof.

Example: $f=x^2$ on $[0,3]$ has average $3$, attained at $c=\sqrt3\approx1.7321$.

---

## Functions Defined by Integrals

$$F(x)=\int_0^x e^{-t^2}\,dt$$

has **no elementary antiderivative** — and is completely understood anyway:

| | |
|---|---|
| $F(0)=0$, $F$ odd | integrand even |
| $F'=e^{-x^2}>0$ | strictly increasing everywhere |
| $F''=-2xe^{-x^2}$ | concave up on $x<0$, down on $x>0$, inflection at $0$ |
| $F\to\dfrac{\sqrt\pi}{2}\approx0.8862$ | increasing and bounded |

Verified: $F(1)=0.7468241328$, $F(2)=0.8820813908$, $F(3)=0.8862073483$.

**"No formula" ≠ "no function."** Notation is a human convenience; $F$ existed before it had a name.

---

## Error Checklist

| Symptom | Cause |
|---|---|
| Chain factor missing | $\frac{d}{dx}\int_a^{x^2}f$ needs $\cdot\,2x$ |
| Sign wrong | The variable was the **lower** limit |
| Negative answer, positive integrand | FTC 2 applied across a discontinuity |
| Distance $=$ displacement | Forgot to split at $v=0$ |

---

*MATH 141 · Week 9 · Reference · © CSE Department*
