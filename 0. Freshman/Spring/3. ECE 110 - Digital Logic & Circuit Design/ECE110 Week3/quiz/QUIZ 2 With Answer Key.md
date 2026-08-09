# ECE 110 · Digital Logic
## Quiz 2 — With Answer Key
### Week 3 · Wednesday · **Covers Week 2**

---

**Time:** 10 minutes, start of Wednesday's lecture
**Closed book, no calculator**
**UNGRADED** — carries no weight; it exists to find out what has not landed.

**Covers Week 2:** logic gates, CMOS cost, the digital abstraction, functional completeness, gate-level conversion.

---

## Questions

**Q1.** In static CMOS, NAND is 4 transistors and AND is 6. **Why?**

**Q2.** Build OR from NAND gates only. How many do you need?

**Q3.** Convert $F = AB + CD$ to a NAND-only circuit. **Does the gate count change?**

**Q4.** Is $\{$AND, OR$\}$ functionally complete? **Give the reason, not just the verdict.**

**Q5.** Two circuits compute $ABCD$: a chain of three 2-input ANDs, and a balanced tree of three. **Which is better, and on what measure?**

---
---

# ANSWER KEY

---

**Q1.** CMOS produces the **complement** of its pull-down condition naturally, so inverting gates are one stage. **AND is a NAND followed by an inverter**: $4+2=6$. **The inverting gates are the cheap primitives.**

**Q2.** $A+B = \overline A\,\text{NAND}\,\overline B$, with each complement itself a NAND:

$$\boxed{3 \text{ gates}}$$

*(Verified.)* *(This is De Morgan: $\overline{\overline A\,\overline B} = A+B$.)*

**Q3.** $F = \big(\overline{AB}\big)\,\text{NAND}\,\big(\overline{CD}\big)$ — **replace each AND with a NAND and the OR with a NAND.**

$$\textbf{The gate count does NOT change: 3 either way.}$$

*(Verified over all 16 assignments.)* **The two added inversions cancel** — that is why the conversion is free.

**Q4.** **No.**

**Reason:** AND and OR are **monotone** (flipping an input $0\to1$ never flips the output $1\to0$), composition preserves monotonicity, and **NOT is not monotone** — so NOT cannot be built. *(Verified.)*

*A verdict with no property named earns nothing — the proof is the answer.*

**Q5.** **Same gate count (3); different delay.**

| | gates | critical path |
|---|---:|---:|
| chain | 3 | **3** |
| tree | 3 | **2** |

**The tree is better on speed and identical on area.** **Gate count is area; critical path is speed** — they are different costs.

---

## Notes for the Instructor

- **Q3 and Q5 are the diagnostic ones.** Q3 catches students who add inverters the cancellation already removed; Q5 catches gate count being used as a proxy for quality.
- **Q5 previews tomorrow directly** — the ripple-carry adder is the case where the two costs come apart badly.
- **Do not collect.** Show of hands per question, then move on.

---

*ECE 110 · Quiz 2 · Week 3 · ungraded*
