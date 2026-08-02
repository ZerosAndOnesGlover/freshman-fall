# PHYS 141 · Lab 12
## Heat Engines, the Gas Laws, and Thermal Efficiency

**Duration:** 3 hours | **Total: 100 points**

---

## Objectives

1. Verify Boyle's and Gay-Lussac's laws experimentally and extract absolute zero from the data
2. Measure the work done by a gas over a thermodynamic cycle from its $PV$ diagram
3. Determine the efficiency of a simple heat engine and compare it with the Carnot limit
4. Measure the coefficient of performance of a thermoelectric heat pump
5. Compute entropy changes and confirm $\Delta S_{\text{total}} > 0$ for a real irreversible process

---

## Apparatus

Gas law apparatus (sealed syringe or air column with pressure sensor), pressure sensor and
temperature probe with data logger, water baths at several temperatures, a low-friction
piston/syringe heat-engine kit with slotted masses, thermoelectric (Peltier) module with power
supply and ammeter, calorimeter, ice, balance.

---

## Part 1 — The Gas Laws and Absolute Zero (45 min, 25 pts)

**Procedure A — Boyle's law.** At constant room temperature, vary the volume of a sealed gas sample
and record the pressure at six volumes.

| $V$ (m³) | $P$ (Pa) | $PV$ (J) | $1/V$ (m⁻³) |
|---|---|---|---|
| | | | |

**Procedure B — Gay-Lussac's law.** Hold the volume fixed and immerse the sample in baths at roughly
0, 20, 40, 60 and 80 °C, recording the pressure once equilibrated.

| $T$ (°C) | $T$ (K) | $P$ (Pa) |
|---|---|---|
| | | |

**Analysis.**

1. Plot $P$ against $1/V$ for Procedure A. Confirm linearity through the origin and state what the
   slope represents. *(6 pts)*
2. Is $PV$ constant across your six rows? Report the mean and spread. *(4 pts)*
3. Plot $P$ against $T$ **in °C** for Procedure B. Extrapolate the line back to $P = 0$ and read off
   the intercept. *(8 pts)*
4. **Your intercept is an experimental determination of absolute zero.** Compare with $-273.15°$C
   and give a percent discrepancy. *(4 pts)*
5. Explain why this extrapolation works, and why no real gas actually reaches $P = 0$. *(3 pts)*

> **Part 1's question 3 is the most satisfying measurement in the course.** You are determining the
> location of absolute zero using a syringe, a pressure sensor, and a few buckets of water — and
> without ever going anywhere near it.

---

## Part 2 — Work from a $PV$ Cycle (45 min, 25 pts)

**Procedure.** Using the heat-engine kit, take the gas around a closed cycle: load the piston
(compress at roughly constant temperature), warm it in a hot bath (expand at roughly constant
pressure, lifting the load), unload, and cool it back. Log $P$ and $V$ continuously.

**Analysis.**

1. Plot the cycle on a $PV$ diagram. Identify each leg and label the process type. *(6 pts)*
2. Determine the **enclosed area** by counting squares or by numerical integration. This is the net
   work per cycle. *(8 pts)*
3. Independently compute the mechanical work done lifting the mass, $W = mgh$. *(5 pts)*
4. Compare (2) and (3). They should agree; account for any discrepancy. *(4 pts)*
5. Which direction did your cycle traverse, and what does that tell you about whether the device is
   an engine or a refrigerator? *(2 pts)*

---

## Part 3 — Engine Efficiency (30 min, 25 pts)

**Procedure.** For the same cycle, estimate the heat input $Q_h$ by monitoring the hot bath — either
from its temperature drop and known heat capacity, or from the electrical energy supplied to a heater.
Record the hot and cold reservoir temperatures.

| Quantity | Value |
|---|---|
| $W$ per cycle (from Part 2) | |
| $Q_h$ per cycle | |
| $T_h$ (K) | |
| $T_c$ (K) | |

**Analysis.**

1. Compute the measured efficiency $e = W/Q_h$. *(6 pts)*
2. Compute the Carnot limit $e_{\text{Carnot}} = 1 - T_c/T_h$. *(5 pts)*
3. Compute the ratio $e/e_{\text{Carnot}}$. **It must be less than 1** — if not, find your error. *(4 pts)*
4. List three specific irreversibilities in your apparatus and estimate which dominates. *(6 pts)*
5. Your $T_h$ and $T_c$ differ by only tens of kelvin. Compute the Carnot limit this implies and
   explain why practical engines run at the highest temperatures their materials permit. *(4 pts)*

> **Expect a very low efficiency** — often a few percent against a Carnot limit of perhaps 10–20%.
> That is the correct result, not a failure. Question 4 is where the marks are.

---

## Part 4 — Heat Pump COP and Entropy (30 min, 25 pts)

**Procedure A — COP.** Run a Peltier module with one face in a calorimeter of water. Record the
electrical power supplied ($VI$) and the rate of temperature rise of the water.

**Procedure B — Entropy.** Drop a known mass of ice at 0 °C into warm water and record initial and
final temperatures.

**Analysis.**

1. Compute the heat delivered per second from $mc\,\Delta T/\Delta t$, and hence
   $\text{COP} = Q_h/W$. *(6 pts)*
2. Compare with the Carnot limit $T_h/(T_h-T_c)$ for your measured temperatures. *(5 pts)*
3. For Procedure B, compute the entropy change of the **ice** (melting plus warming) and of the
   **water** (cooling). *(8 pts)*
4. Show that $\Delta S_{\text{total}} > 0$, and state what a negative total would have implied. *(6 pts)*

> **Question 3 requires care with the warming terms.** Melting ice at a constant 273 K gives
> $\Delta S = mL_f/273$, but warming it afterwards from 273 K to $T_f$ requires
> $\Delta S = mc\ln(T_f/273)$ — a logarithm, because the temperature changes as the heat flows.

---

## Lab Report Requirements

| Component | Points |
|-----------|--------|
| Part 1: both gas-law plots, absolute zero extrapolated and compared | 25 |
| Part 2: $PV$ cycle plotted, enclosed area found, cross-checked against $mgh$ | 25 |
| Part 3: efficiency measured, compared with Carnot, irreversibilities identified | 25 |
| Part 4: COP measured, entropy changes computed, $\Delta S_{\text{total}} > 0$ shown | 25 |
| **Total** | **100** |

---

## Pre-Lab Questions (Due at Start of Lab)

**Q1.** A gas at $1.00\times10^5$ Pa occupies 50.0 mL. If compressed isothermally to 20.0 mL, what is
the new pressure?

**Q2.** A sealed rigid container of gas is at $1.00\times10^5$ Pa and $20°$C. Find its pressure at
$80°$C. Then compute what you would get by wrongly using Celsius, and state the factor by which that
answer is wrong. *(Note what happens to the Celsius calculation if the starting temperature had been
$0°$C instead — this is why the scale matters, not merely the arithmetic.)*

**Q3.** A heat engine operates between $80°$C and $20°$C. Compute the Carnot efficiency, and comment
on what it implies for a low-temperature engine.

**Q4.** 0.100 kg of ice at $0°$C melts and then warms to $10.0°$C. Compute the entropy change for
each stage separately, and explain why the second requires a logarithm.
