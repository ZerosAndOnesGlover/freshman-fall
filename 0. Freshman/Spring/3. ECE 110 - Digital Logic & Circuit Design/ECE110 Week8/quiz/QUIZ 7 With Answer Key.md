# ECE 110 · Digital Logic
## Quiz 7 — With Answer Key
### Week 8 · Wednesday · **Covers Week 7**

**Date:** Wednesday 17 March 2027 · 13:00–13:10 (start of Lecture 1) · Week 8 · ungraded

---

**Time:** 10 minutes · **Closed book** · **UNGRADED**
**Covers Week 7:** latches, flip-flops, timing.

---

## Questions

**Q1.** Why is $S=R=1$ forbidden on an SR latch? **Answer in terms of the outputs.**

**Q2.** What is the difference between a latch and a flip-flop?

**Q3.** Give the JK characteristic equation. **What does $J=K=1$ do?**

**Q4.** Complete the excitation table for $J$ and $K$ for all four transitions.

**Q5.** State the minimum clock period in terms of $t_{cq}$, $t_{su}$ and the logic delay. **A hold violation cannot be fixed by slowing the clock — why?**

---
---

# ANSWER KEY

---

**Q1.** **Both outputs are driven to 0**, so $Q$ and $\overline Q$ are no longer complementary — the circuit violates its own labelling, and anything downstream expecting opposites breaks.

*(And leaving that state is a race whose outcome is set by gate delay, not by the inputs.)*

**Q2.** **A latch is level-sensitive** — it responds while its enable is asserted. **A flip-flop is edge-triggered** — it responds only at the clock transition.

**Q3.** $\boxed{Q^+ = J\overline Q + \overline KQ}$. **$J=K=1$ toggles**, redefining the SR's forbidden combination into its most useful one.

**Q4.**

| $Q\to Q^+$ | $J$ | $K$ |
|:-:|:-:|:-:|
| $0\to0$ | 0 | $\times$ |
| $0\to1$ | 1 | $\times$ |
| $1\to0$ | $\times$ | 1 |
| $1\to1$ | $\times$ | 0 |

*(Verified — the $\times$ are genuine don't-cares.)*

**Q5.** $\boxed{T_{clk}\ge t_{cq}+t_{\text{logic,max}}+t_{su}}$

**A hold violation is data arriving at the next flip-flop too *early*** — it depends on the delay from one flip-flop to the next, **not on the clock period at all.** Slowing the clock changes nothing; **you must add delay** on the fast path.

---

## Notes for the Instructor

- **Q5's second half is the diagnostic.** "Slow the clock" is the instinctive and wrong answer.
- **Q4 previews today's counter design** — the don't-cares are what make JK counters cheap.

---

*ECE 110 · Quiz 7 · Week 8 · ungraded*
