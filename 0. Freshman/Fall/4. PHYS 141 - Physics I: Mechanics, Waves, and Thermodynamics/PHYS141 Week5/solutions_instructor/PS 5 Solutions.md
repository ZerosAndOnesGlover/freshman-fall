# PHYS 141 · Problem Set 5 — INSTRUCTOR SOLUTIONS
**Do not distribute before the due date.**

---

> *Revised 2026-09-28: sub-parts cut from 28 to 18; the ten problems and their points are unchanged. The answers below keep the old letters. New → old: 1 (a, b) = (a, b) · 2 (a, b) = (c, d) · 3 (a, b) = (b, c) · 4 (a, b) = (a, c) · 5 unchanged · 6 (a, b) = (a, c) · 7 (a, b) = (b, c) · 8 unchanged · 9 (a, b) = (a, b) · 10 (a, b) = (a, b). Problem 2's answers now include the weight; see the note there.*


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
| **A** | Momentum and Impulse | 1–3 | 30 |
| **B** | Collisions | 4–7 | 40 |
| **C** | Center of Mass | 8–10 | 30 |
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

**(a)** v = √(2gh) = √(2×9.81×1.2) = √23.544 = **4.85 m/s** (downward)

**(b)** Taking up as positive: v_i=−4.85 m/s, v_f=0 (stops).
Δp = m(0−(−4.85)) = 60×4.85 = **291 kg·m/s** (upward)

**(c)** The impulse above is the **net** impulse. Two forces act during landing: the ground pushes up with $\bar F$ and gravity pulls down with $mg = 60 \times 9.81 = 589$ N. So

$$\bar F - mg = \frac{\Delta p}{\Delta t} = \frac{291}{0.05} = 5820\ \text{N} \quad\Rightarrow\quad \bar F = 5820 + 589 = \mathbf{6.41\ kN}$$

**(d)** $\bar F' = 291/0.4 + 589 = 728 + 589 = \mathbf{1.32\ kN}$. Ratio = 6410/1317 = **4.9** — bending the knees cuts the ground force roughly five-fold.

*Marking: accept 5.82 kN, 728 N and a ratio of 8.0 only when the student says that gravity is neglected. That is a fair approximation for the 0.05 s stop (10% error) but not for the 0.4 s one, where the weight is almost half the force.*

*(Before 2026-09-28 this answer neglected gravity without saying so, and gave 5.82 kN, 728 N and 8.0.)*

---

### Problem 3

**(a)** $$J = \int_0^6 (30-5t)\,dt = [30t-2.5t^2]_0^6 = 180-90 = \mathbf{90 \text{ N·s}}$$

**(b)** Δp = J → mv_f = 90 → v_f = 90/5.0 = **18 m/s**

**(c)** F=0: 30−5t=0 → t=6 s. This is the SAME as the endpoint of the interval (t=6s), so the velocity at that time is the same as computed in (b): **18 m/s**. Since F(t) > 0 throughout [0,6) and reaches exactly zero at t=6, the object's speed increases monotonically over the entire interval, reaching its maximum (within this domain) exactly at t=6 s.

---

### Problem 4

**(a)** v_f = [1500(12)+1000(0)]/(1500+1000) = 18000/2500 = **7.2 m/s**

**(b)** KE_i = ½(1500)(144) = 108,000 J. KE_f = ½(2500)(51.84) = 64,800 J.

**(c)** Fraction lost = (108000−64800)/108000 = 43200/108000 = **40.0%**

---

### Problem 5

**(a)** Momentum conservation (perfectly inelastic): m_bullet·v_bullet = (m_bullet+m_block)·v_f
0.020·v_bullet = (0.020+2.0)(4.0) = 2.02×4.0 = 8.08
v_bullet = 8.08/0.020 = **404 m/s**

**(b)** KE_i = ½(0.020)(404)² = ½(0.020)(163216) = 1632.16 J
KE_f = ½(2.02)(4.0)² = ½(2.02)(16) = 16.16 J
KE lost = 1632.16−16.16 = **1616 J** — converted to heat, sound, and deformation of the wood/bullet during embedding.

---

### Problem 6

m_A=3.0 kg, v_Ai=8.0 m/s, m_B=5.0 kg, v_Bi=0

**(a)** 
$$v_{Af} = \frac{3.0-5.0}{8.0}(8.0)+\frac{2(5.0)}{8.0}(0) = \frac{-2.0}{8.0}(8.0) = -2.0 \text{ m/s}$$
$$v_{Bf} = \frac{2(3.0)}{8.0}(8.0)+\frac{5.0-3.0}{8.0}(0) = \frac{6.0}{8.0}(8.0) = 6.0 \text{ m/s}$$
**v_Af = −2.0 m/s, v_Bf = 6.0 m/s**

**(b)** p_i = 3.0(8.0) = 24.0. p_f = 3.0(−2.0)+5.0(6.0) = −6.0+30.0 = 24.0 ✓

**(c)** KE_i = ½(3.0)(64) = 96.0 J. KE_f = ½(3.0)(4.0)+½(5.0)(36) = 6.0+90.0 = 96.0 J ✓

---

### Problem 7

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

### Problem 8

x_cm = [2.0(1.0)+3.0(4.0)+5.0(8.0)]/(2.0+3.0+5.0) = (2.0+12.0+40.0)/10.0 = 54.0/10.0 = **5.4 m**

---

### Problem 9

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

### Problem 10

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
