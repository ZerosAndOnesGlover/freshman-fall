# MATH 142 · Calculus II
## Week 3 · Reference Sheet
### Improper Integrals; Comparison Tests

---

## Definitions

**Type I — infinite interval**

$$\int_a^\infty f := \lim_{T\to\infty}\int_a^T f \qquad\qquad \int_{-\infty}^b f := \lim_{S\to-\infty}\int_S^b f$$

$$\int_{-\infty}^{\infty} f := \int_{-\infty}^{c}f + \int_c^{\infty}f$$

**Both halves must converge separately.**

**Type II — unbounded integrand**

$$\int_a^b f := \lim_{t\to a^+}\int_t^b f \quad\text{(bad point at }a) \qquad \int_a^b f := \lim_{t\to b^-}\int_a^t f \quad\text{(bad point at }b)$$

**Interior singularity at $c$:** split as $\int_a^c + \int_c^b$ and require **both** to converge.

**Converges** = the limit exists and is finite. Otherwise **diverges**.

> **Write the limit.** The notation is the argument.

---

## The Two $p$-Tests

$$\boxed{\int_1^\infty\frac{dx}{x^p}\ \text{converges}\iff p>1,\ \text{value } \frac{1}{p-1}}$$

$$\boxed{\int_0^1\frac{dx}{x^p}\ \text{converges}\iff p<1,\ \text{value } \frac{1}{1-p}}$$

**They point opposite ways, and the reason is the point:**

| | Need | Because |
|---|---|---|
| at $\infty$ | shrink **fast** | a slowly-decaying tail accumulates forever |
| at $0$ | blow up **slowly** | a violent spike accumulates instantly |

**$p=1$ diverges at both ends.** $1/x$ is the boundary and is on the wrong side of it twice.

**Consequence:** $\int_0^\infty x^{-p}dx$ **diverges for every $p$** — no exponent satisfies both.

---

## Standard Values

| Integral | Value |
|---|---|
| $\int_1^\infty \frac{dx}{x^2}$ | $1$ |
| $\int_1^\infty \frac{dx}{x^{3/2}}$ | $2$ |
| $\int_1^\infty \frac{dx}{x}$ | **diverges** |
| $\int_0^1 \frac{dx}{\sqrt x}$ | $2$ |
| $\int_0^1 \frac{dx}{x}$ | **diverges** |
| $\int_0^1 \ln x\,dx$ | $-1$ |
| $\int_0^\infty e^{-x}dx$ | $1$ |
| $\int_0^\infty xe^{-x}dx$ | $1$ |
| $\int_{-\infty}^{\infty}\frac{dx}{1+x^2}$ | $\pi$ |
| $\int_0^\infty e^{-x^2}dx$ | $\frac{\sqrt\pi}{2}$ |
| $\int_2^\infty\frac{dx}{x\ln x}$ | **diverges** |
| $\int_2^\infty\frac{dx}{x(\ln x)^2}$ | $\frac{1}{\ln 2}$ |

*(all verified)*

**Two useful limits:** $Te^{-T}\to0$ and $t\ln t\to0$ — both by L'Hôpital. **Exponential decay beats every power; every power beats a logarithm.**

---

## The Trap

$$\int_{-1}^{1}\frac{dx}{x^2}\ \overset{\text{wrong}}{=}\ \left[-\frac1x\right]_{-1}^{1} = -2$$

**Absurd** — the integrand is positive. FTC Part 2 requires continuity on $[a,b]$, and the integrand is undefined at $0$. **The integral diverges.**

> **Before evaluating any definite integral: is the integrand defined and bounded on the whole closed
> interval?** Check both endpoints and every interior point where a denominator vanishes, a logarithm
> hits zero, or a fractional power has a negative base. **Split at every bad point.**

**The $-2$ was a gift** — the impossible sign announced the error. Not every wrong answer will.

---

## Comparison Tests

**Both require $f\ge0$ near the limit point.**

### Direct Comparison

If $0\le f\le g$ eventually:

- $\int g$ converges $\implies \int f$ converges *(bound above by a convergent)*
- $\int f$ diverges $\implies \int g$ diverges *(bound below by a divergent)*

**The direction is everything.** Bounding above by a divergent function tells you nothing.

### Limit Comparison

If $f,g>0$ and $L = \lim\dfrac{f}{g}$:

| $L$ | Conclusion |
|---|---|
| $0<L<\infty$ | **same fate** — both converge or both diverge |
| $L=0$ | $\int g$ converges $\implies\int f$ converges |
| $L=\infty$ | $\int g$ diverges $\implies\int f$ diverges |

**Strategy: keep the dominant term top and bottom, discard the rest, compare with what remains.**

### Worked shapes

| Integral | Compare with | Verdict |
|---|---|---|
| $\int_1^\infty\frac{dx}{\sqrt{x^3+1}}$ | $x^{-3/2}$ | converges |
| $\int_1^\infty\frac{x+1}{x^3+x^2+1}dx$ | $x^{-2}$ | converges |
| $\int_1^\infty\frac{2+\sin x}{x}dx$ | $x^{-1}$ | diverges |
| $\int_1^\infty e^{-x^2}dx$ | $e^{-x}$ | converges |
| $\int_0^1\frac{dx}{\sqrt x\sqrt{1+x}}$ | $x^{-1/2}$ | converges |

*(all corroborated numerically)*

### Limitations

- **Never gives a value** — only a verdict, and sometimes a bound.
- **Needs $f\ge0$.** Sign-changing integrands wait for Week 8.
- **Cannot separate logarithmic near-misses.** No power decides $\frac{1}{x\ln x}$ against $\frac{1}{x(\ln x)^2}$; substitute $u=\ln x$ instead.

---

## What Convergence Does Not Follow From

- **$f\to0$ is not enough.** $\frac1x\to0$ and diverges. Speed is everything.
- **An unbounded region is not automatically infinite in area.** $\int_1^\infty\frac{dx}{x^2}=1$.
- **Symmetric cancellation is not convergence.** $\lim_{T\to\infty}\int_{-T}^{T}x\,dx = 0$, but $\int_{-\infty}^{\infty}x\,dx$ diverges.

---

## Lab 3: Why Numerics Cannot Decide This

$$F(T,p)=\int_1^T x^{-p}dx = \frac{1-T^{1-p}}{p-1}\ (p\neq1), \qquad \ln T\ (p=1)$$

| $T$ | $p=0.5$ | $p=0.99$ | $p=1$ | $p=1.01$ | $p=1.5$ | $p=2$ |
|---|---|---|---|---|---|---|
| $10^6$ | $1998$ | $14.82$ | $13.82$ | $12.90$ | $1.998$ | $0.999999$ |
| $10^{100}$ | $2\times10^{50}$ | $900$ | $230.3$ | $90.0$ | $2.0$ | $1.0$ |
| **limit** | $\infty$ | $\infty$ | $\infty$ | $\mathbf{100}$ | $2$ | $1$ |

**At $T=10^6$ the convergent column is the smallest of the three middle ones.**
**At $T=10^{100}$ — a googol — $p=1.01$ has reached only 90% of its limit.**

Meanwhile $p=2$ reaches 90% of its limit at $T=10$. **Both converge.**

**Divergence can be invisible too:** $p=0.5$ grows like $2\sqrt T$ (obvious); $p=1$ grows like $\ln T$ (invisible). And $\int_2^T\frac{dx}{x\ln x} = \ln\ln T - \ln\ln 2$ reaches only $5.81$ at $T=10^{100}$.

> **A finite computation cannot establish a statement about a limit.** The $p$-test does it in one line.

---

*MATH 142 · Week 3 · Reference Sheet*
