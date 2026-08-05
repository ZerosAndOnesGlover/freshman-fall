# MATH 142 · Calculus II
## Week 6 · Reference Sheet
### Sequences

---

## Definitions

A **sequence** is a function on the positive integers, $\{a_n\}$.

$$\lim_{n\to\infty}a_n=L \iff \forall\varepsilon>0\ \exists N:\ n>N \implies |a_n-L|<\varepsilon$$

**Converges** if such an $L$ exists (it is unique); **diverges** otherwise.

> **"Diverges" means "fails to converge", not "blows up".** $(-1)^n$ is bounded and divergent.

| | |
|---|---|
| convergent $\implies$ bounded | **true** |
| bounded $\implies$ convergent | **false** ($(-1)^n$) |
| **bounded + monotone $\implies$ convergent** | **true** |

---

## The Function Connection

> If $a_n=f(n)$ and $\displaystyle\lim_{x\to\infty}f(x)=L$, then $\displaystyle\lim_{n\to\infty}a_n=L$.

**One way only.** The converse is false: $a_n=\sin(\pi n)\equiv0$ converges; $\sin(\pi x)$ does not.

**So:** use L'Hôpital by passing to the function. **Never conclude a sequence diverges because the function does.**

---

## The Geometric Sequence

$$\lim_{n\to\infty}r^n = \begin{cases}0 & |r|<1\\ 1 & r=1\\ \text{diverges} & r\le-1\ \text{or}\ r>1\end{cases}$$

**Converges exactly for $-1<r\le1$.** *(Verified.)* — the most-used fact in Weeks 7–10.

---

## Techniques

| Form | Method |
|---|---|
| ratio of polynomials | divide by the dominant power |
| $\frac00$, $\frac\infty\infty$ | pass to the function, L'Hôpital |
| $1^\infty$, $\infty^0$, $0^0$ | **take logarithms**, then exponentiate |
| $\infty-\infty$ with roots | multiply by the conjugate |
| bounded oscillating factor | **squeeze** |
| factorials / exponentials | **growth hierarchy** |

**Squeeze:** $b_n\le a_n\le c_n$ with $b_n,c_n\to L$ gives $a_n\to L$.
**Corollary:** $|a_n|\to0\implies a_n\to0$. *(Limit zero only — $|(-1)^n|\to1$ but $(-1)^n$ diverges.)*

---

## Standard Limits

| | |
|---|---|
| $\dfrac{\ln n}{n^p}\to0$ | $(p>0)$ |
| $n^{1/n}\to1$ | |
| $\left(1+\dfrac xn\right)^n\to e^x$ | |
| $\dfrac{n^p}{a^n}\to0$ | $(a>1)$ |
| $\dfrac{a^n}{n!}\to0$ | |
| $\dfrac{n!}{n^n}\to0$ | |
| $\sqrt{n+1}-\sqrt n\to0$ | |
| $n\sin\frac1n\to1$ | |

*(all verified)*

---

## The Growth Hierarchy

$$\boxed{\ln n \;\ll\; n^p \;\ll\; a^n \;\ll\; n! \;\ll\; n^n}$$

At $n=20$: $\;3.0,\quad 400\ (p{=}2),\quad 1.05\times10^{6}\ (a{=}2),\quad 2.43\times10^{18},\quad 1.05\times10^{26}$

*(verified)* — **twenty-six orders of magnitude.**

**This is CS 101's complexity ordering**, and this is where it is proved.

**Why $\frac{a^n}{n!}\to0$:** past $n>2a$, every new factor is $<\frac12$, so the tail is dominated by a geometric sequence.

---

## Stirling's Approximation

$$n!\sim\sqrt{2\pi n}\left(\frac ne\right)^n$$

Ratio $n!/\text{Stirling}$: $1.0168$ at $n{=}5$, $1.0084$ at $10$, $1.0042$ at $20$, $1.00083$ at $100$ — matching the correction $1+\frac{1}{12n}$ to five figures. *(Verified.)*

**Its $\sqrt{2\pi}$ comes from Wallis' product — Lab 1.**

Consequence: $\dfrac{n!\,e^n}{n^n\sqrt n}\to\sqrt{2\pi}$.

---

## Monotone Convergence

> **An increasing sequence bounded above converges. A decreasing sequence bounded below converges.**

**Two finite checks replace an infinite question**, and the limit need not be known.

**It is the completeness axiom.** $1,\ 1.4,\ 1.41,\ 1.414,\ldots$ is increasing, bounded, rational — and its limit $\sqrt2$ is not rational. **$\mathbb{Q}$ fails this theorem; $\mathbb{R}$ is defined by satisfying it.**

**Already used in Week 3:** the comparison test worked because $\int_a^T f$ increases in $T$ and is bounded above.

---

## Recursive Sequences

$$a_1=c,\qquad a_{n+1}=g(a_n)$$

> **Step 1: prove convergence** (monotone + bounded).
> **Step 2: then solve $L=g(L)$.**

**Step 1 is not optional.** $a_{n+1}=2a_n$, $a_1=1$ diverges, yet $L=2L$ gives $L=0$. *(Verified.)*

### The fixed point criterion

| $g'(L)$ | Behaviour |
|---|---|
| $\lvert g'(L)\rvert>1$ | **repelling** — no convergence |
| $0<\lvert g'(L)\rvert<1$ | **linear** — error $\times\lvert g'(L)\rvert$ per step |
| $g'(L)=0$ | **quadratic** — error squares; **digits double** |

### Measured (Lab 6)

**Babylonian** $a_{n+1}=\frac12\left(a_n+\frac2{a_n}\right)$ for $\sqrt2$, from $a_0=1$:

correct digits $= 1,\ 2,\ 5,\ 11,\ 24,\ \mathbf{48}$ — and $\dfrac{e_n}{e_{n-1}^2}\to\dfrac{1}{2\sqrt2}=0.353553$.

**Linear alternative** $a_{n+1}=a_n-\frac{a_n^2-2}{4}$: $g'(\sqrt2)=1-\frac{\sqrt2}{2}$, and consecutive error ratios $\to 2+\sqrt2 = 3.41421$.

**Logistic map** $x_{n+1}=rx_n(1-x_n)$: $x^\ast=1-\frac1r$ with $g'(x^\ast)=2-r$, so **stable exactly for $1<r<3$**. Measured orbits: period 1 at $r{=}2.5$, period 2 at $3.2$, period 4 at $3.5$, chaotic at $3.9$.

*(all verified)*

---

## Worked Examples

| Limit | Method | Value |
|---|---|---|
| $\frac{3n^3-n}{7n^3+2n^2}$ | dominant power | $\frac37$ |
| $\frac{\ln n}{\sqrt n}$ | L'Hôpital on $f$ | $0$ |
| $n^{1/n}$ | logs | $1$ |
| $\left(1+\frac2n\right)^{3n}$ | logs | $e^6$ |
| $\frac{\cos n}{n^2}$ | squeeze | $0$ |
| $\frac{5^n}{n!}$ | hierarchy | $0$ |
| $\sqrt{n^2+n}-n$ | conjugate | $\frac12$ |
| $(-1)^n\frac{n}{n+1}$ | — | **diverges** |

---

## The Bridge to Week 7

$$\sum_{n=1}^\infty a_n \;:=\; \lim_{N\to\infty} s_N,\qquad s_N = a_1+\cdots+a_N$$

**A series is a sequence of partial sums.** Everything this week transfers directly, and the first test next week — the **Integral Test** — joins it to Week 3.

---

*MATH 142 · Week 6 · Reference Sheet*
