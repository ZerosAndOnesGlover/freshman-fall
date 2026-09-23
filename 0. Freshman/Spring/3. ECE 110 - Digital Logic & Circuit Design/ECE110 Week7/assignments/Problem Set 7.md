# ECE 110 · Digital Logic
## Problem Set 7
### Topic: Latches and Flip-Flops — SR, D, JK, T
**Released:** Thursday 11 March 2027, 14:30 · Week 7 (after Thursday's Lecture 2)
**Due:** Thursday 18 March 2027, 13:00 (start of class) · Week 8

---

> **For every sequential circuit, say what the state is and how many bits it holds.**
>
> **Timing diagrams must show the clock**, and must mark where the state changes.

---

## Part A — The SR Latch (5 pts each)

**A1.** Draw a cross-coupled NOR SR latch and give its four-row behaviour table.

**A2.** **Why is $S=R=1$ forbidden?** Answer in terms of the *outputs*, not "the datasheet says so".

**A3.** From $S=R=1$, both inputs drop to 0 simultaneously. **What happens, and what decides the outcome?**

**A4.** **Why can a race not be fixed by being careful with the inputs?** What is the actual fix?

---

## Part B — Latches to Flip-Flops (6 pts each)

**B1.** Give $S$ and $R$ for a gated D latch, and **prove the forbidden combination is unreachable.**

**B2.** Define *transparency*. **Why is it a problem when a latch's output can reach its own input?**

**B3.** Explain the master–slave D flip-flop. **Why can data never flow straight through?**

**B4.** Draw a timing diagram for a D latch and a D flip-flop given the same $D$ and clock. **Mark every point where each output changes.**

**B5.** State the difference between *level-sensitive* and *edge-triggered* in one sentence, and say why edge triggering makes large synchronous systems possible.

---

## Part C — JK and T (6 pts each)

**C1.** Give the JK characteristic table and equation.

**C2.** **What does the JK do with the SR's forbidden combination, and how?**

**C3.** Show that tying $J$ and $K$ together gives $Q^+=T\oplus Q$.

**C4.** Complete the **excitation table** for $D$, $T$, $J$ and $K$, marking don't-cares.

**C5.** **Why do JK-based designs minimise better than D-based ones?** Connect this to Week 4.

---

## Part D — Timing (5 pts each)

**D1.** Define $t_{su}$, $t_h$ and $t_{cq}$.

**D2.** Give the minimum clock period in terms of those three and the logic delay. **Relate it to Weeks 3 and 6.**

**D3.** A design has $t_{cq}=50$ ps, $t_{su}=30$ ps, and combinational logic of 2.58 ns. **What is the maximum clock frequency?** Repeat with the logic replaced by a 0.24 ns carry-lookahead adder.

**D4.** **A hold violation cannot be fixed by slowing the clock.** Explain why, and give the actual fix.

**D5.** What is metastability, when can it occur, and **why is a two-flip-flop synchroniser a mitigation rather than a solution?**

---

## Marking Summary

| Part | Problems | Points |
|---|---|---|
| A — the SR latch | 4 × 5 | 20 |
| B — latches to flip-flops | 5 × 6 | 30 |
| C — JK and T | 5 × 6 | 30 |
| D — timing | 4 × 5 | 20 |
| **Total** | | **100** |

---

*ECE 110 · Problem Set 7 · due Thursday of Week 8*
