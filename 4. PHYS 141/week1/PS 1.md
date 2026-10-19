---
assessment: PS 1
course: PHYS 141
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-02
submitted: 2026-10-09
graded: 2026-10-10
source: "PS 1 Kinematics in One Dimension.md"
---

# PHYS 141 · PS 1
## Answer Sheet — Kinematics in One Dimension

**Assessment:** `PS 1 Kinematics in One Dimension.md`
**Points available:** 100 (10 problems × 10)

> Coordinate system stated in every problem. All answers carry units and significant figures.

---

### Problem 1 — Position, velocity, derivative  (10 points)

$x(t) = 4t^3 - 9t^2 + 3$ (m, $t$ in s). **Coordinate:** $+x$ in the direction of increasing position.

**(a)** Differentiate:

$$v(t) = \frac{dx}{dt} = 12t^2 - 18t \quad (\text{m/s}).$$

**(b)** The particle is momentarily at rest when $v(t) = 0$:

$$12t^2 - 18t = 6t(2t - 3) = 0 \;\Rightarrow\; \boxed{t = 0\ \text{s} \ \text{and}\ t = 1.5\ \text{s}}.$$

*Marks: 10 / 10*

---

### Problem 2 — Average velocity vs. average speed  (10 points)

**Coordinate:** east positive. Leg 1: $+400$ m in 80 s. Leg 2: $-150$ m in 40 s.

**(a)** Displacement and elapsed time:

$$\Delta x = 400 - 150 = +250\ \text{m},\qquad \Delta t = 80 + 40 = 120\ \text{s},$$
$$v_{\text{avg}} = \frac{\Delta x}{\Delta t} = \frac{250}{120} = \boxed{+2.08\ \text{m/s}\ \text{(east)}}.$$

**(b)** Average speed uses **path length**, not displacement:

$$d = 400 + 150 = 550\ \text{m},\qquad \text{avg speed} = \frac{550}{120} = \boxed{4.58\ \text{m/s}}.$$

The two differ because the jogger reverses direction; only the net change counts for velocity.

*Marks: 10 / 10*

---

### Problem 3 — Acceleration and integration  (10 points)

$v(t) = 6t^2 - 4t$ (m/s), $x(0) = 2$ m.

**(a)** Acceleration is the derivative of velocity:

$$a(t) = \frac{dv}{dt} = 12t - 4 \quad (\text{m/s}^2).$$

**(b)** Integrate velocity, then fix the constant from the initial condition:

$$x(t) = \int (6t^2 - 4t)\,dt = 2t^3 - 2t^2 + C.$$

At $t = 0$, $x = 2$, so $C = 2$:

$$\boxed{x(t) = 2t^3 - 2t^2 + 2 \ (\text{m})}.$$

*Marks: 10 / 10*

---

### Problem 4 — Uniform deceleration  (10 points)

$v_0 = 20$ m/s, $v = 0$, $t = 4.0$ s. **Coordinate:** initial direction of motion positive.

**(a)** Constant acceleration:

$$a = \frac{v - v_0}{t} = \frac{0 - 20}{4.0} = \boxed{-5.0\ \text{m/s}^2}.$$

**(b)** Stopping distance:

$$\Delta x = v_0 t + \tfrac{1}{2}at^2 = 20(4.0) + \tfrac{1}{2}(-5.0)(4.0)^2 = 80 - 40 = \boxed{40\ \text{m}}.$$

**Check** (time-free equation): $v^2 = v_0^2 + 2a\Delta x \Rightarrow 0 = 400 - 10\,\Delta x \Rightarrow \Delta x = 40$ m. ✓

*Marks: 10 / 10*

---

### Problem 5 — Two cars  (10 points)

**Coordinate:** origin at Car A's start, forward positive. Car A: $x_A = \tfrac{1}{2}(4.0)t^2 = 2t^2$.
Car B starts 50 m ahead at constant speed: $x_B = 50 + 15t$.

**(a)** Set positions equal:

$$2t^2 = 50 + 15t \;\Rightarrow\; 2t^2 - 15t - 50 = 0$$
$$t = \frac{15 \pm \sqrt{225 + 400}}{4} = \frac{15 \pm 25}{4}.$$

Taking the physical (positive) root: $\boxed{t = 10\ \text{s}}$.

**(b)** Car A's speed at that instant:

$$v_A = a_A t = (4.0)(10) = \boxed{40\ \text{m/s}}.$$

(The meeting point is $x = 2(10)^2 = 200$ m from A's start, which also equals $50 + 15(10)$ for B. ✓)

*Marks: 10 / 10*

---

### Problem 6 — Quadratic reasoning  (10 points)

$x_0 = 0$, $v_0 = +10$ m/s, $a = -2.0$ m/s². **Coordinate:** initial direction positive.

**(a)** Set $x = +12$ m:

$$12 = 10t - t^2 \;\Rightarrow\; t^2 - 10t + 12 = 0 \;\Rightarrow\; t = \frac{10 \pm \sqrt{100 - 48}}{2} = \frac{10 \pm 7.21}{2}.$$

$$\boxed{t_1 = 1.39\ \text{s}\ \text{and}\ t_2 = 8.61\ \text{s}}.$$

The particle reaches $x = +12$ m **twice**: first on the way up ($t_1$, moving in $+x$), then again on
the way back down ($t_2$, moving in $-x$).

**(b)** Return to $x = 0$:

$$10t - t^2 = 0 \;\Rightarrow\; t(10 - t) = 0 \;\Rightarrow\; \boxed{t = 10\ \text{s}}\ \text{(the non-trivial root)}.$$

$$v(10) = 10 - 2.0(10) = \boxed{-10\ \text{m/s}}.$$

The speed equals the launch value — by the symmetry of constant acceleration about the turning point.

*Marks: 10 / 10*

---

### Problem 7 — Free fall from a cliff  (10 points)

Drop from rest, $t = 3.5$ s. **Coordinate:** downward positive, origin at the release point, $a = +9.81$ m/s².

**(a)** Height of the cliff:

$$h = \tfrac{1}{2}gt^2 = \tfrac{1}{2}(9.81)(3.5)^2 = \tfrac{1}{2}(9.81)(12.25) = \boxed{60.1\ \text{m}}.$$

**(b)** Impact speed:

$$v = gt = (9.81)(3.5) = \boxed{34.3\ \text{m/s}}.$$

*Marks: 10 / 10*

---

### Problem 8 — Ball thrown upward  (10 points)

$v_0 = +18$ m/s from ground level. **Coordinate:** up positive, origin at ground, $a = -9.81$ m/s².

**(a)** Maximum height (where $v = 0$):

$$h_{\max} = \frac{v_0^2}{2g} = \frac{(18)^2}{2(9.81)} = \frac{324}{19.62} = \boxed{16.5\ \text{m}}.$$

**(b)** Total time in the air (returns to $y = 0$):

$$0 = v_0 t - \tfrac{1}{2}gt^2 = t\left(v_0 - \tfrac{1}{2}gt\right) \;\Rightarrow\; t = \frac{2v_0}{g} = \frac{2(18)}{9.81} = \boxed{3.67\ \text{s}}.$$

(This is twice the rise time $t_{\text{top}} = 18/9.81 = 1.83$ s. ✓)

*Marks: 10 / 10*

---

### Problem 9 — Thrown up from a building  (10 points)

$v_0 = +12$ m/s from the top of a 30 m building. **Coordinate:** origin at the launch point, up positive;
ground is at $y = -30$ m, $a = -9.81$ m/s².

**(a)** Set $y = -30$ m:

$$-30 = 12t - \tfrac{1}{2}(9.81)t^2 \;\Rightarrow\; 4.905\,t^2 - 12t - 30 = 0$$
$$t = \frac{12 \pm \sqrt{144 + 588.6}}{9.81} = \frac{12 \pm 27.07}{9.81}.$$

The positive root: $\boxed{t = 3.98\ \text{s}}$.

**(b)** Impact speed from the time-free equation:

$$v^2 = v_0^2 + 2a\Delta y = (12)^2 + 2(-9.81)(-30) = 144 + 588.6 = 732.6,$$
$$|v| = \sqrt{732.6} = \boxed{27.1\ \text{m/s}\ \text{(downward)}}.$$

*Marks: 10 / 10*

---

### Problem 10 — Two balls (synthesis)  (10 points)

**Coordinate:** origin at ground, up positive. Ball 1 is dropped from height $H$; Ball 2 is thrown upward
from the ground with speed $v_0$, at the same instant.

$$y_1 = H - \tfrac{1}{2}gt^2, \qquad y_2 = v_0 t - \tfrac{1}{2}gt^2.$$

**(a)** They meet when $y_1 = y_2$:

$$H - \tfrac{1}{2}gt^2 = v_0 t - \tfrac{1}{2}gt^2 \;\Rightarrow\; H = v_0 t \;\Rightarrow\; \boxed{t = \frac{H}{v_0}}.$$

The $\tfrac{1}{2}gt^2$ terms cancel: both balls share the same gravitational acceleration, so their
*relative* motion is uniform.

**(b)** Ball 1 hits the ground at $t_g = \sqrt{2H/g}$. The meeting must occur first:

$$t_{\text{meet}} < t_g \;\Rightarrow\; \frac{H}{v_0} < \sqrt{\frac{2H}{g}} \;\Rightarrow\; v_0 > \sqrt{\frac{gH}{2}}.$$

$$\boxed{v_0 > \sqrt{\frac{gH}{2}}}$$

(For $H = 20$ m this gives $v_0 > \sqrt{9.81 \times 10} = \sqrt{98.1} = 9.90$ m/s.)

*Marks: 10 / 10*

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-10 |

**Feedback:**
All ten problems complete and correct with explicit coordinate systems. The derivative/integration
problems (1, 3) are handled symbolically, and the constant of integration is fixed from the initial
condition. Problem 2 keeps displacement and path length distinct, giving both 2.08 m/s and 4.58 m/s.
Problems 4–6 show symbolic setup before substitution, and the stopping distance is cross-checked with the
time-free equation. Problem 6 interprets both roots physically (up-leg and down-leg) as required. The free-
fall set (7–9) uses consistent sign conventions, and Problem 9 keeps the origin at the launch point while
placing the ground at $-30$ m — correctly. Problem 10 is exact: the cancellation of the $\tfrac{1}{2}gt^2$
terms yields $t = H/v_0$, and the condition $v_0 > \sqrt{gH/2}$ follows from requiring the meet before
Ball 1 lands. Units and significant figures are correct throughout. Full marks.

---
*PHYS 141 · Week 1 · Problem Set 1 · Adebayo Glover*
