---
assessment: Quiz 1
course: MATH 151
component: Quizzes
possible: 20
score: 20
status: graded
started: 2026-10-19
submitted: 2026-10-19
graded: 2026-10-19
source: "QUIZ 1 Propositional Logic.md"
---

# MATH 151 · Quiz 1
## Answer Sheet

**Assessment:** `QUIZ 1 Propositional Logic.md`
**Points available:** 20

---

### Problem 1 — Translations (4 points)

**Your answer:**

With $p$ = "the loop terminates", $q$ = "the input is finite", $r$ = "memory is sufficient":

**(a)** "If the input is finite and memory is sufficient, then the loop terminates."
$$(q\land r)\to p.$$

**(b)** "The loop terminates only if memory is sufficient."
$$p\to r.$$
("$p$ only if $r$" means $p\to r$, not the converse.)

**(c)** "The loop does not terminate, but the input is finite."
$$\lnot p\land q.$$

**(d)** "The loop terminates if and only if both the input is finite and memory is sufficient."
$$p\leftrightarrow(q\land r).$$

*Marks: 4 / 4*

---

### Problem 2 — Truth Table (6 points)

**Your answer:**

Formula: $(p\to q)\land(\lnot p\to r)$.

| $p$ | $q$ | $r$ | $p\to q$ | $\lnot p$ | $\lnot p\to r$ | $(p\to q)\land(\lnot p\to r)$ |
|---|---|---|---|---|---|---|
| T | T | T | T | F | T | **T** |
| T | T | F | T | F | T | **T** |
| T | F | T | F | F | T | **F** |
| T | F | F | F | F | T | **F** |
| F | T | T | T | T | T | **T** |
| F | T | F | T | T | F | **F** |
| F | F | T | T | T | T | **T** |
| F | F | F | T | T | F | **F** |

**Classification: contingency** — the formula is true in some rows and false in others (it is neither a
tautology nor a contradiction).

*Marks: 6 / 6*

---

### Problem 3 — Algebraic Proof (5 points)

**Your answer:**

Prove $\lnot(p\to q)\equiv p\land\lnot q$ using only the logical laws:

$$\begin{aligned}
\lnot(p\to q)
&\equiv \lnot(\lnot p\lor q)&&[\text{Conditional Equivalence}]\\
&\equiv \lnot(\lnot p)\land\lnot q&&[\text{De Morgan}]\\
&\equiv p\land\lnot q&&[\text{Double Negation}].
\end{aligned}$$

*Marks: 5 / 5*

---

### Problem 4 (5 points)

**Your answer:**

**(a)** Simplify $\lnot\big((p\lor\lnot q)\land(\lnot p\lor r)\big)$, pushing negations inward:

$$\begin{aligned}
\lnot\big((p\lor\lnot q)\land(\lnot p\lor r)\big)
&\equiv \lnot(p\lor\lnot q)\lor\lnot(\lnot p\lor r)&&[\text{De Morgan}]\\
&\equiv (\lnot p\land\lnot\lnot q)\lor(\lnot\lnot p\land\lnot r)&&[\text{De Morgan twice}]\\
&\equiv (\lnot p\land q)\lor(p\land\lnot r)&&[\text{Double Negation twice}].
\end{aligned}$$

**Answer:** $(\lnot p\land q)\lor(p\land\lnot r)$.

**(b)(i)** $(p\lor q)\land(\lnot p\land\lnot q)$.

By De Morgan, $\lnot p\land\lnot q\equiv\lnot(p\lor q)$, so the formula is
$$(p\lor q)\land\lnot(p\lor q)\equiv \bot.$$
It is false in every row: a **contradiction**.

**(b)(ii)** $(p\to q)\lor(q\to p)$.

$$\begin{aligned}
(p\to q)\lor(q\to p)
&\equiv (\lnot p\lor q)\lor(\lnot q\lor p)&&[\text{Conditional Equivalence}]\\
&\equiv (\lnot p\lor p)\lor(q\lor\lnot q)&&[\text{Commutativity, Associativity}]\\
&\equiv \top\lor\top\equiv\top&&[\text{Excluded Middle}].
\end{aligned}$$
It is true in every row: a **tautology**.

*Marks: 5 / 5*

---

## Grading Summary

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-10-19 |

**Feedback:**
All correct per answer key.

- **P1:** All four translations correct, including "$p$ only if $r$" as $p\to r$ and the biconditional
  in (d).
- **P2:** Truth table complete with every intermediate column; final column and the contingency
  classification correct.
- **P3:** Law-based proof valid, with Conditional Equivalence, De Morgan and Double Negation each cited.
- **P4:** (a) negations pushed fully inward; (b) both classifications correct with justification
  (contradiction via $A\land\lnot A$; tautology via excluded middle).
