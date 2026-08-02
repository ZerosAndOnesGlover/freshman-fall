# PHYS 141 · Week 7
## LAB 7 Solutions — INSTRUCTOR ONLY

> **Representative data.** The numbers below are one realistic dataset, generated and checked
> numerically. Student apparatus will differ — **grade the method, not agreement with these
> figures.** Every derived quantity here is reproducible from the raw data in the same section,
> so you can re-run a student's arithmetic against their own readings.

---

## Part 1 — Rotating Platform (the skater)

Student on a rotating platform, arms out then pulled in. Moments of inertia determined from the
platform calibration.

| State | I (kg·m²) | ω (rad/s) | L = Iω (kg·m²/s) | K = ½Iω² (J) |
|---|---|---|---|---|
| Arms out | 0.0400 | 2.100 | 0.08400 | 0.08820 |
| Arms in (theory) | 0.0180 | 4.667 | 0.08400 | 0.19600 |
| Arms in (measured) | 0.0180 | 4.550 | 0.08190 | 0.18632 |


**Prediction.** No external torque about the vertical axis, so L is conserved:

$$\omega_2 = \frac{I_1\omega_1}{I_2} = \frac{(0.04)(2.1)}{0.018} = 4.667\ \text{rad/s}$$

- **Angular momentum:** 0.08190 vs 0.08400 → **-2.50%**.
  Conserved within error. ✓ The small deficit is bearing friction acting over the pull-in time.
- **Kinetic energy:** 0.18632 J vs 0.08820 J → **increased by a factor of 2.11**
  (theory: I₁/I₂ = 2.22).

### The key question: where did the extra energy come from?

**The student's arms did work.** Pulling the masses inward requires a force directed inward against
the outward-pointing centripetal requirement, applied over a radial displacement — so W > 0, and
that work appears as rotational kinetic energy.

The theoretical ratio is exact and worth deriving:

$$\frac{K_2}{K_1} = \frac{\tfrac{1}{2}I_2\omega_2^2}{\tfrac{1}{2}I_1\omega_1^2} = \frac{I_1}{I_2}$$

using ω₂ = I₁ω₁/I₂. So kinetic energy rises by exactly the factor by which I falls.

> **This is the conceptual crux of the lab.** A conservation law for one quantity says nothing
> about another. L is conserved because no external torque acts; K is *not* conserved because an
> internal force did work. Students who report "energy was created, so something is wrong" have the
> physics backwards — mark the explanation, not the surprise. Equally, penalise any report claiming
> both L and K were conserved, since the data plainly shows K roughly doubling.

---

## Part 2 — Rotational Collision (ring dropped onto a spinning disk)

| State | I (kg·m²) | ω (rad/s) | L (kg·m²/s) | K (J) |
|---|---|---|---|---|
| Before | 0.0225 | 5.600 | 0.12600 | 0.3528 |
| After (theory) | 0.0405 | 3.111 | 0.12600 | 0.1960 |
| After (measured) | 0.0405 | 3.060 | 0.12393 | 0.1896 |


$$\omega_f = \frac{I_d\omega_i}{I_d+I_r} = \frac{(0.0225)(5.6)}{0.0405} = 3.111\ \text{rad/s}$$

- **Angular momentum:** **-1.64%** ✓
- **Kinetic energy:** **53.7% retained**, theory
  I_d/(I_d + I_r) = 55.6%.

**This is the rotational analogue of a perfectly inelastic collision**, and the retention formula
has exactly the parallel form:

$$\frac{K_f}{K_i} = \frac{I_d}{I_d+I_r} \qquad \text{compare} \qquad \frac{K_f}{K_i} = \frac{m_1}{m_1+m_2}$$

from Lab 5. Energy is lost to **kinetic friction between ring and disk** during the brief period
when their surfaces slip against each other. Once they rotate together, slipping ceases and no
further loss occurs. Students should be able to state that the loss here is *required* by angular
momentum conservation, exactly as in the linear case — it is not an experimental defect.

Contrast Part 1 (K increases, work done by internal forces) with Part 2 (K decreases, energy
dissipated by internal friction). **Same conserved quantity, opposite energy behaviour**, decided
entirely by the nature of the internal interaction.

---

## Part 3 — Written Discussion (expected answers)

**Why is angular momentum conserved here?** No net external **torque** acts about the rotation
axis. Gravity and the normal force act vertically, parallel to the axis, and contribute no torque
about it. Bearing friction supplies a small opposing torque, which is precisely what the
2.5–1.6% deficits
measure.

**Does the axis choice matter?** Yes — profoundly. Angular momentum is defined about a *point or
axis*, and a system can conserve L about one axis and not another. All statements in this lab are
about the fixed vertical rotation axis. Students who omit the axis have written an incomplete
statement.

**Largest error sources.** (1) Determining I for a human body with arms out — this is the dominant
uncertainty in Part 1 and is genuinely hard, which is why Part 2 with machined objects gives
tighter agreement. (2) Bearing friction over the measurement interval. (3) Non-instantaneous
transitions: if the ring is dropped off-centre or lowered slowly, it applies a lateral torque and
the model breaks. (4) Measuring ω by stopwatch over few rotations.

**Improvement.** Drop the ring from as small a height as possible and as close to concentric as
possible; measure ω immediately before and after rather than averaging over many rotations, so
friction has less time to act; and extrapolate ω(t) back to the collision instant from a decay
curve — the most sophisticated answer available, and worth bonus marks.

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

*PHYS 141 · Week 7 · Lab Solutions · Instructor Copy · © CSE Department*
