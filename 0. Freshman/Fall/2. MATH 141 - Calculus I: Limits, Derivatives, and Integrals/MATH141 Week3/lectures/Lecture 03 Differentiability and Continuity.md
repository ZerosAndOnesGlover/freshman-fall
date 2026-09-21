# MATH 141 · Calculus I
## Week 3 · Lecture 3 (Wednesday)
### Differentiability and Continuity

**Date:** Wednesday 14 October 2026 · 11:00–11:50 · Week 3

---

**Reading:** Stewart §2.8 | Spivak Ch. 9

---

## One Implication, Not Two

Week 2 built continuity. This week built the derivative. The relationship between them is the point
of today, and it runs in **one direction only**:

> **Theorem.** If $f$ is differentiable at $a$, then $f$ is continuous at $a$.
>
> **The converse is false.**

Students routinely assert the converse, and the counterexamples are not exotic — $|x|$ is the first
one, and it appears in every applied context where a quantity is clipped, rectified, or bounded
below.

---

## 1. Differentiable ⟹ Continuous

**Proof.** Suppose $f'(a)$ exists. For $x \ne a$ write

$$f(x)-f(a)=\frac{f(x)-f(a)}{x-a}\cdot(x-a)$$

This is legitimate because $x \ne a$ makes the division safe. Taking limits as $x \to a$, both
factors have limits — the first is $f'(a)$ by hypothesis, the second is $0$ — so by the product law

$$\lim_{x\to a}\big(f(x)-f(a)\big)=f'(a)\cdot 0=0$$

Hence $\lim_{x\to a} f(x)=f(a)$, which is continuity at $a$. $\blacksquare$

**What the proof actually uses:** only that the difference quotient has a *finite* limit. That
finiteness is doing all the work — and it is exactly what fails in every counterexample below.

### The useful contrapositive

> **If $f$ is not continuous at $a$, then $f$ is not differentiable at $a$.**

So a jump or infinite discontinuity kills differentiability immediately, with no computation needed.
Week 2's classification is therefore a *screening test*: any point that failed continuity fails
differentiability too.

---

## 2. Three Ways to Be Continuous but Not Differentiable

### (a) A corner — $f(x)=|x|$ at $0$

$f$ is continuous at $0$: $\lim_{x\to0}|x| = 0 = f(0)$.

The difference quotient is $\dfrac{|0+h|-0}{h}=\dfrac{|h|}{h}$, which is $+1$ for $h>0$ and $-1$ for
$h<0$. Verified:

| $h$ | right slope | left slope |
|---|---|---|
| $10^{-2}$ | $+1.0$ | $-1.0$ |
| $10^{-5}$ | $+1.0$ | $-1.0$ |
| $10^{-9}$ | $+1.0$ | $-1.0$ |

The one-sided limits exist and are **finite but unequal**, so the two-sided limit does not exist.
$f'(0)$ does not exist; $f'$ is defined on $\{x \ne 0\}$ with value $\operatorname{sign}(x)$.

The graph has a **corner**: two well-defined but different tangent directions.

### (b) A cusp — $f(x)=x^{2/3}$ at $0$

The difference quotient is $\dfrac{h^{2/3}}{h}=h^{-1/3}$. Verified:

| $h$ | right | left |
|---|---|---|
| $10^{-3}$ | $+10.0$ | $-10.0$ |
| $10^{-6}$ | $+100.0$ | $-100.0$ |
| $10^{-9}$ | $+1000.0$ | $-1000.0$ |

Both sides diverge, **in opposite directions**. The graph comes to a sharp point with the tangent
lines approaching vertical from either side — a **cusp**.

### (c) A vertical tangent — $f(x)=x^{1/3}$ at $0$

The difference quotient is $\dfrac{h^{1/3}}{h}=h^{-2/3}$. Verified:

| $h$ | slope |
|---|---|
| $10^{-3}$ | $100.0$ |
| $10^{-6}$ | $10\,000.0$ |
| $10^{-9}$ | $1\,000\,000.0$ |

Here both sides diverge to $+\infty$ **in the same direction**. The graph is smooth to the eye but
its tangent is **vertical** at the origin. Still not differentiable, because $+\infty$ is not a
number.

### The three compared

| | One-sided slopes | Graph |
|---|---|---|
| Corner ($\lvert x\rvert$) | finite, **unequal** | two tangent directions |
| Cusp ($x^{2/3}$) | infinite, **opposite signs** | sharp point, vertical tangents |
| Vertical tangent ($x^{1/3}$) | infinite, **same sign** | smooth curve, vertical tangent |

All three are continuous. None is differentiable. **Continuity constrains the function; it says
nothing about the slope.**

---

## 3. How Bad Can It Get?

The counterexamples above fail at one point. It is natural to expect that a continuous function must
be differentiable *somewhere*.

It need not. In 1872 **Weierstrass** exhibited a function continuous on all of $\mathbb{R}$ and
differentiable at **no point whatsoever**:

$$W(x)=\sum_{n=0}^{\infty} a^n\cos\!\left(b^n\pi x\right), \qquad 0<a<1,\ ab>1+\tfrac{3\pi}{2}$$

The graph is continuous — you could in principle draw it without lifting the pen — yet it has a
corner at every point, at every scale. This demolished the nineteenth-century intuition that
continuous curves are "mostly smooth", and it is one of the reasons the ε-δ definition was needed:
geometric intuition had proved unreliable.

You are not expected to work with $W$. You are expected to know that **continuity is a far weaker
condition than it looks**.

---

## 4. A Function Differentiable Everywhere Whose Derivative Is Discontinuous

One more distinction, because it catches people out. Define

$$f(x)=\begin{cases} x^2\sin\!\left(\dfrac1x\right), & x\ne0\\[6pt] 0,& x=0\end{cases}$$

**$f$ is differentiable at $0$, with $f'(0)=0$.** The difference quotient is
$\dfrac{h^2\sin(1/h)}{h}=h\sin(1/h)$, and $|h\sin(1/h)| \le |h| \to 0$ by the squeeze theorem.
Verified:

| $h$ | quotient | bound $\lvert h\rvert$ |
|---|---|---|
| $10^{-2}$ | $-0.0050636564$ | $10^{-2}$ |
| $10^{-4}$ | $-0.0000305614$ | $10^{-4}$ |
| $10^{-6}$ | $-0.0000003500$ | $10^{-6}$ |
| $10^{-8}$ | $+0.0000000093$ | $10^{-8}$ |

Every value sits inside the bound, and they converge to $0$.

**But $f'$ is not continuous at $0$.** For $x \ne 0$, the product and chain rules give

$$f'(x)=2x\sin\!\frac1x-\cos\!\frac1x$$

The $\cos(1/x)$ term oscillates between $\pm1$ no matter how close $x$ gets to $0$. Verified at
$x = 1/(k\pi)$:

| $x$ | $f'(x)$ |
|---|---|
| $0.031830988618$ | $-1.000000$ |
| $0.003183098862$ | $-1.000000$ |
| $0.000318309886$ | $-1.000000$ |

So $\lim_{x\to0}f'(x)$ does not exist, while $f'(0)=0$. **$f'$ has an essential discontinuity at a
point where $f$ is differentiable.**

The moral: "differentiable" does not mean "smooth". A function whose derivative is itself continuous
is called **continuously differentiable** ($C^1$), and it is a strictly stronger condition. The
distinction matters in Week 6 — several theorems require $C^1$, not merely differentiability.

---

## Summary

| Idea | Takeaway |
|---|---|
| **Differentiable ⟹ continuous** | Proved from the product law; the finite limit does the work |
| **Converse is false** | And the counterexamples are ordinary |
| Contrapositive | Discontinuous ⟹ not differentiable — use it as a screening test |
| Corner, $\lvert x\rvert$ | One-sided slopes **finite, unequal**: $+1$ and $-1$ |
| Cusp, $x^{2/3}$ | Infinite, **opposite** signs: $\pm10, \pm100, \pm1000$ |
| Vertical tangent, $x^{1/3}$ | Infinite, **same** sign: $100, 10^4, 10^6$ |
| Weierstrass function | Continuous everywhere, differentiable **nowhere** |
| $x^2\sin(1/x)$ | Differentiable at $0$, but $f'$ is **discontinuous** there |
| $C^1$ | Continuously differentiable — strictly stronger than differentiable |

---

## Lecture 3 Exercises

**1.** State whether each is differentiable at the given point, with a reason:
(a) $f(x)=|x-3|$ at $x=3$
(b) $f(x)=x|x|$ at $x=0$
(c) $f(x)=\lfloor x\rfloor$ at $x=2$
(d) $f(x)=\sqrt[3]{x-1}$ at $x=1$

**2.** Prove that differentiability at $a$ implies continuity at $a$.

**3.** Find $a$ and $b$ so that
$$f(x)=\begin{cases}x^2,& x\le1\\ ax+b,& x>1\end{cases}$$
is differentiable at $x=1$.

**4.** Give a function continuous everywhere but differentiable nowhere, and one differentiable
everywhere whose derivative is discontinuous somewhere.

### Answers

**1.**

| | Differentiable? | Reason |
|---|---|---|
| **(a)** | **No** | Corner. One-sided slopes are $-1$ and $+1$ — finite but unequal |
| **(b)** | **Yes**, $f'(0)=0$ | $x\lvert x\rvert$ equals $x^2$ for $x\ge0$ and $-x^2$ for $x<0$; both have slope $0$ at the origin, so the one-sided derivatives agree |
| **(c)** | **No** | $\lfloor x\rfloor$ has a **jump discontinuity** at $2$; discontinuous ⟹ not differentiable |
| **(d)** | **No** | Vertical tangent — the difference quotient is $h^{-2/3}\to+\infty$ |

**(b) is the discriminating one.** It looks like $|x|$ and behaves entirely differently: multiplying
by $x$ smooths the corner into a smooth inflection. Note $f'(x)=2|x|$, which is continuous — so $f$
is $C^1$ but not $C^2$.

**2.** For $x \ne a$,

$$f(x)-f(a)=\frac{f(x)-f(a)}{x-a}\cdot(x-a)$$

Both factors have limits as $x\to a$: the first tends to $f'(a)$, which exists by hypothesis and is
finite; the second tends to $0$. By the product law for limits,

$$\lim_{x\to a}\big(f(x)-f(a)\big)=f'(a)\cdot0=0 \implies \lim_{x\to a}f(x)=f(a) \quad\blacksquare$$

*The hypothesis is used exactly once, to guarantee the first factor has a **finite** limit. If the
difference quotient diverged, the product law would not apply — which is why vertical tangents are
consistent with continuity.*

**3.** Two conditions must hold.

**Continuity at $1$** (necessary, by the theorem): the two pieces must agree.

$$1^2 = a(1)+b \implies a+b=1$$

**Matching derivatives:** the left piece has slope $2x$, so $2$ at $x=1$; the right piece has slope
$a$.

$$a = 2$$

Therefore $a=2$ and $b=-1$:

$$f(x)=\begin{cases}x^2,& x\le1\\ 2x-1,& x>1\end{cases}$$

*Check:* at $x=1$ both give $1$, and both slopes are $2$. The line $2x-1$ is precisely the tangent to
$x^2$ at $x=1$ — which is the geometric content of the answer.

*Common error:* matching only the derivatives and forgetting continuity. That gives $a=2$ with $b$
free, and any $b \ne -1$ produces a jump — at which the function is not even continuous, let alone
differentiable.

**4. Continuous everywhere, differentiable nowhere:** the **Weierstrass function**

$$W(x)=\sum_{n=0}^{\infty}a^n\cos(b^n\pi x),\qquad 0<a<1,\ ab>1+\tfrac{3\pi}{2}$$

**Differentiable everywhere with discontinuous derivative:**

$$f(x)=\begin{cases}x^2\sin(1/x),& x\ne0\\ 0,& x=0\end{cases}$$

Verified: $f'(0)=0$ via the squeeze $|h\sin(1/h)|\le|h|$, but $f'(x)=2x\sin(1/x)-\cos(1/x)$ takes the
value $-1$ at $x=1/(k\pi)$ for arbitrarily large $k$, so $\lim_{x\to0}f'(x)$ does not exist.

*This pair marks the two boundaries of the week: continuity alone guarantees nothing about slope, and
differentiability alone guarantees nothing about the smoothness of the slope.*

---

*Next: Week 4, Monday — Differentiation Rules: Power, Product, Quotient*
