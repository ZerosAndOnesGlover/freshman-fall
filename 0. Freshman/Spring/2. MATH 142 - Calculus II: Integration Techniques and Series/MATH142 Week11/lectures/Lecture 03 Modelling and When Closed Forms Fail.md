# MATH 142 · Calculus II
## Week 11 · Lecture 3 (Friday)
### Modelling, and When Closed Forms Fail

**Date:** Friday 9 April 2027 · 11:00–11:50 · Week 11

---

**Reading:** Stewart §9.2, §9.4 | Apostol Ch. 8 §8.7

---

## 1. Slope Fields — Seeing a Solution Without Solving

$$\frac{dy}{dx} = f(x,y)$$

**The equation gives the slope of the solution through every point.** Drawing a short segment of that slope at each point of a grid produces a **slope field**, and a solution curve is any curve that follows the segments.

> **This is the geometric content of a first-order equation**, and it exists whether or not the
> equation can be solved. **You can sketch the qualitative behaviour of $y'=x^2+y^2$ in two minutes,
> and no formula for it exists at all.**

**An initial condition picks a starting point; the field determines the rest.** Lab 11 draws these.

---

## 2. Three Standard Models

### Exponential decay

$$\frac{dN}{dt} = -\lambda N \implies N = N_0e^{-\lambda t}$$

**Half-life:** setting $N=\frac{N_0}{2}$ gives $t_{1/2} = \frac{\ln2}{\lambda}$ — **independent of $N_0$**, which is why half-life is a well-defined property of an isotope.

### Newton's law of cooling

$$\frac{dT}{dt} = -k(T-T_s) \implies \boxed{T(t) = T_s+(T_0-T_s)e^{-kt}}$$

*(Verified.)*

**The excess temperature decays exponentially.** Note the equation is both separable and linear — either method works.

### Logistic growth

$$\frac{dP}{dt} = kP\left(1-\frac PM\right) \implies P(t) = \frac{M}{1+Ae^{-kt}}$$

*(Verified — Monday's Example 5.)*

**Three regimes, readable from the equation without solving it:**

| $P$ | $\frac{dP}{dt}$ | behaviour |
|---|---|---|
| small | $\approx kP$ | nearly exponential |
| $\frac M2$ | maximum | fastest growth |
| $\to M$ | $\to0$ | levels off |

**And two equilibria, $P=0$ and $P=M$.** $P=M$ is **stable** (nearby solutions approach it); $P=0$ is **unstable** (nearby solutions run away). **You can read stability straight off the sign of $\frac{dP}{dt}$ either side of an equilibrium** — no solving required.

---

## 3. When There Is No Closed Form

$$\frac{dy}{dx} = x^2+y^2, \qquad y(0)=0$$

**Not separable** (the right side does not factor). **Not linear** (there is a $y^2$).

**And it has no elementary solution.** *(Verified: a computer algebra system fails on it outright.)*

> **This is Week 0's fact in its final costume.** Most integrals cannot be evaluated in elementary
> terms; **most differential equations cannot be solved in elementary terms either**, and by a wide
> margin. The two solvable families of this week are the exception, not the rule.

**Two honest responses**, and the rest of the course has prepared you for both.

---

## 4. Response One — Power Series

**Assume a solution $y=\sum a_nx^n$, substitute, and match coefficients.** Legal because power series may be differentiated term by term inside their radius (**Week 9**).

### Example — $y'=x+y$, $y(0)=1$

Write $y=\sum_{n\ge0}a_nx^n$, so $y' = \sum_{n\ge0}(n+1)a_{n+1}x^n$. Substituting:

$$\sum_{n\ge0}(n+1)a_{n+1}x^n = x+\sum_{n\ge0}a_nx^n$$

**Matching coefficients:**

| power | equation | result |
|---|---|---|
| $x^0$ | $a_1 = a_0$ | $a_1=1$ |
| $x^1$ | $2a_2 = 1+a_1$ | $a_2=1$ |
| $x^n$, $n\ge2$ | $(n+1)a_{n+1}=a_n$ | $a_{n+1} = \frac{a_n}{n+1}$ |

With $a_0=1$ from the initial condition, this gives

$$1,\ 1,\ 1,\ \tfrac13,\ \tfrac1{12},\ \tfrac1{60},\ \tfrac{1}{360},\ \ldots$$

$$y = 1+x+x^2+\frac{x^3}{3}+\frac{x^4}{12}+\frac{x^5}{60}+\cdots$$

**Check against the exact solution.** This equation *is* linear, so we can solve it: $\mu=e^{-x}$ gives

$$y = 2e^x-x-1$$

whose Maclaurin series is $1+x+x^2+\frac{x^3}{3}+\frac{x^4}{12}+\frac{x^5}{60}+\cdots$ — **identical.** *(Verified.)*

> **The series method works even when the closed-form method does not**, which is exactly why it is
> worth having. **Week 10's machinery applied to an unknown function.**

---

## 5. Response Two — Numerical Solution

**Euler's method.** From $y'=f(x,y)$, step along the tangent line:

$$\boxed{y_{n+1} = y_n + h\,f(x_n,y_n)}, \qquad x_{n+1}=x_n+h$$

**It is the slope field, walked.** Follow the arrow for a short distance, re-read the arrow, repeat.

### It is first order, and that is not good enough

**Lab 11 measures the error on $y'=y-x$, $y(0)=2$** (exact: $y=e^x+x+1$):

| method | error ratio on halving $h$ | order | error at $n=320$ |
|---|---|---|---|
| **Euler** | $\to2$ | 1 | $4.24\times10^{-3}$ |
| **Improved Euler (RK2)** | $\to4$ | 2 | $4.41\times10^{-6}$ |
| **Runge–Kutta 4 (RK4)** | $\to16$ | 4 | $2.15\times10^{-12}$ |

*(All measured.)*

**Improved Euler** averages the slope at the start and at the predicted endpoint:

$$y_{n+1} = y_n+\frac h2\Big[f(x_n,y_n)+f\big(x_n+h,\ y_n+hf(x_n,y_n)\big)\Big]$$

**That single change takes the order from 1 to 2.**

> **The ratio 16 for RK4 should be familiar.** It is Simpson's rule's ratio from **Lab 0**, in Week 0
> — the first measurement of the course. **The same order-of-convergence analysis, on a completely
> different kind of problem.** Halving the step multiplies the error by $\left(\frac12\right)^p$, and
> $p$ is what decides whether a method is usable.

**At $n=320$, RK4 beats Euler by a factor of two billion**, for four function evaluations per step against one.

### The Riccati equation, solved numerically

For $y'=x^2+y^2$, $y(0)=0$, RK4 gives

$$y(1) = 0.350231844\ldots$$

*(Verified: stable to 9 digits from $n=100$ to $n=1000$.)*

**No formula exists. The number does.**

---

## 6. What To Take From This Lecture

1. **A slope field shows the solutions without solving**, and works for every equation.
2. **Equilibria and their stability are readable from the sign of $y'$** alone.
3. **Exponential decay, Newton cooling, logistic growth** — the three standard first-order models.
4. **Most differential equations have no elementary solution**, exactly as most integrals do not.
5. **Power series solve equations that closed forms cannot** — Week 9's term-by-term differentiation, applied to an unknown.
6. **Euler is order 1; improved Euler order 2; RK4 order 4** — and the order is what matters.

---

## Looking Ahead

**Week 12 closes the course.** Systems of equations, a proper preview of the numerical methods you will meet in MATH 341, and the final review.

**The final exam is comprehensive.** Everything from Week 0's Riemann sums to this week's Runge–Kutta.

---

*Next: Week 12, Monday — Systems and Numerical Methods*
