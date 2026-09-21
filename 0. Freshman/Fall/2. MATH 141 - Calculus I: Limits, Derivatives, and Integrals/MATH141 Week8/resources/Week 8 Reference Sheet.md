# MATH 141 · Calculus I
## Week 8 Reference Sheet
### Riemann Sums · The Definite Integral · Its Properties

---

## Sigma Notation and Summation Formulas

$$\sum_{i=1}^n c = nc \qquad \sum_{i=1}^n i = \frac{n(n+1)}{2} \qquad \sum_{i=1}^n i^2 = \frac{n(n+1)(2n+1)}{6} \qquad \sum_{i=1}^n i^3 = \left[\frac{n(n+1)}{2}\right]^2$$

**Also useful:** $\displaystyle\sum_{i=1}^{n}(2i-1)^2 = \frac{n(4n^2-1)}{3}$ *(for midpoint sums)*

**Linearity:** $\displaystyle\sum(a_i+b_i)=\sum a_i+\sum b_i \qquad \sum ca_i = c\sum a_i$

---

## Riemann Sums

$\Delta x = \dfrac{b-a}{n}$, $\quad x_i = a+i\Delta x$

| Sum type | Formula | Sample point |
|----------|---------|--------------|
| Right | $R_n=\sum_{i=1}^n f(x_i)\Delta x$ | Right endpoint of each subinterval |
| Left | $L_n=\sum_{i=1}^n f(x_{i-1})\Delta x$ | Left endpoint |
| Midpoint | $M_n=\sum_{i=1}^n f(\bar x_i)\Delta x$ | Midpoint $\bar x_i=\dfrac{2i-1}{2n}$ on $[0,1]$ |

**For increasing $f$:** $L_n \le \text{true area} \le R_n$. **For decreasing $f$:** reversed.

### Worked closed forms — $f(x)=x^2$ on $[0,1]$, exact value $\tfrac13$

$$R_n=\frac{(n+1)(2n+1)}{6n^2}\qquad L_n=\frac{(n-1)(2n-1)}{6n^2}\qquad M_n=\frac{4n^2-1}{12n^2}$$

| $n$ | $L_n$ | $R_n$ | $M_n$ |
|---|---|---|---|
| $10$ | $0.285000$ | $0.385000$ | $0.332500$ |
| $50$ | $0.323400$ | $0.343400$ | $0.333300$ |

**Convergence orders:** $L_n$ and $R_n$ err by $O(1/n)$; $M_n$ errs by $O(1/n^2)$. Verified: doubling
$n$ from 10 to 20 to 40 cuts the $R_n$ error roughly in half each time ($5.17\to2.54\to1.26\times10^{-2}$)
but cuts the $M_n$ error by four ($8.33\to2.08\to0.52\times10^{-4}$).

---

## The Definite Integral — Definition

$$\int_a^b f(x)\,dx = \lim_{n\to\infty}\sum_{i=1}^n f(x_i^*)\Delta x,\qquad x_i^*\in[x_{i-1},x_i]\ \textbf{arbitrary}$$

**Theorem:** $f$ continuous on $[a,b]$ $\implies$ $f$ is integrable on $[a,b]$, **and the limit is
the same for every choice of sample points.** That independence is what makes the definition well
posed — without it the symbol would not name a single number.

**Geometric meaning:** **signed** area — area above the $x$-axis minus area below. It equals the
geometric area only when $f\ge0$; otherwise use $\int\lvert f\rvert$.

---

## Properties of the Definite Integral

$$\int_a^b c\,dx = c(b-a) \qquad \int_a^b[f\pm g] = \int_a^b f \pm \int_a^b g \qquad \int_a^b cf = c\int_a^b f$$

$$\int_a^b f + \int_b^c f = \int_a^c f \qquad \int_a^a f=0 \qquad \int_b^a f = -\int_a^b f$$

The last is a **definition**, not a theorem — Riemann sums presume $a<b$. It is chosen so that
additivity holds for every ordering of $a,b,c$.

**Comparison:** if $m\le f(x)\le M$ on $[a,b]$, then $\quad m(b-a)\le\int_a^bf\le M(b-a)$

This bounds integrals you cannot evaluate. It is loose when $f$ varies a lot: for
$\int_0^2\frac{dx}{1+x^3}$ it gives only $\tfrac29\le I\le 2$, against a true value of $1.0900$.
Splitting the interval and bounding each piece tightens it — which is what a Riemann sum does.

**Symmetry:** $f$ odd on $[-a,a]$ $\implies \int_{-a}^{a}f=0$. $f$ even $\implies \int_{-a}^{a}f=2\int_0^a f$.

---

## Average Value and the MVT for Integrals

$$f_{\text{avg}} = \frac{1}{b-a}\int_a^b f(x)\,dx$$

**MVT for Integrals:** $f$ continuous on $[a,b]$ $\implies \exists\,c\in[a,b]$ with $f(c)=f_{\text{avg}}$.

A continuous function attains its own average. **This is the theorem Week 9 uses to prove the
Fundamental Theorem** — it is the most important result on this sheet.

*Example: $f=3x^2-2$ on $[0,3]$ has average $7$, attained uniquely at $c=\sqrt3\approx1.7321$.*

---

## Areas You Should Recognise Without Computing

| Integral | Value | Why |
|---|---|---|
| $\int_a^b c\,dx$ | $c(b-a)$ | Rectangle |
| $\int_0^6\lvert x-3\rvert dx$ | $9$ | Two triangles |
| $\int_{-3}^{3}\sqrt{9-x^2}\,dx$ | $\dfrac{9\pi}{2}\approx14.1372$ | Semicircle, $r=3$ |
| $\int_{-1}^{1}x\,dx$ | $0$ | Odd — but the **area** is $1$ |

---

## Common Errors

| ❌ Wrong | ✅ Right |
|---------|---------|
| Treating $\int_a^b f$ as geometric area when $f$ changes sign | It is **signed** area; use $\int\lvert f\rvert$ or split at the roots |
| Treating $R_n$, $L_n$, $M_n$ as equal for finite $n$ | They agree only in the limit $n\to\infty$ |
| Off-by-one in the sums | $R_n$ runs $i=1..n$; $L_n$ runs $i=0..n-1$ |
| Reading $\int_b^a f = -\int_a^b f$ as a theorem | It is a **convention**, adopted to preserve additivity |
| Using comparison bounds without checking monotonicity | The $m$ and $M$ must be the true extremes on $[a,b]$ |
| Reaching for an antiderivative | **Not yet.** The FTC is Week 9; this week everything is sums, geometry, or bounds |

---

## Week 8 Schedule

| Day | Event | Topic |
|-----|-------|-------|
| Monday | **Quiz 08** + Lecture 1 | Sigma notation, Riemann sums, the area and distance problems |
| Tuesday | Lecture 2 | The definite integral: definition and integrability |
| Wednesday | Lecture 3 + **PS 8 released** (12:00) | Properties, comparison, average value, MVT for Integrals |
| Friday | **Lab 08** | Convergence rates, sample-point independence, numerical integrator |

**Next week:** the Fundamental Theorem of Calculus — where all of this collapses into
"antidifferentiate and subtract."

---

*MATH 141 · Week 8 · Reference · © CSE Department*
