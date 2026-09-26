# MATH 141 · Calculus I
## Lab 03

**Date:** Friday 16 October 2026 · 15:00–16:50 · Lab Section (Week 3) — covers Week 3 (Lectures 01–03).
Everything is done from the definition of the derivative; the rules arrive in Week 4.
*(Revised 2026-09-21: the f'' / concavity question — Week 7 — and the product-rule check — Week 4 — were removed.)*
### The Derivative: Numerical Exploration and Graphical Interpretation

**Duration:** 2 hours | **Tools:** Desmos, and Python using only CS 101 Weeks 0–3: `def` and `return`
(CS 101 Lecture 10), `for` over a list, and the `math` module
**Expected time:** the session itself (9 questions), plus at most 30 minutes to tidy your answers
**Submission:** Written report due Monday 19 October 2026, 17:00 (Week 4)

---

## Lab Objectives

1. Experience the derivative as a limit of slopes of secant lines
2. Read a derivative's sign from a graph
3. Recognise what failure of differentiability looks like
4. Compare forward and central difference quotients, and see where round-off takes over

---

## Python for Today

This week CS 101 introduced functions. A difference quotient is a natural one:

```python
def f(x):
    return x**2

def forward(a, h):
    return (f(a + h) - f(a)) / h

for h in [1, 0.1, 0.01, -0.01]:
    print(h, forward(2, h))
```

Save it as `lab03.py` and run `python3 lab03.py`. To study another function, change only the body of `f`.

---

## Part 1 — Secant Lines Converging to the Tangent (20 min)

### Question 1 (10 points)

Run the program above for $f(x) = x^2$ at $a = 2$ and record the table. What value do the slopes
approach? Confirm it from the definition: simplify $\dfrac{(2+h)^2 - 4}{h}$ and let $h \to 0$.

### Question 2 (10 points)

In Desmos, graph $f(x) = x^2$, a slider $h$ from $-2$ to $2$, and the secant line
`y = f(2) + (f(2 + h) - f(2))/h * (x - 2)`. Drag $h$ toward $0$ from both sides. What does the secant
line become, and what is the equation of that line?

---

## Part 2 — Reading the Derivative from a Graph (25 min)

In Desmos, graph $f(x) = x^3 - 3x$.

### Question 3 (8 points)

Without computing, read off the approximate $x$-values where $f$ is increasing ($f' > 0$), decreasing
($f' < 0$), and has a horizontal tangent ($f' = 0$).

### Question 4 (12 points)

Compute $f'(x)$ **from the definition** (expand $(x+h)^3$) and solve $f'(x)=0$ exactly. Graph $f'$ in
Desmos alongside $f$. Do the zeros of $f'$ line up with the turning points of $f$, and does the sign of
$f'$ match your answers to Question 3?

---

## Part 3 — Non-Differentiable Points (30 min)

### Question 5 (10 points)

**A corner.** For $f(x) = |x|$, compute the one-sided limits of the difference quotient at $0$:
$\displaystyle\lim_{h\to0^-}\frac{|h|}{h}$ and $\displaystyle\lim_{h\to0^+}\frac{|h|}{h}$. What do they tell
you about differentiability at $0$? Check with the secant slider from Question 2, using `f(x) = abs(x)`
and the point $0$ instead of $2$.

### Question 6 (10 points)

**A cusp.** For $f(x) = x^{2/3}$, the difference quotient at $0$ is $\dfrac{h^{2/3}}{h} = h^{-1/3}$. What
happens to it as $h \to 0^+$ and as $h \to 0^-$? Graph $f$ in Desmos and describe what you see at $0$.

### Question 7 (10 points)

**A join.** Let $f(x) = x^2$ for $x \le 1$ and $f(x) = 2x - 1$ for $x > 1$. Is $f$ continuous at $1$?
Compute the left and right limits of $\dfrac{f(1+h)-f(1)}{h}$. Is $f$ differentiable at $1$? Graph it and
describe what happens at $x = 1$.

---

## Part 4 — Numerical Differentiation and Its Limits (30 min)

The **forward difference** is $\dfrac{f(a+h)-f(a)}{h}$ and the **central difference** is
$\dfrac{f(a+h)-f(a-h)}{2h}$. Add a `central(a, h)` function to your program, and change `f` to
`math.sqrt(x)` (put `import math` at the top).

At $a = 4$ the exact derivative is $\dfrac{1}{2\sqrt{4}} = 0.25$ (Problem Set 0, Problem 5 found
$\dfrac{1}{2\sqrt{x}}$).

| $h$ | Forward | Error | Central | Error |
|-----|---------|-------|---------|-------|
| $0.1$ | | | | |
| $0.01$ | | | | |
| $0.001$ | | | | |

Compute each error as `abs(forward(4, h) - 0.25)`.

### Question 8 (15 points)

Which formula is more accurate for the same $h$? Each time $h$ shrinks by a factor of 10, by what factor
does each error shrink?

### Question 9 (15 points)

Now try $h = 10^{-15}$ (`1e-15`). What do the two formulas give? Explain what went wrong, using the
catastrophic cancellation you met in Lab 01. Is "make $h$ as small as possible" good advice?

---

## Lab Report Requirements

Include:
1. Your program, and the two tables
2. Answers to Questions 1–9
3. Desmos screenshots or links for Questions 2 and 4

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — Secant convergence | 20 |
| Part 2 — Reading derivatives from graphs | 20 |
| Part 3 — Non-differentiable points | 30 |
| Part 4 — Numerical differentiation | 30 |
| **Total** | **100** |

---

*Revised 2026-09-26: cut from five parts and about 25 questions, with five long tables and a
reflection, to 9 questions and two short tables, so it fits the session. The Python is Week 3 CS 101
(`def`). Removed: the tangent-slope table and hand-plotted $f'$, the hand-sketched derivative, and
Part 5 on $e^x$. The numerical part now uses $\sqrt{x}$ instead of $\sin x$, whose derivative is not
taught until Week 4.*
