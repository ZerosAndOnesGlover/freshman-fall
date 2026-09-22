# PHYS 141 · Lab 9
## Standing Waves on a String

**Duration:** 3 hours | **Total: 100 points**
**Lab session:** Thursday 26 November 2026, 14:00–17:00 · Week 9 — the lab meets Thursday, after that week's Mon/Tue lectures.

---

> **Line fits:** use the formulas in the *Fitting a Straight Line* box in Lab 1 (slope, intercept and
> their uncertainties), or `LINEST`, which gives the same numbers.

## Objectives

1. Produce standing waves on a driven string and identify the resonant frequencies
2. Verify $f_n = nf_1$ and measure the wave speed two independent ways
3. Test $v = \sqrt{F_T/\mu}$ by varying the tension
4. Measure $\mu$ from the wave data and compare with a direct weighing
5. Observe beats and use them to match two frequencies

---

## Apparatus

String or elastic cord, mechanical vibrator driven by a function generator, pulley and slotted mass
hanger, metre rule, digital balance, two tuning forks of nearly equal frequency (or two function
generators with speakers), oscilloscope or phone spectrum app.

---

## Part 1 — Finding the Harmonics (45 min, 30 pts)

**Setup.** Clamp one end of the string to the vibrator, run the other over the pulley to a hanging
mass. Keep the vibrating length $L$ fixed at about 1.0 m and record it precisely.

**Procedure.** With a fixed hanging mass, sweep the generator frequency slowly upward from a few Hz.
Record every frequency at which a clear standing wave appears, and count the antinodes.

| $n$ (antinodes) | $f_n$ (Hz) | $\lambda_n = 2L/n$ (m) | $f_n/n$ (Hz) |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

**Analysis.**

1. Is $f_n/n$ constant across all five rows? It should equal $f_1$. Report the mean and spread. *(6 pts)*
2. Plot $f_n$ against $n$. Confirm a straight line through the origin and extract the slope. *(8 pts)*
3. **Method A:** compute $v$ from the slope, using $f_n = nv/2L$. *(6 pts)*
4. **Method B:** compute $v = \sqrt{F_T/\mu}$ from the hanging mass and a directly weighed $\mu$. *(6 pts)*
5. Compare the two values of $v$ and comment on the agreement. *(4 pts)*

> **The resonances are sharp.** If you sweep too fast you will miss them. Turn the frequency slowly
> and watch for the amplitude to grow suddenly — that growth *is* the resonance building, exactly as
> Week 8 described.

---

## Part 2 — Speed versus Tension (45 min, 30 pts)

**Procedure.** Fix $L$ and drive the string at its **fundamental** each time. For six different
hanging masses, record the fundamental frequency.

| $m$ (kg) | $F_T = mg$ (N) | $f_1$ (Hz) | $v = 2Lf_1$ (m/s) | $v^2$ (m²/s²) |
|---|---|---|---|---|
| | | | | |

**Analysis.**

1. From $v = \sqrt{F_T/\mu}$, show that $v^2 = F_T/\mu$, so a plot of $v^2$ against $F_T$ is linear
   through the origin with slope $1/\mu$. *(5 pts)*
2. Plot $v^2$ against $F_T$ with error bars. *(8 pts)*
3. Extract $\mu$ from the slope, with uncertainty. *(8 pts)*
4. Weigh a measured length of the string directly to obtain $\mu$. Compare. *(5 pts)*
5. Does your line pass through the origin within uncertainty? If not, suggest a systematic cause. *(4 pts)*

> *For question 5:* the hanging mass is not the only tension contribution — the string over the pulley
> has weight, and the pulley has friction. Consider which would shift the intercept and in which
> direction.

---

## Part 3 — Beats (30 min, 20 pts)

**Procedure.** Sound two nearly-equal tuning forks (or two speakers a few Hz apart) together. Count
the beats over 30 s and divide.

| Trial | Beats counted in 30 s | $f_{\text{beat}}$ (Hz) |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |

Then load one fork with a small mass of plasticine (lowering its frequency slightly) and repeat.

**Analysis.**

1. From the measured beat frequency and the known frequency of one fork, give **both** possible
   frequencies for the other. *(5 pts)*
2. Use the loading experiment to decide which is correct, and explain your reasoning. *(6 pts)*
3. Record both signals on an oscilloscope or spectrum app. Identify the envelope and measure its
   period. Confirm that the audible beat rate is **twice** the envelope frequency, and explain why. *(6 pts)*
4. A trained ear can detect beats down to about 0.5 Hz. What fractional frequency difference does
   that represent at 440 Hz, and why is this a more sensitive method than comparing pitches directly? *(3 pts)*

---

## Part 4 — Standing Wave Shape (20 min, 20 pts)

**Procedure.** Drive the string in its third harmonic. Using a metre rule, locate every node and
antinode along the string.

| Feature | Predicted position (m) | Measured (m) |
|---|---|---|
| Node 1 | 0 | |
| Antinode 1 | $L/6$ | |
| Node 2 | $L/3$ | |
| Antinode 2 | $L/2$ | |
| Node 3 | $2L/3$ | |
| Antinode 3 | $5L/6$ | |
| Node 4 | $L$ | |

**Analysis.**

1. Compare measured with predicted positions. *(6 pts)*
2. Measure the distance between adjacent nodes and confirm it equals $\lambda/2$. *(6 pts)*
3. Hold a finger lightly at an **antinode** — the pattern collapses. Touch a **node** — it survives.
   Explain both observations. *(8 pts)*

---

## Lab Report Requirements

| Component | Points |
|-----------|--------|
| Part 1: harmonic table, $f_n$ vs $n$ plot, $v$ by both methods, comparison | 30 |
| Part 2: $v^2$ vs $F_T$ plot with error bars, $\mu$ extracted and compared with weighing | 30 |
| Part 3: beat measurements, ambiguity resolved by loading, envelope explanation | 20 |
| Part 4: node/antinode positions, node spacing, finger-damping explanation | 20 |
| **Total** | **100** |

---

## Pre-Lab Questions (Due at Start of Lab)

**Q1.** For a string fixed at both ends with $L = 1.00$ m and $v = 120$ m/s, compute $f_1$ through
$f_5$.

**Q2.** Show that $v^2 = F_T/\mu$, and state what the slope of a $v^2$-versus-$F_T$ graph gives.

**Q3.** Two forks give 6 beats per second and one is 440 Hz. What are the two candidates for the
other? How would loading one fork with plasticine resolve the ambiguity?

**Q4.** Predict what happens if you touch the string lightly at its **midpoint** while it vibrates in
(a) its fundamental, and (b) its second harmonic. Justify each answer from where the nodes are.
