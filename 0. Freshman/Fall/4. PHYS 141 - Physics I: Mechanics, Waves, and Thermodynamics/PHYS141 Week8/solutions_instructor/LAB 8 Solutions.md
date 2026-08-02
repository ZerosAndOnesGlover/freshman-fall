# PHYS 141 — Lab 8 Solutions
## The Simple Pendulum and Simple Harmonic Motion
## INSTRUCTOR ONLY

---

## Pre-Lab Answers

**Q1.** $T = 2\pi\sqrt{L/g} \Rightarrow T^2 = \dfrac{4\pi^2}{g}L$. Linear in $L$, through the origin,
slope $4\pi^2/g = \mathbf{4.024~\text{s}^2/\text{m}}$.

**Q2.** Timing 20 oscillations with $\pm0.2$ s uncertainty gives $\delta T = 0.2/20 = \mathbf{0.010}$ s.
Timing one gives $\pm0.2$ s — **twenty times worse**. This is the whole reason for the procedure.

**Q3.** Larger. Since $\sin\theta < \theta$, the true restoring force is *weaker* than the linear
approximation, so the pendulum accelerates less and takes longer.

**Q4.** Simple pendulum, $L=1$ m: $T = \mathbf{2.006}$ s. Uniform rod pivoted at one end:
$T = 2\pi\sqrt{2L/3g} = \mathbf{1.638}$ s. **The rod is faster.**

---

## Part 1 — Period versus Length *(25 pts)*

**Expected data** (small amplitude, $g = 9.81$):

| $L$ (m) | $T$ (s) | $T^2$ (s²) |
|---|---|---|
| 0.20 | 0.897 | 0.805 |
| 0.40 | 1.269 | 1.610 |
| 0.60 | 1.554 | 2.415 |
| 0.80 | 1.794 | 3.219 |
| 1.00 | 2.006 | 4.024 |
| 1.20 | 2.198 | 4.829 |

**Analysis answers.**

1. $T^2 = (4\pi^2/g)L$ — linear, through the origin. *(3 pts)*
2. Plot should be a straight line; error bars from $\delta T$ propagated as $\delta(T^2)=2T\delta T$.
   *(6 pts)*
3. **Slope $\approx 4.02$ s²/m**, giving $g = 4\pi^2/\text{slope} \approx \mathbf{9.8~\text{m/s}^2}$.
   *(8 pts)*
4. Typical student results land within 1–3% of 9.81. *(4 pts)*
5. **A non-zero intercept indicates a systematic length error** — almost always measuring $L$ to the
   *top* of the bob rather than its centre, which makes every $L$ too small by the bob's radius and
   produces a **positive** intercept. *(4 pts)*

> *Watch for:* students who measure to the top of the bob typically get $g$ around 9.3–9.5 and a
> visible positive intercept. Do not simply mark it wrong — the intercept is the diagnostic, and
> spotting it is the skill.

---

## Part 2 — Period versus Amplitude *(20 pts)*

**Expected:** $T$ increases slightly with amplitude.

| $\theta_0$ | Predicted excess over small-angle |
|---|---|
| 10° | 0.4% |
| 15° | 1.1% |
| 20° | 2.1% |
| 30° | 4.7% |
| 45° | ~10% |

1. **Increases.** *(3 pts)*
2. Typically constant within uncertainty up to about $15$–$20°$, depending on timing precision.
   With $\delta T \approx 0.01$ s on $T \approx 2$ s, resolution is about 0.5%, so the $30°$ excess
   should be detectable and the $10°$ excess should not. *(5 pts)*
3. Measured excess at $30°$ should be a few percent, consistent with 4.7%. *(6 pts)*
4. **Because $\sin\theta < \theta$.** The real restoring force is weaker than the linear model
   assumes, so the pendulum is accelerated less and takes longer to complete a swing. *(6 pts)*

*Full marks on 4 require the $\sin\theta<\theta$ comparison, not just "the approximation breaks down".*

---

## Part 3 — Period versus Mass *(10 pts)*

1. **Independent of mass** within uncertainty. *(4 pts)*
2. The restoring force $mg\sin\theta$ is proportional to $m$, and so is the inertia. Writing
   $ma = -mg\sin\theta$, the mass cancels: $a = -g\sin\theta$. **The same cancellation that makes all
   objects fall at the same rate.** *(4 pts)*
3. Similar size keeps **air drag** comparable. A large light bob experiences relatively more drag,
   which damps it faster and can measurably shift the period. *(2 pts)*

---

## Part 4 — Spring Constant, Two Ways *(25 pts)*

1. Both methods should give $k$ agreeing to within a few percent. *(8 pts)*
2. Agreement within combined uncertainty is expected. *(4 pts)*
3. $T^2 = (4\pi^2/k)m$, so the plot **should** pass through the origin — but typically shows a small
   **positive intercept**. *(6 pts)*
4. **The spring's own mass oscillates too.** A standard result is that roughly $\tfrac13$ of the
   spring's mass adds to the effective inertia:
   $$T = 2\pi\sqrt{\frac{m + m_{\text{spring}}/3}{k}}$$
   This biases the **dynamic** method: it makes $T$ too large for a given $m$, so the extracted $k$
   comes out **too small**. The static method is unaffected, since it involves no motion. The
   $m_{\text{spring}}/3$ term is exactly what produces the positive intercept in part 3. *(7 pts)*

*Marking: full credit on 4 requires identifying **which** method is biased and in **which
direction**. Merely saying "the spring has mass" earns 3.*

---

## Part 5 — Damping *(20 pts)*

1. $\ln A$ against $t$ should be linear if damping is viscous. Real air damping is closer to
   quadratic in $v$ at these speeds, so slight curvature is common and worth noting rather than
   penalising. *(6 pts)*
2. Slope $= -\gamma$; then $b = 2m\gamma$. *(6 pts)*
3. $Q = \omega_0/2\gamma$, and the number of oscillations before the amplitude falls to $1/e$ is
   $Q/\pi$. *(4 pts)*
4. Compare $b$ with $2\sqrt{mk}$; for any classroom spring–mass system this will be **far** smaller,
   so **underdamped**. *(4 pts)*

---

## Lab Report Marking Summary

| Component | Points | Watch for |
|-----------|--------|-----------|
| Part 1 | 25 | Intercept interpreted, not ignored |
| Part 2 | 20 | $\sin\theta<\theta$ argument in Q4 |
| Part 3 | 10 | Mass cancellation shown algebraically |
| Part 4 | 25 | Spring mass biasing the **dynamic** method downward |
| Part 5 | 20 | Log plot, $\gamma$ extracted, regime justified by comparison |
| **Total** | **100** | |

**Common systematic errors to look for:**

1. Measuring $L$ to the top of the bob rather than its centre — the single most common, and visible
   as a non-zero intercept in Part 1.
2. Timing from the extreme rather than from the centre. Starting the stopwatch at the turning point
   is harder to judge precisely, since the bob is momentarily stationary there.
3. Large amplitudes in Part 1, contaminating the $g$ determination with the Part 2 effect.
4. Counting oscillations wrongly — a "swing" over and back is **one** oscillation, not two.
