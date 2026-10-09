# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Lecture 28 — Wave Properties and the Wave Equation

*“The scale of light can be described by numbers — called the frequency — and as the numbers get higher, the light goes from red to blue to ultraviolet.”* — Richard Feynman, *QED: The Strange Theory of Light and Matter* (1985)

**Date:** Monday 23 November 2026 · 14:00–14:50 · Week 9

**Reading:** Serway & Jewett §16.1–16.5 · HRK Ch. 18

**Coursework:** 📊 **Quiz 8** today 14:00 · 🔬 **Lab 9** Thu 26 Nov 14:00–17:00 · 📝 **PS 8** due Fri 27 Nov 17:00 · 📝 **PS 9** released Fri 27 Nov 15:00, due Fri 4 Dec 17:00

---

## Where This Fits

Week 8 studied a single oscillator. Now couple many of them together — atoms in a string, molecules
in air, charges in a wire — so that each one drives its neighbours.

The result is a **wave**: a disturbance that travels while the medium itself does not. Everything from
Week 8 survives, with one addition. An oscillator's state is a function of time alone, $x(t)$; a
wave's is a function of position *and* time, $y(x,t)$. That single extra variable is the whole
difference.

---

## 1. What a Wave Transports

> **A wave transports energy and momentum through a medium without transporting the medium.**

Watch a cork on rippled water: it bobs up and down and stays put. The wave crosses the pond; the water
does not. This is the single most important idea of the week and the one most often lost.

### Two kinds

| Type | Oscillation direction | Examples |
|---|---|---|
| **Transverse** | Perpendicular to travel | String, light, S-waves |
| **Longitudinal** | Parallel to travel | Sound, P-waves, spring compressions |

Sound in air is longitudinal because a gas has no shear stiffness — it cannot resist a sideways
displacement, so no transverse wave can propagate. Solids resist both, which is why earthquakes
produce two wave types arriving at different times, and why the delay tells you how far away the
epicentre is.

---

## 2. Describing a Harmonic Wave

$$\boxed{y(x,t) = A\sin(kx - \omega t + \phi)}$$

| Symbol | Name | Definition |
|---|---|---|
| $A$ | Amplitude | Maximum displacement |
| $\lambda$ | Wavelength | Distance per cycle (m) |
| $k$ | Wave number | $k = 2\pi/\lambda$ (rad/m) |
| $T$ | Period | Time per cycle (s) |
| $f$ | Frequency | $f = 1/T$ (Hz) |
| $\omega$ | Angular frequency | $\omega = 2\pi f$ (rad/s) |

**Two views of the same function:**

- Freeze time and $y$ varies sinusoidally in **space**, with period $\lambda$.
- Stand at one $x$ and $y$ varies sinusoidally in **time**, with period $T$ — you are watching a
  Week 8 oscillator.

**The minus sign in $(kx-\omega t)$ means the wave moves in $+x$.** A point of constant phase requires
$kx - \omega t$ constant, so $x$ must increase as $t$ does. A plus sign gives leftward travel.

### The wave relation

A wave advances one wavelength in one period:

$$\boxed{v = \frac{\lambda}{T} = f\lambda = \frac{\omega}{k}}$$

**Verified:** $f = 250$ Hz and $\lambda = 1.36$ m give $v = 340$ m/s — the speed of sound in air.

| Wave | $v$ (m/s) | $f$ | $\lambda$ |
|---|---|---|---|
| Sound (air), concert A | 340 | 440 Hz | 0.773 m |
| Ultrasound (tissue) | 1500 | 1.0 MHz | 1.5 mm |
| FM radio | $3.00\times10^8$ | 100 MHz | 3.00 m |

> **The ultrasound row explains medical imaging.** Resolution is limited by wavelength, so 1.5 mm
> features are about the practical limit at 1 MHz. Higher frequency gives finer detail but penetrates
> less deeply — the fundamental trade-off in every ultrasound scan.

---

## 3. What Determines Wave Speed

> **The speed is set by the medium, not by the source.**

For a stretched string:

$$\boxed{v = \sqrt{\frac{F_T}{\mu}}}$$

with $F_T$ the tension and $\mu = m/L$ the mass per unit length.

**The structure is familiar.** It is Week 8's $\omega = \sqrt{\text{stiffness}/\text{inertia}}$ again:
tension is the restoring agent, linear density the inertia. Every wave-speed formula in physics has
this shape.

### Worked example — verified

A string with $F_T = 80.0$ N and $\mu = 5.00\times10^{-3}$ kg/m:

$$v = \sqrt{\frac{80.0}{5.00\times10^{-3}}} = \mathbf{126.5~\text{m/s}}$$

**Quadruple the tension** and the speed only **doubles** — $v \propto \sqrt{F_T}$. This is why tuning
a guitar string requires large tension changes for modest pitch changes, and why over-tightening
snaps strings before it achieves much.

> **Changing the source frequency does not change $v$.** Play a higher note on the same string and
> $f$ rises while $\lambda$ falls, keeping $f\lambda = v$ fixed. **Frequency is set by the source;
> speed by the medium; wavelength is whatever the two force it to be.**

---

## 4. Energy and Power

A wave carries the energy of every oscillating element. For a string,

$$P = \tfrac12\mu v\omega^2A^2$$

**Note the two squares.** Power goes as **amplitude squared** and as **frequency squared**.

**Verified:** the string above, with $A = 5.00$ mm at $f = 100$ Hz, carries $P = \mathbf{3.12~\text{W}}$.
Double the amplitude and it carries $12.5$ W — **four times**, not twice.

> This quadratic dependence recurs everywhere: the intensity of light, the loudness of sound, the
> power in an AC circuit. It is why Week 10 measures sound on a logarithmic scale — the linear range
> is far too wide to be useful.

---

## 5. The Wave Equation

Substituting $y = A\sin(kx-\omega t)$ into its own second derivatives gives

$$\frac{\partial^2 y}{\partial x^2} = \frac{1}{v^2}\frac{\partial^2 y}{\partial t^2}$$

**Any** function of the form $y = f(x - vt)$ satisfies this — not just sinusoids. A pulse of any shape
travels undistorted at speed $v$.

This is the wave equation, and it appears throughout physics: for strings, for sound, and — with
$v = c$ — for light, where it falls out of Maxwell's equations. **Finding it there, with $c$ emerging
from purely electrical constants, is what told Maxwell that light is an electromagnetic wave.**

---

## 6. Summary

| | |
|---|---|
| A wave transports | energy and momentum, **not** the medium |
| Transverse / longitudinal | oscillation ⊥ / ∥ to travel |
| Harmonic wave | $y = A\sin(kx-\omega t+\phi)$ |
| $k$, $\omega$ | $2\pi/\lambda$, $2\pi f$ |
| Wave relation | $v = f\lambda = \omega/k$ |
| Direction | $(kx-\omega t)$ → $+x$; $(kx+\omega t)$ → $-x$ |
| String speed | $v = \sqrt{F_T/\mu}$, so $v\propto\sqrt{F_T}$ |
| Speed set by | the **medium**; frequency by the **source** |
| Power | $P = \tfrac12\mu v\omega^2A^2$ — goes as $A^2$ and $f^2$ |
| Wave equation | $\partial_x^2 y = v^{-2}\partial_t^2 y$ |

---

## 7. Conceptual Questions

1. A wave travels along a rope. Does a point on the rope move in the direction of travel? What *is* transported?

2. You double the frequency of the source driving a string. What happens to $v$, $\lambda$, and $f$?

3. Why is sound in air longitudinal but a wave on a string transverse?

4. Two strings have the same tension, but one is twice as massive per unit length. Which carries waves faster, and by what factor?

5. Why do earthquakes produce two distinct arrivals at a seismograph, and how does the delay give distance?

---

## 8. Problems

1. A wave has $f = 512$ Hz and $\lambda = 0.664$ m. Find $v$, $T$, $k$, and $\omega$.

2. A string has $\mu = 8.00$ g/m under 120 N of tension. Find the wave speed. What tension would double it?

3. A wave is described by $y = (0.0200~\text{m})\sin(4.00x - 60.0t)$ in SI units. Find $A$, $\lambda$, $f$, $T$, $v$, and the direction of travel.

4. A 2.50 m string of mass 12.0 g is under 150 N tension. Find $v$, and the time for a pulse to travel its length.

5. A string wave has $A = 3.00$ mm, $f = 120$ Hz, $\mu = 6.00$ g/m, and $v = 90.0$ m/s. Find the transmitted power. What amplitude would triple it?

---

*Next: Lecture 29 — Superposition and Interference*
