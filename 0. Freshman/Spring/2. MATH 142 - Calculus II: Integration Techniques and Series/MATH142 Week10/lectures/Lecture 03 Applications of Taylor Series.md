# MATH 142 · Calculus II
## Week 10 · Lecture 3 (Wednesday)
### Applications — and Week 0's Debt

---

**Reading:** Stewart §11.10–11.11 | Apostol Ch. 11 §11.11

---

## 1. Limits Without L'Hôpital

**Substitute the series and read off the leading behaviour.** Often faster and always more informative than repeated L'Hôpital.

### Example 1

$$\lim_{x\to0}\frac{\sin x-x}{x^3}$$

Substituting $\sin x = x-\frac{x^3}{6}+\frac{x^5}{120}-\cdots$:

$$\frac{\sin x-x}{x^3} = \frac{-\frac{x^3}{6}+\frac{x^5}{120}-\cdots}{x^3} = -\frac16+\frac{x^2}{120}-\cdots \longrightarrow \boxed{-\frac16}$$

*(Verified.)*

**L'Hôpital would need three applications.** The series does it in one line — **and tells you more**: the next term shows the approach to $-\frac16$ is from above, at rate $\frac{x^2}{120}$.

### Example 2 — a small table

| Limit | via series | Value |
|---|---|---|
| $\dfrac{1-\cos x}{x^2}$ | $\frac{x^2/2 - x^4/24+\cdots}{x^2}$ | $\frac12$ |
| $\dfrac{e^x-1-x}{x^2}$ | $\frac{x^2/2+x^3/6+\cdots}{x^2}$ | $\frac12$ |
| $\dfrac{x-\arctan x}{x^3}$ | $\frac{x^3/3-x^5/5+\cdots}{x^3}$ | $\frac13$ |

*(All verified.)*

> **The method: expand far enough that the lowest surviving power appears, then divide.** If the
> leading terms cancel, expand further — the series always tells you how far.

---

## 2. Integrating What Cannot Be Integrated

**This is the payoff the course has been building toward since Week 0.**

> **Week 0, Lecture 1:** $e^{-x^2}$, $\frac{\sin x}{x}$ and $\sqrt{1+x^3}$ are continuous, so each has
> an antiderivative by the FTC — **and none of those antiderivatives is elementary** (Liouville, 1835).

**The technique: expand and integrate term by term**, which Week 9 established is legal inside the radius.

### Example 3 — the Gaussian

$$e^{-x^2} = \sum_{n=0}^\infty\frac{(-1)^nx^{2n}}{n!} \qquad(R=\infty)$$

Integrating from 0 to 1:

$$\int_0^1e^{-x^2}dx = \sum_{n=0}^\infty\frac{(-1)^n}{n!}\int_0^1x^{2n}dx = \boxed{\sum_{n=0}^\infty\frac{(-1)^n}{n!\,(2n+1)}}$$

$$= 1-\frac13+\frac1{10}-\frac1{42}+\frac{1}{216}-\cdots$$

**It is an alternating series with decreasing terms**, so Week 8's estimate applies: **the error is at most the first omitted term**, with no further work.

*(Verified. Partial sums:)*

| terms | value | error |
|---|---|---|
| $5$ | $0.7474868$ | $6.6\times10^{-4}$ |
| $9$ | $0.74682427$ | $1.3\times10^{-7}$ |
| $12$ | $0.7468241327$ | $7.8\times10^{-11}$ |
| $\mathbf{13}$ | $\mathbf{0.746824132818}$ | $\mathbf{5.6\times10^{-12}}$ |

**Thirteen terms for ten decimal places.**

> **Compare Lab 0, in Week 0.** You computed this same integral with Simpson's rule: **128 function
> evaluations** for the same accuracy. The debrief promised you would do it in 13 terms in Week 10.
> **Here it is.**

### Example 4 — the sine integral

$$\frac{\sin x}{x} = \sum_{n=0}^\infty\frac{(-1)^nx^{2n}}{(2n+1)!} \implies \int_0^1\frac{\sin x}{x}dx = \sum_{n=0}^\infty\frac{(-1)^n}{(2n+1)(2n+1)!}$$

$$= 1-\frac{1}{18}+\frac{1}{600}-\cdots = 0.946083070367\ldots$$

*(Verified — this is $\mathrm{Si}(1)$.)*

**Six terms give eleven correct digits** ($1.2\times10^{-11}$). *(Measured.)*

**Note $\frac{\sin x}{x}$ is undefined at $x=0$** — but the series has constant term 1 and is perfectly well behaved there, which is the series *removing* a singularity that the formula only appeared to have.

---

## 3. Why This Is Not a Trick

**Every one of these steps was licensed by an earlier week:**

| Step | Licensed by |
|---|---|
| $f$ equals its Taylor series | **Week 10**, Taylor's theorem: $R_n\to0$ |
| integrate term by term | **Week 9**, absolute convergence inside $R$ |
| absolute convergence permits it | **Week 8**, rearrangement theorem |
| error bounded by the next term | **Week 8**, alternating series estimate |

> **Four weeks of theorems, all used in a single three-line computation.** That is what the second
> half of this course was building.

---

## 4. The Binomial Series in Use

$$(1+x)^k = \sum_{n=0}^\infty\binom kn x^n,\qquad |x|<1$$

### Example 5 — a square root

$$\sqrt{1.1} = (1+0.1)^{1/2} = 1+\frac{0.1}{2}-\frac{0.01}{8}+\frac{0.001}{16}-\cdots = 1+0.05-0.00125+0.0000625-\cdots$$

Four terms give $1.0488125$ against $\sqrt{1.1}=1.0488088\ldots$ — **five correct digits from four terms of arithmetic.**

### Example 6 — a relativistic approximation

In special relativity the kinetic energy is $K = mc^2\left[(1-v^2/c^2)^{-1/2}-1\right]$. With $x=-v^2/c^2$ and $k=-\frac12$:

$$(1-v^2/c^2)^{-1/2} = 1+\frac{v^2}{2c^2}+\frac{3v^4}{8c^4}+\cdots$$

$$\implies K = \frac12mv^2+\frac{3mv^4}{8c^2}+\cdots$$

**The first term is the Newtonian kinetic energy**, and the rest is the relativistic correction. **This is how a limiting case is extracted from a theory** — and it is one of the most-used calculations in physics.

---

## 5. How a Numerical Library Actually Works

Everything in this course now assembles into an algorithm.

> **To evaluate $\sin(x)$ to machine precision:**
>
> 1. **Argument reduction.** Use periodicity and symmetry to replace $x$ by $\tilde x$ in a small
>    interval, say $\left[-\frac\pi4,\frac\pi4\right]$.
> 2. **Fixed-degree polynomial.** Evaluate a Taylor (or better, minimax) polynomial of a degree chosen
>    **once, at design time**, so the Lagrange bound guarantees the required accuracy across that
>    whole interval.
> 3. **Reconstruct** the answer using the symmetry from step 1.

**Step 1 is Week 9's lesson** — the series is fast near its centre and slow far away, and the $\arctan$ measurement made the cost explicit: $5\times10^9$ terms at $x=1$ against **17** at $x=\frac{1}{\sqrt3}$.

**Step 2 is Week 10's** — a rigorous, computable error bound, valid over an interval.

> **No other method in this course carries a guarantee.** Simpson's rule gave a measured order, not a
> certificate. Taylor's theorem gives a bound you can prove before running anything, which is exactly
> what shipping a library requires.

---

## 6. What To Take From This Lecture

1. **Series evaluate limits** in one line, and show the rate of approach.
2. **Series integrate the non-integrable.** Expand, integrate term by term, bound the error.
3. **$\int_0^1e^{-x^2}dx$ in 13 terms** against Simpson's 128 evaluations — Week 0's debt, paid.
4. **Every step was licensed by Weeks 8–10.** Nothing here is a trick.
5. **The binomial series extracts limiting cases**, as in the Newtonian limit of relativity.
6. **Argument reduction plus a bounded polynomial is how libraries work.**

---

## Looking Ahead

**Week 11 turns to differential equations** — equations whose unknown is a function. Power series are one of the standard methods of solving them, and separable and linear equations are the two cases with closed-form answers.

**Week 12 closes the course** with systems, a preview of numerical methods, and the final review.

---

*Next: Week 11, Monday — Introduction to Differential Equations*
