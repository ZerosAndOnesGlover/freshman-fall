# ECE 110 · Digital Logic
## Lab 2: Gates on a Breadboard, and NAND-Only Rebuilds
### Week 2 Lab Session

---

**Duration:** 2 hours (Friday 14:00–15:50, MEC 110)
**Format:** Pairs. **Both partners submit their own report.**
**Graded on:** completion + correctness — **100 points**
**Parts:** 74HC00 (quad NAND), 74HC02 (quad NOR), 74HC04 (hex inverter), 74HC08 (quad AND), 74HC32 (quad OR), 74HC86 (quad XOR), breadboard, LEDs, 330 Ω resistors, DIP switches
**Also:** Icarus Verilog, for the cross-check in Part D

---

## Overview

**The first hardware session.** You will build gates, measure that they do what last week's algebra said, then rebuild each one from NAND alone and confirm the rebuild is indistinguishable from the original chip.

> **Safety and sanity, in one rule: power down before rewiring.** Every 74HC chip needs
> $V_{CC}$ on pin 14 and GND on pin 7. **An unpowered chip whose inputs are driven is the most common
> way to destroy one**, and the second most common is a floating input — CMOS inputs must never be
> left unconnected.

---

## Part A — Gates on the Bench (25 pts)

**A1 (10 pts).** Wire the 74HC08 (AND), 74HC32 (OR) and 74HC86 (XOR), each with two DIP-switch inputs and an LED output through a 330 Ω resistor.

**Record the measured truth table for each.** Three tables, four rows apiece.

**A2 (8 pts).** Repeat for the 74HC00 (NAND) and 74HC02 (NOR).

**A3 (7 pts).** **Leave one NAND input floating** — disconnected from both rails — and record what the output does over about ten seconds. Then tie it high through a 10 kΩ resistor and record again.

**Report both observations.** Then explain, in two sentences, why a floating CMOS input is not the same as a logic 0.

---

## Part B — NAND-Only Rebuilds (30 pts)

**Use only the 74HC00 for this part.**

**B1 (8 pts).** Build NOT, and verify it against the 74HC04.

**B2 (8 pts).** Build AND from 2 NANDs, and verify against the 74HC08.

**B3 (7 pts).** Build OR from 3 NANDs, and verify against the 74HC32.

**B4 (7 pts).** Build XOR from **4** NANDs, and verify against the 74HC86.

**For each: record the measured truth table and state the gate count.** For B4, **say which sub-expression you wired once and fed to two places** — if you used five gates, find the sharing and rebuild it.

---

## Part C — Cost, Measured (20 pts)

**C1 (8 pts).** For each of B1–B4, tabulate: NAND gates used, **74HC00 packages needed** (four gates per package), and the transistor count at 4 transistors per NAND.

**C2 (6 pts).** Compare each rebuild's transistor count against the dedicated chip's (NOT 2, AND 6, OR 6, XOR 12).

**Which rebuilds are more expensive than the dedicated part, and which are cheaper?**

**C3 (6 pts).** **You have just found that building AND from NAND costs more transistors than an AND chip.** So why does industry build almost everything from NAND?

*Answer in terms of what is being minimised. "It is cheaper" is not the answer, since you have just measured that it is not.*

---

## Part D — The Verilog Cross-Check (25 pts)

**D1 (10 pts).** Write a Verilog module implementing each of your four B-part rebuilds **structurally** — as `nand` primitive instances wired together, not as `assign a & b`.

```verilog
module xor_from_nand(output y, input a, b);
  wire x;
  nand g1(x, a, b);
  nand g2(p, a, x);
  nand g3(q, b, x);
  nand g4(y, p, q);
endmodule
```

**D2 (8 pts).** Write a testbench that drives all four input combinations and compares each rebuild against Verilog's built-in operator (`&`, `|`, `^`, `~`).

**Report the failure count.**

> ⚠ **Use `integer` loop counters, not 1-bit `reg`s.**
>
> ```verilog
> reg a, b;
> for (a = 0; a <= 1; a = a + 1) ...   // NEVER TERMINATES
> ```
>
> A 1-bit `reg` holding 1 wraps to 0 when incremented, so `a <= 1` is *always* true and the
> simulation hangs with no error message. **Declare `integer i, j`, loop on those, and assign
> `a = i[0]`.** This bit us while preparing the lab, and it is the same class of bug as Week 0's
> two's complement overflow: a counter that silently wraps.

**D3 (7 pts).** **Do your bench measurements, your Verilog simulation, and last week's Python checker all agree?**

**Report all three verdicts for XOR.** If any two disagree, **say which you trust and why** — that judgement is the mark.

---

## Marking Summary

| Part | Points |
|---|---|
| A — gates on the bench | 25 |
| B — NAND-only rebuilds | 30 |
| C — cost, measured | 20 |
| D — the Verilog cross-check | 25 |
| **Total** | **100** |

---

## Submission

Measured truth tables (photographed or transcribed), your Verilog, your counts, and your answers. **A truth table you did not measure is worth nothing here** — this is the week the algebra has to survive contact with a chip.

---

*ECE 110 · Week 2 · Lab 2*
