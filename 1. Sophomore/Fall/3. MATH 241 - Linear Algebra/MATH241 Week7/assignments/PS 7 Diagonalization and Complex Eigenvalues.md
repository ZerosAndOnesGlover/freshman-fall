# MATH 241 · Problem Set 7
## Diagonalization and Complex Eigenvalues

---

**Released:** Week 7, Wednesday · **Due:** Week 8, **Friday 17:00**
**Total: 100 points** · Submit one PDF, `PS7_{LastName}_{StudentID}.pdf`

> **Exact arithmetic** except where a surd or a limit forces otherwise; say which you are in.
>
> **Verify every diagonalisation.** $S\Lambda S^{-1} = A$ is one product and it certifies the whole
> computation. **An unverified $S$ earns no marks for the verification.**
>
> **Q1 has a repeated eigenvalue and is diagonalisable anyway.** If that sentence surprises you,
> reread L20 §5 before starting.
>
> **Recitation 7 is the Thursday before this is due**, 15:00–15:50, SSB 108.

---

### Q1: Diagonalise It (24 points)

$$A = \begin{bmatrix}0&1&1\\ 1&0&1\\ 1&1&0\end{bmatrix}$$

**(a) [6]** Find the characteristic polynomial and the eigenvalues. **One eigenvalue is repeated** — say which, and give its algebraic multiplicity.

**(b) [8]** Find every eigenspace and give a basis for each. **State the geometric multiplicity of each eigenvalue.**

**(c) [4]** **Is $A$ diagonalisable?** Justify from the criterion, not from a guess.

**(d) [6]** Give $S$, $\Lambda$ and $S^{-1}$, and **verify $S\Lambda S^{-1} = A$.**

> **A note on (b).** The repeated eigenvalue has a **two-dimensional** eigenspace, so you must give
> **two independent** vectors spanning it. Any valid pair is accepted, and your $S$ must use the pair
> you chose.

---

### Q2: When It Fails (20 points)

**(a) [8]** For $B = \begin{bmatrix}2&1&0\\ 0&2&1\\ 0&0&2\end{bmatrix}$:

- Give the eigenvalues with algebraic multiplicities.
- Compute the eigenspace and give its dimension.
- **Is $B$ diagonalisable?** Justify.
- **What is $B$'s Jordan form?** *(You are not asked to derive it — read it off §3 of L22.)*

**(b) [4]** Show that a **nonzero nilpotent** matrix ($N^k = 0$, $N \ne 0$) is **never** diagonalisable, in two lines.

Then verify directly that Week 4's differentiation matrix on $\mathbb{P}_3$,

$$D = \begin{bmatrix}0&1&0&0\\ 0&0&2&0\\ 0&0&0&3\\ 0&0&0&0\end{bmatrix},$$

has only a one-dimensional eigenspace. **What are its eigenvectors, as polynomials?**

**(c) [4]** $A$ is $4\times4$ with characteristic polynomial $(\lambda - 3)^2(\lambda - 7)^2$. **List every possible pair of geometric multiplicities**, and say which pairs make $A$ diagonalisable.

**(d) [4]** Consider $\begin{bmatrix}5&\varepsilon\\ 0&5\end{bmatrix}$.

- Give the geometric multiplicity of $\lambda = 5$ for $\varepsilon = 10^{-8}$, and for $\varepsilon = 0$.
- **In two sentences: why does no numerical algorithm test whether a matrix is diagonalisable?**

---

### Q3: Complex Eigenvalues (20 points)

**(a) [5]** $C = \begin{bmatrix}3&-5\\ 5&3\end{bmatrix}$. Find the complex eigenvalues, and verify their sum is the trace and their product the determinant.

**(b) [5]** **Without using your answer to (a)**, compute $r$ and $\theta$ from L23 §2's formulas

$$r = \sqrt{\det C}, \qquad \cos\theta = \frac{\operatorname{trace}C}{2\sqrt{\det C}}$$

and check they agree with $\lvert\lambda\rvert$ and $\arg\lambda$. **Describe $C$ geometrically in one sentence.**

**(c) [4]** For which real $c$ does $A_1 = \begin{bmatrix}0&1\\ -4&c\end{bmatrix}$ have complex eigenvalues? **For which does $x_{k+1} = A_1x_k$ converge to $\mathbf{0}$?**

Now the same two questions for $A_2 = \begin{bmatrix}0&1\\ -\tfrac14&c\end{bmatrix}$.

> **The two answers to the second question are different, and the reason is one number you can read
> off each matrix without finding any eigenvalue.** Say what it is.

**(d) [6]** A real matrix has eigenvalues $0.9 \pm 0.4i$ and $0.5$.

- Give the spectral radius.
- Does $A^k \to 0$? Justify.
- **Describe the orbit of a generic starting vector** in words — what does it do in the plane spanned by the complex pair, and what does the third component do?

---

### Q4: Powers in Practice (20 points)

**(a) [8]** The recurrence $a_{k+1} = 5a_k - 6a_{k-1}$, with $a_0 = 0$ and $a_1 = 1$.

- Write it as $\begin{bmatrix}a_{k+1}\\ a_k\end{bmatrix} = M\begin{bmatrix}a_k\\ a_{k-1}\end{bmatrix}$ and give $M$.
- Find the eigenvalues.
- **Give a closed form for $a_k$** and check it at $k = 4$.

**(b) [6]** $P = \begin{bmatrix}0.8&0.3\\ 0.2&0.7\end{bmatrix}$.

- **Show $\lambda = 1$ is an eigenvalue without computing a determinant.**
- Find the steady state and the second eigenvalue.
- **How many steps until $P^k$ is within $10^{-6}$ of its limit?** Show the calculation.

**(c) [6]** Week 0's L03 §2 said PageRank cannot be solved by elimination — $n^3/3$ at $n = 10^9$ is ten million years.

**Explain, in one paragraph, what is computed instead and why it is feasible.** Your answer must say what the answer *is* (which eigenvector), what the iteration is, and **what governs the number of iterations needed.**

---

### Q5: Structure (16 points)

**(a) [4]** Prove $A^k = S\Lambda^kS^{-1}$ by induction, and state what $\Lambda^k$ is.

**(b) [4]** $A = S\Lambda S^{-1}$ is invertible. Prove $A^{-1} = S\Lambda^{-1}S^{-1}$ and say what this requires of the eigenvalues. **Deduce the eigenvalues of $A^{-1}$.**

**(c) [4]** Prove: **two diagonalisable matrices are similar if and only if they have the same eigenvalues with the same multiplicities.**

Then explain why this does **not** contradict PS 4 Q5(d), where $I$ and $\begin{bmatrix}1&1\\0&1\end{bmatrix}$ had the same characteristic polynomial and were not similar.

**(d) [4]** Prove that if $A$ is diagonalisable and every $\lvert\lambda_i\rvert < 1$ then $A^k \to 0$.

Then state what changes if $A$ is **defective** — and why the conclusion survives anyway. *(One sentence; L23 §3's parenthetical.)*

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Diagonalise it | 24 |
| 2 | When it fails | 20 |
| 3 | Complex eigenvalues | 20 |
| 4 | Powers in practice | 20 |
| 5 | Structure | 16 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*MATH 241 · Week 7 · PS 7 · © CSE Department*
