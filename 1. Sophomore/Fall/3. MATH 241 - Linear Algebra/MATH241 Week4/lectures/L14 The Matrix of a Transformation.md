# MATH 241 · Linear Algebra
## Week 4 · Lecture 2 of 3 · **Tuesday**
### The Matrix of a Transformation

---

**Reading:** Strang §8.2 · **Previous:** L13, what a linear transformation is · **Next:** L15, change of basis

> **Every number in this lecture is reproduced by `resources/transformations.py`.**

---

## 1. The Construction

L13 §5: a linear map is determined by what it does to a basis. **So write down what it does to a basis.**

> **Given a basis $v_1,\dots,v_n$ of $V$ and a basis $w_1,\dots,w_m$ of $W$, the matrix of $T$ has
> as its $j$-th column the coordinates of $T(v_j)$ in the $w$-basis.**

$$A = \bigl[\;[T(v_1)]_w \;\big|\; [T(v_2)]_w \;\big|\; \cdots \;\big|\; [T(v_n)]_w\;\bigr]$$

**Then $[T(v)]_w = A\,[v]_v$** — the matrix acting on coordinates does what $T$ does to vectors.

*Why it works:* write $v = \sum c_jv_j$. Linearity gives $T(v) = \sum c_jT(v_j)$, and by Week 0's L01 §4, $Ac$ is exactly the combination of $A$'s columns with the $c_j$ as amounts. **The construction and the column reading of $Ax$ are the same idea.**

> **Two bases, and they need not match.** $T$ maps $V \to W$, so the input basis lives in $V$ and the
> output basis in $W$. When $V = W$ people usually use one basis for both — and **usually** is not
> **always**, which is L15's subject.

**In $\mathbb{R}^n$ with the standard basis, coordinates *are* entries**, so the recipe collapses to:

$$\boxed{\;\text{column } j \text{ of } A \;=\; T(e_j)\;}$$

---

## 2. Worked, in $\mathbb{R}^2$

Apply $T$ to $e_1 = (1,0)$ and $e_2 = (0,1)$ and stack the answers as columns.

| $T$ | $T(e_1)$ | $T(e_2)$ | $A$ |
|---|---|---|---|
| reflect across $y = x$ | $(0,1)$ | $(1,0)$ | $\begin{bmatrix}0&1\\1&0\end{bmatrix}$ |
| project onto $y = x$ | $(\tfrac12,\tfrac12)$ | $(\tfrac12,\tfrac12)$ | $\tfrac12\begin{bmatrix}1&1\\1&1\end{bmatrix}$ |
| shear by factor 2 | $(1,0)$ | $(2,1)$ | $\begin{bmatrix}1&2\\0&1\end{bmatrix}$ |
| scale $x$ by 3 | $(3,0)$ | $(0,1)$ | $\begin{bmatrix}3&0\\0&1\end{bmatrix}$ |
| rotate by $90°$ | $(0,1)$ | $(-1,0)$ | $\begin{bmatrix}0&-1\\1&0\end{bmatrix}$ |

**Rotation by a general angle $\theta$:** $e_1 \mapsto (\cos\theta, \sin\theta)$ and $e_2 \mapsto (-\sin\theta, \cos\theta)$, so

$$R_\theta = \begin{bmatrix}\cos\theta & -\sin\theta\\ \sin\theta & \cos\theta\end{bmatrix}$$

**Do not memorise this.** Draw where $e_1$ goes, draw where $e_2$ goes, read off the columns. **The construction is faster than the memory and it never has the sign wrong.**

> **The projection's matrix satisfies $P^2 = P$**, which Week 1's L05 exercise 6 showed forces
> non-invertibility. **Now you can see why geometrically:** projecting a second time changes
> nothing, because everything is already on the line — and a map that collapses a whole direction
> to zero has thrown away information that no inverse could restore. Its kernel is the line
> perpendicular to $y = x$. **Week 8 is projections properly.**

---

## 3. Composition Is Multiplication

> **If $S$ has matrix $A$ and $T$ has matrix $B$ (compatible bases), then $S \circ T$ has matrix
> $AB$.**

*Proof.* $(S\circ T)(v) = S(T(v))$, which in coordinates is $A(Bc) = (AB)c$ by associativity. $\square$

**This closes a loop opened in Week 1.** L04 §1 *derived* the multiplication formula from the requirement $(AB)x = A(Bx)$, on the grounds that $AB$ ought to mean "first $B$, then $A$". **That requirement was this theorem, stated before the vocabulary existed.**

### Measured: rotations add

$$R_{30°}R_{60°} \stackrel{?}{=} R_{90°}$$

```
R(30) R(60) =            R(90) =
    [ 0.000000 -1.000000]    [ 0.000000 -1.000000]
    [ 1.000000  0.000000]    [ 1.000000  0.000000]

largest disagreement: 1.61e-16  -- rounding, not mathematics.
```

**Rotating by $30°$ then $60°$ is rotating by $90°$, and the matrix product knows it.** Multiplying out $R_\alpha R_\beta$ symbolically and comparing with $R_{\alpha+\beta}$ **produces the angle-addition formulas for sine and cosine** — the ones you memorised in school — as a corollary of matrix multiplication. *(Exercise 4.)*

**And these two commute:** $R_{30}R_{60} = R_{60}R_{30}$, to $0.00\times10^{0}$. **Rotations in the plane are unusual in this respect** — Week 1's L04 §3 was emphatic that $AB \ne BA$ in general, and here is a family where it holds, because the order of two turns about the same point does not matter. **In three dimensions it fails**, which is why aircraft attitude is stated as an ordered sequence of rotations and why gimbal lock exists.

---

## 4. Differentiation, as a Matrix

$D : \mathbb{P}_3 \to \mathbb{P}_3$, basis $1, x, x^2, x^3$. **Differentiate each basis vector and read off coordinates:**

$$D(1) = 0 \to (0,0,0,0) \qquad D(x) = 1 \to (1,0,0,0)$$
$$D(x^2) = 2x \to (0,2,0,0) \qquad D(x^3) = 3x^2 \to (0,0,3,0)$$

$$D = \begin{bmatrix}0&1&0&0\\ 0&0&2&0\\ 0&0&0&3\\ 0&0&0&0\end{bmatrix}$$

**Check it against calculus.** $p = 2 - 5x + x^3$ has coordinates $(2,-5,0,1)$, and

$$D\begin{bmatrix}2\\-5\\0\\1\end{bmatrix} = \begin{bmatrix}-5\\0\\3\\0\end{bmatrix} \;\longrightarrow\; -5 + 3x^2 = p'(x) \ ✓$$

**Rank 3, nullity 1, and $3 + 1 = 4$** — L13 §4's kernel and range, now as a matrix computation.

### The property no geometric example has

$$D^2 \text{ has 2 nonzero entries}, \qquad D^3 \text{ has 1}, \qquad \boxed{D^4 = 0}$$

**$D$ is nilpotent.** Differentiate a cubic four times and you get zero — which is obvious about polynomials and startling about a matrix, since $D \ne 0$ and yet a power of it vanishes. *(Week 1's L04 §3 met a $2\times2$ with $P^2 = 0$; this is the same phenomenon at size 4, and here it means something.)*

$D^3$ has a single entry, $6$, in position $(1,4)$: **the third derivative of $x^3$ is $6$.** The matrix is not a metaphor for differentiation. It *is* differentiation, in coordinates.

> **This is the payoff of Week 3's abstraction.** A course about columns of numbers now computes
> derivatives, and it will compute Fourier coefficients in Week 12 by the same move. **The bridge is
> always the same: fix a basis, and an operator becomes a matrix.**

---

## 5. Reading the Transformation Off the Matrix

| Question about $T$ | Question about $A$ | Answer from |
|---|---|---|
| Is $T$ injective? | $\mathbf{N}(A) = \{0\}$? | pivot in every column |
| Is $T$ surjective? | $\mathbf{C}(A) = \mathbb{R}^m$? | pivot in every row |
| Is $T$ invertible? | is $A$ invertible? | both, so square with $n$ pivots |
| What does $T$ destroy? | $\mathbf{N}(A)$ | special solutions |
| What can $T$ produce? | $\mathbf{C}(A)$ | pivot columns of $A$ |

**Weeks 0–3 answered every one of these**, for a matrix. L13 §3 renamed them. **There is no new computation in Week 4 at all** — what is new is knowing which computation the question is.

**Worked, on $D$:** not injective (kernel is the constants, so information is lost — the $+\,C$), not surjective (nothing maps onto a cubic, since differentiating drops the degree), hence not invertible. **"Differentiation has no inverse" is a rank statement**, and the closest thing — integration — is a right inverse only, and only up to a constant.

---

## 6. What to Take Away

1. **Column $j$ of the matrix is $T$ applied to basis vector $j$**, written in the output basis. In $\mathbb{R}^n$ with the standard basis, that is just $T(e_j)$.
2. **Derive the rotation matrix, do not memorise it.** Where does $e_1$ go, where does $e_2$ go.
3. **Composition is matrix multiplication**, and this is the theorem Week 1's L04 §1 was a special case of — multiplication was *defined* to make it true.
4. **Rotations in the plane commute**; almost nothing else does, and in three dimensions they do not either.
5. **$D$ on $\mathbb{P}_3$ is a $4\times4$ matrix with $D^4 = 0$.** Nilpotency is a genuine fact about differentiating bounded-degree polynomials, not an artefact.
6. **Injective / surjective / invertible are null-space and column-space questions**, all answered by Weeks 0–3. Week 4 supplies the translation, not new machinery.

---

## Exercises

*(Not assessed.)*

1. Find the matrix of: reflection across the $y$-axis; rotation by $180°$; projection onto the $x$-axis. Verify each on a vector of your choosing.
2. Compute the matrix of "reflect across $y=x$, **then** rotate by $90°$", two ways: geometrically, and as a product. **Which matrix is on the left?**
3. Show that the shear $\begin{bmatrix}1&2\\0&1\end{bmatrix}$ has determinant 1 and describe what it does to the unit square. *(Week 5 explains why the determinant is the area factor.)*
4. Multiply $R_\alpha R_\beta$ symbolically and compare with $R_{\alpha+\beta}$. **You have just derived the angle-addition formulas.**
5. Write the matrix of $D : \mathbb{P}_2 \to \mathbb{P}_2$ and of the antiderivative $\int_0^x : \mathbb{P}_2 \to \mathbb{P}_3$. Compute both products. **Which one is the identity, and why is the other not?**
6. $T : \mathbb{R}^2\to\mathbb{R}^2$ has $T(1,1) = (2,2)$ and $T(1,-1) = (0,0)$. Find the standard matrix of $T$. *(The given vectors are a basis, but not the standard one — so L14 §1 gives the matrix in **that** basis first. Getting to the standard one is L15.)*

---

*MATH 241 · Week 4 · L14 · © CSE Department*
