# MATH 241 · Linear Algebra
## Week 0 · Lecture 2 of 3 · **Tuesday** of Week 0
### Gaussian Elimination: Pivots, Row Operations, and Echelon Form

*“But in our opinion truths of this kind should be drawn from notions rather than from notations.”* — Carl Friedrich Gauss, *Disquisitiones Arithmeticae* (1801), Art. 76

---

**Reading:** Strang §2.2, §2.3 (skim §2.3 — the matrix form of what we do here is Week 1's L06) · **Previous:** L01, the two pictures · **Next:** L03, cost and failure

**Coursework:** 📝 **PS 0** released Wed this week, due Fri of Week 1 17:00

---

## 1. The Idea, in One Sentence

**Some systems are trivial to solve, so turn every system into one of those.**

A system is trivial when it is **triangular**:

$$\begin{aligned}
2x_1 + \phantom{1}x_2 - \phantom{1}x_3 &= \phantom{1}1\\
3x_2 + 2x_3 &= 12\\
4x_3 &= 12
\end{aligned}$$

Read it bottom-up. The last equation gives $x_3 = 3$ outright. Put that into the second: $3x_2 + 6 = 12$, so $x_2 = 2$. Put both into the first: $2x_1 + 2 - 3 = 1$, so $x_1 = 1$. **No cleverness, no guessing, no searching** — one division per line, working upwards. That is called **back substitution**, and it is the reason the whole algorithm exists.

Gaussian elimination is the other half: **a procedure that turns any system into a triangular one without changing its solutions.** Two guarantees, and both matter. It always terminates, and the answer it produces is the answer to the question you asked.

---

## 2. The Three Operations, and Why They Are Safe

Elimination is allowed to do exactly three things to a system:

| | Operation | Notation |
|---|---|---|
| **R1** | Add a multiple of one equation to another | $R_i \leftarrow R_i - m\,R_k$ |
| **R2** | Swap two equations | $R_i \leftrightarrow R_k$ |
| **R3** | Multiply an equation by a **nonzero** constant | $R_i \leftarrow cR_i$ |

**Each one preserves the solution set exactly** — not "approximately", not "usually". This is the theorem that licences the whole method, so it is worth seeing the argument once rather than trusting it.

> **Claim.** If $x$ satisfies the original system, it satisfies the modified one, and conversely.
>
> *Forward, for R1.* Suppose $x$ satisfies every equation, in particular $R_i(x) = b_i$ and
> $R_k(x) = b_k$. Then the new $i$-th equation evaluates to $R_i(x) - m R_k(x) = b_i - m b_k$, which
> is exactly its new right-hand side. So $x$ satisfies it.
>
> *Backwards.* **Every one of the three is reversible**, by an operation of the same kind: R1 is
> undone by $R_i \leftarrow R_i + m R_k$, R2 by the same swap, R3 by multiplying by $1/c$. So any $x$
> satisfying the new system satisfies the old one by the forward argument applied to the inverse
> operation. $\square$

**Reversibility is the whole content of the proof, and it is where R3's "nonzero" comes from.** Multiplying an equation by $0$ turns it into $0 = 0$, which is not reversible and which quietly throws a constraint away: $x_1 = 5$ becomes $0 = 0$, and the solution set grows from a point to everything. **The one forbidden operation is forbidden for a reason you can state.**

---

## 3. The Augmented Matrix

The symbols $x_1, x_2, x_3$ carry no information — only their **positions** do. So drop them and keep the numbers, with a bar where the equals signs were:

$$\left[\begin{array}{ccc|c} 2 & 1 & -1 & 1\\ 4 & 5 & 0 & 14\\ -2 & 8 & 11 & 47\end{array}\right]$$

This is the **augmented matrix** $[\,A \mid b\,]$. A row operation is now a row operation, literally. **The right-hand side must ride along** — it is the fourth column, and every operation applied to the coefficients is applied to it too. Forgetting the last column is the single most common arithmetic error in this material, and it produces an answer to a different question with no sign that anything went wrong.

---

## 4. Elimination, Worked

The goal: **zeros below the diagonal, one column at a time, left to right.**

**Column 1.** The entry $a_{11} = 2$ is the first **pivot**. Every other entry in column 1 must become zero, and each is killed by subtracting the right multiple of row 1.

The multiplier is always the same quotient: *the entry you want to kill, divided by the pivot.*

$$\ell_{21} = \frac{4}{2} = 2, \qquad \ell_{31} = \frac{-2}{2} = -1$$

$$R_2 \leftarrow R_2 - 2R_1, \qquad R_3 \leftarrow R_3 - (-1)R_1 = R_3 + R_1$$

$$\left[\begin{array}{ccc|c} \mathbf{2} & 1 & -1 & 1\\ 0 & 3 & 2 & 12\\ 0 & 9 & 10 & 48\end{array}\right]$$

*(Row 2: $4-4=0$, $5-2=3$, $0+2=2$, $14-2=12$. Row 3: $-2+2=0$, $8+1=9$, $11-1=10$, $47+1=48$.)*

**Column 2.** The new $a_{22} = 3$ is the second pivot. **Row 1 is finished and is never touched again** — touching it would put a nonzero back into column 1.

$$\ell_{32} = \frac{9}{3} = 3, \qquad R_3 \leftarrow R_3 - 3R_2$$

$$\left[\begin{array}{ccc|c} \mathbf{2} & 1 & -1 & 1\\ 0 & \mathbf{3} & 2 & 12\\ 0 & 0 & \mathbf{4} & 12\end{array}\right]$$

*(Row 3: $9-9=0$, $10-6=4$, $48-36=12$.)*

**Done.** The matrix is upper triangular, the pivots are $\mathbf{2, 3, 4}$, and back substitution from §1 gives

$$x_3 = 3, \qquad x_2 = 2, \qquad x_1 = 1.$$

**Three multipliers were computed and thrown away: $\ell_{21} = 2$, $\ell_{31} = -1$, $\ell_{32} = 3$.** Write them in the margin. **Week 1's L06 shows they are a matrix**, that $A = LU$, and that having kept them makes every subsequent solve with the same $A$ almost free.

> **The right-hand side was transformed too, from $(1, 14, 47)$ to $(1, 12, 12)$.** That second
> vector is not junk either — it is what you get by running the multipliers forward, and Week 1
> calls it $L^{-1}b$. Keep it in the margin as well.

---

## 5. The Algorithm, Stated Once

```
for k = 1 to n:                            # k is the pivot column
    if a[k][k] == 0: find a row below with a nonzero in column k and swap
    if no such row exists: no pivot in this column -- go to column k+1
    for i = k+1 to n:                      # every row below the pivot
        m = a[i][k] / a[k][k]              # the multiplier
        row i  <-  row i  -  m * row k     # including the right-hand side
```

`resources/elimination.py` in this week's folder is that loop in Python, in `Fraction` so that it is exactly the arithmetic you would do by hand. Run it on the example above and it prints the same echelon form, the same three multipliers and the same pivots.

**Two vocabulary items, used from now on without comment:**

- A **pivot** is the first nonzero entry in a row, once elimination has finished with it. Pivots are what the algorithm produces; they are not chosen in advance.
- A matrix is in **row echelon form** when every pivot is strictly to the right of the pivot in the row above, and any all-zero rows are at the bottom. The general shape is a staircase, and the steps need not be one column wide:

$$\begin{bmatrix}
\boxed{\;*\;} & * & * & * & *\\
0 & 0 & \boxed{\;*\;} & * & *\\
0 & 0 & 0 & 0 & \boxed{\;*\;}\\
0 & 0 & 0 & 0 & 0
\end{bmatrix}$$

Three pivots, in columns 1, 3 and 5. **Columns 2 and 4 have no pivot**, and Week 2 will call their unknowns *free* — they are the ones you get to choose, and each one is a dimension of solutions.

---

## 6. When the Pivot Is Zero

A zero in the pivot position is not one problem. **It is two, and they have different fixes.**

### Case A — a fixable zero: swap

$$\begin{bmatrix} 0 & 2 & 3\\ 1 & 1 & 1\\ 2 & 5 & 8\end{bmatrix}$$

$a_{11} = 0$, so there is no multiplier: you cannot divide by it. But row 2 has a $1$ in that column. **Swap rows 1 and 2** — operation R2, which changes nothing about the solutions — and carry on:

$$\begin{bmatrix} 1 & 1 & 1\\ 0 & 2 & 3\\ 2 & 5 & 8\end{bmatrix} \xrightarrow{\;R_3 - 2R_1\;} \begin{bmatrix} 1 & 1 & 1\\ 0 & 2 & 3\\ 0 & 3 & 6\end{bmatrix} \xrightarrow{\;R_3 - \frac32 R_2\;} \begin{bmatrix} 1 & 1 & 1\\ 0 & 2 & 3\\ 0 & 0 & \tfrac32\end{bmatrix}$$

Three pivots. **Nothing was wrong with the matrix; the rows were in an unhelpful order.**

### Case B — an unfixable zero: singular

$$\begin{bmatrix} 1 & 2 & 3\\ 2 & -1 & 1\\ 3 & 1 & 4\end{bmatrix} \xrightarrow{\;R_2 - 2R_1,\; R_3 - 3R_1\;} \begin{bmatrix} 1 & 2 & 3\\ 0 & -5 & -5\\ 0 & -5 & -5\end{bmatrix} \xrightarrow{\;R_3 - R_2\;} \begin{bmatrix} 1 & 2 & 3\\ 0 & -5 & -5\\ 0 & 0 & 0\end{bmatrix}$$

**A row of zeros, and nothing below it to swap in.** Only two pivots. This is L01 §5's matrix, whose third row was the sum of the first two, and elimination has found that out without being told.

**Now the right-hand side decides which of the two bad outcomes you get.** Run the same operations on the augmented column:

| $b$ | Last row becomes | Meaning |
|---|---|---|
| $(6, 2, 8)$ | $[\,0\ 0\ 0 \mid 0\,]$ | $0 = 0$. True, and vacuous. **Infinitely many solutions** — one free unknown, so a line of them |
| $(6, 2, 9)$ | $[\,0\ 0\ 0 \mid 1\,]$ | $0 = 1$. **No solution** |

> **This is the payoff of the whole lecture.** Elimination does not merely solve solvable systems.
> It *classifies* every system, and it needs no advance knowledge of which kind it has been handed.
> Run it and read the last rows: a pivot in every column and no contradiction means one solution; a
> row $[\,0 \cdots 0 \mid c\,]$ with $c \ne 0$ means none; a missing pivot with no contradiction
> means infinitely many.

### The count that summarises it

For an $n \times n$ system, let $r$ be the number of pivots elimination produces.

| | |
|---|---|
| $r = n$, always | **exactly one solution**, for every $b$. The matrix is **nonsingular** |
| $r < n$ | **singular.** Depending on $b$: no solution, or infinitely many with $n - r$ free unknowns |

Week 2 gives $r$ its name — the **rank** — and Week 3 explains why it is the single most informative number attached to a matrix.

---

## 7. Reduced Row Echelon Form

Echelon form is enough to solve by back substitution, and you can go further. **Keep eliminating upwards, then scale every pivot to $1$:**

$$\left[\begin{array}{ccc|c} 2 & 1 & -1 & 1\\ 0 & 3 & 2 & 12\\ 0 & 0 & 4 & 12\end{array}\right]
\longrightarrow
\left[\begin{array}{ccc|c} 1 & 0 & 0 & 1\\ 0 & 1 & 0 & 2\\ 0 & 0 & 1 & 3\end{array}\right]$$

This is **reduced row echelon form**, `rref`. Its last column *is* the solution — the back substitution has been folded into the elimination.

**It costs more than it looks like it saves**, which is why nobody computes it to solve a single system: clearing upwards is roughly another $n^3/3$ operations, doubling the work, to avoid a back substitution that costs only $n^2$. L03 has the arithmetic.

**Where it earns its place is when the right-hand side is a whole matrix**, and that is Week 1's L05: run elimination on $[\,A \mid I\,]$ all the way to reduced form and the right half becomes $A^{-1}$. That algorithm is called **Gauss–Jordan**, and it is this section applied $n$ times at once.

---

## 8. Doing It By Hand Without Making Mistakes

You will do a great deal of this on paper, in this course and on three exams. Elimination is not conceptually hard and it is **extremely easy to get wrong**, so adopt the discipline now:

1. **Write the multiplier down** next to each row operation — $R_3 \leftarrow R_3 - 3R_2$, not just a new row of numbers. Half of all errors are a multiplier used with the wrong sign, and you cannot find one you did not write down.
2. **Do one column completely, then the next.** Interleaving is where rows get touched twice.
3. **Never touch a finished row.** Once row $k$ has served as a pivot row, it is frozen.
4. **Check the answer by substituting into the original system** — not into your echelon form, which shares any error you made. It costs thirty seconds and catches everything.
5. **Prefer a row swap to an ugly fraction.** Swapping is free and legal; $\ell = \tfrac{17}{23}$ is neither.

> **Fractions are the arithmetic, not a mistake.** A system of integers routinely has a fractional
> answer, and pivots after the first are usually fractions. If you find yourself rounding $\tfrac73$
> to $2.33$ to keep the page tidy, stop: you have left exact arithmetic for floating point without
> deciding to, and **L03 is entirely about what that costs.**

---

## 9. What to Take Away

1. **Triangular systems are solved by back substitution**, bottom-up, one division per row. Everything else is machinery for reaching a triangular system.
2. **Three row operations, all reversible**, and reversibility is exactly why the solution set is preserved. R3 excludes $c = 0$ for that reason.
3. **The multiplier is always $\dfrac{\text{entry to kill}}{\text{pivot}}$**, and the pivots are the diagonal entries the algorithm produces, not entries you pick.
4. **A zero pivot means one of two things.** A nonzero below it: swap, and continue — nothing is wrong. Nothing below it: the matrix is **singular**, and the algorithm has proved it.
5. **Elimination classifies as well as solves.** Count pivots for the matrix; read the last rows for whether *this* $b$ is reachable.
6. **Keep the multipliers.** They are Week 1's $L$, and throwing them away is throwing away the factorisation.

---

## Exercises

*(Not assessed. Do them with paper, not `elimination.py` — the script is for checking.)*

1. Eliminate $\;\begin{bmatrix}1 & 3\\ 2 & 7\end{bmatrix}$ and $\;\begin{bmatrix}1 & 3\\ 2 & 6\end{bmatrix}$. One is singular. Which, and at exactly which step did elimination find out?
2. Solve $\;x_1 + x_2 + x_3 = 2,\; 2x_1 - x_2 + x_3 = 2,\; x_1 + 2x_2 - x_3 = 5\;$ by hand. Record the pivots and all three multipliers, then check with `elimination.py`. **One multiplier is a fraction; do not round it.**
3. For which value of $c$ does $\;\begin{bmatrix}1 & 2\\ 3 & c\end{bmatrix}$ fail to have two pivots? What happens to the row picture as $c$ approaches that value?
4. Take §6's Case B matrix with $b = (6,2,8)$ and find all solutions. Write your answer as *(a particular solution) + t · (something)*, and say what the "something" satisfies.
5. Elimination on a $3\times3$ needs three multipliers. How many for $4 \times 4$? For $n \times n$? Give a formula, and keep it for L03.
6. Show that swapping two rows can be achieved by a sequence of R1 and R3 operations, using no swap. *(Hint: three additions and a sign. This is why some textbooks list only two elementary operations.)*

---

*MATH 241 · Week 0 · L02 · © CSE Department*
