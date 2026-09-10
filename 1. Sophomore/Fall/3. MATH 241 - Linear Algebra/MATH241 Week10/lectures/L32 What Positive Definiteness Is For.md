# MATH 241 · Linear Algebra
## Week 10 · Lecture 3 of 3 · **Friday**
### What Positive Definiteness Is For

---

**Reading:** Strang §6.5, §11.1 · **Previous:** L31, positive definite matrices · **Next:** Week 11's L33, the singular value decomposition

> **Midterm 2 was Wednesday.** Marks and the post-mortem come in Recitation 10, the Thursday of
> Week 11. **The paper is not discussed today**, and today's material was not on it.
>
> **PS 9 is due at 17:00 today. PS 10 was released Wednesday** and is due Friday of Week 11.
>
> **Quiz 11 is the Monday of Week 11 and is the last quiz of the term.**

---

## 1. Why the Last Two Lectures Were Worth It

**Three theorems, all of them unconditional:**

- **L30:** every symmetric matrix is $Q\Lambda Q^\mathsf{T}$.
- **L31:** the positive definite ones are detectable five different ways.
- **Today:** what you get once you know it.

**The list is longer than it looks.**

| You want | Positive definiteness gives you |
|---|---|
| To solve $Ax = b$ fast | **Cholesky** — half the work of elimination, **no pivoting, ever** (§2) |
| To know if a critical point is a minimum | the second-derivative test in $n$ variables (§3) |
| To know how bad your matrix is | $\operatorname{cond}_2(A) = \lambda_\max/\lambda_\min$, read straight off (§4) |
| To trust a computed eigenvalue | **perfect conditioning** — the answer moves no further than the question (§6) |
| Covariance, energy, stiffness to make sense | a variance that cannot be negative |

---

## 2. Cholesky: The Factorisation That Needs No Pivoting

**Take $A = LDL^\mathsf{T}$ from L31 §5 and split $D$.** Every pivot is positive, so $\sqrt{D}$ exists as a real diagonal matrix, and

$$A = LDL^\mathsf{T} = \left(L\sqrt D\right)\left(L\sqrt D\right)^\mathsf{T} = R^\mathsf{T}R,$$

writing $R = \left(L\sqrt D\right)^\mathsf{T}$, which is **upper triangular**. This is **test 5 of L31 §3**, now constructive.

For our $A$ (`symmetric.py` §7):

$$R = \begin{bmatrix} 2.23606798 & 0 & -0.89442719\\ 0 & 1.73205081 & -1.15470054\\ 0 & 0 & 1.36626010\end{bmatrix}, \qquad \max\lvert R^\mathsf{T}R - A\rvert = 8.882\times10^{-16}.$$

**The diagonal entries are $\sqrt5$, $\sqrt3$ and $\sqrt{28/15}$** — the square roots of L31's pivots, exactly as the algebra says. *(This is the one place all week where exact rational arithmetic runs out: $\sqrt5$ is irrational, and the script says so.)*

**What it costs, in Week 0's units** (L03 §2 counted multiply-subtract pairs):

| $n$ | elimination $\left(\tfrac{n^3}{3}\right)$ | Cholesky $\left(\tfrac{n^3}{6}\right)$ | ratio |
|---:|---:|---:|---:|
| $10$ | $3.333\times10^{2}$ | $1.667\times10^{2}$ | $2.0$ |
| $100$ | $3.333\times10^{5}$ | $1.667\times10^{5}$ | $2.0$ |
| $1000$ | $3.333\times10^{8}$ | $1.667\times10^{8}$ | $2.0$ |
| $5000$ | $4.167\times10^{10}$ | $2.083\times10^{10}$ | $2.0$ |

**Half the work and half the storage** — you compute one triangle, because the other is its mirror.

> **And no pivoting.** Week 0's L03 §5 called partial pivoting *unconditional in every real solver*.
> **Cholesky is the exception, and it is the only one.** A positive definite matrix can never
> produce a zero or dangerously small pivot, because every leading minor is positive (L31 §3, test
> 4) and the $k$-th pivot is the ratio of consecutive leading minors. **The stability is a theorem
> about the matrix, not a property of the algorithm.**

**Cholesky is also the cheapest positive-definiteness test there is.** It stops the moment a negative number appears under a square root:

$$\texttt{cholesky}\!\left(\begin{bmatrix}1&3\\3&1\end{bmatrix}\right) \;\longrightarrow\; \texttt{None}$$

**The failure *is* the answer**, and it costs $\tfrac{n^3}{6}$ rather than the $O(n^3)$ iterative sweep that eigenvalues need. **This is what production code does** when it needs to know.

---

## 3. Minimisation, and the Second-Derivative Test in $n$ Variables

**One-variable calculus:** $f'(x_0) = 0$ and $f''(x_0) > 0$ means a minimum.

**In $n$ variables the second derivative is a matrix** — the **Hessian** $H_{ij} = \partial^2f/\partial x_i\partial x_j$, symmetric because mixed partials commute — and the test becomes:

$$\nabla f(x_0) = 0 \ \text{ and } \ H(x_0) \text{ positive definite} \;\Longrightarrow\; x_0 \text{ is a strict local minimum.}$$

> **This is the whole reason the subject has a name in optimisation.** L31 §6's table is the
> classification of critical points: **all eigenvalues positive is a bowl, all negative a dome,
> mixed signs a saddle, one zero a valley you can walk along without changing height.** The
> two-variable version in MATH 142 was $f_{xx}f_{yy} - f_{xy}^2 > 0$, which you can now recognise
> as $\det H > 0$ — **the $2\times2$ case of L31's test 4.**

**And the connection back to $Ax = b$ is exact.** For positive definite $A$, consider

$$f(x) = \tfrac12x^\mathsf{T}Ax - b^\mathsf{T}x, \qquad \nabla f = Ax - b, \qquad H = A.$$

**The unique minimiser of $f$ is the solution of $Ax = b$.** Solving a positive definite system and minimising a quadratic are the same problem, which is why conjugate gradients — the standard method for large sparse systems — is an *optimisation* algorithm.

---

## 4. The Rayleigh Quotient, and Reading Off the Condition Number

$$R(x) = \frac{x^\mathsf{T}Ax}{x^\mathsf{T}x}, \qquad x \ne 0.$$

**For symmetric $A$ this is trapped between the extreme eigenvalues**, and attains both:

$$\lambda_\min \;\le\; \frac{x^\mathsf{T}Ax}{x^\mathsf{T}x} \;\le\; \lambda_\max,$$

with equality exactly at the corresponding eigenvectors. *(Proof: write $x$ in the orthonormal eigenbasis, $x = \sum c_kq_k$. Then $x^\mathsf{T}Ax = \sum\lambda_kc_k^2$ and $x^\mathsf{T}x = \sum c_k^2$, so $R(x)$ is a **weighted average of the eigenvalues** — and an average lies between the extremes.)*

`symmetric.py` §9, on our $A$ with eigenvalues $1, 4, 7$, over $200{,}000$ random directions:

| | observed | true |
|---|---:|---:|
| minimum of $R$ | $1.000012935$ | $\lambda_\min = 1$ |
| maximum of $R$ | $6.999890833$ | $\lambda_\max = 7$ |

**Random sampling approaches both bounds and never crosses either**, and evaluating at the eigenvectors gives $7.000000000000$ and $1.000000000000$ exactly.

> **This gives $\lambda_\max$ and $\lambda_\min$ a definition that never mentions
> $\det(A - \lambda I)$** — they are the extreme values of a ratio. **Week 6's characteristic
> polynomial was declared unusable numerically in L20 §6**, and this is the replacement: every
> serious symmetric eigenvalue algorithm, Jacobi included, is chasing this variational
> characterisation rather than a polynomial root.

**And the condition number falls out.** For a symmetric matrix,

$$\operatorname{cond}_2(A) = \frac{\lambda_\max}{\lambda_\min} \quad (\text{taking absolute values in general}),$$

which for our $A$ is $7/1 = 7$ — **well conditioned, and now you can *say why***: no direction is stretched more than seven times as much as any other. **For a non-symmetric matrix this is false**, and Week 11 says what replaces it.

---

## 5. Week 0's Hilbert Matrix, Finally Diagnosed

**Week 0's L03 §6 exhibited $H_n$, $H_{ij} = 1/(i+j-1)$, and reported that $\operatorname{cond}_\infty(H_{12}) = 4.1\times10^{16}$ without being able to say where the badness lived.** It lives in $\lambda_\min$ (`symmetric.py` §10):

| $n$ | $\lambda_\max$ | $\lambda_\min$ | $\operatorname{cond}_2 = \lambda_\max/\lambda_\min$ | $\operatorname{cond}_\infty$ *(exact, Week 0)* |
|---:|---:|---:|---:|---:|
| $3$ | $1.40831893$ | $2.687\times10^{-3}$ | $5.241\times10^{2}$ | $7.480\times10^{2}$ |
| $5$ | $1.56705069$ | $3.288\times10^{-6}$ | $4.766\times10^{5}$ | $9.437\times10^{5}$ |
| $8$ | $1.69593900$ | $1.112\times10^{-10}$ | $1.526\times10^{10}$ | $3.387\times10^{10}$ |
| $10$ | $1.75191967$ | $1.093\times10^{-13}$ | $1.603\times10^{13}$ | $3.536\times10^{13}$ |
| $12$ | $1.79537206$ | $9.953\times10^{-17}$ | $1.804\times10^{16}$ | $4.115\times10^{16}$ |

**$\lambda_\max$ barely moves. $\lambda_\min$ collapses by fourteen orders of magnitude.** So "nearly singular" is not vague after all: **$H_{12}$ has one direction in which it does almost nothing**, and the condition number is the ratio between the most and least stretched directions.

**And every $H_n$ is positive definite** — all eigenvalues strictly positive, at every $n$. **So "positive definite" does not mean "well behaved".** It means the eigenvalues are on one side of zero, not that they are far from it.

> **An honest note about the last row.** $\lambda_\min(H_{12}) \approx 10^{-17}$ is *smaller than
> the rounding error in the stored entries of $H_{12}$ itself* — $1/3$ is not representable in
> binary. **That figure's digits are not trustworthy; only its order of magnitude is**, and the
> reason to believe even that is the exactly-computed $\operatorname{cond}_\infty$ column beside it,
> which agrees to a factor of about two. **This is L03 §7's own warning applied to L32's own table**,
> and it is the discipline the whole term has been asking for.

**$\operatorname{cond}_2$ and $\operatorname{cond}_\infty$ differ because they are different norms.** Both are correct; they track each other within a small factor, and the rule of thumb *(digits $\approx 16 - \log_{10}\operatorname{cond}$)* is insensitive to which you use.

**Why $H_n$ keeps appearing:** Week 9's L29 §5 showed $H_{ij} = \int_0^1x^{i+j-2}dx$, so $H_n$ **is** $A^\mathsf{T}A$ for polynomial fitting on $[0,1]$. **Symmetric and positive definite by L31 §7, by construction, with no checking required** — and catastrophically conditioned all the same.

---

## 6. The Headline: How Far Do Eigenvalues Move?

**This is the measurement that justifies the whole week.**

**Question:** perturb a matrix by a small amount $\delta$. How far can its eigenvalues move?

### Symmetric: they move by at most $\delta$

**Weyl's inequality** says $\lvert\lambda_i(A + E) - \lambda_i(A)\rvert \le \lVert E\rVert_2$ for symmetric $A$ and $E$. `symmetric.py` §12 measures it, over $200$ random symmetric perturbations at each size:

| $\delta = \lVert E\rVert_2$ | $\max_i\lvert\lambda_i(A+E) - \lambda_i(A)\rvert$ | ratio |
|---:|---:|---:|
| $10^{-2}$ | $9.946402\times10^{-3}$ | $0.9946$ |
| $10^{-4}$ | $9.993408\times10^{-5}$ | $0.9993$ |
| $10^{-6}$ | $9.999006\times10^{-7}$ | $0.9999$ |
| $10^{-8}$ | $9.985105\times10^{-9}$ | $0.9985$ |
| $10^{-10}$ | $9.998313\times10^{-11}$ | $0.9998$ |

**The ratio approaches $1$ from below and never exceeds it.** The symmetric eigenvalue problem is **perfectly conditioned** — condition number exactly $1$ — **and nothing else in this course is.**

### Not symmetric: they can move by $\delta^{1/n}$

Take the $n\times n$ matrix $C$ with $1$s on the superdiagonal and $\varepsilon$ in the bottom-left corner:

$$C = \begin{bmatrix}0&1&&&\\&0&1&&\\&&\ddots&\ddots&\\&&&0&1\\ \varepsilon&&&&0\end{bmatrix}.$$

**$C$ is a cyclic shift with one scaled entry, so $C^n = \varepsilon I$ exactly**, hence $\lambda^n = \varepsilon$ and

$$\lvert\lambda\rvert = \varepsilon^{1/n} \quad\text{for every eigenvalue.}$$

**No eigenvalue solver is involved** — `symmetric.py` §12 verifies $C^n = \varepsilon I$ in exact `Fraction` arithmetic and reads the magnitude off the algebra:

| $n$ | $\varepsilon$ | $C^n = \varepsilon I$? | $\lvert\lambda\rvert = \varepsilon^{1/n}$ | amplification |
|---:|---:|:--:|---:|---:|
| $5$ | $10^{-10}$ | ✓ | $1.000000\times10^{-2}$ | $10^{8}$ |
| $\mathbf{10}$ | $\mathbf{10^{-10}}$ | ✓ | $\mathbf{1.000000\times10^{-1}}$ | $\mathbf{10^{9}}$ |
| $10$ | $10^{-16}$ | ✓ | $2.511886\times10^{-2}$ | $2.512\times10^{14}$ |
| $20$ | $10^{-16}$ | ✓ | $1.584893\times10^{-1}$ | $1.585\times10^{15}$ |

> **Read the bold row.** At $\varepsilon = 0$ every eigenvalue of $C$ is $0$. **Change one entry by
> $10^{-10}$ — a perturbation far below anything you could measure — and every eigenvalue moves out
> to magnitude $0.1$.** The answer moves a **billion** times further than the question.
>
> **At $\varepsilon = 0$ this matrix is Week 7's worst case**: a single Jordan block, one eigenvalue
> repeated $n$ times, **one** eigenvector. **Defectiveness and eigenvalue sensitivity are the same
> phenomenon seen twice**, and L30 rules out both at once with a single hypothesis.

**So the reason to want symmetry is not elegance.** It is that a symmetric eigenvalue you compute is an eigenvalue of a matrix within rounding error of yours, and *that* eigenvalue is within rounding error of yours. **For a general matrix, neither step is safe.**

---

## 7. One Step Toward Week 11

**A symmetric matrix's singular values are the absolute values of its eigenvalues.** `symmetric.py` §13:

| Matrix | eigenvalues | $\sqrt{\text{eig}(A^\mathsf{T}A)}$ |
|---|---|---|
| our $A$ | $7,\ 4,\ 1$ | $7,\ 4,\ 1$ |
| $\begin{bmatrix}1&3\\3&1\end{bmatrix}$ | $4,\ \mathbf{-2}$ | $4,\ \mathbf{2}$ |

**The sign is thrown away, because $A^\mathsf{T}A$ cannot see it.** For a positive definite matrix the two lists coincide exactly; for an indefinite one they differ in sign only.

> **Week 11 defines singular values for *every* matrix** — non-symmetric, non-square, singular,
> anything — **as the square roots of the eigenvalues of $A^\mathsf{T}A$**, which is symmetric
> positive semidefinite by L31 §7 **and therefore has real non-negative eigenvalues and orthonormal
> eigenvectors by L30**. **The SVD is this week's theorem applied to $A^\mathsf{T}A$ and
> $AA^\mathsf{T}$**, and that is why it needs no hypotheses at all: the hypothesis is satisfied by
> construction.

---

## 8. What to Take Away

1. **Cholesky $A = R^\mathsf{T}R$**: half the work of elimination, half the storage, **and no pivoting ever** — the stability is a theorem about the matrix.
2. **Cholesky's failure is the cheapest positive-definiteness test**, and it is what production code runs.
3. **The Hessian test:** $\nabla f = 0$ plus positive definite $H$ means a strict minimum. **L31 §6's table is the classification of critical points.**
4. **Minimising $\tfrac12x^\mathsf{T}Ax - b^\mathsf{T}x$ is solving $Ax = b$**, which is why the standard large-scale solver is an optimisation method.
5. **The Rayleigh quotient is a weighted average of the eigenvalues**, hence trapped between $\lambda_\min$ and $\lambda_\max$, and this is how eigenvalues are actually computed.
6. **$\operatorname{cond}_2 = \lambda_\max/\lambda_\min$ for symmetric matrices.** $H_{12}$'s badness is entirely in $\lambda_\min \approx 10^{-17}$ — **and every $H_n$ is positive definite, so that adjective is not a safety guarantee.**
7. **Symmetric eigenvalue problems are perfectly conditioned.** The measured ratio never exceeds $1$.
8. **Non-symmetric ones need not be:** $10^{-10}$ in one entry moves every eigenvalue to $0.1$. **A billion-fold amplification, verified exactly.**
9. **Singular values of a symmetric matrix are $\lvert\lambda_i\rvert$**, and Week 11 generalises that to every matrix by applying L30 to $A^\mathsf{T}A$.

---

## Exercises

*(Not assessed. PS 10 is the assessed work.)*

1. Compute the Cholesky factor of $\begin{bmatrix}4&2\\2&5\end{bmatrix}$ by hand. **Check $R^\mathsf{T}R$.** Then do $\begin{bmatrix}4&2\\2&1\end{bmatrix}$ and say exactly where it stops.
2. Show that the $k$-th pivot equals $D_k/D_{k-1}$, the ratio of consecutive leading minors, with $D_0 = 1$. **Check on our $A$**, whose minors are $5$, $15$, $28$. *(This is why L31's tests 3 and 4 are the same test.)*
3. $f(x_1,x_2) = x_1^2 + 4x_1x_2 + x_2^2$. Find $H$, classify the critical point at the origin, and **draw a level set** to confirm.
4. **Why does Cholesky never need pivoting, but $LU$ does?** Answer in one sentence using exercise 2.
5. Compute $R(x) = x^\mathsf{T}Ax/x^\mathsf{T}x$ for our $A$ at $x = (1,1,1)$, $(1,0,0)$ and $(1,2,2)$. **Which one is an eigenvector, and how do you know from the value alone?**
6. Verify that $C^n = \varepsilon I$ for §6's matrix at $n = 3$ by multiplying it out by hand. **Then find all three eigenvalues at $\varepsilon = 10^{-6}$**, in modulus and argument.
7. $A$ is symmetric with eigenvalues $2$ and $8$. **What is the aspect ratio of the ellipse $x^\mathsf{T}Ax = 1$?** What is $\operatorname{cond}_2(A)$? *(One number is the square root of the other; say which and why.)*
8. Take $A = \begin{bmatrix}1&3\\3&1\end{bmatrix}$. Compute $A^\mathsf{T}A$, its eigenvalues, and their square roots. **Confirm §7's claim**, and say what information about $A$ has been lost.

---

*MATH 241 · Week 10 · L32 · © CSE Department*
