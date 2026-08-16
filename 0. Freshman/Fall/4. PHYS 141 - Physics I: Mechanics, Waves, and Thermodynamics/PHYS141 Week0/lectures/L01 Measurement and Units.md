# PHYS 141 · Lecture 1
# Measurement, Units & Dimensional Analysis

> **Core Principle:** Physics is an experimental science. Every quantity we discuss must be measurable — and the measurement must be reported with its units and its uncertainty. A number without units is not a physical quantity; it is a mathematical abstraction.

**Date:** Monday 17 August 2026 · 14:00–14:50 · Week 0

---


## Where This Fits

**Previously:** This is the starting point — no prior lecture to build on. What it assumes is only arithmetic and algebra.

---

## 1. Why Measurement is the Foundation of Physics

Physics begins not with equations, but with observation. An observation becomes a measurement when we attach a number and a unit to it. The unit is the agreement — shared by all physicists globally — about what "1 meter" or "1 kilogram" means. Without this agreement, equations would be meaningless.

**The critical insight:** When you write *F = ma*, you are not writing a relationship between numbers — you are writing a relationship between *physical quantities*. Each quantity carries a dimension (Length, Mass, Time, etc.), and the equation must be consistent in dimension on both sides. This is not optional; it is enforced by nature.

---

## 2. The International System of Units (SI)

The SI system defines **7 base units** from which every other physical unit can be derived:

| Quantity | SI Unit | Symbol | Physical Meaning |
|----------|---------|--------|-----------------|
| Length | meter | m | Distance light travels in 1/299,792,458 s |
| Mass | kilogram | kg | Defined via Planck constant h = 6.626×10⁻³⁴ J·s |
| Time | second | s | 9,192,631,770 periods of Cs-133 hyperfine transition |
| Electric current | ampere | A | Defined via elementary charge e = 1.602×10⁻¹⁹ C |
| Temperature | kelvin | K | Defined via Boltzmann constant k_B = 1.381×10⁻²³ J/K |
| Amount of substance | mole | mol | 6.022×10²³ elementary entities (Avogadro's number) |
| Luminous intensity | candela | cd | Defined via specific radiation frequency |

> **Note (post-2019 SI):** Since 2019, all SI base units are defined by fixing the numerical values of fundamental physical constants — not by physical artifacts. The kilogram is no longer defined by a platinum cylinder in Paris; it is defined by fixing Planck's constant. This makes the definitions permanent and universally accessible.

### 2.1 SI Prefixes

| Prefix | Symbol | Factor | Example |
|--------|--------|--------|---------|
| tera | T | 10¹² | 1 THz = 10¹² Hz |
| giga | G | 10⁹ | 1 GW = 10⁹ W |
| mega | M | 10⁶ | 1 MHz = 10⁶ Hz |
| kilo | k | 10³ | 1 km = 10³ m |
| centi | c | 10⁻² | 1 cm = 10⁻² m |
| milli | m | 10⁻³ | 1 mm = 10⁻³ m |
| micro | μ | 10⁻⁶ | 1 μm = 10⁻⁶ m |
| nano | n | 10⁻⁹ | 1 nm = 10⁻⁹ m |
| pico | p | 10⁻¹² | 1 ps = 10⁻¹² s |
| femto | f | 10⁻¹⁵ | 1 fm = 10⁻¹⁵ m (nuclear scale) |

---

## 3. Derived Units

Every other SI unit is a combination of the 7 base units. The derivation is always from **definitions** in physics.

### Examples

**Newton (force):**
Newton's second law: F = ma → [Force] = kg·m/s²

We call this 1 Newton: **1 N = 1 kg·m·s⁻²**

**Joule (energy):**
Work = Force × distance → [Energy] = N·m = kg·m²·s⁻²

We call this 1 Joule: **1 J = 1 kg·m²·s⁻²**

**Watt (power):**
Power = Energy/time → [Power] = J/s = kg·m²·s⁻³

We call this 1 Watt: **1 W = 1 kg·m²·s⁻³**

**Pascal (pressure):**
Pressure = Force/area → [Pressure] = N/m² = kg·m⁻¹·s⁻²

We call this 1 Pascal: **1 Pa = 1 kg·m⁻¹·s⁻²**

---

## 4. Dimensional Analysis

### 4.1 What is a Dimension?

A **dimension** is the physical nature of a quantity — independent of the unit system. We write dimensions using capital letters in square brackets:

- [Length] = L
- [Mass] = M  
- [Time] = T
- [Temperature] = Θ
- [Electric current] = I

The SI unit for length is the meter; the `CGS` unit is the centimeter; the imperial unit is the foot. These are all *units* for the same *dimension* L.

### 4.2 The Fundamental Rule

**Every physically meaningful equation must be `dimensionally` homogeneous:** the dimensions on the left side must equal the dimensions on the right side.

This is one of the most powerful tools in physics — it lets you:
1. **Check equations** for errors
2. **Derive relationships** between quantities when you know what depends on what
3. **Estimate** unknown quantities from known ones

### 4.3 Checking an Equation

**Example:** Is the equation for the period of a simple pendulum T = 2π√(L/g) dimensionally correct?

Left side: [T] = T (time)

Right side: 2π is dimensionless. L is length: [L] = L. g is gravitational acceleration: [g] = L·T⁻²

$$\left[\sqrt{\frac{L}{g}}\right] = \sqrt{\frac{L}{L \cdot T^{-2}}} = \sqrt{T^2} = T$$

✓ Both sides have dimension T. The equation is dimensionally consistent.

### 4.4 Deriving a Relationship (Buckingham π Theorem in action)

**Example:** A ball is dropped from height h. Its speed v when it hits the ground depends on h and g (gravitational acceleration). Find v as a function of h and g.

We assert: v = C · hᵃ · gᵇ where C is a dimensionless constant and a, b are unknown exponents.

Write dimensions:
- [v] = L·T⁻¹
- [h] = L
- [g] = L·T⁻²

So: L·T⁻¹ = Lᵃ · (L·T⁻²)ᵇ = L^(a+b) · T^(-2b)

Match exponents:
- L: 1 = a + b
- T: -1 = -2b → **b = 1/2**
- Therefore: **a = 1/2**

Result: v = C · h^(1/2) · g^(1/2) = C√(gh)

The exact result (from energy conservation) gives C = √2, so v = √(2gh). Dimensional analysis gave us the structure; physics gives the constant.

> **Deep Why:** Dimensional analysis works because the laws of physics are relationships between physical quantities — not between numbers. Nature does not "know" whether you measure in meters or feet. Any valid law must therefore be expressible in a form that is independent of the choice of units, which forces dimensional homogeneity.

---

## 5. Significant Figures and Scientific Notation

### 5.1 Scientific Notation

Every measurement should be expressed in scientific notation when many orders of magnitude are involved:

$$a \times 10^n \quad \text{where } 1 \leq a < 10$$

**Examples:**
- 299,792,458 m/s = 2.99792458 × 10⁸ m/s
- 0.000000000167 m = 1.67 × 10⁻¹⁰ m (atomic radius scale)
- 6.022 × 10²³ mol⁻¹ (Avogadro's number)

### 5.2 Significant Figures

Significant figures communicate the precision of a measurement. The rules:

1. All non-zero digits are significant: **134** has 3 sig figs
2. Zeros between non-zero digits are significant: **1004** has 4 sig figs
3. Leading zeros are NOT significant: **0.0045** has 2 sig figs
4. Trailing zeros after a decimal point ARE significant: **2.300** has 4 sig figs
5. Trailing zeros in an integer are ambiguous: **2300** could be 2, 3, or 4 sig figs → use scientific notation: **2.3 × 10³** (2 sig figs)

### 5.3 Rules for Calculations

**Multiplication/Division:** Result has as many sig figs as the input with the fewest sig figs.

```
3.14159 × 2.5 = 7.853975... → round to 7.9 (2 sig figs)
```

**Addition/Subtraction:** Result has as many decimal places as the input with the fewest decimal places.

```
15.23 + 6.1 + 0.521 = 21.851 → round to 21.9 (1 decimal place)
```

> **Warning:** Do not round intermediate results. Carry extra digits through a calculation and round only the final answer.

---

## 6. Orders of Magnitude

A physicist's essential skill: estimating the approximate scale of a quantity without computing it exactly. This is called **Fermi estimation**.

### Characteristic Length Scales

| Object | Scale |
|--------|-------|
| Proton radius | ~10⁻¹⁵ m |
| Atom radius | ~10⁻¹⁰ m |
| Virus | ~10⁻⁷ m |
| Human cell | ~10⁻⁵ m |
| Human height | ~1 m |
| Earth radius | ~6 × 10⁶ m |
| Earth–Sun distance | ~1.5 × 10¹¹ m |
| Milky Way diameter | ~10²¹ m |
| Observable universe | ~10²⁶ m |

### Characteristic Time Scales

| Event | Scale |
|-------|-------|
| Light crossing an atom | ~10⁻¹⁹ s |
| Nuclear decay (fast) | ~10⁻²³ s |
| Atomic transition | ~10⁻⁸ s |
| Nerve impulse | ~10⁻³ s |
| Human heartbeat | ~1 s |
| Human lifetime | ~2 × 10⁹ s |
| Age of universe | ~4 × 10¹⁷ s |

### Fermi Estimation Example

**Q: How many piano tuners are in Chicago?**

- Chicago population: ~3 × 10⁶ people
- Average household size: ~2.5 people → ~1.2 × 10⁶ households
- Fraction with piano: ~1 in 20 → ~6 × 10⁴ pianos
- Each piano tuned ~1×/year; tuner tunes ~4/day × 250 days/year = 1000/year
- Number of tuners: 6 × 10⁴ / 10³ ≈ **60 piano tuners**

(The actual answer is roughly 50–100.)

---

## 7. Unit Conversion

Unit conversion is multiplication by 1. You express "1" as a ratio of equivalent quantities:

$$1 = \frac{1609.34 \text{ m}}{1 \text{ mile}} = \frac{1 \text{ mile}}{1609.34 \text{ m}}$$

Choose the ratio that cancels the unit you want to eliminate.

**Example:** Convert 60 miles per hour to meters per second.

$$60 \frac{\text{miles}}{\text{hour}} \times \frac{1609.34 \text{ m}}{1 \text{ mile}} \times \frac{1 \text{ hour}}{3600 \text{ s}} = \frac{60 \times 1609.34}{3600} \frac{\text{m}}{\text{s}} \approx 26.8 \text{ m/s}$$

---

## 8. Summary Table

| Concept | Key Point |
|---------|-----------|
| SI Base Units | 7 base units; all others derived |
| Dimensions | L, M, T, Θ, I — nature of quantity, not unit choice |
| Dimensional Homogeneity | Both sides of any valid equation must have the same dimensions |
| Sig Figs | Reflects precision; multiply/divide → match fewest sig figs; add/subtract → match fewest decimal places |
| Fermi Estimation | Order-of-magnitude reasoning; a powerful physical intuition tool |
| Unit Conversion | Multiply by ratios equal to 1; cancel unwanted units |

---

## Worked Problems

**Problem 1.1:** The speed of light is c = 3.00 × 10⁸ m/s. Express this in miles per hour.

**Solution:**
$$c = 3.00 \times 10^8 \frac{\text{m}}{\text{s}} \times \frac{1 \text{ mile}}{1609.34 \text{ m}} \times \frac{3600 \text{ s}}{1 \text{ hr}} = \frac{3.00 \times 10^8 \times 3600}{1609.34} \frac{\text{miles}}{\text{hr}}$$

$$= \frac{1.08 \times 10^{12}}{1609.34} \approx 6.71 \times 10^8 \text{ mph}$$

**Problem 1.2:** Show that pressure (Pa) has dimensions of energy density (J/m³).

**Solution:**
- [Pa] = [N/m²] = [kg·m·s⁻²/m²] = kg·m⁻¹·s⁻²
- [J/m³] = [kg·m²·s⁻²/m³] = kg·m⁻¹·s⁻²

✓ They are the same. Pressure and energy density have the same dimensions.

**Problem 1.3 (Fermi):** Estimate the number of atoms in a human body.

**Solution (order of magnitude):**
- Human body mass: ~70 kg
- Body is mostly water + carbon compounds; average atomic mass ≈ 7–8 g/mol (water is 18 g/mol, carbon 12 g/mol; let's use ~7.5 g/mol as a rough average weighted by abundance)
- Moles of atoms: 70,000 g / 7.5 g/mol ≈ 9,300 mol
- Number of atoms: 9,300 × 6.022 × 10²³ ≈ **5.6 × 10²⁷ atoms**

---

## Conceptual Questions (Think Before Next Lecture)

1. Why do we define the meter via the speed of light rather than a physical rod? What advantages does this provide?

2. The equation F = mv²/r (centripetal force) — verify it is dimensionally correct. What would it mean if it weren't?

3. You measure the diameter of a coin as 24.3 mm. What is its area in cm²? How many sig figs should you report?

4. If you double all lengths in the universe, would the laws of physics change? What does your answer say about dimensional analysis?


---

## CS Connection — Units as a Type System

Dimensional analysis is type-checking. `L/T` and `L/T²` are different types, and adding them is a type error the universe rejects — exactly as a compiler rejects adding a `string` to an `int`. Some languages encode this directly (F#'s units of measure, Haskell's `dimensional`), catching a whole class of bug at compile time. The 1999 Mars Climate Orbiter was lost to precisely this error: pound-force-seconds passed where newton-seconds were expected. Significant figures are the same idea applied to precision — a float carries ~15 decimal digits, but that says nothing about how many are *meaningful*, which is why CS 101's discussion of floating-point precision is about representation while this is about measurement.

---

## Looking Ahead

**L02** puts these measured quantities somewhere: coordinate systems give each number a location and a direction, which is what turns a measurement into a physical description.

