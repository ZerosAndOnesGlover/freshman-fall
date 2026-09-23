# ECE 110 · Digital Logic
## Problem Set 3
### Topic: Half Adders, Full Adders, Ripple-Carry Adders, Delay
**Released:** Thursday 11 February 2027, 14:30 · Week 3 (after Thursday's Lecture 2)
**Due:** Thursday 18 February 2027, 13:00 (start of class) · Week 4

---

> **Every circuit you design must come with its truth table and its gate count.**
>
> **State your delay convention.** One unit per gate regardless of type, unless you say otherwise.
>
> **"It works" is not a result.** Say on how many input combinations, and how you checked.

---

## Part A — Adders From Scratch (5 pts each)

**A1.** Derive the half adder from its truth table. Give $S$, $C$, and the gate count.

**A2.** Give the full adder truth table (all 8 rows), and verify in one line that $S + 2C_{out} = A+B+C_{in}$ holds on every row.

**A3.** Show that $C_{out} = AB + AC_{in} + BC_{in}$ and $C_{out} = AB + (A\oplus B)C_{in}$ are **equal**, and say why the second is preferred in a real full adder.

**A4.** Draw a full adder as two half adders plus one gate. **Which gate, and why that one?**

---

## Part B — The Ripple-Carry Adder (6 pts each)

**B1.** Draw a 4-bit ripple-carry adder. **Give the total gate count** and show your arithmetic.

**B2.** Trace $1111 + 0001$ through it, stage by stage, giving each carry. **What makes this the worst case?**

**B3.** The $C_{in}\to C_{out}$ path through one full adder is **2 gate delays**. Derive the total delay of an $N$-bit ripple-carry adder, and check your formula at $N=4$.

**B4.** Tabulate gates and gate delays for $N = 4, 8, 16, 32, 64$.
At 20 ps per gate, **how long does a 64-bit addition take?** A 3 GHz clock has a period of 0.33 ns — **how many clock periods is that?**

**B5.** **Gate count and delay both grow linearly in $N$. Explain why only one of them is a problem.**

---

## Part C — Subtraction and Flags (5 pts each)

**C1.** Show how one XOR per bit plus a `SUB` control line turns an adder into an adder/subtractor. **Give the two cases.**

**C2.** **Where does the $+1$ of $A+\overline B+1$ come from?** Answer precisely — name the wire.

**C3.** Give the gate count of a 4-bit adder/subtractor **with** carry-out and overflow flags.

**C4.** Express the overflow flag $V$ in terms of the carries, and **verify it by hand** on $0111 + 0001$ read as signed 4-bit values.

**C5.** For the same bits $0111+0001$, give the result read as **unsigned** and as **signed**, and state which flag each reader should have consulted.

---

## Part D — Toward a Faster Adder (5 pts each)

**D1.** Define the **generate** and **propagate** signals $G_i$ and $P_i$, and give the recurrence $C_{i+1} = G_i + P_iC_i$.

**D2.** Expand $C_1$, $C_2$ and $C_3$ into expressions in $G$, $P$ and $C_0$ only. **How many gate delays does each need?**

**D3.** **What is the structural reason the ripple-carry adder is slow?** One sentence. *"Because the carry ripples" is a restatement, not a reason — say what property of the design forces it.*

**D4.** Carry-lookahead makes the delay logarithmic and costs more gates. **Which of Week 2's two costs is being traded for which?**

**D5.** A student proposes making the adder faster by using NAND gates throughout, since NAND is cheaper in transistors. **Will this help the delay? Justify.**

---

## Marking Summary

| Part | Problems | Points |
|---|---|---|
| A — Adders from scratch | 4 × 5 | 20 |
| B — The ripple-carry adder | 5 × 6 | 30 |
| C — Subtraction and flags | 5 × 5 | 25 |
| D — Toward a faster adder | 5 × 5 | 25 |
| **Total** | | **100** |

---

*ECE 110 · Problem Set 3 · due Thursday of Week 4*
