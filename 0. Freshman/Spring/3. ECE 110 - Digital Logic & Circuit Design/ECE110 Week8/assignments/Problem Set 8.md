# ECE 110 · Digital Logic
## Problem Set 8
### Topic: Registers, Counters, and Shift Registers
**Released:** Thursday 18 March 2027, 14:30 · Week 8 (after Thursday's Lecture 2)
**Due:** Thursday 25 March 2027, 13:00 (start of class) · Week 9

---

> **State how many flip-flops and how many gates every design uses.**
>
> **For any counter, give the settling time and say whether transient states occur.**

---

## Part A — Registers (5 pts each)

**A1.** Draw a 4-bit register with a load enable. **Give the per-bit next-state equation.**

**A2.** **Why must a load enable gate the data rather than the clock?** Name two specific hazards.

**A3.** Give the four shift-register modes and name a real use for two of them.

**A4.** A 4-bit shift register holds `1011` and shifts right four times with serial-in 0. **Tabulate the bit shifted out and the state after each clock.**

---

## Part B — Ripple Counters (6 pts each)

**B1.** Draw a 3-bit ripple counter from T flip-flops. **How many gates?**

**B2.** Trace it from `011` to `100`, **listing every intermediate state the outputs actually take.**

**B3.** **Why is that a problem?** Give a specific consequence involving a decoder.

**B4.** Give the settling time of an $N$-bit ripple counter. **Which earlier circuit does this resemble, and why?**

**B5.** Tabulate settling time for $N=4,8,16,32$.

---

## Part C — Synchronous Counters (6 pts each)

**C1.** Give $T_0$ through $T_3$ for a 4-bit synchronous counter. **State the rule in words.**

**C2.** **Why are there no transient states?**

**C3.** Give the delay of an $N$-bit synchronous counter and compare its growth with the ripple version.

**C4.** **What does the synchronous counter cost that the ripple counter does not?** Which of the course's two costs is being traded for which?

**C5.** Design a **mod-10** counter by detect-and-clear. **Give the detect equation and justify why two gates suffice.**

---

## Part D — Design and Hazards (5 pts each)

**D1.** Design a **ring counter** with 4 flip-flops. Give its state sequence and its decode logic.

**D2.** Compare a 4-bit binary counter and a 4-bit ring counter on **flip-flops, states, and decode logic.** When would you choose each?

**D3.** **What happens to a ring counter that powers up in state `0000`?** What does this tell you about reset?

**D4.** An asynchronous clear on a mod-10 counter creates a brief spurious state. **Which state, and what is the clean alternative?**

---

## Marking Summary

| Part | Problems | Points |
|---|---|---|
| A — Registers | 4 × 5 | 20 |
| B — Ripple counters | 5 × 6 | 30 |
| C — Synchronous counters | 5 × 6 | 30 |
| D — Design and hazards | 4 × 5 | 20 |
| **Total** | | **100** |

---

*ECE 110 · Problem Set 8 · due Thursday of Week 9*
