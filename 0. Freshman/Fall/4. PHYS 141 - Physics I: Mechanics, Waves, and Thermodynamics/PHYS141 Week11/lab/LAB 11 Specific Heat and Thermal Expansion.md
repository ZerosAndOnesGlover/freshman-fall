# PHYS 141 · Lab 11
## Specific Heat Capacity, Latent Heat, and Thermal Expansion

**Duration:** 3 hours | **Total: 100 points**

---

## Objectives

1. Measure the specific heat capacity of a metal by calorimetry
2. Measure the latent heat of fusion of ice
3. Measure the linear expansion coefficient of a metal rod
4. Record a cooling curve and identify the phase-change plateau
5. Quantify heat loss to the surroundings and correct for it

---

## Apparatus

Calorimeter with stirrer and lid, digital thermometer or temperature probe with logger, metal samples
(aluminium, copper, lead) of known mass, kettle or hot plate, ice, balance, expansion apparatus
(metal rod, steam generator, dial gauge or micrometer), stopwatch.

---

## Part 1 — Specific Heat of a Metal (45 min, 30 pts)

**Procedure.**

1. Weigh the empty calorimeter, then with water; record $m_{\text{cal}}$ and $m_w$.
2. Record the initial water temperature $T_w$.
3. Heat the metal sample in boiling water for at least 5 minutes so it reaches $100°$C. Record its
   mass $m_s$.
4. Transfer it **quickly** to the calorimeter, stir, and record the maximum temperature reached $T_f$.
5. Repeat for all three metals.

| Metal | $m_s$ (kg) | $m_w$ (kg) | $T_s$ (°C) | $T_w$ (°C) | $T_f$ (°C) | $c$ (J·kg⁻¹K⁻¹) |
|---|---|---|---|---|---|---|
| Aluminium | | | 100 | | | |
| Copper | | | 100 | | | |
| Lead | | | 100 | | | |

**Analysis.**

1. Derive the working equation, **including the calorimeter's own heat capacity**: *(6 pts)*
   $$m_sc_s(T_s-T_f) = \left(m_wc_w + m_{\text{cal}}c_{\text{cal}}\right)(T_f-T_w)$$
2. Compute $c$ for each metal. *(9 pts)*
3. Compare with accepted values (Al 900, Cu 387, Pb 128 J·kg⁻¹K⁻¹) and give percent discrepancies. *(6 pts)*
4. Which metal gave the **largest** temperature rise in the water, and why? *(4 pts)*
5. Estimate your uncertainty in $c$ and identify the dominant contribution. *(5 pts)*

> **The transfer is the critical step.** Every second the hot sample spends in air is energy lost
> before it reaches the water, which makes the measured $c$ come out **low**. Move fast, and note in
> your report whether you think this biased your result.

---

## Part 2 — Latent Heat of Fusion (35 min, 25 pts)

**Procedure.** Add ice at $0°$C — dried on paper first — to warm water in the calorimeter. Record
masses and temperatures before and after, waiting until all the ice has melted.

| Quantity | Value |
|---|---|
| Mass of water $m_w$ | |
| Initial water temperature $T_i$ | |
| Mass of ice $m_{\text{ice}}$ | |
| Final temperature $T_f$ | |

**Analysis.**

1. Write the energy balance and solve for $L_f$: *(6 pts)*
   $$m_{\text{ice}}L_f + m_{\text{ice}}c_w(T_f-0) = \left(m_wc_w + m_{\text{cal}}c_{\text{cal}}\right)(T_i-T_f)$$
2. Compute $L_f$ and compare with the accepted $3.34\times10^5$ J/kg. *(8 pts)*
3. **Why must the ice be dried before weighing?** Estimate the error introduced by 2 g of adhering
   water. *(6 pts)*
4. Confirm that all the ice melted. What would you have observed otherwise, and how would the
   analysis change? *(5 pts)*

---

## Part 3 — Linear Expansion (35 min, 25 pts)

**Procedure.** Measure the rod's length $L_0$ at room temperature. Mount it in the expansion
apparatus with the dial gauge reading zero. Pass steam through and record the extension once the
reading stabilises.

| Rod | $L_0$ (m) | $T_0$ (°C) | $T_1$ (°C) | $\Delta L$ (m) | $\alpha$ (K⁻¹) |
|---|---|---|---|---|---|
| | | | | | |

**Analysis.**

1. Compute $\alpha = \Delta L/(L_0\Delta T)$. *(6 pts)*
2. Compare with the accepted value for your material and identify the metal if it is unlabelled. *(6 pts)*
3. $\Delta L$ is typically under a millimetre. Estimate the fractional uncertainty and explain why a
   **long** rod and a **large** $\Delta T$ both improve the measurement. *(7 pts)*
4. The rod's ends are held by the apparatus, which is itself at room temperature. Does this make your
   $\alpha$ too large or too small? Justify. *(6 pts)*

---

## Part 4 — Cooling Curve (25 min, 20 pts)

**Procedure.** Heat a sample of a low-melting-point substance (stearic acid, or water if only the
freezing plateau is wanted) above its melting point. Remove the heat source and log the temperature
every 15 s until well below the melting point.

**Analysis.**

1. Plot temperature against time. *(6 pts)*
2. **Identify the plateau** and read off the melting point. *(5 pts)*
3. Explain why the temperature stays constant while energy is still leaving the sample. *(5 pts)*
4. The plateau is usually not perfectly flat, and the curve is steeper at higher temperatures.
   Explain both observations. *(4 pts)*

> *For question 4:* Newton's law of cooling says the rate of heat loss is proportional to the
> temperature difference from the surroundings — so a hotter sample cools faster.

---

## Lab Report Requirements

| Component | Points |
|-----------|--------|
| Part 1: three specific heats with calorimeter correction, compared with accepted values | 30 |
| Part 2: $L_f$ determined, drying explained, complete-melting confirmed | 25 |
| Part 3: $\alpha$ determined with uncertainty analysis and systematic discussion | 25 |
| Part 4: cooling curve with plateau identified and explained | 20 |
| **Total** | **100** |

---

## Pre-Lab Questions (Due at Start of Lab)

**Q1.** A 0.200 kg aluminium sample at $100°$C is dropped into 0.300 kg of water at $18.0°$C.
Predict the final temperature, **ignoring** the calorimeter.

**Q2.** Repeat Q1 including a calorimeter of water equivalent 0.020 kg. Does the predicted $T_f$ rise
or fall, and why?

**Q3.** Why is it essential to dry the ice before weighing it in Part 2? Which way would wet ice bias
your $L_f$?

**Q4.** A 1.00 m steel rod ($\alpha = 1.2\times10^{-5}$ K⁻¹) is heated from $20°$C to $100°$C.
Compute $\Delta L$. If your dial gauge reads to $\pm0.01$ mm, what is the fractional uncertainty?
