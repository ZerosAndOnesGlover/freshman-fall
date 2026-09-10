# MATH 241 · Linear Algebra
## Week 4: Linear Transformations and Their Matrices

**Credits:** 4 (3 lecture + 1 recitation) · **Prerequisites:** MATH 141
**Assessment for this course (overall):** Problem Sets 35%, Midterms 40%, Final 25%
**This week's deliverables:** PS 4 (released Wednesday, due **Friday of Week 5**) and **Quiz 4** (Monday, covers Week 3). **PS 3 is due at 17:00 this Friday.**
**Recitation 3 is sat this Thursday** — it covers **Week 3**. Recitation 4, covering this week, is sat on the **Thursday of Week 5**.

> **This is a heavy week, and not because of MATH 241.** **PROG 201's Midterm 1 is Monday evening**
> (18:00–19:30, Weeks 0–3) and **CS 211's is Tuesday evening** (20:00–21:15, Weeks 0–3). This course
> has no exam this week — **its Midterm 1 is the Wednesday of Week 6**, covering Weeks 0–5 — and PS 3
> is due Friday as usual. Plan the front of the week around the two exams.

---

### Why This Week Exists

Because a matrix has been two things at once for four weeks and nobody has said so.

**It has been a table you eliminate** — Weeks 0 and 1 — **and it has been a function**, every time we asked what $Ax$ produces and which $b$ are reachable. Week 4 takes the second reading seriously, and the first question that arises is one that could not have been asked before: **where did the numbers come from?**

The answer is that they came from a **choice of basis** that nobody made explicitly, because it was always the standard one. **A matrix is not a transformation. It is a transformation plus a basis**, and different bases give different matrices for the same map.

**That sounds like an annoyance and is the most productive fact in the subject.** If the matrix depends on a choice, you may make the choice well — and §7 of L15 is the observation that the entire second half of this course is one question asked four times: *given $T$, find the basis in which its matrix is simple.* Week 7 answers it with eigenvectors, Week 10 with orthonormal eigenvectors, Week 11 with two bases at once and no hypotheses at all.

**Nothing this week needs a new computation.** Kernel is the null space, range is the column space, and injective, surjective and invertible are questions Weeks 0–3 already answer. **What is new is knowing which question you are asking**, and that the answer you get depends on where you stand.

---

### Learning Objectives

By the end of Week 4, you should be able to:

1. State the two conditions defining a linear transformation, and use $T(0) = 0$ as a first test.
2. **Say why a translation is not linear**, and how homogeneous coordinates repair it — and hence why 3-D graphics uses $4\times4$ matrices.
3. Translate between transformation and matrix language: kernel/null space, range/column space, injective, surjective, rank–nullity.
4. **Prove that a linear map is determined by its values on a basis**, and identify which half of "basis" gives existence and which gives uniqueness.
5. **Build the matrix of $T$ by computing $T$ on each basis vector** and stacking the coordinate columns.
6. **Derive the rotation matrix rather than recalling it.**
7. Use "composition is multiplication", and connect it to Week 1's derivation of the multiplication rule.
8. **Write differentiation as a matrix**, find its kernel and range, and explain its nilpotency.
9. Find the coordinates of a vector in a non-standard basis, and **state which direction $M$ converts.**
10. **Compute $B = M^{-1}AM$ and check it by an independent route.**
11. State what similar matrices share, and prove it for the trace.
12. **Explain why "find a good basis" is the programme for Weeks 7, 10 and 11.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L13 What a Linear Transformation Is]] | The two conditions; $T(0)=0$ as the first test; **why a translation is not linear and what graphics does about it**; every matrix is a transformation, with kernel/range as the two subspaces you already have; **differentiation, whose kernel is the $+\,C$**; **a linear map is determined by its values on a basis** |
| [[L14 The Matrix of a Transformation]] | Column $j$ is $T(v_j)$; five worked $2\times2$ maps; **derive the rotation matrix, do not memorise it**; **composition is multiplication — the theorem Week 1's definition was built for**; rotations commute and almost nothing else does; **$D$ on $\mathbb{P}_3$ with $D^4 = 0$** |
| [[L15 Change of Basis and the Search for a Good One]] | Coordinates depend on the basis; **$M$ takes new coordinates to old**, which everyone reverses once; $B = M^{-1}AM$ and similarity; **a reflection is $\begin{bmatrix}0&1\\1&0\end{bmatrix}$ or $\operatorname{diag}(1,-1)$ depending only on where you stand**; what similar matrices share; **the programme for Weeks 7, 10 and 11** |
| [[REC 4 One Map Two Bases]] | Board work on building matrices and on the direction of $M$. **Thursday of Week 5** |
| [[PS 4 Linear Transformations and Change of Basis]] | Five questions, 100 points, due **Friday of Week 5** |
| [[MATH241 Week4/assignments/QUIZ 4 Week 4 Monday\|QUIZ 4 Week 4 Monday]] | Ten minutes, covers **Week 3**, answer key printed |
| [[MATH241 Week4/resources/Reading Guide Week 4\|Reading Guide Week 4]] | Strang Ch. 8 — read out of order, and why — plus Axler 3.B, and fourteen questions |
| `resources/transformations.py` | Every number in L13–L15, reproducible. Pure Python, no dependencies |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**The matrix is a description. The transformation is the thing being described.**

$$\text{transformation} \;+\; \text{basis} \;\longrightarrow\; \text{matrix}$$

A reflection across $y = x$ is

$$\begin{bmatrix}0&1\\1&0\end{bmatrix} \qquad\text{or}\qquad \begin{bmatrix}1&0\\0&-1\end{bmatrix}$$

**depending only on which basis you write it in.** The mirror did not move. In the standard basis the matrix mixes the coordinates; in the basis $\{(1,1),(1,-1)\}$ — along the mirror and across it — it is two independent scalings, and it *says* what a reflection is.

**So the individual entries are not facts about the map.** Some combinations of them survive a change of basis — the trace, the determinant, the rank — and those are the real content. The rest is bookkeeping about a choice somebody made.

> **And this is not a curiosity to file away. It is the plan for the rest of the course:**
>
> | Week | Factorisation | Simple means | Exists when |
> |---|---|---|---|
> | **7** | $A = S\Lambda S^{-1}$ | diagonal | $n$ independent eigenvectors |
> | **10** | $A = Q\Lambda Q^\mathsf{T}$ | diagonal, $M^{-1} = M^\mathsf{T}$ | $A$ symmetric — **always** |
> | **11** | $A = U\Sigma V^\mathsf{T}$ | diagonal | **always, every matrix** |
>
> **Read the last column downwards.** Each week removes a hypothesis the one before it needed.

---

### Assessment Reminder

**Quizzes and the recitation carry no weight** and are still required. **Quiz 4 is at the start of Monday's lecture and covers Week 3.**

> **The recitation this week covers Week 3, not this week.** Recitation 3 is sat **this Thursday**;
> **Recitation 4 covers Week 4 and is sat on the Thursday of Week 5** — the last recitation before
> Midterm 1's material is complete.

Quizzes are tracked in [[_MATH 241 Quiz Record]].

---

### Connections

**Back:** **Week 3's L11 §1 is the hinge.** Once coordinates in a basis are unique, a vector in any $k$-dimensional space *is* a column in $\mathbb{R}^k$, which is what lets a course about columns compute derivatives. **Week 3's L11 §2 — that the standard basis was never privileged — is what makes changing it legal.** L13 §3's whole table is Weeks 2 and 3 renamed, and **Week 1's L04 §1 turns out to have been this week's composition theorem**, stated three weeks before the vocabulary existed.

**Sideways:** **CS 211's Week 4 is intermediate representations** — the same program written in source, in an AST, in three-address code, in SSA. **That is L15's idea in a different subject:** one object, several descriptions, and you choose the one in which the operation you want is easy. Neither course needs the other, and the parallel is worth noticing once. *(Its Midterm 1 is Tuesday of this week.)*

**Forward:** **Week 5's determinant is the first similarity invariant to get a proper definition**, and $\det(M^{-1}AM) = \det A$ is the theorem L15 §6 assumed. **Week 6 asks L15 §5's question in general** — which vectors does $T$ send to multiples of themselves — and the answer, eigenvectors, is exactly the basis that makes $B$ diagonal. **Week 7 is L15 §7's first row**, with the hypothesis under which it works. **Week 8's projections are L14 §2's $P^2 = P$**, and **Week 11's SVD is the only entry in L15 §7's table with no hypothesis at all** — because it allows a different basis at the input and the output, which L14 §1 permitted from the start and nothing until then required.

---

*MATH 241 · Week 4 · © CSE Department*
