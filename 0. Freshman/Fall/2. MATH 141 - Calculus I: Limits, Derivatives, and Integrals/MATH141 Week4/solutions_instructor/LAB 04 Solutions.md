# MATH 141 · Lab 04 Solutions (Instructor)
## Rules, Chains, and Motion

All figures below were produced by running the computation. Students' values should match to the
digits shown. *(Revised 2026-09-26 to match the 6-question version of the lab.)*

---

## Part 1: Checking a Rule Numerically (3 pts)

**Q1.** $f'(x) = 2x\sin x + x^2\cos x$, so $f'(1) = 2\sin 1 + \cos 1 = 2.2232442755$.

| $h$ | central difference |
|---|---|
| $10^{-2}$ | $2.2232051534$ |
| $10^{-4}$ | $2.2232442716$ |
| $10^{-6}$ | $2.2232442755$ |

They agree to about 10 significant digits at $h = 10^{-6}$. *(1 for the derivative, 1 for the table, 1 for
the comparison.)*

---

## Part 2: The Chain Rule, Seen (7 pts)

**Q2 (3).** $g(1) = 2$. $\frac{dF}{du} = 5u^4 = 5 \cdot 16 = 80$ at $u = 2$, and $\frac{du}{dx} = 2x = 2$ at
$x = 1$. Product: $\mathbf{160}$. `central(1, 1e-6)` gives $160.0000000046$ ✓.

The rates multiply because a small change in $x$ changes $u$ about $2$ times as much, and each unit of
change in $u$ changes $F$ about $80$ times as much, so $F$ changes $160$ times as much as $x$.

**Q3 (4).** Layers, outside in: square root, $1 + \sin(\cdot)$, and $x^2$.
$$f'(x) = \frac{1}{2\sqrt{1+\sin(x^2)}}\cdot\cos(x^2)\cdot 2x = \frac{x\cos(x^2)}{\sqrt{1+\sin(x^2)}}$$
At $x = 1$: $0.3981570233$; `central(1, 1e-6)` gives $0.3981570232$ ✓.

*Marking: 1 for the layers, 2 for the derivative, 1 for the check.*

---

## Part 3: A Motion Analysis (10 pts)

**Q4 (3).** $v(t) = 3t^2 - 18t + 24 = \mathbf{3(t-2)(t-4)}$ and $a(t) = 6t - 18$.

| t | s | v | a |
|---|---|---|---|
| 0 | 0 | 24 | −18 |
| 1 | 16 | 9 | −12 |
| 2 | 20 | 0 | −6 |
| 3 | 18 | −3 | 0 |
| 4 | 16 | 0 | 6 |
| 5 | 20 | 9 | 12 |

**Q5 (4).** Where $v = 0$ ($t = 2$ and $t = 4$) the graph of $s$ has a horizontal tangent: a local maximum
at $t = 2$ and a local minimum at $t = 4$. Where $a = 0$ ($t = 3$) the graph of $v$ has its lowest point.

The particle speeds up where $v$ and $a$ have the **same sign**: on $(2, 3)$, where both are negative, and
on $(4, 5)$, where both are positive. It slows down on $(0, 2)$ and $(3, 4)$.

*Reject "speeding up because $a > 0$" without comparing signs. On $(3, 4)$, $a > 0$ but the particle is
slowing down.*

**Q6 (3).** Displacement $= s(5) - s(0) = \mathbf{20}$ m. The factors $(t-2)$ and $(t-4)$ are simple, so
$v$ **changes sign** at both roots and the particle reverses twice. Distance
$= |20 - 0| + |16 - 20| + |20 - 16| = \mathbf{28}$ m.

*Contrast PS 4 Problem 3, where the double root $(t-3)^2$ meant no reversal and distance = displacement.*

---

## Marking Scheme

- **Method (≈60%).** Rules named and applied by hand before any numerical check, and a stated reason for
  each graphical observation.
- **Execution (≈40%).** Correct values, and conclusions that follow from them.

---

*MATH 141 · Week 4 · Lab 04 Solutions · Instructor copy — do not distribute*
