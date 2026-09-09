# MATH 241 · Problem Set 2
## Subspaces, the Column Space, and the Null Space

---

**Released:** Week 2, Wednesday · **Due:** Week 3, **Friday 17:00**
**Total: 100 points** · Submit one PDF, `PS2_{LastName}_{StudentID}.pdf`

> **Exact arithmetic throughout.** Fractions, not decimals.
>
> **A subspace claim needs the test, not an assertion.** "Yes, it is a subspace" earns nothing;
> the three conditions of L07 §4, checked, earn everything. **A *counter*example must be specific** —
> name the vectors that break it.
>
> **When you describe a subspace, say which $\mathbb{R}^k$ it lives in.** Half the marks lost on
> this paper are lost to $\mathbf{C}(A)$ and $\mathbf{N}(A)$ being placed in the same space.
>
> **Recitation 2 is the Thursday before this is due**, 15:00–15:50, SSB 108.

---

### Q1: Subspaces (20 points)

**(a) [10]** For each set, decide whether it is a subspace of the stated space. **If yes, verify all three conditions. If no, give the specific vectors that break it and say which condition fails.**

1. $\{(x,y,z) \in \mathbb{R}^3 : x - 2y + z = 0\}$
2. $\{(x,y,z) \in \mathbb{R}^3 : x - 2y + z = 5\}$
3. $\{(x,y,z) \in \mathbb{R}^3 : xyz = 0\}$
4. $\{(x,y,z) \in \mathbb{R}^3 : x \le y \le z\}$
5. $\{A \in \mathbb{R}^{2\times2} : A^\mathsf{T} = A\}$

**(b) [4]** The set of $2\times2$ matrices with $\det A = 0$ is **not** a subspace. Give two such matrices whose sum is invertible, and state which condition that violates.

**(c) [6]** $U$ and $W$ are subspaces of $V$.

- Prove $U \cap W$ is a subspace.
- Give $U, W \subseteq \mathbb{R}^2$ for which $U \cup W$ is **not**, with the specific failing vectors.
- State the one circumstance under which $U \cup W$ *is* a subspace, and prove it is the only one.

---

### Q2: The Column Space (22 points)

Throughout Q2–Q4, let

$$B = \begin{bmatrix}1 & 2 & 0 & 3\\ 2 & 4 & 1 & 8\\ 1 & 2 & 1 & 5\end{bmatrix}.$$

**(a) [4]** Compute $\operatorname{rref}(B)$. State the pivot columns, the free columns, and the rank.

**(b) [5]** Write down a spanning set for $\mathbf{C}(B)$, **taken from the columns of $B$**. Say which $\mathbb{R}^k$ it lives in, and describe it geometrically.

**(c) [5]** Find the single equation $\alpha b_1 + \beta b_2 + \gamma b_3 = 0$ satisfied by every $b \in \mathbf{C}(B)$. **Verify it on all four columns of $B$**, not just the ones you used to derive it.

**(d) [4]** Use your equation to decide, **without eliminating**, which of these are in $\mathbf{C}(B)$: $(6,15,9)$, $(6,15,10)$, $(0,0,0)$, $(1,3,2)$.

**(e) [4]** $\mathbf{C}(B)$ and $\mathbf{C}(\operatorname{rref} B)$ are **different** subspaces. Give the equation of each and exhibit a vector in one and not the other. Then say, in one sentence, what elimination *does* preserve.

---

### Q3: The Null Space (22 points)

**(a) [8]** Find the special solutions of $Bx = 0$ and write $\mathbf{N}(B)$ explicitly. **Verify each special solution against $B$ itself**, not against $\operatorname{rref}(B)$. Say which $\mathbb{R}^k$ it lives in and give its dimension.

**(b) [5]** Each special solution states a dependency among the columns of $B$. **Write both dependencies as equations in $b_1, b_2, b_3, b_4$** — the columns — and verify both by direct addition.

**(c) [4]** Confirm rank + nullity $= n$ for $B$. Then, for

$$B' = \begin{bmatrix}1&2&1&3&2\\ 2&4&3&8&5\\ 0&0&1&2&1\\ 1&2&2&5&3\end{bmatrix}$$

state $m$, $n$, the rank, and the nullity — **without computing the null space itself.** *(You will need $\operatorname{rref}(B')$ for the rank; the nullity follows by counting.)*

**(d) [5]** Prove that $\mathbf{N}(A) = \mathbf{N}(\operatorname{rref} A)$ for every $A$, using the fact that each row operation is left multiplication by an invertible matrix. **Both directions.** Then say in one sentence why the same argument does *not* work for the column space.

---

### Q4: The Complete Solution (20 points)

**(a) [8]** Solve $Bx = (6, 15, 9)$ completely. Give a particular solution, the null-space part, and the full set. **Check your particular solution against $B$.**

**(b) [4]** Verify that $(1,1,1,1)$ is in your solution set by finding the coefficients $t, u$ that produce it.

**(c) [4]** Now solve $Bx = (6, 15, 10)$. Quote the row of $\operatorname{rref}[\,B \mid b\,]$ that settles it, and say which part of Q2 predicted this before any elimination.

**(d) [4]** A classmate solves (a) and gets a different particular solution from yours. **Is one of you wrong?** Answer precisely, and state what *is* uniquely determined by the problem.

---

### Q5: Structure (16 points)

**(a) [4]** Prove $\mathbf{C}(AB) \subseteq \mathbf{C}(A)$ for any conformable $A, B$. *(You proved this in PS 1 Q1(c) without the vocabulary.)* Give $A, B$ where the containment is **strict**.

**(b) [4]** Prove $\mathbf{N}(A) \subseteq \mathbf{N}(BA)$. Give $A, B$ where it is strict.

**(c) [8]** Prove $\;\mathbf{N}(A^\mathsf{T}A) = \mathbf{N}(A)\;$ for every real $A$.

> One direction is (b). For the other, suppose $A^\mathsf{T}Ax = 0$ and consider the scalar
> $x^\mathsf{T}A^\mathsf{T}Ax$. Show it equals $\lVert Ax\rVert^2$, and conclude.

Then answer: **$A$ is $10^6 \times 3$ with rank 3. What are the dimensions of $A^\mathsf{T}A$, and is it invertible?** Justify from the result you just proved. *(This is the fact Week 9's least squares runs on, and Week 1's L06 §2 is why $A^\mathsf{T}A$ was worth forming at all.)*

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Subspaces | 20 |
| 2 | The column space | 22 |
| 3 | The null space | 22 |
| 4 | The complete solution | 20 |
| 5 | Structure | 16 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*MATH 241 · Week 2 · PS 2 · © CSE Department*
