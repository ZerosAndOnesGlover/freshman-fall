# MATH 241 · Recitation 6 — Solutions and Session Notes
## **INSTRUCTOR ONLY** · Do not distribute

**Session:** Thursday of Week 7, 15:00–15:50, SSB 108 · covers Week 6 · unmarked
**PS 6 is due 17:00 the following day. Midterm 1 papers are returned this week.**

---

## Running the Session

**§2(b) is the session, and it decides Week 7.** The distinction between *a repeated eigenvalue* and *a deficient eigenspace* is the hinge of diagonalisation, and a room that leaves without it will experience Week 7 as a sequence of arbitrary conditions.

**Week 6 had only two lectures** (Fall Break took the Monday), so this material was delivered fast. **Expect the room to be shakier than usual** and budget accordingly — §1 is calibration, not revision.

| | Section | Budget | If it overruns |
|---|---|---|---|
| §1 | The drill | 10 min | Cut to (a) and (c) |
| §2 | The two that go wrong | 15 min | **Protect (b) absolutely. Cut §3 and §4** |
| §3 | Predicting from geometry | 10 min | Keep (e) and (f) |
| §4 | The machine | 10 min | Drop, or demo (b) from the front |
| §5 | Clinic | 5 min | Never drop — PS 6 is due tomorrow |

---

## §0 / §1 — The Drill

**(a)** $A = \begin{bmatrix}4&1\\2&3\end{bmatrix}$: trace $7$, determinant $12 - 2 = 10$, so $\lambda^2 - 7\lambda + 10 = 0$ and $\boxed{\lambda = 2, 5}$.

Eigenvectors: $(-1, 2)$ for $\lambda = 2$; $(1,1)$ for $\lambda = 5$.

**Checks:** $2 + 5 = 7$ ✓ and $2 \times 5 = 10$ ✓

> **Make the point explicitly:** the checks cost nothing and they are **two independent tests**. A
> student whose eigenvalues fail either does not need to hunt for the error — they know one exists,
> which is more than most arithmetic gives you.

**(b)** $B = \begin{bmatrix}2&0&0\\1&3&0\\4&5&-1\end{bmatrix}$ is **lower triangular**, so its eigenvalues are its diagonal: $\boxed{2, 3, -1}$. *(Checks: trace $4 = 2+3-1$ ✓, det $-6 = 2\cdot3\cdot(-1)$ ✓)*

$\lambda = 2$: $\mathbf{N}(B - 2I) = \operatorname{span}\{(-3, 3, 1)\}$.

*Verify at the board: $B(-3,3,1) = (-6, -3+9, -12+15-1) = (-6, 6, 2) = 2v$ ✓*

**(c)** $\lambda_4 = 10 - (1+2+3) = \boxed{4}$. Check: $1\cdot2\cdot3\cdot4 = 24 = \det C$ ✓

**If the two disagreed**, the given data would be **inconsistent** — no matrix has that trace, that determinant and those three eigenvalues. *(Worth asking; several will say "recompute", which misses that both are theorems and cannot both fail.)*

---

## §2 — The Two That Go Wrong

### (a) No real eigenvalues

$$R = \begin{bmatrix}1&-1\\ 1&1\end{bmatrix}, \qquad p(\lambda) = \lambda^2 - 2\lambda + 2, \qquad \text{discriminant } 4 - 8 = -4 < 0$$

$$\lambda = \frac{2 \pm 2i}{2} = 1 \pm i$$

$$(1+i) + (1-i) = 2 = \operatorname{trace}R\ ✓ \qquad (1+i)(1-i) = 1 + 1 = 2 = \det R\ ✓$$

**The sentence:** *$R$ leaves no direction of the plane unmoved* — it is a rotation (by $45°$) combined with a scaling (by $\sqrt2$), and a rotation has no invariant line.

### (b) Not enough eigenvectors — **the section**

$$P = \begin{bmatrix}3&0\\0&3\end{bmatrix}, \qquad Q = \begin{bmatrix}3&1\\0&3\end{bmatrix}$$

**(i)** Both give $p(\lambda) = \lambda^2 - 6\lambda + 9 = (3-\lambda)^2$. **Repeated eigenvalue $\lambda = 3$.**

**(ii)** $P - 3I = 0$, so $\mathbf{N} = \mathbb{R}^2$, **dimension 2** — every vector is an eigenvector.
$Q - 3I = \begin{bmatrix}0&1\\0&0\end{bmatrix}$, so $\mathbf{N} = \operatorname{span}\{(1,0)\}$, **dimension 1**.

**(iii)**

| | algebraic | geometric | |
|---|---:|---:|---|
| $P$ | $2$ | $2$ | fine |
| $Q$ | $2$ | $\mathbf{1}$ | **defective** |

**(iv)** **$Q$ is defective; $P$ is not.** The criterion is **geometric $<$ algebraic** — equivalently, fewer than $n$ independent eigenvectors. **Not** "the eigenvalue repeats", since it repeats for both.

**(v)** **Not similar.** $P = 3I$ is a scalar matrix, and $M^{-1}(3I)M = 3M^{-1}M = 3I$ for **every** invertible $M$ — so $3I$ is similar only to itself.

*(Deeper reason, if a pair reaches it: similar matrices have the same geometric multiplicities, because $M$ maps eigenspaces to eigenspaces bijectively. $2 \ne 1$, so they cannot be similar.)*

> **This is PS 4 Q5(d) with the numbers changed**, and the room should be told so. In Week 4 the
> only available argument was the scalar-matrix trick. **Now there is a real invariant**, it applies
> to every pair rather than only to scalar matrices, and it is the one Week 7 uses.
>
> **Do not let the session end without the sentence:** *a repeated eigenvalue does not make a matrix
> defective; a deficient eigenspace does.* Ask a pair to say it back.

---

## §3 — Predicting From Geometry

| | Prediction |
|---|---|
| **(a)** reflect across $y = 3x$ | $\lambda = 1$ with eigenvector along the line, $(1,3)$; $\lambda = -1$ perpendicular, $(3,-1)$ |
| **(b)** project onto $y = 3x$ | $\lambda = 1$ along $(1,3)$; $\lambda = 0$ along $(3,-1)$ |
| **(c)** rotate $270°$ | **no real eigenvalues** — it fixes no direction |
| **(d)** scale by 5 | $\lambda = 5$, and **every** nonzero vector is an eigenvector |

**(e)** **(d)** has a two-dimensional eigenspace. It says the transformation is **$5I$** — it does the same thing in every direction, so it has no special directions at all, and *every* direction is special. *(Contrast (a) and (b), where exactly two directions are picked out.)*

**(f)** Every projection satisfies $\boxed{P^2 = P}$. Then $Av = \lambda v$ gives $\lambda^2 v = \lambda v$, so $\lambda^2 = \lambda$ and $\lambda \in \{0, 1\}$.

**No geometry, no determinant, no elimination** — a single algebraic identity fixes the eigenvalues. *(L20 §4.)*

*Ask which of (a)–(d) also satisfies such an identity. Answer: the reflection, $R^2 = I$, forcing $\lambda = \pm1$. And $5I$ trivially.*

---

## §4 — The Machine

**(a)** The script prints trace $6 = 1+2+3$ and det $6 = 1\times2\times3$, and verifies each eigenvector with an explicit $Av$ product reported as `OK`.

**(b)** The **shear** is flagged `DEFECTIVE` — one independent eigenvector for a $2\times2$. It should match the §2(b)(iv) criterion exactly.

**(c)** $\lambda = \pm i$: sum $0 = \operatorname{trace}R$, product $i \times (-i) = -i^2 = 1 = \det R$ ✓

**(d)** **It does not stop being defective.** $\begin{bmatrix}1&7\\0&1\end{bmatrix}$ still has $\lambda = 1$ twice with eigenspace $\operatorname{span}\{(1,0)\}$ — geometric multiplicity 1 for **any** nonzero off-diagonal entry.

> **The lesson, and it is worth the two minutes:** defectiveness is **not a matter of degree.** The
> matrix is defective for off-diagonal $0.0001$ and diagonalisable at exactly $0$. **There is no
> continuous transition** — which is why defective matrices are numerically awkward and why real
> software does not try to detect them. **Week 7 §7 returns to this.**

---

## §5 — Clinic

**Q2(c) vs Q2(e).** §2(b). Refuse to re-derive.

**Q4(b).** One hint: *start from $4I$, add a single off-diagonal entry, then compute the rank of $A - 4I$.* Nothing more — the rank–nullity step is the exercise.

**Q5(d).** *"What is $\det(M^{-1}AM - \lambda I)$?"* and stop.

### Returned papers

**Do not discuss marks.** If a student's paper revealed a Weeks 2–4 gap, **say plainly that Weeks 7–11 build on it** and name the two places to go: Prof. Abara, Thursdays 10:00–11:00, SSB 310; and the Help Desk, BH 120.

**Week 7 is the last week where a Weeks 2–4 gap can be closed cheaply.** Week 8 adds orthogonality on top of the four subspaces, and Weeks 9–11 assume all of it.

---

## What to Report Back

| Signal | What it means for Week 7 |
|---|---|
| §2(b)(iv) answered "because the eigenvalue repeats" | **The central distinction has not landed.** L21 must open with it, not assume it |
| §2(a) fine but §2(b) shaky | Normal. Complex eigenvalues are easier than defectiveness because they announce themselves |
| §4(d) surprised the room | Good — it should. Note it, and L21 §7 can lean on the surprise |
| Students raising Midterm gaps in Weeks 2–4 | **Names to Prof. Abara this week.** It is the last cheap intervention |

---

*MATH 241 · Week 6 · Recitation 6 Solutions · © CSE Department*
