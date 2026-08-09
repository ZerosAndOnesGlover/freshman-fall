# ECE 110 · Digital Logic
## Lab 8 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.**

---

## Part A — Ripple Counter (25 pts)

### A1 (10)

**Correct count sequence $0\ldots7$ repeating.** *(Verified.)*

### A2 (8)

$$\boxed{\text{Zero gates.}}$$

**Three flip-flops, three wires from $\overline Q$ to $D$, and the clock chain. Nothing else.**

*Marking: 8. **Students who report a gate count above zero have added something unnecessary** — check their wiring, it usually still works.*

### A3 (7)

**The "0" LED flashes at count 0 *and* briefly at other transitions.** At the pushbutton's speed the glitches are far too narrow to see — **expect students to report the LED behaving correctly here.**

**That is the right observation at this speed**, and Part C is what changes it.

*Marking: 7 for an honest record. **Do not penalise "it looked fine"** — that is true at 1 Hz.*

---

## Part B — Synchronous Counter (25 pts)

### B1 (12), B2 (8)

**Same count sequence.** Gates: **one AND** for $T_2=Q_0Q_1$, plus the XORs to drive the D inputs.

**Against A2's zero.** *(The comparison is the mark.)*

### B3 (5)

**No misbehaviour** — and at pushbutton speed this looks identical to A3, which is exactly why Part C exists.

---

## Part C — Catching the Transients (25 pts)

### C1 (12) — the ripple counter on a scope

**Expected: narrow pulses on the decoder's "0" output at transitions where the count is not 0** — specifically on $011\to100$ and $111\to000$, where the counter passes through `000`.

**Pulse width: on the order of one to two gate delays**, tens of nanoseconds for 74HC parts.

*Marking: 8 photograph, 4 measured width. **A report stating no glitches were visible, with the scope settings given and the bandwidth limitation acknowledged, earns 10 of 12.** Honest negative results are acceptable; unexamined ones are not.*

### C2 (8) — the synchronous counter

**Clean.** The "0" output asserts only during count 0.

### C3 (5)

**The ripple counter's bits change in sequence**, so between $011$ and $100$ the outputs pass through $010$ and then $000$ — *(verified)* — and the decoder faithfully decodes `000` during that window.

**The synchronous counter's bits change together**, so no invalid state is ever presented.

*Marking: 5. **The explanation must reference the actual intermediate states**, not just "it is synchronous".*

---

## Part D — Shift Register and Simulation (25 pts)

### D1 (8)

| clock | out | state |
|:-:|:-:|:-:|
| 1 | 1 | `0101` |
| 2 | 1 | `0010` |
| 3 | 0 | `0001` |
| 4 | 1 | `0000` |

*(Verified.)*

### D2 (7)

$$\texttt{0001}\to\texttt{0010}\to\texttt{0100}\to\texttt{1000}\to\texttt{0001}\to\cdots$$

*(Verified.)*

**Started at `0000`: it stays at `0000` forever.** **The lesson is that reset is mandatory.**

*Marking: 4 sequence, **3 for trying `0000` and drawing the conclusion.***

### D3 (10)

**Both counters verified over a full cycle: 0 failures.**

**Mod-10 with $\text{clear}=Q_3Q_1$ produces $0,1,\ldots,9,0,\ldots$** *(Verified.)*

*Marking: 6 the two counters, **4 for the mod-10 with its detect equation stated.***

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 25 |
| C | 25 |
| D | 25 |
| **Total** | **100** |

---

## Checkoff Checklist

1. **A2 reports zero gates**
2. A3 recorded honestly at low speed
3. B2 compares gate counts with A2
4. **C1 photographs the glitch, or documents why it was not visible**
5. **C3 names the actual intermediate states**
6. **D2 tries `0000` and concludes reset is mandatory**
7. D3 states the mod-10 detect equation

---

## Note for the Debrief

**Run C1 and C2 side by side on the projector if you can.**

> **At pushbutton speed both counters looked perfect.** On the scope at 100 kHz, one of them is
> putting out pulses that should not exist — **and the counter is not broken. It is doing exactly
> what it was built to do.**
>
> **The ripple counter passes through 2 and then 0 on its way from 3 to 4**, and the decoder is
> correctly decoding a state the designer never intended to exist.

Then the consequence, plainly:

> **If that decoder output were a memory write-enable, you would have just written to the wrong
> address — at speed, intermittently, and invisibly to single-stepping.** This class of bug is why
> synchronous design is a discipline rather than a preference.

Then the arc:

> **Week 3: a serial dependency made an adder too slow. Week 8: the same serial dependency makes a
> counter both slow and wrong.** In both cases you fix it by spending gates to break the chain.
>
> **You have now met that trade three times.** Next week you will design state machines, and the
> first thing you will do is put every flip-flop on the same clock — **because of what you saw on
> the scope today.**

---

*ECE 110 · Week 8 · Lab 8 Solutions · Instructor Only*
