# MATH 141 · Problem Set 8 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

**Total: 100 points.** All numerical figures below were verified by computation.

---

## Marking Scheme

Point values are printed per problem on the problem set. Within each problem, split the marks:

- **Method (≈60%).** Correct technique named and set up: the right rule or property, hypotheses
  checked where the theorem requires it, and the symbolic work shown before any numerical evaluation.
- **Execution (≈40%).** Correct algebra and simplification, correct final form, and any domain
  restrictions stated.

A bare answer with no working earns at most the execution marks — and in proof problems ("show
that", "prove"), no marks at all, since the reasoning *is* the deliverable.

**Carry-through.** Penalise a given error once. If the student proceeds correctly from their own
wrong intermediate value, award the downstream marks in full.

### Common errors in this problem set

**1. Using the FTC.** It has not been proved yet. Part C in particular must be done from the
definition; a student who writes $\int_0^1 x^3 = [x^4/4]_0^1$ has answered a different question and
earns **0 for C1**, however correct the number. Say so on the problem set when you assign it.

**2. Treating the definite integral as 'area' unconditionally.** $\int f$ is *signed* area — regions
below the axis contribute negatively. Total geometric area needs $\lvert f\rvert$ or splitting at
the roots.

**3. Off-by-one in the sample points.** $R_n$ uses $i=1..n$; $L_n$ uses $i=0..n-1$. The commonest
arithmetic slip in Part A.

**4. Asserting monotonicity without checking.** B3 needs the integrand's max and min on $[0,2]$,
which requires knowing it is decreasing there — not merely evaluating at the endpoints and hoping.

---

*(Revised 2026-09-26: the set was cut to 8 problems. The solutions below follow the new numbering; B3 in the common errors is now Problem 5, and Part C is now Problem 7.)*

---

## Problem 1 — Sigma Notation (8)

**(a)** $\sum_{i=1}^8(4i-3)=4\sum i-3\sum1=4\cdot\dfrac{8(9)}{2}-3(8)=144-24=\mathbf{120}$

**(b)** $\sum_{i=1}^n\dfrac{2i}{n}=\dfrac2n\sum i=\dfrac2n\cdot\dfrac{n(n+1)}{2}=\mathbf{n+1}$

*(Verified: $n=3\to4$, $n=7\to8$, $n=50\to51$.)*

---

## Problem 2 — Left, Right and Midpoint Sums (14)

$f(x)=x^2+1$ on $[0,2]$, $n=4$, $\Delta x=0.5$.

$f$-values: $f(0)=1$, $f(0.5)=1.25$, $f(1)=2$, $f(1.5)=3.25$, $f(2)=5$

| | Sum | Value | Error vs $\tfrac{14}{3}\approx4.6667$ |
|---|---|---|---|
| **(a)** $R_4$ | $0.5[1.25+2+3.25+5]$ | $\mathbf{5.75}$ | $+1.083$ |
| **(b)** $L_4$ | $0.5[1+1.25+2+3.25]$ | $\mathbf{3.75}$ | $-0.917$ |
| **(c)** $M_4$ | $0.5[1.0625+1.5625+2.5625+4.0625]$ | $\mathbf{4.625}$ | $-0.042$ |

**Ranking (2 of the 6 pts):** $M_4$ is by far the most accurate, then $L_4$, then $R_4$.

**Why:** $f$ is **increasing** on $[0,2]$, so right endpoints overestimate every rectangle and left
endpoints underestimate every one. The midpoint rule's errors partially cancel within each
subinterval — for a function with modest curvature it is roughly an order of magnitude better, and
here it is 26× closer than $R_4$.

*A student who ranks correctly but justifies it with "midpoints are usually better" gets 1 of the 2.
The monotonicity argument is the content.*

---

## Problem 3 — A Riemann Sum in Closed Form (14)

$f(x)=2x+1$ on $[1,3]$. $\Delta x=\dfrac2n$, $x_i=1+\dfrac{2i}n$.

$$R_n=\sum_{i=1}^n f(x_i)\Delta x=\sum_{i=1}^n\left[2\left(1+\frac{2i}n\right)+1\right]\cdot\frac2n=\frac2n\sum_{i=1}^n\left[3+\frac{4i}n\right]$$

$$=\frac2n\left[3n+\frac4n\cdot\frac{n(n+1)}2\right]=\frac2n\left[3n+2(n+1)\right]=\frac2n[5n+2]=\mathbf{10+\frac4n}$$

$$\lim_{n\to\infty}R_n=\mathbf{10}$$

**Geometric check:** trapezoid with parallel sides $f(1)=3$ and $f(3)=7$, width $2$:
$\dfrac{3+7}{2}(2)=10$ ✓

*(Verified: $R_1=14$, $R_2=12$, $R_{10}=10.4$, $R_{1000}=10.004$ — matching $10+4/n$ exactly.)*

**Marking:** 2 for $\Delta x$ and $x_i$, 3 for the closed form, 1 for the limit, 1 for the geometric
check.

---

## Problem 4 — Integrals from Geometry (14)

**(a)** $\int_0^6\lvert x-3\rvert dx$: two right triangles, each with legs $3$ and $3$, area
$\tfrac12(3)(3)=4.5$ each. Total $=\mathbf 9$. *(7 pts; verified numerically: $9.000000$)*

**(b)** Upper half of $x^2+y^2=9$: $\tfrac12\pi(3)^2=\mathbf{\dfrac{9\pi}{2}}\approx14.1372$.
*(7 pts; verified: $14.13716694$)*

---

## Problem 5 — Bounding an Integral (12)

$f(x)=\dfrac{1}{1+x^3}$ on $[0,2]$.

$1+x^3$ is strictly increasing on $[0,2]$, so $f$ is strictly **decreasing** there. Hence
$M=f(0)=1$ and $m=f(2)=\tfrac19$.

$$\frac19(2)\le\int_0^2\frac{dx}{1+x^3}\le 1(2)\qquad\Longrightarrow\qquad \mathbf{\frac29\le\int_0^2\frac{dx}{1+x^3}\le 2}$$

**Tightness (2 of the 6 pts).** The bracket $[0.222,\,2]$ is very loose — a factor of 9 wide. The
true value is $\mathbf{1.0900}$, comfortably inside but near neither end.

The comparison property uses a single $m$ and $M$ for the whole interval, so it is only sharp when
the integrand barely varies. Here $f$ falls from $1$ to $\tfrac19$, and the bound pays for that
range. Splitting $[0,2]$ into subintervals and bounding each separately tightens it quickly — which
is exactly the idea a Riemann sum formalises.

---

## Problem 6 — Average Value (12)

$f(x)=2x+1$ on $[0,4]$. The region under the graph is a trapezoid with parallel sides $f(0)=1$ and
$f(4)=9$ and width $4$: $\int_0^4(2x+1)\,dx=\tfrac12(1+9)(4)=20$. So $f_{\text{avg}}=\dfrac{20}{4}=\mathbf 5$.

MVT for integrals: $2c+1=5\implies c=\mathbf 2$. Since $f$ is strictly increasing, this $c$ is **unique**.

*(Revised 2026-09-26: the old function $3x^2-2$ could only be integrated with the FTC (Week 9) or a long
Riemann-sum limit. 4 for the integral, 4 for the average, 3 for $c$, 1 for addressing "every $c$".)*

---

## Problem 7 — An Exact Area from the Definition (16)

$f(x)=x^3$ on $[0,1]$: $\Delta x=\dfrac1n$, $x_i=\dfrac in$.

$$R_n=\sum_{i=1}^n\left(\frac in\right)^3\cdot\frac1n=\frac1{n^4}\sum_{i=1}^n i^3=\frac1{n^4}\left[\frac{n(n+1)}2\right]^2=\frac{n^2(n+1)^2}{4n^4}=\frac{(n+1)^2}{4n^2}$$

$$\lim_{n\to\infty}\frac{(n+1)^2}{4n^2}=\lim_{n\to\infty}\frac{1}{4}\left(1+\frac1n\right)^2=\mathbf{\frac14}$$

**Marking:** 2 for $\Delta x$ and $x_i$, 2 for pulling out $1/n^4$, 3 for the summation formula and
simplification, 3 for the limit. **Any use of an antiderivative scores 0** — see the note in the
marking scheme.

---

## Problem 8 — Signed Area (10)

When $f<0$ on part of $[a,b]$, the heights $f(x_i^*)$ are negative there, so those
rectangles contribute **negatively**. The integral is therefore the **net signed area**: area above
the axis minus area below.

**Explicit example:** $f(x)=x$ on $[-1,1]$.

$$\int_{-1}^{1}x\,dx=0$$

by odd symmetry (or by the two triangles cancelling), while the geometric area of the region between
the graph and the axis is $\tfrac12(1)(1)+\tfrac12(1)(1)=\mathbf 1$.

To recover geometric area, integrate $\lvert f\rvert$: $\int_{-1}^{1}\lvert x\rvert dx=1$ ✓

*Any correct sign-changing example is acceptable ($\sin x$ on $[0,2\pi]$: integral $0$, area $4$).
Award 5 for the explanation, 5 for a worked example showing **both** numbers.*

---

*MATH 141 · Week 8 · Problem Set 8 Solutions · © CSE Department*
