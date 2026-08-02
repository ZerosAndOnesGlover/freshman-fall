# PHYS 141 — Week 5
## LAB 5 Solutions — INSTRUCTOR ONLY

> **Representative data.** The numbers below are one realistic dataset, generated and checked
> numerically. Student apparatus will differ — **grade the method, not agreement with these
> figures.** Every derived quantity here is reproducible from the raw data in the same section,
> so you can re-run a student's arithmetic against their own readings.

---

## Part 1 — Perfectly Inelastic Collisions (carts stick)

Equal masses, m₁ = m₂ = 0.5 kg. Cart 1 incoming at v₁ = 0.842 m/s, cart 2 at rest.

**Prediction.** Momentum conservation gives

$$v_f = \frac{m_1 v_1}{m_1+m_2} = \frac{0.5(0.842)}{1.0} = 0.4210\ \text{m/s}$$

|  | v₁ (m/s) | v₂ (m/s) | p_total (kg·m/s) | K_total (J) |
|---|---|---|---|---|
| Before | 0.842 | 0.000 | 0.4210 | 0.1772 |
| After | 0.418 | 0.418 | 0.4180 | 0.0874 |


- **Momentum:** 0.4180 vs 0.4210 → **-0.71%**. Conserved within
  experimental error. ✓
- **Kinetic energy:** 0.0874 vs 0.1772 → **49.3% retained**, against a
  theoretical 50.0% for equal masses. ✓

**The theoretical retention is exact and worth deriving:**

$$\frac{K_f}{K_i} = \frac{m_1}{m_1+m_2}$$

so equal masses lose exactly half the kinetic energy — not because of friction, but because
**momentum conservation forbids keeping it**. This is the key insight of the lab. With
m₁ = 0.5 kg striking m₂ = 1.000 kg at rest, retention drops to
33.3%; in the limit of a light object striking a very heavy one, nearly all kinetic
energy is lost.

> Students frequently write that "energy was lost to friction". Here friction accounts for well
> under 1% (visible as the small momentum deficit); the other ~50% is a *required* consequence of
> the carts moving together. Marking should distinguish these two sinks explicitly.

---

## Part 2 — Elastic Collisions (magnetic bumpers)

Equal masses. Theory predicts **complete velocity transfer**: v₁′ = 0, v₂′ = v₁.

|  | v₁′ (m/s) | v₂′ (m/s) | p_total | K_total (J) |
|---|---|---|---|---|
| Before | 0.842 | 0.000 | 0.4210 | 0.1772 |
| After (theory) | 0.000 | 0.842 | 0.4210 | 0.1772 |
| After (measured) | 0.031 | 0.808 | 0.4195 | 0.1635 |


- **Momentum:** -0.36% ✓
- **Kinetic energy:** **92.2% retained** — high, but not 100%. Magnetic bumpers are
  a good approximation to elastic, not a perfect one.

The residual v₁′ = 0.031 m/s (rather than exactly 0) is the signature of imperfect elasticity.
Students should quantify it with the **coefficient of restitution**

$$e = \frac{|v_2' - v_1'|}{|v_1 - v_2|} = \frac{0.777}{0.842} = 0.923$$

where e = 1 is perfectly elastic and e = 0 perfectly inelastic. Reporting e is a stronger answer
than reporting a percentage, because it is the standard parameter and interpolates between the two
parts of this lab.

---

## Part 3 — Centre of Mass Motion

$$v_{cm} = \frac{p_{total}}{M_{total}} = \frac{0.4210}{1.0} = 0.4210\ \text{m/s}$$

After the inelastic collision: 0.4180 m/s. **Unchanged.**

This is the deeper statement of the lab: because no *external* horizontal force acts, the centre of
mass moves at constant velocity **through the collision**, whatever happens between the carts.
Collision forces are internal and cancel in pairs by Newton's third law. In the elastic case the
centre of mass also continues unchanged, even though both individual velocities change
dramatically.

A useful check students can run: in the **centre-of-mass frame** the total momentum is zero both
before and after, and a perfectly inelastic collision brings both carts to rest — making it
obvious that this collision loses the *maximum* energy consistent with momentum conservation.

---

## Part 4 — Written Discussion (expected answers)

**Which quantity is conserved in both collision types?** **Momentum.** Kinetic energy is conserved
only in the elastic case. Momentum conservation follows from the absence of external forces, and is
therefore far more robust than energy conservation, which depends on the *nature* of the internal
forces.

**Why is momentum conserved even though energy is not?** The internal forces form third-law pairs:
equal, opposite, and acting for the same duration, so the impulses cancel exactly and total
momentum cannot change. Nothing forces the *work* done by those forces to cancel — deformation and
heating are one-way. Impulse cancels; work need not.

**Largest error source.** Track levelling, almost always. A track off level by 0.5° applies a
systematic external force along the direction of motion and breaks momentum conservation outright.
Test by giving a cart a push in each direction and comparing decelerations. After that: photogate
flag width (an incorrect flag length scales every velocity), and residual friction.

**Would results differ on a frictionless track?** Momentum results would tighten slightly; the
~50% kinetic-energy loss in Part 1 would **not change at all**, since it is required by momentum
conservation rather than caused by friction. Anyone who predicts the inelastic energy loss would
vanish on a frictionless track has missed the central result.

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

*PHYS 141 · Week 5 · Lab Solutions · Instructor Copy · © CSE Department*
