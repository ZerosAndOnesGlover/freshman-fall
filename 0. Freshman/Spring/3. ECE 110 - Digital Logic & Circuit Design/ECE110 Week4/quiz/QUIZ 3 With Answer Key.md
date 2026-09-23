# ECE 110 · Digital Logic
## Quiz 3 — With Answer Key
### Week 4 · Wednesday · **Covers Week 3**

**Date:** Wednesday 17 February 2027 · 13:00–13:10 (start of Lecture 1) · Week 4 · ungraded

---

**Time:** 10 minutes, start of Wednesday's lecture
**Closed book, no calculator** · **UNGRADED**

**Covers Week 3:** half and full adders, ripple-carry, delay, subtraction and flags.

---

## Questions

**Q1.** Give $S$ and $C_{out}$ for a full adder, and its gate count.

**Q2.** An $N$-bit ripple-carry adder has $5N$ gates. **What is its delay in gate delays?** Give the value for $N=4$.

**Q3.** How do you turn an adder into an adder/subtractor? **What does the `SUB` line drive?**

**Q4.** Give the overflow flag in terms of carries. For $0111+0001$ in 4-bit signed, **is $V$ set?**

**Q5.** A 64-bit ripple-carry adder is 320 gates. **Is the gate count or the delay the reason it is not used? Give the number.**

---
---

# ANSWER KEY

---

**Q1.** $S = A\oplus B\oplus C_{in}$; $C_{out} = AB+(A\oplus B)C_{in}$.

$$\textbf{5 gates}\ \text{(2 XOR, 2 AND, 1 OR)}$$

**Q2.** $\boxed{2N+1}$. **At $N=4$: 9 gate delays.** *(Measured.)*

*The $C_{in}\to C_{out}$ path is 2 per stage; stage 0 costs 3 and the top sum bit adds 1.*

**Q3.** **One XOR on each $B$ input**, second input `SUB`.

**`SUB` drives both the XORs *and* the least significant carry-in** — the XORs give $\overline B$ and the carry-in gives the $+1$, together making $A+\overline B+1 = A-B$.

*Half marks if the carry-in is not mentioned — that is the whole trick.*

**Q4.** $V = C_{N-1}\oplus C_{out}$ — the carries **into and out of** the sign bit.

**For $0111+0001$:** carry into bit 3 is **1**, carry out is **0**, so $V = \boxed{1}$. Result $1000 = -8$ where $+8$ was wanted. *(Verified.)*

**Q5.** **The delay.**

$$2(64)+1 = 129 \text{ gate delays} \approx 2.58\text{ ns at }20\text{ ps/gate} = \mathbf{7.7} \text{ periods of a 3 GHz clock}$$

**320 gates is nothing.** *(Measured.)*

---

## Notes for the Instructor

- **Q3 and Q5 are diagnostic.** Q3 catches students who remember the XORs but not the carry-in; Q5 catches gate count still being treated as the measure of quality.
- **Q5 leads straight into today's lecture** — minimisation reduces area, and would not have helped here at all.

---

*ECE 110 · Quiz 3 · Week 4 · ungraded*
