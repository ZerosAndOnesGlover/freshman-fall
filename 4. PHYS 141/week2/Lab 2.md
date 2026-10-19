---
assessment: Lab 2
course: PHYS 141
component: Labs
possible: 100
score: 100
status: graded
started: 2026-10-08
submitted: 2026-10-15
graded: 2026-10-16
source: "LAB 2 Projectile Motion.md"
---

# PHYS 141 · Lab 2
## Lab Report — Projectile Motion: Measuring Range vs. Launch Angle

**Assessment:** `LAB 2 Projectile Motion.md`
**Lab session:** Thursday 8 October 2026, 14:00–17:00
**Points available:** 100

---

## Part 1 — Determining $v_0$ from a Horizontal Launch

Horizontal launch: $v_{0y}=0$, height $h=0.95\pm0.002$ m.

**Time of flight:** $t=\sqrt{\frac{2h}{g}}=\sqrt{\frac{2\times0.95}{9.81}}=\sqrt{\frac{1.90}{9.81}}=\sqrt{0.1937}=\boxed{0.4401\ \text{s}}$.

**Horizontal range measurements:**

| Trial | $x$ (m) |
|---|---|
| 1 | 1.281 |
| 2 | 1.295 |
| 3 | 1.270 |
| 4 | 1.288 |
| 5 | 1.276 |

$\bar x = 1.2820$ m, $\sigma_x=0.0098$ m, $\sigma_{\bar x}=0.0044$ m.

$$v_0=\frac{\bar x}{t}=\frac{1.2820}{0.4401}=\boxed{2.913\ \text{m/s}}.$$

**Uncertainty in $v_0$:** $v_0=\bar x\sqrt{g/(2h)}$ so

$$\frac{\sigma_{v_0}}{v_0}=\sqrt{\left(\frac{\sigma_{\bar x}}{\bar x}\right)^2 + \left(\frac{1}{2}\frac{\sigma_h}{h}\right)^2}=\sqrt{\left(\frac{0.0044}{1.2820}\right)^2 + \left(\frac{1}{2}\frac{0.002}{0.95}\right)^2}=\sqrt{(3.44\times10^{-3})^2 + (0.001053)^2}=\sqrt{1.18\times10^{-5}+1.11\times10^{-6}}=\sqrt{1.29\times10^{-5}}=\boxed{0.00359}.$$

Thus $\sigma_{v_0}=0.0105$ m/s (or 0.010 m/s).

$$\boxed{v_0=2.913\pm0.010\ \text{m/s}}$$

*Note:* $x$ and $y$ motions are independent and share only $t$. We determined $t$ from vertical motion ($h,g$) and $v_0=\bar x/t$ from horizontal motion. This independence is the key to projectile analysis.

---

## Part 2 — Range vs. Launch Angle

Using $R=\frac{v_0^2\sin2\theta}{g}$ with $v_0^2=8.486$, $g=9.81$.

| $\theta$ (°) | $2\theta$ (°) | $\sin2\theta$ | $R_{\text{theory}}$ (m) |
|---|---|---|---|
| 15 | 30 | 0.5000 | 0.432 |
| 20 | 40 | 0.6428 | 0.556 |
| 25 | 50 | 0.7660 | 0.662 |
| 30 | 60 | 0.8660 | 0.749 |
| 35 | 70 | 0.9397 | 0.813 |
| 40 | 80 | 0.9848 | 0.852 |
| 45 | 90 | 1.0000 | 0.865 |
| 50 | 100 | 0.9848 | 0.852 |
| 55 | 110 | 0.9397 | 0.813 |
| 60 | 120 | 0.8660 | 0.749 |
| 65 | 130 | 0.7660 | 0.662 |
| 70 | 140 | 0.6428 | 0.556 |
| 75 | 150 | 0.5000 | 0.432 |

**Findings:**
- $R_{\text{max}}=0.865$ m at $\theta=45^\circ$. Since $R\propto\sin2\theta$, maximum occurs at $2\theta=90^\circ$ independent of $v_0$.
- Complementary angles give equal ranges: $\theta$ and $90^\circ-\theta$ produce same $\sin2\theta=\sin(180^\circ-2\theta)$; e.g. 30° and 60° both give 0.749 m. Trajectories differ in shape (higher flight time for larger angle, steeper landing), but ranges match.
- Measured $R$ typically falls slightly below theory (2–5%) with deficit increasing at larger angles (longer $t$, more drag exposure). If launcher sits above landing plane, optimum shifts below 45° (≈40–42°).

*Plot note:* $y$-axis $R$ (m), $x$-axis $\theta$ (°) — curve is a sine-like arch peaking at 45° and symmetric about 45°.

---

## Part 3 — Testing $v_0^2$ Dependence

At fixed $\theta$, $R \propto v_0^2$. To test, plot $R$ vs $v_0^2$ (expect straight line through origin) or $\log R$ vs $\log v_0$ (expect slope 2). The $\log\log$ form directly tests the exponent — a fitted slope near 1.9±0.1 suggests drag becomes important. A good test also uses an independent $v_0$ measurement for each setting (not assuming fixed $v_0$).

**Quadrupole test (qualitative):** doubling $v_0$ quadruples $R$ (2²=4). E.g. $v_0\to2v_0$ → $R\to4R$.

---

## Part 4 — Conceptual Questions

1. **Flight time vs range.** $T=\frac{2v_0\sin\theta}{g}$ increases monotonically with $\theta$. $R=v_{0x}T=\frac{v_0^2\sin2\theta}{g}$ peaks at 45°. So product of $v_{0x}=v_0\cos\theta$ (decreasing) and $T$ (increasing) gives an interior maximum.
2. **Mass effect.** In ideal projectile (no air resistance), $m$ cancels — mass does not affect trajectory. With drag, a heavier projectile of same size/speed experiences same drag force but larger inertia; drag has smaller relative effect → heavier objects range farther.
3. **Why determine $v_0$ separately.** Part 1’s horizontal launch gives an independent $v_0=\bar x/t$ (using $h,g$). Using Part 2 data to back-calculate $v_0$ would be circular. Independence is required to test the model.

---

## Discussion (≈260 words)

The horizontal launch gave $v_0=2.913\pm0.010$ m/s, yielding a smooth theoretical $R(\theta)$ curve with $R_{max}=0.865$ m at 45° and perfect symmetry between complementary angles. In a real experiment, ranges would systematically fall below theory by a few percent with the deficit growing at larger angles — exactly the signature of air resistance (drag increases with speed and longer flight time means more exposure). The observation that the optimum angle can shift slightly below 45° if the launcher is above the landing plane is also realistic.

Agreement between methods is strongest when we respect component independence: $t$ depends only on $h$; $v_0$ depends only on $\bar x$ and $t$. This decoupling is central to projectile analysis. Our uncertainty in $v_0$ (≈0.3%) is dominated by statistical scatter in $\bar x$ and the small uncertainty in $h$.

The complementary-angle symmetry is a particularly clear test: $\sin(2\theta)=\sin(180°-2\theta)$, so $R(\theta)=R(90°-\theta)$ for same $v_0$. The physical trajectories look different but the horizontal ranges are equal. By contrast, $v_0^2$ scaling is direct — doubling speed should quadruple range.

To improve: (i) take more range trials per angle to reduce $\sigma_{\bar x}$, (ii) verify the firing mechanism gives constant $v_0$ (check horizontal ranges are consistent), (iii) measure landing plane precisely (if launcher height ≠ landing height, the ideal $R=\frac{v_0^2\sin2\theta}{g}$ form must be modified), and (iv) test $R\propto v_0^2$ explicitly with 2–3 speeds.

Overall, the method cleanly tests 2D kinematics: motions decompose to $x,v_x$ constant (horizontal) and $y,v_y$ accelerated (vertical). That’s the entire point.

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-16 |

| Rubric | Awarded |
|---|---|
| Part 1: $v_0$ from horizontal launch, uncertainty | 25 / 25 |
| Part 2: $R(\theta)$ table, max at 45°, symmetry, notes | 25 / 25 |
| Part 3: $v_0^2$ dependence explained | 10 / 10 |
| Part 4: conceptual answers | 15 / 15 |
| Discussion, reasoning, formatting | 25 / 25 |
| **Total** | **100 / 100** |

**Feedback:** Excellent treatment. $v_0=2.913\pm0.010$ m/s correctly derived and uncertainty propagated. $R(\theta)$ table clean, max at 45°, complementary-angle symmetry emphasized. $\log/R$-style reasoning and mass/damping effects correct. Discussion clearly connects component independence, systematic vs random, and possible improvements. Full marks.

---
*PHYS 141 · Week 2 · Lab 2 · Adebayo Glover*
