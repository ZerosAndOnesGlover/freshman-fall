# MATH 141 · Week 5
## LAB 05 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed in Python, not estimated.** Grade the *reasoning and the
> observed trend*, not agreement to the last decimal place.

*(Revised 2026-09-26 to match the 7-question version of the lab.)*

---

## Part 1 — Implicit Curves

**Q1 (10).** At $(3, 4)$: $dy/dx = -3/4$. The line touches the circle at $(3, 4)$ without crossing it.
$dy/dx$ is undefined where $y = 0$, at $(\pm 5, 0)$: the tangent there is **vertical**.

**Q2 (10).** $27 + 27 = 54 = 6 \cdot 3 \cdot 3$ ✓. Slope $= \dfrac{6 - 9}{9 - 6} = -1$, tangent $y = -x + 6$.
$(3, 3)$ is the tip of the loop, on the line $y = x$, and the tangent there is perpendicular to that line.

**Q3 (10).** $y = x^2/2$ in the curve: $x^3 + \dfrac{x^6}{8} = 3x^3$, so $x^6 = 16x^3$. Then $x = 0$ or
$x^3 = 16$. At $x = 16^{1/3} \approx 2.520$, $y = x^2/2 \approx 3.175$: the top of the loop.

$x = 0$ gives the origin, but there the formula is $\frac{0}{0}$. The curve crosses itself at the origin, so
it has no single tangent there. Accept an answer that notes this; don't require it.

---

## Part 2 — Two Derivative Formulas

**Q4 (15).** `central(math.log, 2)` $= 0.50000004$ against $1/2$. `central(math.log, 0.5)` $= 2.0000027$ against
$2$. $\ln x$ is steep near $0$ and flattens as $x$ grows, exactly as $1/x$ is large near $0$ and small for
large $x$. It is always increasing, since $1/x > 0$ on its domain.

**Q5 (15).**

| a | 1/(1+a²) | central |
|---|---|---|
| 0 | 1.0 | 0.99999967 |
| 1 | 0.5 | 0.50000008 |
| 5 | 0.03846154 | 0.03846154 |

$\arctan$ is steepest at $x = 0$ and flattens toward its asymptotes $\pm\pi/2$. That matches
$\frac{1}{1+x^2}$, whose maximum is $1$ at $x = 0$ and which tends to $0$ as $|x| \to \infty$.

---

## Part 3 — Related Rates Simulation

**Q6 (25).** The blank is `-x / y * 2`.

| t | x | y | numerical | exact |
|---|---|---|---|---|
| 0 | 0 | 10.000000 | 0.000000 | 0.000000 |
| 1 | 2 | 9.797959 | −0.408249 | −0.408248 |
| 2 | 4 | 9.165151 | −0.872874 | −0.872872 |
| 3 | 6 | 8.000000 | −1.500007 | −1.500000 |
| 4 | 8 | 6.000000 | −2.666708 | −2.666667 |
| 4.5 | 9 | 4.358899 | −4.129712 | −4.129483 |

They agree to 4–5 decimal places; the gap grows near the end, where $y$ changes fastest.

**Q7 (15).** $dy/dt = -2x/y \to -\infty$ as $y \to 0$. The formula says the top falls infinitely fast, which
no real ladder does. In reality the top leaves the wall before that, so the model, which assumes the top
stays on the wall, stops being valid near the end.

---

## Marking Scheme

- **Method (≈60%).** Derivatives found by hand before any numerical check, and a stated reason for each
  observation.
- **Execution (≈40%).** Correct values, and conclusions that follow from them.

---

*MATH 141 · Week 5 · Lab Solutions · Instructor Copy · © CSE Department*
