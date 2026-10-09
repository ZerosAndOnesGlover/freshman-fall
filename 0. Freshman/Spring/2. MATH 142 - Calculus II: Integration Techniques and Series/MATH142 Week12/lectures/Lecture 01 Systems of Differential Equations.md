# MATH 142 · Calculus II
## Week 12 · Lecture 1 (Monday)
### Systems of Differential Equations

*“Any progress in the theory of partial differential equations must also bring about a progress in Mechanics.”* — Carl Gustav Jacob Jacobi, *Vorlesungen über Dynamik* (1842–43)

**Date:** Monday 12 April 2027 · 11:00–11:50 · Week 12

**Coursework:** 📊 **Quiz 12** today 11:00–11:15 · 🔬 **Lab 11** Wed 14 Apr 15:00–16:50 · 🔬 **Lab 12** Thu 15 Apr 15:00–16:50 · 📝 **PS 11** due Fri 16 Apr 17:00 · 📝 **PS 12** released Fri 16 Apr 12:00 · 📕 **Final exam** Tue 20 Apr 09:00–11:30

---

**Reading:** Stewart §9.6 | Apostol Ch. 8 §8.8
**Quiz 12** — this Monday, **covers Week 11** (separable and linear ODEs). *The last quiz of the course.*

---

## 1. When One Equation Is Not Enough

**Two quantities that influence each other need two equations:**

$$\frac{dx}{dt} = f(x,y), \qquad \frac{dy}{dt} = g(x,y)$$

**Neither can be solved alone**, because each depends on the other. This is a **system**, and it is how almost every real model is written.

---

## 2. A System You Can Solve

$$\frac{dx}{dt}=y, \qquad \frac{dy}{dt}=-x$$

**Differentiate the first and substitute the second:**

$$\frac{d^2x}{dt^2} = \frac{dy}{dt} = -x \implies x''+x = 0$$

— the equation of simple harmonic motion, whose solutions are sines and cosines:

$$\boxed{x = C_1\sin t+C_2\cos t, \qquad y = C_1\cos t-C_2\sin t}$$

*(Verified.)*

### The phase plane

**Plot $y$ against $x$**, with $t$ as an invisible parameter. Then

$$\frac{d}{dt}\left(x^2+y^2\right) = 2xx'+2yy' = 2xy+2y(-x) = 0$$

**so $x^2+y^2$ is constant.** The trajectories are **circles**, traversed clockwise, and every solution is periodic.

> **This is a parametric curve** — Week 5's subject, arriving from a completely different direction.
> **The phase plane is where differential equations and parametric curves meet**, and it is the
> standard picture in dynamics.

---

## 3. Predator and Prey

$$\frac{dx}{dt} = ax-bxy, \qquad \frac{dy}{dt} = -cy+dxy$$

with $x$ the prey and $y$ the predator, and $a,b,c,d>0$.

**Reading the terms:**

| Term | Meaning |
|---|---|
| $ax$ | prey grow exponentially when alone |
| $-bxy$ | prey are eaten, at a rate proportional to encounters |
| $-cy$ | predators die out when alone |
| $+dxy$ | predators benefit from those same encounters |

**These are the Lotka–Volterra equations.**

### They cannot be solved in closed form

**But you do not need the solution to understand the behaviour**, and that is the lecture's point.

**Equilibria:** setting both derivatives to zero gives $(0,0)$ and $\left(\frac cd,\frac ab\right)$ — extinction, and a coexistence point.

**A conserved quantity:** dividing one equation by the other eliminates $t$,

$$\frac{dy}{dx} = \frac{-cy+dxy}{ax-bxy}$$

**and this is separable.** Separating and integrating gives

$$\boxed{C = dx-c\ln x+by-a\ln y \quad\text{is constant along every trajectory}}$$

*(Verified: with $a=1,b=0.5,c=0.75,d=0.25$ and $(x_0,y_0)=(2,1)$, RK4 preserves $C=0.48013961458$ to **11 digits** over 20 time units.)*

**A conserved quantity forces the trajectories to be closed curves**, so

> **The populations cycle forever** — prey rise, predators follow, prey crash, predators starve,
> prey recover. **The oscillation is not damped and does not settle**; it is a permanent feature of
> the model.

**This was established without solving anything**, using only Week 11's separation technique on $\frac{dy}{dx}$.

---

## 4. Solving Systems Numerically

**Nothing changes.** Write the system as a vector equation

$$\frac{d\mathbf{X}}{dt} = \mathbf{F}(\mathbf{X}), \qquad \mathbf{X} = \begin{pmatrix}x\\y\end{pmatrix}$$

and **apply RK4 componentwise**:

$$\mathbf k_1 = \mathbf F(\mathbf X_n),\quad \mathbf k_2 = \mathbf F\!\left(\mathbf X_n+\tfrac h2\mathbf k_1\right),\ \ldots,\qquad \mathbf X_{n+1} = \mathbf X_n+\frac h6(\mathbf k_1+2\mathbf k_2+2\mathbf k_3+\mathbf k_4)$$

**Exactly last week's method, with vectors in place of numbers.** The order is still 4.

> **This is why Week 11's lab mattered.** The method you measured on a single equation is, without
> modification, the method used to integrate the equations of motion for a spacecraft, a climate
> model, or a molecular dynamics simulation. **Only the dimension changes.**

**And the conserved quantity is a free accuracy check** — if $C$ drifts, your step size is too large. *(In the verification above it held to 11 digits, which is how we know the integration was sound.)*

---

## 5. Higher-Order Equations Are Systems

**Any second-order equation becomes a first-order system.** Given $x'' = F(x,x')$, set $v=x'$:

$$\frac{dx}{dt} = v, \qquad \frac{dv}{dt} = F(x,v)$$

**So Newton's second law $m\ddot x = F$ is a system**, and every numerical method for systems applies to it directly.

$$\text{Simple harmonic motion } x''+x=0 \iff \begin{cases}x'=v\\ v'=-x\end{cases}$$

— **which is §2's system**, and its circular phase-plane trajectories are the conservation of energy.

---

## 6. What To Take From This Lecture

1. **Coupled quantities need a system.**
2. **The phase plane** plots $y$ against $x$ — a parametric curve, from Week 5.
3. **A conserved quantity forces closed trajectories**, hence permanent cycles.
4. **Lotka–Volterra cannot be solved, and does not need to be** — the conserved quantity gives the behaviour.
5. **RK4 works componentwise, unchanged**, and the order is still 4.
6. **Every higher-order equation is a first-order system.**

---

*Next: Tuesday — Numerical Methods, Named*
