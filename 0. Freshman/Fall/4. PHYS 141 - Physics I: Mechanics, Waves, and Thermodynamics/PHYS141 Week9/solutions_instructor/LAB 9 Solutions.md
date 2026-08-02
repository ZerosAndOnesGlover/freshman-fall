# PHYS 141 — Lab 9 Solutions
## Standing Waves on a String
## INSTRUCTOR ONLY

---

## Pre-Lab Answers

**Q1.** $L = 1.00$ m, $v = 120$ m/s: $f_n = nv/2L = 60n$ Hz.

| $n$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $f_n$ (Hz) | **60.0** | 120 | 180 | 240 | 300 |

**Q2.** Squaring $v = \sqrt{F_T/\mu}$ gives $v^2 = F_T/\mu$. A plot of $v^2$ against $F_T$ is linear
through the origin with **slope $1/\mu$**.

**Q3.** $440 \pm 6$ gives **434 Hz or 446 Hz**. Loading a fork with plasticine lowers its frequency:
if the beat rate **increases**, the fork was at 434 Hz (moving further away); if it **decreases**, it
was at 446 Hz (moving towards 440).

**Q4.** **(a) Fundamental** — the midpoint is an **antinode**, the point of maximum motion. Touching
it forces zero displacement where the mode demands maximum, so the fundamental is **killed**.
**(b) Second harmonic** — the midpoint is a **node**, already stationary. Touching it changes nothing
and the mode **survives**.

*This is the basis of playing natural harmonics on a guitar or violin, and it makes an excellent live
demonstration.*

---

## Part 1 — Finding the Harmonics *(30 pts)*

**Expected behaviour.** With $L\approx1.0$ m and a typical elastic cord under a few newtons, $f_1$
lands somewhere between 10 and 40 Hz, with harmonics at exact integer multiples.

1. **$f_n/n$ should be constant** across all five rows, equal to $f_1$. A spread of more than a few
   percent indicates miscounted antinodes — check whether a student recorded $n=2$ as $n=1$. *(6 pts)*
2. Plot of $f_n$ against $n$: straight line through the origin, slope $= f_1 = v/2L$. *(8 pts)*
3. **Method A:** $v = 2L \times \text{slope}$. *(6 pts)*
4. **Method B:** $v = \sqrt{F_T/\mu}$ with $F_T = mg$ and $\mu$ from weighing. *(6 pts)*
5. Agreement to within about 5% is typical and good. *(4 pts)*

> **Why the two may disagree slightly.** Method B assumes the tension equals $mg$ exactly, but pulley
> friction and the weight of the string between pulley and vibrator both perturb it. Method A is
> generally the more reliable of the two.

---

## Part 2 — Speed versus Tension *(30 pts)*

1. $v^2 = F_T/\mu$; linear through the origin, **slope $= 1/\mu$**. *(5 pts)*
2. Plot with error bars; $\delta(v^2) = 2v\,\delta v$. *(8 pts)*
3. $\mu = 1/\text{slope}$, with uncertainty from the fit. *(8 pts)*
4. Direct weighing: measure a 2 m length on a balance reading to 0.01 g. Agreement within 5–10% is
   normal. *(5 pts)*
5. **A non-zero intercept is expected and diagnostic.** *(4 pts)*

> **Systematic causes of an intercept**, worth crediting generously if identified:
> - The string's own weight between the pulley and the vibrator adds to the tension, so the true
>   $F_T$ slightly exceeds $mg$ — shifting the line **left**, giving a positive $v^2$ intercept.
> - Pulley friction means the tension on the vibrating side differs from $mg$.
> - The vibrator end is not perfectly fixed; it moves slightly, so $L$ is marginally longer than
>   measured.

---

## Part 3 — Beats *(20 pts)*

1. Both candidates $f \pm f_{\text{beat}}$ must be given. *(5 pts)*
2. Loading lowers the frequency of the loaded fork; watch whether the beats speed up or slow down.
   Full marks require the reasoning, not just the answer. *(6 pts)*
3. **The envelope frequency is $\lvert f_1-f_2\rvert/2$, but the audible beat rate is
   $\lvert f_1-f_2\rvert$** — because loudness depends on the envelope's *magnitude*, which peaks at
   both the positive and negative extremes of each envelope cycle. On the oscilloscope the envelope
   period is twice the interval between loudness maxima. *(6 pts)*
4. At 440 Hz, a 0.5 Hz beat is a fractional difference of $0.5/440 = \mathbf{0.11\%}$ — about two
   cents, far finer than most people can judge by comparing pitches directly. **Counting a slow
   rhythm is much easier than judging a small pitch interval**, which is why the method works. *(3 pts)*

---

## Part 4 — Standing Wave Shape *(20 pts)*

For $L = 1.00$ m in the third harmonic ($\lambda = 2L/3 = 0.667$ m):

| Feature | Position (m) |
|---|---|
| Node 1 | 0 |
| Antinode 1 | 0.167 |
| Node 2 | 0.333 |
| Antinode 2 | 0.500 |
| Node 3 | 0.667 |
| Antinode 3 | 0.833 |
| Node 4 | 1.000 |

1. Measured positions should match to within a centimetre or two. *(6 pts)*
2. **Node spacing $= \lambda/2 = 0.333$ m** for this case — verify against the measured wavelength. *(6 pts)*
3. **The explanation is the key part.** *(8 pts)*
   - Touching an **antinode** imposes zero displacement at a point the mode requires to move
     maximally. The boundary condition is incompatible with the mode, and the pattern **collapses**.
   - Touching a **node** imposes zero displacement where the string is already stationary. The mode
     already satisfies that condition, so nothing changes and the pattern **survives**.
   - This is exactly how a guitarist plays natural harmonics: touch the string lightly at $L/2$ and
     the fundamental dies while the second harmonic — which has a node there — continues, sounding an
     octave higher.

---

## Lab Report Marking Summary

| Component | Points | Watch for |
|-----------|--------|-----------|
| Part 1 | 30 | $f_n/n$ constancy; both methods for $v$ compared |
| Part 2 | 30 | Slope interpreted as $1/\mu$; intercept explained, not ignored |
| Part 3 | 20 | Ambiguity genuinely resolved by loading; factor-of-two understood |
| Part 4 | 20 | Node/antinode damping explained via boundary conditions |
| **Total** | **100** | |

**Common errors to look for:**

1. **Miscounting harmonics.** Recording the $n=2$ pattern as the fundamental shifts every subsequent
   number and makes $f_n/n$ inconsistent. The $f_n/n$ column is designed to expose this.
2. **Sweeping the frequency too quickly** and missing resonances entirely, especially $n=1$, which is
   the weakest and easiest to overlook.
3. **Using $m$ rather than $\mu$** in $v = \sqrt{F_T/\mu}$ — a dimensional error that produces wildly
   wrong speeds.
4. **Forgetting $g$** when converting the hanging mass to tension.
5. **Measuring $L$ to the pulley** rather than to the vibrating end. The vibrating length is what
   determines the harmonics.
