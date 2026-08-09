# ECE 110 · Digital Logic
## Problem Set 5
### Topic: Decoders, Encoders, Multiplexers, Demultiplexers
**Released:** Thursday, Week 5 · **Due:** Thursday, Week 6 at the start of class

---

> **Give the gate count for every design**, under a stated convention.
>
> **When a block can be built from another block, say which and how** — that observation is usually
> where the marks are.

---

## Part A — Decoders and Encoders (5 pts each)

**A1.** Give the truth table and the four output equations of a 2:4 decoder with an active-high enable.

**A2.** How many AND gates and inverters does an $n$:$2^n$ decoder need? Tabulate for $n=2,3,4$. **What does that growth imply about large decoders?**

**A3.** Build a **3:8 decoder from two 2:4 decoders** and one inverter. Show the wiring and explain what the enables do.

**A4.** Give the equations of a 4:2 encoder. **Then give the two situations in which it produces a wrong or ambiguous answer.**

---

## Part B — Priority Encoders (6 pts each)

**B1.** Write the full truth table of a 4:2 **priority** encoder with a *valid* output, using don't-cares for the lower inputs.

**B2.** Derive $A_1$, $A_0$ and *valid* from your table.

**B3.** **Why is the valid output necessary?** Give the specific pair of situations it distinguishes.

**B4.** Name a real system that needs a priority encoder, and say what the priority means there.

**B5.** Compare the valid output to Week 3's overflow flag $V$. **What do the two have in common as a design idea?**

---

## Part C — Multiplexers (6 pts each)

**C1.** Give the output equation of a 4:1 mux. **Identify the decoder inside it.**

**C2.** Build an **8:1 mux from three 4:1 muxes**, or from 2:1 muxes — state which and draw it.

**C3.** Show that a **demultiplexer is a decoder** with its enable used as the data input. **Why does that work?**

**C4.** Implement $F = \sum m(1,2,4,7)$ on a **4:1 mux** with $A,B$ on the selects. Give the four data inputs.
**Then say what this function is, in one word.**

**C5.** Implement $F = \sum m(0,1,5,7,8,10,14,15)$ on an **8:1 mux** with $A,B,C$ on the selects. Give all eight data inputs.

---

## Part D — Why This Matters (5 pts each)

**D1.** State Shannon's expansion theorem.

**D2.** A $2^{k-1}$:1 mux implements **any** $k$-variable function. **Explain why**, using D1.

**D3.** Implementing $F=\sum m(1,3,5,6,7)$ with a 3:8 decoder plus an OR costs how many gates? It minimises to two gates. **When is the decoder version nevertheless the right choice?**

**D4.** **A lookup table costs the same regardless of the function stored in it.** What does that imply about minimisation on an FPGA?

**D5.** A 32:1 mux built flat needs a 32-input OR; built as a tree of 2:1 muxes it is 5 levels deep. **Relate this to Week 3's ripple-carry adder.**

---

## Marking Summary

| Part | Problems | Points |
|---|---|---|
| A — Decoders and encoders | 4 × 5 | 20 |
| B — Priority encoders | 5 × 6 | 30 |
| C — Multiplexers | 5 × 6 | 30 |
| D — Why this matters | 4 × 5 | 20 |
| **Total** | | **100** |

---

*ECE 110 · Problem Set 5 · due Thursday of Week 6*
