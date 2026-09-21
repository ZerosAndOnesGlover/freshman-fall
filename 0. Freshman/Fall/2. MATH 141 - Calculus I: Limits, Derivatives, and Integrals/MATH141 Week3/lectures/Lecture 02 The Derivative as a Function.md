# MATH 141 · Calculus I
## Week 3 · Lecture 2 (Tuesday)
### The Derivative as a Function

**Date:** Tuesday 13 October 2026 · 11:00–11:50 · Week 3

---

**Reading:** Stewart §2.8 | Spivak Ch. 9

---

## From a Number to a Function

Monday defined the derivative **at a point**:

$$f'(a)=\lim_{h\to0}\frac{f(a+h)-f(a)}{h}$$

That produces a single number — the slope of the tangent line at $x=a$. Compute it at $a=1$, then at
$a=2$, then at $a=3$, and a pattern appears. Rather than repeat the limit for every point, do it
once with $a$ left as a variable:

> **Definition.** The **derivative function** of $f$ is
> $$f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$$
> defined at every $x$ where the limit exists.

The shift is conceptual, not technical. $f'$ is a **new function**, built from $f$, whose value at
each point is the slope of $f$ there. Its domain is the set of points where $f$ is differentiable,
which may be smaller than the domain of $f$.

---

## 1. Computing Derivative Functions from the Definition

### $f(x)=x^2$

$$f'(x)=\lim_{h\to0}\frac{(x+h)^2-x^2}{h}
=\lim_{h\to0}\frac{2xh+h^2}{h}
=\lim_{h\to0}(2x+h)=2x$$

The cancellation of $h$ is the essential step, and it is legitimate because the limit never evaluates
at $h=0$ — Week 1's $0<|h|$ again.

Verified against a central difference with $h=10^{-6}$:

| $a$ | numerical $f'$ | $2a$ |
|---|---|---|
| $0$ | $0.000000$ | $0$ |
| $1$ | $2.000000$ | $2$ |
| $2$ | $4.000000$ | $4$ |
| $3$ | $6.000000$ | $6$ |
| $-1.5$ | $-3.000000$ | $-3$ |

### $f(x)=\dfrac1x$

$$f'(x)=\lim_{h\to0}\frac{\frac{1}{x+h}-\frac1x}{h}
=\lim_{h\to0}\frac{\frac{x-(x+h)}{x(x+h)}}{h}
=\lim_{h\to0}\frac{-1}{x(x+h)}=-\frac{1}{x^2}$$

Verified: at $a = 1, 2, 0.5, -2$ the numerical derivative gives $-1.000000$, $-0.250000$,
$-4.000000$, $-0.250000$, matching $-1/a^2$ exactly.

**Note the domains.** $f$ is defined on $x \ne 0$; so is $f'$. Here they coincide.

### $f(x)=\sqrt{x}$

$$f'(x)=\lim_{h\to0}\frac{\sqrt{x+h}-\sqrt x}{h}
=\lim_{h\to0}\frac{h}{h\big(\sqrt{x+h}+\sqrt x\big)}=\frac{1}{2\sqrt x}$$

after rationalising the numerator — the same trick as Week 1's $\sqrt{x^2+1}-x$.

Verified:

| $a$ | numerical $f'$ | $1/(2\sqrt a)$ |
|---|---|---|
| $1$ | $0.500000$ | $0.5$ |
| $4$ | $0.250000$ | $0.25$ |
| $9$ | $0.166667$ | $0.1\overline{6}$ |
| $0.25$ | $1.000000$ | $1$ |

**Here the domains differ.** $f(x)=\sqrt x$ is defined on $[0,\infty)$, but $f'(x)=\frac{1}{2\sqrt x}$
is defined only on $(0,\infty)$ — at $x=0$ the tangent is vertical and the derivative does not exist.
This is the first case where **$\operatorname{dom}(f') \subsetneq \operatorname{dom}(f)$**, and
Wednesday's lecture is about exactly that gap.

---

## 2. Notation

| Notation | Read as | Due to |
|---|---|---|
| $f'(x)$ | "f prime of x" | Lagrange |
| $\dfrac{dy}{dx}$ | "dee y by dee x" | Leibniz |
| $\dfrac{d}{dx}\big[f(x)\big]$ | "the derivative with respect to x of…" | Leibniz |
| $\dot y$ | "y dot" — usually a time derivative | Newton |
| $Df$ | operator notation | Euler |

Each is useful somewhere. $f'$ is compact. **Leibniz notation carries the variables**, which is why
it makes the chain rule (tomorrow) almost self-evident:
$\frac{dy}{dx}=\frac{dy}{du}\cdot\frac{du}{dx}$ reads as cancellation, even though it is not.

For the value at a point, Leibniz needs a bar:

$$f'(2) \quad=\quad \left.\frac{dy}{dx}\right|_{x=2}$$

> **$\frac{dy}{dx}$ is not a fraction.** It is a limit of fractions, and the notation is deliberately
> suggestive. Treating it as a ratio gives right answers often enough to be dangerous — in Week 5's
> implicit differentiation and Week 10's substitution it *behaves* like one, for reasons that are
> theorems, not definitions.

---

## 3. Higher Derivatives

$f'$ is a function, so it can be differentiated in turn:

$$f''=(f')',\qquad f'''=(f'')',\qquad f^{(n)}=\big(f^{(n-1)}\big)'$$

For $f(x)=x^4$:

$$f'=4x^3,\quad f''=12x^2,\quad f'''=24x,\quad f^{(4)}=24,\quad f^{(5)}=0$$

Verified with a second-difference approximation $\frac{f(a+h)-2f(a)+f(a-h)}{h^2}$ at $h=10^{-4}$:

| $a$ | numerical $f''$ | $12a^2$ |
|---|---|---|
| $1$ | $12.0000$ | $12$ |
| $2$ | $48.0000$ | $48$ |

**What they mean.** If $s(t)$ is position, $s'$ is **velocity** and $s''$ is **acceleration**. More
generally $f''$ measures how the *rate* is changing — the **concavity** of the graph, which is
Week 7's subject. Any polynomial of degree $n$ has $f^{(n+1)} \equiv 0$, which is what makes Taylor
polynomials terminate (Week 12).

---

## 4. Reading $f'$ off the Graph of $f$

Given a graph of $f$, you can sketch $f'$ without any algebra:

| On $f$ | On $f'$ |
|---|---|
| Increasing | $f' > 0$ (above the axis) |
| Decreasing | $f' < 0$ (below the axis) |
| Horizontal tangent (peak, trough, flat) | $f' = 0$ (crosses or touches the axis) |
| Steep | $|f'|$ large |
| Corner | $f'$ **undefined** — a jump in $f'$ |
| Vertical tangent | $f'$ has an infinite discontinuity |

The last two rows are worth noticing: **a discontinuity in $f'$ can occur where $f$ itself is
perfectly continuous.** A corner in $f$ is a jump in $f'$. That is Wednesday's lecture.

Conversely, given $f'$, you can describe $f$ up to a constant — which is the entire content of
Week 9's Fundamental Theorem.

---

## Summary

| Idea | Takeaway |
|---|---|
| $f'$ is a **function** | Built from $f$; its value is the slope of $f$ at each point |
| Domain | $\operatorname{dom}(f')\subseteq\operatorname{dom}(f)$, and can be strictly smaller |
| $\frac{d}{dx}x^2=2x$ | Verified numerically at five points |
| $\frac{d}{dx}\frac1x=-\frac1{x^2}$ | Verified at four points |
| $\frac{d}{dx}\sqrt x=\frac1{2\sqrt x}$ | Verified; **undefined at $x=0$** though $f$ is defined there |
| Notation | $f'$, $\frac{dy}{dx}$, $\dot y$, $Df$ — Leibniz carries the variables |
| $\frac{dy}{dx}$ is not a fraction | It is a limit of fractions |
| Higher derivatives | $f''$ verified as $12x^2$ for $x^4$; position → velocity → acceleration |
| Graph reading | Increasing ⇒ $f'>0$; corner ⇒ $f'$ jumps; vertical tangent ⇒ $f'$ blows up |

---

## Lecture 2 Exercises

**1.** Use the definition to find $f'(x)$ for $f(x)=3x^2-5x+1$.

**2.** Use the definition to find $f'(x)$ for $f(x)=\dfrac{1}{x+2}$, and state the domains of $f$ and
$f'$.

**3.** For $f(x)=x^3$, find $f'$, $f''$, $f'''$ and $f^{(4)}$.

**4.** The graph of $f$ rises steeply, levels off at a peak, falls gently, and has a sharp corner at
$x=3$. Describe the graph of $f'$ across that whole range.

**5.** Give a function $f$ for which $\operatorname{dom}(f')$ is strictly smaller than
$\operatorname{dom}(f)$, and say exactly which points are lost and why.

### Answers

**1.**

$$f'(x)=\lim_{h\to0}\frac{3(x+h)^2-5(x+h)+1-\big(3x^2-5x+1\big)}{h}$$

Expanding the numerator: $3x^2+6xh+3h^2-5x-5h+1-3x^2+5x-1 = 6xh+3h^2-5h$.

$$f'(x)=\lim_{h\to0}\frac{h(6x+3h-5)}{h}=\lim_{h\to0}(6x+3h-5)=\mathbf{6x-5}$$

**2.**

$$f'(x)=\lim_{h\to0}\frac{\frac{1}{x+h+2}-\frac{1}{x+2}}{h}
=\lim_{h\to0}\frac{-h}{h(x+h+2)(x+2)}=\mathbf{-\frac{1}{(x+2)^2}}$$

**Domains:** both are $\{x : x \ne -2\}$. They coincide here — unlike $\sqrt x$, nothing extra is
lost, because the failure at $-2$ is already a failure of $f$.

**3.** $f'=3x^2$, $f''=6x$, $f'''=6$, $f^{(4)}=0$.

*(And every higher derivative is $0$. A degree-$n$ polynomial has $f^{(n+1)}\equiv0$ — the fact that
makes Taylor polynomials of polynomials exact.)*

**4.**

| Region of $f$ | Behaviour of $f'$ |
|---|---|
| Rising steeply | $f'$ large and positive |
| Levelling off toward the peak | $f'$ positive but decreasing toward $0$ |
| At the peak | $f' = 0$ — crosses the axis |
| Falling gently | $f'$ negative and small in magnitude |
| At $x=3$ (corner) | $f'$ is **undefined**; it has a **jump discontinuity** there |

The key observation is the last: $f$ is continuous at the corner, but $f'$ is not defined there at
all, so the graph of $f'$ has a genuine break — the left and right one-sided slopes disagree.

**5.** $f(x)=\sqrt{x}$.

$\operatorname{dom}(f)=[0,\infty)$, but $f'(x)=\dfrac{1}{2\sqrt x}$ has
$\operatorname{dom}(f')=(0,\infty)$.

**The point $x=0$ is lost.** At $0$ the difference quotient is

$$\frac{\sqrt{0+h}-0}{h}=\frac{\sqrt h}{h}=\frac{1}{\sqrt h}\longrightarrow+\infty \text{ as } h\to0^+$$

so the limit does not exist — the tangent line is **vertical**. The function is perfectly continuous
at $0$ (indeed $f(0)=0$); it simply has no finite slope there.

*Also acceptable:* $f(x)=|x|$, losing $x=0$ to a corner; or $f(x)=x^{1/3}$, losing $0$ to a vertical
tangent. What is **not** acceptable is a function undefined at the point in question — the whole
point is that $f$ exists there and $f'$ does not.

---

*Next: Wednesday — Differentiability and Continuity*
