# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Lecture 33 — The Doppler Effect

**Date:** Friday 4 December 2026 · 14:00–14:50 · Week 10

---

## Where This Fits

Everything so far assumed the source and the listener stay put. This lecture removes that assumption,
and the result is the one piece of wave physics everybody has already experienced: **the pitch of a
passing siren drops as it goes by.**

The explanation is purely geometric — no new physics, just careful bookkeeping about where wavefronts
end up. But the consequences run from traffic enforcement to the expansion of the universe.

---

## 1. The Idea

The source emits crests at a fixed rate. If the source **moves towards** you, each successive crest is
emitted from a point slightly closer, so it has less distance to cover and arrives sooner than it
otherwise would. The crests arrive **more often**: the frequency you receive is higher.

**The source has not changed what it emits.** The wavelength in front of it has been compressed by the
motion, and since $v$ is fixed by the air, a shorter $\lambda$ means a higher $f$.

Behind the source the opposite happens — wavefronts are stretched apart, and the pitch drops.

---

## 2. The General Formula

$$\boxed{f' = f\left(\frac{v + v_o}{v - v_s}\right)}$$

| Symbol | Meaning |
|---|---|
| $f$ | Emitted frequency |
| $f'$ | Received frequency |
| $v$ | Speed of sound in the medium |
| $v_o$ | Observer's speed, **positive when moving towards the source** |
| $v_s$ | Source's speed, **positive when moving towards the observer** |

> **The sign convention is the whole difficulty.** Memorising it is unreliable. Instead, apply this
> check every time:
>
> **Approaching ⟹ higher pitch. Receding ⟹ lower pitch.**
>
> Compute, then verify your answer moved in the right direction. If it did not, you have a sign wrong.
> This single habit prevents nearly every error in this topic.

### Verified, with $f = 1000$ Hz and $v = 343$ m/s

| Situation | $v_s$ | $v_o$ | $f'$ (Hz) | Check |
|---|---|---|---|---|
| Source approaching at 30 m/s | $+30$ | 0 | **1095.8** | higher ✓ |
| Source receding at 30 m/s | $-30$ | 0 | **919.6** | lower ✓ |
| Observer approaching at 30 m/s | 0 | $+30$ | **1087.5** | higher ✓ |
| Observer receding at 30 m/s | 0 | $-30$ | **912.5** | lower ✓ |

---

## 3. Moving Source and Moving Observer Are Not Equivalent

Look carefully at the table. A source approaching at 30 m/s gives **1095.8** Hz; an observer
approaching at 30 m/s gives **1087.5** Hz. **The same relative speed produces different shifts.**

This surprises people, and the reason matters.

- A **moving source** changes the **wavelength** in the medium — it physically bunches the wavefronts
  up. The denominator carries $v_s$.
- A **moving observer** does not affect the wave at all. The wavelength is unchanged; the observer
  simply runs into more crests per second. The numerator carries $v_o$.

**The medium breaks the symmetry.** Sound propagates through air, and "moving" means moving relative
to that air — so the two cases are genuinely different physical situations.

> **For light there is no medium**, and Einstein's relativistic Doppler formula depends only on the
> *relative* velocity. That asymmetry vanishing is one of the observations that led to special
> relativity.

---

## 4. Worked Example — The Ambulance

A siren emits 660 Hz. The ambulance travels at 25 m/s; you stand still. $v = 343$ m/s.

**Approaching:**
$$f' = 660\left(\frac{343}{343-25}\right) = \mathbf{711.9~\text{Hz}}$$

**Receding:**
$$f' = 660\left(\frac{343}{343+25}\right) = \mathbf{615.2~\text{Hz}}$$

**The drop as it passes is $711.9 - 615.2 = 96.7$ Hz** — nearly a musical minor third, which is why
the change is so obvious.

**Note the shift is not symmetric about 660 Hz**: it rises by 51.9 Hz and falls by 44.8 Hz. The
formula is not linear in $v_s$, and the approaching shift is always the larger.

---

## 5. Shock Waves and the Sonic Boom

What if the source moves as fast as the wave it emits?

At $v_s = v$ the wavefronts pile up into a single flat front. Beyond it, $v_s > v$, the source
outruns its own sound and the wavefronts form a cone trailing behind, with half-angle

$$\sin\theta = \frac{v}{v_s} = \frac{1}{M}$$

where $M$ is the **Mach number**.

**Verified:**

| Mach | Cone half-angle |
|---|---|
| 1.0 | $90.0°$ |
| 1.5 | $41.8°$ |
| 2.0 | $30.0°$ |

> **A sonic boom is not a single event at the moment of "breaking the sound barrier".** The cone
> trails the aircraft continuously, so the boom sweeps along the ground beneath its whole supersonic
> flight path. Anyone standing on that line hears one bang as the cone passes them.

---

## 6. Where It Is Used

| Application | How |
|---|---|
| **Speed cameras** | Radar reflects off a car; the frequency shift gives the speed |
| **Doppler ultrasound** | Shift from moving red blood cells gives blood flow speed and direction |
| **Weather radar** | Shift from raindrops maps wind fields inside storms |
| **Astronomy** | Spectral lines shifted **red** ⟹ receding, **blue** ⟹ approaching |
| **Hubble expansion** | Distant galaxies are all redshifted, and more so with distance |
| **Satellite tracking** | The Doppler curve of a passing satellite gives its orbit — the principle behind the first GPS ancestors |

**The redshift row is worth a moment.** Measuring that essentially every distant galaxy is receding —
and faster the further away it is — is how we learned the universe is expanding. The physics is what
you have just done with an ambulance.

---

## 7. Summary

| | |
|---|---|
| General formula | $f' = f\dfrac{v+v_o}{v-v_s}$ |
| Sign convention | Both positive when moving **towards** each other |
| **The check** | Approaching ⟹ higher; receding ⟹ lower. Verify every answer |
| Moving source | Changes the **wavelength** in the medium |
| Moving observer | Changes the **rate of encountering** crests |
| The two are | **not** equivalent — the medium breaks the symmetry |
| For light | No medium; only relative velocity matters (relativistic Doppler) |
| Ambulance example | 660 Hz → 711.9 Hz approaching, 615.2 Hz receding |
| Shock cone | $\sin\theta = 1/M$ |
| Sonic boom | Sweeps continuously along the flight path |

---

## 8. Conceptual Questions

1. A siren passes you at constant speed. Sketch the pitch you hear against time. Is the change gradual or sudden?

2. Why do a moving source and a moving observer at the same speed give different frequency shifts?

3. You move towards a stationary source. Does the **wavelength** in the air change? Does the frequency you hear?

4. Why is there no Doppler shift when a source moves in a circle around you at constant radius?

5. Why does the Doppler formula for light not distinguish between a moving source and a moving observer?

---

## 9. Problems

1. A train sounds a 440 Hz horn while approaching at 30.0 m/s. Find the frequency heard by a stationary observer, and again after it has passed. Take $v = 343$ m/s.

2. You drive at 25.0 m/s towards a stationary 500 Hz siren. What frequency do you hear? What if you drive away at the same speed?

3. A car approaches a stationary 800 Hz source at 20.0 m/s while the source also moves towards the car at 15.0 m/s. Find the received frequency.

4. A stationary observer hears 1050 Hz from a siren approaching at 22.0 m/s. What is the siren's true frequency?

5. A bat emits 45.0 kHz and flies at 8.00 m/s towards a stationary wall. Find the frequency striking the wall, and the frequency the bat hears reflected back. *(Two Doppler shifts.)*

6. An aircraft flies at Mach 1.8. Find the half-angle of its shock cone.

---

*Next: Week 11 — Thermodynamics I: Temperature, Heat, and Thermal Expansion*
