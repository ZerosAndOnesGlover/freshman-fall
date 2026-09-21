# MATH 141 · Calculus I
## Week 8 · Lecture 1 (Monday)
### Areas, Distances, and Riemann Sums

**Date:** Monday 16 November 2026 · 11:00–11:50 · Week 8

---

**Reading:** Stewart §5.1 | Spivak Ch. 13 (Integration)
**Quiz 08** — this Monday, covers Week 7 (the shape of a graph, curve sketching, applied optimization)

---

## 1. A New Kind of Problem

For five weeks, we have studied **differential calculus** — the mathematics of instantaneous rates of change, built from the tangent line problem. Today we begin **integral calculus** — the mathematics of accumulation, built from a completely different-looking problem: finding the area under a curve.

Remarkably, these two branches of calculus — seemingly unrelated — turn out to be inverse operations of one another. This is the single most important fact in all of calculus, and we will prove it precisely next week (the Fundamental Theorem of Calculus). Today, we build the machinery of accumulation from scratch.

---

## 2. The Area Problem

**The problem:** Given a continuous function $f(x) \geq 0$ on $[a,b]$, find the area of the region bounded by the curve $y=f(x)$, the $x$-axis, and the vertical lines $x=a$ and $x=b$.

For a rectangle, triangle, or trapezoid, elementary geometry suffices. For a curved region, we need a new idea: **approximate the area using rectangles, then take a limit as the rectangles become infinitesimally thin.**

This is exactly analogous to how we defined the derivative: approximate the tangent slope using secant lines, then take a limit as the secant "width" shrinks to zero. The same limiting philosophy that built differential calculus now builds integral calculus.

---

## 3. Sigma Notation — A Necessary Tool

Before building Riemann sums, we need compact notation for sums with many terms.

$$\sum_{i=1}^{n} a_i = a_1 + a_2 + a_3 + \cdots + a_n$$

**Read as:** "the sum from $i=1$ to $n$ of $a_i$."

### Essential Summation Formulas

These formulas let us compute sums exactly, without writing out every term:

$$\sum_{i=1}^{n} c = nc \qquad \text{(sum of a constant)}$$

$$\sum_{i=1}^{n} i = \frac{n(n+1)}{2} \qquad \text{(sum of first } n \text{ integers)}$$

$$\sum_{i=1}^{n} i^2 = \frac{n(n+1)(2n+1)}{6} \qquad \text{(sum of first } n \text{ squares)}$$

$$\sum_{i=1}^{n} i^3 = \left[\frac{n(n+1)}{2}\right]^2 \qquad \text{(sum of first } n \text{ cubes)}$$

**Properties of sums** (linearity — analogous to limit laws and derivative rules):

$$\sum_{i=1}^n (a_i + b_i) = \sum_{i=1}^n a_i + \sum_{i=1}^n b_i \qquad \sum_{i=1}^n ca_i = c\sum_{i=1}^n a_i$$

### Example 1

Compute $\displaystyle\sum_{i=1}^{5}(2i+1)$ two ways: directly, and using formulas.

**Directly:** $3+5+7+9+11 = 35$

**Using formulas:** $\displaystyle\sum_{i=1}^5(2i+1) = 2\sum_{i=1}^5 i + \sum_{i=1}^5 1 = 2\cdot\frac{5(6)}{2} + 5(1) = 30+5=35$ ✓

---

## 4. Approximating Area with Rectangles

Divide $[a,b]$ into $n$ equal subintervals, each of width:

$$\Delta x = \frac{b-a}{n}$$

The subinterval endpoints are: $x_0=a$, $x_1=a+\Delta x$, $x_2=a+2\Delta x$, $\ldots$, $x_n = a+n\Delta x = b$.

On each subinterval $[x_{i-1}, x_i]$, build a rectangle of width $\Delta x$ and height determined by evaluating $f$ at some point in that subinterval. Three common choices:

**Right endpoint sum:**
$$R_n = \sum_{i=1}^{n} f(x_i)\Delta x$$

**Left endpoint sum:**
$$L_n = \sum_{i=1}^{n} f(x_{i-1})\Delta x$$

**Midpoint sum:**
$$M_n = \sum_{i=1}^{n} f(\bar{x}_i)\Delta x \quad \text{where } \bar{x}_i = \frac{x_{i-1}+x_i}{2}$$

Each of these is called a **Riemann sum** — an approximation of the exact area using a finite number of rectangles.

---

## 5. Worked Example — Approximating $\int_0^1 x^2\,dx$ Numerically

Estimate the area under $f(x)=x^2$ on $[0,1]$ using $n=4$ rectangles, with right endpoints.

$\Delta x = \dfrac{1-0}{4} = \dfrac14$. Endpoints: $x_0=0, x_1=\tfrac14, x_2=\tfrac12, x_3=\tfrac34, x_4=1$.

$$R_4 = \left[f\!\left(\tfrac14\right)+f\!\left(\tfrac12\right)+f\!\left(\tfrac34\right)+f(1)\right]\cdot\frac14$$

$$= \left[\frac{1}{16}+\frac{1}{4}+\frac{9}{16}+1\right]\cdot\frac14 = \left[\frac{1+4+9+16}{16}\right]\cdot\frac14 = \frac{30}{16}\cdot\frac14 = \frac{30}{64} = 0.46875$$

With left endpoints:
$$L_4 = \left[f(0)+f\!\left(\tfrac14\right)+f\!\left(\tfrac12\right)+f\!\left(\tfrac34\right)\right]\cdot\frac14 = \left[0+\frac{1}{16}+\frac14+\frac{9}{16}\right]\cdot\frac14 = \frac{14}{16}\cdot\frac14 = 0.21875$$

The true area (which we'll confirm exactly using the Fundamental Theorem next week) is $\dfrac13 \approx 0.3333$. Notice $L_4 < \frac13 < R_4$ — since $f(x)=x^2$ is increasing on $[0,1]$, left sums underestimate and right sums overestimate.

---

## 6. Computing the Exact Area — Taking $n \to \infty$

The key insight: as $n\to\infty$ (more and more, thinner and thinner rectangles), both $L_n$ and $R_n$ approach the same exact value — the true area.

**General setup for $R_n$ on $[a,b]$ with $n$ rectangles:**

$$x_i = a+i\Delta x \qquad \Delta x = \frac{b-a}{n}$$

$$R_n = \sum_{i=1}^n f(x_i)\Delta x$$

**Exact computation for $f(x)=x^2$ on $[0,1]$:**

$\Delta x = \dfrac1n$, $x_i = \dfrac{i}{n}$.

$$R_n = \sum_{i=1}^{n} \left(\frac{i}{n}\right)^2 \cdot \frac1n = \frac{1}{n^3}\sum_{i=1}^n i^2 = \frac{1}{n^3}\cdot\frac{n(n+1)(2n+1)}{6}$$

$$= \frac{n(n+1)(2n+1)}{6n^3} = \frac{(n+1)(2n+1)}{6n^2}$$

Expand: $\dfrac{2n^2+3n+1}{6n^2} = \dfrac13 + \dfrac{1}{2n} + \dfrac{1}{6n^2}$

**Take the limit:**

$$\lim_{n\to\infty} R_n = \lim_{n\to\infty}\left(\frac13+\frac1{2n}+\frac1{6n^2}\right) = \frac13$$

**The exact area under $y=x^2$ from $0$ to $1$ is $\dfrac13$.** This matches our numerical estimate from Section 5, and we derived it with complete rigor — no approximation at the final step.

---

## 7. The Definition of the Definite Integral (Preview)

This limiting process — sum of rectangle areas as $n\to\infty$ — defines the **definite integral**:

$$\int_a^b f(x)\,dx = \lim_{n\to\infty} \sum_{i=1}^n f(x_i)\Delta x$$

We formalize this notation and its properties on Tuesday. For now, understand: **the definite integral is defined as a limit of Riemann sums** — exactly as the derivative was defined as a limit of difference quotients. Both are limits; that is the unifying thread of all of calculus.

---

## 8. The Distance Problem — A Parallel Application

Riemann sums don't just compute area — they compute **any accumulated quantity** built from a rate.

**Problem:** A car's velocity is $v(t)$ (possibly changing). Find the total distance traveled over $[a,b]$.

If velocity were constant, distance $=$ velocity $\times$ time. For changing velocity, approximate: break $[a,b]$ into small time intervals, assume velocity is roughly constant on each (evaluate $v$ at some point in each subinterval), and sum:

$$\text{Distance} \approx \sum_{i=1}^n v(t_i)\Delta t$$

This is **structurally identical** to the area-under-a-curve Riemann sum — because distance traveled equals the area under the velocity-vs-time graph. This is not a coincidence: it is the first hint of the deep connection between derivatives (velocity is the derivative of position) and integrals (distance is accumulated from velocity) that the Fundamental Theorem formalizes.

### Example 2

A particle's velocity is $v(t) = 3t^2$ (m/s). Estimate the distance traveled from $t=0$ to $t=2$ using $n=4$ subintervals and right endpoints.

$\Delta t = 0.5$. $t_1=0.5, t_2=1, t_3=1.5, t_4=2$.

$$R_4 = [v(0.5)+v(1)+v(1.5)+v(2)]\cdot0.5 = [0.75+3+6.75+12]\cdot0.5 = 22.5\cdot0.5 = 11.25\text{ m}$$

(The exact distance, found via the Fundamental Theorem next week, is $t^3\Big|_0^2 = 8$ m — showing again that finite Riemann sums are only approximations; the true value requires the limit.)

---

## 9. CS Connection — Numerical Integration and the Limits of Discretization

**Riemann sums ARE numerical integration.** Every time a computer needs to evaluate $\int_a^b f(x)\,dx$ for a function without an elementary antiderivative (extremely common in physics simulations, statistics, and machine learning), it uses a discretized approximation exactly like $L_n$, $R_n$, or $M_n$ — or refinements of them (Simpson's Rule, Gaussian quadrature).

**Why midpoint sums matter for numerical accuracy:** The midpoint sum $M_n$ typically converges to the true integral much faster than $L_n$ or $R_n$ as $n$ increases — this connects directly to the numerical differentiation error analysis from Lab 2 (central differences beat forward differences for exactly the same reason: symmetric sampling cancels leading-order error).

**Discretization is everywhere in computing:** Digital audio is a Riemann-sum-like discretization of a continuous sound wave. Digital images discretize continuous light intensity over a grid. Every numerical simulation (weather models, financial models, physics engines) works by discretizing continuous processes into finite sums — precisely the philosophy of this lecture, generalized to multiple dimensions and more sophisticated rate equations.

---

## Lecture 1 Exercises

1. Evaluate using summation formulas:
   - (a) $\displaystyle\sum_{i=1}^{10} (3i-2)$
   - (b) $\displaystyle\sum_{i=1}^{6} i^2$
   - (c) $\displaystyle\sum_{i=1}^{4}(i^3-i)$

2. Estimate the area under $f(x) = \sqrt{x}$ on $[0,4]$ using $n=4$ rectangles with (a) right endpoints, (b) left endpoints, (c) midpoints. Compare the three estimates.

3. Set up (but do not yet evaluate the limit of) the right-endpoint Riemann sum $R_n$ for $f(x) = x^3$ on $[0,2]$, expressed as a function of $n$ only (i.e., simplify $x_i$, $\Delta x$, and substitute).

4. Using the sum formula for $\sum i^3$, compute the exact value of $\displaystyle\lim_{n\to\infty}R_n$ from Exercise 3. (This is $\int_0^2 x^3\,dx$ — verify your answer next week using the Fundamental Theorem.)

5. A particle has velocity $v(t) = 4-t^2$ m/s for $t\in[0,2]$. Estimate the total distance traveled using a midpoint sum with $n=4$.

6. **(Conceptual)** Explain why, for a decreasing function, the left-endpoint sum $L_n$ OVERestimates the true area while the right-endpoint sum $R_n$ UNDERestimates it (the opposite of what we found for the increasing function $x^2$ in Section 5).

---


### Answers

**1. (a)** $3\sum i-2(10)=3(55)-20=\boxed{145}$ &nbsp;&nbsp;
**(b)** $\dfrac{6(7)(13)}{6}=\boxed{91}$ &nbsp;&nbsp;
**(c)** $\left(\tfrac{4\cdot5}{2}\right)^2-\tfrac{4\cdot5}{2}=100-10=\boxed{90}$

**2.** $f=\sqrt x$ on $[0,4]$, $n=4$, $\Delta x=1$:

| Method | Sample points | Sum |
|---|---|---|
| Right | $1,2,3,4$ | $\boxed{6.146}$ |
| Left | $0,1,2,3$ | $\boxed{4.146}$ |
| Midpoint | $0.5,1.5,2.5,3.5$ | $\boxed{5.384}$ |

Exact value $=\tfrac{16}{3}\approx5.333$. Since $\sqrt x$ is **increasing**, left underestimates and
right overestimates — and they bracket the truth. The midpoint sum is far closer than either
(error $0.05$ against $0.81$), which previews the $O(1/n^2)$ convergence of Lab 08.

**3.** $\Delta x=\dfrac2n$, $x_i=\dfrac{2i}{n}$, so
$$R_n=\sum_{i=1}^{n}\left(\frac{2i}{n}\right)^3\cdot\frac2n=\boxed{\frac{16}{n^4}\sum_{i=1}^{n}i^3}$$

**4.** Using $\sum i^3=\left[\tfrac{n(n+1)}{2}\right]^2$:
$$R_n=\frac{16}{n^4}\cdot\frac{n^2(n+1)^2}{4}=4\left(\frac{n+1}{n}\right)^2\longrightarrow\boxed{4}$$
So $\displaystyle\int_0^2x^3\,dx=4$ — matching $\tfrac{2^4}{4}$, as FTC will confirm on Wednesday.

**5.** Midpoints $0.25,0.75,1.25,1.75$ with $\Delta t=0.5$:
$$M_4=0.5\left[3.9375+3.4375+2.4375+0.9375\right]=\boxed{5.375\ \text{m}}$$
Exact $=\tfrac{16}{3}\approx5.333$ m. Note $v>0$ on all of $[0,2]$, so distance and displacement
agree here — they would not if $v$ changed sign.

**6.** For a **decreasing** function, the left endpoint of each subinterval is where $f$ is
**largest**, so each left rectangle is taller than the region it covers and $L_n$ **overestimates**.
The right endpoint gives the smallest value on the subinterval, so $R_n$ **underestimates**.

For an increasing function the roles swap. The general statement: the endpoint sum evaluated where
$f$ is larger overestimates. Since monotonicity determines which endpoint that is,
**$L_n$ and $R_n$ always bracket the true value for a monotonic $f$** — which makes
$|R_n-L_n|=|f(b)-f(a)|\Delta x$ a free error bound.

*Next: Tuesday — The Definite Integral: Formal Definition and Properties*
