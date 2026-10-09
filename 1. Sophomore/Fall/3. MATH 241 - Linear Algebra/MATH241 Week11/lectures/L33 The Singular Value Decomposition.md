# MATH 241 · Linear Algebra
## Week 11 · Lecture 1 of 3 · **Monday**
### The Singular Value Decomposition

*“[M]y axiom runs as follows: "The whole is not identical with a part." This axiom leads us at once to a problem. What relation has the part to the whole?”* — Karl Pearson, *The Ethic of Freethought* (1883)

---

**Reading:** Strang Ch. 7, §7.1–§7.2 · **Previous:** Week 10's L32, what positive definiteness is for · **Next:** L34, what the SVD tells you

**Coursework:** 📊 **Quiz 11** today · 📝 **PS 11** released Wed this week, due Fri of Week 12 17:00 · 💬 **Recitation 10** Thu this week 15:00–15:50 · 📝 **PS 10** due Fri this week 17:00

> **Quiz 11 is the first ten minutes of this lecture**, covers Week 10, and is **the last quiz of
> the term.**
>
> **Midterm 2 papers come back at Recitation 10 on Thursday.** **PS 10 is due Friday at 17:00**,
> alongside **CS 211's Project 1**.
>
> **Thanksgiving recess follows this week** — no classes Nov 24. Week 12 starts Dec 1.

---

## 1. The Last Trade

**Week 10's Reading Guide ended on a table of theorems and their caveats**, and one line of it is worth repeating:

| Week | Factorisation | What it costs you |
|---|---|---|
| 7 | $A = S\Lambda S^{-1}$ | **only if** there are enough eigenvectors, and $S$ may be near-singular |
| 10 | $A = Q\Lambda Q^\mathsf{T}$ | **only if** $A$ is symmetric |
| **11** | $A = U\Sigma V^\mathsf{T}$ | **nothing — every matrix, any shape** |

**Week 10 bought an unconditional conclusion by restricting the matrices.** This week makes the other trade: keep every matrix, and give up on using **one** basis.

A similarity $S\Lambda S^{-1}$ describes $A$ in a single basis — the same coordinates for the input and for the output. **Week 4's L14 §1 never required that.** A map from $\mathbb{R}^n$ to $\mathbb{R}^m$ has an input space and an output space, and nothing obliges you to use related bases in the two. Week 7's L22 §6 noticed that *nothing until Week 11 needed it*.

> **Allow a different orthonormal basis at each end, and every matrix becomes diagonal.**
>
> $$\boxed{\;A = U\Sigma V^\mathsf{T}, \qquad U^\mathsf{T}U = I_m,\quad V^\mathsf{T}V = I_n,\quad \Sigma = \text{diagonal},\ \sigma_1 \ge \sigma_2 \ge \cdots \ge 0\;}$$
>
> **$V$ is an orthonormal basis of the input space, $U$ of the output space, and $A$ sends the
> $k$-th of one to a multiple of the $k$-th of the other:** $Av_k = \sigma_ku_k$.

**The $\sigma_k$ are the singular values.** They are never negative, and they are never complex.

---

## 2. Where It Comes From

**The construction is Week 10 applied once.** Whatever $A$ is — $3\times2$, singular, non-symmetric — $A^\mathsf{T}A$ is $n\times n$, symmetric, and positive semidefinite (L31 §7). **So the spectral theorem applies with no checking:**

$$A^\mathsf{T}A = V\Lambda V^\mathsf{T}, \qquad \lambda_1 \ge \cdots \ge \lambda_n \ge 0, \qquad V \text{ orthogonal.}$$

**Define $\sigma_k = \sqrt{\lambda_k}$ and, for each $\sigma_k > 0$, $u_k = Av_k/\sigma_k$.** Then the $u_k$ are orthonormal, and it takes one line:

$$u_i\cdot u_j = \frac{(Av_i)^\mathsf{T}(Av_j)}{\sigma_i\sigma_j} = \frac{v_i^\mathsf{T}(A^\mathsf{T}A)v_j}{\sigma_i\sigma_j} = \frac{\lambda_j\,(v_i\cdot v_j)}{\sigma_i\sigma_j} = \begin{cases}1 & i = j\\ 0 & i \ne j\end{cases}$$

**The orthonormality of the $u$'s is inherited from the orthonormality of the $v$'s**, through $A^\mathsf{T}A$. If there are fewer than $m$ of them, extend to an orthonormal basis of $\mathbb{R}^m$ any way you like (Week 8's Gram–Schmidt). **That is the whole existence proof, and it has no hypotheses because Week 10's didn't.**

**And the $u$'s are eigenvectors of the other product:**

$$AA^\mathsf{T}u_k = AA^\mathsf{T}\frac{Av_k}{\sigma_k} = \frac{A(A^\mathsf{T}A)v_k}{\sigma_k} = \frac{\lambda_kAv_k}{\sigma_k} = \sigma_k^2\,u_k.$$

> **So there are two symmetric matrices in play, $A^\mathsf{T}A$ ($n\times n$) and $AA^\mathsf{T}$
> ($m\times m$). They have the same nonzero eigenvalues, and the bigger one pads with zeros.** $V$
> diagonalises the first, $U$ the second, and $\Sigma$ holds the square roots of what they share.

---

## 3. Worked Exactly

Take

$$B = \begin{bmatrix}9&12\\ 12&16\\ -16&12\end{bmatrix} \qquad (3\times2).$$

**The two symmetric products** (`resources/svd.py` §2):

$$B^\mathsf{T}B = \begin{bmatrix}481&108\\ 108&544\end{bmatrix}, \qquad BB^\mathsf{T} = \begin{bmatrix}225&300&0\\ 300&400&0\\ 0&0&400\end{bmatrix}.$$

$\operatorname{trace}B^\mathsf{T}B = 1025$ and $\det B^\mathsf{T}B = 481\cdot544 - 108^2 = 250{,}000$, so the eigenvalues are $625$ and $400$. **$\operatorname{trace}BB^\mathsf{T} = 1025$ as well**, with a third eigenvalue $0$.

$$\sigma_1 = 25, \qquad \sigma_2 = 20.$$

**The input basis** — eigenvectors of $B^\mathsf{T}B$:

$$v_1 = \tfrac15(3,4), \qquad v_2 = \tfrac15(-4,3).$$

**The output basis**, from $u_k = Bv_k/\sigma_k$:

$$Bv_1 = (15,\ 20,\ 0) = 25\cdot\tfrac15(3,4,0), \qquad Bv_2 = (0,\ 0,\ 20) = 20\cdot(0,0,1),$$

and a third vector to complete $\mathbb{R}^3$, perpendicular to both: $u_3 = \tfrac15(-4,3,0)$, which $BB^\mathsf{T}$ sends to $0$.

$$B = \underbrace{\begin{bmatrix}\tfrac35 & 0 & -\tfrac45\\[2pt] \tfrac45 & 0 & \tfrac35\\[2pt] 0 & 1 & 0\end{bmatrix}}_{U\ (3\times3)} \underbrace{\begin{bmatrix}25&0\\0&20\\0&0\end{bmatrix}}_{\Sigma\ (3\times2)} \underbrace{\begin{bmatrix}\tfrac35&\tfrac45\\[2pt] -\tfrac45&\tfrac35\end{bmatrix}}_{V^\mathsf{T}\ (2\times2)}$$

`svd.py` §1 checks $U^\mathsf{T}U = I$, $V^\mathsf{T}V = I$ and $U\Sigma V^\mathsf{T} = B$ **in exact rational arithmetic**, and does the same for the two other matrices of this week.

> **An honest note about these numbers.** $B$ was built backwards: the singular vectors were chosen
> first, from $(3,4,5)$ triangles, so that everything would come out rational. **That is a
> construction, not a property of SVDs.** Almost every integer matrix has irrational singular values
> — $\begin{bmatrix}1&1\\0&1\end{bmatrix}$ has $\sigma = \tfrac{1\pm\sqrt5}{2}$ in absolute value.
> The theorem is exact; the arithmetic usually is not. **This is Week 10's REC 10 §1(c) again, and
> it is worth saying every time a clean example is used.**

---

## 4. The Picture: A Circle Becomes an Ellipse

**Take a square matrix so that you can draw it:**

$$A = \begin{bmatrix}12&11\\ 4&12\end{bmatrix}, \qquad v_1 = \tfrac15(3,4),\ v_2 = \tfrac15(-4,3), \qquad u_1 = \tfrac15(4,3),\ u_2 = \tfrac15(-3,4), \qquad \sigma = 20,\ 5.$$

Check: $Av_1 = \tfrac15(36+44,\ 12+48) = (16, 12) = 20\cdot\tfrac15(4,3)$ ✓ and $Av_2 = \tfrac15(-48+33,\ -16+36) = (-3, 4) = 5\cdot\tfrac15(-3,4)$ ✓

**Read $A = U\Sigma V^\mathsf{T}$ right to left, as three moves applied to the unit circle:**

1. **$V^\mathsf{T}$ rotates** $v_1, v_2$ onto the axes. *(Here by $-53.13°$; $\det V = +1$, so no reflection.)* The circle is still a circle.
2. **$\Sigma$ stretches** the axes by $20$ and $5$. The circle becomes an ellipse with semi-axes $20$ and $5$.
3. **$U$ rotates** the axes onto $u_1, u_2$. *(By $36.87°$.)* The ellipse turns into place.

**Rotation, stretch, rotation — for every matrix there is.** `svd.py` §3 walks $360{,}000$ points round the unit circle and measures:

| | measured | predicted |
|---|---:|---:|
| $\max\lVert Ax\rVert$ | $20.000000000$ | $\sigma_1 = 20$ |
| $\min\lVert Ax\rVert$ | $5.000000000$ | $\sigma_2 = 5$ |
| where the max is | $(0.600001,\ 0.799999)$ | $v_1 = (0.6,\ 0.8)$ |

> **So $\sigma_1$ is the most $A$ can stretch any vector**, and that is what "the size of a matrix"
> should mean. Compare the other things you might have called its size:
>
> | Candidate | Value |
> |---|---:|
> | largest entry | $12$ |
> | largest $\lvert\text{eigenvalue}\rvert$ | $12 + \sqrt{44} = 18.633250$ |
> | Frobenius norm $\sqrt{\sum a_{ij}^2}$ | $\sqrt{425} = 20.615528$ |
> | **$\max_{\lVert x\rVert = 1}\lVert Ax\rVert$** | **$\sigma_1 = 20$** |
>
> **$\lVert A\rVert_2 = \sigma_1$**, and L34 §2 builds the condition number from it.

### Eigenvalues are not singular values

$A$ has eigenvalues $12 \pm \sqrt{44} = 18.633250$ and $5.366750$, and singular values $20$ and $5$. **The products agree** — both are $100 = \lvert\det A\rvert$ — and **nothing else does.**

**The eigenvectors of $A$ are the directions $A$ does not rotate.** The singular vectors are the directions $A$ stretches most and least, and $A$ is allowed to rotate them. **For a non-symmetric matrix those are different questions with different answers.** For a symmetric positive semidefinite matrix they coincide, which is Week 10's L32 §7.

---

## 5. The Outer-Product Form

**Multiply $U\Sigma V^\mathsf{T}$ out column by row** — Week 1's L04 reading (iv):

$$\boxed{\;A = \sigma_1u_1v_1^\mathsf{T} + \sigma_2u_2v_2^\mathsf{T} + \cdots + \sigma_ru_rv_r^\mathsf{T}\;}$$

**A sum of rank-one matrices, in decreasing order of importance.** For our $2\times2$:

$$20\,u_1v_1^\mathsf{T} = \frac{20}{25}\begin{bmatrix}4\\3\end{bmatrix}\begin{bmatrix}3&4\end{bmatrix} = \begin{bmatrix}\tfrac{48}{5}&\tfrac{64}{5}\\[2pt] \tfrac{36}{5}&\tfrac{48}{5}\end{bmatrix}, \qquad 5\,u_2v_2^\mathsf{T} = \frac{5}{25}\begin{bmatrix}-3\\4\end{bmatrix}\begin{bmatrix}-4&3\end{bmatrix} = \begin{bmatrix}\tfrac{12}{5}&-\tfrac{9}{5}\\[2pt] -\tfrac{16}{5}&\tfrac{12}{5}\end{bmatrix},$$

and the sum is $\begin{bmatrix}12&11\\4&12\end{bmatrix}$ ✓.

> **Week 1's L04 said: *the SVD in Week 11 says every matrix is a sum of rank-one pieces
> $\sigma_ku_kv_k^\mathsf{T}$ ordered by importance; image compression is keeping the first twenty.***
> **This is that sentence, and L35 is the image.** Compare with Week 10's L30 §5,
> $A = \sum\lambda_kq_kq_k^\mathsf{T}$: the symmetric version used **one** vector per term, twice.
> The general version needs **two** — one from each end.

---

## 6. Shapes, and the Thin SVD

For $A$ of size $m\times n$ with rank $r$:

| Factor | Size | Columns |
|---|---|---|
| $U$ | $m\times m$ | $u_1,\dots,u_r$ from $Av_k/\sigma_k$; $u_{r+1},\dots,u_m$ completing $\mathbb{R}^m$ |
| $\Sigma$ | $m\times n$ | $\sigma_1,\dots,\sigma_r > 0$ on the diagonal, zeros everywhere else |
| $V$ | $n\times n$ | eigenvectors of $A^\mathsf{T}A$ |

**The extra columns of $U$ and $V$ multiply zeros in $\Sigma$**, so they contribute nothing to $A$. Dropping them gives the **thin** (or reduced) SVD, $A = U_r\Sigma_rV_r^\mathsf{T}$ with $U_r$ of size $m\times r$ — which is exactly §5's sum of $r$ terms.

**The extra columns are not useless.** L34 §1 shows they are orthonormal bases for the two null spaces, and that is how the SVD answers Week 3's question about the four subspaces in one stroke.

> **Rank is the number of nonzero singular values.** $B$ has two, so rank $2$. This week's third
> example, $M$, has $18$, $9$, $0$ — rank $2$ in a $3\times3$ — and it is L34's matrix.

---

## 7. What It Is Not, and How It Is Actually Computed

**Do not compute it the way §2 constructs it.** Forming $A^\mathsf{T}A$ squares the condition number — **Week 9's L28 §1, exactly** — and the small singular values are the ones that get destroyed. L34 §2 measures it on Läuchli's matrix: $\sigma_\min(A) = 10^{-8}$ is perfectly representable, and the computed $\sigma_\min(A^\mathsf{T}A)$ comes out as **exactly $0$**.

**`svd.py` uses one-sided Jacobi instead** — rotate pairs of columns of $A$ itself until they are mutually orthogonal. What remains is $AV = U\Sigma$: the column lengths are the singular values. **It never forms $A^\mathsf{T}A$**, every step is a rotation, and it is Week 10's Jacobi eigenvalue method transplanted to a rectangular matrix. **Production libraries use a different algorithm (Golub–Kahan bidiagonalisation) for speed**, and the principle is the same: orthogonal transformations only.

> **§2 is the proof. It is not the program.** Week 9 drew that distinction for the normal equations
> and it is the same distinction here.

---

## 8. What to Take Away

1. **Every matrix is $U\Sigma V^\mathsf{T}$** — orthonormal bases at both ends, non-negative diagonal in between. **No hypotheses.**
2. **The price is two bases.** Similarity used one; the SVD uses one for the input and one for the output.
3. **It is built from Week 10:** $V$ diagonalises $A^\mathsf{T}A$, $U$ diagonalises $AA^\mathsf{T}$, $\sigma_k = \sqrt{\lambda_k}$, $u_k = Av_k/\sigma_k$.
4. **$Av_k = \sigma_ku_k$** is the statement to remember; everything else is bookkeeping.
5. **Rotation, stretch, rotation.** The unit circle goes to an ellipse with semi-axes $\sigma_k$ along $u_k$.
6. **$\lVert A\rVert_2 = \sigma_1$** — not the largest entry, not the largest eigenvalue.
7. **Singular values are not eigenvalues** unless $A$ is symmetric positive semidefinite.
8. **$A = \sum\sigma_ku_kv_k^\mathsf{T}$**, a sum of rank-one pieces in order of importance. **Rank $=$ the number of nonzero $\sigma$.**
9. **Construct it through $A^\mathsf{T}A$; compute it without.**

---

## Exercises

*(Not assessed. PS 11 is the assessed work.)*

1. Find the SVD of $\begin{bmatrix}3&0\\0&-2\end{bmatrix}$. **Why is $\Sigma$ not simply the matrix itself?** Where does the sign go?
2. Find the SVD of the rank-one matrix $\begin{bmatrix}3&4\\6&8\\6&8\end{bmatrix}$ by writing it as a column times a row. **What are $\sigma_1$, $u_1$ and $v_1$?** *(No $A^\mathsf{T}A$ required.)*
3. For $B$ in §3, verify $BB^\mathsf{T}u_3 = 0$ and say which of Week 3's four subspaces $u_3$ spans.
4. $A$ is $5\times3$. What sizes are $U$, $\Sigma$, $V$? What are the sizes in the thin SVD if $A$ has rank $2$?
5. **Show that $Q$ orthogonal implies every singular value of $Q$ is $1$.** Then show the converse for square matrices.
6. Show that $A$ and $A^\mathsf{T}$ have the same singular values. **What happens to $U$ and $V$?**
7. $A = \begin{bmatrix}1&1\\0&1\end{bmatrix}$. Compute $A^\mathsf{T}A$, its eigenvalues, and $\sigma_1$, $\sigma_2$. **Check that $\sigma_1\sigma_2 = \lvert\det A\rvert$** and that neither singular value is an eigenvalue.
8. **Why can a singular value never be negative, when an eigenvalue can?** Answer in one sentence using §2. Then say what happens to a negative eigenvalue of a symmetric matrix when you take its SVD.

---

*MATH 241 · Week 11 · L33 · © CSE Department*
