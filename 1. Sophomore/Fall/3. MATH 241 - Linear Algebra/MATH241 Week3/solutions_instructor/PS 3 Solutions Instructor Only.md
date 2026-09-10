# MATH 241 · Problem Set 3 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**All exact arithmetic**; `resources/dimension.py` reproduces the four-subspace computation if a script needs checking.

**What this paper is testing.** Q3(b) is the mechanical core and must be right — a student who cannot produce four bases with the correct ambient spaces is not ready for Week 8. **Q3(b)'s "why the two recipes differ" and Q5(b) are the conceptual core.** Q4 is the payoff of Week 2's loose end and the best question on the paper. Q5(d) is Week 9's foundation stated three times now (PS 2 Q5(c), L12 exercise 7, here) and should be free marks by this point — if it is not, that is the signal.

**Common failure modes:** (1) row-space basis taken from the rows of $P$ rather than of $\operatorname{rref}(P)$ — *not* wrong, but usually unjustified, see the note in (b); (2) column-space basis taken from $\operatorname{rref}$; (3) ambient spaces swapped; (4) Q5(b) answered by restating the theorem instead of saying why it is surprising.

---

## Q1: Independence (18 points)

### (a) [6] — 1.5 each

**1. Dependent.** $\;v_1 + v_2 - v_3 = 0$, i.e. $(1,2,1) + (2,1,3) = (3,3,4)$ ✓ *(rank 2, nullity 1)*

**2. Independent.** Rank 3, $\mathbf{N} = \{0\}$. *(Or: the determinant is $-2 \ne 0$.)*

**3. Dependent, with no computation.** **Three vectors in $\mathbb{R}^2$**, and $k > n$ forces dependence — L10 §4. *(A student who eliminates has answered correctly and missed the instruction; award 1 of 1.5.)*

**4. Independent.** If $c_1 + c_2(x-1) + c_3(x-1)^2 = 0$ as a polynomial, substitute $x = 1$ to get $c_1 = 0$; differentiate and substitute to get $c_2 = 0$; then $c_3 = 0$. *(Or: they have degrees $0, 1, 2$, so no combination of the lower ones can produce the leading term of a higher one.)*

### (b) [4]

**Counterexample:** $(1,0),\ (0,1),\ (1,1)$ in $\mathbb{R}^2$. No one is a multiple of another, and $(1,0) + (0,1) - (1,1) = 0$.

**The definition requires** that the *only* combination $c_1v_1 + \dots + c_kv_k$ equal to $0$ is the one with every $c_i = 0$ — **a statement about all combinations, not about pairs.**

*Marking: 2 for the example, 2 for the correct statement. **Any three vectors in $\mathbb{R}^2$ pairwise non-parallel will do.***

### (c) [4]

Suppose $c_1v_1 + c_2(v_1+v_2) + c_3(v_1+v_2+v_3) = 0$. Collect:

$$(c_1+c_2+c_3)v_1 + (c_2+c_3)v_2 + c_3v_3 = 0$$

Independence of $v_1,v_2,v_3$ forces each coefficient to zero: $c_3 = 0$, then $c_2 = 0$, then $c_1 = 0$. $\square$

*Marking: 2 for collecting correctly, 2 for the back-substitution. **The order matters** — solving from $c_3$ upward is the whole argument.*

### (d) [4]

Say $v_1 = 0$. Then $1\cdot v_1 + 0v_2 + \dots + 0v_k = 0$, and the coefficient on $v_1$ is $1 \ne 0$. **A nontrivial combination giving $0$: dependent.** $\square$

**A basis must be independent**, so it can never contain $0$. *(Also worth noting: the empty list is independent vacuously, which is why $\dim\{0\} = 0$ works.)*

---

## Q2: Basis and Dimension (20 points)

### (a) [5]

The plane is $\mathbf{N}\big([\,2\;\; -1\;\; 3\,]\big)$ — **a null space, so the special-solution algorithm applies.** The matrix is already in rref with pivot column 1, free columns 2 and 3:

$$s_2 = (\tfrac12, 1, 0), \qquad s_3 = (-\tfrac32, 0, 1) \quad\longrightarrow\quad \text{clear fractions: } (1,2,0),\ (-3,0,2)$$

**Basis $\{(1,2,0),\ (-3,0,2)\}$, dimension 2.** Check: $2(1)-2+0 = 0$ ✓ and $-6-0+6 = 0$ ✓

*Accept any correct pair. Marking: 3 for a valid basis, 1 for dimension 2, 1 for naming it as a null-space computation.*

### (b) [5]

**Symmetric $2\times2$:** $\begin{bmatrix}a&b\\b&c\end{bmatrix}$, basis $\begin{bmatrix}1&0\\0&0\end{bmatrix}, \begin{bmatrix}0&0\\0&1\end{bmatrix}, \begin{bmatrix}0&1\\1&0\end{bmatrix}$, **dimension 3.**

**Trace zero:** $\begin{bmatrix}a&b\\c&-a\end{bmatrix}$, basis $\begin{bmatrix}1&0\\0&-1\end{bmatrix}, \begin{bmatrix}0&1\\0&0\end{bmatrix}, \begin{bmatrix}0&0\\1&0\end{bmatrix}$, **dimension 3.**

**Intersection** — symmetric *and* traceless: $\begin{bmatrix}a&b\\b&-a\end{bmatrix}$, basis $\begin{bmatrix}1&0\\0&-1\end{bmatrix}, \begin{bmatrix}0&1\\1&0\end{bmatrix}$, **dimension 2.**

*Marking: 1.5 each for the first two, 2 for the intersection with a basis. **Note $3 + 3 - 2 = 4 = \dim\mathbb{R}^{2\times2}$** — worth remarking on any strong script, as it is the dimension formula for $U + W$ that Week 3 does not formally cover.*

### (c) [4]

$\dim\mathbb{R}^3 = 3$ and the list has **exactly 3** vectors, so **L11 §8 applies: independence alone suffices.**

$$\det\begin{bmatrix}1&0&1\\1&1&0\\0&1&1\end{bmatrix} = 1(1) - 0 + 1(1) = 2 \ne 0 \quad\Rightarrow\quad \text{independent} \Rightarrow \textbf{basis}$$

*(Or eliminate: three pivots.)* **Spanning comes free** because an independent list of $k$ vectors in a $k$-dimensional space that failed to span could be extended to a longer independent list, exceeding a spanning list of size $k$ — contradicting L11 §4's lemma.

*Marking: 2 for checking one condition, 2 for correctly stating why the other is free. **A script that checks both conditions has ignored the instruction; award 2.***

### (d) [6]

- **5 vectors cannot span $V$.** If they did, then any independent list would have at most 5 vectors (L11 §4's lemma) — but a basis has 6 and is independent. Contradiction.
- **7 vectors cannot be independent.** A basis of 6 spans, so an independent list has at most 6.
- **$U = V$:** take a basis of $U$ — 6 independent vectors, lying in $V$. By L11 §8, 6 independent vectors in a 6-dimensional space form a basis for $V$, so they span $V$; but they lie in $U$ and $U$ is a subspace, so $V = \operatorname{span} \subseteq U \subseteq V$. $\square$
- **A 2-dimensional subspace of $\mathbb{P}_3$:** e.g. $\operatorname{span}\{1, x\}$, the polynomials of degree $\le 1$. *(Or $\{p : p(0) = p(1) = 0\} = \operatorname{span}\{x^2-x,\ x^3-x\}$, which is a better answer.)*

*Marking: 1, 1, 2, 2.*

---

## Q3: The Four Subspaces (26 points)

### (a) [4]

$$P = \begin{bmatrix}1&2&0&1&3\\ 2&4&1&4&8\\ 0&0&1&2&2\\ 1&2&1&3&5\end{bmatrix} \longrightarrow \operatorname{rref}(P) = \begin{bmatrix}1&2&0&1&3\\ 0&0&1&2&2\\ 0&0&0&0&0\\ 0&0&0&0&0\end{bmatrix}$$

**Rank $r = 2$. Pivot columns 1 and 3; free columns 2, 4 and 5.** $m = 4$, $n = 5$.

### (b) [12] — 3 per subspace

| Subspace | Lives in | $\dim$ | Basis |
|---|---|---:|---|
| $\mathbf{C}(P)$ | $\mathbb{R}^4$ | $r = 2$ | $(1,2,0,1),\ (0,1,1,1)$ — **columns 1 and 3 of $P$** |
| $\mathbf{N}(P)$ | $\mathbb{R}^5$ | $n-r = 3$ | $(-2,1,0,0,0),\ (-1,0,-2,1,0),\ (-3,0,-2,0,1)$ |
| $\mathbf{C}(P^\mathsf{T})$ | $\mathbb{R}^5$ | $r = 2$ | $(1,2,0,1,3),\ (0,0,1,2,2)$ — **nonzero rows of $\operatorname{rref}(P)$** |
| $\mathbf{N}(P^\mathsf{T})$ | $\mathbb{R}^4$ | $m-r = 2$ | $(2,-1,1,0),\ (1,-1,0,1)$ |

**Why the recipes differ.** Elimination **combines rows**, so the row space is unchanged and a basis can be read straight off $\operatorname{rref}$; it **moves every column**, so the column space is not preserved and the basis must be read back from $P$ at the pivot positions. *(L12 §3.)*

*Marking: 2 for each basis, 1 for each ambient space and dimension, and the "why" sentence is required for full credit on the row/column pair. **Deduct 3 for a column-space basis taken from $\operatorname{rref}$.** A row-space basis taken from the rows of $P$ itself is **not wrong** — rows 1 and 2 of $P$ are independent and span the row space — but it needs the argument that they are independent, which most scripts will not give; award 2 of 3 and note it.*

### (c) [4]

$$r + (n-r) = 2 + 3 = 5 = n \ ✓ \qquad\qquad r + (m-r) = 2 + 2 = 4 = m \ ✓$$

*The pair in $\mathbb{R}^5$ adds to 5; the pair in $\mathbb{R}^4$ adds to 4. Marking: 2 each.*

### (d) [6]

**$3 \times 2 + 2 \times 2 = 10$ dot products.**

$\mathbf{N}(P)$ against the row space:

| | $(1,2,0,1,3)$ | $(0,0,1,2,2)$ |
|---|---:|---:|
| $(-2,1,0,0,0)$ | $0$ | $0$ |
| $(-1,0,-2,1,0)$ | $0$ | $0$ |
| $(-3,0,-2,0,1)$ | $0$ | $0$ |

$\mathbf{N}(P^\mathsf{T})$ against $\mathbf{C}(P)$:

| | $(1,2,0,1)$ | $(0,1,1,1)$ |
|---|---:|---:|
| $(2,-1,1,0)$ | $0$ | $0$ |
| $(1,-1,0,1)$ | $0$ | $0$ |

**All ten zero.**

*Marking: 4 for the computations, 2 for the count of 10 stated explicitly. **Spot-check two or three entries rather than all ten.***

---

## Q4: What the Left Null Space Is For (18 points)

### (a) [5]

$\dim\mathbf{N}(P^\mathsf{T}) = m - r = 2$, so **two independent conditions.** From the basis:

$$y_1 = (2,-1,1,0): \quad \boxed{2b_1 - b_2 + b_3 = 0}$$
$$y_2 = (1,-1,0,1): \quad \boxed{b_1 - b_2 + b_4 = 0}$$

*Marking: 2 for the count with justification, 3 for the two equations.*

### (b) [4]

| $b$ | $2b_1 - b_2 + b_3$ | $b_1 - b_2 + b_4$ | Solvable? |
|---|---:|---:|---|
| $(7,19,5,12)$ | $14-19+5 = 0$ | $7-19+12 = 0$ | **yes** |
| $(7,19,5,13)$ | $0$ | $7-19+13 = 1$ | **no** |
| $(0,0,0,0)$ | $0$ | $0$ | **yes** — $x = 0$ |

> **Note the middle row satisfies the *first* condition and fails the second.** Worth remarking on
> scripts: with $m - r = 2$ there are two independent ways to be unreachable, and failing either is
> enough. A student who checks only one condition gets this row wrong.

*Marking: 1 per verdict, 1 for showing both conditions on the middle row.*

### (c) [5]

$b = (7,19,5,12)$.

$$[\,P \mid b\,] \longrightarrow \left[\begin{array}{ccccc|c}1&2&0&1&3&7\\ 0&0&1&2&2&5\\ 0&0&0&0&0&0\\ 0&0&0&0&0&0\end{array}\right]$$

Free variables to zero: $x_1 = 7$, $x_3 = 5$.

$$x_p = (7,0,5,0,0), \qquad Px_p = 7(1,2,0,1) + 5(0,1,1,1) = (7,14,0,7)+(0,5,5,5) = (7,19,5,12)\ ✓$$

$$x = (7,0,5,0,0) + t(-2,1,0,0,0) + u(-1,0,-2,1,0) + w(-3,0,-2,0,1)$$

*(Sanity: $t = u = w = 1$ gives $(1,1,1,1,1)$, and $P$ times the all-ones vector is indeed $b$.)*

*Marking: 2 for $x_p$, 1 for the check against $P$, 2 for the complete set with all three parameters.*

### (d) [4]

If $Ax = b$ and $A^\mathsf{T}y = 0$, then

$$y^\mathsf{T}b = y^\mathsf{T}(Ax) = (y^\mathsf{T}A)x = (A^\mathsf{T}y)^\mathsf{T}x = 0^\mathsf{T}x = 0. \qquad \square$$

**The converse** — that satisfying every such condition *guarantees* solvability — needs $\mathbf{C}(A)$ to be **everything orthogonal to $\mathbf{N}(A^\mathsf{T})$**, not merely contained in it. That is the orthogonal-complement statement, **Week 8**.

*Marking: 2 for the computation, 2 for correctly identifying what the converse needs. **A script that claims the converse is also proved here has missed the point; award 2.***

---

## Q5: Rank (18 points)

### (a) [5]

$m = 6$, $n = 4$, $r = 4$ — **full column rank.**

| | $\dim$ | |
|---|---:|---|
| $\mathbf{C}(A) \subseteq \mathbb{R}^6$ | $4$ | |
| $\mathbf{N}(A) \subseteq \mathbb{R}^4$ | $0$ | $= \{0\}$ |
| $\mathbf{C}(A^\mathsf{T}) \subseteq \mathbb{R}^4$ | $4$ | all of $\mathbb{R}^4$ |
| $\mathbf{N}(A^\mathsf{T}) \subseteq \mathbb{R}^6$ | $2$ | |

**Not solvable for every $b$**: $\mathbf{C}(A)$ is a 4-dimensional subspace of $\mathbb{R}^6$, and $\dim\mathbf{N}(A^\mathsf{T}) = 2$ gives two conditions on $b$. **When solvable, the solution is unique**, because $\mathbf{N}(A) = \{0\}$.

*Marking: 3 for the four dimensions, 1 for each answer.*

### (b) [4]

**Why surprising** — any reasonable version of: the columns are $n$ vectors in $\mathbb{R}^m$ and the rows are $m$ vectors in $\mathbb{R}^n$; **different vectors, different counts of them, different ambient spaces**, and there is no evident reason a maximal independent subset of one should match a maximal independent subset of the other. For $P$: 5 columns in $\mathbb{R}^4$ and 4 rows in $\mathbb{R}^5$, both giving 2.

**The proof:** elimination yields $r$ pivots; the nonzero rows of $\operatorname{rref}$ are $r$ independent vectors spanning the row space, and the pivot columns of $A$ are $r$ independent vectors spanning the column space. Both dimensions are the pivot count, hence equal.

**What it does not explain:** it routes both counts through one algorithm and concludes they agree because that algorithm produced one number. **It gives no reason intrinsic to $A$.** Week 11's SVD does — $r$ is the number of nonzero singular values, defined without reference to rows, columns or elimination.

*Marking: 2 for a genuine account of the surprise, 1 for the proof, 1 for the limitation. **A script that only restates the theorem gets 1.***

### (c) [4]

**$\operatorname{rank}(A^\mathsf{T}) = \operatorname{rank}(A)$:** by L12 §3, $\operatorname{rank}(A) = \dim\mathbf{C}(A) = \dim\mathbf{C}(A^\mathsf{T})$, and $\mathbf{C}(A^\mathsf{T})$ is by definition the column space of $A^\mathsf{T}$, whose dimension is $\operatorname{rank}(A^\mathsf{T})$. $\square$

**$\operatorname{rank}(AB) \le \min(\operatorname{rank}A, \operatorname{rank}B)$:**

$\mathbf{C}(AB) \subseteq \mathbf{C}(A)$ (PS 2 Q5(a)) gives $\operatorname{rank}(AB) \le \operatorname{rank}(A)$.

For the other half, $(AB)^\mathsf{T} = B^\mathsf{T}A^\mathsf{T}$, so
$$\operatorname{rank}(AB) = \operatorname{rank}(B^\mathsf{T}A^\mathsf{T}) \le \operatorname{rank}(B^\mathsf{T}) = \operatorname{rank}(B). \qquad \square$$

*Marking: 1 for the transpose rank, 3 for the two halves. **The transpose trick is the point of the question**; a student who proves only the first half gets 2.*

### (d) [5]

- **$\operatorname{rank}(A^\mathsf{T}A) = 4$.** PS 2 Q5(c) gives $\mathbf{N}(A^\mathsf{T}A) = \mathbf{N}(A) = \{0\}$ since $A$ has full column rank; so $A^\mathsf{T}A$ has trivial null space, and by rank–nullity on a $4\times4$ matrix its rank is $4$.
- **$A^\mathsf{T}A$ is $4\times4$** — the $10^6$ has vanished — **and it is invertible**, being square with trivial null space (Week 1's L05 §2).
- **Why least squares is possible:** the normal equations $A^\mathsf{T}A\hat x = A^\mathsf{T}b$ reduce a million-row problem with no exact solution to **a $4\times4$ solve with a unique one**, and the reduction costs one matrix product. *(Week 9.)*

*Marking: 2, 1, 2. **This is the third time this fact has appeared** — PS 2 Q5(c), L12 exercise 7, here. A student still shaky on it should be flagged before Week 9.*

---

## Grade Distribution Expected

| Band | Score | Description |
|---|---|---|
| Strong | 88–100 | Q3(b) with the recipe justification, Q5(b)'s account of the surprise, Q5(c)'s transpose trick |
| Solid | 72–87 | All four bases right with correct ambient spaces; Q5(b) proved but not motivated |
| Passing | 55–71 | Q3 mechanically right; Q4 and Q5 thin |
| Concerning | < 55 | **A column-space basis taken from $\operatorname{rref}$, or ambient spaces swapped in Q3(b).** Week 8 is orthogonal complements of exactly these four spaces and is unsurvivable without them. Help Desk immediately |

---

*MATH 241 · Week 3 · PS 3 Solutions · © CSE Department*
