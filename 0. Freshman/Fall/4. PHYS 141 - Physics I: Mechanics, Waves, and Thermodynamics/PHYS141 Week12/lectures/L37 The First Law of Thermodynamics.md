# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Lecture 37 — The First Law of Thermodynamics

**Date:** Monday 9 November 2026 · 14:00–14:50 · Week 12

---

## Where This Fits

Week 11 introduced heat and the ideal gas. This lecture states the **conservation of energy** for
thermal systems — and the statement is deceptively short, because all the work lies in tracking signs
and in knowing which quantity is fixed in a given process.

Week 4 said energy is conserved for mechanical systems. The First Law extends that to systems that
exchange **heat** as well as work, which is to say, to everything.

---

## 1. Internal Energy

> **Internal energy $U$** is the total energy contained in a system — the kinetic and potential energy
> of all its molecules.

For an **ideal monatomic gas**, where molecules have only translational motion,

$$U = \tfrac32 nRT$$

**$U$ depends only on $T$.** This is a genuinely useful fact: for an ideal gas, if the temperature is
unchanged then $\Delta U = 0$, regardless of how the pressure and volume moved to get there.

$U$ is a **state function** — it depends only on the current state, not on the route taken. Heat and
work are not: they describe *processes*, and how much of each you get depends on the path.

---

## 2. The First Law

> $$\boxed{\Delta U = Q - W}$$
>
> where $Q$ is heat **added to** the system and $W$ is work done **by** the system.

**The sign convention is the entire difficulty**, and it is worth stating explicitly:

| Quantity | Positive when |
|---|---|
| $Q$ | Heat flows **into** the system |
| $W$ | The system **expands**, doing work on its surroundings |

So a gas that absorbs heat and expands has $Q > 0$ and $W > 0$, and $\Delta U$ is the difference.

*(Some texts write $\Delta U = Q + W$ with $W$ meaning work done **on** the system. Both are correct;
they differ only in bookkeeping. Fix one convention and stay with it — mixing them is the commonest
source of sign errors in this topic.)*

**In words:** the energy of a system changes by what you put in as heat, minus what it gives back as
work.

---

## 3. Work Done by a Gas

When a gas expands by $dV$ against pressure $P$, it does work $P\,dV$. Over a finite change,

$$W = \int_{V_1}^{V_2} P\,dV$$

**This is the area under the curve on a $PV$ diagram** — which is why $PV$ diagrams are the standard
tool of the subject, and why the *path* matters. Two processes joining the same endpoints enclose
different areas and therefore involve different work.

---

## 4. The Four Standard Processes

| Process | Held constant | $W$ | $\Delta U$ | $Q$ |
|---|---|---|---|---|
| **Isothermal** | $T$ | $nRT\ln(V_2/V_1)$ | $0$ | $= W$ |
| **Isobaric** | $P$ | $P\Delta V$ | $\tfrac32nR\Delta T$ | $\Delta U + W$ |
| **Isochoric** | $V$ | $0$ | $\tfrac32nR\Delta T$ | $= \Delta U$ |
| **Adiabatic** | — ($Q=0$) | $\dfrac{P_1V_1-P_2V_2}{\gamma-1}$ | $-W$ | $0$ |

### Isothermal — verified

Two moles at 300 K expanding from $0.0100$ m³ to $0.0300$ m³:

$$W = nRT\ln\frac{V_2}{V_1} = (2.00)(8.314)(300)\ln 3 = \mathbf{5480~\text{J}}$$

Since $T$ is constant, $\Delta U = 0$, so $Q = W = 5480$ J. **Every joule of heat that entered came
straight back out as work.**

### Isobaric — verified

The same volume change at a constant $1.50\times10^5$ Pa:

$$W = P\Delta V = (1.50\times10^5)(0.0200) = \mathbf{3000~\text{J}}$$

### Isochoric

$\Delta V = 0$, so **$W = 0$ exactly** and all the heat goes into internal energy. Heating a gas in a
sealed rigid container is the clean example.

### Adiabatic — verified

No heat is exchanged, so the system does work entirely at the expense of its own internal energy — and
therefore **cools as it expands**.

For a diatomic gas ($\gamma = 1.4$) expanding from $0.0100$ to $0.0300$ m³ starting at
$2.00\times10^5$ Pa and 300 K:

$$P_2 = P_1\left(\frac{V_1}{V_2}\right)^{\gamma} = \mathbf{4.30\times10^{4}~\text{Pa}} \qquad T_2 = T_1\left(\frac{V_1}{V_2}\right)^{\gamma-1} = \mathbf{193~\text{K}}$$

$$W = \frac{P_1V_1-P_2V_2}{\gamma-1} = \mathbf{1778~\text{J}} \qquad \Delta U = -1778~\text{J}$$

**The gas cooled by 107 K without losing any heat.** This is why a compressed-air canister goes cold
when you discharge it, why rising air cools and forms cloud, and how a diesel engine ignites its fuel
by compression alone.

> **Compare the isothermal and adiabatic expansions above.** Same endpoints in volume, very different
> outcomes: 5480 J of work with heat supplied, against 1778 J with none. **The path is not a detail.**

---

## 5. Cyclic Processes

If a system returns to its starting state, $U$ returns with it, so

$$\Delta U = 0 \qquad\Longrightarrow\qquad \boxed{Q_{\text{net}} = W_{\text{net}}}$$

**Over a complete cycle, the net work equals the net heat.** On a $PV$ diagram, the net work is the
**enclosed area** — positive going clockwise (an engine), negative anticlockwise (a refrigerator).

This is the foundation of Lecture 38.

---

## 6. Why There Is No Perpetual Motion Machine

A "machine of the first kind" would produce work with no energy input, i.e. $W > 0$ with $Q = 0$ and
$\Delta U = 0$. The First Law forbids it outright.

Every such device ever proposed has failed, and patent offices in several countries now refuse
applications for them without a working model — a rare instance of a physical law written into
administrative procedure.

**But the First Law permits things that never happen.** It has no objection to a cup of coffee
spontaneously heating up while the room cools, since energy would be conserved. Something else forbids
that, and it is Lecture 38's subject.

---

## 7. Summary

| | |
|---|---|
| Internal energy | $U = \tfrac32nRT$ (monatomic ideal); a **state function** |
| First Law | $\Delta U = Q - W$ |
| $Q>0$ | heat **into** the system |
| $W>0$ | system **expands** |
| Work | $W = \int P\,dV$ = area under the $PV$ curve |
| Isothermal | $\Delta U = 0$, $Q = W = nRT\ln(V_2/V_1)$ |
| Isobaric | $W = P\Delta V$ |
| Isochoric | $W = 0$, $Q = \Delta U$ |
| Adiabatic | $Q = 0$, $\Delta U = -W$; **expansion cools the gas** |
| Cycle | $\Delta U = 0$, so $Q_{\text{net}} = W_{\text{net}}$ = enclosed area |
| Forbids | perpetual motion of the first kind |
| Does **not** forbid | heat flowing cold → hot |

---

## 8. Conceptual Questions

1. Why is $U$ a state function while $Q$ and $W$ are not?

2. A gas expands isothermally. Its internal energy is unchanged, yet it did work. Where did the energy come from?

3. Why does a gas cool when it expands adiabatically, given that no heat leaves it?

4. Two processes connect the same initial and final states. Must they involve the same $\Delta U$? The same $Q$? The same $W$?

5. The First Law permits a cup of coffee to spontaneously warm while the room cools. Why does this never happen?

---

## 9. Problems

1. A gas absorbs 800 J of heat and does 300 J of work. Find $\Delta U$.

2. A gas is compressed, with 500 J of work done **on** it, while releasing 200 J of heat. Find $\Delta U$.

3. Two moles of ideal gas expand isothermally at 350 K from 0.0150 m³ to 0.0450 m³. Find $W$, $\Delta U$, and $Q$.

4. A gas at constant $2.00\times10^5$ Pa expands from 0.0200 m³ to 0.0500 m³. Find $W$.

5. A monatomic ideal gas ($n = 1.50$ mol) is heated at constant volume from 280 K to 400 K. Find $\Delta U$, $W$, and $Q$.

6. A diatomic gas ($\gamma = 1.40$) at $3.00\times10^5$ Pa and 320 K expands adiabatically from 0.0080 m³ to 0.0240 m³. Find $P_2$, $T_2$, $W$, and $\Delta U$.

7. A gas undergoes a cycle absorbing 1200 J and rejecting 900 J. Find the net work per cycle and state the direction on a $PV$ diagram.

---

*Next: Lecture 38 — The Second Law, Entropy, and Heat Engines*
