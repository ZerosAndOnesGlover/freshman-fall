# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Lecture 32 — Standing Waves in Air Columns and Resonance

**Date:** Tuesday 1 December 2026 · 14:00–14:50 · Week 10

---

## Where This Fits

Week 9 put standing waves on a string, where the boundary condition was simple: clamped ends must be
nodes. This lecture does the same for a **column of air** — a flute, an organ pipe, a bottle, the
vocal tract — where the boundary conditions are subtler and produce a result strings do not: a pipe
closed at one end plays **only odd harmonics**.

That single asymmetry is why a clarinet and a flute sound so different.

---

## 1. The Boundary Conditions

Everything follows from two rules, and the difficulty is that they are stated in terms of
**displacement**, while what you hear is **pressure** — and Lecture 31 established that the two are
90° out of phase.

| End | Displacement | Pressure |
|---|---|---|
| **Closed** (rigid) | **Node** — air cannot move | Antinode |
| **Open** | **Antinode** — air moves freely | Node (fixed at atmospheric) |

> **Get this the right way round.** A closed end is a displacement *node* — the air is against a wall
> and cannot move — but a pressure *antinode*, because that is exactly where the air piles up. An open
> end is the reverse: the air swings freely, but the pressure is pinned to atmospheric.
>
> Working in displacement throughout is the safer habit, and it is what the formulas below assume.

---

## 2. Open–Open Pipe (both ends open)

Antinodes at both ends. The shortest wave fitting has one node in the middle:

$$L = \frac{n\lambda_n}{2} \qquad\Longrightarrow\qquad \boxed{\lambda_n = \frac{2L}{n}, \qquad f_n = \frac{nv}{2L} = nf_1}$$

**Identical in form to the string.** All harmonics present: $f_1, 2f_1, 3f_1, \ldots$

**Verified** for $L = 0.500$ m at $v = 343$ m/s:

| $n$ | $\lambda_n$ (m) | $f_n$ (Hz) |
|---|---|---|
| 1 | 1.000 | **343.0** |
| 2 | 0.500 | 686.0 |
| 3 | 0.333 | 1029.0 |
| 4 | 0.250 | 1372.0 |

*Flutes, recorders, and open organ pipes work this way.*

---

## 3. Closed–Open Pipe (one end closed)

Now a **node** at the closed end and an **antinode** at the open end. The shortest wave fitting is a
**quarter** wavelength, not a half:

$$L = \frac{n\lambda_n}{4} \qquad\Longrightarrow\qquad \boxed{\lambda_n = \frac{4L}{n}, \qquad f_n = \frac{nv}{4L}, \qquad n = 1, 3, 5, \ldots}$$

**Only odd $n$.** An even number of quarter-wavelengths would put the same kind of feature at both
ends, which the boundary conditions forbid.

**Verified** for the same $L = 0.500$ m:

| $n$ | $\lambda_n$ (m) | $f_n$ (Hz) |
|---|---|---|
| 1 | 2.000 | **171.5** |
| 3 | 0.667 | 514.5 |
| 5 | 0.400 | 857.5 |
| 7 | 0.286 | 1200.5 |

### Two consequences worth stating plainly

**1. The closed pipe sounds an octave lower.** $171.5$ Hz against $343.0$ Hz for the same physical
length — the fundamental is exactly **half**. A closed pipe gets the same note from half the material,
which is why the lowest organ pipes are stopped.

**2. It has a completely different timbre.** With only odd harmonics present, the sound is hollow and
"woody". **This is precisely why a clarinet (closed at the reed) sounds different from a flute (open
at both ends)**, even playing the same note — and why a clarinet overblows to a twelfth ($3f_1$)
rather than an octave ($2f_1$).

---

## 4. The End Correction

The formulas above assume the displacement antinode sits exactly at the open end. In reality the air
just outside also moves, so the antinode lies slightly **beyond** the physical opening.

The effective length is

$$L_{\text{eff}} = L + 0.6r$$

for a pipe of radius $r$, per open end.

**Verified magnitude:** for $r = 15$ mm the correction is $0.6(0.015) = \mathbf{9~\text{mm}}$ — small,
but easily measurable, and the reason a resonance-tube experiment that ignores it gives a wave speed
a few percent low.

> **In the lab, take differences.** The end correction cancels when you subtract successive resonance
> positions, which is why Lab 10 measures the **spacing** between resonances rather than the position
> of the first.

---

## 5. The Resonance Tube

Hold a vibrating tuning fork over a tube whose length can be varied (usually by raising or lowering a
water level). At certain lengths the sound becomes suddenly much louder.

This is a **closed–open** pipe, so resonances occur at

$$L = \frac{\lambda}{4},\; \frac{3\lambda}{4},\; \frac{5\lambda}{4},\; \ldots$$

**Successive resonances are $\lambda/2$ apart** — and that spacing is free of the end correction.

**Verified** for a 512 Hz fork at $v = 343$ m/s: $\lambda = 0.670$ m, so the first resonance is near
$0.167$ m (less the end correction) and successive ones are $\mathbf{0.335~\text{m}}$ apart.

**Measure the spacing, double it to get $\lambda$, multiply by $f$, and you have the speed of sound.**
That is Lab 10 in one sentence.

---

## 6. Resonance Elsewhere

The same physics, with the same consequences:

- **Blowing across a bottle.** A closed–open pipe. Fill it with water, shorten the air column, raise
  the pitch.
- **The vocal tract.** Roughly a closed–open pipe about 17 cm long, giving a fundamental resonance
  near $343/(4\times0.17) \approx 500$ Hz. Shaping the tract moves these resonances — called
  **formants** — and that is how vowels are distinguished.
- **Room acoustics.** A room is a three-dimensional resonant cavity. Its modes cause the bass to
  boom in some spots and vanish in others, which is what acoustic treatment addresses.
- **Helmholtz resonators.** A cavity with a neck — a bass-reflex speaker port, or the sound hole of a
  guitar.

---

## 7. Summary

| | |
|---|---|
| Closed end | displacement **node**, pressure antinode |
| Open end | displacement **antinode**, pressure node |
| Open–open | $\lambda_n = 2L/n$, $f_n = nv/2L$ — **all** harmonics |
| Closed–open | $\lambda_n = 4L/n$, $f_n = nv/4L$ — **odd only** |
| Closed pipe fundamental | **half** that of an open pipe of equal length |
| Clarinet vs flute | closed vs open ⟹ odd-only vs all harmonics |
| Clarinet overblows to | a twelfth ($3f_1$), not an octave |
| End correction | $L_{\text{eff}} = L + 0.6r$ per open end |
| Successive resonances | $\lambda/2$ apart — correction cancels |

---

## 8. Conceptual Questions

1. Why is a closed end a displacement node but a pressure antinode?

2. Two pipes of equal length, one open at both ends and one closed at one. Which plays the lower fundamental, and by what factor?

3. Why does a clarinet overblow to a twelfth while a flute overblows to an octave?

4. You blow across a bottle, then add water. Does the pitch rise or fall? Why?

5. Why does taking the *difference* between successive resonance lengths eliminate the end correction?

---

## 9. Problems

1. An open–open pipe is 0.750 m long. Find its first three harmonics at $v = 343$ m/s.

2. A closed–open pipe is 0.750 m long. Find its first three harmonics. Compare with Problem 1.

3. A closed–open pipe has a fundamental of 220 Hz. Find its length and its next two harmonics.

4. A resonance tube with a 384 Hz fork resonates at 0.216 m and again at 0.663 m. Find $\lambda$, the speed of sound, and the end correction.

5. An open pipe 0.400 m long has radius 12.0 mm. Find its fundamental with and without the end correction, and the percentage difference.

6. A vocal tract is modelled as a 17.0 cm closed–open pipe. Estimate its first two resonances.

---

*Next: Lecture 33 — The Doppler Effect*
