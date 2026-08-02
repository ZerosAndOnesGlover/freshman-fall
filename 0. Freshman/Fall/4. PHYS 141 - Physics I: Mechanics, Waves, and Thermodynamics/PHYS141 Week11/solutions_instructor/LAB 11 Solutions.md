# PHYS 141 · Lab 11 Solutions
## Specific Heat Capacity, Latent Heat, and Thermal Expansion
## INSTRUCTOR ONLY

---

## Pre-Lab Answers

**Q1.** Ignoring the calorimeter:
$$T_f = \frac{(0.200)(900)(100)+(0.300)(4186)(18.0)}{(0.200)(900)+(0.300)(4186)} = \mathbf{28.3°\text{C}}$$

**Q2.** With a calorimeter of water equivalent 0.020 kg, the effective water mass becomes 0.320 kg:
$$T_f = \mathbf{27.7°\text{C}}$$
**Lower**, because there is more material to warm for the same energy released by the sample.

**Q3.** Adhering water is at $0°$C but is **already liquid**, so it absorbs no latent heat. Counting it
as ice makes $m_{\text{ice}}$ too large, and since $L_f = Q/m_{\text{ice}}$, the computed $L_f$ comes
out **too small**. For 2 g of water on 80 g of ice, that is a 2.5% underestimate.

**Q4.** $\Delta L = (1.2\times10^{-5})(1.00)(80) = \mathbf{0.960~\text{mm}}$. With a gauge resolution
of $\pm0.01$ mm the fractional uncertainty is $0.01/0.960 = \mathbf{1.04\%}$.

---

## Part 1 — Specific Heat of a Metal *(30 pts)*

**Working equation** *(6 pts)*:
$$m_sc_s(T_s - T_f) = \left(m_wc_w + m_{\text{cal}}c_{\text{cal}}\right)(T_f - T_w)$$
$$c_s = \frac{\left(m_wc_w + m_{\text{cal}}c_{\text{cal}}\right)(T_f-T_w)}{m_s(T_s-T_f)}$$

**Accepted values** for comparison: Al **900**, Cu **387**, Pb **128** J·kg⁻¹K⁻¹. *(9 + 6 pts)*

**4. Which metal warms the water most?** *(4 pts)*
**Aluminium**, because its specific heat is the largest — for equal masses at equal starting
temperature it carries the most energy. With $m_s = 0.200$ kg into 0.300 kg of water at 18°C, typical
final temperatures are roughly:

| Metal | $mc$ (J/K) | $T_f$ (°C) |
|---|---|---|
| Aluminium | 180 | ≈28.3 |
| Copper | 77 | ≈22.8 |
| Lead | 26 | ≈19.6 |

**Lead barely moves the water at all** — a good illustration for the class.

**5. Dominant uncertainty** *(5 pts)*: the temperature rise $T_f - T_w$ is small (a few kelvin) and is
the difference of two measured values, so its fractional uncertainty is the largest in the
calculation. **For lead it is dominant to the point of making the measurement nearly useless** —
which is itself worth discussing.

> **Expect all three results to come out LOW.** Heat lost during the transfer from boiling water to
> the calorimeter reduces $T_f$, and the equation attributes that to a smaller $c_s$. A student
> reporting 850 rather than 900 for aluminium has done the experiment correctly; one reporting 950
> should check their arithmetic.

---

## Part 2 — Latent Heat of Fusion *(25 pts)*

**Working equation** *(6 pts)*:
$$m_{\text{ice}}L_f + m_{\text{ice}}c_w(T_f-0) = \left(m_wc_w+m_{\text{cal}}c_{\text{cal}}\right)(T_i-T_f)$$

**Note the second term on the left** — the melted ice, now at 0°C, must itself be warmed to $T_f$.
Omitting it is the commonest analytical error and inflates $L_f$.

**2.** Accepted $L_f = 3.34\times10^5$ J/kg; student values of $3.0$–$3.6\times10^5$ are typical. *(8 pts)*

**3. Why dry the ice** *(6 pts)*: see Pre-Lab Q3. Wet ice biases $L_f$ **low**, by roughly the ratio of
adhering water to ice mass.

**4. Confirming complete melting** *(5 pts)*: if $T_f > 0°$C and no ice is visible, all of it melted.
Had ice remained, $T_f$ would have been exactly $0°$C and the equation would instead determine **how
much** ice melted rather than $L_f$ — you would have one equation and a different unknown.

---

## Part 3 — Linear Expansion *(25 pts)*

**1.** $\alpha = \Delta L/(L_0\Delta T)$. *(6 pts)*

**2.** Typical rods: steel $1.2\times10^{-5}$, copper $1.7\times10^{-5}$, aluminium
$2.4\times10^{-5}$ K⁻¹. These are far enough apart to identify an unlabelled rod confidently. *(6 pts)*

**3. Why long rods and large $\Delta T$ help** *(7 pts)*: $\Delta L$ is typically under a millimetre,
so the gauge resolution ($\pm0.01$ mm) is a percent-level fractional uncertainty. Since
$\Delta L \propto L_0\Delta T$, increasing either makes the measured quantity larger while the
*absolute* gauge uncertainty stays fixed — so the fractional uncertainty falls. **This is the same
principle as timing 20 oscillations in Lab 8.**

**4. Systematic bias** *(6 pts)*: the ends are clamped in apparatus that stays near room temperature,
so the rod is **not uniformly heated** — the sections near the mounts are cooler than the steam
temperature. The effective $\Delta T$ is therefore **less** than assumed, which makes the measured
$\Delta L$ smaller than it should be for the assumed $\Delta T$, and the computed $\alpha$ comes out
**too small**.

*Full marks require the direction of the bias, not merely noting that the ends are cooler.*

---

## Part 4 — Cooling Curve *(20 pts)*

1. Temperature against time: a falling curve with a distinct flat section. *(6 pts)*
2. The **plateau** occurs at the freezing point — read it off directly. *(5 pts)*
3. **Why the temperature holds constant** *(5 pts)*: during solidification the energy leaving the
   sample comes from the latent heat released as bonds form, not from a reduction in molecular kinetic
   energy. Energy flows out, but the temperature — which measures kinetic energy — does not change
   until the phase transition is complete.
4. **Two observations** *(4 pts)*:
   - The plateau **slopes slightly** because real samples are not pure and freeze over a small range,
     and because the thermometer has its own thermal lag.
   - The curve is **steeper at higher temperature** because Newton's law of cooling makes the loss
     rate proportional to $(T - T_{\text{room}})$, which is greatest at the start.

---

## Lab Report Marking Summary

| Component | Points | Watch for |
|-----------|--------|-----------|
| Part 1 | 30 | Calorimeter term included; results expected LOW; lead's poor precision noted |
| Part 2 | 25 | The $m_{\text{ice}}c_w T_f$ term present; drying explained with a direction |
| Part 3 | 25 | Bias direction identified; uncertainty argument connected to Lab 8 |
| Part 4 | 20 | Plateau explained via latent heat, not "the heater turned off" |
| **Total** | **100** | |

**Common errors to look for:**

1. **Omitting the calorimeter's heat capacity** — biases every $c_s$ low by a few percent.
2. **Forgetting to warm the melted ice** in Part 2's energy balance.
3. **Using the sample's mass in grams** with SI specific heats — a factor of 1000.
4. **Assuming the rod reaches steam temperature along its whole length** without comment.
5. **Explaining the cooling-curve plateau as "the heat source was removed"** — the heat source was
   removed for the *whole* curve; the plateau needs latent heat.
