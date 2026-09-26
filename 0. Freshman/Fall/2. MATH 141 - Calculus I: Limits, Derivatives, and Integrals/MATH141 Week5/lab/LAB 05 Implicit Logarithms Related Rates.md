# MATH 141 · Calculus I
## Lab 05
### Implicit Curves, Logarithmic Derivatives, and Related Rates Simulation

**Date:** Friday 30 October 2026 · 15:00–16:50 · Lab Section (Week 5) — covers Week 5 (Lectures 01–03)  
**Duration:** 2 hours | **Tools:** Desmos, and Python using only CS 101 Weeks 0–3: `def`, `for` over a
list, and `math` (`math.log`, `math.atan`, `math.sqrt`)
**Expected time:** the session itself (7 questions), plus at most 30 minutes to tidy your answers
**Submission:** Written report due Monday 2 November 2026, 17:00 (Week 6)

> *Revised 2026-09-21:* Exercise 1.3 (lemniscate) and Exercise 3.3 (design your own problem) removed to fit
> the two hours.
>
> *Revised 2026-09-26:* cut from four parts and about 26 questions, three long tables and a reflection to
> 7 questions. The folium question used the point $(2, 2)$, which is not on the curve; it now uses $(3, 3)$.
> The $a^x$ slider, the balloon and the $\ln\lvert x\rvert$ items were removed.

---

## Lab Objectives

1. Visualize implicitly defined curves and check implicit derivatives on them
2. Check $(\ln x)' = 1/x$ and $(\arctan x)' = 1/(1+x^2)$ numerically
3. Simulate a related rates problem and compare it with the exact rate

---

## Python for Today

The `central` function from Labs 03–04 does all the numerical checks. It can take the function as an
argument, since CS 101 Lecture 10 showed that functions are values:

```python
import math

def central(f, a, h=0.001):
    return (f(a + h) - f(a - h)) / (2 * h)

print(central(math.log, 2))
```

---

## Part 1 — Implicit Curves in Desmos (35 min)

Desmos plots implicit curves directly: type the equation as it is, e.g. `x^2 + y^2 = 25`.

### Question 1 (10 points)

Graph $x^2 + y^2 = 25$. Implicit differentiation gives $\dfrac{dy}{dx} = -\dfrac{x}{y}$. Compute the slope at
$(3, 4)$, add the tangent line $y - 4 = -\frac{3}{4}(x-3)$, and confirm it touches the circle there. At which
points of the circle is $dy/dx$ undefined, and why?

### Question 2 (10 points)

Graph the folium of Descartes, $x^3 + y^3 = 6xy$. Check that $(3, 3)$ lies on it. Implicit differentiation
gives $\dfrac{dy}{dx} = \dfrac{2y - x^2}{y^2 - 2x}$. Compute the slope at $(3, 3)$ and add the tangent line.

### Question 3 (10 points)

Where does the folium have a horizontal tangent? Estimate the point from the graph (click the curve at the
top of its loop). Then find it exactly: set $2y - x^2 = 0$, substitute $y = x^2/2$ into the curve, and
solve.

---

## Part 2 — Two Derivative Formulas, Checked (30 min)

### Question 4 (15 points)

Use `central(math.log, a)` at $a = 2$ and $a = 0.5$, and compare with $1/a$. Graph $y = \ln x$ in Desmos:
where is it steep, and where is it nearly flat? How does $1/x$ explain that?

### Question 5 (15 points)

Use a `for` loop over `[0, 1, 5]` to print $a$, $\dfrac{1}{1+a^2}$ and `central(math.atan, a)`. Do they agree?
Graph $y = \arctan x$: where is it steepest, and why does $\dfrac{1}{1+x^2}$ predict that?

---

## Part 3 — Related Rates Simulation (40 min)

A 10 m ladder starts upright against a wall. Its foot slides away at 2 m/s, so the foot is at
$x(t) = 2t$ and the top at $y(t) = \sqrt{100 - x(t)^2}$.

### Question 6 (25 points)

Complete this program and run it. It prints, for each time, the numerical $dy/dt$ and the exact rate from
related rates, $\dfrac{dy}{dt} = -\dfrac{x}{y}\cdot\dfrac{dx}{dt}$.

```python
def y_of(t):
    x = 2 * t
    return math.sqrt(100 - x**2)

for t in [0, 1, 2, 3, 4, 4.5]:
    x = 2 * t
    y = y_of(t)
    numerical = (y_of(t + 0.01) - y_of(t - 0.01)) / 0.02
    exact = ______________          # fill in from the related-rates formula
    print(t, x, y, numerical, exact)
```

Record the table. Do the two columns agree?

### Question 7 (15 points)

What happens to $dy/dt$ as the foot approaches $x = 10$ (the ladder almost flat)? Could a real ladder top
do that? What does it tell you about where the model stops describing reality?

---

## Lab Report Requirements

Include your programs and their output, one Desmos screenshot or link for each of Questions 1–3, and
answers to Questions 1–7.

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — Implicit curves | 30 |
| Part 2 — Logarithm and arctangent derivatives | 30 |
| Part 3 — Related rates simulation | 40 |
| **Total** | **100** |
