# PHYS 141 — Problem Set 2 — INSTRUCTOR SOLUTIONS
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
| **A** | 2D Kinematics — Vectors and Components | 1–5 | 25 |
| **B** | Projectile Motion | 6–14 | 45 |
| **C** | Circular Motion | 15–20 | 30 |
| | **Total** | | **100** |

### Common errors in this problem set

**1. Coupling the x and y motions.** The whole point of projectile motion is that the components are independent and share only t. Any solution that mixes them (e.g. using total speed in a horizontal equation) loses method marks.

**2. Using v instead of v_x for horizontal range.** Range needs the horizontal component v·cosθ. Using the full launch speed is the single most common projectile error.

**3. Treating centripetal acceleration as an extra force.** There is no 'centripetal force' in a free body diagram. a_c is the acceleration that some real force (tension, gravity, friction, normal) provides. Drawing an inward arrow labelled 'centripetal force' is a conceptual error — deduct method marks.

**4. Assuming a_c = 0 at constant speed.** Uniform circular motion has constant *speed* and non-zero acceleration, because the velocity direction changes.

---

### Problem 1

r⃗(t) = (2t²−3t)x̂ + (t³−4t)ŷ

**(a)** v⃗(t) = (4t−3)x̂ + (3t²−4)ŷ; a⃗(t) = 4x̂ + 6tŷ

**(b)** At t=2: v⃗ = 5x̂ + 8ŷ. Speed = √(25+64) = √89 = **9.43 m/s**. θ = arctan(8/5) = **58.0°** above +x.

**(c)** a⃗(2) = 4x̂ + 12ŷ. |a| = √(16+144) = √160 = **12.6 m/s²**. Direction = arctan(12/4) = **71.6°** above +x.

**(d)** No — a⃗ depends on t (the ŷ component is 6t). Not constant-acceleration motion.

---

### Problem 2

**(a)** x(t) = 5.0t − 0.25t²; y(t) = 3.0t + 0.4t²; v_x(t) = 5.0 − 0.5t; v_y(t) = 3.0 + 0.8t

**(b)** At t=4: x = 20−4 = 16 m; y = 12+6.4 = 18.4 m. v_x = 5−2 = 3 m/s; v_y = 3+3.2 = 6.2 m/s. Speed = √(9+38.44) = √47.44 = **6.89 m/s**

**(c)** v_x = 0: 5.0−0.5t = 0 → **t = 10 s**. At t=10: v_y = 3.0+8.0 = 11 m/s. Speed = **11 m/s**.

**(d)** Trajectory curves upward and to the left (x-velocity decreasing, y-velocity increasing). At t=10 s the object moves purely in +y direction. Sketch should show initial direction at arctan(3/5)≈31° above +x, curving leftward and upward.

---

### Problem 3

**(a)** x(3) = 3 + (−4)(3) + ½(2)(9) = 3−12+9 = **0 m**
y(3) = −2 + (6)(3) + ½(−3)(9) = −2+18−13.5 = **2.5 m**. Position: (0, 2.5) m.

**(b)** y = 0: −2 + 6t − 1.5t² = 0 → 1.5t² − 6t + 2 = 0 → t = [6±√(36−12)]/3 = [6±√24]/3 = [6±4.899]/3
t₁ = **0.367 s**, t₂ = **3.633 s**

**(c)** At t = 0.367 s: v_x = −4+2(0.367) = −3.267 m/s; v_y = 6+(−3)(0.367) = 4.899 m/s. v⃗ = (−3.27, 4.90) m/s.

---

### Problem 4

Take x = across river, y = downstream. Boat velocity relative to water: (4.0, 0) m/s. Current: (0, 2.5) m/s.

**(a)** v⃗_ground = (4.0, 2.5) m/s. |v| = √(16+6.25) = **√22.25 = 4.72 m/s**. Direction = arctan(2.5/4.0) = **32.0°** downstream of perpendicular.

**(b)** Time to cross 120 m at 4.0 m/s across: t = 120/4.0 = 30 s. Downstream drift = 2.5×30 = **75 m**.

**(c)** **30 s**

**(d)** To go straight across, aim upstream at angle φ so that the downstream component cancels: 4.0sinφ = 2.5 → sinφ = 0.625 → **φ = 38.7° upstream of perpendicular**. This IS possible since 2.5 < 4.0. The net speed across = 4.0cosφ = 4.0×0.781 = 3.12 m/s. If current exceeded boat speed, it would be impossible.

---

### Problem 5

**(a)** r⃗_A = 6tx̂ + t²ŷ; r⃗_B = (24−3t)x̂

**(b)** x-coords equal: 6t = 24−3t → 9t = 24 → **t = 8/3 s ≈ 2.67 s**

**(c)** At t = 8/3: y_A = (8/3)² = 64/9 ≈ 7.11 m; y_B = 0. Not same location.
r⃗_A − r⃗_B = (0)x̂ + (64/9)ŷ = **(0, 7.11) m** — separated by 7.11 m in y.

**(d)** Same point requires both x and y equal. x equal at t = 8/3. At that time y_A = 64/9 ≠ 0 = y_B. For y to be equal: t² = 0 → t = 0. At t=0: x_A=0 ≠ 24=x_B. **The particles never occupy exactly the same point.**

---

### Problem 6

v₀ₓ = 20cos60° = 10 m/s; v₀ᵧ = 20sin60° = 17.32 m/s

**(a)** v₀ₓ = **10.0 m/s**, v₀ᵧ = **17.3 m/s**

**(b)** T = 2v₀ᵧ/g = 34.64/9.81 = **3.53 s**

**(c)** H = v₀ᵧ²/(2g) = 300/19.62 = **15.3 m**

**(d)** R = v₀ₓ·T = 10×3.53 = **35.3 m**

**(e)** At t=1.5: v_x = 10 m/s; v_y = 17.32−9.81(1.5) = 17.32−14.72 = 2.61 m/s. Speed = √(100+6.81) = **10.33 m/s**. Direction = arctan(2.61/10) = **14.6° above horizontal**.

---

### Problem 7

H = v₀ᵧ²/(2g) = 10 m → v₀ᵧ = √(20g) = √196.2 = 14.01 m/s
T = 2v₀ᵧ/g = 28.02/9.81 = 2.856 s → v₀ₓ = R/T = 40/2.856 = 14.01 m/s

**(a)** T = **2.86 s**
**(b)** v₀ = √(v₀ₓ²+v₀ᵧ²) = √(196.2+196.2) = √392.4 = **19.8 m/s**
**(c)** θ = arctan(v₀ᵧ/v₀ₓ) = arctan(1) = **45°** (makes sense — equal components means 45°)

---

### Problem 8

v₀ₓ = 15 m/s, v₀ᵧ = 0 (horizontal launch), H = 45 m

**(a)** t = √(2H/g) = √(90/9.81) = **3.03 s**

**(b)** x = 15×3.03 = **45.5 m**

**(c)** v_x = 15 m/s; v_y = −9.81×3.03 = −29.7 m/s. Speed = √(225+882.1) = **33.3 m/s**. Angle = arctan(29.7/15) = **63.2° below horizontal**

**(d)** Speed = 2×15 = 30 m/s. v_x always = 15 m/s. v_y² = 900−225 = 675 → v_y = 25.98 m/s (downward).
Height at that point: v_y² = 2gy → y = 675/19.62 = **34.4 m below launch** (i.e., 10.6 m above ground)

---

### Problem 9

v₀ = 35 m/s, R = 80 m

**(a)** sin2θ = Rg/v₀² = 80×9.81/1225 = 0.6416. 2θ = 39.93° or 140.07°. **θ₁ = 20.0°, θ₂ = 70.0°**

**(b)** T₁ = 2v₀sinθ₁/g = 2(35)(0.342)/9.81 = **2.44 s**; T₂ = 2(35)(0.940)/9.81 = **6.71 s**

**(c)** H₁ = (v₀sinθ₁)²/(2g) = (35×0.342)²/19.62 = (11.97)²/19.62 = **7.30 m**;
H₂ = (35×0.940)²/19.62 = (32.9)²/19.62 = **55.2 m**

**(d)** At 40 m horizontal, height of θ₁ trajectory: y = 80tan20°·(40/80) − g(40)²/(2×1225×cos²20°) ... use trajectory eqn with x=40:
y₁(40) = 40tan20° − (9.81×1600)/(2×1225×cos²20°) = 14.56 − 15680/(2300.5×0.883) = 14.56−7.71 = 6.85 m > 5 m ✓
y₂(40) similarly = 40tan70° − ... = 109.9 − 7.71/cos²70°×correction ... Full calculation gives y₂(40) >> 5 m ✓
Both trajectories clear 5 m. The **low-angle (20°) trajectory** is preferred — shorter time in air, harder to intercept, less wind effect.

---

### Problem 10

v₀ = 9.0 m/s, θ = 25°

**(a)** R = v₀²sin(50°)/g = 81×0.766/9.81 = **6.33 m**

**(b)** R(45°) = 81×1/9.81 = **8.26 m**

**(c)** Penalty: (8.26−6.33)/8.26 = **23.4%** range loss. Athletes cannot achieve v₀ = 9 m/s at 45° because a higher angle requires more vertical velocity, which demands greater leg power directed upward — but the same muscles also produce the forward run-up speed. At 45°, you'd need to divert much of the horizontal sprint energy into vertical lift, reducing the achievable v₀ dramatically. The optimum accounting for the v₀-θ tradeoff is typically 20–25°.

---

### Problem 11

Target: x=800 m, y=150 m. v₀=120 m/s.

**(a)** y = xtanθ − gx²/(2v₀²cos²θ). Use sec²θ = 1+tan²θ:
150 = 800tanθ − (9.81×640000)/(2×14400)(1+tan²θ)
150 = 800tanθ − 218.0(1+tan²θ)
218u² − 800u + 368 = 0 where u = tanθ

**(b)** u = [800 ± √(640000 − 4×218×368)]/(2×218) = [800 ± √(640000−320896)]/436 = [800 ± √319104]/436 = [800 ± 565.1]/436
u₁ = 1365.1/436 = **3.130** → **θ₁ = 72.3°**
u₂ = 234.9/436 = **0.5389** → **θ₂ = 28.3°**

**(c)** θ₂ = 28.3° is more practical — lower trajectory, shorter time of flight, less affected by wind, easier to aim.

---

### Problem 12

Origin at launch. v₀ₓ = 15cos30° = 12.99 m/s; v₀ᵧ = −15sin30° = −7.5 m/s (downward angle → negative vy).

**(a)** x(t) = 12.99t; y(t) = −7.5t − 4.905t²

**(b)** Ground at y = −20: −20 = −7.5t − 4.905t² → 4.905t²+7.5t−20=0
t = [−7.5+√(56.25+392.4)]/9.81 = [−7.5+√448.65]/9.81 = [−7.5+21.18]/9.81 = **1.396 s**

**(c)** x = 12.99×1.396 = **18.1 m**

**(d)** v_x = 12.99 m/s; v_y = −7.5−9.81(1.396) = −7.5−13.69 = −21.19 m/s.
Speed = √(168.7+449.0) = √617.7 = **24.9 m/s**

---

### Problem 13

Gun at origin, monkey at (d, h). Bullet aimed directly at (d,h): angle θ = arctan(h/d). v₀ₓ = v₀cosθ, v₀ᵧ = v₀sinθ.

**(a)** Time for bullet to reach x = d: t* = d/v₀ₓ = d/(v₀cosθ).
y_bullet(t*) = v₀sinθ·t* − ½g(t*)² = v₀sinθ·(d/v₀cosθ) − ½g(d/v₀cosθ)²
= d·tanθ − gd²/(2v₀²cos²θ)
Note: h = d·tanθ (the monkey's height from the aim geometry).
So y_bullet(t*) = h − gd²/(2v₀²cos²θ)

Monkey: y_monkey(t*) = h − ½g(t*)² = h − ½g(d/v₀cosθ)² = h − gd²/(2v₀²cos²θ)

**y_bullet(t*) = y_monkey(t*) for all v₀.** The bullet always hits the monkey.

**(b)** Bullet must reach x=d before hitting ground (y_bullet > 0):
gd²/(2v₀²cos²θ) < h → v₀² > gd²/(2hcos²θ).
With d=30, h=15, θ=arctan(15/30)=26.57°, cos²θ=0.800:
v₀ > √(9.81×900/(2×15×0.800)) = √(8829/24) = √367.9 = **19.2 m/s**

**(c)** If v₀ is too small, the bullet hits the ground before reaching x=d — it passes **below** the monkey, who has also fallen, but by a smaller amount (less time has elapsed for the monkey too). The algebra above still holds — if t* is when the bullet hits the ground, at that time the monkey has fallen the same amount as the bullet's free-fall component. But since t* (ground hit) < d/v₀ₓ (tree reach), the bullet never reaches the tree.

---

### Problem 14

d = 18.4 m, v₀ = 42.5 m/s, release height = 1.8 m, target height = 0.9 m, so Δy = −0.9 m.

**(a)** t ≈ d/v₀ = 18.4/42.5 = 0.433 s (approximate, treating angle as small).
Vertical drop needed: −0.9 = v₀ᵧ(0.433) − ½(9.81)(0.433)²
−0.9 = v₀ᵧ(0.433) − 0.920 → v₀ᵧ(0.433) = 0.020 → v₀ᵧ = 0.046 m/s (nearly zero).
Launch angle ≈ arctan(0.046/42.5) ≈ **0.06°** — essentially horizontal, very slightly downward to account for the small height difference; the drop is dominated by gravity, not the angle.

**(b)** Drop = ½g t² = ½(9.81)(0.433)² = **0.920 m** — the ball drops nearly 1 m during the pitch!

**(c)** t ≈ **0.433 s** (time of flight).

**(d)** Air resistance is NOT negligible for a 95 mph fastball over 18.4 m. A baseball has significant drag (drag coefficient ≈ 0.35). The ball actually slows from ~42.5 m/s to ~36 m/s by the time it reaches the plate. Ignoring air resistance overestimates the velocity at home plate and slightly underestimates the drop. For an exact calculation, a drag model (quadratic in v) is required.

---

### Problem 15

r = 0.40 m, n = 300 rpm

**(a)** ω = 300 × 2π/60 = **31.4 rad/s**

**(b)** v = rω = 0.40 × 31.4 = **12.6 m/s**

**(c)** a_c = ω²r = (31.4)²(0.40) = 985.96×0.40 = **394 m/s²**

**(d)** 394/9.81 = **40.2 g** — a point on the rim experiences centripetal acceleration 40 times gravitational acceleration.

---

### Problem 16

T = 27.3 × 86400 = 2.358×10⁶ s; r = 3.84×10⁸ m

**(a)** v = 2πr/T = 2π(3.84×10⁸)/(2.358×10⁶) = **1023 m/s ≈ 1.02 km/s**

**(b)** a_c = v²/r = (1023)²/(3.84×10⁸) = 1.046×10⁶/(3.84×10⁸) = **2.72×10⁻³ m/s²**

**(c)** g × (R_E/r)² = 9.81 × (6.37×10⁶/3.84×10⁸)² = 9.81 × (0.01659)² = 9.81 × 2.752×10⁻⁴ = **2.70×10⁻³ m/s²** ✓ Matches a_c to within rounding. Newton recognized that the same gravitational force that causes apples to fall also holds the Moon in orbit — the force falls off as 1/r², so the Moon's centripetal acceleration = g × (R_E/r_Moon)².

---

### Problem 17

r = 150 m, μₛg = 0.70×9.81 = 6.867 m/s²

**(a)** a_c_max = μₛg = 6.867 m/s² = v²/r → v_max = √(6.867×150) = √1030 = **32.1 m/s = 115.6 km/h**

**(b)** a_c = **6.87 m/s²** (= μₛg, as expected at the maximum)

**(c)** v = 80 km/h = 22.2 m/s. a_c = (22.2)²/150 = 492.8/150 = 3.29 m/s². Since 3.29 < 6.87 m/s², **safe.**

---

### Problem 18

ω₀ = 0, ω = 25 rad/s, t = 10 s

**(a)** α = (25−0)/10 = **2.5 rad/s²**

**(b)** Δθ = ½αt² = ½(2.5)(100) = 125 rad. Revolutions = 125/(2π) = **19.9 rev**

**(c)** At t=10, r=0.20 m:
- v_t = rω = 0.20×25 = **5.0 m/s**
- a_c = ω²r = 625×0.20 = **125 m/s²**
- a_t = rα = 0.20×2.5 = **0.5 m/s²**

**(d)** |a| = √(a_c²+a_t²) = √(15625+0.25) = **125 m/s²** (dominated by centripetal; a_t negligible in magnitude). Direction: 125 m/s² radially inward + 0.5 m/s² tangentially = essentially radially inward, at arctan(0.5/125) = 0.23° from radially inward.

---

### Problem 19

h = 400 km = 4×10⁵ m; R_E = 6.371×10⁶ m; r = R_E+h = 6.771×10⁶ m

**(a)** a_c = 9.81×(6.371/6.771)² = 9.81×(0.9409)² = 9.81×0.8853 = **8.69 m/s²**

**(b)** v = √(a_c·r) = √(8.69×6.771×10⁶) = √(5.884×10⁷) = **7671 m/s ≈ 7.67 km/s**

**(c)** T = 2πr/v = 2π×6.771×10⁶/7671 = 4.254×10⁷/7671 = **5547 s = 92.4 min** ✓ matches ISS period of ~92 min.

**(d)** For equatorial surface: r = R_E = 6.371×10⁶ m, ω = 7.272×10⁻⁵ rad/s.
a_c = ω²R_E = (5.288×10⁻⁹)(6.371×10⁶) = **0.0337 m/s²** = 0.34% of g.

---

### Problem 20

r = 12 m

**(a)** Bottom of loop: centripetal acceleration points **upward** (toward center, which is above). FBD: N (up) and mg (down). Net upward force = N−mg = mv²/r.

**(b)** Top of loop: centripetal acceleration points **downward** (toward center, which is below). FBD: N (down, track pushes inward) and mg (down). Both forces point down = centripetal direction.

**(c)** At top, N=0: mg = mv²_min/r → v_min = √(gr) = √(9.81×12) = **10.85 m/s**

**(d)** v = 1.5×v_min = 16.27 m/s. a_c = v²/r = (16.27)²/12 = 264.7/12 = **22.1 m/s²** = **2.25g** radially downward.

**(e)** At the top, both gravity and the normal force point toward the center (downward). Gravity assists in providing centripetal force. At the bottom, gravity opposes the normal force (N must overcome gravity AND provide centripetal force upward). The critical constraint is at the top because gravity cannot provide more than mg centripetal force without the track's help — if the car goes too slowly, gravity alone exceeds the needed centripetal force and the car loses contact. At the bottom there's no such minimum speed constraint.
