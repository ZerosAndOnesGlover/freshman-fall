# PHYS 141 · Lab 4
# Conservation of Energy on a Track

**Duration:** 3 hours | **Partners:** Groups of 2–3
**Lab session:** Thursday 22 October 2026, 14:00–17:00 · Week 4 — the lab meets Thursday, after that week's Mon/Tue lectures.

---

> **Line fits:** use the formulas in the *Fitting a Straight Line* box in Lab 1 (slope, intercept and
> their uncertainties), or `LINEST`, which gives the same numbers.

## Objectives

1. Verify conservation of mechanical energy for a cart on a low-friction track
2. Quantify the energy lost to friction/air resistance by comparing measured speeds to frictionless predictions
3. Determine an effective coefficient of friction from energy loss data
4. Practice combining kinematics measurement with energy analysis

---

## Background

For a cart of mass m released from rest at height h on a track descending to a lower level, energy conservation (frictionless case) predicts:

$$v_{bottom} = \sqrt{2gh}$$

In reality, some mechanical energy is lost to friction (track bearings, air resistance). The energy actually converted to kinetic energy is:

$$\frac{1}{2}mv_{measured}^2 = mgh - E_{lost}$$

We will measure v at the bottom for various release heights and compare to the frictionless prediction, extracting the energy loss as a function of distance traveled.

---

## Apparatus

- Inclined track (adjustable angle) with low-friction cart
- Photogate timers (at least 2, positioned at start and end of measurement region) OR motion sensor
- Meter stick, digital protractor or angle finder
- Electronic balance (for cart mass)
- Additional mass set (to vary cart mass)

---

## Part 1: Basic Energy Conservation Test

### Procedure

1. Set the track at a fixed angle θ. Measure θ precisely.
2. Measure the cart's mass m.
3. Mark a release point at height h (measured vertically) above the bottom photogate.
4. Release the cart from rest at this point. Record the speed at the bottom photogate (v_measured).
5. Repeat for 5 different release heights, spanning a wide range (e.g., 0.10 m to 0.50 m).
6. For each height, take 3 trials and average.

### Data Table

| Trial | h (m) | v_measured (m/s) — mean of 3 | v_theory = √(2gh) (m/s) | % discrepancy |
|-------|-------|-------------------------------|--------------------------|----------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

### Analysis

1. Plot v_measured² vs. h. Theory predicts a straight line through the origin with slope 2g.
2. Fit a line. Extract the slope and compare to 2g = 19.62 m²/(s²·m).
3. Is the y-intercept exactly zero, or slightly negative? A negative intercept (or a slope slightly less than 2g) is evidence of energy loss to friction. Explain what a systematic offset in either direction would mean physically.

---

## Part 2: Quantifying Energy Loss

### Procedure

1. Using your data from Part 1, calculate the kinetic energy at the bottom for each trial: $KE_{measured} = \frac{1}{2}mv_{measured}^2$
2. Calculate the initial potential energy for each trial: $U_i = mgh$
3. Calculate the energy "lost": $E_{lost} = U_i - KE_{measured}$

| h (m) | U_i = mgh (J) | KE_measured (J) | E_lost (J) | E_lost / U_i (%) |
|-------|---------------|-------------------|-------------|--------------------|
| | | | | |

### Analysis

1. Plot E_lost vs. the distance traveled along the track (d = h/sinθ) for each trial.
2. If friction is well-modeled as a constant force f_k opposing motion, E_lost = f_k × d should be linear through the origin. Fit a line; extract f_k from the slope.
3. Calculate an effective coefficient of kinetic friction: μ_k,eff = f_k / (mg cosθ). Report this value.
4. Compare E_lost/U_i (%) across different heights. Does the fractional energy loss stay roughly constant, increase, or decrease with height? What does this imply about whether friction is more like a constant force (∝ distance) or has some other dependence (e.g., ∝ speed, relevant for air resistance)?

---

## Part 3: Effect of Mass on Energy Loss

### Procedure

1. Add a known mass to the cart (e.g., double its mass). Repeat the h = 0.30 m measurement (3 trials).
2. Compare v_measured for the original vs. doubled mass at the same height.

### Analysis

1. In the frictionless prediction v = √(2gh), does mass appear? What does your data show?
2. If E_lost is due to friction (∝ N = mg cosθ, hence ∝ m), does doubling the mass double E_lost? Does it change v_measured at all (since both U_i and E_lost scale with m)? Explain your reasoning algebraically before checking against your data.

---

## Part 4: Conceptual Synthesis (Written in Report)

**Q1.** Two carts are released from the same height on tracks of different shapes (one straight incline, one curved with the same start/end height). Assuming both tracks are frictionless, would you expect the same final speed? Would you expect the same final velocity vector (direction)? Explain the distinction.

**Q2.** Your track has real friction. Does the specific *shape* of the track (straight vs. curved, same height) affect the total energy lost to friction, even though it wouldn't affect the frictionless-case speed? Explain using the fact that friction work depends on the actual path length, while gravitational PE only depends on height change.

**Q3.** If you were to repeat this experiment on a track in vacuum (no air resistance) versus in air, what difference would you expect in the E_lost vs. distance relationship? Which loss mechanism (track friction vs. air resistance) do you think dominates in your setup, and how might you experimentally distinguish between them?

---

## Lab Report Requirements

| Component | Points |
|-----------|--------|
| Data tables (Parts 1–3), properly formatted | 20 |
| v² vs. h plot with fit and slope comparison to 2g | 20 |
| E_lost vs. distance plot; μ_k,eff extraction | 20 |
| Mass-dependence analysis (Part 3) | 15 |
| Conceptual synthesis (Q1–Q3) | 25 |
| **Total** | **100** |

---

## Pre-Lab Questions (Due at Start of Lab)

**Q1.** Derive v = √(2gh) from energy conservation for a cart released from rest at height h (frictionless case). State your reference point for potential energy explicitly.

**Q2.** If E_lost = f_k · d and d = h/sinθ, express E_lost as a function of h, θ, and f_k. If you plot E_lost vs. h (not d) at fixed θ, would you still expect a straight line? What would the slope represent?

**Q3.** Explain in your own words why the plot of v² vs. h (not v vs. h) is the correct choice for extracting 2g as a slope. What would a v vs. h plot look like instead (linear? curved?), and why is it a less convenient choice for this analysis?
