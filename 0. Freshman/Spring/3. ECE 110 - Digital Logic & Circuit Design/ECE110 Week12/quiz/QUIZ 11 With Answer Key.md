# ECE 110 · Digital Logic
## Quiz 11 — With Answer Key
### Week 12 · Wednesday · **Covers Week 11**

**Date:** Wednesday 14 April 2027 · 13:00–13:10 (start of Lecture 1) · Week 12 · ungraded

---

**Time:** 10 minutes · **Closed book** · **UNGRADED** · **The last quiz of the course.**
**Covers Week 11:** SRAM, DRAM, ROM, memory organisation.

---

## Questions

**Q1.** Transistors per bit for a flip-flop, SRAM and DRAM. **Why is memory not built from flip-flops?**

**Q2.** Name DRAM's three complications.

**Q3.** 8192 rows, 64 ms retention. **How often must a row be refreshed?** At tRFC = 350 ns, what fraction of the time is that?

**Q4.** A flat decoder for $2^{20}$ words needs how many gates? **And organised as a square array?**

**Q5.** **A ROM is which Week 5 circuit?**

---
---

# ANSWER KEY

---

**Q1.** ~20T, 6T, 1T. **1 Gib of flip-flops is 21.5 billion transistors** — more than most whole processors. *(Verified.)*

**Q2.** **Destructive reads** (needing a write-back), **leakage**, and hence **refresh**.

**Q3.** $64\text{ ms}/8192 = \boxed{7.81\ \mu\text{s}}$ per row.

$$\frac{8192\times350\text{ ns}}{64\text{ ms}} = \boxed{4.5\%}$$

*(Verified.)*

**Q4.** Flat: $2^{20} = \boxed{1\,048\,576}$. Square $1024\times1024$: $\boxed{2048}$ — **512× fewer.** *(Verified.)*

**Q5.** **A decoder driving a programmable OR plane** — Week 5's "one decoder shared by many OR gates".

**And therefore a lookup table**, which is the same object as Week 5's mux-based logic and tomorrow's FPGA cell.

---

## Notes for the Instructor

- **This is the last quiz.** Say so, and point at the revision guide.
- **Q5 sets up today's lecture directly** — the third arrival at the lookup table.

---

*ECE 110 · Quiz 11 · Week 12 · ungraded*
