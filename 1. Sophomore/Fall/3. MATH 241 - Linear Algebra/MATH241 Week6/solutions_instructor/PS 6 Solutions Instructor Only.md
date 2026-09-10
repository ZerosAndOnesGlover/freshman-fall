# MATH 241 · Problem Set 6 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**All exact arithmetic**; `resources/eigen.py` reproduces every computation.

**What this paper is testing.** Q1 is the mechanical core and must be right — it is the computation Weeks 7, 10, 11 and 12 all rest on. **Q2(c) against Q2(e) is the pair that matters**: both have a repeated eigenvalue and only one is defective, which is the distinction Week 7 is built on. Q4(c) closes the loop on a question first asked in Week 4 and answered three times since, each time better. Q5(d) is the paper's best question — it asks the student to explain something they were told to accept two weeks ago.

**Common failure modes:** (1) eigenvectors unverified, so sign errors survive; (2) Q2(c) called defective because the eigenvalue repeats; (3) Q3(c)'s $A + 3I$ answered $\lambda$ rather than $\lambda + 3$; (4) Q4(d)'s converse example omitted.

---

## Q1: Finding Them (24 points)

### (a) [8]

$$A = \begin{bmatrix}3&-2&2\\ 2&3&2\\ 2&2&3\end{bmatrix}, \qquad \det(A - \lambda I) = \boxed{-\lambda^3 + 9\lambda^2 - 23\lambda + 15}$$

**Why elimination cannot be used:** it would divide by the pivot $3 - \lambda$ to clear the first column — **and $3 - \lambda$ may be zero.** Every pivot is an expression in $\lambda$, so elimination forces a case split at each step. **Cofactor expansion only multiplies and adds**, so it produces the polynomial with no cases. *(L17 §5, L19 §3.)*

*Marking: 6 for the polynomial, 2 for the reason. **The reason must mention dividing by something that may vanish**; "because there is a variable in it" earns 1.*

### (b) [4]

$$-\lambda^3 + 9\lambda^2 - 23\lambda + 15 = -(\lambda - 1)(\lambda - 3)(\lambda - 5) \qquad \boxed{\lambda = 1,\ 3,\ 5}$$

*(Finding the first root by inspection — try small divisors of 15 — then dividing out, is the expected route.)*

### (c) [8]

| $\lambda$ | $\mathbf{N}(A - \lambda I)$ | Check $Av = \lambda v$ |
|---|---|---|
| $1$ | $\operatorname{span}\{(-1,0,1)\}$ | $A(-1,0,1) = (-1,0,1) = 1v$ ✓ |
| $3$ | $\operatorname{span}\{(-1,1,1)\}$ | $A(-1,1,1) = (-3,3,3) = 3v$ ✓ |
| $5$ | $\operatorname{span}\{(0,1,1)\}$ | $A(0,1,1) = (0,5,5) = 5v$ ✓ |

*Marking: 2 per eigenspace, 2 for the three verifications. **No verification, no verification marks** — the paper said so.*

### (d) [4]

$$\operatorname{trace}A = 3+3+3 = 9 = 1 + 3 + 5\ ✓ \qquad \det A = 15 = 1\times3\times5\ ✓$$

**Why they are free:** the trace is the sum of the diagonal — read off, no computation. And **$\det A$ is the constant term of the characteristic polynomial**, since $p(0) = \det(A - 0I) = \det A$ — so it was already computed in part (a) and needs no separate determinant.

*Marking: 2 for the two checks, 2 for the "free" explanation. **The $p(0) = \det A$ observation is the answer**; a student who recomputes $\det A$ from scratch has missed it and gets 1 of the 2.*

---

## Q2: Predict Before You Compute (18 points)

| | $T$ | Matrix | $\lambda$ | Eigenvectors |
|---|---|---|---|---|
| (a) | reflect across $y$-axis | $\begin{bmatrix}-1&0\\0&1\end{bmatrix}$ | $-1,\ 1$ | $(1,0)$, $(0,1)$ |
| (b) | project onto $x$-axis | $\begin{bmatrix}1&0\\0&0\end{bmatrix}$ | $1,\ 0$ | $(1,0)$, $(0,1)$ |
| (c) | rotate $180°$ | $-I$ | $-1$ *(twice)* | **every** nonzero vector |
| (d) | rotate $60°$ | $\begin{bmatrix}\tfrac12&-\tfrac{\sqrt3}{2}\\[2pt] \tfrac{\sqrt3}{2}&\tfrac12\end{bmatrix}$ | **none real** | — |
| (e) | shear $(x,y)\mapsto(x+4y,y)$ | $\begin{bmatrix}1&4\\0&1\end{bmatrix}$ | $1$ *(twice)* | $(1,0)$ **only** |
| (f) | upper triangular | — | $2,\ 5,\ -1$ | — |

**(f):** the eigenvalues of a **triangular** matrix are its diagonal entries, because $\det(A - \lambda I)$ is then the product $(2-\lambda)(5-\lambda)(-1-\lambda)$. **Read off, no work.**

### The two interesting ones

**(d) has no real eigenvalues.** $p(\lambda) = \lambda^2 - \lambda + 1$, discriminant $1 - 4 = -3 < 0$. **Geometrically: a rotation by $60°$ leaves no direction unmoved**, so there is nothing for a real eigenvector to be. Over $\mathbb{C}$, $\lambda = \tfrac12 \pm \tfrac{\sqrt3}{2}i = e^{\pm i\pi/3}$.

**(e) is defective.** $\lambda = 1$ has algebraic multiplicity 2 and geometric multiplicity 1 — **a $2\times2$ matrix with only one independent eigenvector.** Geometrically, a shear fixes the $x$-axis and tilts everything else; no second invariant direction exists.

> **The pair to insist on is (c) against (e).** *Both* have a repeated eigenvalue. **(c) is not
> defective** — $-I$ has a two-dimensional eigenspace, every vector being an eigenvector — while
> **(e) is.** **A repeated eigenvalue does not make a matrix defective; a deficient eigenspace does.**
> This is the single most common misreading of Week 6 and it is fatal in Week 7.

*Marking: 3 each. Full marks on (a)–(e) require the prediction to precede the matrix, as instructed. **Deduct on any script calling (c) defective**, and write the sentence above on it.*

---

## Q3: The Characteristic Polynomial (20 points)

### (a) [4]

$\begin{bmatrix}5&2\\2&2\end{bmatrix}$: trace $7$, determinant $10 - 4 = 6$.

$$\lambda^2 - 7\lambda + 6 = 0 \quad\Longrightarrow\quad \lambda = 1,\ 6$$

Eigenvectors: $\lambda = 1 \to (-1, 2)$; $\lambda = 6 \to (2, 1)$. *(Both verifiable in one product.)*

### (b) [5]

$B = \begin{bmatrix}1&-2\\1&3\end{bmatrix}$: trace $4$, determinant $3 + 2 = 5$.

$$p(\lambda) = \lambda^2 - 4\lambda + 5, \qquad \text{discriminant } 16 - 20 = -4 < 0$$

**No real roots.** Over $\mathbb{C}$: $\lambda = \dfrac{4 \pm 2i}{2} = \boxed{2 \pm i}$.

$$(2+i) + (2-i) = 4 = \operatorname{trace}B\ ✓ \qquad (2+i)(2-i) = 4 + 1 = 5 = \det B\ ✓$$

**What it says about $B$:** **no real direction is preserved** — $B$ maps every line through the origin to a different line. It acts as a rotation combined with a scaling. *(The scaling factor is $\lvert\lambda\rvert = \sqrt5$.)*

*Marking: 2 for the polynomial and no-real-roots, 2 for the complex roots, 1 for the interpretation. **The trace/determinant check surviving into $\mathbb{C}$ is worth remarking on** — it is why the identities are stated over $\mathbb{C}$ in L20 §2.*

### (c) [5] — eigenvalues $2, -1, 4$

| | | Justification |
|---|---|---|
| $\operatorname{trace}A$ | $5$ | sum |
| $\det A$ | $-8$ | product |
| eigenvalues of $A^2$ | $4, 1, 16$ | $Av = \lambda v \Rightarrow A^2v = \lambda^2v$ |
| eigenvalues of $A^{-1}$ | $\tfrac12, -1, \tfrac14$ | multiply $Av = \lambda v$ by $A^{-1}/\lambda$ |
| eigenvalues of $A + 3I$ | $5, 2, 7$ | $(A+3I)v = Av + 3v = (\lambda+3)v$ |
| eigenvalues of $A^\mathsf{T}$ | $2, -1, 4$ | same characteristic polynomial — Q5(b) |

*Marking: 1 for the first two together, 1 each for the last four with justification. **$A + 3I$ is the discriminating one**; a script answering $2, -1, 4$ has confused adding $3I$ with scaling.*

### (d) [6]

**Every eigenvalue satisfies $\lambda^3 = \lambda$.** If $Av = \lambda v$ with $v \ne 0$, then $A^3v = \lambda^3 v$; but $A^3 = A$, so $A^3 v = Av = \lambda v$. Hence $\lambda^3 v = \lambda v$, so $(\lambda^3 - \lambda)v = 0$, and $v \ne 0$ gives

$$\lambda^3 - \lambda = \lambda(\lambda-1)(\lambda+1) = 0 \quad\Longrightarrow\quad \lambda \in \{0, 1, -1\}. \qquad\square$$

**No, $A^3 = A$ does not force $A \in \{0, I, \text{reflection}\}$.** A counterexample:

$$A = \begin{bmatrix}1&0\\0&0\end{bmatrix}, \qquad A^3 = A \ ✓$$

**This is a projection** — eigenvalues $1$ and $0$ — and it is none of the three. *(Any projection works, since $P^2 = P$ gives $P^3 = P$.)*

*Marking: 4 for the proof, 2 for a valid counterexample. **The proof must not compute a determinant** — the question forbids it, and the point is that a polynomial identity constrains eigenvalues directly.*

---

## Q4: Multiplicities (22 points)

### (a) [6]

$$C = \begin{bmatrix}3&1&0\\ 0&3&0\\ 0&0&5\end{bmatrix}, \qquad p(\lambda) = (3-\lambda)^2(5-\lambda)$$

| $\lambda$ | Algebraic | Geometric | |
|---|---:|---:|---|
| $3$ | $2$ | $\mathbf{1}$ | $\mathbf{N}(C - 3I) = \operatorname{span}\{(1,0,0)\}$ |
| $5$ | $1$ | $1$ | $\operatorname{span}\{(0,0,1)\}$ |

**Defective**, because $\lambda = 3$ has geometric $1 <$ algebraic $2$. **Only two independent eigenvectors for a $3\times3$**, so no basis of eigenvectors and no diagonalisation.

*Marking: 3 for the multiplicities, 3 for the verdict with justification. **"Defective because the eigenvalue repeats" is wrong** — see Q2(c) — and should be marked as such even where the verdict is right.*

### (b) [5]

$$\begin{bmatrix}4&0&1\\ 0&4&0\\ 0&0&4\end{bmatrix}$$

**Algebraic:** $p(\lambda) = (4-\lambda)^3$, so $\lambda = 4$ with multiplicity 3. ✓

**Geometric:** $A - 4I = \begin{bmatrix}0&0&1\\0&0&0\\0&0&0\end{bmatrix}$ has rank 1, so its null space has dimension $3 - 1 = 2$, spanned by $(1,0,0)$ and $(0,1,0)$. ✓

*Accept any valid construction. Marking: 2 for the matrix, 3 for verifying both multiplicities. **The rank–nullity route to the geometric multiplicity is the efficient one** and is worth noting on strong scripts.*

### (c) [5]

**Equal characteristic polynomials:** $\det(I - \lambda I) = (1-\lambda)^2$ and $\det(S - \lambda I) = \det\begin{bmatrix}1-\lambda&1\\0&1-\lambda\end{bmatrix} = (1-\lambda)^2$. ✓

**The distinguishing invariant: geometric multiplicity of $\lambda = 1$.**

$$\dim\mathbf{N}(I - I) = \dim\mathbb{R}^2 = \mathbf{2} \qquad\text{against}\qquad \dim\mathbf{N}(S - I) = \mathbf{1}$$

**Which explanation tells you more.** PS 4's argument — $M^{-1}IM = I$ for every $M$ — is **correct, complete, and explains nothing.** It works only because $I$ is exceptional, and gives no method for any other pair.

**The geometric multiplicity is a genuine invariant** that applies to every pair of matrices, and it says *what* differs: $I$ has a full basis of eigenvectors and $S$ does not. **It generalises; the $M^{-1}IM$ trick does not.**

*Marking: 1 for the polynomials, 2 for the invariant with both values, 2 for the comparison. **The comparison is the question**; a script giving only the invariant gets 3.*

### (d) [6]

**Two-eigenvalue case.** Suppose $Av_1 = \lambda_1v_1$, $Av_2 = \lambda_2v_2$, $\lambda_1 \ne \lambda_2$, $v_i \ne 0$, and

$$c_1v_1 + c_2v_2 = 0.$$

Apply $A$: $c_1\lambda_1v_1 + c_2\lambda_2v_2 = 0$. Subtract $\lambda_2\times$ the original:

$$c_1(\lambda_1 - \lambda_2)v_1 = 0.$$

Since $\lambda_1 \ne \lambda_2$ and $v_1 \ne 0$, $c_1 = 0$; then $c_2v_2 = 0$ gives $c_2 = 0$. $\square$

**The induction:** assume any $k$ eigenvectors for distinct eigenvalues are independent; given $k+1$, apply the same subtraction (apply $A$, subtract $\lambda_{k+1}$ times the relation) to kill the last term and reduce to $k$.

**The converse fails.** $I_2$ has the repeated eigenvalue $1$ and **is** diagonalisable — it is already diagonal. *(Or $2I$, or any diagonal matrix with a repeated entry.)*

*Marking: 4 for the base case done properly, 1 for the induction sketch, 1 for the converse example. **The subtraction step is the proof**; a script that says "clearly independent" gets 0.*

---

## Q5: Structure (16 points)

### (a) [4]

$\lambda = 0$ is an eigenvalue $\iff$ there is $v \ne 0$ with $Av = 0v = 0$ $\iff$ $\mathbf{N}(A) \ne \{0\}$ $\iff$ $A$ is singular.

**Connects to characterisation 3** of Week 1's L05 §2 — *$Ax = 0$ only for $x = 0$* — and hence to all seven.

### (b) [4]

$$\det(A^\mathsf{T} - \lambda I) = \det\big((A - \lambda I)^\mathsf{T}\big) = \det(A - \lambda I)$$

using $(\lambda I)^\mathsf{T} = \lambda I$ and Week 5's L18 §3. **Same characteristic polynomial, same eigenvalues.** $\square$

**Eigenvectors: no.** For $A = \begin{bmatrix}1&1\\0&1\end{bmatrix}$, the eigenvector for $\lambda = 1$ is $(1,0)$. For $A^\mathsf{T} = \begin{bmatrix}1&0\\1&1\end{bmatrix}$,

$$A^\mathsf{T} - I = \begin{bmatrix}0&0\\1&0\end{bmatrix}, \qquad \mathbf{N} = \operatorname{span}\{(0,1)\}$$

**Different eigenvector, same eigenvalue.** *(The eigenvectors of $A^\mathsf{T}$ are the **left** eigenvectors of $A$ — and Week 3's left null space was the $\lambda = 0$ case of exactly this.)*

*Marking: 2 for the proof, 2 for the eigenvector counterexample computed.*

### (c) [4]

Write $p(\lambda) = \det(A - \lambda I)$ two ways and set $\lambda = 0$:

- Directly: $p(0) = \det(A - 0I) = \det A$.
- Factored: $p(\lambda) = (-1)^n(\lambda - \lambda_1)\cdots(\lambda - \lambda_n)$, so $p(0) = (-1)^n(-\lambda_1)\cdots(-\lambda_n) = (-1)^n(-1)^n\prod\lambda_i = \prod\lambda_i$.

**Hence $\det A = \prod\lambda_i$.** $\square$

*Marking: 4, with 2 for handling the two sign factors correctly — they cancel, and a script that ignores them has got the right answer by luck.*

### (d) [4]

**Two sentences, and both are needed:**

**Similar matrices have the same characteristic polynomial**, because $\det(M^{-1}AM - \lambda I) = \det\big(M^{-1}(A - \lambda I)M\big) = \det(A - \lambda I)$ by Week 5's product rule — so they have the same eigenvalues.

**And the trace is the sum of the eigenvalues while the determinant is their product**, so both are determined by a quantity that is already basis-independent. **Week 4's two mysterious invariants are consequences of one better invariant.**

*Marking: 2 per sentence. **This is the best question on the paper** — it asks the student to explain something they were told to accept in Week 4 and could not have justified until now. Note any script that says so.*

---

## Grade Distribution Expected

| Band | Score | Description |
|---|---|---|
| Strong | 88–100 | Q2(c)/(e) distinguished correctly, Q4(c)'s comparison, Q5(d) in two clean sentences |
| Solid | 72–87 | Q1 and Q3 correct; multiplicities right; interpretive parts thin |
| Passing | 55–71 | Eigenvalues and eigenvectors computed and verified |
| Concerning | < 55 | **Q2(c) called defective, or eigenvectors unverified.** Week 7 is entirely the defective/diagonalisable dichotomy and cannot be survived without it. Help Desk before Week 8 |

---

*MATH 241 · Week 6 · PS 6 Solutions · © CSE Department*
