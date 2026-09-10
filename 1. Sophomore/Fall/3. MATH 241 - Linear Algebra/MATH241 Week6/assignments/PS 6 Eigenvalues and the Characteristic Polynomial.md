# MATH 241 · Problem Set 6
## Eigenvalues and the Characteristic Polynomial

---

**Released:** Week 6, Wednesday · **Due:** Week 7, **Friday 17:00**
**Total: 100 points** · Submit one PDF, `PS6_{LastName}_{StudentID}.pdf`

> **Exact arithmetic throughout.** Eigenvalues here are integers or simple surds; if you meet an
> ugly decimal, you have made an arithmetic error.
>
> **Check every eigenvector.** One matrix–vector product, exact, and it catches what elimination
> errors otherwise hide. **An unverified eigenvector earns no marks for the verification.**
>
> **Check every eigenvalue set against the trace and the determinant.** Two free checks, and they
> are worth marks on this paper.
>
> **Recitation 6 is the Thursday before this is due**, 15:00–15:50, SSB 108.

---

### Q1: Finding Them (24 points)

$$A = \begin{bmatrix}3&-2&2\\ 2&3&2\\ 2&2&3\end{bmatrix}$$

**(a) [8]** Compute $\det(A - \lambda I)$ as a polynomial in $\lambda$, **by cofactor expansion.**

State in one sentence **why elimination cannot be used here**, referring to what it would have to divide by.

**(b) [4]** Factor it and give the three eigenvalues.

**(c) [8]** For each eigenvalue, find the eigenspace $\mathbf{N}(A - \lambda I)$ and give a basis. **Verify each eigenvector satisfies $Av = \lambda v$.**

**(d) [4]** Check your eigenvalues against $\operatorname{trace}A$ and $\det A$. **Show both computations.** Then state why these two checks are free — that is, why you did not have to compute anything new to run them.

---

### Q2: Predict Before You Compute (18 points)

For each transformation of $\mathbb{R}^2$, **state the eigenvalues and eigenvectors from the geometry, before writing down any matrix.** Then write the matrix and confirm.

**(a) [3]** Reflection across the $y$-axis.
**(b) [3]** Projection onto the $x$-axis.
**(c) [3]** Rotation by $180°$.
**(d) [3]** Rotation by $60°$.
**(e) [3]** The shear $(x,y) \mapsto (x + 4y,\ y)$.
**(f) [3]** $\begin{bmatrix}2&7&1\\ 0&5&3\\ 0&0&-1\end{bmatrix}$ — **write the eigenvalues down immediately** and say why you may.

> **Two of (a)–(e) are the interesting ones.** One has **no real eigenvalues at all**, and one has
> **fewer independent eigenvectors than its size.** Identify both and say what each says about the
> geometry.

---

### Q3: The Characteristic Polynomial (20 points)

**(a) [4]** Use the $2\times2$ shortcut $\lambda^2 - (\operatorname{trace})\lambda + \det = 0$ on $\begin{bmatrix}5&2\\ 2&2\end{bmatrix}$. Give the eigenvalues and both eigenvectors.

**(b) [5]** $B = \begin{bmatrix}1&-2\\ 1&3\end{bmatrix}$. Find its characteristic polynomial and show it has **no real roots.**

Find the two complex eigenvalues, and verify that their **sum is the trace** and their **product is the determinant**. **What does "no real eigenvalue" say about $B$ as a transformation?**

**(c) [5]** $A$ is $3\times3$ with eigenvalues $2, -1, 4$. Without knowing $A$, give:

$\operatorname{trace}A$; $\det A$; the eigenvalues of $A^2$; of $A^{-1}$; of $A + 3I$; of $A^\mathsf{T}$.

**Justify the last three in one line each.**

**(d) [6]** $A$ satisfies $A^3 = A$. **Prove every eigenvalue of $A$ is $0$, $1$ or $-1$**, without computing any determinant.

Then: **does $A^3 = A$ force $A$ to be one of $0$, $I$, or a reflection?** Give a $2\times2$ matrix satisfying $A^3 = A$ that is none of those three.

---

### Q4: Multiplicities (22 points)

**(a) [6]** For $C = \begin{bmatrix}3&1&0\\ 0&3&0\\ 0&0&5\end{bmatrix}$, give the **algebraic** and **geometric** multiplicity of every eigenvalue. **Is $C$ defective?** Justify.

**(b) [5]** Construct a $3\times3$ matrix with a single eigenvalue $\lambda = 4$ of algebraic multiplicity $3$ and geometric multiplicity **exactly 2**. **Verify both multiplicities.**

**(c) [5]** $I$ and $S = \begin{bmatrix}1&1\\ 0&1\end{bmatrix}$ share their trace, determinant, rank **and characteristic polynomial**.

- Show the characteristic polynomials really are equal.
- **Give the invariant that distinguishes them**, with both values.
- PS 4 Q5(d) proved they are not similar by a different argument. **Which of the two explanations tells you more, and why?**

**(d) [6]** Prove: **$n$ distinct eigenvalues $\Rightarrow$ $n$ independent eigenvectors.**

*(Do the two-eigenvalue case in full, as in L20 §6, and say how the induction goes.)*

Then give a matrix with a **repeated** eigenvalue that **is** diagonalisable, showing the converse fails.

---

### Q5: Structure (16 points)

**(a) [4]** Prove that $\lambda = 0$ is an eigenvalue of $A$ **if and only if** $A$ is singular. Which of Week 1's seven characterisations does this connect to?

**(b) [4]** Prove that $A$ and $A^\mathsf{T}$ have the same eigenvalues. *(One line, from Week 5's L18 §3.)*

**Do they have the same eigenvectors?** Settle it with $\begin{bmatrix}1&1\\ 0&1\end{bmatrix}$.

**(c) [4]** $A$ is $n\times n$ with eigenvalues $\lambda_1,\dots,\lambda_n$. Prove $\det A = \prod\lambda_i$ **directly**, by setting $\lambda = 0$ in the characteristic polynomial written two ways.

**(d) [4]** Week 4's L15 §6 found that similar matrices share trace and determinant, and could not say why. **Explain both facts in two sentences, using this week's material.**

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Finding them | 24 |
| 2 | Predict before you compute | 18 |
| 3 | The characteristic polynomial | 20 |
| 4 | Multiplicities | 22 |
| 5 | Structure | 16 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*MATH 241 · Week 6 · PS 6 · © CSE Department*
