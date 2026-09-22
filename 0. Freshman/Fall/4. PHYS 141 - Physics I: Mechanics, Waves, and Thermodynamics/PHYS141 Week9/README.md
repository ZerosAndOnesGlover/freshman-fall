# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Week 9: Waves — Properties, Superposition & Standing Waves

**Semester:** Fall | **Credits:** 4 | **Lab:** Weekly 3-hr lab session

---

## Week 9 Contents

| File | Description |
|------|-------------|
| [[L28 Wave Properties]] | Transverse and longitudinal waves; $y=A\sin(kx-\omega t)$; $v=f\lambda$; $v=\sqrt{F_T/\mu}$; power; the wave equation |
| [[L29 Superposition and Interference]] | The superposition principle; constructive and destructive interference; path difference; beats; reflection and phase inversion |
| [[L30 Standing Waves]] | Standing waves from opposing travelling waves; nodes and antinodes; $f_n=nf_1$; pitch, timbre, and tuning |
| [[LAB 9 Standing Waves on a String]] | Driven string resonances; $v$ two ways; $v^2$ vs $F_T$ to extract $\mu$; beats; node positions |
| [[PS 9 Waves Superposition and Standing Waves]] | 10 problems on wave properties, interference, beats, and harmonics |
| [[QUIZ 9 Waves Superposition and Standing Waves]] | 10-question quiz (administered Monday 30 Nov, 14:00) |
| [[PHYS141 Week9/resources/Resources\|Resources]] | Textbook references, simulations, deeper reading |
| [[PHYS141 Week9/solutions_instructor/PS 9 Solutions\|PS 9 Solutions]] | Full worked solutions (instructor only) |
| [[PHYS141 Week9/solutions_instructor/LAB 9 Solutions\|LAB 9 Solutions]] | Expected data, analysis answers, systematic errors to look for |

---

## Learning Objectives

By the end of Week 9, you will be able to:

1. Distinguish transverse from longitudinal waves and explain why sound in air must be longitudinal
2. Interpret $y(x,t)=A\sin(kx-\omega t+\phi)$, identifying $A$, $k$, $\omega$, $\lambda$, $T$, $f$, and the direction of travel
3. Apply $v=f\lambda=\omega/k$ and explain which of $v$, $f$, $\lambda$ is fixed by the medium and which by the source
4. Compute wave speed on a string from $v=\sqrt{F_T/\mu}$ and explain the $\sqrt{\ }$ dependence
5. Compute transmitted power and explain its dependence on $A^2$ and $f^2$
6. State the superposition principle and explain why it follows from the linearity of the wave equation
7. Determine constructive or destructive interference from a path difference
8. Explain where the energy goes in destructive interference
9. Derive and apply $f_{\text{beat}}=\lvert f_1-f_2\rvert$, and explain why instrument tuning uses it
10. Explain why a fixed-end reflection inverts the pulse and a free-end reflection does not
11. Derive $y=2A\sin(kx)\cos(\omega t)$ and locate nodes and antinodes
12. Derive $f_n = nv/2L$ for a string fixed at both ends, and explain the origin of the quantisation
13. Distinguish pitch from timbre and relate both to the harmonic content

---

## Schedule

| Day | Activity |
|-----|----------|
| Mon 23 Nov, 14:00 | Lecture 28 — Wave Properties |
| Tue 24 Nov, 14:00 | Lecture 29 — Superposition and Interference |
| Thu 26 Nov, 14:00–17:00 | Lab 9 — Standing Waves on a String (3 hrs) |
| Fri 27 Nov, 14:00 | Lecture 30 — Standing Waves |
| Fri 27 Nov, 15:00 | Problem Set 9 released |

---

## Key Results

| | |
|---|---|
| Harmonic wave | $y = A\sin(kx-\omega t+\phi)$ |
| Wave relation | $v = f\lambda = \omega/k$ |
| String speed | $v = \sqrt{F_T/\mu}$ — quadruple $F_T$ to double $v$ |
| Speed set by | the medium; frequency by the source |
| Power | $P = \tfrac12\mu v\omega^2A^2$ — goes as $A^2$ and $f^2$ |
| Superposition | Displacements add; waves emerge unchanged |
| Two identical waves | Resultant amplitude $2A\cos(\phi/2)$ |
| Constructive / destructive | $\Delta d = m\lambda$ / $(m+\tfrac12)\lambda$ |
| Beats | Tone at $\tfrac{f_1+f_2}{2}$, pulsing at $\lvert f_1-f_2\rvert$ |
| Fixed-end reflection | **Inverted**; free-end is not |
| Standing wave | $y = 2A\sin(kx)\cos(\omega t)$ — $x$ and $t$ separate |
| Node spacing | $\lambda/2$ |
| Both ends fixed | $\lambda_n = 2L/n$, $f_n = nf_1$ |
| $n$-th harmonic | $n+1$ nodes, $n$ antinodes |
| Tuning | $f_1 \propto 1/L$, $\propto\sqrt{F_T}$, $\propto 1/\sqrt\mu$ |

---

## Connections

**Back:** Week 8's oscillator is what every point in a wave is doing. The $\omega=\sqrt{\text{stiffness}/\text{inertia}}$
pattern reappears as $v=\sqrt{F_T/\mu}$. Standing-wave resonance is Week 8's driven resonance in a
system with infinitely many natural frequencies rather than one.

**Forward:** Week 10 applies all of this to sound — air columns instead of strings, with the added
complications of the Doppler effect and the decibel scale. The $A^2$ dependence of power found here
is why loudness needs a logarithmic scale.

**Sideways:** the quantisation argument — confine a wave, get integers — is the same mechanism that
produces atomic energy levels. Decomposing a vibration into harmonics is Fourier analysis, developed
in MATH 142 and used in every audio codec and image format you will meet in CS.
