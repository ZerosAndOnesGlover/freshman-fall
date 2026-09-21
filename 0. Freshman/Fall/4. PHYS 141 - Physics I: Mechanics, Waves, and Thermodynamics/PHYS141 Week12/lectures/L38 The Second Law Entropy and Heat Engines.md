# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Lecture 38 — The Second Law, Entropy, and Heat Engines

**Date:** Tuesday 15 December 2026 · 14:00–14:50 · Week 12

---

## Where This Fits

The First Law says energy is conserved. It does **not** say which of the energy-conserving things
actually happen — and most of them do not.

A cup of coffee cooling in a room conserves energy. So would the same coffee spontaneously heating
while the room cooled. We observe one and never the other, and the First Law is silent about the
difference.

**The Second Law supplies the missing direction.** It is the law that gives time an arrow.

---

## 1. Two Statements, One Law

> **Clausius statement.** Heat does not spontaneously flow from a colder body to a hotter one.

> **Kelvin–Planck statement.** No process can convert heat *completely* into work with no other
> effect.

These sound unrelated. They are provably equivalent: a device violating either could be combined with
an ordinary engine to violate the other.

**The second statement is the surprising one.** You can convert work entirely into heat — friction
does it, and a resistor does it with perfect efficiency. **The reverse is impossible.** Heat and work
are both energy, but they are not interchangeable on equal terms, and that asymmetry is the whole
content of the Second Law.

---

## 2. Heat Engines

A **heat engine** takes heat $Q_h$ from a hot reservoir, converts part of it to work $W$, and dumps
the remainder $Q_c$ into a cold reservoir.

Over a complete cycle $\Delta U = 0$, so

$$W = Q_h - Q_c \qquad\text{and}\qquad \boxed{e = \frac{W}{Q_h} = 1 - \frac{Q_c}{Q_h}}$$

**Verified:** an engine absorbing 1000 J and rejecting 700 J does 300 J of work at
$e = \mathbf{30.0\%}$.

> **The cold reservoir is not a design flaw.** The Kelvin–Planck statement says you *must* reject
> heat somewhere — an engine with $Q_c = 0$ would have $e = 1$ and is impossible. Every power station
> needs a cooling tower or a river for exactly this reason, and the "waste" heat is not waste through
> poor engineering but through physical necessity.

---

## 3. The Carnot Limit

> **Carnot's theorem.** No engine operating between two reservoirs can exceed the efficiency of a
> reversible engine between the same two, and that efficiency is
>
> $$\boxed{e_{\text{Carnot}} = 1 - \frac{T_c}{T_h}}$$
>
> with temperatures in **kelvin**.

**Verified:**

| $T_h$ (K) | $T_c$ (K) | $e_{\text{Carnot}}$ |
|---|---|---|
| 500 | 300 | 40.0% |
| 600 | 300 | 50.0% |
| 800 | 300 | **62.5%** |
| 373 | 273 | 26.8% |

**Two lessons from the table.**

First, **efficiency depends only on the temperatures**, not on the working substance, the design, or
the engineering budget. Steam, petrol, or exotic fluid — the same limit applies.

Second, **raising $T_h$ helps far more than lowering $T_c$**, and $T_c$ is usually fixed by the
environment anyway. This is why every advance in power-station efficiency has come from higher
turbine inlet temperatures, and why the limiting technology is metallurgy rather than thermodynamics.

**A real example:** a modern coal plant runs at roughly $T_h = 830$ K and $T_c = 300$ K, giving a
Carnot limit of **63.9%**. Actual plants achieve about 40%. The gap is irreversibility — friction,
turbulence, finite-rate heat transfer — and no amount of engineering closes it entirely.

---

## 4. Refrigerators and Heat Pumps

Run the cycle backwards: put work **in** to move heat from cold to hot. This does not violate the
Clausius statement, which forbids only *spontaneous* flow.

$$\text{COP}_{\text{fridge}} = \frac{Q_c}{W} \le \frac{T_c}{T_h-T_c} \qquad \text{COP}_{\text{heat pump}} = \frac{Q_h}{W} \le \frac{T_h}{T_h-T_c}$$

**Verified** for $T_c = 273$ K and $T_h = 300$ K: $\text{COP}_{\text{fridge}} = 10.1$ and
$\text{COP}_{\text{heat pump}} = 11.1$.

**Note that the two differ by exactly 1**, always — because $Q_h = Q_c + W$, so dividing through by
$W$ gives $\text{COP}_{\text{hp}} = \text{COP}_{\text{fridge}} + 1$.

> **A COP above 1 is not a violation of anything.** A heat pump delivering 11 J of heat per joule of
> electricity is not creating energy; it is *moving* 10 J from outside and adding 1 J of work. This is
> why heat pumps beat resistive heating so decisively — a resistor has COP exactly 1 by definition.
>
> Note also that the COP **collapses as $T_h - T_c$ grows**, which is why heat pumps lose effectiveness
> in very cold weather, precisely when they are needed most.

---

## 5. Entropy

The Second Law can be made quantitative. For a reversible process at temperature $T$,

$$dS = \frac{dQ_{\text{rev}}}{T} \qquad\text{so}\qquad \Delta S = \int\frac{dQ_{\text{rev}}}{T}$$

**Entropy is a state function**, like $U$ and unlike $Q$.

> **Second Law, quantitative form.** For any process in an **isolated** system,
> $$\boxed{\Delta S_{\text{total}} \ge 0}$$
> with equality only for reversible processes.

### Verified examples

**Melting 1.00 kg of ice at 273.15 K:**
$$\Delta S = \frac{Q}{T} = \frac{3.34\times10^5}{273.15} = \mathbf{+1223~\text{J/K}}$$

**Isothermal expansion** of 2.00 mol at 300 K from 0.0100 to 0.0300 m³:
$$\Delta S = \frac{Q}{T} = nR\ln\frac{V_2}{V_1} = \mathbf{+18.27~\text{J/K}}$$

**Heat flowing 1000 J from a 500 K reservoir to a 300 K reservoir:**

| | $\Delta S$ (J/K) |
|---|---|
| Hot reservoir | $-1000/500 = -2.00$ |
| Cold reservoir | $+1000/300 = +3.33$ |
| **Total** | $\mathbf{+1.33}$ |

**Positive, so the process happens.** Reverse it and the total would be $-1.33$ J/K — forbidden. **The
entropy calculation predicts the direction of heat flow**, which is exactly what the First Law could
not do.

### What entropy measures

Statistically, $S = k_B\ln\Omega$, where $\Omega$ is the number of microscopic arrangements consistent
with the macroscopic state. Entropy increases because there are overwhelmingly more disordered
arrangements than ordered ones, so a system exploring its states at random ends up in a disordered one
essentially always.

**"Essentially always" is not "necessarily".** The Second Law is statistical, not absolute. Air *could*
spontaneously gather in one half of a room — but for $10^{23}$ molecules the probability is around
$2^{-10^{23}}$, which is zero for every practical purpose and will remain so for the age of the
universe.

---

## 6. The Third Law, Briefly

> **Third Law.** The entropy of a perfect crystal approaches zero as $T\to0$ K.

A consequence is that **absolute zero cannot be reached in finitely many steps**. Each cooling stage
removes a fraction of the remaining energy, so you approach 0 K asymptotically. Laboratories have
reached below $10^{-9}$ K; none has reached zero, and none will.

---

## 7. Summary

| | |
|---|---|
| **Clausius** | Heat does not spontaneously flow cold → hot |
| **Kelvin–Planck** | Heat cannot be *fully* converted to work |
| Asymmetry | Work → heat is free; heat → work is limited |
| Engine efficiency | $e = 1 - Q_c/Q_h$ |
| **Carnot limit** | $e = 1 - T_c/T_h$, kelvin, **substance-independent** |
| Raising $T_h$ | helps more than lowering $T_c$ |
| Real plant | 63.9% Carnot limit, ~40% achieved |
| Fridge / heat pump COP | $T_c/(T_h-T_c)$ / $T_h/(T_h-T_c)$; differ by exactly **1** |
| COP > 1 | moves heat, does not create energy |
| Entropy | $\Delta S = \int dQ_{\text{rev}}/T$; a **state function** |
| Second Law | $\Delta S_{\text{total}} \ge 0$ for an isolated system |
| Statistical meaning | $S = k_B\ln\Omega$ |
| Third Law | $S\to0$ as $T\to0$; absolute zero unreachable |

---

## 8. Conceptual Questions

1. Why can work be converted entirely into heat, but not the reverse?

2. Why does every heat engine need a cold reservoir? Is this an engineering limitation?

3. A heat pump has COP 4. Does this violate energy conservation? Explain.

4. Why do heat pumps become less effective in very cold weather?

5. The Second Law is statistical rather than absolute. What does this mean, and why does it not matter in practice?

---

## 9. Problems

1. An engine absorbs 2500 J and rejects 1800 J per cycle. Find $W$ and $e$.

2. A Carnot engine operates between 650 K and 310 K. Find its maximum efficiency.

3. An engine claims 55% efficiency between 700 K and 350 K. Is this possible? Justify.

4. A Carnot engine has $e = 0.400$ and $T_c = 290$ K. Find $T_h$.

5. A refrigerator maintains 4.00°C in a 22.0°C kitchen. Find its maximum COP, and the minimum work to remove 5.00 kJ.

6. Find the entropy change when 0.500 kg of ice melts at 0°C.

7. 2000 J of heat flows from a 600 K reservoir to a 350 K reservoir. Find $\Delta S$ for each and the total. Is the process allowed?

8. A heat pump delivers 12.0 kJ to a house using 3.00 kJ of electricity. Find its COP, and the COP of a resistive heater doing the same job.

---

*Next: Lecture 39 — Review and the Road Ahead*
