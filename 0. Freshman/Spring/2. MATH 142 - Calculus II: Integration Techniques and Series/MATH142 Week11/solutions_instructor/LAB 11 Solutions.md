# MATH 142 · Calculus II
## Lab 11 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures produced by running the lab.

---

## Part A — Slope Fields (15 pts)

### A1 (9)

Slope field of $y'=y-x$: at each grid point draw a segment of slope $y-x$.

**The three solution curves** through $(0,2)$, $(0,1)$, $(0,0)$ are $y=e^x+x+1$, $y=x+1$, $y=-e^x+x+1$ respectively.

*Marking: 9 — 5 for a correct field, 4 for three plausible curves following it.*

### A2 (6)

**(a)** The curve through $(0,2)$ matches $y=e^x+x+1$: check $y'=e^x+1$ and $y-x = e^x+1$ ✓

**(b)** **The initial condition $y(0)=1$ gives the straight line $y=x+1$.**

**Why the slope field makes it obvious:** along the line $y=x+1$ we have $y-x=1$ everywhere, so **every segment of the field on that line has slope exactly 1** — which is the line's own slope. **The line follows its own field.**

*(Verified: $y=x+1$ gives $y'=1$ and $y-x=1$ identically.)*

*Marking: 2 + 4. **(b) must explain via the constant slope along the line**, not merely name the solution.*

---

## Part B — Euler's Method (30 pts)

Exact: $y(1) = e+2 = 4.71828182845905$

### B1 (12), B2 (10)

| $n$ | $y_n(1)$ | error | ratio |
|---:|---|---|---|
| $10$ | $4.5937424601$ | $1.24539\times10^{-1}$ | — |
| $20$ | $4.65329770514$ | $6.49841\times10^{-2}$ | $1.917$ |
| $40$ | $4.68506383839$ | $3.32180\times10^{-2}$ | $1.956$ |
| $80$ | $4.70148494075$ | $1.67969\times10^{-2}$ | $1.978$ |
| $160$ | $4.70983557631$ | $8.44625\times10^{-3}$ | $1.989$ |
| $320$ | $4.71404664371$ | $4.23518\times10^{-3}$ | $1.994$ |

*(Verified.)*

**B2(a)** The ratio $\to\mathbf{2}$.

**B2(b)** $2^p=2$ gives $p=1$: **Euler's method is first order.**

*Marking B1: 12. B2: 5 + 5. **The order must be derived from the ratio**, as in every previous lab.*

### B3 (8)

Error $\approx Ch$ with $C\approx\frac{4.235\times10^{-3}}{1/320} = 1.355$.

For error $<10^{-10}$: $h<7.38\times10^{-11}$, so

$$\boxed{n > 1.36\times10^{10}\ \text{steps}}$$

**Not practical.** Thirteen billion steps for ten digits, and accumulated floating-point rounding would dominate long before that.

*Marking: 5 estimate, 3 judgement. **Accept anything of order $10^{10}$.***

---

## Part C — Two Better Methods (35 pts)

### C1 (12) — improved Euler (RK2)

| $n$ | $y_n(1)$ | error | ratio |
|---:|---|---|---|
| $10$ | $4.71408084661$ | $4.20098\times10^{-3}$ | — |
| $20$ | $4.71719105435$ | $1.09077\times10^{-3}$ | $3.851$ |
| $40$ | $4.71800394437$ | $2.77884\times10^{-4}$ | $3.925$ |
| $80$ | $4.71821170110$ | $7.01274\times10^{-5}$ | $3.963$ |
| $160$ | $4.71826421412$ | $1.76143\times10^{-5}$ | $3.981$ |
| $320$ | $4.71827741453$ | $4.41393\times10^{-6}$ | $3.991$ |

**Ratio $\to4$, so order 2.** *(Verified.)*

### C2 (13) — RK4

| $n$ | $y_n(1)$ | error | ratio |
|---:|---|---|---|
| $10$ | $4.71827974414$ | $2.08432\times10^{-6}$ | — |
| $20$ | $4.71828169266$ | $1.35803\times10^{-7}$ | $15.35$ |
| $40$ | $4.71828181979$ | $8.66619\times10^{-9}$ | $15.67$ |
| $80$ | $4.71828182791$ | $5.47306\times10^{-10}$ | $15.83$ |
| $160$ | $4.71828182842$ | $3.43852\times10^{-11}$ | $15.92$ |
| $320$ | $4.71828182846$ | $2.15468\times10^{-12}$ | $15.96$ |

**Ratio $\to16$, so order 4.** *(Verified.)*

### C3 (10)

| method | error at $n=320$ | order | $f$-evals/step |
|---|---|---|---|
| Euler | $4.24\times10^{-3}$ | 1 | 1 |
| Improved Euler | $4.41\times10^{-6}$ | 2 | 2 |
| **RK4** | $2.15\times10^{-12}$ | 4 | 4 |

**(a)** RK4 beats Euler by a factor of $\dfrac{4.24\times10^{-3}}{2.15\times10^{-12}} \approx \boxed{2\times10^{9}}$.

**(b)** **Overwhelmingly.** RK4 costs **four times** the work per step and buys a factor of **two billion** in accuracy. Equivalently: to match RK4's accuracy at $n=320$, Euler would need about $1.4\times10^{12}$ steps — so at equal accuracy RK4 is cheaper by roughly nine orders of magnitude.

**(c)** **The ratio 16 is Simpson's rule's ratio, from Lab 0 in Week 0.** Both methods are fourth order: halving the step multiplies the error by $\left(\frac12\right)^4=\frac1{16}$.

*Marking: 4 table, 2 + 2 + **2 for recognising Lab 0.** The last is the point of the whole lab.*

---

## Part D — No Solution Formula (20 pts)

### D1 (6)

**Not separable:** $x^2+y^2$ is a **sum**, and cannot be factored as $g(x)h(y)$.
**Not linear:** $y$ occurs squared, so it is not of the form $y'+P(x)y=Q(x)$.

**`sympy.dsolve` fails**, raising an exception rather than returning a solution. *(Verified.)*

*Marking: 2 + 2 + 2. **Reporting what the CAS actually does is required** — as with the unevaluated integrals of Weeks 0–5, a failure is a report, not a bug.*

### D2 (8)

RK4 from $y(0)=0$ to $x=1$:

| $n$ | $y(1)$ |
|---|---|
| $10$ | $0.350233741831$ |
| $100$ | $0.350231844534$ |
| $1000$ | $0.350231844317$ |

**The last two agree to 9 significant figures**, so

$$\boxed{y(1) = 0.350231844}$$

*(Verified.)*

*Marking: 4 table, **4 for justifying the digit count from the agreement between refinements** — the standard practical convergence check.*

### D3 (6)

**The same:** a well-posed problem with a definite answer that has **no elementary formula**. In both cases the response is to compute rather than to solve symbolically, and in both cases the computation is easy while the formula does not exist.

**The difference:** in **Week 10** the integral $\int e^{-x^2}dx$ acquired a **power series** — giving a fast method *and* a rigorous a priori error bound from the alternating estimate.

**Here there is no such rescue in general.** A series solution can sometimes be constructed, but for a nonlinear equation like this one the recurrence is not linear and the analysis is far harder. **The honest answer is the numerical one, with its accuracy justified by refinement rather than by a theorem.**

*Marking: 3 for the parallel, 3 for the distinction. **Full marks require noting that the series rescue is not guaranteed here.** A student who says only "both need numerics" earns 3.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 15 |
| B | 30 |
| C | 35 |
| D | 20 |
| **Total** | **100** |

---

## Checkoff Checklist

1. A2(b) explains the straight line via **constant slope along it**
2. **B2 gives order 1 from the ratio 2**
3. B3's estimate is of order $10^{10}$
4. C1 gives order 2; C2 gives order 4
5. **C3(c) identifies Lab 0's Simpson's rule**
6. D1 reports what `dsolve` actually does
7. **D2 justifies the digit count from successive refinement**
8. D3 notes the series rescue is not guaranteed

---

## Note for the Debrief

**This is the last lab with a measurement in it.** Close the arc.

> **Eleven labs, and eleven times you have computed a ratio of consecutive errors.**
>
> **Lab 0, Week 0:** Simpson's rule, ratio 16, order 4.
> **Lab 11, today:** Runge–Kutta 4, ratio 16, order 4.
>
> Between them: Wallis at order 1 and useless; the $p$-test boundary that no computation could find;
> a harmonic series needing $10^{43}$ terms; a numerical library returning twelve wrong digits;
> Taylor series delivering ten digits from thirteen numbers with a bound proved in advance.

Then the point:

> **One number has decided every practical question in this course, and it is the order of
> convergence.** Not cleverness, not elegance — the exponent $p$ in $\text{error}\approx Ch^p$.
>
> **Euler and RK4 solve the same equation with the same arithmetic.** RK4 does four times the work per
> step and wins by a factor of two billion. **That is what $p=4$ against $p=1$ means**, and you have
> now measured it on quadrature, on infinite products, on series, on iterations, and on differential
> equations.

Then close:

> Next week we finish: systems, a look at the numerical methods you will meet properly in MATH 341, and the final review. **The final is comprehensive — Week 0's Riemann sums to today's
> Runge–Kutta.**

---

*MATH 142 · Week 11 · Lab 11 Solutions · Instructor Only*
