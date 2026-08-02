# MATH 141 · Week 4 Reference Sheet
## Differentiation Rules

---

## The Rules

| Rule | Statement |
|---|---|
| Constant | $\dfrac{d}{dx}c=0$ |
| Power | $\dfrac{d}{dx}x^n=nx^{n-1}$ — for **every** real $n$ |
| Constant multiple | $(cf)'=cf'$ |
| Sum | $(f\pm g)'=f'\pm g'$ |
| **Product** | $(fg)'=f'g+fg'$ |
| **Quotient** | $\left(\dfrac fg\right)'=\dfrac{f'g-fg'}{g^2}$ |
| **Chain** | $\big(f(g(x))\big)'=f'(g(x))\cdot g'(x)$ |

**$(fg)' \ne f'g'$.** Counterexample: $f=g=x$ at $x=3$ gives $(x^2)'=6$, but $f'g'=1$.

**The quotient rule's numerator order matters** — $f'g-fg'$, not $fg'-f'g$. Remember it as
"low d-high minus high d-low, over low squared".

---

## Standard Derivatives

| $f(x)$ | $f'(x)$ | | $f(x)$ | $f'(x)$ |
|---|---|---|---|---|
| $x^n$ | $nx^{n-1}$ | | $\sin x$ | $\cos x$ |
| $e^x$ | $e^x$ | | $\cos x$ | $-\sin x$ |
| $a^x$ | $a^x\ln a$ | | $\tan x$ | $\sec^2 x$ |
| $\ln x$ | $\dfrac1x$ | | $\sec x$ | $\sec x\tan x$ |
| $\log_a x$ | $\dfrac{1}{x\ln a}$ | | $\sqrt x$ | $\dfrac{1}{2\sqrt x}$ |

---

## The Chain Rule in Practice

**Decompose before differentiating.** For $\sqrt{1+\sin(x^2)}$:

| Layer | |
|---|---|
| Outer | $\sqrt{\ \cdot\ }$ |
| Middle | $1+\sin(\ \cdot\ )$ |
| Inner | $x^2$ |

$$\frac{d}{dx}=\underbrace{\frac{1}{2\sqrt{1+\sin(x^2)}}}_{\text{outer}'}\cdot\underbrace{\cos(x^2)}_{\text{middle}'}\cdot\underbrace{2x}_{\text{inner}'}$$

Verified at $x=1$: $0.3981570233$.

**Evaluate each factor at its own input.** $\frac{df}{du}$ is computed at $u=g(x)$, not at $x$. For
$(x^2+1)^5$ at $x=1$: $u=2$, $\frac{df}{du}=5u^4=80$, $\frac{du}{dx}=2$, product $=160$ ✓ — not $5\cdot2=10$.

---

## Higher Derivatives

$$f''=(f')',\qquad f^{(n)}=\big(f^{(n-1)}\big)'$$

Write $f^{(4)}$, not $f^4$.

| Function | Pattern |
|---|---|
| $x^k$ | $\dfrac{k!}{(k-n)!}x^{k-n}$ for $n\le k$; $\mathbf 0$ for $n>k$ |
| $e^x$ | $e^x$ for every $n$ |
| $\sin x$ | cycles with **period 4**: $\sin\to\cos\to-\sin\to-\cos$ |
| $\ln x$ | $(-1)^{n-1}(n-1)!\,x^{-n}$ |

So $\frac{d^{50}}{dx^{50}}\cos x=-\cos x$ ($50\equiv2 \bmod 4$), and $\frac{d^9}{dx^9}x^6=0$.

---

## Motion

| | |
|---|---|
| $s(t)$ | position |
| $v(t)=s'(t)$ | velocity — **signed** |
| $a(t)=s''(t)$ | acceleration |
| $\lvert v(t)\rvert$ | speed |

**Speeding up** ⟺ $v$ and $a$ have the **same sign**. Not "$a>0$".

**Displacement** $=s(b)-s(a)$. **Distance** requires splitting at every $t$ where $v$ **changes
sign** — and a *double* root of $v$ is a touch, not a crossing, so it needs no split.

Worked: $v=3(t-1)(t-3)$ on $[0,4]$ — simple roots, sign changes, displacement $4$ m but distance
$12$ m. Versus $v=4t(t-3)^2$ — double root, no sign change, both equal $32$ m.

---

## Rates of Change

$\dfrac{dy}{dx}$ has units of $y$ per unit of $x$.

**Marginal cost** $C'(q) \approx C(q+1)-C(q)$, with error $\approx\tfrac12C''(q)$. Verified for
$C=0.01q^3-0.6q^2+13q+100$: errors $-0.290, +0.010, +0.310, +0.610$ at $q=10,20,30,40$, against
$\tfrac12C''$ of $-0.300, 0, +0.300, +0.600$.

---

## Numerical Check

$$f'(a)\approx\frac{f(a+h)-f(a-h)}{2h}$$

Second order: error $\sim h^2$. But **do not take $h$ too small** — subtractive cancellation makes
the error grow again below $h\approx\varepsilon^{1/3}\approx6\times10^{-6}$. Verified optimum at
$h=10^{-6}$ (error $1.24\times10^{-8}$); at $h=10^{-16}$ the result is exactly $0$.

---

*MATH 141 · Week 4 · Reference · © CSE Department*
