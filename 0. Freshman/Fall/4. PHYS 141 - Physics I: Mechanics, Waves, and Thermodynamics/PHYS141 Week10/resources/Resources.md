# PHYS 141 · Week 10 Resources

## Required Textbook Reading

- **HRK:** Ch. 19 (Sound Waves) — §19.1–19.8, covering intensity, the decibel scale, resonance in
  pipes, and the Doppler effect
- **Serway:** Ch. 17 (Sound Waves) — all sections; Ch. 18 §18.6–18.8 for standing waves in air columns

## Simulations

- **PhET "Sound Waves"** — shows the pressure variation as moving bands of compression and
  rarefaction. Switch between the displacement and pressure views to make the 90° phase relationship
  of Lecture 31 concrete; it is the fastest way to fix that idea.
- **PhET "Wave Interference"** — set the source to *Sound* and add a second speaker to see acoustic
  interference fringes.
- Search for an interactive **Doppler effect** simulation where you can drag the source and vary its
  speed. Push $v_s$ past $v$ and the Mach cone forms visibly — much clearer than the static figure in
  any textbook.

## Practical Tools

- **A phone spectrum analyser app** (there are many free ones) turns your handset into a usable
  frequency meter. It is accurate enough for Part 4 of the lab and worth installing before the
  session.
- **A sound level meter app**, if calibrated against a known source, is adequate for Part 3. Absolute
  accuracy is poor, but the *relative* measurements the inverse-square law needs are fine.

## Video Demonstration Recommendations

- Any recording of an **ambulance or racing car passing a stationary microphone** — the pitch drop is
  audible and can be measured directly from the recording with a spectrum app. Real data, free.
- **Rijke tube** or **singing flame** demonstrations show acoustic resonance driven by heat, and are
  memorable.
- Footage of **aircraft shock cones** made visible by condensation shows the Mach cone of Lecture 33
  directly.

## Deeper Reading

- Feynman, *Feynman Lectures Vol. 1*, Ch. 47 ("Sound. The wave equation") — derives the wave equation
  for sound from first principles, including why the speed depends on temperature.
- Rayleigh, *The Theory of Sound* (1877), Vol. 2 — the classical reference on pipes and resonators;
  the end-correction result is his.
- Anything on **room acoustics** if the modal behaviour mentioned in Lecture 32 interests you; it is a
  direct three-dimensional extension of the standing-wave analysis.

## Why the Decibel Scale Is Everywhere (Enrichment)

The decibel is not a unit of sound. It is a **dimensionless ratio expressed logarithmically**, and
once defined it turned out to be useful across all of engineering:

- **Signal-to-noise ratio** in any communication system
- **Amplifier gain** — cascaded stages *multiply* their gains, so in dB they simply **add**, which is
  why circuit diagrams are annotated in dB
- **Antenna gain**, **optical fibre loss** (dB per kilometre), **radar cross-section**

The reason is always the same: quantities spanning many orders of magnitude become manageable, and
multiplication becomes addition. The ear's logarithmic response was the historical motivation, but the
mathematics stands on its own.

**Note the factor of 10 versus 20.** For *power* ratios, $\beta = 10\log_{10}(P_2/P_1)$. For
*amplitude* ratios — voltage, pressure — it is $20\log_{10}(A_2/A_1)$, because power goes as amplitude
squared. Both describe the same physical change; the factor of two comes from the square. Confusing
them is the commonest error in the whole topic.

## Common Pitfalls This Week

1. **Getting the pipe boundary conditions backwards.** A closed end is a displacement **node** and a
   pressure **antinode**. Work in displacement consistently and you will not go wrong.

2. **Using $f_n = nv/2L$ for a closed pipe.** Closed–open pipes obey $f_n = nv/4L$ with **odd $n$
   only**. This single error accounts for most lost marks in Part C of the problem set.

3. **Doppler sign errors.** Do not memorise the convention. Predict the direction of the shift first,
   compute, and check the answer moved that way.

4. **Adding decibels arithmetically.** Two 70 dB sources give 73 dB, not 140 dB. Convert to intensity,
   add, and convert back.

5. **Confusing $10\log$ with $20\log$.** Ten for power and intensity; twenty for amplitude and
   pressure.

6. **Forgetting the end correction** in the resonance tube, then wondering why the speed of sound
   comes out a few percent low. Take differences between resonances and the problem disappears.
