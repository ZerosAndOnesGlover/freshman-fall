# ECE 110 · Digital Logic
## Week 6 · Reference Sheet
### The ALU and Carry-Lookahead

---

## ALU Structure

**Compute every operation in parallel; select with a mux.**

$$\text{operands} \to \{\text{adder},\ \text{AND},\ \text{OR},\ \text{XOR},\ \text{NOT},\ \text{shift}\} \to \text{mux(op)} \to Y$$

**Silicon is cheaper than time** — sequencing would need control logic and extra cycles.

| op | operation | cost |
|:-:|---|---|
| 000 | $A+B$ | the adder |
| 001 | $A-B$ | **the same adder**, `SUB`=1 |
| 010 | $A \text{ AND } B$ | 4 gates |
| 011 | $A \text{ OR } B$ | 4 gates |
| 100 | $A\oplus B$ | 4 gates |
| 101 | $\overline A$ | 4 gates |
| 110 | $A\ll1$ | **0 gates — wiring** |
| 111 | $A<B$ | **0 gates — from the flags** |

*(All 8 ops × 256 operand pairs = **2048 cases, zero failures**, in Python and independently in Verilog.)*

---

## The Flags

| flag | meaning | hardware |
|:-:|---|---|
| $C$ | unsigned overflow | adder's $C_{out}$ |
| $V$ | signed overflow | $C_{N-1}\oplus C_{out}$ |
| $Z$ | result is zero | **NOR of all result bits** |
| $N$ | result is negative | **the MSB — a wire** |

### Signed comparison is free

$$A<B \iff N\oplus V \quad\text{after computing } A-B$$

*(Verified on all 256 signed 4-bit pairs, zero mismatches.)*

**Example that shows why $V$ is needed:** $A=-6$, $B=5$. $A-B$ gives bits `0101` $=+5$ — **positive** — but $V=1$, so $N\oplus V = 0\oplus1 = 1$: **correctly $A<B$.**

> **Every comparison instruction in every instruction set is this ALU with the result discarded and
> only the flags kept.** `if (a==b)` is a subtraction and a branch on $Z$.

---

## Bit-Slice Structure

**One slice = 1 full adder + 4 logic gates + 1 mux.** Replicate $N$ times.

**Everything replicates except the carry chain** — and that is what decides the clock speed.

---

## Carry-Lookahead

$$G_i = A_iB_i \quad\text{\bf generate} \qquad P_i = A_i\oplus B_i \quad\text{\bf propagate} \qquad C_{i+1}=G_i+P_iC_i$$

**Expanded — every carry two levels deep, computed in parallel:**

$$C_1=G_0+P_0C_0$$
$$C_2=G_1+P_1G_0+P_1P_0C_0$$
$$C_3=G_2+P_2G_1+P_2P_1G_0+P_2P_1P_0C_0$$
$$C_4=G_3+P_3G_2+P_3P_2G_1+P_3P_2P_1G_0+P_3P_2P_1P_0C_0$$

*(Verified equal to the ripple carries on all 512 four-bit cases.)*

### Why not flat at 64 bits

**Fan-in.** $C_{64}$ would need a 65-input OR of terms up to 65 literals. **Week 2: wide gates are slow, libraries stop near 4 inputs.**

### Group signals, for the hierarchy

$$P_{\text{grp}}=P_3P_2P_1P_0 \qquad G_{\text{grp}}=G_3+P_3G_2+P_3P_2G_1+P_3P_2P_1G_0$$

**A second-level unit treats each block as one bit. A third level treats each group of blocks the same way.** A tree.

---

## Measured

| $N$ | ripple $2N{+}1$ | **CLA** | speedup |
|---:|---:|---:|---:|
| 4 | 9 | **4** | 2.2× |
| 8 | 17 | **7** | 2.4× |
| 16 | 33 | **8** | 4.1× |
| 32 | 65 | **11** | 5.9× |
| **64** | **129** | **12** | **10.8×** |

*(measured on a built and exhaustively-checked hierarchical CLA)*

### The verdict at 64 bits, 20 ps/gate, 3 GHz clock (0.33 ns)

| | delay | periods | |
|---|---:|---:|---|
| ripple | 2.58 ns | 7.75 | **does not fit** |
| **CLA** | **0.24 ns** | **0.72** | **fits** |

**Area cost: about $2\times$** — roughly 320 → 640 gates at 64 bits.

> **A 10× reduction in delay for 2× the silicon**, and it is the difference between a design that
> exists and one that does not.

---

## The Course's Two Costs, Finally Traded

| week | what happened |
|---|---|
| **2** | named them: **gate count = area, critical path = speed** |
| **3** | one failed: ripple adder cheap in area, unusable in time |
| **4** | reduced area (43 → 7 gates) and **did nothing for speed** |
| **6** | **spend area to buy speed, deliberately** |

**No substitution of gate types fixes a structural delay** — the chain is $N$ long whatever it is made of. **Only restructuring works.**

---

## Common Errors

1. **Building a second adder for subtraction** instead of reusing the first.
2. **Deriving $V$ by comparing against a wider result** rather than from the carries.
3. **Forgetting $Z$ is a NOR over *all* result bits.**
4. **Using $N$ alone for signed comparison** — it must be $N\oplus V$.
5. **Proposing a flat 64-bit lookahead** and ignoring fan-in.
6. **Expecting minimisation to fix a delay problem.**

---

*ECE 110 · Week 6 · Reference Sheet*
