# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Lecture 25 — Simple Harmonic Motion: Kinematics and Dynamics

**Date:** Monday 12 October 2026 · 14:00–14:50 · Week 8

---

## Where This Fits

Weeks 3–7 built mechanics from Newton's laws: forces cause acceleration, energy is conserved,
momentum is conserved. This week applies all of it to one specific situation — **a system pulled back
towards equilibrium by a force proportional to its displacement.**

That situation is worth its own week because it is *ubiquitous*. Any system sitting in a smooth
potential minimum, disturbed slightly, oscillates this way. Springs, pendulums, atoms in a crystal,
LC circuits, and the balance wheel in a watch all obey the same equation, and the mathematics you
learn here transfers to all of them without modification. Week 9 then shows that a *chain* of such
oscillators is a wave.

---

## 1. The Defining Condition

> **Simple harmonic motion (SHM)** occurs whenever the restoring force is proportional to
> displacement and directed opposite to it:
>
> $$F = -kx$$

The minus sign is the whole physics: displace the system either way and the force pushes it back.

Applying Newton's second law,

$$m\frac{d^2x}{dt^2} = -kx \qquad\Longrightarrow\qquad \frac{d^2x}{dt^2} = -\frac{k}{m}\,x$$

**Read that equation as a sentence:** the acceleration is proportional to the displacement, with the
opposite sign. We need a function that returns to minus itself (times a constant) after two
derivatives — which is exactly what sine and cosine do.

---

## 2. The Solution

$$\boxed{x(t) = A\cos(\omega t + \phi)}\qquad \omega = \sqrt{\frac{k}{m}}$$

| Symbol | Name | Meaning |
|---|---|---|
| $A$ | Amplitude | Maximum displacement (m) |
| $\omega$ | Angular frequency | rad/s |
| $\phi$ | Phase constant | Sets where the motion starts |

Differentiating:

$$v(t) = -A\omega\sin(\omega t+\phi) \qquad a(t) = -A\omega^2\cos(\omega t+\phi) = -\omega^2 x$$

The last equality confirms the solution: $a = -\omega^2 x$ is the differential equation with
$\omega^2 = k/m$.

$$T = \frac{2\pi}{\omega} = 2\pi\sqrt{\frac{m}{k}} \qquad f = \frac1T$$

> **The period does not depend on the amplitude.** Pull the mass twice as far and it travels twice as
> far, but it also moves twice as fast at every corresponding point, and the two effects cancel
> exactly. This property is called **isochronism**, and it is why pendulum clocks work.

### Worked example — verified

$m = 0.500$ kg on a spring with $k = 20.0$ N/m, released from rest at $x = 0.100$ m.

$$\omega = \sqrt{20.0/0.500} = \mathbf{6.3246~\text{rad/s}} \qquad T = \frac{2\pi}{\omega} = \mathbf{0.9935~\text{s}} \qquad f = \mathbf{1.0066~\text{Hz}}$$

Released from rest at maximum displacement ⟹ $A = 0.100$ m and $\phi = 0$.

$$v_{\max} = A\omega = \mathbf{0.6325~\text{m/s}} \qquad a_{\max} = A\omega^2 = \mathbf{4.000~\text{m/s}^2}$$

Snapshot through one cycle:

| $t$ | $x$ (m) | $v$ (m/s) | $a$ (m/s²) |
|---|---|---|---|
| $0$ | $+0.1000$ | $0$ | $-4.000$ |
| $T/8$ | $+0.0707$ | $-0.4472$ | $-2.828$ |
| $T/4$ | $0$ | $-0.6325$ | $0$ |
| $T/2$ | $-0.1000$ | $0$ | $+4.000$ |

**Notice the phase relationships.** When $x$ is maximum, $v = 0$ and $\lvert a\rvert$ is maximum.
When $x = 0$, $\lvert v\rvert$ is maximum and $a = 0$. Velocity leads displacement by $90°$;
acceleration is $180°$ out of phase with displacement.

---

## 3. Energy in SHM

The spring stores $U = \tfrac12kx^2$ and the mass carries $K = \tfrac12mv^2$. Substituting the
solutions and using $\omega^2 = k/m$:

$$E = K + U = \tfrac12 m A^2\omega^2\sin^2(\omega t+\phi) + \tfrac12 kA^2\cos^2(\omega t + \phi) = \boxed{\tfrac12 kA^2}$$

**Constant**, as Week 4 requires — the spring force is conservative.

**Verified** for the example above: $E = \tfrac12(20.0)(0.100)^2 = \mathbf{0.100~\text{J}}$, and
$\tfrac12 m v_{\max}^2 = \tfrac12(0.500)(0.6325)^2 = 0.100$ J ✓

### Speed at any position

Setting $\tfrac12mv^2 + \tfrac12kx^2 = \tfrac12kA^2$:

$$v = \pm\sqrt{\frac{k}{m}\left(A^2 - x^2\right)} = \pm\,\omega\sqrt{A^2-x^2}$$

**Verified** at $x = A/2 = 0.050$ m: $v = \mathbf{0.5477~\text{m/s}}$, and the energy splits as
$U = 0.0250$ J, $K = 0.0750$ J.

> **A result students find surprising:** at **half** the amplitude the system holds only a **quarter**
> of its energy as potential — so $K/E = 3/4$. Energy is quadratic in displacement, so the outer
> half of the swing holds three-quarters of the energy.

---

## 4. The Vertical Spring

Hang the mass instead. At equilibrium the spring is already stretched by $x_0$ where $kx_0 = mg$.

Measuring $y$ from that **new** equilibrium, the net force is

$$F = k(x_0 - y) - mg = -ky$$

— identical to the horizontal case. **Gravity shifts the equilibrium point and changes nothing else.**
The period is still $T = 2\pi\sqrt{m/k}$, independent of $g$.

**Verified:** $m = 0.250$ kg on $k = 50.0$ N/m gives $x_0 = mg/k = \mathbf{0.04905~\text{m}}$ and
$T = \mathbf{0.4443~\text{s}}$. The alternative form $T = 2\pi\sqrt{x_0/g}$ gives the same $0.4443$ s
— a convenient trick for measuring $k$ without knowing $m$.

---

## 5. Why SHM Is Everywhere

Take **any** potential energy function $U(x)$ with a minimum at $x_0$. Expand it in a Taylor series
(MATH 141, Week 12) about that minimum:

$$U(x) = U(x_0) + \underbrace{U'(x_0)}_{=\,0}(x-x_0) + \tfrac12 U''(x_0)(x-x_0)^2 + \cdots$$

The linear term vanishes *because* $x_0$ is a minimum. So for small displacements

$$U \approx \tfrac12 U''(x_0)(x-x_0)^2 \qquad\Longrightarrow\qquad F = -\frac{dU}{dx} \approx -U''(x_0)(x-x_0)$$

which is Hooke's law with $k_{\text{eff}} = U''(x_0)$.

> **Every stable equilibrium is a harmonic oscillator for small enough displacements.** This is why
> the same equation describes a spring, a pendulum, a vibrating molecular bond, an LC circuit, and a
> guitar string. You are not learning about springs; you are learning the universal small-oscillation
> behaviour of matter.

---

## 6. Summary

| | |
|---|---|
| Defining condition | $F = -kx$ |
| Equation of motion | $a = -\omega^2 x$ |
| Solution | $x = A\cos(\omega t + \phi)$ |
| Angular frequency | $\omega = \sqrt{k/m}$ |
| Period | $T = 2\pi\sqrt{m/k}$ — **independent of amplitude** |
| $v_{\max}$, $a_{\max}$ | $A\omega$, $A\omega^2$ |
| Phase | $v$ leads $x$ by 90°; $a$ is 180° from $x$ |
| Total energy | $E = \tfrac12kA^2$, constant |
| Speed at $x$ | $v = \omega\sqrt{A^2-x^2}$ |
| Vertical spring | Same $T$; gravity only shifts equilibrium |
| Why universal | Taylor expansion about any potential minimum |

---

## 7. Conceptual Questions

1. A mass on a spring oscillates with amplitude $A$. If you double $A$, what happens to $T$, $v_{\max}$, and $E$?

2. At what displacement is the kinetic energy equal to the potential energy? Express your answer as a fraction of $A$.

3. Two identical springs, each of constant $k$, are attached in **parallel** to the same mass. What is the period? What if they are in **series**?

4. Why does a vertical spring–mass system have the same period as a horizontal one, despite gravity acting on it?

5. A mass oscillates on a spring in a lift. The lift accelerates upward at $2$ m/s². Does the period change? Does the equilibrium position?

---

## 8. Problems

1. A 0.750 kg mass on a spring of $k = 30.0$ N/m is displaced 8.00 cm and released. Find $\omega$, $T$, $f$, $v_{\max}$, $a_{\max}$, and $E$.

2. An oscillator has $A = 0.120$ m and $T = 0.500$ s. Find its speed and acceleration when $x = 0.060$ m.

3. A 0.400 kg mass hangs from a spring, stretching it 6.50 cm at equilibrium. Find $k$ and the period of small vertical oscillations.

4. An SHM oscillator has $x(t) = (0.250\ \text{m})\cos(12.0t + \pi/3)$. State $A$, $\omega$, $T$, $f$, $\phi$, and $x(0)$, and find the first time the mass passes through $x = 0$.

5. For an oscillator of amplitude $A$, find the displacement at which the speed is half its maximum value.

---

*Next: Lecture 26 — Pendulums and Physical Oscillators*
