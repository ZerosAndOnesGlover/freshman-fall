# MATH 141 · Calculus I
## Lab 08
### Riemann Sums, Convergence, and Sample-Point Independence

**Date:** Friday 20 November 2026 · 15:00–16:50 · Lab Section (Week 8) — covers Week 8 (Lectures 01–03)  
**Duration:** 2 hours | **Tools:** Python using CS 101 Weeks 0–3 (`def`, `for`, `range`, `if`/`elif`, `math`),
plus one call from the `random` module explained below
**Expected time:** the session itself (6 questions), plus at most 30 minutes to tidy your answers
**Submission:** Written report due Monday 23 November 2026, 17:00 (Week 9)
**Total: 100 points**

> **No antiderivatives in this lab.** The Fundamental Theorem arrives in Week 9. Every exact value
> here comes from a Riemann-sum limit or from geometry, because the point of this lab is to see what
> the definite integral *is* before you learn the shortcut for computing it.

> *Revised 2026-09-26:* cut from four parts and 25 questions to 6 questions. The hand derivations of $L_n$
> and $M_n$, the bounding part (Problem Set 8, Problem 5 does it) and the adaptive-integrator pseudocode
> were removed. The Desmos rectangle sketch is now a hand sketch: Desmos has no simple way to draw
> Riemann rectangles.

---

## Lab Objectives

1. See Riemann sums converge, and measure how fast
2. Establish experimentally that the limit does not depend on the sample points
3. Use a numerical integrator on a function with no elementary antiderivative

---

## Part 1 — Watching Riemann Sums Converge (30 min)

For $f(x) = x^2$ on $[0,1]$, whose exact area is $\tfrac13$ (Monday's lecture), the right-endpoint sum is
$R_n = \dfrac{(n+1)(2n+1)}{6n^2}$.

### Question 1 (15 points)

Sketch $y = x^2$ on $[0, 1]$ by hand, with the four right-endpoint rectangles for $n = 4$. Does $R_4$
overestimate or underestimate the area? Justify it from the fact that $f$ is increasing.

### Question 2 (15 points)

Use a `for` loop over `[4, 10, 100, 1000]` to print $n$, $R_n$ and the error $R_n - \tfrac13$. When $n$ is
multiplied by 10, by what factor does the error fall? Compare it with the forward and central differences
of Lab 03: which one does $R_n$ resemble?

---

## Part 2 — Sample-Point Independence (45 min)

The definition of $\int_a^b f$ allows the sample point $x_i^*$ to be **anywhere** in its subinterval. This
part tests that claim.

**One new call.** `random.uniform(lo, hi)` returns a random number between `lo` and `hi`. Put
`import random` at the top of the file. (CS 101 Lecture 17 used `random.randint` the same way to build test
data.)

### Question 3 (15 points)

Complete this function. `rule` is one of `"left"`, `"right"`, `"mid"` or `"random"`.

```python
def riemann(f, a, b, n, rule):
    dx = (b - a) / n
    total = 0.0
    for i in range(n):
        left = a + i * dx
        if rule == "left":
            x = left
        elif rule == "right":
            x = ____________
        elif rule == "mid":
            x = ____________
        else:
            x = random.uniform(left, left + dx)
        total = total + f(x) * dx
    return total
```

Check it: `riemann(f, 0, 1, 1000, "right")` must equal your $R_{1000}$ from Question 2.

### Question 4 (15 points)

For $f(x)=x^2$ on $[0,1]$, tabulate all four rules at $n = 10$, $100$ and $10{,}000$. Run the random rule
twice at each $n$. Which fixed rule is most accurate? How far apart are the four rules at $n = 10$, and at
$n = 10{,}000$?

### Question 5 (15 points)

The random rule gives a different answer each run. Does it still converge? Explain what your table shows
about the **definition** of the definite integral, and why the definition would be broken if the four
rules had different limits.

---

## Part 3 — An Integral You Cannot Do by Hand (25 min)

### Question 6 (25 points)

$e^{-x^2}$ has no elementary antiderivative, so even the Week 9 techniques cannot give $\int_{-2}^{2} e^{-x^2}dx$
exactly. Its value is $1.764162781524843$ to 16 digits. Use `riemann` with the midpoint rule
(`math.exp(-x**2)`) at $n = 10$, $100$ and $1000$, and tabulate the errors. How does the error shrink as $n$
grows by 10? What does this say about which problems belong to exact methods and which to numerical ones?

---

## Lab Report Requirements

1. The Question 1 sketch and the tables from Questions 2, 4 and 6
2. Your `riemann` implementation and its output
3. Answers to Questions 1–6

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — Riemann sum convergence | 30 |
| Part 2 — Sample-point independence | 45 |
| Part 3 — A numerical integral | 25 |
| **Total** | **100** |

---

*MATH 141 · Week 8 · Lab 08 · © CSE Department*
