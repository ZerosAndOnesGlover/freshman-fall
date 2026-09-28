# PHYS 141 · Problem Set 1 — INSTRUCTOR SOLUTIONS
**Do not distribute before the due date.**

---

> *Revised 2026-09-28: sub-parts cut from 41 to 20, two per problem; the ten problems and their points are unchanged. The answers below keep the old letters. New → old: 1 (a, b) = (c, d) · 2 (a, b) = (c, d) · 3 (a, b) = (a, b) · 4 (a, b) = (a, b) · 5 (a, b) = (b, c) · 6 (a, b) = (a, b) · 7 (a, b) = (a, b) · 8 (a, b) = (a, c) · 9 (a, b) = (b, c) · 10 (a, b) = (a, c).*


*Revised 2026-09-21 to match the 10-problem set; problems are numbered as in the new set.*

## Marking Scheme

Each of the 10 problems is worth **10 points**, matching the point allocation printed on the problem set:

- **6 points — method.** A labelled diagram where forces or vectors are involved, an explicit coordinate/sign convention, the governing principle named, and the symbolic setup before numbers are substituted.
- **4 points — answer.** Correct value, correct units, and significant figures consistent with the given data.

A correct final answer with no supporting work earns **at most 4 of 10**. Conversely, a correct method carried through with one arithmetic slip should retain all 3 method marks — grade the physics, not the calculator.

**Carry-through (error propagation).** If a student makes one error early and then reasons correctly from their own wrong value, deduct once at the point of error and award full marks downstream. Do not penalise the same mistake twice.

### Part allocation

| Part | Topic | Problems | Points |
|---|---|---|---|
| **A** | Displacement, Velocity & the Derivative | 1–3 | 30 |
| **B** | Constant Acceleration & Kinematic Equations | 4–6 | 30 |
| **C** | Free Fall | 7–10 | 40 |
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

v₀ = 20 m/s, v = 0, t = 4.0 s

**(a)** a = (v−v₀)/t = (0−20)/4.0 = **−5.0 m/s²**

**(b)** Δx = v₀t + ½at² = 20(4) + ½(−5)(16) = 80 − 40 = **40 m**

**(c)** Verify: v² = v₀² + 2aΔx → 0 = 400 + 2(−5)Δx → Δx = 400/10 = **40 m** ✓

---

### Problem 5

Origin at Car A's start, forward positive. Car A starts at x=0; Car B starts at x=50 m.

**(a)** x_A(t) = ½(4.0)t² = 2t²; x_B(t) = 50 + 15t

**(b)** Set equal: 2t² = 50 + 15t → 2t² − 15t − 50 = 0
t = [15 ± √(225 + 400)]/4 = [15 ± 25]/4
t = 10 s (physical) or t = −2.5 s (unphysical). **Car A catches Car B at t = 10 s.**

**(c)** v_A = at = 4.0(10) = **40 m/s**

**(d)** Parabola (A) and straight line (B) intersecting at x = 2(100) = 200 m from A's start (equivalently at x_B = 50+150 = 200 m ✓).

---

### Problem 6

v₀ = +10 m/s, a = −2.0 m/s²

**(a)** Δx = v₀t + ½at² → 12 = 10t − t² → t² − 10t + 12 = 0
t = [10 ± √(100−48)]/2 = [10 ± 7.21]/2 → **t₁ = 1.39 s** (on the way up) and **t₂ = 8.61 s** (on the way back down after reaching max height and descending).

**(b)** At x=0: t=0 (trivial) or 10t − t² = 0 → t(10−t) = 0 → **t = 10 s**.
v(10) = 10 + (−2)(10) = **−10 m/s** (moving in negative direction, same speed as launch — symmetry).

**(c)** Max x when v=0: t = 10/2 = 5 s. x_max = 10(5) − (5²) = 50 − 25 = **25 m**

**(d)** The particle reaches x=0 at t=10 s with v=−10 m/s and keeps accelerating in the −x direction (since a=−2 m/s²) indefinitely. So the particle continues indefinitely in the negative x direction (accelerating). It never has a "farthest negative x" unless there's a boundary condition. Award full credit for this reasoning.

---

### Problem 7

v₀ = 0, a = −9.81 m/s², t = 3.5 s (taking down as negative, origin at top)

**(a)** Δy = ½at² = −½(9.81)(12.25) = −60.1 m → cliff height = **60.1 m ≈ 60 m**

**(b)** v = at = (−9.81)(3.5) = **−34.3 m/s**, speed = 34.3 m/s

**(c)** x(t): downward-opening curve (actually downward parabola since displacement goes increasingly negative); v(t): straight line from 0 going increasingly negative.

---

### Problem 8

v₀ = +18 m/s, a = −9.81 m/s², origin = ground, up positive

**(a)** Δy_max = v₀²/(2g) = 324/19.62 = **16.5 m**

**(b)** t_top = v₀/g = 18/9.81 = **1.83 s**

**(c)** Return to ground: 0 = 18t − 4.905t² → t(18 − 4.905t)=0 → **t = 3.67 s** (or 2 × 1.83 s ✓)

**(d)** v(1.5) = 18 − 9.81(1.5) = 18 − 14.72 = **+3.28 m/s** (still moving upward)
v(3.2) = 18 − 9.81(3.2) = 18 − 31.4 = **−13.4 m/s** (moving downward)

**(e)** t = 2.5 s > t_top = 1.83 s, so the ball has passed its peak and is moving **downward**.

---

### Problem 9

Origin at top of building, up positive. Launch point = origin, ground = −30 m.

**(a)** Δy_max = v₀²/(2g) = 144/19.62 = **7.34 m above the building top**

**(b)** Δy = −30 m: −30 = 12t − 4.905t² → 4.905t² − 12t − 30 = 0
t = [12 ± √(144 + 588.6)]/9.81 = [12 ± 27.06]/9.81
t = 39.06/9.81 = **3.98 s**

**(c)** v² = (12)² + 2(−9.81)(−30) = 144 + 588.6 = 732.6 → v = **−27.1 m/s** (downward); speed = **27.1 m/s**

**(d)** Path: goes up 7.34 m, then falls 7.34 m back to launch, then falls another 30 m. Total distance = **7.34 + 7.34 + 30 = 44.7 m**

---

### Problem 10

Take up positive, origin at ground. Ball 1 dropped from H: y₁ = H − ½gt². Ball 2 thrown up with v₀: y₂ = v₀t − ½gt².

**(a)** Set equal: H − ½gt² = v₀t − ½gt² → H = v₀t → **t_meet = H/v₀**

**(b)** y_meet = v₀(H/v₀) − ½g(H/v₀)² = **H − gH²/(2v₀²)**

**(c)** Ball 1 hits ground when y₁ = 0: t_ground = √(2H/g). Need t_meet < t_ground: H/v₀ < √(2H/g) → H/v₀² < 2/g → **v₀ > √(gH/2)**

**(d)** H = 20 m: v₀_min = √(9.81×20/2) = √98.1 = **9.90 m/s**

---
