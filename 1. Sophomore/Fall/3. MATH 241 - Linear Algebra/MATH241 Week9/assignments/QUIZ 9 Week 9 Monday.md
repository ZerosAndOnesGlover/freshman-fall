# MATH 241 · Quiz 9
## Administered: Monday, Week 9 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 8** — orthogonality, projections, and Gram–Schmidt.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **Midterm 2 is a week on Wednesday**, covering **Weeks 6–9**. Treat this as a diagnostic.

---

**Q1.** State the one-line proof that $\mathbf{N}(A) \perp \mathbf{C}(A^\mathsf{T})$.

&nbsp;

&nbsp;

---

**Q2.** Two subspaces meet at right angles. Does that make them orthogonal subspaces? Give the standard counterexample.

&nbsp;

&nbsp;

---

**Q3.** Project $b = (4,0,0)$ onto the line through $a = (1,1,0)$. Give $p$ and $e$, and check.

&nbsp;

&nbsp;

---

**Q4.** Write the projection matrix onto $\mathbf{C}(A)$. **Why must $A$ have independent columns**, and which week proved the thing you need?

&nbsp;

&nbsp;

---

**Q5.** What are the eigenvalues of a projection matrix, and what is $\operatorname{trace}P$?

&nbsp;

&nbsp;

---

**Q6.** $Q$ has orthonormal columns. Give three things that become free.

&nbsp;

&nbsp;

---

**Q7.** Why do Weeks 9, 10 and 11 all insist on orthonormal bases? Answer with a number.

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** $Ax = 0$ says **every entry of $Ax$ is zero**, and entry $i$ of $Ax$ is (row $i$)$\,\cdot\,x$. So $x$ is orthogonal to every row, hence to every combination of rows, hence to the whole row space. $\square$ *(L24 §4.)*

---

**Q2.** **No.** The floor and a wall of a room meet at right angles and are **not** orthogonal subspaces — they **share the line where they meet**, and a nonzero vector along that line would have to be orthogonal to itself.

**Orthogonal subspaces intersect only in $\{0\}$.** *(L24 §3.)*

---

**Q3.** $\hat x = \dfrac{a^\mathsf{T}b}{a^\mathsf{T}a} = \dfrac{4}{2} = 2$, so

$$p = 2(1,1,0) = (2,2,0), \qquad e = b - p = (2,-2,0)$$

**Check:** $a^\mathsf{T}e = 2 - 2 + 0 = 0$ ✓

---

**Q4.** $P = A(A^\mathsf{T}A)^{-1}A^\mathsf{T}$.

**Independent columns are needed for $A^\mathsf{T}A$ to be invertible**, which is **PS 2 Q5(c) in Week 2**: $\mathbf{N}(A^\mathsf{T}A) = \mathbf{N}(A) = \{0\}$, and a square matrix with trivial null space is invertible.

---

**Q5.** **$\lambda = 1$ on $W$** (multiplicity $\dim W$) and **$\lambda = 0$ on $W^\perp$** (multiplicity $n - \dim W$) — $P$ fixes what is already in $W$ and kills what is perpendicular.

**So $\operatorname{trace}P = \sum\lambda_i = \dim W$.** *(L25 §5, using Week 6's L20 §2.)*

---

**Q6.** Any three of:

- **$Q^{-1} = Q^\mathsf{T}$** — the inverse is a transpose, not an elimination.
- **Coordinates are dot products:** $c_j = q_j^\mathsf{T}b$, each computed independently.
- **$P = QQ^\mathsf{T}$** — the projection formula with $(A^\mathsf{T}A)^{-1}$ deleted.
- $\lVert Qx\rVert = \lVert x\rVert$ — lengths and angles preserved.

---

**Q7.** **$\operatorname{cond}(Q) = 1$** — the smallest possible, so multiplying by $Q$ **cannot amplify a rounding error at all.**

**Week 7's L22 §4 was the complaint:** near a defective matrix the eigenvector basis has $\operatorname{cond}(S) = 1.3\times10^8$ at $\varepsilon = 10^{-8}$, and $A = S\Lambda S^{-1}$ becomes numerically worthless even though it exists. **Orthonormality is conditioning, not elegance.** *(L24 §5, L26 §2.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L24 §3–§4 |
| **Q3, Q4** | **L25 §2–§3.** **This week is these two questions with data attached** |
| Q5 | L25 §5 |
| Q6 | L26 §1 |
| **Q7** | **L24 §5.** It is why the rest of the course looks as it does — **and it is a likely exam question** |

**Q3 and Q4 are today's lecture.** Least squares is projection; a student who cannot project cannot start Week 9, and Week 9 is on the midterm.

---

*MATH 241 · Week 9 · Quiz 9 · covers Week 8 · ungraded*
