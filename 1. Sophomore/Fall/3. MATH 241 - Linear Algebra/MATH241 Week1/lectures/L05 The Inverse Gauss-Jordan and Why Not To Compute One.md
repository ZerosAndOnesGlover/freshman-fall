# MATH 241 · Linear Algebra
## Week 1 · Lecture 2 of 3 · **Tuesday**
### The Inverse: Gauss–Jordan, and Why You Should Almost Never Compute One

---

**Reading:** Strang §2.5 · **Previous:** L04, matrix multiplication · **Next:** L06, transposes and $A = LU$

---

## 1. What an Inverse Is

$A^{-1}$ is the matrix that undoes $A$:

$$A^{-1}A = I \qquad\text{and}\qquad AA^{-1} = I.$$

$A$ is a function; $A^{-1}$ is its inverse function; $I$ is "do nothing". A matrix with an inverse is **invertible**, or equivalently **nonsingular**, and Week 0's L02 §6 already told you which matrices those are — the ones elimination gives $n$ pivots.

**Two demands, and for square matrices one implies the other.** In general a function can have a left inverse and no right inverse, and $A^{-1}A = I$ is genuinely a different statement from $AA^{-1} = I$. **For square $A$ over $\mathbb{R}$ they are equivalent**, which is a real theorem and not an obvious one — it is Week 3's, once rank exists. Until then, take it, and notice that it fails for non-square matrices: Week 9's least squares is entirely about a matrix with a left inverse and no right one.

**The inverse is unique when it exists**, and the proof is worth seeing because it uses nothing but associativity:

> Suppose $BA = I$ and $AC = I$. Then $B = BI = B(AC) = (BA)C = IC = C$. $\square$

**One line, and it proves more than it says.** It shows any left inverse equals any right inverse — so as soon as both exist, there is exactly one matrix and it is both.

---

## 2. When Does It Exist?

**$A$ is invertible $\iff$ elimination produces $n$ pivots.** That is the test, it is L02's algorithm, and it costs $n^3/3$.

Here is the same fact in the six other forms you will meet. **They are all one theorem**, and by Week 3 you will be able to prove every arrow; for now, recognise them as the same statement wearing different clothes.

| | $A$ is invertible $\iff$ | First proved in |
|---|---|---|
| 1 | elimination produces $n$ pivots | Week 0 |
| 2 | $Ax = b$ has exactly one solution for every $b$ | Week 0, L01 §5 |
| 3 | $Ax = 0$ has only the solution $x = 0$ | **below** |
| 4 | the columns of $A$ are linearly independent | Week 3 |
| 5 | the columns of $A$ span $\mathbb{R}^n$ | Week 3 |
| 6 | $\operatorname{rank} A = n$ | Week 3 |
| 7 | $\det A \ne 0$ | Week 5 |

**Number 3 is the cheapest one to have in your hand, and here is its proof**, since it is two lines and you have everything you need:

> **If $A$ is invertible and $Ax = 0$**, multiply on the left by $A^{-1}$:
> $x = Ix = A^{-1}Ax = A^{-1}0 = 0$. So $x = 0$ is the only solution.
>
> **Conversely, if $Az = 0$ for some $z \ne 0$**, then $A$ cannot be invertible: PS 0 Q3(b) showed
> that $Ax = b$ then has zero or infinitely many solutions for every $b$, never exactly one, which
> contradicts characterisation 2. $\square$

> **Number 7 is on the list and it is the one to distrust.** "$\det A \ne 0$" is a correct
> characterisation and a terrible test — Week 0's L03 §6 measured $\det H_{10} = 2.2\times10^{-53}$
> on a perfectly invertible matrix, and produced a matrix with $\det = 1$ and condition number
> $10^{12}$. **Invertibility is a yes/no question and no real computation is ever asking it.** The
> question you actually have is *"how badly conditioned is it"*, and the determinant does not answer
> that.

---

## 3. The $2\times2$ Formula, and the One You Should Not Memorise

$$A = \begin{bmatrix}a & b\\ c& d\end{bmatrix} \qquad\Longrightarrow\qquad A^{-1} = \frac{1}{ad-bc}\begin{bmatrix}d & -b\\ -c & a\end{bmatrix}$$

**Swap the diagonal, negate the off-diagonal, divide by $ad - bc$.** Worth memorising — $2\times2$ inverses come up constantly, in this course and in graphics.

**Check it by multiplying**, do not take it on trust:

$$\begin{bmatrix}a&b\\c&d\end{bmatrix}\begin{bmatrix}d&-b\\-c&a\end{bmatrix} = \begin{bmatrix}ad-bc & -ab+ba\\ cd-dc & -cb+da\end{bmatrix} = (ad-bc)I \ ✓$$

**There is a $3\times3$ version, and a general one.** The general formula is $A^{-1} = \frac{1}{\det A}\operatorname{adj}A$, where $\operatorname{adj}A$ is built from $n^2$ determinants of $(n-1)\times(n-1)$ submatrices. **It is Week 5's, it is beautiful, and it is useless for computation** — evaluating it costs more than $n!$ if done naively, against Gauss–Jordan's $2n^3$. Learn the $2\times2$ case; use elimination for everything larger.

---

## 4. Gauss–Jordan: Computing $A^{-1}$ Properly

**The idea is L04's column reading of matrix multiplication.** $AA^{-1} = I$ says: column $j$ of $A^{-1}$ is the solution of

$$Ax = e_j$$

so an inverse is **$n$ linear systems with the same matrix and $n$ different right-hand sides**. You already know how to solve those, and Week 0's PS 0 Q4(a) already told you the efficient way to do $n$ of them: **augment once and eliminate once.**

$$[\,A \mid I\,] \;\xrightarrow{\text{elimination, then upward, then scale}}\; [\,I \mid A^{-1}\,]$$

### Worked, on Week 0's matrix

$$A = \begin{bmatrix}2&1&-1\\4&5&0\\-2&8&11\end{bmatrix}$$

**Down** — the same three multipliers Week 0 found, $\ell_{21}=2$, $\ell_{31}=-1$, $\ell_{32}=3$:

$$\left[\begin{array}{ccc|ccc}
2&1&-1 & 1&0&0\\ 4&5&0 & 0&1&0\\ -2&8&11 & 0&0&1
\end{array}\right]
\longrightarrow
\left[\begin{array}{ccc|ccc}
2&1&-1 & 1&0&0\\ 0&3&2 & -2&1&0\\ 0&0&4 & 7&-3&1
\end{array}\right]$$

*(Row 3 after $R_3 + R_1$ is $[\,0\ 9\ 10 \mid 1\ 0\ 1\,]$; then $R_3 - 3R_2$ gives $[\,0\ 0\ 4 \mid 1+6\ \ 0-3\ \ 1\,] = [\,0\ 0\ 4 \mid 7\ -3\ 1\,]$.)*

**Up**, clearing above each pivot, then **scale** each row by $1/\text{pivot}$:

$$\left[\begin{array}{ccc|ccc}
1&0&0 & \tfrac{55}{24} & -\tfrac{19}{24} & \tfrac{5}{24}\\[2pt]
0&1&0 & -\tfrac{11}{6} & \tfrac{5}{6} & -\tfrac16\\[2pt]
0&0&1 & \tfrac74 & -\tfrac34 & \tfrac14
\end{array}\right]
\qquad
A^{-1} = \frac{1}{24}\begin{bmatrix}55&-19&5\\ -44&20&-4\\ 42&-18&6\end{bmatrix}$$

**Verify one entry rather than trusting nine.** Row 1 of $A$ times column 1 of $A^{-1}$:

$$\frac{2(55) + 1(-44) + (-1)(42)}{24} = \frac{110 - 44 - 42}{24} = \frac{24}{24} = 1\ ✓$$

*(`matrices.py` checks all nine and reports `A * A^-1 = I: True`.)*

**Notice what the answer looks like.** $A$ is nine integers. $A^{-1}$ is nine fractions with a common denominator of 24, and **not one entry is zero**. That is not this example being awkward; it is §7's rule.

---

## 5. The Rules

| Rule | | Why |
|---|---|---|
| $(A^{-1})^{-1} = A$ | | undoing the undoing |
| $(AB)^{-1} = B^{-1}A^{-1}$ | **order reverses** | see below |
| $(A^\mathsf{T})^{-1} = (A^{-1})^\mathsf{T}$ | order does *not* reverse | L06 |
| $(cA)^{-1} = \tfrac1c A^{-1}$, $c \ne 0$ | | |
| $(A^k)^{-1} = (A^{-1})^k$ | | |
| $A, B$ invertible $\Rightarrow AB$ invertible | | the product rule exhibits the inverse |
| **$A + B$ invertible?** | **No rule.** $I + (-I) = 0$ | invertibility says nothing about sums |

**Why the order reverses**, and it is worth being able to reconstruct rather than recall:

$$(AB)(B^{-1}A^{-1}) = A(BB^{-1})A^{-1} = AIA^{-1} = AA^{-1} = I \ ✓$$

**Socks and shoes.** To dress: socks, then shoes. To undo: **shoes off first**, then socks. You cannot remove the socks through the shoes, and $B^{-1}$ has to come off first because $B$ went on last. The same reversal governs transposes in L06 and, in Week 7, why $(S\Lambda S^{-1})^k$ telescopes.

---

## 6. What It Costs, and Why You Should Not

Gauss–Jordan on $[\,A\mid I\,]$ costs about $\mathbf{2n^3}$ flops — the extra work over elimination's $n^3/3$ is clearing upward and carrying $n$ extra columns.

**Now compare the two ways to answer $Ax = b$:**

| | Setup | Per right-hand side | $n=1000$, one solve |
|---|---:|---:|---:|
| **Factor, then solve** | $n^3/3$ | $2n^2$ | $3.35\times10^{8}$ |
| **Invert, then multiply** | $2n^3$ | $2n^2$ | $2.00\times10^{9}$ |

$$\boxed{\text{six times the work, for the same answer}}$$

**And the inverse never catches up.** For $k$ right-hand sides it is $n^3/3 + 2kn^2$ against $2n^3 + 2kn^2$: the per-solve terms are *identical*, because multiplying by $A^{-1}$ and back-substituting through $L$ and $U$ both cost $2n^2$. **The factorisation you already have does the same job for the same price, so the $2n^3$ was pure loss.** This is why "I need to solve it many times, so I will invert once" is wrong, and it is wrong for a reason worth understanding rather than a rule worth obeying.

### It is also less accurate

Same matrices, same right-hand sides, same partial pivoting, same machine. Hilbert systems with exact answer $x = (1,\dots,1)$; the only difference is whether $A^{-1}$ was formed on the way:

| $n$ | Solve directly | Form $H^{-1}$, then multiply | Times worse |
|---:|---:|---:|---:|
| 6 | $5.27\times10^{-11}$ | $1.06\times10^{-9}$ | $20.1$ |
| 8 | $1.37\times10^{-7}$ | $5.60\times10^{-7}$ | $4.1$ |
| 10 | $7.18\times10^{-4}$ | $1.47\times10^{-3}$ | $2.0$ |
| 12 | $5.95\times10^{-3}$ | $\mathbf{0.54}$ | $\mathbf{90.7}$ |
| 14 | $6.26$ | $22.1$ | $3.5$ |

**Inverting is worse at every single $n$, and the penalty is between $2\times$ and $90\times$ with no pattern.** That irregularity is the honest result and it is the useful one: **you cannot predict the size of the penalty, so you cannot budget for it.** The extra $2n^3$ operations are $2n^3$ extra opportunities to round, and which of them happen to align badly depends on the matrix.

*(At $n = 14$ both answers are garbage — errors of $6$ and $22$ on an answer of $1$. That is the problem failing, not the method; $\operatorname{cond}(H_{14})$ is past $10^{17}$. Week 0's L03 §7.)*

---

## 7. The Inverse of a Sparse Matrix Is Not Sparse

The third argument, and in practice the one that actually stops people.

$$K = \begin{bmatrix}2&-1&0&0&0\\ -1&2&-1&0&0\\ 0&-1&2&-1&0\\ 0&0&-1&2&-1\\ 0&0&0&-1&2\end{bmatrix} \qquad
6K^{-1} = \begin{bmatrix}5&4&3&2&1\\ 4&8&6&4&2\\ 3&6&9&6&3\\ 2&4&6&8&4\\ 1&2&3&4&5\end{bmatrix}$$

**$K$ has 13 nonzeros out of 25. $K^{-1}$ has 25 out of 25 — not a single zero anywhere.**

*(This $K$ is the second-difference matrix. It is the discretised second derivative, and it or something very like it turns up in every finite-difference PDE solver, every spring-mass chain, and every image-smoothing filter. It is not a contrived example; it is the most common matrix in scientific computing.)*

$L$ and $U$, by contrast, **keep the band**: 9 nonzeros each, and $U$'s pivots are $2, \tfrac32, \tfrac43, \tfrac54, \tfrac65$.

At scale that is the whole argument:

| $n$ | $K$ nonzeros $(3n-2)$ | $K^{-1}$ nonzeros $(n^2)$ | Ratio |
|---:|---:|---:|---:|
| 100 | 298 | 10,000 | 33 |
| 1,000 | 2,998 | 1,000,000 | 333 |
| 10,000 | 29,998 | 100,000,000 | 3,333 |

**A $10^6 \times 10^6$ sparse system is routine; its inverse is $10^{12}$ numbers, which is eight terabytes.** The factorisation fits in memory and the inverse does not. **This is not an optimisation. It is the difference between a computation that runs and one that does not.**

---

## 8. When the Inverse *Is* the Right Object

The advice is "do not compute one", not "do not think about one". $A^{-1}$ is indispensable:

- **In proofs and derivations.** $A = S\Lambda S^{-1}$ (Week 7), $(A^\mathsf{T}A)^{-1}A^\mathsf{T}$ (Week 9). **A formula containing $A^{-1}$ is a statement, not an instruction** — when Week 9 writes $\hat{x} = (A^\mathsf{T}A)^{-1}A^\mathsf{T}b$, the sentence is "$\hat x$ solves $A^\mathsf{T}A\hat x = A^\mathsf{T}b$", and that is what any implementation does. Learn to read the notation that way now.
- **Small fixed dimensions.** A graphics pipeline inverts $4\times4$ matrices constantly, by explicit formula, because at $n=4$ the constants dominate and the matrix will be reused for a million vertices.
- **When the inverse is the answer.** A covariance matrix's inverse is the *precision matrix* and its entries mean something statistically — MATH 251 next term. You want the object itself, not a solve.
- **Rank-one updates.** If $A^{-1}$ is known and $A$ changes by a rank-one perturbation, the Sherman–Morrison formula updates the inverse in $O(n^2)$ rather than refactoring in $O(n^3)$. **Kalman filters are built on this.**

> **The rule to carry out of this lecture:** when you see $A^{-1}b$ in a formula, **write
> `solve(A, b)`**, not `inv(A) @ b`. Every numerical library documents this and it is the single
> most common piece of numerical-linear-algebra advice, because it is the single most common mistake.

---

## 9. What to Take Away

1. **$A^{-1}$ undoes $A$**, it is unique when it exists, and for square real matrices one-sided inverses are two-sided.
2. **Invertible $\iff$ $n$ pivots**, and six other equivalent statements you will collect through Week 5. **$\det A \ne 0$ is the least useful of them.**
3. **The $2\times2$ formula is worth memorising.** The general adjugate formula is Week 5's and is not a method.
4. **Gauss–Jordan is $n$ solves done at once**: $[\,A\mid I\,] \to [\,I\mid A^{-1}\,]$, about $2n^3$.
5. **$(AB)^{-1} = B^{-1}A^{-1}$ — the order reverses.** Shoes before socks.
6. **Do not invert to solve.** Six times the work, worse accuracy by an unpredictable factor of 2 to 90, and for sparse matrices it turns a computation that fits in memory into one that does not.

---

## Exercises

*(Not assessed.)*

1. Invert $\begin{bmatrix}1&2\\3&7\end{bmatrix}$ by the formula and by Gauss–Jordan. Same answer, and which was faster by hand?
2. Prove $(ABC)^{-1} = C^{-1}B^{-1}A^{-1}$ from the two-factor rule. Then guess and prove the $k$-factor version.
3. $A$ is invertible and $B$ is not. Show $AB$ is not invertible. *(Use characterisation 3 — one line.)*
4. Give $2\times2$ matrices $A, B$ both invertible with $A + B$ singular. Then give some with $A+B$ invertible. What, if anything, does invertibility of $A$ and $B$ tell you about $A + B$?
5. Invert the $4\times4$ version of §7's $K$ by Gauss–Jordan, in exact fractions. Count the zeros in $K$ and in $K^{-1}$, and confirm the pivots continue the pattern $2, \tfrac32, \tfrac43, \dots$
6. A matrix satisfies $A^2 = A$ and $A \ne I$. Show $A$ is not invertible. *(Two lines. Such matrices are **projections**, and they are Week 8's whole subject — this exercise is why a projection can never be undone.)*

---

*MATH 241 · Week 1 · L05 · © CSE Department*
