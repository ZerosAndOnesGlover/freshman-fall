# MATH 241 · Problem Set 8 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Exact throughout except normalisations**; `resources/orthogonal.py` reproduces Q2 and Q3.

**What this paper is testing.** Q2 is the mechanical core and is Week 9's prerequisite — a student who cannot project cannot do least squares. **Q4(d) is the best question on the paper**: substituting $A = QR$ into the normal equations and watching $A^\mathsf{T}A$ vanish is Week 9's entire algorithm, discovered rather than announced. Q5(d) asks them to connect orthonormality to Week 7's conditioning complaint, which is the reason this week exists.

**Common failure modes:** (1) $aa^\mathsf{T}$ and $a^\mathsf{T}a$ interchanged in Q2(a); (2) Q3(a) not clearing fractions, making the orthogonality check messy; (3) Q4(d) stopping at $R^\mathsf{T}R\hat x = R^\mathsf{T}Q^\mathsf{T}b$ without cancelling $R^\mathsf{T}$; (4) Q1(c)'s floor-and-wall answer asserting they *are* orthogonal.

---

## Q1: Orthogonality (20 points)

### (a) [4]

$(2,1,2)\cdot(1,2,2) = 2 + 2 + 4 = 8$; both norms are $3$; $\cos\theta = 8/9$, so $\theta = \mathbf{27.27°}$.

$(1,1,1,1)\cdot(1,-1,1,-1) = 1 - 1 + 1 - 1 = 0$, so $\theta = \mathbf{90°}$ — **answered by the dot product alone**, no norms needed.

### (b) [4]

$$\lVert x+y\rVert^2 = (x+y)^\mathsf{T}(x+y) = \lVert x\rVert^2 + 2x^\mathsf{T}y + \lVert y\rVert^2$$

**So the two sides differ by exactly $2x^\mathsf{T}y$**, which vanishes iff $x \perp y$. **Both directions at once** — the cross term does the work.

### (c) [4]

If $V \perp W$ and $v \in V \cap W$, then $v$ is orthogonal to itself: $v^\mathsf{T}v = 0$, so $\lVert v\rVert = 0$, so $v = 0$. $\square$

**Non-orthogonal but meeting only at $0$:** the $x$-axis and the line $\operatorname{span}\{(1,1,0)\}$ in $\mathbb{R}^3$ — they meet only at the origin and the angle between them is $45°$.

**Floor and wall:** they **share the line where they meet**, and a nonzero vector along that line lies in both — so it would have to be orthogonal to itself. **They meet at right angles but are not orthogonal subspaces.**

### (d) [8]

$$A = \begin{bmatrix}1&2&0\\ 0&0&1\\ 1&2&1\end{bmatrix}, \qquad \operatorname{rref}(A) = \begin{bmatrix}1&2&0\\ 0&0&1\\ 0&0&0\end{bmatrix}, \qquad r = 2$$

| Subspace | Basis | Lives in |
|---|---|---|
| $\mathbf{C}(A)$ | $(1,0,1)$, $(0,1,1)$ — **columns 1 and 3 of $A$** | $\mathbb{R}^3$ |
| $\mathbf{N}(A)$ | $(-2,1,0)$ | $\mathbb{R}^3$ |
| $\mathbf{C}(A^\mathsf{T})$ | $(1,2,0)$, $(0,0,1)$ | $\mathbb{R}^3$ |
| $\mathbf{N}(A^\mathsf{T})$ | $(-1,-1,1)$ | $\mathbb{R}^3$ |

**Orthogonality checks — $1\times2 + 1\times2 = \mathbf{4}$ dot products:**

$(-2,1,0)\cdot(1,2,0) = 0$ ✓ · $(-2,1,0)\cdot(0,0,1) = 0$ ✓
$(-1,-1,1)\cdot(1,0,1) = 0$ ✓ · $(-1,-1,1)\cdot(0,1,1) = 0$ ✓

*Marking: 4 for the four bases (1 each, ambient space stated), 3 for the checks, 1 for the count of 4. **A column-space basis taken from $\operatorname{rref}$ costs 1** — Week 2's error, still worth catching.*

---

## Q2: Projections (22 points)

### (a) [5]

$a = (1,1,1)$, $b = (4,1,1)$: $\;\hat x = \dfrac{a^\mathsf{T}b}{a^\mathsf{T}a} = \dfrac{6}{3} = 2$

$$p = (2,2,2), \qquad e = b - p = (2,-1,-1), \qquad a^\mathsf{T}e = 2 - 1 - 1 = 0\ ✓$$

$$P = \frac{aa^\mathsf{T}}{a^\mathsf{T}a} = \frac13\begin{bmatrix}1&1&1\\ 1&1&1\\ 1&1&1\end{bmatrix}, \qquad P^2 = P\ ✓, \qquad \operatorname{trace}P = 1\ ✓$$

**$\operatorname{trace}P = 1$ because the subspace is one-dimensional** — part (d).

*Marking: 3 for $\hat x$, $p$, $e$ with the check; 2 for $P$ and its properties. **Watch for $a^\mathsf{T}a$ in the numerator** — the commonest slip, and it produces a scalar where a matrix belongs.*

### (b) [9]

$$A = \begin{bmatrix}1&1\\ 0&1\\ 1&0\end{bmatrix}, \qquad A^\mathsf{T}A = \begin{bmatrix}2&1\\ 1&2\end{bmatrix}$$

**Invertible because $A$ has independent columns** — $\mathbf{N}(A^\mathsf{T}A) = \mathbf{N}(A) = \{0\}$, proved in **PS 2 Q5(c)** (Week 2), so a square matrix with trivial null space is invertible.

$$P = A(A^\mathsf{T}A)^{-1}A^\mathsf{T} = \frac13\begin{bmatrix}2&1&1\\ 1&2&-1\\ 1&-1&2\end{bmatrix}$$

$$b = (3,0,0) \;\longrightarrow\; p = (2,1,1), \qquad e = (1,-1,-1)$$

$$A^\mathsf{T}e = (1 - 0 - 1,\ 1 - 1 - 0) = (0,0)\ ✓$$

**$e \in \mathbf{N}(A^\mathsf{T})$ — the left null space.**

*Marking: 2 for $A^\mathsf{T}A$ **with the Week 2 citation**, 3 for $P$, 2 for $p$ and $e$, 2 for the verification and naming the subspace.*

### (c) [4]

$P^2 = P$ ✓ and $P^\mathsf{T} = P$ ✓ by direct computation.

**Geometric reasons:** $Pb$ already lies in $W$, so projecting again does nothing. And symmetry follows from $A^\mathsf{T}A$ being symmetric (Week 1's L06 §2) and the reversal rule for transposes.

### (d) [4]

**A projection has eigenvalues $1$ (on $W$) and $0$ (on $W^\perp$)**, with multiplicities $\dim W$ and $n - \dim W$ — because $P$ fixes every vector of $W$ and kills every vector of $W^\perp$, and those two subspaces span $\mathbb{R}^n$.

**By Week 6's L20 §2, $\operatorname{trace}P = \sum\lambda_i = \dim W \cdot 1 + (n - \dim W)\cdot 0 = \dim W$.** $\square$

*Here $\operatorname{trace}P = 2 = \dim\mathbf{C}(A)$ ✓*

*Marking: 2 for the eigenvalues with their multiplicities, 2 for the trace argument. **This is a satisfying question and worth remarking on** — the trace of a projection counts dimensions.*

---

## Q3: Gram–Schmidt (20 points)

### (a) [8]

$$w_1 = (1,1,1)$$
$$w_2 = (1,1,0) - \tfrac23(1,1,1) = \left(\tfrac13,\tfrac13,-\tfrac23\right) \sim (1,1,-2)$$
$$w_3 = (1,0,0) - \tfrac13(1,1,1) - \tfrac16(1,1,-2)\cdot\ldots = \left(\tfrac12,-\tfrac12,0\right) \sim (1,-1,0)$$

**Cleared:** $(1,1,1)$, $(1,1,-2)$, $(1,-1,0)$.

**Checks:** $(1,1,1)\cdot(1,1,-2) = 0$ ✓ · $(1,1,1)\cdot(1,-1,0) = 0$ ✓ · $(1,1,-2)\cdot(1,-1,0) = 0$ ✓

*Marking: 5 for the three vectors, 3 for the checks. **Accept unnormalised and uncleared answers**, but clearing makes the checks trivial and should be encouraged.*

### (b) [4]

$$q_1 = \tfrac{1}{\sqrt3}(1,1,1), \qquad q_2 = \tfrac{1}{\sqrt6}(1,1,-2), \qquad q_3 = \tfrac{1}{\sqrt2}(1,-1,0)$$

$Q$ has these as columns, and $Q^\mathsf{T}Q = I$ ✓ *(the diagonal entries are $3/3$, $6/6$, $2/2$).*

### (c) [4]

**Prediction: the standard basis $e_1, e_2, e_3$.**

$w_1 = (1,0,0) = e_1$; $(1,1,0)$ minus its component along $e_1$ is $(0,1,0)$; $(1,1,1)$ minus its components along $e_1$ and $e_2$ is $(0,0,1)$. ✓

**What it shows: Gram–Schmidt depends on the order of the inputs.** The same three vectors, reordered, give a completely different orthonormal basis for the same space. **$q_1$ is always a multiple of $a_1$**, so the first vector is privileged.

*Marking: 2 for the prediction, 2 for the order-dependence sentence. **The prediction must precede the computation** — the question says so, and a student who computes first has missed the exercise.*

### (d) [4]

$$w_1 = 1$$
$$w_2 = x - \frac{\langle x,1\rangle}{\langle 1,1\rangle}\cdot 1 = x - 0 = x \qquad (\text{since } \textstyle\int_{-1}^1 x\,dx = 0)$$
$$w_3 = x^2 - \frac{\langle x^2,1\rangle}{\langle 1,1\rangle} - \frac{\langle x^2,x\rangle}{\langle x,x\rangle}x = x^2 - \frac{2/3}{2} - 0 = \boxed{x^2 - \tfrac13}$$

*Marking: 4, with 1 for noting that the two vanishing inner products are by odd/even symmetry rather than by computation.*

---

## Q4: $A = QR$ and Orthonormal Bases (20 points)

### (a) [6]

$$A = \begin{bmatrix}1&2\\ 1&0\\ 0&1\end{bmatrix}: \qquad w_1 = (1,1,0), \quad \lVert w_1\rVert = \sqrt2$$

$$w_2 = (2,0,1) - \frac{2}{2}(1,1,0) = (1,-1,1), \quad \lVert w_2\rVert = \sqrt3$$

$$Q = \begin{bmatrix}1/\sqrt2 & 1/\sqrt3\\ 1/\sqrt2 & -1/\sqrt3\\ 0 & 1/\sqrt3\end{bmatrix}, \qquad R = \begin{bmatrix}\sqrt2 & \sqrt2\\ 0 & \sqrt3\end{bmatrix}$$

*(Since $R_{11} = \lVert w_1\rVert = \sqrt2$, $R_{12} = q_1^\mathsf{T}a_2 = 2/\sqrt2 = \sqrt2$, $R_{22} = \sqrt3$.)*

**$QR = A$ ✓ and $Q^\mathsf{T}Q = I_2$ ✓**

### (b) [4]

**$R$ is upper triangular because $a_j$ is a combination of $q_1,\dots,q_j$ only** — the later $q_i$ did not exist when $a_j$ was processed, so $R_{ij} = 0$ for $i > j$.

**Diagonal entries: the norms $\lVert w_j\rVert$ of the Gram–Schmidt vectors.** $R$ is invertible because those are all **nonzero** — and they are nonzero precisely because the columns of $A$ are independent, so no $w_j$ ever comes out as $0$.

### (c) [5]

$$A^\mathsf{T}A = Q^\mathsf{T}Q = I \quad\Longrightarrow\quad P = Q(Q^\mathsf{T}Q)^{-1}Q^\mathsf{T} = QQ^\mathsf{T}$$

$$Pb = QQ^\mathsf{T}b = \sum_j q_j(q_j^\mathsf{T}b) = \sum_j (q_j^\mathsf{T}b)\,q_j$$

**In words: project $b$ onto each orthonormal direction separately, and add the results.**

*Marking: 2 for $QQ^\mathsf{T}$, 2 for the sum, 1 for the sentence. **The sentence is the point** — it is why Fourier series work.*

### (d) [5]

$$A^\mathsf{T}A\hat x = A^\mathsf{T}b \quad\Longrightarrow\quad (QR)^\mathsf{T}(QR)\hat x = (QR)^\mathsf{T}b$$
$$R^\mathsf{T}\underbrace{Q^\mathsf{T}Q}_{I}R\,\hat x = R^\mathsf{T}Q^\mathsf{T}b \quad\Longrightarrow\quad R^\mathsf{T}R\hat x = R^\mathsf{T}Q^\mathsf{T}b$$

**$R$ is invertible, hence so is $R^\mathsf{T}$**, so cancel it:

$$\boxed{\;R\hat x = Q^\mathsf{T}b\;}$$

**What has disappeared: $A^\mathsf{T}A$.**

**Why it matters:** forming $A^\mathsf{T}A$ **squares the condition number** — $\operatorname{cond}(A^\mathsf{T}A) = \operatorname{cond}(A)^2$ — so a moderately ill-conditioned $A$ produces a badly ill-conditioned normal-equations system. **The QR route never forms it**, and $R\hat x = Q^\mathsf{T}b$ is a triangular solve. *(Week 9.)*

*Marking: 3 for reaching $R\hat x = Q^\mathsf{T}b$ **with the cancellation justified**, 2 for the conditioning explanation. **A script that stops at $R^\mathsf{T}R\hat x = \ldots$ gets 2** — the cancellation is the point.*

---

## Q5: Structure (18 points)

### (a) [4]

$Ax = 0$ means every entry of $Ax$ is zero, and entry $i$ is (row $i$)$\cdot x$. **So $x$ is orthogonal to every row**, hence to every combination of rows, hence to $\mathbf{C}(A^\mathsf{T})$. $\square$

**Stronger than Week 3's observation** because L12 §7 verified ten specific dot products on one matrix; this proves it for every $A$.

**And *complement* asserts more still:** not merely that the two are orthogonal, but that **$\dim\mathbf{N}(A) + \dim\mathbf{C}(A^\mathsf{T}) = n$ and every $x$ splits uniquely** into the two parts. **Orthogonality alone does not give that** — REC 3 §2(d)'s two lines in $\mathbb{R}^3$ are orthogonal and fill nothing.

### (b) [4]

Suppose $y^\mathsf{T}b = 0$ for every $y \in \mathbf{N}(A^\mathsf{T})$. Then $b \in \mathbf{N}(A^\mathsf{T})^\perp$. But $\mathbf{N}(A^\mathsf{T}) = \mathbf{C}(A)^\perp$, so

$$b \in \big(\mathbf{C}(A)^\perp\big)^\perp = \mathbf{C}(A),$$

so $Ax = b$ is solvable. $\square$

*Marking: 4, requiring $(W^\perp)^\perp = W$ to be used explicitly.*

### (c) [4]

Suppose $\sum c_iq_i = 0$. Dot both sides with $q_j$:

$$0 = q_j^\mathsf{T}\Big(\sum_i c_iq_i\Big) = \sum_i c_i\,q_j^\mathsf{T}q_i = c_j$$

since $q_j^\mathsf{T}q_i = 0$ for $i \ne j$ and $1$ for $i = j$. **So every $c_j = 0$.** $\square$

*No elimination, no determinant — just one dot product per coefficient.*

### (d) [6]

$$\lVert Qx\rVert^2 = (Qx)^\mathsf{T}(Qx) = x^\mathsf{T}Q^\mathsf{T}Qx = x^\mathsf{T}x = \lVert x\rVert^2$$

**So $Q$ neither stretches nor shrinks any vector**, giving $\lVert Q\rVert = 1$; and $Q^{-1} = Q^\mathsf{T}$ is also orthogonal, so $\lVert Q^{-1}\rVert = 1$. **Hence $\operatorname{cond}(Q) = 1$.**

**Why Weeks 9–11 insist on it.** Week 7's L22 §4 found that $A = S\Lambda S^{-1}$ can exist and be **numerically worthless**: near a defective matrix the eigenvectors are nearly parallel, $\operatorname{cond}(S)$ explodes — $1.3\times10^8$ at $\varepsilon = 10^{-8}$ — and multiplying by $S^{-1}$ amplifies every rounding error by that factor. **An orthonormal basis makes the amplification factor exactly 1**, so the factorisation is as trustworthy as the data going into it.

*Marking: 3 for the proof, 3 for the two-sentence explanation **referring to Week 7 specifically**. A generic "orthonormal is nicer" earns 1.*

---

## Grade Distribution Expected

| Band | Score | Description |
|---|---|---|
| Strong | 88–100 | Q4(d) reaching $R\hat x = Q^\mathsf{T}b$ with the conditioning point, Q3(c) predicted first, Q5(d) tied to Week 7 |
| Solid | 72–87 | Q1–Q3 correct; Q4 computed; structure questions partial |
| Passing | 55–71 | Projections computed and verified |
| Concerning | < 55 | **Q2 wrong.** Week 9 is least squares and is projection with a story attached; a student who cannot project cannot start it. Help Desk immediately |

---

*MATH 241 · Week 8 · PS 8 Solutions · © CSE Department*
