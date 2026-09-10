# MATH 241 · Problem Set 5 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**All exact arithmetic**; `resources/determinants.py` reproduces the Q2 and Q5 computations.

**What this paper is testing.** Q1 and Q2 are the mechanical core and should be near-full marks — **this is the last problem set before Midterm 1 and Q2 is the most likely exam question on the paper.** Q3(c) and Q5's closing warning are the two places where a correct computation has to be *rejected* as a method, which is the Week 5 idea that transfers. Q4(d) closes a loop back to MATH 142 and is the question strong students enjoy.

**Common failure modes:** (1) Q1(a)(1) answered $2\det A$ rather than $2^4\det A$; (2) Q2(c) expanded along the first row out of habit; (3) Q3(c) costed correctly and not answered — the question asks what Cramer's rule is *for*; (4) Q5's warning answered "the determinant is small so the matrix is nearly singular", which is the misconception the whole term has been correcting.

---

## Q1: The Properties (18 points)

### (a) [8] — $\det A = 3$, $A$ is $4\times4$

| | Value | Property |
|---|---|---|
| $\det(2A)$ | $2^4 \cdot 3 = \mathbf{48}$ | P3 applied to **each of the four rows** — $\det(cA) = c^n\det A$ |
| $\det(A^\mathsf{T})$ | $\mathbf{3}$ | L18 §3 |
| $\det(A^{-1})$ | $\mathbf{1/3}$ | product rule on $AA^{-1} = I$ |
| $\det(A^3)$ | $3^3 = \mathbf{27}$ | product rule |
| $\det(-A)$ | $(-1)^4\cdot 3 = \mathbf{3}$ | $c = -1$, and $n$ is even |
| $\det(M^{-1}AM)$ | $\mathbf{3}$ | similarity invariance, L18 §4 |

*Marking: 1 each, plus 2 for the properties being named. **$\det(2A) = 6$ is the error to look for** and it is worth a comment: P3 is linearity in **one row at a time**, so scaling the whole matrix costs a factor per row.*

### (b) [4]

**Two equal rows.** Let $d = \det A$ with rows $i$ and $j$ equal. Swapping them gives $-d$ by P2 — but the matrix is **unchanged**, so its determinant is still $d$. Hence $d = -d$, so $2d = 0$ and $d = 0$. $\square$

**Adding a multiple of a row.** Replace row $i$ by $\text{row}_i + c\,\text{row}_j$. By P3, linearity in row $i$ splits the determinant:

$$\det(\text{new}) = \det(A) + c\det(A \text{ with row}_i \text{ replaced by row}_j)$$

The second matrix has **two equal rows** (rows $i$ and $j$ are both $\text{row}_j$), so by the first part its determinant is $0$. Hence $\det(\text{new}) = \det A$. $\square$

*Marking: 2 each. **The second proof must invoke the first** — that is why the question says so.*

### (c) [3]

$$A = I = \begin{bmatrix}1&0\\0&1\end{bmatrix}, \quad B = -I, \qquad \det A + \det B = 1 + 1 = 2, \qquad \det(A+B) = \det 0 = 0$$

**P3 says the determinant is linear in each row *separately*, all other rows held fixed.** It says nothing about adding two whole matrices, which changes every row at once.

### (d) [3]

**Row 2 is twice row 1.** So the rows are dependent, and L16 §3(e) gives $\det = 0$ — or directly: subtracting $2\times$row 1 from row 2 leaves the determinant unchanged (part (b)) and produces a zero row.

---

## Q2: Computing Them (22 points)

### (a) [8]

$$P = \begin{bmatrix}2&1&0&1\\ 1&3&1&0\\ 0&1&2&1\\ 1&0&1&3\end{bmatrix}$$

Eliminating with no row exchanges gives pivots

$$2,\quad \tfrac52,\quad \tfrac85,\quad \tfrac32$$

$$\det P = 2 \cdot \tfrac52 \cdot \tfrac85 \cdot \tfrac32 = \boxed{12}$$

**No row exchanges, so no sign change.** *(Accept any correct elimination order; a student who exchanges must count the exchanges and get the sign right. Fractional pivots are expected and correct — a script that rounds them has left exact arithmetic.)*

*Marking: 5 for the pivots, 2 for the product, 1 for noting the exchange count.*

### (b) [6]

Cofactor expansion along any row or column gives $\boxed{12}$.

**Elimination is far less work.** Expanding a $4\times4$ needs four $3\times3$ determinants, each of which is six products — **24 multiply-heavy terms**, against elimination's handful of row operations. **Roughly a factor of 3–5 at $n = 4$**, and L17 §3's table shows the gap widening without limit.

*Marking: 4 for the correct value by cofactors with working shown, 2 for a defensible comparison. **Accept any reasonable estimate of the ratio**; the point is that they noticed which was shorter, not that they counted precisely.*

### (c) [4]

$$\begin{bmatrix}3&0&0&2\\ 0&5&1&0\\ 0&2&4&0\\ 1&0&0&4\end{bmatrix}$$

**Expand along row 2 or row 3, or column 2 or column 3** — each has two zeros. Taking **column 1** (entries $3, 0, 0, 1$) is also good.

Cleanest: the matrix is **block diagonal after reordering** — rows/columns $\{1,4\}$ interact only with each other, and $\{2,3\}$ likewise:

$$\det = \det\begin{bmatrix}3&2\\1&4\end{bmatrix}\cdot\det\begin{bmatrix}5&1\\2&4\end{bmatrix} = 10 \times 18 = \boxed{180}$$

*Marking: 2 for the value, 2 for **stating the choice and the reason before computing** — the question asks for it. A student who expands along the first row gets the right answer with four times the work; award 2.*

### (d) [4]

$$\det = 2 \times 3 \times 4 = \boxed{24}$$

**Entitled because** L16 §4: the determinant is the product of the pivots, times $-1$ per row exchange, and Week 1's elimination used **no** exchanges. **The work was done in Week 1 and nobody multiplied the three numbers together.**

*Marking: 2 for the value, 2 for the justification including the no-exchanges point.*

---

## Q3: Cofactors, the Adjugate, and Cramer (20 points)

### (a) [8]

$$C = \begin{bmatrix}1&2&3\\ 0&1&4\\ 5&6&0\end{bmatrix}, \qquad \det C = 1(0-24) - 2(0-20) + 3(0-5) = -24 + 40 - 15 = \boxed{1}$$

$$\operatorname{adj}C = \begin{bmatrix}-24&18&5\\ 20&-15&-4\\ -5&4&1\end{bmatrix}$$

Verification, $C\cdot\operatorname{adj}C$: row 1 gives $(-24 + 40 - 15,\ 18 - 30 + 12,\ 5 - 8 + 3) = (1, 0, 0)$ ✓, and similarly for rows 2 and 3, giving $I = (\det C)I$ ✓

**Why $C^{-1}$ is an integer matrix:** $\operatorname{adj}C$ has integer entries whenever $C$ does — every entry is $\pm$ a determinant of an integer submatrix — and $C^{-1} = \frac{1}{\det C}\operatorname{adj}C$. **Since $\det C = 1$, no division occurs.** *(PS 3 Q3(a): the criterion is exactly $\det = \pm1$, and such matrices are called unimodular.)*

*Marking: 2 for $\det C$, 4 for the adjugate (partial credit per correct row), 1 for the verification, 1 for the integrality argument. **Watch the transpose**: $\operatorname{adj}$ is the transpose of the cofactor matrix, and forgetting it gives a matrix that fails the verification — which is why the verification is asked for.*

### (b) [6]

$$A = \begin{bmatrix}2&-1&3\\ 1&4&-2\\ 3&1&5\end{bmatrix}, \qquad b = \begin{bmatrix}-3\\ 11\\ 0\end{bmatrix}, \qquad \det A = 22$$

| | Matrix | Determinant | $x_j$ |
|---|---|---:|---:|
| $A_1$ | $b$ in column 1 | $22$ | $22/22 = \mathbf{1}$ |
| $A_2$ | $b$ in column 2 | $44$ | $44/22 = \mathbf{2}$ |
| $A_3$ | $b$ in column 3 | $-22$ | $-22/22 = \mathbf{-1}$ |

$$x = (1, 2, -1)$$

Check in the original: $2 - 2 - 3 = -3$ ✓, $1 + 8 + 2 = 11$ ✓, $3 + 2 - 5 = 0$ ✓

*Marking: 4 for the four determinants, 2 for the answer with a check.*

### (c) [6]

- **$n+1$ determinants** — one for $\det A$ and one per unknown.
- **By elimination:** $(n+1)\cdot n^3/3$ against a single solve's $n^3/3$. **A factor of $n+1$ for the same answer.**
- **By cofactors at $n = 20$:** each is $20! = 2.43\times10^{18}$ terms, so **77 years each, times 21 — about 1,600 years.**

**What Cramer's rule is for:** it exhibits each $x_j$ as an explicit **ratio of polynomials in the entries of $A$ and $b$**, which proves that the solution depends smoothly (indeed rationally) on the data. **That is a theoretical statement, useful in proofs and in symbolic computation, and it has never been a way to obtain a number.**

*Marking: 1, 2, 1, and **2 for the final question**, which most scripts will skip. Accept any answer identifying the closed form / smooth dependence / symbolic use as the point.*

---

## Q4: Volume (20 points)

### (a) [4]

$$\det\begin{bmatrix}3&1\\1&4\end{bmatrix} = 12 - 1 = 11 \qquad\Rightarrow\qquad \text{area} = 11$$

Swapping the edges gives $\det\begin{bmatrix}1&3\\4&1\end{bmatrix} = 1 - 12 = -11$.

**The area is unchanged; the sign flipped.** The sign is **orientation** — swapping the two edges reverses the sense in which the parallelogram is traversed. **Area is $\lvert\det\rvert$; the determinant carries one extra bit of information.**

### (b) [4]

$$\det\begin{bmatrix}1&0&2\\ 0&3&1\\ 2&1&0\end{bmatrix} = 1(0-1) - 0(0-2) + 2(0-6) = -1 - 12 = -13 \qquad \text{volume} = \boxed{13}$$

### (c) [6]

| | $\det$ | Effect on area |
|---|---:|---|
| $\begin{bmatrix}1&5\\0&1\end{bmatrix}$ | $1$ | **preserved** — a shear |
| $\begin{bmatrix}0&-1\\1&0\end{bmatrix}$ | $1$ | preserved — a rotation, rigid |
| $\begin{bmatrix}2&0\\0&\tfrac12\end{bmatrix}$ | $1$ | preserved — stretched one way, compressed the other, exactly compensating |
| $\begin{bmatrix}1&2\\2&4\end{bmatrix}$ | $0$ | **destroyed** — the plane collapses to a line *(the columns are dependent)* |

**The shear is the first.** It maps the unit square to a parallelogram with the **same base** (the bottom edge $e_1$ is fixed) and the **same height** (the top edge stays at $y = 1$, merely slid sideways by 5). **Area is base times height**, so the area is unchanged and the determinant must be 1.

*Marking: 1 each for the four, 2 for the base-and-height argument. **Three of the four have determinant 1 by different mechanisms** — worth a comment on any script that notices.*

### (d) [6]

$$J = \begin{bmatrix}\partial x/\partial r & \partial x/\partial\theta\\ \partial y/\partial r & \partial y/\partial\theta\end{bmatrix} = \begin{bmatrix}\cos\theta & -r\sin\theta\\ \sin\theta & r\cos\theta\end{bmatrix}$$

$$\det J = r\cos^2\theta + r\sin^2\theta = r(\cos^2\theta + \sin^2\theta) = \boxed{r}$$

**Why $dA = r\,dr\,d\theta$ is this week's theorem:** a change of variables is, at each point, approximately a **linear** map — its derivative — and L18 §1 says a linear map scales area by $\lvert\det\rvert$. So the area element picks up exactly $\lvert\det J\rvert$, which here is $r$: **a small polar rectangle far from the origin is genuinely bigger than one near it**, by the factor $r$.

**Why the absolute value:** area is positive, and orientation is not the integral's concern. The sign of $\det J$ records whether the coordinate change flips the plane, which affects nothing about how much area there is.

*Marking: 3 for the Jacobian, 3 for the two explanations. **This is the question strong students enjoy** — note any script that connects it back to MATH 142 unprompted.*

---

## Q5: The Product Rule (20 points)

### (a) [4]

$AA^{-1} = I$, so $\det A \cdot \det(A^{-1}) = \det I = 1$, hence $\det(A^{-1}) = 1/\det A$. $\square$

**Deduction:** if $\det A = 0$ then no $B$ can satisfy $\det A \cdot \det B = 1$, since the left side is $0$. **So a matrix with zero determinant has no inverse** — which re-proves **characterisation 7** of Week 1's L05 §2, now from the product rule rather than from the pivot count.

### (b) [4]

$$\det(M^{-1}AM) = \det(M^{-1})\det(A)\det(M) = \frac{1}{\det M}\cdot\det A\cdot\det M = \det A \qquad\square$$

*(Using (a) and the commutativity of multiplying **numbers** — the matrices do not commute, and they do not need to.)*

### (c) [4] — $3\times3$, $\det A = 4$, $\det B = -2$

| | |
|---|---|
| $\det(AB)$ | $4 \times (-2) = \mathbf{-8}$ |
| $\det(BA)$ | $\mathbf{-8}$ — the same, though $AB \ne BA$ |
| $\det(A^\mathsf{T}B)$ | $\det(A^\mathsf{T})\det B = 4\times(-2) = \mathbf{-8}$ |
| $\det(2AB^{-1})$ | $2^3\cdot 4 \cdot \tfrac{1}{-2} = \mathbf{-16}$ |

*Marking: 1 each. **The last is the discriminating one** — it needs $2^n$ with $n = 3$, not $2$.*

### (d) [4]

$Q^\mathsf{T}Q = I$, so taking determinants:

$$\det(Q^\mathsf{T})\det(Q) = 1 \quad\Longrightarrow\quad (\det Q)^2 = 1 \quad\Longrightarrow\quad \det Q = \pm1$$

using $\det(Q^\mathsf{T}) = \det Q$. $\square$

**$+1$: a rotation** — a rigid motion preserving orientation. **$-1$: a reflection** (or a rotation composed with one) — rigid, and orientation-reversing.

*Marking: 2 for the proof, 1 per sign interpreted.*

### (e) [4]

**False.** $I$ and $\begin{bmatrix}1&1\\0&1\end{bmatrix}$ both have determinant $1$, and PS 4 Q5(d) showed they are **not** similar: $M^{-1}IM = I$ for every $M$, so the identity is similar to nothing but itself.

**Equal determinants are necessary, not sufficient.** *(Nor are trace, determinant and rank together — the same PS 4 question exhibited a pair sharing all three that **is** similar and a pair that is not.)*

### The closing warning [within the 20]

Every entry about $0.1$, size $1000$. The determinant is a sum of products of $1000$ entries each, so its magnitude is around $10^{-1000}$.

**A `double` holds down to about $10^{-308}$.** The determinant **underflows to exactly $0.0$**, and `if det(A) != 0:` reports the matrix singular. **It is not** — it is perfectly well conditioned by hypothesis.

**The cause:** $\det$ is not scale-invariant. $\det(cA) = c^n\det A$, so the determinant of a large matrix is dominated by the *scale* of its entries and says almost nothing about its invertibility.

**What to compute instead:** $\operatorname{cond}(A) = \lVert A\rVert\lVert A^{-1}\rVert$, which **is** scale-invariant, and which bounds the relative error of a solve. *(Week 0's L03 §7.)*

*Marking: 4 — 1 for the magnitude, 1 for underflow, 1 for the scale-invariance diagnosis, 1 for naming the condition number. **A script answering "the determinant is small, so it is nearly singular" gets 0 for this part** and should be told plainly: that is the misconception Weeks 0 and 5 have both been correcting, and it will be on the midterm.*

---

## Grade Distribution Expected

| Band | Score | Description |
|---|---|---|
| Strong | 88–100 | Q3(c)'s "what is it for", Q4(d)'s two explanations, the closing warning diagnosed by scale-invariance |
| Solid | 72–87 | Q1, Q2, Q4(a)–(c), Q5(a)–(d) correct; the interpretive parts thin |
| Passing | 55–71 | Determinants computed correctly by at least one method |
| Concerning | < 55 | **$\det(2A) = 2\det A$, or "small determinant means nearly singular".** Both are on the midterm. Help Desk before Wednesday — this paper is due two days after it |

---

*MATH 241 · Week 5 · PS 5 Solutions · © CSE Department*
