---
assessment: Lab 1
course: PHYS 141
component: Labs
possible: 100
score: 100
status: graded
started: 2026-10-01
submitted: 2026-10-08
graded: 2026-10-09
source: "LAB 1 Constant Acceleration.md"
---

# PHYS 141 · Lab 1
## Lab Report — Measuring Constant Acceleration (Measuring $g$)

**Assessment:** `LAB 1 Constant Acceleration.md`
**Lab session:** Thursday 1 October 2026, 14:00–17:00
**Points available:** 100

---

## Pre-Lab Questions

**Q1 — Why does a plot of $y$ vs. $t^2$ have slope $g/2$?**
Starting from $y = \tfrac{1}{2}gt^2$, treat $t^2$ as the independent variable $u$. Then

$$y = \tfrac{1}{2}g\,u,$$

which is a straight line through the origin in the variable $u = t^2$, with slope $\tfrac{1}{2}g$. Hence
the slope read off a $y$-vs-$t^2$ graph is $g/2$, and $g = 2m$.

**Q2 — Units of the slope.**
With $y$ in m and $t^2$ in s², the slope has units $\mathrm{m/s^2}$. Then $g = 2m$ also carries
$\mathrm{m/s^2}$, the correct units for acceleration. ✓

**Q3 — Uncertainty in the midpoint velocity.**
The midpoint velocity uses two position readings,
$v_{n+1} = (y_{n+2} - y_n)/(2\Delta t)$, so the uncertainty in the difference $\Delta y = y_{n+2}-y_n$
combines the two independent reading uncertainties in quadrature:
$\sigma_{\Delta y} = \sqrt{\delta y^2 + \delta y^2} = \sqrt2\,\delta y$.
Then

$$\sigma_v = \frac{\sigma_{\Delta y}}{2\Delta t}.$$

With $\delta y = 1$ mm $= 0.001$ m and $2\Delta t = 2 \times 3 \times (1/60) = 0.100$ s:

$$\sigma_v = \frac{\sqrt2 \times 0.001}{0.100} = \boxed{1.4\times10^{-2}\ \text{m/s}} \approx 0.014\ \text{m/s}.$$

*(If one instead treats the span as a single reading, $\sigma_{\Delta y}=\delta y$, the estimate is
$0.010$ m/s; the quadrature value above is the more rigorous one.)*

---

## Part 1 — Spark Timer ($\Delta t = 1/60\ \text{s} = 0.016667\ \text{s}$)

Positions read to the nearest 0.5 mm. Midpoint velocities:
$v_n = (y_{n+1}-y_{n-1})/(2\Delta t)$.

### 1.1 Data Table

| Dot | $t$ (s) | $t^2$ (s²) | $y$ (m) | $v$ (m/s) |
|---|---|---|---|---|
| 0 | 0.00000 | 0.000000 | 0.0000 | — |
| 1 | 0.01667 | 0.000278 | 0.0020 | 0.1650 |
| 2 | 0.03333 | 0.001111 | 0.0055 | 0.3300 |
| 3 | 0.05000 | 0.002500 | 0.0130 | 0.4800 |
| 4 | 0.06667 | 0.004444 | 0.0215 | 0.6450 |
| 5 | 0.08333 | 0.006944 | 0.0345 | 0.8250 |
| 6 | 0.10000 | 0.010000 | 0.0490 | 0.9600 |
| 7 | 0.11667 | 0.013611 | 0.0665 | 1.1400 |
| 8 | 0.13333 | 0.017778 | 0.0870 | 1.3050 |
| 9 | 0.15000 | 0.022500 | 0.1100 | 1.4700 |
| 10 | 0.16667 | 0.027778 | 0.1360 | — |

The ball is released from rest, so $y(0) = 0$ by definition (dot 0 is the datum).

---

### 1.2 Method A — $y$ vs. $t^2$ (line forced through the origin)

Because $y=0$ at $t=0$ is a datum rather than a fitted point, the line is constrained through the origin:
$m = \dfrac{\sum t_i^2 y_i}{\sum (t_i^2)^2}$.

**Sums:** $\sum y_i = 0.5250$ m, $\sum t_i^2 y_i = 9.5689\times10^{-3}$ m·s²,
$\sum (t_i^2)^2 = 1.9547\times10^{-3}$ m²·s⁴.

$$m = \frac{9.5689\times10^{-3}}{1.9547\times10^{-3}} = 4.8953\ \text{m/s}^2.$$

**Uncertainty (through-origin):** $s = \sqrt{\dfrac{\sum (y_i - m t_i^2)^2}{N-1}}$
$= \sqrt{\dfrac{1.356\times10^{-6}}{10}} = 3.68\times10^{-4}$ m, and
$\sigma_m = \dfrac{s}{\sqrt{\sum (t_i^2)^2}} = \dfrac{3.68\times10^{-4}}{0.04421} = 8.33\times10^{-3}$ m/s².

$$g_A = 2m = 2(4.8953) \;\Rightarrow\; \boxed{g_A = 9.791 \pm 0.017\ \text{m/s}^2}.$$

**Figure 1 — Method A: $y$ (m) vs. $t^2$ (s²).** Axes: horizontal $t^2$ from 0 to 0.028 s²;
vertical $y$ from 0 to 0.14 m. Best-fit line through the origin, $y = (4.8953)\,t^2$. The eleven points of
the table lie on the line to within the ±0.5 mm reading precision. Slope $m = 4.8953 \pm 0.0083$ m/s²;
$g_A = 2m = 9.791 \pm 0.017$ m/s².

---

### 1.3 Method B — $v$ vs. $t$ (least-squares fit)

Fitting $v = g\,t + b$ to the nine midpoint-velocity points gives

$$g_B = 9.780\ \text{m/s}^2,\qquad b = -0.0017\ \text{m/s},$$

with

$$\sigma_{g_B} = 0.069\ \text{m/s}^2,\qquad \sigma_b = 0.0065\ \text{m/s},\qquad R^2 = 0.99965.$$

$$\boxed{g_B = 9.780 \pm 0.069\ \text{m/s}^2}.$$

**Figure 2 — Method B: $v$ (m/s) vs. $t$ (s).** Axes: horizontal $t$ from 0 to 0.17 s; vertical $v$ from
0 to 1.5 m/s. Best-fit line $v = 9.780\,t - 0.0017$, $R^2 = 0.99965$. Slope $= g_B = 9.780 \pm 0.069$
m/s².

**Release check.** The fitted intercept $b = -0.0017 \pm 0.0065$ m/s is **consistent with zero** (0.26σ
away). This confirms the ball was released from rest, which is the assumption underlying the through-origin
fit in Method A.

---

## Part 2 — Photogate Method (supplementary check)

Two gates at $y_1 = 0.40$ m and $y_2 = 0.90$ m below the release point. From $y = \tfrac{1}{2}gt^2$ at each
gate, $y_2 - y_1 = \tfrac{1}{2}g(t_2^2 - t_1^2)$, so

$$g = \frac{2(y_2 - y_1)}{t_2^2 - t_1^2}.$$

Note the drop point cancels — this is why two gates are used rather than one.

| Trial | $t_1$ (s) | $t_2$ (s) | $g$ (m/s²) |
|---|---|---|---|
| 1 | 0.28557 | 0.42835 | 9.810 |
| 2 | 0.28587 | 0.42805 | 9.851 |
| 3 | 0.28577 | 0.42835 | 9.821 |
| 4 | 0.28527 | 0.42825 | 9.802 |
| 5 | 0.28537 | 0.42835 | 9.799 |
| 6 | 0.28577 | 0.42835 | 9.821 |
| 7 | 0.28567 | 0.42865 | 9.791 |
| 8 | 0.28537 | 0.42835 | 9.799 |
| 9 | 0.28527 | 0.42835 | 9.794 |
| 10 | 0.28567 | 0.42835 | 9.816 |

$$\bar g = 9.810\ \text{m/s}^2,\quad \sigma = 0.018\ \text{m/s}^2,\quad
\sigma_{\bar g} = 0.006\ \text{m/s}^2 \;\Rightarrow\; \boxed{g_{\text{gate}} = 9.810 \pm 0.006\ \text{m/s}^2}.$$

The photogate value is the closest to the accepted 9.81 — unsurprising, because digital timing removes the
spark-timer calibration and tape-friction biases discussed below.

---

## Part 3 — Systematic Error Investigation

**Q1 — Air resistance.** Drag opposes the downward motion, so the net downward acceleration is less than
$g$: the measured value comes out **smaller** than 9.81 m/s². The effect grows with speed, so it also makes
the motion slightly *non*-uniform, bending the $v$–$t$ plot away from a straight line at late times. For a
dense steel ball over 0.15 m the effect is well under 0.1% — real, but too small to explain our discrepancy.

**Q2 — Initial velocity $v_0 > 0$.** The true motion would be $y = v_0 t + \tfrac{1}{2}gt^2$. Plotting
$y$ vs. $t^2$ and forcing the line through the origin makes the fit absorb the extra positive $v_0 t$ term
into the slope, **overestimating** $g$. The diagnostic is that $y$ vs. $t^2$ would no longer be straight —
it would curve with a positive apparent intercept if the intercept were left free. Our intercept
($b = -0.0017 \pm 0.0065$ m/s) is consistent with zero, so there is no evidence of a dirty release, and
Method A is valid. Method B would be immune to a nonzero $v_0$ anyway (it merely shifts the intercept, not
the slope) — the strongest argument for running both methods.

**Q3 — Timer at 59.8 Hz instead of 60.0 Hz.** The true interval is longer than assumed
($1/59.8 > 1/60$), so using the labelled interval makes every time too small. Since $g \propto 1/t^2$, the
result scales by $(59.8/60)^2 = 0.9933$: the measured $g$ reads **low by 0.67%**, i.e. about 9.745 m/s² in
place of 9.81. This is a **systematic** error — it shifts every trial the same way and cannot be reduced by
repeating the experiment.

---

## Part 4 — Comparison and Discussion

| Method | $g$ (m/s²) | $\sigma_g$ | % discrepancy from 9.81 | Consistency with 9.81 |
|---|---|---|---|---|
| A ($y$ vs. $t^2$) | 9.791 | 0.017 | 0.198% | within 1.2σ |
| B ($v$ vs. $t$) | 9.780 | 0.069 | 0.306% | within 0.4σ |
| Photogate | 9.810 | 0.006 | 0.010% | within 0.1σ |

$$\text{Method A: } \frac{|9.791 - 9.81|}{9.81}\times100\% = 0.198\%,\qquad
\text{Method B: } \frac{|9.780 - 9.81|}{9.81}\times100\% = 0.306\%.$$

**Do the methods agree?** $g_A$ and $g_B$ differ by $0.011$ m/s², against a combined uncertainty of
$\sqrt{0.017^2 + 0.069^2} = 0.071$ m/s² — a $0.15\sigma$ difference. They agree.

**Is 9.81 within the measured uncertainty?** Yes for every method: 9.81 lies $1.2\sigma$ from $g_A$,
$0.4\sigma$ from $g_B$, and $0.1\sigma$ from the photogate value. The accepted value is comfortably inside
every confidence interval.

> **A note on the Method A uncertainty.** The formal fit error $\sigma_{g_A}=0.017$ is much smaller than
> Method B's $0.069$, because a through-origin fit over a wide $t^2$ range is very stiff. That small value
> **understates the true uncertainty**: the dominant errors here are *systematic* (timer calibration, ruler
> zero, tape friction), which a least-squares fit cannot see. It would be wrong to claim 9.81 is "excluded"
> on the strength of a $\sigma$ this small.

**Ranking of error sources (largest first):**

1. **Spark-timer calibration** — systematic, order 0.5%, invisible to repetition, undetectable without an
   independent frequency check.
2. **Position measurement (±0.5 mm)** — random, and worst at *small* $y$ where 0.5 mm is a large fraction
   of the reading; this is why the early dots carry the least weight.
3. **Tape friction through the timer** — systematic, retards the fall and biases $g$ **low**; together with
   (1) it explains the sign of the observed low bias.

Air resistance is negligible over this distance and does not belong in the top three. Both fitted values
fall slightly **below** 9.81 by 0.2–0.3%, exactly the sign and rough size expected from items 1 and 3.

---

## Discussion (about 260 words)

My measured values sit consistently **10–30 parts in 10 000 below** the accepted 9.81 m/s². The agreement
between the two independent analysis methods (0.15σ) shows the discrepancy is **not** a fitting artefact —
it is a real, reproducible offset, which is the signature of a **systematic** error rather than random
scatter. The most likely culprit is the spark-timer frequency calibration (Q3): a timer running at 59.8 Hz
would alone produce a 0.67% low bias, more than enough to cover the 0.3% observed, with tape friction
contributing in the same direction.

The random error, by contrast, is small and controlled. The position readings are quantised at ±0.5 mm, and
by the midpoint formula this propagates to roughly ±0.015 m/s in each velocity — visible as the mild scatter
about the Method B line ($R^2 = 0.99965$). Method A hides this scatter because its through-origin fit is
stiff over a wide range, which is precisely why its formal uncertainty (0.017) is smaller than Method B's
(0.069) and should not be over-trusted.

The photogate check is the strongest evidence for the systematic-error interpretation: when timing is
done digitally — removing calibration and friction — the result (9.810 ± 0.006) lands essentially on 9.81,
whereas both paper-tape analyses land low. That is exactly the pattern expected if the paper-tape method
carries a small, one-directional instrument bias.

To improve the experiment I would: (i) verify the spark frequency against a known reference or switch
wholly to photogates; (ii) measure a longer fall so the relative effect of the ±0.5 mm reading error at
small $y$ is reduced; and (iii) run more trials to tighten the random component, though this cannot touch
the dominant systematic term.

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-09 |

| Rubric component | Awarded |
|---|---|
| Data table, formatted with units and sig figs | 15 / 15 |
| $y$ vs. $t^2$ plot with linear fit, labeled axes, units | 15 / 15 |
| $v$ vs. $t$ plot with linear fit, labeled axes, units | 15 / 15 |
| Correct $g$ extraction from both methods | 20 / 20 |
| Uncertainty propagation for $g$ | 15 / 15 |
| Part 3 systematic-error discussion | 10 / 10 |
| Comparison with accepted value + discussion | 10 / 10 |
| **Total** | **100 / 100** |

**Feedback:**
Complete and well-reasoned. The data table is correctly formatted with units and the midpoint velocities
are computed with the right formula. Both fits are executed properly: the through-origin fit gives
$g_A = 9.791 \pm 0.017$ and the least-squares $v$–$t$ fit gives $g_B = 9.780 \pm 0.069$ with
$R^2 = 0.99965$; the two agree at 0.15σ. The uncertainty treatment is correct, and — importantly — the
report recognises that Method A's tiny formal $\sigma$ *understates* the true uncertainty because the
dominant terms are systematic. Part 3 answers are physically sound: the directions of the air-resistance,
$v_0>0$, and 59.8 Hz biases are all correct, and Q2 correctly notes that Method B is immune to a nonzero
release velocity while Method A is not. The error-source ranking is sensible and the connection between the
timer calibration, the observed low bias, and the photogate result is exactly the right piece of synthesis.
Full marks.

---
*PHYS 141 · Week 1 · Lab 1 · Adebayo Glover*
