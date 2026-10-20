---
assessment: PS 0
course: MATH 151
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-19
submitted: 2026-10-19
graded: 2026-10-19
source: "PS 0 Propositional Logic.md"
---

# MATH 151 · PS 0
## Answer Sheet

**Assessment:** `PS 0 Propositional Logic.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Problem 1 — Propositions (9 points)

**Your answer:**

**(a)** "Every prime number greater than 2 is odd."

**Proposition, TRUE.** Any even number greater than 2 is divisible by 2 and so is composite; hence it
cannot be prime.

**(b)** "$x^2 - 4 = 0$"

**Not a proposition.** It is an open sentence with a free variable $x$; its truth value depends on
$x$ (true for $x=\pm2$, false otherwise), so it has no fixed truth value as written.

**(c)** "Prove that $1+1=2$."

**Not a proposition.** It is an imperative (a command), not a declarative statement, so it is neither
true nor false.

*Marks: 9 / 9*

---

### Problem 2 — Translation and Negation (12 points)

**Your answer:**

With $p$ = "network connected", $q$ = "server running", $r$ = "database reachable", $s$ = "user can
log in".

**(a)** "The user can log in if and only if the network is connected and the server is running."

Formula: $s \leftrightarrow (p \land q)$.

Negation:
$$\lnot\big(s \leftrightarrow (p\land q)\big)\equiv \big(s\land\lnot(p\land q)\big)\lor\big(\lnot s\land(p\land q)\big)\equiv \big(s\land(\lnot p\lor\lnot q)\big)\lor\big(\lnot s\land p\land q\big).$$

**(b)** "If the network is connected and the server is running, then the database is reachable and the user can log in."

Formula: $(p\land q)\to(r\land s)$.

Negation:
$$\lnot\big((p\land q)\to(r\land s)\big)\equiv (p\land q)\land\lnot(r\land s)\equiv p\land q\land(\lnot r\lor\lnot s).$$

**(c)** "The user cannot log in unless the network is connected."

"Unless" means "if not": $\lnot p\to\lnot s$, equivalently (contrapositive) $s\to p$.

Formula: $s\to p$ (equivalently $\lnot p\to\lnot s$).

Negation:
$$\lnot(s\to p)\equiv s\land\lnot p.$$

*Marks: 12 / 12*

---

### Problem 3 — Truth Tables (18 points)

**Your answer:**

**(a)** $(p\to q)\land(q\to p)$

| $p$ | $q$ | $p\to q$ | $q\to p$ | $(p\to q)\land(q\to p)$ |
|---|---|---|---|---|
| T | T | T | T | **T** |
| T | F | F | T | **F** |
| F | T | T | F | **F** |
| F | F | T | T | **T** |

**(b)** $(p\lor q)\to(p\land q)$

| $p$ | $q$ | $p\lor q$ | $p\land q$ | $(p\lor q)\to(p\land q)$ |
|---|---|---|---|---|
| T | T | T | T | **T** |
| T | F | T | F | **F** |
| F | T | T | F | **F** |
| F | F | F | F | **T** |

**(c)** $(p\to q)\to\big((p\to\lnot q)\to\lnot p\big)$

| $p$ | $q$ | $\lnot q$ | $p\to q$ | $p\to\lnot q$ | $(p\to\lnot q)\to\lnot p$ | whole formula |
|---|---|---|---|---|---|---|
| T | T | F | T | F | T | **T** |
| T | F | T | F | T | F | **T** |
| F | T | F | T | T | T | **T** |
| F | F | T | T | T | T | **T** |

**(d)** Classification:

- (a) is a **contingency**, and it is exactly the biconditional $p\leftrightarrow q$ (true when $p$
  and $q$ agree, false when they differ).
- (b) is a **contingency**; it is also equivalent to $p\leftrightarrow q$.
- (c) is a **tautology** (true in every row).
- None of the three is a contradiction.

The well-known connective that (a) represents is the **biconditional** (if and only if).

*Marks: 18 / 18*

---

### Problem 4 — Converse, Inverse, Contrapositive (12 points)

**Your answer:**

**(a)** "If a number is divisible by 4, then it is divisible by 2." Write $p$ = "divisible by 4",
$q$ = "divisible by 2"; the statement is $p\to q$.

- **Converse** $q\to p$: "If a number is divisible by 2, then it is divisible by 4." — **not equivalent** (e.g. 2).
- **Inverse** $\lnot p\to\lnot q$: "If a number is not divisible by 4, then it is not divisible by 2." — **not equivalent** (e.g. 2).
- **Contrapositive** $\lnot q\to\lnot p$: "If a number is not divisible by 2, then it is not divisible by 4." — **equivalent** to the original.

**(b)** $p\to(q\land r)$.

- **Converse**: $(q\land r)\to p$.
- **Inverse**: $\lnot p\to\lnot(q\land r)\equiv \lnot p\to(\lnot q\lor\lnot r)$.
- **Contrapositive**: $\lnot(q\land r)\to\lnot p\equiv (\lnot q\lor\lnot r)\to\lnot p$ — **equivalent** to the original.

*Marks: 12 / 12*

---

### Problem 5 — Proofs by Laws (21 points)

**Your answer:**

**(a)**
$$(p\land q)\lor(p\land\lnot q)\equiv p\land(q\lor\lnot q)\quad[\text{Distributivity}]\equiv p\land\top\quad[\text{Excluded Middle}]\equiv p\quad[\text{Identity}].$$

**(b)**
$$\begin{aligned}
(p\to q)\land(p\to\lnot q)&\equiv(\lnot p\lor q)\land(\lnot p\lor\lnot q)&&[\text{Conditional Equivalence}]\\
&\equiv\lnot p\lor(q\land\lnot q)&&[\text{Distributivity}]\\
&\equiv\lnot p\lor\bot&&[\text{Non-Contradiction}]\\
&\equiv\lnot p&&[\text{Identity}].
\end{aligned}$$

**(c)**
$$\begin{aligned}
\lnot(p\leftrightarrow q)&\equiv \lnot\big((p\to q)\land(q\to p)\big)&&[\text{Biconditional Expansion}]\\
&\equiv \lnot(p\to q)\lor\lnot(q\to p)&&[\text{De Morgan}]\\
&\equiv (p\land\lnot q)\lor(q\land\lnot p)&&[\text{Negation of Conditional}]\\
&\equiv (p\land\lnot q)\lor(\lnot p\land q)&&[\text{Commutativity}].
\end{aligned}$$

*Marks: 21 / 21*

---

### Problem 6 — Normal Forms (16 points)

**Your answer:**

**(a)** $p\to q\equiv \lnot p\lor q$ [Conditional Equivalence]. This is already a conjunction of one
clause, so
$$\text{CNF: }(\lnot p\lor q).$$

**(b)** $p\leftrightarrow q$
$$\equiv(p\to q)\land(q\to p)\quad[\text{Biconditional Expansion}]\equiv(\lnot p\lor q)\land(\lnot q\lor p)\quad[\text{Conditional Equivalence}].$$
$$\text{CNF: }(\lnot p\lor q)\land(\lnot q\lor p).$$

**(c)** $p\land(q\lor\lnot r)$ by the truth-table method:

| $p$ | $q$ | $r$ | $\lnot r$ | $q\lor\lnot r$ | $p\land(q\lor\lnot r)$ |
|---|---|---|---|---|---|
| T | T | T | F | T | **T** |
| T | T | F | T | T | **T** |
| T | F | T | F | F | **F** |
| T | F | F | T | T | **T** |
| F | T | T | F | T | **F** |
| F | T | F | T | T | **F** |
| F | F | T | F | F | **F** |
| F | F | F | T | T | **F** |

The true rows are $(T,T,T)$, $(T,T,F)$ and $(T,F,F)$, giving minterms $p\land q\land r$,
$p\land q\land\lnot r$ and $p\land\lnot q\land\lnot r$:
$$\text{DNF: }(p\land q\land r)\lor(p\land q\land\lnot r)\lor(p\land\lnot q\land\lnot r).$$

*Marks: 16 / 16*

---

### Problem 7 — Functional Completeness (12 points)

**Your answer:**

**(a)** Using only negation and disjunction, De Morgan gives
$$p\land q\equiv \lnot(\lnot p\lor\lnot q).$$
Since conjunction is expressible with $\{\lnot,\lor\}$, the set $\{\lnot,\lor\}$ is functionally
complete.

**(b)** Using only negation and implication,
$$p\lor q\equiv \lnot p\to q,$$
because $\lnot p\to q\equiv \lnot(\lnot p)\lor q\equiv p\lor q$ [Conditional Equivalence and
Double Negation]. Since disjunction is expressible with $\{\lnot,\to\}$, the set $\{\lnot,\to\}$ is
functionally complete.

*Marks: 12 / 12*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-19 |

**Feedback:**
All seven problems correct and complete.

- **P1:** Proposition/truth-value judgements correct; the open sentence and the imperative both
  correctly rejected as non-propositions with reasons.
- **P2:** All three translations correct, with negations pushed fully inward (De Morgan applied, no
  bare $\lnot(\cdots)$ left).
- **P3:** Truth tables complete with labelled intermediate columns; classifications correct and (a)
  identified as the biconditional.
- **P4:** Converse, inverse and contrapositive correct for both, with equivalence status stated.
- **P5:** Law-based proofs valid, each step citing the law; no truth tables used.
- **P6:** CNF for (a) and (b) and the truth-table DNF for (c) all correct.
- **P7:** Both completeness arguments correct.

No errors. Full marks.
