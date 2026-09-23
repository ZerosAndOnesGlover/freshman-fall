# ECE 110 · Digital Logic
## Week 9 · Overview
### Finite State Machines — Mealy and Moore

---

**Topic:** how a circuit decides over time
**Reading:** Harris & Harris §3.4 | Mano & Ciletti §5.4–5.7
**Assessment this week:** PS 9 (released Thu 25 Mar 14:30, due Thu 1 Apr 13:00), Lab 9 (**Fri 26 Mar**, 14:00), **Quiz 8** *(Wed 24 Mar, 13:00 — covers Week 8, ungraded)*

---

## The General Case

**Week 8's counter was a state machine with a fixed sequence and no inputs. This week the sequence depends on what arrives.**

> **A finite state machine is: a set of states, a rule for moving between them given an input, and a
> rule for producing an output.**

**That is the general form of every sequential circuit** — counters, controllers, protocol handlers, the control unit of a processor. Week 8's counter is the special case where the next state ignores the input.

---

## The Two Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Wednesday | State Diagrams and the Design Procedure | Six steps, every time |
| **Lecture 2** | Thursday | Mealy vs Moore | Same job, different trade |

---

## The Design Procedure

**Six steps, and they are the same six every time:**

1. **State the problem in words**, and decide what must be remembered.
2. **Draw the state diagram.**
3. **Write the state table.**
4. **Assign binary codes to the states.**
5. **Derive next-state and output equations** — Week 4's K-maps do this.
6. **Draw the circuit and verify it exhaustively.**

> **Step 1 is the only creative one.** "What must be remembered?" decides the number of states, and
> everything after it is mechanical.

---

## Mealy and Moore

| | output depends on | output changes |
|---|---|---|
| **Moore** | the **state** only | on the clock edge |
| **Mealy** | the **state and the input** | as soon as the input does |

**Worked all week: an overlapping `1011` sequence detector.**

$$\text{input } \texttt{1011011011} \;\Rightarrow\; \text{output } \texttt{0001001001}$$

*(Verified: both machines match a reference implementation on **2000 random 24-bit sequences**, zero mismatches.)*

| | states |
|---|---:|
| Moore | **5** |
| Mealy | **4** |

> **Mealy typically needs fewer states**, because its output can distinguish cases that Moore must
> separate into distinct states. **Moore's output is glitch-free and easier to reason about**, because
> it changes only at clock edges.
>
> **Neither is better.** Mealy for fewer states and faster response; Moore when the output drives
> something that must not glitch — which, after Week 8's scope photographs, you should take seriously.

---

## From Diagram to Gates

**The Mealy machine with states $A{=}00$, $B{=}01$, $C{=}10$, $D{=}11$:**

$$D_1 = Q_0\overline X + Q_1X\overline{Q_0} \qquad D_0 = X \qquad Y = Q_1Q_0X$$

*(Derived by K-map from the state table, then verified in Verilog: **4000 clock cycles, zero failures** against a reference.)*

**Note $D_0 = X$** — one wire, no gates. **A good state assignment can collapse the logic dramatically**, and a bad one leaves you with a mess that is still correct.

---

## State Assignment Matters

**With $n$ states you need $\lceil\log_2 n\rceil$ flip-flops — but *which* code goes to *which* state is free**, and it changes the logic.

| encoding | flip-flops | logic |
|---|---|---|
| **binary** | fewest | most |
| **one-hot** | one per state | **least** |
| **Gray** | fewest | fewer glitches on transitions |

**One-hot is Week 8's ring counter idea:** the state *is* the output, so the decode is free. **On an FPGA, where flip-flops are plentiful and logic is the scarce resource, one-hot is often the default.**

---

## This Week's Work

1. **Quiz 8** — Wed 24 Mar, covers Week 8. **Ungraded.**
2. **Lab 9** — build the detector both ways and compare.
3. **PS 9** — state diagrams, tables, encoding, and one machine designed from scratch.

---

*Next: Wednesday — State Diagrams and the Design Procedure*
