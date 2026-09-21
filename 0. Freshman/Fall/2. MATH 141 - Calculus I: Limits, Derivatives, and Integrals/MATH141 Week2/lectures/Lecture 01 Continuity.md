# MATH 141 · Calculus I
## Week 2 · Lecture 1 (Monday)
### Continuity: Definition, Types of Discontinuity, and the Intermediate Value Theorem

**Date:** Monday 5 October 2026 · 11:00–11:50 · Week 2

---

**Reading:** Stewart §2.5 | Spivak Ch. 6 (Continuous Functions)

---

## 1. What Is Continuity?

Informally, a function is continuous if its graph can be drawn without lifting the pen. Formally:

> **Definition.** A function $f$ is **continuous at $a$** if:
> $$\lim_{x \to a} f(x) = f(a)$$

This single equation encodes **three simultaneous requirements**:

1. $f(a)$ is defined (the function has a value at $a$)
2. $\lim_{x \to a} f(x)$ exists (the limit exists as $x \to a$)
3. They are equal (the limit equals the function value)

If any one of these fails, $f$ is **discontinuous at $a$**.

---

## 2. Types of Discontinuity

### 2.1 Removable Discontinuity

The limit exists, but either $f(a)$ is undefined, or $f(a) \neq \lim_{x\to a} f(x)$.

**Why "removable":** We can *remove* the discontinuity by redefining $f(a) = \lim_{x \to a} f(x)$.

**Example:** $f(x) = \dfrac{x^2 - 1}{x - 1}$

- $f(1)$ is undefined
- $\lim_{x \to 1} f(x) = 2$

Discontinuity at $x = 1$, but removable: define $g(x) = f(x)$ for $x \neq 1$ and $g(1) = 2$. Now $g$ is continuous at 1.

### 2.2 Jump Discontinuity

The left and right limits both exist but are not equal.

**Example:** $f(x) = \begin{cases} x & x < 1 \\ x + 2 & x \geq 1 \end{cases}$

- $\lim_{x \to 1^-} f(x) = 1$
- $\lim_{x \to 1^+} f(x) = 3$

The function "jumps" from 1 to 3. This discontinuity cannot be removed.

**Real-world analog:** Tax brackets, postage rates, step functions in computer science (floor function $\lfloor x \rfloor$).

### 2.3 Infinite Discontinuity

$f(x) \to \pm\infty$ as $x \to a$.

**Example:** $f(x) = \dfrac{1}{x}$ at $x = 0$.

### 2.4 Oscillatory Discontinuity

$f(x) = \sin(1/x)$ at $x = 0$ — oscillates infinitely, no limit exists.

---

## 3. Continuity on an Interval

- $f$ is **continuous on $(a,b)$** if it is continuous at every point in $(a,b)$.
- $f$ is **continuous on $[a,b]$** if it is continuous on $(a,b)$, continuous from the right at $a$, and continuous from the left at $b$:
  $$\lim_{x \to a^+} f(x) = f(a) \qquad \lim_{x \to b^-} f(x) = f(b)$$

### Standard Continuous Functions

The following are continuous on their domains (direct substitution always works):
- Polynomials: continuous on $\mathbb{R}$
- Rational functions: continuous where denominator $\neq 0$
- Root functions $\sqrt[n]{x}$: continuous on their domains
- Trigonometric functions: continuous on their domains
- Exponential functions $a^x$: continuous on $\mathbb{R}$
- Logarithmic functions $\log_a x$: continuous on $(0, \infty)$

### Continuity Preserved Under Operations

If $f$ and $g$ are continuous at $a$, then so are:
- $f \pm g$, $f \cdot g$, $f/g$ (when $g(a) \neq 0$)
- $f \circ g$ (if $g$ is continuous at $a$ and $f$ is continuous at $g(a)$)

**Consequence:** Any formula built from continuous functions using $+, -, \times, \div, \circ$ is continuous wherever it's defined.

---

## 4. The Intermediate Value Theorem

This is one of the most important theorems in calculus. Seemingly obvious, yet it requires the **completeness** of $\mathbb{R}$ to prove — it fails for $\mathbb{Q}$.

> **Theorem (IVT).** If $f$ is continuous on $[a, b]$ and $N$ is any number strictly between $f(a)$ and $f(b)$, then there exists at least one $c \in (a, b)$ such that $f(c) = N$.

**Informal version:** A continuous function that changes from one value to another must pass through every value in between.

**Geometric meaning:** If you draw a continuous curve from point $(a, f(a))$ to point $(b, f(b))$, it must cross every horizontal line $y = N$ between those two heights at least once.

### Why Completeness Is Required

Consider $f(x) = x^2 - 2$ on $\mathbb{Q}$ (the rationals). $f(1) = -1 < 0$ and $f(2) = 2 > 0$. The IVT would say there's a rational $c$ with $f(c) = 0$, i.e., $c^2 = 2$. But $\sqrt{2}$ is irrational — no such rational exists. The IVT fails on $\mathbb{Q}$ precisely because $\mathbb{Q}$ has "holes." The completeness of $\mathbb{R}$ fills those holes.

---

## 5. Applications of the IVT

### 5.1 Existence of Roots

**Example:** Show that $f(x) = x^5 - 3x^3 + x - 1$ has a root in $(1, 2)$.

$f(1) = 1 - 3 + 1 - 1 = -2 < 0$  
$f(2) = 32 - 24 + 2 - 1 = 9 > 0$

Since $f$ is continuous (it's a polynomial) and $f(1) < 0 < f(2)$, by IVT there exists $c \in (1, 2)$ with $f(c) = 0$.

**Note:** The IVT guarantees existence — it does not find the root. Numerical methods are needed for that — bisection in Lecture 3 this week, Newton's method in MATH 341.

### 5.2 The Bisection Algorithm

The IVT is the theoretical foundation of the **bisection method** for root-finding:
1. Start with $[a, b]$ where $f(a)$ and $f(b)$ have opposite signs
2. Compute midpoint $m = (a+b)/2$
3. If $f(m) = 0$: done. Otherwise, replace $[a,b]$ with $[a,m]$ or $[m,b]$ (whichever has a sign change)
4. Repeat — each step halves the interval size

After $n$ steps, root is located within an interval of length $(b-a)/2^n$. This is $O(\log n)$ convergence — a direct application of the IVT + binary search logic.

### 5.3 The Fixed Point Theorem (consequence of IVT)

> If $f: [a,b] \to [a,b]$ is continuous, then $f$ has a **fixed point**: a point $c \in [a,b]$ with $f(c) = c$.

*Proof:* Let $g(x) = f(x) - x$. Then $g(a) = f(a) - a \geq 0$ (since $f(a) \in [a,b]$) and $g(b) = f(b) - b \leq 0$. By IVT, $g(c) = 0$ for some $c$, i.e., $f(c) = c$. $\square$

**CS Connection:** Fixed-point iteration — the basis of many iterative numerical methods — is guaranteed to converge (under conditions) by this theorem. The `fix` combinator in functional programming is the computational analog.

---

## 6. Continuity and Limits — The Full Picture

The relationship between limits and continuity is subtle but important:

| Situation | $\lim_{x\to a} f(x)$ | $f(a)$ | Continuous? |
|-----------|----------------------|--------|-------------|
| Nice function, $a$ in domain | Exists, $= f(a)$ | Defined | ✅ Yes |
| Hole in graph | Exists, $\neq f(a)$ or $f(a)$ undefined | Maybe undefined | ❌ No (removable) |
| Jump | Both one-sided limits exist, unequal | Defined (one side) | ❌ No (jump) |
| Vertical asymptote | $\pm\infty$ | Undefined | ❌ No (infinite) |

A key theorem: **On its domain, every elementary function is continuous.** The only discontinuities you encounter in practice arise from:
- Points excluded from the domain
- Piecewise definitions with mismatched pieces
- Explicitly constructed examples

---

## 7. A Deeper Look: Why Continuity Makes Calculus Work

Without continuity, almost nothing in calculus holds:

- The derivative requires the limit of $\dfrac{f(x+h)-f(x)}{h}$ to exist — this is only possible if $f$ is "close to continuous" at that point
- The Fundamental Theorem of Calculus (Week 9) requires $f$ to be continuous on $[a,b]$
- Maximum and minimum values are guaranteed to exist on $[a,b]$ **only if $f$ is continuous** (Extreme Value Theorem — Week 6)
- The Mean Value Theorem requires continuity on $[a,b]$ and differentiability on $(a,b)$

Continuity is not a technicality. It is the structural hypothesis that makes analysis possible.

---

## Lecture 3 Exercises

1. Classify each discontinuity (removable, jump, infinite, or oscillatory) and where possible, remove it:
   - (a) $f(x) = \dfrac{x^2 - 4}{x - 2}$ at $x = 2$
   - (b) $g(x) = \dfrac{1}{(x-1)^2}$ at $x = 1$
   - (c) $h(x) = \begin{cases} x^2 & x \leq 0 \\ x + 1 & x > 0 \end{cases}$ at $x = 0$

2. Find all values of $c$ that make $f$ continuous everywhere:
   $$f(x) = \begin{cases} cx^2 + 2x & x < 2 \\ x^3 - cx & x \geq 2 \end{cases}$$

3. Use the IVT to prove that $\cos x = x$ has a solution in $(0, \pi/2)$. *(Define $g(x) = \cos x - x$ and apply IVT.)*

4. **(Bisection)** Use three steps of bisection to locate a root of $f(x) = x^3 - x - 2$ more precisely. Start with the interval $[1, 2]$.

5. **(Theory)** The IVT guarantees existence but not uniqueness. Give an example of a continuous function on $[0, 1]$ with $f(0) = 0$ and $f(1) = 1$ where the equation $f(x) = 1/2$ has exactly three solutions.

6. **(Challenge — Fixed Point)** Show that any continuous function $f: [0,1] \to [0,1]$ must have a fixed point. Can you construct a discontinuous function $f: [0,1] \to [0,1]$ with no fixed point?

---


### Answers

**1. (a) Removable.** $\dfrac{x^2-4}{x-2}=x+2$ for $x\neq2$, so the limit is $4$ while $f(2)$ is
undefined. Define $f(2)=4$ and the function becomes continuous.

**(b) Infinite.** $\dfrac{1}{(x-1)^2}\to+\infty$ from both sides. Not removable — no value assigned
at $x=1$ can repair an unbounded function.

**(c) Jump.** Left limit $\displaystyle\lim_{x\to0^-}x^2=0$; right limit
$\displaystyle\lim_{x\to0^+}(x+1)=1$. Both one-sided limits exist and **differ**, so no redefinition
helps.

**2.** Continuity at $x=2$ requires the two pieces to agree there:
$$c(2)^2+2(2)=2^3-c(2) \Rightarrow 4c+4=8-2c \Rightarrow 6c=4 \Rightarrow \boxed{c=\tfrac23}$$
*(Check: both sides equal $6.\overline{6}$.)* Each piece is a polynomial and so continuous on its own
side; matching the value at the join is the only condition.

**3.** Let $g(x)=\cos x-x$, continuous everywhere. Then $g(0)=1>0$ and
$g(\pi/2)=0-\pi/2\approx-1.571<0$. Since $g$ is continuous on the closed interval $[0,\pi/2]$ and
changes sign, the **IVT** guarantees some $c\in(0,\pi/2)$ with $g(c)=0$, i.e. $\cos c=c$.
$\blacksquare$ *(The root is $\approx0.739$, the "Dottie number".)*

**4.** $f(x)=x^3-x-2$ on $[1,2]$, with $f(1)=-2<0<4=f(2)$:

| Step | Interval | Width |
|---|---|---|
| 1 | $[1.5,\ 2]$ | $0.5$ |
| 2 | $[1.5,\ 1.75]$ | $0.25$ |
| 3 | $\boxed{[1.5,\ 1.625]}$ | $0.125$ |

The width halves each step — after $n$ steps it is $(b-a)/2^n$, which is why bisection needs
$n\geq\log_2\!\left((b-a)/\varepsilon\right)$ steps for tolerance $\varepsilon$. The true root is
$\approx1.5214$.

**5.** Any continuous "zigzag" crossing the level $y=\tfrac12$ three times works. For instance the
piecewise-linear function through
$$(0,0)\ \to\ (0.25,\ 1)\ \to\ (0.5,\ 0)\ \to\ (0.75,\ 1)\ \to\ (1,\ 1)$$
rises past $\tfrac12$, falls back through it, and rises through it again — three solutions of
$f(x)=\tfrac12$, with $f(0)=0$ and $f(1)=1$ as required.

**The IVT guarantees *at least one* crossing, never exactly one.** Claiming uniqueness needs a
separate argument, typically monotonicity ($f'>0$).

**6.** Let $g(x)=f(x)-x$, continuous on $[0,1]$. Since $f$ maps into $[0,1]$:
$$g(0)=f(0)-0=f(0)\geq0, \qquad g(1)=f(1)-1\leq0$$
If either is zero we have a fixed point already; otherwise $g$ changes sign and the IVT gives
$c\in(0,1)$ with $g(c)=0$, i.e. $\boxed{f(c)=c}$. $\blacksquare$

**Discontinuous counterexample:**
$$f(x)=\begin{cases}1 & x\leq\tfrac12\\[2pt] 0 & x>\tfrac12\end{cases}$$
It maps $[0,1]$ into $[0,1]$ but has **no fixed point**: for $x\leq\tfrac12$, $f(x)=1\neq x$ (since
$x\leq\tfrac12<1$); for $x>\tfrac12$, $f(x)=0\neq x$. Continuity is doing all the work in the
theorem — this is a one-dimensional case of the Brouwer fixed-point theorem.

*Next Week: Week 2 — The Derivative: Definition, Geometric Meaning, and Basic Rules*  
*Problem Set 1 released today (Wednesday). Due next Wednesday.*  
*Lab 1 is Friday — see lab instructions file.*
