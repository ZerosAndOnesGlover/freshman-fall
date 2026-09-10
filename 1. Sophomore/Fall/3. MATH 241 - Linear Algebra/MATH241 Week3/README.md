# MATH 241 · Linear Algebra
## Week 3: Independence, Basis, Dimension, and the Four Subspaces

**Credits:** 4 (3 lecture + 1 recitation) · **Prerequisites:** MATH 141
**Assessment for this course (overall):** Problem Sets 35%, Midterms 40%, Final 25%
**This week's deliverables:** PS 3 (released Wednesday, due **Friday of Week 4**) and **Quiz 3** (Monday, covers Week 2). **PS 2 is due at 17:00 this Friday.**
**Recitation 2 is sat this Thursday** — it covers **Week 2**. Recitation 3, covering this week, is sat on the **Thursday of Week 4**.

---

### Why This Week Exists

Because Week 2 used the words *independent*, *plane* and *dimension* freely, and defined none of them.

That was not sloppiness — it was the only way to get the two subspaces built before the vocabulary existed. **But every count in Week 2 rested on something unproved:** that the number of pivots is a property of the *matrix* rather than of the elimination you happened to perform. If two different routes to echelon form could give different pivot counts, then $\dim\mathbf{C}(A)$ is not well defined and rank–nullity is a coincidence.

**This week closes that**, and then collects the dividend. Once dimension exists, two more subspaces appear for free — the **row space** and the **left null space** — and the four of them, with dimensions $r$, $n-r$, $r$, $m-r$, are the complete answer to every question Weeks 0–2 asked.

**Two things are genuinely surprising and one closes an old loop.** The number of independent rows equals the number of independent columns, for every matrix, though rows and columns live in different spaces and there are different numbers of them. Elimination **preserves the row space** while moving the column space — the exact opposite behaviour, from the same operations. And **the mysterious vector $(5,-2,1)$** that Week 2 pulled out of the air to write the equation of $\mathbf{C}(A)$ turns out to be a basis for the left null space, which is why there was exactly one condition.

---

### Learning Objectives

By the end of Week 3, you should be able to:

1. **Define linear independence**, and give the counterexample that kills "no vector is a multiple of another".
2. Test independence by stacking as columns: independent $\iff \mathbf{N}(X) = \{0\} \iff$ every column is a pivot column.
3. **Read a special solution as a dependency**, and say why $k > n$ in $\mathbb{R}^n$ forces dependence.
4. **Define a basis**, and prove that coordinates in a basis are unique — existence from spanning, uniqueness from independence.
5. **Prove that an independent list is never longer than a spanning list**, and derive that all bases have the same size.
6. State $\dim\mathbf{C}(A) = r$ and $\dim\mathbf{N}(A) = n-r$, with bases, and say what Week 3 adds to Week 2's versions.
7. Use the "$k$ vectors in a $k$-dimensional space" shortcut, **and say why the count alone proves nothing.**
8. **Name all four subspaces, their ambient spaces and their dimensions**, from $m$, $n$ and $r$ alone.
9. **Explain why the row-space basis is read off $\operatorname{rref}$ and the column-space basis is not**, from what elimination does to rows and to columns.
10. State row rank $=$ column rank, prove it, and say what the proof fails to explain.
11. **Read $\mathbf{N}(A^\mathsf{T})$ as the list of solvability conditions on $b$**, one per dimension.
12. **Draw the four-subspace diagram from memory** and use it to answer any solvability question.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L10 Linear Independence]] | The definition and its two commonest misreadings; **independence as $\mathbf{N}(X) = \{0\}$**; the null space as the complete list of dependencies; $k > n$ forces dependence; **the special solutions and the pivot columns are already independent**; independence in $\mathbb{P}_3$ and $C[0,1]$, where a trig identity is a linear dependence |
| [[L11 Basis and Dimension]] | Independent *and* spanning, and which condition buys which half of unique coordinates; **bases are not unique, their size is**; the lemma that an independent list never exceeds a spanning one; dimension; $\dim\mathbf{C}(A) = r$, $\dim\mathbf{N}(A) = n-r$; **the shortcut, and why the count alone proves nothing** |
| [[L12 The Four Fundamental Subspaces]] | All four on one matrix; **dimensions $r$, $n-r$, $r$, $m-r$**; **elimination keeps the row space and moves the column space**; row rank $=$ column rank and what the proof does not explain; **$(5,-2,1)$ revealed as a basis for the left null space**; the big picture; orthogonality as a Week 8 preview |
| [[REC 3 Four Subspaces on One Matrix]] | Board work producing all four, with the sums and the ten dot products. **Thursday of Week 4** |
| [[PS 3 Independence Basis Dimension and the Four Subspaces]] | Five questions, 100 points, due **Friday of Week 4** |
| [[MATH241 Week3/assignments/QUIZ 3 Week 3 Monday\|QUIZ 3 Week 3 Monday]] | Ten minutes, covers **Week 2**, answer key printed |
| [[MATH241 Week3/resources/Reading Guide Week 3\|Reading Guide Week 3]] | Strang §3.5–3.6, the week Axler is worth reading properly, and fifteen questions |
| `resources/dimension.py` | Every number in L10–L12, reproducible. Pure Python, no dependencies |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Elimination combines rows. That single fact decides both recipes.**

| | Preserved by elimination? | Basis read from |
|---|---|---|
| **Row space** $\mathbf{C}(A^\mathsf{T})$ | **yes** | the nonzero rows of $\operatorname{rref}(A)$ |
| **Column space** $\mathbf{C}(A)$ | **no** | the pivot columns of **$A$** |

Row operations replace rows by combinations of rows, so the *span of the rows* cannot change — and since the operations are invertible, nothing is lost either. **The row space comes through untouched.** The very same operations mix entries *within* each column, so every column moves, and the space they span moves with it.

**The asymmetry in the two recipes is not a convention to memorise.** It is that one fact, and a student who has it can reconstruct both recipes; a student who has memorised the recipes will eventually swap them, produce a plausible plane, and never find out.

**The dividend is that both spaces still have dimension $r$.** Different vectors, different ambient spaces, different counts of them — the same number. That is row rank $=$ column rank, it is genuinely surprising, and **the proof in L12 §4 establishes it without explaining it.** Week 11 explains it.

---

### Assessment Reminder

**Quizzes and the recitation carry no weight** and are still required. **Quiz 3 is at the start of Monday's lecture and covers Week 2.**

> **The recitation this week covers Week 2, not this week.** Recitation 2 is sat **this Thursday**,
> the day before PS 2 is due; **Recitation 3 covers Week 3 and is sat on the Thursday of Week 4.**

Quizzes are tracked in [[_MATH 241 Quiz Record]].

---

### Connections

**Back:** **Week 2 computed both bases and could not certify either.** L10 §5 shows the special solutions and the pivot columns were independent all along; L11 §4 shows the count is basis-independent, so the pivots were measuring something real. **Week 2's L08 §5 pulled $(5,-2,1)$ out of the air**, and L12 §5 identifies it. **Week 1's L06 §3 supplies the invertible $E$** that makes both the row-space and null-space preservation arguments work.

**Sideways:** **CS 211 is running type systems and inference this term**, and the shape of the argument is the same: a *basis* is a minimal generating set for a space, and a principal type is a minimal generating description of a term's uses. Neither course needs the other; the resemblance is worth noticing once and not pursuing.

**Forward:** **Week 4 is L11 §1 taken seriously.** Once coordinates in a basis are unique, a vector in any $k$-dimensional space *is* a column in $\mathbb{R}^k$ — and a linear transformation *is* a matrix, once you fix bases at both ends. **Changing the basis to make a matrix simple is the main tool of the rest of the course**, and it is available only because L11 §2 showed the standard basis was never special. **Week 5's determinant test** — $\det \ne 0$ means the $n$ columns are a basis — is L11 §8's shortcut. **Week 8 upgrades L12 §7's orthogonality from an observation to a theorem**, and turns "the dimensions add up" into "the subspaces genuinely split the space", which REC 3 §2(d) shows does not follow from dimensions alone. **Week 9 needs $\operatorname{rank}(A^\mathsf{T}A) = \operatorname{rank}(A)$**, which PS 3 Q5(d) proves. **Week 11 finally explains row rank $=$ column rank.**

---

*MATH 241 · Week 3 · © CSE Department*
