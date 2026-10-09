# MATH 241 · Linear Algebra
## Week 10 · Lecture 1 of 3 · **Monday**
### Symmetric Matrices and the Spectral Theorem

*“Symmetry is a vast subject, significant in art and nature. Mathematics lies at its root, and it would be hard to find a better one on which to demonstrate the working of the mathematical intellect.”* — Hermann Weyl, *Symmetry* (1952)

---

**Reading:** Strang §6.4 · **Previous:** Week 9's L29, what least squares assumes · **Next:** L31, positive definite matrices

**Coursework:** 📊 **Quiz 10** today · 📝 **PS 10** released Wed this week, due Fri of Week 11 17:00 · 💬 **Recitation 9** Thu this week 15:00–15:50 · 📝 **PS 9** due Fri this week 17:00

> **Quiz 10 is the first ten minutes of this lecture** and covers Week 9.
>
> **Midterm 2 is this Wednesday**, Nov 12, **18:00–19:15, SSB 110**, covering **Weeks 6–9**.
> **Nothing from this week is on it.**
>
> **CS 201's Midterm 2 is tonight**, 18:00–19:15, VNC 100, covering its Weeks 5–9. **Two midterms
> in three days**, and **PS 9 is still due Friday**.

---

## 1. The Hypothesis Everything Has Been Waiting For

Week 7 ended badly, and said so.

**$A = S\Lambda S^{-1}$ has two failure modes.** The first is that $S$ need not exist: a defective matrix has fewer independent eigenvectors than it has dimensions, and L22 §2 built one. The second is worse, because it looks like success — **$S$ exists and is nearly singular.** L22 §4 exhibited eigenvectors $(1,0)$ and $(1,10^{-8})$, independent by any exact test, with $\operatorname{cond}(S) = 1.3\times10^{8}$. The factorisation is correct and **numerically worthless**.

Week 8 named what would fix it: **if the eigenvectors were orthonormal, $S^{-1}$ would be $S^\mathsf{T}$ and $\operatorname{cond}(S)$ would be exactly $1$.** It did not say when that happens.

> **It happens exactly when $A$ is symmetric**, and it happens *every* time — no hypothesis, no
> genericity condition, no exceptions.
>
> $$\boxed{\;A = A^\mathsf{T} \;\Longrightarrow\; A = Q\Lambda Q^\mathsf{T},\ \ Q^\mathsf{T}Q = I,\ \ \Lambda \text{ real}\;}$$

**This is the spectral theorem**, and it is the most useful theorem in the course. Three claims are packed into it, and each needs its own proof:

1. **The eigenvalues are real.** (§2)
2. **Eigenvectors for different eigenvalues are perpendicular.** (§3)
3. **There are always enough of them** — a repeated eigenvalue never costs you a dimension. (§6)

---

## 2. The Eigenvalues Are Real

**Week 6 warned that eigenvalues can be complex**, and gave the rotation as the standard example: $R = \begin{bmatrix}0&-1\\1&0\end{bmatrix}$ has $\lambda^2 + 1 = 0$, so $\lambda = \pm i$, and no real direction survives a quarter turn.

**Symmetry rules that out.** In $2\times2$ the whole theorem is one discriminant, and it is worth seeing before the general proof, because the general proof is the same idea in heavier notation. Compare

$$S(e) = \begin{bmatrix}5 & e\\ e & 3\end{bmatrix} \qquad\text{and}\qquad B(e) = \begin{bmatrix}5 & e\\ -e & 3\end{bmatrix}.$$

**Same size, same trace $8$, one entry's sign apart.** But $\det S = 15 - e^2$ and $\det B = 15 + e^2$, so

$$\text{disc}\,S = 64 - 4(15 - e^2) = 4 + 4e^2, \qquad \text{disc}\,B = 64 - 4(15 + e^2) = 4 - 4e^2.$$

| $e$ | disc $S$ | eigenvalues of $S$ | disc $B$ | eigenvalues of $B$ |
|---:|---:|---|---:|---|
| $0$ | $4$ | $5,\ 3$ | $4$ | $5,\ 3$ |
| $\tfrac12$ | $5$ | $5.1180,\ 2.8820$ | $3$ | $4.8660,\ 3.1340$ |
| $1$ | $8$ | $5.4142,\ 2.5858$ | $\mathbf{0}$ | $4,\ 4$ **(defective)** |
| $2$ | $20$ | $6.2361,\ 1.7639$ | $-12$ | $4 \pm 1.7321\,i$ |
| $5$ | $104$ | $9.0990,\ \mathbf{-1.0990}$ | $-96$ | $4 \pm 4.8990\,i$ |

**$\text{disc}\,S = 4 + 4e^2$ cannot be negative.** The off-diagonal entry enters *squared and positively*, so no matter how large you make it the roots stay real. **$\text{disc}\,B = 4 - 4e^2$ goes negative at $e = 1$** — and at exactly $e = 1$, $B$ has the double eigenvalue $4$ with a one-dimensional eigenspace. **Week 7's defect, one sign away from this week's theorem.**

> **Read the last row.** $S(5)$ has eigenvalues $9.099$ and $-1.099$. **Symmetry guarantees *real*,
> not *positive*.** Confusing those two is the single most common error on this material, and L31
> is entirely about the extra hypothesis that gets you positivity.

### The general proof

Let $Ax = \lambda x$ with $A$ real symmetric, allowing $\lambda$ and $x$ to be complex, and let $\bar{\phantom{x}}$ denote complex conjugation.

$$\bar x^\mathsf{T}Ax = \bar x^\mathsf{T}(\lambda x) = \lambda\,(\bar x^\mathsf{T}x).$$

Now transpose-and-conjugate the same scalar. Since $A$ is real and symmetric, $\overline{A^\mathsf{T}} = A$, so

$$\overline{\bar x^\mathsf{T}Ax} = x^\mathsf{T}A\bar x = \bar\lambda\,(x^\mathsf{T}\bar x) = \bar\lambda\,(\bar x^\mathsf{T}x).$$

**A scalar equal to its own conjugate is real.** And $\bar x^\mathsf{T}x = \sum |x_i|^2 > 0$ for $x \ne 0$, so it can be divided out:

$$\lambda = \bar\lambda \quad\Longrightarrow\quad \lambda \text{ is real.}$$

**Two lines, and it is the only place in the course where complex numbers are needed** — to prove they are not needed.

---

## 3. Eigenvectors for Different Eigenvalues Are Perpendicular

**Week 7's L21 §3 proved eigenvectors for distinct eigenvalues are independent.** For symmetric matrices they are more than independent.

Let $Ax = \lambda x$ and $Ay = \mu y$ with $\lambda \ne \mu$. Then

$$\lambda\,(x\cdot y) = (Ax)^\mathsf{T}y = x^\mathsf{T}A^\mathsf{T}y = x^\mathsf{T}Ay = \mu\,(x\cdot y).$$

So $(\lambda - \mu)(x\cdot y) = 0$, and since $\lambda \ne \mu$, **$x\cdot y = 0$.**

> **The whole proof is the middle equality**, $A^\mathsf{T} = A$, used once. **Everything this week
> is that one substitution, applied somewhere new.**

---

## 4. $A = Q\Lambda Q^\mathsf{T}$, Worked Exactly

Take

$$A = \begin{bmatrix}5 & 0 & -2\\ 0 & 3 & -2\\ -2 & -2 & 4\end{bmatrix}, \qquad A = A^\mathsf{T},\quad \operatorname{trace}A = 12, \quad \det A = 28.$$

**This matrix carries all three lectures**, and it is built so that every identity in the week is exactly checkable in rational arithmetic. Its eigenvectors are

$$u_1 = \begin{bmatrix}1\\2\\2\end{bmatrix},\quad u_2 = \begin{bmatrix}2\\1\\-2\end{bmatrix},\quad u_3 = \begin{bmatrix}2\\-2\\1\end{bmatrix}, \qquad Au_1 = 1\,u_1,\ \ Au_2 = 7\,u_2,\ \ Au_3 = 4\,u_3.$$

**Check one by hand now:** $A u_2 = (10+0+4,\ 0+3+4,\ -4-2-8) = (14, 7, -14) = 7\,u_2$. ✓

**They are mutually perpendicular** — $u_1\cdot u_2 = 2+2-4 = 0$, $u_1\cdot u_3 = 2-4+2 = 0$, $u_2\cdot u_3 = 4-2-2 = 0$ — as §3 promised, since $1$, $7$, $4$ are distinct. **And all three have length exactly $3$**, which is a piece of deliberate construction rather than a theorem, and it is what makes $Q$ rational:

$$Q = \frac13\begin{bmatrix}1 & 2 & 2\\ 2 & 1 & -2\\ 2 & -2 & 1\end{bmatrix}, \qquad \Lambda = \begin{bmatrix}1&&\\&7&\\&&4\end{bmatrix}.$$

`resources/symmetric.py` §1 verifies, **in `Fraction`, with no rounding anywhere**:

$$Q^\mathsf{T}Q = I, \qquad QQ^\mathsf{T} = I, \qquad Q\Lambda Q^\mathsf{T} = A.$$

> **Compare with Week 7.** There, $A = S\Lambda S^{-1}$ required inverting $S$ — an $O(n^3)$
> computation whose accuracy depended on $\operatorname{cond}(S)$, which L22 §4 showed could be
> $10^8$. **Here $S^{-1}$ is $S^\mathsf{T}$**: you get the inverse by reading the matrix sideways,
> it costs nothing, and $\operatorname{cond}(Q) = 1$ exactly. **This is the payoff L22 §6's table
> promised and Week 8 explained.**

**Sanity checks that cost nothing and should always be done:** $1 + 7 + 4 = 12 = \operatorname{trace}A$, and $1 \times 7 \times 4 = 28 = \det A$. Week 6's invariants still hold, because they hold for every matrix.

---

## 5. A Symmetric Matrix *Is* a Sum of Perpendicular Projections

**Multiply out $Q\Lambda Q^\mathsf{T}$ column by column.** Writing $q_k$ for the $k$-th column of $Q$,

$$\boxed{\;A = \lambda_1 q_1q_1^\mathsf{T} + \lambda_2 q_2q_2^\mathsf{T} + \cdots + \lambda_n q_nq_n^\mathsf{T}\;}$$

**And $q_kq_k^\mathsf{T}$ is exactly Week 8's projection matrix onto the line through $q_k$** — L25 §2's $P = \dfrac{aa^\mathsf{T}}{a^\mathsf{T}a}$, with $a^\mathsf{T}a = 1$ because $q_k$ is a unit vector.

The script's §2 verifies all of the following exactly on our $A$:

| Property | Meaning |
|---|---|
| $P_k^2 = P_k$, $P_k^\mathsf{T} = P_k$ | each is a projection (Week 8's L25 §4) |
| $\operatorname{trace}P_k = 1$ | onto a **line** — Week 8's trace-counts-dimension |
| $P_iP_j = 0$ for $i \ne j$ | perpendicular lines annihilate each other |
| $P_1 + P_2 + P_3 = I$ | the lines **fill** $\mathbb{R}^3$ |
| $1\,P_1 + 7\,P_2 + 4\,P_3 = A$ | the spectral decomposition itself |

> **This is the sentence to remember: a symmetric matrix is a weighted sum of perpendicular
> projections, and the weights are the eigenvalues.** Applying $A$ means "split $x$ into
> perpendicular components, stretch each by its own factor, add them back". Week 7's $S\Lambda S^{-1}$
> said the same thing with the word *perpendicular* removed, and everything numerical that went wrong
> went wrong there.

**Week 8's $P = A(A^\mathsf{T}A)^{-1}A^\mathsf{T}$ is one term of this**, at $\lambda = 1$, with the rest at $\lambda = 0$ — which is why L25 §6 found a projection's eigenvalues to be $1$s and $0$s.

---

## 6. A Repeated Eigenvalue Is Not a Defect

**§3 covers distinct eigenvalues. The theorem claims more**, and this is the part that takes real work in general. Take

$$C = \begin{bmatrix}3&1&1\\1&3&1\\1&1&3\end{bmatrix} = 2I + J.$$

$C(1,1,1) = (5,5,5)$, so $\lambda = 5$. And $\lambda = 2$ is a **double** root: every vector perpendicular to $(1,1,1)$ is an eigenvector, because $Jv = 0$ there. **$(1,-1,0)$, $(1,0,-1)$ and $(1,1,-2)$ all work.**

**Week 7's defective matrices had a double root and a one-dimensional eigenspace.** That is what "defective" meant. **It cannot happen here.** For a symmetric matrix, an eigenvalue repeated $k$ times always has a $k$-dimensional eigenspace — algebraic multiplicity always equals geometric multiplicity, and the reason is §5: $Q$ exists, and its columns are a full basis, so the counts must match.

> **What is *not* determined is which eigenvectors you get.** $(1,-1,0)$ and $(1,0,-1)$ are both
> genuine eigenvectors for $\lambda = 2$ and their dot product is $1$ — **not perpendicular.**
> The theorem does not say every eigenvector is perpendicular to every other; it says an
> orthonormal set *exists*.
>
> **And Week 8 tells you how to find it: run Gram–Schmidt inside the eigenspace.** Subtracting
> the projection of $(1,0,-1)$ onto $(1,-1,0)$ gives $\tfrac12(1,1,-2)$ — perpendicular to
> $(1,-1,0)$, still an eigenvector, because **an eigenspace is a subspace and any combination of
> its members stays inside it.**

**That is why the eigenvalue's multiplicity never causes trouble and never causes ambiguity in $A$ itself:** different orthonormal choices inside the eigenspace give different $Q$, and $Q\Lambda Q^\mathsf{T}$ comes out the same every time.

---

## 7. The Converse Also Holds

**Suppose $A$ has an orthonormal basis of eigenvectors with real eigenvalues.** Then $A = Q\Lambda Q^\mathsf{T}$, so

$$A^\mathsf{T} = (Q\Lambda Q^\mathsf{T})^\mathsf{T} = Q\Lambda^\mathsf{T}Q^\mathsf{T} = Q\Lambda Q^\mathsf{T} = A,$$

using $\Lambda^\mathsf{T} = \Lambda$ because a diagonal matrix is its own transpose. **$A$ is symmetric.**

> **So the spectral theorem is an exact characterisation, not a one-way implication.**
> **Real eigenvalues plus perpendicular eigenvectors $\iff$ symmetric.** If you ever produce an
> orthonormal eigenbasis for a matrix that is not symmetric, you have made an arithmetic error, and
> this is the cheapest way to catch it.

---

## 8. Why This Theorem Is the One That Matters

**Because symmetric matrices are not a special case; they are most of the matrices you will meet.**

| Where it comes from | Why it is symmetric |
|---|---|
| $A^\mathsf{T}A$ in least squares (Week 9) | $(A^\mathsf{T}A)^\mathsf{T} = A^\mathsf{T}A$ — Week 1's L06 §2 |
| Covariance matrices (Week 12's PCA) | $\operatorname{cov}(X_i, X_j) = \operatorname{cov}(X_j, X_i)$ |
| The Hessian of a smooth function (L32 §3) | mixed partials commute |
| Graph adjacency and Laplacian matrices | an undirected edge points both ways |
| Stiffness and inertia matrices in mechanics | Newton's third law |
| Projection matrices (Week 8) | $P^\mathsf{T} = P$ was one of the two defining properties |

**Every one of those has real eigenvalues and orthonormal eigenvectors, for free, always.** Week 7's warnings do not apply to any of them.

---

## 9. What to Take Away

1. **$A = A^\mathsf{T} \Longrightarrow A = Q\Lambda Q^\mathsf{T}$**, with $Q$ orthogonal and $\Lambda$ real. **No hypotheses.**
2. **Real eigenvalues:** $\lambda = \bar\lambda$, in two lines, using symmetry once.
3. **Perpendicular eigenvectors** for distinct eigenvalues: $(\lambda-\mu)(x\cdot y) = 0$.
4. **Repeated eigenvalues are never defective**, and Gram–Schmidt inside the eigenspace supplies the orthonormal set.
5. **$S^{-1} = S^\mathsf{T}$ and $\operatorname{cond}(Q) = 1$** — the answer to L22 §4's complaint.
6. **$A = \sum \lambda_k q_kq_k^\mathsf{T}$:** a weighted sum of perpendicular projections.
7. **The converse holds**, so the theorem characterises symmetry exactly.
8. **Symmetry gives *real*, not *positive*.** $\begin{bmatrix}5&5\\5&3\end{bmatrix}$ has a negative eigenvalue. **L31 is about the extra condition.**

---

## Exercises

*(Not assessed. PS 10 is the assessed work.)*

1. Diagonalise $\begin{bmatrix}2&1\\1&2\end{bmatrix}$ as $Q\Lambda Q^\mathsf{T}$. **Verify $Q^\mathsf{T}Q = I$ by hand.**
2. For our $A$, compute $P_2 = q_2q_2^\mathsf{T}$ explicitly as a matrix of fractions and check $P_2^2 = P_2$.
3. $A$ is symmetric with eigenvalues $1, 7, 4$. What are the eigenvalues of $A^2$? Of $A^{-1}$? Of $A + 3I$? **What are the eigenvectors in each case?**
4. **Prove that a symmetric matrix with all eigenvalues equal to $c$ must be $cI$.** *(Use §5.)* Then find a **non**-symmetric matrix with all eigenvalues $c$ that is not $cI$.
5. Find an orthonormal basis of eigenvectors for $C = 2I + J$ above, and write out $C = 5P_1 + 2P_2 + 2P_3$.
6. $A$ and $B$ are symmetric. Is $AB$ symmetric? **Try $\begin{bmatrix}1&0\\0&2\end{bmatrix}$ and $\begin{bmatrix}0&1\\1&0\end{bmatrix}$.** Then find the exact condition on $A$ and $B$ under which $AB$ *is* symmetric.
7. In §2's table, $B(1)$ has a double eigenvalue and one eigenvector. **Verify that $B(1) - 4I$ has rank $1$**, and say which week's vocabulary that is.
8. **A real matrix with $A^\mathsf{T} = -A$ is called antisymmetric.** Show its eigenvalues are purely imaginary or zero. *(Run §2's proof with one sign changed.)* Check against the rotation $R$.

---

*MATH 241 · Week 10 · L30 · © CSE Department*
