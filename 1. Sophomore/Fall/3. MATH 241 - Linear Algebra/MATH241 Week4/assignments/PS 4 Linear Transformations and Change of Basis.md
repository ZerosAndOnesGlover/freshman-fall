# MATH 241 · Problem Set 4
## Linear Transformations and Change of Basis

---

**Released:** Week 4, Wednesday · **Due:** Week 5, **Friday 17:00**
**Total: 100 points** · Submit one PDF, `PS4_{LastName}_{StudentID}.pdf`

> **Exact arithmetic throughout.** Where an angle forces a surd, leave it as one.
>
> **Every matrix answer must say which basis it is written in.** From this week on, a column of
> numbers with no stated basis is an incomplete answer.
>
> **Derive the rotation matrix; do not quote it.** Where does $e_1$ go, where does $e_2$ go.
>
> **Recitation 4 is the Thursday before this is due**, 15:00–15:50, SSB 108.

---

### Q1: Linear or Not (18 points)

**(a) [10]** Decide whether each is a linear transformation. **For each failure, give the specific vectors or scalar that break it**, and say which of the two conditions fails.

1. $T(x,y) = (3x - y,\; x)$
2. $T(x,y) = (x + 2,\; y)$
3. $T(x,y) = (xy,\; x+y)$
4. $T(A) = A + A^\mathsf{T}$ on $\mathbb{R}^{2\times2}$
5. $T(A) = \det A$ on $\mathbb{R}^{2\times2}$

**(b) [4]** $T(v) = Av + b$ with $b \ne 0$ is **affine**, not linear. Show it fails, then show that

$$\widetilde{T}\begin{bmatrix}v\\1\end{bmatrix} = \begin{bmatrix}A & b\\ 0 & 1\end{bmatrix}\begin{bmatrix}v\\1\end{bmatrix}$$

**is** linear and reproduces $T$ on the plane $w = 1$. **State in one sentence why every 3-D graphics API uses $4\times4$ matrices.**

**(c) [4]** Prove that $T$ is injective **iff** $\ker T = \{0\}$, from the definitions of *injective* and *linear*. **Both directions.**

---

### Q2: Building the Matrix (22 points)

**(a) [8]** Give the standard matrix of each, by computing $T(e_1)$ and $T(e_2)$. **Show both images.**

1. reflection across the $y$-axis
2. rotation by $45°$ anticlockwise
3. projection onto the $x$-axis
4. the shear $(x,y) \mapsto (x + 3y,\; y)$

**(b) [6]** Let $F$ = reflect across $y = x$ and $R$ = rotate by $90°$ anticlockwise.

- Compute the matrices of $R \circ F$ and $F \circ R$.
- **They are different.** Identify each as a familiar transformation, and describe geometrically why the order matters.

**(c) [4]** $T : \mathbb{R}^3 \to \mathbb{R}^2$ has $T(e_1) = (1,2)$, $T(e_2) = (0,-1)$, $T(e_3) = (3,3)$. Write the matrix, give $\ker T$ and the range, and check rank–nullity.

**(d) [4]** $T : \mathbb{R}^2 \to \mathbb{R}^2$ is linear with $T(1,1) = (4,4)$ and $T(1,-1) = (0,0)$.

- Write its matrix **in the basis $\{(1,1),(1,-1)\}$**, directly from L14 §1.
- **Then** find the standard matrix. *(You may use L15's formula, or solve for $T(e_1)$ and $T(e_2)$ directly — say which you did.)*

---

### Q3: Calculus as a Matrix (20 points)

**(a) [6]** Write the matrix of $D : \mathbb{P}_4 \to \mathbb{P}_4$, $D(p) = p'$, in the basis $1, x, x^2, x^3, x^4$. Give its rank and nullity, identify $\ker D$ and the range, and check rank–nullity.

**(b) [4]** Show $D^5 = 0$ but $D^4 \ne 0$. **What single entry survives in $D^4$, and what calculus fact is it?**

**(c) [10]** Now let

$$D : \mathbb{P}_3 \to \mathbb{P}_2 \quad (p \mapsto p'), \qquad J : \mathbb{P}_2 \to \mathbb{P}_3 \quad \Big(p \mapsto \int_0^x p(t)\,dt\Big).$$

- Write both matrices, with their shapes. *(Use $1,x,x^2$ and $1,x,x^2,x^3$.)*
- Compute $DJ$ and $JD$.
- **One is the identity and one is not.** Say which, and state the two theorems of calculus involved.
- **$JD$ differs from the identity in exactly one place.** Identify it, and explain in one sentence why every antiderivative is written with a $+\,C$.

---

### Q4: Change of Basis (24 points)

Let $T(x,y) = (3x - y,\; -x + 3y)$, and let $u_1 = (1,1)$, $u_2 = (1,-1)$.

**(a) [4]** Write $A$, the matrix of $T$ in the standard basis.

**(b) [6]** Compute $T(u_1)$ and $T(u_2)$. **Each is a multiple of the vector you started with** — say which multiple. Use L14 §1 to write $B$, the matrix of $T$ in the $u$-basis, **without computing any inverse.**

**(c) [6]** Now verify by the formula: write $M$, compute $M^{-1}$, and check $B = M^{-1}AM$. **State which direction $M$ converts** — new coordinates to old, or old to new — and demonstrate it on one vector.

**(d) [4]** Find the coordinates of $(5,1)$ in the $u$-basis. Then compute $T(5,1)$ two ways: with $A$ in standard coordinates, and with $B$ in $u$-coordinates followed by conversion back. **The answers must agree.**

**(e) [4]** $B$ is diagonal. **In one paragraph, say what that means about $T$ geometrically**, and what was special about the basis $\{u_1, u_2\}$ that made it happen. *(You are describing eigenvectors. Week 6 names them.)*

---

### Q5: Similarity (16 points)

**(a) [4]** Prove that similarity is an equivalence relation: $A \sim A$; $A\sim B \Rightarrow B \sim A$; $A \sim B$ and $B\sim C \Rightarrow A \sim C$. One line each.

**(b) [4]** Prove $\operatorname{trace}(XY) = \operatorname{trace}(YX)$ for square $X, Y$ by writing both as double sums. **Deduce that similar matrices have equal trace.**

**(c) [4]** Verify for your Q4 matrices that $A$ and $B$ have the same trace, determinant and rank. **Which of the four entries of $A$ is a property of $T$, and which of the basis?**

**(d) [4]** $I$ and $\begin{bmatrix}1&1\\0&1\end{bmatrix}$ have the same trace, determinant and rank. **Are they similar?** Settle it — think about what $M^{-1}IM$ can be for any invertible $M$.

Then show that $\begin{bmatrix}1&0\\0&2\end{bmatrix}$ and $\begin{bmatrix}1&1\\0&2\end{bmatrix}$, which *also* share all three, **are** similar, by exhibiting an $M$.

> **Two pairs, the same evidence, opposite answers.** Say in one sentence what this shows about
> trace, determinant and rank as a test for similarity.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Linear or not | 18 |
| 2 | Building the matrix | 22 |
| 3 | Calculus as a matrix | 20 |
| 4 | Change of basis | 24 |
| 5 | Similarity | 16 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*MATH 241 · Week 4 · PS 4 · © CSE Department*
