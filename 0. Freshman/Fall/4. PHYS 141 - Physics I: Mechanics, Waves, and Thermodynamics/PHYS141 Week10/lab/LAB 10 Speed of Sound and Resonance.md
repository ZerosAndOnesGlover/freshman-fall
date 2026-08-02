# PHYS 141 — Lab 10
## The Speed of Sound and Resonance in Air Columns

**Duration:** 3 hours | **Total: 100 points**

---

## Objectives

1. Measure the speed of sound using a resonance tube, and correct for the end effect
2. Verify that successive resonances are spaced by $\lambda/2$
3. Determine the end correction and compare it with $0.6r$
4. Verify the inverse-square law and the decibel scale with a sound level meter
5. Observe the Doppler effect and measure the shift

---

## Apparatus

Resonance tube with adjustable water level (or a sliding plunger), tuning forks of several
frequencies (256, 384, 512 Hz), metre rule, thermometer, sound level meter or phone app with
calibration, function generator and speaker, small speaker on a string or rotating arm, phone
spectrum analyser app.

---

## Part 1 — Speed of Sound by Resonance Tube (60 min, 35 pts)

**Procedure.** For each tuning fork, strike it and hold it over the tube while slowly lowering the
water level. Record every air-column length at which the sound is loudest. Find at least **two**
resonances per fork; three if the tube is long enough.

**Record the air temperature** at the start and end of the experiment.

| Fork $f$ (Hz) | $L_1$ (m) | $L_2$ (m) | $L_3$ (m) | $L_2-L_1$ (m) | $\lambda = 2(L_2-L_1)$ | $v = f\lambda$ (m/s) |
|---|---|---|---|---|---|---|
| 256 | | | | | | |
| 384 | | | | | | |
| 512 | | | | | | |

**Analysis.**

1. Explain why the resonance tube is a **closed–open** pipe, and why resonances occur at
   $\lambda/4$, $3\lambda/4$, $5\lambda/4$, … *(5 pts)*
2. Show that successive resonances are separated by $\lambda/2$. *(4 pts)*
3. Compute $v$ for each fork. Are the three values consistent? *(8 pts)*
4. Compute the expected $v$ from your measured temperature using $v = 331\sqrt{1+T_C/273.15}$.
   Compare with your mean measured value and give a percent discrepancy. *(8 pts)*
5. **Why does using the spacing $L_2-L_1$ give a better result than using $L_1$ alone?** *(5 pts)*
6. Estimate your uncertainty in $v$ and state whether your discrepancy in (4) is significant. *(5 pts)*

> **The whole design of this experiment is in question 5.** Using $L_1 = \lambda/4$ directly is
> contaminated by the end correction. Taking a *difference* cancels it, because the correction is the
> same at both resonances.

---

## Part 2 — The End Correction (30 min, 15 pts)

**Procedure.** Measure the internal radius $r$ of the tube.

**Analysis.**

1. From your $\lambda$ and your measured $L_1$, compute the end correction
   $e = \lambda/4 - L_1$ for each fork. *(6 pts)*
2. Is $e$ consistent across the three frequencies? Should it be? *(4 pts)*
3. Compare your mean $e$ with the theoretical $0.6r$. *(5 pts)*

---

## Part 3 — Inverse Square Law and Decibels (45 min, 30 pts)

**Procedure.** Drive a speaker with a steady 1.00 kHz tone in as open a space as possible. Measure
the sound level at distances from 0.50 m to 4.00 m.

| $r$ (m) | $\beta$ (dB) | $I = I_0 10^{\beta/10}$ (W/m²) | $1/r^2$ (m⁻²) |
|---|---|---|---|
| 0.50 | | | |
| 0.75 | | | |
| 1.00 | | | |
| 1.50 | | | |
| 2.00 | | | |
| 3.00 | | | |
| 4.00 | | | |

**Analysis.**

1. Plot $I$ against $1/r^2$. It should be linear through the origin. *(8 pts)*
2. Extract the source power from the slope, using $I = P/4\pi r^2$. *(6 pts)*
3. Plot $\beta$ against $\log_{10}r$. Show that theory predicts a slope of $-20$ dB per decade, and
   compare with your measurement. *(8 pts)*
4. Verify the "6 dB per doubling of distance" rule directly from your data, using at least two
   independent pairs of points. *(4 pts)*
5. Room reflections make the real fall-off **less** steep than inverse-square. Does your data show
   this? Explain why reflections have that effect. *(4 pts)*

---

## Part 4 — The Doppler Effect (30 min, 20 pts)

**Procedure.** Attach a small speaker emitting a steady tone (1–2 kHz) to a string and swing it in a
horizontal circle, or mount it on a rotating arm. Record the sound with a phone spectrum analyser
from a few metres away, in the plane of the circle.

**Analysis.**

1. From your recording, identify the maximum and minimum received frequencies, $f_{\max}$ and
   $f_{\min}$. *(5 pts)*
2. Using $f_{\max} = f\dfrac{v}{v-v_s}$ and $f_{\min} = f\dfrac{v}{v+v_s}$, solve for **both** the
   emitted frequency $f$ and the source speed $v_s$. *(8 pts)*
3. Measure the radius and period of the circular motion, compute $v_s = 2\pi R/T$ independently, and
   compare. *(4 pts)*
4. At which points in the circle does the listener hear $f_{\max}$, $f_{\min}$, and the unshifted
   $f$? Explain in terms of the component of velocity along the line of sight. *(3 pts)*

> **Question 4 is the conceptual heart of the part.** The Doppler shift depends only on the velocity
> component *towards the listener*, so the unshifted frequency is heard when the speaker is moving
> **across** the line of sight, not when it is nearest or furthest.

---

## Lab Report Requirements

| Component | Points |
|-----------|--------|
| Part 1: resonance data, $v$ for three forks, comparison with temperature prediction | 35 |
| Part 2: end correction extracted and compared with $0.6r$ | 15 |
| Part 3: $I$ vs $1/r^2$ plot, source power, dB-vs-log-distance slope, 6 dB rule | 30 |
| Part 4: Doppler extremes, $f$ and $v_s$ extracted, independent check | 20 |
| **Total** | **100** |

---

## Pre-Lab Questions (Due at Start of Lab)

**Q1.** For a 512 Hz fork at $v = 343$ m/s, compute $\lambda$, the expected first resonance length,
and the spacing between successive resonances.

**Q2.** Explain why a resonance tube closed by water at the bottom is a closed–open pipe, and state
where the displacement node and antinode are.

**Q3.** Show algebraically that $\beta$ falls by $6.02$ dB when $r$ doubles.

**Q4.** A speaker emitting 1500 Hz is swung in a circle at 6.00 m/s. Compute $f_{\max}$ and
$f_{\min}$ heard by a distant listener in the plane of the circle.
