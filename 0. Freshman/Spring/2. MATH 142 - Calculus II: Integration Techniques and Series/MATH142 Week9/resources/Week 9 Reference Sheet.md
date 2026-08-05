# MATH 142 · Calculus II
## Week 9 · Reference Sheet
### Power Series; Radius and Interval of Convergence

---

## Definition and Structure

$$\sum_{n=0}^\infty c_n(x-a)^n$$

> **Exactly one holds:** converges only at $x=a$ ($R=0$); converges for all $x$ ($R=\infty$); or converges for $|x-a|<R$ and diverges for $|x-a|>R$.

**The convergence set is always an interval centred at $a$.**

---

## Finding the Radius

$$\boxed{R = \left(\lim_{n\to\infty}\left|\frac{c_{n+1}}{c_n}\right|\right)^{-1}}$$

$R=\infty$ if the limit is 0; $R=0$ if it is $\infty$.

> **Missing terms:** the coefficient formula fails when some $c_n=0$. **Apply the Ratio Test to
> consecutive nonzero terms, powers of $x$ included.** For $\sum\frac{x^{2n}}{3^n}$ the ratio is
> $\frac{x^2}{3}$, giving $R=\sqrt3$.

### Verified radii

| Series | $R$ |
|---|---|
| $\sum x^n$, $\sum\frac{x^n}{n}$, $\sum\frac{x^n}{n^2}$ | $1$ |
| $\sum n!\,x^n$ | $0$ |
| $\sum\frac{x^n}{n!}$, $\sum\frac{x^n}{(n!)^2}$ | $\infty$ |
| $\sum\frac{x^n}{n2^n}$ | $2$ |
| $\sum\frac{n\,x^n}{3^n}$ | $3$ |
| $\sum\frac{n^n}{n!}x^n$ | $\frac1e$ |
| $\sum\frac{(3n)!}{(n!)^3}x^n$ | $\frac1{27}$ |

*(all verified)* — the last two come from Week 6 limits.

---

## Endpoints

> **At $|x-a|=R$ the Ratio Test gives $L=1$ by construction. It can never decide an endpoint.**

**Procedure:** find $R$ → write $(a-R,a+R)$ → substitute each endpoint → test with Weeks 7–8 → report the interval.

### All four types occur, all with $R=1$

| Series | $x=-1$ | $x=+1$ | Interval |
|---|---|---|---|
| $\sum x^n$ | diverges | diverges | $(-1,1)$ |
| $\sum\frac{x^n}{n}$ | converges ($-\ln2$) | diverges | $[-1,1)$ |
| $\sum\frac{(-1)^nx^n}{n}$ | diverges | converges | $(-1,1]$ |
| $\sum\frac{x^n}{n^2}$ | converges ($-\frac{\pi^2}{12}$) | converges ($\frac{\pi^2}{6}$) | $[-1,1]$ |

*(all verified)* — **the radius does not determine the endpoints.**

**Shifted centre:** $\sum\frac{(x-3)^n}{n2^n}$ has $R=2$, centre 3, so $(1,5)$; at $x=5$ it is $\sum\frac1n$ (diverges), at $x=1$ it is $\sum\frac{(-1)^n}{n}$ (converges). **Interval $[1,5)$.**

> **Substituting the endpoint always cancels the geometric part.** What survives is governed by the
> rest of the coefficient.

**Inside $R$: absolutely convergent. At an endpoint: possibly only conditionally.**

---

## Term-by-Term Operations

> On $(a-R,a+R)$ a power series may be **differentiated and integrated term by term**, and both new
> series have **the same radius $R$**.

**The licence is absolute convergence inside the radius** — Week 8's result. **Endpoints are not preserved and must be rechecked**: integration tends to gain them, differentiation to lose them.

---

## The Library

| Function | Series | Interval |
|---|---|---|
| $\dfrac{1}{1-x}$ | $\sum_{n\ge0}x^n$ | $(-1,1)$ |
| $\dfrac{1}{1+x}$ | $\sum_{n\ge0}(-1)^nx^n$ | $(-1,1)$ |
| $\dfrac{1}{1+x^2}$ | $\sum_{n\ge0}(-1)^nx^{2n}$ | $(-1,1)$ |
| $\dfrac{1}{1-2x}$ | $\sum_{n\ge0}2^nx^n$ | $\left(-\frac12,\frac12\right)$ |
| $\ln(1+x)$ | $\sum_{n\ge1}\frac{(-1)^{n+1}x^n}{n}$ | $(-1,1]$ |
| $\ln(1-x)$ | $-\sum_{n\ge1}\frac{x^n}{n}$ | $[-1,1)$ |
| $\arctan x$ | $\sum_{n\ge0}\frac{(-1)^nx^{2n+1}}{2n+1}$ | $[-1,1]$ |
| $\dfrac{x}{(1-x)^2}$ | $\sum_{n\ge1}nx^n$ | $(-1,1)$ |
| $\dfrac{x(1+x)}{(1-x)^3}$ | $\sum_{n\ge1}n^2x^n$ | $(-1,1)$ |

*(all verified)*

**Setting $x=1$:** $\;\ln2 = 1-\frac12+\frac13-\cdots$ and $\;\frac\pi4 = 1-\frac13+\frac15-\cdots$ — **the two Week 8 series, explained.**

---

## Where You Evaluate Matters Enormously

For $\sum\frac{x^n}{n} = -\ln(1-x)$, terms needed for $10^{-10}$:

| $x$ | terms | $N(1-x)$ |
|---|---|---|
| $0.5$ | $29$ | $14.5$ |
| $0.9$ | $190$ | $19.0$ |
| $0.99$ | $1{,}988$ | $19.9$ |
| $0.999$ | $19{,}974$ | $20.0$ |
| $1.0$ | **never** | — |

*(measured)* — **$N\approx\frac{20}{1-x}$**: the cost blows up as $x\to R$.

**For $\arctan$, ten digits needs:**

| evaluation point | terms |
|---|---|
| $x=1$ (gives $\frac\pi4$) | $\approx5\times10^{9}$ |
| $x=\frac{1}{\sqrt3}$ (gives $\frac\pi6$) | $\mathbf{17}$ |

*(measured)* — **a factor of about 300 million**, from choosing where to sit inside the radius. **Week 10 exploits this systematically.**

---

## The Boundary Is Invisible to Computation

Partial sums $s_{200}$ of $\sum\frac{x^n}{n}$ ($R=1$):

| $x$ | $s_{200}$ | truth |
|---|---|---|
| $0.99$ | $4.557$ | converges to $4.605$ |
| $1.0$ | $5.878$ | **diverges** |
| $1.01$ | $9.541$ | **diverges** |
| $1.1$ | $1.1\times10^{7}$ | diverges |

*(measured)* — **nothing in the middle three numbers reveals which converge.** At $x=1.01$ divergence only becomes obvious around $N=1000$ ($s=2400$) and unmistakable by $N=5000$ ($8\times10^{19}$).

> **Third time in the course** — after Lab 3's $p$-test and Lab 7's harmonic series — **that a finite
> computation cannot locate a convergence boundary.** The Ratio Test does it exactly, in one line.

---

## Common Errors

1. **Reporting $R$ when the interval was asked for.**
2. **Assuming the two endpoints behave alike.** They are independent.
3. **Forgetting the centre** — $(1,5)$, not $(-2,2)$.
4. **Using the Ratio Test at an endpoint.** It is $L=1$ there by construction.
5. **Using the coefficient formula on a series with missing terms.**
6. **Forgetting to recheck endpoints after differentiating or integrating.**

---

*MATH 142 · Week 9 · Reference Sheet*
