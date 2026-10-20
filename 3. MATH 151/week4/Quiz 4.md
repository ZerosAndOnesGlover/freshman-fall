---
assessment: Quiz 4
course: MATH 151
component: Quizzes
possible: 20
score: 20
status: graded
started: 2026-10-20
submitted: 2026-10-20
graded: 2026-10-20
source: "QUIZ 4 Induction.md"
---

# MATH 151 · Quiz 4
## Answer Sheet

**Assessment:** `QUIZ 4 Induction.md`
**Points available:** 20

---

### Problem 1 — Geometric Sum (7 points)

*Claim.* For all $n\ge0$, $\displaystyle\sum_{i=0}^{n}2^i=2^{n+1}-1$.

**Proof (weak induction).**

*Base case* ($n=0$): LHS $=2^0=1$; RHS $=2^{1}-1=1$. The two sides are equal. $\checkmark$

*Induction hypothesis:* Fix $k\ge0$ and assume
$$\sum_{i=0}^{k}2^i=2^{k+1}-1.$$

*Inductive step:* We show the formula at $n=k+1$. Splitting off the last term and applying the
hypothesis,
$$\sum_{i=0}^{k+1}2^i=\left(\sum_{i=0}^{k}2^i\right)+2^{k+1}
=\bigl(2^{k+1}-1\bigr)+2^{k+1}\quad\text{[by IH]}$$
$$=2\cdot2^{k+1}-1=2^{k+2}-1.$$
This is the formula at $n=k+1$.

*Conclusion:* By the Principle of Mathematical Induction, $\sum_{i=0}^{n}2^i=2^{n+1}-1$ for all
$n\ge0$. $\square$

---

### Problem 2 — Divisibility (6 points)

*Claim.* For all $n\ge1$, $4\mid(5^n-1)$.

**Proof (weak induction).**

*Base case* ($n=1$): $5^1-1=4=4\cdot1$, so $4\mid4$. $\checkmark$

*Induction hypothesis:* Fix $k\ge1$ and assume $4\mid(5^k-1)$; write $5^k-1=4m$ for some
$m\in\mathbb{Z}$, so $5^k=4m+1$.

*Inductive step:*
$$5^{k+1}-1=5\cdot5^k-1=5(4m+1)-1=20m+5-1=20m+4=4(5m+1).$$
Since $5m+1\in\mathbb{Z}$, we have $4\mid(5^{k+1}-1)$.

*Conclusion:* By weak induction, $4\mid(5^n-1)$ for all $n\ge1$. $\square$

---

### Problem 3 — Error Analysis (7 points)

**(a)** The claim is **FALSE** as stated. Checking small values:

| $n$ | $n!$ | $n^2$ | $n!\ge n^2$? |
|---|---|---|---|
| 1 | 1 | 1 | true |
| 2 | 2 | 4 | **false** |
| 3 | 6 | 9 | **false** |
| 4 | 24 | 16 | true |
| 5 | 120 | 25 | true |

It fails at $n=2$ and at $n=3$, and holds for $n=1$ and for all $n\ge4$.

**(b)** The structure breaks because there is a **gap in the chain**: $P(1)$ is true but $P(2)$ is false.
Induction requires an unbroken sequence $P(n_0)\to P(n_0+1)\to\cdots$ from the base case onward; a
single step cannot jump over false cases. Concretely, the implication $P(1)\to P(2)$ is false: $1!\ge1$
is true while $2!\ge4$ is false. The "proof" hides this by using the inequality $k^2\ge k+1$, which
requires $k\ge2$ — a condition not available at $k=1$ and not covered by either stated base case. So the
step silently assumes a range of $k$ for which the claim has not been (and cannot be) anchored. The
presence of the failed base case at $n=2$ is the signal that induction from $n=1$ is impossible.

**(c)** *Corrected theorem:* For all $n\ge4$, $n!\ge n^2$.

This is true: the base case $n=4$ gives $4!=24\ge16=4^2$, and the inductive step's requirement
$k^2\ge k+1$ holds for every $k\ge2$, in particular for all $k\ge4$. (Equivalently, the claim holds at
$n=1$ and for $n\ge4$, but fails at $n=2,3$; starting induction at $n_0=4$ avoids the gap.)

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-10-20 |

**Feedback:**
All three problems correct. Problems 1 and 2 state base case, hypothesis, step, and conclusion
separately, with the hypothesis explicitly invoked in the algebra. Problem 3 identifies both failing
values $n=2,3$ (not just $n=2$), explains the broken $P(1)\to P(2)$ link and the hidden $k\ge2$
requirement, and gives the corrected theorem with $n_0=4$ and a valid base case.
