# ECE 110 · Digital Logic
## Problem Set 2
### Topic: Logic Gates, Functional Completeness, Gate-Level Design
**Released:** Thursday, Week 2 · **Due:** Thursday, Week 3 at the start of class

---

> **State your gate-counting convention before you count.** 2-input gates only unless stated;
> say whether inverters are shared. **A count without a convention is not an answer.**
>
> **Every construction must be verified against a truth table.** You have the tools from Lab 1.

---

## Part A — Gates and the Digital Abstraction (5 pts each)

**A1.** Give the truth tables for NAND, NOR, XOR and XNOR.

**A2.** Explain in three sentences why a chain of 100 logic gates still produces a clean 0 or 1, while a chain of 100 analogue amplifiers does not.

**A3.** Define $NM_H$ and $NM_L$. A gate has $V_{OH}=2.4$, $V_{IH}=2.0$, $V_{IL}=0.8$, $V_{OL}=0.4$ V. **Compute both noise margins.**

**A4.** In static CMOS, NAND costs 4 transistors and AND costs 6. **Explain why**, and state the general rule about inverting versus non-inverting gates.

---

## Part B — NAND and NOR Conversions (6 pts each)

**B1.** Build NOT, AND and OR from NAND alone. Give the gate count for each.

**B2.** Build NOT, OR and AND from NOR alone.

**B3.** Convert $F = AB + CD$ to a NAND-only circuit. **Show why the conversion is valid**, and compare the gate count with the original AND-OR version.

**B4.** Convert $G = (A+B)(C+D)$ to a NOR-only circuit.

**B5.** Build XOR from NAND in **four** gates. Show the expression, and identify the sub-expression that is computed once and shared.
**How many gates does the naive $A\overline B+\overline AB$ construction take in NAND?**

---

## Part C — Functional Completeness (5 pts each)

**C1.** Define *functionally complete*.

**C2.** Prove $\{$NAND$\}$ is functionally complete.

**C3.** **Prove that $\{$AND, OR$\}$ is not functionally complete.**
*A proof by exhibiting a property is wanted, not "I could not find a way".*

**C4.** Is $\{$NOT, XOR$\}$ functionally complete? **Justify.**
*Hint: consider what all such functions have in common. Compare AND.*

**C5.** Is $\{$XOR, AND$\}$ functionally complete?
**Your answer must distinguish two cases** — say what the distinguishing assumption is.

---

## Part D — Cost (5 pts each)

**D1.** Tabulate the transistor count of NOT, NAND, NOR, AND, OR and XOR in static CMOS.

**D2.** Compute the total transistor count for XOR built (a) from 4 NAND gates, (b) from AND/OR/NOT. **Which wins, and by how much?**

**D3.** XOR costs 4 gates in NAND and 5 in NOR. **XNOR reverses this.** State the counts and explain the symmetry in one sentence.

**D4.** Define *critical path*. For $F=ABCD$ built as (i) a chain of three 2-input ANDs and (ii) a balanced tree of three 2-input ANDs, **give the gate count and the critical path of each.**

**D5.** From D4: **the two circuits have the same gate count and different delay.** What does this tell you about using gate count as a measure of quality?

---

## Marking Summary

| Part | Problems | Points |
|---|---|---|
| A — Gates and the abstraction | 4 × 5 | 20 |
| B — NAND/NOR conversions | 5 × 6 | 30 |
| C — Functional completeness | 5 × 5 | 25 |
| D — Cost | 5 × 5 | 25 |
| **Total** | | **100** |

---

*ECE 110 · Problem Set 2 · due Thursday of Week 3*
