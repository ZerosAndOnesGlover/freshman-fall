# MATH 241 · Linear Algebra
## Week 1 · Lecture 3 of 3 · **Friday**
### Transposes, Permutations, and $A = LU$

*“Number, place, and combination... the three intersecting but distinct spheres of thought to which all mathematical ideas admit of being referred.”* — James Joseph Sylvester, *Collected Mathematical Papers*, Vol. 1 (1904), p. 91

---

**Reading:** Strang §2.6, §2.7 — and §2.3 for real now · **Previous:** L05, the inverse · **Next:** Week 2, vector spaces

**Coursework:** 📝 **PS 0** due today 17:00 · 📊 **Quiz 2** Mon of Week 2 · 📝 **PS 2** released Wed of Week 2, due Fri of Week 3 17:00 · 💬 **Recitation 1** Thu of Week 2 15:00–15:50

> **PS 0 is due at 17:00 today.** PS 1 was released on Wednesday and is due the Friday of Week 2.

---

## 1. The Transpose

**Flip across the main diagonal.** $(A^\mathsf{T})_{ij} = a_{ji}$; rows become columns.

$$A = \begin{bmatrix}2&1&-1\\4&5&0\\-2&8&11\end{bmatrix} \qquad A^\mathsf{T} = \begin{bmatrix}2&4&-2\\1&5&8\\-1&0&11\end{bmatrix}$$

An $m\times n$ matrix transposes to $n \times m$. A column vector transposes to a row vector, **which is where the notation $x^\mathsf{T}y$ for the dot product comes from**: $x^\mathsf{T}$ is $1\times n$, $y$ is $n \times 1$, and the product is $1\times1$ — a number. Nothing new is being defined; it is matrix multiplication with the shapes lined up.

| Rule | | |
|---|---|---|
| $(A^\mathsf{T})^\mathsf{T} = A$ | | flipping twice |
| $(A+B)^\mathsf{T} = A^\mathsf{T} + B^\mathsf{T}$ | | entrywise |
| $(cA)^\mathsf{T} = cA^\mathsf{T}$ | | |
| $(AB)^\mathsf{T} = B^\mathsf{T}A^\mathsf{T}$ | **order reverses** | proof below |
| $(A^{-1})^\mathsf{T} = (A^\mathsf{T})^{-1}$ | order does **not** reverse | one factor, nothing to reverse |

**The reversal, proved:** the $(i,j)$ entry of $(AB)^\mathsf{T}$ is the $(j,i)$ entry of $AB$, which is $\sum_k a_{jk}b_{ki}$. The $(i,j)$ entry of $B^\mathsf{T}A^\mathsf{T}$ is $\sum_k (B^\mathsf{T})_{ik}(A^\mathsf{T})_{kj} = \sum_k b_{ki}a_{jk}$. **Same sum.** $\square$

*(And the shapes force it before the arithmetic does: if $A$ is $m\times n$ and $B$ is $n\times p$, then $A^\mathsf{T}B^\mathsf{T}$ is $n\times m$ times $p \times n$, which does not exist unless $m = p$. **The only order that typechecks is the reversed one.**)*

### What the transpose actually is

The formula is a bookkeeping rule. **The definition worth carrying is this one:**

$$(Ax)\cdot y \;=\; x\cdot(A^\mathsf{T}y) \qquad\text{for all } x, y$$

*Proof:* $(Ax)^\mathsf{T}y = (x^\mathsf{T}A^\mathsf{T})y = x^\mathsf{T}(A^\mathsf{T}y)$, by the reversal rule and associativity. $\square$

**$A^\mathsf{T}$ is the matrix that lets you move $A$ from one side of a dot product to the other.** That is what a transpose *means*, it is the characterisation that survives into infinite dimensions (where it is called the *adjoint*), and it is the reason $A^\mathsf{T}$ appears in Week 9's normal equations and Week 8's projections. **The flip is how you compute it; this is what it is.**

---

## 2. Symmetric Matrices, and Why $A^\mathsf{T}A$ Matters

$A$ is **symmetric** when $A^\mathsf{T} = A$ — the entries mirror across the diagonal, $a_{ij} = a_{ji}$. Necessarily square.

$$S = \begin{bmatrix}2&1&-1\\1&5&8\\-1&8&11\end{bmatrix} \quad\text{symmetric} \qquad
K = \begin{bmatrix}2&-1&0\\-1&2&-1\\0&-1&2\end{bmatrix} \quad\text{symmetric}$$

**Symmetric matrices are the best-behaved objects in linear algebra**, and essentially the whole second half of this course is about how much better. Week 10 proves that a symmetric matrix has real eigenvalues and a full set of *orthogonal* eigenvectors — the spectral theorem — which is false in general and is why the applications keep arranging to be symmetric.

### The construction that turns up everywhere

> **Claim.** For **any** $A$, of any shape, $A^\mathsf{T}A$ is symmetric.
>
> *Proof.* $(A^\mathsf{T}A)^\mathsf{T} = A^\mathsf{T}(A^\mathsf{T})^\mathsf{T} = A^\mathsf{T}A$.
> $\square$

**One line, no hypotheses.** $A$ can be $10^6 \times 3$, rectangular, rank-deficient, anything. And $A^\mathsf{T}A$ is always square ($n \times n$), always symmetric.

**This is why so much of applied linear algebra runs through $A^\mathsf{T}A$**, and you will meet it three more times:

| Where | As |
|---|---|
| **Week 9** | The normal equations $A^\mathsf{T}A\hat x = A^\mathsf{T}b$ — least squares, and therefore linear regression |
| **Week 10** | The quadratic form $x^\mathsf{T}A^\mathsf{T}Ax = \lVert Ax\rVert^2 \ge 0$, which makes it *positive semidefinite* |
| **Week 11** | Its eigenvalues are the squared singular values of $A$. **The SVD is built from it** |
| **MATH 251** | A covariance matrix is $\tfrac1n X^\mathsf{T}X$ for centred data. Symmetric for this reason |

**Notice it now.** When Week 9 introduces it there will be a lot happening, and its symmetry ought to be the part you already have.

*(Two more facts, free: $AA^\mathsf{T}$ is symmetric too, by the same line, and is a **different** matrix — $m\times m$ rather than $n \times n$. And $A + A^\mathsf{T}$ is symmetric for square $A$, which gives every matrix a canonical symmetric part.)*

---

## 3. Elimination Is Matrix Multiplication

Week 0 did row operations by hand. **Each one is left multiplication by a matrix**, and seeing that is what turns elimination from a procedure into a factorisation.

Recall L04's reading (iii): **the rows of $EA$ are combinations of the rows of $A$.** So to perform $R_2 \leftarrow R_2 - 2R_1$ on a $3\times3$, take the identity and put $-2$ in position $(2,1)$:

$$E_{21} = \begin{bmatrix}1&0&0\\ -2&1&0\\ 0&0&1\end{bmatrix}$$

Row 1 of $E_{21}A$ is $1\cdot(\text{row 1})$ — unchanged. Row 2 is $-2(\text{row 1}) + 1(\text{row 2})$ — exactly the operation. Row 3 is unchanged. **The elementary matrix is the identity with the multiplier written in the slot it acts on**, negated.

Week 0's three steps on $A$ were $\ell_{21}=2$, $\ell_{31}=-1$, $\ell_{32}=3$, so

$$E_{32}E_{31}E_{21}A = U, \qquad
E_{21} = \begin{bmatrix}1&0&0\\-2&1&0\\0&0&1\end{bmatrix},\;
E_{31} = \begin{bmatrix}1&0&0\\0&1&0\\1&0&1\end{bmatrix},\;
E_{32} = \begin{bmatrix}1&0&0\\0&1&0\\0&-3&1\end{bmatrix}$$

**Read the order right to left**: $E_{21}$ acts first, and is written closest to $A$. This is L04 §3's non-commutativity being load-bearing — swapping two of these gives a different matrix and a wrong answer.

---

## 4. $A = LU$: The Multipliers Were a Matrix All Along

Move the $E$'s to the other side. Each is trivially invertible — **to undo "subtract 2 times row 1", add 2 times row 1**, so $E_{21}^{-1}$ is $E_{21}$ with the sign flipped:

$$A = E_{21}^{-1}E_{31}^{-1}E_{32}^{-1}\,U \;=\; L\,U$$

And now the small miracle. Multiply those three inverses together:

$$L = \begin{bmatrix}1&0&0\\2&1&0\\0&0&1\end{bmatrix}\begin{bmatrix}1&0&0\\0&1&0\\-1&0&1\end{bmatrix}\begin{bmatrix}1&0&0\\0&1&0\\0&3&1\end{bmatrix} = \begin{bmatrix}1&0&0\\ \mathbf{2}&1&0\\ \mathbf{-1}&\mathbf{3}&1\end{bmatrix}$$

**The multipliers drop into their own slots with no interference and no sign changes.** $\ell_{21}=2$ into position $(2,1)$; $\ell_{31}=-1$ into $(3,1)$; $\ell_{32}=3$ into $(3,2)$.

> **This is why you were told in Week 0 to write the multipliers in the margin.** There is no
> computation to do. **$L$ is a record of the elimination you already performed** — lower
> triangular, ones on the diagonal, multipliers below.
>
> *(The non-interference is not an accident. The product of the $E^{-1}$'s in that order never
> multiplies one multiplier by another, because each acts on a row that later factors do not
> disturb. Reversing the order does mix them, and gives a different — wrong — matrix. Exercise 4.)*

$$\boxed{\;A = \begin{bmatrix}2&1&-1\\4&5&0\\-2&8&11\end{bmatrix} = \begin{bmatrix}1&0&0\\2&1&0\\-1&3&1\end{bmatrix}\begin{bmatrix}2&1&-1\\0&3&2\\0&0&4\end{bmatrix} = LU\;}$$

Multiply it out and check. `matrices.py` reports `L times U reproduces A: True`.

**Contrast the two factorisations of the same matrix.** $L$ and $U$ hold **6 nonzero entries, all integers**. $A^{-1}$ from L05 holds **9, and not one is an integer.** The factorisation is smaller, exact, and — §5 — does the same job.

---

## 5. Why $LU$ Is the Form You Want

$Ax = b$ becomes $LUx = b$. Split it:

$$\underbrace{Lc = b}_{\text{forward substitution}} \qquad\text{then}\qquad \underbrace{Ux = c}_{\text{back substitution}}$$

**Two triangular solves, each $n^2$.** On our system, $b = (1, 14, 47)$:

$$Lc = b: \quad c_1 = 1;\quad 2(1) + c_2 = 14 \Rightarrow c_2 = 12; \quad -1(1) + 3(12) + c_3 = 47 \Rightarrow c_3 = 12$$

$$c = (1, 12, 12)$$

**Which is exactly the transformed right-hand side Week 0's L02 §4 produced and told you to keep.** It was $L^{-1}b$ all along. Then $Ux = c$ back-substitutes to $x = (1,2,3)$, as before.

### The point of the whole thing

| | Cost | $n = 1000$ |
|---|---:|---:|
| Factor $A = LU$ — **once** | $n^3/3$ | $3.3\times10^{8}$ |
| Each solve thereafter | $2n^2$ | $2\times10^{6}$ |

**A second right-hand side costs $0.6\%$ of the first.** For 200 right-hand sides, factoring once is roughly $80\times$ cheaper than 200 full eliminations — the number PS 0 Q4(a) asked you to compute, and this is the mechanism behind it.

**And this is exactly what a library does.** `scipy.linalg.lu_factor` then `lu_solve`; LAPACK's `dgetrf` then `dgetrs`. When you call `numpy.linalg.solve` once, it does both and throws the factors away — **which is the right default and the wrong thing to do in a loop.**

> **Where the same idea returns.** $A = LU$ is the first of five factorisations, and the course's
> spine: $QR$ in Week 9, $S\Lambda S^{-1}$ in Week 7, $Q\Lambda Q^\mathsf{T}$ in Week 10, and
> $U\Sigma V^\mathsf{T}$ in Week 11. **Every one is the same move** — replace $A$ by a product of
> matrices you can solve with instantly. Only the notion of "instantly" changes: triangular here,
> orthogonal later.

---

## 6. Permutations, and $PA = LU$

$A = LU$ needs every pivot to appear without a row exchange. **Most matrices need one** — Week 0's L02 §6 Case A, and every floating-point computation, since partial pivoting swaps unconditionally.

A **permutation matrix** $P$ is the identity with its rows reordered. Left-multiplying by $P$ reorders rows; there are $n!$ of them.

$$P = \begin{bmatrix}0&1&0\\1&0&0\\0&0&1\end{bmatrix} \qquad PA \text{ swaps rows 1 and 2 of } A$$

**Doing all the exchanges up front turns any nonsingular $A$ into one that factors:**

$$\boxed{PA = LU}$$

$P$ records which rows were swapped, and it is the **only** thing about the factorisation that cannot be known before you start. LAPACK returns it as an integer pivot vector, `ipiv` — not as a matrix, because storing $n^2$ numbers to describe a reordering of $n$ things would be absurd.

### The fact worth stopping for

$$P^{-1} = P^\mathsf{T}$$

**The inverse of a permutation matrix is its transpose.** No elimination, no division, no arithmetic of any kind: **transposing undoes it.**

*Why:* $P$'s rows are the standard basis vectors in some order. Row $i$ of $P$ times column $j$ of $P^\mathsf{T}$ is row $i$ of $P$ dotted with row $j$ of $P$ — which is $1$ if $i = j$ and $0$ otherwise, since distinct basis vectors are orthogonal. So $PP^\mathsf{T} = I$. $\square$

> **This is the first orthogonal matrix you have met, and it is worth naming.** A matrix with
> $Q^\mathsf{T}Q = I$ is called **orthogonal**, and $Q^{-1} = Q^\mathsf{T}$ is the property that
> makes the entire second half of this course work: it is why $\operatorname{cond}(Q) = 1$
> (Week 0's L03 §7), why Week 9 prefers $QR$ to the normal equations, why Week 10's spectral theorem
> is $Q\Lambda Q^\mathsf{T}$ with no inverse in sight, and why Week 11's SVD is numerically
> trustworthy. **Permutations are the trivial case, and you have just proved it.**

---

## 7. What to Take Away

1. **$(A^\mathsf{T})_{ij} = a_{ji}$, and $(AB)^\mathsf{T} = B^\mathsf{T}A^\mathsf{T}$** — the order reverses, and the shapes force it.
2. **The transpose is what moves $A$ across a dot product:** $(Ax)\cdot y = x\cdot(A^\mathsf{T}y)$. That is the definition worth keeping.
3. **$A^\mathsf{T}A$ is symmetric for every $A$**, in one line and with no hypotheses. Weeks 9, 10 and 11 all run through it.
4. **Every row operation is left multiplication by an elementary matrix**, and each is inverted by flipping one sign.
5. **$A = LU$, and $L$ is the multipliers, written where you computed them.** Nothing is calculated to build it.
6. **Factor once, solve many times:** $n^3/3$ then $2n^2$ each. This is what every library does, and it is the first of the course's five factorisations.
7. **$PA = LU$ in general**, and **$P^{-1} = P^\mathsf{T}$** — your first orthogonal matrix, and a preview of why the rest of the course cares so much about them.

---

## Exercises

*(Not assessed. PS 1 is due Friday of Week 2.)*

1. Find $A = LU$ for $\begin{bmatrix}1&2\\3&8\end{bmatrix}$ and $\begin{bmatrix}2&4&2\\1&5&2\\4&-1&9\end{bmatrix}$. Check both by multiplying out.
2. Use the $LU$ of §4 to solve $Ax = (4, 6, 5)$ by forward then back substitution. **Do not re-eliminate** — that is the point of having the factors.
3. Prove that if $A$ is symmetric and invertible, $A^{-1}$ is symmetric. *(One line from the rules in §1.)*
4. Compute $E_{32}^{-1}E_{31}^{-1}E_{21}^{-1}$ — the **reverse** of §4's order. You will not get $L$. Explain, in terms of which rows each factor touches, why one order interferes and the other does not.
5. Write down all six $3\times3$ permutation matrices. Verify $P^{-1} = P^\mathsf{T}$ for each. **Which ones are their own inverse, and what is special about those as permutations?**
6. $A$ is $5\times3$. What are the shapes of $A^\mathsf{T}A$ and $AA^\mathsf{T}$? Both are symmetric. Can both be invertible? *(Think about how many pivots each can possibly have. This is Week 3's question, and guessing at it now is worth more than being right.)*

---

*MATH 241 · Week 1 · L06 · © CSE Department*
