# ECE 110 · Digital Logic
## Lab 4: Karnaugh Minimization Against a Machine Check
### Week 4 Lab Session

---

**Duration:** 2 hours (Friday 14:00–15:50, MEC 110)
**Format:** Pairs. **Both partners submit their own report.**
**Graded on:** completion + correctness — **100 points**
**Tools:** Python 3 with `sympy` (`SOPform`, `POSform`), Icarus Verilog. Breadboard for Part D.

---

## Overview

**Every previous lab checked whether your circuit was *correct*. This one checks whether it is *minimal*, which is a different and harder question.**

You will minimise by hand, then have a machine minimise the same functions, and **compare literal counts**. Where you lose, the interesting question is not "what is the answer" but **"which rule did I fail to apply".**

> **Expect to lose some.** The most common failure is a cover that is completely correct and uses
> groups that could have been larger — and nothing about a correct answer tells you it is not
> minimal. **That is the lab.**

---

## Part A — Minimise By Hand (30 pts)

**Do these on paper, with maps drawn, before touching a computer.** Record your answer and literal count for each.

| | function |
|---|---|
| **A1** (5) | $\sum m(0,1,2,5,6,7)$ *(3-var)* |
| **A2** (5) | $\sum m(0,2,5,7,8,10,13,15)$ |
| **A3** (5) | $\sum m(0,2,8,10)$ |
| **A4** (5) | $\sum m(0,1,4,5,8,9,12,13)$ |
| **A5** (5) | $\sum m(0,1,2,3,4,5,10,11,14,15)$ |
| **A6** (5) | $\sum m(1,3,7,11,15) + \sum d(0,2,5)$ |

**Seal your answers before Part B.** *(Fold the page over. The comparison is worthless if you revise after seeing the machine's answer.)*

---

## Part B — The Machine Check (25 pts)

**B1 (10 pts).** Using `sympy.logic.boolalg.SOPform`, minimise all six. **Tabulate: your literal count, the machine's, and the difference.**

```python
from sympy import symbols
from sympy.logic.boolalg import SOPform, POSform
A, B, C, D = symbols('A B C D')
print(SOPform([A, B, C, D], [0, 2, 8, 10]))
```

**B2 (8 pts).** For every function where you lost, **state which rule you failed to apply.** Choose from:

- a group could have been larger
- an edge or corner adjacency was missed
- overlapping groups were avoided
- a don't-care was treated as 0
- the cover used more groups than necessary

**B3 (7 pts).** For every function where you **tied**, verify with `POSform` whether the POS is cheaper. **Report any function where it is.**

---

## Part C — Prime Implicants By Program (20 pts)

Let $F = \sum m(0,1,2,5,6,7,8,9,10,14)$.

**C1 (8 pts).** Write code to enumerate **all prime implicants** — merge cubes differing in one bit, repeatedly, and keep whatever never merges.

**Report how many you found.**

**C2 (6 pts).** Find the **essential** ones: for each minterm, count how many prime implicants cover it; a count of exactly 1 makes that implicant essential.

**Report the essentials and the minterm that forces each.**

**C3 (6 pts).** Complete the cover and compare with `SOPform`'s answer. **Do they agree on the literal count?**

---

## Part D — Does Smaller Actually Work? (25 pts)

**D1 (12 pts).** Take A5's canonical form and your minimal form. Write **both** in Verilog and prove by exhaustive testbench that they agree on all 16 inputs.

**Report the failure count.**

**D2 (8 pts).** Count gates for both, under a stated convention. **What is the ratio?**

**D3 (5 pts).** Build the **minimal** version of A3 ($\sum m(0,2,8,10)$) on the breadboard and verify its four 1-rows.

**A3 minimises to two literals.** **How many gates did you need, and how many would the canonical form have taken?**

---

## Marking Summary

| Part | Points |
|---|---|
| A — minimise by hand | 30 |
| B — the machine check | 25 |
| C — prime implicants by program | 20 |
| D — does smaller actually work | 25 |
| **Total** | **100** |

---

## Submission

Your hand maps (photographed), your code, the comparison table, and **your honest count of how many you lost**.

> **Part A is marked on being attempted before Part B, not on being right.** A student who loses four
> and diagnoses all four correctly scores higher than one who loses none and writes nothing about it.

---

*ECE 110 · Week 4 · Lab 4*
