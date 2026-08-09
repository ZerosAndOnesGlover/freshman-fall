# MATH 142 · Calculus II
## Week 12 · Reference Sheet
### Systems; Numerical Methods

---

## Systems of Differential Equations

$$\frac{dx}{dt}=f(x,y), \qquad \frac{dy}{dt}=g(x,y)$$

**Neither equation can be solved alone.**

### The phase plane

**Plot $y$ against $x$, with $t$ invisible** — a parametric curve, which is Week 5's object.

| trajectories | meaning |
|---|---|
| **closed curves** | every solution is periodic |
| spiralling in | equilibrium is attracting |
| spiralling out | equilibrium is repelling |

### Solvable example

$$x'=y,\quad y'=-x \implies x''+x=0 \implies x=C_1\sin t+C_2\cos t,\quad y=C_1\cos t-C_2\sin t$$

*(Verified.)* **$\frac{d}{dt}(x^2+y^2)=2xy+2y(-x)=0$**, so the trajectories are **circles**.

### Conserved quantities

> **Find a quantity whose $t$-derivative vanishes, and you have the trajectories without solving
> anything.**

**Method:** differentiate the candidate, substitute the system, simplify to $0$.

**A conserved quantity $\Rightarrow$ trajectories lie on its level curves. If those are closed, every solution is periodic.**

### Lotka–Volterra

$$x'=ax-bxy, \qquad y'=-cy+dxy$$

| Term | Meaning |
|---|---|
| $ax$ | prey grow alone |
| $-bxy$ | prey eaten at the encounter rate |
| $-cy$ | predators die alone |
| $+dxy$ | predators gain from encounters |

**Equilibria:** $(0,0)$ and $\left(\dfrac cd,\dfrac ab\right)$.

**No closed-form solution exists.** But eliminating $t$ via $\dfrac{dy}{dx}$ gives a **separable** equation, and integrating it yields

$$\boxed{C = dx-c\ln x+by-a\ln y \quad\text{constant along every trajectory}}$$

*(Verified: $a=1,b=0.5,c=0.75,d=0.25$ from $(2,1)$ — RK4 holds $C=0.48013961458$ to **11 digits** over 20 time units.)*

**Hence the populations cycle forever**, undamped.

### Numerics for systems

**RK4 componentwise, unchanged:**

$$\mathbf X_{n+1}=\mathbf X_n+\frac h6(\mathbf k_1+2\mathbf k_2+2\mathbf k_3+\mathbf k_4)$$

**Still order 4.** **A conserved quantity is a free accuracy check** — if it drifts, $h$ is too large.

### Higher order $\Rightarrow$ system

$$x''=F(x,x') \iff \begin{cases}x'=v\\ v'=F(x,v)\end{cases}$$

---

## Order of Convergence

**Two definitions, one word.**

| setting | meaning | measure by |
|---|---|---|
| **step methods** ($h\to0$) | $\text{err}\approx Ch^p$ | ratio of errors on halving $h$: $\to2^p$ |
| **iterations** ($n\to\infty$) | $e_{n+1}\approx Ce_n^{\,p}$ | $\dfrac{\ln e_n}{\ln e_{n-1}}\to p$ |

### Everything measured this term

| method | ratio / exponent | $p$ | lab |
|---|---|---|---|
| Wallis product | — | 1 | 1 |
| Basel partial sums | — | 1 | 7 |
| Euler's method | $\to2$ | 1 | 11 |
| Trapezoid, midpoint | $\to4$ | 2 | 0 |
| Improved Euler (RK2) | $\to4$ | 2 | 11 |
| **Simpson's rule** | $\to\mathbf{16}$ | **4** | 0 |
| **RK4** | $\to\mathbf{16}$ | **4** | 11 |
| Bisection | — | 1 | — |
| Secant | $\to1.625$ | $\frac{1+\sqrt5}{2}$ | — |
| **Newton / Babylonian** | $\to2.019$ | **2** | 6 |

*(All measured.)*

> **Two data points never establish an order.** *(Lab 12: the pair $n=8,16$ on Simpson gives a ratio
> of $37874$, which is the method entering its asymptotic regime, not order 15.)* **Look for a run of
> stable ratios.**

### Bisection's warning

**Bisection halves the *interval*, so the error *bound* halves. The actual error does not** — step 2 can be worse than step 1. **Know which quantity your theorem controls.**

---

## Newton's Method

$$x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)} \qquad\text{— quadratic: the number of correct digits doubles}$$

**On $f(x)=x^2-2$ this is $x_{n+1}=\frac{x_n}{2}+\frac1{x_n}$ — the Babylonian iteration of Lab 6.** *(Verified: algebraically identical.)*

| step | correct digits |
|---:|---|
| 3 | 5 |
| 4 | 11 |
| 5 | 24 |
| 6 | 48 |

---

## Floating Point — What The Theorems Assumed Away

**Every convergence proof in this course assumed exact arithmetic. Machines do not have it.**

```
>>> 0.1 + 0.2
0.30000000000000004
```

### Catastrophic cancellation

**Subtracting nearly equal numbers cancels the leading digits and leaves the noise.**

| computed | at $x=10^{-8}$ |
|---|---|
| $\dfrac{1-\cos x}{x^2}$ | $\mathbf{0.0}$ |
| $\dfrac{2\sin^2(x/2)}{x^2}$ | $\mathbf{0.5}$ |

*(Measured; the two expressions are identical.)*

**Smaller root of $x^2-10^8x+1=0$:**

| formula | value | rel. error |
|---|---|---|
| $\dfrac{b-\sqrt{b^2-4}}{2}$ | $7.4506\times10^{-9}$ | **25%** |
| $\dfrac{2}{b+\sqrt{b^2-4}}$ | $1.0000\times10^{-8}$ | $0$ |

*(Verified against 40 digits.)*

### It reaches convergent series too

$$\int_0^Te^{-x^2}dx=\sum_{k\ge0}\frac{(-1)^kT^{2k+1}}{k!(2k+1)} \qquad (R=\infty)$$

| $T$ | double-precision error | largest term |
|---|---|---|
| $1$ | $0$ | $1$ |
| $4$ | $4.9\times10^{-12}$ | $1.1\times10^{5}$ |
| $6$ | $\mathbf{7.0\times10^{-4}}$ | $\mathbf{2.4\times10^{13}}$ |

*(Measured.)* **The series converges for every $T$ and still returns three correct digits at $T=6$** — and **two orderings of the same terms disagree in the second decimal place.**

> **Convergence is a statement about exact arithmetic.**
> **Simpson on $[0,6]$ with $n=256$ plus a proved tail bound gives $\sqrt\pi/2$ to $8.9\times10^{-16}$.**

---

## Where It Goes

| This course | Next |
|---|---|
| Improper integrals, $\int_0^\infty e^{-x^2}dx=\frac{\sqrt\pi}2$ | **MATH 251** — Probability & Statistics |
| Orthogonality of $\sin nx$ *(Week 1)* | **ECE 210** — Signals and Systems |
| Systems, phase plane, eigenvalues $\pm i$ | **MATH 241** — Linear Algebra |
| Floating point | **CS 201** — Computer Organization |
| Convergence proofs | real analysis |
| Quadrature, RK4, orders | numerical analysis |

---

## The Two Rules

1. **The order of convergence decides the practical question.**
2. **The CAS is a check, not an oracle.**

---

*MATH 142 · Week 12 · Reference Sheet*
