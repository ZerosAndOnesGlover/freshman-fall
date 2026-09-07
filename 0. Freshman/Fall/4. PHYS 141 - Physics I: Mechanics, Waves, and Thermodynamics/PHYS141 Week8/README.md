# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Week 8: Simple Harmonic Motion & Oscillators

**Semester:** Fall | **Credits:** 4 | **Lab:** Weekly 3-hr lab session

---

## Week 8 Contents

| File | Description |
|------|-------------|
| [[L25 Simple Harmonic Motion]] | $F=-kx$; the SHM solution, energy, and why every potential minimum oscillates harmonically |
| [[L26 Pendulums and Physical Oscillators]] | Simple, physical, and torsional pendulums; the small-angle approximation quantified |
| [[L27 Damped and Driven Oscillations]] | Damping regimes, quality factor, driven response, and resonance |
| [[LAB 8 The Simple Pendulum and SHM]] | Determining $g$ from $T^2$ vs $L$; amplitude and mass dependence; spring constant two ways; damping |
| [[PS 8 Simple Harmonic Motion and Oscillators]] | 20 problems on SHM, pendulums, damping, and resonance |
| [[QUIZ 8 Simple Harmonic Motion and Oscillators]] | 10-question quiz (administered Monday, Week 9) |
| [[PHYS141 Week8/resources/Resources\|Resources]] | Textbook references, simulations, deeper reading |
| [[PHYS141 Week8/solutions_instructor/PS 8 Solutions\|PS 8 Solutions]] | Full worked solutions (instructor only) |
| [[PHYS141 Week8/solutions_instructor/LAB 8 Solutions\|LAB 8 Solutions]] | Expected data, analysis answers, systematic errors to look for |

---

## Learning Objectives

By the end of Week 8, you will be able to:

1. Recognise simple harmonic motion from its defining condition $F = -kx$ and write the equation of motion $a = -\omega^2x$
2. Write and interpret $x(t) = A\cos(\omega t+\phi)$, and derive $v(t)$ and $a(t)$ with their phase relationships
3. Compute $\omega$, $T$, $f$, $v_{\max}$, and $a_{\max}$ for a mass–spring system
4. Explain why the period of SHM is independent of amplitude (isochronism)
5. Apply energy conservation in SHM, including $E = \tfrac12kA^2$ and $v = \omega\sqrt{A^2-x^2}$
6. Show that a vertical spring has the same period as a horizontal one, gravity merely shifting equilibrium
7. Derive $T = 2\pi\sqrt{L/g}$ for a simple pendulum and state the validity limits of the small-angle approximation
8. Apply $T = 2\pi\sqrt{I/mgd}$ to physical pendulums, using the parallel-axis theorem from Week 6
9. Classify damping as under-, critically, or overdamped by comparing $b$ with $2\sqrt{mk}$
10. Explain why energy in a damped oscillator decays twice as fast as amplitude
11. Compute the steady-state amplitude of a driven oscillator and identify resonance
12. Explain resonance in terms of energy transfer per cycle, and give engineering examples where it is wanted and unwanted

---

## Schedule

| Day | Activity |
|-----|----------|
| Monday | Lecture 25 — Simple Harmonic Motion |
| Tuesday | Lecture 26 — Pendulums and Physical Oscillators |
| Friday | Lecture 27 — Damped and Driven Oscillations |
| Thursday | Lab 8 — The Simple Pendulum and SHM (3 hrs) |
| Friday EOD | Problem Set 8 released |

---

## Key Results

| | |
|---|---|
| SHM condition | $F = -kx$, giving $a = -\omega^2x$ |
| Solution | $x = A\cos(\omega t+\phi)$, $\omega = \sqrt{k/m}$ |
| Period | $T = 2\pi\sqrt{m/k}$ — **independent of amplitude** |
| Phase | $v$ leads $x$ by 90°; $a$ is 180° from $x$ |
| Energy | $E = \tfrac12kA^2$; $v = \omega\sqrt{A^2-x^2}$ |
| At $x = A/2$ | $U = E/4$, so $K = 3E/4$ |
| Simple pendulum | $T = 2\pi\sqrt{L/g}$; independent of mass |
| Small-angle validity | $<1\%$ error below $\approx15°$; $4.7\%$ at $30°$ |
| Physical pendulum | $T = 2\pi\sqrt{I/mgd}$; rod at end gives $2\pi\sqrt{2L/3g}$ |
| Damping | $\gamma = b/2m$; critical at $b = 2\sqrt{mk}$ |
| Energy decay | Twice as fast as amplitude ($E\propto A^2$) |
| Resonance | Amplitude peaks at $\omega\approx\omega_0$; sharpness set by $Q = \omega_0/2\gamma$ |

---

## Connections

**Back:** Week 4's energy conservation supplies $E = \tfrac12kA^2$ and everything in Part B of the
problem set. Week 6's moment of inertia and parallel-axis theorem are required for physical
pendulums. Week 3's Newton's second law is where the equation of motion comes from.

**Forward:** Week 9 couples oscillators together and finds that the result is a **wave** — the same
mathematics with position as a second variable. Week 10's resonance in air columns is this week's
driven oscillator applied to sound.

**Sideways:** MATH 141's Taylor series (Week 12) is what proves every potential minimum is harmonic
for small displacements. ECE 110's LC circuit obeys $L\ddot q + q/C = 0$, algebraically identical to
$m\ddot x + kx = 0$ — every result here transfers with a change of symbols.
