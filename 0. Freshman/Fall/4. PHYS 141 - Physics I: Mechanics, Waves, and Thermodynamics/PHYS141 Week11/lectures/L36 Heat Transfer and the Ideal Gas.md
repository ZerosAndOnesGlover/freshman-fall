# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Lecture 36 — Heat Transfer and the Ideal Gas

---

## Where This Fits

Lecture 35 computed **how much** energy a temperature change requires. This lecture asks **how fast**
it moves, and then introduces the system Week 12 will need throughout: the **ideal gas**.

The gas matters because it is the one substance whose bulk behaviour follows exactly from its
microscopic mechanics. It is where thermodynamics and Newtonian mechanics meet.

---

## 1. Three Mechanisms

| Mechanism | Requires | Carried by |
|---|---|---|
| **Conduction** | Material contact | Molecular collisions, and free electrons in metals |
| **Convection** | A fluid that can move | Bulk transport of the fluid itself |
| **Radiation** | **Nothing** | Electromagnetic waves |

**Radiation is the one that works in vacuum** — which is how the Sun's energy reaches us, and why a
thermos flask has a silvered vacuum gap: the vacuum blocks the first two, the silvering the third.

---

## 2. Conduction

$$\boxed{P = \frac{kA\,\Delta T}{L}}$$

with $P$ in watts, $k$ the **thermal conductivity** in W·m⁻¹·K⁻¹, $A$ the cross-sectional area, and
$L$ the thickness.

| Material | $k$ (W·m⁻¹·K⁻¹) |
|---|---|
| Copper | 400 |
| Aluminium | 240 |
| Steel | 50 |
| Glass | 0.8 |
| Water | 0.6 |
| Wood | 0.15 |
| **Fibreglass insulation** | **0.04** |
| Air (still) | 0.026 |

**The range spans four orders of magnitude**, and that range is the whole basis of thermal design.

**Verified:** a wall of area 20 m² and thickness 0.10 m across a 20 K difference passes

- **160 W** if it is fibreglass insulation
- **1.6 MW** if it were copper — **ten thousand times** more

> **Metals conduct well because of free electrons**, not because their lattices are special. Electrons
> move far faster than lattice vibrations and carry energy with them. This is why thermal and
> electrical conductivity track each other so closely across the metals — the Wiedemann–Franz law —
> and why a metal doorknob feels colder than a wooden one at the same temperature. **It is not
> colder; it removes heat from your hand faster.**

**Still air is an excellent insulator.** Most practical insulators — fibreglass, wool, foam, double
glazing, a duvet — work by *trapping air* and preventing it from convecting. The solid material is
mostly there to hold the air still.

---

## 3. Convection

Heat a fluid from below and the warmed portion expands, becomes less dense, and rises; cooler fluid
sinks to replace it. The resulting circulation carries energy far faster than conduction through the
same fluid.

**Natural convection** is driven by these density differences alone. **Forced convection** uses a fan
or pump, and is far more effective — which is why a CPU heatsink has a fan and why wind chill exists.

Convection has no simple universal formula; engineering practice uses empirical correlations. **What
matters here is recognising when it dominates**, which in fluids is almost always.

---

## 4. Radiation

Every object radiates electromagnetic energy by virtue of its temperature:

$$\boxed{P = e\sigma A T^4} \qquad \sigma = 5.67\times10^{-8}~\text{W·m}^{-2}\text{K}^{-4}$$

with $e$ the **emissivity** ($0 \le e \le 1$; a perfect black body has $e=1$).

**The $T^4$ is the striking part.** Double the absolute temperature and the radiated power rises
**sixteenfold**. This is why radiation is negligible at room temperature and utterly dominant in a
furnace or a star.

An object also *absorbs* radiation from its surroundings at $T_s$, so the **net** rate is

$$P_{\text{net}} = e\sigma A\left(T^4 - T_s^4\right)$$

**Verified examples:**

| Object | $T$ | $e$ | $A$ | $P$ |
|---|---|---|---|---|
| Human skin | 310 K | 0.97 | 1.8 m² | 914 W emitted |
| Sun's surface | 5778 K | 1.0 | 1 m² | $6.3\times10^{7}$ W/m² |

**Net for a person in a 20°C room:** $e\sigma A(310^4 - 293^4) = \mathbf{185~\text{W}}$.

> That figure is worth pausing on. A resting adult produces roughly 100 W metabolically, and radiates
> a net 185 W in a cool room — which is precisely why you need clothing, and why a room full of people
> warms up noticeably.
>
> **Note that $T$ must be in kelvin, and to the fourth power.** Using Celsius here is not a small
> error; it is catastrophic.

---

## 5. The Ideal Gas Law

$$\boxed{PV = nRT} \qquad R = 8.314~\text{J·mol}^{-1}\text{K}^{-1}$$

or, per molecule, $PV = Nk_BT$ with $k_B = 1.381\times10^{-23}$ J/K.

**"Ideal" means** the molecules have negligible volume and no interactions except perfect elastic
collisions. Real gases approach this at low pressure and high temperature — well away from
condensation.

**Verified:** one mole at 0°C and 1 atm occupies $\mathbf{22.41~\text{L}}$; at 25°C, $24.46$ L.

### The special cases

| Held constant | Relation | Name |
|---|---|---|
| $T$ | $P_1V_1 = P_2V_2$ | Boyle's law |
| $P$ | $V_1/T_1 = V_2/T_2$ | Charles's law |
| $V$ | $P_1/T_1 = P_2/T_2$ | Gay-Lussac's law |

**Verified isothermal example:** compressing $0.010$ m³ at $2.0\times10^5$ Pa to $0.005$ m³ doubles
the pressure to $4.0\times10^5$ Pa; expanding to $0.020$ m³ halves it to $1.0\times10^5$ Pa.

> **Every $T$ here is absolute.** Charles's law with Celsius gives nonsense — it would predict zero
> volume at 0°C.

---

## 6. Kinetic Theory — Where the Gas Law Comes From

Treat the gas as elastic point particles bouncing off the walls. Computing the momentum they deliver
per second (Week 5's impulse) and dividing by area gives the pressure, and comparison with $PV=nRT$
yields

$$\boxed{\tfrac12 m\overline{v^2} = \tfrac32 k_BT}$$

> **Temperature *is* average translational kinetic energy per molecule.** This is the deepest result
> of the week. The bulk quantity introduced in Lecture 34 by an appeal to equilibrium turns out to be
> a direct measure of microscopic motion.

Two consequences:

- **Absolute zero** is where that motion is minimal — which is why the kelvin scale has a true zero
  while Celsius does not.
- At the same temperature, **all** gases have the same average molecular kinetic energy. Lighter
  molecules therefore move **faster**: $v_{\text{rms}} = \sqrt{3k_BT/m}$. This is why hydrogen and
  helium escape Earth's atmosphere while nitrogen and oxygen do not.

---

## 7. Summary

| | |
|---|---|
| Conduction | $P = kA\Delta T/L$; needs contact |
| Convection | Bulk fluid motion; no simple formula |
| Radiation | $P = e\sigma AT^4$; works in **vacuum** |
| $k$ range | copper 400 to insulation 0.04 — $10^4$ |
| Metals conduct via | **free electrons** |
| Insulators work by | trapping **still air** |
| $T^4$ | doubling $T$ gives $16\times$ the power |
| Net radiation | $e\sigma A(T^4-T_s^4)$; 185 W for a person at 20°C |
| Ideal gas | $PV = nRT$; molar volume 22.41 L at STP |
| Boyle / Charles / Gay-Lussac | $T$ / $P$ / $V$ held constant |
| **Kinetic theory** | $\tfrac12m\overline{v^2} = \tfrac32k_BT$ |
| Temperature **is** | average translational kinetic energy |

---

## 8. Conceptual Questions

1. Why does a metal railing feel colder than a wooden one at the same temperature?

2. Why is fibreglass insulation effective when the glass it is made from conducts 20 times better?

3. How does a vacuum flask block all three heat-transfer mechanisms?

4. Why must radiation calculations use kelvin, and what goes wrong with Celsius?

5. At the same temperature, do hydrogen and oxygen molecules have the same average speed? The same average kinetic energy?

---

## 9. Problems

1. A window of area 2.00 m² and thickness 4.00 mm has $k = 0.800$. Find the conduction rate for an inside temperature of 20.0°C and outside of 0°C.

2. Repeat Problem 1 for double glazing: two 4.00 mm panes separated by a 10.0 mm air gap ($k_{\text{air}} = 0.026$). Compare and comment.

3. A blackbody sphere of radius 0.100 m is at 500 K. Find its radiated power.

4. A person of surface area 1.70 m² and emissivity 0.97 at 33.0°C stands in a room at 18.0°C. Find the net radiated power.

5. A gas occupies 0.0500 m³ at $1.50\times10^5$ Pa and 300 K. Find the number of moles, then the pressure if it is compressed isothermally to 0.0200 m³.

6. A sealed rigid container of gas is heated from 20.0°C to 120°C. By what factor does the pressure rise?

7. Find the rms speed of a nitrogen molecule ($M = 0.0280$ kg/mol) at 300 K, and of a hydrogen molecule ($M = 0.00202$ kg/mol) at the same temperature.

---

*Next: Week 12 — Thermodynamics II: the Laws, Entropy, and Heat Engines*
