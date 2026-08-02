# PHYS 141 · Lab 5
# Collisions: Verifying Conservation of Momentum

**Duration:** 3 hours | **Partners:** Groups of 2–3

---

## Objectives

1. Verify conservation of momentum for both elastic and perfectly inelastic collisions
2. Measure kinetic energy before and after each collision type and confirm the expected KE behavior
3. Compare experimental collision outcomes to the theoretical elastic-collision formulas
4. Determine an experimental coefficient of restitution

---

## Background

On a low-friction track, two carts of masses $m_1$ and $m_2$ can collide via:
- **Magnetic bumpers** (approximately elastic — carts repel without contact)
- **Velcro pads** (perfectly inelastic — carts stick together)

We will test momentum conservation for both cases and check whether kinetic energy is also conserved (elastic case) or significantly reduced (inelastic case).

---

## Apparatus

- Low-friction track with two carts (adjustable mass via add-on weights)
- Magnetic bumper attachments (for elastic collisions)
- Velcro attachments (for perfectly inelastic collisions)
- Photogate timers (at least 2) or motion sensors, positioned to record velocity before and after collision
- Electronic balance

---

## Part 1: Perfectly Inelastic Collisions

### Procedure

1. Weigh both carts (with Velcro attachments). Record $m_1$ and $m_2$.
2. Set cart 2 at rest in the middle of the track.
3. Give cart 1 a push toward cart 2. Measure cart 1's velocity just before collision ($v_{1i}$) using the photogate.
4. After collision (carts stick and move together), measure the common final velocity ($v_f$) using the second photogate.
5. Repeat for 5 trials, varying the push strength (i.e., varying $v_{1i}$).
6. Repeat the entire procedure with $m_2$ having added mass (at least 2 different mass ratios).

### Data Table

| Trial | m₁ (kg) | m₂ (kg) | v₁ᵢ (m/s) | v_f measured (m/s) | v_f theory (m/s) | % discrepancy |
|-------|---------|---------|-----------|----------------------|--------------------|----------------|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

$v_{f,theory} = \dfrac{m_1 v_{1i}}{m_1+m_2}$ (since cart 2 starts at rest)

### Analysis

1. For each trial, compute the initial and final kinetic energy. Compute the fraction of KE lost.
2. Plot the fraction of KE lost vs. the mass ratio $m_2/m_1$ across your trials. Is there a trend? (Theory predicts fraction lost = $m_2/(m_1+m_2)$ when cart 2 starts at rest — verify this relationship.)
3. Compute the percent discrepancy between measured and theoretical final velocity for each trial. Discuss sources of discrepancy (track friction, bumper imperfections, timing precision).

---

## Part 2: Elastic Collisions (Magnetic Bumpers)

### Procedure

1. Replace Velcro with magnetic bumpers on both carts.
2. Set cart 2 at rest. Push cart 1 toward it. Measure $v_{1i}$, and the final velocities of BOTH carts, $v_{1f}$ and $v_{2f}$, using photogates positioned appropriately.
3. Repeat for 5 trials with varying $v_{1i}$.
4. Repeat with unequal masses (add mass to one cart) for at least 2 trials.

### Data Table

| Trial | m₁ (kg) | m₂ (kg) | v₁ᵢ (m/s) | v₁f measured | v₂f measured | v₁f theory | v₂f theory |
|-------|---------|---------|-----------|---------------|----------------|--------------|--------------|
| 1 | | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |

Use the elastic collision formulas from Lecture 17 to compute theoretical values.

### Analysis

1. For each trial, verify momentum conservation: compute $p_i$ and $p_f$ and compare.
2. For each trial, verify (or check the degree of deviation from) kinetic energy conservation: compute $KE_i$ and $KE_f$.
3. For the equal-mass trials, confirm the special-case prediction: does cart 1 nearly stop, and cart 2 move off at nearly $v_{1i}$? Quantify any deviation and attribute it to imperfect elasticity of the magnetic bumpers.
4. Compute the **coefficient of restitution** for each trial: $e = \dfrac{v_{2f}-v_{1f}}{v_{1i}-v_{2i}}$ (with $v_{2i}=0$). Is e consistently close to 1 (elastic) or noticeably less?

---

## Part 3: Center of Mass Motion (Conceptual + Quick Measurement)

1. For one of your elastic collision trials, calculate $v_{cm} = \dfrac{m_1v_{1i}+m_2v_{2i}}{m_1+m_2}$ before the collision.
2. Calculate $v_{cm}$ again using the final velocities after collision: $v_{cm} = \dfrac{m_1v_{1f}+m_2v_{2f}}{m_1+m_2}$.
3. Confirm these two values match (within experimental uncertainty). This directly demonstrates that the center of mass velocity is unaffected by the (internal) collision forces.

---

## Part 4: Written Discussion

**Q1.** In Part 1, does the fraction of kinetic energy lost depend on the initial speed $v_{1i}$, or only on the mass ratio? Use your data across different speeds (same masses) to answer empirically, then explain using the algebra of $KE_{lost}/KE_i$ derived from the perfectly inelastic collision formula.

**Q2.** Real "elastic" collisions in this lab (magnetic bumpers) are never perfectly elastic. Identify at least two physical reasons why some KE is always lost even without contact, and connect this to your measured coefficient of restitution.

**Q3.** If the track were tilted very slightly (introducing a small external force from gravity along the track), would momentum still be conserved during the brief collision itself? Would it be conserved over the longer timescale of the whole cart's journey down the track? Explain the distinction between "during the collision" and "over the whole experiment" in terms of the relevant timescales and the size of external vs. internal forces.

---

## Lab Report Requirements

| Component | Points |
|-----------|--------|
| Part 1 data table and KE-loss analysis | 20 |
| Part 2 data table, momentum and KE verification | 25 |
| Coefficient of restitution calculation and discussion | 15 |
| Part 3 center-of-mass velocity check | 15 |
| Part 4 written discussion (Q1–Q3) | 25 |
| **Total** | **100** |

---

## Pre-Lab Questions (Due at Start of Lab)

**Q1.** Derive the fraction of kinetic energy lost in a perfectly inelastic collision, $\dfrac{KE_i-KE_f}{KE_i}$, in terms of $m_1$, $m_2$ only (assuming cart 2 starts at rest). Show that it depends only on the mass ratio, not on $v_{1i}$.

**Q2.** For an elastic collision with $m_1 = m_2$ and cart 2 initially at rest, use the general elastic collision formulas to show algebraically that $v_{1f}=0$ and $v_{2f}=v_{1i}$.

**Q3.** Explain in your own words why the coefficient of restitution e is defined as a ratio of *relative* velocities (separation speed / approach speed) rather than simply comparing final and initial individual speeds.
