# PHYS 141 · Lecture 8
# Projectile Motion

> **Core Principle:** A projectile is any object moving only under the influence of gravity (no air resistance, no thrust). Its horizontal motion is uniform (constant velocity); its vertical motion is free fall (constant downward acceleration g). These two motions are completely independent and share only one variable: time.

**Date:** Tuesday 6 October 2026 · 14:00–14:50 · Week 2

---


## Where This Fits

**Previously:** **L07** established that perpendicular components evolve independently. Projectile motion is that principle with a₍y₎ = −g and a₍x₎ = 0.

---

## 1. Setting Up the Problem

### Standard Coordinate Convention

- Origin at launch point
- x positive to the right (horizontal)
- y positive upward (vertical)
- Launch angle θ measured from the positive x-axis (horizontal)

### Initial Conditions

If launched with speed v₀ at angle θ above horizontal:

$$v_{0x} = v_0 \cos\theta \qquad v_{0y} = v_0 \sin\theta$$

### Accelerations

- Horizontal: $a_x = 0$ (no horizontal force in ideal projectile motion)
- Vertical: $a_y = -g = -9.81$ m/s² (gravity, downward)

---

## 2. The Complete Equation Set

Applying the 2D kinematic equations with a_x = 0 and a_y = −g:

**Position:**
$$x(t) = v_{0x}\,t = (v_0\cos\theta)\,t \tag{1}$$
$$y(t) = v_{0y}\,t - \tfrac{1}{2}gt^2 = (v_0\sin\theta)\,t - \tfrac{1}{2}gt^2 \tag{2}$$

**Velocity:**
$$v_x(t) = v_{0x} = v_0\cos\theta = \text{constant} \tag{3}$$
$$v_y(t) = v_{0y} - gt = v_0\sin\theta - gt \tag{4}$$

**Speed at any time:**
$$|\vec{v}(t)| = \sqrt{v_x^2 + v_y^2(t)} \tag{5}$$

---

## 3. The Trajectory: Eliminating t

From (1): $t = x/(v_0\cos\theta)$. Substitute into (2):

$$y = (v_0\sin\theta)\cdot\frac{x}{v_0\cos\theta} - \frac{1}{2}g\left(\frac{x}{v_0\cos\theta}\right)^2$$

$$\boxed{y = x\tan\theta - \frac{g}{2v_0^2\cos^2\theta}\,x^2} \tag{Trajectory equation}$$

This is a **downward-opening parabola** of the form y = Ax − Bx², where A = tanθ and B = g/(2v₀²cos²θ) are constants for a given launch. Every ideal projectile traces a parabola — independent of mass, shape, or material.

> **Deep Why — Why a parabola?** The horizontal position grows linearly with time (x ∝ t), while the vertical position has a quadratic term (y ∝ t²). Eliminating t from a linear and a quadratic produces a quadratic in x, which is the equation of a parabola. The parabolic shape is a direct consequence of constant gravitational acceleration combined with constant horizontal velocity.

---

## 4. Key Derived Results

### 4.1 Time of Flight (Launched and Landing at Same Height)

The projectile returns to y = 0 when:
$$(v_0\sin\theta)\,t - \tfrac{1}{2}g t^2 = 0 \implies t\left(v_0\sin\theta - \tfrac{1}{2}gt\right) = 0$$

The non-trivial solution:
$$\boxed{T = \frac{2v_0\sin\theta}{g}} \tag{Time of flight}$$

Note: T = 2 × (time to reach peak), confirming the symmetry of free fall from Lecture 6.

### 4.2 Maximum Height

At the peak, $v_y = 0$:
$$t_{peak} = \frac{v_0\sin\theta}{g} = \frac{T}{2}$$

Substituting into y(t):
$$\boxed{H = \frac{(v_0\sin\theta)^2}{2g} = \frac{v_{0y}^2}{2g}} \tag{Maximum height}$$

This is the same as the 1D free-fall result — because at the peak, only the vertical component of launch velocity matters.

### 4.3 Horizontal Range

The horizontal distance traveled during the full time of flight:
$$R = v_{0x}\cdot T = (v_0\cos\theta)\cdot\frac{2v_0\sin\theta}{g} = \frac{v_0^2\cdot 2\sin\theta\cos\theta}{g}$$

Using the double-angle identity 2sinθcosθ = sin(2θ):

$$\boxed{R = \frac{v_0^2\sin(2\theta)}{g}} \tag{Horizontal range}$$

**This formula is valid only when the launch and landing heights are equal.**

### 4.4 Angle for Maximum Range

Since R ∝ sin(2θ), range is maximized when sin(2θ) = 1, i.e., 2θ = 90°:

$$\boxed{\theta_{max\,range} = 45°}$$

> **Deep Why — The 45° result:** Maximum range requires balancing two competing effects. A higher angle gives more time in the air (bigger T) but less horizontal velocity (smaller v_{0x}). A lower angle gives more horizontal velocity but less time. At 45°, both sin and cos equal 1/√2, and their product v₀²sinθcosθ is maximized. This is a classic optimization argument — we're maximizing a product of two quantities that sum to a constant (sin²θ + cos²θ = 1).

### 4.5 Complementary Angles Give Equal Range

Since sin(2θ) = sin(180° − 2θ) = sin(2(90°−θ)), the angles θ and (90° − θ) produce the same range. Examples:
- 30° and 60° → same R
- 20° and 70° → same R
- 45° → maximum R (self-complementary)

---

## 5. Velocity Direction at Any Point

The velocity vector is always tangent to the parabolic path. Its direction angle φ from horizontal is:

$$\tan\phi = \frac{v_y}{v_x} = \frac{v_0\sin\theta - gt}{v_0\cos\theta}$$

**At launch:** φ = θ (given)
**At peak:** v_y = 0, so φ = 0 (velocity is purely horizontal)
**On return to launch height:** v_y = −v₀sinθ (equal magnitude, reversed sign), φ = −θ

The trajectory is symmetric: the angle below horizontal on descent equals the angle above horizontal on ascent, at equal heights.

---

## 6. Speed at Any Height

Using energy methods (anticipating Week 4), or from kinematics:

At height y (taking launch as y = 0):
$$v_y^2 = v_{0y}^2 - 2gy$$
$$|\vec{v}|^2 = v_x^2 + v_y^2 = v_{0x}^2 + v_{0y}^2 - 2gy = v_0^2 - 2gy$$
$$\boxed{|\vec{v}| = \sqrt{v_0^2 - 2gy}}$$

Speed depends only on height, not on the horizontal position. This is the kinematic precursor to conservation of energy.

---

## 7. Projectile Motion on Inclined Planes (Extension)

If a projectile is launched from the top of an incline of angle φ and lands on the incline, the range along the slope and optimal launch angle change. The analysis requires setting up coordinates aligned with the slope or using the standard equations with a modified landing condition y = x·tanφ. This is a common exam problem — watch for it.

---

## 8. Effect of Air Resistance (Qualitative)

Real projectiles experience air drag, which:
- Always opposes velocity
- Reduces range (typically by 20–40% for sports balls at normal speeds)
- Changes the trajectory from a symmetric parabola to an asymmetric curve
- Makes the optimal launch angle **less than 45°** (typically 30–40° for dense objects in air)
- Causes the descent to be steeper than the ascent

The mathematical treatment requires solving a differential equation (drag force ∝ v or v²), beyond this course's scope. But qualitatively understanding the effect on the idealized results is expected.

---

## 9. Worked Examples

### Example 8.1 — Standard projectile

A ball is launched at 25 m/s at 35° above horizontal from ground level. Find: time of flight, maximum height, and horizontal range.

**Components:** v₀ₓ = 25cos35° = 20.48 m/s; v₀ᵧ = 25sin35° = 14.34 m/s

**Time of flight:** T = 2v₀ᵧ/g = 2(14.34)/9.81 = **2.924 s**

**Max height:** H = v₀ᵧ²/(2g) = (14.34)²/19.62 = 205.84/19.62 = **10.49 m**

**Range:** R = v₀ₓ · T = 20.48 × 2.924 = **59.9 m**

Check with formula: R = v₀²sin(2θ)/g = 625sin(70°)/9.81 = 625(0.9397)/9.81 = **59.9 m** ✓

---

### Example 8.2 — Projectile off a cliff

A cannon on a 60 m cliff fires horizontally at 80 m/s. Where does the cannonball land, and with what velocity?

**Setup:** Origin at cannon. a_x = 0, a_y = −9.81 m/s². v₀ₓ = 80 m/s, v₀ᵧ = 0 (horizontal launch).

**Time to fall 60 m:** y = −60 m = −½gt² → t = √(120/9.81) = **3.499 s**

**Horizontal range:** x = 80 × 3.499 = **280 m** from base of cliff

**Impact velocity:**
- vₓ = 80 m/s (unchanged)
- vᵧ = 0 − 9.81(3.499) = −34.32 m/s
- Speed = √(80² + 34.32²) = √(6400+1177.9) = √7577.9 = **87.1 m/s**
- Angle below horizontal: arctan(34.32/80) = **23.2°**

---

### Example 8.3 — Finding launch angle to hit a target

A target is 150 m away at the same height. What launch angle(s) give a hit, if v₀ = 45 m/s?

$$R = \frac{v_0^2\sin2\theta}{g} \implies \sin2\theta = \frac{Rg}{v_0^2} = \frac{150\times9.81}{2025} = \frac{1471.5}{2025} = 0.7267$$

$$2\theta = \arcsin(0.7267) = 46.56° \quad \text{or} \quad 180° - 46.56° = 133.44°$$

$$\theta_1 = 23.3° \qquad \theta_2 = 66.7°$$

Both are valid — a low flat trajectory and a high arcing trajectory both hit the target. This is familiar from artillery and basketball shots.

---

## 10. Summary

| Quantity | Formula | Condition |
|---------|---------|-----------|
| Trajectory | y = xtanθ − gx²/(2v₀²cos²θ) | General |
| Time of flight | T = 2v₀sinθ/g | Same launch and landing height |
| Max height | H = (v₀sinθ)²/(2g) | — |
| Range | R = v₀²sin2θ/g | Same launch and landing height |
| Max range angle | θ = 45° | Level ground, no air resistance |
| Speed at height y | \|v\| = √(v₀² − 2gy) | — |

---


---

## CS Connection — Trajectories and Simulation Error

The parabolic trajectory has a closed form, which makes it the standard benchmark for testing a numerical integrator: simulate, then compare against the exact answer. Any drift is integration error, not physics. Games use the closed form for aiming (solving for launch angle given a target) and numerical integration for the actual flight, because the closed form breaks the moment drag or wind is introduced.

---

## Looking Ahead

**L09** covers the other major 2D case: motion on a curved path at constant speed, where the acceleration points inward rather than downward.

## Conceptual Questions

1. A rifle is fired horizontally. At the same instant, an identical bullet is dropped from the same height. Which hits the ground first? Explain without calculation.

2. At what point in a projectile's trajectory is the speed minimum? What is the direction of velocity there?

3. A golf ball is hit at 45° and travels 200 m. The same ball is hit at 30° with the same initial speed. Without using the range formula, predict whether the range is greater or less than 200 m and why. Then verify with the formula.

4. Why does the range formula R = v₀²sin2θ/g break down when the landing height differs from the launch height? What goes wrong in the derivation?
