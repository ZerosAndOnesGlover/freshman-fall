# MATH 141 · Calculus I
## Problem Set 3
### Topic: The Derivative — Definition, Tangent Lines, and Differentiability
**Released:** Wednesday 14 October 2026, 12:00 (after Lecture 03) · Week 3
**Due:** Wednesday 21 October 2026, 11:00 (start of class) · Week 4 — late penalty after 11:00
**Total:** 100 points

**What this uses:** Week 3 only — the limit definition of the derivative (Lecture 01), the derivative as a
function and numerical difference quotients (Lecture 02), and differentiability versus continuity
(Lecture 03), plus Weeks 1–2's limits and continuity.

**Not needed, and not allowed:** the differentiation rules (power, product, quotient, chain), which are
Week 4. Every derivative here is computed **from the definition**.

> *Revised 2026-09-21.* The earlier version was titled "Definition, Rules, and Applications": 36 points of
> rule drills, a chain-rule part, higher derivatives, an ODE check and a quotient-rule proof, all of which need
> Week 4 lectures that had not happened when the set was released. Rule practice is Problem Set 4's job.

---

**Instructions:** Show all work. Box final answers. Collaboration on ideas is permitted; all writing must be your own.

---

## Part A — Derivatives from the Definition (32 pts, 8 each)

For each function, compute $f'(x)$ using $\displaystyle f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$.

**A1.** $f(x) = 4x^2 - 3x + 1$

**A2.** $f(x) = \dfrac{1}{2x+3}$

**A3.** $f(x) = \sqrt{x+4}$ *(rationalize the numerator)*

**A4.** A function $f$ satisfies $f(x+h) - f(x) = 3x^2h + 3xh^2 + h^3$ for all $x, h$.
- (a) Find $f'(x)$ using the definition.
- (b) Name a function $f$ with this property.

---

## Part B — Tangent Lines and Velocity (32 pts)

**B1.** *(8 pts)* For $f(x) = x^3$, find $f'(x)$ from the definition (expand $(x+h)^3$). Then write the equation of
the tangent line at $x = 2$.

**B2.** *(8 pts)* For $y = x^3 - 4x$, find $y'$ from the definition and the tangent line at the point $(2, 0)$.

**B3.** *(6 pts)* The tangent line to $y = f(x)$ at $x = 1$ passes through the point $(4, 10)$, and $f(1) = 4$. Find $f'(1)$.

**B4.** *(10 pts)* A particle moves along a line with position $s(t) = t^2 - 6t + 5$ metres ($t$ in seconds, $t \ge 0$).

- (a) Find the velocity $v(t) = s'(t)$ **from the definition**.
- (b) When is the particle at rest, and where is it then?
- (c) When is it moving in the positive direction?

---

## Part C — Conceptual Understanding (36 pts)

**C1.** *(8 pts)* Explain in precise language why the statement "the slope of $y = x^2$ at $x = 3$ is $6$" means
$\displaystyle\lim_{h\to0}\frac{(3+h)^2 - 9}{h} = 6$. Then verify the limit algebraically.

**C2 (Differentiability vs Continuity).** *(15 pts, 5 each)* Is $f$ continuous at $x=0$? Is $f$ differentiable at
$x=0$? Justify each from the definitions.

- (a) $f(x) = |x|$
- (b) $f(x) = x|x|$
- (c) $f(x) = \begin{cases} x^2\sin(1/x) & x\neq 0 \\ 0 & x=0 \end{cases}$ *(use the Squeeze Theorem on the difference quotient)*

**C3 (Numerical derivative).** *(13 pts)* For $f(x) = 2^x$, compute the forward difference quotient
$\dfrac{f(1+h)-f(1)}{h}$ and the central difference quotient $\dfrac{f(1+h)-f(1-h)}{2h}$ for $h = 0.1, 0.01, 0.001$
(calculator or Python), to six decimal places. Which converges faster? The exact value is $2\ln 2 \approx 1.386294$ (you will derive it in Week 5); how many
correct digits does each quotient give at $h = 0.001$?

---

## Grading Summary

| Part | Points | Focus |
|------|--------|-------|
| A | 32 | Derivatives from the definition |
| B | 32 | Tangent lines and velocity |
| C | 36 | Meaning, differentiability, numerical derivatives |
| **Total** | **100** | |
