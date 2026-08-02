# PHYS 141 — Lab 1
# Measuring Constant Acceleration — Measuring g

**Duration:** 3 hours | **Partners:** Groups of 2–3

---

## Objectives

1. Measure the free-fall acceleration g using a precision timing device
2. Construct velocity-time graphs from position-time data and extract acceleration from the slope
3. Compare measured g with the accepted value using uncertainty analysis
4. Understand sources of systematic and random error in timing experiments

---

## Background

In free fall (ignoring air resistance), an object dropped from rest falls according to:

$$y(t) = \frac{1}{2}g t^2$$

We can extract g from this by measuring position as a function of time. Two approaches:

**Method A (position-time):** Fit y vs. t² to a straight line. The slope equals g/2, so g = 2×slope.

**Method B (velocity-time):** Compute average velocities over successive intervals, then fit v vs. t to a straight line. The slope equals g.

---

## Apparatus

- **Free-fall timer apparatus:** A solenoid releases a steel ball on command; a spark timer records marks on a paper tape at precisely known time intervals (every 1/60 s = 0.01667 s), OR a photogate-based system records times digitally
- Metric ruler (precision 0.5 mm)
- Paper tape (if spark timer) or laptop with data acquisition software
- Graph paper (for paper tape analysis)

---

## Part 1: Spark Timer Method (Paper Tape)

### 1.1 Procedure

1. Thread a fresh paper tape through the spark timer and attach it to the falling ball clamp.
2. Start the timer before releasing the ball. Release the ball cleanly (no initial push).
3. Catch the tape before it pulls out of the timer.
4. You should see a series of dots on the tape. Identify the first dot (taken as t = 0) and number subsequent dots 1, 2, 3, ...
5. Measure the position of each dot from dot 0 using the metric ruler. Record to the nearest 0.5 mm.

### 1.2 Data Table

Time interval Δt = 1/60 s = 0.01667 s

| Dot # | Time t (s) | Position y (m) | Avg. velocity over interval (m/s) |
|-------|-----------|----------------|----------------------------------|
| 0 | 0 | 0 | — |
| 1 | 0.01667 | | |
| 2 | 0.03333 | | |
| 3 | 0.05000 | | |
| ... | ... | ... | ... |

**Computing average velocity:** The average velocity between dots n and n+2 is a good approximation to the instantaneous velocity at dot n+1:

$$v_{n+1} \approx \frac{y_{n+2} - y_n}{2\Delta t}$$

(This is the "mid-point velocity" formula — more accurate than using adjacent dots because it samples over a larger interval, reducing the relative error from position measurement uncertainty.)

### 1.3 Analysis — Method A (y vs. t²)

1. Plot y (vertical axis) vs. t² (horizontal axis) on graph paper or in a spreadsheet.
2. Fit a straight line through the origin (since y = 0 at t = 0 by definition).
3. Read off the slope m. Then g = 2m.
4. Calculate the uncertainty in the slope (ask your TA for the linear regression uncertainty formula, or use your spreadsheet's LINEST function).
5. Report g ± σ_g.

### 1.4 Analysis — Method B (v vs. t)

1. Plot the average velocities computed above vs. the corresponding times.
2. Fit a straight line. The slope is g.
3. Report g ± σ_g.
4. Compare your Method A and Method B values. Do they agree within their uncertainties?

---

## Part 2: Photogate Method (if available)

### 2.1 Procedure

1. Set up two photogates at precisely measured heights below the drop point. Record the heights y₁ and y₂.
2. Drop the ball from rest. Record the times at which the ball passes each gate: t₁ and t₂.
3. Using g = 2(y₂ − y₁)/(t₂² − t₁²), compute g. (Derive this formula from x = ½gt² before the lab starts — it will be checked.)
4. Repeat 10 times. Compute mean, standard deviation, standard error.

---

## Part 3: Systematic Error Investigation

Respond to the following in your report (no calculation required — qualitative reasoning):

1. **Air resistance:** How would air resistance affect your measured value of g? Would it make g appear larger or smaller than 9.81 m/s²? Explain.

2. **Initial velocity:** If the ball was accidentally given a slight downward push at release (v₀ > 0), and your analysis assumed v₀ = 0, would your fitted slope overestimate or underestimate g? [Hint: think about what the y vs. t² plot looks like for y = v₀t + ½gt².]

3. **Spark timer calibration:** If the spark timer fires at 59.8 Hz instead of the labeled 60.0 Hz, in what direction would this shift your measured g?

---

## Part 4: Comparison and Discussion

1. Report your final values of g from both methods with uncertainties:
   - g_A = ___ ± ___ m/s² (Method A)
   - g_B = ___ ± ___ m/s² (Method B)
2. The accepted value is g_accepted = 9.81 m/s². Calculate the **percent discrepancy**:
   $$\%\text{ discrepancy} = \frac{|g_{measured} - g_{accepted}|}{g_{accepted}} \times 100\%$$
3. Is the accepted value within your measurement uncertainty? (i.e., does the interval [g_measured − σ, g_measured + σ] contain 9.81?)
4. Identify and rank the three largest sources of error in your experiment.

---

## Lab Report Requirements

Submit within **one week** of the lab session.

| Component | Points |
|-----------|--------|
| Data table, clearly formatted with units and sig figs | 15 |
| y vs. t² plot with linear fit, labeled axes, units | 15 |
| v vs. t plot with linear fit, labeled axes, units | 15 |
| Correct g extraction from both methods | 20 |
| Uncertainty propagation for g | 15 |
| Part 3 systematic error discussion (qualitative reasoning) | 10 |
| Comparison with accepted value + discussion | 10 |
| **Total** | **100** |

---

## Pre-Lab Questions (Due at Start of Lab)

Answer these before arriving. Your TA will check them at the start of the session.

**Q1.** Starting from y = ½gt², derive algebraically that a plot of y vs. t² has slope equal to g/2.

**Q2.** What is the unit of the slope of a y vs. t² graph (where y is in meters and t² is in s²)? Verify this gives the right units for g.

**Q3.** If you measure positions with precision δy = ±1 mm and time intervals with negligible uncertainty, derive the uncertainty in the average velocity σ_v = σ_Δy/(2Δt). For Δt = 3 × (1/60 s), what numerical uncertainty does this give in m/s?
