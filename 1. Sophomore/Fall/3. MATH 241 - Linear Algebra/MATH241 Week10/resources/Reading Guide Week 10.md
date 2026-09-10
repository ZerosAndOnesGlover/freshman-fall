# MATH 241 · Reading Guide · Week 10
## Strang §6.4–§6.5, and the first reading with no hypotheses in it

---

**This is the easiest reading of the second half of the course and the most important.** Strang's §6.4 is four pages and one theorem; §6.5 is the five tests. **Neither requires anything you do not already have**, and both are worth reading twice — once for the statements, once for where symmetry is used.

**Read them in the week they are set.** Week 11's SVD is Week 10's theorem applied to $A^\mathsf{T}A$, and a student who has not internalised the spectral theorem will experience the SVD as a second, harder mystery instead of a corollary.

| Chapter | Read? | Why |
|---|---|---|
| **6.4 Symmetric Matrices** | **All of it, twice** | L30 entire |
| **6.5 Positive Definite Matrices** | **All of it** | L31 entire, and L32 §2–§3 |
| 6.3 revisited | **Skim** | Strang's applications of diagonalisation; the symmetric case is where they behave |
| **§11.1 / the Cholesky remarks** | **Read** | L32 §2. Some editions put Cholesky in the numerical chapter |
| **Axler Ch. 7.A** | **Read if you read 6.A last week** | Self-adjoint operators — the spectral theorem without coordinates |
| **Trefethen & Bau, Lectures 23, 24, 26** | **Read 23** | Cholesky; then the symmetric eigenvalue problem |
| **Boyd & Vandenberghe, *Convex Optimization*, App. A** | Skim | Where "positive definite" earns its keep outside this course |
| **Goodfellow §4.3, §8.2** | Skim | The Hessian, condition numbers and why gradient descent is slow on an elongated bowl |

---

## §6.4 — the questions to hold

1. **Strang states the spectral theorem as three claims** (real eigenvalues, orthogonal eigenvectors, always diagonalisable). **Find all three and mark them separately.** They have three different proofs and the third is the one textbooks tend to skip.
2. **The reality proof uses complex conjugates.** Find the step where $A^\mathsf{T} = A$ is used. **Delete it and see the proof fail** — that is the exercise, not reading the proof.
3. **The orthogonality proof is two lines.** Where does symmetry enter? *(L30 §3: the middle equality.)*
4. **Does he prove the repeated-eigenvalue case, or assert it?** Many books assert it. **If he asserts it, note that** — it is the only genuinely hard part of the theorem, and L30 §6 gives the reason without the full proof either. *(The honest full argument is induction on $n$, or Schur's theorem; Axler 7.A does it properly.)*
5. **$A = \sum\lambda_kq_kq_k^\mathsf{T}$.** Find this. **It is the sentence to remember from the whole week**, and it makes Week 8's projections a special case.
6. **Does he state the converse?** *(Orthonormal eigenbasis with real eigenvalues $\Rightarrow$ symmetric — L30 §7. It is one line and it makes the theorem a characterisation.)*
7. **Complex matrices: Hermitian, $\bar A^\mathsf{T} = A$.** He will mention it. **Read the mention and move on** — every theorem of this week holds verbatim with conjugate-transpose in place of transpose, and nothing else in MATH 241 needs it.

---

## §6.5 — the questions to hold

8. **Count his tests.** Different editions give four or five. **Match them against L31 §3's table** and note any he leaves out — the $A = R^\mathsf{T}R$ test is the one most often omitted, and it is the one Cholesky computes.
9. **"Leading" principal minors.** Find where he says *leading* and ask why. **Then construct a matrix showing that dropping the word breaks the test.** *(PS 10 Q2(d). It takes one attempt.)*
10. **Completing the square.** He does this and he connects it to elimination. **Find the connection explicitly** — if it is only implied, write it out: the multipliers in $L$ *are* the substitutions in the completed squares. *(L31 §5.)*
11. **The energy $x^\mathsf{T}Ax$.** He calls it energy and means it physically. **Find one sentence of his that is about the physics rather than the algebra**, and decide whether it helped you.
12. **Ellipses.** He draws $x^\mathsf{T}Ax = 1$. **Check that his axis lengths are $1/\sqrt{\lambda}$ and not $\sqrt\lambda$** — the direction of that square root is the single most common slip on this material, and getting it wrong makes the well-conditioned matrix look badly conditioned.
13. **Does he state $\operatorname{cond}_2 = \lambda_\max/\lambda_\min$ for symmetric matrices?** If so, note that it is **false in general** — Week 11 is the general statement.

---

## Where Axler Earns His Place, Again

**Chapter 7.A does the spectral theorem for *operators*, not matrices**, and the difference is instructive.

**A matrix is symmetric or not. An operator is self-adjoint or not, and the definition involves the inner product:** $\langle Tv, w\rangle = \langle v, Tw\rangle$ for all $v, w$.

> **Why that is better.** "Symmetric" is a statement about a matrix, and a matrix depends on a basis
> (Week 4's L15). **A matrix that is symmetric in one basis need not be symmetric in another** — try
> it, with a non-orthonormal change of basis. **Self-adjointness is basis-free**, and the two notions
> coincide exactly when the basis is orthonormal.
>
> **So Week 10's theorem is quietly about orthonormal bases twice over**: once in its conclusion, and
> once in the hypothesis that "symmetric" means anything basis-independent at all. **Axler makes that
> visible and Strang does not.**

**Read 7.A if you read 6.A last week.** If you did not, skip it — Strang's version is sufficient for everything this course does, and Week 11 is the priority.

---

## What Belongs on the Final's Sheet

**The final is comprehensive** (Dec 15, 09:00–11:30). Six lines from this week:

1. $A = A^\mathsf{T} \Rightarrow A = Q\Lambda Q^\mathsf{T}$, $Q^{-1} = Q^\mathsf{T}$, $\Lambda$ real. **No hypotheses.**
2. $A = \sum\lambda_kq_kq_k^\mathsf{T}$.
3. **The five tests**, in a row: form, eigenvalues, pivots, **leading** minors, $R^\mathsf{T}R$.
4. $A = LDL^\mathsf{T}$ and $x^\mathsf{T}Ax = \sum d_ky_k^2$, $y = L^\mathsf{T}x$.
5. $A^\mathsf{T}A$ symmetric PSD always; PD iff independent columns.
6. $\lambda_\min \le x^\mathsf{T}Ax/x^\mathsf{T}x \le \lambda_\max$; $\operatorname{cond}_2 = \lambda_\max/\lambda_\min$ **(symmetric only)**.

**Do not write out Cholesky.** You can reconstruct it from $LDL^\mathsf{T}$ in one line, and the sheet space is better spent on Week 11.

---

## The Habit for This Week

**Ask what the hypothesis is buying.**

**Every theorem in Weeks 6–9 came with a caveat**, and Week 10 is the first week with none. That is worth noticing rather than enjoying:

| Week | Theorem | Its caveat |
|---|---|---|
| 6 | eigenvalues exist | may be complex |
| 7 | $A = S\Lambda S^{-1}$ | **only if enough eigenvectors**, and $S$ may be near-singular |
| 8 | $A = QR$ | only if independent columns |
| 9 | $\hat x = (A^\mathsf{T}A)^{-1}A^\mathsf{T}b$ | only if independent columns, **and don't compute it that way** |
| **10** | $A = Q\Lambda Q^\mathsf{T}$ | **none — but only for symmetric $A$** |

**The caveat did not disappear; it moved into the hypothesis.** Week 10 buys an unconditional conclusion by restricting the class of matrices. **Week 11 is the other trade**: keep every matrix and give up on using one basis at both ends.

**Ask, of every theorem from here on: what did I give up to get the *always*?**

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| **Strang, MIT 18.06, Lectures 25–28** | Symmetric matrices, positive definite matrices, similar matrices |
| **Trefethen & Bau, Lecture 23** | Cholesky in three pages, including why no pivoting |
| **Axler Ch. 7** | The spectral theorem for operators, done properly |
| **Horn & Johnson, *Matrix Analysis*, Ch. 4** | Everything about Hermitian matrices, including Weyl's inequality with proof |
| **Boyd & Vandenberghe, App. A** | Positive definiteness as the foundation of convex optimisation |
| **Week 11** | The SVD — this week's theorem applied to $A^\mathsf{T}A$, and the last factorisation of the course |

---

*MATH 241 · Week 10 · Reading Guide · © CSE Department*
