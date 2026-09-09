# MATH 241 · Recitation 1 — Solutions and Session Notes
## **INSTRUCTOR ONLY** · Do not distribute

**Session:** Thursday of Week 2, 15:00–15:50, SSB 108 · covers Week 1 · unmarked
**PS 1 is due 17:00 the following day.**

---

## Running the Session

**§2(b) is the session.** Everything else can be compressed. The confusion between *"a swap was discovered at step 2"* and *"$P$ permutes the original matrix"* is the one Week 1 misconception that survives into Week 9, where it reappears as $A = QR$ with column pivoting and is much harder to unpick there.

| | Section | Budget | If it overruns |
|---|---|---|---|
| §1 | Four readings | 10 min | Cut to 5; keep (c) |
| §2 | Building $L$, and $PA = LU$ | 15 min | **Protect. Cut §1 and §3 instead** |
| §3 | The machine | 10 min | Demo (a) from the front, skip (b) |
| §4 | Clinic | 5 min | Help Desk |

---

## §1 — Four Readings

$$AB = \begin{bmatrix}2&-1\\1&3\end{bmatrix}\begin{bmatrix}1&0&4\\2&5&-1\end{bmatrix} = \begin{bmatrix}0&-5&9\\ 7&15&1\end{bmatrix}$$

*By columns:* $A$'s columns are $(2,1)$ and $(-1,3)$, and each column of $B$ supplies the amounts —
$Ab_1 = 1(2,1) + 2(-1,3) = (0,7)$ · $Ab_2 = 0(2,1) + 5(-1,3) = (-5,15)$ · $Ab_3 = 4(2,1) - 1(-1,3) = (9,1)$.

*By rows:* row 1 of $AB$ is $2(1,0,4) - 1(2,5,-1) = (0,-5,9)$; row 2 is $1(1,0,4) + 3(2,5,-1) = (7,15,1)$.

**(a)** $A$ has **two** columns, so reading (iv) gives a sum of **two** matrices, each $2\times3$:

$$\begin{bmatrix}2\\1\end{bmatrix}\begin{bmatrix}1&0&4\end{bmatrix} + \begin{bmatrix}-1\\3\end{bmatrix}\begin{bmatrix}2&5&-1\end{bmatrix}
= \begin{bmatrix}2&0&8\\1&0&4\end{bmatrix} + \begin{bmatrix}-2&-5&1\\6&15&-3\end{bmatrix} = \begin{bmatrix}0&-5&9\\7&15&1\end{bmatrix}\ ✓$$

**What is special about each piece:** every row is a multiple of the same row, and every column a multiple of the same column. *(That is what rank one means. Accept any phrasing of it; the word arrives in Week 3.)*

**(b)** $BA$ does **not** exist. $B$ is $2\times3$ so it maps $\mathbb{R}^3 \to \mathbb{R}^2$; $A$ is $2\times2$ so it maps $\mathbb{R}^2\to\mathbb{R}^2$. **"$A$ first, then $B$" would feed a vector of $\mathbb{R}^2$ into a function that expects $\mathbb{R}^3$.** There is no composition to name.

*Insist on the function phrasing. "The inner dimensions don't match" is the symptom; this is the reason.*

**(c) Not a contradiction, and this is the question worth the section.**

$AB$ has three columns; each is a combination of $A$'s **two** columns. So all three live in the span of two vectors — a plane in $\mathbb{R}^2$, which here is all of $\mathbb{R}^2$. **The three columns of $AB$ cannot be independent; there must be a linear relation among them**, and indeed $\;9\,\text{col}_1 + ?\dots$ — any relation will do, and finding one is a good sixty seconds if the room is quick.

> **Say this out loud:** "the number of columns of $AB$ can exceed the number of columns of $A$, but
> the number of *independent* ones cannot." That sentence is
> $\operatorname{rank}(AB) \le \operatorname{rank}(A)$, which is Week 3, and they have just derived it.

---

## §2 — $L$ Is Not Computed

### (a) The prepared factorisation

$$F = \begin{bmatrix}2&1&0\\4&5&3\\-2&5&10\end{bmatrix}, \qquad
L = \begin{bmatrix}1&0&0\\ \mathbf{2}&1&0\\ \mathbf{-1}&\mathbf{2}&1\end{bmatrix}, \qquad
U = \begin{bmatrix}2&1&0\\0&3&3\\0&0&4\end{bmatrix}$$

Multipliers $\ell_{21} = 2$, $\ell_{31} = -1$, $\ell_{32} = 2$. Check row 3 of $LU$: $-1(2,1,0) + 2(0,3,3) + (0,0,4) = (-2, -1+6, 6+4) = (-2, 5, 10)$ ✓

*The error to expect is $L_{31} = +1$, from writing the multiplier with the sign of the operation ($R_3 + R_1$) rather than the sign of $\ell$. **Let the pairs catch it by multiplying out.***

### (b) The mid-elimination swap

$$G = \begin{bmatrix}1&2&3\\ 2&4&1\\ 3&5&2\end{bmatrix} \xrightarrow[\ell_{31}=3]{\ell_{21}=2} \begin{bmatrix}1&2&3\\ 0&\mathbf{0}&-5\\ 0&-1&-7\end{bmatrix}$$

**(i)** The $(2,2)$ entry is $0$. **Case A, fixable** — row 3 has $-1$ below it in column 2. **The test is: look down the column below the pivot row for a nonzero.** Nothing else.

**(ii)** Swap rows 2 and 3:

$$\begin{bmatrix}1&2&3\\ 0&-1&-7\\ 0&0&-5\end{bmatrix} \qquad \text{pivots } 1,\ -1,\ -5$$

Already triangular; no further elimination. Multipliers along this route: $\ell_{21}=2$, $\ell_{31}=3$, then $\ell_{32}=0$ after the swap.

**(iii)** The swap exchanged rows 2 and 3, so

$$P = \begin{bmatrix}1&0&0\\ 0&0&1\\ 0&1&0\end{bmatrix}, \qquad PG = \begin{bmatrix}1&2&3\\ 3&5&2\\ 2&4&1\end{bmatrix}$$

Eliminating $PG$ from scratch: $\ell_{21} = 3$ gives $[\,0\ -1\ -7\,]$; $\ell_{31} = 2$ gives $[\,0\ \ 0\ -5\,]$; $\ell_{32} = 0$.

$$L = \begin{bmatrix}1&0&0\\ \mathbf{3}&1&0\\ \mathbf{2}&\mathbf{0}&1\end{bmatrix}, \qquad U = \begin{bmatrix}1&2&3\\ 0&-1&-7\\ 0&0&-5\end{bmatrix}, \qquad PG = LU \ ✓$$

**It goes through with no swap.** That is the whole point of doing the exchanges up front.

**(iv)** **$U$ is identical** in (ii) and (iii) — same pivots $1, -1, -5$, same entries.

**The multipliers are not.** Route (ii) produced $2, 3, 0$; route (iii) produced $3, 2, 0$. **The swap exchanged them along with the rows they belong to.** $L$'s rows are permuted exactly as $G$'s were, which is what makes $PG = LU$ work and $G = LU$ fail.

> **The closing sentence, and it is the reason the section exists:**
> *the swap is discovered during the elimination, but it is a fact about the original matrix, and
> $P$ is applied there.* LAPACK records interchanges in the integer vector `ipiv` as it goes and
> never re-runs anything — but what it returns factors $PA$. **Code that calls `lu_factor` and then
> forgets to apply the permutation is the most common bug in this area**, and it produces answers
> that are wrong by a reordering, which is exactly the kind of wrong that survives a spot check.

---

## §3 — The Machine

**(a)** From `matrices.py` on the reference machine:

| $n$ | Solve | $H^{-1}b$ | Times worse |
|---:|---:|---:|---:|
| 6 | $5.27\times10^{-11}$ | $1.06\times10^{-9}$ | $20.1$ |
| 8 | $1.37\times10^{-7}$ | $5.60\times10^{-7}$ | $4.1$ |
| 10 | $7.18\times10^{-4}$ | $1.47\times10^{-3}$ | $2.0$ |
| 12 | $5.95\times10^{-3}$ | $0.54$ | $90.7$ |
| 14 | $6.26$ | $22.1$ | $3.5$ |

**Alarming, and the argument is worth having.** A penalty that grew predictably with $n$ could be budgeted for — you would know what inverting costs you and could decide it was affordable. **This one cannot be predicted from anything you know before running it**, so the only safe policy is not to incur it. *"It is only $2\times$ at $n=10$" is not a defence when the same code at $n = 12$ is $91\times$ worse.*

*Push back on any pair that answers "reassuring, because it doesn't grow". Ask them what they would tell a colleague who wanted a bound.*

**(b)** $K$: **13 nonzeros of 25.** $K^{-1}$: **25 of 25** — not one zero.

At $n = 10^6$: $K^{-1}$ has $10^{12}$ entries at 8 bytes = **8 terabytes**. $L$ and $U$ keep the band — about $2 \times 2\times10^6$ entries = **32 megabytes.**

**A factor of 250,000, and it is the difference between a computation that runs on a laptop and one that runs nowhere.** The flop argument says inverting is six times slower; this one says it is impossible. **In practice this is the argument that changes behaviour.**

**(c)** Flop ratio 750, measured speedup ≈ 787. **The flop count is not counting memory.** $(AB)C$ allocates, writes and re-reads an 8 MB intermediate that does not fit in cache; $A(BC)$ never creates it. Flops are the right first-order model and they are not the whole cost — **which is CS 201 Week 6's entire subject**, and worth naming if anyone in the room is taking it.

---

## §4 — Clinic Notes

**Q1(c).** If §1(c) landed, say so and refuse to re-derive. The transfer is the exercise.

**Q4(c), the $P$.** §2(b)(iii) is the same question. The unstick line: *"which matrix does your $P$ multiply — the one you started with, or the one you were holding when you noticed?"*

**Q5(b), the rule.** Do **not** give it. The productive prompt is: *"write your candidate rule down, then check it against part (a). If it gets (a) wrong, it is not the rule."* Most students propose "associate right", check it, and find the answer themselves in ninety seconds.

> **Do not work any part of PS 1 at the board.** The numbers here differ from the paper's for that
> reason. Prof. Abara has office hours 10:00–11:00 tomorrow, before the 17:00 deadline.

---

## What to Report Back

| Signal | What it means for Week 2 |
|---|---|
| §1(c) needed heavy prompting | The column-space idea is not there. **Week 2's L07 must open slowly**; do not assume Week 1 built it |
| §2(b)(iv) — pairs said the multipliers were unchanged | They are treating $L$ as a formula rather than a record. Re-state it at the start of L07 |
| §3(a) argued "reassuring" | Fine. It is a judgement call and the argument is the value, not the verdict |

---

*MATH 241 · Week 1 · Recitation 1 Solutions · © CSE Department*
