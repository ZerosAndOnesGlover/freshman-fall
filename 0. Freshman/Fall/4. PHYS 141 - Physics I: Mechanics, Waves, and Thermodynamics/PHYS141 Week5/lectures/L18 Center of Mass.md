# PHYS 141 · Lecture 18
# Center of Mass

*“In any triangle the centre of gravity lies on the straight line joining any angle to the middle point of the opposite side.”* — Archimedes, *On the Equilibrium of Planes*, Book I, Proposition 13

> **Core Principle:** Every extended object or system of particles has a single point — the center of mass — that behaves, for the purposes of translational motion, exactly like a single point particle carrying the system's entire mass. This is why we can treat complicated, extended, even rotating or exploding objects as point masses when analyzing their overall trajectory.

**Date:** Friday 30 October 2026 · 14:00–14:50 · Week 5

**Reading:** Serway & Jewett §9.6–9.7 · HRK Ch. 7

**Coursework:** 📝 **PS 4** due today 17:00 · 📝 **PS 5** released today 15:00, due Fri 6 Nov 17:00 · 📊 **Quiz 5** Mon 2 Nov 14:00 · 🔬 **Lab 6** Thu 5 Nov 14:00–17:00

---


## Where This Fits

**Previously:** **L17** treated colliding objects as points. Real objects are extended, and the centre of mass is the point that makes them behave like points.

---

## 1. Center of Mass — Definition for Discrete Particles

For a system of N particles with masses $m_1, m_2, \ldots, m_N$ at positions $\vec r_1, \vec r_2, \ldots, \vec r_N$:

$$\vec{r}_{cm} = \frac{\sum_i m_i \vec{r}_i}{\sum_i m_i} = \frac{m_1\vec{r}_1 + m_2\vec{r}_2 + \cdots + m_N\vec{r}_N}{m_1+m_2+\cdots+m_N}$$

In component form:

$$x_{cm} = \frac{\sum_i m_i x_i}{M} \qquad y_{cm} = \frac{\sum_i m_i y_i}{M} \qquad z_{cm} = \frac{\sum_i m_i z_i}{M}$$

where $M = \sum_i m_i$ is the total mass.

### Interpretation

The center of mass is a **mass-weighted average position**. Points with more mass "pull" the center of mass toward them more strongly, just as more numerous data points pull a statistical average.

---

## 2. Center of Mass for Continuous Objects

For a continuous mass distribution, sums become integrals:

$$x_{cm} = \frac{1}{M}\int x\,dm \qquad y_{cm} = \frac{1}{M}\int y\,dm \qquad z_{cm} = \frac{1}{M}\int z\,dm$$

### Symmetry Shortcut

For any object with a symmetric mass distribution (uniform density and geometric symmetry), the center of mass lies on the axis/plane/point of symmetry. This lets you skip the integral entirely for common shapes:

| Shape | Center of mass location |
|-------|-------------------------|
| Uniform rod | Midpoint |
| Uniform disk or sphere | Center |
| Uniform rectangular plate | Geometric center |
| Uniform triangle | Centroid (average of vertices; 1/3 of the way from each side to the opposite vertex) |

---

## 3. Worked Example — Discrete Particles

### Example 18.1

Three masses lie in the xy-plane: $m_1=2.0$ kg at (0,0), $m_2=3.0$ kg at (4,0), $m_3=5.0$ kg at (2,6). Find the center of mass.

$$x_{cm} = \frac{2.0(0)+3.0(4)+5.0(2)}{2.0+3.0+5.0} = \frac{0+12+10}{10} = \frac{22}{10} = \mathbf{2.2 \text{ m}}$$

$$y_{cm} = \frac{2.0(0)+3.0(0)+5.0(6)}{10} = \frac{0+0+30}{10} = \mathbf{3.0 \text{ m}}$$

**Center of mass at (2.2, 3.0) m.**

---

## 4. Worked Example — Continuous Object (Enrichment, Uses Integration)

### Example 18.2 — Center of mass of a non-uniform rod

A rod of length L lies along the x-axis from x=0 to x=L, with linear mass density (mass per unit length) $\lambda(x) = \lambda_0 x/L$ (density increases linearly from 0 at one end to $\lambda_0$ at the other).

**Total mass:**
$$M = \int_0^L \lambda(x)\,dx = \int_0^L \frac{\lambda_0 x}{L}\,dx = \frac{\lambda_0}{L}\left[\frac{x^2}{2}\right]_0^L = \frac{\lambda_0 L}{2}$$

**Center of mass:**
$$x_{cm} = \frac{1}{M}\int_0^L x\cdot\lambda(x)\,dx = \frac{1}{M}\int_0^L x\cdot\frac{\lambda_0 x}{L}\,dx = \frac{1}{M}\cdot\frac{\lambda_0}{L}\int_0^L x^2\,dx = \frac{1}{M}\cdot\frac{\lambda_0}{L}\cdot\frac{L^3}{3} = \frac{\lambda_0 L^2}{3M}$$

Substituting $M = \lambda_0 L/2$:
$$x_{cm} = \frac{\lambda_0 L^2/3}{\lambda_0 L/2} = \frac{L^2/3}{L/2} = \frac{2L}{3}$$

**The center of mass is at 2L/3 from the light end** — shifted toward the denser (heavier) end, as expected. If the density were uniform, we'd get L/2 (midpoint) — a useful check.

---

## 5. Motion of the Center of Mass

This is the payoff for defining center of mass at all. Differentiate the definition with respect to time:

$$\vec{v}_{cm} = \frac{d\vec{r}_{cm}}{dt} = \frac{\sum_i m_i \vec{v}_i}{M} = \frac{\vec{p}_{total}}{M}$$

Rearranging: $\vec p_{total} = M\vec v_{cm}$ — **the total momentum of a system equals the total mass times the velocity of the center of mass.** This is a remarkably clean result: no matter how complicated the individual motions of the constituent particles are, the total momentum behaves as if all the mass were concentrated at the center of mass, moving at $\vec v_{cm}$.

### Differentiate again:

$$\vec{a}_{cm} = \frac{d\vec{v}_{cm}}{dt} = \frac{\sum_i m_i\vec{a}_i}{M} = \frac{\sum_i \vec{F}_i}{M}$$

Now, the sum of forces on all particles includes both **internal forces** (particles acting on each other within the system) and **external forces** (from outside the system). By Newton's Third Law, all internal forces cancel in pairs (exactly as in the momentum conservation derivation). Only external forces survive:

$$\boxed{\vec{F}_{ext,net} = M\vec{a}_{cm}}$$

> **Deep Why — this is the single most important idea in this lecture:** The center of mass of ANY system — no matter how many particles, how complicated their individual paths, whether they're colliding, exploding, or rotating amongst themselves — moves exactly as if it were a single point particle of mass M subject only to the **net external force**. Internal forces (collisions, explosions, internal stresses) can never change the center of mass's trajectory. This is why, for example, a spinning wrench thrown through the air has its center of mass follow a perfect parabola, even while the wrench itself tumbles chaotically.

---

## 6. Center of Mass and Conservation of Momentum — Unified View

If $\vec F_{ext,net} = 0$ (isolated system, no external forces): then $\vec a_{cm} = 0$, meaning $\vec v_{cm}$ is **constant**. This immediately implies $\vec p_{total} = M\vec v_{cm}$ is also constant — which is exactly conservation of momentum from Lecture 17. The two ideas are two sides of the same coin.

---

## 7. Worked Examples — Motion of the Center of Mass

### Example 18.3 — Exploding projectile

A projectile is launched and follows a parabolic trajectory. At the peak of its flight, it explodes into two equal-mass fragments. One fragment falls straight down immediately after the explosion (zero horizontal velocity right after explosion). Describe the motion of the center of mass and find where the second fragment lands, given the unexploded projectile would have landed at x = 100 m from launch, and the explosion occurs exactly at the midpoint of the flight (x = 50 m).

**Key insight:** The explosion is entirely due to internal forces. The center of mass is unaffected — it continues to follow the SAME parabolic path the original unexploded projectile would have followed, landing at x = 100 m.

Since the fragments have equal mass, and the center of mass must land at x=100 m: if fragment 1 falls straight down (landing directly below the explosion point, at x=50 m), then by the definition of center of mass:

$$x_{cm} = \frac{m(50) + m(x_2)}{2m} = 100 \implies 50+x_2 = 200 \implies x_2 = \mathbf{150 \text{ m}}$$

**The second fragment lands at x=150 m** — this follows purely from the center-of-mass argument, without needing to know anything about the explosion forces, timing, or fragment velocities in detail.

---

### Example 18.4 — Two skaters pushing apart

Two ice skaters (masses 50 kg and 70 kg), initially at rest, push off from each other. Find the ratio of their speeds, and describe the motion of their combined center of mass throughout.

Since the system starts at rest with no external horizontal forces (ice is frictionless), $\vec p_{total} = 0$ throughout, and $\vec v_{cm} = 0$ **for all time** — the center of mass never moves, even as the skaters fly apart in opposite directions.

Momentum conservation: $0 = m_1v_1 + m_2v_2 \implies 50v_1 = -70v_2 \implies \frac{v_1}{v_2} = -\frac{70}{50} = -1.4$

**The lighter skater (50 kg) moves 1.4× faster than the heavier skater (70 kg), in the opposite direction** — consistent with conceptual question 4 from Lecture 17, now derived rigorously via center of mass.

---

## 8. Summary

| Concept | Formula | Key Point |
|---------|---------|-----------|
| Center of mass (discrete) | r⃗_cm = Σmᵢr⃗ᵢ/M | Mass-weighted average position |
| Center of mass (continuous) | r⃗_cm = (1/M)∫r⃗ dm | Use symmetry shortcuts when possible |
| CM velocity | v⃗_cm = p⃗_total/M | Total momentum behaves as if concentrated at CM |
| CM acceleration | F⃗_ext,net = Ma⃗_cm | Only EXTERNAL forces affect CM motion; internal forces cancel |
| Isolated system | v⃗_cm = constant | Direct restatement of momentum conservation |

---


---

## CS Connection — Centre of Mass as a Weighted Average

The centre of mass is a mass-weighted mean of positions — the same computation as a centroid in k-means clustering, or a weighted average in any aggregation pipeline. The theorem that the centre of mass moves as if all external force acted there is the justification for treating a complex body as a single point, which is the physical version of abstraction: replace the internals with one representative value.

---

## Looking Ahead

**L19** turns to what extended bodies do that points cannot: rotate.

## Conceptual Questions

1. A gymnast performs a complicated somersault while airborne, with arms and legs moving wildly. Describe the path of their center of mass during the jump. Does it matter how complicated their body motion is?

2. A boat and a person are both initially at rest, with the person standing at one end of the boat (system isolated — frictionless water, no external horizontal forces). The person walks to the other end of the boat. Does the boat move? Does the center of mass of the person+boat system move? Explain the distinction carefully.

3. Why does the center of mass of a horseshoe (or any object with a hole/concave shape) lie outside the physical material of the object itself? Does this violate any physical principle?

4. A firework shell explodes into many fragments while in flight. Assuming no air resistance, is the vector sum of all fragment momenta immediately after the explosion equal to the momentum the shell had immediately before the explosion? Justify using Newton's Third Law applied to the explosion's internal forces.
