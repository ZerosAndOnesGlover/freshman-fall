# MATH 141 · Problem Set 3 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

---


## Marking Scheme

Point values are printed per problem on the problem set. Within each problem, split the marks:

- **Method (≈60%).** Correct technique named and set up: the right rule or theorem, hypotheses checked where the theorem requires it, and the symbolic work shown before any numerical evaluation.
- **Execution (≈40%).** Correct algebra and simplification, correct final form, and any domain restrictions or constants of integration stated.

A bare answer with no working earns at most the execution marks — and in proof problems ("show that", "prove"), no marks at all, since the reasoning *is* the deliverable.

**Carry-through.** Penalise a given error once. If the student proceeds correctly from their own wrong intermediate value, award the downstream marks in full.

**Equivalent forms.** Accept any algebraically equivalent answer — factored or expanded, and trigonometric identities applied or not — unless the problem explicitly demands a particular form.

### Common errors in this problem set

**1. Confusing the derivative at a point with the derivative function.** f′(a) is a number; f′(x) is a function. Tangent-line problems need f′ evaluated **at the point of tangency**, not at the x the student happens to be solving for.

**2. Losing the definition when asked for it.** 'From the definition' means the difference quotient limit. Differentiating by rule — the rules are Week 4 — earns the answer marks only.

*(Revised 2026-09-26: the set was cut to 7 problems. The solutions below follow the new numbering.)*

---

## Problem 1 — From the Definition (24)

**(a)** $f(x) = 4x^2-3x+1$

$$\frac{f(x+h)-f(x)}{h}=\frac{4(x+h)^2-3(x+h)+1-(4x^2-3x+1)}{h}=\frac{8xh+4h^2-3h}{h}=8x+4h-3$$

$f'(x)=\lim_{h\to0}(8x+4h-3)=8x-3$

---

**(b)** $f(x)=\frac{1}{2x+3}$

$$\frac{f(x+h)-f(x)}{h}=\frac{\frac{1}{2(x+h)+3}-\frac{1}{2x+3}}{h}=\frac{(2x+3)-(2x+2h+3)}{h(2x+2h+3)(2x+3)}=\frac{-2h}{h(2x+2h+3)(2x+3)}$$

$$=\frac{-2}{(2x+2h+3)(2x+3)}\to\frac{-2}{(2x+3)^2}$$

$f'(x)=\dfrac{-2}{(2x+3)^2}$

---

**(c)** $f(x)=\sqrt{x+4}$

$$\frac{\sqrt{x+h+4}-\sqrt{x+4}}{h}\cdot\frac{\sqrt{x+h+4}+\sqrt{x+4}}{\sqrt{x+h+4}+\sqrt{x+4}}=\frac{h}{h(\sqrt{x+h+4}+\sqrt{x+4})}\to\frac{1}{2\sqrt{x+4}}$$

$f'(x)=\dfrac{1}{2\sqrt{x+4}}$

---

## Problem 2 — Working Backwards (10)

**(a)** $\displaystyle\frac{f(x+h)-f(x)}{h}=\frac{3x^2h+3xh^2+h^3}{h}=3x^2+3xh+h^2\to3x^2$

So $f'(x)=3x^2$.

**(b)** $f(x)=x^3$ (since $(x+h)^3-x^3=3x^2h+3xh^2+h^3$).

---

## Problem 3 — A Tangent Line (12)

$\dfrac{(x+h)^3-x^3}{h} = 3x^2+3xh+h^2 \to 3x^2$. At $x=2$: $f(2)=8$, slope $12$, tangent $y = 12x - 16$.

## Problem 4 — A Tangent Through a Point (8)

The tangent passes through $(1,4)$ and $(4,10)$, so its slope is $\dfrac{10-4}{4-1} = 2 = f'(1)$.

## Problem 5 — Velocity (15)

(a) $\dfrac{s(t+h)-s(t)}{h} = \dfrac{2th+h^2-6h}{h} = 2t+h-6 \to v(t) = 2t-6$ m/s.
(b) $v = 0$ at $t = 3$ s, where $s(3) = 9-18+5 = -4$ m. (c) $v > 0$ for $t > 3$.

---

## Problem 6 — Differentiability vs Continuity (16)

**(a)** $|x|$: continuous at 0 ✓. Difference quotient $|h|/h$ is $-1$ from the left and $+1$ from the right → the limit
does not exist → not differentiable.

**(b)** $x|x|$: continuous at 0 ✓. $\frac{h|h|}{h} = |h| \to 0$ → differentiable, $f'(0)=0$.

---

## Problem 7 — What "Slope at a Point" Means (15)

The slope of the tangent at $x=3$ is by definition the limit of secant slopes $\frac{f(3+h)-f(3)}{h}$ as $h\to0$:
$\lim_{h\to0}\frac{9+6h+h^2-9}{h} = \lim_{h\to0}(6+h) = 6$ ✓

*(7 for the explanation: tangent slope defined as the limit of secant slopes; 8 for the algebra.)*

---

*MATH 141 · Week 3 · Problem Set 3 Solutions · © CSE Department*
