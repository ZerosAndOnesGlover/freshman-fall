# PHYS 141 · Problem Set 11 Solutions
## INSTRUCTOR ONLY

**Total: 100 points.** All values verified computationally.

---

*Revised 2026-09-21 to match the 10-problem set; problems are numbered as in the new set.*

## Part A — Temperature and Expansion

### 1. *(10 pts)* Steel rail, 25.000 m, $10.0\to45.0°$C
$$\Delta L = (1.2\times10^{-5})(25.000)(35.0) = 1.05\times10^{-2}~\text{m} \qquad L = \mathbf{25.0105~\text{m}}$$

*A 10.5 mm expansion on a 25 m rail — which is why rails are laid with gaps or welded under
controlled tension.*

---

### 2. *(10 pts)* Steel bridge, 1.20 km, $-10.0\to40.0°$C
$$\Delta L = (1.2\times10^{-5})(1200)(50.0) = \mathbf{0.720~\text{m}}$$

**Consequence:** 72 cm of movement must be accommodated by expansion joints. Without them the deck
would either buckle upward in summer or crack in winter, and the forces involved are enormous — a
constrained steel member develops stress $\sigma = E\alpha\Delta T$, which for $E \approx 200$ GPa
and $\Delta T = 50$ K is about **120 MPa**, comparable to the yield strength of structural steel.

*Marking: 3 for the number, 2 for a sensible engineering comment.*

---

## Part B — Heat and Calorimetry

### 3. *(10 pts)*
$$Q = (2.50)(4186)(70.0) = \mathbf{7.33\times10^5~\text{J}} = 733~\text{kJ}$$

---

### 4. *(10 pts)* 0.250 kg ice at $-10.0°$C to steam at $100°$C

| Stage | Energy (J) |
|---|---|
| Warm ice $-10\to0$ | 5,225 |
| Melt | 83,500 |
| Warm water $0\to100$ | 104,650 |
| Boil | 565,000 |
| **Total** | **758,375** |

**Boiling accounts for $565{,}000/758{,}375 = \mathbf{74.5\%}$ of the total.**

*Marking: 4 for the four stages, 1 for the total, 1 for the fraction. Omitting a latent-heat stage is
the standard error — check that both plateaus appear.*

---

### 5. *(10 pts)* Aluminium into water
$$T_f = \frac{(0.150)(900)(150) + (0.400)(4186)(18.0)}{(0.150)(900)+(0.400)(4186)} = \mathbf{27.8°\text{C}}$$

**Check:** heat lost $= (0.150)(900)(150-27.85) = 16{,}490$ J; heat gained
$= (0.400)(4186)(27.85-18.0) = 16{,}490$ J ✓

---

### 6. *(10 pts)* Ice into warm water — **the check comes first**

Energy to melt all the ice: $(0.080)(3.34\times10^5) = \mathbf{26{,}720~\text{J}}$
Energy available cooling the water to 0°C: $(0.250)(4186)(30.0) = \mathbf{31{,}395~\text{J}}$

Since $31{,}395 > 26{,}720$, **all the ice melts**, and the surplus warms the combined mass:

$$T_f = \frac{31{,}395 - 26{,}720}{(0.250+0.080)(4186)} = \mathbf{3.38°\text{C}}$$

*Marking: **3 of the 6 are for performing the comparison**, whatever follows. A student who solves
straight through without checking may still get the right number here, but will fail the next problem
of this type. Say so in feedback.*

---

## Part C — Heat Transfer

### 7. *(10 pts)* Single glazing
$$P = \frac{(0.800)(2.00)(20.0)}{0.00400} = \mathbf{8000~\text{W}}$$

*8 kW through one window is absurdly high, and correctly so — this is why single glazing performs so
badly, and why the glass is never the limiting resistance in a real window.*

---

### 8. *(10 pts)* Blackbody sphere
$$A = 4\pi r^2 = 0.1257~\text{m}^2 \qquad P = (1)(5.67\times10^{-8})(0.1257)(500)^4 = \mathbf{445~\text{W}}$$

---

## Part D — The Ideal Gas

### 9. *(10 pts)*
$$n = \frac{PV}{RT} = \frac{(1.50\times10^5)(0.0500)}{(8.314)(300)} = \mathbf{3.01~\text{mol}}$$

Isothermal compression: $P_2 = P_1V_1/V_2 = (1.50\times10^5)(0.0500)/0.0200 = \mathbf{3.75\times10^5~\text{Pa}}$.

---

### 10. *(10 pts)* RMS speeds at 300 K
$$v_{\text{rms}} = \sqrt{\frac{3RT}{M}}$$

| Gas | $M$ (kg/mol) | $v_{\text{rms}}$ (m/s) |
|---|---|---|
| N₂ | 0.0280 | **517** |
| H₂ | 0.00202 | **1925** |

**Ratio $= 3.72 = \sqrt{0.0280/0.00202}$** ✓ — speed goes as $1/\sqrt M$.

**Comment:** this is why hydrogen and helium have largely escaped Earth's atmosphere while nitrogen
and oxygen have not. Escape velocity is 11.2 km/s, and although the *average* H₂ speed is well below
that, the high-speed tail of the distribution is not.

---
