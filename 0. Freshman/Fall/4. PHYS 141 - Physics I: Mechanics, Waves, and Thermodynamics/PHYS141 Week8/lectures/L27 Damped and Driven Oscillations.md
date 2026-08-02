# PHYS 141 — Physics I: Mechanics, Waves & Thermodynamics
## Lecture 27 — Damped and Driven Oscillations, and Resonance

---

## Where This Fits

Lectures 25 and 26 described oscillators that never stop. No real oscillator behaves that way: a
plucked string falls silent, a swing coasts to rest. Energy leaks out.

This lecture adds the two ingredients that make the model realistic — a **damping** force that removes
energy, and a **driving** force that supplies it — and arrives at **resonance**, which is the reason
engineers care about this material at all.

---

## 1. Damped Oscillations

Add a resistive force proportional to velocity, which is a good model for air drag at low speed and
for viscous friction:

$$F = -kx - bv$$

Newton's second law gives

$$m\frac{d^2x}{dt^2} + b\frac{dx}{dt} + kx = 0$$

For light damping the solution is

$$\boxed{x(t) = A_0 e^{-\gamma t}\cos(\omega_d t + \phi)} \qquad \gamma = \frac{b}{2m}, \qquad \omega_d = \sqrt{\omega_0^2 - \gamma^2}$$

where $\omega_0 = \sqrt{k/m}$ is the **undamped** angular frequency.

**Two things happen.** The amplitude decays exponentially, and the oscillation slows slightly —
$\omega_d < \omega_0$. For light damping the second effect is tiny.

### Worked example — verified

$m = 0.500$ kg, $k = 20.0$ N/m, $b = 0.200$ kg/s.

$$\omega_0 = 6.3246~\text{rad/s} \qquad \gamma = \frac{b}{2m} = 0.200~\text{s}^{-1} \qquad \omega_d = \mathbf{6.3214~\text{rad/s}}$$

The frequency shift is **0.05%** — negligible, as expected when $\gamma \ll \omega_0$.

**Amplitude half-life:** $A_0e^{-\gamma t} = A_0/2$ at $t = \ln 2/\gamma = \mathbf{3.466~\text{s}}$.

**Energy half-life:** $E \propto A^2 \propto e^{-2\gamma t}$, so energy halves at
$\ln2/(2\gamma) = \mathbf{1.733~\text{s}}$ — **exactly half the amplitude half-life**. Energy drains
twice as fast as amplitude, because it goes as amplitude squared.

---

## 2. The Three Damping Regimes

The behaviour depends on $\gamma$ against $\omega_0$, i.e. on $b$ against $2\sqrt{mk}$:

| Regime | Condition | Behaviour |
|---|---|---|
| **Underdamped** | $b < 2\sqrt{mk}$ | Oscillates with decaying amplitude |
| **Critically damped** | $b = 2\sqrt{mk}$ | Returns to equilibrium **fastest**, no oscillation |
| **Overdamped** | $b > 2\sqrt{mk}$ | Returns slowly, no oscillation |

For the example, $2\sqrt{mk} = \mathbf{6.3246}$ kg/s, and $b = 0.200 \ll 6.32$ — firmly
underdamped ✓

> **Critical damping is a design target, not an accident.** A car suspension, a door closer, and a
> galvanometer needle are all deliberately tuned near critical damping: you want the fastest possible
> return to equilibrium *without* overshoot. Underdamp a car and it bounces; overdamp it and it
> wallows over bumps.

**The quality factor** $Q = \omega_0/2\gamma$ measures how many oscillations survive. For our example
$Q = \mathbf{15.81}$ — the oscillation persists for roughly 16 radians of phase before decaying
appreciably. A church bell has $Q \sim 10^3$; a quartz crystal $\sim 10^5$.

---

## 3. Driven Oscillations and Resonance

Now push the oscillator periodically: $F(t) = F_0\cos(\omega t)$, where $\omega$ is the **driving**
frequency, which you choose, and is generally *not* $\omega_0$.

After transients die away, the system settles into steady oscillation **at the driving frequency**
$\omega$, with amplitude

$$A(\omega) = \frac{F_0/m}{\sqrt{\left(\omega_0^2-\omega^2\right)^2 + \left(2\gamma\omega\right)^2}}$$

**The amplitude depends dramatically on how close $\omega$ is to $\omega_0$.**

### Verified response curve

Same oscillator, $F_0 = 1.00$ N:

| $\omega/\omega_0$ | Amplitude (m) |
|---|---|
| 0.50 | 0.0666 |
| 0.90 | 0.2521 |
| **1.00** | **0.7906** |
| 1.10 | 0.2260 |
| 2.00 | 0.0167 |

**At resonance the amplitude is 47× larger than at twice the driving frequency**, for exactly the
same driving force. The peak is sharp, and it gets sharper as damping falls — in the limit
$\gamma \to 0$ the amplitude at $\omega = \omega_0$ diverges.

> **This is why resonance matters to engineers.** A small periodic force, applied at the right
> frequency, produces a large response. That is useful when you want it and destructive when you do
> not.

---

## 4. Resonance in Practice

**Wanted:**
- **Radio tuning.** An LC circuit is an electrical oscillator; tuning sets $\omega_0$ to the station's
  frequency so that one broadcast among thousands drives a large response.
- **MRI.** Nuclear magnetic *resonance* — the "R" is this phenomenon.
- **Microwave ovens** drive water molecules near a rotational resonance.
- **Musical instruments.** A guitar body resonates to amplify the string.

**Unwanted:**
- **Bridges.** Soldiers break step crossing footbridges because a marching cadence near $\omega_0$
  pumps energy in every cycle. London's Millennium Bridge closed two days after opening in 2000 for
  a lateral resonance problem, and reopened after £5M of dampers were fitted.
- **Buildings in earthquakes.** Seismic design is largely about keeping structural resonances away
  from typical ground-motion frequencies, and adding damping where that is impossible.
- **Machinery.** Rotating equipment is designed so operating speed avoids the shaft's critical speed.

*(The Tacoma Narrows Bridge collapse of 1940 is the usual textbook example, but it is not simple
resonance — it was aeroelastic flutter, a self-excited instability. The bridge supplied its own
driving frequency. Worth knowing, since the misattribution is extremely common.)*

---

## 5. Summary

| | |
|---|---|
| Damped equation | $m\ddot x + b\dot x + kx = 0$ |
| Solution | $x = A_0e^{-\gamma t}\cos(\omega_d t+\phi)$, $\gamma = b/2m$ |
| Damped frequency | $\omega_d = \sqrt{\omega_0^2-\gamma^2} < \omega_0$ |
| Amplitude half-life | $\ln2/\gamma$ |
| Energy half-life | $\ln2/2\gamma$ — **half** the amplitude half-life |
| Critical damping | $b = 2\sqrt{mk}$ — fastest return, no overshoot |
| Quality factor | $Q = \omega_0/2\gamma$ |
| Driven steady state | Oscillates at the **driving** frequency $\omega$ |
| Resonance | Amplitude peaks at $\omega \approx \omega_0$; sharper for lighter damping |

---

## 6. Conceptual Questions

1. Why does a damped oscillator's *energy* decay twice as fast as its *amplitude*?

2. A car's shock absorbers wear out. Is the suspension now under- or overdamped? What do you feel?

3. Why is critical damping — rather than heavy damping — the design target for a door closer?

4. A singer shatters a wine glass. What must be true of the note relative to the glass, and why does a *louder* note not work if the pitch is wrong?

5. In the driven case, the system oscillates at $\omega$, not $\omega_0$. Why, then, does $\omega_0$ appear in the amplitude formula at all?

---

## 7. Problems

1. An oscillator has $m = 0.250$ kg, $k = 100$ N/m, $b = 0.500$ kg/s. Find $\omega_0$, $\gamma$, $\omega_d$, and $Q$. Is it under-, over-, or critically damped?

2. For the oscillator in Problem 1, how long until the amplitude falls to 25% of its initial value? Until the energy does?

3. What value of $b$ would critically damp the oscillator of Problem 1?

4. A damped oscillator loses 5.0% of its energy per cycle. Estimate $Q$.

5. A driven oscillator has $\omega_0 = 40.0$ rad/s and $\gamma = 1.50$ s⁻¹, driven with $F_0/m = 2.00$ m/s². Compute the steady-state amplitude at $\omega = 20$, $38$, $40$, and $42$ rad/s, and identify the resonance.

---

*Next: Week 9 — Waves: Properties, Superposition, and Standing Waves*
