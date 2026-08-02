# MATH 141 · Week 2 Reference Sheet
## Continuity and the IVT

---

## Continuity at a Point

> $f$ is continuous at $a$ when **all three** hold:
> 1. $f(a)$ is defined
> 2. $\lim_{x\to a}f(x)$ exists
> 3. They are equal

**For a continuous function, the limit is the value** — substitute and stop. Everything interesting
happens where this fails.

**Continuous where defined:** polynomials, rational functions, roots, exponentials, logarithms,
trigonometric functions — and any sum, product, quotient or composition of them.

**On an interval:** continuous at every interior point, right-continuous at $a$, left-continuous at
$b$. This is why $\sqrt x$ is continuous on $[0,\infty)$.

---

## The Four Discontinuities

| Type | Test | Repairable |
|---|---|---|
| **Removable** | $\lim$ exists but $\ne f(a)$, or $f(a)$ undefined | ✅ redefine one point |
| **Jump** | One-sided limits exist and differ | ❌ |
| **Infinite** | A one-sided limit is $\pm\infty$ | ❌ vertical asymptote |
| **Essential** | A one-sided limit fails for any other reason | ❌ |

**For $\dfrac{p(x)}{q(x)}$ with $q(a)=0$:**

- $p(a)\ne0$ ⟹ **infinite**
- $p(a)=0$ ⟹ **factor out $(x-a)$ and re-examine**

Both $\dfrac{x^2-1}{x-1}$ (removable) and $\dfrac{x-1}{(x-1)^2}$ (infinite) are $\tfrac00$ at $x=1$.
**The form does not decide.**

**Continuous extension:** if removable, define $\tilde f(a)=\lim_{x\to a}f(x)$.

---

## The Intermediate Value Theorem

> $f$ continuous on $[a,b]$, $N$ strictly between $f(a)$ and $f(b)$ ⟹ **some $c\in(a,b)$ with
> $f(c)=N$.**

| Hypothesis | Why it is needed |
|---|---|
| Continuity | The jump function skips $(0,1)$ entirely |
| Closed interval | Endpoint values must exist |

**Existence only** — the theorem locates nothing and asserts nothing about uniqueness.

**The converse is false.** $\sin(1/x)$ takes every value in $[-1,1]$ near $0$ and is discontinuous
there.

**Bolzano's corollary:** opposite signs ⟹ a root.

---

## Why the IVT Is Deep

Over $\mathbb{Q}$ it is **false**: $x^2-2$ on $[1,2]$ is continuous, changes sign, and has no
rational root.

What makes it true over $\mathbb{R}$ is **completeness** — no gaps. The theorem is as much a
statement about the real number system as about functions.

---

## Bisection

Given a sign change on $[a,b]$: evaluate the midpoint, keep the half that still straddles zero,
repeat.

$$n \ge \log_2\!\left(\frac{b-a}{\varepsilon}\right) \qquad \textbf{rounded up}$$

| Interval | $\varepsilon$ | Steps |
|---|---|---|
| $[1,2]$ | $10^{-6}$ | **20** |
| $[2,3]$ | $10^{-4}$ | **14** |

**Linear convergence** — one bit per step. Slower than Newton's method (MATH 341), but it **cannot
fail** once a sign change is bracketed.

Verified on $x^3-x-2$ over $[1,2]$: after 8 steps the bracket is $[1.519531, 1.523438]$; converged,
the root is $1.521379706805$ with $f = 1.33\times10^{-15}$.

**Bisection is binary search on a continuous domain** — the same invariant, the same halving.

---

*MATH 141 · Week 2 · Reference · © CSE Department*
