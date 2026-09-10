# MATH 241 · Quiz 11
## Administered: Monday, Week 11 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 10** — symmetric matrices, the spectral theorem, and positive definiteness.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **This is the last quiz of the term.** There is no Quiz 12. **Q7 is today's lecture** — L33
> builds the SVD from the answer.

---

**Q1.** State the spectral theorem. **Name the three separate claims** it makes.

&nbsp;

&nbsp;

---

**Q2.** $A$ is symmetric, $Ax = \lambda x$, $Ay = \mu y$, $\lambda \ne \mu$. **Prove $x \perp y$.** Point at the step that uses symmetry.

&nbsp;

&nbsp;

---

**Q3.** Is $\begin{bmatrix}2&3\\3&2\end{bmatrix}$ positive definite? **Answer with an explicit vector**, not only with eigenvalues.

&nbsp;

&nbsp;

---

**Q4.** Write $x_1^2 + 4x_1x_2 + 5x_2^2$ as $x^\mathsf{T}Mx$, then as a sum of squares with the pivots as coefficients. **Is it positive definite?**

&nbsp;

&nbsp;

---

**Q5.** A colleague checks positive definiteness by confirming every diagonal entry is positive and $\det A > 0$. **In which dimension does that work, and in which does it fail?** Give the failing example.

&nbsp;

&nbsp;

---

**Q6.** Perturb a matrix by $10^{-10}$ in one entry. **How far can its eigenvalues move** if it is symmetric? If it is the $10\times10$ shift matrix of L32 §6?

&nbsp;

&nbsp;

---

**Q7.** $A$ is any $m\times n$ matrix. **Why is $A^\mathsf{T}A$ symmetric positive semidefinite**, and exactly when is it positive definite?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **$A = A^\mathsf{T} \Longrightarrow A = Q\Lambda Q^\mathsf{T}$** with $Q$ orthogonal and $\Lambda$ real diagonal. Three claims:

1. **The eigenvalues are real.**
2. **Eigenvectors for distinct eigenvalues are perpendicular.**
3. **There are always enough of them** — a repeated eigenvalue is never defective.

*(L30 §1.)*

---

**Q2.**

$$\lambda(x\cdot y) = (Ax)^\mathsf{T}y = x^\mathsf{T}A^\mathsf{T}y \overset{\text{sym}}{=} x^\mathsf{T}Ay = \mu(x\cdot y),$$

so $(\lambda - \mu)(x\cdot y) = 0$, and $\lambda \ne \mu$ forces $x\cdot y = 0$. **Symmetry is the third equality**, $A^\mathsf{T} = A$, used once. *(L30 §3.)*

---

**Q3.** **No.** $x = (1,-1)$ gives

$$x^\mathsf{T}Ax = 2 - 3 - 3 + 2 = -2 < 0.$$

*(Eigenvalues $5$ and $-1$; pivots $2$ and $-\tfrac52$. **Both diagonal entries are positive and it is still indefinite** — L31 §4's trap. The eigenvector for the negative eigenvalue is always the place to look for $x$.)*

---

**Q4.** $M = \begin{bmatrix}1&2\\2&5\end{bmatrix}$ — **off-diagonal entries are half the cross coefficient.** Pivots $1$ and $5 - 4 = 1$, multiplier $2$:

$$x_1^2 + 4x_1x_2 + 5x_2^2 = (x_1 + 2x_2)^2 + x_2^2.$$

**Positive definite**: a sum of squares with positive coefficients, zero only when $x_2 = 0$ and then $x_1 = 0$. *(L31 §5.)*

---

**Q5.** **It works in $2\times2$**, where $a_{11}$ and $\det$ are the only two leading minors, so the rule *is* test 4. **It fails from $3\times3$ on:**

$$\begin{bmatrix}1&2&2\\2&1&2\\2&2&1\end{bmatrix}: \quad \text{diagonal } 1, 1, 1;\ \det = 5;\ \text{leading minors } 1, \mathbf{-3}, 5;\ \text{eigenvalues } 5, -1, -1.$$

**Test 4 needs every leading minor.** *(PS 10 Q2(d), REC 10 §3(d).)*

---

**Q6.** **Symmetric: by at most $10^{-10}$** — Weyl's inequality, and L32 §6 measured a worst ratio below $1$. **The shift matrix: to magnitude $0.1$**, because $C^{10} = \varepsilon I$ gives $\lvert\lambda\rvert = \varepsilon^{1/10}$. **A billion-fold amplification.** *(L32 §6.)*

---

**Q7.** **Symmetric:** $(A^\mathsf{T}A)^\mathsf{T} = A^\mathsf{T}A^{\mathsf{T}\mathsf{T}} = A^\mathsf{T}A$. **Positive semidefinite:**

$$x^\mathsf{T}(A^\mathsf{T}A)x = (Ax)^\mathsf{T}(Ax) = \lVert Ax\rVert^2 \ge 0.$$

**Positive definite exactly when $Ax = 0$ only for $x = 0$** — independent columns. *(L31 §7; PS 2 Q5(c).)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L30 §1–§3 |
| Q3, Q5 | L31 §3–§4. **Both are on the final** |
| Q4 | L31 §5 — halve the cross coefficient |
| Q6 | L32 §6 |
| **Q7** | **L31 §7, before the lecture starts.** L33 §2 applies the spectral theorem to $A^\mathsf{T}A$ in its first five minutes, and this is the reason it is allowed to |

> **This is the last quiz.** The eleven answer keys together cover Weeks 0–10, and **re-reading them
> is the fastest useful revision for the final** — the Week 12 Revision Guide says so too.

---

*MATH 241 · Week 11 · Quiz 11 · covers Week 10 · ungraded*
