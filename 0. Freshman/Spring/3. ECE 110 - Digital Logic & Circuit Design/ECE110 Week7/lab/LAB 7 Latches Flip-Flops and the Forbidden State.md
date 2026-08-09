# ECE 110 · Digital Logic
## Lab 7: Latches, Flip-Flops, and the Forbidden State
### Week 7 Lab Session

---

**Duration:** 2 hours (Friday 14:00–15:50, MEC 110)
**Format:** Pairs. **Both partners submit their own report.**
**Graded on:** completion + correctness — **100 points**
**Parts:** 74HC02 (quad NOR), 74HC00 (quad NAND), 74HC74 (dual D flip-flop), 74HC04, LEDs, DIP switches, **debounced pushbutton**, 330 Ω resistors
**Also:** Icarus Verilog

---

## Overview

**The first lab with memory in it.**

You will build a latch from two gates, watch it hold a bit, then deliberately drive it into its forbidden state and **observe that leaving that state does not give a repeatable answer.** Then you will fix it, twice.

> **A warning about the race in Part A4.** Real gates are not perfectly matched, so one of them will
> usually win *consistently* on any given chip. **You will probably see the same result every time
> and conclude the race is a myth.** Part A5 is designed to change your mind — swap chips with
> another pair.

---

## Part A — The SR Latch (30 pts)

**A1 (8 pts).** Build a cross-coupled NOR SR latch from a 74HC02. $S$ and $R$ on switches, $Q$ and $\overline Q$ on LEDs.

**A2 (7 pts).** Record the behaviour for $SR = 00, 01, 10$. **Demonstrate hold: set the latch, return $S$ to 0, and confirm $Q$ stays.**

**A3 (5 pts).** Now set $S=R=1$. **Record both $Q$ and $\overline Q$.**

**What is wrong with what you see?** Answer in terms of the output names.

**A4 (5 pts).** From $S=R=1$, drop both inputs to 0 **as close to simultaneously as you can manage** (both switches, one motion). **Record the resulting $Q$.** Repeat **ten times** and tabulate.

**A5 (5 pts).** **Swap your 74HC02 with another pair's and repeat A4 ten more times.**

**Report both tables.** Did the outcome change between chips? **What does that tell you about what decides the result?**

---

## Part B — The Gated D Latch (25 pts)

**B1 (10 pts).** Build a gated D latch: $S=D\cdot EN$, $R=\overline D\cdot EN$, feeding your SR latch.

**B2 (8 pts).** **Demonstrate that the forbidden state is now unreachable.** Try every combination of $D$ and $EN$ and record $S$ and $R$ at each. **Explain why $S=R=1$ cannot occur.**

**B3 (7 pts).** **Demonstrate transparency.** With $EN=1$, toggle $D$ several times and watch $Q$. Then set $EN=0$ and toggle $D$ again.

**Describe what you see in one sentence, and say why this is a problem in a circuit where $Q$ eventually feeds back to $D$.**

---

## Part C — The Flip-Flop (25 pts)

**C1 (10 pts).** Wire a 74HC74 D flip-flop with $D$ on a switch and the clock on a **debounced pushbutton**.

**Set $D$, press the button, and confirm $Q$ changes only on the press.** Then change $D$ *without* pressing, and confirm $Q$ does **not** move.

**C2 (8 pts).** **Contrast with B3 explicitly.** Give the one-sentence difference between your latch and your flip-flop.

**C3 (7 pts).** Wire $\overline Q$ back to $D$. **Press the button repeatedly and record $Q$.**

**What have you built?** *(You will build four of these next week.)*

---

## Part D — Simulation (20 pts)

**D1 (10 pts).** Write a **structural** master–slave D flip-flop in Verilog — two gated D latches from NAND primitives, on opposite clock phases.

**D2 (10 pts).** Testbench it over at least 10 clock edges, **changing $D$ while the clock is high** each cycle.

**Report the failure count**, and confirm two things: that $Q$ takes $D$'s value at the rising edge, and that **$Q$ does not move between edges.**

---

## Marking Summary

| Part | Points |
|---|---|
| A — the SR latch | 30 |
| B — the gated D latch | 25 |
| C — the flip-flop | 25 |
| D — simulation | 20 |
| **Total** | **100** |

---

*ECE 110 · Week 7 · Lab 7*
