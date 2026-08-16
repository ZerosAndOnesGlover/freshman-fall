# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Lecture 26 — Pendulums and Physical Oscillators

**Date:** Tuesday 13 October 2026 · 14:00–14:50 · Week 8

---

## Where This Fits

Lecture 25 established SHM for a mass on a spring, where the restoring force $F = -kx$ is exactly
linear. This lecture applies the same framework to systems where the restoring force is **not**
linear — pendulums — and shows that they behave harmonically anyway, provided the amplitude is small.

That qualification is important and often glossed over. A pendulum is *not* a harmonic oscillator; it
is a system that becomes indistinguishable from one when you do not push it too far. We will quantify
"too far".

---

## 1. The Simple Pendulum

A point mass $m$ on a massless string of length $L$, displaced by angle $\theta$.

The restoring force is the tangential component of gravity:

$$F_t = -mg\sin\theta$$

The minus sign says it pulls back towards $\theta = 0$. With arc length $s = L\theta$:

$$m\frac{d^2s}{dt^2} = -mg\sin\theta \qquad\Longrightarrow\qquad \frac{d^2\theta}{dt^2} = -\frac{g}{L}\sin\theta$$

**This is not SHM.** The restoring term goes as $\sin\theta$, not $\theta$.

### The small-angle approximation

For small $\theta$ (in **radians**), $\sin\theta \approx \theta$ — the first term of the Taylor series
from MATH 141. Then

$$\frac{d^2\theta}{dt^2} \approx -\frac{g}{L}\theta$$

which *is* the SHM equation with $\omega^2 = g/L$:

$$\boxed{T = 2\pi\sqrt{\frac{L}{g}}}$$

> **Two remarkable absences.** The period does not depend on the **mass** — heavier bobs feel more
> gravity but have proportionally more inertia. And it does not depend on the **amplitude**, so long
> as the amplitude is small. Galileo noticed the second in a swinging cathedral lamp around 1583, and
> it made accurate clocks possible.

### How good is the approximation? — verified

| $\theta$ | $\sin\theta$ | $\theta$ (rad) | Error in $T$ |
|---|---|---|---|
| $5°$ | 0.087156 | 0.087266 | 0.13% |
| $10°$ | 0.173648 | 0.174533 | 0.51% |
| $15°$ | 0.258819 | 0.261799 | 1.15% |
| $20°$ | 0.342020 | 0.349066 | 2.06% |
| $30°$ | 0.500000 | 0.523599 | 4.72% |

**Below about $15°$ the error is under about 1%** — smaller than most experimental uncertainty, which
is why the approximation is used freely. At $30°$ it is nearly 5% and no longer negligible.

*(The true period grows with amplitude: a real pendulum swings **slower** at large amplitude, because
$\sin\theta < \theta$ makes the actual restoring force weaker than the linear approximation predicts.)*

### Verified periods

| $L$ (m) | $T$ (s) |
|---|---|
| 0.25 | 1.0030 |
| 0.50 | 1.4185 |
| **1.00** | **2.0061** |

**The "seconds pendulum"** — one that ticks once per second, so $T = 2$ s — needs
$L = g(T/2\pi)^2 = \mathbf{0.9940~\text{m}}$. That a metre is *almost* exactly this length is a
historical near-miss: it was one of the candidate definitions of the metre in the 1790s, rejected
because $g$ varies with latitude.

---

## 2. The Physical Pendulum

Real pendulums are extended bodies, not point masses. Use the rotational form of Newton's second law
from Week 6:

$$\tau = I\alpha \qquad\Longrightarrow\qquad -mgd\sin\theta = I\frac{d^2\theta}{dt^2}$$

where $d$ is the distance from pivot to centre of mass and $I$ is the moment of inertia **about the
pivot**. For small $\theta$:

$$\boxed{T = 2\pi\sqrt{\frac{I}{mgd}}}$$

### Worked example — verified

A uniform rod of length $L = 1.00$ m pivoted at one end.

From Week 6, $I = \tfrac13mL^2$ about the end, and $d = L/2$:

$$T = 2\pi\sqrt{\frac{\tfrac13mL^2}{mg(L/2)}} = 2\pi\sqrt{\frac{2L}{3g}} = \mathbf{1.6379~\text{s}}$$

Compare a **simple** pendulum of the same length: $T = 2.0061$ s. **The rod swings faster.** Its mass
is distributed along its length rather than concentrated at the far end, so it has less rotational
inertia relative to its restoring torque.

The rod behaves exactly like a simple pendulum of length $2L/3 = 0.6667$ m — verified, that length
gives $T = 1.6379$ s. This is the **equivalent length** of a physical pendulum.

**Consistency check:** put all the rod's mass at the far end, giving $I = mL^2$ and $d = L$, and the
formula returns $T = 2\pi\sqrt{L/g}$ — the simple pendulum, as it must.

---

## 3. The Torsional Oscillator

Twist a wire or fibre through angle $\theta$ and it resists with a restoring torque

$$\tau = -\kappa\theta$$

where $\kappa$ is the torsion constant. This is Hooke's law for rotation, so

$$T = 2\pi\sqrt{\frac{I}{\kappa}}$$

**No small-angle approximation is needed** — the relationship is genuinely linear over a wide range,
unlike a pendulum's. This is why torsional oscillators make precise instruments: Cavendish measured
$G$ with one in 1798, and the balance wheel in a mechanical watch is one.

---

## 4. The Pattern

Every oscillator in this lecture has the same structure:

$$\omega = \sqrt{\frac{\text{restoring "stiffness"}}{\text{inertia}}}$$

| System | Stiffness | Inertia | $\omega$ |
|---|---|---|---|
| Mass–spring | $k$ | $m$ | $\sqrt{k/m}$ |
| Simple pendulum | $mg/L$ | $m$ | $\sqrt{g/L}$ |
| Physical pendulum | $mgd$ | $I$ | $\sqrt{mgd/I}$ |
| Torsional | $\kappa$ | $I$ | $\sqrt{\kappa/I}$ |

**Learn the pattern, not the four formulas.** Identify what resists displacement and what resists
acceleration, and the frequency follows.

---

## 5. Summary

| | |
|---|---|
| Simple pendulum | $T = 2\pi\sqrt{L/g}$, small angles only |
| Independent of | mass and amplitude |
| Small-angle validity | $<1\%$ error below $\approx15°$; $4.7\%$ at $30°$ |
| Real pendulums at large amplitude | swing **slower** |
| Physical pendulum | $T = 2\pi\sqrt{I/mgd}$ |
| Uniform rod at end | $T = 2\pi\sqrt{2L/3g}$; equivalent length $2L/3$ |
| Torsional | $T = 2\pi\sqrt{I/\kappa}$, no approximation needed |
| Universal pattern | $\omega = \sqrt{\text{stiffness}/\text{inertia}}$ |

---

## 6. Conceptual Questions

1. A pendulum clock keeps perfect time in London. Taken to the equator, where $g$ is slightly smaller, does it run fast or slow? By what mechanism would you correct it?

2. A child on a swing stands up as she passes the lowest point. Does the period increase or decrease? Explain using the physical pendulum formula.

3. Why does a pendulum's period not depend on the mass of the bob, when a mass–spring system's period does depend on mass?

4. A pendulum is taken to the Moon, where $g = 1.62$ m/s². By what factor does its period change?

5. Two rods of the same length swing from one end — one aluminium, one lead. Which has the longer period?

---

## 7. Problems

1. Find the length of a simple pendulum whose period is exactly 1.00 s on Earth.

2. A pendulum of length 0.750 m is released from $12°$. Find its period, and estimate the error introduced by the small-angle approximation.

3. A uniform rod of length 0.800 m swings from one end. Find its period and its equivalent simple-pendulum length.

4. A uniform disc of radius 0.150 m is pivoted at a point on its rim. Given $I_{\text{cm}} = \tfrac12mR^2$, use the parallel-axis theorem to find $I$ about the pivot, then the period.

5. A torsional oscillator has $I = 3.50\times10^{-4}$ kg·m² and $\kappa = 2.20\times10^{-3}$ N·m/rad. Find its period.

6. A pendulum clock with a 0.9940 m pendulum loses 30 s per day. Should the bob be raised or lowered, and by how much?

---

*Next: Lecture 27 — Damped and Driven Oscillations*
