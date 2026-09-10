# MATH 241 · Linear Algebra
## Week 6: Eigenvalues and Eigenvectors

**Credits:** 4 (3 lecture + 1 recitation) · **Prerequisites:** MATH 141
**Assessment for this course (overall):** Problem Sets 35%, Midterms 40%, Final 25%
**This week's deliverables:** PS 6 (released Wednesday, due **Friday of Week 7**) and **Quiz 6** (**Tuesday** — see below). **PS 5 is due at 17:00 this Friday.**
**Recitation 5 is sat this Thursday** — it covers **Week 5**. Recitation 6, covering this week, is sat on the **Thursday of Week 7**.

> **This week has two lectures, not three.** Its Monday is **Fall Break** and this course lectures
> Mon/Tue/Fri, so Week 6 runs **Tuesday and Friday only**. Nothing is dropped — Week 7 takes
> diagonalisation as planned — but both lectures are dense and the reading carries more than usual.
>
> **Four things happen in five days.** Fall Break Monday; **Quiz 6 Tuesday** (the only non-Monday
> quiz of the term); **Midterm 1 Wednesday**, 18:00–19:15, SSB 110, covering **Weeks 0–5**;
> Recitation 5 Thursday; **PS 5 due Friday**.
>
> **Nothing in this week's lectures is on the midterm.**

---

### Why This Week Exists

Because Week 4 asked a question it could not answer, and Week 5 built the tool.

Week 4's L15 §5 reflected across a line and chose the basis in which the matrix became $\operatorname{diag}(1,-1)$ — the mirror direction and the perpendicular. **What made those two vectors special is that the map sent each to a multiple of itself.** PS 4 Q4(e) and REC 4 §3(e) both asked how you would find such vectors in general and both had to stop there, because the method needs a determinant with a symbol in it.

**That equation is $Av = \lambda v$, and the method is $\det(A - \lambda I) = 0$.**

**This is also where Week 4's loose ends get tied.** Trace and determinant were shown to be similarity invariants and left unexplained; **they are the sum and the product of the eigenvalues.** And the question of why $I$ and $\begin{bmatrix}1&1\\0&1\end{bmatrix}$ are not similar — answered in Week 4 by a trick that works only for scalar matrices — **acquires a real invariant: the dimension of the eigenspace.**

**Two things go wrong, and both matter.** A rotation has **no real eigenvalues**, correctly, because it fixes no direction. And a shear has a **repeated eigenvalue with only one eigenvector** — too few to form a basis, so no diagonalisation is possible. **Week 7 is entirely about the second**, so the distinction between *a repeated eigenvalue* and *a deficient eigenspace* is the thing to leave this week holding.

---

### Learning Objectives

By the end of Week 6, you should be able to:

1. State $Av = \lambda v$, and say why $v \ne 0$ is required while $\lambda = 0$ is permitted.
2. **Derive $\det(A - \lambda I) = 0$** from the definition, in the four steps that use four different weeks.
3. **Say why cofactor expansion is the right tool here** and elimination is not.
4. Find eigenvalues by factoring the characteristic polynomial, and eigenspaces as $\mathbf{N}(A - \lambda I)$.
5. **Verify every eigenvector** with one matrix–vector product.
6. **Check eigenvalues against the trace and the determinant**, and say why both checks are free.
7. **Predict eigenvalues from geometry** for reflections, projections, rotations, scalings and triangular matrices.
8. Get eigenvalues from an identity like $P^2 = P$ or $R^2 = I$, **with no determinant.**
9. **Say why a rotation has no real eigenvalues**, and that trace and determinant survive into $\mathbb{C}$.
10. **Distinguish algebraic from geometric multiplicity**, and define *defective*.
11. **State that a repeated eigenvalue does not imply defective**, with $-I$ and the shear as the pair.
12. Prove that distinct eigenvalues give independent eigenvectors, **and know the converse fails.**

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L19 Eigenvalues and Eigenvectors]] | $Av = \lambda v$, and why $A^kv = \lambda^kv$ is the point; **$\det(A - \lambda I) = 0$, which is why Week 5 happened**; the eigenspace as a null space; a $3\times3$ worked with all three eigenvectors verified; **the six you should predict from geometry**; **a rotation with no real eigenvalues**; **a shear with too few** |
| [[L20 The Characteristic Polynomial]] | Degree $n$, always $n$ roots over $\mathbb{C}$; **$\sum\lambda_i = \operatorname{trace}$ and $\prod\lambda_i = \det$ — Week 4's invariants explained**; the $2\times2$ shortcut; **eigenvalues free from triangularity and from $q(A) = 0$**; **algebraic against geometric multiplicity**; distinct eigenvalues give independence; **pivots are not eigenvalues** |
| [[REC 6 Eigenvalues, and the Two That Go Wrong]] | Board work on the two failure modes, with $3I$ against the shear. **Thursday of Week 7** |
| [[PS 6 Eigenvalues and the Characteristic Polynomial]] | Five questions, 100 points, due **Friday of Week 7** |
| [[MATH241 Week6/assignments/QUIZ 6 Week 6 Tuesday\|QUIZ 6 Week 6 Tuesday]] | Ten minutes, **Tuesday**, covers **Week 5**, answer key printed |
| [[MATH241 Week6/resources/Reading Guide Week 6\|Reading Guide Week 6]] | Strang §6.1 twice, **Axler's determinant-free route and why to read it second**, and ten questions |
| `resources/eigen.py` | Every number in L19–L20, reproducible. Six predictable transformations, one flagged defective |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A repeated eigenvalue does not make a matrix defective. A deficient eigenspace does.**

$$-I = \begin{bmatrix}-1&0\\ 0&-1\end{bmatrix} \qquad\text{and}\qquad S = \begin{bmatrix}1&1\\ 0&1\end{bmatrix}$$

**Both have a single eigenvalue repeated twice.** $-I$ has a **two-dimensional** eigenspace — every vector is an eigenvector — and is diagonal already. $S$ has a **one-dimensional** eigenspace, spanned by $(1,0)$, and **no change of basis will ever make it diagonal.**

**The two multiplicities are the vocabulary for that difference:**

| | algebraic | geometric | |
|---|---:|---:|---|
| $-I$ | $2$ | $2$ | fine |
| $S$ | $2$ | $\mathbf{1}$ | **defective** |

**Always $1 \le \text{geometric} \le \text{algebraic}$, and a gap is fatal to diagonalisation.**

> **This also settles something Week 4 could only assert.** PS 4 Q5(d) proved $I$ and $S$ are not
> similar by observing $M^{-1}IM = I$ for every $M$ — true, and useless, because it works only
> because $I$ is exceptional. **The geometric multiplicity is a real invariant**: it applies to every
> pair, it says *what* differs, and it is the first genuinely new invariant since Week 4.
>
> **Week 7 is this dichotomy and nothing else.**

---

### Assessment Reminder

**Quizzes and the recitation carry no weight** and are still required.

> **Quiz 6 is on TUESDAY**, not Monday — the only one in the term. Week 6's Monday is Fall Break, so
> the quiz moves to the start of the week's first lecture. **Weeks 7–11 revert to Monday.**

Quizzes are tracked in [[_MATH 241 Quiz Record]].

---

### Connections

**Back:** **Week 5 exists for this week.** $\det(A - \lambda I) = 0$ is a determinant with a symbol in it, and **L17 §5's four defences of cofactor expansion** — after showing it $9\times10^{14}$ times too slow — turned on exactly this: elimination would divide by expressions that may vanish. **Week 4's L15 §5 asked the question**; PS 4 Q4(e) and REC 4 §3(e) both stopped at "you would look for directions $T$ does not turn". **Week 2's null-space algorithm is step 2**, unchanged. And **Week 1's L05 §2 characterisation 3** is why $\lambda = 0$ means singular.

**Sideways:** **PROG 201's Week 6 is the shell and job control**; CS 201's is caches. Neither connects, and this is a week with a midterm in it — do not go looking.

**Forward:** **Week 7 is the defective/diagonalisable dichotomy.** $n$ independent eigenvectors give $A = S\Lambda S^{-1}$, which is Week 4's L15 §7 first row with its hypothesis now stated precisely; **L19 §7's shear is the counterexample that makes the hypothesis necessary.** Week 7 also takes complex eigenvalues seriously, which L19 §6 previewed. **Week 10 removes the hypothesis for symmetric matrices** — they are never defective, and their eigenvectors are orthogonal. **Week 11's SVD removes it entirely.** And **Week 12's PageRank and PCA are both the dominant eigenvector of something**, which is why Week 0's L03 §2 said PageRank is not a linear solve.

---

*MATH 241 · Week 6 · © CSE Department*
