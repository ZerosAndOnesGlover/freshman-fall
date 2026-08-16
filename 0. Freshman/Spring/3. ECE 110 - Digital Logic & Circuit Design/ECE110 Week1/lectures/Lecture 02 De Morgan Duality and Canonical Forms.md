# ECE 110 · Digital Logic
## Week 1 · Lecture 2 (Thursday)
### De Morgan's Laws and Canonical Forms

**Date:** Thursday 21 January 2027 · 13:00–14:15 · Week 1

---

**Reading:** Harris & Harris §2.3–2.4 | Mano & Ciletti §2.5–2.6
**PS 1** released today, due Thursday of Week 2.

---

## 1. De Morgan's Laws

$$\boxed{\overline{AB} = \overline A + \overline B} \qquad\qquad \boxed{\overline{A+B} = \overline A\,\overline B}$$

**In words: break the bar and change the operator.**

*(Both verified exhaustively, twice — see Lab 1.)*

**They extend to any number of variables:**

$$\overline{ABC\cdots} = \overline A+\overline B+\overline C+\cdots \qquad \overline{A+B+C+\cdots} = \overline A\,\overline B\,\overline C\cdots$$

### The mistake to avoid

$$\overline{AB} \ne \overline A\,\overline B$$

**Check it at $A=1, B=0$:** the left side is $\overline{0} = 1$; the right side is $0\cdot1 = 0$. **Changing the operator is not optional** — it is the entire content of the law.

### Why they matter more than they look

**Complementing an expression is otherwise hard.** De Morgan makes it mechanical: complement every variable, swap every $+$ with $\cdot$, and you are done.

$$\overline{A\overline B + \overline A C} = (\overline A + B)(A + \overline C)$$

**And next week these laws become the reason a single gate type can build every circuit.** NAND is $\overline{AB}$; De Morgan says that is also $\overline A + \overline B$, so one gate is simultaneously an AND-with-inverted-output and an OR-with-inverted-inputs. **That double reading is what makes NAND universal.**

---

## 2. Reading a Circuit Both Ways

**A NAND gate drawn with a bubble on the output and a NAND gate drawn with bubbles on the inputs of an OR are the same gate.** De Morgan is the proof, and in Week 2 you will use it to redraw multi-level circuits so the bubbles cancel in pairs.

> **Bubble pushing** is the practical form of De Morgan, and it is how experienced designers read a
> schematic without writing an equation.

---

## 3. Canonical Forms — Every Truth Table Has a Formula

**Given a truth table, you can always write a formula for it. Mechanically. No insight required.**

### Sum of products, from the ones

**For each row where the output is 1, write an AND term that is true only on that row.** OR them together.

**Worked example.** $F(A,B,C)$:

| | $A$ | $B$ | $C$ | $F$ | |
|---|:-:|:-:|:-:|:-:|---|
| $m_0$ | 0 | 0 | 0 | 0 | |
| $m_1$ | 0 | 0 | 1 | **1** | $\overline A\,\overline B C$ |
| $m_2$ | 0 | 1 | 0 | 0 | |
| $m_3$ | 0 | 1 | 1 | **1** | $\overline A BC$ |
| $m_4$ | 1 | 0 | 0 | 0 | |
| $m_5$ | 1 | 0 | 1 | **1** | $A\overline B C$ |
| $m_6$ | 1 | 1 | 0 | **1** | $AB\overline C$ |
| $m_7$ | 1 | 1 | 1 | **1** | $ABC$ |

$$F = \sum m(1,3,5,6,7) = \overline A\,\overline BC + \overline ABC + A\overline BC + AB\overline C + ABC$$

**Each term is a *minterm*: every variable appears exactly once, complemented iff its bit is 0.**

### Product of sums, from the zeros

**For each row where the output is 0, write an OR term that is false only on that row.** AND them together.

$$F = \prod M(0,2,4) = (A+B+C)(A+\overline B+C)(\overline A+B+C)$$

**Note the inversion:** in a *maxterm* a variable is complemented iff its bit is **1** — the opposite of the minterm rule. **This is the single most common slip on this material.**

---

## 4. Canonical Is Not Minimal

**The canonical SOP above has 5 terms and 15 literals. The function is:**

$$\boxed{F = C + AB}$$

**Two terms. Three literals.** *(Verified equivalent to the canonical form on all eight rows.)*

**And the minimal POS is:**

$$F = (A+C)(B+C)$$

**Two terms, four literals.** *(Verified equal to the SOP.)*

| form | terms | literals |
|---|---:|---:|
| canonical SOP | 5 | 15 |
| **minimal SOP** | **2** | **3** |
| minimal POS | 2 | 4 |

> **Neither SOP nor POS is always cheaper.** Here SOP wins; for other functions POS does. **You
> compute both and pick**, which is exactly what Week 4's Karnaugh maps will let you do without
> algebra.

---

## 5. How Big Is The Space?

$$\text{Boolean functions of } n \text{ variables} = 2^{2^n}$$

**Because there are $2^n$ rows and each row's output is a free binary choice.**

| $n$ | rows | functions |
|---:|---:|---:|
| 1 | 2 | 4 |
| 2 | 4 | 16 |
| 3 | 8 | 256 |
| 4 | 16 | 65 536 |
| 5 | 32 | 4 294 967 296 |
| 6 | 64 | 18 446 744 073 709 551 616 |

*(Verified.)*

**At $n=6$ there are more Boolean functions than there are distinct 64-bit integers.**

> **This is the argument for method over cleverness.** You cannot search this space, you cannot
> tabulate it, and past about four variables you cannot eyeball a minimisation either. **Week 4
> gives you a procedure**, and Week 12's programmable logic gives you a machine that runs it.

---

## 6. What To Take From This Lecture

1. **$\overline{AB} = \overline A+\overline B$ and $\overline{A+B} = \overline A\,\overline B$** — break the bar, change the operator.
2. **$\overline{AB} \ne \overline A\,\overline B$.** Check at $A=1,B=0$.
3. **De Morgan makes complementing mechanical**, and makes NAND universal next week.
4. **Every truth table has a canonical SOP (from the ones) and a canonical POS (from the zeros).**
5. **Minterms complement on 0; maxterms complement on 1.** Opposite rules.
6. **Canonical is never minimal.** $\sum m(1,3,5,6,7) = C+AB$: 15 literals down to 3.
7. **$2^{2^n}$ functions.** Method, not cleverness.

---

*Next: Friday — Lab 1, verifying every identity exhaustively*
