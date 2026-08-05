# MATH 142 · Calculus II
## Week 10 · Reference Sheet
### Taylor and Maclaurin Series

---

## The Coefficients Are Forced

$$\boxed{c_n = \frac{f^{(n)}(a)}{n!}} \qquad\Longrightarrow\qquad f(x) \sim \sum_{n=0}^\infty\frac{f^{(n)}(a)}{n!}(x-a)^n$$

**Maclaurin** = Taylor at $a=0$. **The representation, if it exists, is unique.**

---

## Taylor's Theorem with Lagrange Remainder

$$f(x) = \underbrace{\sum_{k=0}^n\frac{f^{(k)}(a)}{k!}(x-a)^k}_{P_n(x)} + R_n(x), \qquad R_n(x) = \frac{f^{(n+1)}(c)}{(n+1)!}(x-a)^{n+1}$$

for some $c$ between $a$ and $x$. **At $n=0$ this is the Mean Value Theorem.**

$$\boxed{f = \text{its Taylor series} \iff R_n\to0}$$

**Practical bound:** if $\left|f^{(n+1)}\right|\le M$ **on the interval between $a$ and $x$**, then

$$\left|R_n(x)\right|\le\frac{M\,|x-a|^{n+1}}{(n+1)!}$$

**Say which interval $M$ holds on.** For $\sin$ and $\cos$, $M=1$ everywhere; for $e^x$, $M$ depends on the interval.

**Why $\sin$, $\cos$, $e^x$ equal their series everywhere:** $\frac{|x|^{n+1}}{(n+1)!}\to0$ — Week 6's hierarchy, $\frac{a^n}{n!}\to0$.

### ⚠ A series need not equal its function

$$f(x)=\begin{cases}e^{-1/x^2}&x\ne0\\0&x=0\end{cases}$$

has $f^{(n)}(0)=0$ for all $n$, so its Maclaurin series is $\boldsymbol{0}$ — converging everywhere, to the wrong function. **$f$ agrees with it at exactly one point.**

*(Verified: $\frac{f(x)}{x^{10}}$ takes $18.8,\ 1.4\times10^{-4},\ 3.7\times10^{-34},\ 2.0\times10^{-161}$ at $x=0.5,0.2,0.1,0.05$ — $f$ vanishes faster than every power. And $f(1)=e^{-1}=0.3679\ne0$.)*

---

## The Library

| Function | Series | $R$ |
|---|---|---|
| $e^x$ | $\sum\frac{x^n}{n!}$ | $\infty$ |
| $\sin x$ | $\sum\frac{(-1)^nx^{2n+1}}{(2n+1)!}$ | $\infty$ |
| $\cos x$ | $\sum\frac{(-1)^nx^{2n}}{(2n)!}$ | $\infty$ |
| $\frac{1}{1-x}$ | $\sum x^n$ | $1$ |
| $\ln(1+x)$ | $\sum_{n\ge1}\frac{(-1)^{n+1}x^n}{n}$ | $1$ |
| $\arctan x$ | $\sum\frac{(-1)^nx^{2n+1}}{2n+1}$ | $1$ |
| $(1+x)^k$ | $\sum\binom knx^n$ | $1$ |

*(all verified)*

$$\sqrt{1+x} = 1+\frac x2-\frac{x^2}8+\frac{x^3}{16}-\frac{5x^4}{128}+\cdots \qquad \frac{1}{\sqrt{1+x}} = 1-\frac x2+\frac{3x^2}8-\frac{5x^3}{16}+\cdots$$

> **Manipulate, do not differentiate.** Substitute, multiply by a power, multiply two series,
> differentiate or integrate term by term. **Odd functions have only odd powers** — a free check.

---

## Two Error Bounds — Use the Better One

| | Requires | Bound |
|---|---|---|
| **Lagrange** | a bound $M$ on $\lvert f^{(n+1)}\rvert$ over an interval | $\frac{M\lvert x-a\rvert^{n+1}}{(n+1)!}$ |
| **Alternating** (Week 8) | alternating series, terms decreasing | **the first omitted term** |

**The alternating estimate is easier and usually much tighter.**

*Measured for $\sin(0.5)$, dropping after the $x^5$ term: alternating bound $1.5501\times10^{-6}$ against a true error of $1.5447\times10^{-6}$ — **tight to 0.4%**. The Lagrange bound is typically loose by a factor of 3–10.*

**Term counts** (Lagrange, $\sin$ at $x=0.5$, target $10^{-10}$): $n=9$ gives $2.69\times10^{-10}$ (just misses), **$n=10$ gives $1.22\times10^{-11}$** — and since $\sin$ has only odd powers, that is **five nonzero terms**.

---

## Applications

### Limits

Substitute the series and read the leading power.

| Limit | Value |
|---|---|
| $\frac{\sin x - x}{x^3}$ | $-\frac16$ |
| $\frac{1-\cos x}{x^2}$ | $\frac12$ |
| $\frac{e^x-1-x}{x^2}$ | $\frac12$ |
| $\frac{x-\arctan x}{x^3}$ | $\frac13$ |
| $\frac{e^x-1-x-\frac{x^2}{2}}{x^3}$ | $\frac16$ |

*(all verified)* — **and the next term tells you the rate of approach**, which L'Hôpital does not.

### Non-elementary integrals — **Week 0's debt**

$$\int_0^1e^{-x^2}dx = \sum_{n=0}^\infty\frac{(-1)^n}{n!\,(2n+1)} = 1-\frac13+\frac1{10}-\frac1{42}+\cdots$$

| terms | error |
|---|---|
| $5$ | $6.6\times10^{-4}$ |
| $9$ | $1.3\times10^{-7}$ |
| $12$ | $7.8\times10^{-11}$ |
| $\mathbf{13}$ | $\mathbf{5.6\times10^{-12}}$ |

*(measured)* — **13 terms against Simpson's 128 evaluations in Lab 0.**

$$\int_0^1\frac{\sin x}{x}dx = \sum_{n=0}^\infty\frac{(-1)^n}{(2n+1)(2n+1)!} = 0.946083070367\ldots$$

**Six terms give eleven digits.** *(Measured.)*

### Coefficient extraction

To find $f^{(k)}(0)$ **without differentiating**: get the series, read off $c_k$, and use $f^{(k)}(0)=k!\,c_k$.

*Example: $f=x^2e^{x^3} = \sum\frac{x^{3n+2}}{n!}$; the $x^8$ coefficient is $\frac12$, so $f^{(8)}(0) = \frac{8!}{2} = 20160$.*

### Limiting cases in physics

$$(1-v^2/c^2)^{-1/2} = 1+\frac{v^2}{2c^2}+\frac{3v^4}{8c^4}+\cdots \implies K = \frac12mv^2+\frac{3mv^4}{8c^2}+\cdots$$

**The first term is Newtonian kinetic energy.**

---

## Why It Is All Legal

| Step | Licensed by |
|---|---|
| $f$ equals its Taylor series | **Week 10** — Taylor's theorem, $R_n\to0$ |
| integrate/differentiate term by term | **Week 9** — absolute convergence inside $R$ |
| absolute convergence permits rearrangement | **Week 8** — the rearrangement theorem |
| error $\le$ first omitted term | **Week 8** — alternating series estimate |

---

## How a Numerical Library Works

1. **Argument reduction** — use periodicity/symmetry to move $x$ into a small interval near the centre.
2. **Fixed-degree polynomial**, with the degree chosen once so the Lagrange bound guarantees accuracy across that interval.
3. **Reconstruct** using the symmetry.

**Step 1 is Week 9's lesson.** For $\arctan$, ten digits needs $\approx5\times10^9$ terms at $x=1$ and **17** at $x=\frac{1}{\sqrt3}$ — a factor of $3\times10^8$, purely from where you sit.

> **Taylor's theorem is the only method in this course that gives a rigorous bound *before* you run
> anything.** That is what shipping a library requires.

---

*MATH 142 · Week 10 · Reference Sheet*
