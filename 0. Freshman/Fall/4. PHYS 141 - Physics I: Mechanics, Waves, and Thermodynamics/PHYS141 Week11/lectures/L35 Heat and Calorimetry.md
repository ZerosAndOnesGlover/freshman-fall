# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Lecture 35 — Heat, Specific Heat Capacity, and Calorimetry

---

## Where This Fits

Lecture 34 established what temperature *is*. This lecture is about what **changes** it.

The key distinction — and the one students most often blur — is between **heat** and **temperature**.
They are not the same quantity, not measured in the same units, and not even the same kind of thing.

---

## 1. Heat Is Energy in Transit

> **Heat $Q$ is energy transferred between systems because of a temperature difference.**

Three consequences follow immediately, and all three are commonly got wrong:

1. **Heat is measured in joules.** It is energy, and shares its unit with work and kinetic energy.
2. **An object does not "contain heat".** It contains **internal energy**. Heat is energy *crossing a
   boundary*, in the same way that work is. Once it has arrived it is no longer heat — it is internal
   energy. Saying "this cup contains a lot of heat" is like saying "this bank account contains a lot
   of transfer".
3. **Heat flows from hot to cold, never spontaneously the reverse.** That asymmetry is the Second Law,
   which Week 12 develops.

**Work and heat are the two ways to change a system's internal energy**, and Week 12's First Law
combines them.

---

## 2. Specific Heat Capacity

$$\boxed{Q = mc\,\Delta T}$$

where $c$ is the **specific heat capacity** in J·kg⁻¹·K⁻¹ — the energy needed to raise one kilogram
by one kelvin.

| Substance | $c$ (J·kg⁻¹·K⁻¹) |
|---|---|
| **Water** | **4186** |
| Ice | 2090 |
| Steam | 2010 |
| Aluminium | 900 |
| Copper | 387 |
| Lead | 128 |

### Water's specific heat is extraordinary

At 4186 J·kg⁻¹·K⁻¹, water takes **4.7 times** more energy per kilogram than aluminium and **32 times**
more than lead to warm by the same amount. It is among the highest of any common substance.

**Verified:** heating 0.500 kg by 30 K takes **62.8 kJ** for water but only **13.5 kJ** for aluminium.

> **This single number shapes the planet.** Oceans absorb enormous energy for small temperature change,
> which is why coastal climates are mild and continental interiors extreme; why the sea is still cold
> in June and still warm in October; and why water is the working fluid in almost every cooling system
> ever built — from car radiators to nuclear reactors to the blood in your body.

---

## 3. Latent Heat — Change of Phase

Heat a block of ice and its temperature rises steadily — until it reaches 0°C. Then the temperature
**stops changing** while heat keeps flowing in. All of it goes into breaking the bonds of the solid
lattice, not into faster molecular motion.

$$\boxed{Q = mL}$$

| Transition | Symbol | Water value |
|---|---|---|
| Solid ⇄ liquid | $L_f$ (fusion) | $3.34\times10^5$ J/kg |
| Liquid ⇄ gas | $L_v$ (vaporisation) | $2.26\times10^6$ J/kg |

**Note the ratio: $L_v/L_f = \mathbf{6.77}$.** Boiling water takes nearly seven times the energy of
melting the same mass of ice — because vaporising must separate the molecules entirely, not merely
loosen them.

### The complete heating curve — verified

Taking 0.100 kg from $-20°$C ice to $120°$C steam:

| Stage | Formula | Energy (J) |
|---|---|---|
| Warm ice, $-20\to0$ | $mc_{\text{ice}}\Delta T$ | 4,180 |
| **Melt at 0°C** | $mL_f$ | **33,400** |
| Warm water, $0\to100$ | $mc_w\Delta T$ | 41,860 |
| **Boil at 100°C** | $mL_v$ | **226,000** |
| Warm steam, $100\to120$ | $mc_{\text{steam}}\Delta T$ | 4,020 |
| | **Total** | **309,460** |

**Boiling alone accounts for 73% of the total.** The two flat sections of the heating curve dominate
it entirely.

> **This is why steam burns are so much worse than hot-water burns.** Steam at 100°C condensing on
> your skin releases $2.26\times10^6$ J/kg *before* it even begins to cool — roughly five times what
> the resulting water then delivers cooling from 100°C to body temperature.
>
> It is also why sweating cools you: evaporating water carries away $L_v$ per kilogram, and it does so
> at body temperature rather than requiring boiling.

---

## 4. Calorimetry

An isolated system conserves energy, so

$$\boxed{\sum Q = 0} \qquad\text{or}\qquad Q_{\text{lost by hot}} = Q_{\text{gained by cold}}$$

### Worked example — verified

0.200 kg of aluminium at 100°C is dropped into 0.500 kg of water at 20°C. Find the final temperature.

$$m_{\text{Al}}c_{\text{Al}}(100 - T_f) = m_wc_w(T_f - 20)$$

$$T_f = \frac{m_{\text{Al}}c_{\text{Al}}(100) + m_wc_w(20)}{m_{\text{Al}}c_{\text{Al}} + m_wc_w} = \mathbf{26.3°\text{C}}$$

**Check:** heat lost by aluminium $= 13{,}260$ J; heat gained by water $= 13{,}260$ J ✓

> **Note how little the water warmed** — 6.3 K, while the aluminium cooled by 73.7 K. The water's
> larger mass *and* far larger specific heat both work in the same direction.

### When a phase change may occur

If ice is involved you must **check whether it all melts** before assuming a final temperature.

**Verified example.** 0.050 kg of ice at 0°C into 0.300 kg of water at 25°C:

- Energy to melt all the ice: $mL_f = 16{,}700$ J
- Energy available cooling the water to 0°C: $m c_w(25) = 31{,}395$ J

Since $31{,}395 > 16{,}700$, **all the ice melts** and the mixture settles above 0°C:

$$T_f = \frac{31{,}395 - 16{,}700}{(0.300+0.050)(4186)} = \mathbf{10.0°\text{C}}$$

**Had the ice won**, some would remain and the final temperature would be exactly 0°C. **Always
compare the two energies before solving.** Skipping this check is the most common error in
calorimetry problems, and it produces answers like "final temperature $-8°$C" for a mixture of ice and
warm water — physically impossible, and a signal to go back.

---

## 5. Summary

| | |
|---|---|
| Heat | energy **in transit** due to a temperature difference; measured in **joules** |
| Objects contain | internal energy, **not** heat |
| Heat flows | hot → cold spontaneously; never the reverse |
| Specific heat | $Q = mc\Delta T$ |
| Water | $c = 4186$ — exceptionally high; moderates climate |
| Latent heat | $Q = mL$; temperature does **not** change |
| $L_f$, $L_v$ (water) | $3.34\times10^5$, $2.26\times10^6$ J/kg |
| $L_v/L_f$ | $6.77$ — why steam burns badly |
| Heating $-20$°C ice to $120$°C steam | 309 kJ, of which boiling is 73% |
| Calorimetry | $\sum Q = 0$ |
| With ice present | **check whether it all melts first** |

---

## 6. Conceptual Questions

1. Why is it wrong to say "this object contains a lot of heat"? What does it contain?

2. Equal masses of water and aluminium absorb the same energy. Which ends up hotter, and by what factor?

3. Why is a steam burn worse than a boiling-water burn at the same temperature?

4. Why does sweating cool you, given that the sweat is already at body temperature?

5. In a calorimetry problem involving ice, why must you check whether all the ice melts before computing a final temperature?

---

## 7. Problems

1. How much energy is needed to raise 2.50 kg of water from 15.0°C to 85.0°C?

2. A 0.400 kg copper block absorbs 12.0 kJ. Find its temperature rise.

3. Find the total energy to convert 0.250 kg of ice at $-10.0°$C into steam at 100°C.

4. A 0.150 kg aluminium block at 150°C is dropped into 0.400 kg of water at 18.0°C. Find the final temperature.

5. 0.080 kg of ice at 0°C is added to 0.250 kg of water at 30.0°C. Determine whether all the ice melts, then find the final temperature.

6. A 0.500 kg lead block at 200°C is dropped into 0.200 kg of water at 20.0°C. Find the final temperature, and comment on why it is so close to the water's initial value.

---

*Next: Lecture 36 — Heat Transfer and the Ideal Gas*
