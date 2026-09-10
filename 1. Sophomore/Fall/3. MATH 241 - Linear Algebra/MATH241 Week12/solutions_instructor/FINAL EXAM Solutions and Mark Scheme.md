# MATH 241 · Final Examination — Solutions and Mark Scheme
## Instructor Only

**Do not distribute.** Every number below is asserted by `final_check.py` in this folder — **81 checks, all exact except where a question's answer is irrational**. Run it before marking; if it completes, the arithmetic here is right.

---

## Marking Principles

1. **Method carries the marks.** A correct method with one arithmetic slip loses one mark per slip, not the part.
2. **Checks earn marks.** The paper tells candidates to show trace, determinant and orthogonality checks. **Reward a check that catches an error even when the final answer is wrong.**
3. **Do not double-penalise.** An error in Q7(a) carried correctly into (c) and (d) loses marks once.
4. **Accept any correct sign or ordering convention** for eigenvectors and singular vectors, provided it is consistent — **$U\Sigma V^\mathsf{T}$ must multiply back to $A$.**
5. **Where a part asks for one sentence**, a correct sentence scores full; a paragraph that contains the sentence also scores full; a paragraph that does not, scores zero.

---

# Section A

## Q1 · Elimination and $LU$ (12)

**(a)** *(5)* Multipliers $\ell_{21} = 3$, $\ell_{31} = -2$ give rows $(0, 1, 4)$ and $(0, 3, 7)$; then $\ell_{32} = 3$ gives $(0, 0, -5)$.

$$L = \begin{bmatrix}1&0&0\\3&1&0\\-2&3&1\end{bmatrix}, \qquad U = \begin{bmatrix}2&1&-1\\0&1&4\\0&0&-5\end{bmatrix}, \qquad \det A = 2\cdot1\cdot(-5) = -10.$$

*3 for the multipliers and $U$, 1 for $L$, 1 for $\det$. **The multiplier sign convention must match $L$** — $\ell_{31} = -2$ because row 3 had $2\times$ row 1 **added**.*

**(b)** *(4)* $Lc = b$: $c_1 = -1$; $c_2 = 4 - 3(-1) = 7$; $c_3 = 13 - (-2)(-1) - 3(7) = -10$. So $c = (-1, 7, -10)$.

$Ux = c$: $x_3 = -10/-5 = 2$; $x_2 = 7 - 4\cdot2 = -1$; $x_1 = \tfrac12(-1 - (-1) + 2) = 1$.

$$x = (1, -1, 2) \qquad (\text{check: } Ax = (2 - 1 - 2,\ 6 - 4 + 2,\ -4 - 1 + 18) = (-1, 4, 13)\ ✓)$$

*2 for $c$, 2 for $x$. Solving $Ax = b$ by fresh elimination scores 2 of 4.*

**(c)** *(3)* The multiplier is $10^{20}$, and the new $(2,2)$ entry is $1 - 10^{20}$. **That subtraction rounds to exactly $-10^{20}$** — the $1$ is below the rounding of a number that size — **so the matrix entry that carried the information is gone.** Back substitution then gives $x_2 = 1.0$ and $x_1 = (1 - x_2)/10^{-20} = 0.0$. *(Verified in `final_check.py`.)* **Partial pivoting swaps the rows first**, so the multiplier is $10^{-20}$ and the new entry $1 - 10^{-20}$ rounds harmlessly to $1$.

*1 for locating the loss at the $(2,2)$ update, 1 for "absorbed/rounded away", 1 for pivoting's effect. **"Division by a small number" alone scores 1** — the division is not where the information is lost. (Week 0's L03 §4.)*

---

## Q2 · The Four Subspaces (12)

**(a)** *(4)*

$$R = \begin{bmatrix}1&2&0&1\\0&0&1&2\\0&0&0&0\end{bmatrix}, \qquad \operatorname{rank}B = 2.$$

$\mathbf{C}(B)$: **pivot columns of $B$** (columns 1 and 3), $(1,2,3)$ and $(0,1,1)$. $\mathbf{N}(B)$: free variables $x_2, x_4$ give $(-2,1,0,0)$ and $(-1,0,-2,1)$.

*1 rref, 1 rank, 1 each basis. **Pivot columns of $R$ instead of $B$ for $\mathbf{C}(B)$ loses 1.***

**(b)** *(3)* $y = (1, 1, -1)$: row 1 + row 2 − row 3 $= 0$. Dimensions: $\mathbf{C}(B)$ $2$, $\mathbf{N}(B^\mathsf{T})$ $1$, $\mathbf{C}(B^\mathsf{T})$ $2$, $\mathbf{N}(B)$ $2$.

$$2 + 1 = 3 = m, \qquad 2 + 2 = 4 = n.$$

*1, 1, 1.*

**(c)** *(3)* **$b_1 + b_2 - b_3 = 0$** — $b$ must be orthogonal to $\mathbf{N}(B^\mathsf{T})$. $(1,1,2)$: $1 + 1 - 2 = 0$, **reachable**. $(1,1,1)$: $1 \ne 0$, **not reachable**.

*1, 1, 1.*

**(d)** *(2)* **Yes** — it is the second nonzero row of $R$, and elimination's row operations keep every row of $R$ inside the row space of $B$.

---

## Q3 · Determinants and Eigenvalues (10)

**(a)** *(2)* **Triangular, so the determinant is the product of the diagonal**: $2\cdot3\cdot1\cdot4 = 24$.

**(b)** *(4)* $\lambda^2 - 7\lambda + 10 = (\lambda - 5)(\lambda - 2)$.

$$\lambda = 5:\ (1, 1), \qquad \lambda = 2:\ (1, -2). \qquad 5 + 2 = 7 = \operatorname{trace},\ \ 5\cdot2 = 10 = \det\ ✓$$

*2 eigenvalues with check, 2 eigenvectors.*

**(c)** *(4)* $\det(2C^{-1}) = 2^2\cdot\dfrac{1}{\det C} = \dfrac{4}{10} = \dfrac25$. **$C^3 + I$ has the same eigenvectors** and eigenvalues $5^3 + 1 = 126$ and $2^3 + 1 = 9$, so $\det(C^3 + I) = 1134$.

*1 for $\det(2C^{-1})$ — **$2\cdot\tfrac1{10}$ is the standard error; the factor is $2^n$**. 2 for the eigenvalues, 1 for the determinant.*

---

# Section B

## Q4 · Diagonalisation and Powers (12)

**(a)** *(3)* **The columns sum to $1$**, so $(1,1)M = (1,1)$: $(1,1)$ is an eigenvector of $M^\mathsf{T}$ with $\lambda = 1$, and $M$ and $M^\mathsf{T}$ have the same eigenvalues. **The other is $\operatorname{trace} - 1 = \tfrac32 - 1 = \tfrac12$.**

**(b)** *(5)* $M(3,2) = (3,2)$ and $M(1,-1) = \tfrac12(1,-1)$:

$$S = \begin{bmatrix}3&1\\2&-1\end{bmatrix}, \quad \Lambda = \begin{bmatrix}1&0\\0&\tfrac12\end{bmatrix}, \quad S^{-1} = \frac15\begin{bmatrix}1&1\\2&-3\end{bmatrix},$$

$$M^k = S\Lambda^kS^{-1} = \frac15\begin{bmatrix}3 + 2\cdot2^{-k} & 3 - 3\cdot2^{-k}\\ 2 - 2\cdot2^{-k} & 2 + 3\cdot2^{-k}\end{bmatrix} \ \longrightarrow\ \frac15\begin{bmatrix}3&3\\2&2\end{bmatrix}.$$

*(Checked exactly for $k = 1, \dots, 8$ against repeated multiplication.)*

*2 for $S$ and $\Lambda$, 2 for $M^k$, 1 for the limit. **The limit's columns are the steady state $(\tfrac35, \tfrac25)$** — reward saying so.*

**(c)** *(2)* The largest error entry is $\tfrac35\cdot2^{-k}$. $\tfrac35\cdot2^{-k} \le 10^{-6} \iff 2^k \ge 600{,}000$. $2^{19} = 524{,}288$ is too small; $2^{20} = 1{,}048{,}576$ is enough. **$k = 20$.** *(Errors $1.144\times10^{-6}$ at $k = 19$, $5.722\times10^{-7}$ at $k = 20$.)*

**(d)** *(2)* $\lambda = 3$ is a double root, but $A - 3I = \begin{bmatrix}0&1\\0&0\end{bmatrix}$ has rank $1$, so **the eigenspace is one-dimensional** — one independent eigenvector where two are needed for $S$.

---

## Q5 · Orthogonality and Least Squares (14)

**(a)** *(5)*

$$A = \begin{bmatrix}1&-1\\1&0\\1&1\\1&2\end{bmatrix}, \quad y = \begin{bmatrix}0\\1\\3\\4\end{bmatrix}, \quad A^\mathsf{T}A = \begin{bmatrix}4&2\\2&6\end{bmatrix}, \quad A^\mathsf{T}y = \begin{bmatrix}8\\11\end{bmatrix}, \quad \hat x = \left(\tfrac{13}{10},\ \tfrac75\right).$$

*2 for $A$ and $y$ (**unknowns in $\hat x$, data in $A$** — Week 9's one conceptual step), 2 for the normal equations, 1 for $\hat x$.*

**(b)** *(3)* Fitted values $(-\tfrac1{10}, \tfrac{13}{10}, \tfrac{27}{10}, \tfrac{41}{10})$, so

$$e = \left(\tfrac1{10},\ -\tfrac3{10},\ \tfrac3{10},\ -\tfrac1{10}\right), \quad A^\mathsf{T}e = 0\ ✓, \quad \lVert e\rVert^2 = \tfrac{20}{100} = \tfrac15.$$

Centroid $(\tfrac12, 2)$: $\tfrac{13}{10} + \tfrac75\cdot\tfrac12 = 2$ ✓.

**(c)** *(4)* $q_1 = \tfrac12(1,1,1,1)$. $a_2 - (q_1\cdot a_2)q_1 = (-1,0,1,2) - 1\cdot\tfrac12(1,1,1,1) = (-\tfrac32, -\tfrac12, \tfrac12, \tfrac32)$, of length $\sqrt5$, so $q_2 = \tfrac{1}{2\sqrt5}(-3,-1,1,3)$.

$$R = \begin{bmatrix}2 & 1\\ 0 & \sqrt5\end{bmatrix}, \qquad Q^\mathsf{T}y = \left(4,\ \tfrac{14}{2\sqrt5}\right) = \left(4,\ \tfrac{7}{\sqrt5}\right).$$

Back substitution: $\sqrt5\,d = 7/\sqrt5$ gives $d = \tfrac75$; $2c + d = 4$ gives $c = \tfrac{13}{10}$ ✓.

*2 for $Q$, 1 for $R$, 1 for the solve. **$\sqrt5$ is irrational and must stay symbolic**; decimals that reproduce $\hat x$ to three figures score full.*

**(d)** *(2)* $\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$ — **forming $A^\mathsf{T}A$ doubles the digits lost**, and can make an independent-column problem exactly singular in floating point (Week 9's Läuchli matrix).

---

# Section C

## Q6 · Symmetric and Positive Definite Matrices (14)

**(a)** *(4)* Leading minors $2$, $3$, $\det S = 2(2b - 1) - b = 3b - 2$. **Positive definite exactly when $b > \tfrac23$.** At $b = \tfrac23$: $x = (1, -2, 3)$ gives $Sx = (0, 0, 0)$, so $x^\mathsf{T}Sx = 0$.

*1 minors, 1 threshold, 2 for the vector. **Any nonzero multiple of $(1,-2,3)$.** "$b \ge \tfrac23$" loses 1.*

**(b)** *(6)* Trace $35$, determinant $294 - 144 = 150$: $\lambda = 5, 30$.

$$T(3,4) = (15, 20) = 5(3,4), \qquad T(-4,3) = (-120, 90) = 30(-4,3).$$

$$Q = \frac15\begin{bmatrix}3&-4\\4&3\end{bmatrix}, \quad \Lambda = \begin{bmatrix}5&0\\0&30\end{bmatrix}, \quad T = 5\cdot\frac1{25}\begin{bmatrix}9&12\\12&16\end{bmatrix} + 30\cdot\frac1{25}\begin{bmatrix}16&-12\\-12&9\end{bmatrix}.$$

*2 eigenvalues, 2 orthonormal eigenvectors, 1 $Q\Lambda Q^\mathsf{T}$, 1 projections. **Unnormalised eigenvectors in $Q$ lose 1.** Verified exactly.*

**(c)** *(4)* Pivots $21$ and $14 - \tfrac{144}{21} = \tfrac{50}{7}$, multiplier $-\tfrac47$:

$$21x^2 - 24xy + 14y^2 = 21\left(x - \tfrac47y\right)^2 + \tfrac{50}{7}y^2.$$

*(Checked at $(1,1)$, $(2,-3)$, $(7,4)$: $11$, $354$, $581$.)* **An ellipse**, axes along $(3,4)$ and $(-4,3)$, semi-axes $1/\sqrt5$ and $1/\sqrt{30}$. **Axis ratio $\sqrt{30/5} = \sqrt6 = \sqrt{\operatorname{cond}_2(T)}$.**

*2 for the squares, 1 for the ellipse, 1 for the ratio. **Semi-axes $\sqrt5$, $\sqrt{30}$ (inverted) lose 1** — the most common slip on this material.*

---

## Q7 · The Singular Value Decomposition (14)

**(a)** *(6)*

$$A^\mathsf{T}A = \begin{bmatrix}585&420\\420&340\end{bmatrix}, \quad \operatorname{trace} 925,\ \det 22{,}500 \ \Longrightarrow\ \lambda = 900, 25, \quad \sigma_1 = 30,\ \sigma_2 = 5.$$

$A^\mathsf{T}A - 900I = \begin{bmatrix}-315&420\\420&-560\end{bmatrix}$, rows proportional to $(-3,4)$, so $v_1 = \tfrac15(4,3)$ and $v_2 = \tfrac15(-3,4)$.

$$u_1 = \frac{Av_1}{30} = \frac{1}{150}(90, 120) = \tfrac15(3,4), \qquad u_2 = \frac{Av_2}{5} = \frac1{25}(20, -15) = \tfrac15(4,-3).$$

$$A = \underbrace{\frac15\begin{bmatrix}3&4\\4&-3\end{bmatrix}}_{U}\begin{bmatrix}30&0\\0&5\end{bmatrix}\underbrace{\frac15\begin{bmatrix}4&3\\-3&4\end{bmatrix}}_{V^\mathsf{T}}$$

*2 $A^\mathsf{T}A$ and $\sigma$'s, 2 $v$'s, 1 $u$'s, 1 product. **Sign-consistent alternatives score full if they multiply back to $A$.***

**(b)** *(2)* **$\det U = -1$: a reflection. $\det V = +1$: a rotation.** $\det A = \det U\cdot\det\Sigma\cdot\det V^\mathsf{T} = (-1)(150)(1) = -150$ ✓ — **the negative determinant is carried entirely by the reflection in $U$**, since $\Sigma$'s entries are never negative.

**(c)** *(3)* $A_1 = 30u_1v_1^\mathsf{T} = \tfrac65\begin{bmatrix}12&9\\16&12\end{bmatrix} = \begin{bmatrix}\tfrac{72}5 & \tfrac{54}5\\[2pt] \tfrac{96}5 & \tfrac{72}5\end{bmatrix}$; $\lVert A - A_1\rVert_2 = \lVert A - A_1\rVert_F = \sigma_2 = 5$. **Eckart–Young.**

**(d)** *(3)* $\lambda^2 - 24\lambda - 150 = 0$: $\lambda = 12 \pm \sqrt{294} \approx 29.146,\ -5.146$. **Not the singular values** ($30$, $5$), though real here. **$\sigma_\min \le \lvert\lambda\rvert \le \sigma_\max$: $5 \le 5.146$ and $29.146 \le 30$** ✓. $\operatorname{cond}_2(A) = 30/5 = 6$.

*1 eigenvalues, 1 inequality checked, 1 cond. **Using $\lvert\lambda\rvert$ as $\sigma$ loses the part.***

---

## Q8 · Applications (12)

**(a)** *(5)*

$$D^\mathsf{T}D = \begin{bmatrix}82&24\\24&68\end{bmatrix}, \qquad D^\mathsf{T}D(4,3) = 100(4,3), \qquad D^\mathsf{T}D(-3,4) = 50(-3,4).$$

**Directions $\tfrac15(4,3)$ and $\tfrac15(-3,4)$, explaining $\tfrac{100}{150} = \tfrac23$ and $\tfrac13$.** Squared distances to the first line: four points at $0$, two at $5^2$ — **total $50 = \sigma_2^2$**.

**Why the regression line is flatter** (slope $\tfrac{12}{41} \approx 0.29$ against $\tfrac34$): **regression counts vertical error, so the two points $(\mp3, \pm4)$ sitting far above and below the principal line drag its slope down; PCA counts perpendicular distance, to which those points are symmetric about the principal line.**

*2 directions, 1 fractions, 1 distance, 1 sentence.*

**(b)** *(4)* **Undamped:** eigenvalues $1$ and $-1$; from $(1,0)$ the iterates alternate $(0,1), (1,0), \dots$ **forever, because $\lvert\lambda_2\rvert = 1$ and nothing decays.**

**Damped:** $G = \tfrac45P + \tfrac1{10}\mathbf{1}\mathbf{1}^\mathsf{T} = \begin{bmatrix}\tfrac1{10}&\tfrac9{10}\\[2pt]\tfrac9{10}&\tfrac1{10}\end{bmatrix}$, eigenvalues $1$ (eigenvector $(1,1)$) and $-\tfrac45$ (eigenvector $(1,-1)$). **PageRank $(\tfrac12, \tfrac12)$. Power iteration now converges, with the error flipping sign and shrinking by $\tfrac45$ each step.**

*2 undamped (1 behaviour, 1 reason), 2 damped (1 $G$ and eigenvalues, 1 behaviour). Verified: $G(1,-1) = -\tfrac45(1,-1)$.*

**(c)** *(3)* **Partial sums are orthogonal projections, which minimise squared error — the integral of the error squared — and that integral tends to zero** (Pythagoras: it is the energy in the discarded coefficients; three nonzero terms already keep $93.31\%$). **The overshoot near the jump keeps its height but gets narrower, so it contributes less and less area while its peak stays at about $1.179$** — the Gibbs phenomenon.

*2 for "projection minimises the squared error, which tends to zero", 1 for the narrowing spike. **"The series does not converge" scores 0** — it converges in the squared-error sense, and saying which sense is the question.*

---

## Grade Distribution Expected

| Band | Score | Description |
|---|---|---|
| Strong | 85–100 | Section C substantially complete; Q1(c), Q7(b) and Q8(c) explained, not just computed |
| Solid | 70–84 | Sections A and B correct with checks; Q6 and Q7(a) correct |
| Passing | 50–69 | Mechanical parts of every question; weak on (c)/(d) explanations |
| Concerning | < 50 | **Q7(a) not attempted or not multiplied back.** The SVD is the course's most-used result downstream |

---

*MATH 241 · Final Examination · Solutions and Mark Scheme · © CSE Department*
