# MATH 141 · Calculus I
## Problem Set 3
### Topic: The Derivative — Definition, Rules, and Applications
**Released:** Wednesday, Week 3 · **Due:** Wednesday, Week 4 (start of class)

---

**Instructions:** Show all work. State which rule(s) you use at each step. Box final answers. Collaboration on ideas is permitted; all writing must be your own.

---

## Part A — Derivatives from the Definition (5 pts each)

For each function, compute $f'(x)$ using the limit definition $\displaystyle f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$. Do NOT use differentiation rules.

**A1.** $f(x) = 4x^2 - 3x + 1$

**A2.** $f(x) = \dfrac{1}{2x+3}$

**A3.** $f(x) = \sqrt{x+4}$

**A4.** A function $f$ satisfies $f(x+h) - f(x) = 3x^2h + 3xh^2 + h^3$ for all $x, h$.
- (a) Find $f'(x)$ using the definition.
- (b) What is $f(x)$? (Recall: what function has this property?)

---

## Part B — Differentiation Rules (3 pts each)

Differentiate. Simplify where reasonable. State every rule used.

**B1.** $y = 7x^6 - 4x^{3/2} + \dfrac{2}{x^2} - \pi$

**B2.** $y = (x^2+3)(x^3-5x+1)$ — use the product rule (do NOT expand first)

**B3.** $y = \dfrac{3x^2 - 2x + 1}{x^2 + 1}$

**B4.** $y = x^3\sin x$

**B5.** $y = \dfrac{\cos x}{1 + \sin x}$

**B6.** $y = (2x^3 - x + 4)^6$

**B7.** $y = \sin(4x^2 - 1)$

**B8.** $y = e^{3x^2+2x}$

**B9.** $y = \sqrt{\tan x}$

**B10.** $y = \cos^3(x^2)$ — three layers; identify each before differentiating

**B11.** $y = \dfrac{e^x}{x^2+1}$

**B12.** $y = x^2 e^{-x}\sin x$ — requires product rule twice (or extended product rule)

---

## Part C — Tangent Lines and Linear Approximation (5 pts each)

**C1.** Find the equation of the tangent line and normal line to $y = x^3 - 4x$ at the point $(2, 0)$.

*(The normal line is perpendicular to the tangent line at the point of tangency.)*

**C2.** Find all points on the curve $y = x^4 - 2x^2$ where the tangent line is horizontal.

**C3.** The tangent line to $y = f(x)$ at $x = 1$ passes through the point $(4, 10)$, and $f(1) = 4$. Find $f'(1)$.

**C4.** Use the linearization $L(x) = f(a) + f'(a)(x-a)$ to approximate:
- (a) $\sqrt{9.04}$ by linearizing $f(x) = \sqrt{x}$ at $a = 9$
- (b) $(1.002)^{10}$ by linearizing $f(x) = x^{10}$ at $a = 1$

For each, compute the exact value with a calculator and find the percentage error.

---

## Part D — Higher-Order Derivatives and Physics (4 pts each)

**D1.** For $f(x) = x^5 - 10x^3 + 15x$, find $f'(x)$, $f''(x)$, $f'''(x)$, and $f^{(4)}(x)$.

**D2.** Find $y''$ for $y = x\cos x$.

**D3.** A particle moves along a line with position $s(t) = t^3 - 6t^2 + 9t + 2$ (meters, $t$ in seconds, $t \geq 0$).

- (a) Find the velocity $v(t) = s'(t)$ and acceleration $a(t) = s''(t)$.
- (b) When is the particle at rest?
- (c) When is the particle moving in the positive direction?
- (d) When is the acceleration positive? What does this mean physically?
- (e) Find the total distance traveled in the first 4 seconds. *(Hint: find where velocity changes sign.)*

**D4.** Prove that $y = e^{-x}\sin x$ satisfies the equation $y'' + 2y' + 2y = 0$.

*(This is a second-order linear ODE — the type governing damped oscillators in physics and electrical circuits. You'll see these again in differential equations.)*

---

## Part E — Chain Rule and Composition (4 pts each)

**E1.** Find $\dfrac{dy}{dx}$ using the chain rule. Identify the outer and inner functions explicitly before differentiating.

- (a) $y = \sin^5(3x)$
- (b) $y = e^{\cos(2x)}$
- (c) $y = \left(\dfrac{x+1}{x-1}\right)^3$

**E2.** The following information is known:

| $x$ | $f(x)$ | $f'(x)$ | $g(x)$ | $g'(x)$ |
|-----|--------|---------|--------|---------|
| 1 | 3 | $-2$ | 2 | 5 |
| 2 | 1 | 4 | 1 | $-3$ |
| 3 | 2 | 1 | 3 | 0 |

Find:
- (a) $(f\circ g)'(1)$
- (b) $(g\circ f)'(2)$
- (c) $\left(\dfrac{f}{g}\right)'(3)$
- (d) $(f\cdot g\circ f)'(1)$

---

## Part F — Conceptual Understanding (5 pts each)

**F1.** A student claims: "Since $(fg)' = f'g + fg'$, we have $(fff)' = f'ff + ff'f + fff' = 3f^2f'$ by the same logic." Is the student correct? Either justify the claim by applying the product rule twice, or find the error.

**F2.** Explain in precise mathematical language why the statement "the slope of $y = x^2$ at $x = 3$ is $6$" means $\displaystyle\lim_{h\to0}\frac{(3+h)^2 - 9}{h} = 6$. Then verify this limit algebraically.

**F3 (Differentiability vs Continuity).** For each function, determine: is $f$ continuous at $x=0$? Is $f$ differentiable at $x=0$? Justify each answer.

- (a) $f(x) = |x|$
- (b) $f(x) = x|x|$
- (c) $f(x) = \begin{cases} x^2\sin(1/x) & x\neq 0 \\ 0 & x=0 \end{cases}$

*(Part (c) is hard — compute the derivative from the definition directly.)*

---

## Part G — Challenge (6 pts bonus)

**G1.** Prove the **quotient rule** from the **product rule** and the **chain rule** as follows:

Write $\dfrac{f}{g} = f\cdot(g)^{-1}$. Apply the product rule to get $\left(\dfrac{f}{g}\right)' = f'\cdot g^{-1} + f\cdot(g^{-1})'$.

Then use the chain rule to find $(g^{-1})' = \dfrac{d}{dx}[g(x)^{-1}]$.

Combine to recover the standard quotient rule formula.

**G2.** A function $f$ is differentiable everywhere and satisfies $f(x+y) = f(x)f(y)$ for all $x, y\in\mathbb{R}$, and $f(0) = 1$, $f'(0) = k$.

- (a) Show $f(0) = 1$ is consistent with the functional equation.
- (b) Differentiate both sides of $f(x+y)=f(x)f(y)$ with respect to $x$ (treating $y$ as constant), then set $x=0$ to show $f'(y) = k\cdot f(y)$.
- (c) What well-known function satisfies both $f(x+y)=f(x)f(y)$ and $f'(x)=kf(x)$?

---

## Grading Summary

| Part | Points | Focus |
|------|--------|-------|
| A (4 × 5) | 20 | Definition — no rules allowed |
| B (12 × 3) | 36 | Rule fluency |
| C (4 × 5) | 20 | Geometric applications |
| D (4 × 4) | 16 | Higher derivatives, physics |
| E (2 × 4) | 8 | Chain rule depth |
| F (3 × 5) | 15 | Conceptual understanding |
| G bonus | 12 | Proof and theory |
| **Total** | **115 + 12 bonus** | |
