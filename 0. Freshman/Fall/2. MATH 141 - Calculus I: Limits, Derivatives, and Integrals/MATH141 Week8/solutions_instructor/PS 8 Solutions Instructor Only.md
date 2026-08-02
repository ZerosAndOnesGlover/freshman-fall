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

## Part A — Sigma Notation and Riemann Sums (25 pts)

**A1 (6 pts, 2 each).**

**(a)** $\sum_{i=1}^8(4i-3)=4\sum i-3\sum1=4\cdot\dfrac{8(9)}{2}-3(8)=144-24=\mathbf{120}$

**(b)** $\sum_{i=1}^5(i^2+2i)=\dfrac{5(6)(11)}{6}+2\cdot\dfrac{5(6)}{2}=55+30=\mathbf{85}$

**(c)** $\sum_{i=1}^n\dfrac{2i}{n}=\dfrac2n\sum i=\dfrac2n\cdot\dfrac{n(n+1)}{2}=\mathbf{n+1}$

*(Verified: $n=3\to4$, $n=7\to8$, $n=50\to51$.)*

---

**A2 (6 pts).** $f(x)=x^2+1$ on $[0,2]$, $n=4$, $\Delta x=0.5$.

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

**A3 (7 pts).** $f(x)=2x+1$ on $[1,3]$. $\Delta x=\dfrac2n$, $x_i=1+\dfrac{2i}n$.

$$R_n=\sum_{i=1}^n f(x_i)\Delta x=\sum_{i=1}^n\left[2\left(1+\frac{2i}n\right)+1\right]\cdot\frac2n=\frac2n\sum_{i=1}^n\left[3+\frac{4i}n\right]$$

$$=\frac2n\left[3n+\frac4n\cdot\frac{n(n+1)}2\right]=\frac2n\left[3n+2(n+1)\right]=\frac2n[5n+2]=\mathbf{10+\frac4n}$$

$$\lim_{n\to\infty}R_n=\mathbf{10}$$

**Geometric check:** trapezoid with parallel sides $f(1)=3$ and $f(3)=7$, width $2$:
$\dfrac{3+7}{2}(2)=10$ ✓

*(Verified: $R_1=14$, $R_2=12$, $R_{10}=10.4$, $R_{1000}=10.004$ — matching $10+4/n$ exactly.)*

**Marking:** 2 for $\Delta x$ and $x_i$, 3 for the closed form, 1 for the limit, 1 for the geometric
check.

---

**A4 (6 pts).** $v(t)=2t+3$ on $[0,4]$, $n=4$, $\Delta t=1$. Midpoints $0.5,1.5,2.5,3.5$ give
$v$-values $4,6,8,10$.

$$M_4=1(4+6+8+10)=\mathbf{28}\text{ m}$$

**Exact (trapezoid):** $v(0)=3$, $v(4)=11$, so $\dfrac{3+11}{2}(4)=\mathbf{28}$ m ✓

**Why exact here (3 of the 6 pts).** On each subinterval the midpoint rectangle has height
$v(\text{mid})$, which for a **linear** $v$ equals the average of the two endpoint values. The
rectangle therefore has exactly the area of the trapezoid it replaces: the triangle it cuts off
above the line on one side is congruent to the one it adds below on the other.

**Not general.** The cancellation depends on $v$ being straight. For any $v$ with nonzero curvature
the two triangles differ, and $M_n$ carries an error proportional to $v''$ — which is why $M_4$ in
A2 was close but not exact.

---

## Part B — Properties of the Definite Integral (25 pts)

**B1 (7 pts).**

**(a)** $\int_{-2}^54\,dx=4(5-(-2))=4(7)=\mathbf{28}$ — a rectangle. *(2 pts)*

**(b)** $\int_0^6\lvert x-3\rvert dx$: two right triangles, each with legs $3$ and $3$, area
$\tfrac12(3)(3)=4.5$ each. Total $=\mathbf 9$. *(2 pts; verified numerically: $9.000000$)*

**(c)** Upper half of $x^2+y^2=9$: $\tfrac12\pi(3)^2=\mathbf{\dfrac{9\pi}{2}}\approx14.1372$.
*(3 pts; verified: $14.13716694$)*

---

**B2 (6 pts, 1.5 each).**

**(a)** $\int_1^6f=\int_1^3f+\int_3^6f=4+(-2)=\mathbf 2$ *(additivity)*

**(b)** $\int_6^1f=-\int_1^6f=\mathbf{-2}$ *(orientation)*

**(c)** $\int_1^6[3f-2g]=3(2)-2(7)=6-14=\mathbf{-8}$ *(linearity)*

**(d)** $\int_3^3f=\mathbf 0$ *(degenerate interval)*

*Each part isolates one property deliberately. A student who gets (c) right but (b) wrong has
linearity without orientation — note it, it recurs in Week 9's variable-limit problems.*

---

**B3 (6 pts).** $f(x)=\dfrac{1}{1+x^3}$ on $[0,2]$.

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

**B4 (6 pts).** $f(x)=3x^2-2$ on $[0,3]$.

$\int_0^3(3x^2-2)dx=[x^3-2x]_0^3=27-6=21$, so $f_{\text{avg}}=\dfrac{21}{3}=\mathbf 7$.

MVT for integrals: $3c^2-2=7\implies c^2=3\implies c=\sqrt3\approx\mathbf{1.7321}$.

Reject $c=-\sqrt3$: it is outside $[0,3]$. Since $f$ is strictly increasing on $[0,3]$, this $c$ is
**unique**.

*(Verified: average $=7.000000$.)*

*The question says "every $c$" — students must address whether there are others. 1 pt for that.*

---

## Part C — Exact Areas from the Definition (20 pts)

**C1 (10 pts).** $f(x)=x^3$ on $[0,1]$: $\Delta x=\dfrac1n$, $x_i=\dfrac in$.

$$R_n=\sum_{i=1}^n\left(\frac in\right)^3\cdot\frac1n=\frac1{n^4}\sum_{i=1}^n i^3=\frac1{n^4}\left[\frac{n(n+1)}2\right]^2=\frac{n^2(n+1)^2}{4n^4}=\frac{(n+1)^2}{4n^2}$$

$$\lim_{n\to\infty}\frac{(n+1)^2}{4n^2}=\lim_{n\to\infty}\frac{1}{4}\left(1+\frac1n\right)^2=\mathbf{\frac14}$$

**Marking:** 2 for $\Delta x$ and $x_i$, 2 for pulling out $1/n^4$, 3 for the summation formula and
simplification, 3 for the limit. **Any use of an antiderivative scores 0** — see the note in the
marking scheme.

---

**C2 (5 pts).**

| $n$ | $R_n=\dfrac{(n+1)^2}{4n^2}$ | Error |
|---|---|---|
| $10$ | $0.302500$ | $5.25\times10^{-2}$ |
| $1000$ | $0.250500$ | $5.00\times10^{-4}$ |
| $100\,000$ | $0.250005$ | $5.00\times10^{-6}$ |

**Rate:** each $100\times$ increase in $n$ cuts the error by $100\times$ — the error is
$\mathbf{O(1/n)}$, i.e. **first order**.

Algebraically, $R_n-\tfrac14=\dfrac{2n+1}{4n^2}\approx\dfrac{1}{2n}$, which matches: at $n=1000$ the
prediction is $5.0\times10^{-4}$ ✓

*Full marks require identifying $O(1/n)$, not merely observing that the error shrinks. Students who
give the exact error formula $\tfrac{2n+1}{4n^2}$ have done more than asked — note it.*

---

**C3 (5 pts).** For continuous $f$ on $[a,b]$, every sample point $x_i^*$ lies in a subinterval of
width $\Delta x=\tfrac{b-a}{n}$. On that subinterval, $f$ attains a minimum $m_i$ and a maximum $M_i$
(EVT, Week 6), and **every** choice of sample point gives a value between them. So every Riemann sum
is trapped between the lower sum $\sum m_i\Delta x$ and the upper sum $\sum M_i\Delta x$.

As $n\to\infty$ the subintervals shrink, and **uniform continuity** on the closed bounded interval
forces $M_i-m_i\to0$ uniformly. Upper and lower sums therefore converge to the same limit, and the
squeeze traps every intermediate choice at that same value.

**Why the definition needs this.** $\int_a^b f$ is *defined* as $\lim_{n\to\infty}\sum f(x_i^*)\Delta x$
with $x_i^*$ **arbitrary**. If different sample-point rules gave different limits, that expression
would not name a single number and the symbol $\int_a^b f$ would be meaningless. Sample-point
independence is not a bonus property — it is what makes the definition well posed.

*Award 3 for the squeeze argument, 2 for the well-posedness point. Students who only say "they all
converge to the area" have assumed what is being asked — 1 of 5.*

---

## Part D — Conceptual and Proof (30 pts)

**D1 (8 pts).**

$$\int_a^b f(x)\,dx=\lim_{n\to\infty}\sum_{i=1}^{n}f(x_i^*)\,\Delta x,\qquad \Delta x=\frac{b-a}{n},\quad x_i^*\in[x_{i-1},x_i]$$

| Symbol | Contribution |
|---|---|
| $\Delta x$ | The width of each rectangle — shrinks to zero as $n$ grows |
| $f(x_i^*)$ | The height, sampled somewhere inside the $i$-th subinterval |
| $\sum$ | Total signed area of the $n$ rectangles: a finite, computable approximation |
| $\lim$ | Passes from approximation to exact value |

**Why $x_i^*$ must be arbitrary (4 of the 8 pts).** Fixing it at, say, the right endpoint would give a
perfectly usable *definition* — but a weaker theorem, and a fragile one. Leaving it arbitrary means
the definition asserts that **all** sampling rules agree, so any convenient rule may be used in a
proof and any other in a computation. That is what licenses using midpoints numerically while
reasoning with right endpoints symbolically, and it is what C3 establishes.

---

**D2 (8 pts).** When $f<0$ on part of $[a,b]$, the heights $f(x_i^*)$ are negative there, so those
rectangles contribute **negatively**. The integral is therefore the **net signed area**: area above
the axis minus area below.

**Explicit example:** $f(x)=x$ on $[-1,1]$.

$$\int_{-1}^{1}x\,dx=0$$

by odd symmetry (or by the two triangles cancelling), while the geometric area of the region between
the graph and the axis is $\tfrac12(1)(1)+\tfrac12(1)(1)=\mathbf 1$.

To recover geometric area, integrate $\lvert f\rvert$: $\int_{-1}^{1}\lvert x\rvert dx=1$ ✓

*Any correct sign-changing example is acceptable ($\sin x$ on $[0,2\pi]$: integral $0$, area $4$).
Award 4 for the explanation, 4 for a worked example showing **both** numbers.*

---

**D3 (7 pts).** Riemann sums are built with $\Delta x=\dfrac{b-a}{n}$ and a partition running from
$a$ up to $b$ — the construction **presumes $a<b$**. Nothing in the definition assigns a value when
the limits are reversed, so $\int_b^a f$ is not defined until we say what it means. Any convention
is available to us; we are choosing, not deducing.

**Why this one.** Interval additivity $\int_a^b+\int_b^c=\int_a^c$ is proved for $a<b<c$. With the
sign convention it holds for **every** ordering of $a,b,c$ — including $c<a$, where a naive reading
would be nonsense. Check $a=0$, $b=5$, $c=2$: $\int_0^5+\int_5^2=\int_0^5-\int_2^5=\int_0^2$ ✓

**What breaks without it.** Every theorem stated with additivity would need case analysis on the
ordering of its endpoints, and FTC Part 2 — $\int_a^b F'=F(b)-F(a)$, whose right-hand side flips
sign automatically when $a$ and $b$ swap — would fail for $b<a$. The convention is chosen precisely
so the algebra matches the notation.

*Full marks require both halves: that it is a definition **and** the additivity motivation. Students
who answer only "because the area is negative" have described the convention, not justified it — 2
of 7.*

---

**D4 (7 pts).** Let $f$ be odd and continuous on $[-a,a]$.

Split: $\displaystyle\int_{-a}^{a}f=\int_{-a}^{0}f+\int_{0}^{a}f$.

Partition $[0,a]$ into $n$ equal subintervals with sample points $x_i^*$, and partition $[-a,0]$
into $n$ subintervals with the **reflected** sample points $-x_i^*$. Both partitions have the same
width $\Delta x=\tfrac an$.

Since $f$ is odd, $f(-x_i^*)=-f(x_i^*)$, so the two Riemann sums are

$$\sum_{i=1}^n f(-x_i^*)\Delta x=-\sum_{i=1}^n f(x_i^*)\Delta x$$

for every $n$. Taking $n\to\infty$ — legitimate because continuity guarantees both limits exist and
are sample-point independent (C3) — gives

$$\int_{-a}^{0}f=-\int_{0}^{a}f \qquad\Longrightarrow\qquad \int_{-a}^{a}f=0\;\;\square$$

*(Sanity check: $\int_{-1}^{1}x\,dx=0$ and $\int_{-\pi}^{\pi}\sin x\,dx=0$.)*

*Marking: 2 for the split, 3 for the reflected partition and the odd identity, 2 for justifying the
limit step. A purely pictorial "the areas cancel" earns 2 — it is the right idea without the
argument. Week 10's substitution $u=-x$ gives this in two lines; mention it when returning the set.*

---

*MATH 141 · Week 8 · PS 8 Solutions · Instructor copy — do not distribute*
