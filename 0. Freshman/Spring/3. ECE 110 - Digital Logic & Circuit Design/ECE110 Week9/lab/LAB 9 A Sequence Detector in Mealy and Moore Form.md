# ECE 110 · Digital Logic
## Lab 9: A Sequence Detector in Mealy and Moore Form
### Week 9 Lab Session

---

**Duration:** 2 hours (Friday 14:00–15:50, MEC 110)
**Format:** Pairs. **Both partners submit their own report.**
**Graded on:** completion + correctness — **100 points**
**Parts:** 74HC74 ×2, 74HC08, 74HC32, 74HC04, LEDs, DIP switch, **debounced pushbutton**
**Also:** Icarus Verilog

---

## Overview

**One specification, two machines, and a measured comparison.**

You will build an overlapping `1011` detector as a Mealy machine on the bench, write both forms in Verilog, and verify each against a reference over thousands of cycles.

---

## Part A — Design On Paper (25 pts)

**A1 (8 pts).** Draw the **Mealy** state diagram. **Mark the overlap arc** and say in one sentence why it goes where it does.

**A2 (7 pts).** Write the state table, then assign $A{=}00$, $B{=}01$, $C{=}10$, $D{=}11$ and give the transition table over $(Q_1,Q_0,X)$.

**A3 (10 pts).** Derive $D_1$, $D_0$ and $Y$ by **K-map**. Show the maps.

**Check your answers against these before building — but derive them first:**

$$D_1 = Q_0\overline X + Q_1\overline{Q_0}X \qquad D_0 = X \qquad Y = Q_1Q_0X$$

---

## Part B — Build It (25 pts)

**B1 (15 pts).** Build the Mealy machine: two 74HC74 flip-flops on a **common** debounced clock, plus the next-state and output logic.

**Wire $X$ to a switch, $Q_1Q_0$ to two LEDs, $Y$ to a third.**

**B2 (6 pts).** Feed in `1011011011` one bit per press. **Record $Q_1Q_0$ and $Y$ at every step**, and compare with your paper trace.

**B3 (4 pts).** **Add a reset.** Tie the flip-flops' clear lines to a button and confirm the machine returns to $A$.

**Why is this not optional?** One sentence.

---

## Part C — Both Machines in Verilog (30 pts)

**C1 (10 pts).** Write the **Mealy** machine in Verilog, using your equations.

**C2 (10 pts).** Write the **Moore** machine. **It needs five states** — say in a comment why.

**C3 (10 pts).** Write a testbench that drives **random input** for at least 2000 cycles and compares **both** machines against a reference that simply checks whether the last four bits were `1011`.

**Report cycles checked and failures for each machine.**

> ⚠ **Pulse your reset.** `reg rst = 1;` with `always @(posedge clk or posedge rst)` **never fires** —
> there is no rising edge if the signal starts high. This cost us a debugging session while preparing
> the lab: the state stayed `xx` and the output was `x` for the first cycles. **Start at 0, drive to
> 1, drive back to 0.**

---

## Part D — Compare (20 pts)

**D1 (6 pts).** Tabulate: **states, flip-flops, and next-state logic literals** for both machines.

**D2 (7 pts).** Run both on `1011011011`. **Do the outputs agree?**

**If they differ, say exactly where and why** — and state which output convention you used for Moore.

**D3 (7 pts).** **Which machine would you choose if $Y$ drove a memory write-enable?** Justify, referring to what you saw on the scope in Lab 8.

---

## Marking Summary

| Part | Points |
|---|---|
| A — design on paper | 25 |
| B — build it | 25 |
| C — both machines in Verilog | 30 |
| D — compare | 20 |
| **Total** | **100** |

---

*ECE 110 · Week 9 · Lab 9*
