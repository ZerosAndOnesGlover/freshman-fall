# MATH 142 · Calculus II
## Week 11 · Lecture 1 (Monday)
### Differential Equations and Separable Equations

---

**Reading:** Stewart §9.1, §9.3 | Apostol Ch. 8 §8.1–8.4
**Quiz 11** — this Monday, **covers Week 10** (Taylor series, remainders, applications)

---

## 1. Vocabulary

A **differential equation** relates a function to its derivatives. Its **order** is the highest derivative appearing.

$$\underbrace{\frac{dy}{dx} = 2y}_{\text{first order}}, \qquad \underbrace{y''+4y = 0}_{\text{second order}}$$

**A solution is a function that satisfies the equation identically on an interval.**

### Checking a solution is easy — solving is hard

**Is $y=e^{2x}$ a solution of $y'=2y$?** Differentiate: $y' = 2e^{2x} = 2y$ ✓

**So is $y = Ce^{2x}$ for every constant $C$.** That family is the **general solution**; each choice of $C$ is a **particular solution**.

> **Always check your answer by substituting it back.** It is the exact analogue of Week 0's
> "differentiate your antiderivative", it costs thirty seconds, and it catches almost everything.

### Initial value problems

$$\frac{dy}{dx}=2y, \qquad y(0)=5$$

The general solution $y=Ce^{2x}$ gives $5 = Ce^0 = C$, so $y=5e^{2x}$.

> **Find the general solution first, then apply the condition.** Substituting the initial condition
> partway through is the most common structural error in this material.

---

## 2. The Simplest Kind

$$\frac{dy}{dx} = f(x) \implies y = \int f(x)\,dx$$

**Every antiderivative you computed in Weeks 0–2 was solving a differential equation** — you simply were not calling it that. **And the $+C$ was the general solution's arbitrary constant all along.**

---

## 3. Separable Equations

$$\boxed{\frac{dy}{dx} = g(x)\,h(y)}$$

**The variables separate:** move all the $y$'s to one side and all the $x$'s to the other, then integrate.

$$\frac{dy}{h(y)} = g(x)\,dx \implies \int\frac{dy}{h(y)} = \int g(x)\,dx$$

> **The manipulation $\frac{dy}{dx}\to dy,\ dx$ looks like treating a derivative as a fraction, which
> it is not.** The step is legitimate; it is substitution (Week 0) in disguise, applied to
> $\int\frac{y'(x)}{h(y(x))}dx$. **The notation is doing real work, as it did for the chain rule.**

### Example 1 — exponential growth and decay

$$\frac{dy}{dx} = ky \implies \int\frac{dy}{y} = \int k\,dx \implies \ln|y| = kx+C_1$$

Exponentiating: $|y| = e^{C_1}e^{kx}$, and absorbing signs and constants,

$$\boxed{y = Ce^{kx}}$$

*(Verified.)*

**This is the single most important differential equation in science.** It says *the rate of change is proportional to the amount present*, and it governs radioactive decay ($k<0$), unchecked population growth ($k>0$), continuously compounded interest, and charging capacitors.

### Example 2

$$\frac{dy}{dx} = xy \implies \int\frac{dy}{y} = \int x\,dx \implies \ln|y| = \frac{x^2}{2}+C_1 \implies \boxed{y = Ce^{x^2/2}}$$

*(Verified.)*

### Example 3 — where a solution blows up

$$\frac{dy}{dx}=y^2 \implies \int\frac{dy}{y^2} = \int dx \implies -\frac1y = x+C \implies \boxed{y = \frac{-1}{x+C}}$$

*(Verified.)*

With $y(0)=1$: $-1 = C^{-1}\cdot(-1)$ gives $C=-1$, so $y = \frac{1}{1-x}$.

> **The solution exists only on $(-\infty,1)$ — it blows up at $x=1$.** Nothing in the equation
> $y'=y^2$ warns you of this. **A differential equation's solution can fail to exist globally even
> when the equation is perfectly well behaved**, and finding the interval of validity is part of the
> answer.

### Example 4 — an implicit solution

$$\frac{dy}{dx} = \frac xy \implies \int y\,dy = \int x\,dx \implies \frac{y^2}{2} = \frac{x^2}{2}+C \implies y^2-x^2 = C'$$

$$\boxed{y = \pm\sqrt{x^2+C'}}$$

*(Verified — the CAS returns both branches.)*

**Sometimes the tidiest form is implicit.** Solving for $y$ may force a choice of branch, determined by the initial condition.

---

## 4. Where the Integration Techniques Come Back

**Separating is the easy part.** The integrals it produces are where Weeks 0–2 get used.

### Example 5 — the logistic equation, needing partial fractions

$$\frac{dP}{dt} = kP\left(1-\frac PM\right)$$

**A population growing at rate $k$ but limited by a carrying capacity $M$.** Separating:

$$\int\frac{dP}{P\left(1-\frac PM\right)} = \int k\,dt$$

**The left side needs partial fractions** (Week 2):

$$\frac{1}{P\left(1-\frac PM\right)} = \frac{1}{P}+\frac{1/M}{1-\frac PM}$$

Integrating gives $\ln|P| - \ln\left|1-\frac PM\right| = kt+C$, and solving for $P$:

$$\boxed{P(t) = \frac{M}{1+Ae^{-kt}}}$$

*(Verified — the CAS returns an equivalent form.)*

**The famous S-curve.** As $t\to\infty$, $P\to M$; for small $t$ with $P\ll M$ it grows almost exponentially. **It models epidemics, technology adoption, and any resource-limited growth.**

> **Note what was required:** partial fractions from Week 2, and an exponential rearrangement. **Every
> separable equation is an integration problem wearing a different hat**, and the harder the model,
> the more of Weeks 0–2 it needs.

---

## 5. Equilibrium Solutions

**Where $\frac{dy}{dx}=0$ identically, the constant function is a solution.** For the logistic equation, $h(P)=kP(1-\frac PM)$ vanishes at

$$P=0 \qquad\text{and}\qquad P=M$$

**Both constants are solutions** — an empty population stays empty; a population at carrying capacity stays there.

> **Watch for these when separating.** Dividing by $h(y)$ implicitly assumes $h(y)\ne0$, so the
> equilibrium solutions are **lost in the division** and must be restored by hand. **They are
> genuine solutions and they are often the physically interesting ones.**

*(This is the same discipline as Week 3's "check for singularities before applying a theorem" — dividing by something that may vanish.)*

---

## 6. What To Take From This Lecture

1. **A differential equation's unknown is a function**, and solutions come in families.
2. **Check by substituting back.** The Week 0 habit, restated.
3. **General solution first, initial condition last.**
4. **Separable: $\frac{dy}{h(y)} = g(x)dx$, then integrate.**
5. **$y'=ky \implies y=Ce^{kx}$** — the most important equation in applied science.
6. **The integrals are the hard part**, and they are Weeks 0–2.
7. **Restore equilibrium solutions** lost when you divided.

---

*Next: Tuesday — First-Order Linear Equations*
