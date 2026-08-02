# PHYS 141 — Week 0
## LAB 0 Solutions — INSTRUCTOR ONLY

> **Representative data.** The numbers below are one realistic dataset, generated and checked
> numerically. Student apparatus will differ — **grade the method, not agreement with these
> figures.** Every derived quantity here is reproducible from the raw data in the same section,
> so you can re-run a student's arithmetic against their own readings.

---

## Station A — Ruler vs. Calipers

| Trial | Ruler (cm) | Calipers (cm) |
|---|---|---|
| 1 | 24.5 | 24.62 |
| 2 | 24.0 | 24.59 |
| 3 | 24.5 | 24.63 |
| 4 | 25.0 | 24.60 |
| 5 | 24.5 | 24.61 |

| | **Ruler** | **Calipers** |
|---|---|---|
| Mean x̄ | 24.500 cm | 24.610 cm |
| Std dev σ | 0.3536 cm | 0.0158 cm |
| Std error σ/√N | **0.1581 cm** | **0.0071 cm** |

**Reported:** ruler **24.50 ± 0.16 cm**, calipers **24.610 ± 0.007 cm**.

**Do they agree?** Difference = 0.110 cm. Combined uncertainty =
√(0.1581² + 0.0071²) = 0.1583 cm. The discrepancy is **0.70σ**, so
**yes — they agree within uncertainty.**

**What it shows about accuracy vs. precision.** The calipers are ~22× more *precise*
(σ smaller by that factor), yet both instruments are equally *accurate* — they agree on the true
value. Precision is reproducibility; accuracy is correctness. A student who concludes "the calipers
are more accurate" has conflated the two and should lose the conceptual marks: nothing in this data
establishes which is closer to truth, only which is more repeatable.

Note the ruler's σ ≈ 0.35 cm is roughly a third of its 0.1 cm scale division — about what
repeated re-positioning should give. A student reporting ruler σ = 0.001 cm has not re-positioned
between trials and has measured their own consistency at reading one fixed placement.

---

## Station B — Timing and Reaction Time

**Why timing 10 periods beats timing 1 period ten times.**

Human reaction time contributes an error of roughly ±0.1 s **per stopwatch operation** — once at
start and once at stop.

- *Method 1* (time one period, repeat 10×): each of the 10 measurements carries the full ±0.1 s
  reaction error, so σ per period stays ~0.1 s. Averaging 10 of them gives
  σ_mean ≈ 0.1/√10 ≈ 0.03 s.
- *Method 2* (time 10 consecutive periods once, divide by 10): the reaction error enters
  **once for the whole run**, then is divided by 10 along with the time — giving ~0.01 s per period.

Method 2 wins by a further factor of ~3 here, and the advantage grows linearly with the number of
periods counted. The general principle: **when a fixed error attaches to each measurement
*operation*, reduce the number of operations, not just the scatter.** Averaging fights *random*
error; restructuring the measurement fights the error's *entry point*.

Students who answer only "averaging reduces error" have missed the question — that is Method 1's
mechanism, and Method 1 is the worse method.

---

## Station C — Indirect Measurement and Propagation

| Trial | Diameter (cm) |
|---|---|
| 1 | 2.540 |
| 2 | 2.535 |
| 3 | 2.545 |
| 4 | 2.538 |
| 5 | 2.542 |

Mean d̄ = **2.5400 cm**, σ = 0.0038 cm, σ_d̄ = **0.0017 cm**.

**Volume.** V = (4/3)π(d/2)³ = (π/6)d³ = **8.580 cm³**

Power rule with n = 3 (V ∝ d³):

$$\frac{\sigma_V}{V} = 3\frac{\sigma_d}{d} = 3 \times \frac{0.0017}{2.5400} = 0.00201 = 0.201\%$$

σ_V = 0.201% × 8.580 = **0.017 cm³** → **V = 8.58 ± 0.02 cm³**

> The single most common error here is using the **radius rule on a diameter measurement**, or
> forgetting the factor 3 entirely. A student who writes σ_V/V = σ_d/d has not applied the power
> rule and loses the propagation marks even if V itself is right.

**Density.** With m = 67.4 ± 0.1 g:

$$\rho = \frac{m}{V} = \frac{67.4}{8.580} = 7.855\ \text{g/cm}^3$$

$$\frac{\sigma_\rho}{\rho} = \sqrt{\left(\frac{0.1}{67.4}\right)^2 + (0.00201)^2} = 0.00250 = 0.25\%$$

**ρ = 7.86 ± 0.02 g/cm³.** Accepted value for steel is 7.85 g/cm³; the deviation is
0.27σ, so the result **is consistent** with the accepted value.

Note the mass contributes 0.15% and the volume 0.201% — the two are
comparable here, so neither dominates. If a student's volume term dominates by 10×, improving the
mass measurement is wasted effort; that "which term dominates?" question is what error budgets are
for and should be rewarded in the discussion.

---

## Station D — Fermi Estimation

Accept **any** answer whose reasoning is sound and whose result lands within one order of magnitude.
The reasoning is the deliverable; the number is not.

**1. Breaths in a lifetime.** ~15 breaths/min × 60 × 24 × 365 × 80 yr ≈ **6 × 10⁸**.
Accepted ~5–7 × 10⁸. ✓

**2. Total length of blood vessels.** Capillaries dominate by number. Order 10⁹–10¹⁰ capillaries,
each ~1 mm → 10⁶–10⁷ m ≈ **10³–10⁴ km** from that route; commonly quoted figures are ~10⁵ km
(≈ 10⁸ m). Anything in 10⁴–10⁶ km is a pass. This is the estimate students get *worst*, because the
capillary count is genuinely hard to guess — say so rather than penalising it heavily.

**3. Mass of air in the classroom.** ~10 m × 8 m × 3 m = 240 m³, air density 1.2 kg/m³ →
**≈ 290 kg**. Most students are startled that classroom air weighs as much as three adults; that
reaction is the point of the exercise.

Award full marks for **stated assumptions** even where the arithmetic drifts. Award nothing for a
bare number with no chain of reasoning, however close it lands.

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

**Lab 0 specifically:** this lab is graded on *methodology*, not on hitting accepted values.
A student whose sphere density is 12% off but who propagated correctly and identified the
likely systematic cause earns more than one who got 7.85 with no uncertainty analysis.

---

*PHYS 141 · Week 0 · Lab Solutions · Instructor Copy · © CSE Department*
