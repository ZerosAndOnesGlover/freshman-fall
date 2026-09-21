# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Lecture 34 — Temperature, the Zeroth Law, and Thermal Expansion

**Date:** Monday 7 December 2026 · 14:00–14:50 · Week 11

---

## Where This Fits

Weeks 0–10 tracked individual objects: a block on a ramp, a mass on a spring, a molecule of air
carrying a sound wave. Thermodynamics does something different. It describes systems containing
$10^{23}$ particles by ignoring almost everything about them and keeping a handful of **bulk
quantities** — temperature, pressure, volume, internal energy.

That this works at all is remarkable. You cannot track $10^{23}$ trajectories, and you do not need to:
the averages behave predictably even though the individuals do not.

**Temperature is the first of those bulk quantities**, and this lecture establishes what it actually
measures.

---

## 1. Temperature and the Zeroth Law

Everyday language treats temperature as "how hot something is". That is circular. The physical
definition rests on **thermal equilibrium**.

Two objects placed in contact eventually stop changing — no more net energy flows between them. They
are then in **thermal equilibrium**.

> **Zeroth Law of Thermodynamics.** If A is in thermal equilibrium with C, and B is in thermal
> equilibrium with C, then A is in thermal equilibrium with B.

This sounds like a triviality. It is not — it is the statement that makes `thermometry` possible.

**Why:** it says "being in equilibrium with" is a **transitive** relation, so all objects in mutual
equilibrium share some common property. We name that property **temperature**, and a thermometer is
simply the object C that we carry from A to B.

*(In Week 6 of MATH 151 you met equivalence relations. Thermal equilibrium is one, and its equivalence
classes are precisely the sets of objects at the same temperature. The Zeroth Law is the transitivity
axiom.)*

**It is called "zeroth" because it was `recognised` as logically prior to the first and second laws only
after those had been named.**

---

## 2. Temperature Scales

| Scale | Water freezes | Water boils | Absolute zero |
|---|---|---|---|
| Celsius | $0°$C | $100°$C | $-273.15°$C |
| Fahrenheit | $32°$F | $212°$F | $-459.67°$F |
| **Kelvin** | $273.15$ K | $373.15$ K | **0 K** |

$$T_K = T_C + 273.15 \qquad T_F = \tfrac95 T_C + 32$$

**Verified:**

| $T_C$ | $T_F$ | $T_K$ |
|---|---|---|
| $-273.15$ | $-459.67$ | $0.00$ |
| $-40$ | $\mathbf{-40}$ | $233.15$ |
| $0$ | $32$ | $273.15$ |
| $37$ | $98.60$ | $310.15$ |
| $100$ | $212$ | $373.15$ |

*The scales coincide at exactly $-40°$ — a useful check on the conversion.*

> **Always use kelvin in physics.** Celsius has an arbitrary zero, so ratios of Celsius temperatures
> are meaningless: $20°$C is not "twice as hot" as $10°$C. Every gas law, every efficiency formula,
> and every radiation calculation requires absolute temperature. **Using Celsius in $PV=nRT$ is the
> single most common error in this half of the course.**

**Absolute zero is not "no motion" but the state of minimum possible energy.** It is unattainable, a
fact that turns out to be the Third Law of Thermodynamics.

---

## 3. Linear Thermal Expansion

Heat a solid and its atoms vibrate more vigorously about their lattice sites. Because the interatomic
potential is **asymmetric** — steeply repulsive at short range, gently attractive at long range — the
average separation increases. The material expands.

$$\boxed{\Delta L = \alpha L_0 \Delta T}$$

where $\alpha$ is the **coefficient of linear expansion**, in K⁻¹.

| Material | $\alpha$ (K⁻¹) | 1 m rod over 100 K |
|---|---|---|
| Aluminium | $2.4\times10^{-5}$ | 2.40 mm |
| Copper | $1.7\times10^{-5}$ | 1.70 mm |
| Steel | $1.2\times10^{-5}$ | 1.20 mm |
| Glass | $9\times10^{-6}$ | 0.90 mm |
| **Invar** | $1.2\times10^{-6}$ | **0.12 mm** |

*All verified.* **Invar** is a nickel–iron alloy engineered for near-zero expansion, and is used in
precision instruments and clock pendulums for exactly that reason.

### Why bridges have expansion joints

A 1.00 km steel bridge over a 40 K seasonal range:

$$\Delta L = (1.2\times10^{-5})(1000)(40) = \mathbf{0.48~\text{m}}$$

**Nearly half a metre.** Without joints the structure would either buckle or tear itself apart. The
same reasoning explains the gaps in railway track and the loops in overhead power lines.

---

## 4. Area and Volume Expansion

$$\Delta A = 2\alpha A_0\Delta T \qquad \Delta V = \beta V_0 \Delta T, \qquad \boxed{\beta = 3\alpha}$$

**Why $3\alpha$:** a cube of side $L$ has volume $L^3$. If each side grows by a factor $(1+\alpha\Delta T)$,

$$V = L^3(1+\alpha\Delta T)^3 \approx L^3\left(1 + 3\alpha\Delta T\right)$$

dropping terms in $\alpha^2$ and $\alpha^3$, which are utterly negligible since $\alpha \sim 10^{-5}$.

**For steel:** $\beta = 3.6\times10^{-5}$ K⁻¹ (verified).

### The hole question

> **A metal plate with a hole in it is heated. Does the hole get bigger or smaller?**

**Bigger.** Everyone's first instinct is that the surrounding metal expands inward and closes the gap.
It does not.

The clean argument: imagine the hole filled with a disc of the *same* material. On heating, everything
expands uniformly and the disc still fits exactly — so the hole must have expanded by exactly as much
as the disc did. Removing the disc changes nothing about how the rest of the plate behaves.

**Every dimension scales up together, including empty ones.** This is why a stuck metal jar lid loosens
under hot water, and how shrink-fitting works: cool a shaft, warm a collar, assemble, let them
equalise.

---

## 5. The Anomalous Expansion of Water

Almost everything expands on heating. Water does so only above **4°C**. Between 0°C and 4°C it
**contracts** as it warms.

Consequently water is **densest at 4°C**, and ice — being less dense still — floats.

> **This is why lakes freeze from the top down.** As a lake cools, the coldest water sinks until the
> whole body reaches 4°C. Below that, further-cooled water is *less* dense and stays on top, freezes
> there, and the ice insulates what lies beneath. Fish survive the winter under the ice.
>
> **Had water behaved normally, lakes would freeze solid from the bottom up** and aquatic life in
> temperate zones would be impossible. It is not an exaggeration to say the anomaly is a precondition
> for the biosphere as it exists.

---

## 6. Summary

| | |
|---|---|
| Thermal equilibrium | No net energy flow between objects in contact |
| **Zeroth Law** | Equilibrium is transitive ⟹ temperature exists and thermometers work |
| Kelvin | $T_K = T_C + 273.15$; **always use it in formulas** |
| C and F coincide | at $-40°$ |
| Linear expansion | $\Delta L = \alpha L_0\Delta T$ |
| Volume expansion | $\beta = 3\alpha$ |
| Steel bridge, 1 km, 40 K | expands **0.48 m** |
| A hole in a heated plate | gets **bigger** |
| Water | densest at **4°C**; ice floats; lakes freeze top-down |

---

## 7. Conceptual Questions

1. Why is the Zeroth Law necessary before a thermometer can mean anything?

2. Why must kelvin be used in gas-law calculations, when Celsius works perfectly well for expansion?

3. A brass ring is too tight to fit over a steel rod. Should you heat the ring, cool the rod, or either?

4. A bimetallic strip of brass bonded to steel is heated. Which way does it bend, and why?

5. Why does the anomalous expansion of water matter for life on Earth?

---

## 8. Problems

1. Convert $-15°$C to Fahrenheit and to kelvin. Convert $98.6°$F to Celsius.

2. A steel railway rail is 25.0 m long at $10°$C. Find its length at $45°$C.

3. An aluminium rod is 2.000 m at $20°$C. At what temperature is it 2.005 m?

4. A steel bridge is 1.20 km long. Find the total expansion over a temperature range of $-10°$C to $40°$C.

5. A glass container holds exactly 500 mL at $20°$C. Find its capacity at $80°$C, taking $\alpha_{\text{glass}} = 9.0\times10^{-6}$ K⁻¹.

6. A steel ring of inner diameter 4.000 cm must fit over a shaft of diameter 4.010 cm. To what temperature must the ring be heated, starting from $20°$C?

---

*Next: Lecture 35 — Heat, Specific Heat Capacity, and Calorimetry*
