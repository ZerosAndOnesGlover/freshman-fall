# MATH 142 · Calculus II
## Problem Set 9 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every radius and endpoint verified symbolically.

> **Marking philosophy.** **An interval, with correct brackets, is the deliverable in Part B.** A
> correct radius with untested endpoints is at most half marks — the endpoints are where three weeks
> of convergence tests actually get used.
>
> **Every endpoint test must be named.** "It converges" is not an argument.

---

## Part A — Radius (5 pts each)

### A1 (5) $\;\sum\frac{n\,x^n}{3^n}$

$$\left|\frac{c_{n+1}}{c_n}\right| = \frac{n+1}{3^{n+1}}\cdot\frac{3^n}{n} = \frac13\cdot\frac{n+1}{n}\longrightarrow\frac13 \implies \boxed{R=3}$$

*Verified.*

### A2 (5) $\;\sum\frac{x^n}{(n!)^2}$

$$\left|\frac{c_{n+1}}{c_n}\right| = \frac{(n!)^2}{((n+1)!)^2} = \frac{1}{(n+1)^2}\longrightarrow0 \implies \boxed{R=\infty}$$

*Verified.*

### A3 (5) $\;\sum\frac{(3n)!}{(n!)^3}x^n$

$$\left|\frac{c_{n+1}}{c_n}\right| = \frac{(3n+3)!}{(3n)!}\cdot\frac{(n!)^3}{((n+1)!)^3} = \frac{(3n+1)(3n+2)(3n+3)}{(n+1)^3}\longrightarrow 27$$

$$\boxed{R=\frac{1}{27}}$$

*Verified.*

*Marking: **4 of the 5 for the factorial cancellation.** The three consecutive factors over $(n+1)^3$ each tend to 3, giving $3^3$.*

### A4 (5) $\;\sum\frac{x^{3n}}{n\,5^n}$ — missing terms

**The coefficient formula does not apply** ($c_n=0$ unless $3\mid n$). Use the terms:

$$\left|\frac{a_{n+1}}{a_n}\right| = \left|\frac{x^{3n+3}}{(n+1)5^{n+1}}\cdot\frac{n5^n}{x^{3n}}\right| = \frac{|x|^3}{5}\cdot\frac{n}{n+1}\longrightarrow\frac{|x|^3}{5}$$

Convergence needs $|x|^3<5$:

$$\boxed{R = 5^{1/3}\approx1.710}$$

*Verified.*

*Marking: **3 of the 5 for recognising that the coefficient formula fails** and working with the terms. A student who used $\left|\frac{c_{n+1}}{c_n}\right|=\frac15$ and reported $R=5$ has made exactly the error the problem tests.*

---

## Part B — Interval of Convergence (6 pts each)

*Standard marking: 2 radius, 1 open interval, 1 per endpoint tested (with the test named), 1 for the final interval with correct brackets.*

### B1 (6) $\;\sum\frac{x^n}{\sqrt n}$

$R=1$; open interval $(-1,1)$.

- **$x=1$:** $\sum\frac{1}{\sqrt n}$ — $p$-series, $p=\frac12\le1$. **Diverges.**
- **$x=-1$:** $\sum\frac{(-1)^n}{\sqrt n}$ — Alternating Series Test: $\frac{1}{\sqrt n}$ decreasing, $\to0$. **Converges** (conditionally).

$$\boxed{[-1,1)}$$

### B2 (6) $\;\sum\frac{(x-2)^n}{n3^n}$

$\left|\frac{c_{n+1}}{c_n}\right|\to\frac13$, so $R=3$; centre $a=2$; open interval $|x-2|<3 \iff (-1,5)$.

- **$x=5$:** $(x-2)^n=3^n$, giving $\sum\frac1n$. **Diverges.**
- **$x=-1$:** $(x-2)^n = (-3)^n$, giving $\sum\frac{(-1)^n}{n}$. **Converges.**

$$\boxed{[-1,5)}$$

*Verified.*

### B3 (6) $\;\sum\frac{(-1)^n(x+1)^n}{n^2}$

$R=1$; centre $a=-1$; open interval $|x+1|<1\iff(-2,0)$.

- **$x=0$:** $\sum\frac{(-1)^n}{n^2}$ — **converges absolutely.**
- **$x=-2$:** $(x+1)^n = (-1)^n$, giving $\sum\frac{(-1)^n(-1)^n}{n^2}=\sum\frac{1}{n^2}$. **Converges.**

$$\boxed{[-2,0]}$$

*Verified.*

*Marking: **the sign bookkeeping at $x=-2$ is where marks go** — two $(-1)^n$ factors combining to $+1$.*

### B4 (6) $\;\sum n!\,(x-1)^n$

$\left|\frac{c_{n+1}}{c_n}\right| = n+1\to\infty$, so $R=0$.

$$\boxed{\text{Converges only at } x=1}$$

*Verified.*

*Marking: 4 for $R=0$, **2 for stating the conclusion as a single point** rather than an interval. There are no endpoints to test.*

### B5 (6) $\;\sum\frac{(2x-1)^n}{n}$

**Rewrite first:** $2x-1 = 2\left(x-\tfrac12\right)$, so the series is $\sum\frac{2^n(x-\frac12)^n}{n}$ — **centre $\frac12$**, with effective coefficients $\frac{2^n}{n}$:

$$\left|\frac{c_{n+1}}{c_n}\right| = \frac{2^{n+1}}{n+1}\cdot\frac{n}{2^n}\longrightarrow2 \implies R = \frac12$$

Open interval: $\left|x-\tfrac12\right|<\tfrac12 \iff (0,1)$.

- **$x=1$:** $2x-1=1$, giving $\sum\frac1n$. **Diverges.**
- **$x=0$:** $2x-1=-1$, giving $\sum\frac{(-1)^n}{n}$. **Converges.**

$$\boxed{[0,1)}$$

*Marking: **3 of the 6 for extracting the centre $\frac12$ and radius $\frac12$.** Reporting "$R=1$, interval $(-1,1)$ in the variable $2x-1$" is the standard error — the question asks for the interval **in $x$**.*

---

## Part C — Building Series (6 pts each)

### C1 (6) $\;\frac{1}{1+3x}$

Substitute $-3x$ into the geometric series:

$$\frac{1}{1-(-3x)} = \sum_{n=0}^\infty(-3x)^n = \sum_{n=0}^\infty(-1)^n3^nx^n, \qquad |3x|<1$$

$$\boxed{R=\tfrac13}$$

*Verified: $1-3x+9x^2-27x^3+\cdots$*

### C2 (6) $\;\frac{x}{1-x^2}$

$$= x\sum_{n\ge0}(x^2)^n = \sum_{n=0}^\infty x^{2n+1}, \qquad \boxed{R=1}$$

*Verified: $x+x^3+x^5+x^7+\cdots$*

### C3 (6) $\;\ln(1-x)$

$\frac{1}{1-t} = \sum t^n$, so $\int_0^x\frac{dt}{1-t} = -\ln(1-x)$, giving

$$\boxed{\ln(1-x) = -\sum_{n=1}^\infty\frac{x^n}{n}}, \qquad R=1$$

*Verified: $-x-\frac{x^2}{2}-\frac{x^3}{3}-\cdots$*

**Endpoints:** at $x=1$, $-\sum\frac1n$ **diverges**; at $x=-1$, $-\sum\frac{(-1)^n}{n}$ **converges**.

$$\text{Interval } [-1,1)$$

**Comparison with $\ln(1+x)$**, whose interval is $(-1,1]$: **the two are mirror images**, as they must be, since $\ln(1-x)$ is $\ln(1+u)$ with $u=-x$. **The included endpoint flips sides.**

*Marking: 3 derivation, 2 endpoints, **1 for the comparison** (the question asked).*

### C4 (6) $\;\sum n^2x^n$

Start from $\sum_{n\ge1}nx^n = \frac{x}{(1-x)^2}$. Differentiate:

$$\sum_{n\ge1}n^2x^{n-1} = \frac{d}{dx}\frac{x}{(1-x)^2} = \frac{1+x}{(1-x)^3}$$

Multiply by $x$:

$$\boxed{\sum_{n=1}^\infty n^2x^n = \frac{x(1+x)}{(1-x)^3}}\qquad(|x|<1)$$

*Verified: the CAS returns $-\frac{x(x+1)}{(x-1)^3}$ with the side condition $-1<x<1$ — the same expression, and note **the CAS attaches the domain automatically**, which is the radius doing its work.*

*Marking: 2 for starting from the known series, 3 for differentiating correctly, 1 for the radius.*

### C5 (6) $\;\int_0^x\frac{dt}{1+t^4}$

$$\frac{1}{1+t^4} = \sum_{n\ge0}(-1)^nt^{4n} \qquad(|t|<1)$$

Integrating term by term:

$$\boxed{\int_0^x\frac{dt}{1+t^4} = \sum_{n=0}^\infty\frac{(-1)^nx^{4n+1}}{4n+1} = x-\frac{x^5}{5}+\frac{x^9}{9}-\cdots}, \qquad R=1$$

*Verified against the CAS expansion.*

*Marking: 2 substitution, 3 integration, 1 radius. **Worth remarking:** the elementary antiderivative of $\frac{1}{1+t^4}$ exists but requires factoring $1+t^4$ over the reals into two quadratics and two partial-fraction pieces — several lines of Week 2. **The series takes two.**

---

## Part D — Concept (10 pts each)

### D1 (10) — why endpoints need separate work

**(a)** The Ratio Test on $a_n = c_n(x-a)^n$ gives

$$\left|\frac{a_{n+1}}{a_n}\right| = \left|\frac{c_{n+1}}{c_n}\right|\cdot|x-a| \longrightarrow \frac{1}{R}\cdot|x-a|$$

At $|x-a|=R$ this is exactly $\frac RR = 1$ — **regardless of the $c_n$.** Since $L=1$ is the Ratio Test's inconclusive case (Week 8), **the test can never decide an endpoint.**

**(b)** With centre 0 and $R=1$:

| Series | $x=-1$ | $x=+1$ | Interval |
|---|---|---|---|
| $\sum x^n$ | $\sum(-1)^n$, terms $\not\to0$, **div** | $\sum1$, **div** | $(-1,1)$ |
| $\sum\frac{x^n}{n}$ | alternating harmonic, **conv** | harmonic, **div** | $[-1,1)$ |
| $\sum\frac{(-1)^nx^n}{n}$ | $\sum\frac1n$, **div** | $\sum\frac{(-1)^n}{n}$, **conv** | $(-1,1]$ |
| $\sum\frac{x^n}{n^2}$ | **conv** (absolutely) | $p$-series $p=2$, **conv** | $[-1,1]$ |

*(all verified)*

**(c)** **The radius is determined by the growth rate of $|c_n|$ and says nothing about the endpoints.** All four series above have identical radii and four different intervals — so the endpoint behaviour is a strictly finer question, decided by the coefficients themselves and only by direct testing.

*Marking: 3 + 5 + 2. **(a) must show the $|x-a|$ factoring out** and evaluating to 1 at the boundary — that is why the silence is structural, not accidental.*

### D2 (10) — term-by-term operations

**(a)** If $f(x)=\sum c_n(x-a)^n$ has radius $R>0$, then on $(a-R,a+R)$ $f$ is differentiable and may be differentiated and integrated term by term; **both resulting series have the same radius $R$.**

**(b)** **The licensing property is absolute convergence inside the radius** (Lecture 1 §7).

**Why it is needed:** differentiating or integrating an infinite sum term by term is an **interchange of two limiting processes**, and Week 8 showed that rearranging or recombining a merely conditionally convergent series can change its sum — or destroy it. **Absolute convergence is precisely the hypothesis under which such manipulations are guaranteed valid.**

**(c)** $\frac{1}{1+t} = \sum_{n\ge0}(-1)^nt^n$ on $|t|<1$. Integrating from 0 to $x$:

$$\ln(1+x) = \sum_{n=0}^\infty\frac{(-1)^nx^{n+1}}{n+1} = \sum_{n=1}^\infty\frac{(-1)^{n+1}x^n}{n}$$

**Original endpoints:** at $x=\pm1$, $\sum(\pm1)^n$ has terms not tending to 0 — **both diverge**, interval $(-1,1)$.

**New endpoints:** at $x=1$, $\sum\frac{(-1)^{n+1}}{n}$ **converges**; at $x=-1$, $-\sum\frac1n$ **diverges**. Interval $(-1,1]$.

**(d)** Integrating divides the $n$-th coefficient by roughly $n$, **making the terms smaller** — which can turn a divergent endpoint series into a convergent one, as it did at $x=1$. Differentiating multiplies by roughly $n$, **making terms larger**, which can destroy convergence at an endpoint.

**Hence: integration tends to gain endpoints; differentiation tends to lose them.** *(The radius is unaffected either way, since a factor of $n$ does not change $\lim|c_n|^{1/n}$.)*

*Marking: 2 + 3 + 3 + 2. **(b) is the discriminating part** and must invoke Week 8's rearrangement result, not merely assert that the theorem requires it.*

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A (4 × 5) | 20 | Radius, including missing terms |
| B (5 × 6) | 30 | Full intervals, both endpoints, shifted centres |
| C (5 × 6) | 30 | Substitution, differentiation, integration |
| D (2 × 10) | 20 | Why endpoints are separate; the licence |
| **Total** | **100** | |

---

## Diagnostic Notes

| Question | Weakness | Bites in |
|---|---|---|
| **A4 / B5** | Applying the coefficient formula mechanically | Week 10 ($\sin$, $\cos$ have missing terms) |
| **B2 / B3 / B5** | Losing the centre | Midterm 2 |
| **B3** | Sign bookkeeping at a negative endpoint | Midterm 2 |
| **D2(b)** | Not seeing absolute convergence as a licence | Week 10, throughout |

**Week 10 constructs Taylor series** and then differentiates and integrates them freely — including to obtain a series for $\int e^{-x^2}dx$, the integral from Week 0. **Every one of those manipulations rests on D2(b).**

---

*MATH 142 · Week 9 · PS 9 Solutions · Instructor Only*
