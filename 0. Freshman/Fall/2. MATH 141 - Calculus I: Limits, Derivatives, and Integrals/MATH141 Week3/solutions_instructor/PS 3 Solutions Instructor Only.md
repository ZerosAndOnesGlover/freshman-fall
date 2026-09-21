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

**1. Product and quotient rules as products/quotients of derivatives.** (fg)′ ≠ f′g′. This is a definition-level error; award no method marks where it appears.

**2. Omitting the inner derivative in the chain rule.** d/dx[f(g(x))] = f′(g(x))·g′(x). The missing g′(x) is the single most common differentiation error in the course.

**3. Confusing the derivative at a point with the derivative function.** f′(a) is a number; f′(x) is a function. Tangent-line problems need f′ evaluated **at the point of tangency**, not at the x the student happens to be solving for.

**4. Losing the definition when asked for it.** 'From the definition' means the difference quotient limit. Differentiating by rule when the problem demands the definition earns the answer marks only.

---

## Part A — From the Definition

**A1.** $f(x) = 4x^2-3x+1$

$$\frac{f(x+h)-f(x)}{h}=\frac{4(x+h)^2-3(x+h)+1-(4x^2-3x+1)}{h}=\frac{8xh+4h^2-3h}{h}=8x+4h-3$$

$f'(x)=\lim_{h\to0}(8x+4h-3)=8x-3$

---

**A2.** $f(x)=\frac{1}{2x+3}$

$$\frac{f(x+h)-f(x)}{h}=\frac{\frac{1}{2(x+h)+3}-\frac{1}{2x+3}}{h}=\frac{(2x+3)-(2x+2h+3)}{h(2x+2h+3)(2x+3)}=\frac{-2h}{h(2x+2h+3)(2x+3)}$$

$$=\frac{-2}{(2x+2h+3)(2x+3)}\to\frac{-2}{(2x+3)^2}$$

$f'(x)=\dfrac{-2}{(2x+3)^2}$

---

**A3.** $f(x)=\sqrt{x+4}$

$$\frac{\sqrt{x+h+4}-\sqrt{x+4}}{h}\cdot\frac{\sqrt{x+h+4}+\sqrt{x+4}}{\sqrt{x+h+4}+\sqrt{x+4}}=\frac{h}{h(\sqrt{x+h+4}+\sqrt{x+4})}\to\frac{1}{2\sqrt{x+4}}$$

$f'(x)=\dfrac{1}{2\sqrt{x+4}}$

---

**A4(a).** $\displaystyle\frac{f(x+h)-f(x)}{h}=\frac{3x^2h+3xh^2+h^3}{h}=3x^2+3xh+h^2\to3x^2$

So $f'(x)=3x^2$.

**A4(b).** $f(x)=x^3$ (since $(x+h)^3-x^3=3x^2h+3xh^2+h^3$).

---

## Part B — Tangent Lines and Velocity

**B1.** $\dfrac{(x+h)^3-x^3}{h} = 3x^2+3xh+h^2 \to 3x^2$. At $x=2$: $f(2)=8$, slope $12$, tangent $y = 12x - 16$.

**B2.** $\dfrac{[(x+h)^3-4(x+h)]-[x^3-4x]}{h} = 3x^2+3xh+h^2-4 \to 3x^2-4$. At $(2,0)$: slope $8$, tangent $y = 8x - 16$.

**B3.** The tangent passes through $(1,4)$ and $(4,10)$, so its slope is $\dfrac{10-4}{4-1} = 2 = f'(1)$.

**B4.** (a) $\dfrac{s(t+h)-s(t)}{h} = \dfrac{2th+h^2-6h}{h} = 2t+h-6 \to v(t) = 2t-6$ m/s.
(b) $v = 0$ at $t = 3$ s, where $s(3) = 9-18+5 = -4$ m. (c) $v > 0$ for $t > 3$.

---

## Part C — Conceptual

**C1.** The slope of the tangent at $x=3$ is by definition the limit of secant slopes $\frac{f(3+h)-f(3)}{h}$ as $h\to0$:
$\lim_{h\to0}\frac{9+6h+h^2-9}{h} = \lim_{h\to0}(6+h) = 6$ ✓

**C2(a).** $|x|$: continuous at 0 ✓. Difference quotient $|h|/h$ is $-1$ from the left and $+1$ from the right → the limit
does not exist → not differentiable.

**C2(b).** $x|x|$: continuous at 0 ✓. $\frac{h|h|}{h} = |h| \to 0$ → differentiable, $f'(0)=0$.

**C2(c).** Continuous: $|x^2\sin(1/x)| \le x^2 \to 0 = f(0)$. Difference quotient: $\frac{h^2\sin(1/h)}{h} = h\sin(1/h)$, and
$|h\sin(1/h)| \le |h| \to 0$ → **differentiable, $f'(0) = 0$** by the Squeeze Theorem.
*(Correction, 2026-09-21: the previous key said "not differentiable" — it had divided $h\sin(1/h)$ by $h$ a second time.
The function that is continuous but not differentiable at 0 is $x\sin(1/x)$, from PS 1's old bonus.)*

**C3.** (computed to six decimals)

| $h$ | forward | central |
|---|---|---|
| 0.1 | 1.435469 | 1.387405 |
| 0.01 | 1.391110 | 1.386305 |
| 0.001 | 1.386775 | 1.386294 |

Exact $2\ln2 = 1.386294$. The central quotient converges much faster: at $h=0.001$ it is correct to all six decimals shown,
the forward quotient only to about three (error ≈ 0.0005, shrinking like $h$; the central error shrinks like $h^2$).
*(5 table, 4 comparison, 4 digit count.)*
