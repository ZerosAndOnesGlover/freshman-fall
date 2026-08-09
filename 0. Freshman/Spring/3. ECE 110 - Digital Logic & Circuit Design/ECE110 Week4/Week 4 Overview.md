# ECE 110 · Digital Logic
## Week 4 · Overview
### Karnaugh Maps and Logic Minimization

---

**Topic:** how you make it smaller
**Reading:** Harris & Harris §2.7 | Mano & Ciletti §3.1–3.4
**Assessment this week:** PS 4, Lab 4, **Quiz 3** *(Wednesday — covers Week 3, ungraded)*

---

## The Problem Week 1 Left Open

**Week 1 showed that a canonical SOP is always available and never minimal** — $\sum m(1,3,5,6,7)$ went from 17 gates to 2 — **and then minimised it by algebra.**

**Algebra does not scale.** It requires you to *notice* that $ABC+AB\overline C$ share a factor, and by four variables there is too much to notice. Week 1 also counted the space: $2^{2^n}$ functions, $1.8\times10^{19}$ at $n=6$.

**A Karnaugh map replaces noticing with looking.**

---

## The Two Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Wednesday | Karnaugh Maps | Adjacency made visible |
| **Lecture 2** | Thursday | Minimization, Don't-Cares, and Beyond | Prime implicants, and where maps stop |

---

## The Whole Idea

**A K-map is a truth table with its rows rearranged so that physically adjacent cells differ in exactly one variable.**

**That ordering is Gray code** — $00, 01, 11, 10$, not $00, 01, 10, 11$:

$$\text{gray}(0..7) = 000,\ 001,\ 011,\ 010,\ 110,\ 111,\ 101,\ 100$$

*(Verified: consecutive codes differ in exactly one bit, **including the wrap-around from last to first** — which is why the map's edges join.)*

**Two adjacent 1s differ in one variable, so that variable cancels:**

$$AB\overline C + ABC = AB(\overline C + C) = AB$$

**A group of $2^k$ adjacent cells eliminates $k$ variables.** Circling is algebra you can see.

---

## What It Buys

**Worked example — $F = \sum m(0,1,2,3,4,5,10,11,14,15)$:**

| approach | result | literals |
|---|---|---:|
| canonical SOP | 10 minterms | 40 |
| **grouping only pairs** | 6 terms | **20** |
| **minimal SOP** | $AC + \overline A\,\overline B + \overline A\,\overline C$ | **6** |
| minimal POS | $(C+\overline A)(A+\overline B+\overline C)$ | **5** |

*(All verified equivalent.)*

> **The middle row is the hazard.** A cover made only of pairs is **completely correct** and more than
> three times too big. **A K-map answer that is right is not necessarily finished** — this week's
> whole discipline is looking for the largest groups, not the first ones.

**And note the last row: POS is cheaper here.** Week 1 said neither form always wins; here is the case.

---

## Don't-Cares

**Some input combinations never occur.** A BCD digit uses only $0000$–$1001$; the codes $1010$–$1111$ are **impossible**, so the output there can be anything.

**Marked $\times$ on the map, they can be treated as 1 or 0 — whichever makes the groups bigger.**

**"Is this BCD digit $\ge 5$?"**

| | expression | literals |
|---|---|---:|
| using don't-cares | $A + BC + BD$ | **5** |
| treating them as 0 | $\overline ABC + \overline ABD + A\overline B\,\overline C$ | 9 |

*(Verified — and the don't-care version agrees with the specification on every input that can actually occur.)*

**Don't-cares saved 4 literals, nearly half.** **Free information, if you notice you have it.**

---

## Where Maps Stop

**Maps work to 4 variables comfortably, 5 or 6 with effort, and then not at all** — human pattern recognition does not extend past three dimensions on paper.

**Beyond that the systematic method is Quine–McCluskey**, which is the same idea — find prime implicants, then cover — done as a table rather than a picture. **It is what a synthesis tool runs**, and it is why Week 12's FPGA flow needs no human to minimise anything.

---

## This Week's Work

1. **Quiz 3** — Wednesday, covers Week 3. **Ungraded.**
2. **Lab 4** — minimise by hand, then check every answer against a machine.
3. **PS 4** — maps, don't-cares, and one function where POS wins.

---

*Next: Wednesday — Karnaugh Maps*
