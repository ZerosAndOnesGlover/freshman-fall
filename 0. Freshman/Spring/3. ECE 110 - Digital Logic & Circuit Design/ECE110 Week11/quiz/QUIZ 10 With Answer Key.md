# ECE 110 · Digital Logic
## Quiz 10 — With Answer Key
### Week 11 · Wednesday · **Covers Week 10**

---

**Time:** 10 minutes · **Closed book** · **UNGRADED**
**Covers Week 10:** Verilog, and the three traps.

---

## Questions

**Q1.** What does `reg` mean? **What decides whether you get a flip-flop?**

**Q2.** State the rule for `<=` versus `=`. **What happens if you use `=` in a 3-stage shift register?**

**Q3.** What hardware does `always @(*) if (en) y = d;` produce? **Why?**

**Q4.** `always @(a) y = a & b;` — **what does simulation do, what does synthesis do, and which is wrong?**

**Q5.** You describe an FSM with a `case` statement and write no equations. **What did the synthesis tool do for you?**

---
---

# ANSWER KEY

---

**Q1.** **`reg` means "assigned by a procedural statement"** — nothing more. A `reg` in `always @(*)` is plain gates.

**The clock decides storage:** `always @(posedge clk)`.

**Q2.** $\boxed{\texttt{<=}\text{ sequential},\ \texttt{=}\text{ combinational}}$

**With `=` in a shift register, all three stages load `d` in the same cycle** — three flip-flops behaving as one. *(Measured: `111` then `000`, against `xx1 → x10 → 100`.)*

**Q3.** **A latch.** With `en=0` nothing is assigned, so `y` must hold its previous value, and the tool builds storage to do it. *(Measured: `y` stayed at 1 after its input changed.)*

**Q4.** **Simulation:** the block only re-evaluates when `a` changes, so changing `b` does nothing. **Synthesis:** ignores the list and builds a proper AND gate.

$$\textbf{The simulation is wrong.}$$

**And that is what makes it the worst trap: the testbench passes and the chip fails.**

**Q5.** **State assignment, and derivation of the next-state and output equations** — running a minimisation equivalent to Week 4's.

**It may also have re-encoded your states**, most likely to one-hot, which is cheaper on an FPGA.

---

## Notes for the Instructor

- **Q4 is the diagnostic.** Students must say *which* is wrong, not merely that they differ.
- **Today begins memory** — open by asking how many transistors a flip-flop costs, then how many a gigabit of them would be.

---

*ECE 110 · Quiz 10 · Week 11 · ungraded*
