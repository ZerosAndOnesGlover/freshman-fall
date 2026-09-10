# MATH 241 · Linear Algebra
## Week 3 · Lecture 1 of 3 · **Monday**
### Linear Independence

---

**Reading:** Strang §3.5, first half · **Previous:** Week 2's L09, the null space · **Next:** L11, basis and dimension

> **Quiz 3 is the first ten minutes of this lecture** and covers Week 2.

---

## 1. The Word Week 2 Used Without Defining

Week 2 said "two independent vectors span a plane" and "four columns in $\mathbb{R}^3$ can never be independent", and defined neither. **Both were doing real work** — the first fixed the dimension of $\mathbf{C}(A)$, the second guaranteed a nontrivial null space — so the term needs a definition sharp enough to carry them.

> **Definition.** Vectors $v_1, \dots, v_k$ are **linearly independent** if
>
> $$c_1v_1 + c_2v_2 + \dots + c_kv_k = 0 \qquad\text{forces}\qquad c_1 = c_2 = \dots = c_k = 0.$$
>
> Otherwise they are **dependent**: some combination with *not all* coefficients zero gives $0$.

**Read it as a statement about how many ways there are to make zero.** There is always at least one — take every $c_i = 0$, the *trivial* combination. Independence says **that is the only one.**

> **The two commonest misreadings, both worth naming out loud.**
>
> **"No vector is a multiple of another."** Insufficient. $(1,0)$, $(0,1)$, $(1,1)$ in $\mathbb{R}^2$:
> no one is a multiple of any other, and $(1,0) + (0,1) - (1,1) = 0$. **Dependence is about
> *combinations*, not pairs.**
>
> **"Independent" is a property of the *list*, not of any one vector.** No single vector is
> independent or dependent by itself in a list of three; the list is. Saying "$v_2$ is dependent" is
> meaningless, though "$v_2$ is a combination of the others" is fine and is §3.

---

## 2. It Is a Statement About a Null Space

Stack the vectors as the **columns** of a matrix $X$. Then $c_1v_1 + \dots + c_kv_k$ is exactly $Xc$ — Week 0's L01 §4 — and the definition becomes:

$$\boxed{\;v_1,\dots,v_k \text{ are independent} \iff \mathbf{N}(X) = \{0\}\;}$$

**Which you can already test**, with an algorithm you have had since Week 0:

> **Eliminate. The columns are independent iff every column is a pivot column** — iff there are no
> free columns, iff $\operatorname{rank} = k$.

Nothing new is needed. **Independence is not a new computation; it is a new question answered by the old one.**

### Worked, on two triples

$$v_1 = \begin{bmatrix}1\\2\\3\end{bmatrix},\; v_2 = \begin{bmatrix}2\\5\\7\end{bmatrix},\; v_3 = \begin{bmatrix}1\\3\\5\end{bmatrix} \qquad\text{against}\qquad w_1 = \begin{bmatrix}1\\2\\3\end{bmatrix},\; w_2 = \begin{bmatrix}2\\5\\7\end{bmatrix},\; w_3 = \begin{bmatrix}1\\3\\4\end{bmatrix}$$

**They differ in one entry.**

The $v$'s: elimination gives **rank 3, nullity 0**, so $\mathbf{N} = \{0\}$ and they are **independent**.

The $w$'s: **rank 2, nullity 1**, with $\mathbf{N}$ spanned by $(1,-1,1)$. That vector *is* the dependency, read as coefficients:

$$1\,w_1 - 1\,w_2 + 1\,w_3 = 0, \qquad\text{i.e.}\qquad w_3 = w_2 - w_1$$

Check: $(2,5,7) - (1,2,3) = (1,3,4) = w_3$ ✓

> **This is Week 2's L09 §3 sentence again, and it is now the definition rather than an
> observation.** The null space *is* the complete list of dependencies among the columns. A trivial
> null space means no dependencies, which is independence. **One object, two names, and the second
> is the useful one.**

---

## 3. The Equivalent Form You Will Use in Proofs

> **Claim.** $v_1,\dots,v_k$ (with $k \ge 2$) are dependent **iff** at least one of them is a linear
> combination of the others.
>
> *Proof.* **($\Rightarrow$)** Dependence gives $\sum c_iv_i = 0$ with some $c_j \ne 0$. Divide by
> $c_j$ and rearrange:
> $$v_j = -\frac{1}{c_j}\sum_{i \ne j} c_i v_i.$$
> **($\Leftarrow$)** If $v_j = \sum_{i\ne j} d_i v_i$ then $\sum_{i\ne j} d_iv_i - v_j = 0$, and the
> coefficient on $v_j$ is $-1 \ne 0$. $\square$

**Note what the proof needs: $c_j \ne 0$ for *some* $j$, and then division by that one.** It does **not** say every vector is a combination of the others. In the $w$'s above all three coefficients were nonzero, so any of the three could be expressed by the other two — but in the list $(1,0), (2,0), (0,1)$ the dependency is $2v_1 - v_2 = 0$, and **$v_3$ is not a combination of the others at all.**

> **Which is why the definition is stated with coefficients and not with "one is a combination of
> the rest".** The two are equivalent as stated above, and only the coefficient form makes it
> obvious which vectors are actually implicated.

---

## 4. Two Facts You Get for Free

**Any list containing $0$ is dependent.** If $v_1 = 0$ then $1\cdot v_1 + 0v_2 + \dots + 0v_k = 0$, with a nonzero coefficient. **No zero vector belongs in an independent list**, ever.

**More vectors than dimensions is always dependent.**

> **Theorem.** Any $k$ vectors in $\mathbb{R}^n$ with $k > n$ are dependent.
>
> *Proof.* Stack them as the columns of an $n \times k$ matrix $X$. Elimination produces at most one
> pivot per row, so $r \le n < k$ — **there are more columns than pivots, hence at least one free
> column, hence a nonzero special solution.** $\square$

**Three lines, and it is Week 2's counting argument with a name attached.** It is why four columns in $\mathbb{R}^3$ are never independent (Week 2's L08 §2), and why a wide matrix always has a nontrivial null space (L09 §4).

> **The converse is false and the failure matters.** $k \le n$ does *not* make a list independent —
> $(1,0)$ and $(2,0)$ are two vectors in $\mathbb{R}^2$ and dependent. **Having enough room is
> necessary, not sufficient.** The theorem gives one free "no" and never a "yes"; a "yes" costs an
> elimination.

---

## 5. Independence Where You Have Already Seen It

**The special solutions are independent.** Week 2's L09 §4 argued it: each has a $1$ in its own free position and $0$ in every other free position, so a combination producing $s_2$ needs coefficient $1$ there and $0$ elsewhere. **In the definition's language:** if $\sum c_f s_f = 0$, look at free coordinate $f$ — the only contributor is $c_f \cdot 1$, so $c_f = 0$, for every $f$.

**That is why the special solutions are the right answer to "compute the null space".** They are not merely *some* vectors spanning it; they are an independent spanning set, which L11 calls a **basis**, and it is the smallest possible list.

**The pivot columns of $A$ are independent.** Same argument in the rref: a combination of pivot columns of $R$ that vanishes forces every coefficient to zero, because each pivot column of $R$ has a $1$ in a row where the others have $0$. And relations among columns survive elimination (Week 2's L08 §4), **so the pivot columns of $A$ are independent too** — which is why L08's recipe produced a spanning set of exactly the right size.

---

## 6. Independence in Spaces Without Coordinates

The definition never mentioned $\mathbb{R}^n$, so it applies wherever L07 §3's spaces do.

**In $\mathbb{P}_3$:** are $1, x, x^2$ independent? Suppose $c_1 + c_2x + c_3x^2 = 0$ **as a polynomial** — the zero function, for every $x$. Setting $x = 0$ gives $c_1 = 0$; differentiating and setting $x=0$ gives $c_2 = 0$; then $c_3 = 0$. **Independent.**

**In $C[0,1]$:** are $\sin x$ and $\cos x$ independent? If $c_1\sin x + c_2\cos x = 0$ for all $x$, put $x = 0$ to get $c_2 = 0$, and $x = \pi/2$ to get $c_1 = 0$. **Independent.**

But $\sin^2 x$, $\cos^2 x$ and $1$ are **dependent** — $\sin^2 x + \cos^2 x - 1 = 0$ identically. **A trigonometric identity is a linear dependence**, which is a genuinely useful thing to notice and is the sort of statement ECE 211 will make constantly.

> **Careful: "$= 0$" means the zero *vector*.** In a function space that is the function that is
> zero everywhere, not a value that happens to be zero at one point. $\sin x$ and $x$ agree at
> $x = 0$ and are wildly independent.

---

## 7. What to Take Away

1. **Independent means the only combination giving $0$ is the trivial one.** Not "no vector is a multiple of another" — that is weaker and gets $(1,0),(0,1),(1,1)$ wrong.
2. **It is a property of the list**, not of any individual vector.
3. **Stack them as columns: independent $\iff \mathbf{N}(X) = \{0\} \iff$ every column is a pivot column.** No new algorithm.
4. **The null space is the complete list of dependencies**, and each special solution is one of them written as coefficients.
5. **Dependent $\iff$ one of them is a combination of the others** — but not necessarily *any* one of them.
6. **$k > n$ in $\mathbb{R}^n$ is always dependent**, by counting pivots. The converse is false.
7. **The special solutions are independent, and so are the pivot columns of $A$.** Both facts are already in Week 2 and both are about to be called *bases*.

---

## Exercises

*(Not assessed. PS 3 is the assessed work.)*

1. Are $(1,1,0)$, $(1,0,1)$, $(0,1,1)$ independent in $\mathbb{R}^3$? Now the same three in $\mathbb{R}^3$ **over the field with two elements**, where $1 + 1 = 0$ — still independent? *(CS 341's error-correcting codes live in that field, and this is why they behave differently.)*
2. Show that any list containing two equal vectors is dependent, directly from the definition.
3. For which $t$ are $(1,2,3)$, $(2,5,7)$, $(1,3,t)$ dependent? *(§2 has $t = 4$ and $t = 5$; find the general rule and say what happens geometrically as $t$ passes through the critical value.)*
4. Suppose $v_1, v_2, v_3$ are independent. Prove $v_1$, $v_1 + v_2$, $v_1 + v_2 + v_3$ are independent too.
5. Prove that if $v_1, \dots, v_k$ are independent then so is any sublist. Is the converse true?
6. Are $e^x$, $e^{2x}$ and $e^{3x}$ independent in $C[0,1]$? *(Try three values of $x$, or differentiate twice. Both work, and the second generalises.)*

---

*MATH 241 · Week 3 · L10 · © CSE Department*
