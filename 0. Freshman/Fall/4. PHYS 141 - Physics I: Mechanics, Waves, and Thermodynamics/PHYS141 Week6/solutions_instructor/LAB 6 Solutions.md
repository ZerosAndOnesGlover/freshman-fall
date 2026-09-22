# PHYS 141 · Week 6
## LAB 6 Solutions — INSTRUCTOR ONLY

> **Representative data.** The numbers below are one realistic dataset, generated and checked
> numerically. Student apparatus will differ — **grade the method, not agreement with these
> figures.** Every derived quantity here is reproducible from the raw data in the same section,
> so you can re-run a student's arithmetic against their own readings.

---

## Part 1 — Moment of Inertia via Applied Torque

Spindle radius r = 0.0254 m (calipers, averaged). Hanging mass m released from rest; a measured by
photogate.

| Trial | m (kg) | a (m/s²) | 1/m (kg⁻¹) | 1/a (s²/m) | I = mr²(g/a − 1) |
|---|---|---|---|---|---|
| 1 | 0.020 | 0.01027 | 50.000 | 97.3710 | 0.01231 |
| 2 | 0.050 | 0.02629 | 20.000 | 38.0373 | 0.01200 |
| 3 | 0.100 | 0.05191 | 10.000 | 19.2641 | 0.01213 |
| 4 | 0.150 | 0.07812 | 6.667 | 12.8008 | 0.01206 |
| 5 | 0.200 | 0.10336 | 5.000 | 9.6749 | 0.01212 |


**Direct average of the per-trial values:** I = **0.01212 ± 0.00005 kg·m²** (σ = 0.00012).

### The handout's linearisation — and why it misbehaves

Plotting 1/a vs. 1/m, with intercept 1/g and slope I/(gr²):

- intercept = -0.31533 ± 0.27969 → **g = -3.17 m/s²**
- slope = 1.94972 ± 0.01129 → **I = slope·g·r² = 0.01234 ± 0.00007 kg·m²**
- R² = 0.99990

**The R² looks excellent and the result is the worst of the three methods.** Two things have gone
wrong, and both are worth teaching:

1. **Extreme leverage.** The x-values 1/m are 50.0, 20.0, 10.0, 6.7, 5.0. The
   m = 20 g trial sits at 1/m = 50 while every other point is below 20, giving it a leverage of
   **h = 0.92** — that single point effectively determines the fit. It is also the
   *least reliable* measurement, because a is smallest there and its relative error is largest
   (1.7%
   here versus 0.14% at 200 g).
   **The worst data point controls the answer.**
2. **The intercept is a wild extrapolation.** 1/g is the value at 1/m = 0, i.e. *infinite* hanging
   mass — far outside the data. Hence the meaningless g = -3.17 m/s². A student who reports a
   negative or absurd g here has done the arithmetic correctly and should not be penalised; they
   should be credited for noticing.

### The linearisation that actually works

Keep a friction torque τ_f in the model. From mg − T = ma and Tr − τ_f = Iα = Ia/r:

$$m(g-a) = \frac{I}{r^2}a + \frac{\tau_f}{r}$$

Plot **y = m(g − a)** against **x = a**: slope = I/r², intercept = τ_f/r.

- slope = 18.7488 ± 0.0629 → **I = slope·r² = 0.01210 ± 0.00004 kg·m²**
- intercept = 0.00017 ± 0.00401 → **τ_f = 0.00000 ± 0.00010 N·m**
- R² = 0.999966

This form has balanced leverage (0.54, 0.33, 0.20, 0.30, 0.63),
needs no extrapolation, and **measures the friction rather than letting it bias I**. It recovers
the true I to better than 0.1% even when a friction torque is present, which neither of the other
two methods does.

**Accept any of the three methods** for full credit if correctly executed. Reserve bonus marks for
students who notice the leverage problem or the nonsensical intercept.

---

## Part 2 — Parallel Axis Theorem

Point mass m_p = 0.100 kg clamped at d = 0.150 m from the axis.

$$I_{added, predicted} = m_p d^2 = (0.100)(0.150)^2 = \mathbf{0.00225\ kg\cdot m^2}$$

Measured by difference: I_new − I_platform. With I_platform = 0.01210 kg·m², a correctly
performed repeat gives I_new ≈ 0.01435 kg·m², hence
I_added,measured ≈ 0.00225 kg·m² — agreement at the few-percent level.

**Watch the error propagation.** I_added is a *difference of two comparable numbers*
(0.01435 − 0.01210), so the absolute uncertainties add in quadrature while the
result is small. If each I carries ±0.00004, the difference carries ±0.00006 on a value of
0.00225 — a **3% relative uncertainty** from inputs known to 0.3%.
Subtracting nearly equal quantities destroys precision. Students who report I_added to four
significant figures have not propagated; reward those who note the amplification and who therefore
choose d large enough to make the added term substantial.

---

## Part 4 — Written Discussion (expected answers)

**Q1 — Why linearise rather than average per-trial I values?**

The intended answer is about **uncertainty propagation**: I = mr²(g/a − 1) divides by a, so the
relative error in I is amplified when a is small, and a plain average weights the noisiest trials
equally with the best ones.

The **fuller and more accurate answer** — which the data above supports — is that a fit's real
advantage is *diagnostic*: it reveals systematic error that averaging silently absorbs. A constant
friction torque shows up as a non-zero intercept, and a fit that includes it recovers I correctly
while the average is biased by more than 20%. But the choice of *which* linearisation matters
enormously: the 1/a vs. 1/m form recommended in the handout has pathological leverage and performs
**worse** than naive averaging on clean data. Award full credit to any student who identifies
either the propagation argument or the systematic-error argument; award bonus credit to any student
who tests both and reports that averaging beat the handout's fit.

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

**Lab 6 specifically:** the handout recommends the 1/a vs. 1/m linearisation, which the
worked solution above shows to be statistically poor for this apparatus. Do **not** penalise
students who used direct averaging or the m(g−a) vs. a form — both are defensible and one is
better. Flag this to the lab coordinator; the handout should be revised.

---

*PHYS 141 · Week 6 · Lab Solutions · Instructor Copy · © CSE Department*
