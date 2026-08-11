# PHYS 141 · Lab 2
# Projectile Motion: Measuring Range vs. Launch Angle

**Duration:** 3 hours | **Partners:** Groups of 2–3
**Lab session:** Thursday of Week 2 — the lab meets Thursday, after that week's Mon/Tue lectures.

---

## Objectives

1. Measure the horizontal range of a projectile as a function of launch angle
2. Compare measured ranges to theoretical predictions from the kinematic equations
3. Identify and quantify the effect of air resistance by comparing theory to experiment
4. Determine the launch speed v₀ experimentally from a horizontal-launch trial
5. Practice propagating uncertainty through multi-step calculations

---

## Background

From Lecture 8, for a projectile launched at angle θ with speed v₀ from and landing at the same height:

$$R = \frac{v_0^2 \sin 2\theta}{g}$$

This predicts:
- Maximum range at θ = 45°
- Equal ranges for complementary angles (θ and 90° − θ)
- Range proportional to v₀²

We will test these predictions experimentally and determine how well ideal projectile theory describes reality.

---

## Apparatus

- Spring-loaded projectile launcher (adjustable angle, fixed launch speed)
- Steel ball bearing (projectile)
- Metric tape measure and plumb bob
- Carbon paper + white paper (to record landing position)
- Ruler and calipers
- Protractor (to verify launch angle)
- Clamp stand to fix launcher height

---

## Safety

- Never look down the barrel of the launcher
- Keep bystanders clear of the landing zone (2 m radius)
- Announce "firing" before each launch

---

## Part 1: Determining v₀ from a Horizontal Launch

Before measuring angle-dependent ranges, you must know v₀. The cleanest method: launch horizontally (θ = 0°) from a known height H above the floor.

### Procedure

1. Fix the launcher horizontally at height H above the floor. Measure H carefully (record ±uncertainty).
2. Fire the ball 5 times. Mark each landing position with carbon paper. Measure horizontal distance x from directly below the launch point for each trial.
3. Record all 5 x-values. Compute mean x̄ and standard error σ_x̄.

### Extracting v₀

For horizontal launch: x = v₀ · t and H = ½gt². Eliminating t:

$$v_0 = x\sqrt{\frac{g}{2H}}$$

Using mean x̄:
$$v_0 = \bar{x}\sqrt{\frac{g}{2H}}$$

**Propagate the uncertainty in v₀** from uncertainties in x̄ and H:

$$\frac{\sigma_{v_0}}{v_0} = \sqrt{\left(\frac{\sigma_{\bar{x}}}{\bar{x}}\right)^2 + \frac{1}{4}\left(\frac{\sigma_H}{H}\right)^2}$$

(The ¼ factor comes from the square root of H — apply the power rule for propagation.)

Record: **v₀ = ___ ± ___ m/s**

---

## Part 2: Range vs. Angle

### Procedure

1. Set the launcher to each angle in the table below. Fire 3 times at each angle; record all landing positions using carbon paper.
2. Measure the range R for each trial (horizontal distance from launch point to landing point — set up a plumb bob at the launch point to mark the horizontal reference).
3. Compute the mean range R̄ and standard error for each angle.

| θ (°) | Trial 1 R (m) | Trial 2 R (m) | Trial 3 R (m) | R̄ (m) | σ_R̄ (m) | R_theory (m) |
|--------|--------------|--------------|--------------|--------|-----------|-------------|
| 15 | | | | | | |
| 30 | | | | | | |
| 40 | | | | | | |
| 45 | | | | | | |
| 50 | | | | | | |
| 60 | | | | | | |
| 75 | | | | | | |

Fill in R_theory using R = v₀²sin2θ/g with your measured v₀.

### Analysis

1. Plot R̄ (with error bars ±σ_R̄) vs. θ on the same axes as R_theory vs. θ. Use a smooth curve for theory and data points with error bars for measurements.

2. At which angle is measured range maximum? How does this compare to the theoretical 45°?

3. Test the complementary-angle prediction: compare R̄ at (30°, 60°) and at (15°, 75°). Do the pairs agree within uncertainty?

4. Compute the **percent discrepancy** between measured and theoretical range at each angle:
$$\% \text{ discrepancy} = \frac{|R_{theory} - \bar{R}|}{R_{theory}} \times 100\%$$

Is the discrepancy larger at small angles or large angles? What does this suggest about where air resistance has the most effect?

---

## Part 3: Testing the v₀² Dependence (If Launcher Has Multiple Power Settings)

If your launcher has two or more power settings:

1. Repeat the θ = 45° measurement at each power setting (3 trials each).
2. Determine v₀ for each setting using Part 1's method.
3. Plot R vs. v₀². If R ∝ v₀², the plot should be linear through the origin.
4. Find the slope of the best-fit line. What physical quantity does it equal at θ = 45°? (R = v₀²sin90°/g = v₀²/g, so slope = 1/g.)
5. Extract g from the slope and compare to 9.81 m/s².

---

## Part 4: Conceptual Questions (Written in Report)

Answer fully in your report (3–5 sentences each):

**Q1.** Your measured maximum range occurs at a slightly lower angle than 45°. Propose at least two physical reasons why, and explain which you think is dominant.

**Q2.** At θ = 75°, is the measured range larger or smaller than theory predicts? Explain the direction of the discrepancy using air resistance physics (think about whether the ball spends more or less time in the air compared to 30°, and how drag accumulates over time).

**Q3.** You determined v₀ from a horizontal launch and used it to predict ranges at other angles. List all assumptions built into this procedure. Which assumption is most likely to introduce systematic error, and in what direction?

---

## Lab Report Requirements

Submit within one week of the lab.

| Component | Points |
|-----------|--------|
| Part 1: v₀ determination with full uncertainty propagation | 20 |
| Data table — complete, with units and significant figures | 15 |
| R vs. θ plot: measured (with error bars) + theoretical (smooth curve) | 20 |
| Complementary angle test | 10 |
| Percent discrepancy table and trend discussion | 15 |
| Part 4 conceptual questions | 20 |
| **Total** | **100** |

---

## Pre-Lab Questions (Due at Start of Lab)

**Q1.** Starting from x = v₀t and y = ½gt² (horizontal launch from height H), derive the formula v₀ = x√(g/2H). Show all steps.

**Q2.** Using the error propagation formula for v₀ derived in Part 1, if x̄ has 2% relative uncertainty and H has 1% relative uncertainty, what is the relative uncertainty in v₀?

**Q3.** Predict qualitatively (no calculation needed): if you increase the launch height H while keeping v₀ and θ constant, does the horizontal range increase, decrease, or stay the same? Explain using the kinematic equations.
