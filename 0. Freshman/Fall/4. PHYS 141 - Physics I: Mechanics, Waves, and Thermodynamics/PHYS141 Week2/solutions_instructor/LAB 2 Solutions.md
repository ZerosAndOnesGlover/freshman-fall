# PHYS 141 · Week 2
## LAB 2 Solutions — INSTRUCTOR ONLY

> **Representative data.** The numbers below are one realistic dataset, generated and checked
> numerically. Student apparatus will differ — **grade the method, not agreement with these
> figures.** Every derived quantity here is reproducible from the raw data in the same section,
> so you can re-run a student's arithmetic against their own readings.

---

## Part 1 — Determining v₀ from a Horizontal Launch

Table height h = 0.95 ± 0.002 m. Time of flight is set **entirely by the fall**:

$$t = \sqrt{\frac{2h}{g}} = \sqrt{\frac{2(0.95)}{9.81}} = 0.4401\ \text{s}$$

| Trial | Range x (m) |
|---|---|
| 1 | 1.281 |
| 2 | 1.295 |
| 3 | 1.270 |
| 4 | 1.288 |
| 5 | 1.276 |

x̄ = **1.2820 m**, σ = 0.0098 m, σ_x̄ = **0.0044 m**

$$v_0 = \frac{\bar{x}}{t} = \frac{1.2820}{0.4401} = 2.913\ \text{m/s}$$

Propagating (v₀ = x̄·√(g/2h), so h enters with power −½):

$$\frac{\sigma_{v_0}}{v_0} = \sqrt{\left(\frac{\sigma_{\bar x}}{\bar x}\right)^2 + \left(\tfrac{1}{2}\frac{\sigma_h}{h}\right)^2} = 0.00358$$

**v₀ = 2.91 ± 0.01 m/s**

> The horizontal and vertical motions are **independent** and share only *t*. Students who compute
> t from the horizontal motion, or who use the full launch speed in a vertical equation, have
> missed the entire point of the lab and should lose the method marks regardless of their number.

---

## Part 2 — Range vs. Angle

With v₀ = 2.913 m/s and launch/landing at the same height, R = v₀² sin(2θ)/g:

| Angle θ | R_theory (m) |
|---|---|
| 15° | 0.4325 |
| 20° | 0.5560 |
| 25° | 0.6626 |
| 30° | 0.7491 |
| 35° | 0.8128 |
| 40° | 0.8519 |
| 45° | 0.8650 |
| 50° | 0.8519 |
| 55° | 0.8128 |
| 60° | 0.7491 |
| 65° | 0.6626 |
| 70° | 0.5560 |
| 75° | 0.4325 |


**Expected findings:**

1. **Maximum at θ = 45°**, R_max = v₀²/g = **0.865 m**. Since sin(2θ) peaks at
   2θ = 90°, the maximum is at 45° *independently of v₀* — a result students should state, not
   just observe.
2. **Complementary angles give equal range.** 30° and 60° both give
   0.7491 m; 15° and 75° both give
   0.4325 m. Because sin(2θ) = sin(180° − 2θ), the pairs
   θ and 90° − θ are exactly equal. The two trajectories differ in *shape* — the high-angle shot
   flies higher and lands more steeply — but the ranges match.
3. Measured ranges typically fall **2–5% below** theory, systematically, with the deficit
   growing at large angles where flight time and therefore drag exposure is greatest.

**If the launcher sits above the landing plane**, the symmetry breaks and the optimum shifts
**below 45°** (toward ~40–42° for a typical table). A student whose data peaks near 40° and who
explains it this way is *more* correct than one who reports 45° and stops.

---

## Part 3 — Testing the v₀² Dependence

R ∝ v₀² at fixed angle. Doubling the launch speed should **quadruple** the range.

To test it properly, plot **R vs. v₀²** and confirm linearity through the origin, or plot
**log R vs. log v₀** and confirm a slope of 2. The log–log form is the better test: it *measures*
the exponent rather than assuming it, and a fitted exponent of, say, 1.85 ± 0.05 is real evidence
of drag rather than a failed experiment.

---

## Part 4 — Conceptual Questions

**Time of flight vs. angle.** Flight time depends only on the **vertical** component
v₀sin θ, so it increases monotonically with θ up to 90°. Range does not, because the horizontal
component v₀cos θ is simultaneously shrinking. Range is the product of a rising and a falling
factor — hence the interior maximum.

**Effect of mass.** None, in the absence of drag: the trajectory equations contain no m. With drag
present, a heavier projectile of the same size is affected **less**, because drag force is set by
size and speed while the resisting inertia grows with mass. This is why a lead ball outranges a
plastic one of identical diameter.

**Why measure v₀ separately in Part 1?** Because using Part 2's own data to infer v₀ and then
"verifying" Part 2 would be circular. An **independent** determination is what makes Part 2 a test
rather than a restatement. Reward students who articulate this.

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

*PHYS 141 · Week 2 · Lab Solutions · Instructor Copy · © CSE Department*
