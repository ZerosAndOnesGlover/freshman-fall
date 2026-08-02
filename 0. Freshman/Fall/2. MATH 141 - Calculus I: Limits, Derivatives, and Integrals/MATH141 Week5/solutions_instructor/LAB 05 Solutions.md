# MATH 141 — Week 5
## LAB 05 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed, not estimated.** Students working in Desmos rather
> than Python will see the same behaviour but fewer digits — grade the *reasoning and the observed
> trend*, not agreement to the last decimal place.

---

## Part 1 — Implicit Curves

**1.1 Circle** x² + y² = 25. Implicit differentiation: 2x + 2y·y′ = 0 ⇒ **y′ = −x/y**.

The slope is undefined where y = 0 — at (±5, 0), where the tangent is vertical. That is the
geometric payoff: an implicit curve can have vertical tangents, which no function y = f(x) can.
The circle is not a function, and implicit differentiation is precisely the tool for that case.

**1.2 Folium of Descartes** x³ + y³ = 3axy. Differentiating: 3x² + 3y²y′ = 3a(y + xy′), so

$$y' = \frac{ay - x^2}{y^2 - ax}$$

**1.3 Lemniscate** (x²+y²)² = a²(x²−y²). Same method; the algebra is heavier and the point is that
the *method* is unchanged no matter how unpleasant the curve.

**The universal error to grade for:** dropping the dy/dx factor. Every y is a function of x, so
d/dx(y³) = 3y²·(dy/dx). A student who writes 3y² has not done implicit differentiation at all.

---

## Part 2 — The Logarithm

**2.1** (ln x)′ = 1/x. Numerically, the central difference at x = 2 gives 0.5000000000 against the
exact 0.5. Geometrically: ln x is defined as the area under 1/t from 1 to x, so its rate of change
*is* the height of that curve — the FTC, previewed.

**2.2** e via the derivative: (1 + 1/n)ⁿ →

| n | (1 + 1/n)ⁿ |
|---|---|
| 10 | 2.59374246 |
| 1,000 | 2.71692393 |
| 10⁶ | 2.71828047 |

converging to e = 2.718281828…. Convergence is **slow** — O(1/n) — so a million terms buys only six
correct digits. Worth noting: this is a bad way to compute e, and the series Σ1/k! converges far
faster.

---

## Part 3 — Related Rates

**3.1 Sliding ladder.** L = 10 ft, base moving out at dx/dt = 2 ft/s. From x² + y² = 100,
differentiating with respect to t gives 2x·x′ + 2y·y′ = 0, so **dy/dt = −x·x′/y**.

| x (ft) | y (ft) | dy/dt (ft/s) |
|---|---|---|
| 6 | 8.0000 | −1.5000 |
| 8 | 6.0000 | −2.6667 |
| 9.9 | 1.4107 | **−14.0358** |

**dy/dt → −∞ as x → 10.** The top of the ladder accelerates without bound as the base nears the
wall's distance. This is physically impossible — a real ladder's top cannot exceed the speed the
model implies — and the reason is that the *constraint* "the base moves at constant 2 ft/s" becomes
unsustainable. Students who notice the model breaks down have understood more than those who just
report the number.

**The procedural error to grade for:** substituting x = 6 *before* differentiating. Any quantity
that varies must stay symbolic until after d/dt is applied; substituting early turns a variable into
a constant and forces its rate to zero.

**3.2 Expanding balloon.** V = (4/3)πr³ ⇒ dV/dt = 4πr²·dr/dt. Note dr/dt = (dV/dt)/(4πr²)
**decreases** as r grows, at constant inflation rate — the surface area is spreading the same volume
over more of it.

---

## Part 4 — Inverse Trig Derivatives

(arctan x)′ = 1/(1+x²). Central-difference verification with h = 10⁻⁶:

| x | Numerical | Exact |
|---|---|---|
| 0.5 | 0.8000000000 | 0.8000000000 |
| 1.0 | 0.5000000000 | 0.5000000000 |
| 2.0 | 0.2000000000 | 0.2000000000 |

Agreement to 10 digits. Contrast with (arcsin x)′ = 1/√(1−x²), whose **domain restriction |x| < 1**
matters — attempting the numerical derivative at x = 1 fails, and it should, because the tangent is
vertical there.

---

## Marking Scheme

- **Method (≈60%).** Correct technique named, hypotheses checked where a theorem requires them,
  symbolic setup before numerical evaluation, and a stated reason for each observed behaviour.
- **Execution (≈40%).** Correct arithmetic, sensible precision, correct plot or table, and a
  conclusion that actually follows from the data.

**Carry-through.** Penalise a wrong value once; award downstream marks if the student reasons
correctly from their own error.

**The specific failure to watch for in a computational lab:** reporting *what* the computer printed
without explaining *why*. "The table approaches 0.5" is an observation; "the table approaches 0.5
because the conjugate cancels the removable factor" is the answer. A lab report that is a
transcript earns the execution marks only.

---

*MATH 141 · Week 5 · Lab Solutions · Instructor Copy · © CSE Department*
