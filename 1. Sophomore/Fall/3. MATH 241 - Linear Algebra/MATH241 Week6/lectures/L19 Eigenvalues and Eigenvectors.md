# MATH 241 · Linear Algebra
## Week 6 · Lecture 1 of **2** · **Tuesday**
### Eigenvalues and Eigenvectors

---

**Reading:** Strang §6.1 · **Previous:** Week 5's L18, volume and the product rule · **Next:** L20, the characteristic polynomial

> **Week 6 has two lectures, not three.** Its Monday is **Fall Break** and this course lectures on
> Mondays, so the week runs **Tuesday and Friday only**. Nothing is dropped — Week 7 takes
> diagonalisation as planned — but this week is compressed and both lectures are dense.
>
> **Quiz 6 is the first ten minutes of this lecture** — moved from Monday, and the only quiz in the
> term that is not a Monday. It covers **Week 5**.
>
> **Midterm 1 is tomorrow evening**, 18:00–19:15, SSB 110, covering **Weeks 0–5**. **Nothing in
> today's lecture is on it.**

---

## 1. The Question Week 4 Asked Without the Words

Week 4's L15 §5 reflected across the line $y = x$ and chose the basis $\{(1,1), (1,-1)\}$ — along the mirror and across it — because in that basis the matrix was $\operatorname{diag}(1,-1)$, and the reflection *said* what it was.

**What was special about those two vectors is that $T$ sent each to a multiple of itself.** The mirror line was fixed; the perpendicular was negated. **Nothing was rotated into a new direction.**

Week 4's PS 4 Q4(e) and REC 4 §3(e) both asked you to describe what you would look for in general, without giving you the method. **Here is the equation you were describing:**

> **Definition.** A nonzero vector $v$ is an **eigenvector** of $A$ with **eigenvalue** $\lambda$ if
>
> $$Av = \lambda v.$$

**"Eigen" is German for *own* or *proper*** — these are the matrix's own directions. *(Older English texts say "characteristic vector"; the mixed-language "eigenvector" won.)*

**Two conditions to notice in the definition.** $v \ne 0$ is required — $A0 = \lambda 0$ holds for every $\lambda$ and says nothing. **But $\lambda = 0$ is allowed**, and it means something specific: $Av = 0$ for a nonzero $v$, so $A$ is singular. **$0$ is an eigenvalue exactly when $\mathbf{N}(A) \ne \{0\}$.**

---

## 2. Why This Is Worth a Fortnight

**Because $Av = \lambda v$ turns matrix multiplication into scalar multiplication**, and scalars are easy.

$$A^kv = \lambda^kv$$

**No matrix products at all** — just a number raised to a power. Week 1's L04 §6 promised this: computing $A^k$ costs $O(n^3\log k)$ by repeated squaring, and if you have a basis of eigenvectors it costs $n$ scalar powers. **Week 7 is that idea made into an algorithm.**

And it is why eigenvalues answer questions that look nothing like linear algebra:

| Question | The eigenvalue fact |
|---|---|
| Does this iteration converge? | $\lvert\lambda\rvert < 1$ for every $\lambda$ |
| **What is PageRank?** | the eigenvector of the web graph for $\lambda = 1$ |
| Is this structure stable? | signs of the eigenvalues |
| What are the principal components of this data? | eigenvectors of the covariance matrix — **Week 12** |
| Why does this bridge resonate? | eigenvalues of the stiffness matrix |

**Week 0's L03 §2 said PageRank is not solved by elimination** because $n^3/3$ at $n = 10^9$ is ten million years. **It is solved by repeatedly multiplying by $A$**, which drives any starting vector toward the eigenvector of largest $\lvert\lambda\rvert$ — and that is a Week 7 computation resting on this week's definition.

---

## 3. Finding Them: the Determinant Earns Its Week

Rearrange the definition:

$$Av = \lambda v \iff Av - \lambda v = 0 \iff (A - \lambda I)v = 0$$

**Read that last equation.** It says $v$ is in the null space of $A - \lambda I$ — and $v \ne 0$, so **that null space is nontrivial**, so $A - \lambda I$ is **singular**. By Week 5's L16 §5:

$$\boxed{\;\lambda \text{ is an eigenvalue} \iff \det(A - \lambda I) = 0\;}$$

**This is why Week 5 happened.** And it is why L17 §5 insisted cofactors were worth a lecture despite being $9\times10^{14}$ times too slow: **$\det(A - \lambda I)$ has a symbol in it.** Elimination would divide by expressions like $2 - \lambda$, forcing a case split on whether they vanish. **Cofactor expansion only multiplies and adds**, so it produces a polynomial with no cases at all.

### The two-step method

1. **Solve $\det(A - \lambda I) = 0$** for $\lambda$. This is a polynomial equation — L20 studies it.
2. **For each $\lambda$, find $\mathbf{N}(A - \lambda I)$** by elimination. That null space is the **eigenspace**, and its nonzero vectors are the eigenvectors.

**Step 2 is Week 2's algorithm, unchanged.** The eigenspace *is* a null space, so it is a subspace — which is why "the" eigenvector is never unique: any nonzero multiple of an eigenvector is one, and if the eigenspace has dimension 2 there is a whole plane of them.

> **Never do step 2 by substituting into $Av = \lambda v$ and solving two equations in two
> unknowns.** It works for $2\times2$ and it teaches you nothing transferable.
> **$\mathbf{N}(A - \lambda I)$ is the object**, you have had the algorithm since Week 2, and at
> $3\times3$ the substitution approach becomes a mess while elimination does not.

---

## 4. Worked, on a $3\times3$

$$A = \begin{bmatrix}2&-1&1\\ -1&2&-1\\ 1&1&2\end{bmatrix}$$

**Step 1.** By cofactor expansion — symbolically, which elimination could not do:

$$\det(A - \lambda I) = -\lambda^3 + 6\lambda^2 - 11\lambda + 6 = -(\lambda-1)(\lambda-2)(\lambda-3)$$

$$\boxed{\lambda = 1,\ 2,\ 3}$$

*(The leading coefficient is $-1$ because $n = 3$ is odd; in general $\det(A - \lambda I)$ has leading term $(-1)^n\lambda^n$. Some books use $\det(\lambda I - A)$ to keep it monic. **Both are standard and their roots are identical** — only the overall sign differs.)*

**Step 2**, one eigenvalue at a time. For $\lambda = 1$:

$$A - I = \begin{bmatrix}1&-1&1\\ -1&1&-1\\ 1&1&1\end{bmatrix} \;\longrightarrow\; \mathbf{N}(A - I) = \operatorname{span}\{(-1, 0, 1)\}$$

**Check, always:** $A(-1,0,1) = (-2 + 0 + 1,\ 1 + 0 - 1,\ -1 + 0 + 2) = (-1, 0, 1) = 1 \cdot v$ ✓

| $\lambda$ | Eigenvector | Check $Av = \lambda v$ |
|---|---|---|
| $1$ | $(-1, 0, 1)$ | $(-1,0,1) = 1v$ ✓ |
| $2$ | $(-1, 1, 1)$ | $(-2,2,2) = 2v$ ✓ |
| $3$ | $(-1, 1, 0)$ | $(-3,3,0) = 3v$ ✓ |

**Three distinct eigenvalues, three one-dimensional eigenspaces, three independent eigenvectors.** So $\{(-1,0,1), (-1,1,1), (-1,1,0)\}$ is a basis of $\mathbb{R}^3$ **in which $A$ is $\operatorname{diag}(1,2,3)$** — which is Week 4's L15 §7 first row, and Week 7's subject.

> **Check every eigenvector.** It is one matrix–vector product, it is exact, and it catches sign
> errors in the elimination that nothing else will. **An eigenvector you have not verified is a
> guess.**

---

## 5. The Ones You Should Predict Before Computing

**The geometry comes first.** For every transformation below, work out the eigenvalues by asking *which directions are left alone* — then confirm.

| $T$ | Reasoning | $\lambda$ | Eigenvectors |
|---|---|---|---|
| **reflect** across $y=x$ | the mirror is fixed; the perpendicular is negated | $1, -1$ | $(1,1)$, $(1,-1)$ |
| **project** onto $y=x$ | the line survives; the perpendicular dies | $1, 0$ | $(1,1)$, $(1,-1)$ |
| **scale** $x$ by 3, $y$ by 2 | the axes are the special directions | $3, 2$ | $(1,0)$, $(0,1)$ |
| **triangular** $\begin{bmatrix}2&5\\0&7\end{bmatrix}$ | — | $2, 7$ | $(1,0)$, $(1,1)$ |
| **rotate** $90°$ | **nothing is fixed** | *no real $\lambda$* | §6 |
| **shear** $\begin{bmatrix}1&1\\0&1\end{bmatrix}$ | only the $x$-axis survives | $1$ *(twice)* | $(1,0)$ **only** |

**Two of these are the interesting ones and they are §6 and §7.**

**The projection's $\lambda = 0$ is worth pausing on.** $0$ is a legitimate eigenvalue, and here it says the perpendicular direction is annihilated — which is $\mathbf{N}(P) \ne \{0\}$, which is why a projection is singular. **Week 1's L05 exercise 6 proved $P^2 = P$ forces non-invertibility; the eigenvalue is why.** Indeed $P^2 = P$ gives $\lambda^2 = \lambda$, so **every eigenvalue of a projection is $0$ or $1$**, with no calculation at all.

**And the triangular case is free.** $\det(A - \lambda I)$ of a triangular matrix is the product of its diagonal entries minus $\lambda$, so **the eigenvalues of a triangular matrix are its diagonal entries.** Read them off. *(Which retroactively explains something: Week 1's $A = LU$ gives $U$ triangular, and $\det A$ is $U$'s diagonal product — the pivots. **The pivots are not the eigenvalues**, but both are diagonal products of triangular matrices, and confusing them is a common error. §7 of L20 separates them.)*

---

## 6. A Rotation Has No Real Eigenvalues

$$R = \begin{bmatrix}0&-1\\ 1&0\end{bmatrix} \qquad \det(R - \lambda I) = \lambda^2 + 1$$

**No real root.** And that is not a defect of the algebra — **it is correct.** A rotation by $90°$ leaves *no* direction unmoved; there is nothing for an eigenvector to be.

**Over $\mathbb{C}$ the eigenvalues are $\lambda = \pm i$**, and the bookkeeping still works:

$$i + (-i) = 0 = \operatorname{trace}R, \qquad i \times (-i) = 1 = \det R$$

**So L20 §2's identities survive complex eigenvalues intact** — only the *reality* of the answers is lost. **Week 7 takes this seriously**, because a rotation is not an exotic matrix and complex eigenvalues are the normal case for anything that oscillates. *(This is where ECE 211 next term lives: $e^{i\omega t}$ is an eigenvector of differentiation, and the whole theory of linear systems is that sentence.)*

> **The fundamental theorem of algebra guarantees $n$ roots over $\mathbb{C}$**, counted with
> multiplicity, for every $n\times n$ matrix. **So eigenvalues always exist**; the question is only
> whether they are real and whether there are enough independent eigenvectors — which is §7.

---

## 7. When There Are Not Enough Eigenvectors

$$S = \begin{bmatrix}1&1\\ 0&1\end{bmatrix} \qquad \det(S - \lambda I) = (1-\lambda)^2$$

**$\lambda = 1$, a double root.** Now find the eigenspace:

$$S - I = \begin{bmatrix}0&1\\ 0&0\end{bmatrix} \qquad \mathbf{N}(S - I) = \operatorname{span}\{(1,0)\}$$

**One dimension, for a doubled eigenvalue.** A $2\times2$ matrix with only **one** independent eigenvector — so **no basis of eigenvectors exists**, and no change of basis can make $S$ diagonal.

**Such a matrix is called *defective*.** L20 §5 names the two multiplicities that disagree here; Week 7 is what to do about it.

> **And this settles a question left open in Week 4.** PS 4 Q5(d) showed $I$ and
> $\begin{bmatrix}1&1\\0&1\end{bmatrix}$ are **not similar**, by the argument that $M^{-1}IM = I$ for
> every $M$ — correct, and unsatisfying, because the two matrices share **trace, determinant, rank
> *and* characteristic polynomial** $(1-\lambda)^2$.
>
> **The invariant that separates them is the eigenspace dimension**: $I$ has two independent
> eigenvectors and $S$ has one. **That is the first genuinely new invariant since Week 4**, and it is
> why trace and determinant were never going to be enough.

---

## 8. What to Take Away

1. **$Av = \lambda v$ with $v \ne 0$.** The eigenvectors are the directions $A$ does not turn; $\lambda$ is the stretch factor.
2. **$\lambda = 0$ is allowed** and means $A$ is singular. **$v = 0$ is not.**
3. **$Av = \lambda v$ makes $A^kv = \lambda^kv$** — matrix powers become scalar powers, which is why eigenvalues answer questions about iteration, stability and PageRank.
4. **$\lambda$ is an eigenvalue $\iff \det(A - \lambda I) = 0$**, which is why Week 5 happened — and **why cofactors were worth a lecture**, since the determinant has a symbol in it.
5. **Then the eigenspace is $\mathbf{N}(A - \lambda I)$**, by Week 2's algorithm. Eigenvectors are never unique; the eigenspace is.
6. **Predict from geometry first.** Reflections give $\pm1$, projections give $1$ and $0$, **triangular matrices give their diagonal**.
7. **A rotation has no real eigenvalues** — correctly, since it fixes no direction. Over $\mathbb{C}$ it has two, and trace and determinant still work.
8. **A defective matrix has fewer independent eigenvectors than its size.** The shear is one, and **the eigenspace dimension is the invariant that finally separates $I$ from $\begin{bmatrix}1&1\\0&1\end{bmatrix}$.**

---

## Exercises

*(Not assessed. PS 6 is the assessed work, due Friday of Week 7.)*

1. Find the eigenvalues and eigenvectors of $\begin{bmatrix}3&1\\1&3\end{bmatrix}$. *(Week 5's L17 exercise 3 found the eigenvalues already.)* Check both eigenvectors.
2. Predict, then verify, the eigenvalues of: reflection across the $x$-axis; projection onto the $y$-axis; rotation by $180°$. **Which of these has real eigenvalues, and why is $180°$ different from $90°$?**
3. $A$ is $4\times4$ triangular with diagonal $2, 2, 5, -1$. Write down its eigenvalues, its trace and its determinant, doing no arithmetic beyond addition and multiplication.
4. Show that if $Av = \lambda v$ then $A^2v = \lambda^2 v$ and, for invertible $A$, $A^{-1}v = \lambda^{-1}v$. **What does the second tell you about the eigenvalues of $A^{-1}$?**
5. Show every eigenvalue of a projection ($P^2 = P$) is $0$ or $1$, from $P^2 = P$ alone. Then do the same for a reflection ($R^2 = I$).
6. Find the eigenvalues of $\begin{bmatrix}0&1\\-6&5\end{bmatrix}$, and the eigenspace for each. Check that trace and determinant match the sum and product.

---

*MATH 241 · Week 6 · L19 · © CSE Department*
