---
assessment: Quiz 0
course: PHYS 141
component: Quizzes
possible: 25
score: 25
status: graded
started: 2026-09-28
submitted: 2026-09-28
graded: 2026-09-29
source: "QUIZ 0 Measurement Units Coordinate Systems Vectors.md"
---

# PHYS 141 · Quiz 0
## Answer Sheet — Measurement, Units, Coordinate Systems & Vectors

**Assessment:** `QUIZ 0 Measurement Units Coordinate Systems Vectors.md`
**Points available:** 25

---

**Q1 (2 pts).** Dimensional homogeneity means every term in a valid equation has the same *dimensions*,
independent of the unit system used. In SI *specifically* is too narrow (it must hold in any consistent
system), and the terms need not share a numerical value.

**Answer: (C)**

*Marks: 2 / 2*

---

**Q2 (2 pts).** In $0.003040$, the leading zeros are **not** significant. Reading from the first nonzero
digit: $3,\,0,\,4,\,0$ — the trailing zero after the decimal point **is** significant.

**Answer: (C) 4**

*Marks: 2 / 2*

---

**Q3 (3 pts).** $v^2 = u^2 + 2as$ with $v,u$ speeds, $a$ acceleration, $s$ displacement.

$$[v^2] = [u^2] = (\mathrm{L}\,\mathrm{T}^{-1})^2 = \mathrm{L}^2\,\mathrm{T}^{-2}.$$
$$[2as] = [a][s] = (\mathrm{L}\,\mathrm{T}^{-2})(\mathrm{L}) = \mathrm{L}^2\,\mathrm{T}^{-2}.$$

All three terms have dimension $\mathrm{L}^2\,\mathrm{T}^{-2}$, and $2$ is dimensionless, so the equation
is **dimensionally consistent**. ✓

*Marks: 3 / 3*

---

**Q4 (2 pts).**

$$45\ \frac{\text{m}}{\text{s}}\times\frac{1\ \text{km}}{1000\ \text{m}}\times\frac{3600\ \text{s}}{1\ \text{h}}
= \frac{45\times3600}{1000}\ \frac{\text{km}}{\text{h}} = \boxed{162\ \text{km/h}}$$

*Marks: 2 / 2*

---

**Q5 (3 pts).** $(x,y) = (0,-5)$ lies on the negative $y$-axis. Then

$$r = \sqrt{0^2+(-5)^2} = 5.$$

For the angle measured counter-clockwise from $+x$, the point is directly "south":

$$\boxed{(r,\theta) = (5,\ 270^\circ)}.$$

*Marks: 3 / 3*

---

**Q6 (2 pts).** $\hat r$ is a unit vector by definition — it is $\vec r/|\vec r|$ — so its magnitude is $1$
for every $\theta$. Its *direction* changes with $\theta$, but its magnitude does not.

**Answer: True**

*Marks: 2 / 2*

---

**Q7 (3 pts).** $\vec A = (3,0,4)$:

$$|\vec A| = \sqrt{3^2+0^2+4^2} = \sqrt{25} = \boxed{5},\qquad
\hat A = \frac{\vec A}{|\vec A|} = \boxed{(0.6,\,0,\,0.8)}.$$

(Check: $0.6^2+0^2+0.8^2 = 0.36+0.64 = 1$. ✓)

*Marks: 3 / 3*

---

**Q8 (3 pts).** $\vec A = (1,0,0) = \hat x$ and $\vec B = (0,0,1) = \hat z$:

$$\vec A\times\vec B =
\begin{vmatrix}
\hat x & \hat y & \hat z\\
1 & 0 & 0\\
0 & 0 & 1
\end{vmatrix}
= (0\cdot1 - 0\cdot0)\hat x - (1\cdot1 - 0\cdot0)\hat y + (1\cdot0 - 0\cdot0)\hat z
= \boxed{(0,-1,0)}.$$

**Right-hand rule:** point the fingers of the right hand along $\hat x$ and curl them toward $\hat z$;
the thumb points along $-\hat y$, matching the computed result. ✓

*Marks: 3 / 3*

---

**Q9 (2 pts).** $\vec A\cdot\vec B = |\vec A||\vec B|\cos\theta = 0$ with both vectors nonzero forces
$\cos\theta = 0$, so $\theta = 90^\circ$: the vectors are **perpendicular**.

*Marks: 2 / 2*

---

**Q10 (3 pts).** $x = 10.0 \pm 0.2$, $y = 5.0 \pm 0.1$, $z = xy$:

$$z = (10.0)(5.0) = 50.0.$$

$$\left(\frac{\sigma_z}{z}\right)^2 = \left(\frac{\sigma_x}{x}\right)^2 + \left(\frac{\sigma_y}{y}\right)^2
= \left(\frac{0.2}{10.0}\right)^2 + \left(\frac{0.1}{5.0}\right)^2 = 0.0004 + 0.0004 = 0.0008.$$

$$\frac{\sigma_z}{z} = \sqrt{0.0008} = 0.02828,\qquad \sigma_z = 0.02828\times50.0 = 1.41 \approx 1.4.$$

$$\boxed{z = 50.0 \pm 1.4}$$

*Marks: 3 / 3*

---

## Grading Summary

| | |
|---|---|
| **Score** | 25 / 25 |
| **Percent** | 100% |
| **Graded** | 2026-09-29 |

**Feedback:**
All ten items correct. The two multiple-choice items (dimensional homogeneity; significant figures of
0.003040) are right and explained. The dimensional check of $v^2=u^2+2as$ shows both sides reduce to
$\mathrm{L}^2\mathrm{T}^{-2}$. The conversion gives 162 km/h with unit cancellation shown. Polar
coordinates of $(0,-5)$ are $(5,270^\circ)$ — the axis case handled correctly. The unit-vector magnitude
item is answered True with the right reason. $|\vec A| = 5$ and $\hat A = (0.6,0,0.8)$ check out, as does
$\vec A\times\vec B = (0,-1,0)$ with the right-hand rule. The perpendicular conclusion comes from
$\cos\theta = 0$. The error propagation gives $\sigma_z/z = \sqrt{0.0008}$ and $z = 50.0 \pm 1.4$. Full
marks.

---
*PHYS 141 · Week 0 · Quiz 0 · Adebayo Glover*
