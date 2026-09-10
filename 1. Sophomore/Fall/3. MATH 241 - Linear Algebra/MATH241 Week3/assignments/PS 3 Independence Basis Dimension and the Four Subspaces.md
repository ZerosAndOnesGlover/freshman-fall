# MATH 241 · Problem Set 3
## Independence, Basis, Dimension, and the Four Subspaces

---

**Released:** Week 3, Wednesday · **Due:** Week 4, **Friday 17:00**
**Total: 100 points** · Submit one PDF, `PS3_{LastName}_{StudentID}.pdf`

> **Exact arithmetic throughout.**
>
> **A basis claim is two claims.** Independent *and* spanning — unless you invoke L11 §8's shortcut,
> in which case say so and say why it applies.
>
> **Always name the ambient space.** Four subspaces this week, two in $\mathbb{R}^m$ and two in
> $\mathbb{R}^n$; an answer in the wrong one is an object of the wrong kind.
>
> **Recitation 3 is the Thursday before this is due**, 15:00–15:50, SSB 108.

---

### Q1: Independence (18 points)

**(a) [6]** Decide whether each list is independent. **Give the dependency explicitly where there is one.**

1. $(1,2,1),\ (2,1,3),\ (3,3,4)$ in $\mathbb{R}^3$
2. $(1,0,1),\ (0,1,1),\ (1,1,1)$ in $\mathbb{R}^3$
3. $(1,2),\ (3,4),\ (5,6)$ in $\mathbb{R}^2$ — **answer this one without computing anything**
4. $1,\ x-1,\ (x-1)^2$ in $\mathbb{P}_2$

**(b) [4]** A student writes: *"$v_1, v_2, v_3$ are independent because no one of them is a scalar multiple of another."* **Give a specific counterexample** and state what the definition actually requires.

**(c) [4]** Prove: if $v_1, v_2, v_3$ are independent, then $v_1,\ v_1+v_2,\ v_1+v_2+v_3$ are independent.

**(d) [4]** Prove that any list containing the zero vector is dependent, straight from the definition. Then explain why this means **a basis can never contain $0$.**

---

### Q2: Basis and Dimension (20 points)

**(a) [5]** Find a basis for the plane $2x - y + 3z = 0$ in $\mathbb{R}^3$ and state its dimension. **Say which algorithm you used and why it applies.**

**(b) [5]** Find a basis for the space of $2\times2$ symmetric matrices and give its dimension. Then do the same for the $2\times2$ matrices of trace $0$. **What is the dimension of their intersection?** Exhibit a basis for it.

**(c) [4]** Is $\{(1,1,0),\ (0,1,1),\ (1,0,1)\}$ a basis for $\mathbb{R}^3$? **Use L11 §8's shortcut** — check one condition only, and state explicitly why the other comes free.

**(d) [6]** $V$ is a vector space with $\dim V = 6$.

- Can a list of 5 vectors span $V$? Can 7 vectors be independent in $V$? Justify each from L11 §4.
- $U \subseteq V$ is a subspace with $\dim U = 6$. Prove $U = V$.
- Give an example of a subspace of $\mathbb{P}_3$ with dimension exactly 2.

---

### Q3: The Four Subspaces (26 points)

Throughout Q3–Q4, let

$$P = \begin{bmatrix}1&2&0&1&3\\ 2&4&1&4&8\\ 0&0&1&2&2\\ 1&2&1&3&5\end{bmatrix} \qquad (4\times5)$$

**(a) [4]** Compute $\operatorname{rref}(P)$. State the rank, the pivot columns and the free columns.

**(b) [12]** Give a **basis** and the **dimension** for each of the four fundamental subspaces, and **state which $\mathbb{R}^k$ each lives in**. Set it out as a table.

> Take the column-space basis from the columns of $P$ and the row-space basis from the rows of
> $\operatorname{rref}(P)$. **Say why those two recipes differ** — one sentence, and it is the whole
> of L12 §3.

**(c) [4]** Verify both dimension sums, $r + (n-r) = n$ and $r + (m-r) = m$, with the numbers filled in.

**(d) [6]** Verify the orthogonality of L12 §7 **by direct computation**: every basis vector of $\mathbf{N}(P)$ against every basis vector of the row space, and every basis vector of $\mathbf{N}(P^\mathsf{T})$ against every basis vector of $\mathbf{C}(P)$. **How many dot products is that?** Tabulate them.

---

### Q4: What the Left Null Space Is For (18 points)

**(a) [5]** $\dim\mathbf{N}(P^\mathsf{T}) = m - r$. **How many independent solvability conditions does $Px = b$ therefore have?** Write them out explicitly as equations in $b_1, b_2, b_3, b_4$, using your basis from Q3(b).

**(b) [4]** Use those conditions — **not elimination** — to decide whether each is solvable: $\;(7,19,5,12)$, $\;(7,19,5,13)$, $\;(0,0,0,0)$.

**(c) [5]** For the solvable one from (b) with nonzero entries, give the **complete** solution. Check your particular solution against $P$.

**(d) [4]** Prove in general: if $Ax = b$ has a solution then $y^\mathsf{T}b = 0$ for every $y \in \mathbf{N}(A^\mathsf{T})$. *(Two lines.)* Then say what the converse would need, and which week supplies it.

---

### Q5: Rank (18 points)

**(a) [5]** $A$ is $6\times4$ with rank 4. Give the dimension of each of the four subspaces, say which are $\{0\}$, and answer: is $Ax = b$ solvable for every $b \in \mathbb{R}^6$? When solvable, is the solution unique?

**(b) [4]** Explain, in your own words and in no more than four sentences, **why row rank $=$ column rank is surprising.** Then give the proof from L12 §4 and say what it does *not* explain.

**(c) [4]** Prove $\operatorname{rank}(A) = \operatorname{rank}(A^\mathsf{T})$ follows immediately from L12 §3, and use it to show $\operatorname{rank}(AB) \le \min(\operatorname{rank}A, \operatorname{rank}B)$.

> *(You have $\mathbf{C}(AB) \subseteq \mathbf{C}(A)$ from PS 2 Q5(a). Apply it to $B^\mathsf{T}A^\mathsf{T}$
> for the other half.)*

**(d) [5]** $A$ is $10^6\times4$ with rank 4.

- What is $\operatorname{rank}(A^\mathsf{T}A)$? Justify from PS 2 Q5(c) and (c) above.
- What size is $A^\mathsf{T}A$, and is it invertible?
- **In one sentence: why does this make least squares computationally possible at all?**

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Independence | 18 |
| 2 | Basis and dimension | 20 |
| 3 | The four subspaces | 26 |
| 4 | What the left null space is for | 18 |
| 5 | Rank | 18 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*MATH 241 · Week 3 · PS 3 · © CSE Department*
