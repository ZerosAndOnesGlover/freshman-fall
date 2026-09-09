# MATH 241 · Linear Algebra
## Week 0 · Lecture 3 of 3 · **Friday** of Week 0
### What Elimination Costs, and When It Lies

---

**Reading:** Strang §2.2 (the cost paragraph), §9.1–§9.3 · **Previous:** L02, the algorithm · **Next:** Week 1, matrices as objects

> **Every number in this lecture was computed by `resources/elimination.py`**, which ships with this
> week. Exact results were computed in Python's `Fraction`; floating-point results in `float`, on
> the department reference machine (Intel i5-8250U, Ubuntu 24.04.4, CPython 3.14). **Run it.** The
> exact figures will match yours to the digit; the one timing will not, and should not.

---

## 1. Two Questions L02 Left Open

L02 gave an algorithm that always terminates and always gives the right answer. Both halves of that sentence need auditing:

1. **"Always terminates"** — in how long? The answer decides which problems are solved by elimination and which need something else entirely.
2. **"Always gives the right answer"** — in exact arithmetic, yes, and the proof in L02 §2 is airtight. **Your computer does not do exact arithmetic.** In floating point the same algorithm on the same matrix can return $0$ where the answer is $1$, with no error and no warning.

This lecture is those two audits. The first is arithmetic. The second is the reason numerical linear algebra exists as a subject.

---

## 2. The Cost, Counted

Count **multiply–subtract pairs**; the divisions are lower-order and the additions come free with the multiplications on any machine built since 1990.

**Forward elimination.** At pivot column $k$ there are $n - k$ rows below. Each needs one division for its multiplier, then one multiply–subtract for each of the $n-k$ remaining coefficient columns. So step $k$ costs about $(n-k)^2$, and

$$\sum_{k=1}^{n-1}(n-k)^2 \;=\; \sum_{j=1}^{n-1} j^2 \;=\; \frac{(n-1)n(2n-1)}{6} \;\approx\; \boxed{\frac{n^3}{3}}$$

**Back substitution.** Row $i$ needs $n - i$ multiply–subtracts and one division:

$$\sum_{i=1}^{n} (n-i) \;=\; \frac{n(n-1)}{2} \;\approx\; \boxed{\frac{n^2}{2}}$$

| $n$ | Elimination $\approx n^3/3$ | Back substitution $\approx n^2/2$ | Ratio |
|---:|---:|---:|---:|
| 10 | 333 | 50 | 7 |
| 100 | $3.33 \times 10^5$ | $5 \times 10^3$ | 67 |
| 1,000 | $3.33 \times 10^8$ | $5 \times 10^5$ | 667 |
| 10,000 | $3.33 \times 10^{11}$ | $5 \times 10^7$ | 6,667 |

**Three consequences, and all three shape the rest of the course.**

**(a) The triangular half is free.** At $n = 1000$ back substitution is $0.15\%$ of the work. **The expensive thing is *reaching* triangular form, not using it** — which is exactly why Week 1 wants to keep the factorisation: a second right-hand side with the same $A$ should not cost another $3.33 \times 10^8$ operations, and once you have $L$ and $U$ it costs $n^2$.

**(b) Cubic growth is brutal and it is also survivable.** Ten times the unknowns is a **thousand** times the work. Doubling $n$ costs $8\times$. But $n^3$ is a polynomial, and for $n$ up to a few tens of thousands a dense solve is entirely routine on a laptop.

**(c) Past that, nobody eliminates.** Google's PageRank matrix has $n \approx 10^{9}$; $n^3/3$ is $3 \times 10^{26}$ operations, which at a teraflop is ten million years. **This is why Week 6 computes an eigenvector by repeated multiplication instead**, and why enormous systems in practice are sparse, iterative, or both. When Week 6 asks why PageRank is not solved by elimination, the answer is this table.

> **Cramer's rule, killed early.** Week 5 will show you a formula that writes each $x_i$ as a ratio
> of determinants. It is beautiful and it is $O(n!)$ if you evaluate the determinants by their
> definition — for $n = 20$ that is $2.4 \times 10^{18}$ terms, against elimination's $2{,}700$.
> **Cramer's rule is a theoretical instrument, not a method**, and you should know that before you
> meet it rather than after.

---

## 3. Exact Arithmetic Is Expensive in a Different Way

Elimination on integers stays exact if you keep fractions, and `elimination.py` does. There is a price, and it is not the one you expect:

```
exact elimination on a random 100x100 integer matrix: 2.66 s
the widest pivot it produced needs 299 decimal digits to write down.
```

**Every entry of that matrix was a single digit between $-9$ and $9$.** The pivots are ratios of determinants of growing submatrices, and those determinants grow roughly like $n!$ — so by row 100 the numerators are three hundred digits long, each arithmetic operation is on a big integer rather than a machine word, and the $n^3/3$ operation count buys you nothing because the operations are no longer constant-time.

**So exact arithmetic does not scale, and the alternative is floating point.** Which brings us to why the alternative is dangerous.

---

## 4. The Same Algorithm, Two Orders, Two Answers

$$\begin{aligned}\varepsilon x_1 + x_2 &= 1\\ x_1 + x_2 &= 2\end{aligned}$$

Subtract to get $(\varepsilon - 1)x_1 = -1$, so the **exact** answer is

$$x_1 = \frac{1}{1-\varepsilon}, \qquad x_2 = \frac{1 - 2\varepsilon}{1 - \varepsilon}.$$

For any $\varepsilon$ below $10^{-15}$ both are $1$ to every digit a `double` can hold. **The matrix is nonsingular, the answer is benign, nothing about this problem is hard.**

Now run L02's algorithm on it in floating point, taking the pivots in the order they come:

| $\varepsilon$ | Elimination as written | With a row swap first |
|---|---|---|
| $10^{-15}$ | $x_1 = 0.99920072216264078$ | $x_1 = 1.0000000000000009$ |
| $10^{-16}$ | $x_1 = \mathbf{2.2204460492503131}$ | $x_1 = 1.0$ |
| $10^{-17}$ | $x_1 = \mathbf{0.0}$ | $x_1 = 1.0$ |
| $10^{-20}$ | $x_1 = \mathbf{0.0}$ | $x_1 = 1.0$ |

**Zero, for an answer of one. And 2.22, for an answer of one.** No exception, no warning, no `NaN` — just a number, returned confidently, with a $100\%$ error.

### Where it goes wrong, exactly

The multiplier is $m = 1/\varepsilon$, which for $\varepsilon = 10^{-17}$ is $10^{17}$. Elimination then computes

$$a_{22} \leftarrow 1 - m = 1 - 10^{17}, \qquad b_2 \leftarrow 2 - m = 2 - 10^{17}.$$

A `double` carries 53 bits of significand, about 16 decimal digits. **Next to $10^{17}$, the $1$ and the $2$ are below the last bit and are simply gone**: both results round to exactly $-10^{17}$. So $x_2 = b_2/a_{22} = 1$ *exactly*, and back substitution gives

$$x_1 = \frac{1 - x_2}{\varepsilon} = \frac{1 - 1}{\varepsilon} = \frac{0}{\varepsilon} = 0.$$

The $\varepsilon = 10^{-16}$ row is the same failure caught mid-collapse: there $1 - m$ rounds to $-10^{16}$ and $2-m$ to $-9999999999999998$, so $x_2 = 0.99999999999999978$ and $1 - x_2 = 2.2204460492503131\times 10^{-16}$ — **which is exactly $2^{-52}$, one unit in the last place of $1.0$.** The subtraction returned pure rounding noise, and dividing noise by $10^{-16}$ scaled it up to $2.22$.

> **The lesson generalises past this example.** Subtracting two nearly equal floating-point numbers
> is *catastrophic cancellation*: the leading digits agree and annihilate, and what survives is
> whatever rounding error was hiding in the digits below. The error was always there; the
> subtraction promoted it to the leading digit. **A large multiplier is a machine for manufacturing
> nearly equal numbers**, which is why the fix is to make multipliers small.
>
> **CS 201 Week 1 is this from the other side** — the anatomy of an IEEE 754 `double`, and why
> floating-point addition is not associative. You are meeting the consequence a week before the
> mechanism; the mechanism is worth the wait.

---

## 5. Partial Pivoting

**The rule.** At column $k$, before eliminating, look down column $k$ from row $k$ to row $n$ and **swap the row with the largest absolute value into the pivot position.**

That is the entire fix. It is operation R2, so it changes nothing about the solution set, and it costs $O(n^2)$ comparisons across the whole algorithm — **nothing, against $n^3/3$.**

**What it buys.** Every multiplier becomes

$$|\ell_{ik}| = \left|\frac{a_{ik}}{a_{kk}}\right| \le 1$$

because the pivot is now the largest candidate. No multiplier can amplify anything, so no step can manufacture the huge intermediate that destroyed §4. In the table above, the swapped column is right to sixteen digits at every $\varepsilon$.

> **Use it always, not only when you suspect trouble.** Every production solver — LAPACK's `dgesv`,
> MATLAB's backslash, `numpy.linalg.solve`, every one — does partial pivoting unconditionally, and
> none of them offers an option to switch it off. **A zero pivot is not the reason to swap. A small
> one is**, and "small" is relative to the other candidates, which is why the rule is *largest
> available* rather than *any nonzero*.

**By hand, in this course, you may pivot for convenience instead** — swap to get a $1$ into the pivot and avoid fractions. Exact arithmetic has no rounding to protect against, so the numerical rule does not apply to your paper. **It applies to every line of code you will ever write.**

**What it does not buy: a guarantee.** Partial pivoting bounds the multipliers, not the answer. There are matrices — Wilkinson's, constructed exactly for this — on which entries still grow by $2^{n-1}$ despite it. They are rare enough that everybody uses partial pivoting anyway, and the reason they are rare is genuinely not well understood. **Complete pivoting** (search the whole remaining submatrix, swap rows *and* columns) has provably better bounds and costs $O(n^3)$ comparisons, so nobody uses it.

---

## 6. Nonsingular Is Not the Same as Safe

§4's matrix was ill-behaved because of how the algorithm handled it, and a swap fixed it. **Some matrices cannot be fixed by any algorithm**, because the difficulty is in the problem rather than the method.

The **Hilbert matrix** $H_n$ has entries $h_{ij} = 1/(i+j-1)$:

$$H_4 = \begin{bmatrix}
1 & \tfrac12 & \tfrac13 & \tfrac14\\[2pt]
\tfrac12 & \tfrac13 & \tfrac14 & \tfrac15\\[2pt]
\tfrac13 & \tfrac14 & \tfrac15 & \tfrac16\\[2pt]
\tfrac14 & \tfrac15 & \tfrac16 & \tfrac17\end{bmatrix}$$

**Every $H_n$ is invertible**, and its inverse has integer entries. There is nothing degenerate about it. Solve $H_n x = b$ with $b$ chosen so the exact answer is $x = (1,1,\dots,1)$, in double precision, **with partial pivoting**:

| $n$ | $\operatorname{cond}_\infty(H_n)$ *(exact)* | Worst $\lvert x_i - 1\rvert$ | Correct digits |
|---:|---:|---:|---:|
| 3 | $748$ | $1.03 \times 10^{-14}$ | 14 |
| 5 | $9.44 \times 10^{5}$ | $6.17 \times 10^{-13}$ | 12 |
| 8 | $3.39 \times 10^{10}$ | $1.37 \times 10^{-7}$ | 7 |
| 10 | $3.54 \times 10^{13}$ | $7.18 \times 10^{-4}$ | 3 |
| 12 | $4.12 \times 10^{16}$ | $5.95 \times 10^{-3}$ | 2 |

**At $n = 12$ you have two correct digits out of sixteen, from a perfect algorithm on an invertible matrix.**

And the determinant does *not* diagnose it. $\det H_{10} = 2.16 \times 10^{-53}$, which is tiny — but scaling $H_{10}$ by $10$ multiplies its determinant by $10^{10}$ and changes the accuracy of the solve not at all. **A small determinant is not what "nearly singular" means.** Week 5 returns to this with the determinant properly defined; the warning belongs here, next to the evidence.

---

## 7. The Condition Number

The right measurement is the **condition number**

$$\operatorname{cond}(A) = \lVert A\rVert \cdot \lVert A^{-1}\rVert$$

which asks: **if I perturb $b$ by a relative amount $\delta$, how much can the relative change in $x$ be?** The answer is up to $\operatorname{cond}(A) \cdot \delta$, and that bound is attained.

**The rule of thumb, and it is the practical content of the whole lecture:**

$$\text{correct decimal digits} \;\approx\; 16 - \log_{10}\operatorname{cond}(A)$$

Check it against the table. $n = 8$: $16 - \log_{10}(3.39\times10^{10}) = 16 - 10.5 = 5.5$, measured 7. $n = 10$: $16 - 13.5 = 2.5$, measured 3. $n = 12$: $16 - 16.6 = -0.6$, measured 2. **The estimate is pessimistic by a digit or two and it gets the shape exactly right**, which is all a rule of thumb owes you.

> **$\operatorname{cond}(A) \ge 1$ always, and $\operatorname{cond}(A) = 1$ for the best-behaved
> matrices there are.** Which ones those are is Week 8's answer — orthogonal matrices — and it is
> the reason Week 9 prefers QR to the normal equations, and the reason Week 11's SVD is the
> numerically trustworthy factorisation. **This number is the thread running through the second half
> of the course.**

Your input data has error in it before any arithmetic happens — measurements are rounded, and $0.1$ is not representable in binary. **The condition number tells you how much of that error the problem will hand back to you, and no algorithm can do better.** That is why $\operatorname{cond}(H_{12}) = 4 \times 10^{16}$ is fatal: it exceeds $1/\varepsilon_{\text{mach}} = 4.5 \times 10^{15}$, so the answer to the problem you *meant* to pose and the answer to the one your machine actually stored can differ in the first digit.

---

## 8. What to Actually Do

| Situation | Do |
|---|---|
| Solving by hand in this course | Exact arithmetic. Swap for convenience, keep fractions, check by substitution |
| Solving in code, dense, $n \lesssim 10^4$ | A library solver — `numpy.linalg.solve`, LAPACK `dgesv`. **Never write your own** |
| Solving in code, same $A$ many times | Factor once (Week 1's $A = LU$), reuse. $n^2$ per extra solve rather than $n^3/3$ |
| Solving in code, $n$ enormous | Iterative methods, sparsity. Elimination is not on the table — §2(c) |
| Answer looks wrong | Compute the residual $\lVert Ax - b\rVert$ **and** estimate $\operatorname{cond}(A)$. A small residual with a huge condition number means the answer is wrong and the algorithm is blameless |
| **Ever** | Do not invert $A$ to solve $Ax = b$. **Week 1's L05** is that argument with numbers |

---

## 9. What to Take Away

1. **Elimination costs $\approx n^3/3$; back substitution $\approx n^2/2$.** Reaching triangular form is the expensive part, which is why Week 1 keeps the factorisation.
2. **Cubic is fine to $n \sim 10^4$ and hopeless at $10^9$.** That threshold is why iterative methods exist and why PageRank is not a linear solve.
3. **Exact arithmetic does not scale either** — pivots from a single-digit $100\times100$ matrix needed 299 decimal digits.
4. **In floating point, L02's algorithm can be $100\%$ wrong on a benign problem**, silently, because a large multiplier manufactures catastrophic cancellation.
5. **Partial pivoting is the fix: always swap the largest available entry into the pivot.** It bounds every multiplier by $1$, costs $O(n^2)$, and is unconditional in every real solver.
6. **A matrix can be invertible and still useless.** $\operatorname{cond}(A)$, not $\det A$, is the diagnostic, and you lose about $\log_{10}\operatorname{cond}(A)$ of your sixteen digits.

---

## Exercises

*(Not assessed. 1–3 are paper; 4–6 want `elimination.py`.)*

1. Verify $\sum_{j=1}^{n-1} j^2 = \frac{(n-1)n(2n-1)}{6}$ by induction, and confirm it is $\approx n^3/3$.
2. You have $A$ fixed and 50 different right-hand sides. Compare the total cost of solving each from scratch against factoring once and reusing, at $n = 500$. Give the ratio.
3. Do §4's elimination by hand with $\varepsilon = 10^{-17}$, in **exact** arithmetic. You will get $x_1 = 1$ to as many digits as you care to write. Which single step is the one the machine cannot reproduce?
4. Add $\varepsilon = 10^{-14}$ and $10^{-13}$ to the table in `elimination.py`. At what $\varepsilon$ does the unpivoted answer become acceptable to you, and what did "acceptable" mean when you decided?
5. Extend the Hilbert table to $n = 14$ and $n = 16$. Does the rule of thumb still hold once $\operatorname{cond}$ passes $10^{16}$? Explain what it could possibly mean for it to hold there.
6. Build a $2\times2$ matrix with $\det A = 10^{-8}$ and $\operatorname{cond}_\infty(A) = 1$. *(It exists. Finding it is the point: it proves the determinant and the condition number are measuring different things.)*

---

*MATH 241 · Week 0 · L03 · © CSE Department*
