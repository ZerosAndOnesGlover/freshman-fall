# MATH 241 · Final Examination
## Linear Algebra

---

**Monday 15 December · 09:00–11:30 · 150 minutes · VNC 100** *(overflow seating in TH 200 — check your seat on the course portal)*
**Comprehensive — Weeks 0–12.**
**Weight: 25% of the course grade**

**Permitted:** two handwritten pages of notes. No calculators, no devices.
**Total: 100 marks** — about a mark and a half per minute; budget accordingly.

**Name:** _________________________________ **Student ID:** ___________________

---

> **Answer all eight questions.** Marks are shown per part.
>
> **Section A (Q1–Q3, 34 marks)** is Weeks 0–5. **Section B (Q4–Q5, 26 marks)** is Weeks 6–9.
> **Section C (Q6–Q8, 40 marks)** is Weeks 10–12, which no midterm has examined.
>
> **Every number on this paper comes out exactly.** If a fraction turns ugly, check your arithmetic
> against a trace or a determinant before going on. **Show the check** — it earns marks.
>
> **Budget check:** if you are not starting Section C by 10:30, move on. It is 40 marks.

---

# Section A · Weeks 0–5 (34 marks)

## Q1 · Elimination and $LU$ (12 marks)

$$A = \begin{bmatrix}2&1&-1\\ 6&4&1\\ -4&1&9\end{bmatrix}$$

**(a)** *(5)* Factor $A = LU$ with $L$ unit lower triangular, **stating every multiplier.** Give $\det A$ from your factors.

**(b)** *(4)* Solve $Ax = (-1, 4, 13)$ **using $L$ and $U$** — forward substitution, then back substitution. Show the intermediate vector.

**(c)** *(3)* In double precision, eliminating

$$\begin{bmatrix}10^{-20} & 1\\ 1 & 1\end{bmatrix}x = \begin{bmatrix}1\\2\end{bmatrix}$$

**without** a row exchange returns $x_1 = 0.0$ exactly, although the true $x_1$ is very close to $1$. **Name the arithmetic step at which the information is lost, and say what partial pivoting changes so that it is not.**

---

## Q2 · The Four Subspaces (12 marks)

$$B = \begin{bmatrix}1&2&0&1\\ 2&4&1&4\\ 3&6&1&5\end{bmatrix}$$

**(a)** *(4)* Find the reduced row echelon form and the rank. Give a basis for $\mathbf{C}(B)$ and a basis for $\mathbf{N}(B)$.

**(b)** *(3)* Give a basis for $\mathbf{N}(B^\mathsf{T})$. State the dimensions of all four subspaces **and the two equations they satisfy.**

**(c)** *(3)* Give the condition on $b$ for $Bx = b$ to be solvable. **Is $b = (1, 1, 2)$ reachable? Is $b = (1, 1, 1)$?**

**(d)** *(2)* Is $(0, 0, 1, 2)$ in the row space of $B$? **One sentence.**

---

## Q3 · Determinants and Eigenvalues (10 marks)

**(a)** *(2)* **Without expanding**, give the determinant of

$$\begin{bmatrix}2&0&0&0\\ 1&3&0&0\\ 5&6&1&0\\ 7&8&9&4\end{bmatrix}$$

and say which property you used.

**(b)** *(4)* Find the eigenvalues and eigenvectors of $C = \begin{bmatrix}4&1\\2&3\end{bmatrix}$. **Check both against the trace and determinant.**

**(c)** *(4)* **Without computing any new matrix**, find $\det(2C^{-1})$, the eigenvalues of $C^3 + I$, and $\det(C^3 + I)$.

---

# Section B · Weeks 6–9 (26 marks)

## Q4 · Diagonalisation and Powers (12 marks)

$$M = \begin{bmatrix}\tfrac45 & \tfrac3{10}\\[2pt] \tfrac15 & \tfrac7{10}\end{bmatrix}$$

**(a)** *(3)* **Show $\lambda = 1$ is an eigenvalue without computing a determinant.** Then find the other eigenvalue in one line.

**(b)** *(5)* Diagonalise $M = S\Lambda S^{-1}$ and give $M^k$ **in closed form**, entry by entry. What is $\lim_{k\to\infty}M^k$?

**(c)** *(2)* **What is the smallest $k$** for which every entry of $M^k$ is within $10^{-6}$ of its limit? Show the calculation.

**(d)** *(2)* $\begin{bmatrix}3&1\\0&3\end{bmatrix}$ cannot be diagonalised. **Say why in terms of an eigenspace.**

---

## Q5 · Orthogonality and Least Squares (14 marks)

Fit a line $y = c + dt$ to the four points $(-1, 0)$, $(0, 1)$, $(1, 3)$, $(2, 4)$.

**(a)** *(5)* Write $A$ and $y$, form the normal equations, and solve for $\hat x = (c, d)$ exactly.

**(b)** *(3)* Give the residual $e$. **Check $A^\mathsf{T}e = 0$**, give $\lVert e\rVert^2$, and check that the line passes through the centroid of the data.

**(c)** *(4)* Apply **Gram–Schmidt** to the columns of $A$ to get $A = QR$. **Solve $R\hat x = Q^\mathsf{T}y$** and confirm you get the same $\hat x$.

**(d)** *(2)* **Why do numerical libraries not solve least-squares problems through the normal equations?** Answer with one formula and one sentence.

---

# Section C · Weeks 10–12 (40 marks)

## Q6 · Symmetric and Positive Definite Matrices (14 marks)

**(a)** *(4)* For which values of $b$ is

$$S = \begin{bmatrix}2&1&0\\ 1&2&1\\ 0&1&b\end{bmatrix}$$

positive definite? **At the boundary value**, give a nonzero $x$ with $x^\mathsf{T}Sx = 0$.

**(b)** *(6)* Let $T = \begin{bmatrix}21&-12\\-12&14\end{bmatrix}$. Find its eigenvalues and **orthonormal** eigenvectors, write $T = Q\Lambda Q^\mathsf{T}$ with $Q$ **exact**, and write $T$ as a weighted sum of two projection matrices.

**(c)** *(4)* Write $21x^2 - 24xy + 14y^2$ as a sum of two squares **with the pivots of $T$ as coefficients**. Then describe the curve $21x^2 - 24xy + 14y^2 = 1$: its shape, its axis directions, its semi-axis lengths, and **how the ratio of the axes relates to $\operatorname{cond}_2(T)$.**

---

## Q7 · The Singular Value Decomposition (14 marks)

$$A = \begin{bmatrix}12&14\\ 21&12\end{bmatrix}$$

**(a)** *(6)* Compute $A^\mathsf{T}A$ and the singular values of $A$. Find $v_1, v_2$, then **$u_k = Av_k/\sigma_k$**, and write $A = U\Sigma V^\mathsf{T}$ with every entry exact.

**(b)** *(2)* Find $\det U$ and $\det V$. **What does each say geometrically**, and how do they account for the sign of $\det A$?

**(c)** *(3)* Give the best rank-one approximation $A_1$ as a matrix, and $\lVert A - A_1\rVert_2$ and $\lVert A - A_1\rVert_F$. **Name the theorem.**

**(d)** *(3)* Find the eigenvalues of $A$. **Are they its singular values?** Check the inequality that relates the two lists, and give $\operatorname{cond}_2(A)$.

---

## Q8 · Applications (12 marks)

**(a)** *(5)* **PCA.** The six points $(4,3)$, $(-4,-3)$, $(4,3)$, $(-4,-3)$, $(-3,4)$, $(3,-4)$ are the rows of $D$.

- Compute $D^\mathsf{T}D$ and find the two principal directions and the fraction of variance each explains.
- Give the total squared perpendicular distance from the points to the first principal line.
- The least-squares line $y = mx$ through the same points has $m = \tfrac{12}{41}$. **Why is it so much flatter than the first principal line?** One sentence.

**(b)** *(4)* **PageRank.** Two pages link only to each other.

- Without damping, the Markov matrix is $P = \begin{bmatrix}0&1\\1&0\end{bmatrix}$. **What does power iteration do, and why?**
- With damping $\alpha = \tfrac45$, write $G$, find its eigenvalues and PageRank vector, and **say what power iteration does now.**

**(c)** *(3)* **Fourier.** For the square wave ($+1$ on $(0,\pi)$, $-1$ on $(\pi, 2\pi)$), the term $\tfrac4\pi\sin t$ alone captures $8/\pi^2 \approx 81\%$ of the energy, and the partial sums' squared error tends to zero. **Yet the largest value of the partial sums stays near $1.179$ however many terms are kept. Explain in two sentences why both statements are true.**

---

## Mark Distribution

| Section | Q | Topic | Marks |
|---|---|---|---:|
| A | 1 | Elimination and $LU$ | 12 |
| A | 2 | The four subspaces | 12 |
| A | 3 | Determinants and eigenvalues | 10 |
| B | 4 | Diagonalisation and powers | 12 |
| B | 5 | Orthogonality and least squares | 14 |
| C | 6 | Symmetric and positive definite matrices | 14 |
| C | 7 | The singular value decomposition | 14 |
| C | 8 | Applications | 12 |
| | | **Total** | **100** |

---

*MATH 241 · Final Examination · © CSE Department*
