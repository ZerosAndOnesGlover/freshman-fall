# PHYS 141 · Week 9 Resources

## Required Textbook Reading

- **HRK:** Ch. 18 (Wave Motion) — §18.1–18.8; Ch. 19 (Sound Waves) §19.1 for the transition to Week 10
- **Serway:** Ch. 16 (Wave Motion) — all sections; Ch. 18 (Superposition and Standing Waves) §18.1–18.5

## Simulations

- **PhET "Wave on a String"** — the single most useful simulation this week. Set the end to *fixed*
  and send a pulse: the inversion in Lecture 29 is unmistakable. Switch to *loose* and it vanishes.
  The damping and tension sliders let you reproduce most of Lab 9 before you enter the lab.
- **PhET "Wave Interference"** — two-source interference patterns. Drag the sources apart and watch
  the fringes tighten; this is the path-difference condition made visible.
- **PhET "Normal Modes"** — a chain of coupled oscillators. Increase the number of masses and the
  discrete modes become recognisable as the harmonics of a continuous string.
- **PhET "Fourier: Making Waves"** — build a square wave by adding harmonics. This is the timbre
  discussion of Lecture 30, and a preview of MATH 142.

## Video Demonstration Recommendations

- Any recording of a **driven string with a strobe light** — the standing-wave pattern freezes and the
  nodes become visibly stationary while the antinodes blur.
- **Chladni plates**: sand on a driven metal plate collects at the nodal *lines*, making
  two-dimensional standing waves directly visible. The patterns are strikingly beautiful and are the
  same physics one dimension up.
- A **ripple tank** with two dipping sources shows interference fringes forming in real time.

## Deeper Reading

- Feynman, *Feynman Lectures Vol. 1*, Ch. 47–49 — sound, waves, and modes. Ch. 49 ("Modes") makes the
  connection between standing waves and quantum energy levels explicitly, which is worth reading even
  if the quantum content is unfamiliar.
- Rayleigh, *The Theory of Sound* (1877) — still the reference work, and remarkably readable in its
  early chapters.

## Why Standing Waves Matter Beyond Strings (Enrichment)

The argument in Lecture 30 — confine a wave, impose boundary conditions, and only integer numbers of
half-wavelengths survive — is one of the most transferable results in physics.

- **Atomic structure.** An electron confined to an atom is a wave subject to boundary conditions. The
  allowed standing-wave patterns are the orbitals, and their discrete frequencies are the energy
  levels. The reason atoms have line spectra rather than continuous ones is *the same reason a guitar
  string has a pitch*.
- **Optical cavities.** A laser is a light wave standing between two mirrors; only wavelengths fitting
  an integer number of half-wavelengths survive, which is what makes laser light monochromatic.
- **Microwave ovens.** The standing wave inside has fixed nodes where food never heats — hence the
  turntable. You can measure the wavelength of the microwaves by melting chocolate in a stationary
  oven and measuring the spacing of the melted patches, then multiply by the stated frequency to
  recover $c$ to within a few percent.
- **Structural engineering.** Buildings, bridges, and turbine blades all have modal frequencies, and
  designing so that operating conditions avoid them is a routine part of the job.

## Common Pitfalls This Week

1. **Thinking the medium travels with the wave.** It does not. A cork on a ripple bobs and stays. The
   wave carries energy and momentum, not matter.

2. **Assuming a higher-frequency source makes a faster wave.** It does not. $v$ is fixed by the
   medium; raising $f$ lowers $\lambda$ so that $f\lambda$ stays constant.

3. **Doubling tension to double speed.** $v\propto\sqrt{F_T}$, so doubling the speed needs **four
   times** the tension. Students lose marks on this in almost every cohort.

4. **Treating destructive interference as energy destruction.** Energy is redistributed to regions of
   constructive interference; the total is conserved.

5. **Getting the beat frequency wrong by a factor of two.** The *envelope* oscillates at
   $\lvert f_1-f_2\rvert/2$, but loudness peaks at **both** extremes of the envelope, so the audible
   beat rate is $\lvert f_1-f_2\rvert$. Lecture 29 §4 works through this carefully.

6. **Miscounting nodes.** The $n$-th harmonic has $n$ antinodes and $n+1$ nodes, because both fixed
   ends count.
