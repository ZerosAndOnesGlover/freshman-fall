# ECE 110 · Digital Logic
## Week 6 · Overview
### Arithmetic Logic Units — and the MIDTERM

---

**Topic:** the part that computes
**Reading:** Harris & Harris §5.2.4 | Mano & Ciletti §4.12
**Assessment this week:** PS 6 (released Thu 4 Mar 14:30, due Thu 11 Mar 13:00), Lab 6 (**Fri 5 Mar**, 14:00), **Quiz 5** *(Wed 3 Mar, 13:00 — covers Week 5, ungraded)*, and the **MIDTERM EXAM** *(Thu 4 Mar, 18:00–19:15)*

---

## ⚠ The Midterm

**Thursday 4 March 2027, 18:00–19:15 (VNC 100). 75 minutes. Covers Weeks 0–5. One handwritten sheet, one side. No calculator. 25% of the course.**

**A full revision guide is in this week's `resources/` folder** — topic checklist, the errors that have recurred, a sheet plan, and a sample paper with answers.

**Week 6's own material is not on it.**

---

## Everything So Far, Assembled

**Six weeks of parts. This week they become a component with a name a computer architect would recognise.**

| from | you get |
|---|---|
| Week 0 | two's complement, and why subtraction is addition |
| Week 1 | the algebra, and XOR as a controlled inverter |
| Week 2 | gates, and that structure decides delay |
| Week 3 | the adder, and the flags |
| Week 4 | minimisation |
| Week 5 | **the multiplexer that selects the operation** |

**An ALU is an adder, a few bitwise gates, and a mux.** That is genuinely all it is.

---

## The Two Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Wednesday | Building an ALU | Assembly, not invention |
| **Lecture 2** | Thursday | Carry-Lookahead and the Cost of Speed | Buying speed with area |

---

## The ALU

**Eight operations, selected by a 3-bit opcode:**

| op | operation | how |
|:-:|---|---|
| 000 | $A+B$ | the adder |
| 001 | $A-B$ | **the same adder**, `SUB`=1 |
| 010 | $A \text{ AND } B$ | 4 AND gates |
| 011 | $A \text{ OR } B$ | 4 OR gates |
| 100 | $A \oplus B$ | 4 XOR gates |
| 101 | $\overline A$ | 4 inverters |
| 110 | $A \ll 1$ | **wiring only** |
| 111 | $A<B$ | from the subtractor's flags |

**Plus four status outputs: $C$, $V$, $Z$ (zero), and $N$ (negative).**

*(Verified: all 8 operations across all 256 operand pairs — **2048 cases, zero failures** — in Python and independently in Verilog. The overflow flag checked against true signed arithmetic on all 256 signed pairs.)*

> **Two things worth noticing.** The shift costs **nothing but wiring** — no gates at all. And the
> comparison $A<B$ is **free**, read off the subtractor you already built. **A large part of
> engineering is noticing what you already have.**

---

## The Adder Problem, Finally Solved

**Week 3 measured the ripple-carry adder at $2N+1$ gate delays** — 129 at 64 bits, or 7.7 periods of a 3 GHz clock. **Unusable.**

**Carry-lookahead computes every carry directly from $G_i=A_iB_i$ and $P_i=A_i\oplus B_i$**, in blocks, arranged as a tree.

**Measured, on the same gate-delay model:**

| $N$ | ripple | **CLA** | speedup |
|---:|---:|---:|---:|
| 4 | 9 | **4** | 2.2× |
| 8 | 17 | **7** | 2.4× |
| 16 | 33 | **8** | 4.1× |
| 32 | 65 | **11** | 5.9× |
| **64** | **129** | **12** | **10.8×** |

*(All measured on a built and exhaustively-checked hierarchical CLA.)*

### And the verdict

| 64-bit adder | delay | vs 0.33 ns clock |
|---|---:|---|
| ripple-carry | 2.58 ns | **7.7 periods — does not fit** |
| **carry-lookahead** | **0.24 ns** | **0.72 periods — fits** |

**The cost is area: roughly $2\times$ the gates.**

> **This is the trade Week 2 named and Week 3 made urgent, now priced.** You are buying a **10×**
> reduction in delay for **2×** the silicon, and it is the difference between a design that works and
> one that does not exist.

---

## This Week's Work

1. **Quiz 5** — Wed 3 Mar, covers Week 5. **Ungraded.**
2. **Lab 6** — build a 4-bit ALU and test all 2048 cases.
3. **PS 6** — ALU design, flags, carry-lookahead.
4. **THE MIDTERM.** See [[MIDTERM Revision Guide]].

---

*Next: Wednesday — Building an ALU*
