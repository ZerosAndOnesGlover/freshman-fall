# MATH 241 · Linear Algebra
## Week 8 · Lecture 2 of 3 · **Tuesday**
### Projections

*“Mathematics succeeds in dealing with tangible reality by being conceptual. We cannot cope with the full physical complexity; we must idealize.”* — George Pólya, *Mathematical Methods in Science* (1977)

---

**Reading:** Strang §4.2 · **Previous:** L24, orthogonality · **Next:** L26, orthonormal bases and Gram–Schmidt

**Coursework:** 📝 **PS 8** released Wed this week, due Fri of Week 9 17:00 · 💬 **Recitation 7** Thu this week 15:00–15:50 · 📝 **PS 7** due Fri this week 17:00 · 📊 **Quiz 9** Mon of Week 9

> **Every number in this lecture is reproduced by `resources/orthogonal.py`.**

---

## 1. The Question

**Given a subspace $W$ and a point $b$ outside it, what is the nearest point of $W$ to $b$?**

L24 §4 has already answered it, in a form that does not look like an answer: every $b$ splits uniquely as

$$b = p + e, \qquad p \in W, \qquad e \in W^\perp.$$

**$p$ is the nearest point**, and $e = b - p$ is the error. *Why nearest:* for any other $w \in W$,

$$\lVert b - w\rVert^2 = \lVert (p - w) + e\rVert^2 = \lVert p-w\rVert^2 + \lVert e\rVert^2 \ \ge\ \lVert e\rVert^2$$

by Pythagoras — $p - w \in W$ and $e \in W^\perp$, so the cross term vanishes — **with equality only when $w = p$.** $\square$

> **This is the whole reason projections matter**, and it is Week 9's entire subject in advance:
> when $Ax = b$ has **no** solution because $b \notin \mathbf{C}(A)$, the honest thing to do is solve
> $Ax = p$ instead, where $p$ is the nearest reachable point. **Week 2 could only say "no solution".
> This is what to do about it.**

---

## 2. Onto a Line

Project $b$ onto the line through $a$. The answer is a multiple of $a$, say $p = \hat{x}a$, and **the error must be orthogonal to $a$:**

$$a^\mathsf{T}(b - \hat{x}a) = 0 \quad\Longrightarrow\quad \hat{x} = \frac{a^\mathsf{T}b}{a^\mathsf{T}a}$$

$$\boxed{\;p = \frac{a^\mathsf{T}b}{a^\mathsf{T}a}\,a = \underbrace{\frac{aa^\mathsf{T}}{a^\mathsf{T}a}}_{P}\,b\;}$$

**Note the two products in that last step.** $a^\mathsf{T}a$ is a **number**; $aa^\mathsf{T}$ is an $n\times n$ **matrix** of rank 1 — Week 1's L04 reading (iv), the outer product. **Getting these the right way round is the whole of the algebra here.**

**Example.** $a = (1,1,1)$, $b = (6,0,0)$: $\hat{x} = 6/3 = 2$, so $p = (2,2,2)$ and $e = (4,-2,-2)$, with $a^\mathsf{T}e = 4-2-2 = 0$ ✓

---

## 3. Onto a Subspace

Now let $W = \mathbf{C}(A)$ for a matrix $A$ with **independent columns.** Then $p = A\hat{x}$ for some coefficient vector $\hat{x}$, and the same condition applies: **the error is orthogonal to the whole subspace**, hence to every column of $A$:

$$A^\mathsf{T}(b - A\hat{x}) = 0 \quad\Longrightarrow\quad \boxed{\;A^\mathsf{T}A\,\hat{x} = A^\mathsf{T}b\;}$$

**The *normal equations*.** And since $A$ has independent columns, $A^\mathsf{T}A$ is **invertible** — which is **PS 2 Q5(c)**, proved in Week 2 and used here for the first time:

$$\mathbf{N}(A^\mathsf{T}A) = \mathbf{N}(A) = \{0\}$$

so the square matrix $A^\mathsf{T}A$ has trivial null space and is invertible. **Therefore**

$$\hat{x} = (A^\mathsf{T}A)^{-1}A^\mathsf{T}b, \qquad p = A\hat{x} = \underbrace{A(A^\mathsf{T}A)^{-1}A^\mathsf{T}}_{P}\,b$$

$$\boxed{\;P = A(A^\mathsf{T}A)^{-1}A^\mathsf{T}\;}$$

> **Read that formula, do not compute it.** Week 1's L05 §8 said a formula containing $A^{-1}$ is a
> *statement*, not an instruction, and this is the case it was preparing you for. **In practice you
> solve $A^\mathsf{T}A\hat x = A^\mathsf{T}b$** — one solve, no inverse — or better, use Week 9's QR.
> **Never form $(A^\mathsf{T}A)^{-1}$.**
>
> **And it degenerates correctly.** With one column, $A = a$, the formula collapses to
> $aa^\mathsf{T}/a^\mathsf{T}a$ — §2's line case, since $A^\mathsf{T}A$ is then the number
> $a^\mathsf{T}a$.

---

## 4. Worked

$$A = \begin{bmatrix}1&1\\ 1&2\\ 1&3\end{bmatrix}, \qquad A^\mathsf{T}A = \begin{bmatrix}3&6\\ 6&14\end{bmatrix}, \qquad \det = 6$$

$$P = A(A^\mathsf{T}A)^{-1}A^\mathsf{T} = \frac{1}{6}\begin{bmatrix}5&2&-1\\ 2&2&2\\ -1&2&5\end{bmatrix}$$

**Project $b = (6,0,0)$:**

$$p = Pb = (5,\ 2,\ -1), \qquad e = b - p = (1,\ -2,\ 1)$$

**Check the error is orthogonal to both columns:**

$$e^\mathsf{T}a_1 = 1 - 2 + 1 = 0\ ✓ \qquad e^\mathsf{T}a_2 = 1 - 4 + 3 = 0\ ✓ \qquad A^\mathsf{T}e = (0,0)\ ✓$$

> **And notice where $e$ lives.** $A^\mathsf{T}e = 0$ says $e \in \mathbf{N}(A^\mathsf{T})$ — **the
> left null space.** So the splitting $b = p + e$ is exactly L24 §4's decomposition of $\mathbb{R}^3$
> into $\mathbf{C}(A) \oplus \mathbf{C}(A)^\perp$, and the two pieces are Week 3's two subspaces of
> $\mathbb{R}^m$. **The four-subspace picture and the projection are the same fact.**

---

## 5. The Two Properties, and Why

$$P^2 = P \qquad\qquad P^\mathsf{T} = P$$

**Both verified** on the $P$ above, and both have one-line reasons.

**$P^2 = P$ — projecting twice changes nothing.** Algebraically:

$$P^2 = A(A^\mathsf{T}A)^{-1}\underbrace{A^\mathsf{T}A(A^\mathsf{T}A)^{-1}}_{I}A^\mathsf{T} = A(A^\mathsf{T}A)^{-1}A^\mathsf{T} = P$$

**Geometrically: $Pb$ is already in $W$, so projecting it does nothing.**

**$P^\mathsf{T} = P$ — a projection matrix is symmetric.** Take transposes, using $(XYZ)^\mathsf{T} = Z^\mathsf{T}Y^\mathsf{T}X^\mathsf{T}$ and the fact that $A^\mathsf{T}A$ is symmetric (**Week 1's L06 §2**, one line, no hypotheses).

> **This closes a loop three weeks long.**
>
> - **Week 1's L05 exercise 6** asked you to show $A^2 = A$ with $A \ne I$ forces non-invertibility,
>   and remarked that such matrices are called projections.
> - **Week 4's L14 §2** built $\tfrac12\begin{bmatrix}1&1\\1&1\end{bmatrix}$ geometrically and
>   observed $P^2 = P$ without explaining it.
> - **Week 7's L21 exercise 6** showed a diagonalisable $A$ with $A^2 = A$ has only $0$s and $1$s on
>   $\Lambda$ — *"every such matrix is a projection in some basis"*.
>
> **All three are this lecture.** And the eigenvalue statement is now obvious: $P$ fixes everything
> in $W$ ($\lambda = 1$, multiplicity $\dim W$) and kills everything in $W^\perp$ ($\lambda = 0$,
> multiplicity $n - \dim W$). **A projection is diagonalisable with eigenvalues $0$ and $1$**, and
> the eigenspaces are $W$ and $W^\perp$.

**Two degenerate cases, both correct.** If $W = \mathbb{R}^n$ then $A$ is square and invertible, and $P = A A^{-1}(A^\mathsf{T})^{-1}A^\mathsf{T} = I$ — projecting onto everything changes nothing. If $W = \{0\}$ then $P = 0$.

---

## 6. Why the Projection Is Not $A^{-1}b$ or Anything Like It

**A tempting mistake, and worth naming.** $A$ here is $3\times2$ — **not square**, so it has no inverse, and $\hat{x} = (A^\mathsf{T}A)^{-1}A^\mathsf{T}b$ is not "$A^{-1}b$ with extra steps".

**What $(A^\mathsf{T}A)^{-1}A^\mathsf{T}$ is:** a **left inverse** of $A$. Check:

$$\big[(A^\mathsf{T}A)^{-1}A^\mathsf{T}\big]A = (A^\mathsf{T}A)^{-1}(A^\mathsf{T}A) = I_2$$

**but $A\big[(A^\mathsf{T}A)^{-1}A^\mathsf{T}\big] = P \ne I_3$.** So it undoes $A$ from one side only — which is exactly Week 1's L05 §1 remark that for non-square matrices left and right inverses are different things, with a promise that Week 9 would supply the example. **This is it.**

**And the reason there is no right inverse is a rank statement:** $A$ is $3\times2$ with rank 2, so $\mathbf{C}(A)$ is a plane in $\mathbb{R}^3$ and **most $b$ are unreachable.** No matrix can undo that.

---

## 7. What to Take Away

1. **The nearest point of $W$ to $b$ is $p$, where $b = p + e$ with $e \perp W$** — proved by Pythagoras, and it is the reason projections matter.
2. **Onto a line:** $P = \dfrac{aa^\mathsf{T}}{a^\mathsf{T}a}$ — an $n\times n$ rank-one matrix over a number, and getting those two the right way round is the algebra.
3. **Onto a subspace:** the error is orthogonal to every column, which gives the **normal equations** $A^\mathsf{T}A\hat x = A^\mathsf{T}b$.
4. **$A^\mathsf{T}A$ is invertible when $A$ has independent columns** — PS 2 Q5(c), used here for the first time.
5. **$P = A(A^\mathsf{T}A)^{-1}A^\mathsf{T}$ is a statement, not an instruction.** Solve the normal equations; never form the inverse.
6. **$P^2 = P$ and $P^\mathsf{T} = P$**, with geometric and algebraic reasons — closing loops from Weeks 1, 4 and 7. **A projection has eigenvalues $0$ and $1$, with eigenspaces $W^\perp$ and $W$.**
7. **$(A^\mathsf{T}A)^{-1}A^\mathsf{T}$ is a left inverse and not a right one**, which is Week 1's promised non-square example.

---

## Exercises

*(Not assessed.)*

1. Project $(1,2,3)$ onto the line through $(1,1,1)$. Give $p$, $e$, and check $e \perp a$.
2. Find the projection matrix onto the line through $(3,4)$ in $\mathbb{R}^2$. Verify $P^2 = P$, $P^\mathsf{T} = P$, and $\operatorname{trace}P = 1$. **Why must the trace be 1?**
3. For $A = \begin{bmatrix}1&0\\ 0&1\\ 1&1\end{bmatrix}$, compute $P$ and project $b = (1,1,0)$. Verify the error is in $\mathbf{N}(A^\mathsf{T})$.
4. Prove $\operatorname{trace}P = \dim W$ for any projection matrix. *(Use the eigenvalues from §5 and Week 6's L20 §2.)*
5. Show that $I - P$ is also a projection, and identify the subspace it projects onto.
6. $A$ has **dependent** columns. **What goes wrong with $P = A(A^\mathsf{T}A)^{-1}A^\mathsf{T}$?** Does the projection itself still exist? *(It does — the subspace is fine; only the formula fails. Week 11 fixes this.)*
7. Prove that a symmetric matrix with $P^2 = P$ **is** the projection onto its column space. *(The converse of §5.)*

---

*MATH 241 · Week 8 · L25 · © CSE Department*
