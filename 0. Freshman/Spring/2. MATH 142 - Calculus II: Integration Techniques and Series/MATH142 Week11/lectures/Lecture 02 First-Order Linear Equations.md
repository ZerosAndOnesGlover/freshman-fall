# MATH 142 · Calculus II
## Week 11 · Lecture 2 (Tuesday)
### First-Order Linear Equations

---

**Reading:** Stewart §9.5 | Apostol Ch. 8 §8.5–8.6

---

## 1. The Standard Form

$$\boxed{\frac{dy}{dx}+P(x)\,y = Q(x)}$$

**"Linear" means $y$ and $y'$ appear only to the first power**, with no products of them and no $y^2$, $\sin y$, $e^y$, etc.

**These are usually *not* separable**, so Monday's method fails. $y'+y=x$ cannot be rearranged into $g(x)h(y)$.

> **Get the equation into standard form first**, with the coefficient of $y'$ equal to 1. For
> $xy'+y=x^2$, divide by $x$ to get $y'+\frac1xy = x$, so $P(x)=\frac1x$. **Reading $P$ off the
> undivided equation is the most common error in this material.**

---

## 2. The Idea: Force a Product Rule

**Look at the left side and wish it were a derivative.** It nearly is — the product rule gives

$$(\mu y)' = \mu y'+\mu' y$$

**Compare with what we have**, after multiplying the equation by an as-yet-unknown $\mu(x)$:

$$\mu y'+\mu P y = \mu Q$$

**These match exactly if $\mu' = \mu P$** — and that is a separable equation for $\mu$!

$$\frac{d\mu}{\mu} = P\,dx \implies \ln\mu = \int P\,dx \implies \boxed{\mu(x) = e^{\int P(x)\,dx}}$$

**$\mu$ is the integrating factor.** With it, the equation becomes

$$(\mu y)' = \mu Q \implies \mu y = \int\mu Q\,dx \implies \boxed{y = \frac{1}{\mu}\int \mu\,Q\,dx}$$

> **The whole method is: choose the multiplier that makes the left side an exact product rule.**
> Memorising $\mu=e^{\int P}$ without this derivation makes every unusual case impossible — and the
> derivation is three lines. **Derive it each time until it is automatic.**

**No constant of integration is needed in $\int P\,dx$** — a different constant multiplies $\mu$ by a constant, which cancels in $\frac1\mu\int\mu Q$.

---

## 3. Worked Examples

### Example 1

$$y'+y = x$$

$P=1$, so $\mu = e^{\int1\,dx}=e^x$. Multiplying:

$$e^xy'+e^xy = xe^x \implies (e^xy)' = xe^x$$

Integrating the right side **by parts** (Week 1): $\int xe^xdx = (x-1)e^x+C$. So

$$e^xy = (x-1)e^x+C \implies \boxed{y = x-1+Ce^{-x}}$$

*(Verified — the CAS returns $C_1e^{-x}+x-1$.)*

**Check:** $y' = 1-Ce^{-x}$, and $y'+y = 1-Ce^{-x}+x-1+Ce^{-x} = x$ ✓

### Example 2

$$y'+2y = e^x$$

$\mu=e^{2x}$; $(e^{2x}y)' = e^{3x}$; integrating, $e^{2x}y = \frac{e^{3x}}{3}+C$:

$$\boxed{y = \frac{e^x}{3}+Ce^{-2x}}$$

*(Verified.)*

### Example 3 — standard form first

$$xy'+y = x^2$$

**Divide by $x$:** $y'+\frac1xy = x$, so $P=\frac1x$ and

$$\mu = e^{\int dx/x} = e^{\ln x} = x$$

**But notice the original equation was already $(xy)' = x^2$** — the left side was an exact product rule from the start. Either way:

$$xy = \frac{x^3}{3}+C \implies \boxed{y = \frac{x^2}{3}+\frac Cx}$$

*(Verified.)*

> **Always glance at the left side before computing $\mu$.** Sometimes it is already a derivative,
> and the work is done.

### Example 4 — a negative $P$

$$y'-\frac2xy = x^2$$

$P=-\frac2x$, so $\int P = -2\ln x$ and $\mu = e^{-2\ln x} = x^{-2}$:

$$\left(\frac{y}{x^2}\right)' = 1 \implies \frac{y}{x^2} = x+C \implies \boxed{y = x^3+Cx^2}$$

*(Verified.)*

**Note $e^{-2\ln x} = x^{-2}$, not $-2x$.** Simplifying $e^{\int P}$ with logarithm laws is where marks are lost.

---

## 4. Two Standard Models

### Mixing problems

A tank holds $V$ litres of brine. Solution of concentration $c_{\text{in}}$ enters at rate $r$, and the well-stirred mixture leaves at the same rate. With $y(t)$ the amount of salt:

$$\frac{dy}{dt} = \underbrace{rc_{\text{in}}}_{\text{rate in}} - \underbrace{r\frac{y}{V}}_{\text{rate out}} \implies y'+\frac rVy = rc_{\text{in}}$$

**A first-order linear equation**, with $\mu = e^{rt/V}$. The solution approaches the equilibrium $Vc_{\text{in}}$ exponentially.

> **The structure "rate in minus rate out" produces a linear equation almost every time**, which is
> why this method matters so much in applications.

### RL circuits

Kirchhoff's voltage law for a resistor and inductor in series:

$$L\frac{dI}{dt}+RI = V(t) \implies I'+\frac RLI = \frac VL$$

**Same equation, different letters.** With constant $V$, $\mu=e^{Rt/L}$ and the current approaches $\frac VR$ with time constant $\frac LR$.

**Newton's law of cooling** is separable *and* linear:

$$\frac{dT}{dt} = -k(T-T_s) \implies T = T_s+Ce^{-kt}$$

*(Verified.)* **Every object approaches ambient temperature exponentially**, and $\frac1k$ is the time constant.

---

## 5. Which Method?

| Equation looks like | Method |
|---|---|
| $\frac{dy}{dx}=f(x)$ | integrate directly |
| $\frac{dy}{dx}=g(x)h(y)$ | **separable** |
| $y'+P(x)y=Q(x)$ | **linear**, integrating factor |
| both | either — use the easier |
| **neither** | numerical (Lecture 3, Lab 11) |

**Some equations are both.** $y'=ky$ is separable and linear; $\frac{dT}{dt}=-k(T-T_s)$ likewise. **Use whichever gives the easier integral.**

**Many are neither.** $y'=x^2+y^2$ has a $y^2$, so it is not linear, and it does not factor, so it is not separable. **Tomorrow addresses what to do then.**

---

## 6. What To Take From This Lecture

1. **Standard form first:** coefficient of $y'$ equal to 1, then read off $P$.
2. **$\mu=e^{\int P\,dx}$**, derived by demanding that $\mu y'+\mu Py$ be $(\mu y)'$.
3. **Then $(\mu y)'=\mu Q$**, and integrate.
4. **Simplify $e^{\int P}$ carefully** — $e^{-2\ln x}=x^{-2}$.
5. **Check whether the left side is already a derivative.**
6. **"Rate in minus rate out" gives a linear equation**, which is why mixing and circuit problems all look alike.

---

*Next: Wednesday — Modelling, and When Closed Forms Fail*
