---
assessment: PS 2
course: PHYS 141
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-09
submitted: 2026-10-16
graded: 2026-10-17
source: "PS 2 Kinematics 2D Projectile and Circular Motion.md"
---

# PHYS 141 · PS 2
## Answer Sheet — 2D Kinematics, Projectile Motion & Circular Motion

**Assessment:** `PS 2 Kinematics 2D Projectile and Circular Motion.md`
**Points available:** 100 (10 problems × 10)

> Establish your coordinate system explicitly. Show all work. Report answers with correct units and significant figures.

---

### Problem 1 — Position vector in 2D  (10 points)

$\vec{r}(t) = (2t^2 - 3t)\,\hat{x} + (t^3 - 4t)\,\hat{y}$ m.

**(a)** $\vec{v}(t)=\frac{d\vec{r}}{dt}=(4t-3)\,\hat{x}+(3t^2-4)\,\hat{y}$ m/s; $\vec{a}(t)=\frac{d\vec{v}}{dt}=4\,\hat{x}+6t\,\hat{y}$ m/s².

**(b)** At $t=2$ s, $\vec{v}(2)=5\,\hat{x}+8\,\hat{y}$ m/s. $v=\sqrt{5^2+8^2}=\sqrt{89}=\boxed{9.43\ \text{m/s}}$. Direction $\theta=\arctan(8/5)=\boxed{58.0^\circ\ \text{above }+x}$.

*Marks: 10 / 10*

---

### Problem 2 — River crossing  (10 points)

$x$: across; $y$: downstream. $v_{bw}=4.0\,\hat{x}$ m/s, $v_w=(0,2.5)$ m/s.

**(a)** $\vec{v}_{bg}=(4.0,2.5)$ m/s. $v=\sqrt{4.0^2+2.5^2}=\sqrt{22.25}=\boxed{4.72\ \text{m/s}}$. $\theta=\arctan(2.5/4.0)=\boxed{32.0^\circ\ \text{downstream of perpendicular}}$.

**(b)** Cross time $t=120/(4.0\cos\phi)$, drift $d=(4.0\sin\phi+2.5)t=120\sin\phi/\cos\phi + 2.5\times120/(4.0\cos\phi)=120\tan\phi + 75/\cos\phi$. To go straight across need no drift: aim upstream so that perpendicular component is 4.0 m/s and downstream component of boat cancels current: $4.0\sin\phi=2.5 \implies \sin\phi=0.625 \implies \phi=\boxed{38.7^\circ\ \text{upstream of perpendicular}}$. Possible since $2.5<4.0$. Cross speed $4.0\cos\phi=4.0\times0.781=\boxed{3.12\ \text{m/s}}$; drift downstream if aimed perpendicular is $2.5\times30=\boxed{75\ \text{m}}$.

*Marks: 10 / 10*

---

### Problem 3 — Projectile launched at 60°  (10 points)

$v_0=20$ m/s, $\theta=60^\circ$. $v_{0x}=20\cos60°=10$ m/s; $v_{0y}=20\sin60°=17.32$ m/s.

**(a)** Time of flight $T=\frac{2v_{0y}}{g}=\frac{34.64}{9.81}=\boxed{3.53\ \text{s}}$.

**(b)** Range $R=v_{0x}T=10\times3.53=\boxed{35.3\ \text{m}}$.

*Marks: 10 / 10*

---

### Problem 4 — Horizontal throw from cliff  (10 points)

$v_0=15$ m/s horizontal, $v_{0y}=0$, $h=45$ m.

**(a)** $h=\frac{1}{2}gt^2 \implies t=\sqrt{2h/g}=\sqrt{90/9.81}=\boxed{3.03\ \text{s}}$.

**(b)** $v_x=15$ m/s constant; $v_y=gt=29.7$ m/s downward. $v=\sqrt{15^2+29.7^2}=\sqrt{225+882.1}=\sqrt{1107.1}=\boxed{33.3\ \text{m/s}\ \text{at }63.2^\circ\ \text{below horizontal}}$.

*Marks: 10 / 10*

---

### Problem 5 — Projectile range equations  (10 points)

$v_0=35$ m/s, $R=80$ m.

**(a)** $R=\frac{v_0^2\sin2\theta}{g}\implies \sin2\theta=\frac{Rg}{v_0^2}=\frac{80\times9.81}{1225}=0.6416$. $2\theta=40.0^\circ$ or $140.0^\circ \implies \theta=\boxed{20.0^\circ,\ 70.0^\circ}$.

**(b)** $T=\frac{2v_{0}\sin\theta}{g}$. $\theta=20.0^\circ: T=\frac{2(35)(0.3420)}{9.81}=\frac{23.94}{9.81}=\boxed{2.44\ \text{s}}$. $\theta=70.0^\circ: \sin70.0^\circ=0.9397, T=\frac{2(35)(0.9397)}{9.81}=\frac{65.78}{9.81}=\boxed{6.71\ \text{s}}$.

*Marks: 10 / 10*

---

### Problem 6 — Thrown down from building  (10 points)

$v_0=15$ m/s at $30^\circ$ below horizontal, $v_{0x}=15\cos30°=13.0$ m/s, $v_{0y}=15\sin30°=7.50$ m/s downward (take down positive), $h=20$ m.

**(a)** $x(t)=v_{0x}t=13.0\,t$; $y(t)=v_{0y}t+\frac{1}{2}gt^2=7.50t+4.905t^2$.

**(b)** $y=20$: $4.905t^2+7.50t-20=0$. $t=\frac{-7.50+\sqrt{7.50^2+4(4.905)(20)}}{9.81}=\frac{-7.50+\sqrt{56.25+392.4}}{9.81}=\frac{-7.50+21.18}{9.81}=\boxed{1.40\ \text{s}}$.

**(c)** $x=13.0\times1.40=\boxed{18.2\ \text{m}}$.

**(d)** $v_x=13.0$ m/s, $v_y=v_{0y}+gt=7.50+9.81(1.40)=7.50+13.73=\boxed{21.2\ \text{m/s}\ \text{downward}}$; $v=\sqrt{13.0^2+21.2^2}=\sqrt{169+449.4}=\sqrt{618.4}=\boxed{24.9\ \text{m/s}\ \text{at }58.5^\circ\ \text{below horizontal}}$.

*Marks: 10 / 10*

---

### Problem 7 — Circular motion  (10 points)

$r=0.40$ m, $n=300$ rpm.

**(a)** $\omega=2\pi n/60=2\pi\times300/60=2\pi\times5=10\pi=\boxed{31.4\ \text{rad/s}}$.

**(b)** $v=\omega r=31.4\times0.40=\boxed{12.6\ \text{m/s}}$.

**(c)** $a_c=\omega^2 r=(986)\times0.40=\boxed{394\ \text{m/s}^2}$ toward center.

**(d)** $a_c/g=394/9.81=\boxed{40.2\,g}$.

*Marks: 10 / 10*

---

### Problem 8 — Moon orbit  (10 points)

$T=27.3$ days $=27.3\times86400=2.358\times10^6$ s; $r=3.84\times10^8$ m.

**(a)** $v=2\pi r/T=2\pi\times3.84\times10^8/2.358\times10^6=\boxed{1.02\times10^3\ \text{m/s}}$.

**(b)** $a_c=v^2/r=(1.046\times10^6)/(3.84\times10^8)=\boxed{2.72\times10^{-3}\ \text{m/s}^2}$.

**(c)** $g'\propto 1/r^2$: $g'(r)=g(R_E)(R_E/r)^2=9.81\times(6.37\times10^6/3.84\times10^8)^2=9.81\times(0.01659)^2=9.81\times2.752\times10^{-4}=\boxed{2.70\times10^{-3}\ \text{m/s}^2}$. Matches $a_c$ — shows gravitational force provides centripetal acceleration.

*Marks: 10 / 10*

---

### Problem 9 — Rotation with angular acceleration  (10 points)

$\omega_0=0$, $\omega=25$ rad/s, $t=10$ s, $r=0.20$ m.

**(a)** $\alpha=(\omega-\omega_0)/t=25/10=\boxed{2.5\ \text{rad/s}^2}$.

**(b)** $\Delta\theta=\frac{1}{2}\alpha t^2=125$ rad. Revolutions $=125/(2\pi)=\boxed{19.9\ \text{rev}}$.

**(c)** $v_t=\omega r=5.0$ m/s; $a_t=\alpha r=0.50$ m/s²; $a_c=\omega^2 r=625\times0.20=125$ m/s². Tangential 0.50 m/s² along velocity, centripetal 125 m/s² radially inward.

**(d)** $a=\sqrt{a_c^2+a_t^2}=\sqrt{125^2+0.50^2}=\sqrt{15625+0.25}=\sqrt{15625.3}=\boxed{125\ \text{m/s}^2}$ (dominated by centripetal; angle $\arctan(a_t/a_c)\approx 0.23^\circ$ tangentially relative to radially inward).

*Marks: 10 / 10*

---

### Problem 10 — Satellite in orbit  (10 points)

$h=400$ km, $r=r_E+h=6.771\times10^6$ m.

**(a)** $g(r)=g(r_E)(r_E/r)^2=9.81\times(0.9409)^2=9.81\times0.8853=\boxed{8.69\ \text{m/s}^2}$.

**(b)** $v=\sqrt{g(r)\cdot r}=\sqrt{8.69\times6.771\times10^6}=\sqrt{5.884\times10^7}=\boxed{7.67\times10^3\ \text{m/s}}$.

**(c)** $T=2\pi r/v=2\pi\times6.771\times10^6/7.67\times10^3=\frac{4.254\times10^7}{7.67\times10^3}=\boxed{5.55\times10^3\ \text{s}=92.4\ \text{min}}$ (matches ISS).

**(d)** Equatorial surface: $a_c=\omega^2 r_E=(7.272\times10^{-5})^2\times6.371\times10^6=(5.288\times10^{-9})\times6.371\times10^6=\boxed{3.37\times10^{-2}\ \text{m/s}^2}\simeq 0.34\%\ of g$.

*Marks: 10 / 10*

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-17 |

**Feedback:** All 2D kinematics, projectile, and circular motion problems correct. River crossing gives correct angle, speed, and drift. All projectile calculations (flight times, range, heights, velocities at impact/peak) show correct components and physical reasoning. Circular motion (ω, v, a_c, g’s) and satellite/rotating disk solved correctly. Conventions explicit; units and sig figs correct.

---
*PHYS 141 · Week 2 · Problem Set 2 · Adebayo Glover*
