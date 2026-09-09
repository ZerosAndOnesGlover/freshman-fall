# MATH 241 · Problem Set 1 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**All computed figures below are from the reference machine:** Intel i5-8250U, Ubuntu 24.04.4, CPython 3.14, IEEE 754 binary64. Exact results must match to the digit; the timings in Q5(a) will not.

**What this paper is testing.** Q1(a) is a fluency drill and should be near-full marks; **Q1(c) is the question that matters on this paper**, because "every column of $AB$ is a combination of the columns of $A$" is the lemma Weeks 2 and 3 are built on. Q4 is the mechanical core and must be right — a student who cannot produce $L$ from the multipliers will struggle in Week 9. Q5 is calibration, and Q5(b) is where the thoughtless answer ("associate to the right") gets caught.

**Common failure modes:** (1) Q1(a) done once and presented four times with different words; (2) Q3(d) proving non-invertibility by determinant, which works but misses the point; (3) Q4(c) giving a $P$ that permutes columns; (4) Q5(b) answered with a rule that contradicts (a).

---

## Q1: Four Readings of One Product (20 points)

$$A = \begin{bmatrix}1&2&0\\3&-1&4\end{bmatrix} \ (2\times3), \qquad B = \begin{bmatrix}2&1\\0&3\\-1&5\end{bmatrix} \ (3\times2), \qquad AB \text{ is } 2\times2.$$

### (a) [10] — the same answer four ways

$$AB = \begin{bmatrix}2 & 7\\ 2 & 20\end{bmatrix}$$

**(i) Entry by entry.**
$(AB)_{11} = 1(2)+2(0)+0(-1) = 2$ · $(AB)_{12} = 1(1)+2(3)+0(5) = 7$
$(AB)_{21} = 3(2)+(-1)(0)+4(-1) = 2$ · $(AB)_{22} = 3(1)+(-1)(3)+4(5) = 20$

**(ii) Column by column.** $AB = [\,Ab_1 \mid Ab_2\,]$, each $Ab_j$ a combination of $A$'s columns:

$$Ab_1 = 2\begin{bmatrix}1\\3\end{bmatrix} + 0\begin{bmatrix}2\\-1\end{bmatrix} + (-1)\begin{bmatrix}0\\4\end{bmatrix} = \begin{bmatrix}2\\2\end{bmatrix}, \qquad
Ab_2 = 1\begin{bmatrix}1\\3\end{bmatrix} + 3\begin{bmatrix}2\\-1\end{bmatrix} + 5\begin{bmatrix}0\\4\end{bmatrix} = \begin{bmatrix}7\\20\end{bmatrix}$$

**(iii) Row by row.** Each row of $AB$ is a combination of the rows of $B$:

row 1 $= 1(2,1) + 2(0,3) + 0(-1,5) = (2, 7)$
row 2 $= 3(2,1) - 1(0,3) + 4(-1,5) = (6-0-4,\; 3-3+20) = (2, 20)$

**(iv) Outer products.** $AB = \sum_{k=1}^{3} a_k\beta_k^\mathsf{T}$:

$$\begin{bmatrix}1\\3\end{bmatrix}\!\begin{bmatrix}2&1\end{bmatrix} + \begin{bmatrix}2\\-1\end{bmatrix}\!\begin{bmatrix}0&3\end{bmatrix} + \begin{bmatrix}0\\4\end{bmatrix}\!\begin{bmatrix}-1&5\end{bmatrix}
= \begin{bmatrix}2&1\\6&3\end{bmatrix} + \begin{bmatrix}0&6\\0&-3\end{bmatrix} + \begin{bmatrix}0&0\\-4&20\end{bmatrix} = \begin{bmatrix}2&7\\2&20\end{bmatrix}$$

*Marking: 2.5 each. **The failure mode is one computation dressed four ways** — a script that computes the four entries and then merely re-describes them as "columns" earns 2.5 of the 10. Each reading must produce the answer by its own route; (iv) in particular must show three full $2\times2$ matrices being summed.*

### (b) [4]

$$BA = \begin{bmatrix}5&3&4\\ 9&-3&12\\ 14&-7&20\end{bmatrix}$$

**The most immediate reason:** $AB$ is $2\times2$ and $BA$ is $3\times3$. **They are not the same size**, so the question of equality does not arise — no arithmetic needed.

*Marking: 2 for the product, 2 for the shape argument. A student who says "matrix multiplication is not commutative" gets 1 of the 2 — true, and not the immediate reason.*

### (c) [6]

**Column $j$ of $AB$.** Column $j$ of any matrix $M$ is $Me_j$. So

$$(AB)e_j = A(Be_j) = A\,b_j$$

using associativity, which L04 §1 established by construction. $\square$

**Every column of $AB$ is a combination of $A$'s columns.** By the above, column $j$ of $AB$ is $Ab_j$; and by L01 §4, $Av$ is $\sum_k v_k a_k$ for any $v$. Hence

$$\text{column } j \text{ of } AB = \sum_k (b_j)_k\,a_k$$

— a linear combination of the columns of $A$, with the entries of $B$'s $j$-th column as the amounts. $\square$

> **Say on the script:** this is the lemma behind "$\operatorname{rank}(AB) \le \operatorname{rank}A$"
> in Week 3, and behind the fact that $AB$'s column space sits inside $A$'s. **Students who see that
> the two-line proof is doing real work should be told so.**

*Marking: 3 for the $Me_j$ argument, 3 for the second part. **Do not award the second 3 to a proof that goes back to the entry formula** — the question said to use the fact just proved, and the entire pedagogical point is that reading (ii) makes it a two-liner while reading (i) makes it an index manipulation.*

---

## Q2: The Algebra, and Where It Breaks (18 points)

### (a) [5]

$$(A+B)^2 = A^2 + AB + BA + B^2 \qquad (A-B)(A+B) = A^2 + AB - BA - B^2$$

**Each collapses exactly when $AB = BA$** — then the first becomes $A^2 + 2AB + B^2$ and the second $A^2 - B^2$. **Commuting is the precise condition, not merely a sufficient one**: the difference between the two sides is $AB - BA$ in both cases, which vanishes iff they commute.

*Marking: 2 per expansion, 1 for stating the condition as an "if and only if".*

### (b) [5]

$$A = \begin{bmatrix}0&1\\0&0\end{bmatrix},\; B = \begin{bmatrix}1&0\\0&0\end{bmatrix} \implies AB = \begin{bmatrix}0&0\\0&0\end{bmatrix},\quad BA = \begin{bmatrix}0&1\\0&0\end{bmatrix} \ne 0$$

*(Many other answers work; L04 §3's $P, Q$ do not, since $PQ \ne 0$ — a student who reaches for them has to adapt, which is fine.)*

**On $AB = AC$:** nothing follows. Take $A$ above, $C = B + A$; then $AC = AB + A^2 = 0 + 0 = 0 = AB$ while $B \ne C$. **There is no cancellation law for matrices**, and L05 supplies the missing hypothesis: if $A$ is *invertible*, multiply on the left by $A^{-1}$ and $B = C$ follows.

*Marking: 2 for the first pair, 1 for the second, 2 for the cancellation discussion including the invertibility repair.*

### (c) [4]

$AB$ defined requires $n = p$. $BA$ defined requires $q = m$. So

$$\boxed{B \text{ is } n \times m}$$

$AB$ is then $m\times m$ and $BA$ is $n \times n$. **Same size iff $m = n$**, i.e. both are square — and even then they are generally different matrices, as (b) and L04 §3 show.

*Marking: 2 for the shape deduction, 1 for the two product sizes, 1 for "same size does not mean equal".*

### (d) [4]

$$\begin{bmatrix}I&X\\0&I\end{bmatrix}\begin{bmatrix}I&Y\\0&I\end{bmatrix} = \begin{bmatrix}I\cdot I + X\cdot 0 & I\cdot Y + X\cdot I\\ 0\cdot I + I\cdot 0 & 0\cdot Y + I\cdot I\end{bmatrix} = \begin{bmatrix}I & X+Y\\ 0 & I\end{bmatrix}$$

**Setting $Y = -X$ gives the identity**, so

$$\begin{bmatrix}I&X\\0&I\end{bmatrix}^{-1} = \begin{bmatrix}I&-X\\0&I\end{bmatrix}$$

with no elimination performed. *(And these matrices **do** commute with one another, which is unusual enough to be worth remarking — they form a group isomorphic to addition of the blocks $X$.)*

*Marking: 2 for the block product, 2 for the inverse. Full marks require noting that $Y = -X$ is the whole argument.*

---

## Q3: Inverses (22 points)

### (a) [8]

$$[\,C\mid I\,] = \left[\begin{array}{ccc|ccc}1&2&3&1&0&0\\ 2&5&3&0&1&0\\ 1&0&8&0&0&1\end{array}\right]
\xrightarrow[\ell_{31}=1]{\ell_{21}=2}
\left[\begin{array}{ccc|ccc}1&2&3&1&0&0\\ 0&1&-3&-2&1&0\\ 0&-2&5&-1&0&1\end{array}\right]$$

$$\xrightarrow{\ell_{32}=-2}
\left[\begin{array}{ccc|ccc}1&2&3&1&0&0\\ 0&1&-3&-2&1&0\\ 0&0&-1&-5&2&1\end{array}\right]
\xrightarrow{\text{upward, then scale}}
\left[\begin{array}{ccc|ccc}1&0&0&-40&16&9\\ 0&1&0&13&-5&-3\\ 0&0&1&5&-2&-1\end{array}\right]$$

$$\boxed{C^{-1} = \begin{bmatrix}-40&16&9\\ 13&-5&-3\\ 5&-2&-1\end{bmatrix}}$$

Check row 1 of $C$ against column 1 of $C^{-1}$: $1(-40) + 2(13) + 3(5) = -40 + 26 + 15 = 1$ ✓

**Why the inverse is an integer matrix.** $\operatorname{adj}C$ has integer entries whenever $C$ does, since every entry is $\pm$ a determinant of an integer submatrix. So $C^{-1} = \frac{1}{\det C}\operatorname{adj}C$ is an integer matrix **as soon as $\det C = \pm 1$**, which holds here.

**And the converse.** If $C$ and $C^{-1}$ are both integer matrices then $\det C$ and $\det C^{-1}$ are both integers with product $1$, forcing $\det C = \pm 1$. So the condition is exactly $\det C = \pm 1$. *(Such matrices are called **unimodular**; they are the invertible elements of the ring of integer matrices, and they are what make integer lattice bases interchangeable — a fact CS 341 uses in lattice cryptography.)*

*Marking: 5 for the tableau shown at every stage, 3 for the $\det = \pm1$ characterisation. Award 2 of the 3 for the forward direction alone; the converse is what makes it a characterisation.*

### (b) [5]

$$(AB)(B^{-1}A^{-1}) = A(BB^{-1})A^{-1} = AIA^{-1} = AA^{-1} = I$$

and symmetrically $(B^{-1}A^{-1})(AB) = I$. By L05 §1's uniqueness, $B^{-1}A^{-1}$ **is** $(AB)^{-1}$. $\square$

For three: $(ABC)^{-1} = ((AB)C)^{-1} = C^{-1}(AB)^{-1} = C^{-1}B^{-1}A^{-1}$. $\square$

**Non-mathematical account:** socks then shoes; to undo, shoes come off first. **The last thing done is the first thing undone.**

*Marking: 3 for the proof (both sides, or a citation of uniqueness), 1 for the three-factor version, 1 for the account.*

### (c) [4]

$B$ is not invertible, so there is $z \ne 0$ with $Bz = 0$. Then

$$(AB)z = A(Bz) = A0 = 0$$

with $z \ne 0$, so $AB$ is not invertible either. $\square$

*(Note $A$'s invertibility was never used — the statement is true for any $A$ of compatible shape. Worth a marginal note to any student who used it.)*

*Marking: 4, or 2 for a determinant argument ($\det(AB) = \det A\det B = 0$) — correct, and it uses Week 5.*

### (d) [5]

**Not invertible.** If $A^{-1}$ existed, multiply $A^2 = A$ on the left by it: $A = I$, contradicting $A \ne I$. $\square$

**Example.**

$$A = \begin{bmatrix}1&0\\0&0\end{bmatrix}, \qquad A^2 = A, \qquad A \ne 0, I$$

**Geometrically** it takes $(x, y)$ to $(x, 0)$: **projection onto the $x$-axis**. Every point on the $y$-axis is sent to the origin, so the map is not injective, and **information is destroyed** — from $(x, 0)$ you cannot recover the $y$ you started with.

**"Not invertible" is exactly right for a projection**, and $A^2 = A$ says why: projecting twice is projecting once, because after the first projection there is nothing left to remove. A map that can be undone cannot be idempotent unless it is the identity.

*Marking: 2 for the proof, 1 for the example, 2 for the geometry. **The geometry is the point of the question** — Week 8 builds every projection matrix from $A^2 = A$, and a student who can already say why idempotence forces non-invertibility will find that week easy.*

---

## Q4: $A = LU$ (22 points)

### (a) [10]

$$D = \begin{bmatrix}1&2&3\\ 3&7&7\\ -2&0&-9\end{bmatrix}$$

$\ell_{21} = 3$: $R_2 - 3R_1 = [\,0\ \ 1\ \ {-2}\,]$
$\ell_{31} = -2$: $R_3 + 2R_1 = [\,0\ \ 4\ \ {-3}\,]$
$\ell_{32} = 4$: $R_3 - 4R_2 = [\,0\ \ 0\ \ 5\,]$

$$\boxed{L = \begin{bmatrix}1&0&0\\ 3&1&0\\ -2&4&1\end{bmatrix}, \qquad U = \begin{bmatrix}1&2&3\\ 0&1&-2\\ 0&0&5\end{bmatrix}}$$

**Verification, in full:**

| $LU$ row | Computation | Result |
|---|---|---|
| 1 | $1(1,2,3)$ | $(1, 2, 3)$ ✓ |
| 2 | $3(1,2,3) + 1(0,1,-2)$ | $(3, 7, 7)$ ✓ |
| 3 | $-2(1,2,3) + 4(0,1,-2) + 1(0,0,5)$ | $(-2, -4+4, -6-8+5) = (-2, 0, -9)$ ✓ |

*Marking: 4 for the multipliers, 3 for $L$ and $U$, 3 for the verification. **$L$ built by "computing" something rather than by transcribing the multipliers is the error to look for** — it usually shows up as a sign flip in the $(3,1)$ entry.*

### (b) [6]

**First right-hand side, $b = (2, 10, 7)$.**

$Lc = b$: $c_1 = 2$; $3(2) + c_2 = 10 \Rightarrow c_2 = 4$; $-2(2) + 4(4) + c_3 = 7 \Rightarrow c_3 = -5$.
$Ux = c$: $5x_3 = -5 \Rightarrow x_3 = -1$; $x_2 - 2(-1) = 4 \Rightarrow x_2 = 2$; $x_1 + 4 - 3 = 2 \Rightarrow x_1 = 1$.

$$c = (2, 4, -5), \qquad x = (1, 2, -1)$$

**Second, $b = (9, 20, -31)$.**

$Lc = b$: $c_1 = 9$; $27 + c_2 = 20 \Rightarrow c_2 = -7$; $-18 - 28 + c_3 = -31 \Rightarrow c_3 = 15$.
$Ux = c$: $x_3 = 3$; $x_2 - 6 = -7 \Rightarrow x_2 = -1$; $x_1 - 2 + 9 = 9 \Rightarrow x_1 = 2$.

$$c = (9, -7, 15), \qquad x = (2, -1, 3)$$

**The counts, $n = 3$.**

| | Multiply–subtracts | Divisions |
|---|---:|---:|
| Reusing $L, U$ — forward then back | $3 + 3 = \mathbf{6}$ | $\mathbf{3}$ |
| Fresh elimination on $[\,D\mid b\,]$, then back | $8 + 3 = \mathbf{11}$ | $3 + 3 = \mathbf{6}$ |

*(Forward: $c_2$ costs one pair, $c_3$ two. Back: $x_2$ one, $x_1$ two, plus one division per row. Fresh elimination: column 1 costs two multipliers and $2\times3$ pairs across columns 2, 3 and the RHS; column 2 costs one multiplier and $2$ pairs.)*

**General $n$:** reuse costs $\approx 2n^2$ (two triangular solves at $n^2$ each); fresh costs $\approx n^3/3 + n^2$. **At $n = 3$ the saving is a factor of under two, which is why the point is invisible at hand scale** — at $n = 1000$ it is a factor of $167$.

*Marking: 2 per right-hand side (both $c$ and $x$ needed), 2 for the counts. Accept small variations in the operation count depending on whether divisions are folded in, provided the student states the convention.*

### (c) [6]

**Why $E$ has no $LU$.** $e_{11} = 0$. In $E = LU$, the $(1,1)$ entry is $\ell_{11}u_{11}$ and $L$ is unit lower triangular, so $e_{11} = u_{11}$ — the first pivot. **A zero there means there is no first pivot to have**, and no lower-triangular $L$ can repair it, since $L$'s first row is $(1, 0, \dots, 0)$ and cannot bring in another row.

**Swap rows 1 and 2:**

$$P = \begin{bmatrix}0&1&0\\ 1&0&0\\ 0&0&1\end{bmatrix}, \qquad PE = \begin{bmatrix}1&2&1\\ 0&1&2\\ 2&7&9\end{bmatrix}$$

Eliminate: $\ell_{21} = 0$, $\ell_{31} = 2$ gives $R_3 - 2R_1 = [\,0\ \ 3\ \ 7\,]$; then $\ell_{32} = 3$ gives $R_3 - 3R_2 = [\,0\ \ 0\ \ 1\,]$.

$$\boxed{L = \begin{bmatrix}1&0&0\\ 0&1&0\\ 2&3&1\end{bmatrix}, \qquad U = \begin{bmatrix}1&2&1\\ 0&1&2\\ 0&0&1\end{bmatrix}}$$

Check row 3 of $LU$: $2(1,2,1) + 3(0,1,2) + 1(0,0,1) = (2, 4+3, 2+6+1) = (2, 7, 9)$ ✓

**$P^{-1} = P^\mathsf{T}$.** Here $P$ is its own transpose (a single swap is symmetric), and $P^2 = I$ directly. So

$$E = P^{-1}LU = P^\mathsf{T}LU = \begin{bmatrix}0&1&0\\ 1&0&0\\ 0&0&1\end{bmatrix}\begin{bmatrix}1&0&0\\ 0&1&0\\ 2&3&1\end{bmatrix}\begin{bmatrix}1&2&1\\ 0&1&2\\ 0&0&1\end{bmatrix}$$

*Marking: 2 for the "no $LU$" argument (it must be about $L$'s first row, not merely "the pivot is zero"), 2 for $P, L, U$ with verification, 2 for the $P^\mathsf{T}$ step and the three-factor form. **A student who permutes columns instead of rows has produced $EP$, which does not factor — mark it wrong and say why in one line.**

Note $\ell_{21} = 0$ here; as in PS 0 Q1(a), it must still be recorded, and $L$'s $(2,1)$ entry is genuinely $0$.*

---

## Q5: Where You Put the Brackets (18 points)

### (a) [6]

$m = 1000$, $n = 2$, $p = 1000$, $q = 1$.

| | Flops | Largest intermediate |
|---|---:|---|
| $(AB)C$ | $2(1000)(2)(1000) + 2(1000)(1000)(1) = 6{,}000{,}000$ | $1000\times1000$ = $10^6$ entries = **8.0 MB** |
| $A(BC)$ | $2(2)(1000)(1) + 2(1000)(2)(1) = 8{,}000$ | $2\times1$ = **16 bytes** |

**Flop ratio: 750.**

**Measured on the reference machine:**

```
measured: (AB)C 1.048 s   A(BC) 0.001331 s   speedup 787x
```

**787 against a predicted 750 — the measurement is *faster* than the flop count says it should be.**

The discrepancy goes the direction that flop counting cannot explain, so the explanation must be outside the flop count: **memory traffic.** $(AB)C$ allocates, writes and then re-reads eight megabytes, which does not fit in this machine's L2 cache; $A(BC)$ never creates it. The extra $5\%$ is cache and allocator overhead attaching to the version that was already losing.

*Accept any measured speedup between roughly $500$ and $1500$ — CPython's interpreter overhead varies. **Full marks require the student to notice the direction of the discrepancy and reach for something other than arithmetic to explain it.** A student who reports "matches closely" without comparing the numbers gets 4 of the 6.*

### (b) [6]

$A$ is $200\times200$, $B$ is $200\times3$, $C$ is $3\times200$.

| | Flops | Intermediate |
|---|---:|---|
| $(AB)C$ | $2(200)(200)(3) + 2(200)(3)(200) = 240{,}000 + 240{,}000 = \mathbf{480{,}000}$ | $AB$ is $200\times3$ = 600 entries |
| $A(BC)$ | $2(200)(3)(200) + 2(200)(200)(200) = 240{,}000 + 16{,}000{,}000 = \mathbf{16{,}240{,}000}$ | $BC$ is $200\times200$ = 40,000 entries |

**Left wins, by a factor of $33.8$.**

**The rule:** *form the intermediate product with the fewest entries.* Equivalently — since for a three-factor chain the two costs are $2mnp + 2mpq$ and $2npq + 2mnq$ — **multiply first across the small shared dimension.**

Checking it against both parts: in (a) the candidates are $AB$ at $10^6$ entries and $BC$ at $2$, so right wins; in (b) they are $AB$ at $600$ and $BC$ at $40{,}000$, so left wins. **One rule, both answers.**

*Marking: 3 for the two costs, 3 for a rule that correctly predicts (a) **and** (b). **"Associate to the right" scores zero for the rule** even though it is the right answer to (a) — the question was written to catch exactly that.*

### (c) [6]

$n = 2000$, $B$ has $k = 50$ columns.

| Route | Setup | Multiply / solve | Total |
|---|---:|---:|---:|
| **Invert, then multiply** | $2n^3 = 1.60\times10^{10}$ | $2n^2k = 4.00\times10^{8}$ | $\mathbf{1.64\times10^{10}}$ |
| **Factor, then solve** | $n^3/3 = 2.67\times10^{9}$ | $k \cdot 2n^2 = 4.00\times10^{8}$ | $\mathbf{3.07\times10^{9}}$ |

$$\text{ratio} = \boxed{5.3}$$

**The per-column cost is identical — $2n^2$ either way.** All of the difference is in the setup, which is the whole argument of L05 §6: the inverse buys you nothing that the factorisation has not already bought, and charges $6\times$ for it.

**The line to run:**

```python
X = scipy.linalg.solve(A, B)          # or lu_factor once, then lu_solve per column
```

**The line not to run:**

```python
X = numpy.linalg.inv(A) @ B           # 5x the work, and worse conditioned
```

*Marking: 4 for the two totals and the ratio, 2 for the code. Accept `numpy.linalg.solve(A, B)` — it handles a matrix right-hand side and factors once. **A student who observes that the $2n^2k$ terms are equal and that therefore the ratio approaches $6$ as $k$ grows relative to nothing has understood it exactly**; note it on the script.*

---

## Grade Distribution Expected

| Band | Score | Description |
|---|---|---|
| Strong | 88–100 | Q1(c) proved via $Me_j$ without falling back on indices; Q5(b)'s rule stated correctly and checked against both parts |
| Solid | 72–87 | Q1–Q4 correct; Q5(b) answered with the right winner and a rule that only fits one case |
| Passing | 55–71 | Q4 correct, which is the mechanical minimum for Week 9 |
| Concerning | < 55 | **An error in Q4(a) is the signal.** $L$ is transcription, not computation; a student who cannot produce it has not understood what elimination was doing, and Weeks 9–11 are four more factorisations. Recommend the Help Desk immediately |

---

*MATH 241 · Week 1 · PS 1 Solutions · © CSE Department*
