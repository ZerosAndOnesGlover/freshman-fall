# PHYS 141 — Problem Set 1 — INSTRUCTOR SOLUTIONS
**Do not distribute before the due date.**

---


## Marking Scheme

Each of the 20 problems is worth **5 points**, matching the point allocation printed on the problem set:

- **3 points — method.** A labelled diagram where forces or vectors are involved, an explicit coordinate/sign convention, the governing principle named, and the symbolic setup before numbers are substituted.
- **2 points — answer.** Correct value, correct units, and significant figures consistent with the given data.

A correct final answer with no supporting work earns **at most 2 of 5**. Conversely, a correct method carried through with one arithmetic slip should retain all 3 method marks — grade the physics, not the calculator.

**Carry-through (error propagation).** If a student makes one error early and then reasons correctly from their own wrong value, deduct once at the point of error and award full marks downstream. Do not penalise the same mistake twice.

### Part allocation

| Part | Topic | Problems | Points |
|---|---|---|---|
| **A** | Displacement, Velocity & the Derivative | 1–6 | 30 |
| **B** | Constant Acceleration & Kinematic Equations | 7–14 | 40 |
| **C** | Free Fall | 15–20 | 30 |
| | **Total** | | **100** |

### Common errors in this problem set

**1. Using the constant-acceleration equations when a is not constant.** The kinematic equations are valid only for uniform a. Applying them to a varying-a problem is a method error, not an arithmetic one — no method marks.

**2. Confusing distance with displacement.** Displacement is the net vector change; distance is path length. They differ whenever the motion reverses. Probe with any problem where the object turns around.

**3. Average velocity as the mean of initial and final.** v_avg = (v₀+v)/2 holds **only** for constant acceleration. In general v_avg = Δx/Δt.

**4. Sign convention for g.** g = 9.81 m/s² is a magnitude. Whether it enters as +9.81 or −9.81 depends on the axis the student chose. Marks are for internal consistency with their own stated convention, not for matching ours.

---

### Problem 1

x(t) = 4t³ − 9t² + 3

**(a)** x(0) = 3 m; x(1) = 4−9+3 = −2 m; x(3) = 108−81+3 = **30 m**

**(b)** v̄ = Δx/Δt = (30−3)/3 = **9 m/s**

**(c)** v(t) = 12t² − 18t

**(d)** Set v(t) = 0: 12t² − 18t = 6t(2t−3) = 0 → **t = 0 s and t = 1.5 s**

**(e)** a(t) = 24t − 18. This is NOT constant (it depends on t). This is NOT a constant-acceleration problem; the 5 kinematic equations do not apply.

---

### Problem 2

**(a)** Δx = +400 − 150 = **+250 m** (east)

**(b)** d = 400 + 150 = **550 m**

**(c)** Total time = 80 + 40 = 120 s. v̄ = 250/120 = **2.08 m/s** (east)

**(d)** Average speed = 550/120 = **4.58 m/s**

**(e)** x(t) is linear with slope +5.0 m/s from t=0 to 80 s (rising), then linear with slope −3.75 m/s from t=80 to 120 s (falling). The graph is two connected straight-line segments with a kink at t = 80 s.

---

### Problem 3

v(t) = 6t² − 4t

**(a)** a(t) = dv/dt = **12t − 4** (NOT constant)

**(b)** x(t) = ∫v dt = 2t³ − 2t² + C. At t=0: x=2 m → C=2. So **x(t) = 2t³ − 2t² + 2**

**(c)** By integration: Δx = ∫₀³(6t²−4t)dt = [2t³−2t²]₀³ = (54−18)−0 = **36 m**
By x(t): x(3) = 2(27)−2(9)+2 = 54−18+2 = 38; x(0) = 2; Δx = 38−2 = **36 m** ✓

**(d)** Acceleration is NOT constant. The 5 kinematic equations must NOT be used.

---

### Problem 4

**(a)** The points are very close to a straight line through the origin. This strongly suggests constant acceleration.

**(b)** Linear fit: slope ≈ (12.1−0)/(5.0−0) ≈ **2.42 m/s²** (accept 2.4–2.5 m/s²; precise regression gives ≈ 2.42 m/s²)

**(c)** Area under v vs. t (trapezoid approximation):
Δx ≈ ½(0+2.4)(1) + ½(2.4+4.8)(1) + ½(4.8+7.3)(1) + ½(7.3+9.6)(1) + ½(9.6+12.1)(1)
= 1.2 + 3.6 + 6.05 + 8.45 + 10.85 = **30.15 m ≈ 30 m**
(Or: ½ × base × height for the whole triangle: ½ × 5 × 12.1 ≈ 30.3 m)

**(d)** x(t) = ½(2.42)t² ≈ **1.21t²** (starting from rest at origin)

---

### Problem 5

Take origin at Train A's start, eastward positive. Train A starts at x=0, Train B starts at x=+2000 m.

**(a)** x_A(t) = 30t; x_B(t) = 2000 − 20t

**(b)** Set equal: 30t = 2000 − 20t → 50t = 2000 → **t = 40 s**

**(c)** x_A(40) = 30(40) = **1200 m** from A's start. Train B moved 20(40) = 800 m → **800 m from B's start.** Check: 1200 + 800 = 2000 ✓

**(d)** v_A relative to B = v_A − v_B = 30 − (−20) = **+50 m/s** (eastward, as seen from Train B's frame)

---

### Problem 6

x(t) = 0.50 sin(2πt)

**(a)** v(t) = 0.50(2π)cos(2πt) = **π cos(2πt) ≈ 3.14 cos(2πt) m/s**
a(t) = −0.50(2π)²sin(2πt) = **−2π² sin(2πt) ≈ −19.74 sin(2πt) m/s²**

**(b)** Max speed = Aω = 0.50 × 2π = **π ≈ 3.14 m/s**, occurring when cos(2πt) = ±1 → t = 0, 0.5 s, 1 s... which corresponds to x = sin(0) = **0 m** (the equilibrium position)

**(c)** Max |a| = Aω² = 0.50 × 4π² = **2π² ≈ 19.7 m/s²**, occurring when |sin(2πt)| = 1 → x = ±A = **±0.50 m** (the turning points)

**(d)** a(t) = −(2π)²(0.50 sin(2πt)) = −ω²x(t) ✓ (since x = A sin(ωt))

**(e)** Not constant acceleration: a depends on position (and hence time). The 5 kinematic equations cannot be used. This requires solutions to a differential equation (d²x/dt² = −ω²x), which we will study in Week 8.

---

### Problem 7

v₀ = 20 m/s, v = 0, t = 4.0 s

**(a)** a = (v−v₀)/t = (0−20)/4.0 = **−5.0 m/s²**

**(b)** Δx = v₀t + ½at² = 20(4) + ½(−5)(16) = 80 − 40 = **40 m**

**(c)** Verify: v² = v₀² + 2aΔx → 0 = 400 + 2(−5)Δx → Δx = 400/10 = **40 m** ✓

---

### Problem 8

**(a)** v = v₀ + at = 0 + 35(8.0) = **280 m/s**

**(b)** Δx₁ = ½at² = ½(35)(64) = **1120 m**

**(c)** After cutoff: v₀ = 280 m/s, v = 0, a = −9.81 m/s².
Δx₂ = v²−v₀²)/(2a) = (0−280²)/(2×−9.81) = −78400/(−19.62) = **3996 m ≈ 4000 m**

**(d)** Total height = 1120 + 3996 = **5116 m ≈ 5100 m**

---

### Problem 9

Origin at Car A's start, forward positive. Car A starts at x=0; Car B starts at x=50 m.

**(a)** x_A(t) = ½(4.0)t² = 2t²; x_B(t) = 50 + 15t

**(b)** Set equal: 2t² = 50 + 15t → 2t² − 15t − 50 = 0
t = [15 ± √(225 + 400)]/4 = [15 ± 25]/4
t = 10 s (physical) or t = −2.5 s (unphysical). **Car A catches Car B at t = 10 s.**

**(c)** v_A = at = 4.0(10) = **40 m/s**

**(d)** Parabola (A) and straight line (B) intersecting at x = 2(100) = 200 m from A's start (equivalently at x_B = 50+150 = 200 m ✓).

---

### Problem 10

v₀ = 5000 m/s, v = 200 m/s, Δx = 1.5×10⁶ m

**(a)** v² = v₀² + 2aΔx → (200)² = (5000)² + 2a(1.5×10⁶)
40000 = 25000000 + 3×10⁶ a
a = (40000 − 25000000)/(3×10⁶) = −24960000/(3×10⁶) = **−8.32 m/s²**

**(b)** t = (v−v₀)/a = (200−5000)/(−8.32) = **576 s ≈ 9.6 min**

**(c)** v = 0, v₀ = 5000 m/s: a = (0−25×10⁶)/(3×10⁶) = **−8.33 m/s²** (essentially same, since 200² is negligible vs 5000²)

---

### Problem 11

v₀ = 8.0 m/s, a = −1.5 m/s²

**(a)** v = 0 when t = v₀/|a| = 8.0/1.5 = **5.33 s**

**(b)** Δx = v₀²/(2|a|) = 64/3 = **21.3 m**

**(c)** At t = 10 s: the ball stopped at t = 5.33 s and remains at rest. **Position = 21.3 m from start.** (A common error is to blindly plug t = 10 into the equation, getting a negative position, which is wrong because the ball cannot roll backward on its own.)

---

### Problem 12

v₀ = +10 m/s, a = −2.0 m/s²

**(a)** Δx = v₀t + ½at² → 12 = 10t − t² → t² − 10t + 12 = 0
t = [10 ± √(100−48)]/2 = [10 ± 7.21]/2 → **t₁ = 1.39 s** (on the way up) and **t₂ = 8.61 s** (on the way back down after reaching max height and descending).

**(b)** At x=0: t=0 (trivial) or 10t − t² = 0 → t(10−t) = 0 → **t = 10 s**.
v(10) = 10 + (−2)(10) = **−10 m/s** (moving in negative direction, same speed as launch — symmetry).

**(c)** Max x when v=0: t = 10/2 = 5 s. x_max = 10(5) − (5²) = 50 − 25 = **25 m**

**(d)** The particle reaches x=0 at t=10 s with v=−10 m/s and keeps accelerating in the −x direction (since a=−2 m/s²) indefinitely. So the particle continues indefinitely in the negative x direction (accelerating). It never has a "farthest negative x" unless there's a boundary condition. Award full credit for this reasoning.

---

### Problem 13

v₀ = 0, a = 3.0×10¹⁴ m/s², Δx = 0.080 m

**(a)** v² = 2aΔx = 2(3×10¹⁴)(0.080) = 4.8×10¹³
v = **√(4.8×10¹³) = 6.93×10⁶ m/s**

**(b)** t = v/a = 6.93×10⁶/(3×10¹⁴) = **2.31×10⁻⁸ s = 23.1 ns**

**(c)** v/c = 6.93×10⁶/3×10⁸ = **0.023 = 2.3% of c**. This is below 10% of c, so relativistic corrections are small but not entirely negligible at the percent level.

---

### Problem 14

**(a)** v = v₀ + at → 10 = 0 + a(4.0) → **a = 2.5 m/s²**

**(b)** Δx₁ = ½(2.5)(16) = **20 m**

**(c)** Remaining distance: 100 − 20 = 80 m at 10 m/s → t₂ = 80/10 = 8.0 s. Total: **4.0 + 8.0 = 12.0 s**

**(d)** Average speed = 100 m / 12.0 s = **8.33 m/s**

---

### Problem 15

v₀ = 0, a = −9.81 m/s², t = 3.5 s (taking down as negative, origin at top)

**(a)** Δy = ½at² = −½(9.81)(12.25) = −60.1 m → cliff height = **60.1 m ≈ 60 m**

**(b)** v = at = (−9.81)(3.5) = **−34.3 m/s**, speed = 34.3 m/s

**(c)** x(t): downward-opening curve (actually downward parabola since displacement goes increasingly negative); v(t): straight line from 0 going increasingly negative.

---

### Problem 16

v₀ = +18 m/s, a = −9.81 m/s², origin = ground, up positive

**(a)** Δy_max = v₀²/(2g) = 324/19.62 = **16.5 m**

**(b)** t_top = v₀/g = 18/9.81 = **1.83 s**

**(c)** Return to ground: 0 = 18t − 4.905t² → t(18 − 4.905t)=0 → **t = 3.67 s** (or 2 × 1.83 s ✓)

**(d)** v(1.5) = 18 − 9.81(1.5) = 18 − 14.72 = **+3.28 m/s** (still moving upward)
v(3.2) = 18 − 9.81(3.2) = 18 − 31.4 = **−13.4 m/s** (moving downward)

**(e)** t = 2.5 s > t_top = 1.83 s, so the ball has passed its peak and is moving **downward**.

---

### Problem 17

Origin at top of building, up positive. Launch point = origin, ground = −30 m.

**(a)** Δy_max = v₀²/(2g) = 144/19.62 = **7.34 m above the building top**

**(b)** Δy = −30 m: −30 = 12t − 4.905t² → 4.905t² − 12t − 30 = 0
t = [12 ± √(144 + 588.6)]/9.81 = [12 ± 27.06]/9.81
t = 39.06/9.81 = **3.98 s**

**(c)** v² = (12)² + 2(−9.81)(−30) = 144 + 588.6 = 732.6 → v = **−27.1 m/s** (downward); speed = **27.1 m/s**

**(d)** Path: goes up 7.34 m, then falls 7.34 m back to launch, then falls another 30 m. Total distance = **7.34 + 7.34 + 30 = 44.7 m**

---

### Problem 18

**(a)** Stone B (thrown downward) hits first — it has a head start in velocity. Stone B hits faster — it has been accelerating from a greater initial speed. Stone A, despite reaching a greater height, returns to the launch level with the same speed (18 m/s) — but then must still fall 40 m to the ground, gaining more speed than B which only had the 40 m to fall from the start.

**Verification:** h = 40 m, |v₀| = 15 m/s, g = 9.81 m/s².

**Stone A** (up positive, launch at y=0, ground at y=−40):
−40 = 15t − 4.905t² → 4.905t² − 15t − 40 = 0
t = [15 ± √(225+784.8)]/9.81 = [15 ± 31.77]/9.81 → t_A = **4.77 s**
v_A = 15 − 9.81(4.77) = **−31.8 m/s**, speed = 31.8 m/s

**Stone B** (down positive, a = +9.81 m/s²):
40 = 15t + 4.905t² → 4.905t² + 15t − 40 = 0
t = [−15 ± √(225+784.8)]/9.81 = [−15 + 31.77]/9.81 → t_B = **1.71 s**
v_B = 15 + 9.81(1.71) = **31.8 m/s**

Both stones hit at the same speed (31.8 m/s) ✓ — confirmed by energy conservation (same height, same |v₀|). Stone B hits much sooner (1.71 s vs 4.77 s) ✓.

---

### Problem 19

Take up positive, origin at ground. Ball 1 dropped from H: y₁ = H − ½gt². Ball 2 thrown up with v₀: y₂ = v₀t − ½gt².

**(a)** Set equal: H − ½gt² = v₀t − ½gt² → H = v₀t → **t_meet = H/v₀**

**(b)** y_meet = v₀(H/v₀) − ½g(H/v₀)² = **H − gH²/(2v₀²)**

**(c)** Ball 1 hits ground when y₁ = 0: t_ground = √(2H/g). Need t_meet < t_ground: H/v₀ < √(2H/g) → H/v₀² < 2/g → **v₀ > √(gH/2)**

**(d)** H = 20 m: v₀_min = √(9.81×20/2) = √98.1 = **9.90 m/s**

---

### Problem 20

**(a)** t = v/g = 55/9.81 = **5.6 s**

**(b)** Δx = v²/(2g) = (55)²/19.62 = **154 m**

**(c)** Air resistance opposes motion — it acts upward while the skydiver falls, reducing the net downward force. The net acceleration is less than g throughout the fall, so it takes longer to reach any given speed than in pure free fall. As speed increases, the drag force increases (roughly as v²), reducing the net acceleration further, until drag equals gravity and acceleration reaches zero at terminal velocity.

**(d)** With air resistance, the net force is F_net = mg − bv (or mg − cv², depending on the drag model). Newton's second law gives ma = mg − bv, i.e., a = g − (b/m)v. Acceleration is now a function of velocity (and hence time) — NOT constant. The 5 kinematic equations assume a = const and are therefore invalid. You would need to solve the first-order ODE dv/dt = g − (b/m)v (separable; solution involves an exponential approach to terminal velocity: v(t) = v_terminal(1 − e^(−bt/m))).
