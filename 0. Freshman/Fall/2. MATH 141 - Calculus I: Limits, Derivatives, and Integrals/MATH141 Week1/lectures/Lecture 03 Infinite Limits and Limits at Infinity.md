# MATH 141 Calculus I
## Week 1 · Lecture 3 (Wednesday)
### Infinite Limits and Limits at Infinity

---

**Reading:** Stewart §2.2 (infinite limits), §2.6 (limits at infinity) | Spivak Ch. 5

---

## Why These Are Different Questions

Monday and Tuesday asked what happens as $x \to a$ for a *finite* $a$, with a *finite* answer $L$.
Two further questions remain, and they are genuinely different:

1. **Infinite limits.** What if $f(x)$ grows without bound as $x \to a$? This describes a **vertical
   asymptote**.
2. **Limits at infinity.** What happens as $x$ itself grows without bound? This describes a
   **horizontal asymptote** — the function's long-run behaviour.

Both use limit notation, and neither is a limit in Tuesday's sense: **infinity is not a number**, so
$\lim_{x\to a} f(x) = \infty$ does not say the limit *exists*. It says it fails to exist in a
specific, describable way.

---

## 1. Infinite Limits

> **Definition.** $\displaystyle\lim_{x \to a} f(x) = \infty$ means: for every $M > 0$ there exists
> $\delta > 0$ such that $0 < |x-a| < \delta \implies f(x) > M$.

Compare with Tuesday's definition. Where the ε-δ version said "$f(x)$ can be forced within $\varepsilon$
of $L$", this says "$f(x)$ can be forced **above any $M$ you name**." The structure — *you challenge,
I respond* — is identical; only the target changed.

### The basic example

Verified numerically for $f(x) = 1/x$:

| $x$ | $1/x$ | | $x$ | $1/x$ |
|---|---|---|---|---|
| $0.1$ | $1.0\times10^{1}$ | | $-0.1$ | $-1.0\times10^{1}$ |
| $0.01$ | $1.0\times10^{2}$ | | $-0.01$ | $-1.0\times10^{2}$ |
| $10^{-4}$ | $1.0\times10^{4}$ | | $-10^{-4}$ | $-1.0\times10^{4}$ |
| $10^{-8}$ | $1.0\times10^{8}$ | | $-10^{-8}$ | $-1.0\times10^{8}$ |

$$\lim_{x \to 0^+}\frac 1x = +\infty, \qquad \lim_{x \to 0^-}\frac 1x = -\infty$$

The two one-sided limits differ, so $\lim_{x\to 0} 1/x$ **does not exist** — not even as $\pm\infty$.

Contrast $f(x) = 1/x^2$, verified:

| $x$ | $1/x^2$ |
|---|---|
| $\pm 0.1$ | $100$ |
| $\pm 0.001$ | $1\,000\,000$ |

Both sides agree, so we may write $\lim_{x \to 0} \dfrac{1}{x^2} = +\infty$.

### Vertical asymptotes

> The line $x = a$ is a **vertical asymptote** of $f$ if at least one of the one-sided limits at $a$
> is $+\infty$ or $-\infty$.

For a rational function, look where the **denominator vanishes but the numerator does not**. If both
vanish, you may have a removable discontinuity instead — cancel first and re-examine. That
distinction is Lecture 1 of Week 2.

---

## 2. Limits at Infinity

> **Definition.** $\displaystyle\lim_{x \to \infty} f(x) = L$ means: for every $\varepsilon > 0$ there
> exists $N$ such that $x > N \implies |f(x) - L| < \varepsilon$.

Again the same shape: instead of "close enough to $a$", the hypothesis is "far enough out".

### The technique: divide by the highest power in the denominator

$$\lim_{x\to\infty}\frac{3x^2 + 2x}{x^2 - 5}
 = \lim_{x\to\infty}\frac{3 + \frac2x}{1 - \frac{5}{x^2}} = \frac{3+0}{1-0} = 3$$

Verified:

| $x$ | $\dfrac{3x^2+2x}{x^2-5}$ |
|---|---|
| $10$ | $3.368421$ |
| $100$ | $3.021511$ |
| $1000$ | $3.002015$ |
| $10^5$ | $3.000020$ |
| $10^7$ | $3.000000$ |

### The three cases for rational functions

For $f(x) = \dfrac{p(x)}{q(x)}$ with $\deg p = n$, $\deg q = m$:

| Condition | $\lim_{x\to\infty} f(x)$ | Asymptote |
|---|---|---|
| $n < m$ | $0$ | $y = 0$ |
| $n = m$ | ratio of leading coefficients | $y = a_n/b_m$ |
| $n > m$ | $\pm\infty$ | none horizontal *(possibly oblique)* |

Verified for $n<m$: $\dfrac{2x+1}{x^2+3}$ gives $0.203883,\ 0.020094,\ 0.002001,\ 0.000020$ at
$x = 10, 10^2, 10^3, 10^5$ — decaying like $2/x$, as the degree gap predicts.

### A case that needs algebra first

$$\lim_{x\to\infty}\left(\sqrt{x^2+1} - x\right)$$

This is $\infty - \infty$ — **indeterminate**, so no limit law applies directly. Rationalise:

$$\sqrt{x^2+1}-x = \frac{(\sqrt{x^2+1}-x)(\sqrt{x^2+1}+x)}{\sqrt{x^2+1}+x}
= \frac{1}{\sqrt{x^2+1}+x} \longrightarrow 0$$

Verified: $0.049876,\ 0.005000,\ 0.000500$ at $x = 10, 100, 1000$ — decaying like $1/(2x)$.

> **A computational warning worth having.** Evaluating $\sqrt{x^2+1}-x$ *directly* in floating point
> fails for large $x$: the two terms agree to more digits than a `double` holds, and the subtraction
> loses all of them — **catastrophic cancellation**. Past about $x = 10^8$ it returns exactly $0$,
> which is the right limit reached by the wrong route and would be wrong for any $x$ where the true
> value still mattered.
>
> The rationalised form $\dfrac{1}{\sqrt{x^2+1}+x}$ has no subtraction and stays accurate. The algebra
> that made the limit tractable also made the computation stable — this is not a coincidence, and you
> will meet it again in MATH 341.

---

## 3. Indeterminate Forms

Some expressions carry no information until you do more work:

$$\frac00,\quad \frac{\infty}{\infty},\quad \infty-\infty,\quad 0\cdot\infty,\quad 1^\infty,\quad 0^0,\quad \infty^0$$

**"Indeterminate" does not mean "no limit."** It means the *form alone* does not decide. Each of
$\dfrac{x}{x^2}, \dfrac{x}{x}, \dfrac{x^2}{x}$ is $\infty/\infty$ as $x\to\infty$, with limits
$0$, $1$, $\infty$ respectively.

The tools: factor and cancel, rationalise, divide by the dominant term — and, from Week 6,
**L'Hôpital's rule**, which handles $\frac00$ and $\frac\infty\infty$ directly.

By contrast $\dfrac{1}{0^+} \to \infty$ is **determinate**: that form always blows up.

---

## Summary

| Idea | Takeaway |
|---|---|
| $\lim = \infty$ | The limit **does not exist**; it fails in a describable way |
| $\lim_{x\to 0^\pm} 1/x$ | $\pm\infty$ — sides disagree, so the two-sided limit does not exist |
| $\lim_{x\to 0} 1/x^2$ | $+\infty$ — sides agree |
| Vertical asymptote | Denominator $\to 0$, numerator $\not\to 0$ |
| Limits at infinity | Divide by the highest power in the denominator |
| $\deg p < \deg q$ | $\to 0$ |
| $\deg p = \deg q$ | Ratio of leading coefficients |
| $\deg p > \deg q$ | $\to \pm\infty$ |
| $\infty - \infty$ | Indeterminate — rationalise |
| Indeterminate ≠ no limit | The **form** does not decide; the function does |

---

## Lecture 3 Exercises

**1.** Evaluate, or state that the limit does not exist:
(a) $\displaystyle\lim_{x\to 3^+}\frac{1}{x-3}$
(b) $\displaystyle\lim_{x\to 3^-}\frac{1}{x-3}$
(c) $\displaystyle\lim_{x\to 3}\frac{1}{(x-3)^2}$

**2.** Find all horizontal and vertical asymptotes of $f(x)=\dfrac{3x^2+2x}{x^2-5}$.

**3.** Evaluate $\displaystyle\lim_{x\to\infty}\frac{4x^3 - x}{2x^3 + 7}$ and
$\displaystyle\lim_{x\to\infty}\frac{5x}{x^2+1}$.

**4.** Evaluate $\displaystyle\lim_{x\to\infty}\left(\sqrt{x^2+6x}-x\right)$.

**5.** Explain why $\infty-\infty$ is indeterminate but $\infty+\infty$ is not, giving examples.

### Answers

**1.** (a) $+\infty$ — as $x\to 3^+$, $x-3\to 0^+$. (b) $-\infty$ — $x-3\to 0^-$.
(c) $+\infty$ — the square makes the denominator positive from both sides, so the two one-sided
limits agree.

**2.** **Horizontal:** $y = 3$, since the degrees match and the leading coefficients are $3$ and $1$.
Verified: $f(10^7) = 3.000000$. The same value holds as $x \to -\infty$.

**Vertical:** $x^2-5=0$ at $x = \pm\sqrt5 \approx \pm 2.2360680$. The numerator $3x^2+2x$ is nonzero
at both, so both are genuine vertical asymptotes.

**3.** $\dfrac{4x^3-x}{2x^3+7} \to \dfrac42 = 2$ (equal degrees). $\dfrac{5x}{x^2+1} \to 0$ (numerator
degree lower).

**4.** Rationalise:

$$\sqrt{x^2+6x}-x=\frac{6x}{\sqrt{x^2+6x}+x}=\frac{6}{\sqrt{1+6/x}+1}\longrightarrow \frac{6}{2}=3$$

*(Dividing numerator and denominator by $x$ is the step that makes the limit visible. Note the answer
is $3$, not $0$ — the $6x$ term is large enough to survive, unlike the $+1$ in the lecture's
example.)*

**5.** $\infty-\infty$ is indeterminate because the two quantities may grow at different rates and the
difference can be anything:

- $(x+5)-x \to 5$
- $x^2-x \to \infty$
- $x - x^2 \to -\infty$
- $\sqrt{x^2+1}-x \to 0$

All four are $\infty-\infty$ with four different answers, so the form alone decides nothing.

$\infty+\infty$ is **determinate**: two quantities both growing without bound have a sum growing
without bound. There is no competition to resolve — nothing is being cancelled.

---

*Next: Week 2, Monday — Continuity: The Three-Part Definition and Types of Discontinuity*
