# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Lecture 39 — Review and the Road Ahead

---

## 1. What the Course Was Actually About

Thirty-nine lectures across mechanics, rotation, oscillations, waves, sound, and thermodynamics. They
look like six subjects. They are one method applied six times.

**The method:** identify what is conserved, identify what causes change, and write the relationship
between them.

| Domain | What is conserved | What causes change |
|---|---|---|
| Translation | Momentum, energy | Force |
| Rotation | Angular momentum, energy | Torque |
| Oscillation | Energy (undamped) | Restoring force |
| Waves | Energy, momentum | The medium's stiffness and inertia |
| Thermodynamics | Energy (First Law) | Heat and work |

Every problem you solved was an instance of that pattern. **Recognising which conservation law applies
is more than half of physics**, and it is the transferable skill.

---

## 2. The Structural Analogies

The course is built on repeated structure, and seeing it is worth more than memorising any single
formula.

### Translation ↔ Rotation

| Translation | Rotation |
|---|---|
| $x$, $v$, $a$ | $\theta$, $\omega$, $\alpha$ |
| $m$ | $I$ |
| $F = ma$ | $\tau = I\alpha$ |
| $p = mv$ | $L = I\omega$ |
| $K = \tfrac12mv^2$ | $K = \tfrac12I\omega^2$ |
| $W = Fd$ | $W = \tau\theta$ |

**Every rotational result was obtained by substitution**, not by new physics. Weeks 6 and 7 were
Weeks 3–5 with different symbols.

### The oscillator pattern

$$\omega = \sqrt{\frac{\text{stiffness}}{\text{inertia}}}$$

| System | Stiffness | Inertia |
|---|---|---|
| Mass–spring | $k$ | $m$ |
| Simple pendulum | $mg/L$ | $m$ |
| Physical pendulum | $mgd$ | $I$ |
| Torsional | $\kappa$ | $I$ |
| **Wave on a string** | $F_T$ | $\mu$ |

The last row is the connection between Weeks 8 and 9: a wave is a chain of coupled oscillators, and
$v = \sqrt{F_T/\mu}$ has the same form for the same reason.

### Amplitude squared

Power and intensity go as $A^2$ in **every** wave system. This is why sound needs a logarithmic
scale, why doubling a string's amplitude quadruples its power, and why a 3 dB change means a factor
of two.

---

## 3. The Ideas Worth Keeping

Beyond the formulas, five things in this course change how you look at problems.

**1. Isochronism.** A pendulum's period is independent of amplitude. That single fact made accurate
clocks possible and, with them, navigation and modern astronomy.

**2. Confinement quantises.** A wave trapped between boundaries can only take discrete frequencies.
Strings have pitches for the same reason atoms have spectral lines — you met the mechanism in Week 9
in a form you could photograph.

**3. Every potential minimum is harmonic.** Taylor-expand any smooth potential about a minimum and
the quadratic term is Hooke's law. This is why one week's work on springs describes molecular bonds,
crystal lattices, and LC circuits.

**4. Temperature is kinetic energy.** The bulk quantity of Week 11 turned out, in Week 11's own
kinetic theory, to measure average molecular motion directly.

**5. Energy conservation does not determine direction.** The First Law permits a great many things
that never happen. Only the Second Law, through entropy, says which way processes run — and it does
so statistically rather than absolutely.

---

## 4. Exam-Critical Results

### Mechanics (Weeks 0–5)
- Kinematics: $v = v_0+at$, $x = x_0+v_0t+\tfrac12at^2$, $v^2 = v_0^2+2a\Delta x$
- Projectiles: independent horizontal and vertical motion
- $\sum\vec F = m\vec a$; free-body diagrams before algebra
- $W = \vec F\cdot\vec d$; $K = \tfrac12mv^2$; $U_g = mgh$; $U_s = \tfrac12kx^2$
- $\vec p = m\vec v$; conserved in **all** collisions; $K$ conserved only if elastic

### Rotation (Weeks 6–7)
- $\tau = I\alpha$; parallel-axis $I = I_{\text{cm}} + md^2$
- Rolling: $v = \omega R$; $K = \tfrac12mv^2 + \tfrac12I\omega^2$
- $L = I\omega$, conserved when $\tau_{\text{net}} = 0$
- Static equilibrium: $\sum\vec F = 0$ **and** $\sum\vec\tau = 0$

### Oscillations and waves (Weeks 8–10)
- $x = A\cos(\omega t+\phi)$; $T = 2\pi\sqrt{m/k}$; $E = \tfrac12kA^2$
- $T = 2\pi\sqrt{L/g}$ (small angles); $T = 2\pi\sqrt{I/mgd}$
- Damping: $\gamma = b/2m$; critical at $b = 2\sqrt{mk}$; energy decays **twice as fast** as amplitude
- $v = f\lambda$; $v = \sqrt{F_T/\mu}$
- $f_n = nv/2L$ (both ends fixed or both open); $f_n = nv/4L$, **odd only** (one end closed)
- $f_{\text{beat}} = \lvert f_1-f_2\rvert$
- $\beta = 10\log_{10}(I/I_0)$; $+3$ dB doubles intensity; $-6$ dB per doubling of distance
- $f' = f(v+v_o)/(v-v_s)$ — **check the direction of every answer**

### Thermodynamics (Weeks 11–12)
- $\Delta L = \alpha L_0\Delta T$; $\beta = 3\alpha$
- $Q = mc\Delta T$; $Q = mL$; calorimetry $\sum Q = 0$
- $P = kA\Delta T/L$; $P = e\sigma AT^4$
- $PV = nRT$ — **kelvin always**
- $\Delta U = Q - W$
- $e = 1-Q_c/Q_h \le 1-T_c/T_h$
- $\Delta S_{\text{total}} \ge 0$

---

## 5. The Five Most Common Exam Errors

1. **Using Celsius in gas-law or radiation formulas.** In $P = e\sigma AT^4$ the error is
   fourth-power and catastrophic.
2. **Applying $f_n = nv/2L$ to a closed pipe.** Closed–open pipes are $nv/4L$ with **odd $n$ only**.
3. **Doppler sign errors.** Predict the direction first, compute, then check the answer moved that way.
4. **Forgetting to check whether all the ice melts** before solving a calorimetry problem.
5. **Assuming kinetic energy is conserved in collisions.** Momentum always is; kinetic energy only in
   elastic ones.

---

## 6. Where Each Thread Continues

| This course | Continues in |
|---|---|
| Newtonian mechanics, rotation | **PHYS 241** — Lagrangian and Hamiltonian formulations |
| Oscillations, resonance, damping | **ECE 110** — LC and RLC circuits, identical mathematics |
| Waves, superposition, Fourier content | **MATH 142** — Fourier series; signal processing |
| Standing waves and quantisation | **PHYS 340** — quantum mechanics, where the same argument gives energy levels |
| Thermodynamics, entropy | **PHYS 320** — statistical mechanics, deriving all of Week 12 from counting |
| Heat transfer | Any engineering thermal design |
| Entropy as $k_B\ln\Omega$ | **CS 350** — information theory, where Shannon entropy has the same form |

> That last row is not a coincidence. Shannon's information entropy and Boltzmann's thermodynamic
> entropy have the same functional form because they answer the same question: **how many
> microstates are consistent with what I know?**

---

## 7. A Closing Thought

The most remarkable thing in this course is not any single result. It is that a handful of
relationships — a few conservation laws, one differential equation, and a statistical argument —
describe a pendulum, a guitar string, a siren, a bridge in summer, and a power station.

You did not learn thirty-nine separate topics. You learned that **the same small set of ideas keeps
reappearing**, and how to recognise them in unfamiliar dress. That recognition is what physics gives
an engineer, and it is worth considerably more than any formula you will look up later anyway.

---

## 8. Final Exam Preparation

**Format:** 3 hours, closed book. One double-sided A4 sheet of handwritten notes and a formula sheet
provided.

**Coverage:** Weeks 0–12, weighted towards Weeks 3–5 (Newton, energy, momentum) and 8–12
(oscillations through thermodynamics).

**A working method:**

1. **Redo every quiz first.** Twelve quizzes at 20 minutes each is four hours, and they were written
   to target exactly the transferable skills.
2. **Then the problem sets**, concentrating on setup rather than arithmetic.
3. **Then the lab reports** — experimental reasoning and uncertainty analysis appear on the paper.
4. **Finally one full past paper under timed conditions.**

**Habits that earn marks:**

- **Draw the diagram.** Free-body, ray, or $PV$ — nearly every problem becomes tractable once drawn.
- **Check units at every stage**, not at the end.
- **Sanity-check magnitudes.** A pendulum with a 40 s period or an efficiency above the Carnot limit
  is telling you something.
- **Show the method even when stuck.** Method marks are awarded generously and cost nothing to claim.

---

*PHYS 141 · Week 12 · Lecture 39 · © CSE Department*

*This concludes Physics I. Good luck.*
