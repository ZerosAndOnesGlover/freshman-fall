# PHYS 141 · Lecture 22
# Angular Momentum

*“The areas, which revolving bodies describe by radii drawn to an immovable centre of force do lie in the same immovable planes, and are proportional to the times in which they are described.”* — Isaac Newton, *Principia* (1687), Book I, Proposition I, tr. Motte

> **Core Principle:** Angular momentum is to rotation what linear momentum is to translation — a conserved quantity in isolated systems, arising directly from Newton's laws applied to rotational motion. Just as net external force changes linear momentum, net external torque changes angular momentum. This single relationship explains phenomena from spinning skaters to planetary orbits to gyroscopic stability.

**Date:** Monday 9 November 2026 · 14:00–14:50 · Week 7

**Reading:** Serway & Jewett §11.1–11.3 · HRK Ch. 10

**Coursework:** 📊 **Quiz 6** today 14:00 · 🔬 **Lab 7** Thu 12 Nov 14:00–17:00 · 📝 **PS 6** due Fri 13 Nov 17:00 · 📝 **PS 7** released Fri 13 Nov 15:00, due Fri 20 Nov 17:00

---


## Where This Fits

**Previously:** **L21** completed rotational energy. Angular momentum is the rotational counterpart of linear momentum from L16, and the last of the great conserved quantities in this course.

---

## 1. Angular Momentum of a Point Particle

For a particle with position r⃗ (measured from a chosen origin/axis) and momentum p⃗ = mv⃗:

$$\vec{L} = \vec{r}\times\vec{p} = m(\vec{r}\times\vec{v})$$

**Magnitude:**
$$L = rp\sin\phi = mvr\sin\phi$$

where φ is the angle between r⃗ and p⃗ (or equivalently between r⃗ and v⃗, since p⃗ is parallel to v⃗).

**SI unit:** kg·m²/s (equivalently, J·s)

### 1.1 Special Case: Circular Motion

If a particle moves in a circle of radius r with speed v (so r⃗ ⊥ v⃗, φ=90°):

$$L = mvr = m(r\omega)r = mr^2\omega$$

This matches $L = I\omega$ with $I=mr^2$ (the single-particle moment of inertia from Week 6) — confirming consistency between the particle definition and the rigid-body definition below.

### 1.2 Angular Momentum Depends on the Choice of Origin

Just as torque is defined relative to a pivot point, angular momentum is defined relative to a chosen origin. A particle moving in a straight line (no circular motion at all!) can still have nonzero angular momentum about a point NOT on its line of motion — this is a common point of confusion, addressed in the worked examples below.

---

## 2. Angular Momentum of a Rigid Body

For a rigid body rotating about a fixed axis with angular velocity ω, each particle $i$ at distance $r_i$ contributes angular momentum $m_ir_i^2\omega$ (using the circular motion special case, since every particle in a rotating rigid body moves in a circle about the axis). Summing:

$$L = \sum_i m_ir_i^2\omega = \omega\sum_im_ir_i^2 = I\omega$$

$$\boxed{L = I\omega}$$

This is the rigid-body form we will use most often — the direct rotational analog of $p=mv$.

---

## 3. Newton's Second Law for Rotation, in Angular Momentum Form

Recall from Week 6 that $\tau = I\alpha$. Since $\alpha = d\omega/dt$ and (for a rigid body with constant I) $L=I\omega$:

$$\tau = I\frac{d\omega}{dt} = \frac{d(I\omega)}{dt} = \frac{dL}{dt}$$

$$\boxed{\tau_{net} = \frac{dL}{dt}}$$

This is the exact rotational analog of $F_{net} = dp/dt$ from Week 5 (Lecture 16). It is, in fact, the MORE fundamental and general form of Newton's second law for rotation — valid even when I itself changes with time (as in a spinning skater pulling in their arms), a case where $\tau=I\alpha$ in its simple form breaks down but $\tau = dL/dt$ remains valid.

> **Deep Why — why the L-form is more general:** If I changes with time (mass redistributing relative to the axis, as when a skater's arms move in or out), then $\frac{d(I\omega)}{dt} = I\frac{d\omega}{dt} + \omega\frac{dI}{dt} \neq I\alpha$ alone. The extra term $\omega \, dI/dt$ is essential for correctly describing systems with changing moment of inertia. This exactly parallels the momentum-form of Newton's second law being more general than F=ma when mass itself changes (Week 5, Lecture 16, rocket equation note).

---

## 4. Worked Examples — Computing Angular Momentum

### Example 22.1 — Particle in circular motion

A 0.50 kg particle moves in a circle of radius 2.0 m at 4.0 m/s. Find its angular momentum about the center of the circle.

$$L = mvr = 0.50\times4.0\times2.0 = \mathbf{4.0 \text{ kg·m}^2/\text{s}}$$

---

### Example 22.2 — Particle moving in a straight line (the subtle case)

A 2.0 kg particle moves in a straight line along y = 3.0 m (parallel to the x-axis) with velocity 5.0 m/s in the +x direction. Find its angular momentum about the origin (0,0).

Even though the particle never moves in a circle, it still has angular momentum about the origin because its straight-line path does not pass through the origin.

$$\vec{r} = (x, 3.0, 0), \quad \vec{v} = (5.0, 0, 0)$$

$$\vec{L} = m(\vec{r}\times\vec{v}) = m\begin{vmatrix}\hat x&\hat y&\hat z\\x&3.0&0\\5.0&0&0\end{vmatrix} = m[(3.0\times0-0\times0)\hat x - (x\times0-0\times5.0)\hat y+(x\times0-3.0\times5.0)\hat z]$$

$$= m[0-0-15.0\hat z] = 2.0\times(-15.0)\hat z = \mathbf{-30 \text{ kg·m}^2/\text{s} \, \hat z}$$

**Key insight:** L is constant (−30 kg·m²/s ẑ) regardless of the particle's x-position — because as x changes, the perpendicular distance from the origin to the line of motion (which is what matters for the cross product) stays exactly 3.0 m. This is a general fact: a particle moving at constant velocity in a straight line has CONSTANT angular momentum about any fixed point, even though it's not "rotating" in any everyday sense. This makes sense: with no net torque about the origin (gravity/other forces aside — assume free particle), angular momentum must be conserved, consistent with $\tau=dL/dt=0$.

---

### Example 22.3 — Rigid body angular momentum

A solid disk (M=3.0 kg, R=0.25 m) spins at ω=15 rad/s. Find its angular momentum.

$$I = \frac{1}{2}MR^2 = \frac{1}{2}(3.0)(0.0625) = 0.09375 \text{ kg·m}^2$$
$$L = I\omega = 0.09375\times15 = \mathbf{1.406 \text{ kg·m}^2/\text{s}}$$

---

### Example 22.4 — Torque from angular momentum rate of change

A rotating system's angular momentum increases from 5.0 kg·m²/s to 12.0 kg·m²/s over 3.5 s. Find the average net torque.

$$\bar\tau = \frac{\Delta L}{\Delta t} = \frac{12.0-5.0}{3.5} = \frac{7.0}{3.5} = \mathbf{2.0 \text{ N·m}}$$

---

## 5. Angular Momentum About Different Axes — A Word of Caution

For a rigid body, L=Iω applies about a fixed rotation axis. If a body has both translational AND rotational motion (like a rolling ball), its total angular momentum about a point NOT on the axis of rotation includes a contribution from the translational motion of the center of mass, in addition to the "spin" angular momentum Iω about the center of mass:

$$L_{total} = L_{cm,spin} + \vec{r}_{cm}\times M\vec{v}_{cm}$$

This decomposition (spin + orbital angular momentum) is standard in more advanced treatments; for this course, we primarily deal with simple rotation about a fixed axis where $L=I\omega$ suffices directly.

---

## 6. Summary

| Concept | Formula | Key Point |
|---------|---------|-----------|
| Angular momentum (particle) | L⃗ = r⃗×p⃗; L=mvr sinφ | Depends on choice of origin |
| Angular momentum (rigid body) | L = Iω | Direct rotational analog of p=mv |
| Newton's 2nd law (rotation, general) | τ_net = dL/dt | More general than τ=Iα; valid even if I changes |
| Straight-line motion | Can have nonzero, constant L about an off-line point | No contradiction — L constant with zero torque |

---


---

## CS Connection — Angular Momentum and Cross Products

L = r × p makes angular momentum the first genuinely three-dimensional quantity in the course — the cross product produces a vector perpendicular to both inputs, with a direction given by the right-hand rule. Cross products are everywhere in graphics: surface normals, back-face culling, and the torque a physics engine applies to spin a rigid body.

---

## Looking Ahead

**L23** applies its conservation law, which produces some of the most counter-intuitive results in mechanics.

## Conceptual Questions

1. A particle moves in a straight line that passes directly through the chosen origin. What is its angular momentum about that origin? Explain using both the geometric (r sinφ) and cross-product definitions.

2. Why is $\tau=dL/dt$ described as "more fundamental" than $\tau=I\alpha$? Under what specific circumstance do the two forms disagree?

3. A comet moves in a highly elliptical orbit around the Sun. Is the comet's angular momentum about the Sun constant throughout its orbit, even though its speed changes dramatically (fast near the Sun, slow far away)? What does this imply about the relationship between the comet's speed and its distance from the Sun at any two points in the orbit? (This is Kepler's Second Law — we will return to it in the context of conservation of angular momentum next lecture.)

4. Two identical particles move in circles of different radii but with the same angular momentum about the center. If one has twice the radius of the other, how do their speeds compare?
