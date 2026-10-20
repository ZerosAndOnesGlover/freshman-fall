---
assessment: PS 1
course: MATH 151
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-19
submitted: 2026-10-19
graded: 2026-10-19
source: "PS 1 Predicate Logic.md"
---

# MATH 151 · PS 1
## Answer Sheet

**Assessment:** `PS 1 Predicate Logic.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Part A — Predicates and Domains

#### A1 (9 points)

**Your answer:**

Factor: $P(x)=x^2-5x+6=(x-2)(x-3)$, so $P(x)$ is true exactly when $x=2$ or $x=3$.

**(a)** Over $\{0,1,2,3,4,6\}$: $P(2)=0$ and $P(3)=0$; every other value gives $P(x)\neq0$.
**Answer: $\{2,3\}$.**

**(b)** $\forall x\in\{0,1,2,3,4,6\},\,P(x)$ is **FALSE**. Counterexample: $x=0$, where
$P(0)=0-0+6=6\neq0$.

**(c)** $\exists x\in\{0,1,2,3,4,6\},\,P(x)$ is **TRUE**. Witness: $x=2$, since $P(2)=4-10+6=0$.

*Marks: 9 / 9*

---

#### A2 (9 points)

**Your answer:**

$D(x,y)$ means "$x$ divides $y$": there is an integer $k$ with $y=kx$. Domain: $\mathbb{Z}^+$.

**(a)** $D(3,12)$: **TRUE**, because $12=4\cdot3$ (take $k=4$).

**(b)** $D(5,13)$: **FALSE**, because $13=2\cdot5+3$ leaves remainder $3\neq0$, so no integer $k$
gives $13=5k$.

**(c)** $D(n,0)$ for any $n\in\mathbb{Z}^+$: **TRUE** under the standard definition of divisibility,
where $k$ ranges over all integers: take $k=0$, then $0=0\cdot n$. (If instead $k$ were restricted to
$\mathbb{Z}^+$, then $k\ge1$ forces $k\cdot n\ge n>0\neq0$, and the answer would be FALSE. The
standard convention allows $k=0$.)

*Marks: 9 / 9*

---

### Part B — Single Quantifiers

#### B1 (12 points)

**Your answer:**

Domain: $\mathbb{Z}$ unless stated.

**(a)** $\forall x,\ x^2>x$: **FALSE**. Counterexample: $x=0$, since $0^2=0\not>0$. (Also $x=1$.)

**(b)** $\exists x,\ x^2=x$: **TRUE**. Witness: $x=0$, since $0^2=0$. (Also $x=1$.)

**(c)** $\exists x\in\mathbb{Z},\ x^2=2$: **FALSE**. If $x^2=2$ then $x=\pm\sqrt2$, which is irrational,
so no integer satisfies it.

*Marks: 12 / 12*

---

#### B2 (10 points)

**Your answer:**

**(a)** "Some prime number is even."

Domain: $\mathbb{Z}^+$. Let $P(x)$ = "$x$ is prime" and $E(x)$ = "$x$ is even".
$$\exists x\,\big(P(x)\land E(x)\big).$$
This is **true**, with witness $x=2$.

**(b)** "There is a real number that is not the square of any real number."

Domain: $\mathbb{R}$.
$$\exists x\in\mathbb{R}\ \forall y\in\mathbb{R}\,\big(y^2\neq x\big).$$
This is **true**, with witness $x=-1$: no real square is negative.

*Marks: 10 / 10*

---

### Part C — Negation

#### C1 (15 points)

**Your answer:**

**(a)** $\forall x\in\mathbb{Z}\ \exists y\in\mathbb{Z}\,(x+y=0)$.

Negation:
$$\exists x\in\mathbb{Z}\ \forall y\in\mathbb{Z}\,(x+y\neq0).$$
Original is **TRUE** (given $x$, take $y=-x$); the negation is **FALSE**.

**(b)** $\exists x\in\mathbb{R}\ \forall y\in\mathbb{R}\,(x\cdot y=y)$.

Negation:
$$\forall x\in\mathbb{R}\ \exists y\in\mathbb{R}\,(x\cdot y\neq y).$$
Original is **TRUE**, with witness $x=1$ (since $1\cdot y=y$ for every $y$); the negation is **FALSE**.

**(c)** $\forall x\,\big(E(x)\to\exists k\,(x=2k)\big)$, where $E(x)$ = "$x$ is even".

Negation:
$$\exists x\,\big(E(x)\land\forall k\,(x\neq2k)\big).$$
The original is the definition of being even, so it is **TRUE**; the negation says some even number is
not twice any integer, which is **FALSE**.

*Marks: 15 / 15*

---

#### C2 (10 points)

**Your answer:**

**(a)** Statement: $\exists x\,(P(x)\land Q(x))$. Proposed negation: $\forall x\,(\lnot P(x)\land\lnot Q(x))$.

**Error:** the quantifier was flipped correctly, but De Morgan was applied wrongly inside — the
conjunction must become a **disjunction**. The proposed form says $P$ and $Q$ both fail for every $x$,
which is far too strong.
**Correct negation:** $\forall x\,(\lnot P(x)\lor\lnot Q(x))$.

**(b)** Statement: $\forall x\,(P(x)\to Q(x))$. Proposed negation: $\exists x\,(P(x)\to\lnot Q(x))$.

**Error:** the negation of a conditional is not another conditional. $\lnot(P\to Q)\equiv P\land\lnot Q$,
not $P\to\lnot Q$.
**Correct negation:** $\exists x\,(P(x)\land\lnot Q(x))$.

*Marks: 10 / 10*

---

### Part D — Nested Quantifiers

#### D1 (20 points)

**Your answer:**

Domain: $\mathbb{Z}$ unless stated.

**(a)** $\forall x\,\exists y\,(y>x)$: **TRUE**. Given any $x$, take $y=x+1$.

**(b)** $\exists y\,\forall x\,(y>x)$: **FALSE**. Such a $y$ would have to exceed every integer,
including $y$ itself (and $y+1$); no greatest integer exists.

**(c)** $\forall x\,\exists y\,(x\cdot y=1)$ over $\mathbb{Z}$: **FALSE**. Counterexample: $x=2$
requires $2y=1$, i.e. $y=\tfrac12\notin\mathbb{Z}$.

**(d)** $\forall x\,\exists y\,(x\cdot y=1)$ over $\mathbb{Q}\setminus\{0\}$: **TRUE**. Given a nonzero
rational $x=p/q$, take $y=q/p\in\mathbb{Q}\setminus\{0\}$; then $xy=1$.

*Marks: 20 / 20*

---

### Part E — Applications to CS

#### E1 (15 points)

**Your answer:**

The definition is
$$f(n)=O(g(n))\iff \exists C\in\mathbb{R}^+\ \exists n_0\in\mathbb{N}\ \forall n\in\mathbb{N}\,\big(n\ge n_0\to f(n)\le C\cdot g(n)\big).$$

**(a)** Negating and pushing the negations inward:
$$\begin{aligned}
f(n)\neq O(g(n))
&\iff \lnot\Big(\exists C>0\ \exists n_0\in\mathbb{N}\ \forall n\in\mathbb{N}\,(n\ge n_0\to f(n)\le C\,g(n))\Big)\\
&\iff \forall C>0\ \forall n_0\in\mathbb{N}\ \exists n\in\mathbb{N}\,\big(n\ge n_0\land f(n)>C\,g(n)\big).
\end{aligned}$$

**(b)** In plain English: for **every** positive constant $C$ and **every** threshold $n_0$, there is
some $n\ge n_0$ for which $f(n)$ exceeds $C\cdot g(n)$. No constant multiple of $g$ eventually bounds
$f$ from above — $f$ outgrows every such multiple.

*Marks: 15 / 15*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-19 |

**Feedback:**
All eight problems (22 parts) correct and complete.

- **A1–A2:** Factorisation and the finite-domain evaluation correct; divisibility cases justified,
  including the $D(n,0)$ convention stated explicitly.
- **B1–B2:** Truth values with named witnesses/counterexamples; both translations define predicates and
  domain and state the correct quantifier.
- **C1–C2:** Negations fully simplified with $\lnot$ pushed inward; both errors identified precisely
  (De Morgan inside, and the negation of a conditional).
- **D1:** All four nested statements decided, with a constructive witness or a clear obstruction.
- **E1:** Big-O negation correct ($\exists\exists\forall$ becomes $\forall\forall\exists$) and
  translated accurately.

No errors. Full marks.
