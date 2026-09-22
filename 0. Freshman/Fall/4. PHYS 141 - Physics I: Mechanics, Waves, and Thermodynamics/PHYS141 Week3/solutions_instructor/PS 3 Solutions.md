# PHYS 141 · Problem Set 3 — INSTRUCTOR SOLUTIONS
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
| **A** | Newton's First and Second Laws | 1–3 | 30 |
| **B** | Newton's Third Law | 4–5 | 20 |
| **C** | Friction | 6–7 | 20 |
| **D** | Connected Systems and Inclines | 8–10 | 30 |
| | **Total** | | **100** |

### Common errors in this problem set

**1. Assuming N = mg always.** The normal force equals mg only for a horizontal surface with no vertical acceleration and no other vertical forces. On an incline, in a lift, or with an applied vertical component it does not. This is the highest-frequency error in the set.

**2. Putting an action–reaction pair on the same free body diagram.** Third-law pairs act on *different* bodies and can never both appear in one FBD. If both are drawn, the diagram is wrong regardless of the final number.

**3. Using f = μN for static friction.** Static friction is f ≤ μ_s N — it takes whatever value is needed up to the maximum. Only kinetic friction is f = μ_k N. Using the equality for a static problem is a method error.

**4. Losing the massless-string idealisation.** Tension is uniform throughout a massless string over a frictionless pulley. Introducing different tensions on the two sides without justification is wrong; so is ignoring a *stated* pulley mass.

---

### Problem 1

**(a)** a = Δv/t = 25/8.0 = **3.125 m/s²**

**(b)** F_net = ma = 1200×3.125 = **3750 N**

**(c)** F_engine − F_friction = F_net → F_friction = 5500−3750 = **1750 N**

**(d)** a = (0−25)/5.0 = −5.0 m/s². F_brake = ma = 1200×5.0 = **6000 N** (opposing motion)

---

### Problem 2

N is what the scale reads. ΣFᵧ = N − mg = ma.

**(a)** a=0: N = mg = 70×9.81 = **686 N**

**(b)** a = +2.5 m/s² (up): N = m(g+a) = 70×12.31 = **862 N**

**(c)** Constant velocity: a=0. N = **686 N** (same as rest)

**(d)** Decelerating while moving up: a = −1.8 m/s². N = m(g−1.8) = 70×7.01 = **491 N**

**(e)** Free fall: a = −g. N = m(g−g) = **0 N**. The person is weightless — no contact force from scale. They feel as if floating. This is identical to orbital weightlessness.

---

### Problem 3

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

### Problem 4

**(a)** F = m_sat × a_sat = 200×0.50 = **100 N**

**(b)** By Newton's Third Law, the satellite exerts **100 N** on the astronaut (opposite direction).

**(c)** a_astronaut = F/m_astronaut = 100/60 = **1.67 m/s²** (opposite to satellite's direction)

**(d)** After 2.0 s from rest: satellite moves d_sat = ½(0.50)(4) = 1.0 m; astronaut moves d_ast = ½(1.67)(4) = 3.33 m in opposite direction. Total separation = 1.0+3.33 = **4.33 m**

---

### Problem 5

Total mass = 2000 kg. Total driving force = 4000 N. Total resistance = 800 N.

**(a)** a = (4000−800)/2000 = 3200/2000 = **1.60 m/s²**

**(b)** Isolate trailer (500 kg): only forces are tension T forward and friction 200 N backward.
ΣF = T − 200 = 500×1.60 → **T = 1000 N**

**(c)** By Newton's Third Law, trailer pulls on car with **1000 N backward**.

**(d)** Car (1500 kg): engine force 4000 N forward, friction 600 N backward, trailer pull 1000 N backward.
ΣF = 4000−600−1000 = 2400 N. a = 2400/1500 = **1.60 m/s²** ✓

---

### Problem 6

m = 15 kg, N = mg = 147.2 N.

**(a)** f_s,max = μ_s N = 0.45×147.2 = **66.2 N** (minimum force to start sliding)

**(b)** f_k = μ_k N = 0.30×147.2 = **44.1 N** = force needed to maintain constant velocity (equals kinetic friction exactly)

**(c)** ΣF = 100−44.1 = 55.9 N = 15a → **a = 3.73 m/s²**

**(d)** Kinetic friction (during sliding) < static friction maximum because once surfaces are sliding, fewer microscopic adhesive bonds form between the surfaces — there's less time for bonds to establish between a pair of contact asperities as they rush past each other. Static bonds have time to form and must all be broken simultaneously to start sliding.

---

### Problem 7

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

### Problem 8

m₁ = 3.0 kg, m₂ = 5.0 kg.

**(a)** a = (5−3)×9.81/(3+5) = 19.62/8 = **2.45 m/s²**

**(b)** T = 2m₁m₂g/(m₁+m₂) = 2(3)(5)(9.81)/8 = 294.3/8 = **36.8 N**

**(c)** Net force on m₂ = m₂g − T = 5×9.81−36.8 = 49.05−36.8 = 12.25 N. m₂a = 5×2.45 = **12.25 N** ✓

**(d)** v² = 2aΔy = 2(2.45)(2.0) = 9.80 → **v = 3.13 m/s**

**(e)** When string breaks: m₂ is moving downward at 3.13 m/s → continues in free fall (a = −g upward, decelerates to stop, falls). m₁ is moving upward at 3.13 m/s → projectile upward, decelerates at g, reaches max height, falls.

---

### Problem 9

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

### Problem 10

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
