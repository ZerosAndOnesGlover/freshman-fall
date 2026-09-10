# MATH 241 · Quiz 3
## Administered: Monday, Week 3 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 2** — vector spaces, subspaces, the column space and the null space.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then mark it yourself before you leave the room.

---

**Q1.** State the three conditions of the subspace test. Which one should you check first, and why?

&nbsp;

&nbsp;

---

**Q2.** $A$ is $3\times5$. Which $\mathbb{R}^k$ does $\mathbf{C}(A)$ live in? $\mathbf{N}(A)$?

&nbsp;

&nbsp;

---

**Q3.** Is $\{(x,y) : x \ge 0\}$ a subspace of $\mathbb{R}^2$? Give a specific reason.

&nbsp;

&nbsp;

---

**Q4.** $\operatorname{rref}(A) = \begin{bmatrix}1&4&0&2\\ 0&0&1&5\\ 0&0&0&0\end{bmatrix}$. Give the rank, the number of special solutions, and one special solution.

&nbsp;

&nbsp;

---

**Q5.** Which of $\mathbf{C}(A)$ and $\mathbf{N}(A)$ is unchanged by elimination? Say why in one sentence.

&nbsp;

&nbsp;

---

**Q6.** $Ax_p = b$ and $b \ne 0$. Describe the full solution set. Is it a subspace?

&nbsp;

&nbsp;

---

**Q7.** $A$ is $4\times7$. Can $\mathbf{N}(A) = \{0\}$? Justify without computing anything.

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **(1) $0 \in W$; (2) closed under addition; (3) closed under scalar multiplication.**

**Check $0 \in W$ first** — it is a single substitution and it disposes of most non-examples immediately, including every set defined by an equation with a nonzero right-hand side. *(L07 §4.)*

---

**Q2.** $\mathbf{C}(A) \subseteq \mathbb{R}^3$ — the columns have three entries. $\mathbf{N}(A) \subseteq \mathbb{R}^5$ — $x$ has five entries.

*The columns live where $b$ lives; the null space lives where $x$ lives. **For a rectangular matrix these are different spaces and cannot be compared.***

---

**Q3.** **No.** It contains $0$ and is closed under addition, but **not under scaling**: $(1,0)$ is in it and $(-1)(1,0) = (-1,0)$ is not. *(L07 §4. A "no" needs the specific vector.)*

---

**Q4.** **Rank 2** (two pivots, columns 1 and 3). **Two special solutions** — free columns 2 and 4, and $n - r = 4 - 2 = 2$.

Setting $x_2 = 1, x_4 = 0$: $\;s_2 = (-4, 1, 0, 0)$. *(Or $x_4=1, x_2=0$: $\;s_4 = (-2, 0, -5, 1)$.)*

---

**Q5.** **$\mathbf{N}(A)$ is unchanged.** Every row operation is left multiplication by an **invertible** matrix $E$, so $Ax = 0 \iff EAx = 0$ — the implication runs both ways.

**$\mathbf{C}(A)$ is not**: a row operation mixes entries within each column, so it moves every column and the space they span moves too. *(L09 §2 and L08 §4.)*

---

**Q6.** $\{x_p + x_n : x_n \in \mathbf{N}(A)\}$ — the null space **translated** by $x_p$.

**Not a subspace:** it does not contain $0$, since $A0 = 0 \ne b$. Right shape, wrong place. *(L09 §6–§7.)*

---

**Q7.** **No.** $A$ has $n = 7$ columns and at most $m = 4$ pivots, so $r \le 4 < 7$ — **at least three free columns**, hence at least three nonzero special solutions.

*More unknowns than equations always gives a nontrivial null space. (L09 §4.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q3 | L07 §4 |
| **Q2** | **L08 §1 and L09 §1.** Two spaces, two rooms — **fix this today** |
| Q4 | L09 §2–§3 |
| **Q5** | **L08 §4 and L09 §2.** This week's L12 is built on it |
| Q6 | L09 §6 |
| Q7 | L09 §4 |

**Q2 and Q5 are the ones that recur.** Q2 because this week adds two *more* subspaces and you will need to place four of them; Q5 because L12's row space behaves the opposite way from the column space, and if the Week 2 pair is not solid the Week 3 pair will be noise.

---

*MATH 241 · Week 3 · Quiz 3 · covers Week 2 · ungraded*
