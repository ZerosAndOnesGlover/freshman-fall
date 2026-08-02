# PHYS 141 — Week 4
## LAB 4 Solutions — INSTRUCTOR ONLY

> **Representative data.** The numbers below are one realistic dataset, generated and checked
> numerically. Student apparatus will differ — **grade the method, not agreement with these
> figures.** Every derived quantity here is reproducible from the raw data in the same section,
> so you can re-run a student's arithmetic against their own readings.

---

## Part 1 — Basic Energy Conservation Test

Mass m = 0.25 kg released from rest at height h, speed measured at the bottom.

| h (m) | U = mgh (J) | v_theory = √(2gh) | v_measured (m/s) | K = ½mv² (J) | K/U |
|---|---|---|---|---|---|
| 0.400 | 0.9810 | 2.8014 | 2.7034 | 0.9135 | 0.9312 |
| 0.300 | 0.7358 | 2.4261 | 2.3412 | 0.6852 | 0.9312 |
| 0.200 | 0.4905 | 1.9809 | 1.9116 | 0.4568 | 0.9312 |


**Analysis.** Kinetic energy at the bottom is consistently **7% below** the
gravitational potential energy released. Energy is *not* conserved in the mechanical-only sense —
and that is the expected, correct result, not a failed experiment.

$$\Delta KE + \Delta PE = W_{nc} \quad\Longrightarrow\quad W_{nc} = K - U < 0$$

> Mark generously here, but **penalise any report claiming "energy was conserved"** when the data
> shows a systematic 5–10% deficit. The learning objective is that the missing energy is
> accounted for, not wished away. Equally, penalise "we lost energy so the experiment failed" —
> the experiment succeeded in *measuring* W_nc.

---

## Part 2 — Quantifying the Loss

| h (m) | U (J) | K (J) | Energy lost (J) | % lost |
|---|---|---|---|---|
| 0.400 | 0.9810 | 0.9135 | 0.0675 | 6.9% |
| 0.300 | 0.7358 | 0.6852 | 0.0506 | 6.9% |
| 0.200 | 0.4905 | 0.4568 | 0.0337 | 6.9% |


The **absolute** loss grows with h (0.0337 → 0.0675 J) while the
**fractional** loss stays essentially constant at ~6.9%.

That constancy is the diagnostic. For sliding friction over a path whose length scales with h,
W_nc = μmgd ∝ h, so the *ratio* W_nc/mgh is independent of h — exactly what is observed. A loss
fraction that instead **grew** with h would indicate a speed-dependent mechanism (air drag,
rolling resistance rising with velocity) and would be a different physical finding.

**Where the energy goes:** friction between the object and the track (thermal), air resistance,
sound, and — for a rolling object — rotational kinetic energy that the ½mv² formula ignores. That
last one is not a "loss" at all but a bookkeeping error, and is the most common wrong answer worth
correcting: if the object *rolls*, K_total = ½mv² + ½Iω², and omitting the rotational term makes
conservation appear to fail by up to 29% for a solid sphere.

---

## Part 3 — Effect of Mass

| m (kg) | U at h = 0.400 m (J) | K measured (J) | Fraction lost |
|---|---|---|---|
| 0.250 | 0.9810 | 0.9135 | 6.9% |
| 0.500 | 1.9620 | 1.8271 | 6.9% |


**Expected result: the fraction lost is independent of mass.**

Both U = mgh and the friction work μmgd carry one factor of m, so it cancels in the ratio. The
*absolute* numbers double when the mass doubles; the *percentage* does not move. Students should
predict this before measuring, and the prediction follows from v = √(2gh) containing no m at all.

---

## Part 4 — Conceptual Synthesis (expected answers)

**Is energy conservation violated?** No. **Total** energy is conserved exactly; **mechanical**
energy is not, because non-conservative forces convert it to thermal energy. The distinction
between the two statements is the entire content of this lab.

**Why is gravity conservative?** The work it does depends only on the change in height, not on the
path taken — so a potential energy U = mgh can be defined as a function of position alone. Friction
admits no such function: its work depends on path *length*, so two paths between the same endpoints
give different answers and no potential exists.

**Would a longer, gentler ramp lose more or less energy?** **More**, for the same drop height. The
friction work is μmg·cos θ·d, and reaching the same h over a gentler slope requires a
proportionally longer d — the increase in path length outweighs the reduction in normal force only
partially, and the net is a larger loss. Students who reason "gentler slope, less friction force,
less loss" have considered the force but not the distance, and should be shown the product.

**Redesign to reduce loss.** An air track or low-friction cart; a shorter path; measuring speed by
photogate rather than by timing over a distance; and — most importantly — **accounting for
rotational energy** if the object rolls rather than slides.

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

*PHYS 141 · Week 4 · Lab Solutions · Instructor Copy · © CSE Department*
