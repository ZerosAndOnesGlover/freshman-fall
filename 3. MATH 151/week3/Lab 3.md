---
assessment: Lab 3
course: MATH 151
component: Labs
possible: 100
score: 100
status: graded
started: 2026-10-20
submitted: 2026-10-20
graded: 2026-10-20
source: "LAB 3 Induction Workshop.md"
---

# MATH 151 · Lab 3
## Answer Sheet

**Assessment:** `LAB 3 Induction Workshop.md`
**Points available:** 100 (graded on completion and effort)

---

## Section 1 — Computational Verification Before Proof

### Exercise 1.1 — Verify or Refute

All checks were run in Python for $n=0$ to $30$ (with the stated starting values).

**(a)** $\sum_{i=1}^{n} i=\frac{n(n+1)}{2}$, $n\ge1$: **TRUE** for all tested $n$. Both sides agree
throughout; `verify_claim` returns `(True, None)`.

**(b)** $2^n>n^2$, $n\ge1$: **FALSE** as stated. The smallest counterexample is $n=2$: $2^2=4$ and
$n^2=4$, and $4>4$ is false. Testing further, $n=3$ gives $8<9$ and $n=4$ gives $16=16$; the claim fails
at $n=2,3,4$ and holds from $n=5$ onward ($32>25$, $64>36$, ...). The correct statement is
"$2^n>n^2$ for all $n\ge5$."

**(c)** $n^2-n+41$ is prime for all $n\ge0$: **FALSE** for the unrestricted range, though it holds for
$n=0,\dots,40$. The first counterexample is $n=41$:
$$41^2-41+41=41^2=1681=41\cdot41,$$
which is composite. (`verify_claim` up to $30$ returns `(True, None)` — the failure lies beyond the
tested range, which is exactly why a finite check cannot establish a universal claim.)

**(d)** $7\mid(3^n+4^n)$, $n\ge1$: **FALSE.** At $n=1$, $3+4=7$, so it holds. At $n=2$,
$3^2+4^2=9+16=25$, and $25\bmod7=4\neq0$. First counterexample: $n=2$, value $25$.

**(e)** Every $n\ge8$ is $3a+5b$ with $a,b\ge0$: **TRUE** for all tested $n$ (verified through $n=60$,
with no gaps). For example $8=3+5$, $9=3\cdot3$, $10=5\cdot2$, $11=3\cdot2+5$, $12=3\cdot4$.

### Exercise 1.2 — Building the Inductive Step Computationally

Running `verify_inductive_step`:

- **claim_a (Gauss):** no failures on $1\le k<40$. The implication $P(k)\to P(k+1)$ holds at every
  tested $k$.
- **claim_b ($2^n>n^2$):** first failure at $k=1$. Here $P(1)$ is true ($2>1$) but $P(2)$ is false
  ($4>4$ is false), so $P(1)\to P(2)$ fails. From $k=2$ to $k=4$ the hypothesis $P(k)$ is false, so
  those implications are vacuous; from $k=5$ onward the step holds.
- **claim_c ($n^2-n+41$ prime):** first failure at $k=40$: $P(40)$ is true but $P(41)$ is false
  ($1681=41^2$). (Later failures occur at $k=44,49,56,\dots$ for the same reason — the predicate is not
  prime at those successors.)

**Can a claim be true for all large $n$ while the step fails at small $k$?** Yes. $2^n>n^2$ is true
eventually, but induction started at $n=1$ fails because the implication from $1$ to $2$ is false. The
remedy is to change the base case to $n=5$; then both the base and the step hold, and induction proves
the claim for $n\ge5$. Induction from the wrong starting point is not a proof of the wrong statement — it
is simply inapplicable.

---

## Section 2 — Writing Proofs from Scratch

### Exercise 2.1 — Summation

*Claim.* For all $n\ge0$, $\displaystyle\sum_{i=0}^{n}2^i=2^{n+1}-1$.

**Proof (weak induction).**

*Base case* ($n=0$): LHS $=2^0=1$; RHS $=2^{1}-1=1$. $\checkmark$

*Induction hypothesis:* Fix $k\ge0$ and assume $\displaystyle\sum_{i=0}^{k}2^i=2^{k+1}-1$.

*Inductive step:* We show the formula at $n=k+1$.
$$\sum_{i=0}^{k+1}2^i=\left(\sum_{i=0}^{k}2^i\right)+2^{k+1}
=\bigl(2^{k+1}-1\bigr)+2^{k+1}\quad\text{[IH applied here]}$$
$$=2\cdot2^{k+1}-1=2^{k+2}-1.$$
This is $2^{(k+1)+1}-1$, the formula at $n=k+1$.

*Conclusion:* By weak induction, $\sum_{i=0}^{n}2^i=2^{n+1}-1$ for all $n\ge0$. $\square$

### Exercise 2.3 — Divisibility

*Claim.* For all $n\ge0$, $6\mid(n^3+5n)$.

**Proof (weak induction).**

*Base case* ($n=0$): $0^3+5\cdot0=0=6\cdot0$, so $6\mid0$. $\checkmark$

*Induction hypothesis:* Fix $k\ge0$ and assume $6\mid(k^3+5k)$; write $k^3+5k=6m$ for some
$m\in\mathbb{Z}$.

*Inductive step:*
$$(k+1)^3+5(k+1)=k^3+3k^2+3k+1+5k+5=(k^3+5k)+3k^2+3k+6.$$
By the hypothesis, $k^3+5k=6m$, so
$$=6m+3k^2+3k+6=6m+3k(k+1)+6.$$
Since $k$ and $k+1$ are consecutive, one is even; write $k(k+1)=2t$ for some $t\in\mathbb{Z}$. Then
$$=6m+3(2t)+6=6m+6t+6=6(m+t+1),$$
and $m+t+1\in\mathbb{Z}$, so $6\mid\bigl((k+1)^3+5(k+1)\bigr)$.

*Conclusion:* By weak induction, $6\mid(n^3+5n)$ for all $n\ge0$. $\square$

*(Equivalently: $n^3+5n=(n-1)n(n+1)+6n$, and the product of three consecutive integers is divisible by
$6$ while $6n$ is clearly divisible by $6$.)*

### Exercise 2.5 — Strong Induction

*Claim.* Every integer $n\ge2$ is either prime or a product of two or more primes.

**Proof (strong induction).**

*Base case* ($n=2$): $2$ is prime, so it is either prime or a product of primes (the first alternative
holds). $\checkmark$

*Induction hypothesis:* Fix $k\ge2$ and assume that every integer $m$ with $2\le m\le k$ is prime or a
product of two or more primes.

*Inductive step:* Consider $k+1$.

- *Case 1: $k+1$ is prime.* Then $k+1$ is prime, so the claim holds.
- *Case 2: $k+1$ is composite.* Then $k+1=ab$ for integers $a,b$ with $2\le a,b\le k$ (a proper
  factorisation). By the strong hypothesis, each of $a$ and $b$ is prime or a product of two or more
  primes. Writing
  $$a=p_1p_2\cdots p_r,\qquad b=q_1q_2\cdots q_s$$
  with each $p_i,q_j$ prime, we obtain
  $$k+1=ab=p_1\cdots p_r\,q_1\cdots q_s,$$
  a product of at least two primes. So $k+1$ is prime or a product of two or more primes.

*Conclusion:* By strong induction, every integer $n\ge2$ is prime or a product of two or more primes.
$\square$

---

## Section 3 — Debugging Broken Proofs

### Bug 3.1

**Error.** The base case is missing entirely. Only the inductive step is proved.

**Is the claim true?** Yes — it is Gauss's formula $\sum_{i=1}^{n}i=\frac{n(n+1)}{2}$.

**Why it matters.** The step establishes only "if the formula holds at $k$, it holds at $k+1$." Without
a base case the implication chain has no starting point, so nothing is proved.

**Correct proof.** Add the base case $n=1$: LHS $=1$, RHS $=\frac{1\cdot2}{2}=1$. The given inductive
step is then valid (it also shows the algebra correctly: $\frac{k(k+1)}{2}+(k+1)=\frac{(k+1)(k+2)}{2}$),
so base case plus step complete the induction. $\square$

### Bug 3.2

**Error.** None — the proof is **correct**. The computation
$$(k+1)^3-(k+1)=k^3+3k^2+2k=(k^3-k)+3k^2+3k=(k^3-k)+3k(k+1)$$
is valid, and both terms are divisible by $3$: $3\mid(k^3-k)$ by the hypothesis, and $3\mid3k(k+1)$
obviously. Hence $3\mid\bigl((k+1)^3-(k+1)\bigr)$. The claim "for all $n\ge0$, $3\mid(n^3-n)$" is true,
with base case $0^3-0=0=3\cdot0$. The hint that "the error is subtle" is a distractor.

### Bug 3.3

**Errors.**

1. **The base case fails.** At $n=1$, $1^2+1=2$, which is even, not odd. The student notices this and
   proceeds anyway.
2. **Proceeding without a true base case is invalid.** An induction with a false base case proves
   nothing, however correct the step may be.
3. **The claim is false, and the hypothesis is never true.** In fact $n^2+n=n(n+1)$ is the product of
   consecutive integers, hence always even. So $P(k)$ is false for every $k$; the inductive step is
   vacuously true but never applicable. This is the "vacuous hypothesis" failure: a correct implication
   with a permanently false premise establishes nothing.

**Correct statement.** For all $n\ge1$, $n^2+n$ is **even**. Proof: $n^2+n=n(n+1)$, and one of $n$,
$n+1$ is even, so the product is even. (No induction needed; a parity case split also works.)

---

## Section 4 — Python: An Induction Checker

The function returns the tuple `(base_ok, step_ok, first_failure)`.

```python
def check_induction(base, predicate, n_max):
    if not predicate(base):
        return False, None, base
    for k in range(base, n_max):
        if predicate(k) and not predicate(k + 1):
            return True, False, k
    return True, True, None
```

Outputs obtained:

| Test | Call | Result |
|---|---|---|
| 1 | `check_induction(1, gauss, 100)` | `(True, True, None)` |
| 2 | `check_induction(1, exp_gt_sq, 20)` | `(True, False, 1)` |
| 3 | `check_induction(5, exp_gt_sq, 50)` | `(True, True, None)` |
| 4 | `check_induction(1, odd_claim, 20)` | `(False, None, 1)` |

(Additional checks: `check_induction(0, geo, 40) = (True, True, None)` for the geometric sum,
`check_induction(0, div6, 40) = (True, True, None)` for $6\mid(n^3+5n)$, and
`check_induction(0, div7, 40) = (True, True, None)` for $7\mid(8^n-1)$.)

**Interpretation.**

- **Test 1:** base case holds and every step holds to $n=100$. The tuple `(True, True, None)` says the
  induction is *not refuted* on this range — strong evidence, not proof.
- **Test 2:** base case holds but the step fails at $k=1$: $P(1)$ is true and $P(2)$ is false. Induction
  from $n=1$ is impossible.
- **Test 3:** from base $n=5$ everything holds to $n=50$, consistent with the true theorem for
  $n\ge5$.
- **Test 4:** `(False, None, 1)` — the base case itself fails ($1^2+1=2$ is even), so the step is never
  examined. The claim is false.

**Why a finite check supports but cannot replace a proof.** Checking finitely many $n$ can only refute a
universal claim (one counterexample suffices) or build confidence; it cannot cover infinitely many
cases. The induction proof handles all $n$ at once by establishing the base case and the implication
$P(k)\to P(k+1)$ for arbitrary $k$.

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-20 |

**Feedback:**
Completed and checked off. All checkoff items met: Exercise 1.1 verified/refuted all five claims with
correct outputs ($n=2$ for (b) and (d), $n=41$ for (c)); Exercise 1.2 explains the small-$k$ step
failure; Exercises 2.1, 2.3, 2.5 are complete proofs with labelled parts; Bug 3.1 repaired with the
missing base case; Bug 3.2 correctly identified as valid; Bug 3.3 identifies the failed base case, the
invalid continuation, and the permanently false hypothesis; Section 4 runs and interprets Tests 1 and 4.
