# PHYS 141 · Problem Set 6 INSTRUCTOR SOLUTIONS
**Do not distribute before the due date.**

---

> *Revised 2026-09-28: sub-parts cut from 29 to 18; the ten problems and their points are unchanged. The answers below keep the old letters. New → old: 1 (a, b) = (b, c) · 2 (a, b) = (b, c) · 3 unchanged · 4 (a, b) = (a, b), with (b) reworded to state φ = 50° directly · 5 (a, b) = (b, c) · 6 (a, b) = (a, b) · 7 (a, b) = (a, c) · 8 (a, b) = (b, c) · 9 (a, b) = (a, b) · 10 (a, b) = (b, d).*


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
| **A** | Rotational Kinematics | 1–3 | 30 |
| **B** | Torque and Moment of Inertia | 4–7 | 40 |
| **C** | Rotational Energy and Rolling | 8–10 | 30 |
| | **Total** | | **100** |

### Common errors in this problem set

**1. Using a moment of inertia for the wrong axis.** I is defined about a specific axis; the same body has different I about different axes. Require the axis to be stated, and apply the parallel-axis theorem where the axis is displaced.

**2. Confusing angular and linear quantities.** `α (rad/s²)` and a `(m/s²)` are related by `a = αR` only at radius R. Substituting one for the other is a method error.

**3. Ignoring the lever arm.** `τ = rF sinθ`. A force applied along the line through the pivot produces zero torque regardless of magnitude. Answers that use `rF` unconditionally lose method marks.

**4. Dropping the rolling constraint.** Rolling without slipping means `v_cm = ωR` and `a_cm = αR`. Without it the problem is underdetermined; students who get a numeric answer anyway have usually assumed something unstated.

---

### Problem 1

**(a)** ω = 0+4.0(5.0) = **20 rad/s**

**(b)** Δθ = ½(4.0)(25) = **50 rad**

**(c)** Revolutions = 50/(2π) = **7.96 rev**

---

### Problem 2

**(a)** ω₀=1800×π/30=188.5 rad/s; ω=600×π/30=62.83 rad/s

**(b)** α = (62.83−188.5)/8.0 = −125.66/8.0 = **−15.7 rad/s²**

**(c)** Δθ = ½(ω₀+ω)t = ½(188.5+62.83)(8.0) = ½(251.36)(8.0) = **1005.4 rad = 160.0 rev**

---

### Problem 3

r=0.25 m, ω=6.0 rad/s, α=2.0 rad/s²

$$a_t = r\alpha = 0.25\times2.0 = 0.50 \text{ m/s}^2$$
$$a_c = \omega^2r = 36\times0.25 = 9.0 \text{ m/s}^2$$
$$|a| = \sqrt{0.25+81} = \sqrt{81.25} = \mathbf{9.01 \text{ m/s}^2}$$

Direction from purely centripetal (radial) direction: θ=arctan(a_t/a_c)=arctan(0.50/9.0)=**3.18°** (tilted slightly toward the tangential direction from purely radially inward)

---

### Problem 4

**(a)** τ=Fd=60×0.80=**48.0 N·m**

**(b)** τ=rFsinφ=0.80×60×sin50°=48×0.766=**36.8 N·m**

**(c)** Torque is maximum when sinφ=1, i.e., **φ=90°** (force perpendicular to the lever arm)

---

### Problem 5

M=6.0 kg, R=0.35 m, τ=8.0 N·m

**(a)** I_disk=½(6.0)(0.1225)=0.3675 kg·m². I_hoop=6.0(0.1225)=0.735 kg·m²

**(b)** α_disk=8.0/0.3675=**21.77 rad/s²**. α_hoop=8.0/0.735=**10.88 rad/s²**

**(c)** Disk spins up **faster**, by a factor of 21.77/10.88 = **2.0×** (exactly, since I_hoop=2×I_disk for equal M, R)

---

### Problem 6

m₁=2.5 kg, m₂=4.0 kg, M_p=1.0 kg, R=0.12 m

**(a)** Using the massive-pulley formula:
$$a=\frac{(m_2-m_1)g}{m_1+m_2+\frac{1}{2}M_p}=\frac{(1.5)(9.81)}{2.5+4.0+0.5}=\frac{14.715}{7.0}=\mathbf{2.10 \text{ m/s}^2}$$

**(b)** T₁ (on m₁ side, up positive): T₁−m₁g=m₁a → T₁=m₁(g+a)=2.5(9.81+2.10)=2.5(11.91)=**29.78 N**
T₂ (on m₂ side, down positive): m₂g−T₂=m₂a → T₂=m₂(g−a)=4.0(9.81−2.10)=4.0(7.71)=**30.84 N**

**(c)** Net torque on pulley: (T₂−T₁)R=(30.84−29.78)(0.12)=(1.06)(0.12)=0.1272 N·m
I_pulley=½M_pR²=½(1.0)(0.0144)=0.0072 kg·m². α=a/R=2.10/0.12=17.5 rad/s²
Iα=0.0072×17.5=0.126 N·m ✓ (matches within rounding, 0.1272≈0.126)

---

### Problem 7

M=3.0 kg, L=1.2 m

**(a)** I=ML²/3=3.0(1.44)/3=**1.44 kg·m²**

**(b)** τ=Mg×(L/2)=3.0×9.81×0.60=**17.66 N·m** (gravity acts at CM, r=L/2 from pivot, force perpendicular to rod when horizontal)

**(c)** α=τ/I=17.66/1.44=**12.26 rad/s²**

**(d)** As the rod swings down from horizontal, the angle between the gravity force and the rod (r⃗) changes — specifically, the perpendicular component of gravity relative to the rod decreases as the rod approaches vertical (τ=Mg(L/2)cosφ, where φ is the angle from horizontal, so τ→0 as rod becomes vertical). Since τ is not constant, α is not constant, and the simple kinematic equations (ω=ω₀+αt, etc.) do NOT apply for the full swing. Energy methods (using KE_rot=½Iω² and gravitational PE change of the center of mass) are required instead — this will be covered explicitly in the next unit.

---

### Problem 8

M=4.0 kg, R=0.20 m, v=3.0 m/s

**(a)** ω=v/R=3.0/0.20=**15 rad/s**

**(b)** KE_trans=½(4.0)(9.0)=18.0 J
I=½(4.0)(0.04)=0.08 kg·m². KE_rot=½(0.08)(225)=**9.0 J**
KE_total=18.0+9.0=**27.0 J**

**(c)** Fraction rotational = 9.0/27.0 = **33.3%** (matches β/(1+β)=0.5/1.5=1/3 ✓)

---

### Problem 9

h=1.8 m

**(a)** Sphere (β=0.4): v=√(2×9.81×1.8/1.4)=√(35.316/1.4)=√25.23=**5.02 m/s**
Cylinder (β=0.5): v=√(35.316/1.5)=√23.54=**4.85 m/s**
Hoop (β=1.0): v=√(35.316/2.0)=√17.66=**4.20 m/s**

**(b)** Fastest to slowest speed (and arrival time, same order): **Sphere > Cylinder > Hoop**

**(c)** Frictionless sliding (no rotation, β effectively 0 since no rotational KE at all): v=√(2gh)=√35.316=**5.94 m/s**. This is LARGER than all three rolling cases, because none of the gravitational PE is diverted into rotational KE — 100% converts to translational KE.

---

### Problem 10

M=1.5 kg, R=0.10 m, β=2/3, θ=30°, L=3.0 m

**(a)** h=3.0×sin30°=3.0×0.5=**1.5 m**

**(b)** v=√(2gh/(1+β))=√(2×9.81×1.5/(1+0.667))=√(29.43/1.667)=√17.66=**4.20 m/s**

**(c)** a=g sinθ/(1+β)=9.81×0.5/1.667=4.905/1.667=**2.943 m/s²**
Check: v²=2aL=2(2.943)(3.0)=17.66 → v=4.20 m/s ✓ matches

**(d)** f_s=βMa=0.667×1.5×2.943=2.945 N
N=Mg cosθ=1.5×9.81×0.866=12.74 N
μ_s,min=f_s/N=2.945/12.74=**0.231**

---
