# MATH 241 · Problem Set 1
## Matrices, Inverses, and the $LU$ Factorization

---

**Released:** Week 1, Wednesday · **Due:** Week 2, **Friday 17:00**
**Total: 100 points** · Submit one PDF, `PS1_{LastName}_{StudentID}.pdf`

> **Exact arithmetic in Q1–Q4.** Fractions, not decimals.
>
> **Show the multipliers**, as in PS 0. In Q4 they are the answer, not the working.
>
> **Q5 is run on a computer**, using `resources/matrices.py` from this week's folder. State your
> Python version and your machine.
>
> **Recitation 1 is the Thursday before this is due**, 15:00–15:50, SSB 108.

---

### Q1: Four Readings of One Product (20 points)

$$A = \begin{bmatrix}1 & 2 & 0\\ 3 & -1 & 4\end{bmatrix}, \qquad B = \begin{bmatrix}2 & 1\\ 0 & 3\\ -1 & 5\end{bmatrix}$$

**(a) [10]** Compute $AB$ **four times**, once by each reading in L04 §2: entry by entry, column by column, row by row, and as a sum of outer products. **Write out all four computations in full** — the point is not the answer, which is the same each time, but that you can produce it four ways.

**(b) [4]** Compute $BA$. It exists, and it is not $AB$. **What is the most immediate reason the two cannot be equal**, before any arithmetic?

**(c) [6]** Prove, in general, that **column $j$ of $AB$ equals $A$ times column $j$ of $B$**. Then use that fact — not the entry formula — to prove in two lines that **every column of $AB$ is a linear combination of the columns of $A$**.

> *(That last statement is worth more than the marks it carries. It says the columns of a product
> cannot escape the columns of the left factor, and it is the one-line proof of half a dozen results
> in Weeks 2 and 3.)*

---

### Q2: The Algebra, and Where It Breaks (18 points)

**(a) [5]** Expand $(A+B)^2$ and $(A-B)(A+B)$ without assuming $AB = BA$. State the exact condition under which each collapses to the answer you would expect from ordinary numbers.

**(b) [5]** Find $2\times2$ matrices with $AB = 0$, $A \ne 0$ and $B \ne 0$. Then find some with $AB = 0$ **and** $BA \ne 0$. What does this tell you about deducing anything from $AB = AC$?

**(c) [4]** $A$ is $m \times n$ and $B$ is $p \times q$. Both $AB$ and $BA$ are defined. Find all relations forced among $m, n, p, q$. Under what further condition are the two products the same **size**, and does that make them equal?

**(d) [4]** Using block multiplication, show that

$$\begin{bmatrix}I & X\\ 0 & I\end{bmatrix}\begin{bmatrix}I & Y\\ 0 & I\end{bmatrix} = \begin{bmatrix}I & X+Y\\ 0 & I\end{bmatrix}$$

for square blocks of matching size. **Deduce the inverse of $\begin{bmatrix}I & X\\ 0 & I\end{bmatrix}$ without doing any elimination.**

---

### Q3: Inverses (22 points)

**(a) [8]** Compute $C^{-1}$ by Gauss–Jordan, showing the augmented tableau at every stage:

$$C = \begin{bmatrix}1 & 2 & 3\\ 2 & 5 & 3\\ 1 & 0 & 8\end{bmatrix}$$

**Every entry of $C^{-1}$ is an integer.** That is unusual — L05 §4's example had denominators of 24. Say what has to be true of a matrix for its inverse to be an integer matrix, given that $C^{-1} = \frac{1}{\det C}\operatorname{adj}C$ and $\operatorname{adj}C$ is always an integer matrix when $C$ is. *(You may use $\det C = -1$.)*

**(b) [5]** Prove $(AB)^{-1} = B^{-1}A^{-1}$, and then prove $(ABC)^{-1} = C^{-1}B^{-1}A^{-1}$ from it. Give a one-sentence non-mathematical account of why the order reverses.

**(c) [4]** $A$ is invertible and $B$ is not. Prove $AB$ is not invertible. *(One line, from the characterisation "$Ax = 0$ only for $x = 0$".)*

**(d) [5]** A matrix satisfies $A^2 = A$ and $A \ne I$.

- Prove $A$ is not invertible.
- Give a $2\times2$ example that is neither $0$ nor $I$.
- Such matrices are **projections**. Say what your example does to a vector, geometrically, and why "not invertible" is the right thing for a projection to be.

---

### Q4: $A = LU$ (22 points)

**(a) [10]** Factor

$$D = \begin{bmatrix}1 & 2 & 3\\ 3 & 7 & 7\\ -2 & 0 & -9\end{bmatrix}$$

as $D = LU$ by elimination. State the three multipliers, give $L$ and $U$, and **verify by multiplying $LU$ out in full**.

**(b) [6]** Using **only** the $L$ and $U$ from (a) — no further elimination — solve $Dx = b$ for both

$$b = (2, 10, 7) \qquad\text{and}\qquad b = (9, 20, -31)$$

by forward substitution ($Lc = b$) then back substitution ($Ux = c$). Report $c$ and $x$ for each.

Then count, for this $3\times3$: **how many multiply–subtracts and how many divisions did the second solve take**, and how many would a fresh elimination on $[\,D \mid b\,]$ have taken? Give all four numbers, and then the general-$n$ formula for each ($2n^2$ against $n^3/3 + n^2$).

**(c) [6]** This one has no $LU$ factorisation:

$$E = \begin{bmatrix}0 & 1 & 2\\ 1 & 2 & 1\\ 2 & 7 & 9\end{bmatrix}$$

Say precisely why not — one sentence, about $L$ being lower triangular. Then find a permutation matrix $P$ such that $PE = LU$, and give $P$, $L$ and $U$. Verify $PE = LU$.

Finally: **verify that $P^{-1} = P^\mathsf{T}$ for your $P$**, and use it to write $E$ itself as a product of three matrices.

---

### Q5: Where You Put the Brackets (18 points)

**(a) [6]** $A$ is $1000\times2$, $B$ is $2\times1000$, $C$ is $1000\times1$. Count the flops for $(AB)C$ and for $A(BC)$, and give the size in megabytes of the largest intermediate each one forms (`float64`, 8 bytes per entry).

Then run `matrices.py` and report the measured times and speedup on **your** machine. **Does the measured speedup match the flop ratio?** If not, say which direction the discrepancy goes and offer a reason.

**(b) [6]** Now $A$ is $200\times200$, $B$ is $200\times3$, $C$ is $3\times200$. Cost both bracketings. **This time the left one wins.**

State, in one sentence, the rule that actually decides which bracketing is cheaper. It is not "associate to the right", and your sentence must correctly predict both (a) and (b).

**(c) [6]** You must compute $A^{-1}B$, where $A$ is $2000\times2000$ and $B$ is $2000\times50$.

- Cost the naive route: form $A^{-1}$ by Gauss–Jordan ($\approx 2n^3$), then multiply.
- Cost the correct route: factor $A = LU$ ($\approx n^3/3$), then two triangular solves per column of $B$ ($2n^2$ each).
- Give both totals and the ratio. Then write the one line of NumPy you would actually run, and the one line you should not.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Four readings of one product | 20 |
| 2 | The algebra, and where it breaks | 18 |
| 3 | Inverses | 22 |
| 4 | $A = LU$ | 22 |
| 5 | Where you put the brackets | 18 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*MATH 241 · Week 1 · PS 1 · © CSE Department*
