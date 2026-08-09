# ECE 110 · Digital Logic
## Week 1 · Overview
### Boolean Algebra — Axioms, Theorems, De Morgan's Laws

---

**Topic:** the algebra that circuits obey
**Reading:** Harris & Harris §2.1–2.3 | Mano & Ciletti §2.1–2.6
**Assessment this week:** PS 1, Lab 1. **No quiz** — quizzes begin Week 2.

---

## The Shift

**Week 0 was about numbers. From here to the end of the course, the subject is functions of bits.**

A combinational circuit computes a function from $n$ input bits to some output bits. **There is an algebra for exactly those functions**, it was written down by George Boole in 1854 for reasons that had nothing to do with electronics, and Claude Shannon noticed in 1937 that it described relay circuits exactly.

**This week is that algebra.** Next week it becomes hardware.

---

## The Two Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Wednesday | Boolean Axioms and Theorems | The rules, and where they differ from arithmetic |
| **Lecture 2** | Thursday | De Morgan, Duality, and Canonical Forms | Every truth table has a formula, mechanically |

---

## Boolean Algebra Is Not Arithmetic

**Most of the laws look familiar.** Commutativity, associativity, and $A(B+C) = AB+AC$ all behave as you expect.

**Then there is this one:**

$$A + BC = (A+B)(A+C)$$

**This is a theorem of Boolean algebra and it is false in ordinary arithmetic.** Take $A=1, B=1, C=0$:

| | Boolean | arithmetic |
|---|---|---|
| $A+BC$ | $1$ | $1$ |
| $(A+B)(A+C)$ | $1$ | $2$ |

*(Verified — they differ arithmetically at 2 of 3 sampled points, and agree in Boolean algebra at all 8.)*

> **Every identity in this course is checked against a truth table, not against your intuition about
> $+$ and $\times$.** The symbols were borrowed; the rules were not.

---

## The Two That Do the Work

**De Morgan's Laws:**

$$\overline{AB} = \overline A + \overline B \qquad\qquad \overline{A+B} = \overline A\,\overline B$$

**Break the bar, change the sign.** Next week these become the reason a NAND gate can build anything.

**The Consensus Theorem:**

$$AB + \overline A C + BC \;=\; AB + \overline A C$$

**The third term is redundant** — it is already covered by the other two, and no amount of staring at the expression makes that obvious. *(Verified: both sides give the same eight-row truth table, `[0,1,0,1,0,0,1,1]`.)*

**This one matters because it is exactly the term a Karnaugh map will tell you to delete in Week 4**, and because a redundant term is redundant gates.

---

## Canonical Forms: Every Truth Table Has a Formula

**Given any truth table you can write a formula for it mechanically** — one AND term per row that outputs 1, all OR'd together. That is the **canonical sum of products**.

**Worked example.** $F(A,B,C) = 1$ on rows $1, 3, 5, 6, 7$:

$$F = \overline A\,\overline B C + \overline A BC + A\overline B C + AB\overline C + ABC$$

**Five terms, fifteen literals.** And it simplifies to:

$$\boxed{F = C + AB}$$

**Two terms, three literals.** *(Verified equivalent.)*

> **The canonical form is always available and is almost never what you build.** Getting from one to
> the other is minimisation — algebraic this week, systematic in Week 4.

---

## How Many Functions Are There?

**With $n$ inputs there are $2^n$ rows, and each row's output can be 0 or 1 independently:**

$$\text{number of Boolean functions of } n \text{ variables} = 2^{2^n}$$

| $n$ | functions |
|---:|---:|
| 1 | 4 |
| 2 | 16 |
| 3 | 256 |
| 4 | 65 536 |
| 5 | 4 294 967 296 |
| 6 | 18 446 744 073 709 551 616 |

*(Verified.)*

**Six inputs already exceeds the number of distinct 64-bit integers.** This is why Week 4 needs a *method* rather than cleverness, and why nobody minimises anything by inspection past about four variables.

---

## This Week's Work

1. **Lab 1** — verify every identity in the course exhaustively, two independent ways.
2. **PS 1** — algebraic simplification, De Morgan, canonical forms.
3. **No quiz.** Quiz 1 is next week, and covers this week.

---

*Next: Wednesday — Boolean Axioms and Theorems*
