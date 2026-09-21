# PHYS 141 · Lecture 7
# Kinematics in Two Dimensions

> **Core Principle:** Motion in two dimensions is not a new subject — it is two simultaneous applications of one-dimensional kinematics, one along each perpendicular axis. The key insight is that perpendicular components of motion are completely independent of each other. This independence is not a convenience; it is a deep consequence of the structure of Euclidean space and Newton's laws.

**Date:** Monday 5 October 2026 · 14:00–14:50 · Week 2

---


## Where This Fits

**Previously:** **L06** completed 1D motion. Real motion happens in a plane, and the key result is that perpendicular components are independent.

---

## 1. From 1D to 2D: The Vector Extension

In 1D, position was a signed scalar x(t). In 2D, position becomes a vector:

$$\vec{r}(t) = x(t)\,\hat{x} + y(t)\,\hat{y}$$

The definitions of velocity and acceleration extend naturally via component-wise differentiation:

$$\vec{v}(t) = \frac{d\vec{r}}{dt} = \frac{dx}{dt}\,\hat{x} + \frac{dy}{dt}\,\hat{y} = v_x\,\hat{x} + v_y\,\hat{y}$$

$$\vec{a}(t) = \frac{d\vec{v}}{dt} = \frac{dv_x}{dt}\,\hat{x} + \frac{dv_y}{dt}\,\hat{y} = a_x\,\hat{x} + a_y\,\hat{y}$$

This is valid because `x̂` and `ŷ` are **constant vectors** in Cartesian coordinates — their directions do not change as the particle moves, so they pass through the derivative unchanged. (This will not be true in polar coordinates, as noted in Lecture 2.)

---

## 2. The Independence of Perpendicular Components

This is the most important principle in `2D` kinematics:

> **The motion of a particle in the x-direction is completely independent of its motion in the y-direction, and vice versa.**

This means:
- The x-component of position depends only on the x-component of velocity and acceleration
- The y-component of position depends only on the y-component of velocity and acceleration
- What happens horizontally has no effect on what happens vertically, and vice versa

### Why This Is True

Newton's second law (Week 3) will show that F⃗ = ma⃗, which in components is:

$$F_x = ma_x \qquad F_y = ma_y$$

These are **two completely separate equations**. A force in the x-direction causes only x-acceleration; a force in the y-direction causes only y-acceleration. Since gravity acts only in the y-direction (downward), it affects only vertical motion — not horizontal motion.

### The Famous Demonstration

Drop a ball straight down. Simultaneously, shoot a second ball horizontally from the same height. Both balls hit the ground at exactly the same time, because their vertical motions are identical (both start with v_y = 0, both accelerate downward at g). The horizontal velocity of the second ball has zero effect on when it hits the ground.

This is not intuitive — common sense suggests the moving ball "has more to do" and should take longer. The experiment proves common sense wrong, and independence of components explains why.

---

## 3. 2D Kinematic Equations for Constant Acceleration

When acceleration is constant (both components constant), the kinematic equations from Lecture 5 apply independently to each component:

**x-direction:**
$$x(t) = x_0 + v_{0x}\,t + \tfrac{1}{2}a_x t^2$$
$$v_x(t) = v_{0x} + a_x t$$
$$v_x^2 = v_{0x}^2 + 2a_x\Delta x$$

**y-direction:**
$$y(t) = y_0 + v_{0y}\,t + \tfrac{1}{2}a_y t^2$$
$$v_y(t) = v_{0y} + a_y t$$
$$v_y^2 = v_{0y}^2 + 2a_y\Delta y$$

These six equations are the complete toolkit for 2D constant-acceleration problems. **Time t is shared** — it is the same variable in both sets. This shared time is what links horizontal and vertical motion in a projectile problem.

---

## 4. Velocity: Direction and Magnitude in 2D

At any instant, the velocity vector has:

**Magnitude (speed):**
$$|\vec{v}| = \sqrt{v_x^2 + v_y^2}$$

**Direction (angle from +x axis):**
$$\theta = \arctan\!\left(\frac{v_y}{v_x}\right)$$

The velocity vector is always **tangent to the path** (trajectory) at every point. This is the geometric definition of the derivative in 2D: dr⃗/dt gives a vector tangent to the curve r⃗(t).

---

## 5. The Trajectory Equation: Eliminating t

In many problems you want the shape of the path, y(x), rather than x(t) and y(t) separately. You eliminate t algebraically.

**General method:** Solve one of the parametric equations for t, then substitute into the other.

**Example:** For constant velocity in x and constant acceleration in y (this is projectile motion, covered next lecture):
- x = v_{0x} t → t = x/v_{0x}
- y = v_{0y} t + ½a_y t²

Substitute:
$$y = v_{0y}\left(\frac{x}{v_{0x}}\right) + \frac{1}{2}a_y\left(\frac{x}{v_{0x}}\right)^2 = \left(\frac{v_{0y}}{v_{0x}}\right)x + \frac{a_y}{2v_{0x}^2}x^2$$

This is of the form y = Ax + Bx² — a **parabola**. Every projectile follows a parabolic trajectory (in the absence of air resistance).

---

## 6. Average and Instantaneous Velocity in 2D

**Average velocity** (vector, from t₁ to t₂):
$$\bar{\vec{v}} = \frac{\Delta\vec{r}}{\Delta t} = \frac{\vec{r}(t_2) - \vec{r}(t_1)}{t_2 - t_1}$$

Note: average velocity points in the direction of displacement Δr⃗, **not** along the path. If a ball travels in a semicircle and ends up directly to the right of where it started, the average velocity points east, regardless of the curved path taken.

**Instantaneous velocity** (vector):
$$\vec{v}(t) = \lim_{\Delta t \to 0} \frac{\Delta\vec{r}}{\Delta t} = \frac{d\vec{r}}{dt}$$

Points tangent to the path at time t.

---

## 7. Relative Motion in 2D

The velocity of object A as observed from a reference frame moving with object B is:

$$\vec{v}_{A/B} = \vec{v}_A - \vec{v}_B$$

where all velocities are measured relative to a common (usually ground) frame. This is the **Galilean velocity addition rule** — valid for speeds much less than the speed of light.

**Example:** A boat heads due north at 5 m/s relative to the water. The river flows east at 3 m/s. What is the boat's velocity relative to the ground?

$$\vec{v}_{boat/ground} = \vec{v}_{boat/water} + \vec{v}_{water/ground} = 5\,\hat{y} + 3\,\hat{x} \text{ m/s}$$
$$|\vec{v}| = \sqrt{25+9} = \sqrt{34} \approx 5.83 \text{ m/s}, \quad \theta = \arctan(5/3) = 59.0° \text{ north of east}$$

---

## 8. Worked Examples

**Example 7.1:** A particle has r⃗(t) = (3t² − t)x̂ + (2t − 4t³)ŷ meters.

Find v⃗(t), a⃗(t), and the speed at t = 1 s.

$$\vec{v}(t) = (6t-1)\hat{x} + (2-12t^2)\hat{y}$$
$$\vec{a}(t) = 6\hat{x} + (-24t)\hat{y}$$

At t = 1 s: v⃗ = 5x̂ − 10ŷ m/s. Speed = √(25+100) = √125 = **11.2 m/s**

---

**Example 7.2:** A particle starts at origin with v⃗₀ = (4, 0) m/s and has constant acceleration a⃗ = (−1, 3) m/s².

Find the position and velocity at t = 2 s, and the speed.

$$x(2) = 0 + 4(2) + \tfrac{1}{2}(-1)(4) = 8 - 2 = 6 \text{ m}$$
$$y(2) = 0 + 0(2) + \tfrac{1}{2}(3)(4) = 6 \text{ m}$$
$$v_x(2) = 4 + (-1)(2) = 2 \text{ m/s}, \quad v_y(2) = 0 + 3(2) = 6 \text{ m/s}$$
$$\text{Speed} = \sqrt{4+36} = \sqrt{40} \approx 6.32 \text{ m/s}$$

---

## 9. Summary

| Quantity | 1D | 2D |
|---------|----|----|
| Position | x(t) | r⃗(t) = x(t)x̂ + y(t)ŷ |
| Velocity | v = dx/dt | v⃗ = dr⃗/dt (tangent to path) |
| Acceleration | a = dv/dt | a⃗ = dv⃗/dt |
| Kinematic eqs | 5 equations in 1D | Same equations, applied independently per component |
| Key principle | — | Perpendicular components are independent |

---


---

## CS Connection — Independence of Components as Decomposition

The physical fact that x- and y-motion do not interact is the same idea as decomposing a problem into independent subproblems: once independent, each can be solved separately and the results combined. It is also what makes the computation embarrassingly parallel — no synchronisation is needed between the two axes. Recognising independence is the first move in both physics and algorithm design.

---

## Looking Ahead

**L08** exploits that independence in the canonical case: projectile motion, where horizontal velocity is constant and vertical acceleration is g.

## Conceptual Questions

1. A particle moves in a circle at constant speed. Is its velocity constant? Is its acceleration zero? Explain both answers carefully.

2. Can a particle have zero acceleration in the x-direction and non-zero acceleration in the y-direction simultaneously? What would the trajectory look like?

3. A ball is rolled off a horizontal table. A second ball is dropped straight down from the same height at the same instant. Which hits the floor first? Explain using the independence principle — do not just say "they're the same."

4. Two particles have the same speed at some instant but different velocity vectors. How is this possible? Give a concrete example.
