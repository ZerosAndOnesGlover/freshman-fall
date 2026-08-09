# ECE 110 · Digital Logic
## Problem Set 6 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** ALU verified over all 2048 cases in Python and Verilog; CLA delays measured on a built hierarchical adder.

---

## Part A (5 pts each)

**A1 (5).** Operands into the adder (with the `SUB` XORs) and into four bitwise units in parallel; all results into an **8:1 mux** selected by `op[2:0]`; flags derived from the adder's carries and the mux output.

**A2 (5).** **Because selecting is one mux delay, while sequencing would need control logic, state, and multiple clock cycles.** The unused results cost area, which is cheap; computing them in sequence would cost time, which is not. **Same trade as Week 5's lookup table.**

**A3 (5).** **Left shift** — a renaming of wires ($Y_i \leftarrow A_{i-1}$, $Y_0\leftarrow0$), no gates. **Comparison $A<B$** — read from the subtraction's flags as $N\oplus V$, no new hardware.

**A4 (5).**

| flag | meaning | hardware |
|:-:|---|---|
| $C$ | unsigned overflow | adder $C_{out}$ |
| $V$ | signed overflow | $C_{N-1}\oplus C_{out}$ |
| $Z$ | result zero | NOR of all result bits |
| $N$ | result negative | MSB (a wire) |

---

## Part B (6 pts each)

**B1 (6).** One XOR per $B$ bit with `SUB` as the second input; **`SUB` also drives the least significant carry-in.** `SUB`=0 gives $B$ and $C_{in}=0$; `SUB`=1 gives $\overline B$ and $C_{in}=1$, i.e. $A+\overline B+1 = A-B$.

*Marking: 3 XORs, **3 for the carry-in.***

**B2 (6).** $Z = \overline{Y_3+Y_2+Y_1+Y_0}$ — a 4-input NOR. $N = Y_3$ — **a wire, no gate.**

**B3 (6).**

| | $A-B$ bits | value | $N$ | $V$ | $N\oplus V$ | true $A<B$ |
|---|---|---:|:-:|:-:|:-:|:-:|
| $A=3,B=5$ | `1110` | $-2$ | 1 | 0 | **1** | 1 ✓ |
| $A=-6,B=5$ | `0101` | $+5$ | 0 | **1** | **1** | 1 ✓ |

*(Verified — and $N\oplus V$ matches true signed comparison on all 256 pairs.)*

> **The second row is the point.** $A-B$ came out **positive** ($+5$) even though $A<B$, because
> $-6-5=-11$ overflows. **$N$ alone would have said "not less than" and been wrong.**

*Marking: 3 per case. **Full marks on the second require noting that $N$ alone fails.***

**B4 (6).** **Branch on $Z$.** The subtraction's *result* is irrelevant — only whether it was zero matters — so the ALU output is discarded and only the flag is kept. **That is what a compare instruction is.**

**B5 (6).** **The carry chain.** Every other part of a bit slice is independent and replicates trivially; the carry is a **serial dependency** running the width of the ALU. **It is the longest path, so it sets the minimum clock period** — and it is why widening from 32 to 64 bits is a timing problem rather than a copy-paste.

---

## Part C (6 pts each)

**C1 (6).** $G_i=A_iB_i$; $P_i=A_i\oplus B_i$; $C_{i+1}=G_i+P_iC_i$.

**C2 (6).**

$$C_1=G_0+P_0C_0 \qquad C_2=G_1+P_1G_0+P_1P_0C_0$$
$$C_3=G_2+P_2G_1+P_2P_1G_0+P_2P_1P_0C_0$$
$$C_4=G_3+P_3G_2+P_3P_2G_1+P_3P_2P_1G_0+P_3P_2P_1P_0C_0$$

*(Verified against the ripple carries on all 512 cases.)*

**Each is AND-OR — 2 gate delays — plus 1 to form $G$ and $P$. All four in parallel, independent of position.**

**C3 (6).** **Fan-in.** $C_{64}$ needs a 65-input OR of products up to 65 literals. **Wide gates stack transistors in series and are slow** *(Week 2)*; real libraries stop near 4 inputs. **The expression is correct and unbuildable.**

**C4 (6).** $P_{\text{grp}}=P_3P_2P_1P_0$ *(the block passes a carry only if every bit does)*; $G_{\text{grp}}=G_3+P_3G_2+P_3P_2G_1+P_3P_2P_1G_0$ *(the block makes a carry if any bit does and the ones above it pass)*.

**A second-level unit takes the blocks' $P_{\text{grp}}$/$G_{\text{grp}}$ and applies the same recurrence**, treating each 4-bit block as if it were a single bit.

**C5 (6).**

| | gate delays | at 20 ps | vs 0.33 ns |
|---|---:|---:|---|
| ripple, $N=64$ | 129 | **2.58 ns** | 7.75 periods — **no** |
| CLA, $N=64$ | 12 | **0.24 ns** | 0.72 periods — **yes** |

*(Measured.)*

---

## Part D (5 pts each)

**D1 (5).** **Spending area, buying speed.** About $2\times$ the gates for a $10.8\times$ reduction in delay.

**D2 (5).** **Because the dependency chain is $N$ stages long regardless of what the stages are made of** — a faster gate shortens each link but not the number of links.

**D3 (5).** **No.**

Minimisation reduces gate count and level count *within* a block, but the ripple adder's delay is $N$ **blocks** in series. **Even a zero-delay full adder leaves the structure**, and the full adder is already near-minimal. *(Week 4 turned 43 gates into 7 and changed the depth from 2 levels to 2 levels.)*

**D4 (5).**

| rank | technique | effect on delay |
|:-:|---|---|
| **1** | **carry-lookahead** | large — restructures, $129\to12$ |
| 2 | minimisation | small — may remove a level within a block |
| 3 | NAND-only conversion | **none** — level count is unchanged *(verified in Week 2)* |

**Justification: only carry-lookahead changes the *structure*.** The other two substitute or shrink within a structure that is already the problem.

---

## Marking Summary

| Part | Points |
|---|---|
| A | 20 |
| B | 30 |
| C | 30 |
| D | 20 |
| **Total** | **100** |

---

## The Five Errors To Expect

1. **B1:** the XORs without the carry-in.
2. **B3:** using $N$ alone and getting the $A=-6,B=5$ case wrong.
3. **C3:** answering "it would be too big" without naming fan-in.
4. **D3:** saying minimisation would help "a bit" — it does not address the structure at all.
5. **D4:** ranking NAND conversion above zero.

---

*ECE 110 · Week 6 · PS 6 Solutions · Instructor Only*
