# PHYS 141 — Problem Set 0 — INSTRUCTOR SOLUTIONS

**Do not distribute to students before the due date.**

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
| **A** | Units & Dimensional Analysis | 1–6 | 30 |
| **B** | Significant Figures & Estimation | 7–10 | 20 |
| **C** | Coordinate Systems | 11–15 | 25 |
| **D** | Vectors | 16–20 | 25 |
| | **Total** | | **100** |

### Common errors in this problem set

**1. Treating units as labels rather than algebra.** Units multiply and cancel exactly like symbols. A student who writes the right number but cannot show the units reducing has not done dimensional analysis — award method marks only where the cancellation is visible.

**2. Significant figures from exact vs. measured quantities.** Counted or defined values (12 in a dozen, 100 cm per m) are exact and impose no sig-fig limit. Marking a result down to 2 s.f. because an exact 2 appeared in the formula is the classic error.

**3. Adding vector magnitudes.** |A+B| ≠ |A|+|B| except when parallel. Any answer that sums magnitudes directly loses the method marks even if the arithmetic is clean.

**4. Calculator in the wrong angle mode.** A systematically wrong trig answer with otherwise perfect setup is nearly always degrees/radians. Award the 3 method marks, withhold the 2 answer marks, and say why.

---

### Part A: Units & Dimensional Analysis

**1.**
(a) L = r×p → [r][p] = (L)(M·L·T⁻¹) = M·L²·T⁻¹ → SI: kg·m²/s
(b) E = F/q → [F]/[q] = (M·L·T⁻²)/(I·T) = M·L·T⁻³·I⁻¹ → SI: kg·m·s⁻³·A⁻¹ (= V/m)
(c) G = Fr²/(m₁m₂) → (M·L·T⁻²)(L²)/(M²) = M⁻¹L³T⁻² → SI: m³·kg⁻¹·s⁻²

**2.** [KE] = [m][v²] = M·(L·T⁻¹)² = M·L²·T⁻² = kg·m²/s² = Joule ✓ Consistent.

**3.** [T] = T. [√(m/k)]: [k] = N/m = kg·s⁻². [m/k] = kg/(kg·s⁻²) = s². √(s²) = s. ✓ Dimensionally consistent (formula is correct, in fact).

**4.** [F] = [ρ][v²][A] = (M·L⁻³)(L²T⁻²)(L²) = M·L·T⁻². This matches [Force] = M·L·T⁻². ✓ Consistent.

**5.**
(a) 88 km/h × (1000 m/km) × (1 h/3600 s) = 24.4 m/s
(b) 1 ly = c × 1 yr = 2.998×10⁸ m/s × 3.156×10⁷ s ≈ 9.46×10¹⁵ m. In miles: 9.46×10¹⁵/1609.34 ≈ 5.88×10¹² miles
(c) 101325 Pa × (1 lb/4.448 N) × (0.0254 m/1 in)² = 101325 × (1/4.448) × (0.0254)² ... 
Pa = N/m². Convert: 101325 N/m² × (1 lb/4.448 N) = 22778 lb/m². Then ×(0.0254 m/in)² = 22778 × 6.4516×10⁻⁴ = 14.7 lb/in² (psi). ✓ matches known value of 14.7 psi.

**6.** T = C·rᵃ·Mᵇ·Gᶜ
[T] = T¹
[r] = Lᵃ, [M]=Mᵇ, [G]=L³ᶜM⁻ᶜT⁻²ᶜ
T¹ = L^(a+3c) M^(b-c) T^(-2c)
Match: T: 1 = -2c → c = -1/2
M: 0 = b - c → b = c = -1/2
L: 0 = a + 3c → a = -3c = 3/2
Result: T = C·r^(3/2)·M^(-1/2)·G^(-1/2), i.e., T ∝ √(r³/(GM)) — this is Kepler's Third Law structure.

---

### Part B: Sig Figs & Estimation

**7.**
(a) 4.52×3.1 = 14.012 → 14 (2 sig figs)
(b) 18.0/3.652 = 4.9288... → 4.93 (3 sig figs)
(c) 12.65+1.2+0.075 = 13.925 → 13.9 (1 decimal place, matching 1.2)
(d) (2.50×10³)(1.2×10⁻⁵) = 3.0×10⁻² (2 sig figs)

**8.** 12.34 × 5.2 = 64.168 → **64 cm²** (2 sig figs, matching the 5.2 cm factor which has the fewest sig figs)

**9.** Sample reasoning: Ocean covers ~70% of Earth's surface area (4πR²≈4π(6.4×10⁶)²≈5.1×10¹⁴ m²) → ocean area ≈3.6×10¹⁴ m². Average ocean depth ≈3700 m (or estimate ~3-4 km). Volume ≈3.6×10¹⁴×3700≈1.3×10¹⁸ m³. Mass = volume×density(1000 kg/m³) ≈1.3×10²¹ kg. Matches accepted ~1.4×10²¹ kg well (order of magnitude and even leading digit agree). Grade on reasoning process, not exact numeric match.

**10.** Sample: ~70 beats/min × 60 min × 24 hr × 365 days × ~75 years ≈ 70×60×24×365×75 ≈ 2.76×10⁹ beats. Accept any answer in the 2-3×10⁹ range with sound reasoning.

---

### Part C: Coordinate Systems

**11.** r=√(9+16)=5. θ=atan2(4,-3)=180°-53.13°=126.87° (2nd quadrant since x<0,y>0)

**12.** x=8cos(210°)=8(-0.866)=-6.93, y=8sin(210°)=8(-0.5)=-4.00 → (-6.93,-4.00)

**13.** x=6sin45°cos120°=6(0.707)(-0.5)=-2.12
y=6sin45°sin120°=6(0.707)(0.866)=3.67
z=6cos45°=4.24
→ (-2.12, 3.67, 4.24)

**14.** r=√3≈1.732, θ=arccos(1/√3)≈54.7°, φ=atan2(1,1)=45°

**15.** Sample answer: θ̂ points in the direction of increasing θ at a given location, and that direction rotates as you move around the origin — at θ=0° it points in +y, at θ=90° it points in -x, etc. x̂ in Cartesian always points the same way regardless of position. Consequence: when differentiating position vectors in polar coordinates to get velocity/acceleration, you must apply the product rule to BOTH the magnitude AND the changing unit vectors (dr̂/dt ≠ 0 in general), producing extra terms (centripetal, Coriolis-like) absent in Cartesian differentiation.

---

### Part D: Vectors

**16.**
(a) A+B=(-2,-1,5), A-B=(6,-1,1)
(b) |A|=√(4+1+9)=√14≈3.742, |B|=√(16+0+4)=√20≈4.472
(c) Â = (2,-1,3)/√14 ≈ (0.535,-0.267,0.802)

**17.** A·B=(1)(2)+(2)(0)+(2)(-1)=2-2=0 → cosθ=0 → θ=90°

**18.** W=F·d=(5)(2)+(3)(-1)+(0)(0)=10-3=7 J. Positive — the force has a net component along the direction of displacement, so positive work is done on the object (it speeds up, all else equal).

**19.** A×B=(1,0,0)×(0,1,0)=(0·0-0·1, 0·0-1·0, 1·1-0·0)=(0,0,1). Right-hand rule: fingers along x̂ curl toward ŷ, thumb points +ẑ ✓. B×A=-(A×B)=(0,0,-1), confirming anti-commutativity.

**20.**
(a) τ=r×F=(0.3,0,0)×(0,-20,0)=(0·0-0·(-20), 0·0-0.3·0, 0.3·(-20)-0·0)=(0,0,-6) N·m
(b) |τ|=6 N·m
(c) If r=(0,0.3,0), then τ=r×F=(0,0.3,0)×(0,-20,0)=(0·0-0·(-20), 0·0-0·0, 0·(-20)-0.3·0)=(0,0,0). Torque is zero because r and F are now parallel (both along y) — the cross product of parallel vectors is always zero, and physically, a force applied directly toward/away from the pivot produces no rotational effect (no "leverage").
