# MATH 241 · Linear Algebra
## Week 8 · Lecture 3 of 3 · **Friday**
### Orthonormal Bases and Gram–Schmidt

*“Beauty is the first test: there is no permanent place in the world for ugly mathematics.”* — G. H. Hardy, *A Mathematician's Apology* (1940)

---

**Reading:** Strang §4.4 · **Previous:** L25, projections · **Next:** Week 9, least squares

**Coursework:** 📝 **PS 7** due today 17:00 · 📊 **Quiz 9** Mon of Week 9 · 📝 **PS 9** released Wed of Week 9, due Fri of Week 10 17:00 · 💬 **Recitation 8** Thu of Week 9 15:00–15:50

> **PS 7 is due at 17:00 today.** PS 8 was released Wednesday and is due the Friday of Week 9.

---

## 1. The Basis Worth Having

L25's formulas were full of $(A^\mathsf{T}A)^{-1}$. **With the right basis, that inverse disappears.**

> **Vectors $q_1,\dots,q_n$ are *orthonormal* if they are pairwise orthogonal and each has length 1:**
> $$q_i^\mathsf{T}q_j = \begin{cases}1 & i = j\\ 0 & i \ne j\end{cases}$$
> **As one matrix equation with the $q_i$ as columns of $Q$:** $\;\boxed{Q^\mathsf{T}Q = I}$

**Orthonormal vectors are automatically independent.** If $\sum c_iq_i = 0$, dot with $q_j$: every term dies except $c_j q_j^\mathsf{T}q_j = c_j$. **So $c_j = 0$, for every $j$** — a two-line proof of independence that needs no elimination at all.

**Three things become free.**

**(a) The inverse.** For square $Q$, $Q^{-1} = Q^\mathsf{T}$. **A transpose instead of an $O(n^3)$ elimination** — this is Week 3's $P^{-1} = P^\mathsf{T}$ for permutations, generalised.

**(b) Coordinates.** To write $b = \sum c_iq_i$, dot with $q_j$:

$$\boxed{\;c_j = q_j^\mathsf{T}b\;}$$

**No system to solve.** In a general basis, finding coordinates means solving $Sc = b$ at $n^3/3$; in an orthonormal basis it is $n$ dot products, **and each coordinate is computed independently of the others.**

**(c) Projections.** With $Q$'s columns an orthonormal basis of $W$:

$$A^\mathsf{T}A = Q^\mathsf{T}Q = I \quad\Longrightarrow\quad P = Q(Q^\mathsf{T}Q)^{-1}Q^\mathsf{T} = \boxed{QQ^\mathsf{T}}$$

**L25's formula with the hard part deleted**, and it expands to a sum of rank-one pieces:

$$Pb = \sum_j (q_j^\mathsf{T}b)\,q_j$$

**"Project onto each direction separately and add."** *(This is the formula behind Fourier series, and Week 12 is exactly it with $q_j$ ranging over sines and cosines.)*

---

## 2. And the Conditioning

$$\lVert Qx\rVert = \lVert x\rVert \quad\Longrightarrow\quad \operatorname{cond}(Q) = 1$$

**The smallest possible.** L24 §5 established this; here is what it is worth.

**Week 7's L22 §4 was a complaint:** near a defective matrix the eigenvector basis $S$ is nearly singular, so $A = S\Lambda S^{-1}$ is numerically worthless even though it exists. **Measured:**

| eigenvectors | $\operatorname{cond}(S)$ |
|---|---:|
| $(1,0)$, $(1,10^{-2})$ | $200$ |
| $(1,0)$, $(1,10^{-4})$ | $2\times10^{4}$ |
| $(1,0)$, $(1,10^{-8})$ | $1.3\times10^{8}$ |

**An orthonormal basis gives $1$ in every row.** Multiplying by $Q$ or $Q^\mathsf{T}$ **cannot amplify an error at all** — it is a rigid motion, and rounding errors pass through unmagnified.

> **This is the design principle of the rest of the course, stated plainly:**
>
> **Week 10:** symmetric matrices have **orthonormal** eigenvectors, so $A = Q\Lambda Q^\mathsf{T}$
> with $\operatorname{cond}(Q) = 1$ — the conditioning problem simply does not arise.
> **Week 11:** the SVD gives orthonormal bases at **both** ends, for **every** matrix.
> **Week 9:** least squares via QR rather than the normal equations, for the same reason.
>
> **Existence was never the issue. Conditioning is**, and orthonormality is the answer.

---

## 3. Gram–Schmidt

**Any basis can be made orthonormal.** The procedure is one idea repeated: **take the next vector, subtract off its projections onto everything already done, and normalise.**

$$w_1 = a_1$$
$$w_2 = a_2 - \frac{a_2^\mathsf{T}w_1}{w_1^\mathsf{T}w_1}w_1$$
$$w_3 = a_3 - \frac{a_3^\mathsf{T}w_1}{w_1^\mathsf{T}w_1}w_1 - \frac{a_3^\mathsf{T}w_2}{w_2^\mathsf{T}w_2}w_2$$

and so on, then $q_i = w_i/\lVert w_i\rVert$.

**Each subtraction is L25 §2's projection onto a line.** The new vector is the old one **with its component along each previous direction removed** — so what remains is orthogonal to all of them, by construction.

### Worked, exactly

Start from $a_1 = (1,1,1)$, $a_2 = (1,2,3)$, $a_3 = (1,4,9)$.

| | | |
|---|---|---|
| $w_1 = a_1$ | | $(1,1,1)$, $\lVert w_1\rVert^2 = 3$ |
| $w_2 = a_2 - 2w_1$ | | $(-1,0,1)$, $\lVert w_2\rVert^2 = 2$ |
| $w_3 = a_3 - \tfrac{14}{3}w_1 - 4w_2$ | | $(\tfrac13,-\tfrac23,\tfrac13)$, $\lVert w_3\rVert^2 = \tfrac23$ |

**All three pairwise dot products are zero** ✓, and clearing fractions:

$$w_1 \sim (1,1,1), \qquad w_2 \sim (-1,0,1), \qquad w_3 \sim (1,-2,1)$$

> **Those are not arbitrary.** The three starting vectors are the values of $1$, $x$ and $x^2$ at
> $x = 1, 2, 3$ — **constant, linear and quadratic, sampled.** Orthogonalising them produces the
> **discrete Legendre vectors**, and the pattern $(1,1,1)$, $(-1,0,1)$, $(1,-2,1)$ is recognisable:
> the average, the slope, and the curvature.
>
> **Week 12's Fourier item is this construction on functions**, with $\int$ in place of the dot
> product — and the orthogonal family is sines and cosines instead. **Gram–Schmidt is where
> orthogonal function families come from.**

---

## 4. $A = QR$

**Gram–Schmidt does not lose information**, and recording what it subtracted gives a factorisation.

Each $a_j$ is a combination of $q_1,\dots,q_j$ — **only the ones up to $j$**, since the later ones did not exist yet. Collecting the coefficients:

$$\boxed{\;A = QR\;}$$

with $Q$ orthonormal and **$R$ upper triangular** — upper precisely because $a_j$ involves no $q_i$ with $i > j$.

**And $R$ is easy to read off:** $R_{ij} = q_i^\mathsf{T}a_j$, with the norms $\lVert w_j\rVert$ on the diagonal.

**Computed for the example above:**

$$Q = \begin{bmatrix}0.577350 & -0.707107 & 0.408248\\ 0.577350 & 0 & -0.816497\\ 0.577350 & 0.707107 & 0.408248\end{bmatrix}, \qquad R = \begin{bmatrix}1.732051 & 3.464102 & 8.082904\\ 0 & 1.414214 & 5.656854\\ 0 & 0 & 0.816497\end{bmatrix}$$

**$\lVert QR - A\rVert = 0$ exactly, and $\lVert Q^\mathsf{T}Q - I\rVert = 6.5\times10^{-15}$.** The diagonal of $R$ is $\sqrt3$, $\sqrt2$, $\sqrt{2/3}$ — **the norms from §3.**

> **This is the fourth factorisation of the course**, and the pattern from Week 4's L15 §7 continues:
>
> | | | Simple means |
> |---|---|---|
> | Week 1 | $A = LU$ | triangular |
> | Week 7 | $A = S\Lambda S^{-1}$ | diagonal, **when it exists** |
> | **Week 8** | **$A = QR$** | **orthonormal $\times$ triangular, always** |
> | Week 11 | $A = U\Sigma V^\mathsf{T}$ | diagonal, always |
>
> **$QR$ exists for every matrix with independent columns** — no hypothesis about eigenvalues, no
> defectiveness to worry about. **Week 9 uses it to solve least squares without ever forming
> $A^\mathsf{T}A$.**

---

## 5. The Catch, and What Is Done About It

**Classical Gram–Schmidt as written above is numerically poor.** When the $a_j$ are nearly dependent, the subtractions cancel catastrophically — **Week 0's L03 §4 again** — and the computed $q_j$ drift out of orthogonality.

**The repair is small and standard.** *Modified* Gram–Schmidt subtracts each projection **as it goes**, updating the working vector immediately rather than computing all the coefficients against the original $a_j$:

```
w = a_j
for i in 1..j-1:
    w = w - (q_i . w) q_i      # note: q_i . w, using the UPDATED w
```

**Mathematically identical, numerically much better** — each subtraction operates on a vector that has already had the earlier components removed, so the coefficients are smaller and the cancellation is milder.

> **In production, neither is used.** LAPACK computes $QR$ by **Householder reflections** — building
> $Q$ as a product of orthogonal reflection matrices, each of which is exactly orthogonal to
> machine precision by construction. **No cancellation is possible**, because nothing is subtracted
> in the vulnerable way.
>
> **Gram–Schmidt is the right thing to understand and the wrong thing to run**, which is the same
> relationship the course has had with Cramer's rule (Week 5), the adjugate formula (Week 5) and the
> characteristic polynomial (Week 6). **A pattern worth noticing by now.**

---

## 6. What to Take Away

1. **Orthonormal $\iff Q^\mathsf{T}Q = I$**, and orthonormal vectors are independent by a two-line argument with no elimination.
2. **Three things become free:** $Q^{-1} = Q^\mathsf{T}$; coordinates are dot products $c_j = q_j^\mathsf{T}b$; and $P = QQ^\mathsf{T}$.
3. **$\operatorname{cond}(Q) = 1$**, so multiplying by $Q$ cannot amplify error. **This is why Weeks 9, 10 and 11 all insist on orthonormal bases** — existence was never the problem.
4. **Gram–Schmidt: subtract the projections onto everything already done, then normalise.** Each step is L25 §2.
5. **Orthogonalising $1, x, x^2$ sampled gives $(1,1,1)$, $(-1,0,1)$, $(1,-2,1)$** — the discrete Legendre vectors, and Week 12's Fourier construction is the same thing on functions.
6. **$A = QR$**, with $R$ upper triangular because $a_j$ uses no later $q_i$. **The fourth factorisation, and it always exists** for independent columns.
7. **Classical Gram–Schmidt is numerically poor**; modified Gram–Schmidt is better and Householder reflections are what LAPACK uses. **Understand the first, run the last.**

---

## Exercises

*(Not assessed. PS 8 is due Friday of Week 9.)*

1. Apply Gram–Schmidt to $(1,0,0)$, $(1,1,0)$, $(1,1,1)$. **Predict the answer before computing.**
2. Apply Gram–Schmidt to $(1,1,0)$, $(2,0,2)$, $(3,3,3)$ and check all three pairwise dot products.
3. Find $Q$ and $R$ for $A = \begin{bmatrix}1&1\\ 1&0\\ 0&1\end{bmatrix}$. Verify $QR = A$ and $Q^\mathsf{T}Q = I$.
4. Show that if $Q$ has orthonormal columns then $\lVert Qx\rVert = \lVert x\rVert$, and deduce $\operatorname{cond}(Q) = 1$ for square $Q$.
5. **Why is $R$ invertible** whenever $A$ has independent columns? **What are its diagonal entries?**
6. Use $A = QR$ to show that the normal equations become $R\hat x = Q^\mathsf{T}b$. *(Substitute and cancel. **This is Week 9's algorithm**, and note what has disappeared.)*
7. Orthogonalise $1$, $x$, $x^2$ on $[-1,1]$ using $\langle f,g\rangle = \int_{-1}^{1}fg\,dx$ in place of the dot product. **You should get $1$, $x$, $x^2 - \tfrac13$** — the Legendre polynomials. *(Week 12.)*

---

*MATH 241 · Week 8 · L26 · © CSE Department*
