# MATH 142 · Calculus II
## Week 7 · Reference Sheet
### Series: Geometric, $p$-Series, Integral and Comparison Tests

---

## Definition

$$\sum_{n=1}^\infty a_n := \lim_{N\to\infty}s_N,\qquad s_N = \sum_{n=1}^N a_n$$

**A series is a sequence of partial sums.** All of Week 6 applies.

**Convergence depends only on the tail** — adding or removing finitely many terms changes the value, never the verdict.

---

## The Two Summable Families

### Geometric

$$\sum_{n=0}^\infty ar^n = \frac{a}{1-r}\quad (|r|<1);\qquad \text{diverges for } |r|\ge1$$

**Use $\dfrac{\text{first term}}{1-r}$** — it survives any starting index.

*(Verified: $\sum_{n\ge0}2^{-n}=2$, $\sum_{n\ge1}2^{-n}=1$, $\sum_{n\ge0}3\cdot4^{-n}=4$.)*

### Telescoping

Partial-fraction first, then write out both ends.

$$\sum_{n\ge1}\frac{1}{n(n+1)} = 1,\qquad \sum_{n\ge1}\frac{1}{n(n+2)} = \frac34,\qquad \sum_{n\ge1}\frac{1}{n(n+3)} = \frac{11}{18}$$

*(all verified)* — **if the gap is $k$, then $k$ terms survive at each end.**

---

## The $n$-th Term Test

> If $\sum a_n$ converges then $a_n\to0$.
> **Contrapositive:** $a_n\not\to0 \implies$ **diverges.**

> ### ⚠ It can only ever prove divergence.
> $a_n\to0$ tells you **nothing**. The harmonic series and $\sum\ln\frac{n+1}{n}$ both have terms
> tending to 0 and both diverge.

**Check it first — it costs five seconds.**

---

## The Harmonic Series

$$\sum\frac1n = \infty, \qquad H_N \approx \ln N+\gamma,\qquad \gamma = 0.5772156649\ldots$$

**Oresme's proof (c. 1350):** group in blocks of $2^k$ terms; each block exceeds $\frac12$.

*(Verified: $H_N-(\ln N+\gamma)\to0$ like $\frac{1}{2N}$ — measured $N\times\text{diff}\to0.5$.)*

| sum reached | terms needed |
|---|---|
| 10 | $1.2\times10^{4}$ |
| 20 | $2.7\times10^{8}$ |
| 50 | $2.9\times10^{21}$ |
| 100 | $1.5\times10^{43}$ |

*(computed)* — **no computation will ever see it diverge.**

---

## The Integral Test

> $f$ **positive**, **continuous**, **decreasing** on $[1,\infty)$ with $a_n=f(n)$:
> $$\sum a_n \text{ converges} \iff \int_1^\infty f \text{ converges}$$

**All three hypotheses are required.** "Decreasing" need only hold eventually, but must be checked.

**It is Monotone Convergence plus a rectangle picture.**

### The remainder estimate

$$\boxed{\int_{N+1}^\infty f \;\le\; R_N \;\le\; \int_N^\infty f},\qquad R_N = S-s_N$$

**A free, two-sided error bound.** And **averaging the two bounds raises the order from 1 to 3:**

| $N$ | raw error | averaged |
|---|---|---|
| $10$ | $9.5\times10^{-2}$ | $2.9\times10^{-4}$ |
| $10^2$ | $1.0\times10^{-2}$ | $3.3\times10^{-7}$ |
| $10^3$ | $1.0\times10^{-3}$ | $3.3\times10^{-10}$ |
| $10^4$ | $1.0\times10^{-4}$ | $3.3\times10^{-13}$ |

*(measured for $\sum n^{-2}$ — raw falls by 10 per decade, averaged by 1000)*

---

## $p$-Series

$$\boxed{\sum_{n=1}^\infty\frac{1}{n^p} \text{ converges} \iff p>1}$$

**The same statement as Week 3's improper-integral $p$-test**, transferred by the Integral Test.

| $p$ | value |
|---|---|
| $1$ | **diverges** |
| $2$ | $\frac{\pi^2}{6}=1.644934$ |
| $3$ | $\zeta(3)=1.202057$ — **no closed form known** |
| $4$ | $\frac{\pi^4}{90}$ |

*(verified)* — **even $p$ has closed forms; no odd $p\ge3$ does.** $\zeta(3)$ was proved irrational by Apéry (1978); $\zeta(5)$ is still open.

**Basel converges at order 1:** error $\approx\frac1N$, so 10 digits needs $10^{10}$ terms. *(Measured: $N\times\text{error}\to1$.)*

---

## Comparison Tests

**Both require non-negative terms.**

### Direct

$0\le a_n\le b_n$ eventually:
- $\sum b_n$ converges $\implies\sum a_n$ converges
- $\sum a_n$ diverges $\implies\sum b_n$ diverges

**The direction is everything.** Bounding above by a divergent series proves nothing.

### Limit

$a_n,b_n>0$ and $L=\lim\frac{a_n}{b_n}$ with $0<L<\infty$ $\implies$ **same fate.**

**Strategy: keep the dominant terms top and bottom, discard the rest.**

### Benchmarks

$$\sum\frac{1}{n^p}\ (p>1),\qquad \sum ar^n\ (|r|<1),\qquad \sum\frac{1}{n(\ln n)^p}\ (p>1)$$

### Worked verdicts

| Series | Compare with | Verdict |
|---|---|---|
| $\frac{1}{n^2+1}$ | $n^{-2}$ | converges |
| $\frac{1}{2^n+1}$ | $2^{-n}$ | converges |
| $\frac{n+1}{n^3+2}$ | $n^{-2}$ | converges |
| $\frac{1}{\sqrt{n^2+1}}$ | $n^{-1}$ | **diverges** |
| $\frac{\sin^2 n}{n^2}$ | $n^{-2}$ | converges |
| $\frac{\ln n}{n^2}$ | $n^{-3/2}$ | converges |
| $\frac{1}{n^{1+1/n}}$ | $n^{-1}$ | **diverges** |

*(all corroborated numerically)*

**Trading $\ln n$ for $n^\varepsilon$:** a logarithm never changes convergence for $p\ne1$; it matters only at the boundary.

---

## Two Closed Forms Worth Knowing

$$\sum_{n=1}^\infty\frac{\sin^2 n}{n^2} = \frac{\pi-1}{2} = 1.0707963268\ldots \qquad \sum_{n=1}^\infty\frac{\ln n}{n^2} = -\zeta'(2) = 0.9375482543\ldots$$

*(both verified)* — but **comparison decided both in one line without them.**

---

## A Check That Caught a Library

`mpmath`'s `nsum` returns $0.936715596751$ for $\sum\frac{\ln n}{n^2}$. **This is wrong** by $8.3\times10^{-4}$ (true value $0.937548254316$), and wrong by $7.8\times10^{-5}$ for $\sum\frac{\sin^2n}{n^2}$.

**How to catch it with no prior knowledge:**

> **For positive terms, no partial sum can exceed the sum.**

The partial sum to $N=10^6$ is $0.937533$ — larger than the claimed total. *One line, from the definition.*

**Sixth week running that a machine has given a confident wrong answer.** The defence is always the same: **know a property the answer must have, and check it.**

---

## Strategy

| Series looks like | Try |
|---|---|
| terms $\not\to0$ | $n$-th Term Test — done |
| $ar^n$ | geometric |
| terms cancel | telescoping |
| $n^{-p}$ | $p$-series |
| rational in $n$ | limit comparison |
| $f(n)$, $f$ decreasing | Integral Test — **plus an error bound** |
| bounded oscillation over $n^{-p}$ | direct comparison |
| $\ln n$ at $p=1$ | Integral Test, $u=\ln x$ |

---

*MATH 142 · Week 7 · Reference Sheet*
