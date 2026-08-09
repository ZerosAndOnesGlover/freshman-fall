# ECE 110 · Digital Logic
## Lab 12: Mapping a Design onto Programmable Logic
### Week 12 Lab Session

---

**Duration:** 2 hours (Friday 14:00–15:50, MEC 110)
**Format:** Pairs. **Both partners submit their own report.**
**Graded on:** completion + correctness — **100 points**
**Tools:** Python, Icarus Verilog
**Note:** the final exam is this week — **this lab is shorter than usual by design.**

---

## Overview

**The last lab. You will map circuits you already built onto programmable fabrics and count what they cost** — closing the course on the question it has asked every week: *which cost am I paying?*

---

## Part A — Sizing the Two-Level Family (30 pts)

**A1 (12 pts).** Write a function computing the fuse/bit count for a **PLA**, a **PAL** and a **ROM**, given $n$ inputs, $m$ outputs and $p$ product terms.

**Tabulate for $(n,m,p)$ = (4,4,8), (8,8,16), (10,8,32), (16,8,64).**

**A2 (8 pts).** **At which of those sizes does the ROM stop being competitive?** Give the ratio at $n=16$.

**A3 (10 pts).** Take the mod-10 counter's detect logic and the Week 9 FSM's next-state logic. **Count the product terms each needs, minimised and unminimised**, and say how many PAL product-term slots each would consume.

**Does minimisation change whether it fits?**

---

## Part B — LUT Mapping (35 pts)

**B1 (10 pts).** Write a function that, given a truth table, returns the LUT contents for a $k$-input LUT.

**Verify it on $F=\sum m(1,3,5,6,7)$ and on $F'=\sum m(0,3,5,6,7)$.**

**B2 (10 pts).** **Report the LUT contents and the LUT count for each.** They minimise to 3 and 11 literals respectively.

**What do you conclude?**

**B3 (15 pts).** Map your **Week 6 ALU** onto 6-input LUTs, by hand or by script:

- how many LUTs for the **bitwise** operations?
- how many for the **adder**, at roughly 2 LUTs per full adder?
- how many for the **output mux**?

**Give a total, and compare with the gate count you computed in Week 6.**

---

## Part C — The Flow and the Constraint (20 pts)

**C1 (8 pts).** List the six steps from HDL to bitstream, saying what each produces.

**C2 (6 pts).** **Which steps are NP-hard**, and which earlier week made the same point about a different algorithm?

**C3 (6 pts).** **Routing, not logic capacity, is usually what makes a design fail to fit.** Explain why that is plausible, given what an FPGA physically is.

---

## Part D — Closing the Loop (15 pts)

**D1 (15 pts).** Choose **three** design decisions from the whole course. For each, state:

- **which cost you spent**
- **which cost you bought**
- **the numbers you measured**

**One must be from Weeks 0–5 and one from Weeks 7–11.**

> **This is the last thing you will write for this course.** Make it specific — numbers you measured
> yourselves, not numbers from the lecture slides.

---

## Marking Summary

| Part | Points |
|---|---|
| A — sizing the two-level family | 30 |
| B — LUT mapping | 35 |
| C — the flow and the constraint | 20 |
| D — closing the loop | 15 |
| **Total** | **100** |

---

**Good luck on the final.** *The revision guide is in this week's `resources/`, and the retrospective is for afterwards.*

---

*ECE 110 · Week 12 · Lab 12 — the last one*
