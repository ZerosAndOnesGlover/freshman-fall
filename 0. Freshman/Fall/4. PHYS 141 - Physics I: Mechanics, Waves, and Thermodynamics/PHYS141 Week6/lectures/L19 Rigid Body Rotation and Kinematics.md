# PHYS 141 · Lecture 19
# Rigid Body Rotation & Rotational Kinematics

*“The mathematical difficulties of the theory of rotation arise chiefly from the want of geometrical illustrations and sensible images, by which we might fix the results of analysis in our minds.”* — James Clerk Maxwell, "On a Dynamical Top" (1857)

> **Core Principle:** A rigid body is an idealized object whose particles maintain fixed distances from one another — it can translate and rotate, but not deform. Every particle in a rotating rigid body shares the same angular velocity and angular acceleration, even though different particles have different linear speeds. This shared angular description is what makes rotational mechanics tractable.

**Date:** Monday 2 November 2026 · 14:00–14:50 · Week 6

**Reading:** Serway & Jewett §10.1–10.3 · HRK Ch. 8

**Coursework:** 📊 **Quiz 5** today 14:00 · 🔬 **Lab 6** Thu 5 Nov 14:00–17:00 · 📝 **PS 5** due Fri 6 Nov 17:00 · 📝 **PS 6** released Fri 6 Nov 15:00, due Fri 13 Nov 17:00

---


## Where This Fits

**Previously:** **L18** established the centre of mass, letting extended bodies be treated as points for translation. Rotation is the part that treatment throws away.

---

## 1. The Rigid Body Model

A **rigid body** is a system of particles whose relative positions never change. Real objects deform under stress, but for most everyday solids under normal loads, the rigid body approximation is excellent.

### Why This Matters for Rotation

When a rigid body rotates about a fixed axis, every particle within it moves in a circle, but particles at different distances from the axis have different **linear** speeds — yet all particles share the **same angular** speed. This is the key simplification: instead of tracking every particle's individual linear motion, we track a single angular variable θ(t) that describes the whole body's orientation.

---

## 2. Angular Position, Velocity, and Acceleration — Formal Definitions

These were introduced in Week 2 (Lecture 9) for a point particle in circular motion; here we formalize them for an extended rigid body rotating about a fixed axis.

### 2.1 Angular Position θ

The angle (in radians) that a reference line on the rotating body makes with a fixed reference direction. As the body rotates, θ(t) changes.

### 2.2 Angular Velocity ω

$$\omega = \frac{d\theta}{dt}$$

Every point in the rigid body has the same ω at a given instant — this is the defining feature of rigid-body rotation. Units: rad/s.

**Direction (vector nature of ω):** Although we often treat ω as a scalar for rotation about a single fixed axis, angular velocity is properly a vector, with direction given by the **right-hand rule**: curl the fingers of your right hand in the direction of rotation; your thumb points along ω⃗. For rotation in the xy-plane (counterclockwise viewed from +z), ω⃗ points in the +z direction.

### 2.3 Angular Acceleration α

$$\alpha = \frac{d\omega}{dt} = \frac{d^2\theta}{dt^2}$$

Units: rad/s². Like ω, α is technically a vector, parallel or antiparallel to ω⃗ depending on whether the rotation is speeding up or slowing down.

---

## 3. The Complete Analogy: Linear ↔ Angular

This table is one of the most useful tools in rotational mechanics — nearly every linear equation has a direct rotational counterpart, because both descriptions come from applying the same calculus (differentiation/integration) to a different variable.

| Linear quantity | Symbol | Angular quantity | Symbol | Relation (at radius r) |
|-----------------|--------|-------------------|--------|--------------------------|
| Position | x | Angular position | θ | x = rθ (arc length) |
| Velocity | v | Angular velocity | ω | v = rω |
| Acceleration | a | Angular acceleration | α | a_tangential = rα |
| Mass | m | Moment of inertia | I | (Week 6, Lecture 20) |
| Force | F | Torque | τ | (Week 6, Lecture 20) |
| Momentum | p = mv | Angular momentum | L = Iω | (Week 7) |
| Kinetic energy | ½mv² | Rotational KE | ½Iω² | (Lecture 21) |

---

## 4. Angular Kinematic Equations (Constant α)

Exactly as in Week 1 (linear case) and Week 2 (introduced), for **constant angular acceleration**:

$$\omega(t) = \omega_0 + \alpha t$$
$$\theta(t) = \theta_0 + \omega_0 t + \frac{1}{2}\alpha t^2$$
$$\omega^2 = \omega_0^2 + 2\alpha\Delta\theta$$
$$\Delta\theta = \frac{1}{2}(\omega_0+\omega)t$$

These are derived by exactly the same integration process as the linear kinematic equations in Week 1, Lecture 5 — replace x → θ, v → ω, a → α throughout the derivation, and the algebra is identical.

**Critical restriction (same as linear case):** these equations apply ONLY when α is constant.

---

## 5. Relating Linear and Angular Quantities for a Point on a Rotating Body

For a point at distance r from the rotation axis:

**Position (arc length from reference):**
$$s = r\theta$$

**Tangential velocity:**
$$v_t = r\omega$$

**Tangential acceleration (speeding up/slowing down along the circular path):**
$$a_t = r\alpha$$

**Centripetal (radial) acceleration (always present in circular motion, even at constant ω):**
$$a_c = \frac{v_t^2}{r} = \omega^2 r$$

**Total linear acceleration of the point:**
$$\vec{a} = \vec{a}_t + \vec{a}_c \qquad |\vec{a}| = \sqrt{a_t^2+a_c^2}$$

This exactly reproduces the non-uniform circular motion result from Week 2, Lecture 9 — now understood as a special case of rigid body rotation about a fixed axis.

---

## 6. Converting Between rpm, Hz, and rad/s

Rotational speed is often given in **revolutions per minute (rpm)** in practical contexts (engines, hard drives, centrifuges). Converting to the SI-consistent rad/s is essential before using any of the formulas above.

$$\omega \text{[rad/s]} = n\text{[rpm]} \times \frac{2\pi \text{ rad}}{1 \text{ rev}} \times \frac{1\text{ min}}{60\text{ s}} = n \times \frac{\pi}{30}$$

**Frequency** f (in Hz, cycles per second) relates to ω via:
$$\omega = 2\pi f$$

**Period** T (time for one revolution):
$$T = \frac{2\pi}{\omega} = \frac{1}{f}$$

---

## 7. Worked Examples

### Example 19.1 — Basic angular kinematics

A wheel starts at rest and accelerates uniformly to 15 rad/s over 6.0 s.

**(a)** Angular acceleration: α = Δω/t = 15/6.0 = **2.5 rad/s²**

**(b)** Angular displacement: Δθ = ½αt² = ½(2.5)(36) = **45 rad** (= 7.16 revolutions)

**(c)** If the wheel has radius 0.30 m, the tangential speed of a point on the rim at t=6.0 s: v = rω = 0.30×15 = **4.5 m/s**

---

### Example 19.2 — Converting rpm and finding centripetal acceleration

A hard drive platter spins at 7200 rpm. Find the angular velocity in rad/s, and the centripetal acceleration of a point 0.030 m from the center.

$$\omega = 7200 \times \frac{\pi}{30} = 7200 \times 0.1047 = 753.98 \text{ rad/s}$$

$$a_c = \omega^2 r = (753.98)^2 \times 0.030 = 568{,}487 \times 0.030 = \mathbf{17{,}055 \text{ m/s}^2 \approx 1740\,g}$$

This immense centripetal acceleration (over 1700 times Earth's gravity) is why hard drive platters must be extremely well-balanced and manufactured to precise tolerances — even tiny mass imperfections would generate large vibrational forces at these speeds.

---

### Example 19.3 — Combining tangential and centripetal acceleration

A flywheel of radius 0.50 m has angular velocity 8.0 rad/s and angular acceleration 3.0 rad/s² at a given instant. Find the total linear acceleration of a point on the rim.

$$a_t = r\alpha = 0.50 \times 3.0 = 1.5 \text{ m/s}^2$$
$$a_c = \omega^2 r = (8.0)^2 \times 0.50 = 32.0 \text{ m/s}^2$$
$$|\vec a| = \sqrt{a_t^2+a_c^2} = \sqrt{2.25+1024} = \sqrt{1026.25} = \mathbf{32.03 \text{ m/s}^2}$$

Notice that a_c completely dominates: at even moderate ω, centripetal acceleration typically far exceeds tangential acceleration, because a_c grows with ω² while a_t depends only on α.

---

### Example 19.4 — Angular displacement with non-constant reasoning check

A CD-ROM slows from 500 rpm to 200 rpm while making 50 complete revolutions. Find the angular acceleration (assumed constant), and the time this takes.

Convert: ω₀ = 500×π/30 = 52.36 rad/s; ω = 200×π/30 = 20.94 rad/s; Δθ = 50×2π = 314.16 rad

Using $\omega^2 = \omega_0^2+2\alpha\Delta\theta$:
$$（20.94)^2 = (52.36)^2 + 2\alpha(314.16)$$
$$438.5 = 2741.6 + 628.32\alpha$$
$$\alpha = \frac{438.5-2741.6}{628.32} = \frac{-2303.1}{628.32} = \mathbf{-3.666 \text{ rad/s}^2}$$

Time: using $\omega = \omega_0+\alpha t$: $t = (20.94-52.36)/(-3.666) = -31.42/-3.666 = \mathbf{8.57 \text{ s}}$

---

## 8. Summary

| Concept | Formula | Key Point |
|---------|---------|-----------|
| Angular velocity | ω = dθ/dt | Same for every particle in a rigid body |
| Angular acceleration | α = dω/dt | Same for every particle in a rigid body |
| Linear-angular link | v=rω, a_t=rα, a_c=ω²r | r = distance from rotation axis |
| Angular kinematic equations | Same structure as linear (Week 1) | Valid only for constant α |
| rpm to rad/s | ω = n×π/30 | Always convert before using formulas |

---


---

## CS Connection — Angular Kinematics as a Parallel API

Every rotational quantity mirrors a linear one — θ↔x, ω↔v, α↔a — and the kinematic equations are identical in form. This is a shared interface with two implementations, and once you notice it, everything you learned in L04–L06 transfers directly. Recognising that two domains share structure is the same move as factoring a common interface out of two classes.

---

## Looking Ahead

**L20** supplies the rotational analogue of force: torque, and with it the rotational form of Newton's second law.

## Conceptual Questions

1. Two points on a rotating wheel are at different distances from the axis. Do they have the same angular velocity? The same linear speed? The same centripetal acceleration?

2. A wheel rotates at constant ω (no angular acceleration). Does a point on the rim have zero acceleration? Explain using both a_t and a_c.

3. If you double the radius of a point on a rotating rigid body (moving it further from the axis) while ω stays fixed, how do v, a_t, and a_c each change?

4. A rigid body's angular velocity vector points in the +z direction. Using the right-hand rule, describe the sense of rotation (clockwise or counterclockwise) when viewed from the +z axis looking down at the xy-plane.
