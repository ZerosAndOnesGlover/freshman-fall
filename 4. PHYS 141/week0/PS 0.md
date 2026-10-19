---
assessment: PS 0
course: PHYS 141
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-09-25
submitted: 2026-10-02
graded: 2026-10-04
source: "PS 0 Measurement Units Coordinate Systems Vectors.md"
---

# PHYS 141 · PS 0
## Answer Sheet — Measurement, Units, Coordinate Systems & Vectors

**Assessment:** `PS 0 Measurement Units Coordinate Systems Vectors.md`
**Points available:** 100 (10 problems × 10)

> Show all work. Every numerical answer carries units and appropriate significant figures.

---

### Problem 1 — SI base units  (10 points)

**(a) Angular momentum, from $\vec{L} = \vec{r}\times\vec{p}$.** The cross product multiplies the
dimensions of its operands:

$$[\vec{L}] = [\vec{r}]\,[\vec{p}] = (\mathrm{L})(\mathrm{M}\,\mathrm{L}\,\mathrm{T}^{-1}) = \mathrm{M}\,\mathrm{L}^2\,\mathrm{T}^{-1}
\;\Rightarrow\; \boxed{\mathrm{kg\,m^2\,s^{-1}}}$$

**(b) Electric field, from $\vec{F} = q\vec{E}$**, so $\vec{E} = \vec{F}/q$ with $[F] = \mathrm{M}\,\mathrm{L}\,\mathrm{T}^{-2}$
and charge $[q] = \mathrm{I}\,\mathrm{T}$:

$$[E] = \frac{\mathrm{M}\,\mathrm{L}\,\mathrm{T}^{-2}}{\mathrm{I}\,\mathrm{T}} = \mathrm{M}\,\mathrm{L}\,\mathrm{T}^{-3}\,\mathrm{I}^{-1}
\;\Rightarrow\; \boxed{\mathrm{kg\,m\,s^{-3}\,A^{-1}}}$$

**(c) Gravitational constant, from $F = Gm_1m_2/r^2$**, so $G = Fr^2/(m_1m_2)$:

$$[G] = \frac{(\mathrm{M}\,\mathrm{L}\,\mathrm{T}^{-2})(\mathrm{L}^2)}{\mathrm{M}^2} = \mathrm{M}^{-1}\,\mathrm{L}^3\,\mathrm{T}^{-2}
\;\Rightarrow\; \boxed{\mathrm{m^3\,kg^{-1}\,s^{-2}}}$$

*Marks: 10 / 10*

---

### Problem 2 — Dimensional analysis of $T = 2\pi\sqrt{m/k}$  (10 points)

$k$ is a spring constant with units $\mathrm{N/m} = (\mathrm{kg\,m/s^2})/\mathrm{m} = \mathrm{kg\,s^{-2}}$.
The argument of the square root is

$$\left[\frac{m}{k}\right] = \frac{\mathrm{kg}}{\mathrm{kg\,s}^{-2}} = \mathrm{s}^2
\quad\Rightarrow\quad \left[\sqrt{\frac{m}{k}}\right] = \mathrm{s}.$$

The left side has $[T] = \mathrm{T} = \mathrm{s}$, and $2\pi$ is dimensionless. Both sides have dimension
$\mathrm{T}$, so the formula is **dimensionally consistent** (and indeed correct — this is the exact period
of an ideal mass–spring oscillator).

*Marks: 10 / 10*

---

### Problem 3 — Conversions  (10 points)

**(a) 88 km/h to m/s:**

$$88\,\frac{\text{km}}{\text{h}}\times\frac{1000\ \text{m}}{1\ \text{km}}\times\frac{1\ \text{h}}{3600\ \text{s}}
= \frac{88\,000}{3600}\ \text{m/s} = \boxed{24.4\ \text{m/s}}$$

**(b) 1 light-year to meters, then miles.** Light travels $c = 2.998\times10^{8}$ m/s, and
$1\ \text{yr} = 3.156\times10^{7}$ s:

$$1\ \text{ly} = (2.998\times10^{8}\ \text{m/s})(3.156\times10^{7}\ \text{s}) = \boxed{9.46\times10^{15}\ \text{m}}$$

In miles (1 mile = 1609.34 m):

$$9.46\times10^{15}\ \text{m}\times\frac{1\ \text{mi}}{1609.34\ \text{m}} = \boxed{5.88\times10^{12}\ \text{mi}}$$

**(c) 1 atm = 101 325 Pa to psi.** Since $1\ \text{Pa} = 1\ \text{N/m}^2$:

$$101\,325\ \frac{\text{N}}{\text{m}^2}\times\frac{1\ \text{lb}}{4.448\ \text{N}} = 2.278\times10^{4}\ \frac{\text{lb}}{\text{m}^2}.$$

Convert square meters to square inches, $(1\ \text{in} = 0.0254\ \text{m})^2 = 6.4516\times10^{-4}\ \text{m}^2$:

$$2.278\times10^{4}\ \frac{\text{lb}}{\text{m}^2}\times\frac{6.4516\times10^{-4}\ \text{m}^2}{1\ \text{in}^2}
= \boxed{14.7\ \text{psi}}$$

(This matches the standard value — a good sanity check.)

*Marks: 10 / 10*

---

### Problem 4 — Kepler's third law by dimensions  (10 points)

Assume $T = C\,r^{a}M^{b}G^{c}$ with $C$ dimensionless. In dimensions
$\mathrm{L}$, $\mathrm{M}$, $\mathrm{T}$:

$$[T] = \mathrm{T},\quad [r]=\mathrm{L},\quad [M]=\mathrm{M},\quad [G]=\mathrm{M}^{-1}\mathrm{L}^{3}\mathrm{T}^{-2}.$$

So the right side has dimensions

$$\mathrm{L}^{a}\,\mathrm{M}^{b}\,(\mathrm{M}^{-1}\mathrm{L}^{3}\mathrm{T}^{-2})^{c}
= \mathrm{L}^{a+3c}\,\mathrm{M}^{b-c}\,\mathrm{T}^{-2c}.$$

Matching exponents to $\mathrm{L}^{0}\mathrm{M}^{0}\mathrm{T}^{1}$:

$$
\begin{cases}
\mathrm{T}: & -2c = 1 \;\Rightarrow\; c = -\tfrac{1}{2}\\[2pt]
\mathrm{M}: & b - c = 0 \;\Rightarrow\; b = c = -\tfrac{1}{2}\\[2pt]
\mathrm{L}: & a + 3c = 0 \;\Rightarrow\; a = -3c = \tfrac{3}{2}
\end{cases}
$$

$$\boxed{T = C\,r^{3/2}M^{-1/2}G^{-1/2} \;\propto\; \sqrt{\frac{r^{3}}{GM}}}$$

This is exactly the structure of **Kepler's third law**, $T^2 \propto r^3/(GM)$ — obtained from
dimensional analysis alone.

*Marks: 10 / 10*

---

### Problem 5 — Significant figures  (10 points)

**(a)** $4.52 \times 3.1 = 14.012$ → limited by the 2 s.f. factor: $\boxed{14}$

**(b)** $18.0 / 3.652 = 4.9288\ldots$ → 3 s.f.: $\boxed{4.93}$

**(c)** $12.65 + 1.2 + 0.075 = 13.925$ → addition is limited by the coarsest decimal place (1 decimal,
from 1.2): $\boxed{13.9}$

**(d)** $(2.50\times10^{3})(1.2\times10^{-5}) = 3.00\times10^{-2}$ → 2 s.f.: $\boxed{3.0\times10^{-2}}$

*Marks: 10 / 10*

---

### Problem 6 — Fermi: mass of Earth's oceans  (10 points)

**Intermediate quantities and assumptions:**

1. **Earth's surface area.** $R_\oplus \approx 6.4\times10^{6}$ m, so
   $A = 4\pi R^2 \approx 4\pi(6.4\times10^6)^2 \approx 5.1\times10^{14}\ \text{m}^2$.
2. **Ocean fraction.** Roughly $70\%$ of the surface: $A_{\text{oc}} \approx 0.7 \times 5.1\times10^{14}
   \approx 3.6\times10^{14}\ \text{m}^2$.
3. **Average depth.** Estimate "a few km"; take $\bar d \approx 3.7\times10^{3}$ m.
4. **Density.** Seawater $\approx 1000\ \text{kg/m}^3$ (order of magnitude).

**Volume:**
$$V \approx A_{\text{oc}}\,\bar d \approx (3.6\times10^{14})(3.7\times10^{3}) \approx 1.3\times10^{18}\ \text{m}^3.$$

**Mass:**
$$M = \rho V \approx (1000)(1.3\times10^{18}) \approx \boxed{1.3\times10^{21}\ \text{kg}}$$

**Comparison.** The accepted value is $\approx 1.4\times10^{21}$ kg. My estimate agrees to the same
order of magnitude and even the leading digit, well within the expected factor-of-a-few from the crude
depth estimate. (The dominant uncertainty is the average depth and the ocean-area fraction.)

*Marks: 10 / 10*

---

### Problem 7 — Cartesian to polar  (10 points)

For $(x,y) = (-3, 4)$:

$$r = \sqrt{x^2+y^2} = \sqrt{9+16} = 5.$$

The point lies in the **second quadrant** ($x<0$, $y>0$), so

$$\theta = \operatorname{atan2}(4,-3) = 180^\circ - \arctan\!\left(\tfrac{4}{3}\right)
= 180^\circ - 53.13^\circ = \boxed{126.87^\circ}.$$

**Answer:** $(r,\theta) = (5,\ 126.9^\circ)$.

*Marks: 10 / 10*

---

### Problem 8 — Why $\hat{\theta}$ is not a constant vector  (10 points)

In polar coordinates the unit vectors are defined **relative to the point's angular position**: $\hat r$
points radially outward, and $\hat\theta$ points in the direction of increasing $\theta$ (tangent to the
circle through that point). As a point moves around the origin, the local "counter-clockwise" direction
*rotates with it* — $\hat\theta$ points in $+y$ at $\theta=0^\circ$, in $-x$ at $\theta=90^\circ$, and so
on. Its **direction depends on position**, so it is not a fixed object.

Cartesian $\hat x$ is the same arrow everywhere: it always points along the $+x$ axis, independent of
where the point is.

**Practical consequence.** In Cartesian, $\hat x$ and $\hat y$ are constants, so differentiating a
position $\vec r = x\hat x + y\hat y$ just differentiates the scalar components. In polar,
$\vec r = r\hat r$, and both $r$ **and** $\hat r$ change with time, so the product rule produces
$\dot{\vec r} = \dot r\,\hat r + r\,\dot{\hat r}$; the term $\dot{\hat r} = \dot\theta\,\hat\theta \neq 0$
generates the extra (centripetal/angular) terms in velocity and acceleration. If one wrongly treats
$\hat r$ as constant, those terms are lost.

*Marks: 10 / 10*

---

### Problem 9 — Angle between two vectors  (10 points)

$\vec A = (1,2,2)$, $\vec B = (2,0,-1)$:

$$\vec A\cdot\vec B = (1)(2) + (2)(0) + (2)(-1) = 2 + 0 - 2 = 0.$$

Since $\cos\theta = \dfrac{\vec A\cdot\vec B}{|\vec A||\vec B|} = 0$, the angle is

$$\boxed{\theta = 90^\circ}$$

(the vectors are perpendicular — the dot product vanishes).

*Marks: 10 / 10*

---

### Problem 10 — Torque as a cross product  (10 points)

Given $\vec F = (0,-20,0)$ N and $\vec r = (0.3,0,0)$ m:

**(a) Torque vector** $\vec\tau = \vec r\times\vec F$:

$$\vec\tau =
\begin{vmatrix}
\hat x & \hat y & \hat z\\
0.3 & 0 & 0\\
0 & -20 & 0
\end{vmatrix}
= \big(0\cdot0 - 0\cdot(-20)\big)\hat x - \big(0.3\cdot0 - 0\cdot0\big)\hat y
+ \big(0.3\cdot(-20) - 0\cdot0\big)\hat z
= \boxed{(0,0,-6)\ \text{N}\cdot\text{m}.}$$

**(b) Magnitude:** $|\vec\tau| = \sqrt{0^2+0^2+(-6)^2} = \boxed{6\ \text{N}\cdot\text{m}}$.

**(c) Force moved to $\vec r = (0,0.3,0)$:**

$$\vec\tau' = (0,0.3,0)\times(0,-20,0) = (0,0,0)\ \Rightarrow\ \boxed{\vec\tau' = 0.}$$

Physically: the cross-product magnitude is $rF\sin\theta$, where $\theta$ is the angle between $\vec r$
and $\vec F$. Here $\vec r$ and $\vec F$ are **both along the $y$-axis — parallel** — so $\theta = 0$ and
$\sin\theta = 0$: the torque vanishes. A push directed straight toward (or away from) the pivot line
produces **no leverage** and no rotation, which is exactly the geometric meaning of the cross product.

*Marks: 10 / 10*

---

## Grading Summary

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-04 |

**Feedback:**
All ten problems complete, correct, and fully justified. Units are carried through the derivations in
Problem 1 rather than asserted, and the exponents fall out of the dimension equations. The dimensional
checks (Problems 2 and 4) are set up symbolically before numbers, and Problem 4 lands on Kepler's third
law. Conversions (Problem 3) show explicit unit cancellation, including the psi result matching the known
value. Significant figures (Problem 5) respect the addition-vs-multiplication rule, and the Fermi estimate
(Problem 6) states every assumption and compares to the accepted figure. Problem 7 handles the second
quadrant correctly; Problem 8 explains the position-dependence of $\hat\theta$ and its consequence for
differentiation; Problems 9–10 are exact, with the zero-torque parallel case explained geometrically.
No errors.

---
*PHYS 141 · Week 0 · Problem Set 0 · Adebayo Glover*
