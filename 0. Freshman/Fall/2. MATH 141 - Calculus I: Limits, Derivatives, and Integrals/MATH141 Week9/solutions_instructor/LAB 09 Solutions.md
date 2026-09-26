# MATH 141 · Lab 09 Solutions (Instructor)
## Accumulation Functions and the FTC Numerically

All figures below were produced by running the lab: midpoint rule with $n=10^5$ unless stated.
*(Revised 2026-09-26 to match the 6-question version of the lab.)*

---

## Part 1: Building an Accumulation Function (9 pts)

**Q1 (3).** $\int_0^1 x^2dx$ at $n=1000$ gives $0.33333325$ (error $8.3\times10^{-8}$).

| $x$ | $F(x)$ |
|---|---|
| 0 | 0.0000000000 |
| 0.5 | 0.4612810064 |
| 1 | 0.7468241328 |
| 2 | 0.8820813908 |
| 3 | 0.8862073483 |
| 4 | 0.8862269118 |
| 5 | 0.8862269255 |

**Q2 (3).** The values settle at $0.8862269255$, and $\frac{\sqrt\pi}{2} = 0.8862269255$. They agree to all
ten decimals by $x = 5$.

**Q3 (3).**

| $x$ | central difference of $F$ | $e^{-x^2}$ |
|---|---|---|
| 0.5 | 0.7788007827 | 0.7788007831 |
| 1 | 0.3678794420 | 0.3678794412 |
| 2 | 0.0183156386 | 0.0183156389 |

They agree to about 9 decimal places. The last digit differs because of the midpoint rule's own small
error, magnified by dividing by $2h$.

---

## Part 2: Shape From the Derivative Alone (4 pts)

**Q4 (4).** $F' = e^{-x^2} > 0$ everywhere, so $F$ is **increasing** everywhere. $F'' = -2xe^{-x^2}$ is positive for
$x < 0$ and negative for $x > 0$: **concave up** on $(-\infty, 0)$, **concave down** on $(0, \infty)$, with an
**inflection point at $0$**, where $F$ is steepest. The table rises ever more slowly for $x > 0$, as predicted.

*Expected sentence:* a function needs no formula to be fully understood — FTC 1 hands us its derivative,
and the derivative tells us its shape.

---

## Part 3: Displacement Versus Distance (4 pts)

**Q5 (4).** $\int_0^4 v\,dt = 5.3333333333 = \tfrac{16}{3}$ m is the **displacement**.
$\int_0^4 |v|\,dt = 16.0000000000$ m is the **distance**. $v = 0$ at $t = 2$.
$\int_0^2 v\,dt = -5.3333 = -\tfrac{16}{3}$ and $\int_2^4 v\,dt = 10.6667 = \tfrac{32}{3}$.

- Displacement is the plain sum: $-\tfrac{16}{3} + \tfrac{32}{3} = \tfrac{16}{3}$.
- Distance adds the sizes: $\tfrac{16}{3} + \tfrac{32}{3} = 16$.

The particle moves backwards on $[0, 2)$, and that stretch subtracts from displacement but adds to distance.

---

## Part 4: The Chain Rule Form (3 pts)

**Q6 (3).** The central difference gives $G'(1.3) \approx 1.5264599153$, and the formula gives $1.5264599173$.
They agree to 8 decimal places. With $F$ an antiderivative of $\sin$, $G(x) = F(x^3) - F(x^2)$, so by FTC 1
and the chain rule $G'(x) = \sin(x^3)\cdot 3x^2 - \sin(x^2)\cdot 2x$. The upper limit gives the first term,
and the lower limit gives the second, with a minus sign.

---

## Common Submission Problems

| Symptom | Cause | Action |
|---|---|---|
| Q5 distance reported as $\tfrac{32}{3}$ | Stopped after the second piece | −2 |
| Q6 missing the $-2x\sin(x^2)$ term | Forgot the lower limit depends on $x$ | −1 |
| Q3 "agrees exactly" | Didn't look at the last digits | −1; the point is *how well* they agree |

---

*MATH 141 · Week 9 · Lab 09 Solutions · Instructor copy — do not distribute*
