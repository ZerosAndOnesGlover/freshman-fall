# MATH 142 · Calculus II
## Problem Set 11
### Topic: Differential Equations — Separable and Linear
**Released:** Wednesday, Week 11 | **Due:** Wednesday, Week 12 (start of class)

---

> **Check every solution by substituting it back.** This is Week 0's habit in its final form, and it
> catches almost every error in this material.
>
> **General solution first, initial condition last.**
>
> **State the interval of validity** where a solution fails to exist everywhere.
>
> **For linear equations, put the equation in standard form before reading off $P(x)$.**

---

## Part A — Separable Equations (5 pts each)

**A1.** $\dfrac{dy}{dx}=3y$

**A2.** $\dfrac{dy}{dx}=x^2y$

**A3.** $\dfrac{dy}{dx}=\dfrac{e^x}{y}$

*Your answer may be implicit, or may need a branch choice — say which and why.*

**A4.** $\dfrac{dy}{dx}=y(1-y)$, $y(0)=\tfrac12$.

*Partial fractions (Week 2). Identify the resulting function — you have met it in a computing context.*

---

## Part B — First-Order Linear Equations (6 pts each)

*Show the integrating factor and the standard form.*

**B1.** $y'+3y = e^{-x}$

**B2.** $y'+\dfrac1x\,y = \cos x$

**B3.** $xy'-2y = x^3$

*Put it in standard form first.*

**B4.** $y'+y\tan x = \sin x$

*Simplify $e^{\int\tan x\,dx}$ carefully.*

**B5.** $y'+2y=4$, $y(0)=1$.

- (a) Solve it.
- (b) What is $\lim_{x\to\infty}y(x)$, and how could you have predicted it from the equation without solving?

---

## Part C — Modelling (6 pts each)

**C1.** *(Cooling.)* Solve $\dfrac{dT}{dt}=-k(T-T_s)$ with $T(0)=T_0$.

A cup of coffee at $90^\circ$C is left in a room at $20^\circ$C. After 10 minutes it is $70^\circ$C.

- (a) Find $k$.
- (b) When will it reach $40^\circ$C?

**C2.** *(Decay.)* A radioactive sample decays by $\frac{dN}{dt}=-\lambda N$.

Show the half-life is $\frac{\ln2}{\lambda}$ and explain why it does not depend on the initial amount.

**C3.** *(Mixing.)* A tank holds 100 L of pure water. Brine of concentration $0.5$ kg/L enters at 4 L/min; the well-stirred mixture leaves at 4 L/min.

- (a) Write the differential equation for the salt content $y(t)$.
- (b) Solve it with $y(0)=0$.
- (c) What is the long-run salt content, and why is that the answer you would expect?

**C4.** *(Equilibria.)* For $\dfrac{dP}{dt}=kP\left(1-\dfrac PM\right)$ with $k,M>0$:

- (a) Find both equilibrium solutions.
- (b) Determine the sign of $\frac{dP}{dt}$ for $0<P<M$ and for $P>M$.
- (c) Hence classify each equilibrium as stable or unstable, **without solving the equation.**

**C5.** *(No closed form.)* Consider $\dfrac{dy}{dx}=x^2+y^2$, $y(0)=0$.

- (a) Show it is neither separable nor linear.
- (b) Describe how you would obtain $y(1)$ to several decimal places, naming a method.
- (c) Comment on how this compares with the situation in Week 0 regarding $\int e^{-x^2}dx$.

---

## Part D — Concept (10 pts each)

**D1.** *(Deriving the integrating factor.)*

- (a) Starting from $y'+P(x)y=Q(x)$, derive $\mu=e^{\int P\,dx}$ by requiring that $\mu y'+\mu Py$ be exactly $(\mu y)'$.
- (b) Explain why no constant of integration is needed in $\int P\,dx$.
- (c) Apply your derivation to $y'-\frac2xy=x^2$, showing the simplification of $e^{\int P}$.
- (d) Explain in one or two sentences why memorising the formula without the derivation is a poor idea.

**D2.** *(Series solutions.)* Consider $y'=x+y$ with $y(0)=1$.

- (a) Assume $y=\sum_{n\ge0}a_nx^n$ and derive a recurrence for the coefficients.
- (b) Compute $a_0,\ldots,a_5$.
- (c) Solve the equation exactly by the integrating factor method, and expand your answer as a Maclaurin series to $x^5$. **Confirm the two agree.**
- (d) **Which theorem from Week 9 licensed differentiating the series term by term?** State it.

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Separable equations |
| B (5 × 6) | 30 | Integrating factors |
| C (5 × 6) | 30 | Modelling, equilibria, and a wall |
| D (2 × 10) | 20 | Deriving $\mu$; series solutions |
| **Total** | **100** | |

---

## Before You Submit

1. **Every solution substituted back and checked.**
2. **Every linear problem shows its standard form and $\mu$.**
3. **Check A3 for the branch** and B4 for the simplification of $e^{\int\tan}$.
4. **C4 is answered without solving the equation.** If you solved it, you did more work than asked.

---

*MATH 142 · Week 11 · Problem Set 11*
