# MATH 142 · Calculus II
## Week 11 · Overview
### Introduction to Differential Equations

---

**Topic:** equations whose unknown is a function
**Reading:** Stewart §9.1–9.5 | Apostol Ch. 8 §8.1–8.7
**Assessment this week:** PS 11, Lab 11, **Quiz 11** *(Monday — covers Week 10)*

---

## A Different Kind of Equation

**In an algebraic equation the unknown is a number.** $x^2-5x+6=0$ has solutions $2$ and $3$.

**In a differential equation the unknown is a function**, and the equation relates it to its own derivatives:

$$\frac{dy}{dx} = ky, \qquad y'+P(x)y = Q(x), \qquad \frac{dy}{dt}=ky\left(1-\frac yM\right)$$

**A solution is a function that satisfies the equation identically.** Because differentiating loses a constant, solutions come in families — and an **initial condition** picks one out.

> **This is where the whole course gets used.** Solving a differential equation means computing an
> integral, so every technique from Weeks 0–2 reappears: substitution, parts, partial fractions.
> **Week 11 is Weeks 0–2 with a purpose.**

---

## Why It Matters

**Differential equations are how change is described.** Almost every quantitative law in science is one:

| Field | Equation | What it says |
|---|---|---|
| Radioactivity | $\frac{dN}{dt} = -\lambda N$ | decay rate is proportional to how much is left |
| Population | $\frac{dP}{dt} = kP\left(1-\frac PM\right)$ | growth slows as resources run out |
| Cooling | $\frac{dT}{dt} = -k(T-T_s)$ | cooling rate is proportional to the excess temperature |
| Circuits | $L\frac{dI}{dt}+RI = V$ | Kirchhoff's law for an RL circuit |
| Mechanics | $m\frac{d^2x}{dt^2} = F$ | Newton's second law |

**The last is second-order and beyond this course** — but the first four are exactly what Weeks 11 covers.

---

## The Three Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Monday | Separable Equations | Separate the variables, then integrate |
| **Lecture 2** | Tuesday | First-Order Linear Equations | The integrating factor makes it a product rule |
| **Lecture 3** | Wednesday | Modelling, and When Closed Forms Fail | Where the honest answer is numerical |

---

## Two Solvable Types, and Then a Wall

**This week teaches exactly two methods**, and between them they cover most first-order equations you will meet:

**Separable:** $\dfrac{dy}{dx}=g(x)h(y)$ — rearrange to $\dfrac{dy}{h(y)} = g(x)\,dx$ and integrate both sides.

**Linear:** $y'+P(x)y=Q(x)$ — multiply by $\mu=e^{\int P\,dx}$, which turns the left side into $(\mu y)'$ exactly.

**And then the wall.** The innocuous-looking

$$\frac{dy}{dx} = x^2+y^2$$

is neither separable nor linear, and **has no elementary solution.** *(Verified: a computer algebra system fails on it outright.)*

> **This is the Week 0 pattern one last time.** Most differential equations, like most integrals,
> cannot be solved in closed form — and the response is the same: **numerical methods, with an error
> analysis.**

---

## Lab 11 Closes the Course's Numerical Arc

**Euler's method** approximates a solution by stepping along the slope field:

$$y_{n+1} = y_n + h\,f(x_n,y_n)$$

**Lab 11 measures its order, and two better methods.** On the test problem $y'=y-x$, $y(0)=2$:

| method | error ratio on halving $h$ | order |
|---|---|---|
| **Euler** | $\to2$ | **1** |
| **Improved Euler (RK2)** | $\to4$ | **2** |
| **Runge–Kutta 4 (RK4)** | $\to\mathbf{16}$ | **4** |

*(Measured.)*

> **That 16 should look familiar.** It is Simpson's rule's ratio from **Lab 0, Week 0** — the very
> first measurement of the course. **The same order-of-convergence analysis, applied to a completely
> different problem, ten weeks later.**

At $n=320$ steps, RK4's error is $2.15\times10^{-12}$ against Euler's $4.24\times10^{-3}$ — **a factor of two billion**, for four function evaluations per step instead of one.

---

## What Will Be Hard

**Separable equations hide integration problems.** Separating is the easy part; the resulting integrals often need partial fractions (the logistic equation) or parts. **If you cannot do Week 2, you cannot finish these.**

**The integrating factor must be derived, not memorised.** Knowing $\mu = e^{\int P}$ without knowing *why* it works makes every non-standard case impossible.

**Initial conditions come last.** Find the general solution, *then* apply $y(x_0)=y_0$. Substituting too early is a common and costly error.

---

## This Week's Work

1. **Quiz 11** — Monday, 15 minutes, **covers Week 10** (Taylor series, remainders)
2. **PS 11** — released Wednesday, due Wednesday of Week 12
3. **Lab 11** — slope fields, and Euler versus Runge–Kutta

---

## Looking Ahead

**Week 12 closes the course:** systems of equations, a preview of the numerical methods you will meet properly in later courses, and the final review.

**The final exam is comprehensive**, covering Weeks 0–12.

---

*Next: Monday — Differential Equations and Separable Equations*
