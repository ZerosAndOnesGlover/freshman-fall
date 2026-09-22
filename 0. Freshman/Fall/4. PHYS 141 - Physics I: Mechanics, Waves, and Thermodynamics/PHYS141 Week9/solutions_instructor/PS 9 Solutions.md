# PHYS 141 · Problem Set 9 Solutions
## INSTRUCTOR ONLY

**Total: 100 points.** All values verified computationally. $v_{\text{sound}} = 340$ m/s.

---

*Revised 2026-09-21 to match the 10-problem set; problems are numbered as in the new set.*

## Part A — Wave Properties

### 1. *(10 pts)* $f = 512$ Hz, $\lambda = 0.664$ m

$$v = f\lambda = \mathbf{340~\text{m/s}} \qquad T = 1/f = \mathbf{1.95\times10^{-3}~\text{s}}$$
$$k = 2\pi/\lambda = \mathbf{9.46~\text{rad/m}} \qquad \omega = 2\pi f = \mathbf{3.22\times10^{3}~\text{rad/s}}$$

---

### 2. *(10 pts)* $\mu = 8.00\times10^{-3}$ kg/m, $F_T = 120$ N

$$v = \sqrt{\frac{120}{8.00\times10^{-3}}} = \mathbf{122~\text{m/s}}$$

To double $v$, since $v\propto\sqrt{F_T}$, the tension must **quadruple** to $\mathbf{480~\text{N}}$.

**Practicality:** 480 N is roughly the weight of a 49 kg mass on a thin string. Most strings would
break first — which is why instruments change pitch by changing **length** (fretting), not tension.

*Marking: 2 speed, 2 tension, 1 comment. The factor of four is the point of the question.*

---

### 3. *(10 pts)* $y = 0.0200\sin(4.00x - 60.0t)$

$A = \mathbf{0.0200~\text{m}}$; $k = 4.00$ rad/m so $\lambda = 2\pi/k = \mathbf{1.57~\text{m}}$;
$\omega = 60.0$ rad/s so $f = \mathbf{9.55~\text{Hz}}$ and $T = \mathbf{0.105~\text{s}}$;
$v = \omega/k = \mathbf{15.0~\text{m/s}}$.

**Direction: $+x$**, because the sign between $kx$ and $\omega t$ is negative.

*Marking: 1 for direction, 4 for the six quantities. The commonest error is reading $k$ as $\lambda$.*

---

## Part B — Superposition and Interference

### 4. *(10 pts)* $A = 4.00$ cm each, $\phi = \pi/3$

$$A_{\text{res}} = 2A\cos(\phi/2) = 2(4.00)\cos(\pi/6) = \mathbf{6.93~\text{cm}}$$

Complete cancellation requires $\cos(\phi/2) = 0$, i.e. $\phi = \boldsymbol\pi$ (or any odd multiple).

---

### 5. *(10 pts)* $f = 500$ Hz, $\lambda = 340/500 = 0.680$ m

**(a) Constructive** ($\Delta d = m\lambda$): $\mathbf{0}$, $\mathbf{0.680}$, $\mathbf{1.36}$ m.

**(b) Destructive** ($\Delta d = (m+\tfrac12)\lambda$): $\mathbf{0.340}$, $\mathbf{1.02}$,
$\mathbf{1.70}$ m.

*Marking: 3 each. Students who omit $\Delta d = 0$ from the constructive list lose 1 — zero path
difference is the most constructive case of all.*

---

## Part C — Beats

### 6. *(10 pts)* 5 beats/s against 512 Hz

$f_{\text{beat}} = \lvert f_1-f_2\rvert = 5$, so the other fork is $\mathbf{507~\text{Hz}}$ or
$\mathbf{517~\text{Hz}}$ — the beat frequency alone cannot distinguish them.

**Experiment to decide:** load the unknown fork with a small mass of plasticine, which **lowers** its
frequency. If the beat rate **increases**, the fork was at 507 Hz (moving further below 512). If it
**decreases**, the fork was at 517 Hz (moving towards 512).

*Marking: 2 for both candidates, 3 for a workable discriminating experiment with correct reasoning.*

---

## Part D — Standing Waves

### 7. *(10 pts)* $L = 0.650$ m, $v = 240$ m/s

$$f_1 = \frac{v}{2L} = \mathbf{185~\text{Hz}}$$

Harmonics: $\mathbf{185}$, $\mathbf{369}$, $\mathbf{554}$, $\mathbf{738}$ Hz.

---

### 8. *(10 pts)* $f_3 = 420$ Hz

$f_n = nf_1$, so $f_1 = 420/3 = \mathbf{140~\text{Hz}}$ and $f_5 = 5(140) = \mathbf{700~\text{Hz}}$.

---

### 9. *(10 pts)* $L = 1.50$ m, $\mu = 4.00$ g/m, $F_T = 100$ N

$$v = \sqrt{\frac{100}{4.00\times10^{-3}}} = \mathbf{158~\text{m/s}} \qquad \lambda_1 = 2L = \mathbf{3.00~\text{m}} \qquad f_1 = \frac{v}{2L} = \mathbf{52.7~\text{Hz}}$$

---

### 10. *(10 pts)* Fretting 196 Hz up to 262 Hz

At fixed tension and $\mu$, $f\propto 1/L$, so

$$\frac{L'}{L} = \frac{196}{262} = 0.748$$

The vibrating length must be **74.8%** of the open length, so the fret sits
$1 - 0.748 = \mathbf{0.252}$ — about **25.2% of the string length from the nut**.

*(This is the interval of a perfect fourth, and 25.2% is very close to where the fifth fret sits on a
real guitar.)*

*Marking: 3 for the ratio, 2 for converting to a distance from the nut, 1 for stating which end.
Students who give 74.8% without saying from which end lose 2.*

---
