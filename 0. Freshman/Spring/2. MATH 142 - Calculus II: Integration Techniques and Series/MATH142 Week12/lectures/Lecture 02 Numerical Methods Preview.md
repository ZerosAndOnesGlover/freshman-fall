# MATH 142 · Calculus II
## Week 12 · Lecture 2 (Tuesday)
### Numerical Methods, Named

---

**Reading:** none — this lecture is a retrospective
**Lab 12** is a self-diagnostic under exam conditions. **Do it before you revise, not after.**

---

## 1. You Have Been Doing Numerical Analysis All Term

**Nobody told you, because the names would not have meant anything in Week 0.** They do now.

| What you did | Its name | Where |
|---|---|---|
| Trapezoid, midpoint, Simpson | **Numerical quadrature** | Lab 0 |
| The Babylonian $\sqrt2$ iteration | **Newton's method** | Lab 6 |
| Euler, improved Euler, RK4 | **ODE integrators** | Lab 11 |
| Taylor polynomials with remainder bounds | **Function approximation** | Lab 10 |
| Averaging consecutive partial sums | **Series acceleration** | Labs 7, 8 |
| Error ratios on halving $h$ | **Order of convergence** | *every lab* |

**This lecture names them and shows the two ideas that hold them together.**

---

## 2. The Coincidence You Did Not Notice

**Lab 6, Week 6.** The Babylonian iteration, attributed to a clay tablet around 1700 BC:

$$a_{n+1} = \frac12\left(a_n+\frac{2}{a_n}\right)$$

**Newton's method** for solving $f(x)=0$, the standard modern root-finder:

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

**Apply it to $f(x)=x^2-2$:**

$$x - \frac{x^2-2}{2x} = \frac{2x^2-x^2+2}{2x} = \frac{x^2+2}{2x} = \frac{x}{2}+\frac{1}{x}$$

$$\boxed{\text{They are the same formula.}}$$

*(Verified symbolically: both reduce to $\tfrac x2+\tfrac1x$.)*

> **The oldest algorithm in mathematics and the one in every numerical library are identical.** You
> measured its convergence in Week 6 — errors squaring each step, $48$ correct digits in six
> iterations — without knowing what you were measuring.

---

## 3. Order of Convergence, One Last Time

**For an iteration, "order $p$" means $e_{n+1}\approx Ce_n^{\,p}$** — a different definition from the $\text{error}\approx Ch^p$ of the quadrature and ODE labs, but the same word, and for the same reason: **$p$ decides everything.**

**Measure it by $\dfrac{\ln e_n}{\ln e_{n-1}}$**, which tends to $p$.

| Method | measured exponent | $p$ |
|---|---|---|
| **Bisection** | — (see below) | 1 |
| **Secant** | $1.691,\ 1.680,\ 1.645,\ 1.629,\ \mathbf{1.625}$ | $\frac{1+\sqrt5}{2}\approx1.618$ |
| **Newton** | $2.447,\ 2.173,\ 2.080,\ 2.038,\ \mathbf{2.019}$ | $2$ |

*(All measured on $x^2-2$ from the same starting data.)*

**The secant method's order is the golden ratio.** It is not a numerical coincidence: the error exponents satisfy $p_{n+1}=p_n+1$ in the limit, which is the Fibonacci recursion.

### A warning about bisection

**Bisection halves the *interval* every step, so the error bound halves.** The *actual* error does not:

| step | midpoint | actual error |
|---:|---|---|
| 1 | $1.5$ | $8.58\times10^{-2}$ |
| 2 | $1.25$ | $1.64\times10^{-1}$ |
| 3 | $1.375$ | $3.92\times10^{-2}$ |
| 4 | $1.4375$ | $2.33\times10^{-2}$ |
| 7 | $1.4140625$ | $1.51\times10^{-4}$ |
| 8 | $1.41796875$ | $3.76\times10^{-3}$ |

*(Measured.)* **Step 2 is worse than step 1, and step 8 is twenty-five times worse than step 7.**

> **The guarantee is on the bound, not on the iterate.** Bisection never fails and never surprises
> you — but it also never accelerates, and reading its error table as though it were Newton's will
> mislead you. **Know which quantity your theorem controls.**

---

## 4. The Idea This Course Could Not Show You: Stability

**Everything above concerns how fast a method converges in exact arithmetic. Real machines do not have exact arithmetic**, and that introduces a second failure mode with no analogue in anything you have proved.

```
>>> 0.1 + 0.2
0.30000000000000004
```

**This is not a bug.** Binary floating point cannot represent $0.1$, any more than decimal can represent $\tfrac13$.

### Catastrophic cancellation

**Subtracting two nearly equal numbers destroys accuracy**, because the leading digits agree and cancel, leaving only the noise beneath them.

**Compute $\dfrac{1-\cos x}{x^2}$**, whose limit is $\tfrac12$ (Week 0's L'Hôpital, or the Maclaurin series of Week 10):

| $x$ | $\dfrac{1-\cos x}{x^2}$ | $\dfrac{2\sin^2(x/2)}{x^2}$ |
|---|---|---|
| $10^{-5}$ | $0.5000000413701854$ | $0.4999999999958333$ |
| $10^{-6}$ | $0.5000444502911705$ | $0.4999999999999583$ |
| $10^{-7}$ | $0.4996003610813205$ | $0.4999999999999996$ |
| $10^{-8}$ | $\mathbf{0.0}$ | $\mathbf{0.5}$ |

*(Measured in double precision.)*

**The two columns are the same function**, by the identity $1-\cos x = 2\sin^2(x/2)$. **One returns $0$; the other is correct to 16 digits.**

### It is not a contrived example

**Solve $x^2-10^8x+1=0$ for the smaller root**, using the formula every student knows:

$$x = \frac{b-\sqrt{b^2-4}}{2} \qquad\text{gives}\qquad 7.450580596923828\times10^{-9}$$

**The true root is $1.0000000000000001\times10^{-8}$.** *(Verified at 40 digits.)*

$$\textbf{Relative error: }\ \mathbf{25\%.}$$

**Rationalising the numerator gives the algebraically identical formula**

$$x = \frac{2}{b+\sqrt{b^2-4}} \qquad\text{which returns}\qquad 1.0000000000000000\times10^{-8}$$

> **The same formula, rearranged, moves from two correct digits to sixteen.** Nothing about the
> mathematics changed — only the order of operations. **This is the subject of numerical analysis,
> and it is invisible to everything in this course**, because every theorem you proved assumed exact
> arithmetic.

**You saw one shadow of it in Week 7**, when `mpmath.nsum` returned $0.9367$ for a series whose true value is $0.9375$ — a library, at high precision, returning four wrong digits with no warning. **You caught it because a partial sum of positive terms exceeded the reported total.**

---

## 5. The Two Rules That Survived Twelve Weeks

**Rule 1 — the order of convergence decides the practical question.**

**Rule 2 — the CAS is a check, not an oracle.**

**Every week produced an instance of Rule 2**, and they were not obscure: an unevaluated integral, an `nsum` off in the fourth digit, a `dsolve` that raised an exception, a quadratic formula wrong by 25%. **The failures were caught by cheap independent checks** — a sign, a bound, a monotonicity argument, a partial sum, a refinement — **never by staring harder at the output.**

---

## 6. Where These Go

| Thread | Continues in |
|---|---|
| Quadrature, root-finding, stability | numerical analysis |
| ODE integrators, systems | differential equations, dynamics, simulation |
| Series, convergence, uniform convergence | real analysis |
| Fourier orthogonality *(Week 1)* | signals, PDEs |
| Floating point, error propagation | computer architecture, scientific computing |

**Tomorrow's lecture follows each thread by name.**

---

## 7. What To Take From This Lecture

1. **The Babylonian iteration is Newton's method** — verified, not asserted.
2. **Order of convergence for iterations means $e_{n+1}\approx Ce_n^p$**; measure it by $\ln e_n/\ln e_{n-1}$.
3. **Bisection's guarantee is on the bound, not the iterate.**
4. **Catastrophic cancellation can destroy an algebraically exact formula**, and rearranging it can restore full accuracy.
5. **Every theorem in this course assumed exact arithmetic.** Real computation has a second failure mode.
6. **Rule 1: order decides. Rule 2: the CAS is a check, not an oracle.**

---

*Next: Wednesday — The Road Ahead*
