# MATH 141 · Week 3
## LAB 03 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed in Python, not estimated.** Grade the *reasoning and the
> observed trend*, not agreement to the last decimal place.

*(Revised 2026-09-26 to match the 9-question version of the lab.)*

---

## Part 1 — Secant Lines Converging to the Tangent

**Q1 (10).**

| h | slope |
|---|---|
| 1 | 5.0 |
| 0.1 | 4.100000000000001 |
| 0.01 | 4.009999999999891 |
| −0.01 | 3.9899999999999824 |

The slopes approach **4**. $\dfrac{(2+h)^2-4}{h} = \dfrac{4h + h^2}{h} = 4 + h \to 4$. The symbolic
cancellation and the numerical trend are the same fact.

**Q2 (10).** From both sides the secant line turns into the **tangent line** at $(2, 4)$, with slope 4:
$y = 4 + 4(x - 2)$, or $y = 4x - 4$.

---

## Part 2 — Reading the Derivative from a Graph

**Q3 (8).** Increasing for $x < -1$ and $x > 1$; decreasing on $(-1, 1)$; horizontal tangents at about
$x = \pm 1$.

**Q4 (12).** $\dfrac{(x+h)^3 - 3(x+h) - x^3 + 3x}{h} = 3x^2 + 3xh + h^2 - 3 \to 3x^2 - 3$. Then
$f'(x) = 0 \iff x = \pm 1$. The zeros of $f'$ are exactly the turning points of $f$, and $f' > 0$ exactly
where $f$ rises.

| On f | On f′ |
|---|---|
| increasing | f′ > 0 (above the axis) |
| decreasing | f′ < 0 |
| turning point | f′ **crosses** zero |

---

## Part 3 — Non-Differentiable Points

**Q5 (10).** $\frac{|h|}{h} = -1$ for $h < 0$ and $+1$ for $h > 0$. Both one-sided limits exist but
differ, so the two-sided limit does not exist and $|x|$ is **not differentiable at 0**. The secant line
flips between slopes $-1$ and $+1$ as $h$ crosses zero. This is a **corner**.

**Q6 (10).** $h^{-1/3} \to +\infty$ as $h \to 0^+$ and $\to -\infty$ as $h \to 0^-$. The graph has a sharp
point with a vertical tangent, a **cusp**, so $x^{2/3}$ is **not differentiable at 0**.

**Q7 (10).** Continuous: $\lim_{x\to1^-} x^2 = 1$, $\lim_{x\to1^+}(2x-1) = 1$, and $f(1) = 1$.

Left: $\dfrac{(1+h)^2 - 1}{h} = 2 + h \to 2$. Right: $\dfrac{2(1+h) - 1 - 1}{h} = 2$.

Both equal $2$, so $f$ **is differentiable at 1**, with $f'(1) = 2$. The line $y = 2x - 1$ is the tangent to
the parabola at $(1, 1)$, so the two pieces join smoothly with no corner.

*This is the "subtler case": students expecting every piecewise join to be a corner lose it. Full marks need
both one-sided limits computed, not just the pictures.*

---

## Part 4 — Numerical Differentiation and Its Limits

$f = \sqrt{x}$ at $a = 4$, exact $f'(4) = 0.25$.

| h | Forward | Error | Central | Error |
|---|---|---|---|---|
| 0.1 | 0.2484567313 | 1.543 × 10⁻³ | 0.2500195366 | 1.954 × 10⁻⁵ |
| 0.01 | 0.2498439450 | 1.561 × 10⁻⁴ | 0.2500001953 | 1.953 × 10⁻⁷ |
| 0.001 | 0.2499843770 | 1.562 × 10⁻⁵ | 0.2500000020 | 1.953 × 10⁻⁹ |

**Q8 (15).** The central difference is far more accurate: about 80 times at $h = 0.1$ and 8000 times at
$h = 0.001$. Dividing $h$ by 10 divides the forward error by **10** and the central error by **100**. The
forward error is proportional to $h$ and the central error to $h^2$.

**Q9 (15).** At $h = 10^{-15}$ the forward difference gives **0.0** and the central gives **0.111**, both
badly wrong. `math.sqrt(4 + 1e-15)` rounds to exactly `2.0`, so the numerator is a difference of nearly
equal numbers — catastrophic cancellation, as in Lab 01 — and dividing by the tiny $h$ magnifies the
round-off. So "make $h$ as small as possible" is wrong. Below some $h$, round-off grows faster than the
formula's own error shrinks, so there is a best $h$ in between.

---

## Marking Scheme

- **Method (≈60%).** Derivatives from the definition where asked, and a stated reason for each observed
  behaviour.
- **Execution (≈40%).** Correct values, sensible precision, and a conclusion that follows from the data.

**Carry-through.** Penalise a wrong value once; award downstream marks if the student reasons
correctly from their own error.

**The failure to watch for:** reporting *what* the computer printed without explaining *why*. A report
that is a transcript earns the execution marks only.

---

*MATH 141 · Week 3 · Lab Solutions · Instructor Copy · © CSE Department*
