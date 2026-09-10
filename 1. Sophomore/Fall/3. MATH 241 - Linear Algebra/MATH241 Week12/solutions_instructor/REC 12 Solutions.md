# MATH 241 · Recitation 12 — TA Notes and Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Thursday Dec 11, completion period, 15:00–15:50, SSB 108.** The final is Monday Dec 15, 09:00.

**Shape.** §0 at home. §1 twenty minutes, §2 ten, §3 ten, §4 the rest. **§1 is the session.**

> **Do not discuss the final paper.** Not its topics, not its weighting beyond what the Revision Guide
> publishes, not whether "this kind of question" is on it. **If asked, the answer is: the Revision
> Guide says what is examinable, and this session practises the moves.** Instructors who have seen the
> paper should not run this session.

**Every answer to §1 is a Week 10 figure** — computed exactly by `MATH241 Week10/resources/symmetric.py` — and the Frobenius-norm check is done here.

---

## §1 — One Matrix, Twelve Weeks (20 min)

$$A = \begin{bmatrix}5&0&-2\\0&3&-2\\-2&-2&4\end{bmatrix}$$

**(a)** Multipliers $\ell_{21} = 0$, $\ell_{31} = -\tfrac25$, $\ell_{32} = -\tfrac23$. **Pivots $5$, $3$, $\tfrac{28}{15}$.**

$$L = \begin{bmatrix}1&0&0\\0&1&0\\-\tfrac25&-\tfrac23&1\end{bmatrix}, \qquad D = \operatorname{diag}\left(5,\ 3,\ \tfrac{28}{15}\right), \qquad A = LDL^\mathsf{T}.$$

**(b)** $\det A = 5\cdot3\cdot\tfrac{28}{15} = 28$.

**(c)** **Rank $3$** — three nonzero pivots. $\mathbf{C}(A) = \mathbf{C}(A^\mathsf{T}) = \mathbb{R}^3$ (standard basis will do), $\mathbf{N}(A) = \mathbf{N}(A^\mathsf{T}) = \{0\}$ (empty basis). **Short because $A$ is invertible**, and the four-subspace picture of an invertible matrix is two full spaces and two zeros.

**(d)** $A(1,2,2) = (1,2,2)$; $A(2,1,-2) = (14, 7, -14)$; $A(2,-2,1) = (8,-8,4)$. **Eigenvalues $1$, $7$, $4$.** Sum $12 = 5 + 3 + 4$ ✓; product $28 = \det A$ ✓.

**(e)** $A^{10}$ has eigenvalues $1$, $7^{10} = 282{,}475{,}249$, $4^{10} = 1{,}048{,}576$. **$\operatorname{trace}A^{10} = 1 + 282{,}475{,}249 + 1{,}048{,}576 = 283{,}523{,}826.$**

**(f)** $Q = \tfrac13\begin{bmatrix}1&2&2\\2&1&-2\\2&-2&1\end{bmatrix}$ (columns in the order of (d)). **$Q^{-1} = Q^\mathsf{T}$, $\operatorname{cond}(Q) = 1$.**

**(g)** Any three of: **pivots** $5, 3, \tfrac{28}{15} > 0$ (from (a)); **leading minors** $5$, $15$, $28 > 0$ (the running products of the pivots); **eigenvalues** $1, 7, 4 > 0$ (from (d)); **$A = R^\mathsf{T}R$** exists with $R = \sqrt D L^\mathsf{T}$. **Positive definite.**

**(h)** $A$ is symmetric positive definite, so **$U = V = Q$** (reordered so $\sigma_1 \ge \sigma_2 \ge \sigma_3$) and $\Sigma = \operatorname{diag}(7, 4, 1)$. **Short because the SVD of a symmetric positive semidefinite matrix *is* its spectral decomposition** (Week 10's L32 §7). *If an eigenvalue were negative:* its singular value is $\lvert\lambda\rvert$ and the sign moves into $U$ — flip the corresponding column of $U$ only.

**(i)** $\lVert A\rVert_2 = 7$. $\lVert A\rVert_F^2 = 1 + 49 + 16 = 66$; **from the entries**: $25 + 0 + 4 + 0 + 9 + 4 + 4 + 4 + 16 = 66$ ✓. $\operatorname{cond}_2(A) = 7/1 = 7$.

**(j)** **The direction $\tfrac13(2,1,-2)$, eigenvalue $7$, explains $\tfrac{7}{12} \approx 58.3\%$** of the total variance $1 + 7 + 4 = 12$.

> **What to watch for.** Pairs that do (d) by the characteristic polynomial instead of multiplying the
> given vectors; pairs that do (e) by computing $A^2$. **Stop both** — the paper rewards using what a
> question hands you.

---

## §2 — Which Tool, Which Week (10 min)

| | Method | Week | What goes wrong with the obvious alternative |
|---|---|---|---|
| **(a)** | factor once ($LU$), then $10{,}000$ triangular solves | 1 | recomputing elimination each time: $n^3/3$ per solve instead of $n^2$ |
| **(b)** | Householder $QR$ (or SVD) on the $10^6\times3$ matrix | 9 | normal equations square $\operatorname{cond}$; the monomial basis makes it worse |
| **(c)** | leading minors or pivots, with the parameter carried | 10 | eigenvalues in floating point cannot locate the exact boundary |
| **(d)** | the gap in the singular values | 11 | counting nonzero pivots says full rank on any noisy data |
| **(e)** | $S\Lambda^{50}S^{-1}$, or just the steady state plus $\lambda_2^{50}$ | 7 | fifty matrix products, or repeated squaring without insight |
| **(f)** | truncated SVD, $k = 20$ | 11 | anything else is worse, by Eckart–Young |
| **(g)** | PCA = SVD of the centred data | 11–12 | forming the covariance matrix loses the small variances |
| **(h)** | damped power iteration, never forming $G$ | 6–7, 12 | elimination: $3\times10^{26}$ operations; no damping: no unique answer |

---

## §3 — Seven Lessons, Seven Numbers (10 min)

| # | Replacement | A number from the notes |
|---|---|---|
| 1 | elimination | Week 5: Cramer's rule is $n + 1$ determinants — **$(n+1)!$ terms** by cofactors |
| 2 | elimination; never form $A^{-1}$ | Week 5: the adjugate needs $n^2$ cofactors |
| 3 | product of the pivots | **Week 5: $751\times$ slower than elimination at $n = 8$**, measured |
| 4 | iterate on the matrix (QR, Jacobi) | Week 6's L20: polynomial roots are badly conditioned — tiny coefficient changes move roots enormously |
| 5 | Householder $QR$, or the SVD | **Week 9: Läuchli's $A^\mathsf{T}A$ exactly singular at $\varepsilon = 10^{-8}$** |
| 6 | symmetry, when you have it | **Week 10: $10^{-10}$ in one entry moved every eigenvalue to $0.1$** — a billion-fold amplification |
| 7 | the singular-value gap | **Week 11: six nonzero pivots, $\sigma_2/\sigma_3 = 8\times10^{10}$** |

**Accept any correct number with a correct source.** The exercise is recall-with-provenance, which is exactly what a "why" part of an exam question needs.

---

## §4 — Clinic

**Collect the "least wanted" topics on the board first, and tally them.** Work the most common two or three **on fresh numbers** — never on anything that might resemble the paper.

**Likely requests and where to send them:**

| Topic | Fastest route |
|---|---|
| The SVD by hand | REC 11 §1 — the four steps — then PS 11 Q1 |
| Four subspaces | Week 3's REC 3, then L34 §1's table |
| Positive definite with a parameter | L31 §3's table, then PS 10 Q2(a) |
| Least squares set-up | L27 §3: **unknowns in $\hat x$, data in $A$** |
| "Everything in Weeks 6–7" | Quiz 7 and Quiz 8 keys, then L21 §2 |

> **Flag after the session:** nothing to flag — there is no next session. **If a student is clearly
> in difficulty, send them to the Help Desk today**, not to an email on Sunday night.

---

*MATH 241 · Week 12 · REC 12 Solutions · © CSE Department*
