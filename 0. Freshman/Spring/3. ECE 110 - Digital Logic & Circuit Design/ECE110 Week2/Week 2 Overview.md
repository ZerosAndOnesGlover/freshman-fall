# ECE 110 · Digital Logic
## Week 2 · Overview
### Logic Gates — AND, OR, NOT, NAND, NOR, XOR, XNOR

---

**Topic:** the algebra becomes hardware
**Reading:** Harris & Harris §1.5–1.6, §2.5 | Mano & Ciletti §2.7–2.8, §3.5
**Assessment this week:** PS 2, Lab 2, **Quiz 1** *(Wednesday — covers Week 1, ungraded)*

---

## Symbols With Voltages Behind Them

**Last week's $A\cdot B$ becomes a component with two wires in and one wire out.** The seven gates:

| gate | symbol | output is 1 when | CMOS transistors |
|---|---|---|---:|
| **NOT** | $\overline A$ | input is 0 | **2** |
| **AND** | $AB$ | both inputs are 1 | 6 |
| **OR** | $A+B$ | either input is 1 | 6 |
| **NAND** | $\overline{AB}$ | *not* both are 1 | **4** |
| **NOR** | $\overline{A+B}$ | neither is 1 | **4** |
| **XOR** | $A\oplus B$ | inputs differ | 12 |
| **XNOR** | $\overline{A\oplus B}$ | inputs agree | 12 |

*(Transistor counts: static CMOS, 2-input.)*

---

## The Fact That Reorganises Everything

**AND costs more than NAND.**

$$\text{NAND} = 4 \text{ transistors} \qquad \text{AND} = \text{NAND} + \text{NOT} = 4+2 = 6$$

**CMOS builds inverting gates naturally.** A non-inverting gate is an inverting gate with an inverter bolted on — so **the "simple" gates of Week 1 are the expensive ones in silicon**, and the "compound" ones are the primitives.

> **This is the first time the course's two habits pull in the same direction.** Week 1 counted
> literals and gates; this week the count that matters is transistors, and it reverses which gate you
> would rather have. **Cost depends on what you are counting, and on the technology.**

---

## The Two Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Wednesday | Logic Gates and CMOS Reality | Why NAND is the primitive |
| **Lecture 2** | Thursday | Functional Completeness and Gate-Level Design | One gate type builds everything |

---

## Functional Completeness

**A set of gates is *functionally complete* if every Boolean function can be built from it.**

**$\{$NAND$\}$ alone is complete.** So is $\{$NOR$\}$ alone.

$$\overline A = A\ \text{NAND}\ A \qquad AB = \overline{(A\ \text{NAND}\ B)} \qquad A+B = \overline A\ \text{NAND}\ \overline B$$

*(All verified exhaustively, in Python and independently in Verilog.)*

### And a set that is *not* complete

**$\{$AND, OR$\}$ — without NOT — cannot build every function.** This is a theorem, and the proof is short:

> **Every function built from AND and OR alone is *monotone*: changing an input from 0 to 1 can never
> change the output from 1 to 0.** AND and OR are both monotone, and composing monotone functions
> gives a monotone function. **NOT is not monotone.** Therefore NOT cannot be built.
>
> *(Verified: AND and OR are monotone; NOT is not.)*

**This is the first impossibility proof in the course.** It does not say "we could not find a way" — it says no way exists.

---

## What XOR Costs

**The same function, three technologies:**

| built from | gates |
|---|---:|
| **NAND** | **4** |
| NOR | 5 |
| AND/OR/NOT | 5 |

*(All verified.)*

**The 4-gate NAND construction of XOR is the one to remember** — it appears inside every adder you build next week.

---

## This Week's Work

1. **Quiz 1** — Wednesday, covers Week 1. **Ungraded.**
2. **Lab 2** — gates on a breadboard, and rebuilding each one from NAND alone.
3. **PS 2** — gate-level design, completeness, cost.

---

*Next: Wednesday — Logic Gates and CMOS Reality*
