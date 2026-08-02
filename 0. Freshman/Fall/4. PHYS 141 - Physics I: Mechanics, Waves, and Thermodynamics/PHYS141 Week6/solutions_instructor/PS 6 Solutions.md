# PHYS 141 · Problem Set 6 INSTRUCTOR SOLUTIONS
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
| **A** | Rotational Kinematics | 1–6 | 30 |
| **B** | Torque and Moment of Inertia | 7–14 | 40 |
| **C** | Rotational Energy and Rolling | 15–20 | 30 |
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

r=0.40 m, v=6.0 m/s, a_c=45 m/s²

**(a)** ω=v/r=6.0/0.40=**15 rad/s**. Check: a_c=ω²r=225×0.40=90 m/s²... discrepancy — let's use given a_c directly instead: ω=√(a_c/r)=√(45/0.40)=√112.5=10.6 rad/s. 

Note: the problem gives both v and a_c: they should be consistent if a_c=v²/r. Check: v²/r=36/0.40=90, but given a_c=45. These are inconsistent in the problem as stated — treat as two separate sub-calculations for instructional purposes, primarily using ω=v/r as the intended path:

**(a) ω = v/r = 6.0/0.40 = 15 rad/s** (using tangential speed, as intended)

**(b)** T=2π/ω=2π/15=**0.419 s**

**(c)** v=rω=0.40×15=6.0 m/s ✓ matches given v.

*(Note to instructor: if using the given a_c=45 m/s² independently, ω would be 10.6 rad/s — flag this inconsistency for students who notice it; award full credit for either consistent approach with clear reasoning.)*

---

### Problem 4

v=1.2 m/s (constant), r₁=0.030 m

**(a)** ω₁=v/r₁=1.2/0.030=40 rad/s. In rpm: 40×30/π=**382.0 rpm**

**(b)** ω₂=v/r₂=1.2/0.058=20.69 rad/s. **Decreased** (ω₂<ω₁) — since v is fixed, larger r requires smaller ω (ω=v/r, inverse relationship).

---

### Problem 5

**(a)** ω_max=12000×π/30=1256.6 rad/s. α=Δω/t=1256.6/15=**83.78 rad/s²**

**(b)** Δθ=½ω_max×t (from rest) = ½(1256.6)(15)=9424.8 rad = 9424.8/(2π)=**1500 rev**

**(c)** Constant speed phase: t=5.0×60=300 s. Δθ=ω×t=1256.6×300=376,991 rad = 376991/(2π)=**60,000 rev**

**(d)** α_decel=(0−1256.6)/20=**−62.83 rad/s²**. Δθ=½(1256.6)(20)=12566 rad=12566/(2π)=**2000 rev**

**(e)** Total = 1500+60000+2000 = **63,500 revolutions**

---

### Problem 6

r=0.25 m, ω=6.0 rad/s, α=2.0 rad/s²

$$a_t = r\alpha = 0.25\times2.0 = 0.50 \text{ m/s}^2$$
$$a_c = \omega^2r = 36\times0.25 = 9.0 \text{ m/s}^2$$
$$|a| = \sqrt{0.25+81} = \sqrt{81.25} = \mathbf{9.01 \text{ m/s}^2}$$

Direction from purely centripetal (radial) direction: θ=arctan(a_t/a_c)=arctan(0.50/9.0)=**3.18°** (tilted slightly toward the tangential direction from purely radially inward)

---

### Problem 7

**(a)** τ=Fd=60×0.80=**48.0 N·m**

**(b)** τ=rFsinφ=0.80×60×sin50°=48×0.766=**36.8 N·m**

**(c)** Torque is maximum when sinφ=1, i.e., **φ=90°** (force perpendicular to the lever arm)

---

### Problem 8

M=2.0 kg, L=1.5 m

**Table value (end):** I=ML²/3=2.0(2.25)/3=**1.5 kg·m²**

**Parallel axis check:** I_cm=ML²/12=2.0(2.25)/12=0.375 kg·m². d=L/2=0.75 m.
I_end=I_cm+Md²=0.375+2.0(0.5625)=0.375+1.125=**1.5 kg·m²** ✓ matches

---

### Problem 9

M=6.0 kg, R=0.35 m, τ=8.0 N·m

**(a)** I_disk=½(6.0)(0.1225)=0.3675 kg·m². I_hoop=6.0(0.1225)=0.735 kg·m²

**(b)** α_disk=8.0/0.3675=**21.77 rad/s²**. α_hoop=8.0/0.735=**10.88 rad/s²**

**(c)** Disk spins up **faster**, by a factor of 21.77/10.88 = **2.0×** (exactly, since I_hoop=2×I_disk for equal M, R)

---

### Problem 10

M=250 kg, R=2.0 m, F=150 N

**(a)** I=½(250)(4.0)=**500 kg·m²**

**(b)** τ=FR=150×2.0=300 N·m. α=τ/I=300/500=**0.60 rad/s²**

**(c)** t=ω/α=0.50/0.60=**0.833 s**

**(d)** Δθ=½αt²=½(0.60)(0.694)=0.208 rad = **0.0332 rev**

---

### Problem 11

M_disk=3.0 kg, R=0.20 m, m_point=1.0 kg at r=R

$$I_{disk}=\frac{1}{2}(3.0)(0.04)=0.06 \text{ kg·m}^2$$
$$I_{point}=1.0(0.04)=0.04 \text{ kg·m}^2$$
$$I_{total}=0.06+0.04=\mathbf{0.10 \text{ kg·m}^2}$$

---

### Problem 12

m₁=2.5 kg, m₂=4.0 kg, M_p=1.0 kg, R=0.12 m

**(a)** Using the massive-pulley formula:
$$a=\frac{(m_2-m_1)g}{m_1+m_2+\frac{1}{2}M_p}=\frac{(1.5)(9.81)}{2.5+4.0+0.5}=\frac{14.715}{7.0}=\mathbf{2.10 \text{ m/s}^2}$$

**(b)** T₁ (on m₁ side, up positive): T₁−m₁g=m₁a → T₁=m₁(g+a)=2.5(9.81+2.10)=2.5(11.91)=**29.78 N**
T₂ (on m₂ side, down positive): m₂g−T₂=m₂a → T₂=m₂(g−a)=4.0(9.81−2.10)=4.0(7.71)=**30.84 N**

**(c)** Net torque on pulley: (T₂−T₁)R=(30.84−29.78)(0.12)=(1.06)(0.12)=0.1272 N·m
I_pulley=½M_pR²=½(1.0)(0.0144)=0.0072 kg·m². α=a/R=2.10/0.12=17.5 rad/s²
Iα=0.0072×17.5=0.126 N·m ✓ (matches within rounding, 0.1272≈0.126)

---

### Problem 13

I=12.0 kg·m², τ=30 N·m

**(a)** α=τ/I=30/12.0=**2.5 rad/s²**

**(b)** t=ω/α=100/2.5=**40 s**

**(c)** Δθ=½αt²=½(2.5)(1600)=2000 rad = **318.3 rev**

**(d)** W=τΔθ=30×2000=**60,000 J**
Check: KE_f=½Iω²=½(12.0)(10000)=60,000 J ✓ matches exactly (work-energy theorem for rotation)

---

### Problem 14

M=3.0 kg, L=1.2 m

**(a)** I=ML²/3=3.0(1.44)/3=**1.44 kg·m²**

**(b)** τ=Mg×(L/2)=3.0×9.81×0.60=**17.66 N·m** (gravity acts at CM, r=L/2 from pivot, force perpendicular to rod when horizontal)

**(c)** α=τ/I=17.66/1.44=**12.26 rad/s²**

**(d)** As the rod swings down from horizontal, the angle between the gravity force and the rod (r⃗) changes — specifically, the perpendicular component of gravity relative to the rod decreases as the rod approaches vertical (τ=Mg(L/2)cosφ, where φ is the angle from horizontal, so τ→0 as rod becomes vertical). Since τ is not constant, α is not constant, and the simple kinematic equations (ω=ω₀+αt, etc.) do NOT apply for the full swing. Energy methods (using KE_rot=½Iω² and gravitational PE change of the center of mass) are required instead — this will be covered explicitly in the next unit.

---

### Problem 15

M=2.0 kg, R=0.15 m, ω=12 rad/s

**(a)** I=(2/5)(2.0)(0.0225)=**0.018 kg·m²**

**(b)** KE_rot=½(0.018)(144)=**1.296 J**

---

### Problem 16

M=4.0 kg, R=0.20 m, v=3.0 m/s

**(a)** ω=v/R=3.0/0.20=**15 rad/s**

**(b)** KE_trans=½(4.0)(9.0)=18.0 J
I=½(4.0)(0.04)=0.08 kg·m². KE_rot=½(0.08)(225)=**9.0 J**
KE_total=18.0+9.0=**27.0 J**

**(c)** Fraction rotational = 9.0/27.0 = **33.3%** (matches β/(1+β)=0.5/1.5=1/3 ✓)

---

### Problem 17

h=1.8 m

**(a)** Sphere (β=0.4): v=√(2×9.81×1.8/1.4)=√(35.316/1.4)=√25.23=**5.02 m/s**
Cylinder (β=0.5): v=√(35.316/1.5)=√23.54=**4.85 m/s**
Hoop (β=1.0): v=√(35.316/2.0)=√17.66=**4.20 m/s**

**(b)** Fastest to slowest speed (and arrival time, same order): **Sphere > Cylinder > Hoop**

**(c)** Frictionless sliding (no rotation, β effectively 0 since no rotational KE at all): v=√(2gh)=√35.316=**5.94 m/s**. This is LARGER than all three rolling cases, because none of the gravitational PE is diverted into rotational KE — 100% converts to translational KE.

---

### Problem 18

M=6.0 kg, R=0.11 m, v=2.5 m/s (solid sphere, β=0.4)

**(a)** KE_total=½Mv²(1+β)=½(6.0)(6.25)(1.4)=18.75×1.4=**26.25 J**

**(b)** All KE converts to gravitational PE at max height (ball momentarily fully at rest, both translation and rotation, since rolling without slipping means ω=0 when v=0):
Mgh=26.25 → h=26.25/(6.0×9.81)=26.25/58.86=**0.446 m**

---

### Problem 19

M=1.5 kg, R=0.10 m, β=2/3, θ=30°, L=3.0 m

**(a)** h=3.0×sin30°=3.0×0.5=**1.5 m**

**(b)** v=√(2gh/(1+β))=√(2×9.81×1.5/(1+0.667))=√(29.43/1.667)=√17.66=**4.20 m/s**

**(c)** a=g sinθ/(1+β)=9.81×0.5/1.667=4.905/1.667=**2.943 m/s²**
Check: v²=2aL=2(2.943)(3.0)=17.66 → v=4.20 m/s ✓ matches

**(d)** f_s=βMa=0.667×1.5×2.943=2.945 N
N=Mg cosθ=1.5×9.81×0.866=12.74 N
μ_s,min=f_s/N=2.945/12.74=**0.231**

---

### Problem 20

M=0.20 kg, R_body=0.035 m, R_axle=0.025 m, I=½MR_body²

**(a)** Energy conservation: Mgh=½Mv_cm²+½Iω², with ω=v_cm/R_axle:
Mgh=½Mv_cm²+½I(v_cm/R_axle)²=½Mv_cm²[1+I/(MR_axle²)]
**v=√(2gh/[1+I/(MR_axle²)])** — derived as required.

**(b)** I=½(0.20)(0.035)²=½(0.20)(0.001225)=0.0001225 kg·m²
I/(MR_axle²)=0.0001225/(0.20×0.000625)=0.0001225/0.000125=**0.980**

So the "effective β" for the yo-yo (using axle radius as the rolling radius) is **0.980** — nearly 1, similar to a hoop, and much larger than a typical rolling object's β would be if computed with the body radius.

**(c)** v=√(2×9.81×0.50/(1+0.980))=√(9.81/1.980)=√4.955=**2.226 m/s**

**(d)** A ball falling freely from h=0.50 m would reach v=√(2×9.81×0.50)=√9.81=3.13 m/s — noticeably faster than the yo-yo's 2.23 m/s. The yo-yo descends more slowly because the large ratio I/(MR_axle²)≈0.98 means nearly half of the released gravitational PE goes into rotational KE (spinning the yo-yo body) rather than translational KE (the downward motion), even though the string unwinds from the much smaller axle. This large effective β arises because the yo-yo's moment of inertia is set by its full outer radius R_body, but the rolling constraint operates at the tiny R_axle — a mismatch that dramatically amplifies the fraction of energy diverted to rotation, which is exactly why yo-yos "hover" descending slowly compared to free fall.
