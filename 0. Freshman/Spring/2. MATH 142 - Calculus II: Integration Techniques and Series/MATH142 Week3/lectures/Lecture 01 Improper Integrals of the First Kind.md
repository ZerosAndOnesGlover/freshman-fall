# MATH 142 · Calculus II
## Week 3 · Lecture 1 (Monday)
### Improper Integrals of the First Kind — Infinite Intervals

---

**Reading:** Stewart §7.8 | Apostol Ch. 10 §10.7
**Quiz 03** — this Monday, **covers Week 2** (trigonometric substitution, partial fractions)

---

## 1. Why This Needs a Definition At All

$$\int_1^\infty\frac{dx}{x^2}$$

**This symbol has no meaning yet.** Week 0's definition partitioned a *closed bounded* interval $[a,b]$ into $n$ pieces of width $\frac{b-a}{n}$ — and $\frac{\infty-1}{n}$ is not a number. Neither does FTC Part 2 help: there is no "$F(\infty)$" to evaluate.

So we must **extend** the definition, and the natural extension is a limit:

$$\boxed{\int_a^\infty f(x)\,dx \;:=\; \lim_{T\to\infty}\int_a^T f(x)\,dx}$$

The inner integral is an ordinary definite integral over $[a,T]$ — everything from Weeks 0–2 applies. **Then take one more limit.**

- If the limit exists and is **finite**, the integral **converges** to that value.
- Otherwise it **diverges** (to $\infty$, to $-\infty$, or by oscillation).

Similarly $\int_{-\infty}^b f := \lim_{S\to-\infty}\int_S^b f$.

### The two-sided case needs care

$$\int_{-\infty}^{\infty}f(x)\,dx := \int_{-\infty}^{c}f(x)\,dx + \int_c^{\infty}f(x)\,dx$$

for any convenient $c$, and **both halves must converge separately.**

> **You may not write $\lim_{T\to\infty}\int_{-T}^{T}f$.** That is a different (weaker) quantity — the
> *principal value*. For $f(x)=x$ it gives 0, because the halves cancel, even though
> $\int_0^\infty x\,dx = \infty$. **Symmetric cancellation is not convergence**, and a definition that
> allowed it would break the additivity property from Week 0.

---

## 2. The Method, and the Two Basic Examples

**Always write the limit down.** Marks are lost for computing $\int_1^T$ and then substituting $\infty$ without a $\lim$ symbol — the notation is the argument.

### Example 1 — convergent

$$\int_1^\infty\frac{dx}{x^2} = \lim_{T\to\infty}\int_1^T x^{-2}dx = \lim_{T\to\infty}\left[-\frac1x\right]_1^T = \lim_{T\to\infty}\left(1 - \frac1T\right) = \boxed{1}$$

*Verified symbolically: exactly 1.*

**A region of infinite length with area exactly 1.** The function shrinks fast enough that the tail contributes almost nothing.

### Example 2 — divergent

$$\int_1^\infty\frac{dx}{x} = \lim_{T\to\infty}\Big[\ln x\Big]_1^T = \lim_{T\to\infty}\ln T = \boxed{\infty}$$

*Verified symbolically: diverges.*

**This is the crucial contrast of the week.** Both integrands tend to 0; both regions are infinitely long. One has area 1 and one has infinite area.

And notice **how slowly it diverges**: $\ln T$. At $T = 10^{6}$ the area is only about 13.8. At $T=10^{100}$ it is 230. It grows forever, but so gently that no computation will ever make it look infinite.

> **That is the theme of Lab 3.** Divergence here is not dramatic. It is a function creeping upward
> at a rate no finite experiment can distinguish from settling down.

---

## 3. The $p$-Test

Generalising the two examples:

$$\boxed{\int_1^\infty\frac{dx}{x^p} = \begin{cases}\dfrac{1}{p-1} & p>1 \quad\text{(converges)}\\[8pt] \infty & p\le1\quad\text{(diverges)}\end{cases}}$$

**Derivation.** For $p\neq1$,

$$\int_1^T x^{-p}dx = \left[\frac{x^{1-p}}{1-p}\right]_1^T = \frac{T^{1-p}-1}{1-p}$$

As $T\to\infty$: if $p>1$ then $1-p<0$ so $T^{1-p}\to0$, leaving $\frac{-1}{1-p} = \frac{1}{p-1}$. If $p<1$ then $T^{1-p}\to\infty$ and it diverges. The case $p=1$ is Example 2, giving $\ln T\to\infty$.

*Verified symbolically: the CAS returns $\frac{1}{p-1}$ under the condition $p>1$, and $\infty$ at $p=1$.*

**Memorise the shape, not the formula:** *near infinity, you need the function to shrink faster than $1/x$.* And $1/x$ itself is on the wrong side of the line.

### The values are worth knowing

| $p$ | $\int_1^\infty x^{-p}dx$ |
|---|---|
| $\tfrac12$ | diverges |
| $1$ | diverges |
| $\tfrac32$ | $2$ |
| $2$ | $1$ |
| $3$ | $\tfrac12$ |

*(all verified)*

---

## 4. More Examples

### Example 3 — exponential decay

$$\int_0^\infty e^{-x}dx = \lim_{T\to\infty}\Big[-e^{-x}\Big]_0^T = \lim_{T\to\infty}\big(1-e^{-T}\big) = \boxed{1}$$

*Verified symbolically.*

**Exponentials beat every power.** $e^{-x}$ decays faster than $x^{-p}$ for every $p$, so integrals of exponential type essentially always converge. This is why the normal distribution, the Poisson distribution, and most of probability theory work.

### Example 4 — parts, then a limit

$$\int_0^\infty xe^{-x}dx = \lim_{T\to\infty}\left(\Big[-xe^{-x}\Big]_0^T + \int_0^T e^{-x}dx\right) = \lim_{T\to\infty}\left(-Te^{-T} + 1 - e^{-T}\right) = \boxed{1}$$

*Verified symbolically: exactly 1.*

**The step $Te^{-T}\to0$ is the content.** It is an $\infty\cdot0$ form and needs L'Hôpital (MATH 141, Week 6): $\frac{T}{e^T}\to\frac{1}{e^T}\to0$. **Exponential decay beats polynomial growth**, and that fact is used constantly from here on.

### Example 5 — a two-sided integral

$$\int_{-\infty}^{\infty}\frac{dx}{1+x^2} = \int_{-\infty}^0 + \int_0^\infty = \lim_{S\to-\infty}\Big[\arctan x\Big]_S^0 + \lim_{T\to\infty}\Big[\arctan x\Big]_0^T$$

$$= \left(0-\left(-\frac\pi2\right)\right)+\left(\frac\pi2-0\right) = \boxed{\pi}$$

*Verified symbolically: exactly $\pi$.*

**Both halves converge**, so the split was legitimate. Dividing by $\pi$ gives the **Cauchy distribution** — a probability density with no mean, which will make an appearance in any statistics course you take.

### Example 6 — the Gaussian

$$\int_0^\infty e^{-x^2}dx = \frac{\sqrt\pi}{2}$$

*Verified symbolically.*

**We cannot prove this yet** — the integrand has no elementary antiderivative (Week 0), so the limit method has nothing to take a limit *of*. The standard proof uses a two-dimensional trick you will meet in multivariable calculus.

But note what has happened: **this is the integral from Lab 0.** There you computed $\int_0^1 e^{-x^2}dx$ numerically to ten decimal places. Here the full integral to infinity has a closed form containing $\sqrt\pi$ — and the whole of statistics rests on it.

### Example 7 — a logarithmic near-miss

$$\int_2^\infty\frac{dx}{x\ln x} \quad\text{vs}\quad \int_2^\infty\frac{dx}{x(\ln x)^2}$$

Both have $u=\ln x$, $du = \tfrac{dx}x$:

- First: $\int_{\ln2}^\infty\frac{du}{u}$ — **diverges** (Example 2 again).
- Second: $\int_{\ln2}^\infty\frac{du}{u^2} = \frac{1}{\ln 2}$ — **converges**, to $\approx1.4427$.

*Both verified symbolically.*

**A single power of a logarithm decides it.** These functions are *extraordinarily* close together — at $x=10^6$ they differ by a factor of only $\ln(10^6)\approx13.8$ — and yet one integral is infinite and the other is not. **This is why numerical evidence is worthless here**, and it is the subject of Lab 3.

---

## 5. What Convergence Does *Not* Require

**A common false belief:** "if $f(x)\to0$ then $\int_a^\infty f$ converges."

**False.** $\frac1x\to0$ and its integral diverges. Tending to zero is *necessary* but nowhere near *sufficient* — the function must tend to zero **fast enough**, and the $p$-test says how fast.

*(In Week 7 you will meet the exact analogue for series: the terms of a convergent series must tend to zero, but $\sum\frac1n$ shows that is not enough. It is the same fact.)*

**Also false:** "if the region is unbounded the area is infinite." Example 1 has area 1.

---

## 6. What To Take From This Lecture

1. **$\int_a^\infty f := \lim_{T\to\infty}\int_a^T f$.** Write the limit; it is the argument.
2. **Converges** iff that limit exists and is finite.
3. **The $p$-test:** $\int_1^\infty x^{-p}$ converges $\iff p>1$. The boundary case diverges.
4. **Exponential decay beats every power**; polynomial growth loses to it.
5. **Two-sided integrals need both halves to converge separately** — symmetric cancellation is not convergence.
6. **$f\to0$ does not imply convergence.** Speed is everything.

---

*Next: Tuesday — Improper Integrals of the Second Kind, and Singularities That Hide*
