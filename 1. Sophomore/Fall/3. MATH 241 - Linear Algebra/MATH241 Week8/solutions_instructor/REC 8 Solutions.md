# MATH 241 · Recitation 8 — Solutions and Session Notes
## **INSTRUCTOR ONLY** · Do not distribute

**Session:** Thursday of Week 9, 15:00–15:50, SSB 108 · covers Week 8 · unmarked
**PS 8 is due 17:00 the following day. Midterm 2 is the Wednesday of Week 10, covering Weeks 6–9.**

---

## Running the Session

**§2 is the session.** Week 9 is least squares, which is this projection with data attached, and **every Week 9 difficulty is a Week 8 difficulty in disguise.** A pair that can project onto a plane by hand will find next week routine.

**This is also the last recitation before Midterm 2's material is complete**, so leave a few minutes at the end for exam questions.

| | Section | Budget | If it overruns |
|---|---|---|---|
| §1 | The drill | 10 min | Cut to (b) and (d) |
| §2 | Onto a plane | 15 min | **Protect. Cut §4** |
| §3 | Gram–Schmidt and order | 10 min | Keep (b) and (c) |
| §4 | The machine | 10 min | Drop |
| §5 | Clinic + exam questions | 5 min | Never drop |

---

## §0 / §1 — The Drill

$a = (1,1,1)$, $b = (2,3,5)$: $\;\hat x = \dfrac{10}{3}$, $\;p = \left(\tfrac{10}{3},\tfrac{10}{3},\tfrac{10}{3}\right)$, $\;e = \left(-\tfrac43,-\tfrac13,\tfrac53\right)$

$a^\mathsf{T}e = -\tfrac43 - \tfrac13 + \tfrac53 = 0$ ✓

**(b)** **$a^\mathsf{T}a = 3$ is a number. $aa^\mathsf{T}$ is the $3\times3$ matrix of all ones**, which has rank 1.

$$P = \frac{aa^\mathsf{T}}{a^\mathsf{T}a} = \frac13\begin{bmatrix}1&1&1\\1&1&1\\1&1&1\end{bmatrix}, \qquad P^2 = P\ ✓$$

*This is the commonest slip in Week 8 and it is worth thirty seconds at the board: **the outer product is a matrix, the inner product is a number**, and putting the matrix in the denominator is not a typo you will notice later.*

**(c)** **$\operatorname{trace}P = 1$**, and it must be, because the trace of a projection is the dimension of the subspace it projects onto — here a line. *(PS 8 Q2(d).)*

**(d)** **Predictions, both from the eigenvalues:**

- $P(1,1,1) = (1,1,1)$ — the vector is **on** the line, so it is fixed. $\lambda = 1$.
- $P(1,-1,0) = (0,0,0)$ — the vector is **perpendicular** to the line ($1 - 1 + 0 = 0$), so it is annihilated. $\lambda = 0$.

**A projection has no other behaviour**, and a pair that predicts both correctly has understood L25 §5 better than one that computes them.

---

## §2 — Onto a Plane

$$A = \begin{bmatrix}1&1\\ 1&0\\ 0&1\end{bmatrix}, \qquad b = (3,0,0)$$

*(First: $b$ is outside $\mathbf{C}(A)$ — the columns are $(1,1,0)$ and $(1,0,1)$, and no combination of them has second and third entries both zero unless it is zero. Confirmed properly in (d).)*

**(a)** $A^\mathsf{T}A = \begin{bmatrix}2&1\\1&2\end{bmatrix}$.

**Invertible because $A$ has independent columns**: $\mathbf{N}(A^\mathsf{T}A) = \mathbf{N}(A) = \{0\}$, which is **PS 2 Q5(c), Week 2.** *(Insist on the citation. It was proved seven weeks ago for exactly this moment.)*

**(b)** $A^\mathsf{T}b = (3,3)$, and solving $\begin{bmatrix}2&1\\1&2\end{bmatrix}\hat x = \begin{bmatrix}3\\3\end{bmatrix}$ gives $\hat x = (1,1)$.

**(c)** $p = A\hat x = (1,1,0) + (1,0,1) = (2,1,1)$, and $e = b - p = (1,-1,-1)$.

**(d)** $A^\mathsf{T}e = (1 - 1 + 0,\ 1 + 0 - 1) = (0,0)$ ✓

**$e \in \mathbf{N}(A^\mathsf{T})$ — the left null space**, spanned by $(-1,1,1)$, and indeed $e = -(-1,1,1)$.

**$b$ is being split between $\mathbf{C}(A)$ and $\mathbf{N}(A^\mathsf{T})$** — the two subspaces of $\mathbb{R}^3$ from Week 3's four-subspace picture. **This is L24 §4's decomposition, not a new idea.**

**(e)** $P = \tfrac13\begin{bmatrix}2&1&1\\ 1&2&-1\\ 1&-1&2\end{bmatrix}$, and $Pb = (2,1,1)$ ✓ — the same $p$.

**(f) — the argument**

**For $A$ of size $1000\times5$:**

- **The normal equations** are a $5\times5$ system. $A^\mathsf{T}A$ is $5\times5$ — **25 numbers.**
- **$P$ is $1000\times1000$** — **a million numbers**, to represent a projection onto a 5-dimensional subspace.

**So never form $P$** unless you need it as an object in its own right. **Form $A^\mathsf{T}A$ and solve.**

> **And Week 9 goes one better: it does not form $A^\mathsf{T}A$ either**, because that squares the
> condition number. **PS 8 Q4(d) derives the replacement** — substitute $A = QR$ and the normal
> equations collapse to $R\hat x = Q^\mathsf{T}b$, a triangular solve. **If a pair has done Q4(d),
> ask them to say what disappeared.**

---

## §3 — Gram–Schmidt and the Order

**(a)** From $(1,1,0)$, $(1,0,1)$, $(0,1,1)$:

$$w_1 = (1,1,0), \qquad w_2 = \left(\tfrac12,-\tfrac12,1\right) \sim (1,-1,2), \qquad w_3 = \left(-\tfrac23,\tfrac23,\tfrac23\right) \sim (-1,1,1)$$

**Checks:** $(1,1,0)\cdot(1,-1,2) = 0$ ✓ · $(1,1,0)\cdot(-1,1,1) = 0$ ✓ · $(1,-1,2)\cdot(-1,1,1) = -1-1+2 = 0$ ✓

**(b)** Reversed — $(0,1,1)$, $(1,0,1)$, $(1,1,0)$:

$$w_1 = (0,1,1), \qquad w_2 = \left(1,-\tfrac12,\tfrac12\right) \sim (2,-1,1), \qquad w_3 \sim (1,1,-1)$$

**A completely different orthogonal set**, spanning the same space.

**(c)** **$q_1$ is always a unit multiple of $a_1$** — the first vector is never changed in direction, because there is nothing yet to subtract. **Everything after it is determined by that choice**, so reordering changes all of it. **Gram–Schmidt is order-dependent by construction.**

**(d) — the question worth the section**

**What is the same:**

- **The span of all three** is unchanged — it is $\mathbb{R}^3$ either way.
- **More sharply:** $\operatorname{span}\{q_1\} = \operatorname{span}\{a_1\}$, and $\operatorname{span}\{q_1,q_2\} = \operatorname{span}\{a_1,a_2\}$, and so on. **Gram–Schmidt preserves every *initial* span**, which is precisely why $R$ comes out upper triangular in $A = QR$.

**So the two runs agree on the nested chain of subspaces they build**, and disagree on everything else — because the chains themselves differ once the order does.

*A pair that connects the order-dependence to $R$ being triangular has understood L26 §4. Say so.*

---

## §4 — The Machine

**(a)** Ten dot products, all zero. **Week 3's L12 §7 computed exactly these** and could only observe them; L24 §4 proves them in one line.

**(b)** $e = (1,-2,1)$ against columns $(1,1,1)$ and $(1,2,3)$: $1 - 2 + 1 = 0$ ✓ and $1 - 4 + 3 = 0$ ✓ — **and $A^\mathsf{T}e = 0$ says $e$ is in the left null space.**

**(c)** The connection: **Week 7's L22 §4 showed $A = S\Lambda S^{-1}$ can exist and be numerically worthless**, because $S$ is nearly singular when the eigenvectors are nearly parallel, so $S^{-1}$ amplifies every rounding error by $\operatorname{cond}(S)$. **An orthonormal basis has $\operatorname{cond} = 1$, so there is no amplification at all.**

**That is the entire design rationale for Weeks 9, 10 and 11.**

**(d)** With four points $x = 1,2,3,4$: the first three orthogonal vectors are the constant, linear and quadratic patterns again — $(1,1,1,1)$, $(-3,-1,1,3)$, $(1,-1,-1,1)$. **The pattern continues and the vectors are the discrete orthogonal polynomials at four nodes.**

---

## §5 — Clinic and Exam Notes

**Q2(a).** §1(b). Refuse to re-derive.

**Q4(d).** *"Substitute, then look for $Q^\mathsf{T}Q$."* And then: **"what can you cancel, and why are you allowed to?"** The justification — $R$ invertible, hence $R^\mathsf{T}$ — is half the marks.

**Q3(c).** §3.

**Q5(d).** The two sentences must name Week 7. A general remark about orthonormal bases being convenient is not the answer.

### Midterm 2 — what to say if asked

**Wednesday of Week 10, 18:00–19:15, SSB 110, covering Weeks 6–9.** One handwritten sheet, one side.

**Three things worth saying:**

1. **Weeks 6–9 are a single arc**, not four topics: eigenvalues → diagonalisation → orthogonality → least squares. **A gap in Week 6 shows up as a failure in Week 9.**
2. **On the sheet:** the diagonalisability criterion, $\sum\lambda = \operatorname{trace}$ and $\prod\lambda = \det$, the normal equations, and $P = A(A^\mathsf{T}A)^{-1}A^\mathsf{T}$. **Not** the rotation matrix or the $2\times2$ inverse — derivable in seconds.
3. **The commonest lost marks in this material are verification failures**: an unverified eigenvector, an unchecked $S\Lambda S^{-1}$, a projection whose error was never dotted with the columns. **All three checks are exact and take seconds.**

---

## What to Report Back

| Signal | What it means for Week 9 |
|---|---|
| §1(b) confused the two products | Fix immediately; least squares is unreadable with it wrong |
| §2(f) answered without comparing sizes | The practical instinct is missing. Week 9's whole argument is about what you form and what you avoid |
| §3(d) reached the initial-span answer | Excellent — that is $A = QR$ understood |
| Students asking about Midterm 2 coverage | Expected. **Weeks 6–9**, and Week 9 finishes the material two days before |

---

*MATH 241 · Week 8 · Recitation 8 Solutions · © CSE Department*
