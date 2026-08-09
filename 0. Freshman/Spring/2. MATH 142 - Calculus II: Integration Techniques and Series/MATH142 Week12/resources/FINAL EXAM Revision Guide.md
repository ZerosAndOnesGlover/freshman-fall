# MATH 142 · Calculus II
## Final Exam · Revision Guide
### Covering Weeks 0–12

---

## The Exam

| | |
|---|---|
| **When** | end of Week 12 |
| **Duration** | **150 minutes** |
| **Covers** | **Weeks 0–12 — comprehensive** |
| **Weight** | **20%** of the course |
| **Total** | 150 points |
| **Allowed** | **A two-page handwritten cheat sheet** — one sheet used on both sides, or two sheets used on one side each. No calculator. |

**Weighting.** The exam is spread across the term but **not uniformly**. Weeks 6–10 — sequences, series, convergence tests, power series, Taylor — carry roughly **half the paper**, because that is the half of the course that is new, hard, and load-bearing for what comes next. **Week 12 appears only lightly.**

**Character.** Midterm 1 was computational; Midterm 2 was about justification. **The final is both**, and it adds a third thing: **questions that ask you to choose the method**, with no chapter heading to tell you which one.

---

## Topic Checklist

Tick only what you could do **from a blank page, under time.**

### Week 0 — Foundations
- [ ] FTC **with the chain rule** on variable limits
- [ ] $u$-substitution, including definite limits
- [ ] Riemann sums; trapezoid, midpoint, Simpson **and their orders (2, 2, 4)**

### Week 1 — Parts and trig integrals
- [ ] Integration by parts; **LIATE**; parts twice; the "solve for $I$" trick
- [ ] Reduction formulas
- [ ] $\sin^m\cos^n$: **odd power $\Rightarrow$ $u$-sub; both even $\Rightarrow$ half-angle**
- [ ] $\tan^m\sec^n$
- [ ] **Orthogonality** $\int_{-\pi}^{\pi}\sin mx\sin kx\,dx$

### Week 2 — Substitution and partial fractions
- [ ] The three trig substitutions and **back-substitution via the triangle**
- [ ] Completing the square first
- [ ] Partial fractions: all four denominator cases
- [ ] **Divide first if the degree is not smaller**

### Week 3 — Improper integrals
- [ ] **Limit definition** — every improper integral is a limit, always written
- [ ] Discontinuities **inside** the interval; splitting at them
- [ ] $\int_1^\infty x^{-p}$ vs $\int_0^1 x^{-p}$ — **opposite conditions**
- [ ] Direct and limit comparison

### Week 4 — Applications
- [ ] Area between curves; **integrating in $y$** when it is easier
- [ ] Discs, washers, shells — **and choosing between them**
- [ ] **Radii measured from the axis of rotation**, not from zero
- [ ] Arc length; surface area

### Week 5 — Parametric and polar
- [ ] $\frac{dy}{dx}=\frac{dy/dt}{dx/dt}$; second derivatives
- [ ] Parametric arc length and area
- [ ] $A=\frac12\int r^2d\theta$; $L=\int\sqrt{r^2+(r')^2}d\theta$
- [ ] **The range of $\theta$ that traces the curve exactly once**

### Week 6 — Sequences
- [ ] Limit techniques; **growth hierarchy** $\ln n\ll n^p\ll a^n\ll n!\ll n^n$
- [ ] Monotone Convergence Theorem
- [ ] Recursions: **prove convergence, then** solve $L=g(L)$

### Week 7 — Series, first tests
- [ ] Partial sums; geometric; telescoping
- [ ] **$n$-th Term Test proves divergence only**
- [ ] Integral Test — **three hypotheses** — and its remainder bound
- [ ] $p$-series; direct and limit comparison

### Week 8 — Signs
- [ ] AST — **two hypotheses**; $|R_N|\le b_{N+1}$
- [ ] Absolute vs conditional
- [ ] Ratio and Root; **$L=1$ is silence**

### Week 9 — Power series
- [ ] Radius; **both endpoints tested separately**
- [ ] Term-by-term differentiation and integration
- [ ] The library: $\frac1{1-x}$, $e^x$, $\sin$, $\cos$, $\ln(1+x)$, $\arctan x$

### Week 10 — Taylor series
- [ ] Taylor/Maclaurin coefficients; building new series by substitution
- [ ] **Lagrange remainder** and the alternating estimate
- [ ] Series for limits, for non-elementary integrals, for binomials
- [ ] **Smooth $\ne$ analytic:** $e^{-1/x^2}$

### Week 11 — Differential equations
- [ ] Separable; **restore lost equilibrium solutions**
- [ ] Linear: **standard form first**, then $\mu=e^{\int P}$
- [ ] The standard models; equilibria and stability **without solving**

### Week 12 — Systems *(light)*
- [ ] Phase plane; conserved quantity $\Rightarrow$ closed trajectories
- [ ] Higher-order equation $\Rightarrow$ first-order system

---

## The Ten Errors That Cost The Most Marks

**Every one of these appeared on a problem set, quiz, or midterm this term.**

1. **Dropping the chain rule** in FTC problems. *Check: differentiate your answer back.*
2. **Not writing the limit** on an improper integral, or missing an interior discontinuity.
3. **Radii measured from the origin** instead of from the axis of rotation. *(PS 4 A4.)*
4. **Integrating a polar curve over $[0,2\pi]$** when it is traced on a shorter interval. *(Doubles the area.)*
5. **Solving $L=g(L)$ before proving the limit exists.**
6. **Concluding convergence from $a_n\to0$.**
7. **Applying the Integral Test without checking its three hypotheses.**
8. **Giving a radius of convergence and stopping.** *Endpoints are half the marks.*
9. **Estimating with a series and not bounding the error.** *A number without a bound is not an answer.*
10. **Reading $P(x)$ off an equation not in standard form.**

> **Six of the ten are failures to check something you already knew to check.** That is the single
> largest source of lost marks in this course, and it is entirely recoverable in the last week.

---

## The Method-Choice Table

**The final does not tell you which chapter a problem came from.** This is the decision procedure.

### An integral

| Sign | Try |
|---|---|
| an inside function whose derivative is present | $u$-substitution |
| a product of unlike things | parts |
| powers of $\sin,\cos,\tan,\sec$ | trig-integral patterns |
| $\sqrt{a^2\pm x^2}$, $\sqrt{x^2-a^2}$ | trig substitution |
| a factorable rational function | partial fractions |
| a quadratic under a root | complete the square, then trig sub |
| infinite limit or an unbounded integrand | **improper — write the limit** |
| none of the above | **series**, or numerics |

### A series

1. **$a_n\not\to0$?** Diverges. Stop.
2. **Geometric or telescoping?** Sum it exactly.
3. **Positive terms?** $p$-series → comparison → Integral Test → Ratio/Root.
4. **Alternating?** AST for convergence, then test $\sum|a_n|$ for absolute.
5. **Factorials or $n$-th powers?** Ratio, or Root.
6. **$L=1$?** The test said nothing. Choose another.

### A differential equation

$y'=f(x)$ → integrate. $y'=g(x)h(y)$ → separable. $y'+P y=Q$ → integrating factor. **Neither → series or numerics.**

---

## Building Your Two Pages

**You get two handwritten pages** — twice the midterms' allowance for thirteen weeks of material. **It is not enough to copy everything, and that is the point.** A page you transcribed is a page you cannot navigate under time.

**Suggested allocation:**

| Page | Contents |
|---|---|
| **1** | **Integration and applications.** The method-choice table above; the three trig substitutions with their triangles; the four partial-fraction cases; the $p$-tests for both kinds of improper integral; volume, arc-length and surface formulas; the parametric and polar formulas. |
| **2** | **Series and differential equations.** The full test list **with hypotheses**; $p$-series and geometric facts; the growth hierarchy; the three remainder bounds; the series library; separable and integrating-factor recipes. **Reserve the last quarter for the five things you personally keep getting wrong.** |

> **Write it yourself, by hand, from the reference sheets.** The writing is the revision; the page is
> a by-product. **That last quarter of page 2 is the highest-value square inch on the whole exam**,
> and Lab 12's Part C exists to tell you what belongs in it.

---

## The Recurring Theme, In Case It Is Examined

**One question may ask you to comment rather than compute.** The two things to be able to say:

**1. Order of convergence decides the practical question.** Measured this term: Wallis and Euler at order 1 *(useless — $8\times10^9$ factors, $1.4\times10^{10}$ steps)*; trapezoid and midpoint at 2; **Simpson and RK4 at 4** *(128 points, 320 steps)*; **Newton quadratic** *(48 digits in six steps)*.

**2. The CAS is a check, not an oracle.** Documented failures: unevaluated integrals; `nsum` returning $0.9367$ for $0.9375$; `dsolve` raising an exception; the naive quadratic formula wrong by 25%; a convergent series returning three correct digits at $T=6$.

---

---

# Sample Paper

**150 minutes. 150 points. Two handwritten pages. No calculator.**

---

**Q1 (20 pts) — Integration techniques.** Evaluate:

**(a)** $\displaystyle\int x\arctan x\,dx$
**(b)** $\displaystyle\int_0^{\pi/2}\cos^5x\,dx$
**(c)** $\displaystyle\int\frac{dx}{(x^2+9)^{3/2}}$
**(d)** $\displaystyle\int\frac{3x+11}{(x-3)(x+2)}\,dx$

---

**Q2 (16 pts) — Improper integrals.**

**(a)** $\displaystyle\int_0^1\frac{\ln x}{\sqrt x}\,dx$
**(b)** $\displaystyle\int_1^\infty\frac{dx}{x\sqrt{x^2+1}}$
**(c)** Show that $\displaystyle\int_1^\infty\frac{2+\sin x}{x^2}\,dx$ **converges, without evaluating it.**

---

**Q3 (20 pts) — Applications.** Let $R$ be the region under $y=\sqrt x$ from $x=0$ to $x=4$.

**(a)** Volume when $R$ is rotated about the **$x$-axis**.
**(b)** Volume when $R$ is rotated about the **$y$-axis**.
**(c)** Arc length of $y=\dfrac{x^2}{2}-\dfrac{\ln x}{4}$ on $[1,2]$.

---

**Q4 (18 pts) — Parametric and polar.**

**(a)** Arc length of $x=e^t\cos t,\ y=e^t\sin t$ for $0\le t\le\pi$.
**(b)** Area inside $r=1+\cos\theta$ and **outside** $r=1$.

---

**Q5 (24 pts) — Convergence.** Determine convergence or divergence, **naming the test and verifying its hypotheses.** For alternating series, state absolute or conditional.

**(a)** $\displaystyle\sum_{n=1}^\infty\frac{n}{2n+1}$
**(b)** $\displaystyle\sum_{n=1}^\infty\frac{1}{n^2+n}$
**(c)** $\displaystyle\sum_{n=2}^\infty\frac{\ln n}{n}$
**(d)** $\displaystyle\sum_{n=1}^\infty\frac{n!}{n^n}$
**(e)** $\displaystyle\sum_{n=1}^\infty\frac{(-1)^n}{\ln(n+1)}$
**(f)** $\displaystyle\sum_{n=1}^\infty\frac{(2n)!}{(n!)^2\,5^n}$

---

**Q6 (18 pts) — Power series.** Find the interval of convergence of

$$\sum_{n=1}^\infty\frac{n(x+2)^n}{5^n}$$

**with both endpoints decided.**

---

**Q7 (20 pts) — Taylor series.**

**(a)** Estimate $\ln(1.2)$ using four terms of the Maclaurin series for $\ln(1+x)$, **and bound the error before comparing with anything.**
**(b)** Evaluate $\displaystyle\lim_{x\to0}\frac{e^x-1-x-\frac{x^2}{2}}{x^3}$ **using series.**
**(c)** State, with the standard counterexample, why a function's Taylor series need not converge to the function.

---

**Q8 (14 pts) — Differential equations.** Solve

$$\frac{dy}{dx}+y\tan x=\sin 2x,\qquad y(0)=1$$

**and verify your answer by substitution.**

---

---

# Sample Paper — Answers

---

**Q1 (20).**

**(a)** Parts with $u=\arctan x$: $\boxed{\dfrac{x^2\arctan x}{2}-\dfrac{x}{2}+\dfrac{\arctan x}{2}+C}$
**(b)** Odd power: $u=\sin x$, $\displaystyle\int_0^1(1-u^2)^2du=\boxed{\dfrac{8}{15}}$
**(c)** $x=3\tan\theta$: $\boxed{\dfrac{x}{9\sqrt{x^2+9}}+C}$
**(d)** $\dfrac{4}{x-3}-\dfrac{1}{x+2}$, so $\boxed{4\ln|x-3|-\ln|x+2|+C}$

*(All verified.)*

**Q2 (16).**

**(a)** Improper at $0$. $\displaystyle\lim_{a\to0^+}\int_a^1x^{-1/2}\ln x\,dx = \lim_{a\to0^+}\left[2\sqrt x\ln x-4\sqrt x\right]_a^1 = \boxed{-4}$ *(Verified to 14 digits.)*
**The limit must be written.** $\sqrt a\ln a\to0$ needs a word of justification.

**(b)** $x=\tan\theta$, or $u=1/x$: $\boxed{\ln(1+\sqrt2)}\approx0.881374$ *(Verified.)*

**(c)** $0<\dfrac{2+\sin x}{x^2}\le\dfrac{3}{x^2}$ on $[1,\infty)$, and $\displaystyle\int_1^\infty\frac{3\,dx}{x^2}=3<\infty$. **Direct comparison — converges.**

> **A note worth reading.** The exact value is $2+\sin1-\text{Ci}(1)=2.504067061906928$.
> **Two independent computations of this integral returned two different wrong answers:** a symbolic
> CAS reported $2.50000000000$ *(wrong by $4\times10^{-3}$, printed to twelve digits)*, and a
> general-purpose numerical quadrature routine returned $2.5030124781$ *(wrong by $1\times10^{-3}$)*.
> **Both were caught by an oscillation-aware method and a closed form that agree to twenty digits.**
> **The question asks you to prove convergence by comparison — a three-line argument that neither
> machine could have got wrong.**

**Q3 (20).**

**(a)** Discs: $\displaystyle\pi\int_0^4x\,dx=\boxed{8\pi}$
**(b)** Shells: $\displaystyle2\pi\int_0^4x\sqrt x\,dx=\boxed{\dfrac{128\pi}{5}}$
**(c)** $1+(y')^2$ is a perfect square: $\displaystyle\int_1^2\left(x+\frac{1}{4x}\right)dx=\boxed{\dfrac32+\dfrac{\ln2}{4}}\approx1.673287$

*(All verified.)* **(c) is the standard "the radicand is a perfect square" design** — if yours is not, recheck the derivative.

**Q4 (18).**

**(a)** $\sqrt{(x')^2+(y')^2}=\sqrt2\,e^t$, so $L=\boxed{\sqrt2\left(e^\pi-1\right)}\approx31.3117$
**(b)** The curves meet where $\cos\theta=0$, i.e. $\theta=\pm\frac\pi2$:
$$\frac12\int_{-\pi/2}^{\pi/2}\left[(1+\cos\theta)^2-1^2\right]d\theta = \boxed{2+\frac{\pi}{4}}\approx2.785398$$

*(Both verified.)* **The limits are the whole difficulty in (b).**

**Q5 (24, 4 each).**

| | Verdict | Test |
|---|---|---|
| **(a)** | **Diverges** | $n$-th Term Test: $a_n\to\frac12\ne0$ |
| **(b)** | **Converges**, sum $1$ | Telescoping: $\frac1n-\frac1{n+1}$ |
| **(c)** | **Diverges** | $\frac{\ln n}{n}\ge\frac1n$ for $n\ge3$; direct comparison |
| **(d)** | **Converges** | Ratio $\to e^{-1}<1$ |
| **(e)** | **Conditionally convergent** | AST ✓; $\frac{1}{\ln(n+1)}>\frac1{n}$, so not absolute |
| **(f)** | **Converges** | Ratio $\to\frac45<1$ |

*(All verified.)* **Half the marks on each are for the hypotheses**, not the verdict.

**Q6 (18).** $\left|\dfrac{c_{n+1}}{c_n}\right|=\dfrac{n+1}{5n}\to\dfrac15$, so $R=5$, centre $-2$, open interval $(-7,3)$.

- $x=3$: $\sum n$ — **diverges** ($n$-th Term Test).
- $x=-7$: $\sum(-1)^nn$ — **diverges** ($n$-th Term Test; **AST does not apply**, since $b_n=n\not\to0$).

$$\boxed{(-7,\,3)}$$

**Both endpoints diverge here** — do not assume one of them saves you.

**Q7 (20).**

**(a)** $\ln(1+x)=x-\frac{x^2}2+\frac{x^3}3-\frac{x^4}4+\cdots$ at $x=0.2$:

$$0.2-0.02+\frac{0.008}{3}-\frac{0.0016}{4} = \boxed{0.182266\overline{6}}$$

**Bound first:** alternating with decreasing terms, so $|R_4|\le b_5=\dfrac{(0.2)^5}{5}=6.40\times10^{-5}$.
**Actual error: $5.489\times10^{-5}$** against $\ln1.2=0.182321556793955$. *(Verified — inside the bound, as it must be.)*

**(b)** $e^x=1+x+\frac{x^2}{2}+\frac{x^3}{6}+\cdots$, so the numerator is $\frac{x^3}{6}+O(x^4)$ and the limit is $\boxed{\dfrac16}$. *(Verified.)*

**(c)** $f(x)=e^{-1/x^2}$ for $x\ne0$, $f(0)=0$. **Every derivative vanishes at $0$**, so its Maclaurin series is identically zero — it converges everywhere, and equals $f$ only at $x=0$. **Smooth does not imply analytic.**

**Q8 (14).** Standard form already; $P=\tan x$, so $\mu=e^{\int\tan x\,dx}=\sec x$. Then $(y\sec x)'=\sec x\sin2x=2\sin x$, giving $y\sec x=-2\cos x+C$ and $y=\cos x(C-2\cos x)$. With $y(0)=1$: $C=3$.

$$\boxed{y=(3-2\cos x)\cos x}$$

*(Verified: substituting gives residual exactly $0$, and $y(0)=1$.)*

---

## Marking of the Sample Paper

| Q | Points | Where the marks are |
|---|---|---|
| 1 | 20 | 5 each; **method choice carries 2 of the 5** |
| 2 | 16 | 5 + 5 + 6; **(a) loses 2 without the written limit** |
| 3 | 20 | 6 + 6 + 8; setup carries most |
| 4 | 18 | 8 + 10; **(b)'s limits are 5 of the 10** |
| 5 | 24 | 4 each — **2 for the verdict, 2 for the hypotheses** |
| 6 | 18 | 8 radius, 4 per endpoint, 2 final interval |
| 7 | 20 | 8 + 6 + 6; **(a) loses 4 without the bound** |
| 8 | 14 | 4 $\mu$, 6 general, 2 initial condition, **2 for the substitution check** |

**A pass is about 80; a strong performance is 120+.**

> **If you scored below 70, look at where.** Losses concentrated in Q5–Q7 mean series, and series is
> half the paper — that is where the last week goes. Losses spread evenly across Q1–Q4 mean
> integration fluency, which is fixed by volume, not by reading.

---

## The Last Week

1. **Do PS 12 and Lab 12 first.** They exist to produce your revision list, and the list is worth more than any amount of undirected rereading.
2. **Rework every problem set from a blank page, timed.** Not read — reworked.
3. **Drill Q5-style problems** until the test choice is instant. **Highest-value revision available**, because it is a quarter of the paper and it is a decision procedure, not knowledge.
4. **Build your two pages by hand**, and reserve the last quarter of page 2 for your own recurring errors.
5. **Do this sample paper under exam conditions**, in one 150-minute sitting.

---

**Good luck.** *Name the method, check the hypotheses, bound the error, and substitute your answer back.*

---

*MATH 142 · Final Exam Revision Guide · covers Weeks 0–12*
