# PHYS 141 — Lab 12 Solutions
## Heat Engines, the Gas Laws, and Thermal Efficiency
## INSTRUCTOR ONLY

---

## Pre-Lab Answers

**Q1.** Boyle: $P_2 = P_1V_1/V_2 = (1.00\times10^5)(50.0)/(20.0) = \mathbf{2.50\times10^5~\text{Pa}}$.

**Q2.** Correctly, in kelvin: $P_2 = (1.00\times10^5)(353.15/293.15) = \mathbf{1.20\times10^5~\text{Pa}}$
— a 20% rise.

Using Celsius: $(1.00\times10^5)(80/20) = 4.00\times10^5$ Pa — **wrong by a factor of 3.32**.

*Had the initial temperature been $0°$C, the Celsius calculation would require dividing by zero and
predict infinite pressure. **The absurdity is the point:** Celsius has an arbitrary zero, so ratios of
Celsius temperatures carry no physical meaning at all.*

**Q3.** $e = 1 - 293.15/353.15 = \mathbf{0.170} = 17.0\%$.

Even a *perfect* engine across a 60 K difference wastes 83% of its heat input. Low-temperature engines
are intrinsically poor, which is why waste-heat recovery is difficult and why power stations chase
high $T_h$.

**Q4.** Melting: $\Delta S = mL_f/T = (0.100)(3.34\times10^5)/273.15 = \mathbf{+122~\text{J/K}}$.
Warming $0\to10°$C: $\Delta S = mc\ln(T_2/T_1) = (0.100)(4186)\ln(283.15/273.15) = \mathbf{+15.1~\text{J/K}}$.

**The logarithm is needed because the temperature changes as heat flows.** $Q/T$ is valid only at
constant $T$ — true during melting, false during warming. Total: $+137$ J/K.

---

## Part 1 — The Gas Laws and Absolute Zero *(25 pts)*

1. $P$ against $1/V$: straight line through the origin, **slope $= nRT$**. *(6 pts)*
2. $PV$ constant to within a few percent; systematic drift usually indicates a temperature change
   during the run or a leaking seal. *(4 pts)*
3. $P$ against $T$(°C): straight line, extrapolated back to $P = 0$. *(8 pts)*
4. **The intercept should land near $-273°$C.** Student values of $-250$ to $-290$°C are common; a
   discrepancy under 10% is a good result with school apparatus. *(4 pts)*
5. The extrapolation works because $P \propto T$ in kelvin, so $P = 0$ corresponds to $T = 0$ K.
   **No real gas reaches it** — every gas liquefies first, and the ideal-gas law fails well before
   then. The extrapolation is valid precisely because it is an *extrapolation*: it locates where the
   idealised line would reach zero without ever going there. *(3 pts)*

> **This is the measurement worth dwelling on in the debrief.** A syringe, a pressure sensor, and
> four buckets of water locate absolute zero to within a few percent, without approaching it. Point
> out that this is exactly how it was first determined.

---

## Part 2 — Work from a $PV$ Cycle *(25 pts)*

1. Cycle plotted with legs labelled — typically near-isothermal compression, near-isobaric expansion,
   and two transitions. *(6 pts)*
2. Enclosed area by square-counting or numerical integration. Typical classroom kits give **0.1–1 J
   per cycle** — small, and students should not be alarmed. *(8 pts)*
3. $W = mgh$ from the lifted mass. *(5 pts)*
4. **Expect (2) to exceed (3)**, because not all the gas's work reaches the load — friction in the
   piston, and work done pushing back the atmosphere, consume part of it. Agreement within 20–30% is
   realistic. *(4 pts)*
5. **Clockwise** for an engine — the device produces net work and lifts the mass. *(2 pts)*

---

## Part 3 — Engine Efficiency *(25 pts)*

1. $e = W/Q_h$ from the measured values. *(6 pts)*
2. $e_{\text{Carnot}} = 1 - T_c/T_h$ in kelvin. *(5 pts)*
3. **$e/e_{\text{Carnot}}$ must be less than 1.** A ratio above 1 means either $Q_h$ was
   underestimated (very common — heat leaks into the apparatus are not counted) or $W$ was
   overestimated. *(4 pts)*
4. **Three irreversibilities**, with the dominant one identified: *(6 pts)*
   - **Piston friction** — usually the largest in a classroom kit
   - **Finite-rate heat transfer** — the gas never truly equilibrates with the baths
   - **Heat leakage** to the surroundings through the cylinder walls and tubing
   - *(Also acceptable: turbulence during rapid expansion; non-quasi-static compression.)*
5. With $T_h$ and $T_c$ differing by only tens of kelvin, the Carnot limit is often only 10–20%. **A
   real engine achieving 2–5% of $Q_h$ is therefore performing at a respectable fraction of its
   theoretical maximum**, which students consistently fail to appreciate until they compute the
   ratio. This is why practical engines run as hot as their materials allow. *(4 pts)*

> **Do not let students record a low efficiency as a failed experiment.** The efficiency *should* be
> low; question 4 is where the understanding is demonstrated and where the marks are.

---

## Part 4 — Heat Pump COP and Entropy *(25 pts)*

1. $Q_h/\Delta t = mc\,\Delta T/\Delta t$; electrical input $W/\Delta t = VI$; hence
   $\text{COP} = Q_h/W$. Typical Peltier modules give **COP around 0.5–1.5** — poor, because Peltier
   devices are intrinsically inefficient compared with vapour-compression systems. *(6 pts)*
2. The Carnot limit $T_h/(T_h-T_c)$ will be far higher, often 10 or more. **The large gap is the
   result**, and it should be discussed rather than explained away. *(5 pts)*
3. **Entropy for Procedure B** *(8 pts)*:
   - Ice melting: $\Delta S = m_{\text{ice}}L_f/273.15$
   - Melted ice warming to $T_f$: $\Delta S = m_{\text{ice}}c_w\ln(T_f/273.15)$
   - Water cooling from $T_i$ to $T_f$: $\Delta S = m_wc_w\ln(T_f/T_i)$, which is **negative**
4. **The total must be positive.** *(6 pts)*

   A **negative** total would mean the process could not occur spontaneously — so obtaining one
   indicates an arithmetic error, most often forgetting the logarithm and using $Q/T$ for the
   cooling water.

> **Question 3's middle term is the discriminator.** Students routinely compute the melting entropy
> and the water's cooling entropy but forget that the melted ice must then be warmed from 0 °C to
> $T_f$. Its omission does not usually flip the sign, so it passes unnoticed unless checked.

---

## Lab Report Marking Summary

| Component | Points | Watch for |
|-----------|--------|-----------|
| Part 1 | 25 | Absolute zero extrapolated; explanation of why no gas reaches it |
| Part 2 | 25 | Enclosed area cross-checked against $mgh$; discrepancy explained |
| Part 3 | 25 | $e/e_{\text{Carnot}} < 1$; irreversibilities named and ranked |
| Part 4 | 25 | All **three** entropy terms present; total shown positive |
| **Total** | **100** | |

**Common errors to look for:**

1. **Using Celsius** anywhere in Part 1's extrapolation logic, Part 3's Carnot limit, or Part 4's
   entropy. This is the single most consequential error of the week.
2. **Reporting $e > e_{\text{Carnot}}$** without recognising it as impossible. Treat it as a prompt to
   re-examine $Q_h$, not as a discovery.
3. **Omitting the warming term** in the entropy calculation of Part 4.
4. **Using $Q/T$ where $T$ varies.** Valid for melting; invalid for the cooling water.
5. **Treating a low measured efficiency as experimental failure.** It is the expected result, and the
   analysis of *why* is what is being assessed.
