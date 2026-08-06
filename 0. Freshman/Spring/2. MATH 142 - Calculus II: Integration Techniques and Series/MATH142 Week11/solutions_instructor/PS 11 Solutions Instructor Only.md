# MATH 142 · Calculus II
## Problem Set 11 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every solution verified symbolically.

> **Marking philosophy.** **Award marks for the substitution check.** Students who verify their own
> answers catch their own errors, and this is the last set on which that habit can be reinforced
> before the final.
>
> **The integrals are the assessment.** Separating and finding $\mu$ are mechanical; the Week 0–2
> integration that follows is where the difficulty lives.

---

## Part A — Separable (5 pts each)

### A1 (5) $\;y'=3y$

$$\int\frac{dy}{y} = \int3\,dx \implies \ln|y| = 3x+C_1 \implies \boxed{y = Ce^{3x}}$$

*Verified. Note $y=0$ is the equilibrium solution, recovered by allowing $C=0$.*

### A2 (5) $\;y'=x^2y$

$$\ln|y| = \frac{x^3}{3}+C_1 \implies \boxed{y=Ce^{x^3/3}}$$

*Verified.*

### A3 (5) $\;y'=\frac{e^x}{y}$

$$\int y\,dy = \int e^x dx \implies \frac{y^2}{2} = e^x+C_1 \implies \boxed{y = \pm\sqrt{2e^x+C}}$$

*Verified — the CAS returns both branches.*

**The branch is chosen by the initial condition**: a positive $y(x_0)$ selects the $+$ branch, and the solution stays on it (it cannot cross $y=0$, where the equation is undefined).

*Marking: 3 solution, **2 for addressing the branch** (the question asked).*

### A4 (5) $\;y'=y(1-y)$, $y(0)=\frac12$

**Partial fractions** (Week 2): $\dfrac{1}{y(1-y)} = \dfrac1y+\dfrac{1}{1-y}$, so

$$\ln\left|\frac{y}{1-y}\right| = x+C \implies \frac{y}{1-y} = Ae^x \implies y = \frac{Ae^x}{1+Ae^x}$$

With $y(0)=\frac12$: $A=1$, so

$$\boxed{y = \frac{e^x}{1+e^x} = \frac{1}{1+e^{-x}}}$$

*Verified.*

**This is the logistic (sigmoid) function** — the activation function used throughout machine learning, and the standard model for a saturating process. **Students should recognise it.**

*Marking: 2 partial fractions, 2 solution, **1 for identifying it.***

---

## Part B — Linear (6 pts each)

*Standard marking: 2 standard form and $P$, 2 integrating factor, 2 integration.*

### B1 (6) $\;y'+3y=e^{-x}$

$\mu=e^{3x}$; $(e^{3x}y)'=e^{2x}$; $e^{3x}y = \frac{e^{2x}}{2}+C$:

$$\boxed{y = \frac{e^{-x}}{2}+Ce^{-3x}}$$

*Verified.*

### B2 (6) $\;y'+\frac1xy=\cos x$

$\mu = e^{\int dx/x} = x$; $(xy)' = x\cos x$. **Integration by parts** (Week 1): $\int x\cos x\,dx = x\sin x+\cos x$.

$$xy = x\sin x+\cos x+C \implies \boxed{y = \sin x+\frac{\cos x}{x}+\frac Cx}$$

*Verified.*

### B3 (6) $\;xy'-2y=x^3$

**Standard form:** $y'-\frac2xy = x^2$, so $P=-\frac2x$ and $\mu = e^{-2\ln x} = x^{-2}$.

$$\left(\frac{y}{x^2}\right)' = 1 \implies \frac{y}{x^2} = x+C \implies \boxed{y = x^3+Cx^2}$$

*Verified.*

*Marking: **3 of the 6 for dividing by $x$ first.** Reading $P=-2$ off the undivided equation is the standard error.*

### B4 (6) $\;y'+y\tan x = \sin x$

$$\int\tan x\,dx = -\ln|\cos x| \implies \mu = e^{-\ln|\cos x|} = \frac{1}{\cos x} = \sec x$$

$$(y\sec x)' = \sin x\sec x = \tan x \implies y\sec x = -\ln|\cos x|+C$$

$$\boxed{y = \cos x\big(C-\ln|\cos x|\big)}$$

*Verified.*

*Marking: **3 for simplifying $e^{-\ln|\cos x|}$ to $\sec x$.** This is where the problem's difficulty sits.*

### B5 (6) $\;y'+2y=4$, $y(0)=1$

$\mu=e^{2x}$; $(e^{2x}y)'=4e^{2x}$; $e^{2x}y = 2e^{2x}+C$, so $y=2+Ce^{-2x}$. With $y(0)=1$: $C=-1$.

$$\boxed{y = 2-e^{-2x}}$$

*Verified.*

**(b)** $\lim_{x\to\infty}y = \boxed{2}$.

**Predictable without solving:** the equilibrium is where $y'=0$, i.e. $2y=4$, so $y=2$ — and since $y'>0$ when $y<2$ and $y'<0$ when $y>2$, that equilibrium is **stable** and attracts every solution.

*Marking: 4 + 2. **(b) must give the equilibrium argument**, not just the limit.*

---

## Part C — Modelling (6 pts each)

### C1 (6) — cooling

General solution $T = T_s+(T_0-T_s)e^{-kt} = 20+70e^{-kt}$.

**(a)** $T(10)=70$ gives $50 = 70e^{-10k}$, so

$$k = \frac{1}{10}\ln\frac75 = \boxed{0.033647\ \text{min}^{-1}}$$

**(b)** $T=40$: $\;20 = 70e^{-kt}$, so $t = \frac{1}{k}\ln\frac72 = \boxed{37.23\ \text{minutes}}$

*(Both verified — substituting back gives exactly $70.0$ and $40.0$.)*

*Marking: 2 general solution, 2 + 2.*

### C2 (6) — half-life

$N=N_0e^{-\lambda t}$. Setting $N=\frac{N_0}{2}$:

$$\frac12 = e^{-\lambda t} \implies t_{1/2} = \frac{\ln2}{\lambda}$$

**$N_0$ cancels**, because the equation is *linear* in $N$ — halving is a **ratio**, and the ratio's evolution does not depend on the starting amount. **Every isotope therefore has a well-defined half-life** independent of sample size.

*Marking: 3 derivation, **3 for the explanation of why $N_0$ drops out.***

### C3 (6) — mixing

**(a)** Rate in $= 4\times0.5 = 2$ kg/min. Rate out $= 4\times\frac{y}{100}$. So

$$\frac{dy}{dt} = 2-\frac{y}{25} \implies \boxed{y'+\frac{y}{25} = 2}$$

**(b)** $\mu = e^{t/25}$; solving with $y(0)=0$:

$$\boxed{y(t) = 50\left(1-e^{-t/25}\right)}$$

*Verified.*

**(c)** $y\to\boxed{50}$ kg. **Expected**, because the tank eventually reaches the inflow concentration: $100\text{ L}\times0.5\text{ kg/L} = 50$ kg.

*Marking: 2 + 2 + 2. **(c) must give the physical reason**, not just the limit.*

### C4 (6) — equilibria without solving

**(a)** $kP\left(1-\frac PM\right)=0$ gives $\boxed{P=0}$ and $\boxed{P=M}$.

**(b)** For $0<P<M$: both factors positive, so $\frac{dP}{dt}>0$. For $P>M$: $1-\frac PM<0$, so $\frac{dP}{dt}<0$.

**(c)** Solutions **increase** below $M$ and **decrease** above it, so they approach $M$ from both sides:

- $P=M$ is **stable**
- $P=0$ is **unstable** (any $P>0$ moves away from it)

*Marking: 2 + 2 + 2. **Deduct if the student solved the equation** — the question said not to, and the sign argument is the technique.*

### C5 (6) — no closed form

**(a)** **Not separable:** $x^2+y^2$ cannot be written as $g(x)h(y)$ (a sum, not a product). **Not linear:** $y$ appears squared.

**(b)** **Numerically** — Euler's method, or better **RK4**, stepping from $x=0$ to $x=1$. Halving the step and comparing successive results indicates the number of reliable digits.

*(RK4 gives $y(1)=0.350231844$, stable to 9 digits.)*

**(c)** **The same situation as Week 0**: a perfectly well-posed problem whose answer exists but has no elementary formula, so the answer must be computed rather than written.

**The difference:** in Week 10 the integral $\int e^{-x^2}dx$ acquired a *series* representation, which gave both a fast computation and a rigorous error bound. **A general differential equation may or may not yield to the series method**, and here the numerical route is the practical one.

*Marking: 2 + 2 + 2. **(c) must draw the Week 0 parallel**; full marks require noting that the series rescue is not always available.*

---

## Part D — Concept (10 pts each)

### D1 (10) — deriving $\mu$

**(a)** Multiply $y'+Py=Q$ by $\mu(x)$: $\;\mu y'+\mu Py = \mu Q$. We want the left side to be $(\mu y)' = \mu y'+\mu'y$, which requires

$$\mu' = \mu P$$

— a **separable** equation for $\mu$. Solving: $\frac{d\mu}{\mu} = P\,dx$, so $\ln\mu = \int P\,dx$ and $\mu = e^{\int P\,dx}$. Then $(\mu y)'=\mu Q$ and $y = \frac1\mu\int\mu Q\,dx$. $\blacksquare$

**(b)** A constant $C_0$ in $\int P\,dx$ multiplies $\mu$ by $e^{C_0}$ — **a constant factor, which appears in both $\mu$ and $\int\mu Q$ and cancels** in $\frac1\mu\int\mu Q$. So it is harmless and conventionally omitted.

**(c)** For $y'-\frac2xy=x^2$: $P=-\frac2x$, $\int P\,dx = -2\ln x$, and

$$\mu = e^{-2\ln x} = e^{\ln x^{-2}} = x^{-2}$$

Then $(x^{-2}y)' = 1$, so $x^{-2}y = x+C$ and $y=x^3+Cx^2$. *(Verified.)*

**(d)** The formula alone gives no guidance when the equation is not in standard form, when $e^{\int P}$ needs simplifying, or when the left side is already a derivative. **Knowing that $\mu$ is chosen to force a product rule makes all three cases obvious**, and the derivation is three lines.

*Marking: 4 + 2 + 2 + 2. **(a) must show $\mu'=\mu P$ arising from the product rule requirement**, not merely quote the answer.*

### D2 (10) — series solutions

**(a)** With $y=\sum_{n\ge0}a_nx^n$ we have $y' = \sum_{n\ge0}(n+1)a_{n+1}x^n$. Substituting into $y'=x+y$:

$$\sum_{n\ge0}(n+1)a_{n+1}x^n = x+\sum_{n\ge0}a_nx^n$$

Matching coefficients:

$$a_1=a_0,\qquad 2a_2 = 1+a_1,\qquad (n+1)a_{n+1}=a_n\ \ (n\ge2)$$

**(b)** With $a_0=1$ (from $y(0)=1$):

$$a_0=1,\ a_1=1,\ a_2=1,\ a_3=\tfrac13,\ a_4=\tfrac1{12},\ a_5=\tfrac1{60}$$

*(Verified.)*

**(c)** The equation is linear: $y'-y=x$, $\mu=e^{-x}$, $(e^{-x}y)' = xe^{-x}$, and $\int xe^{-x}dx = -(x+1)e^{-x}$, so $e^{-x}y = -(x+1)e^{-x}+C$ and $y=Ce^x-x-1$. With $y(0)=1$: $C=2$.

$$y = 2e^x-x-1$$

Its Maclaurin series: $2\left(1+x+\frac{x^2}{2}+\frac{x^3}{6}+\frac{x^4}{24}+\frac{x^5}{120}\right)-x-1 = 1+x+x^2+\frac{x^3}{3}+\frac{x^4}{12}+\frac{x^5}{60}+\cdots$

**Identical to (b).** ✓ *(Verified.)*

**(d)** **The theorem permitting term-by-term differentiation of a power series inside its radius of convergence** (Week 9, Lecture 3) — which itself rests on absolute convergence inside the radius (Week 8).

*Marking: 3 + 2 + 3 + 2. **(d) must name the theorem**, and full credit for tracing it back to absolute convergence.*

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Separable equations |
| B (5 × 6) | 30 | Integrating factors |
| C (5 × 6) | 30 | Modelling; equilibria; a wall |
| D (2 × 10) | 20 | Deriving $\mu$; series solutions |
| **Total** | **100** | |

---

## Diagnostic Notes

| Question | Weakness | Bites in |
|---|---|---|
| **B3** | Not putting the equation in standard form | The final |
| **B4** | Mis-simplifying $e^{\int P}$ | The final |
| **C4** | Solving when a sign argument was asked for | The final's conceptual section |
| **D2(d)** | Not tracking which theorem licenses which step | The final |

**This is the last problem set.** The final is comprehensive, and the single most valuable revision instruction remains the one from Midterm 1: **look before you compute** — classify the equation, check the hypotheses, then work.

---

*MATH 142 · Week 11 · PS 11 Solutions · Instructor Only*
