# ECE 110 · Digital Logic
## Quiz 4 — With Answer Key
### Week 5 · Wednesday · **Covers Week 4**

**Date:** Wednesday 24 February 2027 · 13:00–13:10 (start of Lecture 1) · Week 5 · ungraded

---

**Time:** 10 minutes · **Closed book** · **UNGRADED**
**Covers Week 4:** Karnaugh maps, grouping, prime implicants, don't-cares.

---

## Questions

**Q1.** Why are K-map columns ordered $00,01,11,10$?

**Q2.** List every cell adjacent to $m_0$ on a 4-variable map.

**Q3.** Minimise $\sum m(0,2,8,10)$.

**Q4.** Define *prime implicant* and *essential prime implicant*.

**Q5.** A student's cover is correct and uses six terms; the minimum is three. **What did they most likely do wrong, and how would they have caught it?**

---
---

# ANSWER KEY

---

**Q1.** So that **adjacent cells differ in exactly one variable** — which is what lets a pair cancel that variable, $AB\overline C+ABC=AB$. Binary order breaks it ($01\to10$ changes two bits).

**Q2.** $\boxed{m_1,\ m_2,\ m_4,\ m_8}$ — the last two by wrapping off the left and top edges. **The map is a torus.**

**Q3.** $\boxed{\overline B\,\overline D}$ — **two literals.** The four corners form one group. *(Verified.)*

*This is the most-missed item on the problem set; expect it to be missed here too.*

**Q4.** **Prime implicant:** a group that cannot be enlarged.
**Essential prime implicant:** a prime implicant that is the **only** one covering some minterm.

*Every minimal cover consists of prime implicants and contains all the essential ones.*

**Q5.** **They stopped at a correct cover without checking that every group was maximal** — almost certainly circling pairs where fours or eights existed.

**How to catch it:** after covering every 1, **go back over each group and ask whether it could have been larger.** Nothing about a correct answer signals that it is not minimal.

---

## Notes for the Instructor

- **Q3 is the diagnostic.** If most of the room misses it, spend three minutes redrawing the map as a torus before starting decoders.
- **Q5 previews today's lecture** — a decoder-plus-OR implementation skips minimisation entirely, at a cost in gates.

---

*ECE 110 · Quiz 4 · Week 5 · ungraded*
