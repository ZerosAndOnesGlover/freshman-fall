# PHYS 141 · Lab 10 Solutions
## The Speed of Sound and Resonance in Air Columns
## INSTRUCTOR ONLY

---

## Pre-Lab Answers

**Q1.** 512 Hz at $v = 343$ m/s: $\lambda = \mathbf{0.670~\text{m}}$; first resonance at
$\lambda/4 = \mathbf{0.167~\text{m}}$ (less the end correction); successive resonances
$\lambda/2 = \mathbf{0.335~\text{m}}$ apart.

**Q2.** The water surface is a rigid boundary — air cannot move through it — so it is a **displacement
node**. The open top is a **displacement antinode**. That combination defines a closed–open pipe, with
resonances at odd multiples of $\lambda/4$.

**Q3.** $\Delta\beta = 10\log_{10}\left(\dfrac{I/4}{I}\right) = 10\log_{10}(0.25) = \mathbf{-6.02~\text{dB}}$.

**Q4.** 1500 Hz swung at 6.00 m/s: $f_{\max} = 1500\dfrac{343}{343-6} = \mathbf{1527~\text{Hz}}$;
$f_{\min} = 1500\dfrac{343}{343+6} = \mathbf{1474~\text{Hz}}$. Spread $\approx52$ Hz — comfortably
resolvable on a phone spectrum app.

---

## Part 1 — Speed of Sound by Resonance Tube *(35 pts)*

**Expected data** at $v \approx 343$ m/s (room temperature ~20°C):

| Fork (Hz) | $\lambda$ (m) | $L_1 \approx \lambda/4$ | $L_2 \approx 3\lambda/4$ | Spacing $\lambda/2$ |
|---|---|---|---|---|
| 256 | 1.340 | 0.335 | 1.005 | 0.670 |
| 384 | 0.893 | 0.223 | 0.670 | 0.447 |
| 512 | 0.670 | 0.167 | 0.502 | 0.335 |

*Measured $L_1$ values will fall short by the end correction (~5–10 mm); the spacings will not.*

**Analysis answers.**

1. Water at the bottom is a rigid boundary ⟹ displacement **node**; the open top ⟹ displacement
   **antinode**. That forces an odd number of quarter-wavelengths. *(5 pts)*
2. Consecutive odd multiples of $\lambda/4$ differ by $2\times\lambda/4 = \lambda/2$. *(4 pts)*
3. All three forks should give $v$ within about 1–2% of each other. *(8 pts)*
4. Compare with $331\sqrt{1+T_C/273.15}$ at the measured temperature. Agreement within 1–2% is a good
   result. *(8 pts)*
5. **The end correction.** $L_1$ is systematically short by $e \approx 0.6r$, so using $L_1$ alone
   underestimates $\lambda$ and hence $v$. **The correction is the same at every resonance, so it
   cancels in the difference $L_2 - L_1$.** *(5 pts)*
6. Dominant uncertainty is in locating the resonance by ear — typically $\pm2$–5 mm, giving about
   1% in $v$. *(5 pts)*

> **Question 5 is the point of the whole experiment.** A student who computes $v$ from $4fL_1$ will
> get roughly 335 m/s instead of 343 — low by about 2%, and consistently so. That systematic offset
> *is* the end correction, and spotting it is worth more than getting 343 by luck.

---

## Part 2 — The End Correction *(15 pts)*

1. $e = \lambda/4 - L_1$ for each fork. *(6 pts)*
2. **$e$ should be the same for all three frequencies**, because it depends on the tube's geometry,
   not on the wavelength. Consistency here is a good check that the measurements are sound. *(4 pts)*
3. Compare with $0.6r$. For a tube of radius 12–15 mm this predicts 7–9 mm, and student values
   typically land in that range. *(5 pts)*

*If a student's $e$ varies strongly with frequency, suspect that they misidentified which resonance
they found — for example recording $3\lambda/4$ as the first.*

---

## Part 3 — Inverse Square Law and Decibels *(30 pts)*

1. $I$ against $1/r^2$: linear through the origin. *(8 pts)*
2. Slope $= P/4\pi$, so $P = 4\pi\times\text{slope}$. *(6 pts)*
3. $\beta = 10\log_{10}\left(\dfrac{P}{4\pi I_0}\right) - 20\log_{10}r$, so the slope against
   $\log_{10}r$ is **$-20$ dB per decade**. *(8 pts)*
4. Any two points a factor of two apart in $r$ should differ by about 6 dB. *(4 pts)*
5. **Reflections make the measured fall-off shallower than $-20$ dB/decade.** Sound reaching the meter
   by reflection off floor, walls and ceiling has travelled further than the direct path, so it adds
   proportionally more at large $r$ than at small $r$, partially filling in the expected decrease. In
   an ordinary room the measured slope is commonly $-15$ dB/decade or shallower. *(4 pts)*

> Encourage measuring outdoors or in the largest available space. A "failure" to see inverse-square
> indoors is a real result about the room, not an experimental error, and should be credited as such
> when correctly explained.

---

## Lab Report Marking Summary

| Component | Points | Watch for |
|-----------|--------|-----------|
| Part 1 | 35 | Spacing used rather than $L_1$; temperature comparison made |
| Part 2 | 15 | $e$ consistent across frequencies; compared with $0.6r$ |
| Part 3 | 30 | $-20$ dB/decade derived; reflections explained if slope is shallow |
| **Total** | **80** | |

**Common errors to look for:**

1. **Computing $v = 4fL_1$** and ignoring the end correction — gives about 335 m/s. The
   *consistency* of the shortfall is the diagnostic.
2. **Missing the first resonance** because it is faint, then treating $3\lambda/4$ as $\lambda/4$.
   This trebles the apparent wavelength and gives a wildly wrong $v$.
3. **Not recording the temperature**, leaving no basis for the comparison in Part 1(4).
4. **Applying one end correction to an open–open pipe.** There are two open ends and therefore two
   corrections — relevant to PS 10 Problem 15 rather than this lab, but the same misconception.
5. **Expecting a clean inverse-square law indoors.** Reflections guarantee otherwise; the correct
   response is to explain the discrepancy, not to discard the data.
