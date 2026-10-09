# MATH 241 · Linear Algebra
## Week 2 · Lecture 2 of 3 · **Tuesday**
### The Column Space, and When $Ax = b$ Is Solvable

*“This conviction of the solvability of every mathematical problem is a powerful incentive to the worker. We hear within us the perpetual call: There is the problem. Seek its solution. You can find it by pure reason, for in mathematics there is no ignorabimus.”* — David Hilbert, "Mathematical Problems" (1900)

---

**Reading:** Strang §3.1 (second half), §3.2 · **Previous:** L07, subspaces · **Next:** L09, the null space

**Coursework:** 📝 **PS 2** released Wed this week, due Fri of Week 3 17:00 · 💬 **Recitation 1** Thu this week 15:00–15:50 · 📝 **PS 1** due Fri this week 17:00 · 📊 **Quiz 3** Mon of Week 3

> **Every number in this lecture is reproduced by `resources/spaces.py`**, which ships with this week.

---

## 1. The Definition You Have Already Been Using

> **The column space $\mathbf{C}(A)$ is the span of the columns of $A$.**

By L07 §7 a span is always a subspace, so $\mathbf{C}(A)$ is a subspace of $\mathbb{R}^m$ — note $\mathbb{R}^m$, the space the *columns* live in, not $\mathbb{R}^n$ where $x$ lives. **For an $m\times n$ matrix those are different spaces**, and keeping them apart is most of the bookkeeping in this week.

Now recall Week 0's L01 §4: $Ax$ is a combination of the columns of $A$, with the entries of $x$ as the amounts. Put the two sentences together:

$$\boxed{\;Ax = b \text{ has a solution} \iff b \in \mathbf{C}(A)\;}$$

**That is the entire content of the lecture, and it is a restatement rather than a theorem.** $\mathbf{C}(A)$ is *defined* as everything reachable by $Ax$; "reachable" and "the system is solvable" are the same words. The work is in learning to *compute* with it, which is §3 onwards.

> **What has changed is the quantifier.** Elimination answers "is *this* $b$ reachable" for one $b$
> at $n^3/3$ operations. $\mathbf{C}(A)$ is the set of all reachable $b$ at once, computed once. You
> met this trade already: **PS 0 Q2(c)** asked you to prove $Bx = (6,2,9)$ insoluble *without
> eliminating*, and the argument — every column satisfies $v_1 + v_2 = v_3$, so every combination
> does — was a description of $\mathbf{C}(B)$. **You have been doing this for two weeks; today it
> gets a name.**

---

## 2. The Matrix for This Week

$$A = \begin{bmatrix}1 & 3 & 3 & 2\\ 2 & 6 & 9 & 7\\ -1 & -3 & 3 & 4\end{bmatrix} \qquad 3\times 4$$

**Four columns, each in $\mathbb{R}^3$.** So $\mathbf{C}(A) \subseteq \mathbb{R}^3$, and $x \in \mathbb{R}^4$.

$$a_1 = \begin{bmatrix}1\\2\\-1\end{bmatrix}\quad a_2 = \begin{bmatrix}3\\6\\-3\end{bmatrix}\quad a_3 = \begin{bmatrix}3\\9\\3\end{bmatrix}\quad a_4 = \begin{bmatrix}2\\7\\4\end{bmatrix}$$

**Look before computing: $a_2 = 3a_1$.** So $a_2$ contributes nothing $a_1$ did not already contribute, and $\mathbf{C}(A) = \operatorname{span}\{a_1, a_3, a_4\}$ — three vectors, at most.

**Four columns in $\mathbb{R}^3$ can never be independent** (four vectors in three dimensions — Week 3 proves it), so there is at least one relation among them and there may be more. **How many, and which, is what elimination is for.**

---

## 3. Elimination Finds the Dependencies

Run Week 0's algorithm all the way to **reduced** row echelon form (Week 0's L02 §7):

$$A \;\longrightarrow\; R = \operatorname{rref}(A) = \begin{bmatrix}1 & 3 & 0 & -1\\ 0 & 0 & 1 & 1\\ 0 & 0 & 0 & 0\end{bmatrix}$$

**Two pivots, in columns 1 and 3. Columns 2 and 4 are free.** The row of zeros says the third equation was a consequence of the first two.

> **The rank.** The number of pivots is called the **rank** of $A$, written $r$. Here $r = 2$. It is
> the single most informative number attached to a matrix, and Week 3 is about why.

### The rule, and it is the one to remember

> **$\mathbf{C}(A)$ is spanned by the columns of $A$ in the pivot positions.**

Here: columns 1 and 3, so

$$\mathbf{C}(A) = \operatorname{span}\left\{\begin{bmatrix}1\\2\\-1\end{bmatrix}, \begin{bmatrix}3\\9\\3\end{bmatrix}\right\}$$

**Two independent vectors in $\mathbb{R}^3$ span a plane through the origin** — one of L07 §4's four permitted shapes.

**And elimination tells you the dependencies explicitly.** Read column 2 of $R$: it is $3$ times column 1 of $R$. **The same relation holds in $A$** — $a_2 = 3a_1$ ✓, which we spotted by eye. Column 4 of $R$ is $(-1)\cdot$column 1 $+\;1\cdot$column 3, so it should be that $a_4 = -a_1 + a_3$:

$$-\begin{bmatrix}1\\2\\-1\end{bmatrix} + \begin{bmatrix}3\\9\\3\end{bmatrix} = \begin{bmatrix}2\\7\\4\end{bmatrix} = a_4 \ ✓$$

**We did not see that one by eye.** That is what elimination bought.

---

## 4. The Trap: Row Operations Change the Column Space

Everything in §3 read the *pattern* of $R$ and then applied it to the columns of **$A$**. That was deliberate.

$$\mathbf{C}(R) \ne \mathbf{C}(A)$$

**Look at them.** $R$'s columns are $(1,0,0)$, $(3,0,0)$, $(0,1,0)$, $(-1,1,0)$ — every one has third entry zero, so

$$\mathbf{C}(R) = \{b : b_3 = 0\},$$

a perfectly good plane, and **not the same plane** as $\mathbf{C}(A)$ (§5 computes that one). Elimination moved it.

> **Why:** a row operation mixes the *entries within each column*, so it moves every column, and the
> space they span moves with them. What it does **not** disturb is which combinations of columns
> give zero — because a row operation is an invertible matrix $E$ acting on the left, and
> $Ax = 0 \iff EAx = 0$. **The relations survive; the space does not.**
>
> **So: read the dependencies off $R$, then write down the columns of $A$.** Taking the pivot
> columns of $R$ instead is the single most common error in this material, and it is not a slip of
> the pen — it produces a plausible answer that is a different subspace.

*(The flip side is L09's: since $Ax = 0 \iff Rx = 0$, the **null space is completely unchanged** by elimination. Two spaces, opposite behaviour, same reason.)*

---

## 5. The Equation of the Column Space

$\mathbf{C}(A)$ is a plane through the origin in $\mathbb{R}^3$, and every such plane is the solutions of one linear equation. Find it: we need $(\alpha,\beta,\gamma)$ with $\alpha b_1 + \beta b_2 + \gamma b_3 = 0$ for both spanning columns.

$$a_1: \quad \alpha + 2\beta - \gamma = 0 \qquad\qquad a_3: \quad 3\alpha + 9\beta + 3\gamma = 0$$

The second gives $\alpha + 3\beta + \gamma = 0$. Subtracting the first: $\beta + 2\gamma = 0$, so $\beta = -2\gamma$; then $\alpha = -3\beta - \gamma = 6\gamma - \gamma = 5\gamma$. Take $\gamma = 1$:

$$\boxed{\;\mathbf{C}(A) = \{\,b \in \mathbb{R}^3 \;:\; 5b_1 - 2b_2 + b_3 = 0\,\}\;}$$

**Check it on all four columns**, not just the two used:

| | $5b_1 - 2b_2 + b_3$ | |
|---|---|---|
| $a_1 = (1,2,-1)$ | $5 - 4 - 1$ | $0$ ✓ |
| $a_2 = (3,6,-3)$ | $15 - 12 - 3$ | $0$ ✓ |
| $a_3 = (3,9,3)$ | $15 - 18 + 3$ | $0$ ✓ |
| $a_4 = (2,7,4)$ | $10 - 14 + 4$ | $0$ ✓ |

**Now $Ax = b$ is solvable for exactly the $b$ satisfying one arithmetic test**, no elimination required:

- $b = (9, 24, 3)$: $45 - 48 + 3 = 0$. **Solvable.** *(L09 finds all its solutions.)*
- $b = (9, 24, 4)$: $45 - 48 + 4 = 1$. **No solution**, and you knew in five seconds.

> **Where that equation comes from.** The vector $(5, -2, 1)$ is perpendicular to every column of
> $A$ — which says $A^\mathsf{T}(5,-2,1) = 0$, so it lives in the null space of $A^\mathsf{T}$. That
> space is called the **left null space**, it is the fourth of Strang's four fundamental subspaces,
> and **it is exactly the list of solvability conditions on $b$.** One row of $\operatorname{rref}$
> was zero; correspondingly there is one condition. Week 3 makes the counting a theorem.

---

## 6. Reading Off the Shape

For an $m\times n$ matrix of rank $r$, two questions have clean answers.

**Is $\mathbf{C}(A)$ all of $\mathbb{R}^m$?** Only when $r = m$ — a pivot in every *row*. Then $Ax = b$ is solvable for **every** $b$, and the matrix is said to have *full row rank*. Here $r = 2 < 3 = m$, so it is not, and the one missing pivot row corresponds to the one condition in §5.

**Is the solution unique when it exists?** Only when $r = n$ — a pivot in every *column*, so no free variables. Here $r = 2 < 4 = n$, so it never is: **two free columns, and L09 shows the solutions form a two-dimensional family.**

| | $r = m$ (full row rank) | $r < m$ |
|---|---|---|
| **$r = n$** (full column rank) | square, invertible: exactly one solution for every $b$ | at most one solution; some $b$ have none |
| **$r < n$** | infinitely many solutions, for every $b$ | infinitely many for some $b$, none for the rest ← **this matrix** |

**Both extremes are familiar.** Top-left is Weeks 0 and 1, $n$ pivots and $A^{-1}$. Bottom-right is the general case, and it is where Week 9's least squares eventually lives: a tall matrix with no exact solution at all, where the right question stops being *"which $b$ are reachable"* and becomes *"what is the nearest reachable one"*.

---

## 7. What to Take Away

1. **$\mathbf{C}(A)$ is the span of the columns**, a subspace of $\mathbb{R}^m$ — where the columns live, not where $x$ lives.
2. **$Ax = b$ is solvable exactly when $b \in \mathbf{C}(A)$.** This is a restatement, not a theorem; the value is that it quantifies over all $b$ at once.
3. **The rank $r$ is the number of pivots**, and the pivot columns **of $A$** span $\mathbf{C}(A)$.
4. **Elimination changes $\mathbf{C}(A)$ and preserves the dependencies.** Read the relations from $R$, then write down the columns of $A$. Here $\mathbf{C}(A)$ is $5b_1 - 2b_2 + b_3 = 0$ and $\mathbf{C}(R)$ is $b_3 = 0$ — different planes.
5. **A plane column space is one linear condition on $b$**, and that condition's coefficients are a vector killed by $A^\mathsf{T}$ — the left null space, and Week 3's fourth subspace.
6. **$r = m$ means every $b$ is reachable; $r = n$ means at most one $x$ reaches it.** Everything about solvability is those two comparisons.

---

## Exercises

*(Not assessed. Do 1–4 by hand; `spaces.py` is for checking.)*

1. For $\begin{bmatrix}1&2\\2&4\\3&6\end{bmatrix}$: find $\mathbf{C}(A)$, describe it geometrically, and give the equation(s) a $b$ must satisfy. How many conditions, and why that many?
2. Give a $3\times3$ matrix whose column space is (a) a line, (b) a plane, (c) all of $\mathbb{R}^3$. What is the rank in each case?
3. For this week's $A$, express $a_4$ as a combination of $a_1$ and $a_3$ two ways: by reading $\operatorname{rref}$, and by solving directly. Confirm they agree.
4. **True or false, with a reason:** if $\mathbf{C}(A) = \mathbf{C}(B)$ then $A$ and $B$ have the same rref. *(Consider $A$ and $\operatorname{rref}(A)$ themselves, and then §4.)*
5. $A$ is $5\times3$ with rank 3. Is $Ax = b$ solvable for every $b \in \mathbb{R}^5$? When it is solvable, is the solution unique? Answer both from §6's table.
6. Show $\mathbf{C}(AB) \subseteq \mathbf{C}(A)$ for any conformable $A, B$. *(You proved this in PS 1 Q1(c) without the vocabulary. One line now.)* Give $A, B$ with strict containment.

---

*MATH 241 · Week 2 · L08 · © CSE Department*
