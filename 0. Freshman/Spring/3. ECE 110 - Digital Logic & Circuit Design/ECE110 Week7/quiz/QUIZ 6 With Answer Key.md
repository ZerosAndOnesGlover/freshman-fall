# ECE 110 · Digital Logic
## Quiz 6 — With Answer Key
### Week 7 · Wednesday · **Covers Week 6**

---

**Time:** 10 minutes · **Closed book** · **UNGRADED**
**Covers Week 6:** ALU structure, flags, carry-lookahead.

---

## Questions

**Q1.** Which two ALU operations cost **no gates**, and why?

**Q2.** Give the four ALU flags and the hardware for each.

**Q3.** For signed operands, what is the test for $A<B$ after computing $A-B$? **Why is $N$ alone insufficient?**

**Q4.** Define $G_i$ and $P_i$ and give the carry recurrence.

**Q5.** A 64-bit ripple adder is 129 gate delays; a hierarchical CLA is 12. At 20 ps/gate against a 0.33 ns clock, **which fits?** What is the area cost?

---
---

# ANSWER KEY

---

**Q1.** **Left shift** — a renaming of wires ($Y_i\leftarrow A_{i-1}$, $Y_0\leftarrow0$). **Comparison $A<B$** — read from the subtractor's flags. **Both reuse hardware that already exists.**

**Q2.** $C$ = adder's $C_{out}$; $V = C_{N-1}\oplus C_{out}$; $Z$ = **NOR of all result bits**; $N$ = the **MSB, a wire**.

**Q3.** $\boxed{N\oplus V}$.

**$N$ alone fails when the subtraction overflows.** Example: $A=-6$, $B=5$ in 4 bits. $A-B=-11$, which does not fit, so the result reads $+5$ — $N=0$. But $V=1$, so $N\oplus V=1$: **correctly $A<B$.** *(Verified on all 256 signed pairs.)*

**Q4.** $G_i=A_iB_i$ (generate), $P_i=A_i\oplus B_i$ (propagate), $C_{i+1}=G_i+P_iC_i$.

**Q5.** $129\times20\text{ ps}=2.58$ ns $=$ **7.75 periods — does not fit.**
$12\times20\text{ ps}=0.24$ ns $=$ **0.72 periods — fits.**

**Area cost: about $2\times$ the gates.** *(All measured.)*

---

## Notes for the Instructor

- **Q3 is the diagnostic.** Students who answer "$N$" have not met the overflow case; the $A=-6,B=5$ example is worth putting on the board.
- **Today's lecture is the hard pivot of the course** — combinational to sequential. Say so before starting.

---

*ECE 110 · Quiz 6 · Week 7 · ungraded*
