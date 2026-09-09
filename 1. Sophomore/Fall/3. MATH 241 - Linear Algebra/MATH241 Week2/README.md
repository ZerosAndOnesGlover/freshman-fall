# MATH 241 · Linear Algebra
## Week 2: Vector Spaces, the Column Space and the Null Space

**Credits:** 4 (3 lecture + 1 recitation) · **Prerequisites:** MATH 141
**Assessment for this course (overall):** Problem Sets 35%, Midterms 40%, Final 25%
**This week's deliverables:** PS 2 (released Wednesday, due **Friday of Week 3**) and **Quiz 2** (Monday, covers Week 1). **PS 1 is due at 17:00 this Friday.**
**Recitation 1 is sat this Thursday** — it covers **Week 1**. Recitation 2, covering this week, is sat on the **Thursday of Week 3**.

---

### Why This Week Exists

Because for two weeks you have been answering *"does $Ax = b$ have a solution?"* one $b$ at a time, at $n^3/3$ operations each — and there are infinitely many $b$.

**This week answers it for all of them at once, and the answer is a shape.** The set of reachable $b$ turns out to be a subspace, the column space $\mathbf{C}(A)$; the set of $x$ that reach $0$ turns out to be another one, the null space $\mathbf{N}(A)$; and between them they say everything about solvability that there is to say. **Week 0's question is finished by Friday.**

**You have met both objects already without the names.** PS 0 Q2(c) asked you to prove a system insoluble *without eliminating*, and the argument — every column satisfies one linear relation, so every combination does — was the equation of a column space. Week 0's L01 §5 proved that two solutions generate a line, without saying what the line was made of; L09 says it is made of $\mathbf{N}(A)$.

**The lecture that costs people marks is L08 §4**, and it is a single sentence: *elimination preserves the null space and changes the column space.* Both spaces are built from the same numbers by the same algorithm, and they behave oppositely.

---

### Learning Objectives

By the end of Week 2, you should be able to:

1. State the vector-space axioms, and say what is deliberately **absent** from them.
2. Give three vector spaces that are not $\mathbb{R}^n$, and check the axioms for one.
3. **Apply the three-condition subspace test**, checking $0 \in W$ first, and produce a specific counterexample when it fails.
4. List the four kinds of subspace of $\mathbb{R}^3$, and say what "through the origin" excludes.
5. **Prove $\mathbf{N}(A)$ is a subspace using only linearity**, and say why $\{x : Ax = b\}$ with $b \ne 0$ is not.
6. **Say which $\mathbb{R}^k$ each of $\mathbf{C}(A)$ and $\mathbf{N}(A)$ lives in**, before computing either.
7. Compute $\mathbf{C}(A)$ from the pivot columns **of $A$**, and give its defining equation when it is a plane.
8. **Explain why $\mathbf{C}(A) \ne \mathbf{C}(\operatorname{rref}A)$ while $\mathbf{N}(A) = \mathbf{N}(\operatorname{rref}A)$**, with a separating vector for the first and an invertibility argument for the second.
9. Find the special solutions, one per free column, and verify them against $A$ rather than $R$.
10. **Read a special solution as a dependency among the columns.**
11. Derive $\operatorname{rank} + \operatorname{nullity} = n$ by counting columns, and use it without computing a null space.
12. **Give the complete solution as $x_p + \mathbf{N}(A)$**, prove both inclusions, and say what is and is not unique about it.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L07 Vector Spaces and Subspaces]] | Ten axioms and what they omit; matrices, polynomials and functions as spaces; the three-condition test with **two non-examples that each fail a different condition**; the four subspaces of $\mathbb{R}^3$; **$\mathbf{N}(A)$ proved a subspace in three lines**; unions, intersections, span |
| [[L08 The Column Space and When Ax = b Is Solvable]] | $\mathbf{C}(A)$ as the span of the columns; **solvable $\iff b \in \mathbf{C}(A)$**; rank; the pivot columns **of $A$**; **elimination moves the column space** — $5b_1-2b_2+b_3=0$ against $b_3=0$; the plane equation as a solvability test; $r = m$ and $r = n$ |
| [[L09 The Null Space and the Complete Solution]] | **$\mathbf{N}(A) = \mathbf{N}(R)$ exactly**, and why the same argument fails for $\mathbf{C}$; special solutions; **the null space as the list of column dependencies**; rank + nullity $= n$ by counting; **$x_p + \mathbf{N}(A)$, proved both ways**; the solution set as a translate |
| [[REC 2 Two Spaces and Which One Elimination Moves]] | Board work on which $\mathbb{R}^k$, and on the space that moves. **Thursday of Week 3** |
| [[PS 2 Subspaces the Column Space and the Null Space]] | Five questions, 100 points, due **Friday of Week 3** |
| [[MATH241 Week2/assignments/QUIZ 2 Week 2 Monday\|QUIZ 2 Week 2 Monday]] | Ten minutes, covers **Week 1**, answer key printed |
| [[MATH241 Week2/resources/Reading Guide Week 2\|Reading Guide Week 2]] | Strang §3.1–3.4, the week Axler starts to earn his place, and fifteen questions |
| `resources/spaces.py` | Every number in L07–L09, reproducible. Pure Python, no dependencies |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Elimination preserves how the columns depend on each other, and destroys where they are.**

Both spaces come from the same nine numbers and the same algorithm, and they behave in opposite ways:

$$\mathbf{N}(A) = \mathbf{N}(\operatorname{rref}A) \qquad\text{and}\qquad \mathbf{C}(A) \ne \mathbf{C}(\operatorname{rref}A)$$

For this week's matrix, $\mathbf{C}(A)$ is the plane $5b_1 - 2b_2 + b_3 = 0$ and $\mathbf{C}(\operatorname{rref}A)$ is the plane $b_3 = 0$. **Different planes, and $(1,0,0)$ is in the second and not the first.**

**The reason is one sentence.** A row operation combines entries *within each column*, so every column moves and the space they span moves with them. It does not touch $x$ at all — and $\mathbf{N}(A)$ is the set of $x$ with $Ax = 0$, which is the set of *relations among the columns*. Elimination exists to expose those relations, so of course it does not disturb them.

**So: read the pattern off $R$, then write down the columns of $A$.** Taking the pivot columns of $R$ instead produces a plausible plane that is the wrong subspace, and it is the most common error in Week 2.

---

### Assessment Reminder

**Quizzes and the recitation carry no weight** and are still required. **Quiz 2 is at the start of Monday's lecture and covers Week 1.**

> **The recitation this week covers Week 1, not this week.** Recitation 1 is sat **this Thursday**,
> the day before PS 1 is due; **Recitation 2 covers Week 2 and is sat on the Thursday of Week 3.**

Quizzes are tracked in [[_MATH 241 Quiz Record]].

---

### Connections

**Back:** **Week 0's L01 §4 is the whole prerequisite.** "$Ax$ is a combination of the columns" is what makes $\mathbf{C}(A)$ the right object; a student still reading $Ax$ as a stack of dot products cannot see why this week's definition is the natural one. **PS 0 Q2(c) computed a column space** and PS 1 Q1(c) proved $\mathbf{C}(AB) \subseteq \mathbf{C}(A)$, both without the vocabulary. **Week 1's L06 §3 supplies the proof in L09 §2** — row operations are invertible matrices, which is exactly why the null space survives them.

**Sideways:** **This is the week the two courses stop touching.** CS 201's caches and PROG 201's system calls have nothing to say about subspaces, and looking for a connection is wasted effort. The nearest thing is that $\mathbf{C}(A)$ and $\mathbf{N}(A)$ are *specifications* — statements about what a computation can and cannot produce — which is the habit CS 211's type systems are built on.

**Forward:** **Week 3 is this week made precise.** "Two independent vectors span a plane" was used freely here and is defined next week; *dimension* is what makes it a theorem that the number of pivots does not depend on how you eliminated. **Rank + nullity $= n$ is proved here by counting and reproved there as a statement about dimension.** The equation of $\mathbf{C}(A)$ comes from a vector killed by $A^\mathsf{T}$ — **the left null space, the fourth of the four fundamental subspaces**, which Week 3 completes. **Week 8's projection is the nearest point of $\mathbf{C}(A)$ to a $b$ outside it**, which is the question this week can only answer with "there is no solution"; **Week 9 is what to do about that**, and PS 2 Q5(c) proves the fact it rests on.

---

*MATH 241 · Week 2 · © CSE Department*
