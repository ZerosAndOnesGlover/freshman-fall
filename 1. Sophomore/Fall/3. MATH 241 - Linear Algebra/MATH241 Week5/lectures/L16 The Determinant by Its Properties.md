# MATH 241 · Linear Algebra
## Week 5 · Lecture 1 of 3 · **Monday**
### The Determinant, by Its Properties

*“Less depends upon the choice of words than upon this, that their introduction shall be justified by pregnant theorems.”* — Carl Friedrich Gauss, abstract of *Disquisitiones generales circa superficies curvas* (1827)

---

**Reading:** Strang §5.1 · **Previous:** Week 4's L15, change of basis · **Next:** L17, cofactors and what they cost

**Coursework:** 📊 **Quiz 5** today · 📝 **PS 5** released Wed this week, due Fri of Week 6 17:00 · 💬 **Recitation 4** Thu this week 15:00–15:50 · 📝 **PS 4** due Fri this week 17:00

> **Quiz 5 is the first ten minutes of this lecture** and covers Week 4.
>
> **CS 201's Midterm 1 is this evening**, 18:00–19:15, VNC 100, covering its Weeks 0–4.
> **MATH 241's Midterm 1 is the Wednesday of Week 6** and covers **Weeks 0–5** — so this week's
> material is on it, and this is the last teaching week before it.

---

## 1. One Number

The determinant assigns a single number $\det A$ to every **square** matrix. That is a lot of compression — nine numbers to one, for a $3\times3$ — so most of what a matrix knows must be thrown away. **The question worth asking first is what survives.**

Three answers, and this week proves all three:

- **$\det A = 0$ exactly when $A$ is singular.** One number, and it settles invertibility.
- **$\lvert\det A\rvert$ is the factor by which $A$ scales volume.** L18.
- **$\det$ is unchanged by a change of basis**, so it belongs to the transformation rather than to the description. This is the theorem Week 4's L15 §6 used and could not prove.

Week 1's L05 §2 listed seven equivalent characterisations of invertibility and marked the seventh — $\det A \ne 0$ — as **the one to distrust as a test**. That warning stands, and L18 §6 renews it. **A perfect theoretical criterion can still be a bad numerical one**, and knowing why is worth as much as the theorem.

---

## 2. Defined by Three Properties, Not by a Formula

Most books hand you a formula and prove the properties. **This course does the reverse**, following Strang, and the reason is that the formula is unreadable and the properties are exactly what you use.

> **The determinant is the unique function of the rows of a square matrix satisfying:**
>
> **P1.** $\det I = 1$.
>
> **P2.** **Exchanging two rows reverses the sign.**
>
> **P3.** **It is linear in each row separately**, the other rows held fixed:
> $$\det\begin{bmatrix}ca + c'a'\\ \text{row}_2\\ \vdots\end{bmatrix} = c\det\begin{bmatrix}a\\ \text{row}_2\\ \vdots\end{bmatrix} + c'\det\begin{bmatrix}a'\\ \text{row}_2\\ \vdots\end{bmatrix}$$

**P3 is the one to read carefully.** *Separately* means one row at a time. It does **not** say $\det(A + B) = \det A + \det B$ — that is false, spectacularly — and it does not say $\det(cA) = c\det A$. Scaling *one* row multiplies the determinant by $c$; scaling **all $n$** rows multiplies it by $c^n$:

$$\det(cA) = c^n \det A$$

*(Measured: $\det A = 24$, scaling one row by 2 gives 48, scaling the whole matrix by 2 gives $2^3 \cdot 24 = 192$.)*

> **That three properties pin down a unique function is a real theorem**, and it is what makes this
> a definition rather than a wish. §3 derives enough consequences to compute $\det$ for any matrix,
> which is most of the uniqueness argument: any function with P1–P3 must produce those values.

---

## 3. Everything Else Follows

**Each of these is a consequence, not an extra assumption.** They are also the working rules.

**(a) Two equal rows $\Rightarrow \det = 0$.** Swap them: by P2 the determinant becomes $-d$, and the matrix is unchanged, so $d = -d$, so $d = 0$. ✓ *(measured: 0)*

**(b) A zero row $\Rightarrow \det = 0$.** By P3 with $c = 0$.

**(c) Adding a multiple of one row to another does not change $\det$.** By P3, the new determinant splits as $\det(\text{original}) + c\det(\text{matrix with a repeated row})$, and the second term is $0$ by (a).

> **(c) is the load-bearing one.** It says **elimination's main operation leaves the determinant
> alone**, which is what makes §4's algorithm possible — and it is why P2's sign is the only
> bookkeeping needed. *(Measured: adding $5\times$row 1 to row 2 leaves 24 at 24.)*

**(d) A triangular matrix's determinant is the product of its diagonal.** Eliminate the off-diagonal entries using (c), which changes nothing, reaching a diagonal matrix; then apply P3 once per row to pull out each diagonal entry, leaving $\det I = 1$.

**(e) $\det A = 0$ if the rows are dependent.** A dependency lets you produce a zero row using (c), then apply (b). **Combined with §5, this is Week 3's independence criterion in one number.**

---

## 4. How to Actually Compute It

Put (c), P2 and (d) together and the algorithm writes itself — **and it is Week 0's algorithm, unchanged:**

> **Eliminate. The determinant is the product of the pivots, times $-1$ once per row exchange.**

$$\boxed{\;\det A = (-1)^{(\text{number of exchanges})} \times p_1p_2\cdots p_n\;}$$

**Cost: $n^3/3$** — the elimination you were doing anyway, plus $n$ multiplications. L17 compares this with the alternative.

### Week 1's matrix, a fourth time

$$A = \begin{bmatrix}2&1&-1\\ 4&5&0\\ -2&8&11\end{bmatrix}$$

Week 1's L02 §4 eliminated this and found **pivots $2$, $3$, $4$**, with no row exchanges. So

$$\det A = 2 \times 3 \times 4 = \boxed{24}$$

**You computed this in Week 1 and did not know it.** The pivots were on the page; nobody multiplied them together. *(L17 confirms 24 by two other routes.)*

> **This is why the determinant is cheap and the formula is expensive.** Anyone who has run
> elimination has already done the work — the determinant is a by-product, which is exactly how
> LAPACK returns it: factor once with `dgetrf`, then multiply $U$'s diagonal and count the row
> interchanges in `ipiv`.

---

## 5. Singular Exactly When Zero

> **$\det A = 0 \iff A$ is singular.**
>
> *Proof.* Elimination produces $n$ pivots or fewer. **If $n$**, none is zero, so the product is
> nonzero and $A$ is invertible (Week 1's L05 §2, characterisation 1). **If fewer**, some pivot
> position ends up zero, the product is zero — and $A$ is singular. $\square$

**This is characterisation 7 from Week 1's L05 §2**, now proved. The full list, with the week each was established:

| | $A$ is invertible $\iff$ | |
|---|---|---|
| 1 | elimination produces $n$ pivots | Week 0 |
| 2 | $Ax = b$ has exactly one solution for every $b$ | Week 0 |
| 3 | $Ax = 0$ only for $x = 0$ | Week 1 |
| 4 | the columns are independent | Week 3 |
| 5 | the columns span $\mathbb{R}^n$ | Week 3 |
| 6 | $\operatorname{rank} A = n$ | Week 3 |
| 7 | **$\det A \ne 0$** | **this lecture** |

**Seven statements, one theorem.** And it is worth noticing that number 7 is the only one that is a *number* rather than a structural fact — which is what makes it convenient in a proof and unreliable in a computation.

---

## 6. Two Warnings

**$\det(A + B) \ne \det A + \det B$.** Take $A = I$ and $B = -I$ in $2\times2$: the left side is $\det 0 = 0$ and the right is $1 + 1 = 2$. **P3 is linearity in one row at a time and nothing more.**

**A small determinant does not mean nearly singular.** Week 0's L03 §6 made this point with measurements and it is worth restating now that $\det$ is defined:

$$\det(10^{-4}I_2) = 10^{-8} \quad\text{and the matrix is perfectly conditioned}$$
$$\det\begin{bmatrix}10^6 & 0\\ 0 & 10^{-6}\end{bmatrix} = 1 \quad\text{and its condition number is } 10^{12}$$

**The determinant is not scale-invariant** — $\det(cA) = c^n\det A$ — so it changes when you switch from metres to millimetres, and **a quantity that depends on your choice of units cannot be measuring how hard the problem is.** $\operatorname{cond}(A)$ is scale-invariant and is the right diagnostic. *(Week 0's PS 0 Q5(b) built both examples.)*

> **So: $\det A \ne 0$ is a perfect *theoretical* test and a poor *numerical* one.** Use it in proofs
> and in $2\times2$ hand calculations. Never write `if det(A) != 0:` in code.

---

## 7. What to Take Away

1. **The determinant is defined by three properties**: $\det I = 1$, a row swap flips the sign, and linearity **in each row separately**.
2. **Everything else is derived** — equal rows give zero, adding a multiple of a row changes nothing, triangular gives the diagonal product.
3. **Adding a multiple of one row to another leaves $\det$ alone**, which is what lets elimination compute it.
4. **$\det A = \pm$ the product of the pivots**, at $n^3/3$ — the elimination you already ran. Week 1's matrix had pivots $2,3,4$, so $\det = 24$.
5. **$\det A = 0 \iff$ singular**, completing Week 1's list of seven equivalences.
6. **$\det(cA) = c^n\det A$, and $\det(A+B) \ne \det A + \det B$.**
7. **A small determinant is not "nearly singular".** It is not scale-invariant; the condition number is.

---

## Exercises

*(Not assessed. PS 5 is the assessed work.)*

1. Compute $\det\begin{bmatrix}1&2\\3&4\end{bmatrix}$ from the properties alone, without the $ad-bc$ formula. *(Eliminate, then use (d).)*
2. Prove the $2\times2$ formula $\det = ad - bc$ from P1–P3. *(Split the first row as $(a,0) + (0,b)$ and use P3 twice.)*
3. $A$ is $4\times4$ with $\det A = 5$. Find $\det(2A)$, $\det(-A)$, $\det(A^2)$.
4. Without computing, say why $\det\begin{bmatrix}1&2&3\\ 4&5&6\\ 7&8&9\end{bmatrix} = 0$. *(Look at the rows. What combination gives zero?)*
5. Show that if $A$ has a row of zeros then $\det A = 0$, two ways: from P3, and from §5.
6. **True or false:** if $\det A$ is very small then $A$ is close to singular. Give a matrix supporting your answer, and say which quantity does measure closeness to singular.

---

*MATH 241 · Week 5 · L16 · © CSE Department*
