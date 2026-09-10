# MATH 241 · Linear Algebra
## Week 7 · Lecture 1 of 3 · **Monday**
### Diagonalization

---

**Reading:** Strang §6.2 · **Previous:** Week 6's L20, the characteristic polynomial · **Next:** L22, when it fails

> **Quiz 7 is the first ten minutes of this lecture** and covers Week 6. **Back to Monday** — last
> week's Tuesday quiz was the Fall Break exception.
>
> **Midterm 1 papers are returned this week.**

---

## 1. The Promise Being Kept

Week 4's L15 §7 laid out a programme:

$$\text{Given } T\text{, find a basis in which its matrix is as simple as possible.}$$

and tabulated three answers, in Weeks 7, 10 and 11, with hypotheses weakening from *sometimes* to *always*. **This is the first row.**

> **Theorem.** If $A$ ($n \times n$) has $n$ **linearly independent** eigenvectors $s_1,\dots,s_n$
> with eigenvalues $\lambda_1,\dots,\lambda_n$, then
>
> $$\boxed{\;A = S\Lambda S^{-1}\;}$$
>
> where $S$ has the eigenvectors as its **columns** and $\Lambda = \operatorname{diag}(\lambda_1,\dots,\lambda_n)$.
>
> Such an $A$ is called **diagonalizable**.

**The proof is one line and you should be able to produce it.** Consider $AS$, column by column — Week 1's L04 reading (ii):

$$AS = \bigl[\,As_1 \mid As_2 \mid \cdots \mid As_n\,\bigr] = \bigl[\,\lambda_1s_1 \mid \lambda_2s_2 \mid \cdots \mid \lambda_ns_n\,\bigr] = S\Lambda$$

*(That last equality is worth checking: $S\Lambda$ scales the $j$-th **column** of $S$ by $\lambda_j$, because $\Lambda$ is diagonal and multiplies on the right. $\Lambda S$ would scale the rows, and is not what we want.)*

**So $AS = S\Lambda$.** And $S$ is invertible **precisely because its columns are independent** — Week 3's L10 §2 — so

$$A = S\Lambda S^{-1}. \qquad \square$$

> **The hypothesis is the whole content.** "$n$ independent eigenvectors" is exactly what makes $S$
> invertible, and it is exactly what Week 6's defective matrices lack. **L22 is that failure.**

---

## 2. It Is a Change of Basis, and You Already Know Which One

$A = S\Lambda S^{-1}$ is $\Lambda = S^{-1}AS$ rearranged — **Week 4's L15 §4 formula, with $M = S$.**

$$\Lambda = S^{-1}AS$$

**So $\Lambda$ is the matrix of the same transformation in the basis of eigenvectors**, and every word of L15 applies unchanged: $S$ takes eigenvector-coordinates to standard ones, $\Lambda$ acts in eigenvector-coordinates, $S^{-1}$ converts back.

**Diagonalisation is not a new technique. It is change of basis with a particular basis chosen**, and the choice is the one L15 §5 made by hand for a reflection and PS 4 Q4 made by hand for $\begin{bmatrix}3&-1\\-1&3\end{bmatrix}$. **Week 6 supplied the general method for finding it.**

> **The direction of $S$ is Week 4's trap again.** $S$ has the eigenvectors in its **columns**, and
> $S$ converts **eigenbasis coordinates to standard coordinates** — the same direction, and the same
> confusion, as L15 §3's $M$. **REC 4 §2(f)'s check still applies**: if you suspect a reversal,
> compute $As_j$ and confirm it is $\lambda_js_j$.

---

## 3. Assembled, on Week 6's Matrix

$$A = \begin{bmatrix}2&-1&1\\ -1&2&-1\\ 1&1&2\end{bmatrix}$$

Week 6's L19 §4 found eigenvalues $1, 2, 3$ with eigenvectors $(-1,0,1)$, $(-1,1,1)$, $(-1,1,0)$. **Three distinct eigenvalues, so by L20 §6 the eigenvectors are independent** — no eigenspace dimensions to check.

**Put the eigenvectors in the columns of $S$, in the same order as $\Lambda$'s diagonal:**

$$S = \begin{bmatrix}-1&-1&-1\\ 0&1&1\\ 1&1&0\end{bmatrix}, \qquad \Lambda = \begin{bmatrix}1&0&0\\ 0&2&0\\ 0&0&3\end{bmatrix}, \qquad S^{-1} = \begin{bmatrix}-1&-1&0\\ 1&1&1\\ -1&0&-1\end{bmatrix}$$

$$S\Lambda S^{-1} = A \ ✓$$

**The order matters and only in the sense that it must be consistent.** Reorder the eigenvalues and you must reorder $S$'s columns to match; any of the $3! = 6$ consistent pairings works and they all give $A$.

> **$S$ and $S^{-1}$ both came out integer here, and that is luck.** $\det S = 1$, which is
> unusual — eigenvectors are typically irrational, since the eigenvalues are roots of a polynomial.
> **Nothing in the theorem promises integrality**, and the script says so where it prints them.

---

## 4. What It Buys: Powers

**This is the payoff, and it was promised in Week 1.** L04 §6 said that if $A = S\Lambda S^{-1}$ then

$$A^k = S\Lambda^kS^{-1}$$

**because every interior $S^{-1}S$ cancels:**

$$A^2 = (S\Lambda S^{-1})(S\Lambda S^{-1}) = S\Lambda(S^{-1}S)\Lambda S^{-1} = S\Lambda^2S^{-1}$$

and by induction for any $k$. **And $\Lambda^k$ is $n$ scalar powers** — $\operatorname{diag}(\lambda_1^k,\dots,\lambda_n^k)$ — costing nothing.

**Measured on the matrix above:**

$$\Lambda^{10} = \operatorname{diag}(1,\ 1024,\ 59049), \qquad A^{10}\text{'s first row} = (58026,\ -1023,\ 58025)$$

**and the two routes agree exactly.**

### The cost

| | $A^{10}$ | $A^{1000}$ |
|---|---|---|
| Naive repeated multiplication | 9 matrix products | 999 |
| Repeated squaring (Week 1's L04 §6) | 4 | 14 |
| **$S\Lambda^kS^{-1}$** | **3 scalar powers** + 2 fixed products | **3 scalar powers** + 2 |

**The diagonal route does not grow with $k$ at all.** Squaring is $O(\log k)$ matrix products; diagonalising is $O(1)$, after a one-off $O(n^3)$ setup. **For large $k$ there is no comparison**, and that is why this factorisation exists.

> **And it is not only powers.** Any function you can apply to a number, you can apply to a
> diagonalisable matrix by applying it to the eigenvalues:
>
> $$e^A = Se^{\Lambda}S^{-1}, \qquad e^{\Lambda} = \operatorname{diag}(e^{\lambda_1},\dots,e^{\lambda_n})$$
>
> **This is how linear differential equations are solved.** $\dot{x} = Ax$ has solution
> $x(t) = e^{At}x(0)$, and the eigenvalues decide whether it grows or decays — which is ECE 211 next
> term, and L23 §5's stability question.

---

## 5. When You Know It Works Without Checking

> **$n$ distinct eigenvalues $\Rightarrow$ diagonalisable.**

Week 6's L20 §6 proved that eigenvectors for distinct eigenvalues are independent, so $n$ distinct eigenvalues give $n$ independent eigenvectors and the hypothesis holds. **This is the common case** — a random matrix has distinct eigenvalues with probability 1 — which is why defective matrices feel exotic.

**The converse fails**, and the failure is worth naming: $I$ has one eigenvalue repeated $n$ times and is diagonal already. **Distinct eigenvalues are sufficient, never necessary.**

### The full criterion

When eigenvalues repeat you must check the eigenspaces:

$$\boxed{\;A \text{ is diagonalisable} \iff \text{for every } \lambda,\ \text{geometric multiplicity} = \text{algebraic multiplicity}\;}$$

Equivalently: **the eigenspace dimensions sum to $n$.** *(One direction is §1: enough independent eigenvectors gives $S$. The other is L22 §2.)*

**Two matrices with the same repeated eigenvalue, from Week 6:**

| | $\lambda$ | algebraic | geometric | |
|---|---|---:|---:|---|
| $3I$ | $3$ | $2$ | $2$ | **diagonalisable** — it *is* diagonal |
| $\begin{bmatrix}3&1\\0&3\end{bmatrix}$ | $3$ | $2$ | $1$ | **no** |

**A repeated eigenvalue is not the problem. A deficient eigenspace is** — Week 6's central distinction, and now it has a consequence.

---

## 6. Reading Similarity Off the Diagonal Form

**Two diagonalisable matrices are similar if and only if they have the same eigenvalues** (with the same multiplicities).

*Why:* if $A = S\Lambda S^{-1}$ and $B = T\Lambda T^{-1}$ with the **same** $\Lambda$, then

$$B = T\Lambda T^{-1} = T(S^{-1}AS)T^{-1} = (TS^{-1})A(TS^{-1})^{-1},$$

so $A \sim B$. Conversely similar matrices share a characteristic polynomial (Week 6's L20 §2), hence eigenvalues. $\square$

> **So $\Lambda$ is a *canonical form* for diagonalisable matrices** — a standard representative of
> each similarity class, and two matrices are similar exactly when they reduce to the same one (up to
> reordering the diagonal).
>
> **This finishes a question that has been open since Week 4.** PS 4 Q5(d) asked whether trace,
> determinant and rank determine similarity; the answer was no, with $I$ and the shear
> $\begin{bmatrix}1&1\\0&1\end{bmatrix}$. **Now: among diagonalisable matrices, the eigenvalues determine similarity
> completely.** The pair that defeated the earlier tests was defeated precisely because one of them
> is not diagonalisable. **L22 gives the canonical form that covers the rest.**

---

## 7. What to Take Away

1. **$A = S\Lambda S^{-1}$ when $A$ has $n$ independent eigenvectors** — eigenvectors in the columns of $S$, eigenvalues down $\Lambda$.
2. **The proof is $AS = S\Lambda$**, read column by column, plus $S$ invertible because its columns are independent.
3. **It is Week 4's change of basis with $M = S$.** Not a new technique — a particular choice of basis, and Week 6 found it.
4. **$A^k = S\Lambda^kS^{-1}$, and $\Lambda^k$ is $n$ scalar powers.** The cost does not grow with $k$, unlike repeated squaring.
5. **Any function of a matrix follows the same way**, including $e^{At}$, which is how linear ODEs are solved.
6. **$n$ distinct eigenvalues is sufficient and not necessary.** The full criterion is geometric $=$ algebraic for every eigenvalue.
7. **$\Lambda$ is a canonical form:** two diagonalisable matrices are similar exactly when their eigenvalues match.

---

## Exercises

*(Not assessed. PS 7 is the assessed work, due Friday of Week 8.)*

1. Diagonalise $\begin{bmatrix}4&1\\ 2&3\end{bmatrix}$: find $S$, $\Lambda$, $S^{-1}$, and verify $S\Lambda S^{-1} = A$. *(Week 6's REC 6 §0 found the eigenvalues.)*
2. Use your answer to compute $A^5$, and check one entry against direct multiplication.
3. $A$ is $3\times3$ with eigenvalues $1, 1, 2$. **What must you check to decide whether $A$ is diagonalisable?** Give one such $A$ that is and one that is not.
4. Show that if $A = S\Lambda S^{-1}$ is invertible then $A^{-1} = S\Lambda^{-1}S^{-1}$, and say what $\Lambda^{-1}$ is. **What does this require of the eigenvalues?**
5. $A$ is diagonalisable with every $\lvert\lambda_i\rvert < 1$. Prove $A^k \to 0$ as $k \to \infty$. *(One line from $A^k = S\Lambda^kS^{-1}$. This is L23 §5.)*
6. Prove that a diagonalisable matrix with $A^2 = A$ has $\Lambda$ containing only $0$s and $1$s, and deduce that **every such matrix is a projection in some basis.** *(Week 8's subject.)*
7. Two matrices have the same characteristic polynomial $(\lambda-2)^3$. **Give one pair that is similar and one that is not.**

---

*MATH 241 · Week 7 · L21 · © CSE Department*
