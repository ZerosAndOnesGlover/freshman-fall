# MATH 141 · Calculus I
## Week 8 · Lecture 2 (Tuesday)
### The Definite Integral: Formal Definition, Notation, and Properties

**Date:** Tuesday 13 October 2026 · 11:00–11:50 · Week 8

---

**Reading:** Stewart §5.2 | Spivak Ch. 13 (§13.1–13.2)

---

## 1. The Formal Definition

Monday we built Riemann sums using equal-width subintervals and specific sample points (left, right, midpoint). The **general** definition allows arbitrary partitions and arbitrary sample points within each subinterval — this generality is what makes the definite integral robust and well-defined.

> **Definition.** Let $f$ be defined on $[a,b]$. Divide $[a,b]$ into $n$ subintervals (not necessarily equal width) with partition points $a=x_0<x_1<\cdots<x_n=b$. In each subinterval $[x_{i-1},x_i]$, choose a sample point $x_i^*$. Form the Riemann sum:
> $$\sum_{i=1}^n f(x_i^*)\Delta x_i \qquad (\Delta x_i = x_i - x_{i-1})$$
>
> If $\displaystyle\lim_{\max\Delta x_i\to0}\sum_{i=1}^n f(x_i^*)\Delta x_i$ exists (independent of the choice of partition and sample points), we call $f$ **integrable** on $[a,b]$ and define:
> $$\int_a^b f(x)\,dx = \lim_{\max\Delta x_i\to0}\sum_{i=1}^n f(x_i^*)\Delta x_i$$

**Notation breakdown:**

| Symbol | Meaning |
|--------|---------|
| $\int$ | Elongated "S" — for "sum" (Leibniz's notation, chosen deliberately) |
| $f(x)$ | The **integrand** |
| $dx$ | Indicates the variable of integration; the "infinitesimal width" |
| $a, b$ | Lower and upper **limits of integration** |

**Key theorem (stated without full proof — see Spivak for details):**

> If $f$ is continuous on $[a,b]$, then $f$ is integrable on $[a,b]$.

This means: for continuous functions (which covers essentially everything in this course), we don't need to worry about whether the limit exists — it always does, and equal-width partitions with any consistent sample point choice (left, right, or midpoint) all converge to the same value.

---

## 2. Geometric Interpretation — Signed Area

When $f(x) \geq 0$ on $[a,b]$, $\displaystyle\int_a^b f(x)\,dx$ equals the area between the curve and the $x$-axis.

**When $f(x) < 0$:** the Riemann sum terms $f(x_i^*)\Delta x$ are negative, so the integral is negative. Geometrically, $\displaystyle\int_a^b f(x)\,dx$ represents **signed area**:

$$\int_a^b f(x)\,dx = (\text{area above } x\text{-axis}) - (\text{area below } x\text{-axis})$$

### Example 1

Evaluate $\displaystyle\int_{-1}^{1} x\,dx$ using symmetry (no Riemann sum computation needed).

The region above the $x$-axis (on $[0,1]$) is a triangle of area $\frac12$. The region below the $x$-axis (on $[-1,0]$) is a triangle of area $\frac12$, counted as $-\frac12$.

$$\int_{-1}^1 x\,dx = \frac12 - \frac12 = 0$$

This makes sense: $f(x)=x$ is an odd function, and the signed areas on either side of $x=0$ exactly cancel.

---

## 3. Properties of the Definite Integral

These follow directly from the limit-of-sums definition and are used constantly.

### Basic Algebraic Properties

$$\int_a^b c\,dx = c(b-a) \qquad \text{(constant function)}$$

$$\int_a^b [f(x)+g(x)]\,dx = \int_a^b f(x)\,dx + \int_a^b g(x)\,dx$$

$$\int_a^b cf(x)\,dx = c\int_a^b f(x)\,dx$$

$$\int_a^b [f(x)-g(x)]\,dx = \int_a^b f(x)\,dx - \int_a^b g(x)\,dx$$

These are exactly the linearity properties inherited from sums (Monday's lecture) via the limit process.

### Interval Additivity

$$\int_a^b f(x)\,dx + \int_b^c f(x)\,dx = \int_a^c f(x)\,dx$$

**Geometric meaning:** the area from $a$ to $c$ equals the area from $a$ to $b$ plus the area from $b$ to $c$ — obviously true for regions, and it extends even when $b$ is not between $a$ and $c$ (using the convention below).

### Reversal and Degenerate Conventions

$$\int_a^a f(x)\,dx = 0 \qquad \int_b^a f(x)\,dx = -\int_a^b f(x)\,dx$$

The second convention makes interval additivity work universally, regardless of the ordering of $a,b,c$.

### Comparison Properties

If $f(x) \geq 0$ on $[a,b]$:
$$\int_a^b f(x)\,dx \geq 0$$

If $f(x) \geq g(x)$ on $[a,b]$:
$$\int_a^b f(x)\,dx \geq \int_a^b g(x)\,dx$$

If $m \leq f(x) \leq M$ on $[a,b]$:
$$m(b-a) \leq \int_a^b f(x)\,dx \leq M(b-a)$$

This last property is extremely useful for **estimating** an integral without computing it exactly.

### Example 2

Show that $\displaystyle 2 \leq \int_0^1\sqrt{1+x^3}\,dx \leq \sqrt2$.

For $x\in[0,1]$: $x^3\in[0,1]$, so $1+x^3\in[1,2]$, so $\sqrt{1+x^3}\in[1,\sqrt2]$.

By the comparison property: $1\cdot(1-0) \leq \int_0^1\sqrt{1+x^3}\,dx \leq \sqrt2\cdot(1-0)$

$$1 \leq \int_0^1\sqrt{1+x^3}\,dx \leq \sqrt2$$

*(The stated bound of "2" in the problem was an error to catch — the correct upper bound from this method is $\sqrt2\approx1.414$, and the lower bound is $1$, not $2$. This illustrates the importance of checking your own bounding carefully!)*

---

## 4. Computing Definite Integrals via Geometry

For simple functions, we can compute exact integrals using elementary area formulas (triangles, rectangles, semicircles) — no Riemann sum limit required.

### Example 3

Evaluate $\displaystyle\int_0^3(2x+1)\,dx$ using geometry.

The graph of $y=2x+1$ is a line. Over $[0,3]$: $y(0)=1$, $y(3)=7$. The region is a trapezoid with parallel sides $1$ and $7$, width $3$.

$$\text{Area} = \frac{(1+7)}{2}\cdot3 = 12$$

$$\int_0^3(2x+1)\,dx = 12$$

### Example 4

Evaluate $\displaystyle\int_{-2}^{2}\sqrt{4-x^2}\,dx$ using geometry.

$y=\sqrt{4-x^2}$ is the upper half of the circle $x^2+y^2=4$ (radius 2). This is a semicircle with radius 2.

$$\text{Area} = \frac12\pi(2)^2 = 2\pi$$

$$\int_{-2}^2\sqrt{4-x^2}\,dx = 2\pi$$

---

## 5. The Midpoint Rule as a Practical Approximation Tool

For functions without elementary geometric shortcuts, we use the Riemann sum approximations from Monday directly. The **Midpoint Rule** is generally the most efficient of the elementary methods:

$$\int_a^b f(x)\,dx \approx M_n = \Delta x\left[f(\bar x_1)+f(\bar x_2)+\cdots+f(\bar x_n)\right]$$

### Example 5

Approximate $\displaystyle\int_1^2 \frac1x\,dx$ using $M_4$.

$\Delta x = 0.25$. Midpoints: $1.125, 1.375, 1.625, 1.875$.

$$M_4 = 0.25\left[\frac{1}{1.125}+\frac1{1.375}+\frac1{1.625}+\frac1{1.875}\right]$$

$$\approx 0.25[0.8889+0.7273+0.6154+0.5333] = 0.25(2.7649) \approx 0.6912$$

*(The exact value, found next week via the Fundamental Theorem, is $\ln2 \approx 0.6931$ — the midpoint approximation with just 4 rectangles is already accurate to two decimal places!)*

---

## 6. Average Value of a Function

A natural application of the definite integral: the **average value** of $f$ on $[a,b]$.

> **Definition.** The average value of $f$ on $[a,b]$ is:
> $$f_{\text{avg}} = \frac{1}{b-a}\int_a^b f(x)\,dx$$

**Why this definition makes sense:** it generalizes the average of finitely many numbers ($\frac{1}{n}\sum a_i$) to a continuum of values, using the integral in place of the sum.

### The Mean Value Theorem for Integrals

> If $f$ is continuous on $[a,b]$, there exists $c\in[a,b]$ such that:
> $$f(c) = f_{\text{avg}} = \frac{1}{b-a}\int_a^b f(x)\,dx$$

**Note the parallel structure** to the Mean Value Theorem for derivatives (Week 4): there, the instantaneous rate of change equals the average rate of change at some point; here, the function value equals its own average at some point. Both theorems rely on continuity plus the Extreme Value Theorem.

### Example 6

Find the average value of $f(x) = x^2$ on $[0,3]$.

$$f_{\text{avg}} = \frac13\int_0^3 x^2\,dx$$

Using the technique from Monday's lecture (generalized — you'll formalize this with the Fundamental Theorem next week), $\displaystyle\int_0^3x^2\,dx = 9$ (verify via the limit-of-Riemann-sums method, analogous to the $\int_0^1x^2\,dx=1/3$ computation).

$$f_{\text{avg}} = \frac13(9) = 3$$

---

## 7. CS Connection — Integrals as Expected Values

The average value formula $\displaystyle f_{\text{avg}} = \frac{1}{b-a}\int_a^b f(x)\,dx$ is the continuous analog of the **expected value** of a random variable in probability and statistics:

$$E[X] = \int_{-\infty}^{\infty} x \cdot p(x)\,dx$$

where $p(x)$ is a probability density function. Every time a machine learning model computes an expected loss, a Bayesian posterior mean, or an integral over a continuous probability distribution, it is applying exactly this definite integral machinery. The comparison properties (Section 3) are the direct foundation of concentration inequalities and bounds used throughout statistical learning theory.

**Signed area and accumulator patterns:** In systems programming, running totals, accumulator variables, and prefix-sum algorithms are the discrete analog of the definite integral's interval-additivity property. A prefix sum array `S[i] = S[i-1] + a[i]` is literally a discrete Riemann sum, and querying `S[j] - S[i]` for a range sum is the discrete analog of $\int_a^c = \int_a^b + \int_b^c$.

---

## Lecture 2 Exercises

1. Evaluate using geometric formulas (no Riemann sums needed):
   - (a) $\displaystyle\int_0^4(3-x)\,dx$
   - (b) $\displaystyle\int_{-3}^{3}\sqrt{9-x^2}\,dx$
   - (c) $\displaystyle\int_1^5 7\,dx$

2. Given that $\displaystyle\int_0^2 f(x)\,dx = 5$, $\displaystyle\int_2^5 f(x)\,dx = -3$, and $\displaystyle\int_0^5 g(x)\,dx = 8$, find:
   - (a) $\displaystyle\int_0^5 f(x)\,dx$
   - (b) $\displaystyle\int_5^2 f(x)\,dx$
   - (c) $\displaystyle\int_0^5 [2f(x)-3g(x)]\,dx$ (you'll need to determine $\int_0^5 f(x)\,dx$ from (a) first)

3. Use the comparison property to find bounds on $\displaystyle\int_1^4 \frac{1}{1+x^2}\,dx$ (find the max and min of the integrand on $[1,4]$ first).

4. Approximate $\displaystyle\int_0^\pi \sin x\,dx$ using $M_4$ (midpoint rule with 4 rectangles). Compare to the exact value (which you will later show equals $2$).

5. Find the average value of $f(x)=4-x^2$ on $[-2,2]$, then find the value(s) of $c$ guaranteed by the Mean Value Theorem for Integrals.

6. **(Conceptual)** Explain why $\displaystyle\int_a^b f(x)\,dx$ can be negative even though "area" is usually thought of as a non-negative quantity. Give a specific example function and interval where this occurs, and compute the integral geometrically.

---


### Answers

**1. (a)** The line $y=3-x$ gives a triangle of area $\tfrac92$ above the axis on $[0,3]$ and
$\tfrac12$ below on $[3,4]$: $\boxed{\tfrac92-\tfrac12=4}$.
**(b)** Upper half of the circle $x^2+y^2=9$: $\boxed{\tfrac{9\pi}{2}\approx14.137}$.
**(c)** Rectangle: $\boxed{7\times4=28}$.

**2. (a)** $\int_0^5f=\int_0^2f+\int_2^5f=5+(-3)=\boxed{2}$
**(b)** $\int_5^2f=-\int_2^5f=\boxed{3}$ — reversing the limits negates the integral.
**(c)** $2(2)-3(8)=\boxed{-20}$

**3.** $\dfrac{1}{1+x^2}$ is decreasing on $[1,4]$, so its max is $\tfrac12$ (at $x=1$) and min
$\tfrac1{17}$ (at $x=4$). With interval length 3:
$$\boxed{\tfrac{3}{17}\approx0.176 \ \leq\ \int_1^4\frac{dx}{1+x^2}\ \leq\ \tfrac32=1.5}$$
The true value is $\approx0.540$ — comfortably inside, though the bounds are loose. Comparison
bounds are cheap and crude; that is their role.

**4.** $\Delta x=\tfrac\pi4$, midpoints $\tfrac\pi8,\tfrac{3\pi}8,\tfrac{5\pi}8,\tfrac{7\pi}8$:
$$M_4=\boxed{2.0523}$$
against the exact value $2$ — an error of only $2.6\%$ with four rectangles. The midpoint rule is
strikingly good on smooth functions.

**5.** $f_{\text{avg}}=\dfrac{1}{4}\displaystyle\int_{-2}^{2}(4-x^2)\,dx=\dfrac{1}{4}\cdot\dfrac{32}{3}=\boxed{\dfrac83}$

MVT for Integrals: solve $4-c^2=\tfrac83 \Rightarrow c^2=\tfrac43 \Rightarrow
\boxed{c=\pm\tfrac{2}{\sqrt3}\approx\pm1.155}$. Both lie in $(-2,2)$, so **two** values qualify —
the theorem promises at least one, never uniqueness.

**6.** $\int_a^bf$ is **signed** area: regions below the $x$-axis count negatively. It is not "area"
in the geometric sense but the *net accumulation* of $f$, which is exactly what makes it the right
tool for displacement, net change, and work.

Example: $\displaystyle\int_0^{2\pi}\sin x\,dx=0$, because the hump on $[0,\pi]$ (area $2$) is
exactly cancelled by the trough on $[\pi,2\pi]$ (area $-2$). Simpler still,
$\displaystyle\int_{-1}^{1}x\,dx=0$.

For **total geometric area** you must integrate $|f|$, or split at the zeros and negate the
negative pieces — a distinction worth a whole exam question.

*Next: Wednesday — The Fundamental Theorem of Calculus*
