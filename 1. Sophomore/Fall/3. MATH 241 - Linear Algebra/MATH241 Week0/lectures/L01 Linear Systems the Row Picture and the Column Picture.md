# MATH 241 · Linear Algebra
## Week 0 · Lecture 1 of 3 · **Friday** of Week 0
### Linear Systems: the Row Picture and the Column Picture

---

**Reading:** Strang §1.1–§1.3, §2.1 · **Next:** L02, elimination

> **Week 0's Monday is Labor Day**, so this course's three Week 0 lectures are sat on **Friday,
> Tuesday and Friday**. From Week 1 the pattern is the ordinary Monday / Tuesday / Friday.

---

## 1. What Makes an Equation Linear

$$3x_1 - 7x_2 + \tfrac{1}{2}x_3 = 4$$

is linear. Each unknown appears **to the first power, alone, multiplied by a constant**, and the terms are added. That is the whole rule, and everything ruled out is ruled out for the same reason:

| Not linear | Why |
|---|---|
| $x_1 x_2 = 1$ | two unknowns multiplied together |
| $x_1^2 = 4$ | an unknown to a power other than one |
| $\sin x_1 = 0$ | an unknown inside a function |
| $\|x_1\| = 3$ | same — $\lvert\cdot\rvert$ is a function, and not a linear one |
| $x_1 + x_2 = 1$ **and** $x_1 \ge 0$ | an inequality is not an equation *(this is linear programming, a different course)* |

**Two properties follow, and they are the entire subject.** Write $f(x) = a_1x_1 + \dots + a_nx_n$. Then

$$f(x + y) = f(x) + f(y) \qquad\text{and}\qquad f(cx) = c\,f(x).$$

*Additivity* and *homogeneity*. Every theorem in this course is squeezed out of those two lines. When Week 4 defines a **linear transformation** it will define it by exactly these two properties and then prove that every one of them is a matrix.

> **Why the restriction earns its keep.** Non-linear systems are solved, when they are solved at all,
> by *linearising* them — Newton's method replaces $f(x) = 0$ with a linear system at each step, and
> then solves it with the algorithm in L02. The linear case is not a toy on the way to the general
> case. It is the step inside the general case.

---

## 2. The System We Will Use All Week

$$\begin{aligned}
2x_1 + \phantom{1}x_2 - \phantom{1}x_3 &= \phantom{1}1\\
4x_1 + 5x_2 \phantom{{}- 11x_3} &= 14\\
-2x_1 + 8x_2 + 11x_3 &= 47
\end{aligned}
\qquad\qquad
A = \begin{bmatrix} 2 & 1 & -1\\ 4 & 5 & 0\\ -2 & 8 & 11\end{bmatrix},\quad
b = \begin{bmatrix}1\\14\\47\end{bmatrix}$$

**Three equations, three unknowns, one solution, and it is $x = (1, 2, 3)$.** Check it now, by substitution, before reading on — $2 + 2 - 3 = 1$, $4 + 10 + 0 = 14$, $-2 + 16 + 33 = 47$.

This matrix comes back in L02 (elimination finds $x$ without you guessing it), in L03 (its pivots are $2, 3, 4$ and its determinant is their product, $24$), and in **Week 1's L06**, where the numbers elimination throws away turn out to be a second matrix. Keeping one example across five lectures is deliberate: each lecture adds a fact about the same nine numbers, and by the end you will know more about this matrix than about any other.

---

## 3. The Row Picture: Planes That Meet

Take the equations **one at a time**. Each one is a constraint on $(x_1, x_2, x_3)$, and in three dimensions the set of points satisfying a single linear equation is a **plane**.

- $2x_1 + x_2 - x_3 = 1$ — a plane.
- $4x_1 + 5x_2 = 14$ — also a plane, and note it is a plane in *three* dimensions even though $x_3$ is absent. It is vertical: it contains every $x_3$.
- $-2x_1 + 8x_2 + 11x_3 = 47$ — a plane.

**A solution is a point on all three at once.** Three planes in general position meet in exactly one point, and here that point is $(1,2,3)$.

**Do it in two dimensions first**, because you can actually see it:

$$\begin{aligned} x_1 - 2x_2 &= -1\\ 3x_1 + 2x_2 &= 9\end{aligned}$$

Two lines. Sketch them: the first has slope $\tfrac12$ and passes through $(-1, 0)$; the second has slope $-\tfrac32$ and passes through $(3,0)$. They cross at $(2, \tfrac32)$. Substitute back: $2 - 3 = -1$ ✓ and $6 + 3 = 9$ ✓.

**The row picture is the one everybody arrives with**, because it is how linear equations are taught at school, and it is the one that stops working first. Try to see three planes in your head. Now try nine. The row picture is a *fact* about $n$ dimensions and a *picture* only for $n \le 3$.

---

## 4. The Column Picture: One Vector, Built From Others

Now read the same nine numbers **down the columns instead of across the rows**:

$$x_1\begin{bmatrix}2\\4\\-2\end{bmatrix} + x_2\begin{bmatrix}1\\5\\8\end{bmatrix} + x_3\begin{bmatrix}-1\\0\\11\end{bmatrix} = \begin{bmatrix}1\\14\\47\end{bmatrix}$$

Multiply out the first components: $2x_1 + x_2 - x_3 = 1$. That is equation one. The second components give equation two, the third give equation three. **The two pictures are the same three equations, grouped differently**, and no arithmetic was done to get from one to the other.

But the *question* has changed, and this is the point of the lecture:

> **Row picture:** which points lie on all three planes?
> **Column picture:** **how much of each column do I need to build $b$?**

With $x = (1,2,3)$:

$$1\begin{bmatrix}2\\4\\-2\end{bmatrix} + 2\begin{bmatrix}1\\5\\8\end{bmatrix} + 3\begin{bmatrix}-1\\0\\11\end{bmatrix} = \begin{bmatrix}2+2-3\\4+10+0\\-2+16+33\end{bmatrix} = \begin{bmatrix}1\\14\\47\end{bmatrix}\ ✓$$

**A sum like $x_1 a_1 + x_2 a_2 + x_3 a_3$ is called a *linear combination* of the columns, and it is the single most important construction in the course.** Weeks 2 and 3 are about nothing else: the set of all linear combinations of the columns is the **column space**, and $Ax = b$ has a solution **exactly when $b$ lies in it**. You are three weeks early to that sentence, but you have now seen the object it is about.

### Why this picture is the better one

**It survives dimension.** "Which vectors can I build from these ten thousand?" is a question you can think about in ten thousand dimensions. "Where do these ten thousand hyperplanes intersect?" is not. Nothing in the column picture asks you to visualise anything; it asks you to combine.

**It makes $Ax$ mean something.** From here on, read

$$Ax = x_1 a_1 + x_2 a_2 + \dots + x_n a_n$$

— **$Ax$ is a combination of the columns of $A$, with the entries of $x$ as the amounts.** Not "row $i$ dotted with $x$, for each $i$", which is the same number and the wrong idea. Week 1's L04 shows that four different readings of matrix multiplication all give the same answer, and this one is the reading that will make eigenvectors and the SVD say something rather than compute something.

> **The habit to build this week.** When you see $Ax$, say *"a combination of the columns"* to
> yourself before you say anything else. It takes about a fortnight to become automatic and it pays
> for the rest of the degree.

---

## 5. Three Outcomes, and There Is No Fourth

A linear system has **no solution**, **exactly one**, or **infinitely many**. There is no system of linear equations anywhere with exactly two solutions, or seventeen, and the proof is two lines.

> **Claim.** If $x$ and $y$ both solve $Ax = b$ and $x \ne y$, then so does $x + t(y - x)$, for every
> real $t$.
>
> *Proof.* $A\bigl(x + t(y-x)\bigr) = Ax + t(Ay - Ax) = b + t(b - b) = b$. The only properties used
> were additivity and homogeneity — §1. $\square$

Two distinct solutions therefore generate a whole **line** of them, and a line has infinitely many points. **The finiteness you are used to from quadratics is a non-linear phenomenon**; $x^2 = 4$ has exactly two solutions precisely because squaring is not linear.

### What the three cases look like in both pictures

| | Row picture (planes) | Column picture |
|---|---|---|
| **One solution** | Meet in a single point | $b$ is a combination of the columns, in exactly one way |
| **No solution** | No common point — but they may still meet in *pairs* | $b$ lies outside the span of the columns |
| **Infinitely many** | Meet in a whole line or plane | $b$ is in the span, but the columns are redundant, so many combinations reach it |

### A singular example, in both pictures

$$B = \begin{bmatrix}1 & 2 & 3\\ 2 & -1 & 1\\ 3 & 1 & 4\end{bmatrix}$$

**Row 3 is row 1 plus row 2**: $(1,2,3) + (2,-1,1) = (3,1,4)$. So the third equation says nothing the first two did not already say — *provided the right-hand side agrees*.

- $b = (6, 2, 8)$: consistent, because $6 + 2 = 8$. Infinitely many solutions — the three planes meet in a **line**.
- $b = (6, 2, 9)$: **no solution**, because the first two equations force the left side of the third to be $8$, and it is being asked for $9$. The three planes form a triangular prism: each pair meets in a line, all three meet nowhere.

**Now the column picture of the same matrix.** Column 3 is column 1 plus column 2: $(1,2,3) + (2,-1,1) = (3,1,4)$. The three columns all lie in one plane through the origin, so $Ax$ can only ever reach vectors in that plane. $(6,2,9)$ is not in it, and no amount of cleverness will build it.

> **That both the rows and the columns turned out dependent is not a coincidence, and it is not
> because this $B$ happens to be symmetric either.** It is a theorem — the row rank of a matrix
> equals its column rank, for every matrix — and it is genuinely surprising the first time. **Week 3
> proves it.** File the observation now.

---

## 6. Why This Matters Outside the Lecture Room

Solving $Ax = b$ is not an exercise; it is what the following do, in a loop, at speed:

| Where | What $A$ and $b$ are |
|---|---|
| **Circuit simulation** (SPICE) | Kirchhoff's laws are one linear equation per node; $x$ is the node voltages. A transient analysis solves a system of this shape at every timestep |
| **Structural analysis** | Forces balance at each joint. $A$ is the geometry of the truss, $b$ the loads, $x$ the member forces |
| **Computer graphics** | Inverse kinematics: given a hand position $b$, find the joint angles. Linearised and solved each frame |
| **Linear regression** | Week 9's least squares — the normal equations $A^\mathsf{T}\!A\,\hat{x} = A^\mathsf{T}b$ are a linear system |
| **Interpolation** | Fitting a polynomial through $n$ points is an $n \times n$ system in the coefficients |
| **Google's PageRank** | Week 6's eigenvector, computed as repeated multiplication rather than by elimination — and *why* is a Week 6 question worth arriving with |

In every one of those, **$n$ is not three.** It is $10^4$ for a modest circuit and $10^9$ for the web graph, which is why L03 asks what elimination costs and why the answer decides which of these problems are solved by elimination at all.

---

## 7. Notation, Fixed Now So It Stops Being a Distraction

| Symbol | Means | Note |
|---|---|---|
| $A$ | a matrix | capital, upright bold on the board, plain italic here |
| $a_{ij}$ | the entry in **row $i$, column $j$** | rows first, always. $a_{23} = 0$ above |
| $a_j$ | the $j$-th **column** of $A$, as a vector | this course reads columns by default |
| $x$ | a column vector, $n \times 1$ | **vectors are columns.** A row vector is written $x^\mathsf{T}$ |
| $A$ is $m \times n$ | $m$ rows, $n$ columns | "$m$ by $n$". $Ax$ needs $x$ to have $n$ entries and gives $m$ |
| $[\,A \mid b\,]$ | the **augmented matrix** | $A$ with $b$ stapled on as an extra column — L02 |

**$Ax = b$ is $m$ equations in $n$ unknowns**, and the two numbers are allowed to differ. Weeks 0 and 1 keep $m = n$; Week 2 drops that and things get more interesting, not less.

---

## 8. What to Take Away

1. **Linear means additive and homogeneous**, and every result in this course is those two properties applied somewhere.
2. **The row picture is planes intersecting.** It is correct, it is intuitive, and it does not survive past three dimensions.
3. **The column picture is $b$ built from the columns of $A$**, with $x$ as the amounts. It survives any dimension, and it is the picture to default to.
4. **Read $Ax$ as a combination of columns**, not as a stack of dot products. Same number, better idea.
5. **Three outcomes only** — none, one, or infinitely many — and the proof is that two solutions generate a line of them.
6. **Dependent rows and dependent columns arrive together.** You have seen it once; Week 3 says why it always happens.

---

## Exercises

*(Not assessed. PS 0 is the assessed work; these are ten minutes each with paper.)*

1. Draw the row picture and the column picture for $\;x_1 + x_2 = 3,\; x_1 - x_2 = 1$. Which drawing did you find easier, and which do you think will still be drawable at $n = 4$?
2. Find a $b$ for which $\;x_1 + 2x_2 = b_1,\; 2x_1 + 4x_2 = b_2\;$ has infinitely many solutions, and one for which it has none. Describe both in the column picture in one sentence each.
3. Three planes can fail to have a common point in more than one way. Describe two geometrically different failures, and give a matrix for each.
4. For the matrix $B$ of §5, find *all* solutions of $Bx = (6,2,8)$. (Set $x_3 = t$ and solve for the others. You should get a line — say which line.)
5. In §1's table, $\lvert x_1 \rvert = 3$ is not linear. But it does have exactly two solutions. Reconcile this with §5's claim that no linear system has exactly two.
6. Write down a $3 \times 3$ system whose row picture is three planes meeting in a line, and confirm from the columns that one column is a combination of the other two.

---

*MATH 241 · Week 0 · L01 · © CSE Department*
