# MATH 241 · Linear Algebra
## Week 8 · Lecture 1 of 3 · **Monday**
### Orthogonality

---

**Reading:** Strang §4.1 · **Previous:** Week 7's L23, complex eigenvalues · **Next:** L25, projections

> **Quiz 8 is the first ten minutes of this lecture** and covers Week 7.
>
> **Two evening exams this week, neither of them ours.** PROG 201's Midterm 2 is **tonight**
> (18:00–19:30, Weeks 4–7) and CS 211's is **Tuesday** (20:00–21:15). MATH 241 has no exam this week
> — **its Midterm 2 is Week 10** — and PS 7 is due Friday as usual.

---

## 1. The Structure Week 2 Deliberately Left Out

Week 2's L07 §2 defined a vector space with **ten axioms and no length, no angle, no way to multiply two vectors**, and said so explicitly:

> *Length and angle come back in **Week 8**, when they are added as extra structure. Everything
> between here and there is deliberately done without them, so that you find out how much does not
> need them.*

**The answer turned out to be: almost everything.** Bases, dimension, rank, the four subspaces, determinants, eigenvalues, diagonalisation — six weeks of material, none of it needing a notion of *perpendicular*.

**This week adds the missing structure**, and it immediately pays three debts:

| Debt | Owed since |
|---|---|
| The four subspaces are orthogonal in pairs | **Week 3**, L12 §7 — observed, unproved |
| A projection matrix, and why $P^2 = P$ | **Weeks 1 and 4** — met, unexplained |
| An orthonormal basis has $\operatorname{cond} = 1$ | **Weeks 0 and 7** — the fix for L22 §4's problem |

---

## 2. The Dot Product, and What It Measures

$$x^\mathsf{T}y = x_1y_1 + x_2y_2 + \dots + x_ny_n$$

**You have used this since Week 0** as notation for a row times a column. **Now it acquires geometry.**

$$\lVert x\rVert = \sqrt{x^\mathsf{T}x} = \sqrt{x_1^2 + \dots + x_n^2} \qquad\text{(the *length*, or *norm*)}$$

and for nonzero $x, y$,

$$\cos\theta = \frac{x^\mathsf{T}y}{\lVert x\rVert\,\lVert y\rVert}$$

**In $\mathbb{R}^2$ and $\mathbb{R}^3$ this is Pythagoras and the cosine rule**, which is where it comes from. **In $\mathbb{R}^{10}$ it is a definition** — there is no independent notion of "angle" in ten dimensions to check it against, and this formula is what the word means there.

> **That the formula makes sense at all is a theorem.** $\lvert\cos\theta\rvert \le 1$ requires
> $$\lvert x^\mathsf{T}y\rvert \le \lVert x\rVert\,\lVert y\rVert,$$
> the **Cauchy–Schwarz inequality**, which is true in every dimension and is what licenses calling
> the quotient a cosine. *(Proof: $\lVert x - ty\rVert^2 \ge 0$ for all $t$; expand, and the
> discriminant of that quadratic in $t$ must be $\le 0$. Exercise 2.)*

### Orthogonal

$$\boxed{\;x \perp y \iff x^\mathsf{T}y = 0\;}$$

**Perpendicular means the dot product vanishes**, and that is the definition from here on. **$0$ is orthogonal to everything**, which is a convention that keeps every theorem clean and occasionally surprises people.

**Pythagoras, in $n$ dimensions:** $x \perp y$ **iff** $\lVert x+y\rVert^2 = \lVert x\rVert^2 + \lVert y\rVert^2$, since

$$\lVert x+y\rVert^2 = (x+y)^\mathsf{T}(x+y) = \lVert x\rVert^2 + 2x^\mathsf{T}y + \lVert y\rVert^2.$$

**The cross term is exactly the dot product**, so it vanishes precisely when they are orthogonal.

---

## 3. Orthogonal Subspaces

> **Two subspaces $V$ and $W$ are orthogonal if $v^\mathsf{T}w = 0$ for every $v \in V$ and every
> $w \in W$.**

**Every vector of one against every vector of the other** — a strong condition, and easier to check than it looks: **it suffices to check the basis vectors.** If $v = \sum c_iv_i$ and $w = \sum d_jw_j$ then $v^\mathsf{T}w = \sum_{i,j}c_id_j\,v_i^\mathsf{T}w_j$, which vanishes if every $v_i^\mathsf{T}w_j$ does.

> **A common misreading, worth killing now.** The floor and a wall of a room are **not** orthogonal
> subspaces, even though they meet at right angles. They share the line where they meet, and a
> nonzero vector along that line is not orthogonal to itself. **Two orthogonal subspaces intersect
> only in $\{0\}$** — which follows immediately: $v \in V \cap W$ gives $v^\mathsf{T}v = 0$, so
> $\lVert v\rVert = 0$, so $v = 0$.

---

## 4. The Four Subspaces, Orthogonal in Pairs — Week 3's Debt

Week 3's L12 §7 computed ten dot products, found them all zero, and said: *this is part 2 of the fundamental theorem and it is Week 8's, because "perpendicular" needs the dot product.* **Here it is.**

> **Theorem.** $\mathbf{N}(A) \perp \mathbf{C}(A^\mathsf{T})$ in $\mathbb{R}^n$, and
> $\mathbf{N}(A^\mathsf{T}) \perp \mathbf{C}(A)$ in $\mathbb{R}^m$.
>
> *Proof.* $x \in \mathbf{N}(A)$ means $Ax = 0$ — **every entry of $Ax$ is zero.** And entry $i$ of
> $Ax$ is *(row $i$ of $A$) $\cdot\ x$*. So $x$ is orthogonal to **every row**, hence (§3) to every
> combination of rows, hence to the whole row space. $\square$
>
> The second statement is the first applied to $A^\mathsf{T}$.

**One line**, and it needed nothing but the definition of matrix–vector multiplication read the right way. **Verified on Week 3's matrix:** all ten dot products zero, as computed there and reproduced by this week's script.

### The stronger statement, and why it matters

Week 3's REC 3 §2(d) asked a sharp question: **the two dimensions add to $n$ — does that prove the two subspaces fill $\mathbb{R}^n$ between them?** The answer was **no**: two lines in $\mathbb{R}^3$ have dimensions summing to $2$ and fill only a plane at best.

**Orthogonality is what upgrades the arithmetic into a theorem:**

> **Definition.** $W^\perp$ (*"$W$ perp"*) is the set of all vectors orthogonal to every vector of
> $W$ — the **orthogonal complement**.
>
> **Theorem.** For a subspace $W \subseteq \mathbb{R}^n$: $\;\dim W + \dim W^\perp = n$, and every
> $x \in \mathbb{R}^n$ splits **uniquely** as $x = w + w^\perp$.

$$\boxed{\;\mathbf{N}(A) = \mathbf{C}(A^\mathsf{T})^\perp \qquad\text{and}\qquad \mathbf{N}(A^\mathsf{T}) = \mathbf{C}(A)^\perp\;}$$

**Not merely orthogonal — orthogonal *complements*.** The subspaces are as large as orthogonality permits, and together they exhaust the space.

> **Two things this settles.**
>
> **Week 3's L12 §5 owed a converse.** It proved that $Ax = b$ solvable implies
> $y^\mathsf{T}b = 0$ for every $y \in \mathbf{N}(A^\mathsf{T})$, and said the reverse needed Week 8. **It does, and
> it is now immediate:** if $b \perp \mathbf{N}(A^\mathsf{T}) = \mathbf{C}(A)^\perp$, then
> $b \in (\mathbf{C}(A)^\perp)^\perp = \mathbf{C}(A)$, so the system is solvable. **The solvability
> conditions are not just necessary; they are sufficient.**
>
> **And L25's projection is the splitting.** $x = w + w^\perp$ is exactly *"the part of $x$ inside
> $W$, plus the part outside"*, and computing $w$ is what a projection does.

---

## 5. The Matrices That Preserve All of This

A matrix $Q$ with **orthonormal columns** — pairwise orthogonal, each of length 1 — satisfies

$$\boxed{\;Q^\mathsf{T}Q = I\;}$$

because entry $(i,j)$ of $Q^\mathsf{T}Q$ is $q_i^\mathsf{T}q_j$, which is $1$ when $i = j$ and $0$ otherwise. **The condition is the definition, written as one matrix equation.**

**For a square $Q$ this says $Q^{-1} = Q^\mathsf{T}$** — and such a matrix is called **orthogonal**. *(An unfortunate name: it should be "orthonormal", since orthogonal columns alone are not enough. It is standard and you are stuck with it.)*

**You have met three already:**

| | Week |
|---|---|
| **Permutation matrices**, $P^{-1} = P^\mathsf{T}$ | **3**, L06 §6 — "your first orthogonal matrix" |
| **Rotations**, $R_\theta^\mathsf{T}R_\theta = I$ | 4 |
| Reflections | 4 |

**And Week 5's PS 5 Q5(d) proved $\det Q = \pm1$** for all of them: rotations $+1$, reflections $-1$.

**What they preserve:**

$$\lVert Qx\rVert^2 = (Qx)^\mathsf{T}(Qx) = x^\mathsf{T}Q^\mathsf{T}Qx = x^\mathsf{T}x = \lVert x\rVert^2$$

**Lengths are unchanged**, and so are angles, since $(Qx)^\mathsf{T}(Qy) = x^\mathsf{T}y$. **An orthogonal matrix is a rigid motion** — it moves the space without distorting it.

> **And hence the fact this week exists for.** $\operatorname{cond}(Q) = 1$, the smallest a condition
> number can be. **Week 7's L22 §4 was a complaint about exactly this**: near a defective matrix the
> eigenvector basis $S$ is nearly singular, $\operatorname{cond}(S)$ explodes, and
> $A = S\Lambda S^{-1}$ becomes numerically worthless even though it exists.
>
> **Measured:** eigenvectors $(1,0)$ and $(1,\varepsilon)$ give $\operatorname{cond}(S) = 200$,
> $2\times10^4$, $1.3\times10^8$ at $\varepsilon = 10^{-2}, 10^{-4}, 10^{-8}$.
> **An orthonormal basis gives $1$ at every row of that table.**
>
> **Weeks 10 and 11 both insist on orthonormal bases for this reason and no other.**

---

## 6. What to Take Away

1. **Week 2 built vector spaces without length or angle deliberately**, to show how much does not need them. Six weeks did not.
2. **$x^\mathsf{T}y$ gives length and angle**, and $\lvert\cos\theta\rvert \le 1$ is Cauchy–Schwarz — a theorem, not a definition.
3. **$x \perp y \iff x^\mathsf{T}y = 0$**, and Pythagoras holds in $\mathbb{R}^n$ because the cross term *is* the dot product.
4. **Orthogonal subspaces meet only at $0$** — the floor and the wall are not orthogonal.
5. **The four subspaces are orthogonal in pairs**, proved in one line: $Ax = 0$ says $x \perp$ every row.
6. **They are orthogonal *complements*** — dimensions add to $n$ and the split is unique. This is what Week 3's REC 3 §2(d) showed dimension arithmetic alone cannot give, and it supplies **the converse Week 3's L12 §5 owed.**
7. **$Q^\mathsf{T}Q = I$ makes $Q^{-1} = Q^\mathsf{T}$**, preserves lengths and angles, and gives $\operatorname{cond}(Q) = 1$ — **the fix for Week 7's conditioning problem.**

---

## Exercises

*(Not assessed. PS 8 is the assessed work.)*

1. Find the angle between $(1,1,0)$ and $(1,0,1)$. Then between $(1,1,1,1)$ and $(1,1,-1,-1)$ in $\mathbb{R}^4$.
2. Prove Cauchy–Schwarz: expand $\lVert x - ty\rVert^2 \ge 0$ as a quadratic in $t$ and use the discriminant.
3. Show that if $V \perp W$ then $V \cap W = \{0\}$. **Give two subspaces of $\mathbb{R}^3$ that meet only at $0$ and are *not* orthogonal.**
4. For $A = \begin{bmatrix}1&2\\ 1&2\\ 1&2\end{bmatrix}$, find bases for all four subspaces and verify every orthogonality relation by direct computation.
5. Prove that the rows of an orthogonal matrix are also orthonormal. *(Use $Q^\mathsf{T}Q = I$ and $QQ^\mathsf{T} = I$ — and say why the second follows from the first for square $Q$.)*
6. Let $W$ be the plane $x + y + z = 0$ in $\mathbb{R}^3$. Find $W^\perp$, check the dimensions sum to 3, and split $(3,0,0)$ into its two parts.
7. **True or false:** if $\lVert Ax\rVert = \lVert x\rVert$ for every $x$, then $A$ is orthogonal. *(Consider $\lVert A(x+y)\rVert^2$.)*

---

*MATH 241 · Week 8 · L24 · © CSE Department*
