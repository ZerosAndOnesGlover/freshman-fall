# MATH 241 · Problem Set 5
## Determinants

---

**Released:** Week 5, Wednesday · **Due:** Week 6, **Friday 17:00**
**Total: 100 points** · Submit one PDF, `PS5_{LastName}_{StudentID}.pdf`

> **Exact arithmetic throughout.**
>
> **Say which method you used and why.** Several questions can be done by elimination or by
> cofactors, and part of the assessment is choosing well.
>
> **Week 6 is a heavy week.** Midterm 1 is Wednesday (Weeks 0–5), Recitation 5 is Thursday, and this
> paper is due Friday. **Do not leave it until after the exam** — most of it is Week 5 material you
> will be revising anyway.

---

### Q1: The Properties (18 points)

**(a) [8]** $A$ is $4\times4$ with $\det A = 3$. Compute, stating which property you used each time:

1. $\det(2A)$
2. $\det(A^\mathsf{T})$
3. $\det(A^{-1})$
4. $\det(A^3)$
5. $\det(-A)$
6. $\det(M^{-1}AM)$ for any invertible $M$

**(b) [4]** Prove from L16's P1–P3 that a matrix with two equal rows has determinant $0$. Then prove that adding a multiple of one row to another leaves the determinant unchanged. **The second proof uses the first.**

**(c) [3]** Give a $2\times2$ counterexample to $\det(A+B) = \det A + \det B$, and state precisely what P3 does say.

**(d) [3]** Without computing anything, explain why

$$\det\begin{bmatrix}1&2&3&4\\ 2&4&6&8\\ 5&1&7&2\\ 0&3&1&9\end{bmatrix} = 0.$$

---

### Q2: Computing Them (22 points)

**(a) [8]** Compute $\det P$ **by elimination**, showing the pivots and counting any row exchanges:

$$P = \begin{bmatrix}2&1&0&1\\ 1&3&1&0\\ 0&1&2&1\\ 1&0&1&3\end{bmatrix}$$

**(b) [6]** Compute the same determinant by **cofactor expansion**. **They must agree.** Which was less work, and by roughly how much?

**(c) [4]** Compute

$$\det\begin{bmatrix}3&0&0&2\\ 0&5&1&0\\ 0&2&4&0\\ 1&0&0&4\end{bmatrix}$$

**by choosing your row or column deliberately.** State which you chose and why before you start.

**(d) [4]** Week 1's L02 eliminated $\begin{bmatrix}2&1&-1\\ 4&5&0\\ -2&8&11\end{bmatrix}$ and found pivots $2, 3, 4$. **Write down its determinant without doing any work**, and say why you are entitled to.

---

### Q3: Cofactors, the Adjugate, and Cramer (20 points)

**(a) [8]** For

$$C = \begin{bmatrix}1&2&3\\ 0&1&4\\ 5&6&0\end{bmatrix}$$

compute $\det C$ and the full adjugate $\operatorname{adj}C$, and verify $C\cdot\operatorname{adj}C = (\det C)\,I$.

**Every entry of $C^{-1}$ is an integer.** Say why, referring to $\det C$. *(You proved the general criterion in PS 3 Q3(a).)*

**(b) [6]** Solve, by **Cramer's rule**, showing all four determinants:

$$\begin{aligned}
2x_1 - x_2 + 3x_3 &= -3\\
x_1 + 4x_2 - 2x_3 &= 11\\
3x_1 + x_2 + 5x_3 &= 0
\end{aligned}$$

**(c) [6]** Now cost it. For an $n\times n$ system:

- How many determinants does Cramer's rule need?
- If each is computed **by elimination**, what is the total, against a single solve's $n^3/3$?
- If each is computed **by cofactors**, how long does $n = 20$ take at $10^9$ terms per second?

**In two sentences: what is Cramer's rule actually for?**

---

### Q4: Volume (20 points)

**(a) [4]** Find the area of the parallelogram with edges $(3,1)$ and $(1,4)$. Then swap the two edges. **What changed, what did not, and what does the change mean?**

**(b) [4]** Find the volume of the parallelepiped with edges $(1,0,2)$, $(0,3,1)$, $(2,1,0)$.

**(c) [6]** For each, give the determinant and say what it does to area, in one phrase:

1. $\begin{bmatrix}1&5\\0&1\end{bmatrix}$
2. $\begin{bmatrix}0&-1\\1&0\end{bmatrix}$
3. $\begin{bmatrix}2&0\\0&\tfrac12\end{bmatrix}$
4. $\begin{bmatrix}1&2\\2&4\end{bmatrix}$

**One of these is a shear.** Explain, using base and height, why its determinant had to be what it is.

**(d) [6]** Compute the Jacobian determinant of the polar change of variables $x = r\cos\theta$, $y = r\sin\theta$.

**You should get $r$.** State in two sentences why MATH 142's $dA = r\,dr\,d\theta$ is this week's theorem, and why the formula takes the **absolute value** of the Jacobian.

---

### Q5: The Product Rule (20 points)

**(a) [4]** Prove $\det(A^{-1}) = 1/\det A$ from the product rule. **Deduce that a singular matrix has no inverse** — and say which of Week 1's seven characterisations this re-proves.

**(b) [4]** Prove $\det(M^{-1}AM) = \det A$. **This is the theorem Week 4's L15 §6 assumed and deferred.**

**(c) [4]** $A$ and $B$ are $3\times3$ with $\det A = 4$ and $\det B = -2$. Find $\det(AB)$, $\det(BA)$, $\det(A^\mathsf{T}B)$, $\det(2AB^{-1})$.

**(d) [4]** Prove that an orthogonal matrix — one with $Q^\mathsf{T}Q = I$ — has $\det Q = \pm1$. **What does each sign mean geometrically?** *(Week 3's $P^{-1} = P^\mathsf{T}$ gave you the first examples; Week 8 is these matrices in full.)*

**(e) [4]** **True or false, with a reason:** $\det A = \det B$ implies $A$ and $B$ are similar. *(PS 4 Q5(d) has a counterexample ready.)*

> **And the standing warning, one last time.** A colleague tests a $1000\times1000$ matrix for
> invertibility with `if det(A) != 0:`. Every entry is around $0.1$ and the matrix is perfectly well
> conditioned. **Estimate the determinant, say what a `double` does with it, and state what should
> have been computed instead.** *(4 of the marks above are for this; Week 0's L03 §7.)*

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | The properties | 18 |
| 2 | Computing them | 22 |
| 3 | Cofactors, adjugate, Cramer | 20 |
| 4 | Volume | 20 |
| 5 | The product rule | 20 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*MATH 241 · Week 5 · PS 5 · © CSE Department*
