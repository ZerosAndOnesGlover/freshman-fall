# MATH 241 · Linear Algebra
## Week 11 · Lecture 2 of 3 · **Tuesday**
### What the SVD Tells You

---

**Reading:** Strang §7.2, §4.4's pseudoinverse remarks · **Previous:** L33, the SVD · **Next:** L35, low-rank approximation

> **Recitation 10 is Thursday**, and Midterm 2 papers are returned there. **PS 10 is due Friday.**
>
> **Today closes four loops that have been open for weeks.** Week 3 promised an explanation of row
> rank $=$ column rank. Week 8 left a projection formula that fails on dependent columns. Week 9 left
> least squares undefined in the same case. Week 9 also asserted $\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$
> without proof. **All four are one factorisation.**

---

## 1. Four Subspaces, Four Orthonormal Bases, One Factorisation

Take

$$M = \begin{bmatrix}6&0&6\\ 9&6&6\\ 6&12&0\end{bmatrix}, \qquad \sigma = 18,\ 9,\ 0.$$

$$U = \frac13\begin{bmatrix}1&2&2\\ 2&1&-2\\ 2&-2&1\end{bmatrix}, \qquad V = \frac13\begin{bmatrix}2&1&2\\ 2&-2&-1\\ 1&2&-2\end{bmatrix}.$$

**Rank $2$** — two nonzero singular values, and elimination agrees. `svd.py` §4 checks each of the following exactly:

| Subspace | Dimension | Orthonormal basis | Why |
|---|---:|---|---|
| $\mathbf{C}(M)$ | $2$ | $u_1,\ u_2$ | $Mv_k = \sigma_ku_k$ with $\sigma_k \ne 0$ |
| $\mathbf{N}(M^\mathsf{T})$ | $1$ | $u_3$ | $M^\mathsf{T}u_3 = 0$ |
| $\mathbf{C}(M^\mathsf{T})$ | $2$ | $v_1,\ v_2$ | $M^\mathsf{T}u_k = \sigma_kv_k$ with $\sigma_k \ne 0$ |
| $\mathbf{N}(M)$ | $1$ | $v_3$ | $Mv_3 = 0$ |

*(Check the last one: $M(2,-1,-2) = (12 + 0 - 12,\ 18 - 6 - 12,\ 12 - 12 + 0) = 0$ ✓)*

> **Week 3's L12 found these four spaces by four different recipes**, none of them orthogonal.
> **Week 8 proved they are orthogonal in pairs.** **The SVD hands you all four at once, each with an
> orthonormal basis, and the orthogonality is not a theorem to prove — it is inherited from $U$ and
> $V$.** The first $r$ columns of each factor span the column and row spaces; the rest span the null
> spaces.

### Row rank $=$ column rank, explained

**Week 3's L12 §4 proved it and apologised:** *the proof routes both counts through one algorithm and concludes they agree because the algorithm produced one number — true, and it does not explain why rows and columns should know about each other.*

**Here is why.** Transpose $A = U\Sigma V^\mathsf{T}$:

$$A^\mathsf{T} = V\Sigma^\mathsf{T}U^\mathsf{T}, \qquad\text{so}\qquad Av_k = \sigma_ku_k \quad\text{and}\quad A^\mathsf{T}u_k = \sigma_kv_k.$$

**Each nonzero $\sigma_k$ is a matched pair** — one direction $v_k$ in the row space and one direction $u_k$ in the column space, joined by the same number in both directions. **There is no way to have a row-space direction without its column-space partner.** So the two dimensions are the same count, and the count is the number of nonzero singular values: a quantity attached to $A$ itself, with no reference to rows, columns or elimination.

**Week 3's own matrix**, run through the float SVD (`svd.py` §4):

$$\begin{bmatrix}1&3&3&2\\ 2&6&9&7\\ -1&-3&3&4\end{bmatrix}: \qquad \sigma = 14.1277,\ \ 5.32991,\ \ 2.10\times10^{-16}.$$

**Two singular values, then rounding noise.** Four columns in $\mathbb{R}^3$, three rows in $\mathbb{R}^4$, one count.

---

## 2. Norms, Condition Numbers, and Week 9's Squaring

**Two norms fall straight out.** Because $U$ and $V$ preserve lengths,

$$\lVert A\rVert_2 = \sigma_1, \qquad \lVert A\rVert_F^2 = \sum_{i,j}a_{ij}^2 = \sigma_1^2 + \sigma_2^2 + \cdots + \sigma_r^2.$$

| Matrix | $\sum a_{ij}^2$ | $\sum\sigma_k^2$ | $\lVert\cdot\rVert_2$ |
|---|---:|---:|---:|
| L33's $A = \begin{bmatrix}12&11\\4&12\end{bmatrix}$ | $425$ | $400 + 25$ | $20$ |
| L33's $B$ | $1025$ | $625 + 400$ | $25$ |
| $M$ | $405$ | $324 + 81 + 0$ | $18$ |

**The condition number, for any matrix** (Week 0's L03 §7, finally in general):

$$\boxed{\;\operatorname{cond}_2(A) = \frac{\sigma_1}{\sigma_n}\;}$$

— the ratio of the most to the least that $A$ stretches. $A$: $20/5 = 4$. $B$: $25/20 = 1.25$. $M$: $18/0$, infinite, because $M$ is singular. **Week 10's $\lambda_\max/\lambda_\min$ was the symmetric positive definite special case**, and Week 10's Reading Guide warned it was false in general. This is what replaces it.

### $\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$, in one line

**Week 9's L28 §1 asserted this and said it would be obvious in Week 11.** It is:

$$A^\mathsf{T}A = (U\Sigma V^\mathsf{T})^\mathsf{T}(U\Sigma V^\mathsf{T}) = V\Sigma^\mathsf{T}(U^\mathsf{T}U)\Sigma V^\mathsf{T} = V(\Sigma^\mathsf{T}\Sigma)V^\mathsf{T}.$$

**That is an SVD of $A^\mathsf{T}A$, with singular values $\sigma_k^2$.** So the ratio squares. On L33's $A$ the script measures singular values $400$ and $25$ for $A^\mathsf{T}A$ and $\operatorname{cond} = 16.000000000 = 4^2$.

**And on Läuchli's matrix** (`svd.py` §5):

| $\varepsilon$ | $\sigma_1(A)$ | $\sigma_2(A)$ | $\operatorname{cond}(A)$ | computed $\sigma_\min(A^\mathsf{T}A)$ |
|---:|---:|---:|---:|---:|
| $10^{-4}$ | $1.414214$ | $1.000\times10^{-4}$ | $1.414\times10^{4}$ | $1.000\times10^{-8}$ |
| $10^{-7}$ | $1.414214$ | $1.000\times10^{-7}$ | $1.414\times10^{7}$ | $1.005\times10^{-14}$ |
| $10^{-8}$ | $1.414214$ | $1.000\times10^{-8}$ | $1.414\times10^{8}$ | $\mathbf{0}$ |

> **Read the last row.** $\sigma_2(A) = 10^{-8}$ is computed correctly from $A$ itself. **Its square,
> $10^{-16}$, is below the rounding in $1 + \varepsilon^2$**, so $A^\mathsf{T}A$'s smallest singular
> value is exactly zero. At $\varepsilon = 10^{-7}$ the computed value is already wrong in the third
> digit. **Week 9's table, explained number by number.**

---

## 3. The Pseudoinverse

**$M$ has no inverse.** It sends $v_3$ to zero, and nothing can undo that. **But on the row space it is perfectly invertible** — it sends $v_1 \mapsto 18u_1$ and $v_2 \mapsto 9u_2$, and those can be undone.

$$\boxed{\;A^+ = V\Sigma^+U^\mathsf{T}, \qquad \Sigma^+ = \text{transpose of }\Sigma\text{ with each nonzero }\sigma_k\text{ replaced by }1/\sigma_k\;}$$

**$A^+$ sends $u_k \mapsto v_k/\sigma_k$ for $\sigma_k \ne 0$, and $u_k \mapsto 0$ otherwise.** It inverts what can be inverted and discards the rest. For $M$ (`svd.py` §6, exact):

$$M^+ = \begin{bmatrix}\tfrac1{27} & \tfrac1{27} & 0\\[2pt] -\tfrac1{27} & 0 & \tfrac2{27}\\[2pt] \tfrac1{18} & \tfrac1{27} & -\tfrac1{27}\end{bmatrix}.$$

**The four Penrose conditions**, all verified exactly:

$$MM^+M = M, \qquad M^+MM^+ = M^+, \qquad (MM^+)^\mathsf{T} = MM^+, \qquad (M^+M)^\mathsf{T} = M^+M.$$

**And the two products are Week 8's projections:**

$$MM^+ = \frac19\begin{bmatrix}5&4&-2\\4&5&2\\-2&2&8\end{bmatrix} \ \text{projects onto } \mathbf{C}(M), \qquad M^+M = \frac19\begin{bmatrix}5&2&4\\2&8&-2\\4&-2&5\end{bmatrix} \ \text{projects onto } \mathbf{C}(M^\mathsf{T}).$$

Both are symmetric, both square to themselves, **both have trace $2$ = the rank** — Week 8's L25 §5, which said a projection's trace counts the dimension it projects onto.

> **Week 8's L25 exercise 6 asked what goes wrong with $P = A(A^\mathsf{T}A)^{-1}A^\mathsf{T}$ when the
> columns are dependent, and answered *the subspace is fine; only the formula fails. Week 11 fixes
> this.*** **$P = AA^+$ is the fix.** It is the projection onto $\mathbf{C}(A)$ for every $A$, and it
> reduces to Week 8's formula when $A^\mathsf{T}A$ is invertible.

---

## 4. Least Squares When the Columns Are Dependent

**Week 9's L27 §6 named the case and deferred it**: two predictors that say the same thing. Take $x$ = years of schooling, and a second predictor, age on leaving school, which is $x + 5$ for a cohort that all started at five:

$$A = \begin{bmatrix}1&8&13\\ 1&10&15\\ 1&12&17\\ 1&16&21\end{bmatrix}, \qquad b = \begin{bmatrix}30\\34\\41\\52\end{bmatrix}.$$

**The third column is the first five times plus the second.** Rank $2$, and $\det(A^\mathsf{T}A) = 0$: **the normal equations are singular.** Week 9 could only say *remove a column*.

**The SVD says more.** The projection $p$ onto $\mathbf{C}(A)$ is unique, so the residual is fixed — but **every** $x$ with $Ax = p$ is a minimiser, and they form a line, $x^+ + t\,(5, 1, -1)$, because $(5,1,-1)$ spans $\mathbf{N}(A)$. **The pseudoinverse picks the shortest one** (`svd.py` §7, exact):

$$x^+ = A^+b = \left(-\tfrac{1}{90},\ \tfrac{452}{315},\ \tfrac{869}{630}\right), \qquad A^\mathsf{T}(b - Ax^+) = 0\ ✓$$

| $t$ | $\lVert x^+ + t(5,1,-1)\rVert^2$ | residual$^2$ |
|---:|---:|---:|
| $-2$ | $111.961769$ | $1.542857$ |
| $-1$ | $30.961769$ | $1.542857$ |
| $\mathbf{0}$ | $\mathbf{3.961769}$ | $1.542857$ |
| $1$ | $30.961769$ | $1.542857$ |
| $2$ | $111.961769$ | $1.542857$ |

**Same fit, different lengths, and $t = 0$ is shortest** — because $x^+\cdot(5,1,-1) = 0$ exactly: $x^+$ lies in the row space, perpendicular to the null space, and Pythagoras does the rest.

> **Why "shortest" is the right tie-break.** Among coefficient vectors that fit equally well, the
> shortest one puts no weight on directions the data cannot see. **It does not pretend to know how
> to split credit between two predictors that always move together** — it splits it in proportion,
> and says nothing it was not told. *(Weighting toward small coefficients is also the idea behind
> ridge regression, in CS 331.)*

**The float SVD agrees.** Singular values $41.1067$, $1.49566$, $8.08\times10^{-16}$; discard the third as rounding noise, invert the other two, and $x = (-0.011111111,\ 1.434920635,\ 1.379365079)$ — **equal to the exact $x^+$ to all nine digits shown.**

---

## 5. Numerical Rank: Elimination Counts, the SVD Measures

**Week 3 defined rank as the number of pivots.** That is exact on exact data and it is **useless on measured data.**

`svd.py` §8 builds a $6\times6$ integer matrix of rank exactly $2$ — a sum of two outer products — and adds noise of size $10^{-10}$, which is less than any instrument could see.

| | Result |
|---|---|
| **Pivots** (partial pivoting) | $18,\ 4,\ 1.144\times10^{-9},\ 1.293\times10^{-10},\ 3.566\times10^{-10},\ 3.101\times10^{-10}$ |
| **Nonzero pivots** | **$6$ — "rank 6"** |
| **Singular values** | $63.38,\ 29.14,\ 3.617\times10^{-10},\ 2.045\times10^{-10},\ 1.448\times10^{-10},\ 5.956\times10^{-11}$ |
| $\sigma_2/\sigma_3$ | $\mathbf{8.1\times10^{10}}$ |

**Elimination reports rank $6$ because none of its pivots is exactly zero**, and it has no way to decide which small pivots are real — a pivot's size depends on the row order. **The singular values report a gap of ten orders of magnitude**, and the gap is the answer: rank $2$, plus noise.

> **Why the singular value is the right thing to threshold.** $\sigma_{k+1}$ is exactly the distance
> from $A$ to the nearest matrix of rank $k$ — that is L35 §1's theorem. **So $\sigma_3 = 3.6\times10^{-10}$
> says: moving the entries by $3.6\times10^{-10}$ reaches a rank-2 matrix.** No pivot has a meaning
> like that.
>
> **This is what `numpy.linalg.matrix_rank` computes**, and what the `rcond` parameter of
> `numpy.linalg.lstsq` sets — **Week 9's Reading Guide flagged `rcond` as Week 11**, and it is the
> threshold below which a singular value is declared zero before inverting.

---

## 6. What to Take Away

1. **The SVD gives orthonormal bases for all four subspaces at once**: the first $r$ columns of $U$ and $V$ for the column and row spaces, the rest for the null spaces.
2. **Row rank $=$ column rank because $Av_k = \sigma_ku_k$ and $A^\mathsf{T}u_k = \sigma_kv_k$** pair them one-for-one.
3. **$\lVert A\rVert_2 = \sigma_1$, $\lVert A\rVert_F^2 = \sum\sigma_k^2$, $\operatorname{cond}_2 = \sigma_1/\sigma_n$.**
4. **$A^\mathsf{T}A = V(\Sigma^\mathsf{T}\Sigma)V^\mathsf{T}$**, so its singular values are $\sigma_k^2$ and its condition number is squared. Week 9, proved.
5. **$A^+ = V\Sigma^+U^\mathsf{T}$** inverts $A$ on its row space and discards the rest. **$AA^+$ and $A^+A$ are the projections onto $\mathbf{C}(A)$ and $\mathbf{C}(A^\mathsf{T})$.**
6. **$x^+ = A^+b$ is the shortest least-squares solution**, and it exists when the normal equations are singular.
7. **Numerical rank is a gap in the singular values**, not a count of nonzero pivots.

---

## Exercises

*(Not assessed. PS 11 is the assessed work.)*

1. From $M$'s SVD, write an orthonormal basis for each of the four subspaces **without looking at §1**. Then check $u_3 \perp$ every column of $M$.
2. **If $A$ is invertible, show $A^+ = A^{-1}$.** If $A$ has independent columns, show $A^+ = (A^\mathsf{T}A)^{-1}A^\mathsf{T}$ — Week 9's formula.
3. Compute the pseudoinverse of the rank-one matrix $uv^\mathsf{T}$ with $\lVert u\rVert = \lVert v\rVert = 1$. Then of $\begin{bmatrix}1&2\\2&4\end{bmatrix}$.
4. **Is $(AB)^+ = B^+A^+$?** Try $A = \begin{bmatrix}1&0\end{bmatrix}$, $B = \begin{bmatrix}1\\1\end{bmatrix}$.
5. Verify $\lVert M\rVert_F^2 = 405$ from the entries, then from the singular values.
6. In §4, confirm by hand that $(5,1,-1) \in \mathbf{N}(A)$, and that $x^+\cdot(5,1,-1) = 0$ from the three fractions.
7. **Why does elimination's pivot count depend on the row order, when rank does not?** Construct a $2\times2$ where swapping rows changes the second pivot by a factor of $10^6$.
8. $A$ has singular values $5$, $1$, $10^{-9}$, $10^{-12}$. **What rank would you report, and at what threshold?** What would you report if you knew the entries were measured to three significant figures?

---

*MATH 241 · Week 11 · L34 · © CSE Department*
