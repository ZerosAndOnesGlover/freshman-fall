# ECE 110 · Digital Logic
## Problem Set 4
### Topic: Karnaugh Maps, Minimization, Don't-Cares
**Released:** Thursday, Week 4 · **Due:** Thursday, Week 5 at the start of class

---

> **Draw the map.** An answer with no map earns half marks even when minimal — the map is the method
> being assessed.
>
> **Report the literal count** for every answer.
>
> **After you finish each map, go back and ask whether any group could have been larger.** That
> question is worth more marks on this problem set than anything else.

---

## Part A — Reading and Drawing Maps (5 pts each)

**A1.** Why are K-map columns ordered $00, 01, 11, 10$ rather than $00, 01, 10, 11$? **What property does that ordering guarantee?**

**A2.** Draw the 4-variable map template and label every cell with its minterm number.

**A3.** On a 4-variable map, list every cell adjacent to $m_0$. **There are four.** Explain the two that are not obvious.

**A4.** State the four rules for legal groups. **Why is a group of 6 illegal?**

---

## Part B — Minimisation (6 pts each)

**Minimise to a minimal SOP. Give the map, the groups, and the literal count.**

**B1.** $F = \sum m(0,1,2,5,6,7)$ *(3 variables)*

**B2.** $F = \sum m(0,2,5,7,8,10,13,15)$
*Something notable happens here — say what, and which variables the function actually depends on.*

**B3.** $F = \sum m(0,2,8,10)$
*This one is entirely about a rule from A3.*

**B4.** $F = \sum m(0,1,4,5,8,9,12,13)$

**B5.** $F = \sum m(0,1,2,3,4,5,10,11,14,15)$
**Then minimise it as a POS as well, and say which is cheaper.**

---

## Part C — Prime Implicants (5 pts each)

Let $F = \sum m(0,1,2,5,6,7,8,9,10,14)$.

**C1.** List **all six** prime implicants.

**C2.** Identify the **essential** prime implicants, and for each name a minterm that only it covers.

**C3.** Which minterms remain after the essentials? **Complete the cover.**

**C4.** Give the minimal SOP and its literal count.

**C5.** Three prime implicants do not appear in your answer. **List them, and explain why being prime was not enough.**

---

## Part D — Don't-Cares and Limits (5 pts each)

**D1.** $F = \sum m(1,3,7,11,15) + \sum d(0,2,5)$. **Minimise as SOP and as POS.** Which wins?

**D2.** A BCD digit drives "is it $\ge 5$?". Minimise **using** the don't-cares, and **again treating them as 0**. Report both literal counts.

**D3.** Your D2 don't-care answer outputs 1 for input $1111$. **Is that a bug? Justify carefully.**

**D4.** **What must you write down whenever you use a don't-care**, and why?

**D5.** K-maps become unusable past about six variables. **Name the systematic method that replaces them**, state its two steps, and say why real synthesis tools do not always return a true minimum.

---

## Marking Summary

| Part | Problems | Points |
|---|---|---|
| A — Reading and drawing maps | 4 × 5 | 20 |
| B — Minimisation | 5 × 6 | 30 |
| C — Prime implicants | 5 × 5 | 25 |
| D — Don't-cares and limits | 5 × 5 | 25 |
| **Total** | | **100** |

---

*ECE 110 · Problem Set 4 · due Thursday of Week 5*
