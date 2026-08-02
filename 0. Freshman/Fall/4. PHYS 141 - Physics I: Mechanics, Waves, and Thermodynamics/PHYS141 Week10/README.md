# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Week 10: Sound — Doppler Effect, Resonance & Decibels

**Semester:** Fall | **Credits:** 4 | **Lab:** Weekly 3-hr lab session

---

## Week 10 Contents

| File | Description |
|------|-------------|
| `lectures/L31 Sound Waves and Intensity.md` | Longitudinal pressure waves; speed vs temperature; intensity, inverse-square law, and the decibel scale |
| `lectures/L32 Air Columns and Resonance.md` | Boundary conditions in pipes; open–open and closed–open harmonics; end correction; the resonance tube |
| `lectures/L33 The Doppler Effect.md` | Moving sources and observers; why they differ; shock waves and the Mach cone |
| `lab/LAB 10 Speed of Sound and Resonance.md` | $v$ from a resonance tube; end correction; inverse-square law with a level meter; Doppler from a swung speaker |
| `assignments/PS 10 Sound Doppler Resonance and Decibels.md` | 22 problems on intensity, decibels, air columns, and Doppler |
| `quiz/QUIZ 10 Sound Doppler Resonance and Decibels.md` | 10-question quiz (administered Monday, Week 11) |
| `resources/Resources.md` | Textbook references, simulations, deeper reading |
| `solutions_instructor/PS 10 Solutions.md` | Full worked solutions (instructor only) |
| `solutions_instructor/LAB 10 Solutions.md` | Expected data, analysis answers, systematic errors to look for |

---

## Learning Objectives

By the end of Week 10, you will be able to:

1. Explain why sound in a gas must be longitudinal
2. Relate the displacement and pressure descriptions of a sound wave and state their 90° phase relationship
3. Compute the speed of sound from temperature, and explain why pressure does not enter
4. Apply $I = P/4\pi r^2$ and the inverse-square law
5. Convert between intensity and sound level, and use the $+3$ dB, $+10$ dB, and $-6$ dB rules fluently
6. Explain why a logarithmic scale is used, in terms of both dynamic range and ear response
7. State the displacement boundary conditions at open and closed pipe ends
8. Derive $f_n = nv/2L$ for open–open and $f_n = nv/4L$ (odd $n$) for closed–open pipes
9. Explain why a closed pipe sounds an octave lower and has a different timbre
10. Apply the end correction and explain why taking differences eliminates it
11. Apply the Doppler formula with correct signs, checking the direction of every shift
12. Explain why a moving source and a moving observer are not equivalent, and what changes for light
13. Compute the Mach cone angle and describe how a sonic boom propagates

---

## Schedule

| Day | Activity |
|-----|----------|
| Monday | Lecture 31 — Sound Waves and Intensity |
| Tuesday | Lecture 32 — Air Columns and Resonance |
| Friday | Lecture 33 — The Doppler Effect |
| Thursday | Lab 10 — Speed of Sound and Resonance (3 hrs) |
| Friday EOD | Problem Set 10 released |

---

## Key Results

| | |
|---|---|
| Sound | longitudinal pressure wave; displacement and pressure 90° out of phase |
| Speed in air | $v \approx 331+0.6T_C$; **343 m/s** at room temperature |
| Depends on | temperature, **not** pressure |
| Intensity | $I = P/4\pi r^2 \propto A^2$ |
| Decibels | $\beta = 10\log_{10}(I/I_0)$, $I_0 = 10^{-12}$ W/m² |
| $\times2$, $\times10$ intensity | $+3.01$ dB, $+10$ dB |
| Doubling distance | $-6.02$ dB |
| Twice as loud | about $+10$ dB |
| Open–open pipe | $f_n = nv/2L$ — all harmonics |
| Closed–open pipe | $f_n = nv/4L$, **odd $n$ only** |
| Closed pipe fundamental | **half** the open pipe of equal length |
| Clarinet vs flute | odd-only vs all harmonics ⟹ different timbre |
| End correction | $L_{\text{eff}} = L + 0.6r$; cancels in differences |
| Doppler | $f' = f(v+v_o)/(v-v_s)$ |
| **The check** | approaching ⟹ higher; receding ⟹ lower |
| Source ≠ observer | the medium breaks the symmetry |
| Mach cone | $\sin\theta = 1/M$ |

---

## Connections

**Back:** Week 9's standing waves transfer directly to air columns — only the boundary conditions
change. The $I\propto A^2$ dependence is Week 9's $P\propto A^2$, and it is what makes the decibel
scale necessary. Week 8's resonance is what a pipe does at $f_n$.

**Forward:** Week 11 turns to thermodynamics, where the temperature that set the speed of sound this
week becomes the central variable, and the molecular motion behind it is made explicit.

**Sideways:** the Doppler effect for light underpins astronomical redshift and hence the expanding
universe. The decibel scale reappears throughout engineering — in signal-to-noise ratios, amplifier
gain, and antenna performance — always as $10\log_{10}$ of a power ratio.
