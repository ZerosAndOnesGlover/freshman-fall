# ECE 110 · Digital Logic
## Week 6 · Lecture 1 (Wednesday)
### Building an ALU

**Date:** Wednesday 3 March 2027 · 13:00–14:15 · Week 6

---

**Reading:** Harris & Harris §5.2.4 | Mano & Ciletti §4.12
**Quiz 5** — at the start of today's lecture. **Covers Week 5.** Ungraded.
**The MIDTERM is Thursday 4 March, 18:00.** Revision guide in `resources/`.

---

## 1. What An ALU Is

> **An arithmetic logic unit takes two operands and an opcode, and produces a result plus status
> flags.**

**It is the part of a processor that computes.** Everything else — registers, memory, control — exists to feed it and to store what it produces.

**And it is assembly, not invention.** You have built every piece.

---

## 2. The Structure

**Compute *all* the operations in parallel, then use a multiplexer to select one.**

```
        A ──┬─────────────┐
            │             │
   B ──┬────┼──[XOR]──[4-bit ADDER]──── sum, Cout
       │    │   ▲                          │
       │    │  SUB                         │
       │    ├──[AND]──────────────────┐    │
       │    ├──[OR ]──────────────────┤    │
       │    └──[XOR]──────────────────┤    │
       │       [NOT A]────────────────┤    │
       │       [A<<1] (wires only)────┤    │
       └───────────────────────────[ 8:1 MUX ]──── Y
                                        ▲
                                       op[2:0]
```

**Why compute everything and throw most of it away?** Because **selecting is fast and cheap** — one mux delay — while doing them in sequence would need control logic and multiple clock cycles. **Silicon is cheaper than time**, which is the same trade as Week 5's lookup table.

---

## 3. The Eight Operations

| op | operation | cost |
|:-:|---|---|
| 000 | $A+B$ | the adder |
| 001 | $A-B$ | **the same adder** |
| 010 | $A\text{ AND }B$ | 4 gates |
| 011 | $A\text{ OR }B$ | 4 gates |
| 100 | $A\oplus B$ | 4 gates |
| 101 | $\overline A$ | 4 gates |
| 110 | $A\ll1$ | **0 gates** |
| 111 | $A<B$ | **0 gates** |

*(Verified: all eight operations across all 256 operand pairs — 2048 cases, zero failures — in Python and independently in Verilog.)*

### The two free ones

**A left shift is a renaming of wires.** $Y_3 \leftarrow A_2$, $Y_2\leftarrow A_1$, $Y_1\leftarrow A_0$, $Y_0\leftarrow 0$. **No gates.** The bit shifted out becomes the carry.

**The comparison $A<B$ is read off the subtraction you already do.** For signed operands, $A<B$ exactly when the sign of $A-B$ disagrees with overflow — $N\oplus V$. **No new hardware.**

> **Noticing what you already have is a large part of engineering**, and both of these are free only
> because Weeks 0 and 3 built the right thing.

---

## 4. The Flags

| flag | meaning | how |
|:-:|---|---|
| **$C$** | carry out | the adder's $C_{out}$ |
| **$V$** | signed overflow | $C_{N-1}\oplus C_{out}$ *(Week 3)* |
| **$Z$** | result is zero | NOR of all result bits |
| **$N$** | result is negative | the result's MSB |

*(Verified: $V$ against true signed arithmetic on all 256 signed pairs; $Z$ across all 2048 cases.)*

**$Z$ is one wide NOR gate. $N$ is a wire.**

> **The flags are how a processor makes decisions.** `if (a == b)` compiles to a subtraction and a
> branch on $Z$; `if (a < b)` to a subtraction and a branch on $N\oplus V$. **The comparison
> instruction in every instruction set you will ever meet is this ALU, with its result discarded and
> only the flags kept.**

---

## 5. Bit-Slice Structure

**Build one bit's worth, then replicate it $N$ times.**

**Each slice: one full adder, one AND, one OR, one XOR, one inverter, one 8:1 mux — and the carry chain threading through.** A 32-bit ALU is 32 identical slices plus the opcode fanout.

> **This is why processor datapaths are drawn as one slice with "×32" beside it**, and why widening
> from 32 to 64 bits is an engineering exercise rather than a redesign.

**The only part that does not simply replicate is the carry chain** — and that is tomorrow's subject, because it is the part that decides the clock speed.

---

## 6. What To Take From This Lecture

1. **An ALU is an adder, some bitwise gates, and a mux.** Assembly, not invention.
2. **Compute all operations in parallel and select** — silicon is cheaper than time.
3. **Subtraction reuses the adder** (Week 3's XOR trick).
4. **Shift costs no gates. Comparison costs no gates.**
5. **Four flags: $C$, $V$, $Z$, $N$.** $Z$ is a NOR, $N$ is a wire.
6. **Every comparison instruction is this ALU with the result thrown away.**
7. **Bit-slice replication** — except the carry chain.

---

*Next: Thursday — Carry-Lookahead and the Cost of Speed*
