# ECE 110 · Digital Logic
## Lab 6: A 4-Bit ALU, Built and Exhaustively Tested
### Week 6 Lab Session

**Date:** Friday 5 March 2027 · 14:00–15:50 · Lab section (Week 6) — after both of Week 6's lectures

---

**Duration:** 2 hours (MEC 110)
**Format:** Pairs. **Both partners submit their own report.**
**Graded on:** completion + correctness — **100 points**
**Tools:** Python 3 (your gate functions and Week 3 adder from Labs 2–3); breadboard for Part D
**Note:** the midterm was yesterday (Thursday 4 March) — **Parts A–C are the whole lab; Part D is short by design.**

---

## Overview

**Six weeks of parts, assembled into one component, then tested on every input it can receive.**

Your ALU has 8 operations and two 4-bit operands: **2048 combinations**. You will check all of them, and then measure the thing that decides whether such a design could go in a real processor.

---

## Part A — The ALU (35 pts)

**A1 (12 pts).** Write a 4-bit ALU in Python, `alu(op, a, b)` on lists of four bits, with a 3-bit opcode:

| op | operation |
|:-:|---|
| 000 | $A+B$ |
| 001 | $A-B$ |
| 010 | $A \text{ AND } B$ |
| 011 | $A \text{ OR } B$ |
| 100 | $A \oplus B$ |
| 101 | $\overline A$ |
| 110 | $A \ll 1$ |
| 111 | $A<B$ *(unsigned, result 1 or 0)* |

**Build the adder structurally** from your Lab 3 full adders. **The bitwise operations and the output
selection may use Python's operators on single bits.**

**A2 (12 pts).** Add the four flags: $C$, $V$, $Z$, $N$.

**$V$ must come from the carries** ($C_3\oplus C_4$), not from comparing against a wider result.

**A3 (11 pts).** **Subtraction must reuse the adder.** A second adder, or Python's `a - b` in place of the datapath, earns **half marks for this part** — the point is the Week 3 XOR trick.

---

## Part B — All 2048 (25 pts)

**B1 (15 pts).** Sweep **all 8 opcodes × 16 values of $A$ × 16 values of $B$**, comparing against Python's
own operators on integers.

**Report cases tested and failures.**

> ⚠ **Mask your comparisons to 4 bits.** This bit us in Lab 3 and it will bite you here: `a - b`
> in Python is not 4 bits wide (it can be negative), and comparing it directly against a 4-bit result
> reports hundreds of false failures on a correct design. Compare against `(a - b) & 0xF`.

**B2 (10 pts).** Separately verify **$V$ against true signed arithmetic** on all 256 operand pairs for the
ADD operation: read each 4-bit pattern as two's complement (`x - 16 if x >= 8 else x`, Week 0) and
set the expected $V$ when the true sum falls outside $-8\ldots7$.

**Report failures.**

---

## Part C — Timing (25 pts)

**C1 (10 pts).** Using one unit per gate, give the critical path of your 4-bit ALU. **Which operation and which output is on it?**

**C2 (8 pts).** Extend the ripple-carry model to $N = 8, 16, 32, 64$ and tabulate delay in gate delays and in nanoseconds at 20 ps/gate.

**C3 (7 pts).** For a 64-bit ALU in a 3 GHz processor (0.33 ns period): **does the ripple version fit? Give the number.**

Then: a hierarchical carry-lookahead adder at 64 bits measures **12 gate delays**. **Does that fit? By what margin?**

---

## Part D — On the Bench (15 pts)

**D1 (10 pts).** Build **just the logic operations** — AND, OR, XOR, NOT — for one bit slice, with a 4:1 mux selecting between them.

**Verify all four operations on the bench.**

**D2 (5 pts).** **You have built one slice of the ALU's logic unit.** State how many packages a full 4-bit version of just this part would need, and what a 32-bit version would need.

---

## Marking Summary

| Part | Points |
|---|---|
| A — the ALU | 35 |
| B — all 2048 | 25 |
| C — timing | 25 |
| D — on the bench | 15 |
| **Total** | **100** |

---

## Submission

Your ALU code, your sweep, your case and failure counts, your timing tables, and the bench results.

> **The midterm was yesterday.** Marked papers come back in Week 8.

---

*ECE 110 · Week 6 · Lab 6*
