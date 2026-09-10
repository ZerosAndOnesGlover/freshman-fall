# MATH 241 · Problem Set 8
## Orthogonality, Projections, and Gram–Schmidt

---

**Released:** Week 8, Wednesday · **Due:** Week 9, **Friday 17:00**
**Total: 100 points** · Submit one PDF, `PS8_{LastName}_{StudentID}.pdf`

> **Exact arithmetic** except where normalisation forces a surd; leave surds as surds.
>
> **Every projection must be checked** by verifying that the error is orthogonal to the subspace.
> One dot product per basis vector, and it certifies the whole computation.
>
> **Recitation 8 is the Thursday before this is due**, 15:00–15:50, SSB 108.

---

### Q1: Orthogonality (20 points)

**(a) [4]** Find the angle between $(2,1,2)$ and $(1,2,2)$ in $\mathbb{R}^3$. Then between $(1,1,1,1)$ and $(1,-1,1,-1)$ in $\mathbb{R}^4$.

> **Compute the dot product first in both cases.** One of them answers itself.

**(b) [4]** Prove that $x \perp y$ **iff** $\lVert x + y\rVert^2 = \lVert x\rVert^2 + \lVert y\rVert^2$. **Both directions**, and say which term does the work.

**(c) [4]** Prove that if two subspaces are orthogonal then they meet only at $\mathbf{0}$.

Then: **give two subspaces of $\mathbb{R}^3$ that meet only at $\mathbf{0}$ and are *not* orthogonal**, and say why the floor and a wall of a room are not an example of orthogonal subspaces.

**(d) [8]** For

$$A = \begin{bmatrix}1&2&0\\ 0&0&1\\ 1&2&1\end{bmatrix}$$

find a basis for each of the four fundamental subspaces and **verify every orthogonality relation by direct computation.** State how many dot products that is.

---

### Q2: Projections (22 points)

**(a) [5]** Project $b = (4,1,1)$ onto the line through $a = (1,1,1)$. Give $\hat x$, $p$ and $e$, and check $e \perp a$.

Then write the $3\times3$ projection matrix onto that line and **verify $P^2 = P$ and $\operatorname{trace}P = 1$.**

**(b) [9]** Let

$$A = \begin{bmatrix}1&1\\ 0&1\\ 1&0\end{bmatrix}.$$

- Compute $A^\mathsf{T}A$ and say why it is invertible, **citing the week it was proved.**
- Compute $P = A(A^\mathsf{T}A)^{-1}A^\mathsf{T}$.
- Project $b = (3,0,0)$. Give $p$ and $e$.
- **Verify $A^\mathsf{T}e = 0$** and say which of the four subspaces $e$ lies in.

**(c) [4]** Verify $P^2 = P$ and $P^\mathsf{T} = P$ for your matrix, and **give the geometric reason for each** in one sentence apiece.

**(d) [4]** $\operatorname{trace}P = 2$ for the $P$ in (b). **Prove in general that $\operatorname{trace}P = \dim W$**, using the eigenvalues of a projection and Week 6's L20 §2.

---

### Q3: Gram–Schmidt (20 points)

**(a) [8]** Apply Gram–Schmidt to

$$a_1 = (1,1,1), \qquad a_2 = (1,1,0), \qquad a_3 = (1,0,0)$$

**Work exactly.** Give the orthogonal set, clear any fractions, and **verify all three pairwise dot products are zero.**

**(b) [4]** Normalise your answer to an orthonormal set $q_1, q_2, q_3$ and write the matrix $Q$. **Verify $Q^\mathsf{T}Q = I$.**

**(c) [4]** **Predict, before computing:** what does Gram–Schmidt give for $(1,0,0)$, $(1,1,0)$, $(1,1,1)$ — the same three vectors in the opposite order? Then confirm.

**Say in one sentence what this shows about Gram–Schmidt.**

**(d) [4]** Orthogonalise $1$, $x$, $x^2$ on $[-1,1]$ using $\langle f,g\rangle = \int_{-1}^{1}f(x)g(x)\,dx$ in place of the dot product.

**You should get $1$, $x$, $x^2 - \tfrac13$.** *(These are the Legendre polynomials, and Week 12's Fourier construction is the same procedure with a different family.)*

---

### Q4: $A = QR$ and Orthonormal Bases (20 points)

**(a) [6]** Find $Q$ and $R$ for

$$A = \begin{bmatrix}1&2\\ 1&0\\ 0&1\end{bmatrix}$$

**Verify $QR = A$ and $Q^\mathsf{T}Q = I$.** Leave surds as surds.

**(b) [4]** **Why is $R$ upper triangular?** Answer from the Gram–Schmidt construction, not by inspection.

**What are its diagonal entries**, and why is $R$ invertible whenever $A$ has independent columns?

**(c) [5]** With $Q$'s columns an orthonormal basis for a subspace $W$:

- Show $P = QQ^\mathsf{T}$, starting from L25's formula.
- Show $Pb = \sum_j (q_j^\mathsf{T}b)\,q_j$, and say in words what that formula instructs you to do.

**(d) [5]** Substitute $A = QR$ into the normal equations $A^\mathsf{T}A\hat x = A^\mathsf{T}b$ and simplify as far as possible.

**You should reach $R\hat x = Q^\mathsf{T}b$.** **Say what has disappeared, and why that matters numerically.** *(This is Week 9's algorithm.)*

---

### Q5: Structure (18 points)

**(a) [4]** Prove $\mathbf{N}(A) \perp \mathbf{C}(A^\mathsf{T})$ in one line, from $Ax = 0$.

Then explain why this is **stronger** than the observation Week 3's L12 §7 made, and what extra the word *complement* asserts.

**(b) [4]** Week 3's L12 §5 proved: $Ax = b$ solvable $\Rightarrow y^\mathsf{T}b = 0$ for every $y \in \mathbf{N}(A^\mathsf{T})$.

**Prove the converse**, now that you have orthogonal complements. *(Two lines.)*

**(c) [4]** Prove that orthonormal vectors are linearly independent, **without using elimination or determinants.**

**(d) [6]** Prove that an orthogonal matrix preserves lengths: $\lVert Qx\rVert = \lVert x\rVert$.

Deduce $\operatorname{cond}(Q) = 1$, and **explain in two sentences why Weeks 9, 10 and 11 all insist on orthonormal bases** — referring to what went wrong in Week 7's L22 §4.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Orthogonality | 20 |
| 2 | Projections | 22 |
| 3 | Gram–Schmidt | 20 |
| 4 | $A = QR$ and orthonormal bases | 20 |
| 5 | Structure | 18 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*MATH 241 · Week 8 · PS 8 · © CSE Department*
