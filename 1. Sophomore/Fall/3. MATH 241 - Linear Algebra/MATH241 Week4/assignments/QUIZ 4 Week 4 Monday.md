# MATH 241 · Quiz 4
## Administered: Monday, Week 4 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 3** — independence, basis, dimension, and the four fundamental subspaces.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then mark it yourself before you leave the room.

---

**Q1.** Define linear independence. Then give three vectors in $\mathbb{R}^2$, no one a multiple of another, that are dependent.

&nbsp;

&nbsp;

---

**Q2.** $A$ is $3\times7$ with rank 3. Give the dimension of all four fundamental subspaces, and say which $\mathbb{R}^k$ each lives in.

&nbsp;

&nbsp;

---

**Q3.** A basis is two things. Name them, and say which one gives *existence* of coordinates and which gives *uniqueness*.

&nbsp;

&nbsp;

---

**Q4.** $\operatorname{rref}(A) = \begin{bmatrix}1&3&0\\0&0&1\\0&0&0\end{bmatrix}$. Give a basis for the row space, and say why you may read it off the rref — when a column-space basis may not be.

&nbsp;

&nbsp;

---

**Q5.** $\dim\mathbf{N}(A^\mathsf{T}) = 2$. What does that tell you about solving $Ax = b$?

&nbsp;

&nbsp;

---

**Q6.** $V$ has dimension 4. Can 5 vectors in $V$ be independent? Can 3 span it?

&nbsp;

&nbsp;

---

**Q7.** State row rank $=$ column rank, and say in one sentence why it is surprising.

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **$c_1v_1 + \dots + c_kv_k = 0$ forces every $c_i = 0$** — the trivial combination is the only one giving zero.

$(1,0)$, $(0,1)$, $(1,1)$: no one is a multiple of any other, and $(1,0) + (0,1) - (1,1) = 0$. *(Any three vectors in $\mathbb{R}^2$ are dependent — L10 §4.)*

---

**Q2.** $m = 3$, $n = 7$, $r = 3$.

| | | |
|---|---|---|
| $\mathbf{C}(A) \subseteq \mathbb{R}^3$ | $\dim 3$ | all of $\mathbb{R}^3$ |
| $\mathbf{N}(A) \subseteq \mathbb{R}^7$ | $\dim 4$ | $n - r$ |
| $\mathbf{C}(A^\mathsf{T}) \subseteq \mathbb{R}^7$ | $\dim 3$ | |
| $\mathbf{N}(A^\mathsf{T}) \subseteq \mathbb{R}^3$ | $\dim 0$ | $= \{0\}$ |

*$3 + 4 = 7$ and $3 + 0 = 3$ ✓. Full row rank: **every $b$ is reachable**, and no solution is unique.*

---

**Q3.** **Independent** and **spanning**.

**Spanning gives existence** — every vector is reachable, so coordinates exist. **Independence gives uniqueness** — two representations subtract to a vanishing combination, forcing the coefficients to agree. *(L11 §1.)*

---

**Q4.** **Row space basis: $(1,3,0)$ and $(0,0,1)$** — the nonzero rows of the rref.

**Allowed because elimination combines rows**, so the span of the rows is unchanged and (the operations being invertible) nothing is lost. **The column space is different**: row operations mix entries *within* each column, so every column moves and the space they span moves with it — a column-space basis must be read back from $A$ at the pivot positions. *(L12 §3.)*

---

**Q5.** **There are two independent solvability conditions on $b$**, one per dimension of $\mathbf{N}(A^\mathsf{T})$: for each basis vector $y$, $Ax = b$ requires $y^\mathsf{T}b = 0$.

*Equivalently $\operatorname{rref}(A)$ has two zero rows, and $\mathbf{C}(A)$ is a proper subspace of $\mathbb{R}^m$ of codimension 2. (L12 §5.)*

---

**Q6.** **5 independent: no.** A basis of 4 spans, and an independent list never exceeds a spanning list (L11 §4).

**3 spanning: no.** If 3 spanned, an independent list would be capped at 3 — but a basis has 4 and is independent.

---

**Q7.** **$\dim\mathbf{C}(A) = \dim\mathbf{C}(A^\mathsf{T})$** — the number of independent columns equals the number of independent rows.

**Surprising because** the columns are $n$ vectors in $\mathbb{R}^m$ and the rows are $m$ vectors in $\mathbb{R}^n$ — different vectors, different counts of them, different ambient spaces — with no evident reason the two maximal independent counts should agree. *(L12 §4.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1 | L10 §1 |
| **Q2** | **L12 §3.** Four spaces, four dimensions, two ambient spaces — **this is the week's core** |
| Q3 | L11 §1 |
| **Q4** | **L12 §3.** The asymmetry is a consequence, not a pair of recipes |
| Q5 | L12 §5 |
| Q6 | L11 §4 |
| Q7 | L12 §4 |

**Q2 and Q4 are the ones that recur.** Week 8 takes orthogonal complements of exactly these four spaces, and Week 11 hands all four an orthonormal basis at once. **A student who cannot place them now will find both weeks unreadable.**

---

*MATH 241 · Week 4 · Quiz 4 · covers Week 3 · ungraded*
