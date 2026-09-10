# MATH 241 · Linear Algebra
## Week 11: The Singular Value Decomposition

**Credits:** 4 (3 lecture + 1 recitation) · **Prerequisites:** MATH 141
**Assessment for this course (overall):** Problem Sets 35%, Midterms 40%, Final 25%
**This week's deliverables:** PS 11 (released Wednesday, due **Friday of Week 12**) and **Quiz 11** (Monday, covers Week 10 — **the last quiz of the term**). **PS 10 is due at 17:00 this Friday.**
**Recitation 10 is sat this Thursday** — it covers **Week 10**, and **Midterm 2 papers are returned there**. Recitation 11, covering this week, is sat on the **Thursday of Week 12**.

> **Thanksgiving recess follows this week** — no classes Nov 24. Week 12 begins Monday Dec 1 and is
> the last teaching week.
>
> **PS 11 and PS 12 are both due Friday Dec 5.** PS 11 spans the recess; PS 12 is released that
> Wednesday and is short. **Start PS 11 before the break.**
>
> **CS 211's Project 1 is due this Friday** at 17:00, alongside PS 10.

---

### Why This Week Exists

Because every factorisation so far has come with a condition, and this one does not.

**Week 7's $S\Lambda S^{-1}$ needed enough eigenvectors. Week 9's $QR$ needed independent columns. Week 10's $Q\Lambda Q^\mathsf{T}$ needed symmetry.** Each week bought something by restricting the matrices. **This week keeps every matrix** — rectangular, singular, non-symmetric, with complex eigenvalues — and pays instead by allowing **a different orthonormal basis at the input and at the output**:

$$A = U\Sigma V^\mathsf{T}, \qquad Av_k = \sigma_ku_k.$$

**Week 4's L14 §1 permitted two bases from the start, and nothing until now needed it.**

**The construction is Week 10 applied once.** $A^\mathsf{T}A$ is symmetric positive semidefinite for *every* $A$, so the spectral theorem hands you $V$ and the $\sigma_k^2$ with nothing to check, and $u_k = Av_k/\sigma_k$ does the rest.

**And it closes more loops than any other week:**

- **Week 3** proved row rank $=$ column rank and apologised for not explaining it. **L34 §1 explains it.**
- **Week 8** left a projection formula that fails on dependent columns. **$AA^+$ is the fix.**
- **Week 9** left least squares undefined in the same case, and asserted $\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$ without proof. **L34 §2 and §4 do both.**
- **Week 1** measured a $787\times$ speedup from never forming a low-rank product and said *Week 11 explains why any matrix can be approximated this way*. **L35 is that explanation.**

---

### Learning Objectives

By the end of Week 11, you should be able to:

1. **State the SVD** for an $m\times n$ matrix, with the shapes of all three factors, full and thin.
2. **Construct it** from $A^\mathsf{T}A$, and prove the $u$'s are orthonormal.
3. **Compute it by hand** for a $2\times2$, a $2\times3$ and a rank-one matrix — deriving $U$ from $V$, not independently.
4. **Draw it**: rotation, stretch, rotation; the unit circle to an ellipse with semi-axes $\sigma_k$.
5. **Distinguish singular values from eigenvalues**, and prove $\sigma_\min \le \lvert\lambda\rvert \le \sigma_\max$.
6. **Read all four subspaces off $U$ and $V$**, with orthonormal bases.
7. **Explain row rank $=$ column rank** from $Av_k = \sigma_ku_k$ and $A^\mathsf{T}u_k = \sigma_kv_k$.
8. **Compute $\lVert A\rVert_2$, $\lVert A\rVert_F$ and $\operatorname{cond}_2$** from the singular values, and prove $\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$.
9. **Build $A^+$**, check the Penrose conditions, and find the shortest least-squares solution.
10. **Decide numerical rank** from a gap in the singular values, and say why pivots cannot.
11. **State and apply Eckart–Young** in both norms.
12. **Fit a line by total least squares**, and say when it is and is not the right model.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L33 The Singular Value Decomposition]] | **The last trade: two bases instead of one**; the construction from $A^\mathsf{T}A$; **a $3\times2$ worked exactly**; circle to ellipse, measured; **eigenvalues are not singular values**; the outer-product form |
| [[L34 What the SVD Tells You]] | **Four subspaces, four orthonormal bases**; **row rank $=$ column rank explained**; norms and $\operatorname{cond}(A^\mathsf{T}A)$; **the pseudoinverse, exactly**; least squares with dependent columns; **numerical rank: 6 pivots, 2 singular values** |
| [[L35 Low-Rank Approximation]] | **Eckart–Young, measured**; **compressing a picture**, and where its rank comes from; low rank without decompressing; **total least squares**; Week 9's table completed; **the five factorisations in one table** |
| [[REC 11 Singular Values by Hand]] | Four steps on paper, a matrix with complex eigenvalues, a rank-one pseudoinverse. **Thursday of Week 12** |
| [[PS 11 The Singular Value Decomposition]] | Five questions, 100 points, due **Friday of Week 12** |
| [[MATH241 Week11/assignments/QUIZ 11 Week 11 Monday\|QUIZ 11 Week 11 Monday]] | Ten minutes, covers **Week 10**, answer key printed. **The last quiz** |
| [[MATH241 Week11/resources/Reading Guide Week 11\|Reading Guide Week 11]] | Strang Ch. 7, **Trefethen & Bau Lectures 4–5**, and seven lines for the final's sheet |
| `resources/svd.py` | Every number in L33–L35, reproducible. **A one-sided Jacobi SVD, in pure Python** |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Rank is not a count. It is a gap.**

Take a $6\times6$ integer matrix of rank exactly $2$ and add noise of size $10^{-10}$ — less than any measurement could see (L34 §5):

| | What it reports |
|---|---|
| **Elimination** | pivots $18,\ 4,\ 1.1\times10^{-9},\ 1.3\times10^{-10},\ 3.6\times10^{-10},\ 3.1\times10^{-10}$ — **six nonzero, "rank 6"** |
| **The SVD** | $\sigma = 63.38,\ 29.14,\ 3.6\times10^{-10},\ 2.0\times10^{-10},\ 1.4\times10^{-10},\ 6.0\times10^{-11}$ — **a gap of $8\times10^{10}$ after the second** |

**Week 3's definition — the number of pivots — is exact on exact data and meaningless on measured data.** A pivot's size depends on the row order. **A singular value does not**: $\sigma_{k+1}$ is exactly the distance from $A$ to the nearest matrix of rank $k$ (L35 §1). So $\sigma_3 = 3.6\times10^{-10}$ is a measurement — *move the entries that far and the matrix has rank 2* — and the gap is the rank.

> **This is the seventh time this term that "correct" and "usable" have come apart**, and the first
> time the correct definition itself had to be replaced. **Every real rank computation —
> `numpy.linalg.matrix_rank`, `lstsq`'s `rcond`, the rank a statistics package reports — thresholds
> singular values.** None of them counts pivots.

---

### Assessment Reminder

**Quizzes and the recitation carry no weight** and are still required. **Quiz 11 is at the start of Monday's lecture, covers Week 10, and is the last quiz of the term.**

**Midterm 2 papers are returned at Recitation 10 on Thursday.** Questions about your own mark go to Prof. Abara — Monday 13:00–15:00 or Thursday 10:00–11:00, SSB 310.

**The final is Monday Dec 15, 09:00–11:30**, comprehensive, 25%. **Week 11 is the most-used result of the course in everything that comes after it**, and the paper will reflect that.

Quizzes are tracked in [[_MATH 241 Quiz Record]].

---

### Connections

**Back:** **Week 10's spectral theorem is the whole construction** — applied to $A^\mathsf{T}A$ and $AA^\mathsf{T}$, both symmetric positive semidefinite by L31 §7. **Week 8's orthonormal bases and projections** are $U$, $V$, $AA^+$ and $A^+A$. **Week 9's L28** asserted $\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$ and deferred rank-deficient least squares; both are L34. **Week 7's L22 §6 table** ended with *every matrix, any shape — $U\Sigma V^\mathsf{T}$ — always*. **Week 3's L12 §4** promised this week an explanation of row rank $=$ column rank. **Week 1's L04** called the outer-product reading *Week 11*, and its $787\times$ measurement is the payoff of L35 §4. **Week 0's L03 §7** named $\operatorname{cond}(A)$ the thread of the second half; $\sigma_1/\sigma_n$ is its general definition.

**Sideways:** **CS 211's Project 1 is due Friday.** No content connection — but CS 331 and every data-science course after this one will assume the SVD on their first day.

**Forward:** **Week 12 is four applications and they are this week, twice.** **PCA is L35 §5 in more dimensions** — the best $k$-dimensional subspace through a cloud of points, from the top $k$ singular vectors. **PageRank is Week 6's eigenvector found by Week 7's powers**, on a matrix too large to factor. **Regression is Week 9 with the SVD available** when predictors are redundant. **Fourier is Week 8's orthonormal expansion on functions**, and JPEG is L35 §3's compression in a fixed basis instead of the optimal one.

---

*MATH 241 · Week 11 · © CSE Department*
