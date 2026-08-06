# MATH 142 · Calculus II
## Week 11 · Reference Sheet
### Differential Equations

---

## Vocabulary

**Order** = highest derivative present. **A solution is a function satisfying the equation identically.**

**General solution** carries arbitrary constants; an **initial condition** selects a particular one.

> **Find the general solution first, apply the initial condition last.**
> **Check every answer by substituting it back.**

---

## Separable Equations

$$\frac{dy}{dx}=g(x)h(y) \implies \int\frac{dy}{h(y)} = \int g(x)\,dx$$

| Equation | Solution |
|---|---|
| $y'=ky$ | $y=Ce^{kx}$ |
| $y'=xy$ | $y=Ce^{x^2/2}$ |
| $y'=y^2$ | $y=\dfrac{-1}{x+C}$ |
| $y'=\dfrac xy$ | $y=\pm\sqrt{x^2+C}$ |
| $y'=y(1-y)$, $y(0)=\tfrac12$ | $y=\dfrac{1}{1+e^{-x}}$ — **the sigmoid** |

*(all verified)*

> **Restore equilibrium solutions lost when dividing by $h(y)$.** For the logistic equation, $P=0$
> and $P=M$ are genuine solutions killed by the division.

**Solutions need not exist globally:** $y'=y^2$, $y(0)=1$ gives $y=\frac{1}{1-x}$, valid only on $(-\infty,1)$. **State the interval.**

---

## First-Order Linear Equations

$$\frac{dy}{dx}+P(x)y = Q(x)$$

**Standard form first** — coefficient of $y'$ equal to 1 — **then** read off $P$.

$$\boxed{\mu = e^{\int P\,dx}}\qquad\Longrightarrow\qquad (\mu y)' = \mu Q \qquad\Longrightarrow\qquad y = \frac1\mu\int\mu Q\,dx$$

**Derivation:** demand that $\mu y'+\mu Py$ equal $(\mu y)' = \mu y'+\mu'y$, i.e. $\mu'=\mu P$ — itself a separable equation. **No constant of integration is needed**, since a constant multiple of $\mu$ cancels.

| Equation | $\mu$ | Solution |
|---|---|---|
| $y'+y=x$ | $e^x$ | $x-1+Ce^{-x}$ |
| $y'+2y=e^x$ | $e^{2x}$ | $\frac{e^x}{3}+Ce^{-2x}$ |
| $xy'+y=x^2$ | $x$ | $\frac{x^2}{3}+\frac Cx$ |
| $y'-\frac2xy=x^2$ | $x^{-2}$ | $x^3+Cx^2$ |

*(all verified)*

**Simplify $e^{\int P}$ with logarithm laws:** $e^{-2\ln x}=x^{-2}$, **not** $-2x$.

> **Glance at the left side first** — sometimes it is already a product rule, as in $xy'+y=(xy)'$.

---

## Standard Models

| Model | Equation | Solution |
|---|---|---|
| Exponential growth/decay | $\frac{dN}{dt}=\pm\lambda N$ | $N_0e^{\pm\lambda t}$ |
| Newton cooling | $\frac{dT}{dt}=-k(T-T_s)$ | $T_s+(T_0-T_s)e^{-kt}$ |
| Logistic | $\frac{dP}{dt}=kP\left(1-\frac PM\right)$ | $\dfrac{M}{1+Ae^{-kt}}$ |
| Mixing / RL circuit | $y'+\frac rVy = rc_{\text{in}}$ | linear, $\mu=e^{rt/V}$ |

*(all verified)*

**Half-life:** $t_{1/2}=\frac{\ln2}{\lambda}$ — **independent of $N_0$.**

**"Rate in minus rate out" produces a linear equation** almost every time.

### Equilibria and stability, without solving

Set $\frac{dy}{dx}=0$ and solve for $y$. Then **the sign of $y'$ on either side gives stability**:

For the logistic equation: $P=M$ is **stable** (solutions approach it), $P=0$ is **unstable**.

---

## When There Is No Closed Form

$$\frac{dy}{dx}=x^2+y^2$$

**Not separable** (does not factor), **not linear** ($y^2$), **and not elementary.** *(Verified: a CAS fails.)*

> **Most differential equations cannot be solved in closed form**, exactly as most integrals cannot.
> The two families above are the exception.

### Response 1 — power series

Assume $y=\sum a_nx^n$, substitute, match coefficients. **Licensed by Week 9's term-by-term differentiation.**

*Example: $y'=x+y$, $y(0)=1$ gives $a_1=a_0$, $2a_2=1+a_1$, and $(n+1)a_{n+1}=a_n$ for $n\ge2$, hence*

$$y = 1+x+x^2+\frac{x^3}{3}+\frac{x^4}{12}+\frac{x^5}{60}+\cdots$$

*— identical to the Maclaurin series of the exact solution $2e^x-x-1$. (Verified.)*

### Response 2 — numerical

$$\textbf{Euler: } y_{n+1}=y_n+hf(x_n,y_n)$$

$$\textbf{Improved Euler: } y_{n+1}=y_n+\frac h2\big[k_1+k_2\big],\quad k_1=f(x_n,y_n),\ k_2=f(x_n+h,y_n+hk_1)$$

$$\textbf{RK4: } y_{n+1}=y_n+\frac h6\big[k_1+2k_2+2k_3+k_4\big]$$

### Measured orders

On $y'=y-x$, $y(0)=2$ (exact $y=e^x+x+1$, $y(1)=4.71828182845905$):

| method | ratio on doubling $n$ | order | error at $n=320$ | $f$-evals/step |
|---|---|---|---|---|
| **Euler** | $\to2$ | **1** | $4.24\times10^{-3}$ | 1 |
| **Improved Euler** | $\to4$ | **2** | $4.41\times10^{-6}$ | 2 |
| **RK4** | $\to\mathbf{16}$ | **4** | $2.15\times10^{-12}$ | 4 |

*(all measured)*

> **RK4's ratio of 16 is Simpson's rule's ratio from Lab 0, in Week 0.** The same order analysis,
> eleven weeks apart, on a completely different problem. **RK4 beats Euler by a factor of two
> billion at $n=320$, for four evaluations per step against one.**

**Riccati example:** $y'=x^2+y^2$, $y(0)=0$ gives $y(1)=0.350231844\ldots$ by RK4, stable to 9 digits from $n=100$. **No formula exists; the number does.**

---

## Method Selection

| Equation | Method |
|---|---|
| $y'=f(x)$ | integrate |
| $y'=g(x)h(y)$ | separable |
| $y'+P(x)y=Q(x)$ | linear, integrating factor |
| both | whichever integral is easier |
| neither | series, or numerical |

---

## Common Errors

1. **Applying the initial condition before finding the general solution.**
2. **Reading $P$ off an equation not in standard form.**
3. **Mis-simplifying $e^{\int P}$.**
4. **Losing equilibrium solutions** when dividing by $h(y)$.
5. **Not stating the interval of validity.**
6. **Not checking the answer by substitution.**

---

*MATH 142 · Week 11 · Reference Sheet*
