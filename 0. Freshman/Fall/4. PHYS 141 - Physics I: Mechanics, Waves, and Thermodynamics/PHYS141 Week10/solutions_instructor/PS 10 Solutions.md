# PHYS 141 · Problem Set 10 Solutions
## INSTRUCTOR ONLY

**Total: 100 points.** All values verified computationally. $v = 343$ m/s, $I_0 = 10^{-12}$ W/m².

---

*Revised 2026-09-21 to match the 10-problem set; problems are numbered as in the new set.*

## Part A — Sound Waves and Intensity

### 1. *(10 pts)* $P = 2.00$ W at $r = 3.00$ m
$$I = \frac{2.00}{4\pi(3.00)^2} = \mathbf{1.77\times10^{-2}~\text{W/m}^2} \qquad \beta = 10\log_{10}\frac{1.77\times10^{-2}}{10^{-12}} = \mathbf{102~\text{dB}}$$

---

### 2. *(10 pts)*
$$\beta = 10\log_{10}\frac{4.00\times10^{-6}}{10^{-12}} = 10\log_{10}(4.00\times10^{6}) = \mathbf{66.0~\text{dB}}$$

---

### 3. *(10 pts)* 78.0 dB at 5.00 m
$$I = 10^{-12}\times10^{7.80} = 6.31\times10^{-5}~\text{W/m}^2$$
$$P = I(4\pi r^2) = 6.31\times10^{-5}\times4\pi(5.00)^2 = \mathbf{1.98\times10^{-2}~\text{W}}$$

At 20.0 m the distance is $4\times$ greater, so
$$\Delta\beta = 10\log_{10}\left(\tfrac{1}{16}\right) = -12.0~\text{dB} \qquad \beta_{20} = \mathbf{66.0~\text{dB}}$$

*Note how little power a loud sound requires — about 20 mW produces 78 dB at 5 m. Sound is
energetically cheap; this surprises students and is worth remarking on.*

---

## Part B — Decibels and Perception

### 4. *(10 pts)* Two 70 dB sources
Convert, add, convert back: each has $I = 10^{-5}$ W/m², so together $2\times10^{-5}$ W/m².
$$\beta = 10\log_{10}(2\times10^{7}) = \mathbf{73.0~\text{dB}}$$

**Not 140 dB** because decibels are **logarithms**, and logarithms do not add when the quantities they
represent do. Adding the dB values would correspond to *multiplying* the intensities — giving
$10^{14}I_0$, which is far above the threshold of pain.

*Marking: 2 for 73 dB, 2 for the explanation.*

---

## Part C — Air Columns and Resonance

### 5. *(10 pts)* Open–open, $L = 0.750$ m
$$f_n = \frac{nv}{2L} \;\Longrightarrow\; \mathbf{229~\text{Hz}},\; \mathbf{457~\text{Hz}},\; \mathbf{686~\text{Hz}}$$

---

### 6. *(10 pts)* Closed–open, $L = 0.750$ m
$$f_n = \frac{nv}{4L},\ n \text{ odd} \;\Longrightarrow\; \mathbf{114~\text{Hz}},\; \mathbf{343~\text{Hz}},\; \mathbf{572~\text{Hz}}$$

**Ratio of fundamentals:** $228.7/114.3 = \mathbf{2.00}$ — the open pipe sounds exactly one octave
higher for the same length.

*Marking: 3 for the harmonics, 2 for the ratio. Students who include even harmonics lose 2.*

---

### 7. *(10 pts)* Resonance tube, 384 Hz fork
Spacing: $0.663 - 0.216 = 0.447$ m $= \lambda/2$, so $\lambda = \mathbf{0.894~\text{m}}$.
$$v = f\lambda = 384\times0.894 = \mathbf{343~\text{m/s}}$$
End correction: $e = \lambda/4 - L_1 = 0.2235 - 0.216 = \mathbf{7.5\times10^{-3}~\text{m}}$.

*This is 7.5 mm, consistent with $0.6r$ for a tube of radius about 12 mm. Marking: 2 for $\lambda$
from the spacing, 2 for $v$, 2 for the correction.*

---

## Part D — The Doppler Effect

### 8. *(10 pts)* Train, 440 Hz at 30.0 m/s
**Prediction:** higher approaching, lower receding.
$$f'_{\text{app}} = 440\frac{343}{343-30} = \mathbf{482~\text{Hz}} \qquad f'_{\text{rec}} = 440\frac{343}{343+30} = \mathbf{405~\text{Hz}}$$
**Total drop: $\mathbf{77.6~\text{Hz}}$.**

*Note the shift is asymmetric: $+42.2$ Hz approaching, $-35.4$ Hz receding. Worth pointing out.*

---

### 9. *(10 pts)* Both moving towards each other
$$f' = 800\frac{343+20.0}{343-15.0} = \mathbf{885~\text{Hz}}$$

---

### 10. *(10 pts)* Bat and wall
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
