# MATH 241 · Recitation 2 — Solutions and Session Notes
## **INSTRUCTOR ONLY** · Do not distribute

**Session:** Thursday of Week 3, 15:00–15:50, SSB 108 · covers Week 2 · unmarked
**PS 2 is due 17:00 the following day.**

---

## Running the Session

**§2 is the session.** "Elimination preserves $\mathbf{N}$ and moves $\mathbf{C}$" is the one Week 2 idea students carry away wrong, and it does not stay contained — it comes back in Week 3 as *row rank = column rank* and in Week 9 as a genuine bug in least-squares code.

| | Section | Budget | If it overruns |
|---|---|---|---|
| §1 | Which $\mathbb{R}^k$ | 10 min | Cut to 5, keep (d) |
| §2 | The one that moves | 15 min | **Protect. Cut §3 and §4 first** |
| §3 | Complete solutions | 10 min | Do (a) and (c) only |
| §4 | The machine | 10 min | Demo (b) from the front |
| §5 | Clinic | 5 min | Help Desk |

---

## §0 / §1 — The Prepared Matrix

$$M = \begin{bmatrix}2&4&1&3\\ 1&2&0&1\\ 3&6&2&5\end{bmatrix} \qquad \operatorname{rref}(M) = \begin{bmatrix}1&2&0&1\\ 0&0&1&1\\ 0&0&0&0\end{bmatrix}$$

**Pivot columns 1 and 3; free columns 2 and 4; rank $r = 2$.**

**(a)** $\mathbf{C}(M) \subseteq \mathbb{R}^3$ (three rows — the columns have three entries). $\mathbf{N}(M) \subseteq \mathbb{R}^4$ (four columns — $x$ has four entries).

*Make them say the two numbers before anything is written. The pairs that hesitate here are the ones who will lose PS 2 Q3(a).*

**(b)** $\mathbf{C}(M)$ is at most all of $\mathbb{R}^3$, dimension 3. $\mathbf{N}(M)$ is at most all of $\mathbb{R}^4$, dimension 4 — **though the second is only achievable if $M = 0$.**

**(c)** $\dim\mathbf{C}(M) = r = 2$; $\dim\mathbf{N}(M) = n - r = 4 - 2 = 2$. They add to **$n = 4$, the number of columns** — not to $m = 3$.

> **The reason, and it is worth the thirty seconds:** every column is either a pivot column or a
> free one, and there is nothing else to be. The rank counts the first kind and the nullity the
> second. **It is a statement about columns, so it adds to the number of columns.** Students who
> add to $m$ have memorised a formula rather than a count.

**(d)** Four columns living in $\mathbb{R}^3$. **Four vectors in a 3-dimensional space cannot be independent**, so some combination of them is zero, so some nonzero $x$ has $Mx = 0$. Equivalently: $r \le m = 3 < 4 = n$, so there is always at least one free column. **No computation required.**

---

## §2 — The One That Moves

### (a)

$$\mathbf{C}(M) = \operatorname{span}\left\{\begin{bmatrix}2\\1\\3\end{bmatrix}, \begin{bmatrix}1\\0\\2\end{bmatrix}\right\} \qquad \mathbf{C}(\operatorname{rref}M) = \operatorname{span}\left\{\begin{bmatrix}1\\0\\0\end{bmatrix}, \begin{bmatrix}0\\1\\0\end{bmatrix}\right\}$$

*Columns 1 and 3 of each. **Watch for pairs taking columns 1 and 3 of the rref and calling it $\mathbf{C}(M)$** — that is the error the section exists to catch, and it is worth interrupting for.*

### (b)

For $\mathbf{C}(M)$, find $(\alpha,\beta,\gamma)$ killing both spanning columns:

$$2\alpha + \beta + 3\gamma = 0, \qquad \alpha + 2\gamma = 0$$

The second gives $\alpha = -2\gamma$; then $-4\gamma + \beta + 3\gamma = 0$, so $\beta = \gamma$. Take $\gamma = -1$:

$$\mathbf{C}(M) = \{\,b : 2b_1 - b_2 - b_3 = 0\,\} \qquad\qquad \mathbf{C}(\operatorname{rref}M) = \{\,b : b_3 = 0\,\}$$

Check all four columns of $M$ against the first: $(2,1,3) \to 4-1-3 = 0$ ✓ · $(4,2,6) \to 8-2-6=0$ ✓ · $(1,0,2) \to 2-0-2=0$ ✓ · $(3,1,5) \to 6-1-5=0$ ✓

### (c)

**Different planes.** A separating vector:

| $v$ | $2b_1 - b_2 - b_3$ | $b_3$ | |
|---|---:|---:|---|
| $(1,0,0)$ | $2$ | $0$ | in $\mathbf{C}(\operatorname{rref}M)$ **only** |
| $(1,0,2)$ | $0$ | $2$ | in $\mathbf{C}(M)$ **only** |
| $(1,2,0)$ | $0$ | $0$ | **in both** — the trap |

*Accept either of the first two, verified. **A pair that offers $(1,2,0)$ has guessed rather than checked**, and the sheet warned them; make them check.*

### (d)

$$\mathbf{N}(M) = \mathbf{N}(\operatorname{rref}M) = \operatorname{span}\{(-2,1,0,0),\ (-1,0,-1,1)\}$$

**Identical**, and the sentence: each row operation is left multiplication by an **invertible** matrix $E$, so $Mx = 0 \iff EMx = 0$ — the implication runs both ways precisely because $E^{-1}$ exists.

*Verify the specials against $M$ at the board, since PS 2 Q3(a) asks for exactly that:*
$-2(2,1,3) + (4,2,6) = (0,0,0)$ ✓ and $-(2,1,3) - (1,0,2) + (3,1,5) = (0,0,0)$ ✓

### (e) — the discussion

**The answer to steer toward:**

A row operation combines **entries within each column**. So every column moves, and the space they span moves with them — $\mathbf{C}$ is a statement about *where the columns are*, and they are no longer there.

$x$ is untouched. $\mathbf{N}$ is a statement about *which combinations of the columns vanish* — the relations among them — and elimination is designed to expose exactly those relations without altering them. **Relations survive; positions do not.**

> **The compression to leave on the board:**
> $\mathbf{C}$ asks *where the columns are.* $\mathbf{N}$ asks *how the columns depend on each
> other.* Elimination moves them and preserves the dependencies, so it destroys the first answer and
> is the tool for computing the second.

*If a pair gets there unprompted, tell them they have just explained why Week 3's "row rank = column rank" is surprising: two counts that survive an operation that moves both spaces.*

---

## §3 — Complete Solutions at Speed

**(a)** $b = (3,1,5)$: $2(3) - 1 - 5 = 0$ ✓ **solvable.**

*The one-line alternative:* $b = (3,1,5)$ **is column 4 of $M$**, so $x = (0,0,0,1)$ solves it on sight. Either answer is right; a pair that spots the column has read the matrix rather than processed it.

**(b)**

$$[\,M\mid b\,] \longrightarrow \left[\begin{array}{cccc|c}1&2&0&1&1\\ 0&0&1&1&1\\ 0&0&0&0&0\end{array}\right] \Rightarrow x_p = (1,0,1,0)$$

$$Mx_p = (2,1,3) + (1,0,2) = (3,1,5)\ ✓$$

$$x = (1,0,1,0) + t(-2,1,0,0) + u(-1,0,-1,1)$$

**(c)** The "obvious" solution $(0,0,0,1)$ from (a) is in the set: take $t = 0$, $u = 1$, giving $(1,0,1,0) + (-1,0,-1,1) = (0,0,0,1)$ ✓

**Two different particular solutions, one solution set.** This is PS 2 Q4(d), and a pair that has done it here can answer that question in a sentence.

**(d)** $b = (3,1,6)$: $2(3) - 1 - 6 = -1 \ne 0$. **Not solvable.** *One subtraction settles it.* Eliminating anyway gives a last row $(0,0,0,0\mid 1)$.

---

## §4 — The Machine

**(a)** The script's matrix has $\mathbf{C}(A) = \{5b_1 - 2b_2 + b_3 = 0\}$ and $\mathbf{C}(\operatorname{rref}A) = \{b_3 = 0\}$. **Same phenomenon, different plane** — which is the point of running it on a second matrix.

**(b)**

- **$\{xyz = 0\}$** — closed under scaling, **not** under addition: $(1,1,0) + (0,0,1) = (1,1,1)$.
- **$\{x \ge 0\}$** — closed under addition, **not** under scaling: $(-1)(1,0) = (-1,0)$.

**Opposite failures, and both contain $0$.** That is why the test has three conditions and why checking one is worthless.

**(c)** A second reason the invertible matrices fail: **$0$ is not invertible**, so condition 1 fails outright. *(The $I + (-I)$ example is closure under addition. Either alone is fatal; having both is the point.)*

**(d)** Editing the script's `A` to $M$ should print rank 2, free columns 2 and 4, and the two specials from §2(d). **If a pair's hand computation disagrees, the script is right and finding the discrepancy is the exercise** — send them to compare the rref row by row rather than re-deriving.

---

## §5 — Clinic Notes

**Q2(b), which columns.** If §2(a) landed, refuse to re-derive; say "you did this twenty minutes ago."

**Q4(d), "is one of us wrong".** §3(c) is that question. The prompt: *"you and your partner had different $x_p$ half an hour ago — was one of you wrong then?"*

**Q5(c), $\mathbf{N}(A^\mathsf{T}A) = \mathbf{N}(A)$.** Give exactly one hint and stop: *multiply $A^\mathsf{T}Ax = 0$ on the left by $x^\mathsf{T}$, and ask what the resulting scalar is.* Do **not** say "norm"; that is the step worth having.

> **Do not work any part of PS 2 at the board.** Prof. Abara has office hours 10:00–11:00 tomorrow,
> before the 17:00 deadline.

---

## What to Report Back

| Signal | What it means for Week 3 |
|---|---|
| §1(a) hesitated | The two spaces are still one blur. **Week 3's L10 must re-establish it before independence** |
| §2(e) needed the answer given | Expected — it is the hardest thing in Week 2. But note it, because "row rank = column rank" will land as arbitrary rather than surprising |
| §1(c) added to $m$ | Rank–nullity is being recalled, not counted. Re-derive it from free columns at the start of L10 |

---

*MATH 241 · Week 2 · Recitation 2 Solutions · © CSE Department*
