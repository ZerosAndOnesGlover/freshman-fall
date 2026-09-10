# MATH 241 · Linear Algebra
## Week 10 · Lecture 2 of 3 · **Tuesday**
### Positive Definite Matrices and Quadratic Forms

---

**Reading:** Strang §6.5 · **Previous:** L30, the spectral theorem · **Next:** L32, what positive definiteness is for

> **Midterm 2 is tomorrow**, Nov 12, **18:00–19:15, SSB 110**, covering **Weeks 6–9**. **Nothing
> from this week is on it**, and the last hour of revision is better spent on Week 7's
> diagonalisation than on today's material.
>
> **Recitation 9 is Thursday** — the day after the paper — and covers **Week 9**. **PS 9 is due
> Friday at 17:00.**

---

## 1. The Question L30 Left Open

**L30 §8 ended on a warning.** Symmetry buys you *real* eigenvalues. It does not buy you *positive* ones: $\begin{bmatrix}5&5\\5&3\end{bmatrix}$ is symmetric and has eigenvalues $9.099$ and $-1.099$.

**So: which symmetric matrices have all eigenvalues positive?** That is today's entire subject, and the reason it deserves a lecture is that the answer has **five completely different forms** — one geometric, one spectral, one from elimination, one from determinants, one from factorisation — and they are all equivalent, and each is the cheap one in some situation.

> **Why anyone cares.** Positive definite is the matrix version of *positive number*. It is the
> condition under which a quadratic has a minimum rather than a saddle, under which a physical
> system is stable, under which Cholesky works, under which a covariance matrix is a covariance
> matrix, and under which the fastest linear solvers apply. **You will meet it in optimisation,
> statistics, mechanics and machine learning, and it will be the same condition every time.**

---

## 2. The Quadratic Form

**A matrix eats a vector and returns a vector. A quadratic form eats a vector and returns a number.**

$$f(x) = x^\mathsf{T}Ax = \sum_{i}\sum_{j} a_{ij}x_ix_j.$$

For $2\times2$ with $A = \begin{bmatrix}a&b\\b&c\end{bmatrix}$:

$$x^\mathsf{T}Ax = ax_1^2 + 2b\,x_1x_2 + cx_2^2.$$

**Every quadratic in $n$ variables with no linear or constant term is $x^\mathsf{T}Ax$ for exactly one symmetric $A$**, and that is why only symmetric matrices are ever considered here. If $A$ were not symmetric, only $\tfrac12(A + A^\mathsf{T})$ would show up in $f$ — **the antisymmetric part contributes nothing**, since $x^\mathsf{T}Mx = 0$ whenever $M^\mathsf{T} = -M$. *(One line: $x^\mathsf{T}Mx$ is a scalar, so it equals its own transpose $x^\mathsf{T}M^\mathsf{T}x = -x^\mathsf{T}Mx$.)*

> **So restricting to symmetric matrices costs nothing at all here.** Quadratic forms cannot see
> anything else.

### The definition

$$\boxed{\;A \text{ is \textbf{positive definite} if } x^\mathsf{T}Ax > 0 \text{ for every } x \ne 0.\;}$$

**Positive *semi*definite** weakens $>$ to $\ge$. **Indefinite** means it takes both signs. Note the *for every $x$*: checking a few vectors can disprove positive definiteness and can never prove it.

On this week's $A = \begin{bmatrix}5&0&-2\\0&3&-2\\-2&-2&4\end{bmatrix}$, four samples (`symmetric.py` §5):

| $x$ | $(1,0,0)$ | $(1,1,1)$ | $(3,-2,5)$ | $(1,2,2)$ |
|---|---:|---:|---:|---:|
| $x^\mathsf{T}Ax$ | $5$ | $4$ | $137$ | $9$ |

**All positive — and that proves nothing.** There are infinitely many $x$ left. §3 is how you actually decide.

---

## 3. Five Tests, and They Are the Same Test

For a **symmetric** $A$, the following are equivalent:

| # | Test | Cost | Best when |
|---|---|---|---|
| **1** | $x^\mathsf{T}Ax > 0$ for all $x \ne 0$ | — | proving theorems |
| **2** | every eigenvalue $\lambda_i > 0$ | $O(n^3)$, iterative | you already have them |
| **3** | every **pivot** is positive | $\tfrac{n^3}{3}$, direct | you are eliminating anyway |
| **4** | every **leading** principal minor $> 0$ | $O(n^3)$ | $n$ is $2$ or $3$, by hand |
| **5** | $A = R^\mathsf{T}R$ with $R$ having independent columns | $\tfrac{n^3}{6}$ | you want the answer *and* a factorisation |

**Test 3 is the practical one and it is the one nobody expects**, because pivots come from elimination and eigenvalues come from a different algorithm entirely, and there is no reason from the definitions why they should agree even in sign. §4 is why.

### The threshold, computed

Take our matrix and let the corner entry vary:

$$A(b) = \begin{bmatrix}5&0&-2\\0&3&-2\\-2&-2&b\end{bmatrix}, \qquad \det A(b) = 5(3b - 4) - 2\cdot 6 = 15b - 32.$$

**So test 4 says positive definite exactly when $b > \tfrac{32}{15} = 2.1\overline{3}$**, since the first two leading minors are $5$ and $15$ regardless of $b$. **Test 2 and test 3 must therefore flip at the same place**, and `symmetric.py` §5 checks that they do:

| $b$ | eigenvalues | pivots | leading minors | pd? |
|---:|---|---|---|:--:|
| $1$ | $6.06418,\ 3.69459,\ -0.75877$ | $5,\ 3,\ -\tfrac{17}{15}$ | $5,\ 15,\ -17$ | no |
| $2$ | $6.29707,\ 3.78680,\ -0.08387$ | $5,\ 3,\ -\tfrac{2}{15}$ | $5,\ 15,\ -2$ | no |
| $\tfrac{32}{15} - \tfrac{1}{1000}$ | $6.33306,\ 3.79990,\ -0.00062$ | $5,\ 3,\ -\tfrac{1}{1000}$ | $5,\ 15,\ -\tfrac{3}{200}$ | no |
| $\mathbf{\tfrac{32}{15}}$ | $6.33333,\ 3.80000,\ \mathbf{0}$ | $5,\ 3,\ \mathbf{0}$ | $5,\ 15,\ \mathbf{0}$ | **semi** |
| $\tfrac{32}{15} + \tfrac{1}{1000}$ | $6.33361,\ 3.80010,\ 0.00062$ | $5,\ 3,\ \tfrac{1}{1000}$ | $5,\ 15,\ \tfrac{3}{200}$ | **yes** |
| $3$ | $6.60388,\ 3.89008,\ 0.50604$ | $5,\ 3,\ \tfrac{13}{15}$ | $5,\ 15,\ 13$ | **yes** |
| $4$ | $\mathbf{7,\ 4,\ 1}$ | $5,\ 3,\ \tfrac{28}{15}$ | $5,\ 15,\ 28$ | **yes** |

**All three tests change their answer at exactly $b = \tfrac{32}{15}$**, and only the exact determinant locates that point — the eigenvalue at $b = \tfrac{32}{15} - \tfrac{1}{1000}$ is $-6.2\times10^{-4}$, which no floating-point test would confidently call negative.

> **At $b = \tfrac{32}{15}$ the matrix is positive *semi*definite**: smallest eigenvalue $0$, last
> pivot $0$, determinant $0$. **The boundary of the positive definite matrices is exactly the
> singular ones**, which is the right mental picture — a positive definite matrix is invertible,
> and it fails to be so precisely by an eigenvalue reaching zero.

---

## 4. Why Pivots and Eigenvalues Agree in Sign

**They are not the same numbers.** Our $A$ has eigenvalues $1, 4, 7$ and pivots $5, 3, \tfrac{28}{15}$. **Neither list determines the other.** What is true — **Sylvester's law of inertia** — is that the *number of positive, negative and zero* entries agrees.

`symmetric.py` §6 checks four matrices:

| Matrix | eigenvalue signs | pivot signs | diagonal signs |
|---|:--:|:--:|:--:|
| $A$ (this week's) | $+\,+\,+$ | $+\,+\,+$ | $+\,+\,+$ |
| $\begin{bmatrix}1&3\\3&1\end{bmatrix}$ | $+\,-$ | $+\,-$ | $\mathbf{+\,+}$ |
| $\begin{bmatrix}2&-1&0\\-1&2&-1\\0&-1&2\end{bmatrix}$ | $+\,+\,+$ | $+\,+\,+$ | $+\,+\,+$ |
| $\begin{bmatrix}1&0\\0&-1\end{bmatrix}$ | $+\,-$ | $+\,-$ | $+\,-$ |

> **Row two is the trap, and it is on every exam.** $\begin{bmatrix}1&3\\3&1\end{bmatrix}$ has both
> diagonal entries positive and is **indefinite** — eigenvalues $4$ and $-2$, pivots $1$ and $-8$.
> **Positive diagonal entries are necessary and nowhere near sufficient.** *(Necessary because
> $e_i^\mathsf{T}Ae_i = a_{ii}$, so a non-positive diagonal entry kills the matrix immediately —
> and that is the first thing to check, precisely because it is free.)*

**The pivot signs always match. The diagonal signs need not.** §5 is why.

---

## 5. $LDL^\mathsf{T}$ Is Completing the Square

**This is the reason the pivot test works**, and it is one of the more satisfying arguments in the course.

Week 1 factored $A = LU$. For symmetric $A$, pull the pivots out of $U$ into a diagonal matrix $D$; what is left is $L^\mathsf{T}$:

$$A = LDL^\mathsf{T}, \qquad L \text{ unit lower triangular}, \qquad D = \operatorname{diag}(\text{pivots}).$$

For our $A$ (`symmetric.py` §7, exact):

$$L = \begin{bmatrix}1&0&0\\ 0&1&0\\ -\tfrac25 & -\tfrac23 & 1\end{bmatrix}, \qquad D = \begin{bmatrix}5&&\\&3&\\&&\tfrac{28}{15}\end{bmatrix}, \qquad LDL^\mathsf{T} = A.$$

**$D$ holds Week 5's pivots, unchanged.** Now substitute into the quadratic form and set $y = L^\mathsf{T}x$:

$$x^\mathsf{T}Ax = x^\mathsf{T}LDL^\mathsf{T}x = (L^\mathsf{T}x)^\mathsf{T}D(L^\mathsf{T}x) = y^\mathsf{T}Dy = \boxed{\;d_1y_1^2 + d_2y_2^2 + \cdots + d_ny_n^2\;}$$

**A sum of squares with the pivots as coefficients.** Written out for our $A$:

$$x^\mathsf{T}Ax = 5\left(x_1 - \tfrac25x_3\right)^2 + 3\left(x_2 - \tfrac23x_3\right)^2 + \tfrac{28}{15}x_3^2.$$

Verified exactly at four random integer vectors:

| $x$ | $(8,-6,2)$ | $(-7,-2,8)$ | $(-4,-1,-1)$ | $(2,-5,-9)$ |
|---|---:|---:|---:|---:|
| $x^\mathsf{T}Ax$ | $428$ | $801$ | $67$ | $311$ |
| $\sum d_ky_k^2$ | $428$ | $801$ | $67$ | $311$ |

> **And now the proof writes itself.** $L^\mathsf{T}$ is invertible (unit triangular), so $y = 0$
> only when $x = 0$. If every $d_k > 0$, then $x^\mathsf{T}Ax$ is a sum of positive multiples of
> squares and is therefore $> 0$ unless every $y_k = 0$ — that is, unless $x = 0$.
> **Positive pivots $\Longrightarrow$ positive definite**, in two sentences.
>
> **And elimination *is* completing the square.** The two techniques you have been taught
> separately since school are the same procedure, and $L$ records the substitutions.

**The converse direction** — positive definite $\Longrightarrow$ positive pivots — is L31 exercise 5, and it follows by feeding in the right $x$.

---

## 6. The Geometry: $x^\mathsf{T}Ax = 1$

**The level sets are where positive definiteness becomes visible.** Take

$$E = \begin{bmatrix}5&4\\4&5\end{bmatrix}, \qquad E(1,1) = 9(1,1), \quad E(1,-1) = 1\,(1,-1),$$

so $\lambda = 9$ along $(1,1)/\sqrt2$ and $\lambda = 1$ along $(1,-1)/\sqrt2$. The curve $x^\mathsf{T}Ex = 1$ is

$$5x_1^2 + 8x_1x_2 + 5x_2^2 = 1,$$

which in the eigenvector coordinates $y = Q^\mathsf{T}x$ becomes $9y_1^2 + y_2^2 = 1$ — **an ellipse in standard position.** `symmetric.py` §8 confirms the semi-axes:

| $\lambda$ | direction | semi-axis $1/\sqrt\lambda$ | check $x^\mathsf{T}Ex$ |
|---:|---|---:|---:|
| $9$ | $(1,1)/\sqrt2$ | $0.3333333333$ | $1.000000000000$ |
| $1$ | $(1,-1)/\sqrt2$ | $1.0000000000$ | $1.000000000000$ |

> **The axes of the ellipse are the eigenvectors and their lengths are $1/\sqrt{\lambda}$.**
> The **large** eigenvalue gives the **short** axis: a direction the matrix stretches hard is a
> direction you need to travel little in to reach the level set.

**The classification, which is the whole of §3 in a picture:**

| Eigenvalues | $x^\mathsf{T}Ax = 1$ | Surface $z = x^\mathsf{T}Ax$ |
|---|---|---|
| all $> 0$ | ellipse / ellipsoid | **bowl** — a strict minimum at $0$ |
| all $< 0$ | empty | dome — a strict maximum |
| mixed signs | hyperbola | **saddle** |
| one zero, rest $> 0$ | parallel lines (a trough) | **valley** — a flat direction |

**And the ratio of the longest axis to the shortest is $\sqrt{\lambda_\max/\lambda_\min} = \sqrt{\operatorname{cond}(A)}$**, here $\sqrt9 = 3$. A round ellipse is a well-conditioned matrix, **literally and not by analogy** — L32 §3 makes that exact.

---

## 7. $A^\mathsf{T}A$, Which You Have Been Using Since Week 8

**Every $A^\mathsf{T}A$ is symmetric** — Week 1's L06 §2 — **and positive semidefinite, always**:

$$x^\mathsf{T}(A^\mathsf{T}A)x = (Ax)^\mathsf{T}(Ax) = \lVert Ax\rVert^2 \ge 0.$$

**And it is zero exactly when $Ax = 0$.** So

$$\boxed{\;A^\mathsf{T}A \text{ is positive definite} \iff \mathbf{N}(A) = \{0\} \iff A \text{ has independent columns.}\;}$$

**That is PS 2 Q5(c)**, proved in Week 2 before there was any word for it, and used in every week since Week 8. `symmetric.py` §11:

| $A$ | $A^\mathsf{T}A$ | eigenvalues | verdict |
|---|---|---|---|
| $\begin{bmatrix}1&0\\1&1\\1&2\end{bmatrix}$ | $\begin{bmatrix}3&3\\3&5\end{bmatrix}$ | $7.162278,\ 0.837722$ | positive definite |
| $\begin{bmatrix}1&2\\1&2\\1&2\end{bmatrix}$ | $\begin{bmatrix}3&6\\6&12\end{bmatrix}$ | $15,\ \mathbf{0}$ | positive **semi**definite |
| Week 9's fitting matrix | $\begin{bmatrix}3&6\\6&14\end{bmatrix}$ | $16.639410,\ 0.360590$ | positive definite |

> **The middle row is Week 9's dependent-columns failure, seen from this side.** The normal
> equations were unsolvable there because $A^\mathsf{T}A$ had a zero eigenvalue — **not because the
> projection failed to exist**, which is the distinction L27 §6 insisted on.

**And test 5 of §3 is this fact read backwards:** $A$ is positive definite exactly when $A = R^\mathsf{T}R$ for some $R$ with independent columns. **Finding that $R$ is Cholesky**, which is L32 §2.

---

## 8. What to Take Away

1. **$x^\mathsf{T}Ax$ sees only the symmetric part of $A$**, so quadratic forms and symmetric matrices are the same subject.
2. **Positive definite: $x^\mathsf{T}Ax > 0$ for every $x \ne 0$.** Sampling can disprove it and can never prove it.
3. **Five equivalent tests**: the form, the eigenvalues, the pivots, the leading minors, $A = R^\mathsf{T}R$. **They flip together, at the same parameter value, exactly.**
4. **Positive diagonal entries are necessary and not sufficient** — $\begin{bmatrix}1&3\\3&1\end{bmatrix}$.
5. **$A = LDL^\mathsf{T}$, and $x^\mathsf{T}Ax = \sum d_ky_k^2$ with $y = L^\mathsf{T}x$.** Elimination *is* completing the square, and this is the proof that positive pivots suffice.
6. **Sylvester's law of inertia:** pivot signs match eigenvalue signs. The numbers do not match.
7. **$x^\mathsf{T}Ax = 1$ is an ellipse with axes along the eigenvectors and semi-axes $1/\sqrt{\lambda}$.** Its aspect ratio is $\sqrt{\operatorname{cond}(A)}$.
8. **$A^\mathsf{T}A$ is always positive semidefinite, and positive definite exactly when $A$'s columns are independent.**

---

## Exercises

*(Not assessed. PS 10 is the assessed work.)*

1. Is $\begin{bmatrix}2&-1\\-1&2\end{bmatrix}$ positive definite? Answer by **all four** computable tests and confirm they agree.
2. For which $c$ is $\begin{bmatrix}1&c\\c&9\end{bmatrix}$ positive definite? Positive semidefinite? Indefinite? **Sketch the three regimes.**
3. Write $x^\mathsf{T}Ax$ for our $A$ as a sum of three squares, from the $L$ and $D$ in §5, and verify at $x = (1,1,1)$ against the value $4$ in §2.
4. $A$ is positive definite. Prove that $A^{-1}$ is too. *(Eigenvalues.)* Prove that $A^2$ is too. **Is $A + B$ positive definite when both are? Is $AB$?**
5. Prove the converse in §5: **positive definite $\Longrightarrow$ every pivot positive.** *(Take $x$ with $y = L^\mathsf{T}x = e_k$; such an $x$ exists because $L^\mathsf{T}$ is invertible.)*
6. **Why "leading" minors?** Find a symmetric matrix all of whose *non*-leading $2\times2$ principal minors are positive and which is not positive definite. Then find one with $\det A > 0$ that is not positive definite. *(In $2\times2$ this is easy; say what goes wrong.)*
7. Sketch $x^\mathsf{T}Ax = 1$ for $A = \begin{bmatrix}1&0\\0&4\end{bmatrix}$, then for $\begin{bmatrix}1&0\\0&-4\end{bmatrix}$, then for $\begin{bmatrix}1&0\\0&0\end{bmatrix}$. **Name each curve.**
8. $A$ is $3\times5$. Is $A^\mathsf{T}A$ ever positive definite? Is $AA^\mathsf{T}$? **Answer with dimensions, not examples.**

---

*MATH 241 · Week 10 · L31 · © CSE Department*
