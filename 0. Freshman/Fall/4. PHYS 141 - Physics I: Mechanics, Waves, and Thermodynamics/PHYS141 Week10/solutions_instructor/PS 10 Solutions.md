# PHYS 141 · Problem Set 10 Solutions
## INSTRUCTOR ONLY

**Total: 100 points.** All values verified computationally. $v = 343$ m/s, $I_0 = 10^{-12}$ W/m².

---

## Part A — Sound Waves and Intensity

### 1. *(4 pts)*
$$v(15°) = 331\sqrt{1+15/273.15} = \mathbf{340~\text{m/s}} \qquad v(35°) = \mathbf{352~\text{m/s}}$$

**Why pressure is absent:** raising the pressure of a gas increases both its stiffness (bulk modulus)
and its density in the same proportion. Since $v=\sqrt{B/\rho}$, the two effects cancel exactly.
Temperature raises the molecular speeds without adding molecules, so it does change $v$.

*Marking: 2 for the values, 2 for the explanation. "Because the formula has no $P$ in it" earns 0 —
the question asks why.*

---

### 2. *(5 pts)* $P = 2.00$ W at $r = 3.00$ m
$$I = \frac{2.00}{4\pi(3.00)^2} = \mathbf{1.77\times10^{-2}~\text{W/m}^2} \qquad \beta = 10\log_{10}\frac{1.77\times10^{-2}}{10^{-12}} = \mathbf{102~\text{dB}}$$

---

### 3. *(4 pts)*
$$\beta = 10\log_{10}\frac{4.00\times10^{-6}}{10^{-12}} = 10\log_{10}(4.00\times10^{6}) = \mathbf{66.0~\text{dB}}$$

---

### 4. *(4 pts)* 65 dB → 85 dB
A rise of 20 dB is a factor of $10^{20/10} = \mathbf{100}$ in intensity.

**Perceived loudness:** roughly 10 dB corresponds to a doubling of perceived loudness, so 20 dB sounds
about **four times** as loud — not 100 times.

*Marking: 2 for the factor of 100, 2 for the perceptual answer. The gap between the two is the point.*

---

### 5. *(5 pts)* 78.0 dB at 5.00 m
$$I = 10^{-12}\times10^{7.80} = 6.31\times10^{-5}~\text{W/m}^2$$
$$P = I(4\pi r^2) = 6.31\times10^{-5}\times4\pi(5.00)^2 = \mathbf{1.98\times10^{-2}~\text{W}}$$

At 20.0 m the distance is $4\times$ greater, so
$$\Delta\beta = 10\log_{10}\left(\tfrac{1}{16}\right) = -12.0~\text{dB} \qquad \beta_{20} = \mathbf{66.0~\text{dB}}$$

*Note how little power a loud sound requires — about 20 mW produces 78 dB at 5 m. Sound is
energetically cheap; this surprises students and is worth remarking on.*

---

### 6. *(3 pts)* $f = 500$ Hz, $\lambda = 0.686$ m
$$v = f\lambda = 343~\text{m/s} \;\Longrightarrow\; 343 = 331\sqrt{1+T_C/273.15} \;\Longrightarrow\; T_C = \mathbf{20.2°\text{C}}$$

---

## Part B — Decibels and Perception

### 7. *(4 pts)* Two 70 dB sources
Convert, add, convert back: each has $I = 10^{-5}$ W/m², so together $2\times10^{-5}$ W/m².
$$\beta = 10\log_{10}(2\times10^{7}) = \mathbf{73.0~\text{dB}}$$

**Not 140 dB** because decibels are **logarithms**, and logarithms do not add when the quantities they
represent do. Adding the dB values would correspond to *multiplying* the intensities — giving
$10^{14}I_0$, which is far above the threshold of pain.

*Marking: 2 for 73 dB, 2 for the explanation.*

---

### 8. *(4 pts)*
$$\Delta\beta = 10\log_{10}\frac{2I}{I} = 10\log_{10}2 = \mathbf{3.01~\text{dB}}$$
The starting intensity cancels, so the increment is the same at every level. ∎

---

### 9. *(4 pts)* 2.00 m → 8.00 m
Distance $\times4$, so intensity $\times\tfrac{1}{16}$:
$$\Delta\beta = 10\log_{10}\tfrac{1}{16} = \mathbf{-12.0~\text{dB}}$$

**General rule:** doubling $r$ gives $I\to I/4$, so
$\Delta\beta = 10\log_{10}(1/4) = -6.02$ dB. Two doublings give $-12.0$ dB ✓

---

### 10. *(3 pts)*
Two reasons, and both are needed for full marks.

**Range:** audible intensities span $10^{-12}$ to $1$ W/m² — twelve orders of magnitude. No linear
axis can display that usefully.

**Perception:** the ear responds roughly logarithmically, so equal *ratios* of intensity produce
equal steps in perceived loudness. A logarithmic scale therefore matches how loudness actually feels,
which a linear one does not.

---

## Part C — Air Columns and Resonance

### 11. *(5 pts)* Open–open, $L = 0.750$ m
$$f_n = \frac{nv}{2L} \;\Longrightarrow\; \mathbf{229~\text{Hz}},\; \mathbf{457~\text{Hz}},\; \mathbf{686~\text{Hz}}$$

---

### 12. *(5 pts)* Closed–open, $L = 0.750$ m
$$f_n = \frac{nv}{4L},\ n \text{ odd} \;\Longrightarrow\; \mathbf{114~\text{Hz}},\; \mathbf{343~\text{Hz}},\; \mathbf{572~\text{Hz}}$$

**Ratio of fundamentals:** $228.7/114.3 = \mathbf{2.00}$ — the open pipe sounds exactly one octave
higher for the same length.

*Marking: 3 for the harmonics, 2 for the ratio. Students who include even harmonics lose 2.*

---

### 13. *(5 pts)* Closed–open, $f_1 = 220$ Hz
$$L = \frac{v}{4f_1} = \mathbf{0.390~\text{m}}$$
Next harmonics are the **odd** multiples: $f_3 = \mathbf{660~\text{Hz}}$, $f_5 = \mathbf{1100~\text{Hz}}$.

*A student answering 440 Hz has assumed all harmonics are present — the single most common error in
Part C.*

---

### 14. *(6 pts)* Resonance tube, 384 Hz fork
Spacing: $0.663 - 0.216 = 0.447$ m $= \lambda/2$, so $\lambda = \mathbf{0.894~\text{m}}$.
$$v = f\lambda = 384\times0.894 = \mathbf{343~\text{m/s}}$$
End correction: $e = \lambda/4 - L_1 = 0.2235 - 0.216 = \mathbf{7.5\times10^{-3}~\text{m}}$.

*This is 7.5 mm, consistent with $0.6r$ for a tube of radius about 12 mm. Marking: 2 for $\lambda$
from the spacing, 2 for $v$, 2 for the correction.*

---

### 15. *(5 pts)* Open pipe, $L = 0.400$ m, $r = 12.0$ mm
Without correction: $f_1 = v/2L = \mathbf{429~\text{Hz}}$.
With correction, an open pipe has **two** open ends, so $L_{\text{eff}} = L + 2(0.6r) = 0.4144$ m:
$$f_1 = \frac{343}{2(0.4144)} = \mathbf{414~\text{Hz}}$$
Difference: $\mathbf{3.5\%}$.

*Marking: 2 uncorrected, 2 corrected, 1 percentage. **Applying only one end correction is the trap** —
an open–open pipe needs two.*

---

### 16. *(4 pts)* Clarinet vs flute
A **flute** is open at both ends, so $f_n = nv/2L$ with **all** harmonics present. Overblowing excites
the next mode, $2f_1$ — an **octave**.

A **clarinet** is effectively closed at the reed end and open at the bell, so $f_n = nv/4L$ with
**odd $n$ only**. The next available mode above $f_1$ is $3f_1$ — a **twelfth**.

The boundary conditions differ because the reed end is a pressure antinode (displacement node), while
both ends of a flute are open.

*Marking: 2 for the harmonic series in each case, 2 for tying it to the boundary conditions.*

---

## Part D — The Doppler Effect

### 17. *(5 pts)* Train, 440 Hz at 30.0 m/s
**Prediction:** higher approaching, lower receding.
$$f'_{\text{app}} = 440\frac{343}{343-30} = \mathbf{482~\text{Hz}} \qquad f'_{\text{rec}} = 440\frac{343}{343+30} = \mathbf{405~\text{Hz}}$$
**Total drop: $\mathbf{77.6~\text{Hz}}$.**

*Note the shift is asymmetric: $+42.2$ Hz approaching, $-35.4$ Hz receding. Worth pointing out.*

---

### 18. *(5 pts)* Observer at 25.0 m/s towards a 500 Hz siren
$$f'_{\text{towards}} = 500\frac{343+25}{343} = \mathbf{536~\text{Hz}} \qquad f'_{\text{away}} = 500\frac{343-25}{343} = \mathbf{464~\text{Hz}}$$

*Here the shifts **are** symmetric ($\pm36.4$ Hz), because $v_o$ appears linearly in the numerator.
Contrast with Problem 17. This pair of problems exists to expose that asymmetry.*

---

### 19. *(5 pts)* Both moving towards each other
$$f' = 800\frac{343+20.0}{343-15.0} = \mathbf{885~\text{Hz}}$$

---

### 20. *(5 pts)* Working backwards
$$1050 = f\frac{343}{343-22.0} \;\Longrightarrow\; f = 1050\times\frac{321}{343} = \mathbf{983~\text{Hz}}$$

*Marking: full marks require rearranging correctly. A student who multiplies instead of dividing gets
1122 Hz — which fails the sanity check, since the true frequency must be **lower** than what an
approaching observer hears.*

---

### 21. *(6 pts)* Bat and wall
**(a) At the wall.** The bat is a moving source, the wall a stationary observer:
$$f_{\text{wall}} = 45000\frac{343}{343-8.00} = \mathbf{46{,}075~\text{Hz}}$$

**(b) Back at the bat.** The wall now re-radiates at $f_{\text{wall}}$ as a **stationary source**, and
the bat is a **moving observer** approaching it:
$$f_{\text{bat}} = 46075\frac{343+8.00}{343} = \mathbf{47{,}149~\text{Hz}}$$

**Why two shifts:** the wall first *receives* a shifted frequency, then *re-emits* that shifted
frequency, which the moving bat shifts again on reception. The roles swap between the two stages.

**Beat frequency against its own call:** $47149 - 45000 = \mathbf{2149~\text{Hz}}$.

*Bats really do use this: the beat frequency is proportional to closing speed, so the bat measures
how fast it is approaching prey. Marking: 2 + 2 for the frequencies, 1 for the two-stage explanation,
1 for the beat.*

---

### 22. *(4 pts)* Why source and observer differ
A **moving source** physically alters the wave in the medium — it bunches the wavefronts, changing
$\lambda$. This puts $v_s$ in the **denominator**, so the effect is nonlinear in $v_s$.

A **moving observer** does not affect the wave at all. The wavelength in the air is unchanged; the
observer merely encounters crests at a different rate. This puts $v_o$ in the **numerator**, linearly.

**The medium breaks the symmetry.** "Moving" means moving relative to the air, so the two situations
are physically distinct.

**For light there is no medium.** The relativistic Doppler formula depends only on the *relative*
velocity, and the asymmetry disappears. Historically, the failure to detect a medium for light was
among the observations leading to special relativity.

*Marking: 3 for the acoustic asymmetry, 1 for the contrast with light.*

---

*PHYS 141 · Week 10 · PS 10 Solutions · Instructor copy*
