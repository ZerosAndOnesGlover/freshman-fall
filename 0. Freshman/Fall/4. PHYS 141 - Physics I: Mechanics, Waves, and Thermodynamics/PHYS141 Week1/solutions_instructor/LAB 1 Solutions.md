# PHYS 141 · Week 1
## LAB 1 Solutions — INSTRUCTOR ONLY

> **Representative data.** The numbers below are one realistic dataset, generated and checked
> numerically. Student apparatus will differ — **grade the method, not agreement with these
> figures.** Every derived quantity here is reproducible from the raw data in the same section,
> so you can re-run a student's arithmetic against their own readings.

---

## Part 1 — Spark Timer (Δt = 1/60 s = 0.016667 s)

Positions read to the nearest 0.5 mm, as instructed. Mid-point velocities from
v_{n} ≈ (y_{n+1} − y_{n−1})/(2Δt).

| Dot | t (s) | t² (s²) | y (m) | v (m/s) |
|---|---|---|---|---|
| 0 | 0.00000 | 0.000000 | 0.0000 | — |
| 1 | 0.01667 | 0.000278 | 0.0015 | 0.1650 |
| 2 | 0.03333 | 0.001111 | 0.0055 | 0.3150 |
| 3 | 0.05000 | 0.002500 | 0.0120 | 0.4950 |
| 4 | 0.06667 | 0.004444 | 0.0220 | 0.6600 |
| 5 | 0.08333 | 0.006944 | 0.0340 | 0.8100 |
| 6 | 0.10000 | 0.010000 | 0.0490 | 0.9750 |
| 7 | 0.11667 | 0.013611 | 0.0665 | 1.1400 |
| 8 | 0.13333 | 0.017778 | 0.0870 | 1.3050 |
| 9 | 0.15000 | 0.022500 | 0.1100 | 1.4700 |
| 10 | 0.16667 | 0.027778 | 0.1360 | — |


### Method A — y vs. t², forced through the origin

Fitting y = m·t² with the intercept fixed at zero (justified: y = 0 at t = 0 *by definition* of
dot 0, so the origin is a datum, not a fitted point):

**m = 4.8933 ± 0.0030 m/s²  →  g = 2m = 9.787 ± 0.006 m/s²**

### Method B — v vs. t

Slope = **9.795 ± 0.048 m/s²**, intercept = -0.0012 ± 0.0045 m/s, R² = 0.99983.

**g_B = 9.79 ± 0.05 m/s²**

The intercept is v₀ and comes out **-0.0012 ± 0.0045 m/s** — consistent with zero, confirming
the ball was released from rest. That check is worth marks in its own right: a significantly
non-zero intercept means the release was not clean, and invalidates Method A (see Part 3 Q2).

### Comparison

| | g (m/s²) | σ | % discrepancy from 9.81 |
|---|---|---|---|
| Method A | 9.787 | 0.006 | 0.24% |
| Method B | 9.795 | 0.048 | 0.15% |

The two agree with each other. Both fall slightly **below** 9.81 — see Part 3.

> **Instructor note on the Method A uncertainty.** The formal fit error (0.006) is far smaller
> than Method B's, because a through-origin fit over a wide t² range is very stiff. This
> **understates the true uncertainty**, which is dominated by *systematic* effects (timer
> calibration, ruler zero) that a fit cannot see. A student who reports g = 9.787 ± 0.006
> and then declares 9.81 "excluded at 4σ" has made a real error of
> reasoning — reward those who notice that a σ this small is not credible for this apparatus.

---

## Part 2 — Photogate

With y₁ = 0.4 m and y₂ = 0.9 m, measured t₁ = 0.2859 s and t₂ = 0.4288 s:

$$g = \frac{2(y_2-y_1)}{t_2^2 - t_1^2} = \frac{2(0.9-0.4)}{0.18386 - 0.08172} = 9.790\ \text{m/s}^2$$

The derivation students must supply: from y = ½gt² at both gates, y₂ − y₁ = ½g(t₂² − t₁²). Note
this form **does not require knowing the drop point** — the unknown origin cancels — which is the
whole reason for using two gates rather than one.

---

## Part 3 — Systematic Error (expected answers)

**Q1 — Air resistance.** Drag opposes motion, reducing the downward acceleration below g. The
measured value is therefore **smaller** than 9.81. The effect grows with speed, so it also makes
the motion *non*-uniformly accelerated: the v–t plot curves slightly, bending away from the fit at
late times. Students who spot the curvature (rather than just asserting the sign) deserve extra
credit. For a dense ball over 0.15 m the effect is well under 0.1%.

**Q2 — Initial velocity v₀ > 0.** The true motion is y = v₀t + ½gt². Plotting y against t² and
forcing the line through the origin makes the fit absorb the extra v₀t into the slope. Since v₀t is
positive and grows more slowly than t², the fitted slope is pulled **up** at small t — the fit
**overestimates** g. The diagnostic is that y vs. t² is no longer straight: it curves, with a
positive apparent intercept if the intercept is left free. **Method B is immune** — a non-zero v₀
merely shifts the v–t intercept, leaving the slope correct. This is the strongest argument for
running both methods, and is the answer to look for.

**Q3 — Timer at 59.8 Hz instead of 60.0 Hz.** The true interval is longer than assumed
(1/59.8 > 1/60). Using the labelled value makes every t too small, and since g ∝ 1/t², g scales by
(59.8/60)² = 0.99334. The measured g would read
**low by 0.67%** — i.e. 9.745 m/s² in place of 9.81.

This is a **systematic** error: it shifts every trial the same way and **cannot be reduced by
repeating the experiment**. It is also the single most likely explanation for the low bias seen in
Part 1, and a student who connects Q3 to their own result has done the analysis properly.

---

## Part 4 — Ranking the Error Sources

Expected ranking for this apparatus, largest first:

1. **Spark timer calibration** — systematic, ~0.5%, invisible to repetition, and undetectable
   without an independent frequency check.
2. **Position measurement (±0.5 mm)** — random, and worst at *small* y where 0.5 mm is a large
   fraction of the reading. This is why the early dots should carry less weight.
3. **Tape friction through the timer** — systematic, retards the fall, biases g **low**. Together
   with (1) this explains the sign of the observed discrepancy.

Air resistance is negligible over this distance and a student who ranks it first has not thought
quantitatively.

---

## Marking Scheme

Point values follow the rubric printed on the lab handout. Within each section:

- **Method (≈60%).** Correct procedure, a stated sign/coordinate convention, symbolic setup before
  numbers, uncertainties propagated by the right rule, and units carried throughout.
- **Result (≈40%).** Correct arithmetic, sensible significant figures, and a stated comparison
  against theory (percent discrepancy *and* a σ-based consistency statement).

**Carry-through.** Penalise a wrong value once. If the student reasons correctly from their own
earlier error, award the downstream marks in full.

**A result that disagrees with theory is not automatically wrong.** Full marks are available for a
discrepant result that is correctly measured, correctly propagated, and honestly discussed. Award
*no* credit for a suspiciously perfect result with no uncertainty analysis — that is the more
common form of academic dishonesty in a lab course.

---

*PHYS 141 · Week 1 · Lab Solutions · Instructor Copy · © CSE Department*
