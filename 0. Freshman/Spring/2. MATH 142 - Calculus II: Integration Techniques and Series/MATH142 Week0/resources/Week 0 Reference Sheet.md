# MATH 142 · Calculus II
## Week 0 · Reference Sheet
### Review of Integration; Applications

---

## The Definition

$$\int_a^b f(x)\,dx = \lim_{n\to\infty}\sum_{i=1}^n f(x_i^*)\,\Delta x, \qquad \Delta x = \frac{b-a}{n},\quad x_i^*\in[x_{i-1},x_i]$$

Every continuous function on a closed bounded interval is integrable.

---

## The Fundamental Theorem

**Part 1** — if $f$ is continuous and $F(x)=\displaystyle\int_a^x f(t)\,dt$, then $F'(x)=f(x)$.

**Part 2** — if $F$ is any antiderivative of a continuous $f$, then $\displaystyle\int_a^b f = F(b)-F(a)$.

**General form with variable limits:**

$$\frac{d}{dx}\int_{g(x)}^{h(x)} f(t)\,dt = f(h(x))\,h'(x) - f(g(x))\,g'(x)$$

---

## Properties

| | |
|---|---|
| Linearity | $\displaystyle\int_a^b(\alpha f+\beta g) = \alpha\int_a^b f + \beta\int_a^b g$ |
| Additivity | $\displaystyle\int_a^c f = \int_a^b f + \int_b^c f$ |
| Reversal | $\displaystyle\int_b^a f = -\int_a^b f$ |
| Comparison | $f\le g \implies \displaystyle\int_a^b f \le \int_a^b g$ |
| Bounds | $m\le f\le M \implies m(b-a)\le\displaystyle\int_a^b f\le M(b-a)$ |

---

## Substitution

$$\int f(g(x))\,g'(x)\,dx = \int f(u)\,du \qquad\qquad \int_a^b f(g(x))g'(x)\,dx = \int_{g(a)}^{g(b)} f(u)\,du$$

**Change the limits, or convert back to $x$ — never mix.**

The shape to look for: $\displaystyle\int\frac{g'(x)}{g(x)}\,dx = \ln|g(x)| + C$

---

## Symmetry

$f$ odd $\implies \displaystyle\int_{-a}^{a} f = 0$    $\qquad$    $f$ even $\implies \displaystyle\int_{-a}^{a} f = 2\int_0^a f$

**Both require the interval to be symmetric about $0$.** Check symmetry before integrating anything.

---

## Antiderivative Catalogue

*(every entry omits $+C$; all 19 verified by differentiation)*

| $f$ | $\int f$ | $f$ | $\int f$ |
|---|---|---|---|
| $x^n,\ n\neq-1$ | $\dfrac{x^{n+1}}{n+1}$ | $\sec^2 x$ | $\tan x$ |
| $\dfrac1x$ | $\ln\lvert x\rvert$ | $\csc^2 x$ | $-\cot x$ |
| $e^x$ | $e^x$ | $\sec x\tan x$ | $\sec x$ |
| $a^x$ | $\dfrac{a^x}{\ln a}$ | $\csc x\cot x$ | $-\csc x$ |
| $\sin x$ | $-\cos x$ | $\dfrac{1}{\sqrt{1-x^2}}$ | $\arcsin x$ |
| $\cos x$ | $\sin x$ | $\dfrac{1}{1+x^2}$ | $\arctan x$ |
| $\tan x$ | $-\ln\lvert\cos x\rvert$ | $\dfrac{1}{\lvert x\rvert\sqrt{x^2-1}}$ | $\operatorname{arcsec} x$ |
| $\cot x$ | $\ln\lvert\sin x\rvert$ | $\sinh x$ | $\cosh x$ |
| $\sec x$ | $\ln\lvert\sec x+\tan x\rvert$ | $\cosh x$ | $\sinh x$ |
| $\csc x$ | $-\ln\lvert\csc x+\cot x\rvert$ | | |

---

## Applications

**Area between curves** — $f$ above $g$ on $[a,b]$:

$$A = \int_a^b\big[f(x)-g(x)\big]\,dx$$

If they cross, split at the crossings. **Area is never negative.**

Horizontal slices: $A = \displaystyle\int_c^d\big[p(y)-q(y)\big]dy$, $p$ right of $q$.

**Average value:**

$$f_{\text{avg}} = \frac{1}{b-a}\int_a^b f(x)\,dx$$

**MVT for Integrals:** if $f$ is continuous, some $c\in[a,b]$ has $f(c)=f_{\text{avg}}$.

**Net change:** $\displaystyle\int_a^b F'(x)\,dx = F(b)-F(a)$

| | |
|---|---|
| Displacement | $\displaystyle\int_{t_1}^{t_2} v(t)\,dt$ |
| Distance | $\displaystyle\int_{t_1}^{t_2} \lvert v(t)\rvert\,dt$ — **split at sign changes** |

---

## Numerical Rules (Lab 0)

With $h=\dfrac{b-a}{n}$:

| Rule | Formula | Order |
|---|---|---|
| Trapezoid | $h\left[\tfrac{f_0}{2}+f_1+\cdots+f_{n-1}+\tfrac{f_n}{2}\right]$ | $O(h^2)$ |
| Midpoint | $h\sum f\big(a+(i+\tfrac12)h\big)$ | $O(h^2)$ |
| Simpson ($n$ even) | $\tfrac{h}{3}\big[f_0+4f_1+2f_2+\cdots+4f_{n-1}+f_n\big]$ | $O(h^4)$ |

**Error ratio on doubling $n$:** $2^p$ — so $4$ for trapezoid and midpoint, $16$ for Simpson. *(Measured in Lab 0.)*

Simpson is **exact for polynomials of degree $\le 3$**.

---

## The Course's Premise

These functions are continuous, so by FTC Part 1 each has an antiderivative — but **none is elementary** (Liouville, 1835):

$$e^{-x^2} \qquad \frac{\sin x}{x} \qquad \sqrt{1+x^3}$$

**Existence and expressibility are different questions.** Weeks 1–5 extend what can be expressed; Weeks 6–12 replace expression with approximation.

---

## Two Habits

1. **Check every antiderivative by differentiating it.** Thirty seconds, catches nearly everything.
2. **The CAS is a check, not an oracle.** In this week alone it returned an unsimplifiable hypergeometric form for a one-line FTC problem, refused to evaluate $\int_0^3|t^2-4|\,dt$, and gave $\int\sec x\,dx$ in a form unrecognisably different from the textbook's. All three were resolved by hand in a line.

---

*MATH 142 · Week 0 · Reference Sheet*
