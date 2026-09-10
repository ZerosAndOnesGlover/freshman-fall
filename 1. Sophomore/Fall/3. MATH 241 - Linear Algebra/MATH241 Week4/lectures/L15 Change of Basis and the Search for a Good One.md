# MATH 241 · Linear Algebra
## Week 4 · Lecture 3 of 3 · **Friday**
### Change of Basis, and the Search for a Good One

---

**Reading:** Strang §8.3 · **Previous:** L14, the matrix of a transformation · **Next:** Week 5, determinants

> **PS 3 is due at 17:00 today.** PS 4 was released Wednesday and is due the Friday of Week 5.

---

## 1. The Matrix Was Never a Property of the Transformation

L14 built a matrix from a transformation **and a choice of basis**. Nobody drew attention to the choice, because it was always the standard one. **It is a choice, and a different one gives a different matrix for the same map.**

$$\text{transformation} \;+\; \text{basis} \;\longrightarrow\; \text{matrix}$$

The transformation is the object; the matrix is a *description* of it. **This lecture is about changing the description, and about the fact that you get to pick — which turns out to be the single most productive freedom in the subject.**

---

## 2. Coordinates Depend on the Basis

Week 3's L11 §1: in a basis $v_1,\dots,v_n$, every $v$ has unique coordinates $[v]_v = (c_1,\dots,c_n)$ with $v = \sum c_iv_i$.

Take $v = (3,1)$ in $\mathbb{R}^2$.

**Standard basis** $e_1, e_2$: coordinates $(3,1)$ — *the entries are the coordinates*, which is exactly why the standard basis feels invisible.

**Basis $u_1 = (1,1)$, $u_2 = (1,-1)$:** solve $c_1(1,1) + c_2(1,-1) = (3,1)$, giving $c_1 + c_2 = 3$ and $c_1 - c_2 = 1$, so $c_1 = 2$, $c_2 = 1$:

$$[v]_u = (2, 1), \qquad\text{since}\qquad 2(1,1) + 1(1,-1) = (3,1)\ ✓$$

**One vector. Two coordinate columns, $(3,1)$ and $(2,1)$.** The arrow on the page did not move.

> **The habit this requires.** From here on, a column of numbers is meaningless until you say which
> basis it is written in. Most of the time it is the standard one and nobody says so — **but Weeks 7,
> 10 and 11 all work in a basis that is not standard**, and confusing $[v]_u$ with $v$ is the
> characteristic error of the second half of this course.

---

## 3. The Change-of-Basis Matrix

Put the **new basis vectors, in old coordinates, as the columns of $M$:**

$$M = \bigl[\;u_1 \;\big|\; u_2 \;\big|\; \cdots \;\big|\; u_n\;\bigr] = \begin{bmatrix}1&1\\1&-1\end{bmatrix}$$

Then, for every $v$:

$$\boxed{\;[v]_{\text{old}} = M\,[v]_{\text{new}}\;} \qquad\text{and}\qquad [v]_{\text{new}} = M^{-1}[v]_{\text{old}}$$

*Why:* $M[v]_{\text{new}}$ is the combination of $M$'s columns with the new coordinates as amounts — Week 0's L01 §4 — and that combination is $v$ itself.

**Check:** $M\begin{bmatrix}2\\1\end{bmatrix} = 2\begin{bmatrix}1\\1\end{bmatrix} + 1\begin{bmatrix}1\\-1\end{bmatrix} = \begin{bmatrix}3\\1\end{bmatrix}$ ✓

> **$M$ is invertible**, because its columns are a basis and so are independent — Week 3's L10 §2.
> **The direction of the arrow is the thing everyone gets backwards:** $M$ takes *new* coordinates
> to *old* ones, even though its columns are the *new* basis. Check it on one vector every single
> time; it costs five seconds and the error is invisible otherwise.

---

## 4. The Same Transformation, in the New Basis

$T$ has matrix $A$ in the old basis. **What is its matrix $B$ in the new one?**

Follow the coordinates round:

$$[v]_{\text{new}} \;\xrightarrow{\;M\;}\; [v]_{\text{old}} \;\xrightarrow{\;A\;}\; [Tv]_{\text{old}} \;\xrightarrow{\;M^{-1}\;}\; [Tv]_{\text{new}}$$

$$\boxed{\;B = M^{-1}AM\;}$$

**Read it right to left, as a sentence:** *translate into old coordinates, apply the map there, translate back.* And it is L14 §3 three times — composition is multiplication.

> **Matrices $A$ and $B$ with $B = M^{-1}AM$ for some invertible $M$ are called **similar**.**
> Similarity is an equivalence relation *(reflexive with $M = I$, symmetric with $M^{-1}$,
> transitive by composing)*, and **its classes are exactly the linear transformations**: two
> matrices are similar precisely when they describe one map in two bases.

---

## 5. Worked: A Reflection Becomes Diagonal

$T$ reflects across the line $y = x$. In the standard basis (L14 §2):

$$A = \begin{bmatrix}0&1\\1&0\end{bmatrix}$$

**Now choose the basis the geometry suggests:** $u_1 = (1,1)$ *along* the mirror line, $u_2 = (1,-1)$ *perpendicular* to it.

**Before computing, predict.** Reflection **fixes** anything on the mirror, so $T(u_1) = u_1$. It **reverses** anything perpendicular, so $T(u_2) = -u_2$. By L14 §1 the matrix in the $u$-basis has columns $[T(u_1)]_u = (1,0)$ and $[T(u_2)]_u = (0,-1)$:

$$B = \begin{bmatrix}1&0\\0&-1\end{bmatrix}$$

**Confirm by the formula.** $M = \begin{bmatrix}1&1\\1&-1\end{bmatrix}$, $M^{-1} = \tfrac12\begin{bmatrix}1&1\\1&-1\end{bmatrix}$:

$$M^{-1}AM = \tfrac12\begin{bmatrix}1&1\\1&-1\end{bmatrix}\begin{bmatrix}0&1\\1&0\end{bmatrix}\begin{bmatrix}1&1\\1&-1\end{bmatrix} = \begin{bmatrix}1&0\\0&-1\end{bmatrix}\ ✓$$

**Same transformation. In one basis it is an off-diagonal matrix that mixes the coordinates; in the other it is two independent scalings.** Nothing about the reflection changed — the description did.

### The projection, same basis

$P$ projects onto $y = x$. Standard matrix $\tfrac12\begin{bmatrix}1&1\\1&1\end{bmatrix}$, and

$$M^{-1}PM = \begin{bmatrix}1&0\\0&0\end{bmatrix}$$

**Keep the component along the line, discard the component across it** — which is what "project" means, said in the only basis where the matrix says it.

*(And $P^2 = P$ holds in both descriptions, as it must: idempotence is a property of the map. Week 8.)*

---

## 6. What Similar Matrices Share

If $B = M^{-1}AM$, the two describe one transformation — so **anything that is genuinely a property of the transformation must agree.**

| | $A$ = reflection | $B$ = its diagonal form | $P$ = projection | $M^{-1}PM$ |
|---|---:|---:|---:|---:|
| **trace** | $0$ | $0$ | $1$ | $1$ |
| **determinant** | $-1$ | $-1$ | $0$ | $0$ |
| **rank** | $2$ | $2$ | $1$ | $1$ |

**Rank is obvious** — it is $\dim(\text{range})$, and the range is a property of the map. **Determinant and trace are not obvious**, and both are theorems:

$$\det(M^{-1}AM) = \det(M^{-1})\det(A)\det(M) = \det(A) \qquad \text{(Week 5)}$$
$$\operatorname{trace}(M^{-1}AM) = \operatorname{trace}(AMM^{-1}) = \operatorname{trace}(A) \qquad \text{(trace}(XY) = \text{trace}(YX))$$

**So the four entries of a $2\times2$ matrix are not four independent facts about a transformation.** Some combinations of them survive a change of basis and some do not. **The ones that survive are the real content; the rest is bookkeeping about a basis somebody chose.**

> **Week 6 adds the eigenvalues to this list**, and they subsume both: the trace is their sum and the
> determinant is their product. **That is why eigenvalues are the answer to "what is a matrix really
> like"** — they are basis-independent, and there are $n$ of them, which is exactly enough to
> determine a diagonal matrix.

---

## 7. The Search for a Good Basis

§5 was not a trick. **It is the program for the rest of the course.**

$$\text{Given } T\text{, find a basis in which its matrix is as simple as possible.}$$

Every remaining topic is an instance, with a different notion of "simple" and a different guarantee about when it can be achieved:

| Week | Factorisation | The basis | Simple means | Exists when |
|---|---|---|---|---|
| **7** | $A = S\Lambda S^{-1}$ | eigenvectors | **diagonal** | $n$ independent eigenvectors |
| **10** | $A = Q\Lambda Q^\mathsf{T}$ | orthonormal eigenvectors | **diagonal**, and $M^{-1} = M^\mathsf{T}$ | $A$ symmetric — **always** |
| **11** | $A = U\Sigma V^\mathsf{T}$ | two bases, one each end | **diagonal** | **always, for every matrix** |

**Read the last column downwards.** Week 7's method is the natural one and it can fail. Week 10 removes the hypothesis by restricting the matrices. **Week 11 removes it entirely by allowing a different basis at the input and the output** — which L14 §1 permitted from the start and which nothing until now has needed.

And $A = LU$ from Week 1 is the same instinct with a cruder notion of simple: *triangular*, reachable by elimination, and not a change of basis at all — which is why it tells you about solving $Ax = b$ and nothing about what $A$ *is*.

> **The one-sentence version of the second half of this course:**
> *the matrix you were handed is an accident of somebody's basis; find the basis that tells the
> truth.*

---

## 8. What to Take Away

1. **A matrix describes a transformation *in a basis*.** The transformation is the object; the matrix is a description, and you may choose it.
2. **The same vector has different coordinates in different bases.** $(3,1)$ and $(2,1)$ were the same arrow.
3. **$M$ has the new basis vectors as columns, and $[v]_{\text{old}} = M[v]_{\text{new}}$** — the direction everyone gets backwards. Check it on one vector.
4. **$B = M^{-1}AM$:** translate in, apply, translate back. Matrices related this way are **similar**, and similarity classes are transformations.
5. **A reflection is $\begin{bmatrix}0&1\\1&0\end{bmatrix}$ or $\begin{bmatrix}1&0\\0&-1\end{bmatrix}$**, depending only on which basis you write it in. The second is better because it was chosen to fit the geometry.
6. **Similar matrices share rank, trace and determinant** — those belong to the transformation. Individual entries do not.
7. **"Find the basis that makes the matrix simple" is Weeks 7, 10 and 11**, with guarantees that improve from *sometimes* to *always*.

---

## Exercises

*(Not assessed. PS 4 is due Friday of Week 5.)*

1. Find the coordinates of $(4,2)$ in the basis $\{(1,1),(1,-1)\}$, then in $\{(2,0),(0,3)\}$. Same vector, three coordinate columns counting the standard one.
2. $A = \begin{bmatrix}2&1\\0&3\end{bmatrix}$ and $M = \begin{bmatrix}1&1\\0&1\end{bmatrix}$. Compute $B = M^{-1}AM$, and check that trace and determinant are unchanged.
3. Reflection across the $x$-axis has matrix $\begin{bmatrix}1&0\\0&-1\end{bmatrix}$ in the standard basis. **Find a basis in which its matrix is $\begin{bmatrix}0&1\\1&0\end{bmatrix}$.** *(§5 backwards.)*
4. Show similarity is an equivalence relation: reflexive, symmetric, transitive. One line each.
5. Prove $\operatorname{trace}(XY) = \operatorname{trace}(YX)$ by writing both as double sums, and deduce that trace is a similarity invariant.
6. Are $I = \begin{bmatrix}1&0\\0&1\end{bmatrix}$ and $\begin{bmatrix}1&1\\0&1\end{bmatrix}$ similar? Trace and determinant agree, so §6's tests are silent. **Settle it anyway** — think about what $M^{-1}IM$ can possibly be. *(Then check that $\begin{bmatrix}1&0\\0&2\end{bmatrix}$ and $\begin{bmatrix}1&1\\0&2\end{bmatrix}$, which also share trace and determinant, **are** similar. Two pairs, same evidence, opposite answers — which is why Week 7 needs more than trace and determinant.)*
7. $T$ is projection onto the line $y = 2x$ in $\mathbb{R}^2$. Find its matrix in a well-chosen basis **first**, then convert to the standard basis with $A = MBM^{-1}$. **Which order was less work?**

---

*MATH 241 · Week 4 · L15 · © CSE Department*
