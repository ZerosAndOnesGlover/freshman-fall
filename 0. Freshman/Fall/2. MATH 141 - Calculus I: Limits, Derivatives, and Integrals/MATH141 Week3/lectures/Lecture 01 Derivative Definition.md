# MATH 141 · Calculus I
## Week 3 · Lecture 1 (Monday)
### The Derivative: Definition, Geometric Meaning, and the Difference Quotient

**Date:** Monday 12 October 2026 · 11:00–11:50 · Week 3

---

**Reading:** Stewart §2.6–2.7 | Spivak Ch. 9 (Derivatives)
**Quiz 03** — this Monday, covers Week 2 (continuity, types of discontinuity, the IVT)

---

## The Problem That Created Calculus

Two problems drove the invention of calculus:

**Problem 1 — The Tangent Problem:** Given a curve $y = f(x)$ and a point $P$ on it, find the slope of the line tangent to the curve at $P$.

**Problem 2 — The Velocity Problem:** Given a position function $s(t)$, find the instantaneous velocity at time $t$.

These look different. They are the same problem. Both reduce to computing:

$$\lim_{h \to 0} \frac{f(a+h) - f(a)}{h}$$

This limit — when it exists — is called the **derivative**. It is the central object of differential calculus.

---

## 1. The Difference Quotient — Slope of a Secant

Consider the graph of $y = f(x)$ and two points on it:
- $P = (a,\, f(a))$ — fixed point
- $Q = (a+h,\, f(a+h))$ — nearby point, $h \neq 0$

The slope of the **secant line** $PQ$ is:

$$m_{PQ} = \frac{f(a+h) - f(a)}{(a+h) - a} = \frac{f(a+h) - f(a)}{h}$$

This is the **difference quotient**. It is the average rate of change of $f$ over the interval $[a,\, a+h]$.

**What happens as $h \to 0$?** The point $Q$ slides along the curve toward $P$. The secant line rotates and approaches the **tangent line** at $P$. The slope of the secant approaches the slope of the tangent.

---

## 2. The Derivative — Definition

> **Definition.** The **derivative of $f$ at $a$**, denoted $f'(a)$, is:
>
> $$f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}$$
>
> provided this limit exists.

If $f'(a)$ exists, we say $f$ is **differentiable at $a$**.

**Equivalent form** (with $x \to a$ instead of $h \to 0$, where $h = x - a$):

$$f'(a) = \lim_{x \to a} \frac{f(x) - f(a)}{x - a}$$

Both forms are used — choose whichever is more convenient.

---

## 3. Computing Derivatives from the Definition

The four-step process:
1. Write $f(a+h)$
2. Compute $f(a+h) - f(a)$
3. Divide by $h$ and simplify (cancel the $h$)
4. Take the limit as $h \to 0$

### Example 1 — Power Function: $f(x) = x^2$

$$f'(a) = \lim_{h\to 0}\frac{(a+h)^2 - a^2}{h} = \lim_{h\to 0}\frac{a^2 + 2ah + h^2 - a^2}{h} = \lim_{h\to 0}\frac{2ah + h^2}{h}$$

$$= \lim_{h\to 0}\frac{h(2a + h)}{h} = \lim_{h\to 0}(2a + h) = 2a$$

So $(x^2)' = 2x$. At any point $a$, the slope of $y = x^2$ is $2a$.

### Example 2 — Linear Function: $f(x) = mx + b$

$$f'(a) = \lim_{h\to 0}\frac{[m(a+h)+b] - [ma+b]}{h} = \lim_{h\to 0}\frac{mh}{h} = m$$

A linear function has constant derivative equal to its slope. Makes geometric sense.

### Example 3 — Square Root: $f(x) = \sqrt{x}$

$$f'(a) = \lim_{h\to 0}\frac{\sqrt{a+h} - \sqrt{a}}{h}$$

Rationalize by multiplying by $\dfrac{\sqrt{a+h}+\sqrt{a}}{\sqrt{a+h}+\sqrt{a}}$:

$$= \lim_{h\to 0}\frac{(a+h) - a}{h(\sqrt{a+h}+\sqrt{a})} = \lim_{h\to 0}\frac{h}{h(\sqrt{a+h}+\sqrt{a})} = \lim_{h\to 0}\frac{1}{\sqrt{a+h}+\sqrt{a}} = \frac{1}{2\sqrt{a}}$$

So $(\sqrt{x})' = \dfrac{1}{2\sqrt{x}}$ for $x > 0$.

### Example 4 — Reciprocal: $f(x) = \dfrac{1}{x}$

$$f'(a) = \lim_{h\to 0}\frac{\frac{1}{a+h} - \frac{1}{a}}{h} = \lim_{h\to 0}\frac{\frac{a-(a+h)}{a(a+h)}}{h} = \lim_{h\to 0}\frac{-h}{h \cdot a(a+h)} = \lim_{h\to 0}\frac{-1}{a(a+h)} = \frac{-1}{a^2}$$

So $(1/x)' = -1/x^2$.

---

## 4. The Derivative as a Function

When we let $a$ vary, replacing it with $x$, the derivative becomes a new function:

$$f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$$

**Notation — four equivalent ways to write the derivative:**

| Notation | Read as | Credit |
|----------|---------|--------|
| $f'(x)$ | "$f$ prime of $x$" | Lagrange |
| $\dfrac{dy}{dx}$ | "$dy$ by $dx$" | Leibniz |
| $\dfrac{d}{dx}[f(x)]$ | "$d$ by $dx$ of $f$" | Leibniz |
| $\dot{y}$ | "$y$ dot" | Newton (physics) |

Leibniz notation $\dfrac{dy}{dx}$ is not a fraction — it is a limit. But it behaves like a fraction in many contexts (Chain Rule, related rates), which is why it's powerful and widely used.

**Evaluated at a point:** $f'(a) = \left.\dfrac{dy}{dx}\right|_{x=a}$

---

## 5. Geometric Interpretation

$f'(a)$ is the **slope of the tangent line** to $y = f(x)$ at the point $(a, f(a))$.

**Equation of the tangent line at $(a, f(a))$:**

$$y - f(a) = f'(a)(x - a) \qquad \text{i.e.,} \qquad y = f(a) + f'(a)(x-a)$$

This is the **linearization** of $f$ at $a$ — it's the best linear approximation to $f$ near $a$.

**Example:** Find the tangent line to $y = x^2$ at $x = 3$.

$f(3) = 9$, $f'(3) = 2(3) = 6$.

Tangent line: $y - 9 = 6(x-3)$, i.e., $y = 6x - 9$.

---

## 6. Physical Interpretation — Rates of Change

If $s(t)$ is position at time $t$:
- $\dfrac{s(t+h)-s(t)}{h}$ = average velocity over $[t,\, t+h]$
- $s'(t) = \lim_{h\to 0}\dfrac{s(t+h)-s(t)}{h}$ = **instantaneous velocity** at $t$
- $v'(t) = s''(t)$ = **acceleration**

More generally: $f'(a)$ is the **instantaneous rate of change** of $f$ with respect to $x$ at $x = a$.

**Units:** If $y = f(x)$ with $y$ in meters and $x$ in seconds, then $f'$ is in meters/second.

The derivative captures how fast a quantity is changing — it is the mathematical formalization of "speed" in the most general possible sense.

---

## 7. When Is a Function NOT Differentiable?

$f$ fails to be differentiable at $a$ in three ways:

### 7.1 — Corner (Kink)
$f(x) = |x|$ at $x = 0$:
- $\displaystyle\lim_{h\to 0^-}\frac{|h|}{h} = -1$ (left derivative)
- $\displaystyle\lim_{h\to 0^+}\frac{|h|}{h} = +1$ (right derivative)

One-sided derivatives exist but differ → no derivative at $x = 0$.

### 7.2 — Vertical Tangent
$f(x) = x^{1/3}$ at $x = 0$:
$$\frac{f(0+h)-f(0)}{h} = \frac{h^{1/3}}{h} = h^{-2/3} \to \infty$$

The tangent is vertical (slope infinite) → not differentiable.

### 7.3 — Discontinuity
If $f$ is not continuous at $a$, it cannot be differentiable there.

**Theorem:** Differentiable at $a$ $\Rightarrow$ continuous at $a$.

**Contrapositive:** Discontinuous at $a$ $\Rightarrow$ not differentiable at $a$.

**Warning:** The converse is FALSE. Continuous at $a$ does NOT imply differentiable at $a$ (corners and cusps are continuous but not differentiable). Weierstrass even constructed a function continuous everywhere but differentiable nowhere.

---

## 8. Connection to Computer Science

### The Derivative as a Local Linear Model
Near any differentiable point, $f(x) \approx f(a) + f'(a)(x-a)$. This is the foundation of:
- **Newton's method** for root-finding (MATH 341): uses the tangent line to approximate where $f = 0$
- **Gradient descent** in machine learning: the gradient generalizes the derivative to multiple variables; each training step moves in the direction of the negative gradient
- **Taylor approximations** (Week 12): polynomials built from successive derivatives

### Numerical Differentiation
Computers approximate derivatives using finite differences:
$$f'(x) \approx \frac{f(x+h) - f(x)}{h} \quad \text{(forward difference)}$$
$$f'(x) \approx \frac{f(x+h) - f(x-h)}{2h} \quad \text{(central difference — more accurate)}$$

The central difference has error $O(h^2)$ vs $O(h)$ for the forward difference. The derivative definition itself tells you why: the central form is a better symmetric approximation to the limit.

### Automatic Differentiation
Modern ML frameworks (PyTorch, JAX) compute derivatives **exactly** (not numerically) using the chain rule applied symbolically to computation graphs. Understanding the mathematical derivative is the prerequisite to understanding how backpropagation works.

---

## 9. Common Errors

**1. Cancelling $h$ before it is legal.** In $\frac{(x+h)^3-x^3}{h}$ you may cancel $h$ only after
expanding and factoring it out of *every* surviving term. Cancelling early — or worse, setting
$h=0$ in the numerator — destroys the limit.

**2. Setting $h=0$ instead of taking a limit.** The quotient is $\tfrac00$ at $h=0$; that is the
whole difficulty. The algebra exists to remove the $h$ from the denominator so that substitution
becomes *legal*.

**3. Confusing $f'(a)$ with $f'(x)$.** $f'(a)$ is a **number** — the slope at one point. $f'(x)$ is
a **function**. A tangent-line problem needs $f'$ evaluated at the point of tangency, and the
commonest wrong answer substitutes the wrong $x$.

**4. Differentiating by rule when the definition is demanded.** "From the definition" means the
difference-quotient limit. Using the power rule earns the answer marks and none of the method
marks — and the point of §3 is that the rules are *consequences* of the definition.

**5. Assuming continuity implies differentiability.** It does not — $|x|$ at $0$ is the standard
counterexample. The converse *is* true: differentiable $\Rightarrow$ continuous.

---

## Lecture 1 Exercises

1. Using the limit definition, find $f'(x)$ for each:
   - (a) $f(x) = x^3$
   - (b) $f(x) = \dfrac{1}{x+2}$
   - (c) $f(x) = \sqrt{2x+1}$

2. Find the equation of the tangent line to $y = \dfrac{1}{x}$ at $x = 2$.

3. A particle's position is $s(t) = t^2 - 4t + 3$ meters, $t$ in seconds.
   - (a) Find the velocity function $v(t) = s'(t)$ using the definition.
   - (b) When is the particle at rest?
   - (c) When is it moving forward (positive velocity)?

4. Show using the definition that $f(x) = |x - 3|$ is not differentiable at $x = 3$.

5. **(Thinking)** The function $f(x) = x\sin(1/x)$ for $x\neq 0$ and $f(0) = 0$ is continuous at 0 (we showed this in Lab 1). Is it differentiable at 0? Compute $\lim_{h\to0}\frac{f(h)-f(0)}{h}$ and interpret.

---

### Answers

All results verified numerically.

**1.** Each uses $\displaystyle f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$.

**(a)** $\dfrac{(x+h)^3-x^3}{h}=\dfrac{3x^2h+3xh^2+h^3}{h}=3x^2+3xh+h^2 \to \boxed{3x^2}$

**(b)** $\dfrac{1}{h}\left[\dfrac{1}{x+h+2}-\dfrac{1}{x+2}\right]
=\dfrac{-h}{h(x+h+2)(x+2)} \to \boxed{-\dfrac{1}{(x+2)^2}}$

**(c)** Multiply by the conjugate:
$$\frac{\sqrt{2(x+h)+1}-\sqrt{2x+1}}{h}\cdot\frac{\sqrt{2(x+h)+1}+\sqrt{2x+1}}{\sqrt{2(x+h)+1}+\sqrt{2x+1}}
=\frac{2}{\sqrt{2(x+h)+1}+\sqrt{2x+1}} \to \boxed{\dfrac{1}{\sqrt{2x+1}}}$$
The conjugate trick is the same device that stabilises the limit in Lab 1 §1.2 — algebra that
removes a cancellation is exactly what makes a limit computable *and* numerically safe.

**2.** $y=1/x$, $y'=-1/x^2$. At $x=2$: point $(2,\tfrac12)$, slope $-\tfrac14$.
$$y-\tfrac12=-\tfrac14(x-2) \Rightarrow \boxed{y=-\tfrac{x}{4}+1}$$

**3.** $s(t)=t^2-4t+3$.
**(a)** From the definition, $v(t)=\boxed{2t-4}$ m/s.
**(b)** At rest when $v=0$: $\boxed{t=2}$ s.
**(c)** Moving forward when $v>0$: $\boxed{t>2}$. For $t<2$ the particle moves backward, turning
around at $t=2$ — so *distance travelled* and *displacement* differ on any interval containing 2.

**4.** $\dfrac{|3+h-3|-0}{h}=\dfrac{|h|}{h}$, which is $+1$ for $h>0$ and $-1$ for $h<0$. The
one-sided limits are $+1$ and $-1$; they disagree, so the limit — and the derivative — **does not
exist**. The graph has a corner, yet $f$ is perfectly continuous at 3.

**5.** $\dfrac{f(h)-f(0)}{h}=\dfrac{h\sin(1/h)}{h}=\sin(1/h)$.

As $h\to0$ this oscillates through every value in $[-1,1]$ infinitely often — sampling $h=10^{-2},
10^{-3}, 10^{-4}$ gives $-0.506$, $+0.827$, $-0.306$. **The limit does not exist, so $f$ is not
differentiable at 0** despite being continuous there.

Instructive contrast: $g(x)=x^2\sin(1/x)$ **is** differentiable at 0, because the quotient becomes
$h\sin(1/h)$, which the squeeze theorem sends to 0. One extra factor of $x$ converts a
non-differentiable point into a differentiable one — and $g'$ is still discontinuous at 0, showing
"differentiable" does not imply "continuously differentiable".

---

*Next: Tuesday — Differentiation Rules: Power, Constant, Sum, Product, Quotient*
