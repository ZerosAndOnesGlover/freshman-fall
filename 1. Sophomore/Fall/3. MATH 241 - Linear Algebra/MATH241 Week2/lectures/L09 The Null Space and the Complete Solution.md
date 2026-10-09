# MATH 241 · Linear Algebra
## Week 2 · Lecture 3 of 3 · **Friday**
### The Null Space, and the Complete Solution

*“A mathematical problem should be difficult in order to entice us, yet not completely inaccessible, lest it mock at our efforts. It should be to us a guide post on the mazy paths to hidden truths.”* — David Hilbert, "Mathematical Problems" (1900)

---

**Reading:** Strang §3.2, §3.3 · **Previous:** L08, the column space · **Next:** Week 3, independence and dimension

**Coursework:** 📝 **PS 1** due today 17:00 · 📊 **Quiz 3** Mon of Week 3 · 📝 **PS 3** released Wed of Week 3, due Fri of Week 4 17:00 · 💬 **Recitation 2** Thu of Week 3 15:00–15:50

> **PS 1 is due at 17:00 today.** PS 2 was released Wednesday and is due the Friday of Week 3.

---

## 1. The Second Subspace

$$\mathbf{N}(A) = \{\,x \in \mathbb{R}^n \;:\; Ax = 0\,\}$$

**L07 §5 already proved this is a subspace**, in three lines using nothing but linearity. Note the space it sits in: $\mathbb{R}^n$, where $x$ lives — **not** $\mathbb{R}^m$, where $\mathbf{C}(A)$ lives. For a $3\times4$ matrix the two subspaces are not merely different, they are subspaces of different spaces and cannot be compared.

| | Lives in | Is | Answers |
|---|---|---|---|
| $\mathbf{C}(A)$ | $\mathbb{R}^m$ | span of the columns | **which $b$** have a solution |
| $\mathbf{N}(A)$ | $\mathbb{R}^n$ | solutions of $Ax = 0$ | **how many** solutions each reachable $b$ has |

**Together they answer Week 0's question completely**, and §6 is where the two halves are joined.

---

## 2. Computing It

$\mathbf{N}(A)$ is an infinite set, so "computing" it means producing a **finite list of vectors whose combinations are exactly it**. Elimination does that, and this time with no caveat:

> **$Ax = 0 \iff Rx = 0$, where $R = \operatorname{rref}(A)$.**
>
> Every row operation is left multiplication by an invertible $E$ (Week 1's L06 §3), and
> $Ax = 0 \Rightarrow EAx = 0$, while $EAx = 0 \Rightarrow Ax = E^{-1}0 = 0$. **Both directions, so
> the solution sets are equal.**

**$\mathbf{N}(A) = \mathbf{N}(R)$, exactly.** Contrast L08 §4, where $\mathbf{C}(A) \ne \mathbf{C}(R)$ — same operations, opposite effect, and for the same reason: elimination preserves the *relations among columns*, which is what the null space records, and moves the columns themselves, which is what the column space records.

*(The zero right-hand side never changes, so there is no need to augment. $A$ alone suffices.)*

### The recipe

1. Reduce $A$ to $R = \operatorname{rref}(A)$. **Pivot columns** get pivots; the rest are **free**.
2. **One special solution per free column.** For free column $j$: set $x_j = 1$, set every *other* free variable to $0$, and solve for the pivot variables.
3. $\mathbf{N}(A)$ is all combinations of the special solutions.

**Step 2 is where the free variables earn their name:** nothing constrains them, so you choose, and choosing the standard basis pattern — one of them $1$, the rest $0$ — produces the cleanest list.

---

## 3. Worked, on This Week's Matrix

$$A = \begin{bmatrix}1 & 3 & 3 & 2\\ 2 & 6 & 9 & 7\\ -1 & -3 & 3 & 4\end{bmatrix}, \qquad R = \begin{bmatrix}1 & 3 & 0 & -1\\ 0 & 0 & 1 & 1\\ 0 & 0 & 0 & 0\end{bmatrix}$$

Pivots in columns 1 and 3; **free columns 2 and 4**. Written out, $Rx = 0$ is

$$x_1 + 3x_2 \phantom{{}+ x_3} - x_4 = 0, \qquad x_3 + x_4 = 0.$$

**Special solution $s_2$** — set $x_2 = 1$, $x_4 = 0$:

$$x_3 + 0 = 0 \Rightarrow x_3 = 0, \qquad x_1 + 3 - 0 = 0 \Rightarrow x_1 = -3$$

$$s_2 = (-3,\, 1,\, 0,\, 0)$$

**Special solution $s_4$** — set $x_4 = 1$, $x_2 = 0$:

$$x_3 + 1 = 0 \Rightarrow x_3 = -1, \qquad x_1 + 0 - 1 = 0 \Rightarrow x_1 = 1$$

$$s_4 = (1,\, 0,\, -1,\, 1)$$

**Check both against the original $A$, not against $R$:**

$$As_2 = -3a_1 + a_2 = -3(1,2,-1) + (3,6,-3) = (0,0,0)\ ✓$$
$$As_4 = a_1 - a_3 + a_4 = (1,2,-1) - (3,9,3) + (2,7,4) = (0,0,0)\ ✓$$

$$\boxed{\;\mathbf{N}(A) = \{\,t(-3,1,0,0) + u(1,0,-1,1) \;:\; t, u \in \mathbb{R}\,\}\;}$$

**A two-dimensional subspace of $\mathbb{R}^4$** — a plane through the origin, in four dimensions.

> **The special solutions *are* the column dependencies of L08 §3, written as vectors.** $s_2$ says
> $-3a_1 + a_2 = 0$, which is $a_2 = 3a_1$. $s_4$ says $a_1 - a_3 + a_4 = 0$, which is
> $a_4 = a_3 - a_1$. **The null space is the complete list of ways the columns depend on each
> other**, and that is the sentence to carry into Week 3.

---

## 4. Why One Per Free Column, and the Count

Each special solution has a $1$ in its own free position and $0$ in every other free position. **So no special solution is a combination of the others** — any combination producing $s_2$ would need coefficient $1$ on $s_2$ and $0$ on the rest. They are independent, in the sense Week 3 makes precise, and there are exactly as many as there are free columns.

$$\#\text{pivot columns} + \#\text{free columns} = n$$

is just counting: every column is one or the other. Naming the two counts,

$$\boxed{\;\operatorname{rank} + \operatorname{nullity} = n\;}$$

Here $2 + 2 = 4$ ✓. **This is the rank–nullity theorem**, and it has just been proved for anything elimination can be run on — which is everything. Week 3 restates it with dimension defined properly and shows the count does not depend on how you eliminated.

> **Read it as a conservation law.** $n$ is the number of dials on the machine. The rank is how many
> of them do something visible; the nullity is how many you can turn with no effect at all. **A wide
> matrix ($n > m$) always has $r \le m < n$, so it always has free columns and never a trivial null
> space.** More unknowns than equations always means infinitely many solutions or none — which is
> the honest version of a fact you have believed since school.

---

## 5. The Two Extremes

**$\mathbf{N}(A) = \{0\}$** — the *zero* subspace, not the empty set; $x = 0$ always solves $Ax = 0$. This happens exactly when there are no free columns, i.e. $r = n$: **a pivot in every column.** Then $Ax = b$ has at most one solution, and for square $A$ this is Week 1's L05 §2 characterisation 3 of invertibility. **"Full column rank" and "trivial null space" and "the columns are independent" are three names for one condition.**

**$\mathbf{N}(A) = \mathbb{R}^n$** — every $x$ solves $Ax = 0$, so $A = 0$. Uninteresting, and worth stating so that the range of possibilities is closed.

---

## 6. The Complete Solution

Now join the two halves. Suppose $b \in \mathbf{C}(A)$, so at least one solution exists.

> **Theorem.** If $Ax_p = b$, then the set of all solutions of $Ax = b$ is
> $$\{\,x_p + x_n \;:\; x_n \in \mathbf{N}(A)\,\}.$$
>
> *Proof.* **($\supseteq$)** $A(x_p + x_n) = Ax_p + Ax_n = b + 0 = b$.
> **($\subseteq$)** If $Ax = b$, put $x_n = x - x_p$; then $Ax_n = b - b = 0$, so
> $x_n \in \mathbf{N}(A)$ and $x = x_p + x_n$. $\square$

**Both directions matter.** The first says everything of that form is a solution; the second says there is nothing else. **This is the promised structure of Week 0's L01 §5**, which proved two solutions generate a line without saying what the line was made of. It is made of $\mathbf{N}(A)$.

### Worked

Take $b = (9, 24, 3)$. Check it is reachable using L08 §5's test: $5(9) - 2(24) + 3 = 45 - 48 + 3 = 0$ ✓.

Augment and reduce:

$$[\,A \mid b\,] \;\longrightarrow\; \left[\begin{array}{cccc|c}1&3&0&-1&3\\ 0&0&1&1&2\\ 0&0&0&0&0\end{array}\right]$$

**A particular solution: set every free variable to zero.** Then $x_1 = 3$ and $x_3 = 2$:

$$x_p = (3,\, 0,\, 2,\, 0), \qquad Ax_p = 3a_1 + 2a_3 = (3,6,-3) + (6,18,6) = (9,24,3)\ ✓$$

$$\boxed{\;x = \begin{bmatrix}3\\0\\2\\0\end{bmatrix} + t\begin{bmatrix}-3\\1\\0\\0\end{bmatrix} + u\begin{bmatrix}1\\0\\-1\\1\end{bmatrix}\;}$$

**Sanity check with $t = u = 1$:** $(3-3+1,\; 0+1+0,\; 2+0-1,\; 0+0+1) = (1,1,1,1)$ — and indeed $A(1,1,1,1) = a_1+a_2+a_3+a_4 = (9,24,3)$ ✓. **A different particular solution, reached by different $t$ and $u$, describing the same set.**

> **$x_p$ is not unique and the solution *set* is.** Choosing the free variables to be zero is a
> convention that makes the arithmetic easy, not a property of the answer. Two students with
> different $x_p$ have the same solution set, and PS 2 is marked on the set.

### And when $b$ is not reachable

$b = (9,24,4)$: the test gives $45 - 48 + 4 = 1 \ne 0$. Eliminating anyway,

$$\left[\begin{array}{cccc|c}1&3&0&-1&3\\ 0&0&1&1&2\\ 0&0&0&0&\mathbf{1}\end{array}\right]$$

**The last row reads $0 = 1$.** The zero row of $R$ became a contradiction, which is exactly Week 0's L02 §6 Case B — and §5's plane equation predicted it without any of this work.

---

## 7. The Geometry, and the Thing That Is Not a Subspace

$\mathbf{N}(A)$ is a plane **through the origin** in $\mathbb{R}^4$. The solution set of $Ax = b$ is that same plane **slid over** so that it passes through $x_p$.

$$\text{solution set of } Ax = b \;=\; \mathbf{N}(A) \text{ translated by } x_p$$

**It is not a subspace** — L07 §5 said so, because it misses $0$ — and now you can see precisely how it fails: it is the right *shape*, sitting in the wrong *place*. Same dimension, same directions, no origin.

> **This is the pattern behind an enormous amount of mathematics.** Solve the homogeneous problem
> to get the structure; find one particular solution to fix the position. It is how linear ODEs are
> solved in MATH 142 ($y_c + y_p$, and now you know why the two pieces are what they are), and it
> is Week 9's least squares when no exact $x_p$ exists at all.

---

## 8. What to Take Away

1. **$\mathbf{N}(A) \subseteq \mathbb{R}^n$ and $\mathbf{C}(A) \subseteq \mathbb{R}^m$** — different spaces, and for a rectangular $A$ they are not comparable.
2. **$\mathbf{N}(A) = \mathbf{N}(R)$ exactly**, because row operations are invertible. The column space is *not* preserved; the null space is. Same operations, opposite effect.
3. **One special solution per free column**: set that variable to $1$, the other free ones to $0$, solve for the pivots.
4. **The special solutions are the column dependencies as vectors.** $s_2 = (-3,1,0,0)$ *is* the statement $a_2 = 3a_1$.
5. **$\operatorname{rank} + \operatorname{nullity} = n$**, by counting columns. A wide matrix always has free columns, so it never has a trivial null space.
6. **$\mathbf{N}(A) = \{0\} \iff r = n \iff$ at most one solution** — and for square $A$, that is invertibility.
7. **Complete solution $= x_p + \mathbf{N}(A)$**, proved both ways. $x_p$ is not unique; the set is.
8. **The solution set is $\mathbf{N}(A)$ translated** — right shape, wrong place, and not a subspace.

---

## Exercises

*(Not assessed. PS 2 is due Friday of Week 3.)*

1. Find $\mathbf{N}(A)$ for $\begin{bmatrix}1&2&3\\2&4&6\end{bmatrix}$. How many special solutions, and why that many before you compute any?
2. For this week's $A$, find the complete solution of $Ax = (2, 7, 4)$. *(Look at the columns before eliminating — one line of work is available.)*
3. Give a $3\times3$ matrix with $\mathbf{N}(A)$ equal to (a) $\{0\}$, (b) a line, (c) a plane, (d) all of $\mathbb{R}^3$. State the rank in each case and check rank + nullity $= 3$.
4. $A$ is $4\times6$. What is the smallest possible nullity? Can $\mathbf{N}(A) = \{0\}$? Justify from §4 alone.
5. Prove $\mathbf{N}(A) \subseteq \mathbf{N}(BA)$ for any conformable $B$. Give $A$ and $B$ where the containment is strict.
6. Prove $\mathbf{N}(A^\mathsf{T}A) = \mathbf{N}(A)$. *(One direction is exercise 5. For the other, suppose $A^\mathsf{T}Ax = 0$ and consider $x^\mathsf{T}A^\mathsf{T}Ax = \lVert Ax\rVert^2$.) This is the fact that makes Week 9's least squares work at all, and Week 1's L06 §2 is why $A^\mathsf{T}A$ was worth forming.*

---

*MATH 241 · Week 2 · L09 · © CSE Department*
