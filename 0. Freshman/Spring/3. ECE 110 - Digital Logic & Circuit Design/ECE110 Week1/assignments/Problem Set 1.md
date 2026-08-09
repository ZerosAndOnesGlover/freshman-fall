# ECE 110 · Digital Logic
## Problem Set 1
### Topic: Boolean Algebra, De Morgan's Laws, Canonical Forms
**Released:** Thursday, Week 1 · **Due:** Thursday, Week 2 at the start of class

---

> **Name the law at every step.** An algebraic simplification with unnamed steps earns half marks
> even when the answer is right — in this algebra, an unjustified rewrite is exactly the thing that
> goes wrong.
>
> **Check every simplification against a truth table before you submit.** Your answer and the
> original must agree on every row. This is mechanical and it catches nearly everything.
>
> **Count your literals.** Every simplification below should say how many you started with and how
> many you finished with.

---

## Part A — Axioms and Proofs (5 pts each)

**A1.** Prove $A + AB = A$ algebraically, naming the law used at each step.

**A2.** Prove the second distributive law $A + BC = (A+B)(A+C)$ **by truth table**, showing all eight rows.
Then give a two-line argument for why the corresponding *arithmetic* statement is false, with a numerical counterexample.

**A3.** State the **duality principle**. Give the dual of each of: $A+\overline A = 1$, $A(A+B)=A$, and $A+BC=(A+B)(A+C)$.

**A4.** Prove the **consensus theorem** $AB+\overline AC+BC = AB+\overline AC$ algebraically.
*Hint: multiply the redundant term by $(A+\overline A)$.*

---

## Part B — Simplification (6 pts each)

**Simplify each to a minimal sum of products. Report the literal count before and after.**

**B1.** $AB + A\overline B$

**B2.** $A + \overline A B$

**B3.** $ABC + AB\overline C + A\overline BC$

**B4.** $(A+B)(A+\overline B)(\overline A+C)$

**B5.** $A\overline B + B\overline C + \overline AC + A\overline BC$

*For B5, say which term you removed and which theorem licensed it.*

---

## Part C — De Morgan and Complementation (5 pts each)

**C1.** Complement $AB + \overline C$.

**C2.** Complement $(A+\overline B)(\overline A+C)$.

**C3.** Complement $A + B\overline C + \overline B D$.

**C4.** A student writes $\overline{AB} = \overline A\,\overline B$.
**Give the input assignment that disproves it**, and state the correct law.

**C5.** Show that $\overline{A \oplus B} = A \oplus \overline B$, either by truth table or algebraically.

---

## Part D — Canonical Forms (5 pts each)

Let $F(A,B,C) = \sum m(0,2,5,7)$.

**D1.** Write the **truth table**, and the **canonical sum of products** (all four minterms in full).

**D2.** Write the **canonical product of sums**, listing the maxterms first.
*Remember that maxterms complement on 1, the opposite of minterms.*

**D3.** Minimise $F$ to a sum of products. **Report the literal count.**

**D4.** Minimise $F$ to a product of sums. **Which form is cheaper here?**

**D5.** **Look at your answer to D3 and describe $F$ in one sentence of plain English.**
There is something notable about which inputs $F$ actually depends on — say what it is, and how you can see it from the truth table alone.

---

## Marking Summary

| Part | Problems | Points |
|---|---|---|
| A — Axioms and proofs | 4 × 5 | 20 |
| B — Simplification | 5 × 6 | 30 |
| C — De Morgan | 5 × 5 | 25 |
| D — Canonical forms | 5 × 5 | 25 |
| **Total** | | **100** |

---

*ECE 110 · Problem Set 1 · due Thursday of Week 2*
