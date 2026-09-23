# ECE 110 · Digital Logic
## Week 5 · Overview
### Decoders, Encoders, Multiplexers, Demultiplexers

---

**Topic:** the reusable blocks
**Reading:** Harris & Harris §2.8, §5.2.4–5.2.6 | Mano & Ciletti §4.6–4.11
**Assessment this week:** PS 5 (released Thu 25 Feb 14:30, due Thu 4 Mar 13:00), Lab 5 (**Fri 26 Feb**, 14:00), **Quiz 4** *(Wed 24 Feb, 13:00 — covers Week 4, ungraded)*

---

## Stop Designing From Truth Tables

**Weeks 1–4 gave you a complete method: truth table → expression → minimise → gates.** It works, and it does not scale — a 16-input function has 65 536 rows and nobody draws that map.

**Real design is assembly.** A handful of blocks recur in every system, and you reach for those instead of starting from a truth table each time.

**This week is that handful.** Next week you assemble them into something that computes.

---

## The Two Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Wednesday | Decoders and Encoders | Turning a code into a line, and back |
| **Lecture 2** | Thursday | Multiplexers and Demultiplexers | Choosing — and a block that implements *anything* |

---

## The Four Blocks

| block | in → out | does |
|---|---|---|
| **Decoder** | $n$ → $2^n$ | asserts exactly **one** output, the one the input names |
| **Encoder** | $2^n$ → $n$ | reports **which** input is asserted |
| **Multiplexer** | $2^n$ data + $n$ select → 1 | **chooses** one input |
| **Demultiplexer** | 1 data + $n$ select → $2^n$ | **routes** it to one output |

**Decoder and encoder are inverses. Mux and demux are inverses.** And **a demultiplexer is a decoder with its enable used as the data input** — the same silicon, relabelled.

---

## Two Facts Worth The Week

### A decoder plus an OR gate implements any function

**A decoder's outputs *are* the minterms.** So the canonical SOP of Week 1 becomes: take the decoder outputs for the rows where $F=1$, OR them together.

$$F=\sum m(1,3,5,6,7) \;\Rightarrow\; \text{3:8 decoder} + \text{one 5-input OR}$$

*(Verified.)* **No minimisation, no algebra — read the minterm list, wire the OR.**

### A multiplexer implements any function, more cheaply

**Shannon's expansion:**

$$F = x\cdot F|_{x=1} + \overline x\cdot F|_{x=0}$$

**Put $k-1$ variables on the select lines and the last one on the data inputs**, and a $2^{k-1}\!:\!1$ mux computes **any** $k$-variable function.

**Worked: $F = AB+\overline AC+BC$ on a 4:1 mux with $A,B$ selecting:**

| select $AB$ | data input |
|:-:|:-:|
| 00 | $C$ |
| 01 | $C$ |
| 10 | $0$ |
| 11 | $1$ |

*(Verified on all 8 inputs.)* **One 4:1 mux and one inverter — no minimisation at all.**

> **This is the week's real idea.** A mux is not just a selector; it is a **programmable lookup
> table**, and its data inputs are the truth table. **Week 12's FPGA is built from exactly this**, and
> that is why an FPGA needs no minimisation to implement your design.

---

## The Encoder's Trap

**A plain $2^n\!:\!n$ encoder assumes exactly one input is high.** Give it two and it produces garbage; give it none and it outputs $000$ — **indistinguishable from "line 0 is active".**

**A priority encoder fixes both:** it reports the **highest** asserted line, and adds a **valid** output.

| input | plain encoder | priority encoder |
|---|---|---|
| `0110` | undefined | code $2$, valid $1$ |
| `0000` | $00$ *(looks like line 0)* | code $0$, **valid $0$** |

*(Verified.)*

> **The valid bit is the whole difference**, and it is the same kind of fix as Week 0's overflow
> flag: a status output that tells you whether to believe the data output.

---

## This Week's Work

1. **Quiz 4** — Wed 24 Feb, covers Week 4. **Ungraded.**
2. **Lab 5** — mux-based logic, and the universal-block trick.
3. **PS 5** — decoders, priority encoders, mux design, Shannon expansion.

---

*Next: Wednesday — Decoders and Encoders*
