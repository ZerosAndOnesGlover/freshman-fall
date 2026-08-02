# PHYS 141 — Lab 7
# Verifying Conservation of Angular Momentum

**Duration:** 3 hours | **Partners:** Groups of 2–3

---

## Objectives

1. Verify conservation of angular momentum using a rotating platform with variable moment of inertia
2. Quantify the relationship between angular velocity and moment of inertia when angular momentum is conserved
3. Measure the change in kinetic energy during an angular-momentum-conserving process and connect it to work done by the person/system
4. Verify angular momentum conservation in a rotational "collision" (falling ring onto a spinning disk)

---

## Part 1: The Rotating Platform (Skater Analog)

### Background

A rotating platform (or stool) with a person holding weights in extended arms models the spinning skater from Lecture 23. As the person pulls the weights inward, the moment of inertia decreases, and — with no external torque about the vertical axis (assuming a low-friction bearing) — angular velocity increases according to $I_i\omega_i = I_f\omega_f$.

### Apparatus

- Rotating platform/stool with low-friction bearing
- Hand weights (or a rotating platform with a built-in mechanism for masses at variable radius)
- Stopwatch or motion sensor/photogate to measure rotation rate
- Meter stick (to measure arm/mass extension radius)
- Electronic balance

### Procedure

1. Measure the mass of each hand weight, and the person's approximate moment of inertia contribution (or use a platform with a known, built-in variable-radius mass system if available, for more precise/reproducible results).
2. With arms extended (measure the radius r_extended from the rotation axis to the weights), set the platform spinning at a measured initial angular velocity ω_i (using photogate/stopwatch — count rotations over a measured time).
3. Quickly pull the weights inward to a measured radius r_retracted. Measure the new angular velocity ω_f.
4. Repeat for at least 5 trials, varying the initial spin rate and/or the extended/retracted radii.

### Data Table

| Trial | r_extended (m) | r_retracted (m) | ω_i (rad/s) | ω_f (rad/s) | I_i (est.) | I_f (est.) | I_iω_i | I_fω_f |
|-------|------------------|--------------------|--------------|--------------|--------------|--------------|----------|----------|
| 1 | | | | | | | | |
| 2 | | | | | | | | |
| 3 | | | | | | | | |
| 4 | | | | | | | | |
| 5 | | | | | | | | |

Estimate I using $I = I_{person+platform} + 2m_{weight}r^2$ (factor of 2 for two weights, one per hand) — use a reasonable estimate for $I_{person+platform}$ provided by your instructor or measured separately via a torque method (as in Lab 6).

### Analysis

1. For each trial, compute the percent difference between $I_i\omega_i$ and $I_f\omega_f$. This should be small (within experimental uncertainty) if angular momentum is conserved.
2. Plot $\omega_f$ vs. $1/I_f$ (with $I_i\omega_i$ approximately constant across trials with similar initial conditions) — theory predicts this should be linear, with slope equal to the (approximately constant) initial angular momentum $L_i$.
3. For one trial, compute $KE_i=\frac12 I_i\omega_i^2$ and $KE_f=\frac12I_f\omega_f^2$. Confirm $KE_f > KE_i$ (kinetic energy increases) despite angular momentum staying constant. Discuss where this additional energy comes from.

---

## Part 2: Rotational "Collision" — Ring Dropped onto a Spinning Disk

### Background

A disk spins freely at a known ω₀. A ring (or second disk) is dropped from a small height onto the spinning disk and sticks (via friction), and the combined system settles to a new common angular velocity — directly analogous to a perfectly inelastic linear collision, but for rotation.

### Procedure

1. Measure the moment of inertia of the spinning disk alone $I_1$ (using the torque method from Lab 6, if not already known/provided).
2. Measure the mass and radius of the ring to be dropped; compute its moment of inertia $I_2 = MR^2$ (ring/hoop formula) or as provided by your instructor.
3. Spin the disk alone to a measured $\omega_0$.
4. Drop the ring onto the spinning disk (centered, so no significant off-axis torque is introduced) and measure the resulting common angular velocity $\omega_f$.
5. Repeat for 3 trials with different initial $\omega_0$.

### Data Table

| Trial | ω₀ (rad/s) | ω_f measured (rad/s) | ω_f theory = I₁ω₀/(I₁+I₂) | % discrepancy |
|-------|------------|-------------------------|--------------------------------|----------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### Analysis

1. Compute the theoretical prediction using $L_i=I_1\omega_0$ (the ring starts at rest, contributing zero angular momentum) and $\omega_f=\dfrac{I_1\omega_0}{I_1+I_2}$.
2. Compare to your measured values. Discuss sources of discrepancy (e.g., the ring not landing perfectly centered, friction during the brief "collision," air resistance).
3. Compute the kinetic energy before and after this rotational collision. Confirm that KE DECREASES (unlike Part 1) — this rotational collision is "inelastic" in the same sense as a linear perfectly-inelastic collision, and the lost KE converts to heat/sound at the disk-ring interface.

---

## Part 3: Written Discussion

**Q1.** In Part 1, is the platform+person+weights system perfectly isolated (zero external torque)? Identify at least one realistic source of external torque (however small) that could cause your measured $I_i\omega_i$ and $I_f\omega_f$ to disagree slightly.

**Q2.** Compare the energy behavior in Part 1 (KE increases) vs. Part 2 (KE decreases). Both processes conserve angular momentum — explain, in terms of internal energy sources/sinks, why one increases KE and the other decreases it.

**Q3.** If the ring in Part 2 were dropped OFF-CENTER (not coaxial with the disk's rotation axis), would simple angular momentum conservation ($I_1\omega_0=(I_1+I_2)\omega_f$) still directly apply? What additional complication would arise? (You do not need to solve this quantitatively — a qualitative explanation is sufficient.)

---

## Lab Report Requirements

| Component | Points |
|-----------|--------|
| Part 1 data table and I_iω_i vs I_fω_f verification | 25 |
| Part 1 KE analysis and discussion | 15 |
| Part 2 data table and theory comparison | 25 |
| Part 2 KE-loss analysis | 15 |
| Part 3 written discussion (Q1–Q3) | 20 |
| **Total** | **100** |

---

## Pre-Lab Questions (Due at Start of Lab)

**Q1.** Starting from $\tau_{net}=dL/dt$, explain in your own words why $\tau_{net}=0$ implies L is constant, and why this holds regardless of how complicated the internal rearrangement of mass (e.g., arms moving in and out) might be.

**Q2.** For Part 2, derive the formula $\omega_f = I_1\omega_0/(I_1+I_2)$ from conservation of angular momentum, given that the ring starts at rest (zero angular momentum) before landing on the disk.

**Q3.** If a skater's moment of inertia decreases by a factor of 3 (arms pulled in), by what factor does their angular velocity increase? By what factor does their kinetic energy increase? Show both calculations symbolically before doing any lab measurements.
