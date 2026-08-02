# PHYS 141 · Problem Set 3 — INSTRUCTOR SOLUTIONS
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
| **A** | Newton's First and Second Laws | 1–7 | 35 |
| **B** | Newton's Third Law | 8–10 | 15 |
| **C** | Friction | 11–14 | 20 |
| **D** | Connected Systems and Inclines | 15–20 | 30 |
| | **Total** | | **100** |

### Common errors in this problem set

**1. Assuming N = mg always.** The normal force equals mg only for a horizontal surface with no vertical acceleration and no other vertical forces. On an incline, in a lift, or with an applied vertical component it does not. This is the highest-frequency error in the set.

**2. Putting an action–reaction pair on the same free body diagram.** Third-law pairs act on *different* bodies and can never both appear in one FBD. If both are drawn, the diagram is wrong regardless of the final number.

**3. Using f = μN for static friction.** Static friction is f ≤ μ_s N — it takes whatever value is needed up to the maximum. Only kinetic friction is f = μ_k N. Using the equality for a static problem is a method error.

**4. Losing the massless-string idealisation.** Tension is uniform throughout a massless string over a frictionless pulley. Introducing different tensions on the two sides without justification is wrong; so is ignoring a *stated* pulley mass.

---

### Problem 1

**(a)** m = F/a = 48/6.0 = **8.0 kg**

**(b)** m = 48/24 = **2.0 kg**

**(c)** m_total = 10.0 kg. a = 48/10.0 = **4.8 m/s²**

---

### Problem 2

**(a)** a = Δv/t = 25/8.0 = **3.125 m/s²**

**(b)** F_net = ma = 1200×3.125 = **3750 N**

**(c)** F_engine − F_friction = F_net → F_friction = 5500−3750 = **1750 N**

**(d)** a = (0−25)/5.0 = −5.0 m/s². F_brake = ma = 1200×5.0 = **6000 N** (opposing motion)

---

### Problem 3

**(a)** F⃗_net = (12−5+0, 0+8−6) = **(7, 2) N**

**(b)** a⃗ = F⃗/m = (7/2.5, 2/2.5) = **(2.8, 0.80) m/s²**

**(c)** |a| = √(7.84+0.64) = √8.48 = **2.91 m/s²**. Direction = arctan(0.80/2.80) = **15.9° above +x**

**(d)** From rest: v⃗ = a⃗t = (2.8×3, 0.80×3) = **(8.4, 2.4) m/s** at t=3 s.
r⃗ = ½a⃗t² = (½×2.8×9, ½×0.80×9) = **(12.6, 3.6) m** from start.

---

### Problem 4

N is what the scale reads. ΣFᵧ = N − mg = ma.

**(a)** a=0: N = mg = 70×9.81 = **686 N**

**(b)** a = +2.5 m/s² (up): N = m(g+a) = 70×12.31 = **862 N**

**(c)** Constant velocity: a=0. N = **686 N** (same as rest)

**(d)** Decelerating while moving up: a = −1.8 m/s². N = m(g−1.8) = 70×7.01 = **491 N**

**(e)** Free fall: a = −g. N = m(g−g) = **0 N**. The person is weightless — no contact force from scale. They feel as if floating. This is identical to orbital weightlessness.

---

### Problem 5

Let T₁ = tension in left string (30° from vertical), T₂ = tension in right string (60° from vertical).

**(a)** FBD: weight W = mg = 0.50×9.81 = 4.905 N downward; T₁ upward-left at 30° from vertical (60° from horizontal); T₂ upward-right at 60° from vertical (30° from horizontal).

**(b)** ΣFₓ = 0: −T₁ sin30° + T₂ sin60° = 0 → T₂ sin60° = T₁ sin30°
ΣFᵧ = 0: T₁ cos30° + T₂ cos60° − mg = 0

**(c)** From x: T₁ = T₂(sin60°/sin30°) = T₂(0.866/0.500) = 1.732 T₂
Substitute into y: 1.732T₂(0.866) + T₂(0.500) = 4.905
1.500T₂ + 0.500T₂ = 4.905 → 2.000T₂ = 4.905 → **T₂ = 2.45 N**
**T₁ = 1.732×2.45 = 4.24 N**

**(d)** As the right string angle from vertical increases toward 90° (nearly horizontal), sin60°→1 and cos60°→0. From x: T₂ = T₁sin30°/sin60° — but T₁ must support nearly all of the weight (cos30° term dominates in y equation). As the angle → 90°, T₂ → ∞ because the string is nearly horizontal and can provide almost no vertical support. This is exactly why you cannot make a perfectly horizontal cable support a vertical load — infinite tension would be required.

---

### Problem 6

The cable forms a "V" shape. Each half of the cable makes angle θ with horizontal.

tan θ = vertical sag / half-span = 0.30/6.0 = 0.050 → **θ = arctan(0.050) = 2.86°**

**(b)** At equilibrium, both cable segments pull upward and inward on the traffic light. By symmetry each half carries half the weight upward:
T sinθ + T sinθ = mg (net upward)
2T sinθ = 22×9.81 = 215.8 N
**T = 215.8/(2×sin2.86°) = 215.8/(2×0.04994) = 215.8/0.09988 = 2161 N ≈ 2160 N**

This is ~10× the weight of the light! The tension is large because sinθ is very small. As θ → 0 (zero sag), sin θ → 0 and T → ∞. An absolutely horizontal cable cannot support any vertical load without infinite tension — this is a fundamental constraint. Real cable bridges and power lines must sag.

---

### Problem 7

Horizontal force F = 45 N pushes block into vertical wall.

**(a)** FBD: F = 45 N horizontal (into wall), N = normal from wall (horizontal, away from wall, = 45 N opposing F), mg = 3.0×9.81 = 29.4 N downward, f_s = static friction upward (prevents sliding down).

**(b)** ΣFₓ = 0 (no horizontal acceleration into wall): N = F = **45 N**

**(c)** f_s,max = μ_s N = 0.60×45 = **27.0 N**

**(d)** ΣFᵧ = 0 (block is stationary): f_s − mg = 0 → f_s = mg = **29.4 N upward**

**(e)** But f_s,max = 27.0 N < 29.4 N = mg. The required friction exceeds the maximum available! **The block slides down.** The minimum force to prevent sliding is found from: μ_s × F_min = mg → F_min = mg/μ_s = 29.4/0.60 = **49.0 N**. The given 45 N is insufficient.

---

### Problem 8

**(a)** F = m_sat × a_sat = 200×0.50 = **100 N**

**(b)** By Newton's Third Law, the satellite exerts **100 N** on the astronaut (opposite direction).

**(c)** a_astronaut = F/m_astronaut = 100/60 = **1.67 m/s²** (opposite to satellite's direction)

**(d)** After 2.0 s from rest: satellite moves d_sat = ½(0.50)(4) = 1.0 m; astronaut moves d_ast = ½(1.67)(4) = 3.33 m in opposite direction. Total separation = 1.0+3.33 = **4.33 m**

---

### Problem 9

Total mass = 2000 kg. Total driving force = 4000 N. Total resistance = 800 N.

**(a)** a = (4000−800)/2000 = 3200/2000 = **1.60 m/s²**

**(b)** Isolate trailer (500 kg): only forces are tension T forward and friction 200 N backward.
ΣF = T − 200 = 500×1.60 → **T = 1000 N**

**(c)** By Newton's Third Law, trailer pulls on car with **1000 N backward**.

**(d)** Car (1500 kg): engine force 4000 N forward, friction 600 N backward, trailer pull 1000 N backward.
ΣF = 4000−600−1000 = 2400 N. a = 2400/1500 = **1.60 m/s²** ✓

---

### Problem 10

System: you (65 kg) + box (5.0 kg) total = 70 kg, accelerating upward at 3.0 m/s².

**(a)** Floor on feet: ΣFᵧ on whole system = N_floor − (65+5)g = (65+5)a
N_floor = 70(9.81+3.0) = 70×12.81 = **896.7 N**

**(b)** Force hands exert on box (box alone, mass 5.0 kg):
ΣFᵧ = F_hands − m_box g = m_box a
F_hands = m_box(g+a) = 5.0×12.81 = **64.1 N upward**

**(c)** By Third Law: box exerts **64.1 N downward** on your hands.

**(d)** Force of your feet on floor: by Third Law, **896.7 N downward** (the reaction to the floor's upward force on your feet).

---

### Problem 11

m = 15 kg, N = mg = 147.2 N.

**(a)** f_s,max = μ_s N = 0.45×147.2 = **66.2 N** (minimum force to start sliding)

**(b)** f_k = μ_k N = 0.30×147.2 = **44.1 N** = force needed to maintain constant velocity (equals kinetic friction exactly)

**(c)** ΣF = 100−44.1 = 55.9 N = 15a → **a = 3.73 m/s²**

**(d)** Kinetic friction (during sliding) < static friction maximum because once surfaces are sliding, fewer microscopic adhesive bonds form between the surfaces — there's less time for bonds to establish between a pair of contact asperities as they rush past each other. Static bonds have time to form and must all be broken simultaneously to start sliding.

---

### Problem 12

m = 4.0 kg, θ = 38°. N = mg cos38° = 4.0×9.81×0.788 = 30.9 N.

**(a)** mg sin38° = 4.0×9.81×0.616 = 24.2 N. f_s,max = 0.50×30.9 = 15.5 N.
24.2 N > 15.5 N → **block slides** ✓

**(b)** f_k = 0.35×30.9 = 10.8 N.
a = (mg sinθ − f_k)/m = (24.2−10.8)/4.0 = 13.4/4.0 = **3.35 m/s²** (down slope)

**(c)** With two identical blocks stacked (total mass 2m):
N' = 2mg cos38°; f_k' = μ_k×2mg cos38° = 2×(μ_k mg cosθ)
a = (2mg sinθ − 2μ_k mg cosθ)/(2m) = g(sinθ − μ_k cosθ) — **unchanged!**
Mass cancels exactly. The acceleration is the same regardless of mass (same as free fall on inclines).

**(d)** Pushing up at constant velocity (a=0): gravity component down slope + kinetic friction down slope = applied force F up slope.
F = mg sinθ + μ_k mg cosθ = mg(sinθ + μ_k cosθ) = 4.0×9.81×(0.616+0.35×0.788) = 39.24×(0.616+0.276) = 39.24×0.892 = **35.0 N**

---

### Problem 13

m₁ = 3.0 kg, m₂ = 1.5 kg, μ_s = 0.28, μ_k = 0.20.

**(a)** Driving force = m₂g = 1.5×9.81 = 14.7 N.
f_s,max = μ_s m₁g = 0.28×3.0×9.81 = 8.24 N.
14.7 > 8.24 → **system moves** ✓

**(b)** f_k = μ_k m₁g = 0.20×3.0×9.81 = 5.89 N.
Net force = m₂g − f_k = 14.7−5.89 = 8.81 N. Total mass = 4.5 kg.
**a = 8.81/4.5 = 1.96 m/s²**
T = m₂(g−a) = 1.5(9.81−1.96) = 1.5×7.85 = **11.8 N**

**(c)** If μ_k doubles to 0.40: f_k = 0.40×29.4 = 11.76 N.
a = (14.7−11.76)/4.5 = 2.94/4.5 = **0.653 m/s²**. Doubling friction more than halves acceleration — non-linear because friction enters in the numerator and doesn't affect denominator.

**(d)** At threshold (barely moves): m₂g = μ_s m₁g → m₂ = μ_s m₁ = 0.28×3.0 = **0.84 kg**

---

### Problem 14

r = 80 m, v = 60 km/h = 16.67 m/s, m = mass of car (cancels), μ_s = 0.70.

**(a)** a_c = v²/r = (16.67)²/80 = 277.9/80 = **3.47 m/s²**

**(b)** F_friction = ma_c = m×3.47 N (depends on car mass)

**(c)** f_s,max = μ_s mg = 0.70×m×9.81 = 6.867m N

**(d)** Need: ma_c ≤ μ_s mg → v²/r ≤ μ_s g → v ≤ √(μ_s gr) = √(0.70×9.81×80) = √549.4 = **23.4 m/s = 84.3 km/h**.
At 60 km/h: a_c = 3.47 m/s² < 6.87 m/s² (= μ_s g) → **safe**. Max safe speed = **84.3 km/h**.

---

### Problem 15

m₁ = 3.0 kg, m₂ = 5.0 kg.

**(a)** a = (5−3)×9.81/(3+5) = 19.62/8 = **2.45 m/s²**

**(b)** T = 2m₁m₂g/(m₁+m₂) = 2(3)(5)(9.81)/8 = 294.3/8 = **36.8 N**

**(c)** Net force on m₂ = m₂g − T = 5×9.81−36.8 = 49.05−36.8 = 12.25 N. m₂a = 5×2.45 = **12.25 N** ✓

**(d)** v² = 2aΔy = 2(2.45)(2.0) = 9.80 → **v = 3.13 m/s**

**(e)** When string breaks: m₂ is moving downward at 3.13 m/s → continues in free fall (a = −g upward, decelerates to stop, falls). m₁ is moving upward at 3.13 m/s → projectile upward, decelerates at g, reaches max height, falls.

---

### Problem 16

Two equations: T − m₁g = m₁a and m₂g − T = m₂a.

From eq 1: T = m₁(g+a) = m₁(9.81+2.0) = 11.81m₁ = 18 → **m₁ = 1.524 kg ≈ 1.52 kg**
From eq 2: T = m₂(g−a) = m₂(7.81) = 18 → **m₂ = 2.305 kg ≈ 2.31 kg**

Verify: a = (2.31−1.52)×9.81/(2.31+1.52) = 0.79×9.81/3.83 = 7.75/3.83 = 2.02 ≈ 2.0 m/s² ✓

---

### Problem 17

m₁ = 6.0 kg (on 40° incline), m₂ = 4.0 kg (hanging).

**(a)** Component of m₁'s weight along incline (downward): m₁g sin40° = 6.0×9.81×0.643 = 37.8 N (pulling system in direction: block down, mass up).
Weight of hanging mass pulling down: m₂g = 4.0×9.81 = 39.2 N (pulling: mass down, block up).
39.2 > 37.8 → **hanging mass pulls block up the incline**.

**(b)** Let a = acceleration (block up, mass down, positive direction).
Block (up slope positive): T − m₁g sin40° = m₁a → T − 37.8 = 6.0a ... (1)
Hanging mass (down positive): m₂g − T = m₂a → 39.2 − T = 4.0a ... (2)

**(c)** Add (1)+(2): 39.2−37.8 = 10.0a → 1.4 = 10a → **a = 0.14 m/s²**
T = 37.8+6.0×0.14 = 37.8+0.84 = **38.6 N**

**(d)** d = ½at² → 1.5 = ½(0.14)t² → t² = 21.43 → **t = 4.63 s**

---

### Problem 18

m_A = 2.0 kg (top), m_B = 5.0 kg (bottom), μ_s(A on B) = 0.40, μ_k(A on B) = 0.30.

**(a)** If they move together with acceleration a = F/(m_A+m_B) = F/7.0:
Force on A from B (friction) = m_A × a = 2.0×(F/7.0) = 2F/7

**(b)** Max static friction on A = μ_s m_A g = 0.40×2.0×9.81 = 7.85 N.
This limits: 2F/7 ≤ 7.85 → F ≤ **27.5 N**

**(c)** F = 30 N > 27.5 N → A slips on B.
Friction on A from B = f_k = μ_k m_A g = 0.30×2.0×9.81 = 5.89 N (forward on A)
**Block A:** ΣF = f_k = m_A a_A → a_A = 5.89/2.0 = **2.94 m/s²**
**Block B:** ΣF = F − f_k = m_B a_B → (30−5.89) = 5.0×a_B → a_B = 24.11/5.0 = **4.82 m/s²**
B accelerates faster than A → A slides backward relative to B ✓.

---

### Problem 19

m_L = 2.0 kg left incline (30°), m_R = 5.0 kg right incline (50°).

**(a)** Left block gravity along slope: 2.0×9.81×sin30° = 9.81 N (pulling left block down-left = string tension direction: right block up)
Right block gravity along slope: 5.0×9.81×sin50° = 37.6 N (pulling right block down-right)
37.6 > 9.81 → **right block slides down, left block is pulled up**.

**(b)** Let a = acceleration magnitude.
Right block (down slope = positive): m_R g sin50° − T = m_R a → 37.6−T = 5.0a ...(1)
Left block (up slope = positive): T − m_L g sin30° = m_L a → T−9.81 = 2.0a ...(2)
Add: 37.6−9.81 = 7.0a → 27.79 = 7.0a → **a = 3.97 m/s²**

**(c)** T = 9.81+2.0×3.97 = 9.81+7.94 = **17.75 N ≈ 17.8 N**

**(d)** The approach changes primarily in how N enters friction (if added), and in how the weight components align. For a flat table with hanging mass: the component along the surface is simply 0 for horizontal motion (no gravity component along motion direction), and the full weight of the hanging mass drives the system. The setup of two equations with shared acceleration and shared tension is identical in structure.

---

### Problem 20

m = 10 kg, rope at 25° above horizontal, μ_s = 0.55, g = 9.81 m/s².

**(a)** FBD: Weight mg = 98.1 N downward; Normal force N from wall horizontal (outward from wall); Tension T along rope upward and away from wall at 25° above horizontal; Friction f_s from wall (could be up or down — determine from equations).

**(b)** ΣFₓ = 0: T cos25° − N = 0 → N = T cos25°
ΣFᵧ = 0: T sin25° + f_s − mg = 0 → f_s = mg − T sin25°

**(c)** From x: N = T cos25° = 0.9063T
From y: f_s = 98.1 − T sin25° = 98.1 − 0.4226T

Need another equation: f_s ≤ μ_s N. At minimum T (just holding):
f_s = μ_s N → 98.1 − 0.4226T = 0.55×0.9063T = 0.4985T
98.1 = 0.9211T → **T = 106.5 N**
**N = 0.9063×106.5 = 96.5 N**

**(d)** **f_s = 98.1−0.4226×106.5 = 98.1−44.9 = 53.2 N** (upward, supporting the block against gravity)

**(e)** f_s,max = μ_s N = 0.55×96.5 = 53.1 N ≈ 53.2 N ✓ (at the threshold — this is the minimum T scenario)

**(f)** From the equilibrium equations without assuming slip:
From x: N = T cosθ. From y: T sinθ + μ_s T cosθ = mg (at slip threshold)
T(sinθ + μ_s cosθ) = mg → T = mg/(sinθ + μ_s cosθ)

Minimize T: dT/dθ = 0 → d/dθ[sinθ + μ_s cosθ] = 0 → cosθ − μ_s sinθ = 0 → tanθ = 1/μ_s = 1/0.55 = 1.818 → **θ_optimal = arctan(1/μ_s) = arctan(1.818) = 61.2°**

At this angle, sinθ + μ_s cosθ is maximized, so T is minimized. The minimum rope tension is T_min = mg/√(1+μ_s²) = 98.1/√(1+0.3025) = 98.1/1.141 = **86.0 N**.
