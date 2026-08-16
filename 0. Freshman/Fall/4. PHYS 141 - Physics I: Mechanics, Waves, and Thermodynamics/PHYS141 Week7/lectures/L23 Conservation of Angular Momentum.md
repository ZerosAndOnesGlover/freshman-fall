# PHYS 141 · Lecture 23
# Conservation of Angular Momentum

> **Core Principle:** When the net external torque on a system is zero, its total angular momentum is exactly conserved. This single principle explains the spinning skater speeding up as they pull in their arms, the stability of gyroscopes and bicycle wheels, and the way orbiting bodies sweep out equal areas in equal times. It is as fundamental to rotational mechanics as linear momentum conservation is to translational mechanics.

**Date:** Tuesday 6 October 2026 · 14:00–14:50 · Week 7

---


## Where This Fits

**Previously:** **L22** defined angular momentum. When no external torque acts, it is conserved — and because I can change, ω must change to compensate.

---

## 1. Conservation of Angular Momentum — Derivation

From Lecture 22: $\tau_{net} = \dfrac{dL}{dt}$

If the net external torque is zero:

$$\tau_{net}=0 \implies \frac{dL}{dt}=0 \implies L = \text{constant}$$

$$\boxed{L_i = L_f}$$

For a rigid body with changing moment of inertia (but no external torque):

$$\boxed{I_i\omega_i = I_f\omega_f}$$

> **Deep Why:** Just as conservation of linear momentum follows from Newton's Third Law (internal forces canceling in pairs), conservation of angular momentum follows from the rotational form of the Third Law: internal torques within an isolated system also cancel in pairs (any internal force pair, being equal and opposite along the same line of action in simple cases, produces equal and opposite torques about any common axis). This is why angular momentum conservation applies to a huge range of situations — spinning skaters, colliding rotating disks, exploding rotating objects, and orbital mechanics — without ever needing to know the complicated internal torques involved.

---

## 2. The Spinning Skater — Classic Application

A skater spins with arms extended, then pulls their arms in. No external torque acts about the vertical spin axis (ice is frictionless; gravity and the normal force act vertically and produce no torque about the vertical axis).

$$I_i\omega_i = I_f\omega_f$$

Pulling the arms in **decreases I** (mass moves closer to the rotation axis, and I depends on the square of distance from the axis — recall $I=\sum m_ir_i^2$). Since $I_i\omega_i=I_f\omega_f=\text{constant}$, decreasing I must **increase ω** proportionally.

### Worked Numbers

A skater has $I_i = 4.0$ kg·m² with arms extended, spinning at $\omega_i=2.0$ rad/s. Pulling arms in reduces I to 1.2 kg·m². Find the new angular velocity.

$$\omega_f = \frac{I_i\omega_i}{I_f} = \frac{4.0\times2.0}{1.2} = \mathbf{6.67 \text{ rad/s}}$$

The skater spins more than 3× faster — purely from redistributing their own mass, with no external torque involved.

### What Happens to Kinetic Energy?

$$KE_i = \frac{1}{2}I_i\omega_i^2 = \frac{1}{2}(4.0)(4.0) = 8.0 \text{ J}$$
$$KE_f = \frac{1}{2}I_f\omega_f^2 = \frac{1}{2}(1.2)(44.5) = 26.7 \text{ J}$$

**Kinetic energy INCREASES** (8.0 J → 26.7 J), even though angular momentum stays constant! This is not a violation of energy conservation — the skater does positive work pulling their arms inward against the "centrifugal tendency" (more precisely, against the requirement to provide centripetal force on their own arm mass as it moves inward while already rotating) — this work comes from the skater's own muscles (internal chemical energy), converted into additional rotational kinetic energy. Angular momentum conservation does NOT imply energy conservation; they are independent principles.

---

## 3. Collisions Involving Rotation

Angular momentum conservation applies to rotational "collisions" exactly as linear momentum conservation applies to translational collisions.

### Example 23.1 — Falling object onto a rotating disk

A disk (I=0.40 kg·m²) spins freely at ω₀=8.0 rad/s. A small object (m=0.50 kg) falls vertically and lands on the disk at radius r=0.30 m from the center, sticking to it (perfectly inelastic rotational "collision"). Find the new angular velocity.

**Before:** $L_i = I_{disk}\omega_0 = 0.40\times8.0=3.2$ kg·m²/s (the falling object has zero angular momentum about the disk's axis before landing, since it falls straight down — its velocity is parallel to the axis if the axis is vertical, giving zero angular momentum in this radial direction... more precisely, if it falls straight down onto the disk, its velocity has no component contributing angular momentum about the vertical axis, since $\vec r \times \vec v$ for a purely vertical v and any r has a vertical component determined by the horizontal position — but if the object falls purely vertically with no horizontal velocity, its angular momentum about the vertical axis IS zero, since its velocity is parallel to the axis)

**After:** $I_f = I_{disk} + mr^2 = 0.40+0.50(0.09) = 0.40+0.045=0.445$ kg·m²

$$\omega_f = \frac{L_i}{I_f} = \frac{3.2}{0.445} = \mathbf{7.19 \text{ rad/s}}$$

The disk slows down slightly because the added mass increases the total moment of inertia, and angular momentum (not angular velocity) is what's conserved.

---

## 4. Gyroscopic Effects (Conceptual Introduction)

A spinning gyroscope resists changes to the DIRECTION of its angular momentum vector, not just its magnitude. Because $\vec\tau = d\vec L/dt$ is a vector equation, an applied torque perpendicular to L⃗ changes the DIRECTION of L⃗ (causing "precession" — the slow rotation of the spin axis itself) rather than its magnitude. This is why a fast-spinning top or gyroscope doesn't simply fall over under gravity's torque — instead, its axis slowly sweeps out a cone (precesses). A full quantitative treatment requires vector calculus beyond this course's scope, but the qualitative principle — **large L⃗ makes the spin axis's direction highly stable against small torques, and any applied torque perpendicular to L⃗ redirects L⃗ rather than opposing it directly** — explains a wide range of phenomena: bicycle stability at speed, spinning coins, and the precession of Earth's own rotation axis (a 26,000-year cycle).

---

## 5. Kepler's Second Law — Angular Momentum in Orbital Mechanics

A planet or comet orbiting the Sun experiences a gravitational force always directed exactly toward the Sun (a **central force**). Since torque about the Sun is $\tau = rF\sin\phi$, and the force is always along r⃗ (φ=0 or 180°), the torque about the Sun is **always zero**.

$$\tau_{Sun}=0 \implies L_{orbit} = \text{constant throughout the orbit}$$

Since $L = mvr\sin\phi = mv_{\perp}r$ (where $v_\perp$ is the velocity component perpendicular to r⃗), and this stays constant:

$$v_\perp r = \text{constant}$$

This means that when a comet is close to the Sun (small r), its perpendicular speed must be large; when far away (large r), its perpendicular speed is small. This is exactly **Kepler's Second Law**: "a line joining a planet and the Sun sweeps out equal areas in equal times" — the swept area rate is directly proportional to $v_\perp r$, which we've just shown is constant.

> **Deep Why:** Kepler discovered this law empirically in 1609, decades before Newton's laws existed. It is a beautiful historical example of a correct physical law being found before its underlying explanation (conservation of angular momentum due to gravity being a central force) was understood. This is analogous to Kepler's Third Law appearing in Week 2's Problem Set 0 (dimensional analysis), also derivable from Newtonian mechanics.

---

## 6. Worked Examples

### Example 23.2 — Diver pulling into a tuck

A diver leaves the board with $I_i=15$ kg·m² and $\omega_i=2.0$ rad/s (a slow rotation). Tucking into a ball reduces I to 4.0 kg·m². Find the new angular velocity, and the time for one full rotation in the tucked position.

$$\omega_f = \frac{I_i\omega_i}{I_f} = \frac{15\times2.0}{4.0} = 7.5 \text{ rad/s}$$

$$T = \frac{2\pi}{\omega_f} = \frac{2\pi}{7.5} = \mathbf{0.838 \text{ s per rotation}}$$

---

### Example 23.3 — Merry-go-round and a jumping child

A merry-go-round (I=300 kg·m²) spins at ω₀=1.5 rad/s. A 40 kg child, initially at the center (contributing negligible I), walks out to the rim at r=2.0 m. Find the new angular velocity.

$$I_f = I_{platform}+mr^2 = 300+40(4.0)=300+160=460 \text{ kg·m}^2$$

$$\omega_f = \frac{I_i\omega_i}{I_f} = \frac{300\times1.5}{460} = \frac{450}{460} = \mathbf{0.978 \text{ rad/s}}$$

The system slows down as the child moves outward, increasing the total moment of inertia while angular momentum stays fixed — the rotational analog of the ice skater example, but in reverse (I increasing rather than decreasing).

---

## 7. Summary

| Concept | Formula | Key Point |
|---------|---------|-----------|
| Conservation of angular momentum | L_i = L_f (when τ_net=0) | Direct rotational analog of momentum conservation |
| Changing I | I_iω_i = I_fω_f | ω increases when I decreases, and vice versa |
| Energy in these processes | NOT automatically conserved | Internal work (e.g., muscles) can change KE while L stays fixed |
| Kepler's Second Law | Consequence of zero torque from central (gravitational) force | Equal areas swept in equal times |

---


---

## CS Connection — Conservation Under Reconfiguration

A skater pulling their arms in spins faster because L = Iω is fixed while I drops. The invariant holds while its components trade off — the same shape as a system that maintains a fixed total budget while reallocating between components. Reasoning from the invariant to the consequence, rather than simulating the process, is the whole technique.

---

## Looking Ahead

**L24** closes the course with the special case where *nothing* moves: static equilibrium, where both net force and net torque vanish.

## Conceptual Questions

1. A figure skater spinning with arms out pulls them in and spins faster. Where does the extra kinetic energy come from? Is this consistent with conservation of energy?

2. A star collapses under its own gravity (dramatically decreasing its radius, and hence its moment of inertia), forming a rapidly-spinning neutron star. Using angular momentum conservation, explain qualitatively why neutron stars can spin hundreds of times per second even though their progenitor stars rotated far more slowly.

3. Explain why a comet moves fastest at its closest approach to the Sun (perihelion) and slowest at its farthest point (aphelion), using conservation of angular momentum rather than energy.

4. A person sits on a frictionless rotating stool holding a spinning bicycle wheel with its axis vertical. If they flip the wheel upside down (reversing its angular momentum direction), what happens to the person's own rotation? Explain using conservation of the TOTAL angular momentum of the person+wheel system.
