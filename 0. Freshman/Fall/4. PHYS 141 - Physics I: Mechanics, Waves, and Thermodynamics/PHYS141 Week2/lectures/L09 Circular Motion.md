# PHYS 141 — Lecture 9
# Circular Motion: Uniform and Non-Uniform

> **Core Principle:** An object moving in a circle at constant speed is still accelerating — because its velocity direction is changing. This centripetal acceleration always points toward the center of the circle. It requires a centripetal force (Week 3) and is the reason planets orbit, cars corner, and electrons (classically) circle nuclei.

---


## Where This Fits

**Previously:** **L08** handled projectiles, where acceleration is constant. Circular motion is the first case where acceleration is constant in *magnitude* but continuously changing in *direction*.

---

## 1. Angular Quantities

For circular motion it is natural to describe position by an angle rather than x and y coordinates.

### 1.1 Arc Length and Angle

For a circle of radius r, the arc length s subtended by angle θ (in **radians**):

$$s = r\theta$$

This formula requires θ in radians. One full revolution = 2π radians = 360°.

**Conversion:** θ(rad) = θ(degrees) × π/180

### 1.2 Angular Velocity ω

$$\omega = \frac{d\theta}{dt} \quad \text{[rad/s]}$$

For uniform circular motion, ω is constant. One full revolution in period T gives:

$$\omega = \frac{2\pi}{T} = 2\pi f$$

where f = 1/T is the **frequency** in Hz (cycles per second).

### 1.3 Angular Acceleration α

$$\alpha = \frac{d\omega}{dt} = \frac{d^2\theta}{dt^2} \quad \text{[rad/s}^2\text{]}$$

Zero for uniform circular motion; non-zero for non-uniform circular motion.

---

## 2. Relating Angular and Linear Quantities

At radius r from the center:

| Angular quantity | Linear quantity | Relation |
|-----------------|----------------|---------|
| θ (position) | s (arc length) | s = rθ |
| ω (angular velocity) | v (tangential speed) | v = rω |
| α (angular acceleration) | a_t (tangential acceleration) | a_t = rα |

These relations hold at every instant, even when ω and α are not constant.

---

## 3. Centripetal Acceleration — Derivation

This is one of the most important derivations in introductory physics. Follow it carefully.

### Setup

Consider a particle moving in a circle of radius r at **constant speed** v. At time t, it is at position r⃗₁; a short time Δt later, it is at r⃗₂. The angle swept is Δθ = ωΔt.

### The Velocity Change Vector

At each point, the velocity vector is tangent to the circle — perpendicular to the radius vector. When the particle moves through angle Δθ, the velocity vector also rotates by angle Δθ (since velocity is always perpendicular to radius).

The change in velocity Δv⃗ = v⃗₂ − v⃗₁ forms an isoceles triangle with the two velocity vectors. For small Δθ:

$$|\Delta\vec{v}| \approx v\,\Delta\theta = v\,\omega\,\Delta t$$

### Direction of Δv⃗

For small Δθ, Δv⃗ points **toward the center** of the circle (perpendicular to v⃗ and radially inward).

### Centripetal Acceleration

$$a_c = \lim_{\Delta t \to 0} \frac{|\Delta\vec{v}|}{\Delta t} = v\omega = v\cdot\frac{v}{r} = \frac{v^2}{r}$$

Using v = rω:

$$\boxed{a_c = \frac{v^2}{r} = \omega^2 r} \quad \text{directed toward center}$$

This is the **centripetal acceleration** — it always points radially inward, toward the center of the circle.

> **Deep Why:** Acceleration does not require changing speed. It requires changing velocity — and velocity is a vector. Changing direction at constant speed still constitutes acceleration. This is why a car traveling in a circle at constant speedometer reading is accelerating (the steering wheel is providing centripetal force). Neglecting this is one of the most common conceptual errors in introductory physics.

---

## 4. Uniform Circular Motion — Complete Picture

**Uniform circular motion:** r = constant, v = constant (speed), ω = constant.

| Quantity | Value | Direction |
|---------|-------|-----------|
| Speed |v = rω | — |
| Velocity v⃗ | magnitude v, changes direction | Tangent to circle |
| Centripetal acceleration a⃗_c | v²/r = ω²r | Radially inward (toward center) |
| Angular acceleration α | 0 | — |
| Period T | 2πr/v = 2π/ω | — |
| Frequency f | v/(2πr) = ω/(2π) | — |

**What is NOT changing:** speed, angular speed, radius, magnitude of centripetal acceleration.
**What IS changing:** velocity direction, acceleration direction, angular position.

---

## 5. Position as a Function of Time in UCM

Taking the center of the circle as the origin, with the particle starting at (r, 0) at t = 0:

$$\vec{r}(t) = r\cos(\omega t)\,\hat{x} + r\sin(\omega t)\,\hat{y}$$

Differentiating:
$$\vec{v}(t) = -r\omega\sin(\omega t)\,\hat{x} + r\omega\cos(\omega t)\,\hat{y}$$

Differentiating again:
$$\vec{a}(t) = -r\omega^2\cos(\omega t)\,\hat{x} - r\omega^2\sin(\omega t)\,\hat{y} = -\omega^2\vec{r}(t)$$

The acceleration is proportional to −r⃗: it has magnitude ω²r and points **opposite** to the position vector — i.e., radially inward. This confirms the centripetal acceleration formula and shows it points toward the center at all times.

Note also: v⃗(t) · r⃗(t) = −r²ωsinωtcosωt + r²ωcosωtsinωt = 0. The velocity is always perpendicular to the radius — confirming the tangent direction.

---

## 6. Non-Uniform Circular Motion

When the speed changes (ω is not constant), there is both centripetal acceleration **and** tangential acceleration.

### Total Acceleration

$$\vec{a} = \vec{a}_c + \vec{a}_t$$

where:
- **Centripetal (radial) component:** $a_c = v^2/r = \omega^2 r$, directed **inward**
- **Tangential component:** $a_t = dv/dt = r\alpha$, directed **along the circle** (tangentially, in the direction of increasing speed)

**Magnitude of total acceleration:**
$$|\vec{a}| = \sqrt{a_c^2 + a_t^2}$$

The centripetal component changes direction; the tangential component changes speed. They are always perpendicular to each other.

### Example: A car accelerating around a curve

If a car travels at v = 20 m/s around a curve of radius r = 50 m, and the engine gives it tangential acceleration a_t = 2 m/s²:

- a_c = v²/r = 400/50 = 8 m/s² (inward)
- a_t = 2 m/s² (along curve)
- Total: |a| = √(64+4) = √68 ≈ 8.25 m/s²
- Direction: arctan(2/8) = 14° from the inward radial direction

---

## 7. Angular Kinematic Equations

For **constant angular acceleration** α, the angular quantities obey the same equations as 1D constant-acceleration kinematics:

| Linear (a = const) | Angular (α = const) |
|--------------------|---------------------|
| v = v₀ + at | ω = ω₀ + αt |
| Δx = v₀t + ½at² | Δθ = ω₀t + ½αt² |
| v² = v₀² + 2aΔx | ω² = ω₀² + 2αΔθ |
| Δx = ½(v₀+v)t | Δθ = ½(ω₀+ω)t |

This is not a coincidence — angular motion is defined by the same calculus (differentiation and integration) as linear motion, just applied to the angle θ instead of position x.

---

## 8. Worked Examples

### Example 9.1 — Earth's rotation

Calculate the centripetal acceleration experienced by a person standing on Earth's equator.

r = 6.371 × 10⁶ m; T = 24 × 3600 = 86400 s

$$\omega = \frac{2\pi}{T} = \frac{2\pi}{86400} = 7.272 \times 10^{-5} \text{ rad/s}$$

$$a_c = \omega^2 r = (7.272\times10^{-5})^2 \times 6.371\times10^6 = 5.288\times10^{-9} \times 6.371\times10^6 = \mathbf{0.0337 \text{ m/s}^2}$$

This is about 0.34% of g = 9.81 m/s². This centripetal acceleration is directed toward Earth's rotation axis (not the center), so it slightly reduces the effective gravitational acceleration at the equator — explaining why g_equator ≈ 9.78 m/s² while g_poles ≈ 9.83 m/s².

### Example 9.2 — Spinning wheel

A wheel starts from rest and reaches 1200 rpm in 5.0 s (assume constant α).

**Convert:** 1200 rpm × (2π rad/rev) × (1 min/60 s) = 125.7 rad/s

**(a)** α = Δω/Δt = 125.7/5.0 = **25.1 rad/s²**

**(b)** Angle turned: Δθ = ω₀t + ½αt² = 0 + ½(25.1)(25) = **314 rad** = 50 full revolutions

**(c)** Centripetal acceleration of a point at r = 0.30 m at t = 5.0 s:
a_c = ω²r = (125.7)²(0.30) = 15800 × 0.30 = **4740 m/s²** (≈ 483 g — immense!)

### Example 9.3 — Centripetal vs. tangential in non-uniform circular motion

A car enters a circular on-ramp of radius 80 m at 12 m/s and accelerates at 1.5 m/s². What is the total acceleration when its speed has reached 20 m/s?

$$a_c = v^2/r = 400/80 = 5.0 \text{ m/s}^2$$
$$a_t = 1.5 \text{ m/s}^2$$
$$|\vec{a}| = \sqrt{25 + 2.25} = \sqrt{27.25} \approx \mathbf{5.22 \text{ m/s}^2}$$

Direction: θ = arctan(1.5/5.0) = **16.7°** from radially inward, toward the tangential (forward) direction.

---

## 9. Summary

| Concept | Formula | Notes |
|---------|---------|-------|
| Arc length | s = rθ | θ in radians |
| Tangential speed | v = rω | — |
| Centripetal acceleration | a_c = v²/r = ω²r | Always radially inward |
| Tangential acceleration | a_t = rα = dv/dt | Tangent to circle |
| Total acceleration | \|a\| = √(a_c²+a_t²) | a_c ⊥ a_t |
| Period | T = 2π/ω = 2πr/v | — |
| Angular kinematics | Same structure as linear | Replace x→θ, v→ω, a→α |

---


---

## CS Connection — Centripetal Acceleration and Rotation Matrices

Uniform circular motion is what a rotation matrix generates when applied repeatedly. The fact that acceleration is perpendicular to velocity — changing direction without changing speed — is the geometric statement that rotation preserves magnitude, which is why rotation matrices are orthogonal. CS 322 (Computer Graphics, Year 4) builds on exactly this property.

---

## Looking Ahead

**L10** asks what causes acceleration at all. Everything so far has described motion; Newton's laws explain it.

## Conceptual Questions

1. A car travels at constant speed around a circular track. Is it accelerating? In what direction is the acceleration at the top of the loop? At the bottom? At the side?

2. If the speed of a particle in circular motion doubles, by what factor does the centripetal acceleration change (for fixed radius)? If the radius doubles at fixed speed, by what factor does it change?

3. An object undergoes uniform circular motion. A student says "the net work done by all forces on the object must be zero because the speed isn't changing." Is this reasoning correct? (Anticipates Week 4.)

4. A satellite in low Earth orbit has speed ≈ 7900 m/s and orbital radius ≈ 6.5 × 10⁶ m. Compute its centripetal acceleration. Compare this to g = 9.81 m/s² and comment on what this tells you about the satellite's orbit.
