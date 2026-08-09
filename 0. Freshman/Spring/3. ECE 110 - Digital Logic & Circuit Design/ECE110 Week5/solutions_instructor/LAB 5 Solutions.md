# ECE 110 · Digital Logic
## Lab 5 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All implementations verified exhaustively in Python and Icarus Verilog.

---

## Part A — The Decoder (25 pts)

### A1 (8)

**74HC138 outputs are ACTIVE LOW.** The selected output goes **low**; the other seven stay high. **All eight are high when disabled.**

*Marking: 8. **Award full marks for recording the active-low behaviour**, even if the student expected active-high — the instruction was to record what they saw.*

### A2 (9)

$$F = \sum m(1,3,5,6,7)$$

**With active-low outputs, an OR is wrong.** De Morgan:

$$F = m_1+m_3+m_5+m_6+m_7 = \overline{\overline{m_1}\cdot\overline{m_3}\cdot\overline{m_5}\cdot\overline{m_6}\cdot\overline{m_7}}$$

**The decoder gives $\overline{m_i}$ directly, so the correct gate is a 5-input NAND.** *(Verified.)*

*Marking: 5 working circuit, **4 for the De Morgan justification.** A student who uses a NAND because "it worked" earns 5.*

### A3 (8)

| implementation | gates |
|---|---:|
| decoder + NAND | 8 ANDs + 3 inverters + 1 NAND = **12** |
| minimal $C+AB$ | **2** |

$$\textbf{6× more silicon for the decoder version.}$$

---

## Part B — The Multiplexer (30 pts)

### B1 (10) — 8:1, all three variables selecting

**Data inputs are the truth-table column:**

$$D_0\ldots D_7 = 0,\ 1,\ 0,\ 1,\ 0,\ 1,\ 1,\ 1$$

*(Verified.)* **No derivation needed — it is the truth table.**

### B2 (12) — 4:1, $A,B$ selecting, $C$ on data

| sel $AB$ | $F(C{=}0)$ | $F(C{=}1)$ | data |
|:-:|:-:|:-:|:-:|
| 00 | 0 | 1 | $C$ |
| 01 | 0 | 1 | $C$ |
| 10 | 0 | 1 | $C$ |
| 11 | 1 | 1 | $\mathbf 1$ |

*(Verified.)*

*Marking: 6 circuit, **6 for the derivation table.** The derivation must be shown — it is the method being assessed.*

### B3 (8)

$$F=\sum m(1,2,4,7): \quad C,\ \overline C,\ \overline C,\ C$$

$$\textbf{The function is parity: } A\oplus B\oplus C.$$

*(Verified.)*

---

## Part C — The Comparison (20 pts)

### C1 (10)

| method | design effort | gates / packages |
|---|---|---|
| minimised gates | **highest** — draw map, group, check maximal | **2 gates**, 2 packages |
| decoder + NAND | low — read the minterm list | 12 gates, 2 packages |
| 8:1 mux | **lowest** — copy the truth table | 1 package |
| 4:1 mux | low — one derivation table | 1 package + inverter |

*Marking: 10, and **accept any honest effort ranking.** The gate column must be right.*

### C2 (5)

**No minimisation needed: the 8:1 mux** *(and the decoder version)*.
**Fewest gates: the minimised implementation.**

**They are opposite ends of the same trade.**

### C3 (5) — the design changes to $\sum m(0,3,5,6,7)$

| method | what you must do |
|---|---|
| minimised gates | **redo the map and rebuild** — the answer becomes $AB+AC+BC+\overline A\,\overline B\,\overline C$ |
| decoder + NAND | **move two wires** on the NAND input |
| 8:1 mux | **change two constants** — $D_0$ to 1, $D_1$ to 0 |
| 4:1 mux | redo the small derivation table |

$$\textbf{Cheapest to change: the mux.}$$

> **The minimised version does not merely need rework — it gets far worse.** $C+AB$ is 3 literals;
> $AB+AC+BC+\overline A\,\overline B\,\overline C$ is **11**. *(Verified.)* **One minterm moved and the
> gate implementation nearly quadrupled, while the LUT stayed exactly 8 bits.**

*Marking: 5. **The mark is for noticing that the minimised design degrades**, not merely that it needs redoing.*

---

## Part D — Verilog and the Lookup Table (25 pts)

### D1 (10)

**All four implementations agree on all 8 inputs: 0 failures.** *(Verified.)*

### D2 (8)

```verilog
module lut3(output y, input [7:0] table_bits, input a, b, c);
  assign y = table_bits[{a,b,c}];
endmodule
```

**`table_bits = 8'b11101010` computes $\sum m(1,3,5,6,7)$** *(bit $i$ is the value at minterm $i$, so index 7 is the MSB)*.
**`table_bits = 8'b11101001` computes $\sum m(0,3,5,6,7)$.**

**The module is unchanged.** *(Verified.)*

*Marking: 5 module, **3 for demonstrating two different functions from one module.***

### D3 (7)

**Because a LUT's cost is fixed by its input count, not by the function inside it.**

Minimisation exists to reduce gate count; **an FPGA does not buy gates, it buys tables**, and an 8-bit table holds a 2-gate function and an 11-literal function equally well. **The synthesis tool's job is therefore to *pack* logic into as few LUTs as possible and to route them — a different optimisation problem entirely.**

*Marking: 7. **Full marks require "the cost does not depend on the function".***

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 30 |
| C | 20 |
| D | 25 |
| **Total** | **100** |

---

## Checkoff Checklist

1. **A1 records active-low outputs**
2. **A2 justifies the NAND by De Morgan**
3. B1's data inputs are the truth-table column
4. **B2 shows the derivation table**
5. B3 names the function as parity
6. **C3 notices the minimised form gets worse, not just different**
7. D2 gets two functions from one unchanged module
8. D3 says the LUT cost is function-independent

---

## Note for the Debrief

**Open on C3, because it is the moment the week lands.**

> **You changed one minterm.** The mux implementation needed two constants changed. **The minimised
> gate implementation went from 3 literals to 11** — it did not just need redoing, **it got four
> times worse**, and you could not have predicted that from the change.

Then name what they built:

> **The module in D2 is a 3-input lookup table, and it is the basic cell of every FPGA on the
> market** — usually 4 to 6 inputs, built as a mux tree with memory cells on the data inputs.
> **You program it by writing those bits.**
>
> **This is why an FPGA toolchain never runs Week 4's algorithm.** Minimisation reduces gates;
> an FPGA does not buy gates.

Then close honestly:

> **None of that makes Week 4 wrong.** When you are making ten million of something, gates are what
> you pay for and two beats twelve every time. **When you are making one, or when it will change next
> week, the table wins.**
>
> **"Best" depends on what is scarce, and you now have numbers for both.**

---

*ECE 110 · Week 5 · Lab 5 Solutions · Instructor Only*
