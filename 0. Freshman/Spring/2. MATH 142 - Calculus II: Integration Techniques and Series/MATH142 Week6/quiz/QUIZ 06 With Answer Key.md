# MATH 142 · Calculus II
## Quiz 06 — With Answer Key
### Week 6 · Monday · **Covers Week 5**

---

**Date:** Monday 1 March 2027 · 11:00–11:15 (start of Lecture 1) · Week 6
**Time:** 15 minutes, start of Monday's lecture
**Closed book, no calculator**
**Total: 20 points** (4 points each)

**Covers Week 5:** parametric curves, calculus with parametric curves, polar coordinates.

---

## Questions

**Q1.** For $x=t^2+1$, $y=t^3-t$, find $\dfrac{dy}{dx}$ at $t=1$.

**Q2.** Find the arc length of $x=\cos t$, $y=\sin t$ for $t\in[0,\pi]$. Say what curve this is.

**Q3.** Find the area enclosed by the cardioid $r = 2(1+\cos\theta)$.

**Q4.** Find the area of **one petal** of the rose $r = 3\cos2\theta$. State the range of $\theta$ you used.

**Q5.** Convert $r = 6\sin\theta$ to Cartesian form and identify the curve.

---
---

# ANSWER KEY

---

**Q1. (4)**

$$\frac{dy}{dx} = \frac{dy/dt}{dx/dt} = \frac{3t^2-1}{2t}\Bigg|_{t=1} = \frac{3-1}{2} = \boxed{1}$$

*Marking: 2 for the formula, 2 for evaluation. **Deduct 2 for $\frac{d^2y}{dt^2}\big/\frac{d^2x}{dt^2}$-style confusion** or for inverting the ratio. Verified symbolically.*

**Q2. (4)** Speed $= \sqrt{\sin^2t+\cos^2t} = 1$, so

$$L = \int_0^\pi 1\,dt = \boxed{\pi}$$

**The curve is the upper half of the unit circle** — a semicircle of radius 1, whose length is indeed $\pi$.

*Marking: 3 for the length, **1 for identifying the curve** (the question asked). Verified symbolically.*

**Q3. (4)**

$$A = \frac12\int_0^{2\pi}4(1+\cos\theta)^2d\theta = 2\int_0^{2\pi}\big(1+2\cos\theta+\cos^2\theta\big)d\theta = 2\big(2\pi+0+\pi\big) = \boxed{6\pi}$$

*Marking: 1 for the $\frac12$, 3 for evaluation. **$\int_0^{2\pi}\cos^2 = \pi$** is the usual slip. Verified symbolically.*

*Consistency check worth mentioning: the standard cardioid $r=1+\cos\theta$ has area $\frac{3\pi}{2}$, and scaling $r$ by 2 multiplies area by $4$: $4\cdot\frac{3\pi}{2}=6\pi$ ✓.*

**Q4. (4)** $r=0$ when $\cos2\theta=0$, i.e. $2\theta=\pm\frac\pi2$, so the petal on the positive $x$-axis is traced for

$$\theta\in\left[-\frac\pi4,\ \frac\pi4\right]$$

$$A = \frac12\int_{-\pi/4}^{\pi/4}9\cos^22\theta\,d\theta = \boxed{\frac{9\pi}{8}}$$

*Marking: **2 of the 4 for the range with its justification.** Integrating over $[0,2\pi]$ gives $\frac{9\pi}{2}$ — the whole four-petalled rose, four times too much. Verified symbolically.*

**Q5. (4)** Multiply by $r$:

$$r^2 = 6r\sin\theta \implies x^2+y^2 = 6y \implies \boxed{x^2+(y-3)^2 = 9}$$

**A circle of radius 3 centred at $(0,3)$**, passing through the origin.

*Marking: 2 for the "multiply by $r$" step, 1 for completing the square, 1 for identifying it.*

---

## Marking Summary

| Question | Points | Tests |
|---|---|---|
| Q1 | 4 | Parametric slope |
| Q2 | 4 | Parametric arc length |
| Q3 | 4 | Polar area, the $\frac12$ |
| Q4 | 4 | Polar limits — the hard part |
| Q5 | 4 | Polar → Cartesian |
| **Total** | **20** | |

---

## Note for the Instructor

**Q4 is the diagnostic**, and it is the same error as PS 5 C2: integrating a petal over the full $[0,2\pi]$.

**This is the last quiz on the first half of the course.** From today the subject is sequences and series, and the failure modes change completely — from *wrong limits of integration* to *unjustified conclusions*. Worth saying so explicitly when returning these: the students who have been getting by on careful computation are about to need a different skill, and the ones who have been struggling with algebra may find the next six weeks easier.

---

*MATH 142 · Week 6 · Quiz 06 · covers Week 5*
