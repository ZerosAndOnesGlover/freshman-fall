# ECE 110 · Digital Logic
## Week 5 · Lecture 2 (Thursday)
### Multiplexers and Demultiplexers

*“The computer reminds one of Lon Chaney -- it is the machine of a thousand faces.”* — Alan Perlis, "Epigrams on Programming" (1982), #91

**Date:** Thursday 25 February 2027 · 13:00–14:15 · Week 5

**Coursework:** 📝 **PS 4** due today 13:00 · 📝 **PS 5** released today 14:30, due Thu 4 Mar 13:00 · 🔬 **Lab 5** Fri 26 Feb 14:00–15:50 · 📊 **Quiz 5** Wed 3 Mar 13:00–13:10 · 📘 **Midterm** Thu 4 Mar 18:00–19:15

---

**Reading:** Harris & Harris §2.8.1, §5.2.5 | Mano & Ciletti §4.11
**PS 5** released today, due Thursday of Week 6.

---

## 1. The Multiplexer

> **A $2^n\!:\!1$ multiplexer has $2^n$ data inputs, $n$ select inputs, and one output: the data input
> the select lines name.**

**4:1 mux:**

$$Y = \overline{S_1}\,\overline{S_0}D_0 + \overline{S_1}S_0D_1 + S_1\overline{S_0}D_2 + S_1S_0D_3$$

*(Verified.)*

**Look at the structure: that is a decoder on the select lines, AND-ing each decoded line with its data input, then OR-ing.** A mux *is* a decoder with data gating.

**A mux is how one wire carries many sources** — a bus, a register file read port, an ALU output select.

---

## 2. The Demultiplexer

> **The inverse: one data input, $n$ select lines, $2^n$ outputs. The data goes to the selected
> output; the rest are 0.**

**And here is the economy: a demultiplexer is a decoder whose enable is used as the data input.**

**When `EN` is the data:** the selected AND gate passes `EN`, all others are 0 — **which is exactly demultiplexing.** *(Verified: with the enable low every output is low; with it high exactly the selected output is high.)*

**Same silicon. Different label.**

---

## 3. A Mux Implements Any Function

**Shannon's expansion theorem:**

$$\boxed{F(x, \ldots) = x\cdot F|_{x=1} + \overline x\cdot F|_{x=0}}$$

**Any function splits on any variable into two smaller functions.** Applied repeatedly, it turns a function into a tree of muxes.

### The direct version

**A $2^k\!:\!1$ mux with all $k$ variables on the selects:** wire each data input to the truth-table entry for that row — a constant 0 or 1.

**The data inputs *are* the truth table.**

### The efficient version

**Use $k-1$ variables as selects and let the last variable appear on the data inputs.** Each data input is then one of just four things: $0$, $1$, $x$, or $\overline x$.

**Worked: $F = AB + \overline AC + BC$, with $A,B$ selecting a 4:1 mux.**

**For each $(A,B)$, ask what $F$ does as $C$ varies:**

| $A$ | $B$ | $F(C{=}0)$ | $F(C{=}1)$ | data input |
|:-:|:-:|:-:|:-:|:-:|
| 0|0| 0 | 1 | $C$ |
| 0|1| 0 | 1 | $C$ |
| 1|0| 0 | 0 | $0$ |
| 1|1| 1 | 1 | $1$ |

$$\textbf{One 4:1 mux. No minimisation, no map, no algebra.}$$

*(Verified on all 8 inputs.)*

> **A $2^{k-1}\!:\!1$ mux implements any $k$-variable function.** An 8:1 mux handles any function of
> four variables; a 16:1 handles any function of five.

---

## 4. Why This Is The Most Important Block In The Course

**A mux used this way is a *lookup table*: you are not designing logic, you are storing the answer.**

**Change the data inputs and the same hardware computes a different function.** Nothing is re-wired.

> **That is what an FPGA is.** Its basic cell is a small lookup table — typically 4 to 6 inputs —
> implemented as a mux tree with memory cells on the data inputs. **Programming an FPGA means writing
> those memory cells.**
>
> **And it is why an FPGA flow does not need Week 4's minimisation:** a lookup table costs the same
> whether the function inside it is $\overline B\,\overline D$ or a 40-literal monster. **Minimisation
> matters when gates cost; it stops mattering when you are buying tables.**

**Week 12 returns to this.**

---

## 5. Building Bigger Blocks

**Muxes compose.** An 8:1 mux is two 4:1 muxes feeding a 2:1, with the high select bit choosing between them. **Decoders compose the same way** using their enables.

**This is how real designs handle width:** you never build a 32:1 mux as one gate network — you build a tree, and **the delay grows as $\log$ of the width** rather than linearly.

> **Compare Week 3.** The ripple-carry adder was linear in delay because of a *serial dependency*. A
> mux tree is logarithmic because its structure is a *tree*. **Structure decides delay** — which is
> exactly the lesson Week 6 will apply to the adder.

---

## 6. What To Take From This Lecture

1. **A mux selects; a demux routes.** They are inverses.
2. **A mux is a decoder with data gating; a demux is a decoder using its enable as data.**
3. **Shannon: $F = xF|_{x=1} + \overline xF|_{x=0}$.**
4. **A $2^k\!:\!1$ mux with constants on the data inputs is a truth table in hardware.**
5. **A $2^{k-1}\!:\!1$ mux implements any $k$-variable function**, with $0$, $1$, $x$ or $\overline x$ on each data input.
6. **A lookup table costs the same regardless of the function inside it** — which is why FPGAs do not minimise.
7. **Trees give logarithmic delay.** Structure decides delay.

---

*Next: Friday — Lab 5, multiplexer logic*
