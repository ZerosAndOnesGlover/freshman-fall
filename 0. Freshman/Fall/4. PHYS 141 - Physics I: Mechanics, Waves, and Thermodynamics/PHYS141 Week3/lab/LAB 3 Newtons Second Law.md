# PHYS 141 — Lab 3
# Newton's Second Law: The Atwood Machine

**Duration:** 3 hours | **Partners:** Groups of 2–3

---

## Objectives

1. Verify Newton's second law experimentally by measuring acceleration as a function of net force (at constant total mass) and as a function of total mass (at constant net force)
2. Compare measured accelerations to theoretical predictions from the Atwood machine formula
3. Identify and characterize systematic errors due to pulley friction and string/pulley mass
4. Practice linear regression as a method of extracting physical quantities from data

---

## Background

For an ideal (massless, frictionless) Atwood machine with masses m₁ and m₂:

$$a = \frac{(m_2 - m_1)g}{m_1 + m_2} = \frac{\Delta m \cdot g}{M_{total}}$$

where Δm = m₂ − m₁ is the mass difference and M_total = m₁ + m₂ is the total mass.

This gives two testable linear relationships:

**Test 1 — Vary net force, keep total mass constant:**
Move mass from one side to the other (so Δm increases but M_total = m₁ + m₂ stays fixed).
Then: a = (g/M_total) · Δm — a should be linear in Δm, with slope g/M_total.

**Test 2 — Vary total mass, keep net force constant:**
Add equal mass to both sides (so M_total increases but Δm stays fixed).
Then: a = (Δm · g) / M_total — a should be linear in 1/M_total, with slope Δm · g.

---

## Apparatus

- Atwood machine: low-friction pulley on stand, string
- Set of calibrated masses (50 g, 100 g, 200 g hangers + small rider masses of 5 g, 10 g, 20 g)
- Photogate timer or smart pulley (measures velocity vs. time digitally)
- **Alternative if photogates unavailable:** Meter stick + stopwatch (measure distance fallen in a measured time from rest; use Δy = ½at² to extract a)
- Electronic balance (to verify masses)
- Lab notebook / data sheet

---

## Part 1: Familiarization and Systematic Error Check

### 1.1 Verify mass values

Weigh each mass hanger and rider mass on the electronic balance. Record actual values — they may differ slightly from labeled values. Use actual measured masses throughout.

### 1.2 Check pulley friction

Load equal masses on both sides (e.g., 200 g + 200 g). Give one side a gentle push. Observe: does the system decelerate and stop (friction present), or continue at constant speed (friction negligible)?

If the system decelerates noticeably, your pulley has significant friction. Record this qualitative observation — it will be a systematic error in your analysis.

### 1.3 Establish the measurement procedure

Set up one test run with m₁ = 200 g and m₂ = 220 g (Δm = 20 g). Using your measurement system (photogate or stopwatch), determine how you will extract acceleration a from your raw data. Write the extraction formula in your notebook before taking data.

**For photogate/smart pulley:** The software gives v(t). Fit a line to v(t); slope = a.

**For stopwatch method:** Release from rest. Measure the time t for the heavier mass to fall a distance d. Use a = 2d/t² (derived from d = ½at²). Average multiple trials.

---

## Part 2: Test 1 — Acceleration vs. Net Force (Δm), Fixed Total Mass

### Setup

Fix total mass: M_total = m₁ + m₂ = 400 g (constant throughout).

Transfer small rider masses from m₁ side to m₂ side to increase Δm while keeping M_total fixed.

| m₁ (g) | m₂ (g) | Δm (g) | M_total (g) | a_measured (m/s²) | a_theory (m/s²) |
|--------|--------|--------|------------|-------------------|----------------|
| 200 | 200 | 0 | 400 | 0 (by symmetry) | 0 |
| 195 | 205 | 10 | 400 | | |
| 190 | 210 | 20 | 400 | | |
| 180 | 220 | 40 | 400 | | |
| 160 | 240 | 80 | 400 | | |
| 140 | 260 | 120 | 400 | | |

Take 3 trials at each Δm value. Record all raw data. Compute the mean and standard error for each a_measured.

### Analysis

1. Plot a_measured (with error bars) vs. Δm on graph paper or spreadsheet.
2. Fit a straight line through the origin (theory predicts a = (g/M_total) · Δm with zero intercept).
3. Extract the slope. Compare to the predicted slope g/M_total = 9.81/0.400 = 24.5 m/s²/kg.
4. Compute percent discrepancy between measured slope and theoretical slope.

---

## Part 3: Test 2 — Acceleration vs. 1/M_total, Fixed Δm

### Setup

Fix Δm = 20 g (e.g., always have 10 g more on the heavy side). Increase M_total by adding equal mass to both sides.

| m₁ (g) | m₂ (g) | Δm (g) | M_total (g) | 1/M_total (kg⁻¹) | a_measured (m/s²) | a_theory (m/s²) |
|--------|--------|--------|------------|-----------------|-------------------|----------------|
| 190 | 210 | 20 | 400 | 2.500 | | |
| 240 | 260 | 20 | 500 | 2.000 | | |
| 290 | 310 | 20 | 600 | 1.667 | | |
| 390 | 410 | 20 | 800 | 1.250 | | |
| 490 | 510 | 20 | 1000 | 1.000 | | |

### Analysis

1. Plot a_measured vs. 1/M_total. Theory predicts a straight line through the origin with slope Δm · g = 0.020 × 9.81 = 0.196 N.
2. Fit a line. Extract slope. Compare to 0.196 N.
3. Does the y-intercept differ significantly from zero? If so, this may indicate friction (a constant deceleration offset reduces all measured accelerations equally, shifting the line downward).

---

## Part 4: Extracting g from the Data

From Test 1: slope_1 = g/M_total → g = slope_1 × M_total

From Test 2: slope_2 = Δm · g → g = slope_2 / Δm

Compute g from both tests. Report each as g ± σ_g (propagate slope uncertainty).

Compare both values to g_accepted = 9.81 m/s². Compute percent discrepancy for each.

---

## Part 5: Systematic Error Analysis (Written in Report)

**Q1.** Pulley friction acts as an additional force opposing the motion of the string. If friction force f acts, the modified equation for the Atwood machine becomes:

$$a = \frac{(\Delta m) g - f_{eff}}{M_{total}}$$

where f_eff is an effective friction force. How would friction shift your a vs. Δm graph (intercept? slope?)? Does your data show evidence of this?

**Q2.** The real pulley has mass M_pulley. A massive pulley has rotational inertia and effectively adds to the system mass. The corrected formula is:

$$a = \frac{\Delta m \cdot g}{M_{total} + \frac{1}{2}M_{pulley}}$$

(The ½ factor comes from rotational mechanics — Week 6.) If M_pulley is unknown, how would you extract it from your data? Which graph (Test 1 or Test 2) makes this easier?

**Q3.** Your string is not perfectly massless. If it has total mass m_s, how does this affect the system? In what direction would this shift your measured g?

---

## Lab Report Requirements

| Component | Points |
|-----------|--------|
| Data tables with raw data, means, and standard errors | 15 |
| a vs. Δm plot with fit, error bars, and slope extraction | 20 |
| a vs. 1/M_total plot with fit, error bars, and slope extraction | 20 |
| g extracted from both tests with uncertainties | 15 |
| Percent discrepancy from accepted g for both tests | 10 |
| Systematic error analysis (Q1–Q3) | 20 |
| **Total** | **100** |

---

## Pre-Lab Questions (Due at Start of Lab)

**Q1.** Derive the Atwood machine acceleration formula a = (m₂−m₁)g/(m₁+m₂) from Newton's second law applied to each mass separately. Show every step.

**Q2.** In Test 1, the slope of a vs. Δm should equal g/M_total. If M_total = 400 g, calculate the expected slope in SI units (m/s²) per (kg). What are the units of the slope?

**Q3.** If the measured acceleration is consistently 5% less than theoretical, propose two distinct physical explanations and explain how you would distinguish between them experimentally.
