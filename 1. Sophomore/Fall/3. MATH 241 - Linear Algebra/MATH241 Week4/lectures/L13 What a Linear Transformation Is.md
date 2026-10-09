# MATH 241 · Linear Algebra
## Week 4 · Lecture 1 of 3 · **Monday**
### What a Linear Transformation Is

*“Mathematicians do not study objects, but the relations between objects; to them it is a matter of indifference if these objects are replaced by others, provided that the relations do not change.”* — Henri Poincaré, *Science and Hypothesis* (1902)

---

**Reading:** Strang §8.1 · **Previous:** Week 3's L12, the four subspaces · **Next:** L14, the matrix of a transformation

**Coursework:** 📊 **Quiz 4** today · 📝 **PS 4** released Wed this week, due Fri of Week 5 17:00 · 💬 **Recitation 3** Thu this week 15:00–15:50 · 📝 **PS 3** due Fri this week 17:00

> **Quiz 4 is the first ten minutes of this lecture** and covers Week 3.
>
> **This is a heavy week for other reasons.** PROG 201's Midterm 1 is Monday evening and CS 211's is
> Tuesday evening. MATH 241 has no exam this week — **its Midterm 1 is Week 6** — and PS 3 is due
> Friday as usual.

---

## 1. Back to the Beginning, With Everything Since

Week 0's L01 §1 defined linear equations and extracted two properties:

$$f(x + y) = f(x) + f(y) \qquad\text{and}\qquad f(cx) = c\,f(x).$$

**Everything in this course has been squeezed out of those two lines**, and the definition below is nothing more than giving them a name and letting the inputs be vectors.

> **Definition.** A function $T : V \to W$ between vector spaces is a **linear transformation** if
> for all $v, u \in V$ and all scalars $c$:
>
> $$T(v + u) = T(v) + T(u) \qquad\text{and}\qquad T(cv) = c\,T(v).$$

Combined into one condition: $T(c_1v_1 + c_2v_2) = c_1T(v_1) + c_2T(v_2)$, and by induction

$$T\!\left(\sum c_i v_i\right) = \sum c_i\,T(v_i).$$

**$T$ commutes with linear combinations** — which, since Week 2, is the only operation a vector space has. **A linear transformation is a function that respects the entire structure and nothing else exists to respect.**

### The consequence to check first, every time

$$T(0) = T(0 \cdot 0) = 0 \cdot T(0) = 0$$

**Every linear transformation sends $0$ to $0$.** Like the subspace test's first condition (Week 2's L07 §4), this is one substitution and it disposes of most non-examples immediately.

---

## 2. Examples, and the Ones That Fail

| $T$ | Linear? | |
|---|---|---|
| $T(v) = Av$ for a fixed matrix $A$ | **yes** | $A(v+u) = Av + Au$ — §3 |
| $T(x,y) = (2x - y,\; x + 3y)$ | **yes** | it is $Av$ in disguise |
| $T(v) = 3v$ | **yes** | scaling |
| $T(v) = 0$ | **yes** | the zero transformation |
| $T(v) = v$ | **yes** | the identity |
| **$T(v) = v + b$** for fixed $b \ne 0$ | **no** | $T(0) = b \ne 0$. **A translation is not linear** |
| $T(x,y) = (x^2, y)$ | **no** | $T(2,0) = (4,0) \ne 2T(1,0) = (2,0)$ |
| $T(x,y) = (\lvert x\rvert, y)$ | **no** | $T(-1,0) = (1,0) \ne -T(1,0)$ |
| $T(v) = \lVert v\rVert$ | **no** | scaling by $-1$ fails, and it lands in $\mathbb{R}$ not a vector |
| $T(A) = A^\mathsf{T}$ on $\mathbb{R}^{n\times n}$ | **yes** | Week 1's L06 §1 rules |
| $T(A) = A^{-1}$ | **no** | $T(2A) = \tfrac12A^{-1} \ne 2T(A)$ |
| $T(A) = \operatorname{trace}(A)$ | **yes** | the diagonal sum is a sum |
| $T(p) = p'$ on $\mathbb{P}_3$ | **yes** | **§4 — and it is the interesting one** |
| $T(f) = \int_0^1 f$ on $C[0,1]$ | **yes** | integration is linear |

> **The translation row is the one worth sitting with.** $T(v) = Av + b$ is called an **affine**
> map, it is what a graphics pipeline actually applies to a vertex, and it is **not linear.** The
> standard trick — homogeneous coordinates — embeds $\mathbb{R}^3$ in $\mathbb{R}^4$ as the plane
> $w = 1$, where the translation *becomes* linear:
>
> $$\begin{bmatrix}A & b\\ 0 & 1\end{bmatrix}\begin{bmatrix}v\\1\end{bmatrix} = \begin{bmatrix}Av + b\\ 1\end{bmatrix}$$
>
> **Every 3-D graphics API uses $4\times4$ matrices for this reason and no other.** CS 321 will
> present it as a convention; it is a repair for the failure in that table row.

---

## 3. Every Matrix Is a Linear Transformation

$$T(v) = Av \quad\Longrightarrow\quad A(v+u) = Av + Au, \qquad A(cv) = c(Av)$$

Both are Week 1's L04 rules. **So every $m\times n$ matrix gives a linear transformation $\mathbb{R}^n \to \mathbb{R}^m$**, and the two subspaces you already know are its two most basic features:

| Transformation language | Matrix language | Week |
|---|---|---|
| **kernel** $\ker T = \{v : Tv = 0\}$ | $\mathbf{N}(A)$ | 2 |
| **range** (image) $= \{Tv : v \in V\}$ | $\mathbf{C}(A)$ | 2 |
| $T$ is **injective** (one-to-one) | $\mathbf{N}(A) = \{0\}$ | 3 |
| $T$ is **surjective** (onto) | $\mathbf{C}(A) = \mathbb{R}^m$ | 3 |
| **rank–nullity** | $\dim\mathbf{C}(A) + \dim\mathbf{N}(A) = n$ | 3 |

**Nothing is new — the words are.** But the words are the ones the rest of mathematics uses, and rank–nullity in this language reads as a statement about functions: *the dimensions the map destroys plus the dimensions it preserves equal the dimensions it started with.*

**The converse is L14's subject:** every linear transformation between finite-dimensional spaces *is* a matrix, once bases are chosen. So the two notions coincide — and yet the transformation is the more fundamental object, because it exists before anyone picks a basis. **That gap is the whole of L15.**

---

## 4. Differentiation Is a Linear Transformation

$$D : \mathbb{P}_3 \to \mathbb{P}_3, \qquad D(p) = p'$$

**Linear**, because $(p+q)' = p' + q'$ and $(cp)' = cp'$ — two rules from MATH 141, now recognised as an instance of one definition.

- **$\ker D$** = the polynomials with $p' = 0$ = **the constants.** Dimension 1.
- **range $D$** = every polynomial of degree $\le 2$ *(any such $q$ is $p'$ for some cubic $p$)*. Dimension 3.
- **Rank–nullity:** $3 + 1 = 4 = \dim\mathbb{P}_3$ ✓

> **"The kernel of differentiation is the constants" is the reason $+\,C$ appears in every
> antiderivative you have ever written.** Two functions have the same derivative exactly when they
> differ by an element of $\ker D$ — which is Week 2's L09 §6 complete solution, $x_p + \mathbf{N}(A)$,
> for a map whose null space is the constants. **MATH 141's constant of integration and this course's
> null space are the same object**, and the resemblance is not an analogy.

L14 writes $D$ down as a $4\times4$ matrix. **It has a property no geometric example has**, and §4 of that lecture is where it shows up.

---

## 5. A Linear Map Is Determined by What It Does to a Basis

This is the theorem the rest of the week is built on.

> **Theorem.** Let $v_1,\dots,v_n$ be a basis for $V$, and let $w_1,\dots,w_n$ be **any** vectors in
> $W$. Then there is **exactly one** linear $T : V \to W$ with $T(v_i) = w_i$ for every $i$.
>
> *Proof.* **Uniqueness.** Every $v \in V$ is $\sum c_iv_i$ for a unique list of coefficients
> (Week 3's L11 §1). Linearity forces
> $$T(v) = T\!\left(\sum c_i v_i\right) = \sum c_i\,T(v_i) = \sum c_i w_i,$$
> so $T$'s value everywhere is dictated by its values on the basis.
>
> **Existence.** *Define* $T(v) = \sum c_iw_i$ using those unique coefficients. It is well defined
> because the $c_i$ are unique, and checking linearity is one line. $\square$

**Read what each half needed.** Uniqueness used *spanning* — every $v$ is reachable, so no vector escapes being determined. Existence used *independence* — the coefficients are unambiguous, so the recipe is a function. **Both halves of "basis", each doing exactly one job**, precisely as in Week 3's L11 §1.

### Why this is the productive fact

**You may specify a linear map by $n$ arbitrary choices and no more.** To define a transformation on $\mathbb{R}^3$, say where $e_1$, $e_2$, $e_3$ go — anywhere you like — and the map exists, is unique, and is linear. There is no consistency condition to check.

**And a linear map cannot surprise you.** Know it on a basis and you know it everywhere. This is why $n$ numbers per column suffice, why L14's construction works, and why **checking a claim about a linear map on a basis is a proof rather than a sample.**

> **Contrast a non-linear function**, where knowing $f$ on any finite set tells you nothing about
> the rest. Linearity is an extremely strong hypothesis, and this theorem is where the strength
> is visible.

---

## 6. Composition and Inverses

**If $T : U \to V$ and $S : V \to W$ are linear, so is $S \circ T$.**

$$(S\circ T)(v + u) = S\big(T(v)+T(u)\big) = S(T(v)) + S(T(u))$$

using $T$'s linearity and then $S$'s. **L14 §3 shows composition is matrix multiplication**, which will close a loop opened in Week 1: matrix multiplication was *defined* to make $(AB)x = A(Bx)$ hold, and this is the general statement of which that was the special case.

**If $T$ is a bijection, $T^{-1}$ is linear too.** Apply $T^{-1}$ to $T(T^{-1}(v) + T^{-1}(u)) = v + u$. **This is why $A^{-1}$ is a matrix and not something more exotic.**

---

## 7. What to Take Away

1. **$T(v+u) = Tv + Tu$ and $T(cv) = cTv$** — Week 0's two properties, with vectors in place of numbers.
2. **$T(0) = 0$ always**, so check it first. **A translation is not linear**, which is the entire reason 3-D graphics uses $4\times4$ matrices.
3. **Every matrix is a linear transformation**, with $\ker T = \mathbf{N}(A)$ and range $= \mathbf{C}(A)$. Injective means trivial kernel; surjective means the column space is everything.
4. **Differentiation is a linear transformation**, and $\ker D$ = the constants — which is why antiderivatives carry $+\,C$.
5. **A linear map is completely determined by its values on a basis**, and those values may be chosen arbitrarily. Spanning gives uniqueness; independence gives existence.
6. **Compositions and inverses of linear maps are linear**, which is why L14's matrix arithmetic is available at all.

---

## Exercises

*(Not assessed. PS 4 is the assessed work.)*

1. Which are linear? (a) $T(x,y) = (y,x)$; (b) $T(x,y) = (x+1, y)$; (c) $T(x,y) = (xy, 0)$; (d) $T(x,y) = (x, 0)$. For each failure give the specific vectors.
2. $T : \mathbb{R}^2 \to \mathbb{R}^2$ is linear with $T(1,0) = (2,3)$ and $T(0,1) = (-1,4)$. Find $T(5,-2)$. **You have enough information by §5** — say why.
3. Is $T(A) = A^\mathsf{T}A$ linear on $\mathbb{R}^{n\times n}$? Test it on $cA$.
4. Find $\ker T$ and the range for $T(x,y,z) = (x+y+z,\ x+y+z)$. Check rank–nullity.
5. $T : \mathbb{P}_3 \to \mathbb{P}_3$ is $T(p)(x) = p(x+1)$. Show it is linear, and find its kernel. Is it invertible?
6. Prove that $T$ is injective **iff** $\ker T = \{0\}$, directly from linearity. *(One direction is Week 3; do both from the definition of injective.)*

---

*MATH 241 · Week 4 · L13 · © CSE Department*
