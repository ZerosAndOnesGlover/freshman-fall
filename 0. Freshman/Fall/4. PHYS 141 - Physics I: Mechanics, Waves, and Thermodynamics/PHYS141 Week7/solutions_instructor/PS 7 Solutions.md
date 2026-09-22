# PHYS 141 · Problem Set 7 — INSTRUCTOR SOLUTIONS
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
| **A** | Angular Momentum | 1–3 | 30 |
| **B** | Conservation of Angular Momentum | 4–7 | 40 |
| **C** | Static Equilibrium | 8–10 | 30 |
| | **Total** | | **100** |

### Common errors in this problem set

**1. Applying L = Iω outside its scope.** L = Iω holds for a rigid body rotating about a fixed axis. For a point particle use L = r × p = rmv sinθ.

**2. Conserving L without checking external torque.** Angular momentum conserves only when the net external torque about the chosen axis is zero. The axis matters — L can be conserved about one point and not another.

**3. Checking only ΣF = 0 for equilibrium.** Static equilibrium requires **both** ΣF = 0 and Στ = 0. A solution that balances forces and stops has done half the problem.

**4. Believing the pivot choice changes the answer.** In equilibrium any pivot works, because Στ = 0 about every point. Choosing the pivot at an unknown force's line of action eliminates it — reward students who exploit this.

---

### Problem 1

L=mvr=0.30×6.0×1.5=**2.7 kg·m²/s**

---

### Problem 2

I=½MR²=½(5.0)(0.16)=0.40 kg·m²
L=Iω=0.40×10=**4.0 kg·m²/s**

---

### Problem 3

m=2.0 kg, r⃗=(3.0,0,0), v⃗=(0,5.0,0)

**(a)** L⃗=m(r⃗×v⃗)=2.0[(0×0−0×5.0)x̂−(3.0×0−0×0)ŷ+(3.0×5.0−0×0)ẑ]=2.0(0,0,15)=**(0,0,30) kg·m²/s**

**(b)** τ⃗=r⃗×F⃗=(3.0,0,0)×(0,0,10)=[(0×10−0×0)x̂−(3.0×10−0×0)ŷ+(3.0×0−0×0)ẑ]=(0,−30,0) N·m

This torque points in the −y direction, which means dL⃗/dt has a −y component — this would change the y-component of L (currently zero) to become negative over time, tilting the angular momentum vector away from pure +z. This is directionally consistent — a torque perpendicular to the current L⃗ changes its direction, exactly as described conceptually for gyroscopic precession in Lecture 23.

---

### Problem 4

I_i=5.0, ω_i=3.0, I_f=2.0

**(a)** ω_f=I_iω_i/I_f=(5.0×3.0)/2.0=15.0/2.0=**7.5 rad/s**

**(b)** KE_i=½(5.0)(9.0)=22.5 J. KE_f=½(2.0)(56.25)=56.25 J.
**KE increases from 22.5 J to 56.25 J** (an increase of 33.75 J) — this additional energy comes from the internal work done by the skater's muscles pulling their arms inward against the effective outward tendency of their own rotating mass, converting chemical/muscular energy into rotational kinetic energy.

---

### Problem 5

I_platform=200, m=60, ω_i=2.0, r=1.5

**(a)** I_f=200+60(1.5)²=200+60(2.25)=200+135=335 kg·m²
ω_f=I_iω_i/I_f=(200×2.0)/335=400/335=**1.194 rad/s**

**(b)** Fractional decrease=(2.0−1.194)/2.0=0.806/2.0=**40.3%**

---

### Problem 6

I₁=0.60, ω₀=12, I₂=0.60 (stationary)

**(a)** L_i=I₁ω₀=0.60×12=7.2 kg·m²/s. ω_f=L_i/(I₁+I₂)=7.2/1.2=**6.0 rad/s**

**(b)** KE_i=½(0.60)(144)=43.2 J. KE_f=½(1.2)(36)=21.6 J. **KE lost=43.2−21.6=21.6 J** (exactly 50% lost)

**(c)** Linear analog: equal masses, one at rest, perfectly inelastic collision. Fractional KE lost=m₂/(m₁+m₂)=1/2=50% (from Week 5 pattern). **This exactly matches the 50% found here** — confirming the deep structural analogy between linear and rotational perfectly-inelastic "collisions" when the interacting quantities (mass↔moment of inertia) are equal.

---

### Problem 7

**(a)** I_f/I_i = (2/5)MR_f²/[(2/5)MR_0²] = (R_f/R_0)² = (12000/7×10^8)² = (1.714×10⁻⁵)² = **2.939×10⁻¹⁰**

**(b)** I_iω_i=I_fω_f → ω_f=ω_i×(I_i/I_f)=ω_i/(2.939×10⁻¹⁰)
ω_i=2π/T_i, T_i=25 days=25×86400=2.16×10⁶ s. ω_i=2π/2.16×10⁶=2.909×10⁻⁶ rad/s
ω_f=2.909×10⁻⁶/2.939×10⁻¹⁰=9895 rad/s
T_f=2π/ω_f=2π/9895=**6.35×10⁻⁴ s** (about 0.635 milliseconds per rotation, i.e., ~1575 rotations per second)

**(c)** This is extremely fast — faster even than the fastest known real pulsars (~716 rotations/second, or ~1.4 ms period). This idealized calculation (perfect angular momentum conservation, uniform sphere throughout, no mass loss) overestimates the true spin-up, since real supernovae eject significant mass (carrying away angular momentum) and involve complex internal structure changes — but the calculation correctly demonstrates the qualitative and order-of-magnitude plausibility of forming an extremely fast-spinning neutron star from a slowly-rotating progenitor star, purely via angular momentum conservation during radius collapse.

---

### Problem 8

L=8.0 m, W_beam=600 N (center, x=4.0 m from left), W_load=900 N at x=3.0 m

Pivot at left support (x=0):
Στ = N_right(8.0) − 600(4.0) − 900(3.0) = 0
N_right(8.0) = 2400+2700=5100
N_right = 5100/8.0 = **637.5 N**

ΣF_y: N_left+N_right−600−900=0 → N_left=1500−637.5=**862.5 N**

---

### Problem 9

L=4.0 m, W=180 N, θ=65°

Pivot at base:
N_wall(Lsinθ) = W(L/2)cosθ
N_wall(4.0×sin65°)=180×2.0×cos65°
N_wall(4.0×0.906)=180×2.0×0.4226
N_wall(3.624)=152.1
N_wall=**41.96 N ≈ 42.0 N**

N_floor=W=**180 N** (from ΣF_y=0, since wall force is purely horizontal)

f_s=N_wall (from ΣF_x=0)=**42.0 N**
μ_s,min=f_s/N_floor=42.0/180=**0.233**

---

### Problem 10

L=5.0 m, W_beam=300 N (center, x=2.5 m), θ_cable=35°, hinge at x=0

**(a)** Pivot at hinge:
Στ = T sin35°(5.0) − 300(2.5) = 0
T(0.5736)(5.0) = 750
T(2.868) = 750
T = **261.5 N**

**(b)** ΣF_x: H_x − Tcos35° = 0 → H_x = 261.5×0.8192 = **214.2 N**
ΣF_y: H_y + Tsin35° − 300 = 0 → H_y = 300 − 261.5(0.5736) = 300−150.0 = **150.0 N**

**(c)** |H| = √(214.2²+150.0²) = √(45882+22500) = √68382 = **261.5 N**

---
