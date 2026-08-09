# ECE 110 · Digital Logic
## Lab 3: Building and Timing a 4-Bit Ripple-Carry Adder
### Week 3 Lab Session

---

**Duration:** 2 hours (Friday 14:00–15:50, MEC 110)
**Format:** Pairs. **Both partners submit their own report.**
**Graded on:** completion + correctness — **100 points**
**Parts:** 74HC86 (quad XOR), 74HC08 (quad AND), 74HC32 (quad OR), breadboard, DIP switches, LEDs, 330 Ω resistors
**Also:** Icarus Verilog

---

## Overview

**This is the first circuit in the course you cannot check by looking at it.**

A 4-bit adder has **512** input combinations. You will verify a sample by hand on the bench, verify **all** of them in simulation, and then measure the thing the truth table cannot tell you: **how long it takes.**

> **The lab's real subject is the gap between "correct" and "usable".** By the end you will have a
> working adder and a measured reason why nobody builds a 64-bit one this way.

---

## Part A — One Full Adder (25 pts)

**A1 (10 pts).** Build a **half adder** (1 XOR, 1 AND). Record its 4-row truth table from the bench.

**A2 (10 pts).** Build a **full adder** from two half adders plus an OR gate. Record all **8** rows.

**Verify on every row that $S + 2C_{out} = A+B+C_{in}$.**

**A3 (5 pts).** Count the gates. **Which chips did you use, and how many packages?**

---

## Part B — Four Bits (25 pts)

**B1 (12 pts).** Chain four full adders into a 4-bit ripple-carry adder. **Wire $A$ and $B$ to DIP switches, the five outputs to LEDs.**

**B2 (8 pts).** Test at least these, and record the LED readings:

| $A$ | $B$ | $C_{in}$ | expected |
|---|---|---|---|
| 0011 | 0101 | 0 | 01000 |
| 1111 | 0001 | 0 | 10000 |
| 1010 | 0101 | 0 | 01111 |
| 1111 | 1111 | 1 | 11111 |

**B3 (5 pts).** **You have now checked 4 of 512 combinations.** What fraction is that, and what does passing them entitle you to conclude?

---

## Part C — All 512, In Simulation (25 pts)

**C1 (12 pts).** Write the adder **structurally** in Verilog — `xor`, `and`, `or` primitive instances wired into half adders, half adders into full adders, full adders into the chain. **No `assign a + b`.**

**C2 (8 pts).** Write a testbench sweeping every $A$, every $B$ and both carry-ins, comparing `{cout, sum}` against Verilog's `a + b + cin`.

**Report cases tested and failures.**

> ⚠ **Two traps, both of which caught us while preparing this lab.**
>
> **Use `integer` loop counters**, not 1-bit `reg`s — a 1-bit counter wraps and the loop never ends.
>
> **Mind the width of your comparison.** `sum` is 4 bits; `a + b` in a Verilog `integer` context is
> not. Comparing them directly reports hundreds of false failures. **Mask, or compare `{cout,sum}`
> against the full-width value.**

**C3 (5 pts).** **Do your four bench readings appear among the 512 simulated cases, with the same answers?** Confirm explicitly.

---

## Part D — Timing (25 pts)

**D1 (10 pts).** Using **one unit per gate**, compute the arrival time of every output of your 4-bit adder. **What is the critical path, and which output is on it?**

**D2 (8 pts).** Derive $t = 2N+1$ from your stage-by-stage analysis, and **check it at $N=2,3,4$** by extending or shortening your model.

**D3 (7 pts).** Extrapolate to $N = 8, 16, 32, 64$. At **20 ps per gate**, tabulate the delay in nanoseconds.

**A 3 GHz processor has a 0.33 ns clock period. State plainly whether a 64-bit ripple-carry adder can be used in one, and give the number that settles it.**

---

## Marking Summary

| Part | Points |
|---|---|
| A — one full adder | 25 |
| B — four bits | 25 |
| C — all 512, in simulation | 25 |
| D — timing | 25 |
| **Total** | **100** |

---

## Submission

Bench truth tables, your Verilog and testbench, your case/failure counts, and your timing tables.

> **Part D is the half of this lab that will still matter in Week 6.** Do not rush it to get the LEDs
> blinking.

---

*ECE 110 · Week 3 · Lab 3*
