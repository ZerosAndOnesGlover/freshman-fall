# ECE 110 · Digital Logic
## Problem Set 6
### Topic: Arithmetic Logic Unit Design
**Released:** Thursday, Week 6 · **Due:** Thursday, Week 7 at the start of class

---

> **Give gate counts and delays, with your convention stated.**
>
> **Where a piece of hardware is reused, say so explicitly** — most of this problem set is about
> noticing reuse.

---

## Part A — ALU Structure (5 pts each)

**A1.** Draw the block diagram of a 4-bit, 8-operation ALU. **Label the mux and its select lines.**

**A2.** **Why compute all eight operations in parallel and discard seven**, rather than computing only the one selected?

**A3.** Which two of the eight operations cost **no gates at all**? Explain each.

**A4.** Give the four status flags, what each means, and the hardware for each.

---

## Part B — Operations and Flags (6 pts each)

**B1.** Show how one adder performs both $A+B$ and $A-B$. **What does the opcode bit drive?**

**B2.** Give the logic for $Z$ (zero) and for $N$ (negative) on a 4-bit result.

**B3.** For **signed** operands, $A<B$ is $N\oplus V$ after computing $A-B$. **Verify this on $A=3, B=5$ and on $A=-6, B=5$**, 4-bit.

**B4.** `if (a == b)` compiles to a subtraction and a branch. **Which flag, and why is the subtraction's result discarded?**

**B5.** A 32-bit ALU is built as 32 identical bit slices. **Which part does not simply replicate, and why does that part decide the clock speed?**

---

## Part C — Carry-Lookahead (6 pts each)

**C1.** Define $G_i$ and $P_i$ and give the carry recurrence.

**C2.** Expand $C_1$ through $C_4$ in terms of $G$, $P$ and $C_0$ only. **How many gate delays does each take?**

**C3.** **Why is a flat 64-bit carry-lookahead impossible?** Name the specific constraint.

**C4.** Give the **group** generate and propagate for a 4-bit block, and explain how a second-level unit uses them.

**C5.** A ripple adder is $2N+1$ gate delays. A hierarchical CLA at $N=64$ measures **12**. **Compute both in nanoseconds at 20 ps/gate and state which fits a 0.33 ns clock period.**

---

## Part D — The Trade (5 pts each)

**D1.** A 64-bit CLA costs about twice the gates of a ripple adder and is 10.8× faster. **Which of Week 2's two costs is being spent, and which bought?**

**D2.** **Why can no substitution of gate types fix the ripple adder's delay?** One sentence.

**D3.** Week 4's minimisation reduced a circuit from 43 gates to 7. **Would applying it to the ripple adder have made it usable? Justify.**

**D4.** Rank these by how much they reduce *delay*: minimisation, NAND-only conversion, carry-lookahead. **Justify the ranking.**

---

## Marking Summary

| Part | Problems | Points |
|---|---|---|
| A — ALU structure | 4 × 5 | 20 |
| B — Operations and flags | 5 × 6 | 30 |
| C — Carry-lookahead | 5 × 6 | 30 |
| D — The trade | 4 × 5 | 20 |
| **Total** | | **100** |

---

*ECE 110 · Problem Set 6 · due Thursday of Week 7*
