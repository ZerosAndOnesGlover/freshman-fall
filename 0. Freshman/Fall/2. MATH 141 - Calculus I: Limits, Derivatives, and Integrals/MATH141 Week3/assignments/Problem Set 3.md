# MATH 141 · Calculus I
## Problem Set 3
### Topic: The Derivative — Definition, Tangent Lines, and Differentiability
**Released:** Wednesday 14 October 2026, 12:00 (after Lecture 03) · Week 3
**Due:** Wednesday 21 October 2026, 11:00 (start of class) · Week 4 — late penalty after 11:00
**Expected time:** about 3 hours — 7 problems, 13 parts
**Total:** 100 points

**What this uses:** Week 3 only — the limit definition of the derivative (Lecture 01), the derivative as a
function (Lecture 02), and differentiability versus continuity (Lecture 03), plus Weeks 1–2's limits and
continuity.

**Not needed, and not allowed:** the differentiation rules (power, product, quotient, chain), which are
Week 4. Every derivative here is computed **from the definition**.

> *Revised 2026-09-21.* The earlier version was titled "Definition, Rules, and Applications": 36 points of
> rule drills, a chain-rule part, higher derivatives, an ODE check and a quotient-rule proof, all of which need
> Week 4 lectures that had not happened when the set was released. Rule practice is Problem Set 4's job.
>
> *Revised 2026-09-26.* Cut from 11 problems to 7 to fit about three hours. The second cubic tangent line,
> the $x^2\sin(1/x)$ case and the numerical-derivative table (Lab 03 Part 4 does the same comparison) were
> removed.

---

**Instructions:** Show all work. Box final answers. Collaboration on ideas is permitted; all writing must be your own.

---

## Problem 1: Derivatives from the Definition (24 points)

For each function, compute $f'(x)$ using $\displaystyle f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$. *(8 pts each)*

**(a)** $f(x) = 4x^2 - 3x + 1$

**(b)** $f(x) = \dfrac{1}{2x+3}$

**(c)** $f(x) = \sqrt{x+4}$ *(rationalize the numerator)*

---

## Problem 2: Working Backwards (10 points)

A function $f$ satisfies $f(x+h) - f(x) = 3x^2h + 3xh^2 + h^3$ for all $x, h$.

**(a)** Find $f'(x)$ using the definition. *(6 pts)*

**(b)** Name a function $f$ with this property. *(4 pts)*

---

## Problem 3: A Tangent Line (12 points)

For $f(x) = x^3$, find $f'(x)$ from the definition (expand $(x+h)^3$). Then write the equation of the
tangent line at $x = 2$.

---

## Problem 4: A Tangent Through a Point (8 points)

The tangent line to $y = f(x)$ at $x = 1$ passes through the point $(4, 10)$, and $f(1) = 4$. Find $f'(1)$.

---

## Problem 5: Velocity (15 points)

A particle moves along a line with position $s(t) = t^2 - 6t + 5$ metres ($t$ in seconds, $t \ge 0$).

**(a)** Find the velocity $v(t) = s'(t)$ **from the definition**. *(7 pts)*

**(b)** When is the particle at rest, and where is it then? *(4 pts)*

**(c)** When is it moving in the positive direction? *(4 pts)*

---

## Problem 6: Differentiability vs Continuity (16 points)

Is $f$ continuous at $x=0$? Is $f$ differentiable at $x=0$? Justify each from the definitions. *(8 pts each)*

**(a)** $f(x) = |x|$

**(b)** $f(x) = x|x|$

---

## Problem 7: What "Slope at a Point" Means (15 points)

Explain in precise language why the statement "the slope of $y = x^2$ at $x = 3$ is $6$" means
$\displaystyle\lim_{h\to0}\frac{(3+h)^2 - 9}{h} = 6$. Then verify the limit algebraically.
