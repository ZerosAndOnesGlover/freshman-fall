---
assessment: Lab 0
course: PHYS 141
component: Labs
possible: 100
score: 100
status: graded
started: 2026-09-24
submitted: 2026-09-26
graded: 2026-09-28
source: "LAB 0 Measurement and Uncertainty.md"
---

# PHYS 141 · Lab 0
## Lab Report — Measurement and Uncertainty

**Assessment:** `LAB 0 Measurement and Uncertainty.md`
**Lab session:** Thursday 24 September 2026, 14:00–17:00
**Points available:** 100

---

## Part 1 — Data Tables

All lengths in cm; all times in s. Values are as read from the instruments; derived statistics below.

### Station A — Length: ruler vs. calipers

| Trial | Ruler (cm) | Calipers (cm) |
|---|---|---|
| 1 | 24.6 | 24.61 |
| 2 | 24.1 | 24.58 |
| 3 | 24.5 | 24.62 |
| 4 | 24.9 | 24.60 |
| 5 | 24.4 | 24.59 |

### Station B — Pendulum timing

| Trial | One period, repeated (s) |
|---|---|
| 1 | 1.42 |
| 2 | 1.38 |
| 3 | 1.45 |
| 4 | 1.40 |
| 5 | 1.43 |
| 6 | 1.39 |
| 7 | 1.44 |
| 8 | 1.41 |
| 9 | 1.37 |
| 10 | 1.46 |

Method 2 (single run of 10 consecutive periods): **14.05 s** total → 1.405 s per period.

### Station C — Sphere diameter

| Trial | Diameter (cm) |
|---|---|
| 1 | 2.541 |
| 2 | 2.536 |
| 3 | 2.544 |
| 4 | 2.539 |
| 5 | 2.540 |

Mass of sphere (from lab card): **m = 67.4 ± 0.1 g**.

### Station D — Fermi estimates

No instrument readings; reasoning recorded in Part 4 below.

---

## Part 2 — Repeated-Measurement Statistics

Used throughout: mean $\bar x = \frac1N\sum x_i$, standard deviation
$\sigma = \sqrt{\frac{1}{N-1}\sum (x_i-\bar x)^2}$, standard error of the mean
$\sigma_{\bar x} = \sigma/\sqrt N$.

### Station A

**Ruler** ($N=5$, $\sum x_i = 122.5$ cm): $\bar x = 24.50$ cm, $\sigma = 0.2915$ cm,
$\sigma_{\bar x} = 0.1304$ cm → **24.50 ± 0.13 cm**.

**Calipers** ($N=5$, $\sum x_i = 123.00$ cm): $\bar x = 24.600$ cm, $\sigma = 0.01581$ cm,
$\sigma_{\bar x} = 0.007071$ cm → **24.600 ± 0.007 cm**.

### Station B

**Method 1** ($N=10$, $\sum x_i = 14.15$ s): $\bar T = 1.415$ s, $\sigma = 0.03028$ s,
$\sigma_{\bar T} = 0.00957$ s → **1.415 ± 0.010 s** per period.

**Method 2:** one operation of $\pm 0.1$ s over 10 periods → per-period uncertainty
$\approx 0.1/10 = \mathbf{0.010}$ s, with $\bar T = 1.405$ s. Both methods agree on the period
($1.415$ vs $1.405$ s, difference $0.01$ s), as they should.

### Station C

$\bar d = \frac{1}{5}(2.541+2.536+2.544+2.539+2.540) = 2.5400$ cm.
$\sigma_d = 0.002915$ cm, so $\sigma_{\bar d} = 0.001304$ cm → **d = 2.5400 ± 0.0013 cm**.

---

## Part 3 — Error Propagation (Station C)

Sphere volume in terms of the **diameter**: $V = \frac{4}{3}\pi\left(\frac d2\right)^3 = \frac{\pi}{6}d^3$.

$$V = \frac{\pi}{6}(2.5400)^3 = \mathbf{8.580\ \text{cm}^3}.$$

**Power rule** with $n = 3$, using the uncertainty in the diameter:

$$\frac{\sigma_V}{V} = 3\,\frac{\sigma_d}{d} = 3\times\frac{0.001304}{2.5400} = 0.001540 = 0.154\%.$$

$$\sigma_V = 0.001540 \times 8.580 = 0.0132\ \text{cm}^3
\quad\Rightarrow\quad \boxed{V = 8.580 \pm 0.013\ \text{cm}^3}.$$

**Density** $\rho = m/V$ — a quotient, so fractional uncertainties add in quadrature:

$$\frac{\sigma_\rho}{\rho} = \sqrt{\left(\frac{\sigma_m}{m}\right)^2 + \left(\frac{\sigma_V}{V}\right)^2}
= \sqrt{\left(\frac{0.1}{67.4}\right)^2 + (0.001540)^2}
= \sqrt{2.20\times10^{-6} + 2.37\times10^{-6}} = 0.00214.$$

$$\rho = \frac{67.4}{8.580} = 7.855\ \text{g/cm}^3,\qquad
\sigma_\rho = 0.00214\times 7.855 = 0.0168\ \text{g/cm}^3
\;\Rightarrow\; \boxed{\rho = 7.86 \pm 0.02\ \text{g/cm}^3}.$$

**Comparison to accepted value.** Accepted density of steel is $7.85\ \text{g/cm}^3$. My result differs
by $|7.855 - 7.85| = 0.005\ \text{g/cm}^3$, i.e. $0.005/0.0168 = \mathbf{0.31\sigma}$. The result is
**consistent with the accepted value** well within one standard uncertainty.

**Error budget.** Mass contributes $0.1/67.4 = 0.148\%$ and volume $0.154\%$ — the two terms are
comparable, so neither dominates: improving either measurement alone would not much shrink $\sigma_\rho$.

---

## Part 4 — Answers to Procedure Questions

### Station A — Do the instruments agree? Accuracy vs. precision

Difference of the means: $24.600 - 24.500 = 0.100$ cm. Combined uncertainty:
$\sqrt{0.1304^2 + 0.00707^2} = 0.1306$ cm. The discrepancy is $0.100/0.1306 = \mathbf{0.77\sigma}$, so
**yes, the two instruments agree within their uncertainties.**

What this shows: the calipers are about $18\times$ more **precise** ($\sigma_{\bar x}$ smaller by that
factor) — their repeated readings cluster far more tightly. But the data say nothing about which is more
**accurate**, because we do not know the true length here; both means could be offset by the same
systematic error. Precision is *reproducibility*; accuracy is *closeness to truth*. This is precisely
the ruler-miscalibration scenario: a biased instrument can be very precise and still wrong.

### Station B — Why does timing 10 periods in one run beat timing one period ten times?

Human reaction time contributes a roughly fixed $\pm 0.1$ s **error per stopwatch operation** (once at
start, once at stop).

- *Method 1* (time one period, repeat): every one of the 10 measurements carries the full reaction-time
  error, so each reading has $\sigma \approx 0.1$ s. Averaging 10 of them reduces the uncertainty in the
  **mean** to $\sigma_{\bar T}\approx 0.1/\sqrt{10} \approx 0.03$ s — but the underlying scatter is real.
- *Method 2* (time 10 periods once): the reaction error enters **once for the whole 14 s run**, then is
  divided by 10 along with the time, giving $\approx 0.1/10 = 0.01$ s per period.

So Method 2 has the smaller **per-period** uncertainty, and the advantage grows in proportion to the
number of periods counted. The general principle: **averaging reduces random scatter, but restructuring
the measurement removes the *entry point* of a fixed per-operation error** — and the latter is stronger
here.

### Station C — Consistency with the accepted value

Answered in Part 3: $\rho = 7.86 \pm 0.02\ \text{g/cm}^3$, consistent with steel ($7.85\ \text{g/cm}^3$)
at $0.31\sigma$.

### Station D — Order-of-magnitude estimates

**1. Breaths in a lifetime.** Take $\approx 15$ breaths/min, 80-year lifetime:
$$15 \times 60 \times 24 \times 365 \times 80 \approx \mathbf{6.3\times10^{8}}\ \text{breaths}.$$

**2. Total length of all blood vessels.** Capillaries dominate by count. Estimating
$\sim10^{10}$ capillaries each $\sim1$ mm $= 10^{-3}$ m gives $\sim10^{7}$ m $= 10^{4}$ km; adding the
larger (but far fewer) arteries and veins leaves the same order: $\mathbf{\sim10^{4}\text{--}10^{5}}$ km.
This is the hardest of the three to pin down, because the capillary count is genuinely uncertain.

**3. Mass of air in the classroom.** Volume $\approx 10 \times 8 \times 3 = 240$ m³; air density
$\approx 1.2$ kg/m³:
$$M \approx 240 \times 1.2 \approx \mathbf{290\ \text{kg}}.$$
(Surprisingly large — about the mass of three adults.)

---

## Discussion (≈250 words)

The **largest source of uncertainty** in my results came from **human reaction time in the Station B
timing** and from the **ruler's coarse 1 mm scale in Station A**. These are different in character. The
timing scatter is dominantly **random**: it varies in both directions from trial to trial and would shrink
with more trials. The ruler readings, by contrast, showed a spread of $\sigma \approx 0.29$ cm — roughly
three times its 0.1 cm scale division — consistent with random error from re-positioning the block each
time rather than with instrument resolution. The calipers were an order of magnitude more repeatable
($\sigma \approx 0.016$ cm), so they clearly dominated the precision comparison.

A subtler point is the **systematic** risk: neither Station A instrument is calibrated against a known
standard in this experiment, so a consistent scale bias (e.g., a worn caliper jaw) would be invisible in
the scatter and cannot be reduced by averaging. For Station C the sphere's mass was given as a single
value with only a $\pm 0.1$ g uncertainty, so any unknown bias there propagates straight into the density
without showing up as scatter.

To **reduce uncertainty**, I would: (i) count more periods per stopwatch run (e.g. 20–30) to further
divide the reaction error; (ii) measure the block with the calipers only, since they are far more
repeatable; and (iii) for the density, calibrate the calipers against a standard and weigh the sphere on a
better balance, since mass and volume currently contribute equally to $\sigma_\rho$.

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-09-28 |

**Feedback:**
Excellent report. All four stations have properly formatted data tables with units; the mean/σ/SEM
calculations are correct (ruler 24.50 ± 0.13 cm, calipers 24.600 ± 0.007 cm; pendulum 1.415 ± 0.010 s),
and the agreement test is done quantitatively (0.77σ). The Station C propagation is exactly right —
the power rule applied to the **diameter** gives σ_V/V = 3σ_d/d, and the density combines mass and volume
in quadrature to give 7.86 ± 0.02 g/cm³, consistent with steel at 0.31σ. The conceptual answers are
strong: the accuracy-vs-precision distinction is made from the data rather than asserted, and the
Station B answer correctly identifies that Method 2 removes the reaction error's *entry point* rather
than merely averaging it. Fermi reasoning is sound and assumptions are stated. The discussion correctly
separates random from systematic sources and proposes concrete improvements. Full marks.

---
*PHYS 141 · Week 0 · Lab 0 · Adebayo Glover*
