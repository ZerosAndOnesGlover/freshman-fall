# PHYS 141 · Problem Set 5 — INSTRUCTOR SOLUTIONS
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
| **A** | Momentum and Impulse | 1–6 | 30 |
| **B** | Collisions | 7–15 | 45 |
| **C** | Center of Mass | 16–20 | 25 |
| | **Total** | | **100** |

### Common errors in this problem set

**1. Claiming momentum conservation without checking external forces.** Momentum is conserved only when the net external impulse is negligible over the interval. During a collision this is usually fine; over a long fall it is not.

**2. Assuming kinetic energy is conserved in every collision.** KE is conserved only in *elastic* collisions. Perfectly inelastic collisions lose the maximum KE consistent with momentum conservation. Using KE conservation on an inelastic problem is a method error.

**3. Treating a 2D collision as scalar.** Momentum conserves independently in each component. A 2D collision needs two equations; solving one scalar equation cannot determine two unknowns.

**4. Impulse sign and direction.** J = Δp is a vector. A ball reversing direction has |Δp| = m|v₁|+m|v₂|, not the difference — this catches many students.

---

### Problem 1

Taking pitch direction as positive: v_i=+38 m/s, v_f=−45 m/s (opposite direction after being hit)

**(a)** Δp = m(v_f−v_i) = 0.14(−45−38) = 0.14(−83) = **−11.62 kg·m/s**

**(b)** F̄ = Δp/Δt = −11.62/0.0015 = **−7747 N** (magnitude 7747 N, opposing the original pitch direction)

**(c)** Weight = mg = 0.14×9.81 = 1.373 N. Ratio = 7747/1.373 = **5642×** the ball's weight.

---

### Problem 2

**(a)** Δp = m(v_f−v_i) = 1000(0−18) = **−18,000 kg·m/s**. J = Δp = **−18,000 N·s**

**(b)** F̄ = Δp/Δt = −18000/4.0 = **−4500 N**

**(c)** F̄' = −18000/1.0 = **−18,000 N** — four times larger force for a stop time 4× shorter, confirming F̄ ∝ 1/Δt.

---

### Problem 3

**(a)** v = √(2gh) = √(2×9.81×1.2) = √23.544 = **4.85 m/s** (downward)

**(b)** Taking up as positive: v_i=−4.85 m/s, v_f=0 (stops).
Δp = m(0−(−4.85)) = 60×4.85 = **291 kg·m/s** (upward)

**(c)** F̄_net = Δp/Δt = 291/0.05 = 5820 N. This is the NET impulse (ground force − gravity). Since gravity's contribution over such a short time is small but let's be precise: actually the problem intends the ground's average force minus weight gives net upward force producing the deceleration. For a quick estimate treating gravity as negligible over 0.05s: **F_ground ≈ 5820 N** (plus weight ≈588 N if included exactly, but standard treatment uses net impulse ≈ ground force for short collision times). Accept **F_ground ≈ 5820 N** as primary answer.

**(d)** F̄' = 291/0.4 = **728 N**. Ratio = 5820/728 = **8.0×** — bending knees reduces the force by a factor of 8, dramatically reducing injury risk.

---

### Problem 4

**(a)** $$J = \int_0^6 (30-5t)\,dt = [30t-2.5t^2]_0^6 = 180-90 = \mathbf{90 \text{ N·s}}$$

**(b)** Δp = J → mv_f = 90 → v_f = 90/5.0 = **18 m/s**

**(c)** F=0: 30−5t=0 → t=6 s. This is the SAME as the endpoint of the interval (t=6s), so the velocity at that time is the same as computed in (b): **18 m/s**. Since F(t) > 0 throughout [0,6) and reaches exactly zero at t=6, the object's speed increases monotonically over the entire interval, reaching its maximum (within this domain) exactly at t=6 s.

---

### Problem 5

Mass flow rate dm/dt = 3.0 kg/s. Each kg arrives at 8.0 m/s and loses all horizontal velocity (Δv = 8.0 m/s per kg, in magnitude).

$$\bar{F} = \frac{\Delta p}{\Delta t} = \frac{dm}{dt}\times \Delta v = 3.0 \times 8.0 = \mathbf{24 \text{ N}}$$

(This treats the water stream as continuously delivering momentum change to the wall — force = mass flow rate × velocity change.)

---

### Problem 6

**(a)** Before impact: v = √(2gh₁) = √(2×9.81×2.0) = √39.24 = 6.26 m/s, **downward, so v_i = −6.26 m/s**
After bounce (rises to 1.4 m): v = √(2gh₂) = √(2×9.81×1.4) = √27.47 = 5.24 m/s, **upward, so v_f = +5.24 m/s**

**(b)** Δp = m(v_f−v_i) = 0.50(5.24−(−6.26)) = 0.50(11.5) = **5.75 kg·m/s** (upward)

**(c)** F̄ = Δp/Δt = 5.75/0.008 = 718.75 N. Weight = 0.50×9.81 = 4.905 N. Ratio = 718.75/4.905 = **146.6×** the ball's weight.

---

### Problem 7

**(a)** v_f = [1500(12)+1000(0)]/(1500+1000) = 18000/2500 = **7.2 m/s**

**(b)** KE_i = ½(1500)(144) = 108,000 J. KE_f = ½(2500)(51.84) = 64,800 J.

**(c)** Fraction lost = (108000−64800)/108000 = 43200/108000 = **40.0%**

---

### Problem 8

**(a)** Taking A's direction as positive: v_A=+6.0, v_B=−2.0
v_f = [2.0(6.0)+3.0(−2.0)]/(2.0+3.0) = (12.0−6.0)/5.0 = 6.0/5.0 = **1.2 m/s** (in A's original direction)

**(b)** KE_i = ½(2.0)(36)+½(3.0)(4.0) = 36+6=42 J. KE_f = ½(5.0)(1.44) = 3.6 J.
KE lost = 42−3.6 = **38.4 J**

---

### Problem 9

**(a)** Momentum conservation (perfectly inelastic): m_bullet·v_bullet = (m_bullet+m_block)·v_f
0.020·v_bullet = (0.020+2.0)(4.0) = 2.02×4.0 = 8.08
v_bullet = 8.08/0.020 = **404 m/s**

**(b)** KE_i = ½(0.020)(404)² = ½(0.020)(163216) = 1632.16 J
KE_f = ½(2.02)(4.0)² = ½(2.02)(16) = 16.16 J
KE lost = 1632.16−16.16 = **1616 J** — converted to heat, sound, and deformation of the wood/bullet during embedding.

---

### Problem 10

v_f (from Problem 9) = 4.0 m/s, m_total = 2.02 kg, μ_k=0.30

Work-energy theorem: −f_k·d = 0 − ½m_total v_f²
f_k = μ_k·m_total·g = 0.30×2.02×9.81 = 5.946 N
d = ½(2.02)(16)/5.946 = 16.16/5.946 = **2.72 m**

---

### Problem 11

m_A=3.0 kg, v_Ai=8.0 m/s, m_B=5.0 kg, v_Bi=0

**(a)** 
$$v_{Af} = \frac{3.0-5.0}{8.0}(8.0)+\frac{2(5.0)}{8.0}(0) = \frac{-2.0}{8.0}(8.0) = -2.0 \text{ m/s}$$
$$v_{Bf} = \frac{2(3.0)}{8.0}(8.0)+\frac{5.0-3.0}{8.0}(0) = \frac{6.0}{8.0}(8.0) = 6.0 \text{ m/s}$$
**v_Af = −2.0 m/s, v_Bf = 6.0 m/s**

**(b)** p_i = 3.0(8.0) = 24.0. p_f = 3.0(−2.0)+5.0(6.0) = −6.0+30.0 = 24.0 ✓

**(c)** KE_i = ½(3.0)(64) = 96.0 J. KE_f = ½(3.0)(4.0)+½(5.0)(36) = 6.0+90.0 = 96.0 J ✓

---

### Problem 12

m_A=1.0 kg, v_Ai=6.0 m/s, v_Af=−2.0 m/s (bounces back)

**(a)** Momentum: 1.0(6.0) = 1.0(−2.0)+m(v_Bf) → 6.0+2.0 = m·v_Bf → v_Bf = 8.0/m

**(b)** Energy: ½(1.0)(36) = ½(1.0)(4.0)+½(m)(v_Bf²)
18 = 2.0 + ½m(8.0/m)²= 2.0+32/m
16 = 32/m → **m = 2.0 kg**

Then v_Bf = 8.0/2.0 = **4.0 m/s**

**(c)** Using general formula: v_Af = [(1.0−m)/(1.0+m)](6.0). With m=2.0: v_Af = [(1.0−2.0)/(3.0)](6.0) = (−1/3)(6.0) = **−2.0 m/s** ✓ matches given value, confirming m=2.0 kg is correct.

---

### Problem 13

m_A=2.0 kg, v_Ai=5.0 m/s (+x), m_B=4.0 kg (stationary). After: v_Af=2.0 m/s at 60° above +x.

**x-momentum:** 2.0(5.0) = 2.0(2.0cos60°)+4.0(v_Bx)
10.0 = 2.0(1.0)+4.0v_Bx = 2.0+4.0v_Bx
v_Bx = 8.0/4.0 = 2.0 m/s

**y-momentum:** 0 = 2.0(2.0sin60°)+4.0(v_By)
0 = 2.0(1.732)+4.0v_By = 3.464+4.0v_By
v_By = −0.866 m/s

**(a)** |v_B| = √(4.0+0.75) = √4.75 = **2.18 m/s**. Direction = arctan(−0.866/2.0) = **−23.4°** (below +x axis)

**(b)** KE_i = ½(2.0)(25) = 25.0 J
KE_f = ½(2.0)(4.0)+½(4.0)(4.75) = 4.0+9.5 = 13.5 J
KE_f < KE_i → **inelastic** (but not perfectly inelastic, since the objects have different final velocities, not a common one)

---

### Problem 14

m_bullet=0.010 kg, m_block=2.0 kg, h=0.12 m

**(a)** Energy conservation (post-collision): ½(m_total)v_f² = m_total·g·h
v_f = √(2gh) = √(2×9.81×0.12) = √2.354 = **1.534 m/s**

**(b)** Momentum conservation: m_bullet·v_bullet = m_total·v_f
0.010·v_bullet = 2.01×1.534 = 3.084
v_bullet = 3.084/0.010 = **308.4 m/s**

**(c)** KE_i = ½(0.010)(308.4)² = ½(0.010)(95130.6) = 475.65 J
KE_f (post-collision, pre-swing) = ½(2.01)(1.534)² = ½(2.01)(2.353) = 2.365 J
KE lost = 475.65−2.365 = **473.3 J**

---

### Problem 15

m_total=2.0 kg, at peak v=0 before explosion. m1=0.8 kg at 15 m/s horizontal, m2=1.2 kg unknown.

Momentum conservation (was zero before explosion, in both x and y):
**x:** 0 = 0.8(15)+1.2(v2x) → v2x = −12/1.2 = −10 m/s
**y:** 0 = 0+1.2(v2y) [fragment 1 purely horizontal, no y-component] → v2y = 0

**Fragment 2: v2 = 10 m/s in the direction opposite to fragment 1 (horizontal, −x direction if fragment 1 was +x).**

---

### Problem 16

x_cm = [2.0(1.0)+3.0(4.0)+5.0(8.0)]/(2.0+3.0+5.0) = (2.0+12.0+40.0)/10.0 = 54.0/10.0 = **5.4 m**

---

### Problem 17

**(a)** x_cm = [4.0(2.0)+6.0(8.0)]/(4.0+6.0) = (8.0+48.0)/10.0 = 56.0/10.0 = 5.6 m
y_cm = [4.0(3.0)+6.0(−1.0)]/10.0 = (12.0−6.0)/10.0 = 6.0/10.0 = 0.6 m
**CM at (5.6, 0.6) m**

**(b)** v_cm,x = [4.0(3.0)+6.0(−1.0)]/10.0 = (12.0−6.0)/10.0 = 0.6 m/s
v_cm,y = [4.0(0)+6.0(2.0)]/10.0 = 12.0/10.0 = 1.2 m/s
**v_cm = (0.6, 1.2) m/s**

**(c)** p_total = M·v_cm = 10.0×(0.6,1.2) = (6.0, 12.0) kg·m/s
Direct sum: p1=(4.0×3.0, 4.0×0)=(12.0,0); p2=(6.0×(−1.0),6.0×2.0)=(−6.0,12.0)
Sum = (12.0−6.0, 0+12.0) = (6.0, 12.0) ✓ matches

---

### Problem 18

**(a)** By symmetry, rod's CM is at its midpoint: **x_cm,rod = 1.5 m**

**(b)** Combined CM: x_cm = [6.0(1.5)+4.0(3.0)]/(6.0+4.0) = (9.0+12.0)/10.0 = 21.0/10.0 = **2.1 m**

---

### Problem 19

m_cannon=1200 kg, m_ball=8.0 kg, v_ball=120 m/s

**(a)** Momentum conservation (starts at rest, total = 0):
0 = 1200(v_cannon)+8.0(120) → v_cannon = −960/1200 = **−0.80 m/s** (recoils backward)

**(b)** Before firing: v_cm=0 (system at rest). After firing: v_cm = [1200(−0.80)+8.0(120)]/1208 = (−960+960)/1208 = **0 m/s**. Unchanged — makes sense because the firing is entirely an internal force (gunpowder explosion within the system); no external horizontal force acts, so v_cm must remain constant (zero).

**(c)** KE_cannon = ½(1200)(0.80)² = ½(1200)(0.64) = 384 J
KE_ball = ½(8.0)(120)² = ½(8.0)(14400) = 57,600 J
Total KE = 384+57600 = 57,984 J. This energy comes from the **chemical potential energy of the gunpowder**, converted to kinetic energy during the explosion — analogous to the reverse of a perfectly inelastic collision (energy is added to the system rather than removed).

---

### Problem 20

m_person=70 kg, m_boat=120 kg, L=4.0 m

**(a)** CM cannot move (isolated system, starts at rest). Let boat displacement = d_boat (opposite direction to person's walk), person's displacement relative to water = d_person.
CM condition: m_person·d_person + m_boat·d_boat = 0 (net displacement of CM = 0)

Also, relative to the boat, the person moves 4.0 m (the length of the boat): d_person − d_boat = 4.0 m (taking person's walking direction as positive; boat moves in the opposite direction, so d_boat is negative if we define d_person as positive)

Let's define: person moves +d_p relative to water; boat moves +d_b relative to water (d_b will come out negative, i.e., boat moves backward).
Relative displacement: d_p − d_b = 4.0 (person moves 4.0 m relative to boat)

CM: 70·d_p + 120·d_b = 0 → d_p = −(120/70)d_b = −(12/7)d_b

Substitute: −(12/7)d_b − d_b = 4.0 → −d_b(12/7+1) = 4.0 → −d_b(19/7) = 4.0 → d_b = −4.0×7/19 = −1.474 m

**Boat moves 1.474 m in the direction opposite to the person's walk** (i.e., "backward" relative to water).

**(b)** d_p = −(12/7)(−1.474) = 2.526 m
**Person moves 2.526 m (in their walking direction) relative to the water.**

**(c)** Check: d_p − d_b = 2.526−(−1.474) = 4.0 m ✓ matches the boat length.

**(d)** If the person walks back to the original end: by symmetry, all displacements reverse exactly, and the boat returns to its **original position relative to the water** (net zero displacement for both boat and person after the round trip, since the CM must return to where it started along the direction of net momentum, which was zero throughout — the boat's position tracks the reverse of the outward trip exactly).
