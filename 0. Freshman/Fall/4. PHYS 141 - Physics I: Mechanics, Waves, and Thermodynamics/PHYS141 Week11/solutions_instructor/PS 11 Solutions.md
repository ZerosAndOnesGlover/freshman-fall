# PHYS 141 · Problem Set 11 Solutions
## INSTRUCTOR ONLY

**Total: 100 points.** All values verified computationally.

---

## Part A — Temperature and Expansion

### 1. *(4 pts)*
$$-15.0°\text{C} = \mathbf{5.00°\text{F}} = \mathbf{258.15~\text{K}} \qquad 98.6°\text{F} = \mathbf{37.0°\text{C}}$$

The scales read the same at $\mathbf{-40°}$: setting $T = \tfrac95T+32$ gives $T = -40$.

---

### 2. *(4 pts)* Steel rail, 25.000 m, $10.0\to45.0°$C
$$\Delta L = (1.2\times10^{-5})(25.000)(35.0) = 1.05\times10^{-2}~\text{m} \qquad L = \mathbf{25.0105~\text{m}}$$

*A 10.5 mm expansion on a 25 m rail — which is why rails are laid with gaps or welded under
controlled tension.*

---

### 3. *(4 pts)* Aluminium, $2.0000\to2.0050$ m
$$\Delta T = \frac{\Delta L}{\alpha L_0} = \frac{0.0050}{(2.4\times10^{-5})(2.0000)} = 104.2~\text{K} \qquad T = \mathbf{124°\text{C}}$$

---

### 4. *(5 pts)* Steel bridge, 1.20 km, $-10.0\to40.0°$C
$$\Delta L = (1.2\times10^{-5})(1200)(50.0) = \mathbf{0.720~\text{m}}$$

**Consequence:** 72 cm of movement must be accommodated by expansion joints. Without them the deck
would either buckle upward in summer or crack in winter, and the forces involved are enormous — a
constrained steel member develops stress $\sigma = E\alpha\Delta T$, which for $E \approx 200$ GPa
and $\Delta T = 50$ K is about **120 MPa**, comparable to the yield strength of structural steel.

*Marking: 3 for the number, 2 for a sensible engineering comment.*

---

### 5. *(4 pts)* Glass container, 500.0 mL, $20.0\to80.0°$C
$$\beta = 3\alpha = 2.7\times10^{-5}~\text{K}^{-1} \qquad \Delta V = (2.7\times10^{-5})(500.0)(60.0) = 0.81~\text{mL}$$
$$V = \mathbf{500.81~\text{mL}}$$

*The container's **capacity** expands, exactly as the hole argument requires. Students who reason that
the glass "thickens inward" and reduces capacity should be referred to Lecture 34 §4.*

---

### 6. *(4 pts)* Steel ring over a shaft
$$\Delta T = \frac{4.010-4.000}{(1.2\times10^{-5})(4.000)} = \mathbf{208~\text{K}} \qquad T = 20 + 208 = \mathbf{228°\text{C}}$$

*This is shrink-fitting, and it is genuinely how railway wheels are mounted on axles.*

---

## Part B — Heat and Calorimetry

### 7. *(4 pts)*
$$Q = (2.50)(4186)(70.0) = \mathbf{7.33\times10^5~\text{J}} = 733~\text{kJ}$$

---

### 8. *(4 pts)*
$$\Delta T = \frac{12{,}000}{(0.400)(387)} = \mathbf{77.5~\text{K}}$$

---

### 9. *(6 pts)* 0.250 kg ice at $-10.0°$C to steam at $100°$C

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

### 10. *(5 pts)* Aluminium into water
$$T_f = \frac{(0.150)(900)(150) + (0.400)(4186)(18.0)}{(0.150)(900)+(0.400)(4186)} = \mathbf{27.8°\text{C}}$$

**Check:** heat lost $= (0.150)(900)(150-27.85) = 16{,}490$ J; heat gained
$= (0.400)(4186)(27.85-18.0) = 16{,}490$ J ✓

---

### 11. *(6 pts)* Ice into warm water — **the check comes first**

Energy to melt all the ice: $(0.080)(3.34\times10^5) = \mathbf{26{,}720~\text{J}}$
Energy available cooling the water to 0°C: $(0.250)(4186)(30.0) = \mathbf{31{,}395~\text{J}}$

Since $31{,}395 > 26{,}720$, **all the ice melts**, and the surplus warms the combined mass:

$$T_f = \frac{31{,}395 - 26{,}720}{(0.250+0.080)(4186)} = \mathbf{3.38°\text{C}}$$

*Marking: **3 of the 6 are for performing the comparison**, whatever follows. A student who solves
straight through without checking may still get the right number here, but will fail the next problem
of this type. Say so in feedback.*

---

### 12. *(5 pts)* Lead into water
$$T_f = \frac{(0.500)(128)(200) + (0.200)(4186)(20.0)}{(0.500)(128)+(0.200)(4186)} = \mathbf{32.8°\text{C}}$$

**Why so close to 20°C:** the thermal capacities are wildly unequal. The lead contributes
$mc = (0.500)(128) = 64$ J/K; the water $(0.200)(4186) = 837$ J/K — **thirteen times larger**. The
mixture's final temperature is a weighted average, and the water dominates the weighting despite
being the lighter and initially cooler body.

*Marking: 3 for the number, 2 for the $mc$ comparison. "Because water has a high specific heat" earns
1; the question asks for the comparison.*

---

## Part C — Heat Transfer

### 13. *(5 pts)* Single glazing
$$P = \frac{(0.800)(2.00)(20.0)}{0.00400} = \mathbf{8000~\text{W}}$$

*8 kW through one window is absurdly high, and correctly so — this is why single glazing performs so
badly, and why the glass is never the limiting resistance in a real window.*

---

### 14. *(7 pts)* Double glazing — resistances in series

Per unit area, $R = L/k$ for each layer:

| Layer | $L$ (m) | $k$ | $R$ (m²K/W) |
|---|---|---|---|
| Glass | 0.00400 | 0.800 | 0.00500 |
| **Air gap** | 0.0100 | 0.026 | **0.3846** |
| Glass | 0.00400 | 0.800 | 0.00500 |
| | | **Total** | **0.3946** |

$$P = \frac{A\Delta T}{R_{\text{total}}} = \frac{(2.00)(20.0)}{0.3946} = \mathbf{101~\text{W}}$$

**A factor of $8000/101 = \mathbf{79}$ improvement.**

**The air gap dominates**, contributing 97.5% of the total resistance. The glass is nearly
irrelevant — its only job is to hold the air still and stop it convecting.

*Marking: 3 for the series-resistance method, 2 for the value, 2 for identifying the dominant layer.
Students who average the conductivities rather than summing resistances get this badly wrong.*

---

### 15. *(5 pts)* Blackbody sphere
$$A = 4\pi r^2 = 0.1257~\text{m}^2 \qquad P = (1)(5.67\times10^{-8})(0.1257)(500)^4 = \mathbf{445~\text{W}}$$

---

### 16. *(5 pts)* Net radiation from a person

$T = 306.15$ K, $T_s = 291.15$ K:
$$P_{\text{net}} = (0.97)(5.67\times10^{-8})(1.70)\left(306.15^4 - 291.15^4\right) = \mathbf{150~\text{W}}$$

**Comment:** this exceeds a resting metabolic output of about 100 W, which is why a person in an 18°C
room feels cold without clothing — you are losing energy faster than you generate it. Clothing works
by adding conductive resistance and by raising the effective radiating surface temperature.

*Marking: 3 for the value, 2 for the comparison. Using Celsius here gives a wildly wrong answer and
should score 0 for the calculation — it is the error the question is designed to catch.*

---

### 17. *(3 pts)* Vacuum flask

| Mechanism | How it is blocked |
|---|---|
| **Conduction** | The vacuum gap has no medium to conduct through; only the thin neck connects the walls |
| **Convection** | Requires a fluid; there is none in a vacuum |
| **Radiation** | The **silvered** surfaces have very low emissivity, so little is emitted or absorbed |

*All three must be named for full marks. The silvering is the part students forget.*

---

## Part D — The Ideal Gas

### 18. *(5 pts)*
$$n = \frac{PV}{RT} = \frac{(1.50\times10^5)(0.0500)}{(8.314)(300)} = \mathbf{3.01~\text{mol}}$$

Isothermal compression: $P_2 = P_1V_1/V_2 = (1.50\times10^5)(0.0500)/0.0200 = \mathbf{3.75\times10^5~\text{Pa}}$.

---

### 19. *(4 pts)* Rigid container, $20.0\to120°$C

Constant $V$, so $P \propto T$ **in kelvin**:
$$\frac{P_2}{P_1} = \frac{393.15}{293.15} = \mathbf{1.34}$$

**Using Celsius** would give $120/20 = 6.0$ — a **six-fold** pressure rise instead of a 34% one. The
error arises because Celsius has an arbitrary zero, so ratios of Celsius temperatures have no physical
meaning.

*Marking: 2 for the correct factor, 2 for demonstrating the Celsius error explicitly. The question
asks for both.*

---

### 20. *(5 pts)* RMS speeds at 300 K
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

### 21. *(3 pts)*
$$V = \frac{nRT}{P} = \frac{(1)(8.314)(273.15)}{1.013\times10^5} = 2.24\times10^{-2}~\text{m}^3 = \mathbf{22.4~\text{L}}$$

---

### 22. *(3 pts)* Two gases at the same temperature

**Average kinetic energies are equal.** $\tfrac12m\overline{v^2} = \tfrac32k_BT$ depends only on $T$,
not on the molecule.

**Average speeds are not.** Since the kinetic energies match, $v_{\text{rms}}\propto1/\sqrt m$, so the
lighter gas moves faster.

**Why they differ:** temperature is defined as a measure of kinetic *energy* per molecule, not of
speed. A heavy molecule achieves the same energy at lower speed.

---

*PHYS 141 · Week 11 · PS 11 Solutions · Instructor copy*
