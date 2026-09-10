# MATH 241 · Problem Set 7 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Exact arithmetic except where noted**; `resources/diagonalize.py` reproduces the Q1 and Q4 computations.

**What this paper is testing.** **Q1 is the paper's trap and its most important question**: a repeated eigenvalue that *is* diagonalisable. A student who has confused "repeated" with "defective" will declare it non-diagonalisable and lose most of Q1 and Q2. Q2(d) and Q3(c) are the two places where the right answer is a *refusal* — no algorithm can test diagonalisability, and no $c$ makes $A_1$ converge. Q4(c) closes the PageRank loop opened in Week 0.

**Common failure modes:** (1) Q1(c) answered "no, the eigenvalue repeats"; (2) Q1(b) giving one vector for a two-dimensional eigenspace; (3) Q3(c) treated as a computation rather than as a determinant observation; (4) Q5(c) not addressing the apparent contradiction it explicitly asks about.

---

## Q1: Diagonalise It (24 points)

$$A = \begin{bmatrix}0&1&1\\ 1&0&1\\ 1&1&0\end{bmatrix}$$

### (a) [6]

$$\det(A - \lambda I) = -\lambda^3 + 3\lambda + 2 = -(\lambda - 2)(\lambda + 1)^2$$

$$\boxed{\lambda = 2 \ \text{(algebraic 1)}, \qquad \lambda = -1 \ \text{(algebraic 2)}}$$

**Checks:** trace $= 0 = 2 + (-1) + (-1)$ ✓ · $\det = 2 = 2 \cdot (-1) \cdot (-1)$ ✓

### (b) [8]

**$\lambda = 2$:** $A - 2I = \begin{bmatrix}-2&1&1\\1&-2&1\\1&1&-2\end{bmatrix}$, and $\mathbf{N} = \operatorname{span}\{(1,1,1)\}$. **Geometric multiplicity 1.**

**$\lambda = -1$:** $A + I = \begin{bmatrix}1&1&1\\1&1&1\\1&1&1\end{bmatrix}$, **rank 1**, so the null space has dimension $3 - 1 = \mathbf{2}$:

$$\mathbf{N}(A + I) = \{x : x_1 + x_2 + x_3 = 0\} = \operatorname{span}\{(-1,1,0),\ (-1,0,1)\}$$

**Geometric multiplicity 2.**

*Marking: 3 for $\lambda = 2$, 5 for $\lambda = -1$ **with two independent vectors**. **A single vector for the repeated eigenvalue is the commonest error and costs 3** — the rank-1 observation makes the dimension immediate and is worth pointing out on any script that eliminated laboriously.*

### (c) [4]

**Yes, diagonalisable.** For every eigenvalue, geometric $=$ algebraic:

| $\lambda$ | algebraic | geometric |
|---|---:|---:|
| $2$ | $1$ | $1$ |
| $-1$ | $2$ | $2$ |

**The eigenspace dimensions sum to $1 + 2 = 3 = n$**, so there are three independent eigenvectors.

> **This is the question the paper is built around.** A **repeated eigenvalue does not prevent
> diagonalisation** — only a deficient eigenspace does. **Any script answering "no, because
> $\lambda = -1$ repeats" should be marked 0 here and given the sentence in writing**; it is Week 6's
> central distinction and Week 7 is unusable without it.

### (d) [6]

$$S = \begin{bmatrix}-1&-1&1\\ 1&0&1\\ 0&1&1\end{bmatrix}, \qquad \Lambda = \begin{bmatrix}-1&0&0\\ 0&-1&0\\ 0&0&2\end{bmatrix}, \qquad S^{-1} = \tfrac13\begin{bmatrix}-1&2&-1\\ -1&-1&2\\ 1&1&1\end{bmatrix}$$

$$S\Lambda S^{-1} = A \ ✓$$

*Any valid basis of the $\lambda = -1$ eigenspace is accepted, and $S^{-1}$ must match the chosen $S$. Marking: 3 for a consistent $S$ and $\Lambda$, 1 for $S^{-1}$, 2 for the verification. **No verification, no verification marks.***

---

## Q2: When It Fails (20 points)

### (a) [8]

$$B = \begin{bmatrix}2&1&0\\ 0&2&1\\ 0&0&2\end{bmatrix}$$

**Triangular, so $p(\lambda) = (2-\lambda)^3$: $\lambda = 2$ with algebraic multiplicity 3.**

$$B - 2I = \begin{bmatrix}0&1&0\\ 0&0&1\\ 0&0&0\end{bmatrix}, \quad \text{rank } 2, \quad \dim\mathbf{N} = 3 - 2 = \mathbf{1}, \quad \mathbf{N} = \operatorname{span}\{(1,0,0)\}$$

**Not diagonalisable**: geometric $1 <$ algebraic $3$. **One eigenvector for a $3\times3$** — maximally defective.

**Jordan form: a single $3\times3$ block**

$$\begin{bmatrix}2&1&0\\ 0&2&1\\ 0&0&2\end{bmatrix}$$

— $B$ **is already in Jordan form.** *(A student who says so has read L22 §3 properly.)*

*Marking: 2 for the eigenvalues, 3 for the eigenspace with its dimension, 2 for the verdict, 1 for the Jordan form.*

### (b) [4]

**Nilpotent $\Rightarrow$ not diagonalisable.** Every eigenvalue satisfies $\lambda^k = 0$ (Week 6's L20 §4), so **every eigenvalue is $0$**, so $\Lambda = 0$. If $N$ were diagonalisable then $N = S0S^{-1} = 0$, contradicting $N \ne 0$. $\square$

**For $D$:** $D - 0I = D$ has rank 3, so $\dim\mathbf{N}(D) = 4 - 3 = \mathbf{1}$, spanned by $(1,0,0,0)$.

**As polynomials, the eigenvectors are the nonzero constants** — $\ker D$, which is Week 4's L13 §4 and the $+\,C$.

*Marking: 2 for the proof, 2 for $D$'s eigenspace identified as the constants.*

### (c) [4]

$p(\lambda) = (\lambda-3)^2(\lambda-7)^2$: each eigenvalue has algebraic multiplicity 2, so each geometric multiplicity is $1$ or $2$.

| $(g_3, g_7)$ | Diagonalisable? |
|---|---|
| $(1,1)$ | no |
| $(1,2)$ | no |
| $(2,1)$ | no |
| $\mathbf{(2,2)}$ | **yes** |

**Only $(2,2)$** — every geometric multiplicity must equal its algebraic one, so the dimensions sum to $4$.

### (d) [4]

$$\varepsilon = 10^{-8}: \ \text{geometric multiplicity } \mathbf{1} \qquad\qquad \varepsilon = 0: \ \text{geometric multiplicity } \mathbf{2}$$

**Why no algorithm tests it.** The property **jumps** — defective for every nonzero $\varepsilon$, however small, and diagonalisable at exactly $0$, **with no continuous transition.** In floating point you cannot distinguish $\varepsilon = 0$ from $\varepsilon = 10^{-300}$, so the question *is this matrix diagonalisable* **is not decidable by a computation**, and production software does not ask it — Weeks 10 and 11 restrict the matrices or change the factorisation instead.

*Marking: 2 for the two multiplicities, 2 for the explanation. **The word to look for is "jumps" or "discontinuous"**; "floating point is inaccurate" is not the answer and earns 1.*

---

## Q3: Complex Eigenvalues (20 points)

### (a) [5]

$C = \begin{bmatrix}3&-5\\5&3\end{bmatrix}$: trace $6$, determinant $9 + 25 = 34$.

$$\lambda^2 - 6\lambda + 34 = 0 \quad\Longrightarrow\quad \lambda = \frac{6 \pm \sqrt{36 - 136}}{2} = \boxed{3 \pm 5i}$$

$$(3+5i) + (3-5i) = 6 = \operatorname{trace}\ ✓ \qquad (3+5i)(3-5i) = 9 + 25 = 34 = \det\ ✓$$

### (b) [5]

$$r = \sqrt{34} = 5.8310, \qquad \cos\theta = \frac{6}{2\sqrt{34}} = 0.5145 \quad\Longrightarrow\quad \theta = 59.04°$$

And $\lvert 3 + 5i\rvert = \sqrt{34} = 5.8310$ ✓, $\arg(3+5i) = \arctan(5/3) = 59.04°$ ✓

**Geometrically: $C$ rotates the plane by about $59°$ and scales it by $\sqrt{34} \approx 5.83$.**

*Marking: 3 for the two formulas applied, 2 for the agreement and the sentence. **The point is that $r$ and $\theta$ came from trace and determinant alone** — no eigenvector, no complex arithmetic.*

### (c) [4]

**$A_1 = \begin{bmatrix}0&1\\-4&c\end{bmatrix}$:** trace $c$, $\det = 4$. Complex iff $c^2 - 16 < 0$, i.e. $\boxed{\lvert c\rvert < 4}$.

**Converges for no $c$ at all.**

**$A_2 = \begin{bmatrix}0&1\\-\tfrac14&c\end{bmatrix}$:** trace $c$, $\det = \tfrac14$. Complex iff $c^2 < 1$, i.e. $\lvert c\rvert < 1$. **Converges iff $\lvert c\rvert < \tfrac54$.**

*(At $c = \tfrac54$ the roots are exactly $1$ and $\tfrac14$, so the spectral radius is exactly $1$ — the boundary.)*

**The number you read off: the determinant.** $\det A = \prod\lambda_i$, so

$$\lvert\det A\rvert \ge 1 \quad\Longrightarrow\quad \text{some } \lvert\lambda_i\rvert \ge 1 \quad\Longrightarrow\quad A^k \not\to 0.$$

**$\det A_1 = 4$, so convergence is impossible for every $c$**, without computing a single eigenvalue. $\det A_2 = \tfrac14 < 1$, so it is at least possible — and then the trace decides.

*Marking: 1 for each "complex iff", 2 for **the determinant observation**, which is the question. A script that computes eigenvalues for a range of $c$ and reports "none work" for $A_1$ has the right answer by the wrong route; award 3 of 4.*

### (d) [6]

**Spectral radius** $= \max(\lvert 0.9 \pm 0.4i\rvert,\ 0.5) = \sqrt{0.81 + 0.16} = \sqrt{0.97} = \mathbf{0.9849}$.

**$A^k \to 0$: yes**, since every $\lvert\lambda_i\rvert < 1$ — though **only just**, and slowly: $0.9849^k$ needs $k \approx 900$ to reach $10^{-6}$.

**The orbit.** In the real plane spanned by the complex pair, a generic vector **spirals inwards**, rotating by $\arg\lambda = \arctan(0.4/0.9) \approx 24°$ per step and shrinking by $0.985$ each time. The third component **decays monotonically** by a factor $0.5$ per step, with no rotation.

**So the motion is a slow inward spiral in one plane plus a fast decay along one axis** — and the spiral dominates the long-run behaviour, because $0.985 > 0.5$.

*Marking: 2, 2, 2. **The last point — the slowest mode dominates — is what the question is for.***

---

## Q4: Powers in Practice (20 points)

### (a) [8]

$$\begin{bmatrix}a_{k+1}\\ a_k\end{bmatrix} = \begin{bmatrix}5&-6\\ 1&0\end{bmatrix}\begin{bmatrix}a_k\\ a_{k-1}\end{bmatrix}, \qquad M = \begin{bmatrix}5&-6\\ 1&0\end{bmatrix}$$

trace $5$, determinant $6$, so $\lambda^2 - 5\lambda + 6 = 0$ and $\boxed{\lambda = 2, 3}$.

**Closed form** $a_k = c_1 2^k + c_2 3^k$; from $a_0 = 0$ and $a_1 = 1$: $c_1 + c_2 = 0$ and $2c_1 + 3c_2 = 1$, so $c_2 = 1$, $c_1 = -1$:

$$\boxed{a_k = 3^k - 2^k}$$

**Check at $k = 4$:** $81 - 16 = 65$. And from the recurrence: $a_2 = 5$, $a_3 = 19$, $a_4 = 5(19) - 6(5) = 95 - 30 = 65$ ✓

*Marking: 2 for $M$, 2 for the eigenvalues, 3 for the closed form with constants determined, 1 for the check.*

### (b) [6]

**$\lambda = 1$ without a determinant:** the columns of $P$ sum to $1$, so $(1,1)P = (1,1)$ — meaning $(1,1)$ is an eigenvector of $P^\mathsf{T}$ with $\lambda = 1$. **And $P$ and $P^\mathsf{T}$ have the same eigenvalues** (PS 6 Q5(b)), so $1$ is an eigenvalue of $P$. $\square$

trace $1.5$, determinant $0.56 - 0.06 = 0.5$, so the other eigenvalue is $1.5 - 1 = \mathbf{0.5}$. *(Or $0.5/1$.)*

**Steady state:** $(P - I)v = \begin{bmatrix}-0.2&0.3\\ 0.2&-0.3\end{bmatrix}v = 0$ gives $v = (3,2)$, normalised $\boxed{(0.6,\ 0.4)}$.

**Steps to $10^{-6}$:** the error decays as $0.5^k$, so

$$0.5^k < 10^{-6} \iff k > \frac{\log 10^{-6}}{\log 0.5} = 19.93 \quad\Longrightarrow\quad \boxed{k = 20}$$

*Marking: 2 for the $\lambda = 1$ argument **without a determinant**, 2 for the steady state, 2 for the rate calculation.*

### (c) [6]

**Expected content, all three parts required:**

**What is computed:** the **eigenvector of the web's transition matrix for $\lambda = 1$** — the steady state of a random surfer. Not a solution of $Ax = b$; PageRank *is* an eigenvector.

**The iteration:** repeatedly multiply any starting probability vector by the transition matrix. Since $\lambda_1 = 1$ and every other $\lvert\lambda\rvert < 1$, $\Lambda^k \to \operatorname{diag}(1, 0, \dots, 0)$ and **every start converges to the $\lambda = 1$ eigenvector.** Each step is a matrix–vector product costing $O(\text{nonzeros})$ — the web graph is extremely sparse, a few links per page — not $O(n^3)$.

**What governs the count:** $\lvert\lambda_2\rvert$, the second-largest modulus. Error decays as $\lvert\lambda_2\rvert^k$. **Google's damping factor makes $\lvert\lambda_2\rvert \approx 0.85$, and $0.85^{50} \approx 3\times10^{-4}$** — hence about fifty iterations.

**So the contrast with Week 0's L03 §2 is: elimination is $n^3/3 \approx 3\times10^{26}$ operations and ten million years; this is fifty sparse matrix–vector products.**

*Marking: 2 per required element. **A paragraph that says "use eigenvalues" without naming $\lvert\lambda_2\rvert$ as the rate gets 4.***

---

## Q5: Structure (16 points)

### (a) [4]

**Base:** $A^1 = S\Lambda S^{-1}$ by hypothesis.
**Step:** $A^{k+1} = A^kA = (S\Lambda^kS^{-1})(S\Lambda S^{-1}) = S\Lambda^k(S^{-1}S)\Lambda S^{-1} = S\Lambda^{k+1}S^{-1}$. $\square$

$\Lambda^k = \operatorname{diag}(\lambda_1^k, \dots, \lambda_n^k)$ — **$n$ scalar powers.**

### (b) [4]

$$(S\Lambda^{-1}S^{-1})(S\Lambda S^{-1}) = S\Lambda^{-1}\Lambda S^{-1} = SS^{-1} = I$$

so $A^{-1} = S\Lambda^{-1}S^{-1}$. **Requires every $\lambda_i \ne 0$** — which is exactly $\det A = \prod\lambda_i \ne 0$, i.e. $A$ invertible.

$\Lambda^{-1} = \operatorname{diag}(1/\lambda_1,\dots,1/\lambda_n)$, so **the eigenvalues of $A^{-1}$ are the reciprocals**, with the same eigenvectors.

### (c) [4]

**($\Leftarrow$)** $A = S\Lambda S^{-1}$ and $B = T\Lambda T^{-1}$ with the same $\Lambda$. Then $\Lambda = T^{-1}BT$, so

$$A = S(T^{-1}BT)S^{-1} = (ST^{-1})B(ST^{-1})^{-1},$$

hence $A \sim B$.

**($\Rightarrow$)** Similar matrices share a characteristic polynomial (Week 6's L20 §2), hence eigenvalues with multiplicities. $\square$

**No contradiction with PS 4 Q5(d):** the theorem is conditional on **both** matrices being diagonalisable. $I$ is; $\begin{bmatrix}1&1\\0&1\end{bmatrix}$ is **not**. **The hypothesis fails, so the conclusion is not claimed.**

*Marking: 3 for the proof, 1 for correctly locating the failed hypothesis. **A script that does not address the apparent contradiction loses that mark** — the question asks explicitly.*

### (d) [4]

$$A^k = S\Lambda^kS^{-1} \quad\text{and}\quad \Lambda^k = \operatorname{diag}(\lambda_i^k) \to 0 \quad\text{since every } \lvert\lambda_i\rvert < 1,$$

so $A^k \to S0S^{-1} = 0$. $\square$

**If $A$ is defective**, $\Lambda^k$ is replaced by powers of Jordan blocks, whose entries are of the form $\binom{k}{j}\lambda^{k-j}$ — **a polynomial in $k$ times $\lambda^k$.** Since $\lvert\lambda\rvert < 1$ decays exponentially and a polynomial grows only polynomially, **the product still tends to zero**, so the conclusion is unchanged.

*Marking: 2 for the diagonalisable case, 2 for the defective remark. Accept any correct statement that exponential decay beats polynomial growth.*

---

## Grade Distribution Expected

| Band | Score | Description |
|---|---|---|
| Strong | 88–100 | Q1(c) confident and justified, Q3(c) via the determinant, Q4(c) naming $\lvert\lambda_2\rvert$, Q5(c) addressing the contradiction |
| Solid | 72–87 | Q1 and Q2 correct; Q3 and Q4 computed; interpretive parts thin |
| Passing | 55–71 | Diagonalisation performed and verified on Q1 |
| Concerning | < 55 | **Q1(c) answered "no, it repeats".** Week 6's central distinction has not landed and Weeks 10–11 assume it throughout. Help Desk this week |

---

*MATH 241 · Week 7 · PS 7 Solutions · © CSE Department*
