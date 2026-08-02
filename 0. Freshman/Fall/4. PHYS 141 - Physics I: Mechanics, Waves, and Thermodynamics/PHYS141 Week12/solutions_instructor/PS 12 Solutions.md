# PHYS 141 — Problem Set 12 Solutions
## INSTRUCTOR ONLY

**Total: 100 points.** All values verified computationally.
**Convention throughout: $\Delta U = Q - W$, with $W$ done BY the system.**

---

## Part A — The First Law

### 1. *(4 pts)*
$$\Delta U = Q - W = 800 - 300 = \mathbf{+500~\text{J}}$$

---

### 2. *(4 pts)*
Work done **on** the gas is $500$ J, so work done **by** it is $W = -500$ J. Heat released means
$Q = -200$ J.
$$\Delta U = (-200) - (-500) = \mathbf{+300~\text{J}}$$

**The internal energy rises** even though heat left the gas — compression did more work on it than
heat carried away.

*Marking: 2 for the sign handling, 2 for the value. **Award the 2 only if the convention is stated**;
the question asks for it explicitly.*

---

### 3. *(5 pts)* Isothermal, $n = 2.00$, $T = 350$ K, $0.0150 \to 0.0450$ m³
$$W = nRT\ln\frac{V_2}{V_1} = (2.00)(8.314)(350)\ln 3 = \mathbf{6394~\text{J}}$$
$$\Delta U = \mathbf{0} \quad\text{(isothermal, ideal gas)} \qquad Q = W = \mathbf{6394~\text{J}}$$

---

### 4. *(4 pts)*
$$W = P\Delta V = (2.00\times10^5)(0.0500-0.0200) = \mathbf{6000~\text{J}}$$

---

### 5. *(4 pts)* Isochoric, monatomic, $n = 1.50$, $280 \to 400$ K
$$W = \mathbf 0 \qquad \Delta U = \tfrac32nR\Delta T = \tfrac32(1.50)(8.314)(120) = \mathbf{2245~\text{J}} \qquad Q = \Delta U = \mathbf{2245~\text{J}}$$

---

### 6. *(4 pts)*
$U$ depends only on the system's current state — for an ideal gas, only on $T$. Return the gas to its
original state by any route and $U$ returns to its original value.

$Q$ and $W$ describe **processes**, not states. There is no "amount of heat in" a gas, only heat that
crossed its boundary during some change.

**Concrete consequence:** two different paths between the same endpoints give the **same** $\Delta U$
but **different** $Q$ and $W$ — as Problems 3 and 7 demonstrate for the same volume change. Over a
closed cycle $\Delta U = 0$ exactly, while $Q$ and $W$ are generally non-zero and equal to each other.

*Marking: 2 for the definition, 2 for a genuine consequence. A restatement without an example earns 2.*

---

## Part B — Processes and Cycles

### 7. *(7 pts)* Adiabatic, $\gamma = 1.40$, $0.0080\to0.0240$ m³
$$P_2 = P_1\left(\frac{V_1}{V_2}\right)^{\gamma} = (3.00\times10^5)\left(\tfrac13\right)^{1.40} = \mathbf{6.44\times10^{4}~\text{Pa}}$$
$$T_2 = T_1\left(\frac{V_1}{V_2}\right)^{\gamma-1} = 320\left(\tfrac13\right)^{0.40} = \mathbf{206~\text{K}}$$
$$W = \frac{P_1V_1 - P_2V_2}{\gamma-1} = \mathbf{2134~\text{J}} \qquad \Delta U = -W = \mathbf{-2134~\text{J}}$$

**Why it cools:** with $Q = 0$, the First Law gives $\Delta U = -W$ directly. The gas does 2134 J of
work on its surroundings and has no heat supply to draw on, so it pays for that work out of its own
internal energy. Since $U \propto T$ for an ideal gas, the temperature falls — here by 114 K.

*Marking: 1 each for $P_2$, $T_2$, $W$, $\Delta U$; 3 for the explanation. The explanation must
invoke $Q = 0$, not merely assert that expansion cools.*

---

### 8. *(5 pts)*
$$W_{\text{net}} = Q_h - Q_c = 1200 - 900 = \mathbf{300~\text{J}}$$

Positive net work means the cycle runs **clockwise** on a $PV$ diagram — it is an **engine**.

---

### 9. *(4 pts)*
Both curves fall from left to right, but the **adiabat is steeper** (slope $\propto\gamma$ rather than
1 on a log–log view), so from a common starting point it lies **below** the isotherm.

The **isotherm encloses more area**, meaning more work is done in the isothermal expansion —
verified by Lecture 37's worked pair: 5480 J isothermal against 1778 J adiabatic for the same volume
change.

**Physically:** the isothermal process is fed heat continuously to hold $T$ constant, so it has more
energy available to convert to work. The adiabatic process must fund the work from internal energy
alone.

---

### 10. *(4 pts)*
$\Delta U$ is fixed by the endpoints because $U$ is a state function. $Q$ and $W$ are not: they measure
energy *crossing the boundary* during the process, and different paths transfer different amounts.

From Problem 9: both paths connect the same volumes, but one absorbs 5480 J and does 5480 J of work,
while the other absorbs nothing and does 1778 J. **Yet if both ended at the same state, $\Delta U$
would be identical.** *(In this instance they do not end at the same $T$, which is precisely why the
work differs.)*

---

## Part C — Heat Engines and the Second Law

### 11. *(4 pts)*
$$W = 2500-1800 = \mathbf{700~\text{J}} \qquad e = \frac{700}{2500} = \mathbf{0.280} = 28.0\%$$

---

### 12. *(4 pts)*
$$e = 1 - \frac{310}{650} = \mathbf{0.523} = 52.3\%$$

---

### 13. *(5 pts)*
$$e_{\text{Carnot}} = 1 - \frac{350}{700} = 0.500 = 50.0\%$$

The claim of **55% exceeds the Carnot limit of 50%**, so it is **impossible**. No engine operating
between these reservoirs can do better than 50%, whatever its design or working substance — this is
Carnot's theorem, and it follows from the Second Law.

*Marking: 2 for the limit, 3 for a correct verdict **with the comparison shown**. A verdict without
the number earns 1.*

---

### 14. *(4 pts)*
$$e = 1-\frac{T_c}{T_h} \;\Longrightarrow\; T_h = \frac{T_c}{1-e} = \frac{290}{0.600} = \mathbf{483~\text{K}}$$

---

### 15. *(6 pts)* Refrigerator, $4.00°$C interior, $22.0°$C kitchen
$T_c = 277.15$ K, $T_h = 295.15$ K.
$$\text{COP}_{\max} = \frac{T_c}{T_h-T_c} = \frac{277.15}{18.00} = \mathbf{15.4}$$
$$W_{\min} = \frac{Q_c}{\text{COP}} = \frac{5000}{15.40} = \mathbf{325~\text{J}}$$

**Only 325 J of work to move 5000 J of heat** — because the temperature difference is small. Note how
sensitive this is: doubling $\Delta T$ roughly halves the COP.

---

### 16. *(4 pts)*
$$\text{COP} = \frac{Q_h}{W} = \frac{12.0}{3.00} = \mathbf{4.00}$$

A resistive heater converts electricity to heat with $\text{COP} = 1$ exactly — every joule in gives
one joule of heat. **The heat pump delivers four times as much heat per joule of electricity.**

**No conservation violation:** the pump does not create 12 kJ from 3 kJ. It *moves* 9 kJ from outside
the house and adds the 3 kJ of work, giving $Q_h = Q_c + W$. Energy is conserved exactly.

*Marking: 1 COP, 1 comparison, 2 for the conservation explanation.*

---

### 17. *(3 pts)*
**Clausius:** heat does not flow spontaneously from a colder body to a hotter one.
**Kelvin–Planck:** no cyclic process can convert heat entirely into work with no other effect.

**Why a cold reservoir is unavoidable:** by Kelvin–Planck, an engine cannot convert all of $Q_h$ into
work, so some heat must be rejected — and it can only be rejected to something colder. An engine with
$Q_c = 0$ would have $e = 1$, which the Second Law forbids.

---

## Part D — Entropy

### 18. *(5 pts)*
$$\Delta S = \frac{Q}{T} = \frac{(0.500)(3.34\times10^5)}{273.15} = \mathbf{+611~\text{J/K}}$$

*Constant $T$ throughout the melt, so the simple $Q/T$ applies.*

---

### 19. *(7 pts)* 2000 J from 600 K to 350 K

| | $\Delta S$ (J/K) |
|---|---|
| Hot reservoir | $-2000/600 = \mathbf{-3.33}$ |
| Cold reservoir | $+2000/350 = \mathbf{+5.71}$ |
| **Total** | $\mathbf{+2.38}$ |

**Positive, so the process is permitted** — and indeed it is what happens spontaneously.

**Reversed**, the total would be $\mathbf{-2.38}$ J/K. A negative total entropy change for an isolated
system is forbidden by the Second Law, which is precisely why heat never flows spontaneously from cold
to hot. **The entropy calculation predicts the direction**, which the First Law cannot do — both
directions conserve energy perfectly.

*Marking: 2 each for the two reservoirs, 1 for the total, 2 for the reverse-process argument.*

---

### 20. *(5 pts)* Isothermal expansion, $n = 2.00$, $T = 300$ K, $0.0100\to0.0300$ m³

**Via $Q/T$:** $W = nRT\ln3 = 5480$ J, and $Q = W$ since $\Delta U = 0$, so
$$\Delta S = \frac{5480}{300} = \mathbf{+18.27~\text{J/K}}$$

**Via the direct formula:** $\Delta S = nR\ln(V_2/V_1) = (2.00)(8.314)\ln3 = \mathbf{+18.27~\text{J/K}}$ ✓

They agree, as they must — the second is the first with $W$ substituted and $T$ cancelled.

---

### 21. *(4 pts)*
$\Omega$ is the number of microscopic arrangements (microstates) consistent with the observed
macroscopic state. $S = k_B\ln\Omega$ says entropy counts them, logarithmically.

**Why statistical:** entropy increases because disordered macrostates correspond to vastly more
microstates than ordered ones, so a system wandering among its microstates is overwhelmingly likely to
be found in a disordered one. **It is not forbidden for entropy to decrease — merely astronomically
improbable.** For $10^{23}$ particles the probability of a noticeable spontaneous decrease is around
$2^{-10^{23}}$, which will not occur in the lifetime of the universe.

*Marking: 2 for the microstate definition, 2 for the probabilistic reading. Students who assert the
Second Law is absolute lose 2.*

---

### 22. *(4 pts)*
Suppose heat $Q$ flows from a room at $T_r$ into hotter coffee at $T_c > T_r$.

$$\Delta S_{\text{total}} = \underbrace{-\frac{Q}{T_r}}_{\text{room}} + \underbrace{+\frac{Q}{T_c}}_{\text{coffee}} = Q\left(\frac{1}{T_c}-\frac{1}{T_r}\right) < 0 \quad\text{since } T_c > T_r$$

**The total entropy change is negative, so the Second Law forbids it** — even though the First Law is
perfectly satisfied, since energy is merely relocated.

**This is the whole point of the Second Law.** Conservation of energy permits both directions; only
entropy distinguishes the one that happens from the one that does not.

*Marking: 2 for the calculation with correct signs, 2 for the First-vs-Second Law contrast.*

---

*PHYS 141 · Week 12 · PS 12 Solutions · Instructor copy*
