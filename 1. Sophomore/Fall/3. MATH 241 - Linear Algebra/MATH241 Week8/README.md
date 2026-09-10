# MATH 241 · Linear Algebra
## Week 8: Orthogonality, Projections, and Gram–Schmidt

**Credits:** 4 (3 lecture + 1 recitation) · **Prerequisites:** MATH 141
**Assessment for this course (overall):** Problem Sets 35%, Midterms 40%, Final 25%
**This week's deliverables:** PS 8 (released Wednesday, due **Friday of Week 9**) and **Quiz 8** (Monday, covers Week 7). **PS 7 is due at 17:00 this Friday.**
**Recitation 7 is sat this Thursday** — it covers **Week 7**. Recitation 8, covering this week, is sat on the **Thursday of Week 9**.

> **Two evening exams this week, neither of them ours.** **PROG 201's Midterm 2 is Monday**
> (18:00–19:30, its Weeks 4–7) and **CS 211's is Tuesday** (20:00–21:15). MATH 241 has no exam this
> week — **its Midterm 2 is Week 10**, covering Weeks 6–9 — and PS 7 is due Friday as usual.
> **Plan the front of the week around the two exams**, as in Week 4.

---

### Why This Week Exists

Because Week 2 built vector spaces **with no length and no angle**, said so deliberately, and named the week they would come back:

> *Length and angle come back in **Week 8**, when they are added as extra structure. Everything
> between here and there is deliberately done without them, so that you find out how much does not
> need them.* — **L07 §2**

**The answer was: six weeks of material.** Bases, dimension, rank, the four subspaces, determinants, eigenvalues, diagonalisation — none of it needed a notion of *perpendicular*.

**This week adds it, and three debts fall due at once.**

| Debt | Owed since | Paid by |
|---|---|---|
| The four subspaces are orthogonal in pairs | **Week 3**, L12 §7 — computed, unproved | L24 §4, in one line |
| $Ax = b$ solvable **iff** $b \perp \mathbf{N}(A^\mathsf{T})$ | **Week 3**, L12 §5 — only "$\Rightarrow$" | L24 §4, via complements |
| $P^2 = P$, and why projections are singular | **Weeks 1, 4 and 7** — met three times | L25 §5 |
| $\operatorname{cond}(S)$ explodes near a defective matrix | **Week 7**, L22 §4 — a complaint | L24 §5: $\operatorname{cond}(Q) = 1$ |

**That last one is why the rest of the course looks the way it does.** Week 7 found that $A = S\Lambda S^{-1}$ can **exist and be numerically worthless** — eigenvectors nearly parallel, $\operatorname{cond}(S) = 1.3\times10^8$ at $\varepsilon = 10^{-8}$, every rounding error amplified by that factor. **An orthonormal basis has condition number exactly 1.** Weeks 9, 10 and 11 all insist on orthonormal bases, and this is the only reason.

---

### Learning Objectives

By the end of Week 8, you should be able to:

1. Compute lengths and angles from the dot product, and state **Cauchy–Schwarz** as what licenses the cosine.
2. **Prove $x \perp y \iff$ Pythagoras**, identifying the cross term as the dot product.
3. Define orthogonal subspaces, and **say why the floor and a wall are not an example.**
4. **Prove the four subspaces are orthogonal in pairs**, in one line from $Ax = 0$.
5. **State what *complement* adds** beyond orthogonality, and use it to prove Week 3's missing converse.
6. **Prove the nearest point of $W$ to $b$ is $p$**, where $b = p + e$ with $e \perp W$.
7. Project onto a line, keeping $aa^\mathsf{T}$ and $a^\mathsf{T}a$ straight.
8. **Derive the normal equations**, and say where independent columns are needed.
9. **Prove $P^2 = P$ and $P^\mathsf{T} = P$**, geometrically and algebraically, and give a projection's eigenvalues.
10. **Run Gram–Schmidt exactly**, and say why the result depends on the order.
11. **Produce $A = QR$**, and say why $R$ is upper triangular and invertible.
12. **Explain why $\operatorname{cond}(Q) = 1$ is the point**, and why classical Gram–Schmidt is not what production code runs.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L24 Orthogonality]] | The structure Week 2 withheld; Cauchy–Schwarz; **the four subspaces orthogonal in pairs, proved in one line**; **orthogonal complements, and the converse Week 3 owed**; $Q^\mathsf{T}Q = I$, rigid motions, and **$\operatorname{cond}(Q) = 1$ as the fix for Week 7** |
| [[L25 Projections]] | **The nearest point, by Pythagoras**; onto a line, $aa^\mathsf{T}$ over a number; **the normal equations**, using PS 2 Q5(c) for the first time; $P = A(A^\mathsf{T}A)^{-1}A^\mathsf{T}$ as a statement not an instruction; **$P^2 = P$ and $P^\mathsf{T} = P$, closing loops from Weeks 1, 4 and 7**; a left inverse that is not a right one |
| [[L26 Orthonormal Bases and Gram-Schmidt]] | **Three things that become free**; the conditioning table; Gram–Schmidt worked exactly, **producing the discrete Legendre vectors**; **$A = QR$, the fourth factorisation, always available**; **why classical Gram–Schmidt is the wrong thing to run** |
| [[REC 8 Projections by Hand]] | Board work on projections and on Gram–Schmidt's order-dependence. **Thursday of Week 9** |
| [[PS 8 Orthogonality Projections and Gram-Schmidt]] | Five questions, 100 points, due **Friday of Week 9** |
| [[MATH241 Week8/assignments/QUIZ 8 Week 8 Monday\|QUIZ 8 Week 8 Monday]] | Ten minutes, covers **Week 7**, answer key printed |
| [[MATH241 Week8/resources/Reading Guide Week 8\|Reading Guide Week 8]] | Strang Ch. 4, **Axler 6.A and why it matters for Week 12**, and sixteen questions |
| `resources/orthogonal.py` | Every number in L24–L26, reproducible. Ten dot products, a projection, Gram–Schmidt, and $A = QR$ |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Orthonormality is not elegance. It is conditioning.**

$$Q^\mathsf{T}Q = I \quad\Longrightarrow\quad Q^{-1} = Q^\mathsf{T} \quad\text{and}\quad \lVert Qx\rVert = \lVert x\rVert \quad\text{and}\quad \operatorname{cond}(Q) = 1$$

Week 7 ended on a complaint: $A = S\Lambda S^{-1}$ can exist and be useless, because near a defective matrix the eigenvector basis is nearly singular.

| eigenvectors | $\operatorname{cond}(S)$ |
|---|---:|
| $(1,0)$, $(1,10^{-2})$ | $200$ |
| $(1,0)$, $(1,10^{-4})$ | $2\times10^{4}$ |
| $(1,0)$, $(1,10^{-8})$ | $1.3\times10^{8}$ |

**An orthonormal basis gives $1$ in every row of that table.** Multiplying by $Q$ or $Q^\mathsf{T}$ is a rigid motion: it **cannot amplify a rounding error at all.**

> **So the design of the remaining weeks is not aesthetic.**
>
> **Week 9** solves least squares by $QR$ rather than the normal equations, because forming
> $A^\mathsf{T}A$ **squares the condition number.**
> **Week 10** is about symmetric matrices *because* their eigenvectors are orthonormal —
> $A = Q\Lambda Q^\mathsf{T}$, and Week 7's problem cannot arise.
> **Week 11's SVD** gives orthonormal bases at **both** ends, for **every** matrix.
>
> **Existence was never the difficulty. Conditioning is**, and this week is the answer.

---

### Assessment Reminder

**Quizzes and the recitation carry no weight** and are still required. **Quiz 8 is at the start of Monday's lecture and covers Week 7.**

> **Midterm 2 is the Wednesday of Week 10**, 18:00–19:15, SSB 110, covering **Weeks 6–9**. This week
> and next are two of the four weeks on it.

Quizzes are tracked in [[_MATH 241 Quiz Record]].

---

### Connections

**Back:** **Week 2's L07 §2 named this week explicitly** and withheld the dot product to show how much does not need it. **Week 3's L12 §7 computed ten dot products** and could not prove why they vanished; L24 §4 proves it in one line. **Week 3's L12 §5 proved only one direction** of the solvability criterion; L24 §4 supplies the converse. **PS 2 Q5(c) proved $A^\mathsf{T}A$ invertible** in Week 2 and it is used for the first time in L25 §3. **Week 1's L06 §2** ($A^\mathsf{T}A$ symmetric) gives $P^\mathsf{T} = P$. **Week 5's PS 5 Q5(d)** gave $\det Q = \pm1$. And **Week 7's L22 §4 is the complaint this week answers.**

**Sideways:** **PROG 201 and CS 211 both hold Midterm 2 this week**, on their Weeks 4–7. Nothing here bears on either; the note is scheduling, not content.

**Forward:** **Week 9 is L25 with data attached** — when $Ax = b$ has no solution, solve $Ax = p$ instead, and the normal equations become $R\hat x = Q^\mathsf{T}b$ once $A = QR$ is substituted (**PS 8 Q4(d) derives it**). **Week 10's spectral theorem** is $A = Q\Lambda Q^\mathsf{T}$ — Week 7's diagonalisation with an orthonormal $S$, available for every symmetric matrix without exception. **Week 11's SVD** has orthonormal bases at both ends and needs no hypotheses at all. **Week 12's Fourier item is L26 §1(c)** on a space of functions, with $\int fg$ in place of the dot product — **PS 8 Q3(d) already does the first three Legendre polynomials.**

---

*MATH 241 · Week 8 · © CSE Department*
