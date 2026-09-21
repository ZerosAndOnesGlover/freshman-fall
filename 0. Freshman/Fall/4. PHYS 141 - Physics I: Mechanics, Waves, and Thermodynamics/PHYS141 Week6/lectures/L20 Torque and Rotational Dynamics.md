# PHYS 141 · Lecture 20
# Torque & Rotational Dynamics

> **Core Principle:** Torque is the rotational analog of force — it is what causes angular acceleration. Just as F = ma governs linear motion, τ = Iα governs rotational motion, where the moment of inertia I plays the role of "rotational mass," quantifying how the mass of an object is distributed relative to the rotation axis.

**Date:** Tuesday 3 November 2026 · 14:00–14:50 · Week 6

---


## Where This Fits

**Previously:** **L19** gave rotational kinematics. Torque is what causes angular acceleration, completing the parallel with L10's F = ma.

---

## 1. Torque — Definition

Recall from Week 0 (Lecture 3) that torque is defined as a cross product:

$$\vec{\tau} = \vec{r}\times\vec{F}$$

where r⃗ is the position vector from the rotation axis (or pivot point) to the point where the force is applied, and F⃗ is the applied force.

**Magnitude:**
$$\tau = rF\sin\phi$$

where φ is the angle between r⃗ and F⃗.

**SI unit:** N·m (dimensionally the same as the Joule, but torque is NOT energy — it's a distinct vector quantity, and we never call torque "Joules")

### 1.1 The Lever Arm Interpretation

Define the **lever arm** (or moment arm) $d = r\sin\phi$ — the perpendicular distance from the rotation axis to the line of action of the force. Then:

$$\tau = Fd$$

**This is the most practically useful form of the torque equation.** Only the component of force perpendicular to r⃗ contributes to torque; a force pointing directly along r⃗ (toward or away from the pivot) produces zero torque, no matter how large.

### 1.2 Sign Convention

By convention, counterclockwise torques are positive, clockwise torques are negative (consistent with the right-hand rule: counterclockwise rotation corresponds to angular velocity/torque pointing out of the page, in +z).

---

## 2. Torque from Multiple Forces — Net Torque

Just as net force determines linear acceleration, **net torque** determines angular acceleration:

$$\tau_{net} = \sum_i \tau_i$$

Multiple forces applied to a rigid body each contribute their own torque (computed about the same pivot point), and these add algebraically (with sign).

---

## 3. Newton's Second Law for Rotation — Derivation

We derive τ = Iα from F = ma applied to a single particle undergoing circular motion, then generalize to an extended rigid body.

### 3.1 Single Particle

Consider a particle of mass m at distance r from a rotation axis, constrained to move in a circle (e.g., attached by a massless rigid rod). A tangential force $F_t$ produces tangential acceleration:

$$F_t = ma_t = mr\alpha \quad \text{(using } a_t = r\alpha \text{ from Lecture 19)}$$

Multiply both sides by r:

$$F_t r = mr^2\alpha$$

The left side, $F_t r$, is exactly the torque (since $F_t$ is perpendicular to r⃗ by construction — it's the tangential component):

$$\tau = mr^2\alpha$$

Define $I = mr^2$ for this single particle — the **moment of inertia**.

$$\boxed{\tau = I\alpha}$$

### 3.2 Extended Rigid Body

For a rigid body made of many particles (or a continuous mass distribution), each particle $i$ at distance $r_i$ from the axis contributes $\tau_i = m_ir_i^2\alpha$ (same α for all particles, since it's a rigid body). Summing over all particles:

$$\tau_{net} = \sum_i m_ir_i^2\alpha = \alpha\sum_i m_ir_i^2$$

Define the **moment of inertia of the whole body**:

$$\boxed{I = \sum_i m_ir_i^2} \quad \text{(discrete)} \qquad \boxed{I = \int r^2\,dm} \quad \text{(continuous)}$$

This gives the general result:

$$\boxed{\tau_{net} = I\alpha}$$

> **Deep Why:** Moment of inertia is NOT just "the mass" of a rotating object — it depends on how that mass is distributed relative to the axis, weighted by the square of the distance. This is why a figure skater spins faster when pulling their arms in (reducing the average r, hence reducing I) — a phenomenon we formalize with angular momentum conservation next week. The r² dependence (not just r) means mass far from the axis contributes disproportionately to rotational inertia.

---

## 4. Moment of Inertia — Standard Shapes

Computing I from the integral $\int r^2\,dm$ requires calculus for each shape. The results for common uniform objects (rotating about an axis through the center of mass, unless noted) are:

| Shape | Axis | Moment of Inertia |
|-------|------|---------------------|
| Point mass at radius r | — | $I = mr^2$ |
| Thin hoop/ring (radius R) | Through center, ⊥ to plane | $I = MR^2$ |
| Solid disk/cylinder (radius R) | Through center, along axis | $I = \frac{1}{2}MR^2$ |
| Solid sphere (radius R) | Through center | $I = \frac{2}{5}MR^2$ |
| Thin spherical shell (radius R) | Through center | $I = \frac{2}{3}MR^2$ |
| Thin rod (length L) | Through center, ⊥ to rod | $I = \frac{1}{12}ML^2$ |
| Thin rod (length L) | Through one end, ⊥ to rod | $I = \frac{1}{3}ML^2$ |
| Rectangular plate (sides a, b) | Through center, ⊥ to plate | $I = \frac{1}{12}M(a^2+b^2)$ |

### Sample Derivation: Thin Rod About Its Center

Let the rod have length L, mass M, uniform linear density $\lambda = M/L$, centered at the origin (extending from $-L/2$ to $+L/2$).

$$I = \int_{-L/2}^{L/2} x^2\,\lambda\,dx = \lambda\left[\frac{x^3}{3}\right]_{-L/2}^{L/2} = \frac{\lambda}{3}\left[\left(\frac{L}{2}\right)^3-\left(-\frac{L}{2}\right)^3\right] = \frac{\lambda}{3}\cdot\frac{L^3}{4} = \frac{\lambda L^3}{12}$$

Substituting $\lambda = M/L$:

$$I = \frac{ML^2}{12}$$

matching the table.

---

## 5. The Parallel Axis Theorem

Often you need the moment of inertia about an axis that does NOT pass through the center of mass. The **parallel axis theorem** provides a shortcut:

$$\boxed{I = I_{cm} + Md^2}$$

where $I_{cm}$ is the moment of inertia about a parallel axis through the center of mass, M is the total mass, and d is the perpendicular distance between the two parallel axes.

### Example: Rod About One End

Using the parallel axis theorem with $I_{cm} = ML^2/12$ (center) and $d = L/2$ (distance from center to end):

$$I_{end} = \frac{ML^2}{12} + M\left(\frac{L}{2}\right)^2 = \frac{ML^2}{12}+\frac{ML^2}{4} = \frac{ML^2}{12}+\frac{3ML^2}{12} = \frac{4ML^2}{12} = \frac{ML^2}{3}$$

confirming the table entry for a rod about its end.

> **Deep Why:** The parallel axis theorem tells us that the moment of inertia is always minimized when the axis passes through the center of mass — moving the axis away always increases I (since $Md^2 \geq 0$). This makes physical sense: the center of mass is, in a specific sense, the "balance point" of the mass distribution, and rotating about it requires the least rotational inertia.

---

## 6. Worked Examples

### Example 20.1 — Torque from a single force

A wrench applies a 40 N force perpendicular to its handle, at a distance of 0.25 m from the bolt. Find the torque.

$$\tau = Fd = 40 \times 0.25 = \mathbf{10.0 \text{ N·m}}$$

### Example 20.2 — Torque at an angle

The same wrench applies 40 N at 30° from the handle direction (not perpendicular), at the same 0.25 m distance.

$$\tau = rF\sin\phi = 0.25 \times 40 \times \sin30° = 0.25\times40\times0.5 = \mathbf{5.0 \text{ N·m}}$$

Note this is exactly half the perpendicular case — a direct consequence of sin30° = 0.5. Applying force at an angle other than 90° to the lever arm always reduces effective torque.

### Example 20.3 — Net torque from multiple forces; find angular acceleration

A uniform disk (M = 4.0 kg, R = 0.30 m, $I=\frac{1}{2}MR^2$) can rotate about its central axis. A rope wrapped around its rim exerts a tangential force of 15 N. Find the angular acceleration.

$$I = \frac{1}{2}(4.0)(0.30)^2 = \frac{1}{2}(4.0)(0.09) = 0.18 \text{ kg·m}^2$$
$$\tau = FR = 15 \times 0.30 = 4.5 \text{ N·m}$$
$$\alpha = \frac{\tau}{I} = \frac{4.5}{0.18} = \mathbf{25.0 \text{ rad/s}^2}$$

### Example 20.4 — Using the parallel axis theorem

A uniform disk of mass 2.0 kg and radius 0.20 m rotates about an axis through its edge (not the center). Find its moment of inertia about this axis.

$$I_{cm} = \frac{1}{2}MR^2 = \frac{1}{2}(2.0)(0.04) = 0.04 \text{ kg·m}^2$$
$$I_{edge} = I_{cm} + Md^2 = 0.04 + 2.0(0.20)^2 = 0.04+0.08 = \mathbf{0.12 \text{ kg·m}^2}$$

### Example 20.5 — Two-object system (pulley with mass)

Revisit the Atwood machine (Week 3) but now the pulley has mass $M_p = 0.50$ kg and radius $R=0.10$ m (treat as a uniform disk, $I=\frac{1}{2}M_pR^2$). Masses $m_1=2.0$ kg and $m_2=3.0$ kg hang on either side. Find the acceleration.

**Key new physics:** The pulley now has rotational inertia — the string tension differs on either side of the pulley (T₁ ≠ T₂) because a net torque is needed to angularly accelerate the pulley.

**For m₁ (up positive):** $T_1 - m_1g = m_1a$
**For m₂ (down positive):** $m_2g - T_2 = m_2a$
**For pulley:** $\tau_{net} = I\alpha \implies (T_2-T_1)R = I\alpha = I\frac{a}{R}$ (using $a=R\alpha$, no slipping)

$$T_2 - T_1 = \frac{Ia}{R^2} = \frac{\frac{1}{2}M_pR^2 \cdot a}{R^2} = \frac{1}{2}M_p a$$

Adding all three equations (the T's partially cancel):
$$m_2g - m_1g = m_1a + m_2a + \frac{1}{2}M_pa$$

$$\boxed{a = \frac{(m_2-m_1)g}{m_1+m_2+\frac{1}{2}M_p}}$$

$$a = \frac{(3.0-2.0)(9.81)}{2.0+3.0+0.25} = \frac{9.81}{5.25} = \mathbf{1.87 \text{ m/s}^2}$$

Compare to the massless-pulley result (Week 3): $a = (1.0)(9.81)/5.0 = 1.962$ m/s². The massive pulley **reduces** the acceleration, because some of the released gravitational PE now goes into spinning up the pulley itself, not just accelerating the two masses.

---

## 7. Summary

| Concept | Formula | Key Point |
|---------|---------|-----------|
| Torque | τ⃗ = r⃗ × F⃗; τ = rF sinφ = Fd | d = lever arm = perpendicular distance |
| Newton's 2nd Law (rotation) | τ_net = Iα | Direct analog of F=ma |
| Moment of inertia (discrete) | I = Σmᵢrᵢ² | Depends on mass distribution, not just total mass |
| Moment of inertia (continuous) | I = ∫r²dm | Requires integration for exact shapes |
| Parallel axis theorem | I = I_cm + Md² | I is minimized through the center of mass |

---


---

## CS Connection — Moment of Inertia as Configuration-Dependent Cost

Mass is a fixed property; moment of inertia depends on the axis you rotate about. The same object has different I about different axes, which is why the axis must always be stated. This is the physical version of a cost that depends on access pattern rather than on the data alone — the same array is cheap or expensive to traverse depending on the direction you walk it, because of cache layout.

---

## Looking Ahead

**L21** brings energy methods into rotation, mirroring L13–L15.

## Conceptual Questions

1. Why does a longer wrench handle make it easier to loosen a stuck bolt? Explain using the lever arm concept.

2. Two disks have the same mass and radius, but one is solid and one is a thin hoop (all mass at the rim). Which has a larger moment of inertia about the central axis? Use this to predict which would be harder to spin up with the same applied torque.

3. A force is applied exactly at the pivot point of a rotating object (r = 0). What is the torque, regardless of the force's magnitude or direction? Explain physically why pushing directly at a hinge produces no rotation.

4. Explain, using τ = Iα, why a massive pulley (with nonzero I) causes the tension to differ on either side of an Atwood machine's string, whereas a massless pulley (I=0) always has equal tension throughout.
