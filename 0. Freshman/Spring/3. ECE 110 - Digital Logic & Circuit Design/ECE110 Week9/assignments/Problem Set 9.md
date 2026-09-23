# ECE 110 · Digital Logic
## Problem Set 9
### Topic: Finite State Machines — Mealy and Moore
**Released:** Thursday 25 March 2027, 14:30 · Week 9 (after Thursday's Lecture 2)
**Due:** Thursday 1 April 2027, 13:00 (start of class) · Week 10

---

> **Every state diagram must have exactly one outgoing arc per input value per state.** Check this
> before you go further; it is the commonest structural error.
>
> **State your output convention** for Moore machines — before or after the transition.
>
> **Say what every unused state code does.**

---

## Part A — The Procedure (5 pts each)

**A1.** List the six steps of FSM design. **Which is the only one requiring judgement?**

**A2.** For an overlapping `1011` detector, **what must the machine remember?** How many states does that give, and why is remembering the whole input impossible?

**A3.** Draw the Mealy state diagram for the detector. **Mark the arc that handles overlap** and explain it.

**A4.** Write the state table for your diagram.

---

## Part B — From Table to Gates (6 pts each)

**B1.** Assign $A{=}00$, $B{=}01$, $C{=}10$, $D{=}11$ and give the transition table over $(Q_1,Q_0,X)$.

**B2.** Give $D_1$, $D_0$ and $Y$ as minterm lists, then **minimise all three by K-map.**

**B3.** Draw the circuit. **How many flip-flops and how many gates?**

**B4.** $D_0$ minimises to a single wire. **Is that luck?** What would a different state assignment have cost?

**B5.** Verify your machine on the input `1011011011`. **Give the output sequence.**

---

## Part C — Mealy and Moore (6 pts each)

**C1.** State the difference in one sentence each.

**C2.** Draw the **Moore** version of the same detector. **How many states does it need, and why more than Mealy?**

**C3.** For the input `1011011011`, give both machines' outputs. **Do they agree? On what does the answer depend?**

**C4.** **Which one can glitch, and why?** Give a specific consequence, referring to Week 8.

**C5.** Describe the **registered-Mealy** hybrid and say what it buys.

---

## Part D — Encoding and Robustness (5 pts each)

**D1.** Compare **binary**, **one-hot** and **Gray** state encoding on flip-flop count and logic.

**D2.** **Why is one-hot often the default on an FPGA?** Connect this to Week 5.

**D3.** A 5-state machine is encoded in 3 bits. **How many unused codes are there, and what must you decide about them?**

**D4.** Design a Moore FSM for a traffic light: **Green (30 s) → Yellow (5 s) → Red (25 s) → Green**, using a timer input `T` that pulses when the interval expires. Give the state diagram and outputs.

---

## Marking Summary

| Part | Problems | Points |
|---|---|---|
| A — the procedure | 4 × 5 | 20 |
| B — from table to gates | 5 × 6 | 30 |
| C — Mealy and Moore | 5 × 6 | 30 |
| D — encoding and robustness | 4 × 5 | 20 |
| **Total** | | **100** |

---

*ECE 110 · Problem Set 9 · due Thursday of Week 10*
