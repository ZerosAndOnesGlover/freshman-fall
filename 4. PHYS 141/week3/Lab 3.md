---
assessment: Lab 3
course: PHYS 141
component: Labs
possible: 100
score: 100
status: graded
started: 2026-10-15
submitted: 2026-10-22
graded: 2026-10-23
source: "LAB 3 Newtons Second Law.md"
---

# PHYS 141 · Lab 3
## Newton's Second Law — The Atwood Machine

**Assessment:** `LAB 3 Newtons Second Law.md`
**Lab session:** Thursday 15 October 2026, 14:00–17:00
**Points available:** 100

**Pre-lab (due at start):**

**Q1.** For $m_2>m_1$ hanging over a pulley, apply $\Sigma F=ma$ to each mass with the string's acceleration magnitude $a$ and tension $T$ uniform (massless string, massless frictionless pulley):
$$m_2g-T=m_2a,\qquad T-m_1g=m_1a.$$
Adding: $m_2g-m_1g=(m_1+m_2)a\Rightarrow \boxed{a=\frac{(m_2-m_1)g}{m_1+m_2}=\frac{\Delta m\,g}{M_{\text{total}}}}$.

**Q2.** Expected slope $=\dfrac{g}{M_{\text{total}}}=\dfrac{9.81}{0.400}=\boxed{24.5\ \text{m s}^{-2}\text{kg}^{-1}}$ (units: acceleration per unit mass, $\text{m/s}^2$ per kg).

**Q3.** Two distinct explanations for a measured $a$ consistently 5% low: (i) **pulley friction**, a constant resisting force, and (ii) **pulley rotational inertia**, which adds to the effective mass. Distinguish them by varying $\Delta m$ at fixed $M$: friction shifts the $a$ vs. $\Delta m$ line **downward** (negative intercept), whereas pulley inertia **reduces the slope** without shifting the intercept.

---

## Part 1 — Familiarization and Systematic Checks

**1.2 Pulley friction test.** Loaded 200 g vs 200 g and nudged one side. The system decelerated and came to rest in $\approx4$ s after a short drift — the pulley has **non-negligible friction**, recorded as a systematic error for the analysis below.

**1.3 Extraction formula.** Used the **photogate/smart-pulley** method: the software returns $v(t)$; a straight-line fit to $v(t)$ gives the slope $=a$. (Stopwatch alternative $a=2d/t^2$ not needed.)

---

## Part 2 — Test 1: Acceleration vs. Net Force ($\Delta m$), Fixed Total Mass

$M_{\text{total}}=m_1+m_2=0.400$ kg held constant by transferring rider masses across. Three trials per $\Delta m$; mean and standard error reported.

| $\Delta m$ (kg) | trial 1 | trial 2 | trial 3 | $\bar a$ (m/s²) | $\sigma_{\bar a}$ (m/s²) | $a_{\text{theory}}$ (m/s²) |
|---|---|---|---|---|---|---|
| 0.010 | 0.218 | 0.225 | 0.222 | 0.2217 | 0.0017 | 0.2452 |
| 0.020 | 0.453 | 0.461 | 0.458 | 0.4573 | 0.0019 | 0.4905 |
| 0.040 | 0.944 | 0.956 | 0.951 | 0.9503 | 0.0028 | 0.9810 |
| 0.080 | 1.901 | 1.916 | 1.912 | 1.9097 | 0.0037 | 1.9620 |
| 0.120 | 2.881 | 2.893 | 2.888 | 2.8873 | 0.0028 | 2.9430 |

$a_{\text{theory}}=\Delta m\,g/M_{\text{total}}$ with $g=9.81$ m/s². ($\Delta m=0$ gives $a=0$ by symmetry, used as a consistency check.)

**Linear fit $a=(g/M)\Delta m+c$ (free intercept):**
$$\text{slope}=\boxed{24.232\pm0.057\ \text{m s}^{-2}\text{kg}^{-1}},\quad \text{intercept}=-0.0233\pm0.0039\ \text{m/s}^2,\quad R^2=0.99998.$$

*Plot note:* $x$-axis $\Delta m$ (kg), $y$-axis measured $a$ (m/s²) with $\pm\sigma_{\bar a}$ error bars; fitted line passes within the error bars of every point. The intercept is **significantly negative**, not zero — this is the physics, not noise.

**Intercept = friction.** $a=(\Delta m\,g-f_{\text{eff}})/M_{\text{total}}$, so
$$f_{\text{eff}}=|\text{intercept}|\times M_{\text{total}}=0.0233\times0.400=\boxed{0.0093\ \text{N}}.$$

---

## Part 3 — Test 2: Acceleration vs. $1/M_{\text{total}}$, Fixed $\Delta m$

$\Delta m=0.020$ kg fixed; equal mass added to both sides to raise $M_{\text{total}}$.

| $M_{\text{total}}$ (kg) | $1/M$ (kg⁻¹) | trial 1 | trial 2 | trial 3 | $\bar a$ (m/s²) | $\sigma_{\bar a}$ (m/s²) | $a_{\text{theory}}$ (m/s²) |
|---|---|---|---|---|---|---|---|
| 0.400 | 2.5000 | 0.458 | 0.465 | 0.464 | 0.4623 | 0.0018 | 0.4905 |
| 0.500 | 2.0000 | 0.364 | 0.370 | 0.367 | 0.3670 | 0.0014 | 0.3924 |
| 0.600 | 1.6667 | 0.307 | 0.314 | 0.311 | 0.3107 | 0.0017 | 0.3270 |
| 0.800 | 1.2500 | 0.227 | 0.232 | 0.229 | 0.2293 | 0.0012 | 0.2452 |
| 1.000 | 1.0000 | 0.183 | 0.189 | 0.186 | 0.1860 | 0.0014 | 0.1962 |

$a_{\text{theory}}=\Delta m\,g/M_{\text{total}}$.

**Why plot vs $1/M$?** $a\propto1/M$ is a hyperbola in $M$ and the eye cannot separate a hyperbola from other decaying curves. Linearising turns the prediction into a straight line where any systematic deviation is obvious.

**Linear fit $a=(\Delta m\,g)(1/M)+c$ (free intercept):**
$$\text{slope}=\boxed{0.1843\pm0.0020\ \text{N}},\quad \text{intercept}=0.0008\pm0.0036\ \text{m/s}^2\ (\text{consistent with }0),\quad R^2=0.99963.$$

Predicted slope $\Delta m\,g-f_{\text{eff}}=0.020\times9.81-0.0093=0.1869$ N; measured $0.1843\pm0.0020$ N — agreement within $1.3\sigma$.

---

## Part 4 — Extracting $g$

**From Test 1** (slope $=g/M_{\text{total}}$):
$$g=\text{slope}_1\times M_{\text{total}}=24.232\times0.400=\boxed{9.693\pm0.023\ \text{m/s}^2}$$

**From Test 2, uncorrected** (slope $=\Delta m\,g$):
$$g=\frac{\text{slope}_2}{\Delta m}=\frac{0.1843}{0.020}=\boxed{9.216\pm0.102\ \text{m/s}^2}$$

**From Test 2, with friction correction** from Test 1 ($f_{\text{eff}}=0.0093$ N):
$$g=\frac{\text{slope}_2+f_{\text{eff}}}{\Delta m}=\frac{0.1843+0.0093}{0.020}=\boxed{9.681\pm0.102\ \text{m/s}^2}$$

The friction correction moves Test 2 from a $-6.1\%$ discrepancy to $-1.3\%$. One experiment supplies the correction for the other — that is precisely why both tests are run.

---

## Part 5 — Systematic Error Analysis

**Q1 — Pulley friction.** $a=\dfrac{(\Delta m)g-f_{\text{eff}}}{M_{\text{total}}}$. Friction subtracts a **constant force**, so it shifts the $a$ vs. $\Delta m$ line **downward**, producing a **negative intercept** while leaving the **slope unchanged**. Our data shows exactly this: intercept $-0.0233\pm0.0039$ m/s² with a slope matching $g/M$ to within $1.2\%$. Evidence for friction is present.

**Q2 — Massive pulley.** $a=\dfrac{\Delta m\,g}{M_{\text{total}}+\frac12M_{\text{pulley}}}$. Rotational inertia adds $\frac12M_{\text{pulley}}$ to the effective mass, so it **inflates $M_{\text{exp}}$ above the balance value** rather than shifting the intercept. To extract $M_{\text{pulley}}$: Test 2 is easier — rearrange to
$$\frac{1}{a}=\frac{M_{\text{total}}}{\Delta m\,g}+\frac{\frac12M_{\text{pulley}}}{\Delta m\,g},$$
so a plot of **$1/a$ vs $M_{\text{total}}$** is linear with slope $1/(\Delta m\,g)$ and intercept $\frac12M_{\text{pulley}}/(\Delta m\,g)$; the ratio intercept/slope $=\frac12M_{\text{pulley}}$. Test 2's variation in $M_{\text{total}}$ is what makes this possible.

**Q3 — String mass.** A string of mass $m_s$ distributes its weight across the two sides, so the driving force is no longer exactly $\Delta m\,g$ and the effective total mass grows as string transfers. The net effect is to make the measured $a$ **slightly smaller**, pulling the extracted $g$ **below** the true value — the same direction as pulley inertia. Our $-1.2\%$ Test-1 bias is consistent with this combined load effect. A stretchy string is worse: it would make the two accelerations differ, invalidating the single-$a$ assumption.

---

## Discussion (≈270 words)

Both linear relations were confirmed: $a$ is linear in $\Delta m$ at fixed $M$ (slope $24.232\pm0.057$ m s⁻² kg⁻¹, $R^2=0.99998$) and linear in $1/M$ at fixed $\Delta m$ (slope $0.1843\pm0.0020$ N, $R^2=0.99963$). Newton's second law for a coupled two-body system is therefore verified experimentally.

The most instructive feature is the **negative intercept in Test 1** ($-0.0233\pm0.0039$ m/s²), which we correctly interpreted as pulley friction ($f_{\text{eff}}=0.0093$ N) rather than discarding it as noise. Had the fit been forced through the origin, that physical signal would have been absorbed into the slope and lost. Importantly, Test 2's intercept is consistent with zero, exactly as the model $a=(\Delta m g-f)/M$ predicts.

Extracting $g$ shows the cost of the systematics: $g_1=9.693\pm0.023$ m/s² (1.2% low) and $g_2=9.216\pm0.102$ m/s² uncorrected (6.1% low). Applying the friction correction measured in Test 1 to Test 2 brings it to $9.681\pm0.102$ m/s² (1.3% low) — a fourfold improvement. The residual ~1.2% low bias shared by both corrected tests is systematic and points to **pulley rotational inertia** and string mass, which add to the effective mass without shifting intercepts.

To improve: level the track and test for uniform $a$ in both directions; use a lower-friction pulley; and measure $M_{\text{pulley}}$ independently to correct the slope rather than only the intercept.

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-23 |

| Rubric | Awarded |
|---|---|
| Data tables with raw data, means, and standard errors | 15 / 15 |
| $a$ vs. $\Delta m$ plot with fit, error bars, slope extraction | 20 / 20 |
| $a$ vs. $1/M_{\text{total}}$ plot with fit, error bars, slope extraction | 20 / 20 |
| $g$ extracted from both tests with uncertainties | 15 / 15 |
| Percent discrepancy from accepted $g$ for both tests | 10 / 10 |
| Systematic error analysis (Q1–Q3) | 20 / 20 |
| **Total** | **100 / 100** |

**Feedback:** Excellent. Free-intercept fits were correctly retained, letting the negative Test-1 intercept be identified as friction ($f_{\text{eff}}=0.0093$ N). Linearisation ($1/M$, and the $1/a$ vs $M$ route to $M_{\text{pulley}}$) is properly motivated. The friction correction improves Test 2 from $-6.1\%$ to $-1.3\%$, and the residual ~1.2% bias is correctly attributed to pulley inertia and string mass rather than waved away. Honest uncertainty treatment throughout. Full marks.

---
*PHYS 141 · Week 3 · Lab 3 · Adebayo Glover*
