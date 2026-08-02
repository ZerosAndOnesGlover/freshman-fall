# PHYS 141 · Problem Set 9 Solutions
## INSTRUCTOR ONLY

**Total: 100 points.** All values verified computationally. $v_{\text{sound}} = 340$ m/s.

---

## Part A — Wave Properties

### 1. *(5 pts)* $f = 512$ Hz, $\lambda = 0.664$ m

$$v = f\lambda = \mathbf{340~\text{m/s}} \qquad T = 1/f = \mathbf{1.95\times10^{-3}~\text{s}}$$
$$k = 2\pi/\lambda = \mathbf{9.46~\text{rad/m}} \qquad \omega = 2\pi f = \mathbf{3.22\times10^{3}~\text{rad/s}}$$

---

### 2. *(5 pts)* $\mu = 8.00\times10^{-3}$ kg/m, $F_T = 120$ N

$$v = \sqrt{\frac{120}{8.00\times10^{-3}}} = \mathbf{122~\text{m/s}}$$

To double $v$, since $v\propto\sqrt{F_T}$, the tension must **quadruple** to $\mathbf{480~\text{N}}$.

**Practicality:** 480 N is roughly the weight of a 49 kg mass on a thin string. Most strings would
break first — which is why instruments change pitch by changing **length** (fretting), not tension.

*Marking: 2 speed, 2 tension, 1 comment. The factor of four is the point of the question.*

---

### 3. *(5 pts)* $y = 0.0200\sin(4.00x - 60.0t)$

$A = \mathbf{0.0200~\text{m}}$; $k = 4.00$ rad/m so $\lambda = 2\pi/k = \mathbf{1.57~\text{m}}$;
$\omega = 60.0$ rad/s so $f = \mathbf{9.55~\text{Hz}}$ and $T = \mathbf{0.105~\text{s}}$;
$v = \omega/k = \mathbf{15.0~\text{m/s}}$.

**Direction: $+x$**, because the sign between $kx$ and $\omega t$ is negative.

*Marking: 1 for direction, 4 for the six quantities. The commonest error is reading $k$ as $\lambda$.*

---

### 4. *(5 pts)* $L = 2.50$ m, $m = 12.0$ g, $F_T = 150$ N

$$\mu = \frac{0.0120}{2.50} = 4.80\times10^{-3}~\text{kg/m} \qquad v = \sqrt{\frac{150}{4.80\times10^{-3}}} = \mathbf{177~\text{m/s}}$$

$$t = \frac{L}{v} = \frac{2.50}{176.8} = \mathbf{1.41\times10^{-2}~\text{s}}$$

*Watch for students using $m = 12.0$ g as $\mu$ directly — it must be divided by the length.*

---

### 5. *(5 pts)* $A = 3.00$ mm, $f = 120$ Hz, $\mu = 6.00$ g/m, $v = 90.0$ m/s

$\omega = 2\pi(120) = 754.0$ rad/s.

$$P = \tfrac12\mu v\omega^2A^2 = \tfrac12(6.00\times10^{-3})(90.0)(754.0)^2(3.00\times10^{-3})^2 = \mathbf{1.38~\text{W}}$$

To triple $P$, since $P\propto A^2$, we need $A\to\sqrt3 A = \mathbf{5.20~\text{mm}}$.

*Marking: 3 for the power, 2 for the $\sqrt3$ scaling. Answering $9.00$ mm (tripling $A$) is the
standard error.*

---

## Part B — Superposition and Interference

### 6. *(5 pts)* $A = 4.00$ cm each, $\phi = \pi/3$

$$A_{\text{res}} = 2A\cos(\phi/2) = 2(4.00)\cos(\pi/6) = \mathbf{6.93~\text{cm}}$$

Complete cancellation requires $\cos(\phi/2) = 0$, i.e. $\phi = \boldsymbol\pi$ (or any odd multiple).

---

### 7. *(6 pts)* $f = 500$ Hz, $\lambda = 340/500 = 0.680$ m

**(a) Constructive** ($\Delta d = m\lambda$): $\mathbf{0}$, $\mathbf{0.680}$, $\mathbf{1.36}$ m.

**(b) Destructive** ($\Delta d = (m+\tfrac12)\lambda$): $\mathbf{0.340}$, $\mathbf{1.02}$,
$\mathbf{1.70}$ m.

*Marking: 3 each. Students who omit $\Delta d = 0$ from the constructive list lose 1 — zero path
difference is the most constructive case of all.*

---

### 8. *(6 pts)* Speakers, $f = 1.20$ kHz, distances 4.00 m and 4.85 m

$$\lambda = \frac{340}{1200} = 0.2833~\text{m} \qquad \Delta d = 4.85 - 4.00 = 0.850~\text{m}$$

$$\frac{\Delta d}{\lambda} = \frac{0.850}{0.2833} = \mathbf{3.00}$$

An exact whole number of wavelengths, so the interference is **constructive** — this is a **loud**
position.

*Marking: 2 for $\lambda$, 2 for the ratio, 2 for the conclusion. The ratio must be computed; guessing
from the raw distances earns nothing.*

---

### 9. *(4 pts)* Where the energy goes

**It is redistributed, not destroyed.** Two waves cannot cancel everywhere — where they interfere
destructively at one location, they necessarily interfere constructively elsewhere, and the amplitude
there is $2A$ rather than $A$.

Since energy goes as amplitude squared, a region of amplitude $2A$ carries **four times** the energy
of a single wave, not twice. Integrated over all space, the total equals the sum of what the two
sources emitted, and conservation holds exactly.

*Marking: 2 for redistribution, 2 for the $A^2$ argument. "It cancels out" earns 0 — that is the
misconception the question targets.*

---

### 10. *(4 pts)* Reflection

**Fixed end:** the pulse returns **inverted** — a crest comes back as a trough. The end cannot move,
so incident and reflected displacements must sum to zero there at all times, which requires the
reflected wave to be the negative of the incident one (a $\pi$ phase change).

**Free end:** the pulse returns **upright**, with no inversion. The end is free to move, and in fact
overshoots to twice the incident amplitude momentarily.

*Marking: 1 per sketch, 1 per explanation.*

---

## Part C — Beats

### 11. *(5 pts)* 5 beats/s against 512 Hz

$f_{\text{beat}} = \lvert f_1-f_2\rvert = 5$, so the other fork is $\mathbf{507~\text{Hz}}$ or
$\mathbf{517~\text{Hz}}$ — the beat frequency alone cannot distinguish them.

**Experiment to decide:** load the unknown fork with a small mass of plasticine, which **lowers** its
frequency. If the beat rate **increases**, the fork was at 507 Hz (moving further below 512). If it
**decreases**, the fork was at 517 Hz (moving towards 512).

*Marking: 2 for both candidates, 3 for a workable discriminating experiment with correct reasoning.*

---

### 12. *(5 pts)* 4 beats/s against 330 Hz; beats slow on loosening

Candidates: 326 Hz or 334 Hz.

Loosening the string **lowers** its frequency. The beats **slowed**, so the string moved **towards**
330 Hz — it must have been **above** it.

$$\text{The string was \textbf{sharp}, at }\mathbf{334~\text{Hz}}$$

*Marking: 2 for the candidates, 3 for the reasoning. This is Problem 11's experiment applied.*

---

### 13. *(5 pts)* Derivation

$$y = A\cos(2\pi f_1t) + A\cos(2\pi f_2t) = 2A\cos\left(2\pi\frac{f_1-f_2}{2}t\right)\cos\left(2\pi\frac{f_1+f_2}{2}t\right)$$

The second factor is a rapid oscillation at the **average** frequency; the first is a slow envelope at
$\lvert f_1-f_2\rvert/2$.

**Why the audible rate is the difference, not half of it:** loudness depends on the *magnitude* of the
envelope, not its sign. The envelope $\cos(2\pi f_{\text{env}}t)$ reaches maximum magnitude **twice**
per cycle — once at $+1$ and once at $-1$ — so the ear hears

$$f_{\text{beat}} = 2 \times \frac{\lvert f_1-f_2\rvert}{2} = \lvert f_1-f_2\rvert$$

*Marking: 3 for the algebra, 2 for the factor-of-two argument. This is the most commonly bungled
derivation in the topic; the identity alone earns 3.*

---

## Part D — Standing Waves

### 14. *(5 pts)* $L = 0.650$ m, $v = 240$ m/s

$$f_1 = \frac{v}{2L} = \mathbf{185~\text{Hz}}$$

Harmonics: $\mathbf{185}$, $\mathbf{369}$, $\mathbf{554}$, $\mathbf{738}$ Hz.

---

### 15. *(5 pts)* $f_3 = 420$ Hz

$f_n = nf_1$, so $f_1 = 420/3 = \mathbf{140~\text{Hz}}$ and $f_5 = 5(140) = \mathbf{700~\text{Hz}}$.

---

### 16. *(6 pts)* $L = 1.50$ m, $\mu = 4.00$ g/m, $F_T = 100$ N

$$v = \sqrt{\frac{100}{4.00\times10^{-3}}} = \mathbf{158~\text{m/s}} \qquad \lambda_1 = 2L = \mathbf{3.00~\text{m}} \qquad f_1 = \frac{v}{2L} = \mathbf{52.7~\text{Hz}}$$

---

### 17. *(5 pts)* $L = 0.800$ m, fourth harmonic

$\lambda_4 = 2L/4 = 0.400$ m, so nodes are $\lambda/2 = 0.200$ m apart.

**Nodes:** $0$, $0.200$, $0.400$, $0.600$, $0.800$ m — **five** of them.
**Antinodes:** $0.100$, $0.300$, $0.500$, $0.700$ m — **four**.

*Consistent with $n+1$ nodes and $n$ antinodes.*

---

### 18. *(6 pts)* Fretting 196 Hz up to 262 Hz

At fixed tension and $\mu$, $f\propto 1/L$, so

$$\frac{L'}{L} = \frac{196}{262} = 0.748$$

The vibrating length must be **74.8%** of the open length, so the fret sits
$1 - 0.748 = \mathbf{0.252}$ — about **25.2% of the string length from the nut**.

*(This is the interval of a perfect fourth, and 25.2% is very close to where the fifth fret sits on a
real guitar.)*

*Marking: 3 for the ratio, 2 for converting to a distance from the nut, 1 for stating which end.
Students who give 74.8% without saying from which end lose 2.*

---

### 19. *(4 pts)* 440 Hz to 494 Hz by tension

$f\propto\sqrt{F_T}$, so

$$\frac{F_T'}{F_T} = \left(\frac{494}{440}\right)^2 = \mathbf{1.26}$$

a **26% increase** for one whole tone.

**Practicality:** tuning by tension works over a narrow range — a semitone or two — which is exactly
what tuning pegs are for. Covering an octave would need **four times** the tension, so instruments
change pitch by length or by using different strings instead.

---

### 20. *(4 pts)* Why quantised

A string fixed at both ends **must** have a node at each end — the clamps physically prevent motion
there. A standing wave can only exist if a whole number of half-wavelengths fits between them:
$L = n\lambda/2$.

Since $v$ is fixed by the medium, constraining $\lambda$ constrains $f$, giving the discrete ladder
$f_n = nv/2L$.

An **unbounded** string has no such requirement. Any wavelength propagates, so any frequency is
allowed.

**The quantiser is the boundary condition**, not the wave equation. Confinement is what produces
discreteness — the same mechanism that gives atoms discrete energy levels.

*Marking: 2 for the boundary condition, 1 for the integer requirement, 1 for the contrast with the
unbounded case.*

---

*PHYS 141 · Week 9 · PS 9 Solutions · Instructor copy*
