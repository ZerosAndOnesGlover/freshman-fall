# PHYS 141 · Problem Set 4 — INSTRUCTOR SOLUTIONS
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
| **A** | Work | 1–5 | 25 |
| **B** | Work-Energy Theorem | 6–10 | 25 |
| **C** | Potential Energy & Conservative Forces | 11–14 | 20 |
| **D** | Conservation of Energy | 15–20 | 30 |
| | **Total** | | **100** |

### Common errors in this problem set

**1. Omitting non-conservative work.** Mechanical energy is conserved only when no friction or drag acts. With friction present the correct statement is ΔKE + ΔPE = W_nc, and W_nc is negative for friction.

**2. Sign of work.** W = F·d·cosθ. Force opposing motion gives negative work. A student reporting friction as doing positive work has a sign error worth the answer marks, not the method marks.

**3. Fixing the gravitational PE reference inconsistently.** U = mgh requires one chosen h = 0 datum used throughout. Any datum is legal; changing it mid-problem is not.

**4. Conflating the work–energy theorem with conservation of energy.** W_net = ΔKE is always true. ΔKE + ΔPE = 0 requires conservative forces only. Students who quote the second when the first applies typically drop the friction term.

---

### Problem 1

**(a)** W_applied = 85×12 = **1020 J**

**(b)** W_friction = −30×12 = **−360 J**

**(c)** Both gravity and normal force are perpendicular to horizontal motion: **W_gravity = 0 J, W_N = 0 J**

**(d)** W_net = 1020−360+0+0 = **660 J**

---

### Problem 2

**(a)** W = F⃗·d⃗ = (6)(4)+(−3)(5) = 24−15 = **9 J**

**(b)** |F| = √(36+9) = √45 = 6.708 N. |d| = √(16+25) = √41 = 6.403 m.
cosθ = (F⃗·d⃗)/(|F||d|) = 9/(6.708×6.403) = 9/42.95 = 0.2095 → θ=77.9°
W = 6.708×6.403×0.2095 = **9.0 J** ✓ matches part (a)

---

### Problem 3

$$W = \int_1^4 5x^2\,dx = 5\left[\frac{x^3}{3}\right]_1^4 = \frac{5}{3}(64-1) = \frac{5}{3}(63) = \mathbf{105 \text{ J}}$$

---

### Problem 4

Constant velocity → a=0.

**(a)** W_tension = T×d. Since a=0: T=mg=1200×9.81=11772 N. W_T = 11772×15 = **176,580 J**

**(b)** W_gravity = −mg×d = −11772×15 = **−176,580 J**

**(c)** W_net = 176580−176580 = **0 J**. This must be zero because ΔKE=0 (constant velocity means no change in speed), and W_net = ΔKE by the work-energy theorem.

---

### Problem 5

At every point along the pendulum's arc, the velocity is tangent to the circular path (perpendicular to the radius). The string tension always points along the radius (toward the pivot). Since tension is always perpendicular to velocity (hence to the instantaneous displacement direction) at every single point of the motion — not just the bottom — the differential work dW = T⃗·dr⃗ = 0 at every instant. Integrating zero over the whole path still gives zero. This is a general property of any force that remains perpendicular to velocity throughout circular/curved motion (identical to the centripetal force argument from Lecture 13).

---

### Problem 6

m=1500 kg, v₀=25 m/s, v=0, d=60 m

**(a)** W_net = ΔKE = 0 − ½(1500)(625) = −468750 J
W_net = F_brake × d (F_brake negative, opposing motion): −468750 = F_brake × 60 → F_brake = **−7812.5 N** (magnitude 7812.5 N, opposing motion)

**(b)** f_k = μ_k mg → 7812.5 = μ_k(1500)(9.81) → μ_k = 7812.5/14715 = **0.531**

---

### Problem 7

m=0.15 kg, v₀=40 m/s, v=0, d=0.12 m

**(a)** W = ΔKE = 0 − ½(0.15)(1600) = −120 J
F×d = W (F opposing motion) → F = −120/0.12 = **−1000 N** (magnitude 1000 N)

**(b)** Weight = mg = 0.15×9.81 = 1.47 N. Ratio = 1000/1.47 = **680×** the ball's weight! This enormous force (over half a ton of force momentarily) is why catching a fast ball stings — the short stopping distance requires a very large force to remove the kinetic energy.

---

### Problem 8

**(a)** $$W = \int_0^6 (12-2x)\,dx = [12x - x^2]_0^6 = 72 - 36 = \mathbf{36 \text{ J}}$$

**(b)** W = ΔKE = ½(3.0)v_f² − 0 → 36 = 1.5v_f² → v_f² = 24 → **v_f = 4.90 m/s**

**(c)** Speed is maximum where KE is maximum, i.e. where the cumulative work — the area under F(x)
from 0 to x — stops increasing. That happens where F(x) = 0: 12 − 2x = 0 → **x = 6 m**.

Check the sign of F across the domain before concluding: F(0) = 12 N, F(3) = 6 N, F(6) = 0. So
**F ≥ 0 throughout 0 ≤ x ≤ 6**, the kinetic energy increases monotonically over the whole interval,
and the maximum speed occurs at the **right endpoint x = 6 m**, where F just reaches zero.

> **Marking note.** This is an endpoint maximum, not an interior critical point. A student who
> solves F(x) = 0 and reports x = 6 has the right answer; a student who *also* checks that F does
> not change sign inside the interval has given the complete argument. Had the domain extended past
> x = 6, F would turn negative, KE would begin falling, and x = 6 would be a genuine interior
> maximum — so the reasoning, not just the equation, is what makes the answer right.

---

### Problem 9

m=5.0 kg, v₀=8.0 m/s, v=0, d=10 m

**(a)** W_friction = ΔKE = 0−½(5.0)(64) = −160 J. f_k = 160/10 = **16 N**

**(b)** μ_k = f_k/(mg) = 16/(5.0×9.81) = 16/49.05 = **0.326**

**(c)** With v₀'=16 m/s: W_friction = −f_k×d' = ΔKE = 0−½(5.0)(256) = −640 J
d' = 640/16 = **40 m**. Note: 640/160 = 4 = (16/8)² — stopping distance scales with v₀² (quadrupling speed factor of 2 → quadruples distance), consistent with KE ∝ v².

---

### Problem 10

m=500 kg, F(x)=8000−400x, 0≤x≤20

**(a)** F=0: 8000−400x=0 → **x=20 m**

**(b)** $$W = \int_0^{20}(8000-400x)dx = [8000x-200x^2]_0^{20} = 160000 - 80000 = \mathbf{80,000 \text{ J}}$$

**(c)** W=ΔKE → 80000 = ½(500)v² → v² = 320 → **v = 17.9 m/s**

**(d)** At x=20 m, F=0 — this IS the endpoint of the given interval, so the speed calculated in (c) (at x=20) is also the speed where F=0. Since F(x) > 0 for all x < 20 in this domain (check: F(10)=8000−4000=4000>0), the net force does positive work throughout 0 to 20, so KE increases monotonically over the whole interval — the maximum speed within the domain occurs at x=20 m, which is **the same point as (c): v=17.9 m/s.** (If the force continued past x=20 with the same formula, it would become negative and decelerate the object — but that's outside the given domain.)

---

### Problem 11

U(x) = 4x³−18x²+6

**(a)** F(x) = −dU/dx = **−(12x²−36x) = −12x²+36x**

**(b)** F=0: −12x²+36x=0 → 12x(3−x)=0 → **x=0 or x=3**

**(c)** d²U/dx² = 24x−36
At x=0: d²U/dx² = −36 < 0 → **unstable** (U maximum)
At x=3: d²U/dx² = 72−36=36 > 0 → **stable** (U minimum)

---

### Problem 12

k=250 N/m, x=0.20 m, m=0.40 kg

**(a)** U = ½(250)(0.04) = **5.0 J**

**(b)** ½mv² = 5.0 → v² = 25 → **v = 5.0 m/s**

**(c)** All spring PE converts to gravitational PE at the stopping point (frictionless):
5.0 = mgh = mg(d sin20°) → 5.0 = 0.40×9.81×d×0.342
5.0 = 1.342d → **d = 3.73 m** (distance along incline)

---

### Problem 13

F⃗ = (3y, 2x). Path A: straight line (0,0)→(2,2), parameterize x=t, y=t, t:0→2.
$$W_A = \int_0^2 [3t\,dx + 2t\,dy] = \int_0^2 [3t(1) + 2t(1)]dt = \int_0^2 5t\,dt = \frac{5}{2}(4) = 10\text{ J}$$

Path B: (0,0)→(2,0)→(2,2).
Segment 1: y=0 throughout, dy=0, x:0→2. W = ∫F_x dx = ∫3(0)dx = 0 (since y=0 along this segment)
Segment 2: x=2 throughout, dx=0, y:0→2. W = ∫F_y dy = ∫2(2)dy = ∫4dy = 4(2) = 8 J
$$W_B = 0 + 8 = 8\text{ J}$$

**W_A = 10 J ≠ W_B = 8 J.** Since the work differs between two paths connecting the same endpoints, **this force is NOT conservative.**

---

### Problem 14

m=1.5 kg, h=3.0 m

**(a)** mgh = ½mv² → v=√(2gh) = √(2×9.81×3.0) = √58.86 = **7.67 m/s**

**(b)** No — gravity is conservative, so work (and hence the resulting speed via energy conservation) depends only on the height dropped, not the path shape.

**(c)** No — with friction present, the work done by friction depends on the total path length traveled, which DOES depend on the ramp's shape (a longer, more winding path accumulates more friction work even for the same height drop). So the final speed would differ between differently-shaped ramps if friction is present.

---

### Problem 15

m=4.0 kg, θ=30°, h=5.0 m

**(a)** v=√(2gh)=√(2×9.81×5.0)=√98.1=**9.90 m/s**

**(b)** Length of incline L = h/sinθ = 5.0/0.5 = 10 m. a=g sin30°=4.905 m/s².
v²=2aL=2(4.905)(10)=98.1 → v=**9.90 m/s** ✓ matches (a)

**(c)** No — the length doesn't matter for final speed (in the frictionless case) because gravity is conservative and only ΔU (dependent on height) determines the KE gained. The kinematic calculation confirms this: even though a and L both depend on θ, they combine (via 2aL = 2g sinθ × h/sinθ = 2gh) to eliminate the θ-dependence entirely.

---

### Problem 16

m=800 kg, h₁=45 m

**Bottom of first hill:** v₁=√(2gh₁)=√(2×9.81×45)=√882.9=**29.7 m/s**

**Top of second hill (height 20 m):** Energy conservation from start: mgh₁ = mg(20) + ½mv₂²
v₂² = 2g(45−20) = 2(9.81)(25) = 490.5 → **v₂ = 22.1 m/s**

---

### Problem 17

m=0.20 kg, v₀=15 m/s, θ=50°

**(a)** At max height, v_y=0 but v_x=v₀cos50° remains.
Energy conservation: ½mv₀² = ½mv_x² + mgH
H = (v₀²−v_x²)/(2g) = (v₀²−v₀²cos²50°)/(2g) = v₀²(1−cos²50°)/(2g) = v₀²sin²50°/(2g)
H = (225)(0.5868)/(19.62) = 132.03/19.62 = **6.73 m**

**(b)** H=(v₀sinθ)²/(2g) = (15×0.766)²/19.62 = (11.49)²/19.62 = 132.0/19.62 = **6.73 m** ✓ matches

---

### Problem 18

m=0.50 kg, r=0.80 m

**(a)** h_min = (5/2)r = 2.5×0.80 = **2.0 m**

**(b)** h=3.0 m. Energy conservation from start to top of loop (height 2r=1.60 m):
mgh = ½mv_top² + mg(2r)
v_top² = 2g(h−2r) = 2(9.81)(3.0−1.60) = 2(9.81)(1.40) = 27.47
**v_top = 5.24 m/s**

**(c)** At top: N+mg = mv_top²/r (both N and gravity point toward center, downward)
N = mv_top²/r − mg = 0.50×27.47/0.80 − 0.50×9.81 = 17.17 − 4.905 = **12.27 N**

---

### Problem 19

m=6.0 kg, incline L=4.0 m, θ=35°, μ_k=0.15, k=500 N/m

**(a)** h = Lsin35° = 4.0×0.574 = 2.296 m
N = mgcos35° = 6.0×9.81×0.819 = 48.20 N
f_k = μ_k N = 0.15×48.20 = 7.23 N
W_friction = −f_k×L = −7.23×4.0 = −28.92 J

Energy: mgh + W_friction = ½mv²
6.0×9.81×2.296 − 28.92 = ½(6.0)v²
135.13 − 28.92 = 3.0v²
106.21 = 3.0v² → v² = 35.4 → **v = 5.95 m/s**

**(b)** Frictionless horizontal surface: no energy loss → **v = 5.95 m/s** (unchanged)

**(c)** All KE converts to spring PE: ½mv² = ½kx²
½(6.0)(35.4) = ½(500)x²
106.2 = 250x² → x² = 0.4248 → **x = 0.652 m**

**(d)** With friction on horizontal surface (μ_k=0.10, distance 2.0 m):
Additional friction work: W_friction2 = −μ_k×mg×2.0 = −0.10×6.0×9.81×2.0 = −11.77 J

Modified energy equation:
mgh + W_friction(incline) + W_friction(horizontal) = ½mv'² (before spring)
135.13 − 28.92 − 11.77 = 3.0v'²
94.44 = 3.0v'² → v'² = 31.48

Then: ½mv'² = ½kx'² → 3.0(31.48) = 250x'² → 94.44 = 250x'² → x'² = 0.3778 → **x' ≈ 0.615 m** (slightly less compression than part (c), as expected due to additional energy loss)

---

### Problem 20

m=70 kg, θ=6°, v=8.0 m/s, f_roll=15 N

**(a)** Constant speed → net force = 0 along incline.
F_cyclist = mg sinθ + f_roll = 70×9.81×sin6° + 15 = 70×9.81×0.1045 + 15 = 71.75+15 = **86.75 N**

**(b)** P = Fv = 86.75×8.0 = **694.0 W**

**(c)** P(hp) = 694.0/746 = **0.930 hp**

**(d)** Ignoring rolling friction: F = mg sinθ. P = Fv = mg sinθ × v = 300 W
sinθ = 300/(mgv) = 300/(70×9.81×8.0) = 300/5493.6 = 0.05461
**θ = arcsin(0.05461) = 3.13°**
