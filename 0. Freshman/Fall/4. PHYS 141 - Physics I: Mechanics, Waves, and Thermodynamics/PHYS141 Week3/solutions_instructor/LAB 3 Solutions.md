# PHYS 141 · Week 3
## LAB 3 Solutions — INSTRUCTOR ONLY

> **Representative data.** The numbers below are one realistic dataset, generated and checked
> numerically. Student apparatus will differ — **grade the method, not agreement with these
> figures.** Every derived quantity here is reproducible from the raw data in the same section,
> so you can re-run a student's arithmetic against their own readings.

---

## Part 2 — Test 1: a vs. Net Force (M_total = 0.5 kg fixed)

Hanging mass Δm transferred from the cart to the hanger, so **M_total stays constant** — this is
what isolates F as the only variable.

| Trial | Δm (kg) | F = Δm·g (N) | a measured (m/s²) |
|---|---|---|---|
| 1 | 0.010 | 0.0981 | 0.1782 |
| 2 | 0.020 | 0.1962 | 0.3594 |
| 3 | 0.030 | 0.2943 | 0.5686 |
| 4 | 0.040 | 0.3924 | 0.7718 |
| 5 | 0.050 | 0.4905 | 0.9500 |


**Linear fit a = (1/M)F + c:**

- slope = **1.9939 ± 0.0319 kg⁻¹** → M_experimental = 1/slope = **0.5015 ± 0.0080 kg**
- intercept = **-0.0212 ± 0.0104 m/s²**
- R² = 0.99923

**Interpretation.** M_experimental = 0.502 ± 0.008 kg against a balance value of
0.500 kg — agreement within 0.19σ. Newton's second law is
confirmed: **a is linear in F, with slope 1/M.**

**The intercept is the physics.** It is *negative* (-0.0212 m/s²), which is not noise — it says a
non-zero force is required before any acceleration occurs. That is **friction**:

$$f = |{\rm intercept}| \times M = 0.0212 \times 0.5 = \mathbf{0.0106\ N}$$

A student who forces the fit through the origin destroys this result and should lose method marks —
the free intercept is what makes the experiment able to *detect* systematic error rather than absorb
it into the slope.

---

## Part 3 — Test 2: a vs. 1/M_total (Δm = 0.030 kg fixed)

| Trial | M_total (kg) | 1/M (kg⁻¹) | a measured (m/s²) |
|---|---|---|---|
| 1 | 0.300 | 3.3333 | 0.9300 |
| 2 | 0.400 | 2.5000 | 0.7137 |
| 3 | 0.500 | 2.0000 | 0.5596 |
| 4 | 0.700 | 1.4286 | 0.4093 |
| 5 | 1.000 | 1.0000 | 0.2853 |


**Linear fit a = F_net·(1/M) + c:**

- slope = **0.2772 ± 0.0041 N**
- intercept = 0.0107 ± 0.0090 m/s² (consistent with zero)
- R² = 0.99935

The slope *is* the net force: predicted F_net = Δm·g − f = 0.2943 − 0.0120 =
**0.2823 N**, measured **0.2772 ± 0.0041 N** — agreement within
1.26σ.

> **Why plot against 1/M and not M?** Because a ∝ 1/M is a *hyperbola* in M, and the eye cannot
> distinguish a hyperbola from other decaying curves. Plotting against 1/M turns the prediction
> into a straight line, where systematic deviation is obvious. **Linearise before you fit** — the
> same reasoning drives Lab 6.

---

## Part 4 — Extracting g

From Test 2, slope = Δm·g − f, so

$$g = \frac{{\rm slope} + f}{\Delta m} = \frac{0.2772 + 0.0106}{0.030} = 9.59\ \text{m/s}^2$$

using the friction force measured independently in Test 1. **Neglecting the friction correction
gives 9.24 m/s²**, low by 5.8% — the correction is not
optional, and the fact that one experiment supplies the correction for the other is the reason both
tests are run.

Expect student values in the range 9.3–9.9 m/s². Anything within ~5% with a stated friction
correction is a good result.

---

## Part 5 — Systematic Error Analysis (expected answers)

**Pulley friction and pulley mass.** Both retard the system. Friction appears as the negative
intercept in Test 1 and is correctable. Pulley *rotational inertia* is different: it adds I/r² to
the effective mass, so it inflates M_experimental above the balance value rather than shifting the
intercept. If a student's M_exp exceeds the balance mass by a consistent few percent, this is why —
and it is a better answer than "measurement error".

**String mass and stretch.** Negligible for thread; a stretchy string makes the two bodies'
accelerations differ, breaking the single-a assumption entirely.

**Assuming tension is uniform.** Valid only for a massless string over a frictionless, massless
pulley. With a massive pulley the tensions on the two sides **differ** — that difference is what
supplies the torque to spin it up.

**Timing method.** Ask what the student actually measured. Average velocity over an interval is not
instantaneous velocity, and using it as such biases a. Photogate timing is far better than a
stopwatch here, and students should say which they used.

**The check that matters most:** does the cart accelerate uniformly? If a drifts systematically
across the run, the track is not level. Reward anyone who tested for this by rolling the cart in
both directions.

---

## Marking Scheme

Point values follow the rubric printed on the lab handout. Within each section:

- **Method (≈60%).** Correct procedure, a stated sign/coordinate convention, symbolic setup before
  numbers, uncertainties propagated by the right rule, and units carried throughout.
- **Result (≈40%).** Correct arithmetic, sensible significant figures, and a stated comparison
  against theory (percent discrepancy *and* a σ-based consistency statement).

**Carry-through.** Penalise a wrong value once. If the student reasons correctly from their own
earlier error, award the downstream marks in full.

**A result that disagrees with theory is not automatically wrong.** Full marks are available for a
discrepant result that is correctly measured, correctly propagated, and honestly discussed. Award
*no* credit for a suspiciously perfect result with no uncertainty analysis — that is the more
common form of academic dishonesty in a lab course.

---

*PHYS 141 · Week 3 · Lab Solutions · Instructor Copy · © CSE Department*
