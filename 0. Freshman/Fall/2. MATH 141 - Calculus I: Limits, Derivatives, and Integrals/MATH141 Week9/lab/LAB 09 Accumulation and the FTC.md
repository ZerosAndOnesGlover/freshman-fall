# MATH 141 · Lab 09
## Accumulation Functions and the FTC Numerically

**Date:** Friday 27 November 2026 · 15:00–16:50 · Lab Section (Week 9) — covers Week 9 (Lectures 01–03)
**Duration:** 2 hours · **20 points**
**Tools:** Python using CS 101 Weeks 0–3 (`def`, `for`, `math`), and a Desmos table
**Expected time:** the session itself (6 questions), plus at most 30 minutes to tidy your answers

> *Revised 2026-09-21.* 1A used to ask for Simpson's rule, which no lecture or handout gives. It now reuses
> the Lab 08 midpoint rule, which reaches the same ten decimal places at $n=100\,000$.
>
> *Revised 2026-09-26.* Cut from 15 items and two plots to 6 questions. These questions used to be on
> Problem Set 9 as well; they are now only here. The plot of position against distance and the repeat of
> the chain-rule check at two more points were removed.

---

## The Tool

This is the midpoint rule from Lab 08, written as its own function:

```python
import math

def midpoint_rule(f, a, b, n):
    dx = (b - a) / n
    total = 0.0
    for i in range(n):
        total = total + f(a + (i + 0.5) * dx) * dx
    return total
```

Use $n = 100\,000$ everywhere below unless told otherwise. Each call takes well under a second.

---

## Part 1: Building an Accumulation Function (9 pts)

Let $F(x)=\displaystyle\int_0^x e^{-t^2}\,dt$. It has no elementary formula, but it is a perfectly good
function:

```python
def F(x):
    return midpoint_rule(lambda t: math.exp(-t**2), 0, x, 100000)
```

### Question 1 (3 points)

Check `midpoint_rule` on $\displaystyle\int_0^1 x^2\,dx=\tfrac13$ with $n=1000$. Then use a `for` loop to tabulate
$F(x)$ for $x=0, 0.5, 1, 2, 3, 4, 5$ to ten decimal places.

### Question 2 (3 points)

$F$ is increasing and bounded above. From your table, estimate $\lim_{x\to\infty}F(x)$ and compare it with
$\dfrac{\sqrt\pi}{2}$ (`math.sqrt(math.pi) / 2`).

### Question 3 (3 points)

Check FTC 1 numerically: compute $\dfrac{F(x+h)-F(x-h)}{2h}$ with $h=10^{-5}$ at $x=0.5, 1, 2$, and compare
each with $e^{-x^2}$. To how many digits do they agree?

---

## Part 2: Shape From the Derivative Alone (4 pts)

### Question 4 (4 points)

Using **only** $F'(x)=e^{-x^2}$ and $F''(x)=-2xe^{-x^2}$, predict where $F$ increases, where it is concave up
or down, and where it has an inflection point. Then, in Desmos, add a table (click **+**, then **table**)
with your Question 1 values and check the points follow your prediction. In one sentence: what have you
shown about a function with no elementary formula?

---

## Part 3: Displacement Versus Distance (4 pts)

### Question 5 (4 points)

A particle has $v(t)=t^2-4$ m/s on $[0,4]$. Compute $\displaystyle\int_0^4 v\,dt$ and
$\displaystyle\int_0^4 \lvert v\rvert\,dt$ numerically (`abs` is a Python built-in). Find where $v$ changes sign,
compute $\int_0^2 v\,dt$ and $\int_2^4 v\,dt$, and show how these two pieces give both of your answers.
Which is the displacement and which the distance?

---

## Part 4: The Chain Rule Form (3 pts)

### Question 6 (3 points)

Let $G(x)=\displaystyle\int_{x^2}^{x^3}\sin t\,dt$. Estimate $G'(1.3)$ by a central difference with $h = 10^{-5}$
(define `G(x)` with `midpoint_rule`, as for `F`). Compare it with $3x^2\sin(x^3)-2x\sin(x^2)$ at $x=1.3$, and
explain where each of the two terms comes from.

---

## Deliverables

Your code, all tables, the Desmos table from Question 4, and written answers to Questions 1–6.

## Grading

| Part | Points |
|---|---|
| 1 — integrator, table, limit, FTC 1 verified | 9 |
| 2 — shape predicted from the derivative, then confirmed | 4 |
| 3 — displacement and distance distinguished | 4 |
| 4 — chain-rule form verified | 3 |
| **Total** | **20** |

---

*MATH 141 · Week 9 · Lab 09 · © CSE Department*
