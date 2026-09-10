# MATH 241 · Linear Algebra
## Week 3 · Lecture 3 of 3 · **Friday**
### The Four Fundamental Subspaces

---

**Reading:** Strang §3.6 · **Previous:** L11, basis and dimension · **Next:** Week 4, linear transformations

> **PS 2 is due at 17:00 today.** PS 3 was released Wednesday and is due the Friday of Week 4.
>
> **Every number in this lecture is reproduced by `resources/dimension.py`.**

---

## 1. Two More, and Where They Come From

Week 2 built $\mathbf{C}(A)$ and $\mathbf{N}(A)$. **Now apply the same two constructions to $A^\mathsf{T}$** and you have four:

| | Name | Definition | Lives in |
|---|---|---|---|
| 1 | **column space** | $\mathbf{C}(A)$, span of the columns | $\mathbb{R}^m$ |
| 2 | **null space** | $\mathbf{N}(A) = \{x : Ax = 0\}$ | $\mathbb{R}^n$ |
| 3 | **row space** | $\mathbf{C}(A^\mathsf{T})$, span of the **rows** | $\mathbb{R}^n$ |
| 4 | **left null space** | $\mathbf{N}(A^\mathsf{T}) = \{y : A^\mathsf{T}y = 0\}$ | $\mathbb{R}^m$ |

**No new definitions were needed** — transposing turns rows into columns, so the row space of $A$ *is* the column space of $A^\mathsf{T}$, and this course reads columns by default.

**"Left" null space, because $A^\mathsf{T}y = 0$ is the same as $y^\mathsf{T}A = 0$** — transposing both sides. So $y$ kills $A$ from the left, where $x \in \mathbf{N}(A)$ kills it from the right.

> **Why four and not eight.** These are the only subspaces you can build from $A$ by spanning or by
> solving $=0$, on either side. **And two of them you have already met without the name:** Week 2's
> L08 §5 found the equation of $\mathbf{C}(A)$ from a vector perpendicular to all the columns —
> that vector is a basis for $\mathbf{N}(A^\mathsf{T})$, and §5 is the payoff.

---

## 2. All Four, on One Matrix

The same $A$ as Week 2, now for the third week:

$$A = \begin{bmatrix}1&3&3&2\\ 2&6&9&7\\ -1&-3&3&4\end{bmatrix} \quad (3\times4), \qquad R = \operatorname{rref}(A) = \begin{bmatrix}1&3&0&-1\\ 0&0&1&1\\ 0&0&0&0\end{bmatrix}, \qquad r = 2$$

| Subspace | In | $\dim$ | Basis |
|---|---|---:|---|
| $\mathbf{C}(A)$ | $\mathbb{R}^3$ | $r = 2$ | $(1,2,-1),\;(3,9,3)$ — **pivot columns of $A$** |
| $\mathbf{N}(A)$ | $\mathbb{R}^4$ | $n - r = 2$ | $(-3,1,0,0),\;(1,0,-1,1)$ — special solutions |
| $\mathbf{C}(A^\mathsf{T})$ | $\mathbb{R}^4$ | $r = 2$ | $(1,3,0,-1),\;(0,0,1,1)$ — **nonzero rows of $R$** |
| $\mathbf{N}(A^\mathsf{T})$ | $\mathbb{R}^3$ | $m - r = 1$ | $(5,-2,1)$ |

**Two live in $\mathbb{R}^3$ and two in $\mathbb{R}^4$, and the pairing is not the one you would guess:** $\mathbf{C}(A)$ pairs with $\mathbf{N}(A^\mathsf{T})$ in $\mathbb{R}^m$, and $\mathbf{N}(A)$ pairs with $\mathbf{C}(A^\mathsf{T})$ in $\mathbb{R}^n$. **§7 shows those pairings are orthogonal**, which is why they are the right ones.

---

## 3. The Dimensions

> **The fundamental theorem of linear algebra, part 1.** For any $m\times n$ matrix of rank $r$:
>
> $$\dim\mathbf{C}(A) = r \qquad \dim\mathbf{C}(A^\mathsf{T}) = r$$
> $$\dim\mathbf{N}(A) = n - r \qquad \dim\mathbf{N}(A^\mathsf{T}) = m - r$$

**Two of these are Week 2 with L11's guarantee attached.** The other two are new, and the row-space one is the surprise.

$$\underbrace{r + (n-r) = n}_{\text{in } \mathbb{R}^n} \qquad\qquad \underbrace{r + (m-r) = m}_{\text{in } \mathbb{R}^m}$$

**Each space is split by the pair living in it**, and the same $r$ appears in both lines.

### Why $\dim\mathbf{C}(A^\mathsf{T}) = r$: elimination keeps the row space

**Row operations replace rows by combinations of rows.** So every row of the new matrix is in the span of the old rows — and since the operations are invertible, every old row is in the span of the new ones. **The span is unchanged:**

$$\mathbf{C}(A^\mathsf{T}) = \mathbf{C}(R^\mathsf{T})$$

For the example, each row of $A$ is a combination of $R$'s two nonzero rows:

| | | |
|---|---|---|
| row 1 | $1(1,3,0,-1) + 3(0,0,1,1)$ | $= (1,3,3,2)$ ✓ |
| row 2 | $2(1,3,0,-1) + 9(0,0,1,1)$ | $= (2,6,9,7)$ ✓ |
| row 3 | $-1(1,3,0,-1) + 3(0,0,1,1)$ | $= (-1,-3,3,4)$ ✓ |

And the nonzero rows of $R$ are **independent** — each has a leading $1$ in a column where the others are $0$ — so they are a basis, and there are $r$ of them.

> **This is the exact dual of Week 2's L08 §4, and the pair is worth memorising as a pair:**
>
> | | Preserved by elimination? | Basis read from |
> |---|---|---|
> | **Row space** $\mathbf{C}(A^\mathsf{T})$ | **yes** | the nonzero rows of $R$ |
> | **Column space** $\mathbf{C}(A)$ | **no** | the pivot columns of $A$ |
>
> Elimination *combines rows*, so the row space survives and the column space does not. **The
> asymmetry in the recipes is not arbitrary** — it is this fact, and every student who mixes up the
> two recipes has not noticed that the algorithm treats rows and columns completely differently.

---

## 4. Row Rank $=$ Column Rank

$$\dim\mathbf{C}(A) = \dim\mathbf{C}(A^\mathsf{T}) = r$$

**The number of independent columns equals the number of independent rows.** Here: $4$ columns in $\mathbb{R}^3$ with $2$ independent, and $3$ rows in $\mathbb{R}^4$ with $2$ independent. **The same $2$.**

**It should strike you as unlikely.** The columns are four vectors in a 3-dimensional space; the rows are three vectors in a 4-dimensional space. Different vectors, different ambient spaces, different counts of them — and the answers agree, for every matrix ever written.

*Proof, and it is short because §3 did the work:* elimination produces $r$ pivots. The nonzero rows of $R$ are $r$ independent vectors spanning the row space, so $\dim\mathbf{C}(A^\mathsf{T}) = r$. The pivot columns of $A$ are $r$ independent vectors spanning the column space (L10 §5, L11 §6), so $\dim\mathbf{C}(A) = r$. **Both counts are the number of pivots, so they are equal.** $\square$

> **The proof is a little unsatisfying and it is worth saying so.** It routes both counts through
> one algorithm and concludes they agree because the algorithm produced one number — true, and it
> does not explain *why* rows and columns should know about each other. **Week 11's SVD gives the
> answer that does explain it:** $r$ is the number of nonzero singular values, a quantity attached
> to $A$ itself with no reference to rows, columns, or elimination.

---

## 5. The Left Null Space Is the List of Solvability Conditions

**This is the lecture's payoff, and it closes something Week 2 left open.**

Week 2's L08 §5 found by hand that $\mathbf{C}(A)$ is the plane $5b_1 - 2b_2 + b_3 = 0$, and remarked that $(5,-2,1)$ must be perpendicular to every column. Being perpendicular to every column of $A$ is exactly $A^\mathsf{T}y = 0$:

$$y = (5,-2,1): \qquad y^\mathsf{T}A = (0,\ 0,\ 0,\ 0)$$

$$\boxed{\;\mathbf{N}(A^\mathsf{T}) = \operatorname{span}\{(5,-2,1)\}, \qquad \dim = m - r = 1\;}$$

**So the plane's coefficient vector was a basis for the left null space all along.** And the dimension count says how many such conditions there are:

> **$Ax = b$ is solvable $\iff$ $y^\mathsf{T}b = 0$ for every $y \in \mathbf{N}(A^\mathsf{T})$.**
>
> *Why:* if $Ax = b$ then $y^\mathsf{T}b = y^\mathsf{T}Ax = 0 \cdot x = 0$. *(The converse needs
> §7's orthogonality and is Week 8's.)*

**$\dim\mathbf{N}(A^\mathsf{T}) = m - r$ is therefore the number of independent solvability conditions on $b$** — and it matches the number of zero rows in $R$, because each zero row is one equation that has become $0 = (\text{something about } b)$.

Here $m - r = 1$: **one zero row, one condition, one dimension.** Week 2 found the condition without knowing to expect exactly one.

---

## 6. The Big Picture

$$
\begin{array}{ccc}
\textbf{in } \mathbb{R}^n = \mathbb{R}^4 & \qquad\xrightarrow{\quad A \quad}\qquad & \textbf{in } \mathbb{R}^m = \mathbb{R}^3\\[6pt]
\hline\\[-6pt]
\mathbf{C}(A^\mathsf{T}) \;\; \dim r = 2 & \longrightarrow & \mathbf{C}(A) \;\; \dim r = 2\\[4pt]
\text{\small row space} & \text{\small carried across, one-to-one} & \text{\small column space}\\[10pt]
\oplus\ \perp & & \oplus\ \perp\\[10pt]
\mathbf{N}(A) \;\; \dim n - r = 2 & \longrightarrow\ \{0\} & \mathbf{N}(A^\mathsf{T}) \;\; \dim m - r = 1\\[4pt]
\text{\small null space} & \text{\small crushed to zero} & \text{\small left null space, unreached}
\end{array}
$$

**Read $A$ as a machine taking $\mathbb{R}^4$ to $\mathbb{R}^3$.**

- **$\mathbb{R}^4$ splits into the row space and the null space** — dimensions $2 + 2 = 4$.
- Everything in the **null space** is sent to $0$: the machine cannot see it.
- Everything in the **row space** is carried onto the **column space**, and §7's orthogonality makes this a one-to-one correspondence between two spaces of the same dimension $r$. **That is the real content of row rank = column rank.**
- **$\mathbb{R}^3$ splits into the column space and the left null space** — $2 + 1 = 3$. Nothing lands outside $\mathbf{C}(A)$, and the left null space measures how much of the target is out of reach.

> **Every question from Weeks 0–3 is a question about this diagram.** *Is $Ax = b$ solvable?* — is
> $b$ in the right-hand top box. *Is the solution unique?* — is the bottom-left box $\{0\}$. *How
> many solutions?* — the dimension of that box. **Week 9's least squares is what to do when $b$ has
> a component in the bottom-right box**: you cannot reach it, so you project it away.

---

## 7. The Pairs Are Orthogonal

Every dot product between a null-space vector and a row-space vector, computed:

| | $(1,3,0,-1)$ | $(0,0,1,1)$ |
|---|---:|---:|
| $(-3,1,0,0)$ | $0$ | $0$ |
| $(1,0,-1,1)$ | $0$ | $0$ |

And on the other side, $(5,-2,1)$ against the column-space basis: $5 - 4 - 1 = 0$ and $15 - 18 + 3 = 0$.

**All six are zero, and nothing was arranged to make them so.**

**The reason is one line.** $x \in \mathbf{N}(A)$ means $Ax = 0$, and the $i$-th entry of $Ax$ is *(row $i$) $\cdot\, x$*. So $Ax = 0$ says precisely that **$x$ is perpendicular to every row** — hence to every combination of rows, hence to the whole row space.

$$\mathbf{N}(A) \perp \mathbf{C}(A^\mathsf{T}) \qquad\text{and}\qquad \mathbf{N}(A^\mathsf{T}) \perp \mathbf{C}(A)$$

> **This is part 2 of the fundamental theorem and it is Week 8's**, because "perpendicular" needs
> the dot product, and L07 §2 deliberately built vector spaces without one. What you can see now is
> that **the dimensions already fit**: $r + (n-r) = n$ is exactly what two perpendicular subspaces
> filling $\mathbb{R}^n$ would need. **Week 8 turns that arithmetic coincidence into a theorem**, and
> Weeks 9 and 11 are built on it.

---

## 8. What to Take Away

1. **Four subspaces, from two constructions applied to $A$ and $A^\mathsf{T}$.** Row space and left null space are not new ideas.
2. **Dimensions $r$, $n-r$, $r$, $m-r$** — the pair in $\mathbb{R}^n$ adds to $n$, the pair in $\mathbb{R}^m$ adds to $m$.
3. **Elimination preserves the row space and moves the column space.** That single asymmetry is why a row-space basis is read off $R$ and a column-space basis must be read back from $A$.
4. **Row rank $=$ column rank**, both equal to the pivot count. It is surprising, the elimination proof does not explain it, and Week 11 does.
5. **$\mathbf{N}(A^\mathsf{T})$ is the list of solvability conditions on $b$**, one per dimension — which is why Week 2 found exactly one for this matrix.
6. **$\mathbb{R}^n$ splits into row space + null space; $\mathbb{R}^m$ into column space + left null space.** $A$ crushes the second and carries the first across one-to-one.
7. **The pairs are orthogonal**, which the dimensions already anticipate and Week 8 proves.

---

## Exercises

*(Not assessed. PS 3 is due Friday of Week 4.)*

1. For $A = \begin{bmatrix}1&2&3\\ 2&4&6\end{bmatrix}$, find bases and dimensions for all four subspaces, and check both dimension sums.
2. $A$ is $5\times3$ with rank 3. Give the dimension of each of the four subspaces. Which are $\{0\}$? Is $Ax = b$ solvable for every $b$?
3. Construct a $3\times3$ matrix whose left null space is spanned by $(1,1,1)$. *(What must be true of the rows?)*
4. Prove $\mathbf{N}(A) \perp \mathbf{C}(A^\mathsf{T})$ directly from $Ax = 0$, in two lines, as in §7.
5. **True or false, with a reason:** $\mathbf{C}(A) = \mathbf{C}(A^\mathsf{T})$ is impossible unless $A$ is square. If $A$ *is* square, must they be equal?
6. $A$ is $m\times n$ with $m < n$. Show $\mathbf{N}(A) \ne \{0\}$ using only the dimension formulas of §3. *(You proved this twice already — Week 2's L09 §4 and L10 §4. This is the third proof and the shortest.)*
7. Show that $\operatorname{rank}(A) = \operatorname{rank}(A^\mathsf{T})$ implies $\operatorname{rank}(A^\mathsf{T}A) = \operatorname{rank}(A)$, using PS 2 Q5(c). **This is the fact Week 9 runs on.**

---

*MATH 241 · Week 3 · L12 · © CSE Department*
