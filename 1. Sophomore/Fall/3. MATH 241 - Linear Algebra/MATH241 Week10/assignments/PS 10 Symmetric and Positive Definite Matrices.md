# MATH 241 · Problem Set 10
## Symmetric Matrices, the Spectral Theorem, and Positive Definiteness

---

**Released:** Week 10, Wednesday · **Due:** Week 11, **Friday 17:00**
**Total: 100 points** · Submit one PDF, `PS10_{LastName}_{StudentID}.pdf`

> **Exact arithmetic in Q1–Q3.** Every matrix on this paper is built so that the answers are
> rational or small integers. **If a fraction turns ugly, you have made an arithmetic error**, and
> the trace and determinant checks in Q1(b) will catch it in ten seconds.
>
> **Q4 is run on a computer**, using `resources/symmetric.py` from this week's folder. Quote its
> output where you rely on it, and state your Python version.
>
> **Q5 is proof.** No arithmetic is required and none will earn marks.
>
> **Recitation 10 is the Thursday before this is due**, and it is where Midterm 2 is returned and
> discussed. **Bring this paper's Q2 if it is giving you trouble** — the five tests are the single
> most exam-likely item of the week.
>
> **Collaboration on approaches is fine; the write-up must be yours.**

---

### Q1: The Spectral Theorem, by Hand (24 points)

Throughout, let

$$A = \begin{bmatrix}7&2&2\\ 2&8&0\\ 2&0&6\end{bmatrix}.$$

**(a) [4]** Verify $A = A^\mathsf{T}$. Write down $\operatorname{trace}A$ and $\det A$ **before** doing anything else, and say what each will be used to check.

**(b) [6]** Show that

$$\det(A - \lambda I) = -\left(\lambda^3 - 21\lambda^2 + 138\lambda - 280\right)$$

*(L20 §1's convention: the leading coefficient is $(-1)^n$)* and that its roots are $\lambda = 10, 7, 4$.

> **Check both invariants from (a) before continuing.** The middle coefficient $138$ is the sum of
> the three $2\times2$ principal minors — **the fact L20 §2 mentions and declines to make you
> memorise.** Verify it here anyway; it is a third free check, and it catches errors the trace and
> determinant miss.

**(c) [6]** Find an eigenvector for each eigenvalue. **They are integer vectors with entries in $\{-2,-1,1,2\}$.** Verify all three pairwise dot products are zero, and say which theorem guarantees this **without** any computation.

**(d) [4]** Build $Q$ and verify $Q^\mathsf{T}Q = I$ **exactly**, in fractions. Then state $Q^{-1}$ without inverting anything, and say what $\operatorname{cond}(Q)$ is.

**(e) [4]** Write $A = 10P_1 + 7P_2 + 4P_3$ with $P_k = q_kq_k^\mathsf{T}$. **Compute $P_2$ explicitly**, verify $P_2^2 = P_2$ and $\operatorname{trace}P_2 = 1$, and say what that trace is counting.

---

### Q2: Five Tests (22 points)

**(a) [10]** For

$$B(t) = \begin{bmatrix}3&1&t\\ 1&3&1\\ t&1&3\end{bmatrix},$$

determine **exactly** the values of $t$ for which $B(t)$ is positive definite. Give the three leading principal minors with $t$ carried through, and state the interval and its two endpoints as exact numbers.

**(b) [6]** At **both** endpoints, and at $t = 0$ and $t = 4$, compute the **pivots** and confirm that the sign pattern of the pivots matches the sign pattern of the eigenvalues. *(You may get the eigenvalues from `symmetric.py`.)* **Name the law you have just verified.**

**(c) [3]** At each endpoint, $B(t)$ is positive **semi**definite. **Exhibit a nonzero $x$ with $x^\mathsf{T}B(t)x = 0$** at $t = 3$, and say what that $x$ is in the vocabulary of Weeks 2 and 6.

**(d) [3]** A colleague proposes: *"all diagonal entries positive and $\det > 0$, therefore positive definite."* **Give a $3\times3$ symmetric counterexample** and say precisely which of the five tests they have half-remembered.

---

### Q3: Quadratic Forms (16 points)

**(a) [8]** Let

$$f(x) = 2x_1^2 + 2x_2^2 + 3x_3^2 + 2x_1x_2 - 2x_2x_3.$$

Write $f(x) = x^\mathsf{T}Mx$ with $M$ symmetric. Compute $M = LDL^\mathsf{T}$ exactly, and hence write $f$ as a **sum of three squares with the pivots as coefficients**. Verify your identity at $x = (1,1,1)$ and at $x = (2,-1,3)$.

**(b) [4]** Is $f$ positive definite? Answer from your sum of squares alone, in one sentence, **without eigenvalues**.

**(c) [4]** Sketch $x^\mathsf{T}Nx = 1$ for $N = \begin{bmatrix}3&1\\1&3\end{bmatrix}$. Give the two axis **directions**, the two semi-axis **lengths**, the aspect ratio, and $\operatorname{cond}_2(N)$. **State the relationship between the last two.**

---

### Q4: On the Machine (20 points)

Run `resources/symmetric.py`. Quote output where you rely on it.

**(a) [6]** Reproduce §5's table for $A(b)$, then **extend it to $b = 2.1333$ and $b = 2.1334$** — either side of $32/15$ but closer than the notes go.

- Report the smallest eigenvalue at each.
- **At which of the two would you be willing to declare the matrix positive definite from the eigenvalue alone**, and why is the exact determinant a better instrument here? *(One paragraph. Week 0's L03 §7 is the frame.)*

**(b) [6]** Reproduce §10's Hilbert table and **extend it to $n = 14$**.

- Report $\lambda_\max$, $\lambda_\min$, $\operatorname{cond}_2$ and the exact $\operatorname{cond}_\infty$.
- **$\lambda_\min$ at $n = 14$ should not be believed.** Say why, in the terms L32 §5 uses about $n = 12$, and say what you *can* legitimately conclude from the number.

**(c) [8]** Reproduce §12's two experiments, then **run the symmetric one on the Hilbert matrix $H_8$ instead of $A$** at $\delta = 10^{-6}$.

- Report the largest eigenvalue movement.
- **$H_8$ has $\operatorname{cond}_2 = 1.5\times10^{10}$ and the eigenvalues still move by at most $\delta$.** Explain why there is no contradiction. *(The condition number of the **eigenvalue problem** and the condition number of the **linear system** are different things, and this is the question that separates them.)*

---

### Q5: Proofs (18 points)

**(a) [4]** Prove that a symmetric matrix with all eigenvalues equal to $c$ is exactly $cI$. Then give a **non-symmetric** matrix with all eigenvalues $c$ that is not $cI$, and name the Week 7 word for it.

**(b) [4]** $A$ is positive definite. Prove $A^{-1}$ is positive definite **two ways** — once via eigenvalues, once directly from the definition using the substitution $y = A^{-1}x$.

**(c) [4]** $A$ is symmetric positive definite and $C$ is any invertible matrix of the same size. **Prove $C^\mathsf{T}AC$ is positive definite.** Then say why this makes $A^\mathsf{T}A$'s positive definiteness (L31 §7) a special case.

**(d) [3]** $A$ is $m\times n$ with $m < n$. **Prove $A^\mathsf{T}A$ is never positive definite**, using dimensions only — no example.

**(e) [3]** Prove the Rayleigh bound $\lambda_\min \le \dfrac{x^\mathsf{T}Ax}{x^\mathsf{T}x} \le \lambda_\max$ for symmetric $A$, by expanding $x$ in the orthonormal eigenbasis. **Say where symmetry is used**, and give a $2\times2$ non-symmetric matrix for which the bound fails.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | The spectral theorem, by hand | 24 |
| 2 | Five tests | 22 |
| 3 | Quadratic forms | 16 |
| 4 | On the machine | 20 |
| 5 | Proofs | 18 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*MATH 241 · Week 10 · PS 10 · © CSE Department*
