# MATH 241 · Final Exam · Revision Guide
## Weeks 0–12 · Monday 15 December, 09:00–11:30 · VNC 100

---

## The Exam

| | |
|---|---|
| **When** | **Monday Dec 15, 09:00–11:30** — the first final of the Fall exam week |
| **Where** | **VNC 100**, with overflow to TH 200 — **your seat is posted on the course portal** at least a week before |
| **Duration** | **150 minutes** |
| **Marks** | **100** — about a mark and a half per minute |
| **Weight** | **25%** of the course grade |
| **Permitted** | **Two handwritten pages** of notes. No calculators, no devices |
| **Covers** | **Weeks 0–12, comprehensive** |

**Eight questions in three sections:**

| Section | Weeks | Questions | Marks |
|---|---|---|---:|
| **A** | 0–5 | elimination and $LU$; the four subspaces; determinants and eigenvalues | $34$ |
| **B** | 6–9 | diagonalisation and powers; orthogonality and least squares | $26$ |
| **C** | **10–12** | **symmetric and positive definite; the SVD; applications** | $\mathbf{40}$ |

**Section C is weighted most because no midterm has examined it.** Weeks 0–5 and 6–9 were each examined properly once; the final checks you still have them and spends its depth on what is new.

---

## The Fastest Useful Thing You Can Do

**Re-read the eleven quiz answer keys.** Quizzes 1–11 cover Weeks 0–10, the reasoning is written out, and between them they touch every question on the paper except the SVD and the applications.

**Then the two midterm papers and their feedback. Then PS 10 and PS 11** — because Weeks 10 and 11 have not been examined and the final has to examine them.

**If you have four hours:** ninety minutes on the quiz keys, an hour on PS 10–11, an hour on this guide's "know cold" lists, thirty minutes on your two pages.

---

## What Is Actually Examinable

**The lectures, the problem sets and the recitation sheets.** A figure that a script *printed* is fair to ask about — **what it showed, and why** — but you will not be asked to reproduce a measured number. "The normal equations failed at $\varepsilon = 10^{-8}$ because $1 + \varepsilon^2$ rounds to $1$" is a full answer; "$0.500000000$" is not an answer.

**Every computation on the paper comes out exactly** — integers, small fractions, or one clean square root. **If your arithmetic produces a messy fraction, you have made an error**, and the paper tells you to find it with a trace, a determinant or an orthogonality check. **Those checks earn marks when you show them.**

---

## Section A · Weeks 0–5 (34 marks)

### Q1 — Elimination and $LU$, 12 marks

**Know cold:** $A = LU$ with the multipliers in $L$ and **the sign convention right**; forward substitution then back substitution; $\det A$ = product of pivots.

**Prepare as a sentence:** **why unpivoted elimination on $\begin{bmatrix}\varepsilon&1\\1&1\end{bmatrix}$ returns $x_1 = 0$** — which step loses the information, and what partial pivoting changes. *(Week 0's L03 §4. The loss is at a subtraction, not a division.)*

### Q2 — The four subspaces, 12 marks

**Know cold:** reduced row echelon form; **pivot columns of the original matrix** for $\mathbf{C}(A)$; special solutions for $\mathbf{N}(A)$; a left-null-space vector from a row dependency; **the two dimension equations** $r + (m - r) = m$ and $r + (n - r) = n$; solvability as orthogonality to $\mathbf{N}(A^\mathsf{T})$.

### Q3 — Determinants and eigenvalues, 10 marks

**Know cold:** triangular determinant; $\det(cA) = c^n\det A$; $\det A^{-1} = 1/\det A$; **eigenvalues of a polynomial in $A$** are that polynomial of the eigenvalues, with the same eigenvectors; trace and determinant as sum and product.

---

## Section B · Weeks 6–9 (26 marks)

### Q4 — Diagonalisation and powers, 12 marks

**Know cold:** $\lambda = 1$ for a Markov matrix **from the column sums**, with no determinant; $A^k = S\Lambda^kS^{-1}$; the limit of $A^k$ and its columns as the steady state; **how many steps** from $\lvert\lambda_2\rvert^k$; defective means an eigenspace too small.

### Q5 — Orthogonality and least squares, 14 marks

**Know cold:** setting up $A$ and $y$ (**unknowns in $\hat x$**); the normal equations; **$A^\mathsf{T}e = 0$ and the centroid check**; Gram–Schmidt on two columns; $R\hat x = Q^\mathsf{T}y$.

**Prepare as a sentence:** $\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$ and what it does.

---

## Section C · Weeks 10–12 (40 marks)

### Q6 — Symmetric and positive definite, 14 marks

**Know cold:** **all five tests**, and that the minors test needs **every leading** minor; the boundary of positive definiteness is where a vector gives $x^\mathsf{T}Sx = 0$ — **a null vector**; $Q\Lambda Q^\mathsf{T}$ with **normalised** eigenvectors; $A = \sum\lambda_kq_kq_k^\mathsf{T}$; $LDL^\mathsf{T}$ as completing the square — **halve the cross coefficient**; the ellipse's **semi-axes are $1/\sqrt\lambda$**, and the axis ratio is $\sqrt{\operatorname{cond}}$.

### Q7 — The SVD, 14 marks

**Know cold, and practise until it is automatic — this is the question to be fluent at:**

1. $A^\mathsf{T}A$, its eigenvalues, and **$\sigma$ equal to their square roots**.
2. Unit eigenvectors $v_k$.
3. **$u_k = Av_k/\sigma_k$** — derived, not found independently, so the signs match.
4. **Multiply one entry back** to confirm $U\Sigma V^\mathsf{T} = A$.

**Also:** $\det U$, $\det V$ as rotation or reflection; $A_1 = \sigma_1u_1v_1^\mathsf{T}$ and Eckart–Young's error; **eigenvalues are not singular values**, and $\sigma_\min \le \lvert\lambda\rvert \le \sigma_\max$; $\operatorname{cond}_2 = \sigma_1/\sigma_n$.

### Q8 — Applications, 12 marks

**Know cold:** PCA as the eigenvectors of $D^\mathsf{T}D$ for centred data, variance fractions, and **lost variance $= \sigma_2^2$**; **why regression and PCA give different lines**; the damped Google matrix $G = \alpha P + \tfrac{1-\alpha}{n}\mathbf{1}\mathbf{1}^\mathsf{T}$ and what happens to power iteration with and without it; **Fourier partial sums minimise squared error, and Gibbs's overshoot does not go away.**

---

## Your Two Pages

**The Reading Guides for Weeks 10, 11 and 12 each end with a list of what belongs on the sheet from that week** — six, seven and four lines. **Start from those.** Then:

| Put on the sheet | Leave off |
|---|---|
| The five tests for positive definite, **with "leading"** | Anything you can derive in two lines |
| The SVD construction in four steps | Worked examples copied from the notes |
| The five factorisations: exists when, used for | Cholesky's algorithm (it is $LDL^\mathsf{T}$) |
| $\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$ | Numbers printed by scripts |
| The seven correct-but-unusable methods, one line each (L38 §7) | Proofs |

> **A page you wrote is worth more than a page you copied**, because writing it is the revision. **Two
> pages is enough for the definitions and the traps**; it is not enough for the course, and it is not
> meant to be.

---

## Before the Exam

**Recitation 12 is Thursday Dec 11, 15:00–15:50, SSB 108** — the final review. **Bring the one topic you would least like to see on the paper.**

**Prof. Abara's office hours in the completion period** are the usual ones: **Monday Dec 8, 13:00–15:00** and **Thursday Dec 11, 10:00–11:00**, SSB 310. The Engineering Help Desk is BH 120.

**On the day:** arrive by 08:45; **check your seat on the portal the night before**; bring two pens and your two pages. **If you are not starting Section C by 10:30, move on.**

---

*MATH 241 · Final Exam · Revision Guide · © CSE Department*
