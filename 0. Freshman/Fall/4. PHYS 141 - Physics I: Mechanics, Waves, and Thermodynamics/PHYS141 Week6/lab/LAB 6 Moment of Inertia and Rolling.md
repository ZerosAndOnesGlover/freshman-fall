# PHYS 141 · Lab 6
# Moment of Inertia and the Parallel-Axis Theorem

**Duration:** 3 hours | **Partners:** Groups of 2–3
**Lab session:** Thursday 5 November 2026, 14:00–17:00 · Week 6 — the lab meets Thursday, after that week's Mon/Tue lectures.

---

> **Line fits:** use the formulas in the *Fitting a Straight Line* box in Lab 1 (slope, intercept and
> their uncertainties), or `LINEST`, which gives the same numbers.

> *Revised 2026-09-21.* Part 3 was removed: it needs Lecture 21 (Friday), after this Thursday lab. The lab is now out of 75.

## Objectives

1. Experimentally determine the moment of inertia of a rotating disk using torque and angular acceleration measurements
2. Verify the parallel axis theorem
4. Practice linearizing a nonlinear relationship for graphical analysis

---

## Part 1: Measuring Moment of Inertia via Applied Torque

### Background

A rotating platform (or disk) with unknown moment of inertia I is spun up by a falling mass connected via a string wrapped around a spindle of radius r. As in the massive-pulley Atwood analysis (Lecture 20, Example 20.5), applying Newton's second law to both the falling mass and the rotating platform gives:

$$mg - T = ma \qquad Tr = I\alpha = I\frac{a}{r}$$

Combining:
$$a = \frac{mg}{m + I/r^2}$$

Rearranging to isolate I:
$$I = r^2\left(\frac{mg}{a} - m\right) = mr^2\left(\frac{g}{a}-1\right)$$

### Apparatus

- Rotating platform/disk with spindle of known radius r
- String, hanging mass set
- Photogate or motion sensor to measure the falling mass's acceleration (or a stopwatch + ruler method as in Lab 1)
- Electronic balance
- Calipers (to measure spindle radius precisely)

### Procedure

1. Measure the spindle radius r with calipers (multiple measurements, average).
2. Attach a hanging mass m (start with a small value, e.g., 20 g) via the string over the spindle.
3. Release from rest. Measure the acceleration a of the falling mass using your timing method.
4. Repeat for at least 5 different hanging masses (varying from small to larger).
5. For each trial, compute I using the formula above.

### Data Table

| Trial | m (kg) | a (m/s²) | I = mr²(g/a − 1) (kg·m²) |
|-------|--------|----------|-----------------------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

### Analysis — Linearization

Start from the acceleration equation and rearrange so that a straight-line fit extracts I:

$$mg = a\left(m+\frac{I}{r^2}\right) \implies \frac{1}{a} = \frac{1}{g} + \frac{I}{gr^2}\cdot\frac{1}{m}$$

**Method A — plot 1/a vs. 1/m.** A straight line with

- **y-intercept = 1/g**
- **slope = I/(gr²)**, so $I = \text{slope}\times g \times r^2$

1. Construct this plot from your 5 trials.
2. Extract the y-intercept and compare 1/(intercept) to g = 9.81 m/s².
3. Extract the slope and solve for I.
4. Report I with an uncertainty taken from the fit's slope uncertainty.

**Method B — plot m(g − a) vs. a.** Keeping a friction torque τ_f in the model gives

$$m(g-a) = \frac{I}{r^2}\,a + \frac{\tau_f}{r}$$

so the **slope is I/r²** and the **intercept is τ_f/r** — this form measures the friction instead of
letting it bias I.

> **Do both, and compare.** Method A is the traditional presentation, but its x-values (1/m) are
> very unevenly spaced: your smallest hanging mass sits far from the rest and therefore dominates
> the fit, even though it is the *least* reliable trial (small a means large relative error). Its
> intercept is also an extrapolation to 1/m = 0 — infinite mass — well outside your data, so the g
> you recover from it may be wildly off or even negative.
>
> Method B has evenly spread x-values and needs no extrapolation. **Report I from both, say which
> you trust and why.** Discussing that disagreement is worth more than either number alone.

---

## Part 2: Verifying the Parallel Axis Theorem

### Procedure

1. If your rotating platform allows attaching a known point mass at a measured distance d from the rotation axis, do so (e.g., a small mass clamped at a marked radius on the disk).
2. Repeat the Part 1 procedure (torque + acceleration measurement) with the added mass in place.
3. The new total moment of inertia should be $I_{new} = I_{platform} + I_{added}$, where $I_{added} = m_{point}d^2$ (treating the added mass as a point mass at distance d — the parallel axis theorem in its simplest form).

### Analysis

1. Compute $I_{added,predicted} = m_{point}d^2$ using your measured point mass and distance.
2. Compute $I_{added,measured} = I_{new,measured} - I_{platform,measured}$ (using your Part 1 result for the bare platform).
3. Compare predicted and measured values of $I_{added}$. Compute percent discrepancy.

---

## Part 4: Written Discussion

**Q1.** In Part 1, why is it better to use the linearized 1/a vs. 1/m plot rather than simply averaging the I values computed from each individual trial? (Hint: think about how measurement uncertainty in a propagates differently depending on which variable you treat as primary.)

---

## Lab Report Requirements

| Component | Points |
|-----------|--------|
| Part 1 data table and I extraction via linearized fit | 25 |
| Part 2 parallel axis theorem verification | 20 |
| Part 4 written discussion (Q1) | 30 |
| **Total** | **75** |

---

## Pre-Lab Questions (Due at Start of Lab)

**Q1.** Starting from $mg-T=ma$ and $Tr=I\alpha$ with $a=r\alpha$, derive $I = mr^2(g/a - 1)$ showing every algebraic step.

**Q2.** Derive the linearized relationship $1/a = 1/g + I/(gr^2)\cdot(1/m)$ from the acceleration formula $a = mg/(m+I/r^2)$. Show your algebra.
