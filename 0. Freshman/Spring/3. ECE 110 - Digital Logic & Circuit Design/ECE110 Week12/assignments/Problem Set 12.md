# ECE 110 · Digital Logic
## Problem Set 12
### Topic: Programmable Logic — PLAs, PALs, FPGAs
**Released:** Thursday, Week 12 · **Due:** Thursday of exam week

---

> **This is the last problem set, and it is deliberately short** — the final exam is this week.
>
> **Show the sizing arithmetic.** That is most of the marks.

---

## Part A — The Two-Level Family (6 pts each)

**A1.** Tabulate which plane is programmable for a ROM, a PLA and a PAL.

**A2.** For $n$ inputs, $m$ outputs and $p$ product terms, give the fuse count for a PLA, a PAL and a ROM.

**A3.** Evaluate all three for $n=16$, $m=8$, $p=64$. **State the ratio between the largest and smallest.**

**A4.** **Why does a ROM grow as $2^n$ while a PLA does not?**

**A5.** **Which device makes Week 4's minimisation pay off architecturally, and how?**

---

## Part B — FPGAs (6 pts each)

**B1.** Describe the contents of an FPGA logic cell.

**B2.** How many bits does a 6-input LUT store, and how many distinct functions can it implement? **Which week did you first meet that second number?**

**B3.** Roughly how many 6-LUTs and how many levels does a 32-input function need?

**B4.** $C+AB$ is 3 literals; $AB+AC+BC+\overline A\,\overline B\,\overline C$ is 11. **How many 3-input LUTs does each need?** What does that imply about minimisation on an FPGA?

**B5.** List the six steps of the FPGA flow. **Which are NP-hard, and which earlier week said so?**

---

## Part C — Synthesis (7 pts each)

**C1.** **Why do FPGAs contain dedicated carry chains?** Refer to a specific earlier week.

**C2.** An FPGA gives up roughly 10× in speed and 20× in area against custom silicon. **When is that obviously the right trade, and when is it obviously wrong?**

**C3.** **Name the three habits this course has tried to build**, and give one concrete example of each from your own lab work.

**C4.** Choose any **three** design decisions from the course and, for each, state **which cost was spent and which was bought.**

---

## Marking Summary

| Part | Problems | Points |
|---|---|---|
| A — the two-level family | 5 × 6 | 30 |
| B — FPGAs | 5 × 6 | 30 |
| C — synthesis | 4 × 7 | 28 |
| *Presentation and arithmetic shown* | | 12 |
| **Total** | | **100** |

---

*ECE 110 · Problem Set 12 · the last one*
