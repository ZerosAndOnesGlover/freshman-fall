# MATH 141 · Calculus I
## Week 2 · Lecture 3 (Wednesday)
### The Intermediate Value Theorem

**Date:** Wednesday 7 October 2026 · 11:00–11:50 · Week 2

---

**Reading:** Stewart §2.5 | Spivak Ch. 7 (the three hard theorems)

---

## The First Theorem That Pays for the Definition

Two lectures established what continuity *is*. This one shows what it *buys*.

The Intermediate Value Theorem is the first result in this course that is genuinely non-obvious,
genuinely useful, and genuinely dependent on the ε-δ machinery. It says something that feels like it
should be free — and is not.

---

## 1. Statement

> **Intermediate Value Theorem (IVT).** Let $f$ be continuous on the closed interval $[a,b]$, and let
> $N$ be any number strictly between $f(a)$ and $f(b)$. Then there exists at least one $c \in (a,b)$
> with $f(c) = N$.

Informally: **a continuous function cannot skip a value.** To get from $f(a)$ to $f(b)$ it must pass
through everything in between.

### Every hypothesis is load-bearing

**Continuity is essential.** The jump function from Lecture 2,

$$f(x)=\begin{cases}x,& x<0\\ x+1,& x\ge0\end{cases}$$

has $f(-1) = -1$ and $f(1) = 2$, yet takes **no value** in $(0,1)$ — it jumps straight over that
interval. Verified: $f(-10^{-6}) = -0.000001$ and $f(10^{-6}) = +1.000001$, with nothing between.

**The interval must be closed.** On $(0,1]$, $f(x)=1/x$ is continuous, but there is no bounded pair
of endpoint values to sit between.

**The conclusion is existence, not uniqueness.** The theorem promises *at least one* $c$. A function
may cross the level $N$ many times, and the IVT names none of them.

**It is not reversible.** A function can take every intermediate value and still be discontinuous —
$\sin(1/x)$ on $[-1,1]$ (with $f(0)=0$) hits every value in $[-1,1]$ on any interval containing $0$,
and is discontinuous there. So "takes all intermediate values" does **not** imply continuity.

---

## 2. Why It Is Not Obvious

The picture — a curve drawn without lifting the pen must cross any horizontal line between its
endpoints — makes the IVT look like a definition rather than a theorem.

It is not, and the reason is the **real numbers**. Consider $f(x) = x^2 - 2$ on $[1,2]$ over the
**rationals** only. Then $f(1) = -1 < 0$ and $f(2) = 2 > 0$, but there is **no rational $c$** with
$f(c)=0$ — because $\sqrt2$ is irrational.

The function is continuous, the endpoints straddle zero, and the conclusion fails. **The IVT is
false over $\mathbb{Q}$.**

What makes it true over $\mathbb{R}$ is **completeness**: the reals have no gaps. That is why the
proof needs the least-upper-bound axiom and cannot be done by picture. Spivak's Chapter 7 gives it in
full; you are not expected to reproduce the proof, but you should know what it rests on.

---

## 3. The Standard Application: Root Location

**Corollary (Bolzano).** If $f$ is continuous on $[a,b]$ and $f(a)$ and $f(b)$ have **opposite
signs**, then $f$ has at least one root in $(a,b)$.

This is the IVT with $N = 0$.

### Worked example

Does $f(x) = x^3 - x - 2$ have a root in $[1,2]$?

$$f(1) = 1 - 1 - 2 = -2, \qquad f(2) = 8 - 2 - 2 = +4$$

$f$ is a polynomial, hence continuous everywhere. The signs differ, so **the IVT guarantees a root**
in $(1,2)$.

Note what has and has not been established: existence is certain; the location is not.

---

## 4. Bisection: Turning the Theorem into an Algorithm

The IVT does more than assert existence — its proof is constructive, and the construction is a usable
algorithm.

**Bisection.** Given a sign change on $[a,b]$: evaluate the midpoint $m$. The sign change now lies in
$[a,m]$ or $[m,b]$. Keep that half and repeat. The bracket halves every step.

Verified trace on $f(x)=x^3-x-2$ over $[1,2]$:

| Iteration | Bracket | Midpoint | $f(\text{mid})$ |
|---|---|---|---|
| 1 | $[1.000000,\ 2.000000]$ | $1.500000$ | $-0.125000$ |
| 2 | $[1.500000,\ 2.000000]$ | $1.750000$ | $+1.609375$ |
| 3 | $[1.500000,\ 1.750000]$ | $1.625000$ | $+0.666016$ |
| 4 | $[1.500000,\ 1.625000]$ | $1.562500$ | $+0.252197$ |
| 5 | $[1.500000,\ 1.562500]$ | $1.531250$ | $+0.059113$ |
| 6 | $[1.500000,\ 1.531250]$ | $1.515625$ | $-0.034054$ |
| 7 | $[1.515625,\ 1.531250]$ | $1.523438$ | $+0.012250$ |
| 8 | $[1.515625,\ 1.523438]$ | $1.519531$ | $-0.010971$ |

After 8 iterations the bracket is $[1.519531,\ 1.523438]$, of width $3.91\times10^{-3}$.

Continuing to convergence gives the root

$$c = 1.521379706805, \qquad f(c) = 1.33\times10^{-15}$$

### The convergence rate

Each step halves the bracket, so after $n$ steps the width is $\dfrac{b-a}{2^n}$.

To reach an accuracy of $\varepsilon$ you need

$$n \ge \log_2\!\left(\frac{b-a}{\varepsilon}\right)$$

For $[1,2]$ and $\varepsilon = 10^{-6}$: $n \ge \log_2(10^6) \approx 19.93$, so **20 iterations**.

That is **linear convergence** — one bit of accuracy per step. Newton's method, which you will meet
in MATH 341, roughly *doubles* the number of correct digits each step, but it can fail to converge at
all. Bisection is slow and **cannot fail** once a sign change is bracketed. That trade-off — a
guaranteed slow method against a fast fragile one — recurs throughout numerical analysis.

> **CS connection.** Bisection *is* binary search, on a continuous domain. The invariant is the
> same — "the answer is in this interval" — and so is the halving. Any student who has implemented
> binary search has implemented the constructive proof of the IVT.

---

## 5. Other Uses

**Fixed points.** To show $f(x) = x$ has a solution, apply the IVT to $g(x) = f(x) - x$. If $g$
changes sign, a fixed point exists. This is the one-dimensional ancestor of Brouwer's fixed-point
theorem.

**Existence arguments.** A continuous temperature on a circular wire has two antipodal points at the
same temperature: let $g(\theta) = T(\theta) - T(\theta+\pi)$; then $g(0) = -g(\pi)$, so $g$ changes
sign (or is zero), and the IVT does the rest.

**Guaranteeing a solver will work.** Before running a numerical root-finder, bracketing a sign change
proves a root exists. Without it, a failure to converge is ambiguous — no root, or a bad method?

---

## Summary

| Idea | Takeaway |
|---|---|
| **IVT** | $f$ continuous on $[a,b]$, $N$ between $f(a)$ and $f(b)$ $\Rightarrow$ some $c$ with $f(c)=N$ |
| Continuity required | The jump function skips $(0,1)$ entirely |
| Closed interval required | |
| Existence, not uniqueness | At least one $c$; the theorem locates nothing |
| Converse is false | $\sin(1/x)$ takes all values and is discontinuous |
| Why it is deep | **False over $\mathbb{Q}$** — $x^2-2$ on $[1,2]$ has no rational root |
| It rests on completeness | The reals have no gaps |
| Bolzano | Opposite signs $\Rightarrow$ a root |
| Bisection | Constructive; bracket halves each step |
| Accuracy | $n \ge \log_2\!\big((b-a)/\varepsilon\big)$; **20 steps** for $10^{-6}$ on $[1,2]$ |
| Trade-off | Bisection is slow and cannot fail; Newton is fast and can |

---

## Lecture 3 Exercises

**1.** Show $f(x)=x^3-x-2$ has a root in $[1,2]$, and state precisely what the IVT does and does not
tell you.

**2.** Show $\cos x = x$ has a solution in $[0,1]$.

**3.** How many bisection steps are needed to locate a root in $[2,3]$ to within $10^{-4}$?

**4.** Give a function on $[0,1]$ with $f(0)<0<f(1)$ and **no** root, and identify which hypothesis
fails.

**5.** Explain why the IVT is false over the rationals, with an explicit example.

### Answers

**1.** $f$ is a polynomial, hence continuous on $[1,2]$. $f(1)=-2$ and $f(2)=+4$, so $0$ lies
strictly between them. By the IVT there is $c \in (1,2)$ with $f(c)=0$.

**What it tells you:** at least one root exists in the open interval.

**What it does not:** *where* the root is; *how many* there are; and it gives no way to compute one —
that requires the constructive bisection argument, not the theorem's statement. *(In fact this cubic
has exactly one real root, $c \approx 1.521379706805$, but the IVT does not establish uniqueness —
that needs $f'(x)=3x^2-1>0$ on $[1,2]$, which is Week 6.)*

**2.** Let $g(x)=\cos x - x$, continuous on $[0,1]$ as a difference of continuous functions.

$$g(0)=\cos 0 - 0 = 1 > 0, \qquad g(1)=\cos 1 - 1 \approx 0.540302 - 1 = -0.459698 < 0$$

Signs differ, so by the IVT there is $c \in (0,1)$ with $g(c)=0$, i.e. $\cos c = c$.

*(Verified: the fixed point is $c \approx 0.739085$, the Dottie number.)*

**3.** Bracket width $b-a = 1$. After $n$ steps the width is $2^{-n}$, and we need $2^{-n} \le 10^{-4}$:

$$n \ge \log_2(10^4) = 4\log_2 10 \approx 13.29$$

So **14 iterations**.

*Common error:* rounding $13.29$ down to 13, which leaves the bracket at $1.22\times10^{-4}$ — wider
than required. Always round **up**.

**4.** $f(x)=\begin{cases}-1,& x<\tfrac12\\ \ \ 1,& x\ge\tfrac12\end{cases}$

Then $f(0)=-1<0<1=f(1)$, and $f$ never takes the value $0$ — it takes only $-1$ and $1$.

**The hypothesis that fails is continuity**: $f$ has a jump discontinuity at $x=\tfrac12$, where the
one-sided limits are $-1$ and $+1$.

*(Any jump function straddling zero works. What does **not** work is a continuous function — by the
theorem, no such example exists.)*

**5.** Take $f(x)=x^2-2$ on $[1,2]$, restricted to rational $x$.

$f$ is continuous, $f(1)=-1<0$ and $f(2)=2>0$. If the IVT held over $\mathbb{Q}$ there would be a
**rational** $c$ with $c^2=2$ — but $\sqrt2$ is irrational, so no such $c$ exists.

The IVT therefore fails over $\mathbb{Q}$. What the rationals lack is **completeness**: they have
gaps, and the "curve" slips through one. The theorem is a statement about the real number system as
much as about continuous functions, which is precisely why it needs a proof rather than a picture.

---

*Next: Week 3, Monday — The Derivative: Definition and Geometric Interpretation*
