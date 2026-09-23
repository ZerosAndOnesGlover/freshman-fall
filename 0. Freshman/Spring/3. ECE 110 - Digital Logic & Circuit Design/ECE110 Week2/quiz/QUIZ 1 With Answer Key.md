# ECE 110 · Digital Logic
## Quiz 1 — With Answer Key
### Week 2 · Wednesday · **Covers Week 1**

**Date:** Wednesday 3 February 2027 · 13:00–13:10 (start of Lecture 1) · Week 2 · ungraded

---

**Time:** 10 minutes, start of Wednesday's lecture
**Closed book, no calculator**
**UNGRADED** — this quiz carries no weight. It exists so that you and I both find out what has not landed.

**Covers Week 1:** Boolean axioms and theorems, De Morgan's Laws, duality, canonical forms.

---

## Questions

**Q1.** Simplify $A + \overline A B$.

**Q2.** Complement $AB + \overline C$, giving the result as a product of sums.

**Q3.** State the duality principle, and give the dual of $A + AB = A$.

**Q4.** $F(A,B,C) = \sum m(3,5)$. Write the **canonical sum of products**.

**Q5.** True or false, with a one-line reason: *for every Boolean function, the minimal SOP has fewer literals than the minimal POS.*

---
---

# ANSWER KEY

---

**Q1.** $A+\overline AB = (A+\overline A)(A+B) = 1\cdot(A+B) = \boxed{A+B}$

*(Verified.)* **The second distributive law is doing the work** — students who try absorption here get stuck, because $A+\overline AB$ is not of the form $A+AB$.

**Q2.** $\overline{AB+\overline C} = \overline{AB}\cdot\overline{\overline C} = \boxed{(\overline A+\overline B)\,C}$

*(Verified.)* **Two applications: De Morgan on the sum, then De Morgan on $AB$, then involution on $\overline{\overline C}$.**

**Q3.** **The dual of a valid identity is valid**; form it by swapping $+\leftrightarrow\cdot$ and $0\leftrightarrow1$, leaving variables and complements unchanged.

$$A+AB=A \quad\xrightarrow{\text{dual}}\quad \boxed{A(A+B)=A}$$

**Q4.** $m_3 = \overline ABC$ and $m_5 = A\overline BC$:

$$\boxed{F = \overline ABC + A\overline BC}$$

*(Verified.)* *(It simplifies to $C(A\oplus B)$ — not required, but worth noting if a student offers it.)*

**Q5.** **FALSE.**

**Reason:** for $F=\sum m(0,2,5,7)$ the minimal SOP $AC+\overline A\,\overline C$ and the minimal POS $(A+\overline C)(\overline A+C)$ both have **4 literals**. *(Verified.)* **Neither form is always cheaper — you compute both.**

*(A counterexample where POS is strictly cheaper also earns full marks.)*

---

## Notes for the Instructor

- **Q1 and Q5 are the diagnostic ones.** Q1 separates students who pattern-match on absorption from those who read the expression; Q5 catches the very common belief that SOP is canonical *and* optimal.
- **If more than a third of the room misses Q2**, spend five minutes of Thursday on bubble pushing before starting functional completeness — the NAND conversions depend on De Morgan being automatic.
- **Do not collect these.** Ask for a show of hands per question and move on.

---

*ECE 110 · Quiz 1 · Week 2 · ungraded*
