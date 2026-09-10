# MATH 241 · Problem Set 11
## The Singular Value Decomposition

---

**Released:** Week 11, Wednesday · **Due:** Week 12, **Friday 17:00**
**Total: 100 points** · Submit one PDF, `PS11_{LastName}_{StudentID}.pdf`

> **Thanksgiving recess falls between release and deadline** — no classes Nov 24. You have two
> calendar weeks and one teaching week. **PS 12 is also due that Friday**, and it is short. **Do Q1
> and Q2 before the break**, while L33 and L34 are fresh.
>
> **Exact arithmetic in Q1–Q3.** Every matrix here has a rational SVD. **If a square root refuses to
> come out, you have made an arithmetic error** — check $\sigma_1\sigma_2$ and $\sum\sigma_k^2$
> against the entries before going further.
>
> **Q4 is run on a computer**, using `resources/svd.py`. **Q4 asks you to predict before you
> measure, and the prediction carries marks** — write it down first.
>
> **Recitation 11 is the Thursday before this is due.** **Collaboration on approaches is fine; the
> write-up must be yours.**

---

### Q1: The SVD by Hand, of a Wide Matrix (22 points)

$$W = \begin{bmatrix}-2&8&20\\ 14&19&10\end{bmatrix} \qquad (2\times3)$$

**(a) [4]** Compute $WW^\mathsf{T}$ — **the $2\times2$ product, not the $3\times3$** — and its eigenvalues. Give $\sigma_1$ and $\sigma_2$, and check $\sigma_1^2 + \sigma_2^2$ against the sum of the squares of the six entries.

**(b) [6]** Find unit eigenvectors $u_1, u_2$ of $WW^\mathsf{T}$. **Then compute $v_k = W^\mathsf{T}u_k/\sigma_k$** — the mirror image of L33 §2's construction — and verify that $v_1$ and $v_2$ are orthonormal. *(Their entries are in thirds.)*

**(c) [4]** $W$ is $2\times3$, so $V$ needs a third column. **Find $v_3$**, verify $Wv_3 = 0$, and say which of the four subspaces it spans.

**(d) [4]** Write the full SVD $W = U\Sigma V^\mathsf{T}$, giving the **size** of each factor. Multiply out the $(1,3)$ entry and confirm it is $20$.

**(e) [4]** Give the best rank-one approximation $W_1$ **as a matrix of integers**. State $\lVert W - W_1\rVert_2$ and $\lVert W - W_1\rVert_F$ **without computing $W - W_1$**, then compute $W - W_1$ and check both.

---

### Q2: Four Subspaces and the Pseudoinverse (22 points)

$$N = \begin{bmatrix}0&2&4\\ 4&6&4\\ 2&5&6\end{bmatrix}, \qquad N^\mathsf{T}N = \begin{bmatrix}20&34&28\\ 34&65&62\\ 28&62&68\end{bmatrix}.$$

You are told $v_1 = \tfrac13(1,2,2)$ and $v_2 = \tfrac13(-2,-1,2)$.

**(a) [6]** Verify that $v_1$ and $v_2$ are eigenvectors of $N^\mathsf{T}N$, and read off $\sigma_1$ and $\sigma_2$. Compute $u_1$ and $u_2$. **Then find $u_3$ and $v_3$** — each is forced, up to sign, by orthogonality. What is $\sigma_3$?

**(b) [5]** Give an orthonormal basis for each of $\mathbf{C}(N)$, $\mathbf{N}(N^\mathsf{T})$, $\mathbf{C}(N^\mathsf{T})$, $\mathbf{N}(N)$. **Verify the two null-space claims by multiplication.**

**(c) [6]** Compute $N^+ = V\Sigma^+U^\mathsf{T}$ **exactly**. Verify $NN^+N = N$. Then compute $NN^+$, and show it equals $I - u_3u_3^\mathsf{T}$ — **say in one sentence why it had to.**

**(d) [5]** For $b = (0, 9, 9)$: find $x^+ = N^+b$, the projection $p = Nx^+$, and the residual $e$. **Check $N^\mathsf{T}e = 0$.** Then write down **every** least-squares solution, and show $x^+$ is the shortest by computing the length of the general one.

---

### Q3: Approximation and Rank, Without a Computer (16 points)

**(a) [5]** A $4\times4$ matrix $A$ has singular values $10$, $6$, $3$, $1$. Give $\lVert A\rVert_2$, $\lVert A\rVert_F$, $\operatorname{cond}_2(A)$, $\lVert A - A_1\rVert_2$, $\lVert A - A_2\rVert_F$, and the fraction of $\lVert A\rVert_F^2$ kept by $A_2$.

**(b) [5]** A $600\times800$ greyscale image is stored as its rank-$40$ approximation. **How many numbers are stored**, and what fraction of the original is that? **Above what rank $k$ does the "compressed" version take more storage than the image?**

**(c) [6]** A $5\times5$ matrix has computed singular values

$$7.2, \qquad 3.1, \qquad 0.9, \qquad 4\times10^{-9}, \qquad 3\times10^{-15}.$$

**What rank would you report**

- **(i)** if its entries were measured to three significant figures;
- **(ii)** if they were exact and you used `numpy`'s default threshold, $\sigma_1\cdot\max(m,n)\cdot2.2\times10^{-16}$;
- **(iii)** if you counted nonzero pivots in exact rational arithmetic, and these singular values were themselves exact?

**Justify each in a sentence.** The three answers should differ.

---

### Q4: On the Machine (20 points)

Run `resources/svd.py`. **Write each prediction down before you run anything.**

**(a) [7]** In `picture()`, add a fourth shape: the diagonal stroke `abs(4*i - 3*j) <= 3`.

- **Predict**, before measuring: the numerical rank of **the diagonal on its own**, and of **the whole picture with it added**. *(The original picture has rank 7.)*
- **Measure** both, and for each report the smallest $k$ that keeps $99\%$ of the energy.
- **Explain the diagonal's rank** in terms of its rows. Why is a thin straight line the *most* expensive shape in the picture, when the bar and the post cost one term each?

**(b) [6]** In `part8`, change the noise level `1e-10` to each of $10^{-14}, 10^{-12}, \dots, 10^{-2}, 1$.

- Report $\sigma_3$ and the gap $\sigma_2/\sigma_3$ at each.
- **Over what range does the gap scale exactly with the noise**, and why? **At which end does that stop, and what is the floor you have hit** at that end?
- At noise $1$, would you still call the matrix rank $2$? **Defend a yes or a no.**

**(c) [7]** In `part11`, the $x$-coordinates get noise `random.gauss(0, 0.6)`. **Change that $0.6$** to $0$, $0.3$ and $1.2$, leaving the $y$-noise at $0.6$.

- Report all three slopes at each of the four $x$-noise levels (the notes give $0.6$).
- **At $x$-noise $0$, which method is right, and does total least squares still beat it?**
- **State precisely the assumption under which total least squares is the correct method**, and say what goes wrong for *both* methods at $x$-noise $1.2$.

---

### Q5: Proofs (20 points)

**(a) [4]** Prove $\lVert A\rVert_2 = \max_{\lVert x\rVert = 1}\lVert Ax\rVert = \sigma_1$, by writing $x$ in the basis $v_1, \dots, v_n$.

**(b) [4]** Prove that $A$ and $A^\mathsf{T}$ have the same singular values. **Then prove that the singular values of a symmetric matrix are the absolute values of its eigenvalues**, constructing the SVD from $A = Q\Lambda Q^\mathsf{T}$ explicitly.

**(c) [5]** **Eckart–Young, the hard half.** Let $X$ have rank at most $k$. Prove $\lVert A - X\rVert_2 \ge \sigma_{k+1}$.

> *Hint:* $\dim\mathbf{N}(X) \ge n - k$. The span of $v_1, \dots, v_{k+1}$ has dimension $k + 1$.
> Two subspaces of $\mathbb{R}^n$ whose dimensions add to more than $n$ must share a nonzero vector.
> Evaluate $\lVert(A - X)z\rVert$ on a unit vector $z$ they share.

**(d) [4]** Prove that if $A$ has independent columns then $A^+ = (A^\mathsf{T}A)^{-1}A^\mathsf{T}$, and that if $A$ is invertible then $A^+ = A^{-1}$. **Say what this means for Week 9's normal equations.**

**(e) [3]** Prove $\lVert A\rVert_F^2 = \sum_k\sigma_k^2$, using $\lVert A\rVert_F^2 = \operatorname{trace}(A^\mathsf{T}A)$.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | The SVD by hand, of a wide matrix | 22 |
| 2 | Four subspaces and the pseudoinverse | 22 |
| 3 | Approximation and rank, without a computer | 16 |
| 4 | On the machine | 20 |
| 5 | Proofs | 20 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*MATH 241 · Week 11 · PS 11 · © CSE Department*
