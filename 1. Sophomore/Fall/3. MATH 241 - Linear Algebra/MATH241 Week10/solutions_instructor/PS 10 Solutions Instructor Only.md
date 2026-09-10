# MATH 241 · Problem Set 10 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Exact in Q1–Q3 and Q5**; Q4 is floating point and says so. `resources/symmetric.py` reproduces everything, and Q4 is written against it.

**What this paper is testing.** Q1 is the mechanical core and every student should score near full marks — the eigenvectors are given in all but name. **Q2 is the paper**, and Q2(d) is the single most exam-likely item of the week. **Q4(b) is the best question here**: extending the Hilbert table to $n = 14$ produces a **negative** smallest eigenvalue for a matrix that is provably positive definite, and the student has to say what that means rather than what it says. **Q5(c) is the elegant one** and the one strong students enjoy.

**Common failure modes:** (1) Q2(a) giving only $\det > 0$ and missing that all three minors are required; (2) Q2(d) producing a $2\times2$ counterexample, which cannot exist — see below; (3) Q3(b) reaching for eigenvalues when the sum of squares is already on the page; (4) Q4(b) reporting the negative eigenvalue without comment, or "fixing" it by taking an absolute value; (5) Q5(d) arguing by example.

---

## Q1: The Spectral Theorem, by Hand (24 points)

### (a) [4]

$A = A^\mathsf{T}$ by inspection. $\operatorname{trace}A = 7 + 8 + 6 = 21$; $\det A = 280$.

**Uses:** the trace must equal $\sum\lambda_i$ and the determinant $\prod\lambda_i$. **Both are free checks on (b)**, and both are Week 6 (L20 §2), valid for every matrix, not only symmetric ones.

*Marking: 1 for symmetry, 1 each for the two numbers, 1 for saying what they will check. **Computing $\det$ after finding the eigenvalues instead of before earns 0 for the last mark** — the point is the order.*

### (b) [6]

Expanding along the last row:

$$\det(A - \lambda I) = -\lambda^3 + 21\lambda^2 - 138\lambda + 280 = -\left(\lambda^3 - 21\lambda^2 + 138\lambda - 280\right).$$

Trying $\lambda = 10$: $1000 - 2100 + 1380 - 280 = 0$ ✓. Dividing out, $\lambda^2 - 11\lambda + 28 = (\lambda - 7)(\lambda - 4)$.

$$\boxed{\lambda = 10,\ 7,\ 4}$$

**Checks:** $10 + 7 + 4 = 21$ ✓ and $10\cdot7\cdot4 = 280$ ✓.

**The middle coefficient**: the three $2\times2$ principal minors are $\begin{vmatrix}7&2\\2&8\end{vmatrix} = 52$, $\begin{vmatrix}7&2\\2&6\end{vmatrix} = 38$, $\begin{vmatrix}8&0\\0&6\end{vmatrix} = 48$, and $52 + 38 + 48 = 138$ ✓ — which is also $\lambda_1\lambda_2 + \lambda_1\lambda_3 + \lambda_2\lambda_3 = 70 + 40 + 28 = 138$.

*Marking: 3 for the polynomial, 2 for the roots, 1 for the three checks. **Accept either sign convention if stated**; L20 §1 uses $(-1)^n$ leading.*

### (c) [6]

$$u_1 = (2,2,1),\quad u_2 = (1,-2,2),\quad u_3 = (2,-1,-2), \qquad Au_1 = 10u_1,\ \ Au_2 = 7u_2,\ \ Au_3 = 4u_3.$$

Verifying the second: $Au_2 = (7 - 4 + 4,\ 2 - 16 + 0,\ 2 + 0 + 12) = (7, -14, 14) = 7u_2$ ✓

$$u_1\cdot u_2 = 2 - 4 + 2 = 0, \qquad u_1\cdot u_3 = 4 - 2 - 2 = 0, \qquad u_2\cdot u_3 = 2 + 2 - 4 = 0.$$

**Guaranteed by L30 §3**: for a symmetric matrix, eigenvectors belonging to **distinct** eigenvalues are orthogonal, and $10$, $7$, $4$ are distinct. **No computation was necessary.**

*Marking: 3 for the vectors, 1 for the dot products, 2 for naming the theorem **and** the distinctness hypothesis. **A student who cites the theorem without noticing that distinctness is required loses 1** — it is the hypothesis that fails in PS 10 Q2's boundary cases.*

### (d) [4]

All three have length $3$, so

$$Q = \frac13\begin{bmatrix}2&1&2\\ 2&-2&-1\\ 1&2&-2\end{bmatrix}, \qquad \Lambda = \operatorname{diag}(10,7,4).$$

$Q^\mathsf{T}Q$: diagonal entries $\tfrac19(4+4+1) = 1$, $\tfrac19(1+4+4) = 1$, $\tfrac19(4+1+4) = 1$; off-diagonal entries are the dot products of (c), all zero. **$Q^\mathsf{T}Q = I$.**

$$Q^{-1} = Q^\mathsf{T}, \qquad \operatorname{cond}(Q) = 1.$$

*Marking: 2 for $Q$ and the exact check, 1 for $Q^{-1} = Q^\mathsf{T}$, 1 for $\operatorname{cond} = 1$. **The column order must match $\Lambda$'s** — a mismatched pair is worth 1 of the 4 and should be flagged, because it silently breaks (e).*

### (e) [4]

$$P_2 = q_2q_2^\mathsf{T} = \frac19\begin{bmatrix}1\\-2\\2\end{bmatrix}\begin{bmatrix}1&-2&2\end{bmatrix} = \frac19\begin{bmatrix}1&-2&2\\ -2&4&-4\\ 2&-4&4\end{bmatrix}.$$

$P_2^2 = P_2$ because $q_2^\mathsf{T}q_2 = 1$: $P_2^2 = q_2(q_2^\mathsf{T}q_2)q_2^\mathsf{T} = q_2q_2^\mathsf{T}$. $\operatorname{trace}P_2 = \tfrac19(1 + 4 + 4) = 1$.

**The trace counts the dimension of the subspace projected onto** — Week 8's L25 §5 — and it is $1$ because $P_2$ projects onto a **line**.

*Marking: 2 for $P_2$, 1 for the two properties, 1 for what the trace counts. **Verifying $P_2^2 = P_2$ by multiplying out nine entries is correct and earns the mark**, but the one-line argument should be shown in the returned script — it is the argument that generalises.*

---

## Q2: Five Tests (22 points)

### (a) [10]

$$D_1 = 3, \qquad D_2 = 9 - 1 = 8, \qquad D_3 = \det B(t) = 3\cdot8 - (3 - t) + t(1 - 3t) = 21 + 2t - 3t^2.$$

$D_1$ and $D_2$ are positive for every $t$, so the condition is $D_3 > 0$:

$$3t^2 - 2t - 21 < 0, \qquad t = \frac{2 \pm \sqrt{4 + 252}}{6} = \frac{2 \pm 16}{6} = 3 \ \text{ or } \ -\tfrac73.$$

$$\boxed{\;B(t) \text{ is positive definite} \iff -\tfrac73 < t < 3\;}$$

*Marking: 4 for the three minors with $t$ carried, 3 for the quadratic and its roots, 3 for the interval and the two exact endpoints. **Answering "$t < 3$" loses 3** — the interval is two-sided, and a student who only checked $t$ large has not understood that $\det$ is a downward parabola.*

### (b) [6]

| $t$ | leading minors | pivots | eigenvalues | signs |
|---:|---|---|---|:--:|
| $-\tfrac73$ | $3,\ 8,\ 0$ | $3,\ \tfrac83,\ \mathbf{0}$ | $5.33333,\ 3.66667,\ \mathbf{0}$ | $+\,+\,0$ |
| $0$ | $3,\ 8,\ 21$ | $3,\ \tfrac83,\ \tfrac{21}{8}$ | $4.41421,\ 3,\ 1.58579$ | $+\,+\,+$ |
| $3$ | $3,\ 8,\ 0$ | $3,\ \tfrac83,\ \mathbf{0}$ | $6.56155,\ 2.43845,\ \mathbf{0}$ | $+\,+\,0$ |
| $4$ | $3,\ 8,\ -19$ | $3,\ \tfrac83,\ -\tfrac{19}{8}$ | $7.44949,\ 2.55051,\ \mathbf{-1}$ | $+\,+\,-$ |

**Sylvester's law of inertia.** The signs match in every row; **the numbers never do**.

> **Worth saying to the class:** at $t = 4$ the pivots are $3$, $2.667$, $-2.375$ and the eigenvalues
> are $7.449$, $2.551$, $-1$. **Two completely different triples with the same sign pattern.** The
> law is about counting, not about values.

*Marking: 1 per row for pivots (4), 2 for naming the law. **The pivots at the two endpoints are exactly $0$, not "very small"** — a student reporting $-10^{-16}$ from a float computation should be told to eliminate by hand; the exercise is exact.*

### (c) [3]

At $t = 3$, $B = \begin{bmatrix}3&1&3\\1&3&1\\3&1&3\end{bmatrix}$, whose **first and third rows are equal**. So

$$x = (1, 0, -1) \quad\Longrightarrow\quad Bx = (3-3,\ 1-1,\ 3-3) = 0 \quad\Longrightarrow\quad x^\mathsf{T}Bx = 0.$$

**$x \in \mathbf{N}(B)$** (Week 2), and equivalently **$x$ is an eigenvector for $\lambda = 0$** (Week 6) — the two statements are the same statement, which is L19 §3's observation.

*Marking: 1 for the vector, 1 for the null space, 1 for the eigenvalue-zero reading. **Both readings are required for full marks**; the equivalence is the content.*

### (d) [3]

$$C = \begin{bmatrix}1&2&2\\ 2&1&2\\ 2&2&1\end{bmatrix} = 2J - I.$$

**Diagonal entries all $1 > 0$.** $\det C = 5 > 0$. **Eigenvalues $5, -1, -1$** — since $J$ has eigenvalues $3, 0, 0$ — so $C$ is **indefinite**.

**Leading minors: $1$, $\mathbf{-3}$, $5$.** They half-remembered **test 4**: it requires **all** leading principal minors positive, not just the last one. **A positive determinant only says the eigenvalues have an even number of negative signs among them**, and here there are two.

> **Note for the TA:** this counterexample **cannot** be done in $2\times2$. There, $\det > 0$ plus
> $a_{11} > 0$ *does* force positive definiteness, because $D_1 = a_{11}$ and $D_2 = \det$ are the
> only two minors. **A student who produces a $2\times2$ "counterexample" has made an arithmetic
> error**, and finding it is a useful thirty seconds.

*Marking: 2 for a valid counterexample, 1 for identifying the test. **The $2\times2$ impossibility earns a bonus mention but no extra marks.***

---

## Q3: Quadratic Forms (16 points)

### (a) [8]

$$M = \begin{bmatrix}2&1&0\\ 1&2&-1\\ 0&-1&3\end{bmatrix}$$

**(off-diagonal entries are *half* the cross-term coefficients — the standard slip is to write $2$ and $-2$).**

$$L = \begin{bmatrix}1&0&0\\ \tfrac12&1&0\\ 0&-\tfrac23&1\end{bmatrix}, \qquad D = \operatorname{diag}\!\left(2,\ \tfrac32,\ \tfrac73\right), \qquad LDL^\mathsf{T} = M.$$

$$\boxed{\;f(x) = 2\left(x_1 + \tfrac12x_2\right)^2 + \tfrac32\left(x_2 - \tfrac23x_3\right)^2 + \tfrac73x_3^2\;}$$

**Checks:**

| $x$ | $f(x)$ direct | sum of squares |
|---|---:|---:|
| $(1,1,1)$ | $2+2+3+2-2 = 7$ | $2\left(\tfrac32\right)^2 + \tfrac32\left(\tfrac13\right)^2 + \tfrac73 = \tfrac92 + \tfrac16 + \tfrac73 = 7$ ✓ |
| $(2,-1,3)$ | $8+2+27-4+6 = 39$ | $2\left(\tfrac32\right)^2 + \tfrac32(-3)^2 + \tfrac73\cdot 9 = \tfrac92 + \tfrac{27}{2} + 21 = 39$ ✓ |

*Marking: 2 for $M$, 3 for $L$ and $D$, 1 for the identity, 2 for the two checks. **Writing $M$ with the full cross-coefficients loses 2 and usually breaks everything downstream** — flag it prominently on the script rather than deducting twice.*

### (b) [4]

**Yes.** All three pivots $2$, $\tfrac32$, $\tfrac73$ are positive, so $f$ is a sum of positive multiples of squares; it vanishes only when all three squares vanish, and since $L^\mathsf{T}$ is invertible that forces $x = 0$.

*Marking: 2 for "yes, positive pivots", 2 for the invertibility step. **A student who computes eigenvalues here has answered a different question correctly and gets 2** — the eigenvalues are $3.80194$, $2.44504$, $0.75302$ and cannot be found by hand, which is the point of asking.*

### (c) [4]

$N = \begin{bmatrix}3&1\\1&3\end{bmatrix}$: $N(1,1) = 4(1,1)$ and $N(1,-1) = 2(1,-1)$.

| $\lambda$ | direction | semi-axis $1/\sqrt\lambda$ |
|---:|---|---:|
| $4$ | $(1,1)/\sqrt2$ | $\tfrac12$ |
| $2$ | $(1,-1)/\sqrt2$ | $1/\sqrt2 \approx 0.70711$ |

**Aspect ratio** $= \dfrac{1/\sqrt2}{1/2} = \sqrt2 \approx 1.41421$. **$\operatorname{cond}_2(N) = 4/2 = 2$.**

$$\boxed{\;\text{aspect ratio} = \sqrt{\operatorname{cond}_2}\;}$$

*Marking: 1 directions, 1 lengths, 1 the two numbers, 1 the relationship. **The square root is the whole question**; getting $1/\sqrt\lambda$ upside down is the standard error and is worth flagging even where the ratio comes out right by accident.*

---

## Q4: On the Machine (20 points)

### (a) [6]

| $b$ | $\det A(b)$ (exact) | $\lambda_\min$ (float) |
|---|---:|---:|
| $2.1333$ | $-\tfrac{1}{2000} = -5.000000\times10^{-4}$ | $-2.077567\times10^{-5}$ |
| $\tfrac{32}{15}$ | $0$ | $+8.817996\times10^{-17}$ |
| $2.1334$ | $+\tfrac{1}{1000} = +1.000000\times10^{-3}$ | $+4.155105\times10^{-5}$ |

**Neither.** $\lambda_\min$ at $b = 2.1334$ is $4.2\times10^{-5}$, which is genuinely positive but is only about $10^{11}$ times machine epsilon relative to $\lambda_\max \approx 6.33$ — **it survives, but a student cannot see from the number alone that it would.** And at $b = 32/15$, where the true $\lambda_\min$ is **exactly $0$**, the computed value is $+8.8\times10^{-17}$: **positive, and therefore a false "yes" if read naively.**

**The exact determinant is the better instrument because it is a polynomial in $b$ with integer coefficients** — $15b - 32$ — computable with no rounding at all, and it changes sign at the exact rational $32/15$. **Week 0's L03 §7 framing:** the eigenvalue answers a question the arithmetic can only answer approximately; the determinant answers a nearby question exactly. **Ask the question you can answer.**

*Marking: 3 for the table, 3 for the paragraph. **Full marks require noticing that $b = 32/15$ gives a positive computed eigenvalue.** A student who only compares the two off-boundary rows has missed the sharpest evidence and gets 4.*

### (b) [6]

| $n$ | $\lambda_\max$ | $\lambda_\min$ | $\operatorname{cond}_2$ | $\operatorname{cond}_\infty$ (exact) |
|---:|---:|---:|---:|---:|
| $12$ | $1.79537206$ | $9.9531\times10^{-17}$ | $1.8038\times10^{16}$ | $4.1154\times10^{16}$ |
| $\mathbf{14}$ | $1.83059470$ | $\mathbf{-7.4142\times10^{-18}}$ | $\mathbf{-2.4691\times10^{17}}$ | $4.5378\times10^{19}$ |

> **This is the question on the paper.** $H_{14}$ is **provably positive definite** — every Hilbert
> matrix is, being the Gram matrix of the independent functions $1, x, \dots, x^{n-1}$ under
> $\int_0^1fg$ (PS 9 Q4(d)) — **and the computed $\lambda_\min$ is negative.** So is the computed
> condition number, which is not a number any condition number can be.

**What to say:** the computed $\lambda_\min$ is smaller in magnitude than the rounding error in the *stored entries* of $H_{14}$ — $1/3$, $1/7$, $1/11$ are not representable in binary — so **the algorithm is being asked to resolve a quantity that is not present in its input.** The sign is noise. **This is exactly L32 §5's warning about $n = 12$, one step further along, where the noise has become visible instead of merely suspected.**

**What can legitimately be concluded:** $\lvert\lambda_\min\rvert \lesssim 10^{-17}$, hence $\operatorname{cond}_2(H_{14}) \gtrsim 10^{17}$ — **a lower bound on the badness, which is all anyone needed.** The exact $\operatorname{cond}_\infty = 4.5\times10^{19}$ corroborates the order of magnitude and is the number to quote.

*Marking: 2 table, 2 for "the sign is noise, and here is why", 2 for the legitimate conclusion. **A student who takes $\lvert\lambda_\min\rvert$ and reports $\operatorname{cond}_2 = 2.5\times10^{17}$ without comment gets 2** — the arithmetic is defensible and the silence is the error.*

### (c) [8]

The two experiments reproduce as printed. On $H_8$ at $\delta = 10^{-6}$, over $200$ random symmetric perturbations:

$$\max_i\lvert\lambda_i(H_8 + E) - \lambda_i(H_8)\rvert = 8.631036\times10^{-7}, \qquad \text{ratio } 0.8631 \le 1.$$

**And $\operatorname{cond}_2(H_8) = 1.5258\times10^{10}$.**

**No contradiction, because two different problems have two different condition numbers.**

| Problem | Input | Output | Its condition number |
|---|---|---|---|
| Solve $Hx = b$ | $b$ (and $H$) | $x$ | $\operatorname{cond}_2(H) = 1.5\times10^{10}$ |
| **Find the eigenvalues of $H$** | $H$ | $\lambda_1,\dots,\lambda_n$ | **$1$, for any symmetric matrix** |

**$\operatorname{cond}_2(H)$ measures how much a perturbation of $b$ is amplified in $x$.** It says nothing about eigenvalues. **Weyl's inequality bounds the eigenvalue movement by $\lVert E\rVert$ absolutely** — no condition number appears in it at all.

> **The subtlety worth drawing out.** The bound is on the **absolute** movement.
> $\lambda_\max(H_8) \approx 1.7$ moves by at most $10^{-6}$, a **relative** error of
> $6\times10^{-7}$ — fine. But $\lambda_\min(H_8) \approx 1.1\times10^{-10}$ also moves by up
> to $10^{-6}$, which is $10^{4}$ times its own size — **it can be obliterated.** So the *small*
> eigenvalues of an
> ill-conditioned symmetric matrix have poor **relative** accuracy while the problem remains
> perfectly conditioned in the **absolute** sense. **Both statements are true and they are about
> different things**, which is why (b)'s $H_{14}$ came out negative.

*Marking: 3 for the three measurements, 3 for the two-problems distinction, 2 for the absolute-versus-relative refinement. **The refinement is a stretch item**; award the 8 to any script that gets the first two right and gestures at the third.*

---

## Q5: Proofs (18 points)

### (a) [4]

If $A$ is symmetric with every $\lambda_i = c$, then $\Lambda = cI$ and

$$A = Q(cI)Q^\mathsf{T} = c\,QQ^\mathsf{T} = cI.$$

**Non-symmetric counterexample:** $\begin{bmatrix}c&1\\0&c\end{bmatrix}$ has both eigenvalues $c$ and is not $cI$. **Week 7's word: defective** — one eigenvector where two are needed.

*Marking: 2 for the proof, 1 for the example, 1 for "defective". **The proof must go through $Q$**; "all eigenvalues equal so it's a scalar matrix" is the claim, not an argument.*

### (b) [4]

**Via eigenvalues:** $A = Q\Lambda Q^\mathsf{T}$ gives $A^{-1} = Q\Lambda^{-1}Q^\mathsf{T}$, whose eigenvalues are $1/\lambda_i > 0$. *(And $A^{-1}$ is symmetric, so the test applies.)*

**Directly:** let $x \ne 0$ and put $y = A^{-1}x$, so $y \ne 0$ since $A^{-1}$ is invertible. Then

$$x^\mathsf{T}A^{-1}x = (Ay)^\mathsf{T}A^{-1}(Ay) = y^\mathsf{T}A^\mathsf{T}y = y^\mathsf{T}Ay > 0.$$

*Marking: 2 each. **The direct argument must note $y \ne 0$** and must use $A^\mathsf{T} = A$; losing either costs 1.*

### (c) [4]

Let $x \ne 0$. Since $C$ is invertible, $Cx \ne 0$, so

$$x^\mathsf{T}(C^\mathsf{T}AC)x = (Cx)^\mathsf{T}A(Cx) > 0.$$

**And $C^\mathsf{T}AC$ is symmetric:** $(C^\mathsf{T}AC)^\mathsf{T} = C^\mathsf{T}A^\mathsf{T}C = C^\mathsf{T}AC$. $\square$

**Why L31 §7 is a special case:** take $A = I$ (positive definite) and $C$ any matrix with independent columns. Then $C^\mathsf{T}IC = C^\mathsf{T}C$, and independent columns is exactly the condition that $Cx \ne 0$ for $x \ne 0$ — **which is the only place invertibility was used.**

> **The theorem is more general than it looks.** $C$ need not be square: it needs only trivial null
> space. **That single observation covers Week 8's projections, Week 9's normal equations and Week
> 11's SVD in one line**, and it is worth putting on the board.

*Marking: 2 for the inequality, 1 for symmetry, 1 for the specialisation. **The observation that $C$ need only have trivial null space is the strong answer**; note it in the returned script even where not required.*

### (d) [3]

$A$ is $m\times n$ with $m < n$, so $A$ has more columns than rows and $\operatorname{rank}A \le m < n$. By Week 3's rank–nullity, $\dim\mathbf{N}(A) = n - \operatorname{rank}A \ge n - m > 0$, so **there is a nonzero $x$ with $Ax = 0$**, and

$$x^\mathsf{T}(A^\mathsf{T}A)x = \lVert Ax\rVert^2 = 0.$$

**Positive semidefinite, never positive definite.** $\square$

*Marking: 1 rank bound, 1 rank–nullity, 1 conclusion. **An argument by example scores 0** — the question says "using dimensions only", and the general statement is the point.*

### (e) [3]

Write $x = \sum c_kq_k$ in the orthonormal eigenbasis, which **exists because $A$ is symmetric** (L30). Then $Ax = \sum\lambda_kc_kq_k$ and, by orthonormality,

$$x^\mathsf{T}Ax = \sum_k \lambda_kc_k^2, \qquad x^\mathsf{T}x = \sum_k c_k^2,$$

so $R(x)$ is a **weighted average of the $\lambda_k$ with non-negative weights $c_k^2$ summing to $x^\mathsf{T}x$** — hence between $\lambda_\min$ and $\lambda_\max$.

**Symmetry is used twice:** to have an orthonormal eigenbasis at all, and to have real $\lambda_k$ so that "between" means anything.

**Failure without it:** $A = \begin{bmatrix}0&1\\0&0\end{bmatrix}$ has $\lambda_1 = \lambda_2 = 0$, so the bound would force $x^\mathsf{T}Ax = 0$ for every $x$ — but $x = (1,1)$ gives $x^\mathsf{T}Ax = 1$.

*Marking: 2 for the expansion and the averaging conclusion, 1 for the counterexample. **"Symmetry is used to make $A$ diagonalisable" is half the answer** — realness is the other half and is what makes the inequality meaningful.*

---

## Grade Distribution Expected

| Band | Score | Description |
|---|---|---:|
| Strong | 88–100 | Q2(d) with the $2\times2$ impossibility noticed, Q4(b) calling the negative eigenvalue noise, Q5(c)'s generalisation |
| Solid | 72–87 | Q1–Q3 correct; Q4 run and tabulated; Q5(a)–(b) complete |
| Passing | 55–71 | Q1 full, Q2(a) correct, Q3(a) correct with the halved cross-terms |
| Concerning | < 55 | **Q3(a) with unhalved off-diagonal entries**, or Q2(a) answered one-sided. Both are on the final |

---

*MATH 241 · Week 10 · PS 10 Solutions · © CSE Department*
