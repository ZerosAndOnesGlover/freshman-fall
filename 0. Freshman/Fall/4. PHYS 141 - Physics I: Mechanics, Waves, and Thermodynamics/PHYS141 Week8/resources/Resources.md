# PHYS 141 — Week 8 Resources

## Required Textbook Reading

- **HRK:** Ch. 17 (Oscillations) — §17.1–17.7 for SHM, the pendulum, and damped/forced oscillations
- **Serway:** Ch. 15 (Oscillatory Motion) — all sections

## Simulations

- **PhET "Masses and Springs"** — vary $m$, $k$, and gravity independently. The energy display makes
  the continuous $K \leftrightarrow U$ exchange visible, and the damping slider lets you watch the
  three regimes.
- **PhET "Pendulum Lab"** — the amplitude slider is the important one. Set two pendulums to $5°$ and
  $45°$ and watch them drift out of phase; this is Part 2 of the lab, for free.
- **PhET "Normal Modes"** — a preview of Week 9. A chain of coupled oscillators *is* a wave.

## Video Demonstration Recommendations

- Search for footage of the **Millennium Bridge** lateral oscillation from June 2000. Pedestrians
  unconsciously synchronised their steps to the bridge's sway, driving it at its own resonant
  frequency — a textbook illustration of a driven oscillator, recorded by accident.
- The **Tacoma Narrows Bridge** collapse (1940) is the famous footage, but be careful: this was
  aeroelastic **flutter**, not simple resonance. The bridge generated its own driving frequency from
  the airflow, rather than being driven by an external periodic force. The misattribution appears in
  many textbooks; knowing the difference is worth more than knowing the film.
- Any recording of a **wine glass shattered by sound** demonstrates resonance and $Q$ together: the
  glass responds only to a narrow band of frequencies, which is exactly what a high $Q$ means.

## Deeper Reading

- Feynman, *Feynman Lectures Vol. 1*, Ch. 21–25 — five chapters on the harmonic oscillator, on the
  grounds that it is the most important system in physics. Ch. 23 on resonance is outstanding.
- Any text on the **anharmonic** pendulum: the exact period involves an elliptic integral, and its
  series expansion $T = T_0\left(1 + \tfrac{1}{16}\theta_0^2 + \cdots\right)$ is what produces the
  4.7% figure at $30°$ quoted in Lecture 26. Deriving it is beyond this course; knowing it exists is
  not.

## Why This Week Matters Beyond Physics (Enrichment)

The Taylor-expansion argument at the end of Lecture 25 is the reason this week generalises so far.
**Any** system sitting in a smooth potential minimum behaves as a harmonic oscillator for small
displacements, because the linear term in the expansion vanishes at a minimum and the quadratic term
is Hooke's law.

The consequences reach well outside mechanics:

- **Molecular vibration.** A chemical bond near its equilibrium length is a spring; infrared
  spectroscopy measures $\omega=\sqrt{k/\mu}$ and reads off the bond stiffness.
- **Solid-state physics.** Atoms in a crystal lattice oscillate about their sites; quantising those
  oscillations gives **phonons**, which carry heat and sound through solids.
- **Electronics.** An LC circuit obeys $L\ddot q + q/C = 0$ — algebraically identical to
  $m\ddot x + kx = 0$, with inductance playing the role of mass and $1/C$ of stiffness. Every result
  in this week transfers with a change of symbols, and ECE 110 will use it.
- **Quantum mechanics.** The quantum harmonic oscillator is one of the very few exactly solvable
  systems, and for the same reason: it approximates everything near a minimum.

## Common Pitfalls This Week

1. **Using degrees in $\sin\theta \approx \theta$.** The approximation holds only in **radians**.
   $\sin(10°) = 0.1736$ and $10$ radians is meaningless in this context — a calculator left in degree
   mode gives silent nonsense.

2. **Assuming the pendulum period depends on mass.** It does not, and the reason is the same as for
   free fall: gravity supplies both the restoring force and the inertia, and they cancel. A
   mass–spring system *does* depend on mass, because the spring's stiffness has nothing to do with
   how much mass is attached.

3. **Confusing $\omega$ (angular frequency, rad/s) with $f$ (frequency, Hz).** They differ by $2\pi$,
   and this is the most common arithmetic error on the quiz.

4. **Treating a driven oscillator as oscillating at $\omega_0$.** In the steady state it oscillates at
   the **driving** frequency $\omega$. The natural frequency $\omega_0$ determines only *how large*
   the response is, not how fast it goes.

5. **Forgetting the amplitude/energy factor of two.** Amplitude decays as $e^{-\gamma t}$; energy as
   $e^{-2\gamma t}$, because $E \propto A^2$.
