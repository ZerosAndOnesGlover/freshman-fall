---
assessment: Quiz 2
course: MATH 151
component: Quizzes
possible: 20
score: 20
status: graded
started: 2026-10-19
submitted: 2026-10-19
graded: 2026-10-19
source: "QUIZ 2 Predicate Logic.md"
---

# MATH 151 · Quiz 2
## Answer Sheet

**Assessment:** `QUIZ 2 Predicate Logic.md`
**Points available:** 20

---

### Problem 1 — Truth Values (4 points)

Domain $\mathbb{Z}^+$; $E(x)$ = "$x$ is even", $P(x)$ = "$x$ is prime".

**(a)** $\forall x\,(P(x)\to E(x))$: **FALSE.** Counterexample $x=3$: $P(3)$ is true and $E(3)$ is
false, so $P(3)\to E(3)$ is $T\to F$, which is false.

**(b)** $\exists x\,(P(x)\land E(x))$: **TRUE.** Witness $x=2$: $2$ is prime and $2$ is even.

**(c)** $\forall x\,(E(x)\to\lnot P(x))$: **FALSE.** Counterexample $x=2$: $E(2)$ is true and
$\lnot P(2)$ is false, so the implication is false. (The statement wrongly denies that any even number
is prime, but $2$ is.)

**(d)** $\exists x\,\forall y\,(x\le y)$: **TRUE.** Witness $x=1$: every $y\in\mathbb{Z}^+$ satisfies
$y\ge1$, so $1\le y$ for all $y$. (Over $\mathbb{Z}$ this would be false, but the domain here is
$\mathbb{Z}^+$, which has a least element.)

---

### Problem 2 — Negations (6 points)

**(a)** $\forall x\,\exists y\,(x+y=0)$

$$\lnot\bigl(\forall x\,\exists y\,(x+y=0)\bigr)\equiv\exists x\,\forall y\,(x+y\neq0).$$

"There is an integer $x$ such that $x+y\neq0$ for every integer $y$." (The original is true, with
$y=-x$; the negation is false.)

**(b)** $\exists x\,\forall y\,(x\cdot y=y)$

$$\lnot\bigl(\exists x\,\forall y\,(xy=y)\bigr)\equiv\forall x\,\exists y\,(xy\neq y).$$

"For every integer $x$ there is an integer $y$ with $xy\neq y$." (The original is true, with $x=1$; the
negation is false.)

**(c)** $\forall x\,\forall y\,(x<y\to\exists z\,(x<z<y))$

$$\lnot\bigl(\forall x\,\forall y\,(x<y\to\exists z\,(x<z<y))\bigr)
\equiv\exists x\,\exists y\,\bigl(x<y\land\forall z\,\lnot(x<z<y)\bigr),$$

equivalently

$$\exists x\,\exists y\,\bigl(x<y\land\forall z\,(z\le x\lor z\ge y)\bigr).$$

"There exist integers $x<y$ such that no integer $z$ lies strictly between them." Over $\mathbb{Z}$
the original is false ($x=0,y=1$ has no integer between) and the negation is true.

---

### Problem 3 — Translations (4 points)

**(a)** "Every function that terminates produces a correct output."

Domain: all functions. $T(f)$ = "$f$ terminates", $C(f)$ = "$f$ produces a correct output".

$$\forall f\,\bigl(T(f)\to C(f)\bigr).$$

(The connective must be $\to$, not $\land$: the claim restricts to terminating functions, it does not
assert that every function both terminates and is correct.)

**(b)** "There is no largest prime number."

Domain: $\mathbb{Z}^+$. $P(x)$ = "$x$ is prime".

$$\forall p\,\bigl(P(p)\to\exists q\,(P(q)\land q>p)\bigr).$$

"For every prime $p$ there is a prime $q$ with $q>p$." This is a positive $\forall\exists$ statement, as
required.

---

### Problem 4 — Nested Quantifiers (6 points)

**(a)** Are $\forall x\,\exists y\,P(x,y)$ and $\exists y\,\forall x\,P(x,y)$ equivalent? **NO.**

Counterexample: domain $\mathbb{Z}$, $P(x,y)$ = "$y>x$".

- $\forall x\,\exists y\,(y>x)$ is **true**: given any integer $x$, take $y=x+1$.
- $\exists y\,\forall x\,(y>x)$ is **false**: no fixed integer exceeds every integer.

So the two statements differ; the order of unlike quantifiers matters.

**(b)** $P(x,y)$ = "$x$ is a factor of $y$", domain $\mathbb{Z}^+$.

**(i)** $\forall x\,\exists y\,P(x,y)$: **TRUE.** For each $x$, take $y=x$; then $x\mid x$.

**(ii)** $\exists y\,\forall x\,P(x,y)$: **FALSE.** This would require one positive integer divisible by
every positive integer. Explicit failure: $y=1$ is not divisible by $2$; $y=2$ is not divisible by $3$;
no finite $y$ is divisible by $y+1$.

**(iii)** $\exists x\,\forall y\,P(x,y)$: **TRUE.** Witness $x=1$: $1\mid y$ for every $y\in\mathbb{Z}^+$.

**(iv)** $\forall x\,\forall y\,P(x,y)$: **FALSE.** Counterexample $x=2$, $y=3$: $2\nmid3$.

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-10-19 |

**Feedback:**
All four problems correct. Problem 1(d) correctly uses the least element $1$ of $\mathbb{Z}^+$ rather
than treating the domain as $\mathbb{Z}$. All negations are pushed fully inward with no $\lnot\forall$
or $\lnot\exists$ remaining. Translations use the correct connectives, and the nested-quantifier
counterexample is valid.
