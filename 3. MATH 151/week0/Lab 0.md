---
assessment: Lab 0
course: MATH 151
component: Labs
possible: 100
score: 100
status: graded
started: 2026-10-19
submitted: 2026-10-19
graded: 2026-10-19
source: "LAB 0 Truth Table Explorer.md"
---

# MATH 151 · Lab 0
## Answer Sheet

**Assessment:** `LAB 0 Truth Table Explorer.md`
**Points available:** 100 (graded on completion and effort)

> Write your answers under each heading. When you are done, set `status: submitted` in the
> frontmatter above.

---

## Section 1 — Warm-up: Hand Calculations

### Exercise 1.1 — Systematic Column Construction

**(a)** $p\land(q\lor\lnot r)$

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

True in rows 1, 2 and 4; false in the other five.

**(b)** $(p\lor q)\to(q\lor r)$

| $p$ | $q$ | $r$ | $p\lor q$ | $q\lor r$ | $(p\lor q)\to(q\lor r)$ |
|---|---|---|---|---|---|
| T | T | T | T | T | **T** |
| T | T | F | T | T | **T** |
| T | F | T | T | T | **T** |
| T | F | F | T | F | **F** |
| F | T | T | T | T | **T** |
| F | T | F | T | T | **T** |
| F | F | T | F | T | **T** |
| F | F | F | F | F | **T** |

Only row 4 is false, so this is a contingency.

---

### Exercise 1.2 — Equivalence Detection

**(a)** Are $p\to(q\to r)$ and $(p\land q)\to r$ equivalent?

| $p$ | $q$ | $r$ | $q\to r$ | $p\to(q\to r)$ | $p\land q$ | $(p\land q)\to r$ |
|---|---|---|---|---|---|---|
| T | T | T | T | T | T | T |
| T | T | F | F | F | T | F |
| T | F | T | T | T | F | T |
| T | F | F | T | T | F | T |
| F | T | T | T | T | F | T |
| F | T | F | F | T | F | T |
| F | F | T | T | T | F | T |
| F | F | F | T | T | F | T |

The two result columns agree in every row, so the formulas are **equivalent**. This is the
**Exportation** law: $p\to(q\to r)\equiv(p\land q)\to r$.

**(b)** Are $(p\lor q)\to r$ and $(p\to r)\land(q\to r)$ equivalent?

| $p$ | $q$ | $r$ | $p\lor q$ | $(p\lor q)\to r$ | $p\to r$ | $q\to r$ | $(p\to r)\land(q\to r)$ |
|---|---|---|---|---|---|---|---|
| T | T | T | T | T | T | T | T |
| T | T | F | T | F | F | F | F |
| T | F | T | T | T | T | T | T |
| T | F | F | T | F | F | T | F |
| F | T | T | T | T | T | T | T |
| F | T | F | T | F | T | F | F |
| F | F | T | F | T | T | T | T |
| F | F | F | F | T | T | T | T |

The two result columns agree in every row, so the formulas are **equivalent**. This is the
distribution of implication over disjunction:
$(p\lor q)\to r\equiv(p\to r)\land(q\to r)$.

---

### Exercise 1.3 — Tautology Hunting

**(a)** $(p\to q)\to(\lnot q\to\lnot p)$

This is the **Law of Contrapositive** as a tautology: it asserts that a conditional and its
contrapositive are equivalent. Every row is true, so it is a **tautology**.

**(b)** $\big(p\land(p\to q)\big)\to q$

Every row is true, so it is a **tautology**. This is **modus ponens** — the fundamental inference
rule: "if $p$ is true, and $p$ implies $q$, then $q$ is true."

---

## Section 2 — Logic in the Wild

### Exercise 2.1 — Decoding Code Conditions

**(a)** `not (x > 0 and y > 0)`, with $p$ = "$x>0$", $q$ = "$y>0$":
$$\lnot(p\land q)\equiv\lnot p\lor\lnot q\quad[\text{De Morgan}].$$
The branch executes when **$x\le 0$ or $y\le 0$** — at least one of $x,y$ is non-positive, matching the
comment.

**(b)** `!connected || (connected && !authenticated)`, with $p$ = "connected", $q$ = "authenticated":
$$\begin{aligned}
\lnot p\lor(p\land\lnot q)&\equiv(\lnot p\lor p)\land(\lnot p\lor\lnot q)&&[\text{Distributivity}]\\
&\equiv\top\land(\lnot p\lor\lnot q)&&[\text{Excluded Middle}]\\
&\equiv\lnot p\lor\lnot q\equiv\lnot(p\land q)&&[\text{Identity, De Morgan}].
\end{aligned}$$
So the condition simplifies to **`!(connected && authenticated)`**: deny access unless the user is both
connected and authenticated. The original is redundant.

**(c)** `!(a == b) || !(b == c)`, with $p$ = "$a=b$", $q$ = "$b=c$":
$$\lnot p\lor\lnot q\equiv\lnot(p\land q)\quad[\text{De Morgan}],$$
i.e. **`!(a == b && b == c)`** — the branch executes when $a,b,c$ are **not all equal**, matching the
comment.

---

### Exercise 2.2 — Logic Gates as Connectives

Inputs $A=1$, $B=0$, $C=1$.

**(a)** Step by step:

- Gate 1: $X=A\text{ AND }B=1\text{ AND }0=0$.
- Gate 2: $Y=\text{NOT }X=\text{NOT }0=1$.
- Gate 3: $Z=Y\text{ OR }C=1\text{ OR }1=1$.
- Gate 4: $\text{Output}=Z\text{ AND }(\text{NOT }C)=1\text{ AND }0=0$.

**Output $=0$.**

**(b)** In terms of $A,B,C$:
$$\text{Output}=\Big(\lnot(A\land B)\lor C\Big)\land\lnot C.$$

**(c)** Simplify:
$$\begin{aligned}
\big(\lnot(A\land B)\lor C\big)\land\lnot C
&\equiv\big(\lnot(A\land B)\land\lnot C\big)\lor(C\land\lnot C)&&[\text{Distributivity}]\\
&\equiv\big(\lnot(A\land B)\land\lnot C\big)\lor\bot&&[\text{Non-Contradiction}]\\
&\equiv\lnot(A\land B)\land\lnot C&&[\text{Identity}]\\
&\equiv\lnot\big((A\land B)\lor C\big)&&[\text{De Morgan}].
\end{aligned}$$
Simplest form: **$\lnot((A\land B)\lor C)$** — the output is $1$ only when neither $A\text{ and }B$
nor $C$ is true.

---

## Section 3 — Truth Tables in the Python REPL

### Exercise 3.1 — One Row at a Time

Evaluating `(not p) or q` for all four rows:

| $p$ | $q$ | `(not p) or q` |
|---|---|---|
| True | True | True |
| True | False | False |
| False | True | True |
| False | False | True |

This is exactly the truth table of $p\to q$.

### Exercise 3.2 — Checking an Equivalence

For each of the four rows, `(not (p and q)) == ((not p) or (not q))` prints `True`:

| $p$ | $q$ | result |
|---|---|---|
| True | True | True |
| True | False | True |
| False | True | True |
| False | False | True |

All four results are `True`, so the biconditional between the two formulas is true in every row — i.e.
a **tautology**. Therefore $\lnot(p\land q)\equiv\lnot p\lor\lnot q$: the formulas are logically
equivalent (De Morgan's law).

### Exercise 3.3 — Finding a Counterexample

Evaluating `((not p) or q) == ((not q) or p)` row by row:

| $p$ | $q$ | result |
|---|---|---|
| True | True | True |
| True | False | False |
| False | True | False |
| False | False | True |

The `False` rows are $(T,F)$ and $(F,T)$; either is a **counterexample**. With $p$ = "It is raining"
and $q$ = "The ground is wet", take $p$ false and $q$ true: it is not raining but the ground is wet
(a sprinkler). Then $p\to q$ is vacuously true, while the converse $q\to p$ ("if the ground is wet it
rained") is false. So a conditional is **not** equivalent to its converse.

---

## Section 4 — Reflection

1. **Most surprising result.** The redundancy in Exercise 2.1(b): a condition that looks like it has
   three separate cases collapses, by the laws, to the single condition `!(connected && authenticated)`.
   Without the algebra the redundancy is invisible.

2. **Logic and Python.** Python's `and`, `or` and `not` implement exactly the connectives $\land$,
   $\lor$ and $\lnot$ over `True`/`False`; their truth tables are identical. The one practical
   difference is that Python evaluates them by short-circuit (lazily), whereas a truth table evaluates
   both operands.

3. **Cost of truth tables.** `2 ** 32` is $4{,}294{,}967{,}296$ rows, so at $10^9$ rows per second that
   is about **4.29 seconds**. For $n=64$, `2 ** 64` is about $1.845\times10^{19}$ rows, which at
   $10^9$ rows per second is about $1.845\times10^{10}$ seconds, or roughly **585 years**. Brute-force
   truth-table enumeration is therefore not a viable algorithm for large formulas.

---

## Checkoff Criteria

- [x] Completed hand truth tables for Section 1 (1.1 and 1.2)
- [x] Section 2.1 with simplified conditions
- [x] Exercise 3.2's four `True` results, and Exercise 3.3's counterexample explained

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-19 |

**Feedback:**
Completed and checked off. All Section 1 truth tables are systematic and correctly labelled; both
Section 2.1 conditions are simplified with the laws and matched to the code comments; the REPL
equivalence check and the converse counterexample are both correct and explained. Lab is graded on
completion, and every required item was presented.
