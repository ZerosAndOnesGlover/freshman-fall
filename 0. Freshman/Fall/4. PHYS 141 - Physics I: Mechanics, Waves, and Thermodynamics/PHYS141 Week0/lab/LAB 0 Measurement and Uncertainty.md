# PHYS 141 — Lab 0
# Measurement and Uncertainty

**Duration:** 3 hours | **Grading:** Completion + correctness (not graded on "right answer" — graded on correct methodology)

---

## Objectives

1. Practice measuring physical quantities with appropriate precision
2. Understand and quantify measurement uncertainty
3. Learn the rules of error propagation
4. Distinguish between **accuracy** and **precision**
5. Produce a properly formatted lab report with uncertainty analysis

---

## Part 1: Conceptual Background

### 1.1 Every Measurement Has Uncertainty

No physical measurement is perfectly exact. A measurement is only meaningful when reported as:

$$\text{measured value} \pm \text{uncertainty}$$

**Example:** L = 12.4 ± 0.1 cm means the true value of L most likely lies between 12.3 cm and 12.5 cm.

### 1.2 Accuracy vs. Precision

These terms are NOT interchangeable:

- **Accuracy:** How close a measurement is to the *true* value.
- **Precision:** How reproducible repeated measurements are (how tightly clustered).

A measurement can be precise but inaccurate (a miscalibrated ruler gives consistent but wrong readings), or accurate but imprecise (a shaky measurement that averages to the right value).

| | High Precision | Low Precision |
|---|---|---|
| **High Accuracy** | Ideal: tight cluster centered on true value | Scattered but centered on true value |
| **Low Accuracy** | Tight cluster, offset from true value (systematic error) | Scattered and offset (worst case) |

### 1.3 Types of Error

1. **Systematic error:** A consistent bias in one direction (e.g., a ruler that's actually 1% too short, a scale that's not zeroed). Cannot be reduced by repeated measurement — must be corrected by calibration.

2. **Random error:** Statistical fluctuation from one measurement to the next (e.g., reaction time variability in a stopwatch measurement). CAN be reduced by averaging many measurements.

### 1.4 Reporting Uncertainty: Standard Deviation

For N repeated measurements $x_1, x_2, ..., x_N$ of the same quantity, report:

**Mean (best estimate):**
$$\bar{x} = \frac{1}{N}\sum_{i=1}^{N} x_i$$

**Standard deviation (spread of individual measurements):**
$$\sigma = \sqrt{\frac{1}{N-1}\sum_{i=1}^{N}(x_i - \bar{x})^2}$$

**Standard error of the mean (uncertainty in your best estimate):**
$$\sigma_{\bar{x}} = \frac{\sigma}{\sqrt{N}}$$

> **Critical distinction:** σ tells you how spread out *individual* measurements are. σ_x̄ tells you how confident you are in the *mean* — and it shrinks as you take more measurements. This is why averaging many measurements improves your result: more data reduces the uncertainty in the mean, even though it doesn't reduce the spread of individual readings.

---

## Part 2: Error Propagation Rules

When you compute a result from measured quantities that each have uncertainty, the uncertainty propagates into your final answer. You must NEVER simply use the measured uncertainties as if the calculated quantity has the same fractional error without applying these rules.

### 2.1 Addition / Subtraction

If $z = x + y$ or $z = x - y$:
$$\sigma_z = \sqrt{\sigma_x^2 + \sigma_y^2}$$

(Absolute uncertainties add in quadrature.)

### 2.2 Multiplication / Division

If $z = xy$ or $z = x/y$:
$$\frac{\sigma_z}{|z|} = \sqrt{\left(\frac{\sigma_x}{x}\right)^2 + \left(\frac{\sigma_y}{y}\right)^2}$$

(Fractional/relative uncertainties add in quadrature.)

### 2.3 Power Law

If $z = x^n$:
$$\frac{\sigma_z}{|z|} = |n|\frac{\sigma_x}{x}$$

### 2.4 General Formula (for any function)

For $z = f(x, y, ...)$:
$$\sigma_z = \sqrt{\left(\frac{\partial f}{\partial x}\sigma_x\right)^2 + \left(\frac{\partial f}{\partial y}\sigma_y\right)^2 + \cdots}$$

This is the general law from which all the above rules can be derived — it comes from a first-order Taylor expansion of f around the measured values, assuming the errors are independent and random.

### 2.5 Worked Example

You measure the radius of a circle: r = 5.0 ± 0.1 cm. Find the area and its uncertainty.

$$A = \pi r^2$$
$$A = \pi (5.0)^2 = 78.5 \text{ cm}^2$$

Using the power rule (n=2):
$$\frac{\sigma_A}{A} = 2\frac{\sigma_r}{r} = 2 \times \frac{0.1}{5.0} = 0.04 = 4\%$$
$$\sigma_A = 0.04 \times 78.5 = 3.14 \text{ cm}^2$$

**Report: A = 78.5 ± 3.1 cm²** (round uncertainty to 1-2 sig figs, match decimal places in the value)

---

## Part 3: Lab Procedure

### Station A — Length Measurement (Ruler vs. Calipers)

1. Measure the length of the provided rectangular block using a standard ruler (precision ~1 mm). Take 5 independent measurements (re-position the ruler each time).
2. Measure the same length using digital calipers (precision ~0.01 mm). Take 5 independent measurements.
3. For each instrument, calculate the mean, standard deviation, and standard error of the mean.
4. **Question:** Do the two instruments agree within their uncertainties? What does this tell you about accuracy vs. precision?

### Station B — Timing Measurement (Reaction Time Limitations)

1. Using a stopwatch (manual reaction time), time 10 swings of a pendulum (provided) for a full period each. Record all 10 times.
2. Calculate mean, standard deviation, and standard error.
3. Now time **10 consecutive periods** in a single stopwatch run (start the watch, count 10 full swings, stop). Divide by 10 to get average period.
4. **Question:** Why does method (3) typically give a smaller uncertainty per period than method (1)? [Hint: think about where the human reaction time error enters each method, and how many times it enters.]

### Station C — Indirect Measurement and Propagation

1. Measure the diameter (not radius!) of a sphere using calipers (5 trials).
2. Calculate the volume of the sphere: V = (4/3)π(d/2)³
3. Propagate the uncertainty from your diameter measurement to your volume calculation using the power law rule.
4. Compare your computed density (using the sphere's known mass, provided on the lab card) to the accepted density of the material. Is your measured value consistent with the accepted value within your calculated uncertainty?

### Station D — Order-of-Magnitude Estimation (Fermi Problem)

Without using any measuring instruments, estimate (showing your reasoning, not looking anything up):

1. The number of breaths you will take in a lifetime
2. The total length of all the blood vessels in your body
3. The mass of air in your classroom

Compare your estimates to actual/accepted values (your TA will reveal these at the end of lab) and discuss the order-of-magnitude agreement.

---

## Part 4: Lab Report Requirements

Your lab report (due at the start of next week's lab) must include:

1. **Data tables** for all 4 stations, with units and appropriate sig figs
2. **Calculations** showing mean, standard deviation, standard error for repeated measurements
3. **Error propagation** worked explicitly for Station C (volume and density)
4. **Answers** to all numbered questions in the procedure
5. **A short discussion (200–300 words)** addressing: Where did the largest source of uncertainty in your results come from? Was it systematic or random? How could the experiment be redesigned to reduce it?

---

## Grading Rubric

| Component | Points |
|-----------|--------|
| Data tables, properly formatted with units | 20 |
| Correct mean/std dev/SEM calculations | 20 |
| Correct error propagation (Station C) | 25 |
| Answers to conceptual questions | 20 |
| Discussion section quality | 15 |
| **Total** | **100** |

---

## Safety Notes

- Handle calipers and glass spheres carefully — report breakage immediately, no penalty
- Pendulum stand must remain clamped to the table at all times
