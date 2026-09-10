# MATH 241 · Recitation 3 — Solutions and Session Notes
## **INSTRUCTOR ONLY** · Do not distribute

**Session:** Thursday of Week 4, 15:00–15:50, SSB 108 · covers Week 3 · unmarked
**PS 3 is due 17:00 the following day.**

---

## Running the Session

**§1 is the session.** Four bases with correct ambient spaces is the mechanical minimum for Week 8, and a student who cannot produce it under supervision will not produce it on the midterm. **§2(d) is the best question on the sheet** and is worth protecting even at the cost of §4.

| | Section | Budget | If it overruns |
|---|---|---|---|
| §1 | The table | 15 min | **Protect.** Cut §4 entirely |
| §2 | Sums and dot products | 10 min | Keep (a) and (d); spot-check (b) |
| §3 | Solvability | 10 min | Do (a) and (b) only |
| §4 | The machine | 10 min | Demo (b) from the front |
| §5 | Clinic | 5 min | Help Desk |

---

## §0 / §1 — The Table

$$M = \begin{bmatrix}1&2&1&4\\ 2&4&3&9\\ 3&6&4&13\end{bmatrix} \qquad \operatorname{rref}(M) = \begin{bmatrix}1&2&0&3\\ 0&0&1&1\\ 0&0&0&0\end{bmatrix}$$

**$m = 3$, $n = 4$, rank $r = 2$. Pivot columns 1 and 3; free columns 2 and 4.**

| Subspace | Lives in | $\dim$ | Basis |
|---|---|---:|---|
| $\mathbf{C}(M)$ | $\mathbb{R}^3$ | $2$ | $(1,2,3),\ (1,3,4)$ — **columns 1 and 3 of $M$** |
| $\mathbf{N}(M)$ | $\mathbb{R}^4$ | $2$ | $(-2,1,0,0),\ (-3,0,-1,1)$ |
| $\mathbf{C}(M^\mathsf{T})$ | $\mathbb{R}^4$ | $2$ | $(1,2,0,3),\ (0,0,1,1)$ — **nonzero rows of $\operatorname{rref}$** |
| $\mathbf{N}(M^\mathsf{T})$ | $\mathbb{R}^3$ | $1$ | $(-1,-1,1)$ |

**Verify the specials against $M$ at the board** — PS 3 asks for it:
$-2(1,2,3) + (2,4,6) = (0,0,0)$ ✓ and $-3(1,2,3) - (1,3,4) + (4,9,13) = (0,0,0)$ ✓

**And the left null vector:** $(-1,-1,1)^\mathsf{T}M = (-1-2+3,\ -2-4+6,\ -1-3+4,\ -4-9+13) = (0,0,0,0)$ ✓

### The two "why" questions

**Why not the pivot columns of $\operatorname{rref}(M)$?** Because elimination **moves the columns** — it combines entries within each column — so $\mathbf{C}(\operatorname{rref}M)$ is a different subspace. Here it is $\{b : b_3 = 0\}$, and $\mathbf{C}(M)$ is $\{b : -b_1 - b_2 + b_3 = 0\}$. *(Week 2's L08 §4.)*

**Why are the rows of $\operatorname{rref}$ allowed?** Because elimination **combines rows**, so every new row is in the span of the old ones and — the operations being invertible — every old row is in the span of the new. **The row space is unchanged.** *(L12 §3.)*

> **Make a pair say both sentences.** The asymmetry is not a convention to memorise; it is a fact
> about what the algorithm does, and the recipes follow from it.

*Watch for: $\mathbf{N}(M^\mathsf{T})$ computed as a row vector and then compared with column vectors. It lives in $\mathbb{R}^3$ either way; the transpose in the name refers to the matrix, not the answer.*

---

## §2 — The Sums and the Dot Products

**(a)** $r + (n-r) = 2 + 2 = 4 = n$, **in $\mathbb{R}^4$** — the null space and the row space. $r + (m-r) = 2 + 1 = 3 = m$, **in $\mathbb{R}^3$** — the column space and the left null space.

**(b)** $\mathbf{N}(M)$ against the row space is $2 \times 2 = 4$; $\mathbf{N}(M^\mathsf{T})$ against $\mathbf{C}(M)$ is $1 \times 2 = 2$. **Six in total.**

| | $(1,2,0,3)$ | $(0,0,1,1)$ |
|---|---:|---:|
| $(-2,1,0,0)$ | $0$ | $0$ |
| $(-3,0,-1,1)$ | $0$ | $0$ |

$(-1,-1,1)\cdot(1,2,3) = -1-2+3 = 0$ ✓ · $(-1,-1,1)\cdot(1,3,4) = -1-3+4 = 0$ ✓

**(c)** $Mx = 0$ says every entry of $Mx$ is zero, and the $i$-th entry is *(row $i$) $\cdot\ x$*. **So $x$ is perpendicular to every row, hence to every combination of rows, hence to the whole row space.**

**(d) — the question worth the section**

**No.** Dimensions adding to the whole is **necessary and not sufficient.**

**Counterexample to hand them if they stall:** in $\mathbb{R}^3$, take the $x$-axis and the $y$-axis. $\dim = 1 + 1 = 2$, and together they reach only the $xy$-plane — nothing near filling $\mathbb{R}^3$, and they are not even a plane, since their *union* is not a subspace (Week 2's L07 §6). A cleaner one: two **distinct planes** in $\mathbb{R}^3$ have $2 + 2 = 4 > 3$ and still fail to be complementary, because they share a line.

**What is actually needed** is that the two subspaces meet only at $0$ *and* their dimensions add up — and **orthogonality gives the first for free**: if $u$ is in both and they are orthogonal, then $u \cdot u = 0$, so $u = 0$.

> **That is exactly why L12 §7 is labelled a preview.** The dimension arithmetic in §3 is suggestive
> and proves nothing on its own; **Week 8 supplies the orthogonality as a theorem and the splitting
> follows.** A pair that reaches this has understood the structure of the whole second half of the
> course.

---

## §3 — Solvability Without Elimination

**(a)** $\dim\mathbf{N}(M^\mathsf{T}) = m - r = 1$, so **one condition**, from $y = (-1,-1,1)$:

$$-b_1 - b_2 + b_3 = 0 \qquad\text{equivalently}\qquad \boxed{b_3 = b_1 + b_2}$$

*Cross-check: $\operatorname{rref}(M)$ has exactly one zero row. **One zero row, one condition, one dimension** — make them notice the three counts agree.*

**(b)** $(8,18,26)$: $8 + 18 = 26$ ✓ **solvable.** $(8,18,27)$: $8 + 18 = 26 \ne 27$ ✗ **not solvable.** *One addition each.*

**(c)** For $b = (8,18,26)$:

$$[\,M \mid b\,] \longrightarrow \left[\begin{array}{cccc|c}1&2&0&3&6\\ 0&0&1&1&2\\ 0&0&0&0&0\end{array}\right] \Rightarrow x_p = (6,0,2,0)$$

$$Mx_p = 6(1,2,3) + 2(1,3,4) = (6,12,18) + (2,6,8) = (8,18,26)\ ✓$$

$$x = (6,0,2,0) + t(-2,1,0,0) + u(-3,0,-1,1)$$

**(d)** The plane $b_3 = b_1 + b_2$ **is $\mathbf{C}(M)$** — the set of reachable $b$, which is what the column space is defined to be. **How they know:** the condition was derived from a vector orthogonal to every column, so the plane it defines contains every column and hence their span; and its dimension is 2, which matches $\dim\mathbf{C}(M)$, so it is not merely a superset.

*The second half of that justification is the part to insist on. "It contains the columns" alone would allow a bigger set.*

---

## §4 — The Machine

**(a)** Script matrix: $3\times4$, $r=2$, dims $2,2,2,1$. $M$: $3\times4$, $r=2$, dims $2,2,2,1$. **Identical pattern, different numbers** — which is the point.

**(b)** The script's $(5,-2,1)$ is Week 2's plane coefficients; $M$'s $(-1,-1,1)$ is §3(a)'s. **Same sentence, twice.**

**(c)** Rows of $M$ from the rref's rows, coefficients taken from the pivot columns:

| | | |
|---|---|---|
| row 1 | $1(1,2,0,3) + 1(0,0,1,1)$ | $= (1,2,1,4)$ ✓ |
| row 2 | $2(1,2,0,3) + 3(0,0,1,1)$ | $= (2,4,3,9)$ ✓ |
| row 3 | $3(1,2,0,3) + 4(0,0,1,1)$ | $= (3,6,4,13)$ ✓ |

**(d)** Raising the rank to 3 (e.g. change the script's $a_{22}$ so column 2 is no longer $3a_1$): $\dim\mathbf{C}$ and $\dim\mathbf{C}(A^\mathsf{T})$ both rise to 3; $\dim\mathbf{N}$ falls to 1; $\dim\mathbf{N}(A^\mathsf{T})$ falls to 0. **Both sums still hold**, and the left null space becoming $\{0\}$ means every $b$ is now reachable — which is the interesting part.

---

## §5 — Clinic Notes

**Q3(b), which recipe.** §1's two "why" sentences. Refuse to re-derive.

**Q4(a), how many conditions.** $m - r$, and the zero rows of the rref are a free check. **PS 3's matrix has $m - r = 2$, so there are two** — students who found one have stopped early, and the count is how they catch it.

**Q5(c).** One word — *transpose* — and nothing more.

> **Do not work any part of PS 3 at the board.** Prof. Abara has office hours 10:00–11:00 tomorrow.

---

## What to Report Back

| Signal | What it means for Week 4 |
|---|---|
| §1's "lives in" column needed prompting | The four spaces are not placed. **Week 4 changes basis constantly and will be chaos**; re-establish before L13 |
| §2(d) answered "yes" | Expected, and worth correcting carefully — it is the misconception Week 8 has to clear |
| §3(d) justified only by "it contains the columns" | Half the argument. The dimension match is the other half; mention it in L13's recap |

---

*MATH 241 · Week 3 · Recitation 3 Solutions · © CSE Department*
