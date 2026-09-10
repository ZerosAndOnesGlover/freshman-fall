# MATH 241 · Linear Algebra
## Week 5 · Lecture 2 of 3 · **Tuesday**
### Cofactor Expansion, and What It Costs

---

**Reading:** Strang §5.2, §5.3 · **Previous:** L16, the three properties · **Next:** L18, volume and the product rule

> **Every number in this lecture is reproduced by `resources/determinants.py`.**

---

## 1. The Formula the Properties Force

L16 defined $\det$ by three properties and computed it by elimination. **There is also an explicit formula**, and it is worth seeing once — partly because it is where the sign conventions come from, and mostly because its cost is the argument of this lecture.

Split each row into its $n$ pieces using P3 and expand. Almost every resulting term contains a repeated column and dies. What survives is **one term per permutation**:

$$\det A = \sum_{\sigma} \operatorname{sign}(\sigma)\, a_{1\sigma(1)}a_{2\sigma(2)}\cdots a_{n\sigma(n)}$$

**$n!$ terms**, each a product of $n$ entries — one from each row, one from each column — signed by whether the permutation is even or odd.

For $n = 3$ that is $6$ terms and gives the familiar rule:

$$\det\begin{bmatrix}a&b&c\\ d&e&f\\ g&h&i\end{bmatrix} = aei + bfg + cdh - ceg - bdi - afh$$

> **Do not learn the $3\times3$ mnemonic with the diagonals.** It works only for $n = 3$, students
> apply it to $4\times4$ every year, and it is wrong there. **Cofactor expansion (§2) works for
> every $n$**, and elimination is faster than both.

---

## 2. Cofactor Expansion

The $n!$ terms can be **grouped by which entry of the first row they contain**. Factoring gives:

$$\det A = a_{11}C_{11} + a_{12}C_{12} + \dots + a_{1n}C_{1n}$$

where the **cofactor** $C_{ij}$ is

$$C_{ij} = (-1)^{i+j}\,\det M_{ij}, \qquad M_{ij} = A \text{ with row } i \text{ and column } j \text{ deleted}$$

**$M_{ij}$ is the *minor*; $C_{ij}$ is the minor with the sign attached.** The signs alternate in a checkerboard:

$$\begin{bmatrix}+&-&+&-\\ -&+&-&+\\ +&-&+&-\\ -&+&-&+\end{bmatrix}$$

**You may expand along any row or any column** — all $2n$ choices give the same answer. *(That columns work as well as rows is L18 §4's $\det A^\mathsf{T} = \det A$.)*

### Worked

$$A = \begin{bmatrix}2&1&-1\\ 4&5&0\\ -2&8&11\end{bmatrix}$$

Along the first row:

$$\det A = 2\det\begin{bmatrix}5&0\\8&11\end{bmatrix} - 1\det\begin{bmatrix}4&0\\-2&11\end{bmatrix} + (-1)\det\begin{bmatrix}4&5\\-2&8\end{bmatrix}$$

$$= 2(55 - 0) - 1(44 - 0) - 1(32 + 10) = 110 - 44 - 42 = \boxed{24}$$

**Which agrees with L16 §4's product of pivots, $2\times3\times4 = 24$**, and with the $n!$ formula. *(All three are computed in the script.)*

> **Choose the row or column with the most zeros.** Each zero entry kills a whole minor. Expanding
> a $4\times4$ along a row with three zeros costs one $3\times3$ instead of four — and this is the
> one circumstance in which cofactors beat elimination by hand.

---

## 3. What the Formula Costs

The $n!$ formula has $n!$ terms of $n$ factors each. **Cofactor expansion is the same count, rearranged.** Against elimination's $n^3/3$:

| $n$ | $n!$ terms | $n^3/3$ operations | Ratio |
|---:|---:|---:|---:|
| 5 | $120$ | $42$ | $2.9$ |
| 10 | $3.63\times10^{6}$ | $333$ | $1.1\times10^{4}$ |
| 15 | $1.31\times10^{12}$ | $1{,}125$ | $1.2\times10^{9}$ |
| 20 | $2.43\times10^{18}$ | $2{,}667$ | $\mathbf{9.1\times10^{14}}$ |
| 25 | $1.55\times10^{25}$ | $5{,}208$ | $3.0\times10^{21}$ |

**At a billion terms per second, a $20\times20$ determinant by the formula takes 77 years. By elimination it is 2,666 operations** — microseconds.

**Measured**, on a nonsingular $8\times8$ integer matrix, in the same language on the same machine:

```
elimination :  0.00031 s
cofactors   :  0.23542 s   -- 751x slower, and n is only 8
```

**751× at $n = 8$**, where the ratio table predicts a few hundred. **And $n = 8$ is nothing.** The two curves are $n^3$ against $n!$; there is no size at which the gap narrows.

> **This is the same shape of argument as Week 0's L03 §2** — where $n^3/3$ was the *expensive*
> thing, against back substitution's $n^2$. Here $n^3/3$ is the cheap thing. **The lesson is that
> "expensive" is only ever relative to the alternative**, and the alternative here is factorial.

---

## 4. The Inverse Formula, and Cramer's Rule

Cofactors give closed forms for two things you already know how to compute. **Both are beautiful and neither is a method.**

**The adjugate.** Let $\operatorname{adj}A$ be the transpose of the matrix of cofactors, $(\operatorname{adj}A)_{ij} = C_{ji}$. Then

$$A^{-1} = \frac{1}{\det A}\operatorname{adj}A$$

**Week 1's L05 §3 quoted this and deferred it.** For $2\times2$ it is the formula you memorised:

$$\begin{bmatrix}a&b\\c&d\end{bmatrix}^{-1} = \frac{1}{ad-bc}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}$$

**Cramer's rule.** For $Ax = b$ with $A$ invertible,

$$x_j = \frac{\det A_j}{\det A}, \qquad A_j = A \text{ with column } j \text{ replaced by } b$$

**A closed form for each unknown separately**, which is genuinely remarkable — you can compute $x_3$ without ever finding $x_1$.

### And now the arithmetic

**Cramer's rule needs $n+1$ determinants of size $n$.** Even computing each by elimination that is $(n+1)\cdot n^3/3$ against a single solve's $n^3/3$ — **a factor of $n+1$ for no benefit.** Computed by cofactors, as the formula invites, it is $(n+1)\cdot n!$:

- $n = 20$: **77 years per determinant, times 21.**
- The adjugate needs $n^2$ minors of size $n-1$: **$400$ determinants of size $19$** for a $20\times20$ inverse, against Gauss–Jordan's $2n^3 = 16{,}000$ operations.

> **Week 0's L03 §2 killed Cramer's rule before you met it**, and here is the follow-through. **It is
> a theoretical instrument.** Its value is that it exhibits each $x_j$ as a *ratio of polynomials in
> the entries of $A$ and $b$* — which proves that solutions depend smoothly on the data, and which
> matters in proofs and in symbolic computation. **It has never been the right way to get a number.**

---

## 5. When Cofactors Are the Right Tool

Not never. Four cases:

| Case | Why |
|---|---|
| **$2\times2$ and $3\times3$ by hand** | The constants win. $ad-bc$ is faster than eliminating |
| **A row or column with many zeros** | Each zero deletes a minor — §2's note |
| **Symbolic entries** | Elimination divides by pivots, producing rational functions that explode. **Cofactors only ever multiply and add**, so they stay polynomial |
| **Proofs** | The adjugate formula shows $A^{-1}$'s entries are polynomials in $A$'s, divided by $\det A$. **PS 3 Q3(a) used exactly this** to characterise integer matrices with integer inverses |

**The third is the one worth remembering.** Ask for $\det\begin{bmatrix}1-\lambda & 2\\ 3 & 4-\lambda\end{bmatrix}$ and elimination would divide by $1-\lambda$, requiring a case split on whether that is zero. **Cofactors give $(1-\lambda)(4-\lambda) - 6$ with no cases at all.**

> **And that is exactly what Week 6 does.** The characteristic polynomial is $\det(A - \lambda I)$,
> computed symbolically, for every eigenvalue problem you will ever solve by hand. **Cofactors are
> the tool for it**, and this is the reason they are worth a lecture despite §3.

---

## 6. What to Take Away

1. **The big formula has $n!$ signed terms**, one per permutation — one entry from each row and each column.
2. **Cofactor expansion groups those terms**: $\det A = \sum_j a_{ij}C_{ij}$, with $C_{ij} = (-1)^{i+j}\det M_{ij}$. Any row or column works; **pick the one with the most zeros.**
3. **Never use the $3\times3$ diagonal mnemonic for $n > 3$.** It is not a general rule.
4. **The cost is $n!$ against elimination's $n^3/3$** — a factor of $9\times10^{14}$ at $n = 20$, and **measured at 751× for $n = 8$.**
5. **The adjugate formula and Cramer's rule are exact, closed-form and unusable.** Cramer's needs $n+1$ determinants to do one solve's work.
6. **Cofactors win for small $n$, for sparse rows, and — above all — for symbolic entries**, which is why Week 6 needs them.

---

## Exercises

*(Not assessed.)*

1. Compute $\det\begin{bmatrix}1&2&3\\ 0&4&5\\ 0&0&6\end{bmatrix}$ by cofactors along the **first column**, and check against L16 §3(d).
2. Compute the determinant of $\begin{bmatrix}2&0&0&1\\ 0&3&0&0\\ 1&0&4&0\\ 0&0&0&5\end{bmatrix}$. **Choose your row or column deliberately** and say why.
3. Write out $\det(A - \lambda I)$ for $A = \begin{bmatrix}3&1\\ 1&3\end{bmatrix}$ as a polynomial in $\lambda$, and find its roots. *(Compare with Week 4's PS 4 Q4 — you have met those two numbers before.)*
4. Solve $\;2x + y = 5,\ x + 3y = 10\;$ by Cramer's rule, then by elimination. **Time yourself on both.**
5. For a $10\times10$ matrix, how many multiplications does the $n!$ formula need? At $10^9$ per second, how long? Compare with $n^3/3$.
6. Show $\det(\operatorname{adj}A) = (\det A)^{n-1}$ for invertible $A$. *(Take determinants of $A \cdot \operatorname{adj}A = (\det A)I$, using L18's product rule.)*

---

*MATH 241 · Week 5 · L17 · © CSE Department*
