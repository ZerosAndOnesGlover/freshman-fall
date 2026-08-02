# PHYS 141 — Lab 8
## The Simple Pendulum and Simple Harmonic Motion

**Duration:** 3 hours | **Total: 100 points**

---

## Objectives

1. Measure the period of a simple pendulum as a function of length and determine $g$
2. Test experimentally whether the period depends on amplitude, and find where the small-angle approximation fails
3. Test whether the period depends on the mass of the bob
4. Measure the spring constant of a spring two independent ways and compare
5. Observe damping and estimate a decay constant

---

## Apparatus

String, assorted bobs (brass, aluminium, plastic — similar size, different mass), metre rule,
protractor, stopwatch or photogate timer, retort stand and clamp, spring, slotted mass set,
motion sensor (if available).

---

## Part 1 — Period versus Length (30 min, 25 pts)

**Procedure.** For each of six lengths from 0.20 m to 1.20 m, time **20 complete oscillations** and
divide by 20. Keep the amplitude below $10°$ throughout. Repeat each measurement three times.

> **Why 20 oscillations?** Your reaction time (~0.2 s) contributes the same absolute error whether
> you time 1 swing or 20, so timing 20 divides that error by 20. This is the single most effective
> uncertainty-reduction technique in the lab, and it costs nothing.

**Measure $L$ from the pivot to the *centre* of the bob**, not to its top. This is the commonest
systematic error in this experiment.

| $L$ (m) | $t_{20}$ trial 1 | trial 2 | trial 3 | mean $t_{20}$ | $T$ (s) | $T^2$ (s²) |
|---|---|---|---|---|---|---|
| 0.20 | | | | | | |
| 0.40 | | | | | | |
| 0.60 | | | | | | |
| 0.80 | | | | | | |
| 1.00 | | | | | | |
| 1.20 | | | | | | |

**Analysis.**

1. From $T = 2\pi\sqrt{L/g}$, show that $T^2 = (4\pi^2/g)L$. *(3 pts)*
2. Plot $T^2$ against $L$ with error bars. It should be a straight line through the origin. *(6 pts)*
3. Extract the slope with its uncertainty, and compute $g = 4\pi^2/\text{slope}$. *(8 pts)*
4. Compare with the accepted $9.81$ m/s². Compute the percent discrepancy. *(4 pts)*
5. Does your line pass through the origin within uncertainty? If not, what systematic error would
   produce a non-zero intercept? *(4 pts)*

---

## Part 2 — Period versus Amplitude (30 min, 20 pts)

**Procedure.** Fix $L = 1.00$ m. Measure the period at initial amplitudes of $5°$, $10°$, $15°$,
$20°$, $30°$, and $45°$, timing 20 oscillations each.

| $\theta_0$ | $t_{20}$ (s) | $T$ (s) | $T/T_{5°}$ | Predicted excess |
|---|---|---|---|---|
| 5° | | | 1.000 | — |
| 10° | | | | 0.4% |
| 15° | | | | 1.1% |
| 20° | | | | 2.1% |
| 30° | | | | 4.7% |
| 45° | | | | — |

**Analysis.**

1. Does $T$ increase or decrease with amplitude? *(3 pts)*
2. Up to what amplitude is $T$ constant **within your experimental uncertainty**? *(5 pts)*
3. Compare your measured excess at $30°$ with the predicted 4.7%. *(6 pts)*
4. Explain physically why a real pendulum swings **slower** at large amplitude. *(6 pts)*

> *Hint for 4:* compare $\sin\theta$ with $\theta$. Which is larger, and what does that say about the
> actual restoring force compared with the linear approximation?

---

## Part 3 — Period versus Mass (20 min, 10 pts)

**Procedure.** Fix $L = 1.00$ m and $\theta_0 < 10°$. Measure $T$ for three bobs of markedly
different mass but similar size.

| Bob | Mass (kg) | $t_{20}$ (s) | $T$ (s) |
|---|---|---|---|
| | | | |

**Analysis.**

1. Is $T$ independent of mass within uncertainty? *(4 pts)*
2. Explain why, using Newton's second law applied to the pendulum. *(4 pts)*
3. Why is it important that the bobs be of **similar size**? *(2 pts)*

---

## Part 4 — Spring Constant, Two Ways (40 min, 25 pts)

**Method A — static.** Hang masses from the spring and measure the extension for each.
Plot $F = mg$ against extension $x$; the slope is $k$.

| $m$ (kg) | $F$ (N) | $x$ (m) |
|---|---|---|
| | | |

**Method B — dynamic.** For each of three masses, set the spring oscillating vertically with small
amplitude and time 20 oscillations. From $T = 2\pi\sqrt{m/k}$, extract $k$.

| $m$ (kg) | $t_{20}$ (s) | $T$ (s) | $k$ (N/m) |
|---|---|---|---|
| | | | |

**Analysis.**

1. Report $k$ from each method with uncertainties. *(8 pts)*
2. Do they agree within uncertainty? *(4 pts)*
3. Plot $T^2$ against $m$ for Method B. Should it pass through the origin? Does it? *(6 pts)*
4. The spring itself has mass. Explain qualitatively how this affects the dynamic result, and which
   of the two methods it biases. *(7 pts)*

---

## Part 5 — Damping (20 min, 20 pts)

**Procedure.** Set the spring–mass system oscillating with an initial amplitude of about 10 cm.
Record the amplitude every 5 oscillations until it has fallen below a quarter of its start.

| Oscillation $n$ | Time (s) | Amplitude (m) |
|---|---|---|
| 0 | 0 | |
| 5 | | |
| 10 | | |
| … | | |

**Analysis.**

1. Plot $\ln A$ against $t$. If the damping is viscous ($F = -bv$), this should be a straight line.
   Is it? *(6 pts)*
2. Extract $\gamma$ from the slope, and hence $b = 2m\gamma$. *(6 pts)*
3. Compute $Q = \omega_0/2\gamma$ and state how many oscillations occur before the amplitude falls to
   $1/e$. *(4 pts)*
4. Is this system under-, critically, or overdamped? Justify by comparing $b$ with $2\sqrt{mk}$. *(4 pts)*

---

## Lab Report Requirements

| Component | Points |
|-----------|--------|
| Part 1: data table, $T^2$ vs $L$ plot with error bars, $g$ with uncertainty | 25 |
| Part 2: amplitude data, comparison with predicted excess, physical explanation | 20 |
| Part 3: mass independence demonstrated and explained | 10 |
| Part 4: $k$ by both methods with uncertainties, agreement assessed | 25 |
| Part 5: log plot, $\gamma$ and $Q$ extracted, damping regime identified | 20 |
| **Total** | **100** |

---

## Pre-Lab Questions (Due at Start of Lab)

**Q1.** Starting from $T = 2\pi\sqrt{L/g}$, show that a plot of $T^2$ against $L$ is linear and state
the slope in terms of $g$.

**Q2.** You time 20 oscillations with a stopwatch you can read to $\pm0.2$ s. What is the resulting
uncertainty in a single period? What would it be if you timed only one oscillation?

**Q3.** Predict, before measuring: will the period at $45°$ be larger or smaller than at $5°$?
Justify from the relationship between $\sin\theta$ and $\theta$.

**Q4.** For a 1.00 m pendulum, compute the expected period. Then compute the expected period of a
uniform rod of the same length pivoted at one end, and state which swings faster.
