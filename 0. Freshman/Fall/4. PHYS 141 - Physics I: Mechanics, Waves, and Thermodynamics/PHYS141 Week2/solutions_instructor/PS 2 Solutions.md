# PHYS 141 · Problem Set 2 — INSTRUCTOR SOLUTIONS
**Do not distribute before the due date.**

---

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
| **A** | 2D Kinematics — Vectors and Components | 1–2 | 20 |
| **B** | Projectile Motion | 3–6 | 40 |
| **C** | Circular Motion | 7–10 | 40 |
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

Take x = across river, y = downstream. Boat velocity relative to water: (4.0, 0) m/s. Current: (0, 2.5) m/s.

**(a)** v⃗_ground = (4.0, 2.5) m/s. |v| = √(16+6.25) = **√22.25 = 4.72 m/s**. Direction = arctan(2.5/4.0) = **32.0°** downstream of perpendicular.

**(b)** Time to cross 120 m at 4.0 m/s across: t = 120/4.0 = 30 s. Downstream drift = 2.5×30 = **75 m**.

**(c)** **30 s**

**(d)** To go straight across, aim upstream at angle φ so that the downstream component cancels: 4.0sinφ = 2.5 → sinφ = 0.625 → **φ = 38.7° upstream of perpendicular**. This IS possible since 2.5 < 4.0. The net speed across = 4.0cosφ = 4.0×0.781 = 3.12 m/s. If current exceeded boat speed, it would be impossible.

---

### Problem 3

v₀ₓ = 20cos60° = 10 m/s; v₀ᵧ = 20sin60° = 17.32 m/s

**(a)** v₀ₓ = **10.0 m/s**, v₀ᵧ = **17.3 m/s**

**(b)** T = 2v₀ᵧ/g = 34.64/9.81 = **3.53 s**

**(c)** H = v₀ᵧ²/(2g) = 300/19.62 = **15.3 m**

**(d)** R = v₀ₓ·T = 10×3.53 = **35.3 m**

**(e)** At t=1.5: v_x = 10 m/s; v_y = 17.32−9.81(1.5) = 17.32−14.72 = 2.61 m/s. Speed = √(100+6.81) = **10.33 m/s**. Direction = arctan(2.61/10) = **14.6° above horizontal**.

---

### Problem 4

v₀ₓ = 15 m/s, v₀ᵧ = 0 (horizontal launch), H = 45 m

**(a)** t = √(2H/g) = √(90/9.81) = **3.03 s**

**(b)** x = 15×3.03 = **45.5 m**

**(c)** v_x = 15 m/s; v_y = −9.81×3.03 = −29.7 m/s. Speed = √(225+882.1) = **33.3 m/s**. Angle = arctan(29.7/15) = **63.2° below horizontal**

**(d)** Speed = 2×15 = 30 m/s. v_x always = 15 m/s. v_y² = 900−225 = 675 → v_y = 25.98 m/s (downward).
Height at that point: v_y² = 2gy → y = 675/19.62 = **34.4 m below launch** (i.e., 10.6 m above ground)

---

### Problem 5

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

### Problem 6

Origin at launch. v₀ₓ = 15cos30° = 12.99 m/s; v₀ᵧ = −15sin30° = −7.5 m/s (downward angle → negative vy).

**(a)** x(t) = 12.99t; y(t) = −7.5t − 4.905t²

**(b)** Ground at y = −20: −20 = −7.5t − 4.905t² → 4.905t²+7.5t−20=0
t = [−7.5+√(56.25+392.4)]/9.81 = [−7.5+√448.65]/9.81 = [−7.5+21.18]/9.81 = **1.396 s**

**(c)** x = 12.99×1.396 = **18.1 m**

**(d)** v_x = 12.99 m/s; v_y = −7.5−9.81(1.396) = −7.5−13.69 = −21.19 m/s.
Speed = √(168.7+449.0) = √617.7 = **24.9 m/s**

---

### Problem 7

r = 0.40 m, n = 300 rpm

**(a)** ω = 300 × 2π/60 = **31.4 rad/s**

**(b)** v = rω = 0.40 × 31.4 = **12.6 m/s**

**(c)** a_c = ω²r = (31.4)²(0.40) = 985.96×0.40 = **394 m/s²**

**(d)** 394/9.81 = **40.2 g** — a point on the rim experiences centripetal acceleration 40 times gravitational acceleration.

---

### Problem 8

T = 27.3 × 86400 = 2.358×10⁶ s; r = 3.84×10⁸ m

**(a)** v = 2πr/T = 2π(3.84×10⁸)/(2.358×10⁶) = **1023 m/s ≈ 1.02 km/s**

**(b)** a_c = v²/r = (1023)²/(3.84×10⁸) = 1.046×10⁶/(3.84×10⁸) = **2.72×10⁻³ m/s²**

**(c)** g × (R_E/r)² = 9.81 × (6.37×10⁶/3.84×10⁸)² = 9.81 × (0.01659)² = 9.81 × 2.752×10⁻⁴ = **2.70×10⁻³ m/s²** ✓ Matches a_c to within rounding. Newton recognized that the same gravitational force that causes apples to fall also holds the Moon in orbit — the force falls off as 1/r², so the Moon's centripetal acceleration = g × (R_E/r_Moon)².

---

### Problem 9

ω₀ = 0, ω = 25 rad/s, t = 10 s

**(a)** α = (25−0)/10 = **2.5 rad/s²**

**(b)** Δθ = ½αt² = ½(2.5)(100) = 125 rad. Revolutions = 125/(2π) = **19.9 rev**

**(c)** At t=10, r=0.20 m:
- v_t = rω = 0.20×25 = **5.0 m/s**
- a_c = ω²r = 625×0.20 = **125 m/s²**
- a_t = rα = 0.20×2.5 = **0.5 m/s²**

**(d)** |a| = √(a_c²+a_t²) = √(15625+0.25) = **125 m/s²** (dominated by centripetal; a_t negligible in magnitude). Direction: 125 m/s² radially inward + 0.5 m/s² tangentially = essentially radially inward, at arctan(0.5/125) = 0.23° from radially inward.

---

### Problem 10

h = 400 km = 4×10⁵ m; R_E = 6.371×10⁶ m; r = R_E+h = 6.771×10⁶ m

**(a)** a_c = 9.81×(6.371/6.771)² = 9.81×(0.9409)² = 9.81×0.8853 = **8.69 m/s²**

**(b)** v = √(a_c·r) = √(8.69×6.771×10⁶) = √(5.884×10⁷) = **7671 m/s ≈ 7.67 km/s**

**(c)** T = 2πr/v = 2π×6.771×10⁶/7671 = 4.254×10⁷/7671 = **5547 s = 92.4 min** ✓ matches ISS period of ~92 min.

**(d)** For equatorial surface: r = R_E = 6.371×10⁶ m, ω = 7.272×10⁻⁵ rad/s.
a_c = ω²R_E = (5.288×10⁻⁹)(6.371×10⁶) = **0.0337 m/s²** = 0.34% of g.

---
