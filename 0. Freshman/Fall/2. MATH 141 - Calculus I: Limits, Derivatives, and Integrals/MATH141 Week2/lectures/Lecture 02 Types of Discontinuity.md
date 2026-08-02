# MATH 141 · Calculus I
## Week 2 · Lecture 2 (Tuesday)
### Classifying Discontinuities

---

**Reading:** Stewart §2.5 | Spivak Ch. 6

---

## Why Classify?

Monday gave the three-part definition: $f$ is continuous at $a$ when $f(a)$ is defined,
$\lim_{x\to a}f(x)$ exists, and the two agree.

A function can fail that test in several distinct ways, and the distinction is not academic. One kind
of failure can be **repaired by redefining a single point**; another cannot be repaired at all. Which
one you have determines whether the Intermediate Value Theorem applies (Lecture 3), whether the
function is integrable (Week 8), and whether a numerical method will converge.

---

## 1. The Four Types

| Type | What fails | Repairable? |
|---|---|---|
| **Removable** | The limit exists but $f(a)$ is undefined or has the wrong value | ✅ Yes — redefine $f(a)$ |
| **Jump** | Both one-sided limits exist but differ | ❌ No |
| **Infinite** | At least one one-sided limit is $\pm\infty$ | ❌ No |
| **Essential** *(oscillatory)* | A one-sided limit fails to exist for any other reason | ❌ No |

The first is qualitatively different from the rest: the function is "almost" continuous, wrong at one
point only.

---

## 2. Removable Discontinuity

$$f(x) = \frac{x^2-1}{x-1}$$

At $x = 1$ the expression is $\frac00$ — undefined. But for every $x \ne 1$,

$$\frac{x^2-1}{x-1} = \frac{(x-1)(x+1)}{x-1} = x+1$$

so the limit is $2$. Verified:

| $x$ | $f(x)$ | | $x$ | $f(x)$ |
|---|---|---|---|---|
| $0.9$ | $1.900000$ | | $1.001$ | $2.001000$ |
| $0.99$ | $1.990000$ | | $1.01$ | $2.010000$ |
| $0.999$ | $1.999000$ | | $1.1$ | $2.100000$ |

The graph is the line $y = x+1$ with a **single point removed** — a hole at $(1,2)$.

**The repair:**

$$\tilde f(x) = \begin{cases} \dfrac{x^2-1}{x-1}, & x \ne 1\\[6pt] 2, & x = 1\end{cases}$$

is continuous everywhere. This is called the **continuous extension** of $f$.

> **Note the cancellation is legitimate.** $\dfrac{(x-1)(x+1)}{x-1} = x+1$ requires $x \ne 1$, which is
> exactly the condition under which a limit as $x \to 1$ is computed — the limit never evaluates the
> function *at* the point. Week 1's definition says $0 < |x-a|$, and that strict inequality is what
> licenses the cancellation.

---

## 3. Jump Discontinuity

$$f(x) = \begin{cases} x, & x < 0\\ x+1, & x \ge 0\end{cases}$$

Verified either side of $0$:

| $x$ | $f(x)$ |
|---|---|
| $-0.01$ | $-0.010000$ |
| $-10^{-6}$ | $-0.000001$ |
| $+10^{-6}$ | $+1.000001$ |
| $+0.01$ | $+1.010000$ |

$$\lim_{x\to 0^-}f(x)=0,\qquad \lim_{x\to 0^+}f(x)=1$$

Both one-sided limits exist and are finite; they simply **disagree**. No choice of $f(0)$ can fix
this — whatever value you assign, it can match at most one side.

The **jump** is $1 - 0 = 1$. Jump discontinuities are what step functions, rounding, and any
piecewise-defined threshold produce, so they are extremely common in applications.

---

## 4. Infinite Discontinuity

$$f(x) = \frac1x \quad\text{at } x=0$$

From Week 1, verified: $\lim_{x\to 0^+} 1/x = +\infty$ and $\lim_{x\to 0^-} 1/x = -\infty$.

This is a **vertical asymptote**, and no repair is possible — the function is unbounded near the
point, so no finite value could restore continuity.

**Distinguishing removable from infinite in a rational function.** Given $\dfrac{p(x)}{q(x)}$ with
$q(a)=0$:

- If $p(a) \ne 0$: **infinite** discontinuity, vertical asymptote at $a$.
- If $p(a) = 0$ too: factor out $(x-a)$ from both and re-examine. It may be **removable**, or the
  denominator may retain a factor and it is still infinite.

$$\frac{x^2-1}{x-1}\ \text{(removable at 1)}\qquad\text{vs}\qquad \frac{x-1}{(x-1)^2}=\frac{1}{x-1}\ \text{(infinite at 1)}$$

Both are $\frac00$ at $x=1$. **The form does not decide** — you must do the algebra. This is Week 1's
"indeterminate ≠ no limit" lesson in a new setting.

---

## 5. Essential (Oscillatory) Discontinuity

$$f(x) = \sin\!\left(\frac1x\right) \quad\text{at } x=0$$

As $x \to 0$, $1/x$ grows without bound and the sine cycles ever faster. Verified at points chosen to
hit the peaks and troughs:

| $x$ | $\sin(1/x)$ |
|---|---|
| $0.6366197724$ | $+1$ |
| $0.2122065908$ | $-1$ |
| $0.1273239545$ | $+1$ |
| $0.0909456818$ | $-1$ |
| $0.0707355303$ | $+1$ |
| $0.0578745248$ | $-1$ |

Every neighbourhood of $0$, however small, contains points where $f = +1$ and points where $f = -1$.
So **no one-sided limit exists** — not finite, not infinite. The function is bounded, yet has no
limit.

This is the case that shows why the ε-δ definition had to be so careful. "Gets close to $L$" is not
enough; it must *stay* close, and here it never does.

> **Contrast with Week 1's squeeze example.** $x\sin(1/x) \to 0$ as $x \to 0$, because the
> oscillation is damped by a factor going to zero. Same wild oscillation, different answer — the
> amplitude is what matters, and $|x\sin(1/x)| \le |x|$ pins it down.

---

## 6. Continuity on an Interval

> $f$ is **continuous on $[a,b]$** if it is continuous at every interior point, right-continuous at
> $a$, and left-continuous at $b$.

The one-sided requirement at the endpoints matters: $f(x)=\sqrt x$ is continuous on $[0,\infty)$
even though it is undefined for $x<0$, because only the right-hand limit is required at $0$.

**Which functions are continuous where they are defined?** Polynomials (everywhere), rational
functions (except zeros of the denominator), roots, exponentials, logarithms, and the trigonometric
functions. Sums, products, quotients and compositions of continuous functions are continuous.

That inventory is what makes limit evaluation routine: **for a continuous function, the limit is just
the value.** Substitute and you are done. The interesting cases — the ones this week is about — are
exactly the points where that fails.

---

## Summary

| Type | Test | Repairable |
|---|---|---|
| **Removable** | $\lim$ exists, $\ne f(a)$ or $f(a)$ undefined | ✅ redefine one point |
| **Jump** | Both one-sided limits exist, differ | ❌ |
| **Infinite** | A one-sided limit is $\pm\infty$ | ❌ vertical asymptote |
| **Essential** | A one-sided limit fails for any other reason | ❌ |
| $\frac{p}{q}$ with $q(a)=0$ | $p(a)\ne0 \Rightarrow$ infinite; $p(a)=0 \Rightarrow$ factor and re-check | |
| Continuous function | $\lim_{x\to a} f(x) = f(a)$ — substitute | |

---

## Lecture 2 Exercises

**1.** Classify the discontinuity at the given point:
(a) $\dfrac{x^2-4}{x-2}$ at $x=2$
(b) $\dfrac{x+2}{x-2}$ at $x=2$
(c) $\dfrac{|x|}{x}$ at $x=0$
(d) $\cos\!\left(\dfrac1x\right)$ at $x=0$

**2.** For $f(x)=\dfrac{x^2-9}{x^2-3x}$, find every discontinuity and classify each.

**3.** Define $f(2)$ so that $f(x)=\dfrac{x^3-8}{x-2}$ becomes continuous at $x=2$.

**4.** Give a function continuous on $(0,1)$ but not on $[0,1]$, and say which condition fails.

### Answers

**1.**

| | Classification | Reason |
|---|---|---|
| **(a)** | **Removable** | $\dfrac{(x-2)(x+2)}{x-2}=x+2 \to 4$; the hole is at $(2,4)$ |
| **(b)** | **Infinite** | Numerator $\to 4 \ne 0$ while denominator $\to 0$; vertical asymptote |
| **(c)** | **Jump** | $\lim_{x\to0^-}=-1$, $\lim_{x\to0^+}=+1$; jump of $2$ |
| **(d)** | **Essential** | $\cos(1/x)$ oscillates between $\pm1$ infinitely often near $0$ |

(a) and (b) are the pair worth dwelling on: both have a vanishing denominator, and only the numerator
distinguishes them.

**2.** $f(x)=\dfrac{x^2-9}{x^2-3x}=\dfrac{(x-3)(x+3)}{x(x-3)}$.

The denominator vanishes at $x = 0$ and $x = 3$.

- **At $x=3$:** numerator also vanishes. Cancelling gives $\dfrac{x+3}{x}$, whose limit is
  $\dfrac{6}{3}=2$. **Removable** — hole at $(3,2)$.
- **At $x=0$:** after cancellation the function is $\dfrac{x+3}{x}$, numerator $\to 3 \ne 0$.
  **Infinite** — vertical asymptote.

*Both came from the same original denominator, and they classify differently. Factor first, always.*

**3.** $\dfrac{x^3-8}{x-2}=\dfrac{(x-2)(x^2+2x+4)}{x-2}=x^2+2x+4$ for $x \ne 2$, so the limit is
$4+4+4=12$.

Define $f(2)=\mathbf{12}$.

**4.** $f(x)=\dfrac1x$ is continuous on $(0,1)$ but not on $[0,1]$: it is **not defined at $x=0$**, so
the first condition of the three-part definition fails, and no value assigned to $f(0)$ would help
since $\lim_{x\to0^+}1/x=+\infty$.

*Also acceptable:* $f(x)=\sin(1/x)$ — defined on $(0,1)$, essential discontinuity at $0$. Or
$\tan x$ on $(0,\pi/2)$ against $[0,\pi/2]$.

*Not acceptable:* $f(x)=x$ restricted to $(0,1)$ — that has a continuous extension to $[0,1]$, so the
failure is an artefact of the domain rather than of the function.

---

*Next: Wednesday — The Intermediate Value Theorem*
