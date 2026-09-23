# ECE 110 · Digital Logic
## Lab 1: Boolean Identities, Verified Exhaustively
### Week 1 Lab Session

**Date:** Friday 29 January 2027 · 14:00–15:50 · Lab section (Week 1) — after both of Week 1's lectures

---

**Duration:** 2 hours (MEC 110)
**Format:** Pairs. **Both partners submit their own report.**
**Graded on:** completion + correctness — **100 points**
**Tools:** Python 3. No breadboard yet — hardware starts in Lab 2. (Verilog is Week 10; nothing here needs it.)

---

## Overview

**This lab establishes the method you will use for the rest of the course: check a claim two independent ways, and believe it only when both agree.**

You will verify every identity from this week with two independently written Python checkers, and then use the same machinery to test three claims that are *not* all true.

> **Why two tools?** Because a bug in your checker looks exactly like a true theorem. **Two unrelated
> implementations agreeing is evidence; one implementation agreeing with itself is not.**

---

## Part A — The Python Checker (25 pts)

**A1 (10 pts).** Write `check(f, g, n)` that returns `True` iff two $n$-input Boolean functions agree on **all $2^n$ assignments**, and returns a **counterexample** otherwise.

**A2 (10 pts).** Use it to verify all of:

| | |
|---|---|
| $A+0=A$ | $A\cdot1=A$ |
| $A+1=1$ | $A\cdot0=0$ |
| $A+A=A$ | $A\cdot A=A$ |
| $A+\overline A=1$ | $A\cdot\overline A=0$ |
| $\overline{\overline A}=A$ | |
| $A+AB=A$ | $A(A+B)=A$ |
| $A(B+C)=AB+AC$ | $A+BC=(A+B)(A+C)$ |
| $\overline{AB}=\overline A+\overline B$ | $\overline{A+B}=\overline A\,\overline B$ |
| $AB+\overline AC+BC=AB+\overline AC$ | |

**Report the number of identities checked and the number that failed.**

**A3 (5 pts).** Now verify $\overline{AB} = \overline A\,\overline B$ with the same checker.
**Report the counterexample your code returns**, and confirm by hand that it is genuine.

---

## Part B — A Second, Independent Checker (30 pts)

**B1 (15 pts).** Write a second checker that **does not loop over assignments at all.** Represent each
variable by its whole truth-table column, packed into an 8-bit integer — one bit per row:

```python
A, B, C = 0b11110000, 0b11001100, 0b10101010   # the eight rows of a 3-input truth table
MASK = 0xFF
def NOT(x): return ~x & MASK                      # Python's ~ alone gives a negative number
# x & y is AND on all eight rows at once; x | y is OR; x ^ y is XOR
print(A & (B | C) == (A & B) | (A & C))           # an identity holds iff both sides are equal
```

Check every identity from A2 this way, counting failures.

**B2 (8 pts).** **Do your two checkers agree, identity for identity?**
Report both counts. **If they disagree, the interesting work of this lab is finding out which one is
wrong** — say what you found.

**B3 (7 pts).** Deliberately break one identity in *one* of the two checkers — change a `&` to a `|`.
**Confirm the disagreement is detected**, and report what the failing checker printed. Then restore it.

---

## Part C — Three Claims (25 pts)

**Exactly one of the following is false. Do not guess — test all three.**

**C1 (8 pts).** $\;A\oplus B = AB' + A'B$

**C2 (8 pts).** $\;\overline{A\oplus B} = \overline A \oplus \overline B$

**C3 (9 pts).** $\;A\oplus(B\oplus C) = (A\oplus B)\oplus C$

**For each: report your verdict, and for the false one give the counterexample and the corrected statement.**

---

## Part D — Canonical Forms and Cost (20 pts)

Let $F(A,B,C) = \sum m(1,3,5,6,7)$.

**D1 (6 pts).** Generate the canonical SOP **programmatically** from the minterm list — do not write it out by hand. Count its terms and literals.

**D2 (6 pts).** Verify that $F = C + AB$ agrees with your canonical form on all eight rows.
**Report the literal counts of both**, and the ratio.

**D3 (8 pts).** Now count **gates**, not literals, for each form. Assume 2-input gates only, and state your counting convention *before* you count.

**Which form is cheaper, and by how much?** *This is the first time in the course you will put a number on "better", and it will not be the last.*

---

## Marking Summary

| Part | Points |
|---|---|
| A — the Python checker | 25 |
| B — the independent checker | 30 |
| C — three claims | 25 |
| D — canonical forms and cost | 20 |
| **Total** | **100** |

---

## Submission

Your code (both checkers), your measured counts, and your answers. **Every count reported must come from a run.**

> **"All identities verified" without the number of identities earns half marks.** The number is the
> evidence.

---

*ECE 110 · Week 1 · Lab 1*
