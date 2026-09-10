# MATH 241 · Problem Set 4 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**All exact arithmetic**; `resources/transformations.py` reproduces the Q2 and Q4 computations.

**What this paper is testing.** Q2(a) and Q3(a) are mechanical and should be near-full marks. **Q3(c) is the best question on the paper** — it identifies the constant of integration as a matrix entry, and a student who sees that has understood what Week 4 is for. **Q4 is the conceptual core**: the same transformation in two bases, with the diagonal form arrived at *geometrically* in (b) before any inverse is computed. Q5(d) is the question that stops trace-and-determinant being mistaken for a complete invariant, and it sets up Week 7.

**Common failure modes:** (1) Q2(a)(2) quoted from memory with a sign error rather than derived; (2) Q4(c) with $M$ the wrong way round; (3) Q3(c) computing $DJ$ and $JD$ correctly and not noticing what the difference *means*; (4) Q5(d) answered "yes" for the first pair.

---

## Q1: Linear or Not (18 points)

### (a) [10] — 2 each

**1. $T(x,y) = (3x-y,\ x)$ — LINEAR.** It is $Av$ with $A = \begin{bmatrix}3&-1\\1&0\end{bmatrix}$, and every matrix map is linear (L13 §3).

**2. $T(x,y) = (x+2,\ y)$ — NOT.** $T(0,0) = (2,0) \ne 0$. **Additivity fails**, and the $T(0) = 0$ test caught it in one substitution.

**3. $T(x,y) = (xy,\ x+y)$ — NOT.** $T(2,2) = (4,4)$ but $2\,T(1,1) = 2(1,2) = (2,4)$. **Homogeneity fails.**

**4. $T(A) = A + A^\mathsf{T}$ — LINEAR.** $(A+B) + (A+B)^\mathsf{T} = (A + A^\mathsf{T}) + (B + B^\mathsf{T})$ and $(cA) + (cA)^\mathsf{T} = c(A + A^\mathsf{T})$, both from Week 1's L06 §1.

**5. $T(A) = \det A$ — NOT.** For $2\times2$, $\det(2A) = 4\det A \ne 2\det A$ unless $\det A = 0$. **Homogeneity fails.** *(Or: $\det(I) + \det(I) = 2$ while $\det(I + I) = \det(2I) = 4$.)*

*Marking: 1 for the verdict, 1 for the specific witness. **A "not linear" with no vectors earns 1.***

### (b) [4]

**$T(v) = Av + b$ fails:** $T(0) = b \ne 0$. *(Also $T(v+u) = A(v+u) + b = Av + Au + b$, while $T(v) + T(u) = Av + Au + 2b$ — they differ by $b$.)*

**$\widetilde T$ is linear** because it is multiplication by a fixed $(n{+}1)\times(n{+}1)$ matrix. And

$$\begin{bmatrix}A&b\\0&1\end{bmatrix}\begin{bmatrix}v\\1\end{bmatrix} = \begin{bmatrix}Av + b\\ 1\end{bmatrix}$$

so on the plane $w = 1$ it reproduces $T$ exactly, and lands back on that plane.

**Why $4\times4$:** a graphics pipeline must compose rotations, scalings **and translations** into a single object, and translation is not linear in $\mathbb{R}^3$. **Embedding $\mathbb{R}^3$ as the plane $w=1$ in $\mathbb{R}^4$ makes it linear**, so the whole pipeline becomes one $4\times4$ product.

*Marking: 1 for the failure, 2 for the block computation, 1 for the graphics sentence.*

### (c) [4]

**($\Rightarrow$)** $T$ injective. $T(0) = 0$, so if $Tv = 0$ then $Tv = T0$, and injectivity gives $v = 0$. Hence $\ker T = \{0\}$.

**($\Leftarrow$)** $\ker T = \{0\}$. If $Tv = Tu$ then $T(v - u) = Tv - Tu = 0$ by linearity, so $v - u \in \ker T = \{0\}$, so $v = u$. $\square$

*Marking: 2 each. **The $\Leftarrow$ direction is where linearity is used** — a script that does not form $T(v-u)$ has not used the hypothesis.*

---

## Q2: Building the Matrix (22 points)

### (a) [8] — 2 each

| | $T(e_1)$ | $T(e_2)$ | Matrix |
|---|---|---|---|
| reflect across $y$-axis | $(-1,0)$ | $(0,1)$ | $\begin{bmatrix}-1&0\\0&1\end{bmatrix}$ |
| rotate $45°$ | $\left(\tfrac{\sqrt2}{2}, \tfrac{\sqrt2}{2}\right)$ | $\left(-\tfrac{\sqrt2}{2}, \tfrac{\sqrt2}{2}\right)$ | $\tfrac{1}{\sqrt2}\begin{bmatrix}1&-1\\1&1\end{bmatrix}$ |
| project onto $x$-axis | $(1,0)$ | $(0,0)$ | $\begin{bmatrix}1&0\\0&0\end{bmatrix}$ |
| shear $(x,y)\mapsto(x+3y,y)$ | $(1,0)$ | $(3,1)$ | $\begin{bmatrix}1&3\\0&1\end{bmatrix}$ |

*Marking: 1 for the two images, 1 for the matrix. **Both images must be shown** — the instruction was explicit, and a quoted rotation matrix with the sign wrong is the failure the instruction exists to prevent.*

### (b) [6]

$$F = \begin{bmatrix}0&1\\1&0\end{bmatrix}, \qquad R = \begin{bmatrix}0&-1\\1&0\end{bmatrix}$$

**$R \circ F$ means $F$ first**, so the matrix is $RF$:

$$RF = \begin{bmatrix}0&-1\\1&0\end{bmatrix}\begin{bmatrix}0&1\\1&0\end{bmatrix} = \begin{bmatrix}-1&0\\0&1\end{bmatrix} \quad\text{— reflection across the } y\text{-axis}$$

$$FR = \begin{bmatrix}0&1\\1&0\end{bmatrix}\begin{bmatrix}0&-1\\1&0\end{bmatrix} = \begin{bmatrix}1&0\\0&-1\end{bmatrix} \quad\text{— reflection across the } x\text{-axis}$$

**Both composites are reflections** — a reflection followed by a rotation is a reflection — **but across different axes.**

**Geometrically — track each basis vector through both orders:**

| | $R \circ F$ *(reflect, then rotate)* | $F \circ R$ *(rotate, then reflect)* |
|---|---|---|
| $e_1$ | $\to e_2 \to -e_1$ | $\to e_2 \to e_1$ |
| $e_2$ | $\to e_1 \to e_2$ | $\to -e_1 \to -e_2$ |

**The two composites already disagree on $e_1$**, and the tables read off as the two matrices above. One fixes the $y$-axis and flips the $x$-axis; the other does the reverse.

*Marking: 3 for the two products with the correct order, 3 for identifying both and a geometric account. **Watch for $FR$ computed and labelled $R\circ F$** — the order convention is the point.*

### (c) [4]

$$A = \begin{bmatrix}1&0&3\\ 2&-1&3\end{bmatrix}, \qquad \operatorname{rref}(A) = \begin{bmatrix}1&0&3\\ 0&1&3\end{bmatrix}$$

**Rank 2, nullity 1.** Free column 3, so $\ker T = \operatorname{span}\{(-3,-3,1)\}$.

Check: $A(-3,-3,1) = -3(1,2) - 3(0,-1) + 1(3,3) = (-3,-6)+(0,3)+(3,3) = (0,0)$ ✓

**Range $= \mathbf{C}(A) = \mathbb{R}^2$** (rank 2 = $m$). **Rank–nullity: $2 + 1 = 3 = n$** ✓

### (d) [4]

$T(u_1) = 4u_1$ and $T(u_2) = 0 = 0\cdot u_2$, so in the $u$-basis the columns are $(4,0)$ and $(0,0)$:

$$B = \begin{bmatrix}4&0\\0&0\end{bmatrix} \quad (\text{basis } \{(1,1),(1,-1)\})$$

**Standard matrix:** $A = MBM^{-1}$ with $M = \begin{bmatrix}1&1\\1&-1\end{bmatrix}$, $M^{-1} = \tfrac12\begin{bmatrix}1&1\\1&-1\end{bmatrix}$:

$$A = \begin{bmatrix}1&1\\1&-1\end{bmatrix}\begin{bmatrix}4&0\\0&0\end{bmatrix}\cdot\tfrac12\begin{bmatrix}1&1\\1&-1\end{bmatrix} = \begin{bmatrix}2&2\\2&2\end{bmatrix}$$

Check: $A(1,1) = (4,4)$ ✓ and $A(1,-1) = (0,0)$ ✓

*(The direct route: $e_1 = \tfrac12(u_1 + u_2)$, so $T(e_1) = \tfrac12(4u_1 + 0) = 2u_1 = (2,2)$; similarly $T(e_2) = (2,2)$. **Accept either, and note which was less work** — for most students the direct route is.)*

*Marking: 2 for $B$ with its basis stated, 2 for $A$ with a check.*

---

## Q3: Calculus as a Matrix (20 points)

### (a) [6]

$$D = \begin{bmatrix}0&1&0&0&0\\ 0&0&2&0&0\\ 0&0&0&3&0\\ 0&0&0&0&4\\ 0&0&0&0&0\end{bmatrix} \qquad (5\times5,\ \text{basis } 1,x,x^2,x^3,x^4)$$

**Rank 4, nullity 1.** $\ker D$ = the constants (dim 1); range = $\mathbb{P}_3$, the polynomials of degree $\le 3$ (dim 4). **$4 + 1 = 5 = \dim\mathbb{P}_4$** ✓

### (b) [4]

$$D^2: 3 \text{ nonzeros} \quad D^3: 2 \quad D^4: 1 \quad D^5 = 0$$

**$D^4$ has the single entry $24$ in position $(1,5)$.**

$$\frac{d^4}{dx^4}x^4 = 24 = 4!$$

**The only degree-4 polynomial surviving four differentiations is $x^4$, and what survives is $4!$.** $D^5 = 0$ because five derivatives kill everything of degree $\le 4$.

*Marking: 2 for the nilpotency, 2 for identifying the entry as $4!$ and saying what calculus fact it is.*

### (c) [10]

$$D = \begin{bmatrix}0&1&0&0\\ 0&0&2&0\\ 0&0&0&3\end{bmatrix} \ (3\times4), \qquad J = \begin{bmatrix}0&0&0\\ 1&0&0\\ 0&\tfrac12&0\\ 0&0&\tfrac13\end{bmatrix} \ (4\times3)$$

*(From $J(1) = x$, $J(x) = \tfrac{x^2}{2}$, $J(x^2) = \tfrac{x^3}{3}$.)*

$$DJ = \begin{bmatrix}1&0&0\\0&1&0\\0&0&1\end{bmatrix} = I_3 \qquad\qquad JD = \begin{bmatrix}\mathbf{0}&0&0&0\\ 0&1&0&0\\ 0&0&1&0\\ 0&0&0&1\end{bmatrix}$$

**$DJ = I$ is the Fundamental Theorem of Calculus, part 1:** $\dfrac{d}{dx}\displaystyle\int_0^x p(t)\,dt = p(x)$. Differentiating an antiderivative recovers the function exactly.

**$JD \ne I$ is part 2, and the discrepancy is the whole point:** $\displaystyle\int_0^x p'(t)\,dt = p(x) - p(0)$. **Integrating a derivative recovers the function only up to its value at $0$.**

**The single differing entry is $(1,1)$, which is $0$ instead of $1$** — the coordinate of the constant term. $JD$ **annihilates the constant** and leaves everything else alone.

> **That entry is the $+\,C$.** $\ker D$ is the constants (L13 §4), so $D$ destroys exactly one
> dimension of information and no right inverse can restore it. Every antiderivative is written with
> an arbitrary constant because **the matrix $JD$ has a zero in position $(1,1)$**, and the family of
> functions with a given derivative is $J D p + \ker D$ — Week 2's complete solution
> $x_p + \mathbf{N}(A)$, for the derivative operator.

*Marking: 3 for the two matrices with shapes, 3 for the two products, 2 for naming both theorems, 2 for the $+\,C$ explanation. **The last 2 are the question**; a student who computes both products and says nothing about the entry gets 6 of 10.*

---

## Q4: Change of Basis (24 points)

### (a) [4]

$$A = \begin{bmatrix}3&-1\\-1&3\end{bmatrix} \qquad(\text{standard basis})$$

### (b) [6]

$$T(u_1) = T(1,1) = (3-1,\ -1+3) = (2,2) = \mathbf{2}\,u_1$$
$$T(u_2) = T(1,-1) = (3+1,\ -1-3) = (4,-4) = \mathbf{4}\,u_2$$

Coordinates in the $u$-basis: $[T(u_1)]_u = (2,0)$ and $[T(u_2)]_u = (0,4)$, so

$$B = \begin{bmatrix}2&0\\0&4\end{bmatrix} \qquad(u\text{-basis})$$

**No inverse was computed.** *(Marking: full credit requires the multiples $2$ and $4$ stated explicitly.)*

### (c) [6]

$$M = \begin{bmatrix}1&1\\1&-1\end{bmatrix}, \qquad \det M = -2, \qquad M^{-1} = \tfrac12\begin{bmatrix}1&1\\1&-1\end{bmatrix}$$

$$M^{-1}AM = \tfrac12\begin{bmatrix}1&1\\1&-1\end{bmatrix}\begin{bmatrix}3&-1\\-1&3\end{bmatrix}\begin{bmatrix}1&1\\1&-1\end{bmatrix} = \begin{bmatrix}2&0\\0&4\end{bmatrix} = B\ ✓$$

**$M$ converts *new* coordinates to *old*.** Demonstration: $[v]_u = (1,0)$ means $v = u_1 = (1,1)$, and

$$M\begin{bmatrix}1\\0\end{bmatrix} = \begin{bmatrix}1\\1\end{bmatrix}\ ✓$$

*Marking: 3 for the verification, 3 for the direction **with a demonstration**. **The direction is the commonest error on the paper** — a script asserting it without checking gets 1 of the 3.*

### (d) [4]

$$T(5,1) = (3\cdot5 - 1,\ -5 + 3) = (14, -2)$$

**Coordinates of $(5,1)$ in the $u$-basis:** $c_1 + c_2 = 5$, $c_1 - c_2 = 1$, so $[v]_u = (3,2)$.

$$B\begin{bmatrix}3\\2\end{bmatrix} = \begin{bmatrix}6\\8\end{bmatrix} \;\longrightarrow\; 6u_1 + 8u_2 = 6(1,1) + 8(1,-1) = (14,-2)\ ✓$$

**They agree.**

### (e) [4]

$B$ diagonal means $T$ **acts independently along the two basis directions**, stretching $u_1$ by $2$ and $u_2$ by $4$ and mixing them not at all. Any vector decomposes as $c_1u_1 + c_2u_2$, and $T$ simply rescales each piece.

**What was special about $\{u_1, u_2\}$:** each is sent to a *multiple of itself*. $T$ does not rotate them into new directions — these are the two directions $T$ leaves invariant, and picking them as the basis is what removes the off-diagonal entries.

*(Any correct account. **Award full marks to a student who uses the word "eigenvector" without having been taught it** — several will, and they are right; note it. Week 6.)*

---

## Q5: Similarity (16 points)

### (a) [4]

**Reflexive:** $A = I^{-1}AI$.
**Symmetric:** $B = M^{-1}AM \Rightarrow A = MBM^{-1} = (M^{-1})^{-1}B(M^{-1})$.
**Transitive:** $B = M^{-1}AM$ and $C = N^{-1}BN$ give $C = N^{-1}M^{-1}AMN = (MN)^{-1}A(MN)$.

### (b) [4]

$$\operatorname{trace}(XY) = \sum_i (XY)_{ii} = \sum_i\sum_k x_{ik}y_{ki} = \sum_k\sum_i y_{ki}x_{ik} = \sum_k (YX)_{kk} = \operatorname{trace}(YX)$$

**Hence** $\operatorname{trace}(M^{-1}AM) = \operatorname{trace}\big((M^{-1})(AM)\big) = \operatorname{trace}\big((AM)(M^{-1})\big) = \operatorname{trace}(A)$. $\square$

*Marking: 2 for the swap of summation order, 2 for the application to similarity.*

### (c) [4]

| | trace | det | rank |
|---|---:|---:|---:|
| $A = \begin{bmatrix}3&-1\\-1&3\end{bmatrix}$ | $6$ | $9-1 = 8$ | $2$ |
| $B = \begin{bmatrix}2&0\\0&4\end{bmatrix}$ | $6$ | $8$ | $2$ |

**Which entries belong to $T$: none of them individually.** No single entry survives a change of basis — $A_{12} = -1$ became $0$. **What survives are certain *combinations*:** the sum of the diagonal, and $ad - bc$. The four numbers are four facts about the basis; trace and determinant are two facts about $T$.

*Marking: 2 for the table, 2 for the "no individual entry" answer. **A student who names an entry has missed it.***

### (d) [4]

**$I$ and $\begin{bmatrix}1&1\\0&1\end{bmatrix}$ are NOT similar.** For any invertible $M$,

$$M^{-1}IM = M^{-1}M = I.$$

**The identity is similar only to itself** — it is alone in its class. So nothing else, however matching its trace and determinant, can be similar to it.

**$\begin{bmatrix}1&0\\0&2\end{bmatrix}$ and $\begin{bmatrix}1&1\\0&2\end{bmatrix}$ ARE similar.** Take $M = \begin{bmatrix}1&-1\\0&1\end{bmatrix}$, $M^{-1} = \begin{bmatrix}1&1\\0&1\end{bmatrix}$:

$$M^{-1}\begin{bmatrix}1&0\\0&2\end{bmatrix}M = \begin{bmatrix}1&1\\0&1\end{bmatrix}\begin{bmatrix}1&0\\0&2\end{bmatrix}\begin{bmatrix}1&-1\\0&1\end{bmatrix} = \begin{bmatrix}1&1\\0&2\end{bmatrix}\ ✓$$

**What it shows:** trace, determinant and rank are **necessary but not sufficient** for similarity. Two pairs share all three and only one pair is similar, so no test built from those three can ever decide the question.

> *(The real distinction: both matrices in the second pair have distinct eigenvalues $1, 2$ and are
> diagonalisable, hence both similar to $\operatorname{diag}(1,2)$ and so to each other. The first
> pair has a repeated eigenvalue $1$, and $\begin{bmatrix}1&1\\0&1\end{bmatrix}$ has only a
> one-dimensional eigenspace — it is **not** diagonalisable. **Week 7.** Do not expect this
> vocabulary; award full marks for the $M^{-1}IM = I$ argument plus a valid $M$.)*

*Marking: 2 for the $I$ argument, 1 for a valid $M$, 1 for the conclusion about the three tests.*

---

## Grade Distribution Expected

| Band | Score | Description |
|---|---|---|
| Strong | 88–100 | Q3(c) with the $+\,C$ explained, Q4(b) done geometrically, Q5(d) both halves |
| Solid | 72–87 | Q2 and Q4 correct throughout; Q3(c) computed but not interpreted |
| Passing | 55–71 | Matrices built correctly; change of basis mechanical, direction of $M$ shaky |
| Concerning | < 55 | **$M$ the wrong way round in Q4(c), or Q2(a)(2) quoted rather than derived.** Weeks 7, 10 and 11 are all change of basis; a student who cannot do it here will not recover unaided. Help Desk before Week 5 |

---

*MATH 241 · Week 4 · PS 4 Solutions · © CSE Department*
