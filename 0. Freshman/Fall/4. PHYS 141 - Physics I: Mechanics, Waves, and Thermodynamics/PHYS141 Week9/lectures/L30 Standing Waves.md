# PHYS 141 — Physics I: Mechanics, Waves & Thermodynamics
## Lecture 30 — Standing Waves and Resonance on Strings

---

## Where This Fits

Lecture 29 established two facts: waves superpose, and a wave reflects inverted from a fixed end.

Put them together on a string clamped at both ends. The wave you send travels to the far end,
reflects, comes back, reflects again — and interferes with itself, endlessly. **Most frequencies
produce a jumble that cancels itself out. A special few produce a stable, dramatic pattern.**

Those few are the **resonant frequencies**, and they are why a string has a pitch at all.

---

## 1. Two Opposing Waves

Superpose identical waves travelling in opposite directions:

$$y = A\sin(kx-\omega t) + A\sin(kx+\omega t)$$

The sum-to-product identity gives

$$\boxed{y(x,t) = 2A\sin(kx)\cos(\omega t)}$$

**Look at what happened to the structure.** The original waves had $x$ and $t$ locked together in
$(kx \mp \omega t)$ — that coupling is what made them travel. Here they are **separated**: a fixed
spatial shape $\sin(kx)$, multiplied by an oscillation in time $\cos(\omega t)$.

**Nothing propagates.** Every point oscillates in place, with an amplitude $2A\sin(kx)$ that depends
only on where it is. This is a **standing wave**.

| Feature | Position | Amplitude |
|---|---|---|
| **Node** | $\sin(kx)=0$, i.e. $x = 0, \tfrac\lambda2, \lambda, \ldots$ | **Zero** — never moves |
| **Antinode** | $\lvert\sin(kx)\rvert=1$, i.e. $x = \tfrac\lambda4, \tfrac{3\lambda}4,\ldots$ | **$2A$** — maximum |

Adjacent nodes are $\lambda/2$ apart, and antinodes sit halfway between them.

---

## 2. The Boundary Condition Quantises the Frequency

A string fixed at both ends **must** have a node at each end. That is not a choice — the clamps
enforce it.

With nodes at $x=0$ and $x=L$, an exact whole number of half-wavelengths must fit:

$$L = n\frac{\lambda_n}{2} \qquad\Longrightarrow\qquad \boxed{\lambda_n = \frac{2L}{n}} \qquad n = 1,2,3,\ldots$$

and since $v = f\lambda$ with $v$ fixed by the medium,

$$\boxed{f_n = \frac{nv}{2L} = \frac{n}{2L}\sqrt{\frac{F_T}{\mu}} = n f_1}$$

> **This is quantisation, and it arises from geometry alone.** Confine a wave and only certain
> frequencies survive. Exactly the same argument — a wave, a boundary, an integer — gives the
> discrete energy levels of an atom. You are meeting the mechanism here first, in a form you can
> photograph.

$f_1$ is the **fundamental**; $f_n = nf_1$ are the **harmonics**.

### Worked example — verified

$L = 1.20$ m, $F_T = 80.0$ N, $\mu = 5.00\times10^{-3}$ kg/m, so $v = 126.5$ m/s.

| $n$ | $\lambda_n$ (m) | $f_n$ (Hz) | Nodes | Antinodes |
|---|---|---|---|---|
| 1 | 2.400 | **52.70** | 2 | 1 |
| 2 | 1.200 | 105.41 | 3 | 2 |
| 3 | 0.800 | 158.11 | 4 | 3 |
| 4 | 0.600 | 210.82 | 5 | 4 |
| 5 | 0.480 | 263.52 | 6 | 5 |

The $n$-th harmonic has $n+1$ nodes (counting both ends) and $n$ antinodes.

**For $n=3$ on this string**, nodes sit at $x = 0, 0.400, 0.800, 1.200$ m and antinodes at
$x = 0.200, 0.600, 1.000$ m — verified.

---

## 3. Why Only These Frequencies

Drive the string at an arbitrary frequency and the reflected wave returns out of step with the wave
still being sent. Successive round trips arrive at random phases and largely cancel: the string
shivers weakly.

Drive it at $f_n$ and every reflection returns **exactly in phase** with the outgoing wave. Each
round trip adds constructively, and the amplitude builds until damping limits it.

**This is Week 8's resonance, in a system with many natural frequencies instead of one.** A
mass–spring has a single $\omega_0$; a string has an infinite ladder $f_1, 2f_1, 3f_1, \ldots$

---

## 4. Why Instruments Sound Different

A plucked string does not vibrate in one mode. It vibrates in **many simultaneously** — superposition
again — with amplitudes set by how and where it was plucked.

- The **fundamental** $f_1$ sets the perceived **pitch**.
- The **relative strengths of the harmonics** set the **timbre**.

**A violin and a flute playing A440 both have $f_1 = 440$ Hz.** They sound different because their
harmonic recipes differ. Plucking a guitar string near the bridge emphasises high harmonics and
sounds bright; plucking over the soundhole emphasises the fundamental and sounds mellow. Same string,
same pitch, different sound.

*Decomposing a complex vibration into its harmonics is **Fourier analysis** — the same mathematics
behind MP3 compression, JPEG images, and every spectrum analyser. MATH 142 develops the series.*

### Tuning a string

$$f_1 = \frac{1}{2L}\sqrt{\frac{F_T}{\mu}}$$

Three ways to change the pitch, all visible in the formula:

| Change | Effect |
|---|---|
| **Shorten $L$** (fret it) | $f_1 \propto 1/L$ — halving the length raises the pitch an octave |
| **Increase $F_T$** (tune it) | $f_1 \propto \sqrt{F_T}$ — quadruple tension for one octave |
| **Heavier string** (bass strings) | $f_1 \propto 1/\sqrt{\mu}$ — thicker strings play lower at the same tension |

**A guitar uses all three:** six strings of different $\mu$, each tensioned to pitch, then fretted to
change $L$.

---

## 5. Summary

| | |
|---|---|
| Standing wave | $y = 2A\sin(kx)\cos(\omega t)$ — $x$ and $t$ **separate** |
| Nothing propagates | each point oscillates in place |
| Node spacing | $\lambda/2$; antinodes halfway between |
| Both ends fixed | $\lambda_n = 2L/n$, $f_n = nv/2L = nf_1$ |
| $n$-th harmonic | $n+1$ nodes, $n$ antinodes |
| Why quantised | boundary conditions + integer number of half-wavelengths |
| Resonance | reflections return in phase and build |
| Pitch | set by $f_1$ |
| Timbre | set by the harmonic mix |
| Tuning | $f_1 \propto 1/L$, $\propto\sqrt{F_T}$, $\propto 1/\sqrt{\mu}$ |

---

## 6. Conceptual Questions

1. In a standing wave, which points never move? Which move most? How far apart are they?

2. Why does a string fixed at both ends vibrate only at certain frequencies, while a wave on an infinite string can have any frequency?

3. A guitarist frets a string exactly halfway. What happens to the fundamental frequency?

4. Two guitar strings have the same length and tension but different thicknesses. Which plays the lower note?

5. A violin and a flute both play A440. Why can you tell them apart?

---

## 7. Problems

1. A 0.650 m string fixed at both ends carries waves at 240 m/s. Find $f_1$ and the first four harmonics.

2. A string's third harmonic is 420 Hz. Find its fundamental and its fifth harmonic.

3. A 1.50 m string has $\mu = 4.00$ g/m and is under 100 N tension. Find $v$, $f_1$, and $\lambda_1$.

4. A string 0.800 m long vibrates in its fourth harmonic. Give the positions of all nodes and antinodes.

5. A guitar string sounds 196 Hz open. Where must a fret be placed to sound 262 Hz? Give the distance from the nut as a fraction of the string length.

6. A string is tuned to 440 Hz. By what factor must the tension change to raise it to 494 Hz? Comment on whether this is practical.

---

*Next: Week 10 — Sound: the Doppler Effect, Resonance, and Decibels*
