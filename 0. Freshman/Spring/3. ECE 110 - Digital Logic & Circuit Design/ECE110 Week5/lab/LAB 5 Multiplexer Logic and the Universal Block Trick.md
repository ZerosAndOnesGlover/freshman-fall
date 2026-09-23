# ECE 110 · Digital Logic
## Lab 5: Multiplexer Logic and the Universal-Block Trick
### Week 5 Lab Session

**Date:** Friday 26 February 2027 · 14:00–15:50 · Lab section (Week 5) — after both of Week 5's lectures

---

**Duration:** 2 hours (MEC 110)
**Format:** Pairs. **Both partners submit their own report.**
**Graded on:** completion + correctness — **100 points**
**Parts:** 74HC138 (3:8 decoder), 74HC151 (8:1 mux), 74HC153 (dual 4:1 mux), 74HC04, 74HC32, breadboard
**Also:** Python 3

---

## Overview

**Three ways to build the same function, and a measurement of what each costs.**

You will implement one function with gates (Week 4's method), with a decoder plus an OR, and with a multiplexer — then compare **design effort** and **gate count**, which point in opposite directions.

> **The lab's point: "best" depends on what is scarce.** When silicon is scarce you minimise. When
> *your time* is scarce, or the design will change, you use a universal block. **Both are correct
> engineering and the course has now shown you the numbers for each.**

---

## Part A — The Decoder (25 pts)

**A1 (8 pts).** Wire a 74HC138 and record its truth table, including the enable.

**Note the 74HC138's outputs are active LOW.** Record what you actually see, not what you expected.

**A2 (9 pts).** Implement $F = \sum m(1,3,5,6,7)$ using the decoder plus one OR gate.

**Verify all 8 rows on the bench.**

> With active-low outputs you will need a **NAND** rather than an OR. **Work out why before you
> wire it** — this is De Morgan from Week 1, and getting it wrong is the most common failure in
> this lab.

**A3 (8 pts).** Count the gates your decoder implementation uses, and compare with the minimal gate implementation of the same function ($C+AB$, two gates).

---

## Part B — The Multiplexer (30 pts)

**B1 (10 pts).** Wire a 74HC151 (8:1) with $A,B,C$ on the selects and constants on the data inputs, so that it implements $F = \sum m(1,3,5,6,7)$ **directly from the truth table**.

**Record all 8 rows.**

**B2 (12 pts).** Now implement the same $F$ on a **4:1** mux (74HC153) with $A,B$ selecting and $C$ on the data inputs.

**Derive the four data inputs first**, by asking what $F$ does as $C$ varies with $A,B$ fixed. **Show that derivation in your report.**

**B3 (8 pts).** Implement $F = \sum m(1,2,4,7)$ on the 4:1 mux. **Give the four data inputs, and name the function.**

---

## Part C — The Comparison (20 pts)

**C1 (10 pts).** Tabulate, for $F = \sum m(1,3,5,6,7)$:

| method | design effort | gates / packages |
|---|---|---|
| minimised gates | | |
| decoder + OR | | |
| 8:1 mux | | |
| 4:1 mux | | |

**Score design effort honestly** — how long did each take you, start to working circuit?

**C2 (5 pts).** **Which method needed no minimisation at all?** Which needed the fewest gates?

**C3 (5 pts).** **Your design changes: $F$ becomes $\sum m(0,3,5,6,7)$.** For each of the four methods, say what you would physically have to do. **Which method is cheapest to change?**

---

## Part D — Simulation and the Lookup Table (25 pts)

**D1 (10 pts).** Write all four implementations as Python functions (gate by gate, as in Lab 2) and prove
by checking all 8 inputs that they agree. **Report the failure count.**

**D2 (8 pts).** Write `lut3(table_bits, a, b, c)`, where `table_bits` is an 8-bit integer, returning bit
number `4*a + 2*b + c` of it: `(table_bits >> (4*a + 2*b + c)) & 1`.

**Show that setting `table_bits` to the right constant makes it compute $F$** — and that a different constant makes it compute something else, **with no change to the function.**

**D3 (7 pts).** **You have just built the basic cell of an FPGA.** In two or three sentences, explain why an FPGA toolchain does not need Week 4's minimisation.

---

## Marking Summary

| Part | Points |
|---|---|
| A — the decoder | 25 |
| B — the multiplexer | 30 |
| C — the comparison | 20 |
| D — simulation and the lookup table | 25 |
| **Total** | **100** |

---

*ECE 110 · Week 5 · Lab 5*
