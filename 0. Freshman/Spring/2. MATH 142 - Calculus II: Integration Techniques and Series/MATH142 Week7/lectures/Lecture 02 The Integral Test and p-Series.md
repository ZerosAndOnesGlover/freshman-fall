# MATH 142 · Calculus II
## Week 7 · Lecture 2 (Tuesday)
### The Integral Test, and $p$-Series

**Date:** Tuesday 2 March 2027 · 11:00–11:50 · Week 7

---

**Reading:** Stewart §11.3 | Apostol Ch. 10 §10.12

---

## 1. A Sum Is Almost an Integral

$$\sum_{n=1}^\infty a_n \qquad\text{versus}\qquad \int_1^\infty f(x)\,dx$$

If $a_n = f(n)$, these are the same accumulation done two ways — **one by rectangles of width 1, one continuously.** It should not be a surprise that they converge together.

> **Integral Test.** Let $f$ be **positive**, **continuous** and **decreasing** on $[1,\infty)$, and
> let $a_n=f(n)$. Then
> $$\sum_{n=1}^\infty a_n \ \text{converges} \iff \int_1^\infty f(x)\,dx \ \text{converges.}$$

### All three hypotheses are needed

| Hypothesis | Why |
|---|---|
| **positive** | so partial sums increase and monotone convergence applies |
| **continuous** | so the integral exists |
| **decreasing** | so the rectangles bracket the area — this is the geometry |

**"Decreasing" need only hold eventually**, since convergence depends only on the tail. But it must be checked — usually by showing $f'<0$.

> **This is Week 6's Monotone Convergence Theorem doing the work.** The partial sums increase (terms
> are positive); if the integral is finite it bounds them above; bounded and increasing implies
> convergent. **The test is that theorem plus a picture.**

### The picture, which is the proof

Draw $f$ and rectangles of width 1.

- **Rectangles with height $f(n)$ placed to the *right* of $x=n$ sit below the curve**, so
$$a_2+a_3+\cdots+a_{N} \le \int_1^{N}f(x)\,dx$$
- **Rectangles placed to the *left* sit above it**, so
$$\int_1^{N+1}f(x)\,dx \le a_1+a_2+\cdots+a_N$$

**Both inequalities need $f$ decreasing.** Together they trap the partial sums between two integrals, and the conclusion follows.

---

## 2. $p$-Series

The immediate payoff. Apply the test to $f(x)=x^{-p}$, which is positive, continuous and decreasing on $[1,\infty)$ for $p>0$:

$$\boxed{\sum_{n=1}^\infty\frac{1}{n^p} \ \text{converges} \iff p>1}$$

**because $\int_1^\infty x^{-p}dx$ converges exactly when $p>1$ — the $p$-test from Week 3, Lecture 1.**

*(Verified: $p=1$ diverges; $p=2$ gives $\frac{\pi^2}{6}$; $p=4$ gives $\frac{\pi^4}{90}$.)*

> **You already knew this.** The $p$-series test *is* the improper-integral $p$-test, transferred by
> the Integral Test. **The two halves of the course meet exactly here.**

**For $p\le0$ the terms do not tend to 0**, so the $n$-th Term Test disposes of it immediately.

### Values, and the limits of what is known

| $p$ | $\sum n^{-p}$ |
|---|---|
| $1$ | **diverges** |
| $2$ | $\dfrac{\pi^2}{6} = 1.6449\ldots$ |
| $3$ | $\zeta(3) = 1.2021\ldots$ — **no closed form known** |
| $4$ | $\dfrac{\pi^4}{90}$ |

*(Verified: a CAS returns $\zeta(3)$ for $p=3$ and closed forms only for even $p$.)*

**Every even $p$ has a closed form; no odd $p\ge3$ does.**

**$\zeta(3)$ was proved irrational by Roger Apéry in June 1978** — and essentially nothing else about it is known. *(Whether $\zeta(5)$ is irrational is still open.)*

> **The reception of that proof is worth a moment.** Apéry's presentation was so terse and so
> unexpected that **much of the audience dismissed it as flawed.** Henri Cohen, Hendrik Lenstra and
> Alfred van der Poorten suspected otherwise, and spent **two months verifying it line by line**
> before it was accepted.
>
> **A correct proof, disbelieved until three people checked it.** That is the habit this course has
> been drilling since Week 0, practised at the highest level of the subject.

> **This is the asymmetry from the Overview, made concrete.** We prove $\sum n^{-3}$ converges in one
> line. Its value has resisted three centuries of effort. **Convergence and evaluation are different
> problems, and only the first is generally tractable.**

---

## 3. Worked Examples

### Example 1 — the harmonic series again

$f(x)=\frac1x$ is positive, continuous, decreasing. $\int_1^\infty\frac{dx}{x}$ **diverges**, so $\sum\frac1n$ **diverges** ✓ — recovering Oresme's result in one line.

### Example 2

$$\sum_{n=2}^\infty\frac{1}{n\ln n}$$

$f(x)=\frac{1}{x\ln x}$ is positive and decreasing on $[2,\infty)$. From **Week 3, Lecture 1, Example 7**:

$$\int_2^\infty\frac{dx}{x\ln x} = \infty \implies \textbf{the series diverges}$$

### Example 3

$$\sum_{n=2}^\infty\frac{1}{n(\ln n)^2}$$

Same function family; **Week 3 showed $\int_2^\infty\frac{dx}{x(\ln x)^2} = \frac{1}{\ln2}$ converges**, so **the series converges.**

> **These two are the borderline pair from Lab 3**, where no power of $x$ could separate them and no
> computation could tell them apart at $T=10^{100}$. **The Integral Test settles both in one line
> each** — and it is the same substitution $u=\ln x$ that did it then.

### Example 4 — hypotheses must be checked

$$\sum_{n=1}^\infty\frac{\sin^2 n}{n^2}$$

**The Integral Test does not apply** — $f(x)=\frac{\sin^2x}{x^2}$ is not decreasing (it wobbles). **You must not use it here.** *(Comparison handles this tomorrow; the point today is to notice the hypothesis fails.)*

---

## 4. The Remainder Estimate — Where the Test Earns Its Keep

The Integral Test does more than answer yes or no. **It bounds how much of the sum you are missing.**

Let $s_N=\sum_{n=1}^N a_n$ and let $R_N = S-s_N = \sum_{n=N+1}^\infty a_n$ be the **remainder**. The same rectangle picture gives

$$\boxed{\int_{N+1}^{\infty}f(x)\,dx \;\le\; R_N \;\le\; \int_N^\infty f(x)\,dx}$$

**Two-sided, computable bounds on an infinite tail.** This is the only error estimate you have met that comes free with the convergence proof.

### Example 5 — the Basel series

For $\sum\frac{1}{n^2}$ we have $\int_N^\infty x^{-2}dx = \frac1N$, so

$$\frac{1}{N+1}\;\le\;R_N\;\le\;\frac1N$$

*(Verified at $N=10,100,1000$: the true remainders $0.09517,\ 0.009950,\ 0.0009995$ lie inside the bounds every time.)*

**So $s_N$ underestimates the sum by about $\frac1N$** — which means ten correct digits would need $N\approx10^{10}$ terms. *(Measured: $N\times R_N\to1$.)*

### The trick that makes this usable

**Both bounds are available, so use their average.** Take

$$S \approx s_N + \frac12\left(\frac{1}{N+1}+\frac1N\right)$$

**The error collapses:**

| $N$ | raw error | averaged error |
|---|---|---|
| $10$ | $9.5\times10^{-2}$ | $2.9\times10^{-4}$ |
| $10^2$ | $1.0\times10^{-2}$ | $3.3\times10^{-7}$ |
| $10^3$ | $1.0\times10^{-3}$ | $3.3\times10^{-10}$ |
| $10^4$ | $1.0\times10^{-4}$ | $3.3\times10^{-13}$ |

*(Measured. The raw error falls by 10 per decade — order 1. The averaged error falls by **1000** per decade — **order 3**.)*

> **One extra line of arithmetic buys six orders of magnitude at $N=10^3$**, and the advantage grows.
> **This is Lab 3's lesson inverted:** there, order of convergence made a method useless; here,
> improving the order makes a useless method excellent. **Lab 7 makes you measure it.**

---

## 5. What To Take From This Lecture

1. **Integral Test:** $f$ positive, continuous, **decreasing** ⟹ series and integral share a fate.
2. **It is Monotone Convergence plus a picture**, and all three hypotheses matter.
3. **$p$-series converges iff $p>1$** — the same statement as Week 3's $p$-test.
4. **Convergence is provable; the value usually is not.** $\zeta(3)$ is the standing example.
5. **The remainder is trapped between two integrals** — a free, two-sided error bound.
6. **Averaging those bounds raises the order from 1 to 3.**

---

*Next: Wednesday — Comparison Tests for Series*
