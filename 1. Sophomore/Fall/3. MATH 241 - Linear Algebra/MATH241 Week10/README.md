# MATH 241 · Linear Algebra
## Week 10: Symmetric Matrices, the Spectral Theorem, and Positive Definiteness

**Credits:** 4 (3 lecture + 1 recitation) · **Prerequisites:** MATH 141
**Assessment for this course (overall):** Problem Sets 35%, Midterms 40%, Final 25%
**This week's deliverables:** PS 10 (released Wednesday, due **Friday of Week 11**) and **Quiz 10** (Monday, covers Week 9). **PS 9 is due at 17:00 this Friday.**
**Recitation 9 is sat this Thursday** — it covers **Week 9**. Recitation 10, covering this week, is sat on the **Thursday of Week 11**.

> **Midterm 2 is this Wednesday**, Nov 12, **18:00–19:15, SSB 110**, covering **Weeks 6–9**.
> **Nothing from this week is on it.**
>
> **CS 201's Midterm 2 is Monday evening**, 18:00–19:15, VNC 100, covering its Weeks 5–9.
> **Two midterms in three days, and PS 9 still due Friday** — a heavy week, and none of it can move.
>
> **Papers are returned in Week 11**, and Recitation 10 is the post-mortem.

---

### Why This Week Exists

Because Week 7 ended by admitting that its main theorem could fail twice, and Week 10 is the hypothesis under which it cannot fail at all.

**$A = S\Lambda S^{-1}$ has two failure modes.** L22 §2 built a **defective** matrix, with fewer independent eigenvectors than dimensions, for which $S$ does not exist. And L22 §4 exhibited something worse — **$S$ existing and being numerically worthless**, with eigenvectors $(1,0)$ and $(1,10^{-8})$ giving $\operatorname{cond}(S) = 1.3\times10^{8}$. Week 8 named the fix and did not say when it was available.

> **It is available exactly when $A$ is symmetric, and then it is available every time.**
>
> $$A = A^\mathsf{T} \;\Longrightarrow\; A = Q\Lambda Q^\mathsf{T}, \qquad Q^\mathsf{T}Q = I, \qquad \Lambda \text{ real}$$

**Real eigenvalues, orthonormal eigenvectors, never defective. No hypotheses beyond symmetry.**

**And symmetric matrices are not a special case.** $A^\mathsf{T}A$ from Week 9, covariance matrices, Hessians, graph Laplacians, projection matrices, stiffness matrices — **all symmetric, all covered, always.**

**L31 then asks the second question:** which symmetric matrices have all eigenvalues *positive*? The answer — **positive definite** — has five equivalent forms that look nothing alike, and the fact that the **pivots** from elimination agree in sign with the **eigenvalues** from a completely different algorithm is not obvious and is the most useful thing in the lecture.

**L32 is what it is all for**, and it ends on a measurement rather than a theorem.

---

### Learning Objectives

By the end of Week 10, you should be able to:

1. **State the spectral theorem** and say which three claims it packs together.
2. **Prove the eigenvalues are real**, in two lines, and point at where symmetry is used.
3. **Prove eigenvectors for distinct eigenvalues are perpendicular.**
4. **Say why a repeated eigenvalue costs nothing**, and how to get an orthonormal set inside an eigenspace.
5. **Build $Q$ and verify $Q\Lambda Q^\mathsf{T} = A$ exactly**, and give $Q^{-1}$ without inverting.
6. **Write $A = \sum\lambda_kq_kq_k^\mathsf{T}$** and connect it to Week 8's projections.
7. **State the converse**, and use it as an error check.
8. **Apply all five positive-definiteness tests**, and know which is cheap when.
9. **Explain why positive diagonal entries are not enough**, with a counterexample.
10. **Compute $LDL^\mathsf{T}$ and complete the square**, and give the proof that positive pivots suffice.
11. **Read the geometry** of $x^\mathsf{T}Ax = 1$ — axes, lengths, and the aspect ratio as $\sqrt{\operatorname{cond}}$.
12. **Use Cholesky**, and say why it needs no pivoting.
13. **State the Rayleigh bound** and read $\operatorname{cond}_2$ off the eigenvalues.
14. **Say what "perfectly conditioned" means for an eigenvalue problem**, and give the non-symmetric counterexample.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L30 Symmetric Matrices and the Spectral Theorem]] | The hypothesis Weeks 7 and 8 were waiting for; **real eigenvalues in two lines**; perpendicular eigenvectors; **$Q\Lambda Q^\mathsf{T}$ verified exactly in fractions**; **$A$ as a sum of perpendicular projections**; repeated eigenvalues; **the converse** |
| [[L31 Positive Definite Matrices and Quadratic Forms]] | The quadratic form; **five tests flipping at exactly $b = \tfrac{32}{15}$**; **Sylvester's law and the positive-diagonal trap**; **$LDL^\mathsf{T}$ as completing the square**; the ellipse and its aspect ratio; $A^\mathsf{T}A$ |
| [[L32 What Positive Definiteness Is For]] | **Cholesky, and why it never pivots**; the Hessian test; **the Rayleigh quotient**; **Week 0's Hilbert matrix finally diagnosed**; **the perturbation measurement**; singular values, for Week 11 |
| [[REC 10 The Spectral Theorem on One Matrix]] | One matrix, four ways, plus the midterm post-mortem. **Thursday of Week 11** |
| [[PS 10 Symmetric and Positive Definite Matrices]] | Five questions, 100 points, due **Friday of Week 11** |
| [[MATH241 Week10/assignments/QUIZ 10 Week 10 Monday\|QUIZ 10 Week 10 Monday]] | Ten minutes, covers **Week 9**, answer key printed. **The last diagnostic before Midterm 2** |
| [[MATH241 Week10/resources/Reading Guide Week 10\|Reading Guide Week 10]] | Strang §6.4–§6.5, **Axler 7.A on why "symmetric" is basis-dependent**, and what belongs on the final's sheet |
| `resources/symmetric.py` | Every number in L30–L32, reproducible. **A Jacobi eigenvalue solver, in pure Python** |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A symmetric eigenvalue problem is perfectly conditioned. Nothing else in this course is.**

Perturb a matrix by $\delta$ and ask how far its eigenvalues move.

| | perturbation | eigenvalue movement | amplification |
|---|---:|---:|---:|
| **Symmetric $3\times3$** | $10^{-10}$ | $\le 9.998\times10^{-11}$ | $\mathbf{0.9998}$ |
| **A $10\times10$ that is not** | $10^{-10}$ | $\mathbf{1.0\times10^{-1}}$ | $\mathbf{10^{9}}$ |

**The second matrix is the shift with $\varepsilon$ in the corner.** $C^{10} = \varepsilon I$ exactly, so $\lvert\lambda\rvert = \varepsilon^{1/10}$ — **verified in exact rational arithmetic, with no eigenvalue solver involved.** Change one entry from $0$ to $10^{-10}$ and every eigenvalue leaves the origin and lands at magnitude $0.1$.

> **At $\varepsilon = 0$ that matrix is Week 7's worst case** — a single Jordan block, one eigenvalue
> repeated ten times, **one** eigenvector. **Defectiveness and eigenvalue sensitivity are the same
> phenomenon seen from two sides**, and the spectral theorem excludes both with a single hypothesis.

**This is the sixth time this term that "correct" and "usable" have come apart** — after Cramer's rule, the adjugate, the $n!$ determinant, the characteristic polynomial and the normal equations. **It is the first time the fix is free.** You do not choose a better algorithm; you notice that your matrix is symmetric, which it usually is, and the problem was never hard.

---

### Assessment Reminder

**Quizzes and the recitation carry no weight** and are still required. **Quiz 10 is at the start of Monday's lecture and covers Week 9** — the last diagnostic before Wednesday's paper, and Week 9 is the part of Midterm 2 you have had least time with.

**Midterm 2 is 20% of the course grade.** Weeks 6–9: eigenvalues, the characteristic polynomial, diagonalisation and its failures, orthogonality, projections, Gram–Schmidt, $QR$, least squares.

Quizzes are tracked in [[_MATH 241 Quiz Record]].

---

### Connections

**Back:** **Week 7's L22 §4 is the complaint this week answers** — $\operatorname{cond}(S) = 1.3\times10^8$ becomes $\operatorname{cond}(Q) = 1$. **Week 8's L26 §1 supplied orthonormal bases** and its Gram–Schmidt is what produces an orthonormal set inside a repeated eigenspace (L30 §6). **Week 8's L25 §2's projection matrix $qq^\mathsf{T}$ is each term of the spectral decomposition.** **Week 5's pivots return as $D$ in $LDL^\mathsf{T}$**, and Week 1's $LU$ becomes Cholesky. **PS 2 Q5(c)** — $A^\mathsf{T}A$ invertible iff independent columns — is L31 §7's whole content, three months early. **Week 0's Hilbert matrix is finally diagnosed**: its badness is entirely in $\lambda_\min \approx 10^{-17}$, and it is positive definite at every size, which settles what that adjective does and does not promise.

**Sideways:** **CS 201's Midterm 2 is Monday evening**, covering its Weeks 5–9. Different subject, same week; nothing in this material bears on it, and the only useful response is calendar management.

**Forward:** **Week 11's SVD is this week's theorem applied to $A^\mathsf{T}A$ and $AA^\mathsf{T}$** — both symmetric positive semidefinite by L31 §7, hence both covered by L30 with no hypotheses to check. **The singular values are the square roots of those eigenvalues**, which for a symmetric matrix reduce to $\lvert\lambda_i\rvert$ (L32 §7). **Week 11 also finally explains row rank $=$ column rank**, promised since Week 3's L12 §4. **Week 12's PCA is the spectral theorem on a covariance matrix**, and PageRank is L30 §5 on a matrix of size $10^9$.

---

*MATH 241 · Week 10 · © CSE Department*
