# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Lecture 29 — Superposition and Interference

**Date:** Tuesday 20 October 2026 · 14:00–14:50 · Week 9

---

## Where This Fits

Lecture 28 described one wave. This lecture asks what happens when two arrive at the same place —
and the answer is the reason waves behave unlike anything in Weeks 0–7.

Two billiard balls cannot occupy the same point. Two waves can, and the result is not a collision but
an **addition**. Everything distinctive about waves — interference, beats, standing waves,
diffraction, the whole of optics and acoustics — follows from that one fact.

---

## 1. The Superposition Principle

> **When two or more waves overlap, the resultant displacement at every point is the algebraic sum of
> the individual displacements.**

$$y_{\text{total}}(x,t) = y_1(x,t) + y_2(x,t)$$

**And afterwards the waves pass through unchanged.** Two pulses meeting on a rope combine, then
separate and continue as if nothing had happened. This is why you can hold a conversation across a
crowded room: thousands of sound waves cross the same air, add momentarily at your ear, and emerge
undistorted.

**Why it holds:** the wave equation is *linear* — no $y^2$ or $y\,\partial y/\partial x$ terms — so
any sum of solutions is itself a solution. Superposition fails for very large amplitudes, where
nonlinear terms matter. That is why a shock wave from an explosion behaves differently from ordinary
sound.

---

## 2. Interference of Two Identical Waves

Take two waves of the same amplitude and frequency, differing in phase by $\phi$:

$$y_1 = A\sin(kx-\omega t) \qquad y_2 = A\sin(kx-\omega t+\phi)$$

Adding, with the identity $\sin\alpha+\sin\beta = 2\sin\frac{\alpha+\beta}{2}\cos\frac{\alpha-\beta}{2}$:

$$y = \underbrace{2A\cos\left(\frac{\phi}{2}\right)}_{\text{resultant amplitude}}\sin\left(kx-\omega t+\frac{\phi}{2}\right)$$

**The result is a wave of the same frequency, with an amplitude that depends entirely on $\phi$.**

| $\phi$ | $\cos(\phi/2)$ | Amplitude | Name |
|---|---|---|---|
| $0$ | 1 | $2A$ | **Fully constructive** |
| $\pi/2$ | $0.707$ | $1.41A$ | Partial |
| $\pi$ | 0 | **0** | **Fully destructive** |
| $2\pi$ | 1 | $2A$ | Constructive again |

> **Destructive interference is not destruction.** Energy is not lost — it is redistributed. Where two
> waves cancel, they reinforce somewhere else, and the total energy is conserved. Noise-cancelling
> headphones exploit exactly this.

---

## 3. Path Difference

In practice the phase difference usually arises because the waves travelled **different distances**
from their sources. A path difference $\Delta d$ corresponds to

$$\phi = \frac{2\pi}{\lambda}\Delta d$$

giving the conditions that matter in the laboratory:

$$\boxed{\text{Constructive: } \Delta d = m\lambda \qquad \text{Destructive: } \Delta d = \left(m+\tfrac12\right)\lambda}$$

for integer $m$.

**Verified**, with $\lambda = 0.500$ m:

| $\Delta d$ | In wavelengths | Result |
|---|---|---|
| 0 | 0 | constructive |
| 0.25 m | $\tfrac12\lambda$ | **destructive** |
| 0.50 m | $1\lambda$ | constructive |
| 0.75 m | $\tfrac32\lambda$ | **destructive** |
| 1.00 m | $2\lambda$ | constructive |

**Half a wavelength is the crucial distance.** Move one source back by $\lambda/2$ and a loud point
becomes silent.

*This is the principle behind the two-slit experiment, radio antenna arrays, anti-reflective coatings,
and the acoustic dead spots you can walk through between two loudspeakers playing the same tone.*

---

## 4. Beats

Now let the two waves have slightly **different frequencies**, at the same point in space:

$$y_1 = A\cos(2\pi f_1 t) \qquad y_2 = A\cos(2\pi f_2 t)$$

Adding and applying the sum-to-product identity:

$$y = \underbrace{2A\cos\left(2\pi\frac{f_1-f_2}{2}t\right)}_{\text{slowly varying envelope}}\cos\left(2\pi\frac{f_1+f_2}{2}t\right)$$

You hear a tone at the **average** frequency whose loudness pulses at a rate set by the **difference**.

Because loudness peaks **twice** per envelope cycle — the envelope is loud at both its positive and
negative extremes — the audible beat frequency is

$$\boxed{f_{\text{beat}} = \lvert f_1 - f_2\rvert}$$

### Worked example — verified

Two tuning forks at $440$ Hz and $443$ Hz produce a tone at $\mathbf{441.5~\text{Hz}}$ pulsing
**3 times per second**.

> **This is how instruments are tuned by ear.** Sound your string against a reference and adjust until
> the beats slow and stop. The method is extraordinarily sensitive: a 1 Hz beat against a 440 Hz
> reference is a mistuning of 0.2%, and a trained ear detects beats well below 1 Hz. **You are
> detecting a small difference by listening to a slow rhythm rather than a pitch** — far easier for
> the human ear.

---

## 5. Reflection and Phase Inversion

When a wave reaches a boundary, part reflects. What happens depends on the boundary:

| Boundary | Reflected pulse |
|---|---|
| **Fixed end** (rigid) | **Inverted** — flips upside down |
| **Free end** | **Not inverted** |

**Why the fixed end inverts:** the end cannot move, so the incident and reflected waves must sum to
zero there at all times. That requires the reflected wave to be the exact negative of the incident
one — a phase change of $\pi$.

**This inversion is what makes standing waves possible**, and Lecture 30 builds on it directly.

*The same rule governs light reflecting off a denser medium, which is why anti-reflective coatings on
lenses work and why a soap film shows colours.*

---

## 6. Summary

| | |
|---|---|
| Superposition | Displacements **add**; waves pass through unchanged |
| Why it holds | The wave equation is **linear** |
| Two identical waves | Amplitude $2A\cos(\phi/2)$ |
| Constructive | $\phi = 2\pi m$, or $\Delta d = m\lambda$ |
| Destructive | $\phi = \pi(2m+1)$, or $\Delta d = (m+\tfrac12)\lambda$ |
| Destructive interference | Redistributes energy; does not destroy it |
| Beats | Tone at $\tfrac{f_1+f_2}{2}$, pulsing at $\lvert f_1-f_2\rvert$ |
| Fixed-end reflection | **Inverted** ($\pi$ phase change) |
| Free-end reflection | Not inverted |

---

## 7. Conceptual Questions

1. Two waves interfere destructively and the displacement is zero everywhere they overlap. Where has the energy gone?

2. Why can two people talk across a room without their sound waves permanently distorting each other?

3. A guitarist hears 4 beats per second against a 330 Hz reference. What are the two possible frequencies of the string? How would she determine which?

4. Why does a pulse reflect inverted from a fixed end but upright from a free end?

5. Two loudspeakers play the same 680 Hz tone in phase. Taking $v = 340$ m/s, how far must you move from a loud point to reach a quiet one?

---

## 8. Problems

1. Two waves of amplitude 4.00 cm interfere with a phase difference of $\pi/3$. Find the resultant amplitude.

2. Two sources emit 500 Hz sound ($v = 340$ m/s) in phase. Find the three smallest path differences giving (a) constructive and (b) destructive interference.

3. Two tuning forks produce 5 beats per second. One is 512 Hz. Give both possible values for the other, and describe an experiment to decide between them.

4. Two speakers 3.00 m apart emit 1.20 kHz in phase. A listener stands 4.00 m from one and 4.85 m from the other. Taking $v = 340$ m/s, is this a loud or a quiet position? Show the path difference in wavelengths.

5. A pulse travels along a rope towards a fixed end, reflects, and returns. Sketch the pulse before and after reflection, and state what changes.

---

*Next: Lecture 30 — Standing Waves and Resonance on Strings*
