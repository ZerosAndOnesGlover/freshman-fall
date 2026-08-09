# ECE 110 · Digital Logic
## Lab 8: Counters and Shift Registers on the Bench
### Week 8 Lab Session

---

**Duration:** 2 hours (Friday 14:00–15:50, MEC 110)
**Format:** Pairs. **Both partners submit their own report.**
**Graded on:** completion + correctness — **100 points**
**Parts:** 74HC74 (dual D FF) ×2, 74HC08, 74HC00, 74HC138, 74HC164 or 74HC195 (shift register), LEDs, **debounced pushbutton**, **function generator**, **oscilloscope**
**Also:** Icarus Verilog

---

## Overview

**You will build both kinds of counter and then catch the ripple counter misbehaving on a scope.**

The transient states from Thursday's lecture are not a theoretical concern — **they are visible**, and Part C is about seeing them.

---

## Part A — Ripple Counter (25 pts)

**A1 (10 pts).** Build a 3-bit ripple counter: three D flip-flops, each with $\overline Q$ tied to $D$, and each clocked by the previous stage's $Q$.

**Clock it from the pushbutton and record the sequence over 10 presses.**

**A2 (8 pts).** **How many gates did you use?** *(Count carefully — the answer is unusual.)*

**A3 (7 pts).** Now attach a 74HC138 decoder to the counter outputs, with the decoder's "0" output on an LED.

**Press through a full cycle. Does the LED light only at count 0?** Record what you see.

---

## Part B — Synchronous Counter (25 pts)

**B1 (12 pts).** Build a 3-bit **synchronous** counter: all three flip-flops on **one** clock, with

$$T_0=1,\qquad T_1=Q_0,\qquad T_2=Q_0Q_1$$

*(With D flip-flops, $D_k = Q_k \oplus T_k$.)*

**Record the sequence over 10 presses.**

**B2 (8 pts).** Count the gates. **Compare with A2.**

**B3 (5 pts).** Attach the decoder as in A3. **Does the LED still misbehave?**

---

## Part C — Catching the Transients (25 pts)

**Replace the pushbutton with a function generator at about 100 kHz.**

**C1 (12 pts).** Put the scope on the **decoder's "0" output** for the **ripple** counter. **Trigger on that output and photograph what you see.**

**You are looking for narrow pulses at times when the count is not 0.** Measure their width.

**C2 (8 pts).** Repeat with the **synchronous** counter. **Photograph the same node.**

**C3 (5 pts).** **Explain the difference from your two photographs**, referring to the state sequence from A1.

> **If you see no glitches on the ripple counter**, your scope's bandwidth or timebase may be hiding
> them — the pulses are on the order of a gate delay. **Say so in your report rather than concluding
> they are absent.**

---

## Part D — Shift Register and Simulation (25 pts)

**D1 (8 pts).** Load `1011` into a 4-bit shift register and clock it four times with serial-in 0. **Record the bit shifted out and the state each time.**

**D2 (7 pts).** Wire the last output back to the first input to make a **ring counter**. Start it at `0001` and record 8 clocks.

**What happens if you start it at `0000`?** Try it.

**D3 (10 pts).** In Verilog, write both counters and a testbench that checks each against the expected count sequence for a full cycle. **Report failures.**

Then add a **mod-10** synchronous counter with detect-and-clear, and verify it produces $0\ldots9$ and repeats. **Give the detect equation you used.**

---

## Marking Summary

| Part | Points |
|---|---|
| A — ripple counter | 25 |
| B — synchronous counter | 25 |
| C — catching the transients | 25 |
| D — shift register and simulation | 25 |
| **Total** | **100** |

---

*ECE 110 · Week 8 · Lab 8*
