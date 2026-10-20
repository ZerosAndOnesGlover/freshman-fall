---
assessment: Lab 1
course: MATH 151
component: Labs
possible: 100
score: 100
status: graded
started: 2026-10-19
submitted: 2026-10-19
graded: 2026-10-19
source: "LAB 1 Quantifier Workshop.md"
---

# MATH 151 · Lab 1
## Answer Sheet

**Assessment:** `LAB 1 Quantifier Workshop.md`
**Points available:** 100 (graded on completion and effort)

> Write your answers under each heading. When you are done, set `status: submitted` in the
> frontmatter above.

---

## Section 1 — Hand Exercises: Evaluation over Finite Domains

### Exercise 1.1 — Evaluating Quantified Statements

Domain $D=\{1,2,3,4,5,6\}$, with $E=\{2,4,6\}$, $O=\{1,3,5\}$, $P=\{2,3,5\}$.

**(a)** $\forall x\in D\,(E(x)\lor O(x))$: **TRUE.** Every element of $D$ is either even or odd, and the
two sets exhaust $D$ with no overlap, so the disjunction holds for all six elements.

**(b)** $\exists x\in D\,(P(x)\land E(x))$: **TRUE.** Witness $x=2$: $2$ is prime and $2$ is even, so
$P(2)\land E(2)$ holds.

**(c)** $\exists x\in D\,\forall y\in D\,G(x,y)$, i.e. some $x>y$ for every $y$: **FALSE.** Any such
$x$ would have to exceed every element of $D$, including $x$ itself. The largest element is $6$, and
$6>6$ is false.

**(d)** $\forall x\in D\,\exists y\in D\,G(x,y)$: **FALSE.** Counterexample $x=1$: there is no $y\in D$
with $1>y$, since $1$ is the smallest element.

---

### Exercise 1.2 — The Quantifier Order Experiment

Divisibility table $P(x,y)$ = "$x$ divides $y$" for $D=\{1,\dots,10\}$:

| | $y=1$ | $y=2$ | $y=3$ | $y=4$ | $y=5$ | $y=6$ | $y=7$ | $y=8$ | $y=9$ | $y=10$ |
|---|---|---|---|---|---|---|---|---|---|---|
| $x=1$ | T | T | T | T | T | T | T | T | T | T |
| $x=2$ | F | T | F | T | F | T | F | T | F | T |
| $x=3$ | F | F | T | F | F | T | F | F | T | F |
| $x=4$ | F | F | F | T | F | F | F | T | F | F |
| $x=5$ | F | F | F | F | T | F | F | F | F | T |

**(a)** $\forall x\in D\,\exists y\in D\,P(x,y)$: **TRUE.** Each $x$ divides itself, and $x\le10$ means
$x\in D$: for $x=1,\dots,5$ take $y=x$.

**(b)** $\exists y\in D\,\forall x\in\{1,2,3,4,5\}\,P(x,y)$: **FALSE.** This would need a single $y$
divisible by all of $1,2,3,4,5$; the least such $y$ is $\operatorname{lcm}(1,2,3,4,5)=60>10$. Scanning
the columns, none has all T in rows $1$–$5$ (e.g. $y=6$ fails at $x=4,5$; $y=10$ fails at $x=3,4$).

**(c)** The statements are **not equivalent**: (a) is true and (b) is false, so $\forall x\exists y$ is
**not** the same as $\exists y\forall x$. In (a) the witness $y$ may depend on $x$ (here $y=x$); in (b) a
single fixed $y$ must work for every $x$ at once.

---

### Exercise 1.3 — Negation Practice

Domain: $\mathbb{Z}$.

**(a)** $\forall x\,\exists y\,(y=x+1)$.

Negation:
$$\exists x\,\forall y\,(y\neq x+1).$$
Original **TRUE** (given $x$, take $y=x+1$); negation **FALSE**.

**(b)** $\forall x\,\forall y\,(x<y\to x^2<y^2)$.

Negation:
$$\exists x\,\exists y\,(x<y\land x^2\ge y^2).$$
Original **FALSE**: counterexample $x=-3$, $y=1$, where $-3<1$ but $(-3)^2=9\ge1=1^2$. The negation is
**TRUE**, with witness $(x,y)=(-3,1)$.

---

### Exercise 1.4 — Translation Drill

**(a)** "For every bug, there exists a developer who can fix it."

Domain: bugs and developers. $\text{Fix}(d,b)$ = "developer $d$ can fix bug $b$."
$$\forall b\,\exists d\ \text{Fix}(d,b).$$
Same meaning: "No bug is beyond every developer's ability to fix."

**(b)** "Some feature is requested by every user."

Domain: features and users. $R(u,f)$ = "user $u$ requests feature $f$."
$$\exists f\,\forall u\ R(u,f).$$
Same meaning: "There is a feature that every user has requested."

**(c)** "No test case passes on an incorrect implementation."

Domain: test cases and implementations. $\text{Pass}(t,i)$ = "test $t$ passes on implementation $i$",
$\text{Correct}(i)$ = "$i$ is correct."
$$\forall t\,\forall i\,\big(\text{Pass}(t,i)\to\text{Correct}(i)\big).$$
Same meaning: "Any implementation on which a test passes is correct."

---

## Section 2 — Quantifiers in the Python REPL

### Exercise 2.1 — One Quantifier

Domain $D=\{1,2,3,4,5\}$.

**(a)** $\forall x\in D,\ x^2\ge x$:

`1**2 >= 1 and 2**2 >= 2 and 3**2 >= 3 and 4**2 >= 4 and 5**2 >= 5` evaluates to **`True`** — the
prediction is TRUE.

**(b)** $\exists x\in D,\ x^2=9$:

`1**2 == 9 or 2**2 == 9 or 3**2 == 9 or 4**2 == 9 or 5**2 == 9` evaluates to **`True`**, with witness
$x=3$.

**(c)** $\forall x\in D,\ x\text{ is odd}$:

`1 % 2 == 1 and 2 % 2 == 1 and 3 % 2 == 1 and 4 % 2 == 1 and 5 % 2 == 1` evaluates to **`False`**. Because
`and` short-circuits at the first `False`, evaluation stops at $x=2$: **$2$ is the counterexample**.

---

### Exercise 2.2 — Quantifier Order

Domain $\{1,2,3\}$, $P(x,y)$ = "$x+y=4$".

**(a)** $\forall x\,\exists y\,P(x,y)$:

```python
(1+1 == 4 or 1+2 == 4 or 1+3 == 4) and \
(2+1 == 4 or 2+2 == 4 or 2+3 == 4) and \
(3+1 == 4 or 3+2 == 4 or 3+3 == 4)
```

This is **`True`**: $x=1$ takes $y=3$, $x=2$ takes $y=2$, $x=3$ takes $y=1$.

**(b)** $\exists y\,\forall x\,P(x,y)$:

```python
(1+1 == 4 and 2+1 == 4 and 3+1 == 4) or \
(1+2 == 4 and 2+2 == 4 and 3+2 == 4) or \
(1+3 == 4 and 2+3 == 4 and 3+3 == 4)
```

This is **`False`**: no single $y$ works for every $x$ (e.g. $y=1$ works only for $x=3$).

**(c)** In $\forall x\,\exists y$ the choice of $y$ is made **after** $x$ is fixed, so $y$ may depend
on $x$. In $\exists y\,\forall x$ a single $y$ must be chosen **first** and then work for every $x$.
That is why (a) is true and (b) false.

---

### Exercise 2.3 — De Morgan for Quantifiers

On $D=\{1,2,3\}$ with $P(x)$ = "$x^2>1$":

```python
not (1**2 > 1 and 2**2 > 1 and 3**2 > 1)
(not 1**2 > 1) or (not 2**2 > 1) or (not 3**2 > 1)
```

Both evaluate to **`True`** (the first because $1^2>1$ is false, so the conjunction is false and its
negation true; the second because the first disjunct is true). They agree.

The law is **De Morgan's law for a conjunction**, $\lnot(A\land B\land C)\equiv\lnot A\lor\lnot B\lor\lnot C$,
which is exactly $\lnot\forall x\,P(x)\equiv\exists x\,\lnot P(x)$ written out over a finite domain.

---

## Section 3 — Reflection

1. **Difference between the two orders.** $\forall x\exists y\,P(x,y)$ lets the witness $y$ depend on
   $x$; $\exists y\forall x\,P(x,y)$ requires one fixed $y$ that works for all $x$. A non-mathematical
   example: "Everybody loves somebody" (the beloved may be different for each person) versus "There is
   somebody whom everybody loves" (one fixed person is loved by all). The first can be true while the
   second is false.

2. **Why an empty universal is TRUE.** A universal statement is an `and` over the domain. With no
   elements there are no terms, and the empty conjunction is the identity for `and` — TRUE. Equivalently,
   a universal claim is false only if it has a counterexample; an empty domain supplies none, so the
   claim is **vacuously true**.

---

## Checkoff Criteria

- [x] Exercise 1.1: all four statements evaluated with justification
- [x] Exercise 1.2: division table filled, questions (a)–(c) answered
- [x] Exercise 1.3: both negations correctly simplified
- [x] Exercise 2.2: both expressions evaluated and the difference explained
- [x] Exercise 2.3: both sides evaluated
- [x] Reflection question 1 answered

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-19 |

**Feedback:**
Completed and checked off. The four Section 1 evaluations each carry a justification or a named
counterexample; the divisibility table is correct and the $\forall\exists$ / $\exists\forall$
distinction is drawn from it; both negations are fully simplified; the REPL exercises match the
expected outputs, with the short-circuit counterexample and the quantifier-order explanation given;
and both reflection questions are answered. Every checkoff item was presented.
