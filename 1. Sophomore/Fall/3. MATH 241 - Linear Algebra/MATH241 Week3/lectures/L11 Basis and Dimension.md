# MATH 241 · Linear Algebra
## Week 3 · Lecture 2 of 3 · **Tuesday**
### Basis and Dimension

*“Whoever maintains the contrary must undertake to derive the dimensions of space from the pure laws of thought—a problem which is at once seen to be impossible of solution.”* — Hermann Grassmann, *Die lineale Ausdehnungslehre* (1844), Introduction

---

**Reading:** Strang §3.5, second half · **Previous:** L10, independence · **Next:** L12, the four subspaces

**Coursework:** 📝 **PS 3** released Wed this week, due Fri of Week 4 17:00 · 💬 **Recitation 2** Thu this week 15:00–15:50 · 📝 **PS 2** due Fri this week 17:00 · 📊 **Quiz 4** Mon of Week 4

---

## 1. Two Requirements, Pulling Opposite Ways

To describe a subspace you want a list of vectors that **reaches everything** in it and **wastes nothing**.

- **Spanning** is a lower bound on the list: too few and you cannot reach everything.
- **Independence** is an upper bound: too many and some are redundant.

> **Definition.** A **basis** for a vector space $V$ is a list of vectors that is
> **(i) independent** and **(ii) spans $V$**.

**The two conditions squeeze from opposite sides, and §4 is the theorem that they meet at exactly one number.**

### The reason a basis is worth having

> **Theorem (unique coordinates).** If $v_1,\dots,v_k$ is a basis for $V$, then every $v \in V$ is
> $c_1v_1 + \dots + c_kv_k$ for **exactly one** list of coefficients.
>
> *Proof.* **Existence** is spanning. **Uniqueness:** suppose
> $\sum c_iv_i = v = \sum d_iv_i$. Subtracting, $\sum(c_i - d_i)v_i = 0$, and independence forces
> every $c_i - d_i = 0$. $\square$

**That is the whole point of the word.** A basis turns an abstract vector into a list of numbers, unambiguously. **The $c_i$ are the *coordinates* of $v$ in that basis** — and once you have them, a vector in *any* $k$-dimensional space is a column in $\mathbb{R}^k$, which is why the whole subject can be done with matrices. **Week 4 is that sentence taken seriously.**

*(Notice which condition does which job: spanning gives existence, independence gives uniqueness. Drop either and you lose exactly one half.)*

---

## 2. Bases Are Not Unique — Their Size Is

$$\left\{\begin{bmatrix}1\\0\end{bmatrix}, \begin{bmatrix}0\\1\end{bmatrix}\right\}, \qquad
\left\{\begin{bmatrix}1\\1\end{bmatrix}, \begin{bmatrix}1\\-1\end{bmatrix}\right\}, \qquad
\left\{\begin{bmatrix}2\\3\end{bmatrix}, \begin{bmatrix}1\\5\end{bmatrix}\right\}$$

**All three are bases for $\mathbb{R}^2$**, and there are infinitely many more — any two independent vectors will do. The first is the **standard basis** $e_1, e_2$, whose coordinates are just the entries of the vector; it is convenient and it is not privileged.

**What every one of them has in common is that there are two of them.** That is not a coincidence and it is not obvious, and it is §4.

> **This matters more than it looks.** Weeks 7, 10 and 11 are all about *choosing a different basis*
> so that a matrix becomes simple — diagonal, or triangular. **The freedom to change basis is the
> main tool in the second half of this course**, and it exists precisely because the standard basis
> was never special.

---

## 3. What Fails, and How

For $\mathbb{R}^3$:

| List | Independent? | Spans? | Basis? |
|---|---|---|---|
| $e_1, e_2, e_3$ | yes | yes | **yes** |
| $e_1, e_2$ | yes | **no** — misses the $z$-axis | no: too few |
| $e_1, e_2, e_3, (1,1,1)$ | **no** — L10 §4, four in $\mathbb{R}^3$ | yes | no: too many |
| $e_1, e_2, e_1 + e_2$ | **no** | **no** | no: **both** fail at once |

**The last row is the one to sit with.** Three vectors in $\mathbb{R}^3$, and they neither span nor are independent — they all lie in the $xy$-plane. **"The right number of vectors" is not a test for anything**, which is why the definition has two conditions and not a count.

---

## 4. Every Basis Has the Same Size

This is the theorem the whole chapter rests on. Without it, "dimension" is not well defined and every count in Week 2 was luck.

> **Lemma.** If $v_1,\dots,v_p$ **span** $V$, and $w_1,\dots,w_q$ in $V$ are **independent**, then
> $q \le p$.
>
> *Proof.* Each $w_j$ is in $V$, so it is a combination of the $v$'s. Collect the coefficients: with
> $V\!m$ the matrix whose columns are the $v_i$, and $W$ the matrix whose columns are the $w_j$,
> there is a $p \times q$ matrix $C$ with
> $$W = V\!m\,C.$$
> Suppose $q > p$. Then $C$ has more columns than rows, so by **L10 §4** its columns are dependent:
> there is $x \ne 0$ with $Cx = 0$. But then
> $$Wx = V\!m\,Cx = V\!m\,0 = 0,$$
> and $x \ne 0$ — so the columns of $W$ are dependent, contradicting independence of the $w$'s.
> Hence $q \le p$. $\square$

**Read the shape of that argument.** *An independent list can never be longer than a spanning list.* Everything else follows in two lines:

> **Theorem.** Any two bases of $V$ have the same number of vectors.
>
> *Proof.* Let $B_1$ have $p$ vectors and $B_2$ have $q$. $B_1$ spans and $B_2$ is independent, so
> $q \le p$. $B_2$ spans and $B_1$ is independent, so $p \le q$. Hence $p = q$. $\square$

> **Definition.** That common number is the **dimension** of $V$, written $\dim V$.

**$\dim\{0\} = 0$**, its basis being the empty list — a convention, and the one that makes every later formula come out right.

---

## 5. Dimension Puts the Loose Talk on a Footing

Week 2 said "two independent vectors in $\mathbb{R}^3$ span a plane" and L07 §4 claimed the subspaces of $\mathbb{R}^3$ are exactly $\{0\}$, a line, a plane, and $\mathbb{R}^3$. **Both are now statements with proofs available**: a subspace of $\mathbb{R}^3$ has dimension $0$, $1$, $2$ or $3$ — it cannot have more, since $4$ vectors in $\mathbb{R}^3$ are dependent — and those four numbers are precisely the point, line, plane and whole space.

**And $\dim \mathbb{R}^n = n$**, which sounds like a tautology and is not: it says the standard basis is *a* basis (easy) **and** that no other basis could have a different size (§4).

---

## 6. Bases for the Two Subspaces of Week 2

Both were computed in Week 2. **What was missing was a guarantee that they were the right size**, and §4 supplies it.

$$A = \begin{bmatrix}1&3&3&2\\ 2&6&9&7\\ -1&-3&3&4\end{bmatrix}, \qquad R = \begin{bmatrix}1&3&0&-1\\ 0&0&1&1\\ 0&0&0&0\end{bmatrix}, \qquad r = 2$$

### A basis for $\mathbf{C}(A)$: the pivot columns **of $A$**

$$\left\{\begin{bmatrix}1\\2\\-1\end{bmatrix}, \begin{bmatrix}3\\9\\3\end{bmatrix}\right\} \qquad \dim \mathbf{C}(A) = r = 2$$

**Spanning** is Week 2's L08 §3. **Independent** is L10 §5. So it is a basis, and

$$\boxed{\;\dim\mathbf{C}(A) = r\;}$$

*(And the columns **of $R$** would have been the wrong answer — Week 2's L08 §4. They are a basis, but for a different subspace.)*

### A basis for $\mathbf{N}(A)$: the special solutions

$$\left\{(-3,1,0,0),\ (1,0,-1,1)\right\} \qquad \dim\mathbf{N}(A) = n - r = 2$$

**Spanning** is Week 2's L09 §2. **Independent** is L10 §5. So

$$\boxed{\;\dim\mathbf{N}(A) = n - r\;}$$

**And now rank–nullity is a statement about dimensions rather than about a counting trick:**

$$\dim\mathbf{C}(A) + \dim\mathbf{N}(A) = r + (n-r) = n$$

Week 2 proved it by counting columns, which was honest and left one thing open: *the count of pivots might have depended on how you eliminated.* **It does not, and §4 is why** — the two subspaces have dimensions, dimensions are basis-independent, and the pivots merely compute them.

---

## 7. Bases Without Coordinates

$\mathbb{P}_3$, the polynomials of degree $\le 3$. **$\{1, x, x^2, x^3\}$ is a basis**: it spans by definition, and it is independent by L10 §6. So $\dim\mathbb{P}_3 = 4$.

**Four**, for an object that looks nothing like $\mathbb{R}^4$ — and the unique-coordinates theorem says $2 - 5x + x^3$ *is* the column $(2,-5,0,1)$, once the basis is fixed. **Every 4-dimensional real vector space is $\mathbb{R}^4$ wearing a disguise**, and the basis is what removes it. Week 4 makes this precise and it is the reason a course about columns of numbers says anything about functions.

**$\{1, x-1, (x-1)^2, (x-1)^3\}$ is also a basis for $\mathbb{P}_3$** — still four vectors, different coordinates. That change of basis is the Taylor expansion about $x = 1$.

> **And some spaces have no finite basis at all.** $C[0,1]$ is infinite-dimensional:
> $1, x, x^2, x^3, \dots$ are independent however many you take. Everything in this course is
> finite-dimensional and says so; the infinite case is a different subject and a harder one.

---

## 8. Two Shortcuts, Once You Know the Dimension

Testing "independent **and** spanning" is two jobs. **If you already know the dimension, one suffices.**

> **Theorem.** In a space of dimension $k$, any list of **exactly $k$** vectors that is *either*
> independent *or* spanning is automatically a basis.

*Why:* an independent list of $k$ vectors that failed to span could be extended to a longer independent list, exceeding a spanning list of size $k$ and contradicting §4's lemma. Symmetrically for the other case.

**Use it constantly.** To show three vectors form a basis for $\mathbb{R}^3$, check independence and stop — do not verify spanning. *(This is what Week 5's determinant test will be doing: $\det \ne 0$ for a square matrix says the $n$ columns are independent, hence a basis, hence the matrix is invertible.)*

**But the count alone proves nothing** — §3's last row is three vectors in $\mathbb{R}^3$ that are not a basis. **You still have to check one of the two conditions.**

---

## 9. What to Take Away

1. **A basis is independent *and* spanning.** Spanning gives existence of coordinates, independence gives uniqueness.
2. **Coordinates are what a basis is for.** Fix a basis and any vector becomes a column of numbers — which is why matrices describe polynomials and functions.
3. **Bases are not unique; their size is.** An independent list is never longer than a spanning list, and the two-line consequence is that all bases match.
4. **That common size is the dimension**, and $\dim\{0\} = 0$.
5. **$\dim\mathbf{C}(A) = r$ and $\dim\mathbf{N}(A) = n - r$**, with bases already computed in Week 2 — the pivot columns of $A$, and the special solutions.
6. **Rank–nullity is now about dimension**, so the pivot count cannot depend on how you eliminated.
7. **At the right size, independence *or* spanning is enough** — but the right size on its own is enough for nothing.

---

## Exercises

*(Not assessed.)*

1. Is $\{(1,1,0),(0,1,1),(1,0,1)\}$ a basis for $\mathbb{R}^3$? Use §8's shortcut and say which condition you checked and why the other is free.
2. Find a basis for the plane $x + 2y - z = 0$ in $\mathbb{R}^3$, and state its dimension. *(It is a null space. You have an algorithm.)*
3. Find a basis for the subspace of $2\times2$ **symmetric** matrices, and give its dimension. Now the $2\times2$ matrices with trace $0$. What is the dimension of their intersection?
4. Give a basis for $\mathbf{C}(A)$ and one for $\mathbf{N}(A)$ where $A = \begin{bmatrix}1&2&3\\2&4&6\end{bmatrix}$, and verify $\dim\mathbf{C} + \dim\mathbf{N} = 3$.
5. $V$ has dimension 5 and $U \subseteq V$ is a subspace with $\dim U = 5$. Prove $U = V$. *(Use §8.)*
6. Write $2 - 5x + x^3$ in coordinates with respect to $\{1, x, x^2, x^3\}$ and then with respect to $\{1, x-1, (x-1)^2, (x-1)^3\}$. Same polynomial, two columns in $\mathbb{R}^4$ — and the second is a Taylor expansion.

---

*MATH 241 · Week 3 · L11 · © CSE Department*
