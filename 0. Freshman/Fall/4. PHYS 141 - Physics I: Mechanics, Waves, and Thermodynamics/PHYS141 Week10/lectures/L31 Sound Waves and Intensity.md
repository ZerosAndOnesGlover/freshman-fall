# PHYS 141 · Physics I: Mechanics, Waves & Thermodynamics
## Lecture 31 — Sound Waves, Intensity, and the Decibel Scale

*“The well known elevation of the pitch of wind instruments, in the course of playing, sometimes amounting to half a note, is not, as is commonly supposed, owing to any expansion of the instrument, for this should produce a contrary effect, but to the increased warmth of the air in the tube.”* — Thomas Young, "Outlines of Experiments and Inquiries Respecting Sound and Light" (1800)

**Date:** Monday 30 November 2026 · 14:00–14:50 · Week 10

**Reading:** Serway & Jewett §16.6–16.8 · HRK Ch. 19

**Coursework:** 📊 **Quiz 9** today 14:00 · 🔬 **Lab 10** Thu 3 Dec 14:00–17:00 · 📝 **PS 10** released Fri 4 Dec 15:00, due Fri 11 Dec 17:00 · 📝 **PS 9** due Fri 4 Dec 17:00

---

## Where This Fits

Week 9 developed waves in the abstract and on strings. This week applies all of it to **sound** — the
wave you have the most direct experience of, and the one where the numbers turn out to be strange
enough to need a new scale.

Everything from Week 9 carries over unchanged: $v = f\lambda$, superposition, interference, standing
waves. What sound adds is a medium that is a **gas**, an intensity that spans **twelve orders of
magnitude**, and a source that can **move**.

---

## 1. Sound Is a Longitudinal Pressure Wave

A vibrating object pushes on the air beside it, compressing it. That compression pushes the next
layer, and a **pressure disturbance** travels outward while the air molecules merely jiggle back and
forth about fixed positions.

**Sound is longitudinal because a gas has no shear stiffness.** Air cannot resist a sideways
displacement, so no transverse wave can propagate through it. Solids resist both, which is why
earthquakes produce two wave types.

There are two equivalent descriptions of the same wave:

| Description | Form | Where the maxima are |
|---|---|---|
| **Displacement** $s(x,t)$ | $s_{\max}\cos(kx-\omega t)$ | Where pressure is *unchanged* |
| **Pressure** $\Delta p(x,t)$ | $\Delta p_{\max}\sin(kx-\omega t)$ | Where displacement is *zero* |

**They are 90° out of phase.** Where the air is most compressed, individual molecules are momentarily
at rest — they have just been squeezed from both sides. This catches students out in standing-wave
problems, and Lecture 32 depends on getting it right.

---

## 2. The Speed of Sound

For a gas,

$$v = \sqrt{\frac{\gamma RT}{M}}$$

which is again Week 8's $\sqrt{\text{stiffness}/\text{inertia}}$ — here the gas's resistance to
compression over its density.

In practice, for air:

$$\boxed{v = 331\sqrt{1 + \frac{T_C}{273.15}}~\text{m/s} \;\approx\; 331 + 0.6\,T_C}$$

**Verified:**

| $T_C$ | Exact (m/s) | Linear approximation |
|---|---|---|
| $0°$ | 331.0 | 331.0 |
| $20°$ | **342.9** | 343.0 |
| $25°$ | 345.8 | 346.0 |
| $37°$ | 352.7 | 353.2 |

The linear form is accurate to about 0.5 m/s over normal temperatures.

> **Sound speed depends on temperature, not pressure.** Raising the pressure increases both the
> stiffness and the density proportionally, and the effects cancel. This is why sound travels at
> essentially the same speed at the top of a mountain as at sea level — but noticeably faster on a hot
> day.

**We use $v = 343$ m/s (room temperature) unless told otherwise.**

---

## 3. Intensity

> **Intensity** is power per unit area: $I = P/A$, in W/m².

From Week 9, wave power goes as amplitude squared, so

$$I \propto A^2$$

For a point source radiating uniformly, the power spreads over a sphere of area $4\pi r^2$:

$$\boxed{I = \frac{P}{4\pi r^2}} \qquad\Longrightarrow\qquad I \propto \frac{1}{r^2}$$

**The inverse-square law.** Double your distance and the intensity drops to a **quarter**.

**Verified** for a 0.500 W source:

| $r$ (m) | $I$ (W/m²) |
|---|---|
| 1.0 | $3.98\times10^{-2}$ |
| 2.0 | $9.95\times10^{-3}$ |
| 4.0 | $2.49\times10^{-3}$ |
| 10.0 | $3.98\times10^{-4}$ |

---

## 4. Why Decibels Exist

The quietest audible sound has intensity about $10^{-12}$ W/m². The threshold of pain is about
$1$ W/m².

**That is a factor of $10^{12}$** — a trillion. No linear scale can display that range usefully, and
worse, human perception is not linear either: a sound of twice the intensity does **not** sound twice
as loud.

So we use a logarithmic scale:

$$\boxed{\beta = 10\log_{10}\left(\frac{I}{I_0}\right)~\text{dB}} \qquad I_0 = 10^{-12}~\text{W/m}^2$$

**Verified:**

| $I$ (W/m²) | $\beta$ (dB) | Comparable to |
|---|---|---|
| $10^{-12}$ | **0** | Threshold of hearing |
| $10^{-10}$ | 20 | Rustling leaves |
| $10^{-6}$ | 60 | Conversation |
| $10^{-4}$ | 80 | Busy traffic |
| $10^{-2}$ | 100 | Pneumatic drill |
| $1$ | **120** | Threshold of pain |

### The three numbers to memorise

| Change in intensity | Change in $\beta$ |
|---|---|
| $\times 2$ | **+3.01 dB** |
| $\times 10$ | **+10 dB** |
| $\times 100$ | **+20 dB** |

**Verified.** These follow directly from $\log_{10}2 = 0.301$ and $\log_{10}10 = 1$.

> **A 3 dB increase means twice the power.** Doubling the number of identical speakers adds 3 dB, not
> 6, and certainly does not double the loudness — subjectively, about **10 dB** is needed for a sound
> to seem twice as loud, which is a factor of **ten** in intensity.

### Decibels and distance

Since $I\propto1/r^2$, doubling the distance multiplies intensity by $\tfrac14$:

$$\Delta\beta = 10\log_{10}\left(\tfrac14\right) = \mathbf{-6.02~\text{dB}}$$

**Every doubling of distance costs about 6 dB.** Verified against the table in §3: 106.0 dB at 1 m
falls to 99.98 dB at 2 m and 93.96 dB at 4 m.

---

## 5. What the Ear Actually Does

The human ear responds to roughly $20$ Hz – $20$ kHz, with sensitivity peaking near $3$–$4$ kHz —
which is, not coincidentally, where speech consonants carry most of their information.

**Sensitivity is frequency-dependent**, so a 100 Hz tone at 60 dB sounds quieter than a 3 kHz tone at
60 dB. Weighted scales (dBA) correct for this, and are what noise regulations specify.

**The ear is a logarithmic detector**, which is why the decibel scale matches perception so well. The
same is true of the eye for brightness and of many other senses — a general pattern known as the
Weber–Fechner law.

---

## 6. Summary

| | |
|---|---|
| Sound is | a **longitudinal pressure wave** |
| Displacement and pressure | **90° out of phase** |
| Speed in air | $v \approx 331 + 0.6T_C$; $343$ m/s at room temperature |
| Depends on | temperature, **not** pressure |
| Intensity | $I = P/A \propto A^2$ |
| Point source | $I = P/4\pi r^2$ — **inverse square** |
| Decibels | $\beta = 10\log_{10}(I/I_0)$, $I_0 = 10^{-12}$ W/m² |
| $\times2$ intensity | $+3$ dB |
| $\times10$ intensity | $+10$ dB |
| Double the distance | $-6$ dB |
| Twice as **loud** | about $+10$ dB, i.e. $\times10$ intensity |
| Audible range | 20 Hz – 20 kHz, most sensitive near 3–4 kHz |

---

## 7. Conceptual Questions

1. Why is sound in air longitudinal rather than transverse?

2. Why does sound travel faster on a hot day but not on a high-pressure day?

3. Two identical speakers each produce 70 dB at your position. What is the combined level? Why is it not 140 dB?

4. You move from 2 m to 8 m from a speaker. By how many dB does the level fall?

5. Why is a logarithmic scale used for sound but not, say, for length?

---

## 8. Problems

1. Find the speed of sound at $15°$C and at $35°$C.

2. A source emits 2.00 W uniformly. Find the intensity and level at 3.00 m.

3. A sound has intensity $4.00\times10^{-6}$ W/m². Find its level in dB.

4. A sound level rises from 65 dB to 85 dB. By what factor has the intensity increased?

5. At 5.00 m from a source the level is 78.0 dB. Find the level at 20.0 m, and the source's power.

6. A 500 Hz sound has $\lambda = 0.686$ m. What is the temperature of the air?

---

*Next: Lecture 32 — Standing Waves in Air Columns and Resonance*
