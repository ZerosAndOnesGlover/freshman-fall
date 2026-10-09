# MATH 241 · Linear Algebra
## Week 6 · Lecture 2 of **2** · **Friday**
### The Characteristic Polynomial

*“A ring of polynomials in any number of variables over a ring of coefficients that has an identity element and a finite basis, itself has a finite basis.”* — Emmy Noether, as quoted in Morris Kline, *Mathematical Thought from Ancient to Modern Times* (1972), p. 1153

---

**Reading:** Strang §6.1 (second half), §6.2 opening · **Previous:** L19, eigenvalues and eigenvectors · **Next:** Week 7, diagonalisation

**Coursework:** 📝 **PS 5** due today 17:00 · 📊 **Quiz 7** Mon of Week 7 · 📝 **PS 7** released Wed of Week 7, due Fri of Week 8 17:00 · 💬 **Recitation 6** Thu of Week 7 15:00–15:50

> **PS 5 is due at 17:00 today.** PS 6 was released Wednesday and is due the Friday of Week 7.
>
> **Midterm 1 was Wednesday.** Papers are returned in Week 7.
>
> **This is Week 6's second and last lecture** — Monday was Fall Break.

---

## 1. The Polynomial

$$p(\lambda) = \det(A - \lambda I)$$

is the **characteristic polynomial** of $A$, and L19 §3 established that **its roots are exactly the eigenvalues.**

**It is a polynomial of degree $n$**, and you can see why from the $n!$ formula (Week 5's L17 §1): the only term contributing $\lambda^n$ is the product down the diagonal, $(a_{11}-\lambda)(a_{22}-\lambda)\cdots(a_{nn}-\lambda)$, and every other term omits at least two diagonal entries. So

$$p(\lambda) = (-1)^n\lambda^n + \dots$$

> **A convention worth settling now.** These notes use $\det(A - \lambda I)$, following Strang, so
> the leading coefficient is $(-1)^n$ — negative for odd $n$, as in L19 §4's
> $-\lambda^3 + 6\lambda^2 - 11\lambda + 6$. **Many books use $\det(\lambda I - A)$ instead**, which
> is monic. **The roots are identical**; only the overall sign differs. Check which convention a
> source uses before comparing coefficients with it.

**By the fundamental theorem of algebra, $p$ has exactly $n$ roots in $\mathbb{C}$, counted with multiplicity.** So:

$$\boxed{\;\text{every } n\times n \text{ matrix has exactly } n \text{ eigenvalues over } \mathbb{C}\;}$$

**Always $n$ — no exceptions, no hypotheses.** They may be complex (L19 §6's rotation) and they may repeat (L19 §7's shear), but they are always there and there are always $n$. **What is *not* guaranteed is $n$ independent eigenvectors**, and §5 is that distinction.

---

## 2. Trace and Determinant, Explained at Last

Write $p$ in factored form and compare coefficients with the expanded form. Two of them are readable:

$$\boxed{\;\lambda_1 + \lambda_2 + \dots + \lambda_n = \operatorname{trace}A\;} \qquad\qquad \boxed{\;\lambda_1\lambda_2\cdots\lambda_n = \det A\;}$$

*(The determinant one is immediate: set $\lambda = 0$ in $p(\lambda) = \det(A - \lambda I)$ to get $p(0) = \det A$, and in factored form $p(0)$ is $\pm$ the product of the roots.)*

**Verified on L19's matrix:** eigenvalues $1, 2, 3$; $\operatorname{trace}A = 6 = 1+2+3$ ✓; $\det A = 6 = 1\times2\times3$ ✓

### Why this is the payoff of Week 4

Week 4's L15 §6 found that similar matrices share **rank, trace and determinant**, and could say what that meant for only one of them. Rank was easy — it is $\dim(\text{range})$, a property of the map. **Trace and determinant were verified and unexplained.**

**Now they have meanings.** They are the sum and the product of the eigenvalues, and **the eigenvalues themselves are basis-independent:**

$$\det(M^{-1}AM - \lambda I) = \det\big(M^{-1}(A - \lambda I)M\big) = \det(A - \lambda I)$$

by Week 5's L18 §4. **So similar matrices have the same characteristic polynomial**, hence the same eigenvalues, hence the same trace and determinant. **Week 4's two mysterious invariants are consequences of one better invariant.**

> **This is also a free sanity check and you should use it constantly.** Compute eigenvalues; add
> them and compare with the trace; multiply them and compare with the determinant. **Two independent
> checks, five seconds, and they catch nearly every arithmetic error in a $2\times2$ or $3\times3$.**

---

## 3. The $2\times2$ Shortcut

For $2\times2$, comparing coefficients gives

$$p(\lambda) = \lambda^2 - (\operatorname{trace}A)\lambda + \det A$$

**with no determinant expansion at all.** So for

$$A = \begin{bmatrix}3&1\\ 1&3\end{bmatrix}: \qquad \lambda^2 - 6\lambda + 8 = 0 \quad\Longrightarrow\quad \lambda = 2, 4$$

**Two numbers read straight off the matrix.** Use this for every $2\times2$ you meet — it is faster than expanding, and the trace/determinant check is built in.

*(For $3\times3$ there is an analogous formula with a middle coefficient built from the three $2\times2$ principal minors. **It is not worth memorising**; expand the determinant.)*

---

## 4. Eigenvalues You Get for Free

**Triangular matrices: the diagonal.** $\det(A - \lambda I)$ is the product of the diagonal entries minus $\lambda$, so the roots are the diagonal entries. **Read them off.**

**Matrices satisfying a polynomial identity.** If $A$ satisfies $q(A) = 0$ for a polynomial $q$, then **every eigenvalue satisfies $q(\lambda) = 0$** — because $Av = \lambda v$ gives $q(A)v = q(\lambda)v$, and $q(A) = 0$ with $v \ne 0$ forces $q(\lambda) = 0$.

| $A$ satisfies | Eigenvalues must satisfy | So $\lambda \in$ |
|---|---|---|
| $P^2 = P$ (projection) | $\lambda^2 = \lambda$ | $\{0, 1\}$ |
| $R^2 = I$ (reflection) | $\lambda^2 = 1$ | $\{1, -1\}$ |
| $N^k = 0$ (nilpotent) | $\lambda^k = 0$ | $\{0\}$ **only** |

**No determinant, no elimination.** *(The nilpotent row explains Week 4's $D$ on $\mathbb{P}_3$: $D^4 = 0$, so **every eigenvalue of differentiation is zero** — and indeed $D$ is triangular with a zero diagonal. Its only eigenvectors are the constants.)*

> **The converse fails and matters.** Knowing $\lambda \in \{0,1\}$ does not make $A$ a projection.
> The identity constrains the eigenvalues; it does not determine the matrix.

---

## 5. The Two Multiplicities

**This is the most important distinction in the lecture**, and it is the entire hinge of Week 7.

> **Algebraic multiplicity** of $\lambda$: how many times it repeats as a root of $p$.
>
> **Geometric multiplicity** of $\lambda$: $\dim\mathbf{N}(A - \lambda I)$ — the dimension of the
> eigenspace.

**They can differ, and when they do the matrix is in trouble.**

| Matrix | $p(\lambda)$ | $\lambda$ | Algebraic | Geometric | |
|---|---|---|---|---|---|
| $I_2$ | $(1-\lambda)^2$ | $1$ | $2$ | $2$ | fine |
| $\begin{bmatrix}1&1\\0&1\end{bmatrix}$ | $(1-\lambda)^2$ | $1$ | $2$ | $\mathbf{1}$ | **defective** |

**Same characteristic polynomial. Different geometric multiplicity.** *(Verified in the script.)*

**Always $1 \le \text{geometric} \le \text{algebraic}$.** The lower bound holds because a root of $p$ makes $A - \lambda I$ singular, so the eigenspace is at least a line. The upper bound is a real theorem and is Week 7's.

> **A matrix is *defective* when some eigenvalue has geometric $<$ algebraic.** Equivalently: fewer
> than $n$ independent eigenvectors, so **no basis of eigenvectors, so no diagonalisation.**
> **Week 7 is exactly this dichotomy** — when the search for a good basis succeeds, and what to do
> when it does not.

### And it settles Week 4's leftover

PS 4 Q5(d) showed $I$ and $\begin{bmatrix}1&1\\0&1\end{bmatrix}$ are not similar, via $M^{-1}IM = I$. **Correct, and it explained nothing** — the two share trace, determinant, rank **and now characteristic polynomial.**

**The geometric multiplicity separates them**, and it is the first invariant since Week 4 that is genuinely new rather than a consequence of the old ones. **Two matrices with the same characteristic polynomial need not be similar; if they are diagonalisable and have the same eigenvalues, they are.** *(Both halves are Week 7.)*

---

## 6. Independent Eigenvalues Give Independent Eigenvectors

> **Theorem.** Eigenvectors for **distinct** eigenvalues are linearly independent.

*Sketch, for two.* Suppose $c_1v_1 + c_2v_2 = 0$ with $Av_i = \lambda_iv_i$ and $\lambda_1 \ne \lambda_2$. Apply $A$: $c_1\lambda_1v_1 + c_2\lambda_2v_2 = 0$. Now subtract $\lambda_2$ times the first equation: $c_1(\lambda_1 - \lambda_2)v_1 = 0$. Since $\lambda_1 \ne \lambda_2$ and $v_1 \ne 0$, we get $c_1 = 0$, and then $c_2 = 0$. $\square$ *(The general case is the same argument by induction.)*

**The consequence is the one to remember:**

$$\boxed{\;n \text{ distinct eigenvalues} \implies n \text{ independent eigenvectors} \implies \text{diagonalisable}\;}$$

**L19 §4's matrix had eigenvalues $1, 2, 3$ — distinct — so it is diagonalisable, without checking any eigenspace dimensions.** That is the common case and it is why defective matrices feel exotic.

> **The converse is false and worth stating.** $I$ has a single repeated eigenvalue and is
> diagonal already. **Distinct eigenvalues are sufficient, not necessary** — and Week 10 will show
> that *symmetric* matrices are always diagonalisable no matter how their eigenvalues repeat.

---

## 7. Two Things the Characteristic Polynomial Is Not

**It is not how anyone computes eigenvalues numerically.** Finding roots of a degree-$n$ polynomial is **badly conditioned** — tiny changes in the coefficients can move the roots enormously — and for $n \ge 5$ there is no formula at all (Abel–Ruffini). **Real software runs the QR algorithm**, iterating on the matrix directly and never forming $p$. *(Ironically, `numpy.roots` finds polynomial roots by building a companion matrix and computing **its** eigenvalues — the reverse of what you have just been taught.)*

**Do not confuse eigenvalues with pivots.** Both are $n$ numbers, both come from a triangular matrix, and **both multiply to $\det A$** — which makes the confusion tempting.

| | Pivots | Eigenvalues |
|---|---|---|
| From | elimination, $A = LU$ | roots of $\det(A - \lambda I)$ |
| Cost | $n^3/3$ | iterative; no closed form for $n \ge 5$ |
| Product | $\det A$ | $\det A$ |
| **Sum** | **nothing in particular** | **$\operatorname{trace}A$** |
| Change of basis | **not** invariant | **invariant** |

**L19 §4's matrix has eigenvalues $1, 2, 3$ and pivots $2, \tfrac32, 2$** — both products are $6$, and the two lists are otherwise unrelated. *(Week 1's matrix had pivots $2, 3, 4$ and its eigenvalues are none of those.)*

---

## 8. What to Take Away

1. **$p(\lambda) = \det(A - \lambda I)$ has degree $n$**, leading coefficient $(-1)^n$ in this course's convention. **Check which convention a source uses.**
2. **Every $n\times n$ matrix has exactly $n$ eigenvalues over $\mathbb{C}$**, with multiplicity. Always. What is not guaranteed is $n$ independent *eigenvectors*.
3. **$\sum\lambda_i = \operatorname{trace}A$ and $\prod\lambda_i = \det A$** — Week 4's two unexplained invariants, now consequences of a better one. **Use both as checks, every time.**
4. **Similar matrices have the same characteristic polynomial**, which is why the eigenvalues belong to the transformation.
5. **$2\times2$: $\lambda^2 - (\operatorname{trace})\lambda + \det = 0$.** Read it off.
6. **Triangular matrices hand you their diagonal**, and any identity $q(A) = 0$ constrains the eigenvalues to $q$'s roots.
7. **Algebraic multiplicity $\ge$ geometric multiplicity**, and a gap means **defective** — no basis of eigenvectors, no diagonalisation. **This is Week 7's dichotomy**, and it is the invariant that finally separates $I$ from the shear.
8. **$n$ distinct eigenvalues $\Rightarrow$ diagonalisable.** Sufficient, not necessary.
9. **Nobody computes eigenvalues from $p$**, and **pivots are not eigenvalues** even though both multiply to $\det A$.

---

## Exercises

*(Not assessed. PS 6 is due Friday of Week 7.)*

1. Find the characteristic polynomial, eigenvalues and eigenvectors of $\begin{bmatrix}4&1\\ 2&3\end{bmatrix}$. **Check trace and determinant against the eigenvalues.**
2. $A$ is $3\times3$ with eigenvalues $2, -1, 4$. Write down $\operatorname{trace}A$, $\det A$, the eigenvalues of $A^2$, of $A^{-1}$, and of $A + 3I$. *(The last two need one line of reasoning each.)*
3. Find the algebraic and geometric multiplicities of every eigenvalue of $\begin{bmatrix}2&1&0\\ 0&2&0\\ 0&0&3\end{bmatrix}$. **Is it defective?**
4. Show that $A$ and $A^\mathsf{T}$ have the same eigenvalues. *(Week 5's L18 §3, in one line.)* **Do they have the same eigenvectors?** Try $\begin{bmatrix}1&1\\0&1\end{bmatrix}$.
5. Prove that if $\lambda$ is an eigenvalue of $A$ then $\lambda + c$ is an eigenvalue of $A + cI$, with the same eigenvector. **What does this do to the characteristic polynomial?**
6. A $3\times3$ matrix has $\operatorname{trace} = 6$ and $\det = 6$ and one eigenvalue equal to $1$. **Find the other two.** *(Two equations, two unknowns — and this is L19 §4's matrix.)*
7. Construct a $3\times3$ matrix with a single eigenvalue $\lambda = 2$ of algebraic multiplicity 3 and geometric multiplicity **exactly 2**. *(Start from a diagonal matrix and add one entry.)*

---

*MATH 241 · Week 6 · L20 · © CSE Department*
