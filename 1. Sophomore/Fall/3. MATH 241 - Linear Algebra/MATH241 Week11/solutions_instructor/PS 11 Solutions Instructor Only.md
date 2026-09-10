# MATH 241 · Problem Set 11 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Exact in Q1–Q3 and Q5**; Q4 is floating point and says so. `resources/svd.py` reproduces the lecture figures; every Q4 figure below was produced by the modification the question describes, with the script's own random seeds unchanged, so a correct student run matches to every digit shown.

**What this paper is testing.** Q1 and Q2 are the mechanical core — the four steps, and the four subspaces — and are the most likely final-exam computations of the week. **Q4(a) is the best question on the paper**: a single thin diagonal line turns out to be **full rank**, and raises the whole picture from rank $7$ to rank $20$, which almost nobody predicts. **Q4(c) is the subtle one**: total least squares is *not* better than ordinary least squares when only $y$ is noisy, and the question is whether students notice.

**Common failure modes:** (1) Q1(b) computing $u$'s and $v$'s independently and ending with a sign mismatch, so that $U\Sigma V^\mathsf{T} \ne W$; (2) Q2(c) claiming $NN^+ = I$; (3) Q3(c) giving the same answer three times; (4) Q4(a) predicting the diagonal is rank $1$ "because it is a line"; (5) Q4(c) concluding that TLS is always better.

---

## Q1: The SVD by Hand, of a Wide Matrix (22 points)

### (a) [4]

$$WW^\mathsf{T} = \begin{bmatrix}4 + 64 + 400 & -28 + 152 + 200\\ -28 + 152 + 200 & 196 + 361 + 100\end{bmatrix} = \begin{bmatrix}468&324\\324&657\end{bmatrix}.$$

Trace $1125$, determinant $468\cdot657 - 324^2 = 307{,}476 - 104{,}976 = 202{,}500$. **$\lambda^2 - 1125\lambda + 202500 = (\lambda - 900)(\lambda - 225)$.**

$$\sigma_1 = 30, \qquad \sigma_2 = 15, \qquad \sigma_1^2 + \sigma_2^2 = 1125 = 4 + 64 + 400 + 196 + 361 + 100\ ✓$$

*Marking: 2 for $WW^\mathsf{T}$, 1 for the eigenvalues, 1 for the check. **Using $W^\mathsf{T}W$** ($3\times3$, eigenvalues $900, 225, 0$) **is correct and earns full marks here**, but costs the student (b)'s shortcut; note it.*

### (b) [6]

$WW^\mathsf{T} - 900I = \begin{bmatrix}-432&324\\324&-243\end{bmatrix}$, rows proportional to $(-4, 3)$, so

$$u_1 = \tfrac15(3,4), \qquad u_2 = \tfrac15(-4,3).$$

$$v_1 = \frac{W^\mathsf{T}u_1}{30} = \frac{1}{150}(-6 + 56,\ 24 + 76,\ 60 + 40) = \frac{1}{150}(50, 100, 100) = \tfrac13(1,2,2)$$
$$v_2 = \frac{W^\mathsf{T}u_2}{15} = \frac{1}{75}(8 + 42,\ -32 + 57,\ -80 + 30) = \frac{1}{75}(50, 25, -50) = \tfrac13(2,1,-2)$$

$v_1\cdot v_2 = \tfrac19(2 + 2 - 4) = 0$; $\lVert v_1\rVert^2 = \lVert v_2\rVert^2 = \tfrac99 = 1$ ✓.

*Marking: 2 for the $u$'s, 3 for the $v$'s via $W^\mathsf{T}u_k/\sigma_k$, 1 for orthonormality. **A student who finds $v$'s as eigenvectors of $W^\mathsf{T}W$ independently loses 1 unless the signs happen to match** — (d) will expose a mismatch, and the returned script should say where.*

### (c) [4]

$v_3 \perp v_1, v_2$: $(1,2,2)\times(2,1,-2) = (-6, 6, -3)$, so

$$v_3 = \tfrac13(2,-2,1), \qquad Wv_3 = \tfrac13(-4 - 16 + 20,\ 28 - 38 + 10) = (0, 0)\ ✓$$

**$v_3$ spans $\mathbf{N}(W)$.** *(Rank $2$ in $\mathbb{R}^3$: nullity $1$.)*

### (d) [4]

$$W = \underbrace{\tfrac15\begin{bmatrix}3&-4\\4&3\end{bmatrix}}_{U,\ 2\times2}\underbrace{\begin{bmatrix}30&0&0\\0&15&0\end{bmatrix}}_{\Sigma,\ 2\times3}\underbrace{\tfrac13\begin{bmatrix}1&2&2\\2&1&-2\\2&-2&1\end{bmatrix}}_{V^\mathsf{T},\ 3\times3}$$

$(1,3)$ entry: $\tfrac1{15}\bigl(3\cdot30\cdot2 + (-4)\cdot15\cdot(-2)\bigr) = \tfrac1{15}(180 + 120) = 20$ ✓.

*Marking: 2 for the three factors with sizes, 2 for the entry. **$\Sigma$ must be $2\times3$**; a $2\times2$ $\Sigma$ with a $2\times3$ $V^\mathsf{T}$ is the thin SVD mislabelled and loses 1.*

### (e) [4]

$$W_1 = 30\,u_1v_1^\mathsf{T} = \frac{30}{15}\begin{bmatrix}3\\4\end{bmatrix}\begin{bmatrix}1&2&2\end{bmatrix} = \begin{bmatrix}6&12&12\\8&16&16\end{bmatrix}.$$

**By Eckart–Young, without computing:** $\lVert W - W_1\rVert_2 = \sigma_2 = 15$ and $\lVert W - W_1\rVert_F = \sqrt{\sigma_2^2} = 15$ — equal, because only one singular value is discarded.

$$W - W_1 = \begin{bmatrix}-8&-4&8\\6&3&-6\end{bmatrix} = 15\,u_2v_2^\mathsf{T}, \qquad \lVert\cdot\rVert_F^2 = 64 + 16 + 64 + 36 + 9 + 36 = 225\ ✓$$

**Worth noting on scripts:** the relative error is $15/\sqrt{1125} = 1/\sqrt5 \approx 0.447$ — rank one keeps $80\%$ of the energy and still misses almost half the norm.

*Marking: 2 for $W_1$, 1 for the two predicted norms, 1 for the check.*

---

## Q2: Four Subspaces and the Pseudoinverse (22 points)

### (a) [6]

$$N^\mathsf{T}N(1,2,2) = (20 + 68 + 56,\ 34 + 130 + 124,\ 28 + 124 + 136) = (144, 288, 288) = 144\,(1,2,2)$$
$$N^\mathsf{T}N(-2,-1,2) = (-40 - 34 + 56,\ -68 - 65 + 124,\ -56 - 62 + 136) = (-18, -9, 18) = 9\,(-2,-1,2)$$

$$\sigma_1 = 12, \qquad \sigma_2 = 3.$$

$$u_1 = \frac{Nv_1}{12} = \frac{1}{36}(0 + 4 + 8,\ 4 + 12 + 8,\ 2 + 10 + 12) = \tfrac13(1,2,2), \qquad u_2 = \frac{Nv_2}{3} = \frac19(6, -6, 3) = \tfrac13(2,-2,1).$$

**Completions**, by cross products:

$$u_3 \propto (1,2,2)\times(2,-2,1) = (6, 3, -6) \Rightarrow u_3 = \tfrac13(2,1,-2); \qquad v_3 \propto (1,2,2)\times(-2,-1,2) = (6,-6,3) \Rightarrow v_3 = \tfrac13(2,-2,1).$$

**$\sigma_3 = 0$** — $\operatorname{trace}N^\mathsf{T}N = 153 = 144 + 9 + 0$, so there is nothing left for it.

*Marking: 2 verification, 1 $\sigma$'s, 2 $u_1, u_2$, 1 completions and $\sigma_3$. **Accept either sign on $u_3$ and $v_3$.***

### (b) [5]

| Subspace | Orthonormal basis |
|---|---|
| $\mathbf{C}(N)$ | $u_1 = \tfrac13(1,2,2)$, $u_2 = \tfrac13(2,-2,1)$ |
| $\mathbf{N}(N^\mathsf{T})$ | $u_3 = \tfrac13(2,1,-2)$ |
| $\mathbf{C}(N^\mathsf{T})$ | $v_1 = \tfrac13(1,2,2)$, $v_2 = \tfrac13(-2,-1,2)$ |
| $\mathbf{N}(N)$ | $v_3 = \tfrac13(2,-2,1)$ |

$$N(2,-2,1) = (0 - 4 + 4,\ 8 - 12 + 4,\ 4 - 10 + 6) = 0\ ✓, \qquad N^\mathsf{T}(2,1,-2) = (0 + 4 - 4,\ 4 + 6 - 10,\ 8 + 4 - 12) = 0\ ✓$$

*Marking: 1 per row, 1 for the two checks. **Swapping the column space with the row space is the standard error and costs 2.***

### (c) [6]

$$N^+ = \frac{1}{12}v_1u_1^\mathsf{T} + \frac13v_2u_2^\mathsf{T} = \frac{1}{108}\begin{bmatrix}1\\2\\2\end{bmatrix}\begin{bmatrix}1&2&2\end{bmatrix} + \frac1{27}\begin{bmatrix}-2\\-1\\2\end{bmatrix}\begin{bmatrix}2&-2&1\end{bmatrix} = \begin{bmatrix}-\tfrac5{36} & \tfrac16 & -\tfrac1{18}\\[2pt] -\tfrac1{18} & \tfrac19 & 0\\[2pt] \tfrac16 & -\tfrac19 & \tfrac19\end{bmatrix}.$$

$NN^+N = N$ ✓ *(verified exactly; all four Penrose conditions hold).*

$$NN^+ = \frac19\begin{bmatrix}5&-2&4\\-2&8&2\\4&2&5\end{bmatrix} = I - \frac19\begin{bmatrix}4&2&-4\\2&1&-2\\-4&-2&4\end{bmatrix} = I - u_3u_3^\mathsf{T}\ ✓$$

**Why it had to:** $NN^+$ is the projection onto $\mathbf{C}(N)$, and $\mathbf{C}(N)$ is the orthogonal complement of the line through $u_3$ — so projecting onto it is removing the $u_3$ component. *(Trace $2$ = rank, as a check.)*

*Marking: 3 for $N^+$, 1 for the Penrose check, 1 for $NN^+$, 1 for the sentence. **"$NN^+ = I$"** scores 0 for the last two marks — it is the claim that a singular matrix has an inverse.*

### (d) [5]

$$x^+ = N^+b = \left(\tfrac96 - \tfrac9{18},\ \tfrac99 + 0,\ -\tfrac99 + \tfrac99\right) = (1,\ 1,\ 0).$$

$$p = N(1,1,0) = (2,\ 10,\ 7), \qquad e = b - p = (-2,\ -1,\ 2), \qquad N^\mathsf{T}e = (0 - 4 + 4,\ -4 - 6 + 10,\ -8 - 4 + 12) = 0\ ✓$$

**$e = -3u_3$**, and $\lVert e\rVert^2 = 9 = (b\cdot u_3)^2$ — the residual is the $\mathbf{N}(N^\mathsf{T})$ component of $b$, exactly as Week 8 said.

**Every least-squares solution** is $x = (1,1,0) + t\,(2,-2,1)$, since $(2,-2,1)$ spans $\mathbf{N}(N)$. And $(1,1,0)\cdot(2,-2,1) = 0$, so

$$\lVert x\rVert^2 = \lVert(1,1,0)\rVert^2 + t^2\lVert(2,-2,1)\rVert^2 = 2 + 9t^2,$$

**minimised uniquely at $t = 0$.** $\square$

*Marking: 2 for $x^+$, 1 for $p$, $e$ and the check, 2 for the family and the length argument.*

---

## Q3: Approximation and Rank, Without a Computer (16 points)

### (a) [5]

| Quantity | Value |
|---|---:|
| $\lVert A\rVert_2 = \sigma_1$ | $10$ |
| $\lVert A\rVert_F = \sqrt{100 + 36 + 9 + 1}$ | $\sqrt{146} \approx 12.083$ |
| $\operatorname{cond}_2 = \sigma_1/\sigma_4$ | $10$ |
| $\lVert A - A_1\rVert_2 = \sigma_2$ | $6$ |
| $\lVert A - A_2\rVert_F = \sqrt{9 + 1}$ | $\sqrt{10} \approx 3.162$ |
| energy kept by $A_2$ | $136/146 \approx 93.15\%$ |

*Marking: 1 each for the first four taken together as 2, then 2 and 1.*

### (b) [5]

$$40\,(600 + 800 + 1) = 56{,}040 \text{ numbers}, \qquad \frac{56{,}040}{480{,}000} \approx 11.7\%.$$

**Break-even:** $k(1401) = 480{,}000$ gives $k \approx 342.6$, so **from rank $343$ upward the approximation is larger than the image.** *(Full rank is $600$.)*

*Marking: 2 storage, 1 fraction, 2 break-even. Accept $k > 342$ or $k \ge 343$.*

### (c) [6]

- **(i) Rank $3$.** Three-significant-figure entries carry perturbations of relative size $\sim10^{-3}$, so the data cannot distinguish the matrix from one within $\sim10^{-3}\cdot\sigma_1 \approx 10^{-2}$ of it. $\sigma_4 = 4\times10^{-9}$ is far inside that, and **$\sigma_4$ is the distance to a rank-3 matrix** (Eckart–Young).
- **(ii) Rank $4$.** Threshold $7.2\cdot5\cdot2.2\times10^{-16} \approx 7.9\times10^{-15}$. $\sigma_4 = 4\times10^{-9}$ is above it; $\sigma_5 = 3\times10^{-15}$ is below.
- **(iii) Rank $5$.** In exact arithmetic every nonzero singular value is a nonzero pivot's worth of independence — nothing is below any threshold because there is no threshold.

> **The point to put on the returned scripts:** *rank* is a property of the matrix only when the
> entries are exact. **For measured data it is a property of the matrix and the measurement
> together**, and the singular values are how you combine them.

*Marking: 2 each, 1 for the answer and 1 for the reason.*

---

## Q4: On the Machine (20 points)

### (a) [7]

| Image | Numerical rank | $k$ for $99\%$ energy |
|---|---:|---:|
| the diagonal alone (55 pixels) | $\mathbf{24}$ — **full rank** | $23$ |
| the original picture | $7$ | $5$ |
| **the picture with the diagonal** | $\mathbf{20}$ | $\mathbf{14}$ |

*First singular values with the diagonal: $14.88,\ 5.58,\ 3.62,\ 3.27,\ 2.82,\ 1.99,\ 1.83,\ 1.73,\ \dots$ The diagonal alone: $2.10,\ 2.09,\ 2.07,\ 2.04,\ 2.01,\ 1.98,\ 1.95,\ 1.80,\ \dots$ — almost flat, which is what full rank with no dominant direction looks like.*

**Why:** each row of the diagonal has its few pixels in a **different set of columns**, shifted along by about $\tfrac43$ per row. **No row is a combination of the others** — the rows form a staircase, and a staircase is echelon form with a pivot in every row. **So the rank is the number of rows, $24$.** A bar or a post is one row pattern repeated, which is rank $1$ by definition.

> **The lesson students should write:** low rank rewards structure **aligned with the axes of the
> matrix**. A line at an angle has no such alignment, so it is the most expensive thing to draw —
> **which is exactly why JPEG does not use the pixel basis**, and why Week 12's Fourier item exists.

*Marking: 2 for recorded predictions (any, honestly made), 3 for the table, 2 for the staircase explanation. **A prediction of rank $1$ for the diagonal, followed by a correct measurement and a correct explanation, scores full** — the marks are for predicting and then reconciling, not for predicting right.*

### (b) [6]

| noise | $\sigma_3$ | $\sigma_2/\sigma_3$ |
|---:|---:|---:|
| $10^{-14}$ | $3.497\times10^{-14}$ | $8.332\times10^{14}$ |
| $10^{-12}$ | $3.616\times10^{-12}$ | $8.057\times10^{12}$ |
| $10^{-10}$ | $3.617\times10^{-10}$ | $8.055\times10^{10}$ |
| $10^{-8}$ | $3.617\times10^{-8}$ | $8.055\times10^{8}$ |
| $10^{-6}$ | $3.617\times10^{-6}$ | $8.055\times10^{6}$ |
| $10^{-4}$ | $3.617\times10^{-4}$ | $8.055\times10^{4}$ |
| $10^{-2}$ | $3.618\times10^{-2}$ | $8.051\times10^{2}$ |
| $1$ | $3.731$ | $7.687$ |

**Exact scaling from about $10^{-12}$ to $10^{-4}$.** The rank-2 part is unchanged, so $\sigma_1, \sigma_2$ stay put, and $\sigma_3$ **is** the noise matrix's own largest singular value to first order — multiply the noise by $100$ and $\sigma_3$ multiplies by $100$.

**It stops at both ends.** At $10^{-14}$, $\sigma_3 = 3.497\times10^{-14}$ instead of $3.617\times10^{-14}$: **the floating-point floor**, $\sigma_1\cdot\varepsilon_\text{mach} \approx 63\cdot2.2\times10^{-16} \approx 1.4\times10^{-14}$, is now the same size as the noise, and rounding in the SVD itself contributes. At $10^{-2}$ and above, the noise is **no longer small relative to $\sigma_2$**, first-order perturbation theory fails, and $\sigma_1, \sigma_2$ themselves move ($63.82, 28.68$ at noise $1$).

**At noise $1$: defensibly either**, and the argument is the marks. *Yes:* a gap of $7.7$ after the second value, with the remaining four decaying smoothly, still separates two dominant directions. *No:* a factor of $7.7$ is not a gap in any statistical sense without knowing the noise level, and $\sigma_3 = 3.7$ is $13\%$ of $\sigma_2$.

*Marking: 2 table, 2 for the scaling range and its reason, 1 for identifying the floor, 1 for a defended verdict.*

### (c) [7]

| $x$-noise | $y$ on $x$ | $x$ on $y$, inverted | TLS |
|---:|---:|---:|---:|
| $0$ | $\mathbf{2.034663}$ | $2.066902$ | $2.060693$ |
| $0.3$ | $1.914679$ | $1.993384$ | $1.976936$ |
| $0.6$ | $1.723358$ | $1.924916$ | $\mathbf{1.877326}$ |
| $1.2$ | $1.303287$ | $1.801183$ | $1.642661$ |

*(True slope $2$ throughout.)*

**At $x$-noise $0$, ordinary least squares of $y$ on $x$ is the right model** — all the error really is in $y$, which is Week 9's assumption holding exactly — **and it beats TLS** ($2.0347$ against $2.0607$). TLS spends effort accounting for error in $x$ that is not there.

**TLS is the correct method when the noise in the two coordinates has the same size** — isotropic error — because perpendicular distance treats both coordinates identically. **At $x$-noise $1.2$ with $y$-noise $0.6$ that fails for both**: OLS attenuates badly ($1.30$, the classic errors-in-variables bias), and TLS is also biased ($1.64$), because it assumes the noise is equal when it is twice as large in $x$.

> **The fix, for strong students:** rescale one coordinate so the noise levels match, run TLS, and
> scale back. That is **Deming regression**, and it needs the noise ratio — which is information,
> not arithmetic.

*Marking: 2 table, 2 for "OLS is right at zero $x$-noise and TLS is worse", 2 for the equal-noise assumption, 1 for both methods failing at $1.2$. **"TLS is always better" scores at most 3.***

---

## Q5: Proofs (20 points)

### (a) [4]

Write $x = \sum c_jv_j$ with $\sum c_j^2 = \lVert x\rVert^2 = 1$ (orthonormal basis). Then $Ax = \sum c_j\sigma_ju_j$, and since the $u_j$ are orthonormal,

$$\lVert Ax\rVert^2 = \sum_j c_j^2\sigma_j^2 \le \sigma_1^2\sum_jc_j^2 = \sigma_1^2,$$

with equality at $x = v_1$. $\square$

*Marking: 2 for the expansion, 1 for the bound, 1 for attainment.*

### (b) [4]

$A^\mathsf{T} = (U\Sigma V^\mathsf{T})^\mathsf{T} = V\Sigma^\mathsf{T}U^\mathsf{T}$: **an SVD of $A^\mathsf{T}$**, with $V$ and $U$ swapped and $\Sigma^\mathsf{T}$ having the same diagonal. So the singular values agree.

**Symmetric:** $A = Q\Lambda Q^\mathsf{T}$. Let $D = \operatorname{diag}(\operatorname{sign}\lambda_i)$, taking $+1$ for $\lambda_i = 0$. Then $\Lambda = D\lvert\Lambda\rvert$ and

$$A = (QD)\,\lvert\Lambda\rvert\,Q^\mathsf{T},$$

with $QD$ orthogonal ($D^2 = I$) and $\lvert\Lambda\rvert$ non-negative diagonal. **After reordering, that is an SVD**, so $\sigma_i = \lvert\lambda_i\rvert$. $\square$

*Marking: 2 each. **The sign matrix $D$ must be explicit**; "take absolute values" without saying where the sign goes earns 1.*

### (c) [5]

$\dim\mathbf{N}(X) \ge n - k$ and $\dim\operatorname{span}(v_1, \dots, v_{k+1}) = k + 1$. The dimensions sum to at least $n + 1 > n$, so the subspaces share a unit vector $z = \sum_{j\le k+1}c_jv_j$, $\sum c_j^2 = 1$. Then $Xz = 0$ and

$$\lVert(A - X)z\rVert^2 = \lVert Az\rVert^2 = \sum_{j\le k+1}c_j^2\sigma_j^2 \ge \sigma_{k+1}^2\sum_{j\le k+1}c_j^2 = \sigma_{k+1}^2.$$

**So $\lVert A - X\rVert_2 \ge \lVert(A - X)z\rVert \ge \sigma_{k+1}$.** $\square$

*Marking: 2 for the intersection argument (the dimension count must be stated), 2 for the computation, 1 for concluding the norm inequality. **The step "dimensions sum to more than $n$, hence a nonzero intersection" is Week 3's**, and a script that asserts it without the count loses 1.*

### (d) [4]

Independent columns means $\sigma_1, \dots, \sigma_n > 0$, so $A^\mathsf{T}A = V(\Sigma^\mathsf{T}\Sigma)V^\mathsf{T}$ is invertible and

$$(A^\mathsf{T}A)^{-1}A^\mathsf{T} = V(\Sigma^\mathsf{T}\Sigma)^{-1}V^\mathsf{T}\,V\Sigma^\mathsf{T}U^\mathsf{T} = V\,\bigl[(\Sigma^\mathsf{T}\Sigma)^{-1}\Sigma^\mathsf{T}\bigr]\,U^\mathsf{T} = V\Sigma^+U^\mathsf{T},$$

since $(\Sigma^\mathsf{T}\Sigma)^{-1}\Sigma^\mathsf{T}$ is $n\times m$ with $\sigma_k/\sigma_k^2 = 1/\sigma_k$ on its diagonal. **If $A$ is invertible**, $\Sigma$ is square and invertible, $\Sigma^+ = \Sigma^{-1}$, and $V\Sigma^{-1}U^\mathsf{T} = (U\Sigma V^\mathsf{T})^{-1}$.

**For Week 9:** $\hat x = (A^\mathsf{T}A)^{-1}A^\mathsf{T}b = A^+b$ — **the normal equations' solution is the pseudoinverse solution whenever the former exists**, and $A^+b$ continues to make sense when it does not.

*Marking: 2 + 1 + 1.*

### (e) [3]

$$\lVert A\rVert_F^2 = \operatorname{trace}(A^\mathsf{T}A) = \operatorname{trace}\bigl(V(\Sigma^\mathsf{T}\Sigma)V^\mathsf{T}\bigr) = \operatorname{trace}\bigl((\Sigma^\mathsf{T}\Sigma)V^\mathsf{T}V\bigr) = \operatorname{trace}(\Sigma^\mathsf{T}\Sigma) = \sum_k\sigma_k^2,$$

using $\operatorname{trace}(XY) = \operatorname{trace}(YX)$. $\square$

*Marking: 1 per equality that needs a reason; **the cyclic property must be named.***

---

## Grade Distribution Expected

| Band | Score | Description |
|---|---|---|
| Strong | 88–100 | Q4(a) reconciled with the staircase, Q4(c)'s "OLS is right at zero noise", Q5(c) complete |
| Solid | 72–87 | Q1–Q3 correct; Q4 run with partial explanations; Q5(a), (b), (e) |
| Passing | 55–71 | Q1 and Q2(a)–(b) correct, with consistent signs |
| Concerning | < 55 | **Q1 with mismatched signs so that $U\Sigma V^\mathsf{T} \ne W$ and no check made.** The final has an SVD on it, and the check takes one entry |

---

*MATH 241 · Week 11 · PS 11 Solutions · © CSE Department*
