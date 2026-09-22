# PHYS 141 · Problem Set 12 Solutions
## INSTRUCTOR ONLY

**Total: 100 points.** All values verified computationally.
**Convention throughout: $\Delta U = Q - W$, with $W$ done BY the system.**

---

*Revised 2026-09-21 to match the 10-problem set; problems are numbered as in the new set.*

## Part A — The First Law

### 1. *(10 pts)*
$$\Delta U = Q - W = 800 - 300 = \mathbf{+500~\text{J}}$$

---

### 2. *(10 pts)* Isothermal, $n = 2.00$, $T = 350$ K, $0.0150 \to 0.0450$ m³
$$W = nRT\ln\frac{V_2}{V_1} = (2.00)(8.314)(350)\ln 3 = \mathbf{6394~\text{J}}$$
$$\Delta U = \mathbf{0} \quad\text{(isothermal, ideal gas)} \qquad Q = W = \mathbf{6394~\text{J}}$$

---

### 3. *(10 pts)*
$$W = P\Delta V = (2.00\times10^5)(0.0500-0.0200) = \mathbf{6000~\text{J}}$$

---

## Part B — Processes and Cycles

### 4. *(10 pts)* Adiabatic, $\gamma = 1.40$, $0.0080\to0.0240$ m³
$$P_2 = P_1\left(\frac{V_1}{V_2}\right)^{\gamma} = (3.00\times10^5)\left(\tfrac13\right)^{1.40} = \mathbf{6.44\times10^{4}~\text{Pa}}$$
$$T_2 = T_1\left(\frac{V_1}{V_2}\right)^{\gamma-1} = 320\left(\tfrac13\right)^{0.40} = \mathbf{206~\text{K}}$$
$$W = \frac{P_1V_1 - P_2V_2}{\gamma-1} = \mathbf{2134~\text{J}} \qquad \Delta U = -W = \mathbf{-2134~\text{J}}$$

**Why it cools:** with $Q = 0$, the First Law gives $\Delta U = -W$ directly. The gas does 2134 J of
work on its surroundings and has no heat supply to draw on, so it pays for that work out of its own
internal energy. Since $U \propto T$ for an ideal gas, the temperature falls — here by 114 K.

*Marking: 1 each for $P_2$, $T_2$, $W$, $\Delta U$; 3 for the explanation. The explanation must
invoke $Q = 0$, not merely assert that expansion cools.*

---

### 5. *(10 pts)*
$$W_{\text{net}} = Q_h - Q_c = 1200 - 900 = \mathbf{300~\text{J}}$$

Positive net work means the cycle runs **clockwise** on a $PV$ diagram — it is an **engine**.

---

## Part C — Heat Engines and the Second Law

### 6. *(10 pts)*
$$W = 2500-1800 = \mathbf{700~\text{J}} \qquad e = \frac{700}{2500} = \mathbf{0.280} = 28.0\%$$

---

### 7. *(10 pts)*
$$e = 1 - \frac{310}{650} = \mathbf{0.523} = 52.3\%$$

---

### 8. *(10 pts)* Refrigerator, $4.00°$C interior, $22.0°$C kitchen
$T_c = 277.15$ K, $T_h = 295.15$ K.
$$\text{COP}_{\max} = \frac{T_c}{T_h-T_c} = \frac{277.15}{18.00} = \mathbf{15.4}$$
$$W_{\min} = \frac{Q_c}{\text{COP}} = \frac{5000}{15.40} = \mathbf{325~\text{J}}$$

**Only 325 J of work to move 5000 J of heat** — because the temperature difference is small. Note how
sensitive this is: doubling $\Delta T$ roughly halves the COP.

---

## Part D — Entropy

### 9. *(10 pts)*
$$\Delta S = \frac{Q}{T} = \frac{(0.500)(3.34\times10^5)}{273.15} = \mathbf{+611~\text{J/K}}$$

*Constant $T$ throughout the melt, so the simple $Q/T$ applies.*

---

### 10. *(10 pts)* 2000 J from 600 K to 350 K

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
