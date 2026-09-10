# MATH 241 · Reading Guide · Week 11
## Strang Chapter 7, and the factorisation with no hypotheses

---

**Strang calls the SVD the climax of linear algebra, and this is the week to believe him.** Chapter 7 is short, it assumes exactly Weeks 8 and 10, and every section of it is something you can check with `resources/svd.py`.

**Read it in the week it is set, before Thanksgiving.** Week 12 is applications — PCA is §7.3 — and a student who arrives on Dec 1 without the SVD will spend the last teaching week catching up instead of seeing the course close.

| Source | Read? | Why |
|---|---|---|
| **Strang §7.1 Image Processing by Linear Algebra** | **All of it** | L35 §3. **Do his rank-one flag example on paper** |
| **Strang §7.2 Bases and Matrices in the SVD** | **All of it, twice** | L33 entire, and L34 §1 |
| Strang §7.3 Principal Component Analysis | **Skim now, read in Week 12** | L36 |
| **Strang §7.4 The Geometry of the SVD** | **Read** | L33 §4, and the pseudoinverse (L34 §3) |
| **Trefethen & Bau, Lectures 4 and 5** | **Read if you read one thing** | The SVD done geometrically first. Lecture 5 has Eckart–Young with a proof |
| Trefethen & Bau, Lecture 31 | Skim | How the SVD is actually computed — L33 §7 |
| **Axler 7.D** | Read if you read 7.A last week | Polar decomposition and the SVD for operators |
| **Goodfellow §2.8–§2.9** | **Read** | The SVD and the pseudoinverse, in the notation CS 331 will use |

---

## Strang §7.2 — the questions to hold

1. **He builds the SVD from $A^\mathsf{T}A$**, as L33 §2 does. Find the line where he shows the $u$'s are orthonormal. **Where does the orthonormality of the $v$'s get used?**
2. **Two bases, one at each end.** Find where he says so. **Then find Week 4's L14 §1 and check it permitted this from the start.**
3. **$Av_k = \sigma_ku_k$.** He writes it as $AV = U\Sigma$. **Convert one to the other**, column by column.
4. **Which columns of $U$ and $V$ span which of the four subspaces?** He gives a picture. **Reproduce it for $M$ in L34 §1 without looking.**
5. **Does he explain row rank $=$ column rank here, or only use it?** *(Week 3 promised an explanation; L34 §1 gives one. Decide whether his is the same.)*
6. He warns against computing the SVD through $A^\mathsf{T}A$. **Find the warning and connect it to Week 9's L28 §1.** If he does not warn, note that — L33 §7 does.
7. **Full versus reduced (thin) SVD.** Which does he use by default? **What are the shapes of each factor in each?**

---

## Strang §7.1 and §7.4 — the questions to hold

8. **His flag example.** A flag with stripes aligned to the edges has low rank; a flag with a diagonal has high rank. **Predict the rank of three flags before reading his answers.** *(L35 §3 measured a bar, a post and a ring: $1$, $1$, $5$.)*
9. **Eckart–Young.** Does he prove it? **State it in both norms.** Which norm does image compression care about, and why?
10. **The pseudoinverse.** He writes $A^+ = V\Sigma^+U^\mathsf{T}$. **Check the four Penrose conditions on a $2\times2$ of rank one** with your own numbers.
11. **Rotation, stretch, rotation.** He draws it. **Do his $U$ and $V$ ever include a reflection**, and does it matter? *(L33 §4's example has $\det U = \det V = +1$. Not every SVD does — try $\begin{bmatrix}0&1\\1&0\end{bmatrix}$.)*
12. **Polar decomposition** $A = QS$, orthogonal times symmetric positive semidefinite. **Derive it from $U\Sigma V^\mathsf{T}$ in one line** — insert $V^\mathsf{T}V$. It is the statement that every matrix is a rotation followed by a stretch.

---

## Where Trefethen & Bau Earns Its Place

**Lecture 4 defines the SVD from the picture** — the image of the unit sphere is a hyperellipse — and derives the algebra afterwards. **That is the opposite order from Strang and from L33**, and reading both orders is how the SVD stops being a formula.

> **Lecture 5's Theorem 5.8 is Eckart–Young**, with a proof that is exactly the dimension argument
> sketched in L35 §1. **PS 11 Q5 asks you to fill it in**; reading Lecture 5 first is allowed and
> recommended.

---

## What Belongs on the Final's Sheet

**The final is Monday Dec 15, 09:00–11:30, two handwritten pages.** Seven lines from this week:

1. $A = U\Sigma V^\mathsf{T}$; $Av_k = \sigma_ku_k$; $A^\mathsf{T}u_k = \sigma_kv_k$. **Always exists.**
2. $\sigma_k^2$ = eigenvalues of $A^\mathsf{T}A$ **and** of $AA^\mathsf{T}$ (nonzero ones).
3. **Four subspaces:** $u_{1..r}$, $u_{r+1..m}$, $v_{1..r}$, $v_{r+1..n}$ — say which is which.
4. $\lVert A\rVert_2 = \sigma_1$, $\lVert A\rVert_F^2 = \sum\sigma_k^2$, $\operatorname{cond}_2 = \sigma_1/\sigma_n$.
5. $A^+ = V\Sigma^+U^\mathsf{T}$; $AA^+$ projects onto $\mathbf{C}(A)$; $x^+ = A^+b$ is the shortest least-squares solution.
6. **Eckart–Young:** $\lVert A - A_k\rVert_2 = \sigma_{k+1}$, $\lVert A - A_k\rVert_F = \sqrt{\sum_{j>k}\sigma_j^2}$.
7. **Five factorisations**, one line each: exists when, outer factors, used for — L35 §7.

**Do not write out the construction of the SVD.** It is L33 §2 and it follows from line 2 in four lines of algebra, which you should practise until you can.

---

## The Habit for This Week

**Ask which basis you are in, and whether it has to be the same one at both ends.**

Every factorisation this term has been a choice of basis. **Weeks 7 and 10 insisted on one basis for input and output**, because they were answering questions about $A^k$ and $x^\mathsf{T}Ax$, where the output feeds back in as input. **The SVD is answering a different question** — how big is $A$, what does it keep, what does it lose — and for that question the output never has to go back in, so two bases cost nothing.

> **So "which factorisation?" is really "which question?"** Powers and dynamics need eigenvalues.
> Size, rank and approximation need singular values. **Week 12 has one of each**: PageRank is a
> power iteration, and PCA is a low-rank approximation.

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| **Strang, MIT 18.06, Lecture 29** | The SVD, forty minutes, on a blackboard |
| **Strang, MIT 18.065** | A whole course built on the SVD, for data science |
| **Trefethen & Bau, Lectures 4, 5, 31** | Geometry, Eckart–Young, and computation |
| **Eckart & Young (1936), *Psychometrika* 1(3)** | The original paper, four pages, and readable |
| **Golub & Kahan (1965)** | The algorithm LAPACK still uses |
| **Week 12** | PCA, PageRank, regression and Fourier — **and why they are one theorem** |

---

*MATH 241 · Week 11 · Reading Guide · © CSE Department*
