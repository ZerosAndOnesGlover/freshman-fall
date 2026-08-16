# PHYS 141 · Lecture 5
# Acceleration & The Kinematic Equations

> **Core Principle:** Acceleration is the rate of change of velocity. Under constant acceleration — the most important special case — the five kinematic equations can be derived rigorously from calculus. Memorizing them without this derivation is fragile; understanding the derivation makes them unforgettable and tells you exactly when they apply.

**Date:** Tuesday 25 August 2026 · 14:00–14:50 · Week 1

---


## Where This Fits

**Previously:** **L04** defined velocity as the derivative of position. Differentiating once more gives acceleration.

---

## 1. Acceleration

### 1.1 Average Acceleration

$$\bar{a} = \frac{\Delta v}{\Delta t} = \frac{v_f - v_i}{t_f - t_i}$$

Average acceleration is the change in velocity divided by the time elapsed. It is a **vector** in 1D (signed).

### 1.2 Instantaneous Acceleration

$$a(t) = \lim_{\Delta t \to 0} \frac{\Delta v}{\Delta t} = \frac{dv}{dt} = \frac{d^2x}{dt^2}$$

Acceleration is the **first derivative of velocity** and the **second derivative of position** with respect to time.

The geometric interpretation on a v(t) graph: instantaneous acceleration = **slope of the tangent line** to v(t) at time t. And displacement = **area under the v(t) curve**.

### 1.3 What Acceleration Does (and Doesn't) Tell You

Many students confuse acceleration with "speeding up." This is wrong. Acceleration tells you how **velocity is changing** — in both magnitude and direction.

| Situation | Acceleration direction | What's happening |
|-----------|----------------------|-----------------|
| Moving +x, speeding up | +x | Velocity and acceleration in same direction |
| Moving +x, slowing down | −x | Velocity and acceleration in opposite directions |
| Moving −x, speeding up | −x | Velocity and acceleration in same direction (both negative) |
| Moving −x, slowing down | +x | Velocity and acceleration in opposite directions |
| At rest, about to move +x | +x | Zero velocity, non-zero acceleration |

**Key rule:** Speed increases when velocity and acceleration are in the **same direction** (same sign). Speed decreases when they are in **opposite directions** (opposite signs). This is independent of the sign of either one alone.

> **Deep Why — the jerk, snap, crackle, pop:** Just as velocity is the derivative of position, and acceleration is the derivative of velocity, we can go further: the **jerk** (da/dt) is the rate of change of acceleration. A sudden jerk (a large da/dt) is physically jarring — you feel it as your body is pushed into or lifted out of a seat. Ride designers, automotive engineers, and elevator designers carefully minimize jerk for passenger comfort. The third derivative of position has a real engineering name and real engineering significance.

---

## 2. The Hierarchy of Derivatives

$$x(t) \xrightarrow{\frac{d}{dt}} v(t) \xrightarrow{\frac{d}{dt}} a(t) \xrightarrow{\frac{d}{dt}} j(t) \text{ (jerk)}$$

Going the other direction (integration):

$$a(t) \xrightarrow{\int dt} v(t) \xrightarrow{\int dt} x(t)$$

---

## 3. Deriving the Constant-Acceleration Equations

### Setup

Assume acceleration is constant: a(t) = a = constant.

We want to find v(t) and x(t). We do this by **integrating**, not by memorizing formulas.

### Step 1: Integrate a to get v(t)

$$v(t) = \int a\, dt = at + C_1$$

The constant of integration C₁ is determined by the **initial condition**: at t = 0, v = v₀. Therefore C₁ = v₀.

$$\boxed{v(t) = v_0 + at} \tag{Eq. 1}$$

### Step 2: Integrate v(t) to get x(t)

$$x(t) = \int v(t)\, dt = \int (v_0 + at)\, dt = v_0 t + \frac{1}{2}at^2 + C_2$$

The constant of integration C₂ is the **initial position**: at t = 0, x = x₀. Therefore C₂ = x₀.

$$\boxed{x(t) = x_0 + v_0 t + \frac{1}{2}at^2} \tag{Eq. 2}$$

### Step 3: Derive a time-independent equation

From Eq. 1: $t = (v - v_0)/a$. Substitute into Eq. 2:

$$x - x_0 = v_0\left(\frac{v-v_0}{a}\right) + \frac{1}{2}a\left(\frac{v-v_0}{a}\right)^2$$

$$\Delta x = \frac{v_0(v-v_0)}{a} + \frac{(v-v_0)^2}{2a} = \frac{2v_0(v-v_0) + (v-v_0)^2}{2a} = \frac{(v-v_0)(2v_0 + v - v_0)}{2a} = \frac{(v-v_0)(v+v_0)}{2a}$$

$$\boxed{v^2 = v_0^2 + 2a\Delta x} \tag{Eq. 3}$$

### Step 4: Derive an equation without acceleration

From Eq. 1: v = v₀ + at. The average velocity over a constant-acceleration interval is:

$$\bar{v} = \frac{v_0 + v}{2}$$

(This is only true for **constant acceleration** — average velocity is not always (v₀+v)/2 in general.) Then:

$$\boxed{\Delta x = \frac{v_0 + v}{2}\cdot t} \tag{Eq. 4}$$

### Step 5: Derive an equation without initial velocity

From Eq. 1: v₀ = v − at. Substitute into Eq. 2:

$$x = x_0 + (v-at)t + \frac{1}{2}at^2 = x_0 + vt - \frac{1}{2}at^2$$

$$\boxed{x = x_0 + vt - \frac{1}{2}at^2} \tag{Eq. 5}$$

---

## 4. The Five Kinematic Equations

These are the five equations, each one lacking one of the five kinematic variables {x₀, v₀, v, a, t}. The strategy: identify which variable you don't know and don't need, then use the equation that **doesn't contain it**.

| Equation | Missing variable |
|----------|----------------|
| v = v₀ + at | Δx |
| Δx = v₀t + ½at² | v |
| v² = v₀² + 2aΔx | t |
| Δx = ½(v₀ + v)t | a |
| Δx = vt − ½at² | v₀ |

> **Critical restriction:** These equations are valid **only when acceleration is constant** throughout the time interval. If acceleration varies with time (e.g., a rocket burning fuel as its mass decreases), these equations give wrong answers. Always check this assumption before applying them.

---

## 5. Problem-Solving Strategy for 1D Kinematics

A disciplined approach eliminates most errors:

1. **Draw a diagram.** Sketch the situation. Mark initial and final positions.
2. **Establish your coordinate system.** State your origin and positive direction explicitly.
3. **List knowns and unknowns.** Write down every given quantity with its sign. Identify what you're solving for.
4. **Identify the missing variable** (the one you neither know nor need). Select the kinematic equation that omits it.
5. **Solve algebraically first**, then substitute numbers.
6. **Check units, sign, and magnitude.** Does the sign make physical sense? Is the magnitude reasonable (order of magnitude)?

---

## 6. Worked Examples

### Example 5.1 — Basic kinematics

A car starts from rest (v₀ = 0) and accelerates at a = 3.5 m/s² for t = 8.0 s.
Find: (a) final velocity, (b) distance traveled.

**(a)** Use v = v₀ + at: v = 0 + 3.5 × 8.0 = **28 m/s**

**(b)** Use Δx = v₀t + ½at²: Δx = 0 + ½(3.5)(64) = **112 m**

Check with Eq. 3: v² = 0 + 2(3.5)(112) = 784 → v = 28 m/s ✓

### Example 5.2 — Solving for acceleration

A train moving at 25 m/s decelerates to rest in a stopping distance of 200 m.
Find the acceleration.

Known: v₀ = 25 m/s, v = 0, Δx = 200 m. Missing: t.

Use v² = v₀² + 2aΔx:
$$0 = 625 + 2a(200) \Rightarrow a = -\frac{625}{400} = -1.5625 \approx -1.56 \text{ m/s}^2$$

The negative sign confirms deceleration (acceleration opposes motion).

### Example 5.3 — Two-phase problem

A car accelerates from rest at 2.0 m/s² for 5.0 s, then moves at constant velocity for another 10 s.
Find: (a) maximum velocity, (b) total displacement.

**Phase 1 (a = 2.0 m/s², t = 5.0 s):**
- v₁ = 0 + 2.0(5.0) = 10 m/s
- Δx₁ = 0 + ½(2.0)(25) = 25 m

**Phase 2 (v = 10 m/s constant, t = 10 s):**
- Δx₂ = 10 × 10 = 100 m

**Total displacement = 25 + 100 = 125 m**

### Example 5.4 — Finding when two conditions are met simultaneously (requires quadratic)

A ball is thrown upward with v₀ = 15 m/s from the ground (take up as +, a = −9.8 m/s²).
When does it reach x = 8.0 m?

Use Δx = v₀t + ½at²:
$$8.0 = 15t + \frac{1}{2}(-9.8)t^2 = 15t - 4.9t^2$$
$$4.9t^2 - 15t + 8.0 = 0$$
$$t = \frac{15 \pm \sqrt{225 - 4(4.9)(8.0)}}{2(4.9)} = \frac{15 \pm \sqrt{225 - 156.8}}{9.8} = \frac{15 \pm \sqrt{68.2}}{9.8} = \frac{15 \pm 8.26}{9.8}$$

**t₁ = 0.69 s** (on the way up) and **t₂ = 2.37 s** (on the way down)

Both answers are physically valid — there are two times when the ball is at x = 8.0 m.

---

## 7. Summary

| Concept | Key Point |
|---------|-----------|
| Acceleration | a = dv/dt = d²x/dt² |
| Constant a restriction | Kinematic equations ONLY valid when a is constant |
| Selecting an equation | Identify the missing (unneeded) variable; use the equation that lacks it |
| Two-phase problems | Apply kinematic equations to each phase separately |
| Quadratic solutions | Both roots may be physically meaningful; check each one |
| Sign convention | Negative a does not mean "decelerating" — it depends on direction of motion |

---


---

## CS Connection — Integration and the Game Loop

The kinematic equations are the closed-form solution for constant acceleration. Physics engines cannot assume constant acceleration, so they integrate numerically each frame — `v += a*dt; x += v*dt` is Euler integration, and it is exactly what you get by discretising these definitions. It is also visibly wrong over long runs, which is why real engines use Verlet or RK4. You are learning the analytic answer that numerical methods try to approximate.

---

## Looking Ahead

**L06** applies the constant-acceleration equations to the most important special case in introductory physics: free fall under gravity.

## Conceptual Questions

1. Is it possible for an object to have a northward velocity and a southward acceleration simultaneously? Describe the motion if so.

2. A ball is thrown straight upward. At the highest point, what is its velocity? What is its acceleration? Explain why a non-zero acceleration is consistent with zero velocity at that instant.

3. Two cars start from rest at the same position. Car A accelerates at 2a for time t, then moves at constant velocity. Car B accelerates at a for time 2t, then moves at constant velocity. Which car has the higher final velocity? Which traveled farther during the acceleration phase? (Derive both answers.)

4. The position of an object is x(t) = t³ − 6t². Find all times when the object is at rest, all times when its acceleration is zero, and sketch the motion qualitatively.
