# ECE 110 · Digital Logic
## Lab 12 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All arithmetic verified. **The last lab.**

---

## Part A — Sizing the Two-Level Family (30 pts)

### A1 (12)

$$\text{PLA}=2np+pm \qquad \text{PAL}=2np \qquad \text{ROM}=2^n m$$

| $n,m,p$ | PLA | PAL | ROM |
|---|---:|---:|---:|
| 4, 4, 8 | 96 | 64 | 64 |
| 8, 8, 16 | 384 | 256 | 2 048 |
| 10, 8, 32 | 896 | 640 | 8 192 |
| 16, 8, 64 | 2 560 | 2 048 | **524 288** |

*(Verified.)*

### A2 (8)

**The ROM is competitive at $n=4$ (equal to the PAL) and loses decisively from $n=8$.**

$$\text{At } n=16: \quad 524288/2048 = \mathbf{256\times}$$

### A3 (10)

**Mod-10 detect:** minimised $Q_3Q_1$ — **one product term.** Unminimised (full decode of `1010`) — **still one term**, but of four literals rather than two.

**Week 9 FSM next-state:** $D_1=Q_0\overline X+Q_1\overline{Q_0}X$ — **two product terms**; $D_0=X$ — **one**.

**Does minimisation change whether it fits?** **For these small examples, no** — everything fits comfortably in a typical 8-product-term PAL macrocell.

> **The honest answer here is "not for this design", and students should say so rather than
> manufacture a dramatic result.** The point is that **it *would* matter for a wider function**: an
> unminimised 4-variable function can need up to 16 product terms, which does not fit.

*Marking: 6 counts, **4 for an honest verdict.** A student who claims a dramatic fit/no-fit difference for these examples has not counted.*

---

## Part B — LUT Mapping (35 pts)

### B1 (10), B2 (10)

| function | LUT contents ($D_0\ldots D_7$) | LUTs |
|---|---|---|
| $\sum m(1,3,5,6,7)$ | `0,1,0,1,0,1,1,1` | **1** |
| $\sum m(0,3,5,6,7)$ | `1,0,0,1,0,1,1,1` | **1** |

*(Verified.)*

**Conclusion: minimisation is irrelevant to LUT cost.** One is 3 literals and the other 11; **both are one 3-LUT.**

### B3 (15)

**A 4-bit ALU on 6-input LUTs:**

| part | LUTs |
|---|---:|
| bitwise AND/OR/XOR/NOT | 4 bits × 1 LUT = **4** *(each output bit is a function of $a_i$, $b_i$, op)* |
| adder | ~2 LUTs per full adder × 4 = **8** |
| output mux (8:1 per bit) | ~2 LUTs per bit × 4 = **8** |
| **total** | **≈ 20 LUTs** |

**Against Week 6's gate count of roughly 25–30 gates for the same 4-bit ALU.**

> **The comparison is not apples to apples and students should say so** — a LUT is not a gate, and 20
> LUTs is far more silicon than 25 gates. **What it buys is that the design is loadable in seconds.**

*Marking: 9 for the three counts, **6 for noting that LUTs and gates are not comparable units.***

---

## Part C — The Flow and the Constraint (20 pts)

### C1 (8)

HDL → **synthesis** (gate netlist) → **mapping** (LUTs and flip-flops) → **placement** (which cell) → **routing** (the interconnect) → **bitstream**.

### C2 (6)

**Steps 2–5 are NP-hard in general.** **Week 4 said the same of Quine–McCluskey's covering step**, which is why real synthesis does not guarantee a true minimum.

### C3 (6)

**Because an FPGA's interconnect is a fixed, finite resource laid down at manufacture.**

**Logic capacity scales with the number of cells, but the wires between them do not scale as freely** — a design can need more connections through a region than there are wires crossing it, and no amount of spare LUTs elsewhere helps. **Congestion is local; capacity is global.**

*Marking: 6. **Full marks require the point that the interconnect is fixed and finite.***

---

## Part D — Closing the Loop (15 pts)

**No single right answer.** Full marks require, for each of three decisions: **the cost spent, the cost bought, and numbers the student measured themselves.**

**Reference set** *(all measured in this course)*:

| decision | spent | bought |
|---|---|---|
| carry-lookahead | ~2× area | 129 → 12 gate delays |
| synchronous counter | toggle logic | no transients; $32t_{cq}$ → 5 levels |
| DRAM | 4.5% refresh overhead | 6× density |
| minimisation | design effort | 43 gates → 7 |
| LUT over gates | silicon | 2 constants changed instead of a rebuild |
| BCD | 37% of the code space | exact decimal fractions |

*Marking: 5 per decision. **A trade with no numbers earns 2. Numbers copied from lecture slides rather than the student's own labs earn 3.***

---

## Marking Summary

| Part | Points |
|---|---|
| A | 30 |
| B | 35 |
| C | 20 |
| D | 15 |
| **Total** | **100** |

---

## Checkoff Checklist

1. A1's table correct, **A2 gives 256×**
2. **A3 gives an honest "does not matter here"**
3. B2 concludes minimisation is irrelevant to LUT cost
4. **B3 notes LUTs and gates are not comparable**
5. C3 says the interconnect is fixed and finite
6. **D uses the student's own measured numbers**

---

## Note for the Debrief — the last one

**Keep it short. Two things.**

> **Part B is the third time this course has told you the same thing, and the last.** A lookup table's
> cost is set by its input count, never by the function inside it. **You met it as a multiplexer in
> Week 5, as a ROM in Week 11, and as an FPGA cell today** — one object, three disguises.

Then close the course:

> **Look at your Part D table. Every row is a number you measured yourselves.**
>
> **The ripple adder worked and was unusable. The ripple counter worked and glitched a decoder. The
> latch worked and raced. The Verilog simulated and described a different circuit.** Four times this
> term, "it works" turned out to be the beginning of the argument rather than the end.
>
> **That is the course.** The gate counts will fade; that will not.

Then point forward:

> **CS 201 opens with a datapath. The ALU is Week 6, the register file is Week 8, the control unit is
> Week 9, and the cache exists because of Week 11's fifty-to-one gap.**
>
> **You will recognise all of it. Good luck on the final.**

---

*ECE 110 · Week 12 · Lab 12 Solutions · Instructor Only*
