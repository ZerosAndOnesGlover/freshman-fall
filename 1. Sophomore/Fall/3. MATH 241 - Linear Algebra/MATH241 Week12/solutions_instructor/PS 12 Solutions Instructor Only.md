# MATH 241 · Problem Set 12 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Exact throughout.** Every figure was checked in `Fraction` — Q1's matrix, eigenvectors, scores and both residual sums; Q2's two exact PageRank vectors, both characteristic polynomials, and their roots — or, for Q3, against a $20{,}000$-sample numerical projection and a $10^6$-term partial sum of $\sum 1/k^2$.

**What this paper is testing.** It is short and it is synthesis. **Q1(d) and Q2(d) are the two parts that need a sentence rather than arithmetic**, and they are the parts to read carefully. **Q3(c) is the one students remember** — the Basel sum falling out of Pythagoras is the most compact demonstration in the course that Week 8's theorems work in a function space.

**Common failure modes:** (1) Q1(d) including an intercept, which is harmless but costs time, or omitting centring and then including nothing; (2) Q2(a) writing $P$ with rows and columns swapped — **columns must sum to $1$**; (3) Q2(c) assuming the eigenvalues of $G$ are those of $P$ unchanged; (4) Q3(b) losing the sign $(-1)^{k+1}$.

---

## Q1: PCA and Regression on Four Points (30 points)

### (a) [4]

Column sums $6 - 6 - 4 + 4 = 0$ and $8 - 8 + 3 - 3 = 0$ ✓.

$$D^\mathsf{T}D = \begin{bmatrix}36 + 36 + 16 + 16 & 48 + 48 - 12 - 12\\ 72 & 64 + 64 + 9 + 9\end{bmatrix} = \begin{bmatrix}104&72\\72&146\end{bmatrix}.$$

### (b) [8]

$$D^\mathsf{T}D\begin{bmatrix}3\\4\end{bmatrix} = \begin{bmatrix}600\\800\end{bmatrix} = 200\begin{bmatrix}3\\4\end{bmatrix}, \qquad D^\mathsf{T}D\begin{bmatrix}-4\\3\end{bmatrix} = \begin{bmatrix}-200\\150\end{bmatrix} = 50\begin{bmatrix}-4\\3\end{bmatrix}.$$

*(Checks: trace $250 = 200 + 50$; determinant $104\cdot146 - 72^2 = 10{,}000 = 200\cdot50$.)*

| | direction | $\sigma$ | variance explained |
|---|---|---:|---:|
| first | $\tfrac15(3,4)$ | $\sqrt{200} = 10\sqrt2$ | $200/250 = \mathbf{80\%}$ |
| second | $\tfrac15(-4,3)$ | $\sqrt{50} = 5\sqrt2$ | $\mathbf{20\%}$ |

*Marking: 3 for the eigen-verification, 2 for directions and $\sigma$'s, 3 for the fractions. **Singular values are the square roots**; giving $200$ and $50$ as $\sigma$'s loses 2.*

### (c) [8]

| point | score $x\cdot\tfrac15(3,4)$ | coordinate along $\tfrac15(-4,3)$ | squared distance to first line |
|---|---:|---:|---:|
| $(6, 8)$ | $10$ | $0$ | $0$ |
| $(-6, -8)$ | $-10$ | $0$ | $0$ |
| $(-4, 3)$ | $0$ | $5$ | $25$ |
| $(4, -3)$ | $0$ | $-5$ | $25$ |

**Sum $50 = \sigma_2^2$** ✓. **Eckart–Young at rank one** (Week 11's L35 §1 and §5): the error of the best rank-one approximation in the Frobenius norm is $\sqrt{\sigma_2^2}$, and for centred data that squared error is exactly the total squared perpendicular distance to the first principal line.

*Marking: 3 scores, 3 distances, 2 for naming Eckart–Young (accept "PCA is the SVD of the centred data, and the discarded energy is $\sigma_2^2$").*

### (d) [10]

$$m = \frac{\sum x_iy_i}{\sum x_i^2} = \frac{72}{104} = \boxed{\tfrac{9}{13} \approx 0.6923} \qquad\text{against the principal line's slope } \tfrac43 \approx 1.3333.$$

**The lines are $18.43°$ apart.**

**Which points:** $(-4, 3)$ and $(4, -3)$. **Regression measures error vertically**, so these two points — far below and above the principal line in the $y$ direction — pull hard on the slope and flatten it. **PCA measures perpendicular distance**, and to it these points are simply the second direction, sitting symmetrically about the first line and exerting no net pull. The points $(\pm6, \pm8)$ lie exactly on the principal line and so contribute no perpendicular error at all, but they do contribute vertical error to any flatter line.

| line | squared **vertical** distances | squared **perpendicular** distances |
|---|---:|---:|
| regression, $m = \tfrac9{13}$ | $\mathbf{\tfrac{1250}{13} \approx 96.15}$ | $65$ |
| principal line, slope $\tfrac43$ | $\tfrac{1250}{9} \approx 138.89$ | $\mathbf{50}$ |

**Each wins the contest it was built for** — L36 §5, in four points.

*Marking: 2 for $m$, 3 for identifying the two points with a reason, 4 for the table, 1 for the verdict. **The perpendicular distance to the regression line is the vertical distance times $1/\sqrt{1 + m^2}$** — accept either route, and accept the value to two decimals.*

---

## Q2: PageRank on Three Pages (30 points)

### (a) [6]

Column $j$ spreads page $j$'s vote over its out-links:

$$P = \begin{bmatrix}0 & \tfrac12 & 1\\ 1 & 0 & 0\\ 0 & \tfrac12 & 0\end{bmatrix}.$$

$Px = x$: $x_1 = x_0$, $x_2 = \tfrac12x_1$, and $x_0 = \tfrac12x_1 + x_2 = x_1$ (consistent). With the sum equal to $1$:

$$\boxed{x = \left(\tfrac25,\ \tfrac25,\ \tfrac15\right)}.$$

*Marking: 3 for $P$ (**columns sum to $1$** — a row-stochastic $P$ loses all 3 and should be flagged prominently), 3 for $x$.*

### (b) [8]

$$\det(\lambda I - P) = \lambda^3 - \tfrac12\lambda - \tfrac12 = (\lambda - 1)\left(\lambda^2 + \lambda + \tfrac12\right),$$

and $\lambda^2 + \lambda + \tfrac12 = 0$ gives

$$\lambda = -\tfrac12 \pm \tfrac12 i, \qquad \lvert\lambda\rvert = \tfrac{1}{\sqrt2} \approx 0.7071.$$

**Yes, it converges** — both other eigenvalues have modulus less than $1$ — **at rate $(1/\sqrt2)^k$**, halving the error every two steps. **Because the pair is complex, the error spirals**: it does not shrink by the same factor each step. *(From $(1,0,0)$ the iterates are $(0,1,0)$, $(\tfrac12,0,\tfrac12)$, $(\tfrac12,\tfrac12,0)$, $(\tfrac14,\tfrac12,\tfrac14)$, $(\tfrac12,\tfrac14,\tfrac14)$, …, with $L^1$ error $1.2, 0.8, 0.4, 0.3, 0.3$ — visibly not geometric step by step — reaching $4.9\times10^{-5}$ at step $30$.)*

*Marking: 3 for the factorisation, 2 for the eigenvalues, 3 for convergence, rate, and the spiral. **"Converges because it is a Markov matrix" earns 0 for that part** — L37 §5 exhibits a Markov matrix for which it does not.*

### (c) [10]

**Proof.** $Gw = \tfrac45Pw + \tfrac1{15}\mathbf{1}(\mathbf{1}^\mathsf{T}w) = \tfrac45Pw$ whenever $\mathbf{1}^\mathsf{T}w = 0$.

*The bonus:* if $Pw = \mu w$, apply $\mathbf{1}^\mathsf{T}$ to both sides. The columns of $P$ sum to $1$, so $\mathbf{1}^\mathsf{T}P = \mathbf{1}^\mathsf{T}$, and the left side is $\mathbf{1}^\mathsf{T}w$. Hence $\mathbf{1}^\mathsf{T}w = \mu\,\mathbf{1}^\mathsf{T}w$, so $(1 - \mu)\,\mathbf{1}^\mathsf{T}w = 0$, and $\mu \ne 1$ forces $\mathbf{1}^\mathsf{T}w = 0$.

**So for every eigenvector of $P$ with $\mu \ne 1$, $Gw = \tfrac45Pw = \tfrac45\mu w$.** $\square$

**Eigenvalues of $G$:** $1$ and $\tfrac45\left(-\tfrac12 \pm \tfrac12i\right) = -\tfrac25 \pm \tfrac25i$, with $\lvert\lambda_2(G)\rvert = \tfrac{2\sqrt2}{5} \approx 0.5657$. *(Confirmed: $\det(\lambda I - G) = \lambda^3 - \tfrac15\lambda^2 - \tfrac{12}{25}\lambda - \tfrac{8}{25}$, whose roots are exactly these.)*

$$G = \frac{1}{15}\begin{bmatrix}1 & 7 & 13\\ 13 & 1 & 1\\ 1 & 7 & 1\end{bmatrix}, \qquad \boxed{x = \left(\tfrac{21}{53},\ \tfrac{61}{159},\ \tfrac{35}{159}\right) \approx (0.3962,\ 0.3836,\ 0.2201)}, \qquad Gx = x\ ✓$$

*Marking: 4 proof (bonus 1 for the eigenvector-sum argument), 2 eigenvalues, 4 for the exact $x$. **Accept $\tfrac{63}{159}$ for $\tfrac{21}{53}$.***

### (d) [6]

**Page $0$ moves ahead of page $1$** ($0.3962$ against $0.3836$).

**Why, in terms of links:** undamped, all of page $0$'s vote goes to page $1$, and all of page $1$'s vote comes back to page $0$ — half directly, half by way of page $2$. The two pages sit on one loop and must carry equal weight.

**Damping gives every page a uniform share of $\tfrac1{15}$ per step, and what a page does with its share depends on its out-links.** **Page $2$ is a funnel**: its only out-link is to page $0$, so the uniform share that lands on page $2$ is passed on, damped once, to page $0$ alone. **No page funnels into page $1$** except page $0$ itself. Page $2$'s weight rises from $0.20$ to $0.22$ under damping, and that extra weight flows to page $0$ — which is why page $0$ ends ahead.

*Marking: 2 for the direction, 4 for a link-based explanation. **An explanation that only recomputes the numbers scores 2 of the 4.** Accept any argument that correctly identifies page $2$ as passing its whole share to page $0$.*

---

## Q3: Fourier, and a Famous Sum (25 points)

### (a) [4]

$f(t) = t$ is **odd** and $\cos kt$ is **even**, so their product is odd and its integral over the symmetric interval $(-\pi, \pi)$ is zero. $\square$

### (b) [8]

$\langle\sin kt, \sin kt\rangle = \int_{-\pi}^{\pi}\sin^2kt\,dt = \pi$. And

$$\int_{-\pi}^{\pi}t\sin kt\,dt = \left[-\frac{t\cos kt}{k}\right]_{-\pi}^{\pi} + \frac1k\int_{-\pi}^{\pi}\cos kt\,dt = -\frac{2\pi\cos k\pi}{k} + 0 = \frac{2\pi(-1)^{k+1}}{k}.$$

$$b_k = \frac{2\pi(-1)^{k+1}/k}{\pi} = \frac{2(-1)^{k+1}}{k}\ \square \qquad (b_1 = 2,\ b_2 = -1,\ b_3 = \tfrac23,\ \dots)$$

*(Numerical check: projection from $20{,}000$ samples gives $+2.000000$, $-1.000000$, $+0.666667$, $-0.500000$, $+0.400000$.)*

*Marking: 2 for $\lVert\sin kt\rVert^2 = \pi$, 4 for the integration by parts, 2 for the sign.*

### (c) [8]

$$\lVert f\rVert^2 = \int_{-\pi}^{\pi}t^2\,dt = \frac{2\pi^3}{3}, \qquad \sum_kb_k^2\,\pi = \pi\sum_k\frac{4}{k^2}.$$

$$\frac{2\pi^3}{3} = 4\pi\sum_k\frac1{k^2} \quad\Longrightarrow\quad \boxed{\sum_{k=1}^\infty\frac1{k^2} = \frac{\pi^2}{6}}\ \square$$

**Worth saying on the scripts:** this is Euler's 1734 result, and here it is **Pythagoras's theorem** applied to one function in an infinite-dimensional space. *(Numerical: $\pi^2/6 = 1.6449340668$; $\sum_{k\le10^6}1/k^2 = 1.6449330668$, the missing $10^{-6}$ being the tail.)*

*Marking: 3 for each side, 2 for the deduction.*

### (d) [5]

Fraction captured by the first $K$ terms $= \dfrac{4\pi\sum_{k\le K}1/k^2}{2\pi^3/3} = \dfrac{6}{\pi^2}\displaystyle\sum_{k\le K}\frac1{k^2}$:

| $K$ | exact | percentage |
|---:|---|---:|
| $1$ | $6/\pi^2$ | $60.79\%$ |
| $3$ | $\tfrac{6}{\pi^2}\left(1 + \tfrac14 + \tfrac19\right) = \tfrac{49}{6\pi^2}$ | $82.75\%$ |
| $10$ | $\tfrac{6}{\pi^2}\sum_{k\le10}\tfrac1{k^2}$ | $94.21\%$ |

**Compare L38 §4: three DCT terms left the smooth signal with a relative error of $2.48\%$ — $1 - 0.0248^2 \approx 99.94\%$ of its energy kept. $f(t) = t$ keeps only $82.75\%$ of its energy from three terms**, because its periodic extension has a jump at $\pm\pi$, and jumps are what Fourier series are slowest at (L38 §3). *(Watch for scripts that compare an error percentage with an energy percentage; they are different quantities.)*

*Marking: 1 for the general expression, 1 each for the three rows, 1 for any sensible remark on slow decay. Accept $1.36111\cdot6/\pi^2$ for $K = 3$.*

---

## Q4: The Course in One Table (15 points)

### (a) [8]

| | matrix / space | computed | existence from | orthogonality |
|---|---|---|---|---|
| **Regression** | design matrix $A$ | projection of $b$ onto $\mathbf{C}(A)$ | Week 8 (projection), Week 9 | yes — $QR$ or SVD |
| **PCA** | centred data $D$ | top singular vectors / variances | Weeks 10–11 (spectral theorem, SVD, Eckart–Young) | yes — $U$, $V$ |
| **PageRank** | Google matrix $G$ | $\lambda = 1$ eigenvector | Weeks 6–7, plus Perron–Frobenius | **no** |
| **Fourier** | functions with $\int fg$ | coefficients as projections | Week 8 (orthogonal expansion), Week 2 (functions are vectors) | yes — sines and cosines |

*Marking: 2 per row. **Accept any correct week attribution**; the column that matters is the last.*

### (b) [4]

**PageRank.** It needed **positivity** — every entry of $G$ positive — so that **Perron–Frobenius** makes $\lambda = 1$ simple with a positive eigenvector and $\lvert\lambda_2\rvert < 1$. **The hypothesis was engineered by damping** (L37 §5), because the raw link matrix can have $\lambda = -1$ or a repeated $\lambda = 1$.

*Marking: 1 for naming PageRank, 3 for positivity, Perron–Frobenius and damping.*

### (c) [3]

**Forming $X^\mathsf{T}X$ squares the condition number and destroys the small singular values** — in Week 9, solving least squares through the normal equations $A^\mathsf{T}A\hat x = A^\mathsf{T}b$; in L36, doing PCA through the covariance matrix $D^\mathsf{T}D/(N-1)$, which returned a **negative** variance.

*Marking: 2 for the point, 1 for naming both.*

---

## Grade Distribution Expected

| Band | Score | Description |
|---|---|---|
| Strong | 88–100 | Q1(d) and Q2(d) explained from the geometry and the links; Q3(c) clean |
| Solid | 72–87 | All computations right; Q1(d) or Q2(d) explained only by arithmetic |
| Passing | 55–71 | Q1(a)–(c), Q2(a)–(b), Q3(a)–(b) |
| Concerning | < 55 | **Q2(a) with a row-stochastic $P$.** It breaks all of Q2, and the final has a Markov matrix on it |

---

*MATH 241 · Week 12 · PS 12 Solutions · © CSE Department*
