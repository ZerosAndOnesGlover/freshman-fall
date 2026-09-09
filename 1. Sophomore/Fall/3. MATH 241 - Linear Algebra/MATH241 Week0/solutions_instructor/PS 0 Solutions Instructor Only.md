# MATH 241 · Problem Set 0 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**All computed figures below are from the reference machine:** Intel i5-8250U, Ubuntu 24.04.4, CPython 3.14, IEEE 754 binary64. Students' *exact* results must match to the digit; the one timing figure will not.

**What this paper is testing.** Q1 is mechanical and should be near-full marks for anyone who did the reading — mark the *method* (multipliers written down, exchanges named) rather than the answers, because a single sign error should not cost eight points. Q2(c) and Q3(b) are the conceptual core; a student who gets both has understood what the column picture is *for* and will be fine in Week 2. Q4 and Q5 are calibration, and Q5(c) is the question that separates the top of the cohort — it is the only one where a correct-looking computation has to be *rejected*.

**Common failure modes, in order of frequency:** (1) dropping the augmented column partway through Q1; (2) answering Q2(c) by eliminating, which is not what was asked; (3) Q3(b) proving only one direction of the case split; (4) Q5(c) confusing residual with error and never noticing.

---

## Q1: Elimination by Hand (24 points)

### (a) [8]

$$\left[\begin{array}{ccc|c} 1 & 2 & 2 & 3\\ 2 & 5 & 7 & 5\\ 3 & 6 & 8 & 7\end{array}\right]
\xrightarrow[\;\ell_{31}=3\;]{\;\ell_{21}=2\;}
\left[\begin{array}{ccc|c} 1 & 2 & 2 & 3\\ 0 & 1 & 3 & -1\\ 0 & 0 & 2 & -2\end{array}\right]$$

Row 3 after $R_3 - 3R_1$ is $[\,0\ \ 0\ \ 2 \mid -2\,]$ — **already clear in column 2**, so $\ell_{32} = 0$ and the second elimination step does nothing.

**Pivots $1, 1, 2$.** Back substitution: $2x_3 = -2 \Rightarrow x_3 = -1$; $x_2 + 3(-1) = -1 \Rightarrow x_2 = 2$; $x_1 + 4 - 2 = 3 \Rightarrow x_1 = 1$.

$$\boxed{x = (1, 2, -1)}$$

Check in the originals: $1 + 4 - 2 = 3$ ✓, $2 + 10 - 7 = 5$ ✓, $3 + 12 - 8 = 7$ ✓.

**The zero multiplier** means row 3 already had a zero in the pivot column at that stage — that is, after the column-1 step, row 3 had no component of row 2 to remove. *(Marking: accept anything equivalent. **Do not accept "there was no row 3 operation"** — there was; it was the identity. Week 1's $L$ has a genuine $0$ in that slot, and students who quietly omit it will build the wrong $L$ in PS 1.)*

*Marking: 5 for the elimination and answer, 2 for the multipliers being written, 1 for the zero-multiplier sentence.*

### (b) [8]

$a_{11} = 0$: **there is no multiplier, because forming one requires dividing by the pivot.** This is L02 §6 Case A — a fixable zero. Row 2 has a $1$ in column 1, so **swap $R_1 \leftrightarrow R_2$: operation R2.**

$$\left[\begin{array}{ccc|c} 0 & 1 & 2 & 3\\ 1 & 3 & 1 & 0\\ 2 & 5 & 4 & 5\end{array}\right]
\xrightarrow{\;R_1 \leftrightarrow R_2\;}
\left[\begin{array}{ccc|c} 1 & 3 & 1 & 0\\ 0 & 1 & 2 & 3\\ 2 & 5 & 4 & 5\end{array}\right]
\xrightarrow{\;\ell_{31}=2\;}
\left[\begin{array}{ccc|c} 1 & 3 & 1 & 0\\ 0 & 1 & 2 & 3\\ 0 & -1 & 2 & 5\end{array}\right]
\xrightarrow{\;\ell_{32}=-1\;}
\left[\begin{array}{ccc|c} 1 & 3 & 1 & 0\\ 0 & 1 & 2 & 3\\ 0 & 0 & 4 & 8\end{array}\right]$$

**Pivots $1, 1, 4$.** $x_3 = 2$; $x_2 + 4 = 3 \Rightarrow x_2 = -1$; $x_1 - 3 + 2 = 0 \Rightarrow x_1 = 1$.

$$\boxed{x = (1, -1, 2)}$$

Check: $-1 + 4 = 3$ ✓, $1 - 3 + 2 = 0$ ✓, $2 - 5 + 8 = 5$ ✓.

> **Note $\ell_{32} = -1$, a negative multiplier**, which means $R_3 \leftarrow R_3 + R_2$. Students
> who have memorised "subtract" rather than "subtract $\ell$ times" get $[\,0\ 0\ 0 \mid 8\,]$ here
> and conclude the system is inconsistent. **Worth a comment on every script that does it** — it is
> the most instructive error on the paper.

*Marking: 2 for diagnosing and naming the exchange as R2, 5 for the elimination and answer, 1 for the check.*

### (c) [8]

$$\left[\begin{array}{ccc|c} 1 & 3 & -2 & 1\\ 2 & 1 & 4 & 7\\ 4 & 7 & 0 & d\end{array}\right]
\xrightarrow[\;\ell_{31}=4\;]{\;\ell_{21}=2\;}
\left[\begin{array}{ccc|c} 1 & 3 & -2 & 1\\ 0 & -5 & 8 & 5\\ 0 & -5 & 8 & d-4\end{array}\right]
\xrightarrow{\;\ell_{32}=1\;}
\left[\begin{array}{ccc|c} 1 & 3 & -2 & 1\\ 0 & -5 & 8 & 5\\ 0 & 0 & 0 & d-9\end{array}\right]$$

**Only two pivots ($1$ and $-5$): the matrix is singular.** The last row reads $0 = d - 9$.

$$\boxed{\text{consistent} \iff d = 9}$$

For any $d \ne 9$ the row $[\,0\ \ 0\ \ 0 \mid d-9\,]$ with $d - 9 \ne 0$ asserts $0 = d-9$, so **no solution**.

**All solutions when $d = 9$.** One free unknown; set $x_3 = t$.

$-5x_2 + 8t = 5 \Rightarrow x_2 = \tfrac{8t-5}{5}$, and $x_1 = 1 - 3x_2 + 2t = \tfrac{20 - 14t}{5}$.

Reparametrise with $t = 5s$ to clear the fractions:

$$\boxed{x = \begin{bmatrix}4\\-1\\0\end{bmatrix} + s\begin{bmatrix}-14\\8\\5\end{bmatrix}, \qquad s \in \mathbb{R}}$$

Check the particular solution: $4 - 3 - 0 = 1$ ✓, $8 - 1 + 0 = 7$ ✓, $16 - 7 + 0 = 9$ ✓.
Check the direction vector solves $Ax = 0$: $-14 + 24 - 10 = 0$ ✓, $-28 + 8 + 20 = 0$ ✓, $-56 + 56 + 0 = 0$ ✓.

*Accept any correct parametrisation, including fractional ones and any other particular solution — the solution **set** is what is marked, not the representative. Full marks require both the particular vector and the direction vector, and 2 of the 8 are for verifying that the direction vector satisfies $Ax = 0$, which most students omit.*

---

## Q2: The Two Pictures (18 points)

### (a) [6]

Solution $(2, \tfrac32)$.

- **Row picture:** two lines in the plane, $x_2 = \tfrac{x_1+1}{2}$ and $x_2 = \tfrac{9 - 3x_1}{2}$, crossing at $(2, \tfrac32)$.
- **Column picture:** $2\begin{bmatrix}1\\3\end{bmatrix} + \tfrac32\begin{bmatrix}-2\\2\end{bmatrix} = \begin{bmatrix}2-3\\6+3\end{bmatrix} = \begin{bmatrix}-1\\9\end{bmatrix}$ ✓

**The two sentences.** Row picture: *a solution is a point lying on every one of the lines at once.* Column picture: *a solution is the list of amounts of each column vector needed to add up to $b$.* 

*Marking: 2 per drawing, 2 for the sentences. **Deduct if the two sentences are the same sentence** — "the values of $x_1$ and $x_2$ that work" twice is the answer the question was written to exclude, and it indicates the student has one picture, not two.*

### (b) [6]

**The relationship: $c_3 = c_1 + c_2$.** Indeed $(1,2,3) + (2,-1,1) = (3,1,4)$.

Two combinations reaching $(6,2,8)$:

$$2c_1 + 2c_2 + 0c_3 = (2+4,\;4-2,\;6+2) = (6,2,8)\ ✓ \qquad\Longrightarrow\qquad x = (2,2,0)$$
$$1c_1 + 1c_2 + 1c_3 = (1+2+3,\;2-1+1,\;3+1+4) = (6,2,8)\ ✓ \qquad\Longrightarrow\qquad x = (1,1,1)$$

**Why they must both work, in one line:** replacing $c_3$ by $c_1 + c_2$ converts the second into the first, so any solution can be slid along $(-1,-1,1)$ — which is precisely L01 §5's line of solutions, found here without eliminating.

*Accept any two distinct valid combinations. Full marks need the relation $c_3 = c_1 + c_2$ **stated**, not merely used.*

### (c) [6]

**The relation:** every column of $B$ has *third entry equal to the sum of the first two*.

$$c_1: 3 = 1 + 2\ ✓ \qquad c_2: 1 = 2 + (-1)\ ✓ \qquad c_3: 4 = 3 + 1\ ✓$$

Write $\phi(v) = v_1 + v_2 - v_3$. Then $\phi(c_1) = \phi(c_2) = \phi(c_3) = 0$, and **$\phi$ is linear**, so for any $x$

$$\phi(Bx) = \phi(x_1c_1 + x_2c_2 + x_3c_3) = x_1\phi(c_1) + x_2\phi(c_2) + x_3\phi(c_3) = 0.$$

Every reachable vector satisfies $v_1 + v_2 = v_3$. But $\phi(6,2,9) = 6 + 2 - 9 = -1 \ne 0$.

$$\boxed{Bx = (6,2,9) \text{ has no solution.}}$$

> **The bonus the question was fishing for:** this argument characterises *every* unreachable $b$ at
> once — $Bx = b$ is solvable **iff** $b_1 + b_2 = b_3$ — whereas elimination settles one $b$ at a
> time. Award the full 6 for a correct $\phi$ argument; award 4 for a correct answer reached by
> elimination, since the question explicitly forbade it but the mathematics is sound. **Students who
> notice that this describes the column space are three weeks ahead; say so on the script.**

*Marking: 2 for finding the relation, 2 for the linearity step, 2 for the conclusion. The linearity step is the one that gets skipped, and it is the whole proof.*

---

## Q3: Three Outcomes (16 points)

### (a) [6]

$$\left[\begin{array}{ccc|c} 1 & 2 & 3 & 1\\ 2 & 5 & 8 & 3\\ 3 & 7 & c & d\end{array}\right]
\xrightarrow[\;\ell_{31}=3\;]{\;\ell_{21}=2\;}
\left[\begin{array}{ccc|c} 1 & 2 & 3 & 1\\ 0 & 1 & 2 & 1\\ 0 & 1 & c-9 & d-3\end{array}\right]
\xrightarrow{\;\ell_{32}=1\;}
\left[\begin{array}{ccc|c} 1 & 2 & 3 & 1\\ 0 & 1 & 2 & 1\\ 0 & 0 & c-11 & d-4\end{array}\right]$$

| | Condition | Why |
|---|---|---|
| **(i) exactly one** | $c \ne 11$, any $d$ | three pivots |
| **(ii) none** | $c = 11$ **and** $d \ne 4$ | last row is $[\,0\ 0\ 0 \mid d-4\,]$, $d-4 \ne 0$ |
| **(iii) infinitely many** | $c = 11$ **and** $d = 4$ | last row is all zero; $x_3$ free |

*Marking: 3 for the echelon form with symbols carried correctly, 1 per case. **The most common error is giving (ii) as "$c = 11$" with no condition on $d$**, which is half an answer.*

### (b) [5]

Suppose $Az = 0$ with $z \ne 0$, and fix any $b$.

**If $Ax = b$ has no solution, we are done** — "no solution" is one of the two permitted outcomes.

**Otherwise it has at least one**, say $x_0$. Then for every scalar $t$,

$$A(x_0 + tz) = Ax_0 + tAz = b + t\cdot 0 = b.$$

Distinct $t$ give distinct vectors $x_0 + tz$, because $z \ne 0$. So there are infinitely many solutions. Exactly one is therefore impossible. $\blacksquare$

*Marking: 2 for the case split being present at all, 2 for the computation, 1 for using $z \ne 0$ to argue the vectors are distinct. **That last step is skipped by most and it is not decoration** — without $z \ne 0$ the "infinitely many" vectors are all the same vector.*

### (c) [5]

$$x_1 + x_2 = 1, \qquad x_2 + x_3 = 1, \qquad x_1 - x_3 = 1$$

**No common point.** Subtracting the second equation from the first gives $x_1 - x_3 = 0$; the third demands $x_1 - x_3 = 1$. Contradiction.

**They do meet in pairs.** No two of the normals $(1,1,0)$, $(0,1,1)$, $(1,0,-1)$ are parallel, so each pair of planes meets in a line. Explicit points:

| Pair | A point on it |
|---|---|
| 1 & 2 | $(1, 0, 1)$ — $1+0=1$ ✓, $0+1=1$ ✓ |
| 1 & 3 | $(1, 0, 0)$ — $1+0=1$ ✓, $1-0=1$ ✓ |
| 2 & 3 | $(1, 1, 0)$ — $1+0=1$ ✓, $1-0=1$ ✓ |

Three parallel lines of intersection: a **triangular prism**. *(Sanity check that the three points are distinct — they are, and a student who produces the same point three times has not built a prism and has made an arithmetic error somewhere.)*

*Accept any valid system. Marking: 2 for the system, 1 for the contradiction, 2 for exhibiting the three pairwise points.*

---

## Q4: What Elimination Costs (22 points)

### (a) [8]

**Forward elimination.** At pivot column $k$ there are $n-k$ rows below, each needing one division and $n-k$ multiply–subtracts across the remaining coefficient columns:

$$\sum_{k=1}^{n-1}(n-k)^2 = \sum_{j=1}^{n-1}j^2 = \frac{(n-1)n(2n-1)}{6} = \frac{n^3}{3} - \frac{n^2}{2} + \frac{n}{6} \approx \frac{n^3}{3}$$

**Back substitution.** Row $i$ needs $n-i$ multiply–subtracts and one division:

$$\sum_{i=1}^{n}(n-i) = \frac{n(n-1)}{2} \approx \frac{n^2}{2}$$

**The 200 right-hand sides, $n = 400$.** $n^3/3 = 2.133\times10^7$ and $n^2/2 = 8\times10^4$.

| | Elimination | Forward pass on the RHS columns | Back substitutions | Total |
|---|---:|---:|---:|---:|
| **(i)** 200 full solves | $200 \times 2.133\times10^7$ | *(included)* | $200 \times 8\times10^4$ | $\mathbf{4.283\times10^9}$ |
| **(ii)** one augmented pass | $2.133\times10^7$ | $200 \times 8\times10^4$ | $200 \times 8\times10^4$ | $\mathbf{5.333\times10^7}$ |

$$\text{ratio} = \frac{4.283\times10^9}{5.333\times10^7} = \boxed{80.3}$$

*(Accept 80 ± 2 — students who drop the $n^2/2$ forward pass on the right-hand sides get $114.7$. **That answer is wrong but the reasoning is sound**, so award 3 of the 4 and note the omitted term. Week 1 makes the same point as $A = LU$, and the omitted term is exactly the forward substitution $Lc = b$.)*

**One hour at $10^{10}$ ops/s.** $n^3/3 = 3600 \times 10^{10} = 3.6\times10^{13}$, so $n = (1.08\times10^{14})^{1/3} \approx \boxed{47{,}600}$.

*Marking: 3 for the two derivations, 3 for the 200-RHS comparison, 2 for the hour.*

### (b) [8]

Measured, `float`, reference machine. Exact answer is $x_1 = 1/(1-\varepsilon)$, which is $1.0$ to sixteen digits throughout.

| $\varepsilon$ | Unpivoted $x_1$ | Relative error | Pivoted $x_1$ |
|---|---|---:|---|
| $10^{-13}$ | $1.000310945187266$ | $3.11\times10^{-4}$ | $1.0000000000000999$ |
| $10^{-14}$ | $0.99920072216264089$ | $7.99\times10^{-4}$ | $1.00000000000001$ |
| $10^{-15}$ | $0.99920072216264078$ | $7.99\times10^{-4}$ | $1.0000000000000009$ |
| $10^{-16}$ | $\mathbf{2.2204460492503131}$ | $\mathbf{1.22}$ | $1.0$ |
| $10^{-17}$ | $\mathbf{0.0}$ | $\mathbf{1.00}$ | $1.0$ |
| $10^{-20}$ | $\mathbf{0.0}$ | $\mathbf{1.00}$ | $1.0$ |

**Where it is not monotone: between $10^{-16}$ and $10^{-17}$ the error *falls*, from $122\%$ to exactly $100\%$.**

**Explanation.** The error is worst at the *transition*, not in the limit.

- Once $\varepsilon \le 10^{-17}$, both $1 - 1/\varepsilon$ and $2 - 1/\varepsilon$ round to the same value $-1/\varepsilon$, so $x_2 = 1$ **exactly**, $1 - x_2 = 0$ **exactly**, and $x_1 = 0/\varepsilon = 0$. An answer of $0$ for $1$ is an error of exactly $1.00$, and it cannot get worse, because $0$ is as far from $1$ as this failure mode can reach.
- At $\varepsilon = 10^{-16}$ the cancellation is not quite total: $1 - x_2$ survives as $2.2204\times10^{-16} = 2^{-52}$, **one unit in the last place of $1.0$ — pure rounding noise.** Dividing noise by $\varepsilon = 10^{-16}$ multiplies it by $10^{16}$, giving $2.22$ and an error of $122\%$.

**So the mechanism is: total cancellation gives a clean $0$; near-total cancellation amplifies garbage.** The second is worse, and it is worse in the way that matters, because $2.22$ looks more like an answer than $0.0$ does.

*Marking: 4 for the six-row table, 4 for identifying the non-monotone step **and** explaining it. Accept any explanation that correctly locates the amplified ulp; do not accept "floating point is inaccurate".*

### (c) [6]

**The step:** $a_{22} \leftarrow 1 - \ell\cdot 1$ with $\ell = 1/\varepsilon = 10^{17}$, and $b_2 \leftarrow 2 - \ell\cdot 1$.

**The quantity lost:** the original $a_{22} = 1$ and $b_2 = 2$. A `double` holds 53 significand bits, about 16 decimal digits; next to $10^{17}$ the values $1$ and $2$ fall below the last representable bit, so **both results round to exactly $-10^{17}$** and every trace of the second equation's own coefficients is gone.

The rest is forced: $x_2 = (-10^{17})/(-10^{17}) = 1$ exactly, so $1 - x_2 = 0$ exactly, so $x_1 = 0/\varepsilon = 0$.

**What pivoting changes.** Swapping puts the $1$ in the pivot position, making $\ell = \varepsilon/1 = 10^{-17}$. The updates become $1 - 10^{-17}\cdot 1$ and $1 - 10^{-17}\cdot 2$ — a **tiny** correction to a number of size $1$, which rounds to $1$ and loses nothing that was there to lose. No large multiplier, no cancellation, no amplification. **The general guarantee is $|\ell| \le 1$**, and it is bought with $O(n^2)$ comparisons.

*Marking: 2 for naming the step, 2 for "the 1 and the 2 fall below the last bit", 2 for the pivoting contrast. A student who says "we divide by zero" has not read the trace — nothing divides by zero here, and that is what makes the failure silent.*

---

## Q5: Nonsingular Is Not the Same as Safe (20 points)

### (a) [8]

Exact $\operatorname{cond}_\infty$ via `Fraction`; error from a `float` solve with partial pivoting, $b_i = \sum_j h_{ij}$.

| $n$ | $\operatorname{cond}_\infty(H_n)$ | $\max\lvert x_i - 1\rvert$ | Digits obtained | Rule predicts | Discrepancy |
|---:|---:|---:|---:|---:|---:|
| 4 | $2.84\times10^{4}$ | $4.56\times10^{-13}$ | 12.3 | 11.5 | $+0.8$ |
| 6 | $2.91\times10^{7}$ | $5.27\times10^{-11}$ | 10.3 | 8.5 | $+1.8$ |
| 8 | $3.39\times10^{10}$ | $1.37\times10^{-7}$ | 6.9 | 5.5 | $+1.4$ |
| 10 | $3.54\times10^{13}$ | $7.18\times10^{-4}$ | 3.1 | 2.5 | $+0.6$ |
| 12 | $4.12\times10^{16}$ | $5.95\times10^{-3}$ | 2.2 | $-0.6$ | $+2.8$ |

**The rule is pessimistic, and consistently so** — every discrepancy is positive, between $+0.6$ and $+2.8$ digits. It never promised more accuracy than was delivered.

**That is the right direction for it to be wrong in**, and worth saying so: a rule of thumb about numerical accuracy that erred optimistically would be worse than no rule. It bounds the damage rather than predicting it.

**At $n = 12$ it predicts $-0.6$ digits**, which is not a quantity of digits. The correct reading is *"no digit is guaranteed"* — and indeed the answer has two, by luck rather than by right, since $\operatorname{cond}(H_{12}) = 4.1\times10^{16}$ exceeds $1/\varepsilon_{\text{mach}} = 4.5\times10^{15}$ and the stored matrix is no longer reliably the matrix that was meant.

*Marking: 5 for the table, 3 for "pessimistic, consistently, and that is the useful direction". **Award the full 3 to any student who notices the $n = 12$ prediction is negative and says what that means**, whether or not they use the phrase.*

### (b) [6]

**(i) $\det = 10^{-8}$, perfectly conditioned.**

$$A = \begin{bmatrix}10^{-4} & 0\\ 0 & 10^{-4}\end{bmatrix}, \qquad \det A = 10^{-8}, \qquad A^{-1} = \begin{bmatrix}10^{4} & 0\\ 0 & 10^{4}\end{bmatrix}$$

$\lVert A\rVert_\infty = 10^{-4}$, $\lVert A^{-1}\rVert_\infty = 10^{4}$, so $\operatorname{cond}_\infty(A) = 1$ — **the smallest value a condition number can take.** Solving with this matrix is exact division by a power of ten.

**(ii) $\det = 1$, atrociously conditioned.**

$$A = \begin{bmatrix}10^{6} & 0\\ 0 & 10^{-6}\end{bmatrix}, \qquad \det A = 1, \qquad A^{-1} = \begin{bmatrix}10^{-6} & 0\\ 0 & 10^{6}\end{bmatrix}$$

$\lVert A\rVert_\infty = 10^{6}$, $\lVert A^{-1}\rVert_\infty = 10^{6}$, so $\operatorname{cond}_\infty(A) = 10^{12}$.

**What the pair establishes.** The determinant and the condition number are **independent**: knowing one constrains the other not at all. The determinant is not scale-invariant — multiplying $A$ by $c$ multiplies it by $c^n$ — whereas the condition number is, since the $c$ in $\lVert cA\rVert$ cancels against the $1/c$ in $\lVert (cA)^{-1}\rVert$. **A quantity that changes when you switch from metres to millimetres cannot be measuring how hard the problem is.**

*Marking: 2 per matrix (both must include the norm computations), 2 for the conclusion. **The scale-invariance observation is the answer**; "they measure different things" alone is worth 1 of the 2.*

### (c) [6]

**Why the conclusion fails.** The residual measures whether $x$ nearly satisfies the *equations*. The error measures whether $x$ is near the *answer*. The two are related by the condition number and by nothing else:

$$\frac{\lVert x - \hat{x}\rVert}{\lVert \hat{x}\rVert} \;\le\; \operatorname{cond}(A)\,\frac{\lVert Ax - b\rVert}{\lVert b\rVert}$$

**When $\operatorname{cond}(A)$ is large the bound is vacuous**, and a tiny residual is compatible with an enormous error. Geometrically: an ill-conditioned $A$ squashes a long thin region of $x$-space into a tiny region of $b$-space, so being close in $b$ says almost nothing about being close in $x$.

**Explicit $2\times2$.** Let $\delta = 10^{-14}$:

$$A = \begin{bmatrix}1 & 1\\ 1 & 1+\delta\end{bmatrix}, \qquad b = \begin{bmatrix}2\\ 2+\delta\end{bmatrix}, \qquad \hat{x} = \begin{bmatrix}1\\1\end{bmatrix} \text{ exactly.}$$

Take the computed answer $x = (2, 0)$. Then

$$Ax = \begin{bmatrix}2\\ 2\end{bmatrix}, \qquad \lVert Ax - b\rVert_\infty = \delta = \boxed{10^{-14}}, \qquad \lVert x - \hat{x}\rVert_\infty = \boxed{1}$$

**A residual of $10^{-14}$ and an error of $100\%$, on the same computation.** And $\operatorname{cond}_\infty(A) = (2+\delta)\cdot\frac{2+\delta}{\delta} \approx 4\times10^{14}$, which is exactly the factor that permits it: $10^{-14} \times 4\times10^{14} = 4$, and an error of $1$ sits comfortably inside that.

**What the colleague should have done:** estimate $\operatorname{cond}(A)$ — `numpy.linalg.cond`, or LAPACK's `dgecon`, which is $O(n^2)$ once the factorisation exists and is therefore free — and multiply it by the relative residual to get an actual error bound. A small residual on its own certifies only that the solver did its job; **it says nothing about whether the problem was worth solving that way.**

*Marking: 2 for distinguishing residual from error, 2 for the explicit example with both numbers computed, 2 for "estimate the condition number". **A student who gives the inequality but no example gets 4** — the question asked for a construction, and the construction is where the understanding shows.*

---

## Grade Distribution Expected

| Band | Score | Description |
|---|---|---|
| Strong | 88–100 | Q2(c) via the linear functional, Q5(c) constructed rather than described |
| Solid | 72–87 | All of Q1–Q4 correct; Q5(c) argued but not constructed |
| Passing | 55–71 | Q1 and Q3(a) correct; Q4 and Q5 attempted with the scripts run |
| Concerning | < 55 | **Arithmetic errors in Q1 are the signal to watch.** A student who cannot eliminate a $3\times3$ reliably by the Friday of Week 1 will not survive Week 5's determinants. Recommend the Help Desk before Week 2 |

---

*MATH 241 · Week 0 · PS 0 Solutions · © CSE Department*
