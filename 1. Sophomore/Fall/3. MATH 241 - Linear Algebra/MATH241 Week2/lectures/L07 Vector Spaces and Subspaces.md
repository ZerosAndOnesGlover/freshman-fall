# MATH 241 · Linear Algebra
## Week 2 · Lecture 1 of 3 · **Monday**
### Vector Spaces and Subspaces

---

**Reading:** Strang §3.1 · **Previous:** Week 1's L06, $A = LU$ · **Next:** L08, the column space

> **Quiz 2 is the first ten minutes of this lecture** and covers Week 1.

---

## 1. The Change of Altitude

For two weeks a vector has been a column of numbers and $A$ has been a thing you eliminate. **This week both become objects with properties, and the questions change.**

Week 0 asked *does $Ax = b$ have a solution?* and answered it one $b$ at a time, for $n^3/3$ operations each. **Week 2 asks which $b$ have solutions — all of them at once — and the answer turns out to be a geometric object.** You have already met it twice without the name: PS 0 Q2(c) found the equation of one, and Week 0's L01 §5 drew one.

The vocabulary for that object is *vector space*, and the definition is going to look disappointing. Bear with it; the payoff is in §5.

---

## 2. The Definition, and Why It Is So Bare

A **vector space** is a set $V$ with an addition and a scalar multiplication, such that for all $u, v, w \in V$ and all scalars $c, d$:

| | | | |
|---|---|---|---|
| 1 | $u + v \in V$ | **closed under addition** | |
| 2 | $cv \in V$ | **closed under scaling** | |
| 3 | $u + v = v + u$ | commutative | |
| 4 | $(u+v)+w = u+(v+w)$ | associative | |
| 5 | $\exists\,0$ with $v + 0 = v$ | a zero vector | |
| 6 | $\exists\,{-v}$ with $v + (-v) = 0$ | negatives | |
| 7 | $1v = v$ | | |
| 8 | $c(dv) = (cd)v$ | | |
| 9 | $c(u+v) = cu + cv$ | distributive | |
| 10 | $(c+d)v = cv + dv$ | distributive | |

**Notice what is absent.** There is no length, no angle, no dot product, no notion of one vector being bigger than another, and no way to multiply two vectors together. **A vector space is a set in which you can add and scale, and nothing else.**

> **That poverty is the whole point.** Every theorem proved from these ten axioms is true of *every*
> structure satisfying them — and the structures satisfying them are wildly unalike. The theorems
> are cheap to prove and enormously reusable, which is the trade the definition is making.
>
> Length and angle come back in **Week 8**, when they are added as extra structure (an *inner
> product*). Everything between here and there is deliberately done without them, so that you find
> out how much does not need them. The answer is: bases, dimension, rank, determinants,
> eigenvalues — most of the course.

**In this course the scalars are real numbers**, until Week 7 needs complex ones for eigenvalues of a rotation. Nothing before then changes when they do.

---

## 3. Spaces That Are Not $\mathbb{R}^n$

The axioms are worth having because so many things satisfy them.

| $V$ | A "vector" is | Zero vector |
|---|---|---|
| $\mathbb{R}^n$ | a column of $n$ reals | $(0,\dots,0)$ |
| $\mathbb{R}^{m\times n}$ | **an $m\times n$ matrix** | the zero matrix |
| $\mathbb{P}_3$ | a polynomial of degree $\le 3$ | the zero polynomial |
| $C[0,1]$ | **a continuous function on $[0,1]$** | the function $f(x) = 0$ |
| solutions of $y'' + y = 0$ | a function | $y = 0$ |
| $\mathbb{R}^\infty$ | an infinite sequence | $(0,0,0,\dots)$ |

**Check one of the strange ones.** Is $C[0,1]$ a vector space? Add two continuous functions — continuous. Scale one — continuous. There is a zero function, negatives exist, and addition of functions is commutative and associative because addition of *numbers* is. **All ten axioms, and none of them needed a coordinate.**

> **Why a CS student should care that functions form a vector space.** Because the theorems
> transfer. Week 8's projection — the nearest point in a subspace — becomes, in $C[0,1]$, the best
> approximation of a function by a polynomial. Week 12's Fourier item is a change of basis in a
> space of functions. **ECE 211 next term is that sentence for a whole course**, and it will assume
> you find it unremarkable.

**And one that is not a vector space.** The polynomials of degree *exactly* 3: $x^3$ and $-x^3 + x$ are both in it, and their sum $x$ is not. **Closure is the axiom that does the work**, and the one that fails.

---

## 4. Subspaces

Almost every space you meet arrives inside another one, so the useful notion is not "is this a vector space from scratch" but **"is this subset of a space I already have one of its own?"**

> **A subspace of $V$ is a subset $W \subseteq V$ that is itself a vector space under the same
> addition and scaling.**

Seven of the ten axioms are **inherited for free** — commutativity, associativity and the distributive laws hold in $W$ because they hold in $V$, and there is nothing to check. What can fail is only closure and the existence of $0$ and negatives. That collapses to a three-line test:

> **The subspace test.** $W \subseteq V$ is a subspace **iff**
>
> 1. $0 \in W$
> 2. $u, v \in W \Rightarrow u + v \in W$
> 3. $v \in W$, $c$ scalar $\Rightarrow cv \in W$
>
> *(Negatives come free from 3 with $c = -1$; and given 3 and a non-empty $W$, condition 1 follows
> from $c = 0$. Checking $0 \in W$ first is still the right habit, because it is instant and it
> disposes of most non-examples.)*

**Check $0$ first, always.** It is one substitution and it kills the commonest failure.

### Worked, in $\mathbb{R}^2$

| Set | Subspace? | Why |
|---|---|---|
| $\{(x,y) : y = 2x\}$ | **yes** | contains $(0,0)$; sums and multiples of points on a line through the origin stay on it |
| $\{(x,y) : y = 2x + 1\}$ | **no** | $(0,0)$ is not on it. *A line that misses the origin is not a subspace* |
| $\{(x,y) : xy = 0\}$ | **no** | the two axes. Contains $0$, closed under scaling, **and $(1,0) + (0,1) = (1,1)$ escapes** |
| $\{(x,y) : x \ge 0\}$ | **no** | the right half-plane. Closed under addition, and $(-1)(1,0) = (-1,0)$ escapes |
| $\{(0,0)\}$ | **yes** | the **zero subspace**. Small, legal, and it will matter |
| $\mathbb{R}^2$ itself | **yes** | every space is a subspace of itself |

**The third and fourth rows are the instructive ones.** Each satisfies two conditions out of three, which is why the test has three and why checking one is not enough. *(The axes fail addition; the half-plane fails scaling — and note that the half-plane is exactly the shape of a **linear-programming** feasible region, which is why that subject needs different machinery.)*

### The complete list for $\mathbb{R}^3$

**Every subspace of $\mathbb{R}^3$ is one of exactly four things:**

$$\{0\}, \qquad \text{a line through the origin}, \qquad \text{a plane through the origin}, \qquad \mathbb{R}^3$$

Dimensions $0, 1, 2, 3$. **There is nothing else** — no curved surfaces, no discs, no half-spaces, no sphere. Straight, unbounded, and through the origin, or it is not a subspace. Week 3 proves the list is complete; for now, notice how short it is, and that "through the origin" is doing most of the excluding.

---

## 5. Subspaces From Matrices

Now the reason any of this was introduced.

> **Claim.** For any $m\times n$ matrix $A$, the set $\;\mathbf{N}(A) = \{x \in \mathbb{R}^n : Ax = 0\}\;$ is a
> subspace of $\mathbb{R}^n$.
>
> *Proof.* $A0 = 0$, so $0 \in \mathbf{N}(A)$. If $Ax = 0$ and $Ay = 0$ then $A(x+y) = Ax + Ay = 0$.
> And $A(cx) = c(Ax) = c\cdot 0 = 0$. All three conditions, and **the only property of $A$ used was
> linearity** — §1 of Week 0's L01. $\square$

**Three lines, and it is the whole reason the definition is so bare.** Nothing about elimination, pivots, the size of $A$, or which entries it has. It is L09's subject and it is already proved.

**Now the contrast that makes the point.** Take $b \ne 0$ and consider $\{x : Ax = b\}$ — the solution set of an ordinary system.

$$A0 = 0 \ne b, \qquad\text{so } 0 \notin \{x : Ax = b\}.$$

**Not a subspace.** And it fails everything else too: if $Ax = b$ and $Ay = b$ then $A(x+y) = 2b \ne b$.

> **This is not a technicality; it is the structure of L09.** The solution set of $Ax = b$ is
> $\mathbf{N}(A)$ **shifted off the origin** by any one solution — a plane parallel to a subspace
> rather than a subspace. Week 0's L01 §5 proved that two solutions generate a line of them; this
> says what that line is a copy of. **The homogeneous problem $Ax = 0$ carries all the structure,
> and $b$ only decides where it sits.**

---

## 6. Intersections and Unions

Two subspaces $U, W$ of the same $V$:

**$U \cap W$ is always a subspace.** $0$ is in both. If $u$ is in both then so is $cu$, in each separately. Same for sums. *(Two planes through the origin in $\mathbb{R}^3$ meet in a line through the origin — or in the whole plane, if they coincide. Never in nothing: they always share $0$.)*

**$U \cup W$ is almost never one.** Take the $x$-axis and the $y$-axis in $\mathbb{R}^2$: their union is §4's third row, and $(1,0) + (0,1)$ escapes it. **A union is a subspace only when one of the two contains the other**, which is the degenerate case.

> **The repair is $U + W$**, the set of all $u + w$ — which *is* a subspace, and is the smallest one
> containing both. The two axes have $U + W = \mathbb{R}^2$. This is worth knowing now because Week 3
> counts dimensions with it, and Week 8 uses the special case where $U$ and $W$ meet only at $0$.

---

## 7. Span

Given any vectors $v_1, \dots, v_k$ in $V$:

$$\operatorname{span}\{v_1,\dots,v_k\} \;=\; \{\,c_1v_1 + \dots + c_kv_k \;:\; c_i \in \mathbb{R}\,\}$$

— every linear combination of them. **A span is always a subspace**, and the proof is the one you would write: it contains $0$ (all $c_i = 0$), a sum of two combinations is a combination, and a multiple of one is one.

**Span is the constructive way to produce a subspace**, as against the subspace test, which is the way to check one you were handed. Both are needed, and L08 is what happens when you apply the constructive one to the columns of a matrix.

> **Two spans, one subspace.** $\operatorname{span}\{(1,0),(0,1)\}$ and
> $\operatorname{span}\{(1,1),(1,-1),(2,0)\}$ are both $\mathbb{R}^2$. **The spanning set is not part
> of the answer** — which is exactly the question "how few vectors do I need, and how do I know?"
> that Week 3 is about.

---

## 8. What to Take Away

1. **A vector space is a set you can add in and scale in — nothing more.** No length, no angle, no product. That poverty is deliberate and Week 8 is where the missing structure is put back.
2. **Matrices, polynomials and continuous functions are vector spaces.** The theorems transfer, which is why ECE 211 and Week 12 can treat a Fourier transform as a change of basis.
3. **The subspace test is three conditions, and $0 \in W$ is the one to check first.** It disposes of most non-examples in one substitution.
4. **The subspaces of $\mathbb{R}^3$ are exactly: $\{0\}$, a line, a plane, $\mathbb{R}^3$** — all through the origin.
5. **$\mathbf{N}(A) = \{x : Ax = 0\}$ is a subspace, for every $A$**, and the proof uses only linearity.
6. **$\{x : Ax = b\}$ with $b \ne 0$ is not** — it misses $0$. It is $\mathbf{N}(A)$ translated, which is L09's complete solution.
7. **A span is always a subspace**, and the same subspace has many spanning sets.

---

## Exercises

*(Not assessed. PS 2 is the assessed work.)*

1. Which of these are subspaces of $\mathbb{R}^3$? (a) $\{(x,y,z) : x + y + z = 0\}$; (b) $\{(x,y,z): x+y+z = 1\}$; (c) $\{(x,y,z) : x = y\}$; (d) $\{(x,y,z) : x^2 = y^2\}$. For each failure, give the specific vectors that break it.
2. Is the set of $2\times2$ matrices with $\det A = 0$ a subspace? Give two such matrices whose sum is invertible.
3. Is the set of $n\times n$ **symmetric** matrices a subspace of $\mathbb{R}^{n\times n}$? What about the **invertible** ones? *(Week 1's L06 §2 has the first; the second is in `spaces.py`'s table.)*
4. Show that the polynomials $p$ with $p(1) = 0$ form a subspace of $\mathbb{P}_3$, and that those with $p(1) = 2$ do not.
5. Let $U$ be the $x$-axis and $W$ the line $y = x$, both in $\mathbb{R}^2$. Find $U \cap W$ and $U + W$. Is $U \cup W$ a subspace?
6. Prove that $\operatorname{span}\{v_1,\dots,v_k\}$ is the **smallest** subspace containing all the $v_i$ — that is, it is contained in every subspace that contains them.

---

*MATH 241 · Week 2 · L07 · © CSE Department*
