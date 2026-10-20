---
assessment: PS 3
course: MATH 151
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-20
submitted: 2026-10-20
graded: 2026-10-20
source: "PS 3 Induction.md"
---

# MATH 151 · PS 3
## Answer Sheet

**Assessment:** `PS 3 Induction.md`
**Points available:** 100

---

### Part A — Weak Induction: Summation Formulas  (14 points)

**Your answer:**

#### A1 (14 points)

**(a)** *Claim.* For all $n\ge1$, $\displaystyle\sum_{i=1}^{n} i(i+1)=\frac{n(n+1)(n+2)}{3}$.

**Proof (weak induction).**

*Base case* ($n=1$): LHS $=1\cdot2=2$; RHS $=\frac{1\cdot2\cdot3}{3}=2$. Both sides agree. $\checkmark$

*Induction hypothesis:* Fix $k\ge1$ and assume
$$\sum_{i=1}^{k} i(i+1)=\frac{k(k+1)(k+2)}{3}.$$

*Inductive step:* We show the formula at $n=k+1$. Using the hypothesis,
$$\sum_{i=1}^{k+1} i(i+1)=\frac{k(k+1)(k+2)}{3}+(k+1)(k+2).$$
Factor out $(k+1)(k+2)$:
$$=(k+1)(k+2)\left(\frac{k}{3}+1\right)=(k+1)(k+2)\cdot\frac{k+3}{3}=\frac{(k+1)(k+2)(k+3)}{3}.$$
Since $(k+1)+1=k+2$ and $(k+1)+2=k+3$, this is exactly the formula with $n=k+1$.

*Conclusion:* By weak induction, the identity holds for all $n\ge1$. $\square$

**(b)** *Claim.* For all $n\ge1$, $\displaystyle\sum_{i=1}^{n}\frac{1}{i(i+1)}=\frac{n}{n+1}$.

**Proof (weak induction).**

*Base case* ($n=1$): LHS $=\frac{1}{1\cdot2}=\frac12$; RHS $=\frac{1}{2}$. $\checkmark$

*Induction hypothesis:* Fix $k\ge1$ and assume
$$\sum_{i=1}^{k}\frac{1}{i(i+1)}=\frac{k}{k+1}.$$

*Inductive step:* Using the hypothesis,
$$\sum_{i=1}^{k+1}\frac{1}{i(i+1)}=\frac{k}{k+1}+\frac{1}{(k+1)(k+2)}
=\frac{k(k+2)+1}{(k+1)(k+2)}=\frac{k^2+2k+1}{(k+1)(k+2)}.$$
Since $k^2+2k+1=(k+1)^2$,
$$=\frac{(k+1)^2}{(k+1)(k+2)}=\frac{k+1}{k+2},$$
which is the formula at $n=k+1$.

*Conclusion:* By weak induction, the identity holds for all $n\ge1$. $\square$

*Marks: 14 / 14*

---

### Part B — Weak Induction: Inequalities and Divisibility  (16 points)

**Your answer:**

#### B1 (16 points)

**(a)** *Claim.* For all $n\ge0$, $7\mid(8^n-1)$.

**Proof (weak induction).**

*Base case* ($n=0$): $8^0-1=1-1=0=7\cdot0$, so $7\mid0$. $\checkmark$

*Induction hypothesis:* Fix $k\ge0$ and assume $7\mid(8^k-1)$; write $8^k-1=7m$ for some $m\in\mathbb{Z}$, i.e. $8^k=7m+1$.

*Inductive step:*
$$8^{k+1}-1=8\cdot8^k-1=8(7m+1)-1=56m+8-1=56m+7=7(8m+1).$$
Since $8m+1\in\mathbb{Z}$, we have $7\mid(8^{k+1}-1)$.

*Conclusion:* By weak induction, $7\mid(8^n-1)$ for all $n\ge0$. $\square$

**(b)** *Claim.* For all $n\ge4$, $n!>2^n$.

**Proof (weak induction).**

*Base case* ($n=4$): $4!=24$ and $2^4=16$, and $24>16$. $\checkmark$

*Induction hypothesis:* Fix $k\ge4$ and assume $k!>2^k$.

*Inductive step:*
$$(k+1)!=(k+1)\cdot k!>(k+1)\cdot2^k,$$
using the hypothesis and $k+1>0$. Since $k\ge4$, we have $k+1\ge5>2$, so
$$(k+1)\cdot2^k>2\cdot2^k=2^{k+1}.$$
Chaining the two inequalities gives $(k+1)!>2^{k+1}$.

*Conclusion:* By weak induction, $n!>2^n$ for all $n\ge4$. $\square$

*Marks: 16 / 16*

---

### Part C — Weak Induction: Recursive Sequences and Algorithms  (14 points)

**Your answer:**

#### C1 (14 points)

Let $a_1=5$ and $a_n=3a_{n-1}-4$ for $n\ge2$.

**(a)** Computing directly:
$$a_1=5,\qquad a_2=3(5)-4=11,\qquad a_3=3(11)-4=29,\qquad a_4=3(29)-4=83.$$

**(b)** *Conjecture:* $a_n=3^n+2$ for all $n\ge1$.

*How it is found:* Rearranging the recurrence,
$$a_n-2=3a_{n-1}-6=3(a_{n-1}-2),$$
so $a_n-2$ is geometric with ratio $3$ and first term $a_1-2=3$. Hence $a_n-2=3\cdot3^{n-1}=3^n$, giving $a_n=3^n+2$. The values in (a) check: $3^1+2=5$, $3^2+2=11$, $3^3+2=29$, $3^4+2=83$.

**(c)** *Claim.* For all $n\ge1$, $a_n=3^n+2$.

**Proof (weak induction).**

*Base case* ($n=1$): $a_1=5=3^1+2$. $\checkmark$

*Induction hypothesis:* Fix $k\ge1$ and assume $a_k=3^k+2$.

*Inductive step:* By the recurrence and then the hypothesis,
$$a_{k+1}=3a_k-4=3(3^k+2)-4=3^{k+1}+6-4=3^{k+1}+2.$$

*Conclusion:* By weak induction, $a_n=3^n+2$ for all $n\ge1$. $\square$

*Marks: 14 / 14*

---

### Part D — Strong Induction  (26 points)

**Your answer:**

#### D1 (12 points)

*Claim.* Every integer $n\ge2$ has a prime divisor.

**Proof (strong induction).**

*Base case* ($n=2$): $2$ is prime and $2\mid2$, so $2$ has a prime divisor, namely itself. $\checkmark$

*Induction hypothesis:* Fix $k\ge2$ and assume that every integer $m$ with $2\le m\le k$ has a prime divisor.

*Inductive step:* Consider $k+1$.

- *Case 1: $k+1$ is prime.* Then $k+1\mid k+1$, so $k+1$ is its own prime divisor.
- *Case 2: $k+1$ is composite.* Then $k+1=ab$ with integers $a,b$ satisfying $2\le a\le k$ and $2\le b\le k$. By the hypothesis applied to $a$, $a$ has a prime divisor $p$. Since $p\mid a$ and $a\mid(k+1)$, transitivity of divisibility gives $p\mid(k+1)$, so $k+1$ has a prime divisor.

In both cases $k+1$ has a prime divisor.

*Conclusion:* By strong induction, every integer $n\ge2$ has a prime divisor. $\square$

#### D2 (14 points)

*Claim.* Every integer $n\ge6$ can be written as $n=3a+4b$ with $a,b$ non-negative integers.

**Proof (strong induction).**

*Base cases:*
$$6=3(2)+4(0),\qquad 7=3(1)+4(1),\qquad 8=3(0)+4(2).$$
Each has the required form with $a,b\ge0$. $\checkmark$

*Induction hypothesis:* Fix $k\ge8$ and assume that every integer $m$ with $6\le m\le k$ can be written as $m=3a+4b$ with $a,b\ge0$.

*Inductive step:* Consider $k+1$. Since $k\ge8$, we have $k-2\ge6$, and $k-2\le k$, so the hypothesis applies to $m=k-2$. Thus
$$k-2=3a+4b$$
for some non-negative integers $a,b$. Then
$$k+1=(k-2)+3=3a+4b+3=3(a+1)+4b,$$
and $a+1\ge0$, $b\ge0$. So $k+1$ has the required form.

*Conclusion:* By strong induction, every integer $n\ge6$ is of the form $3a+4b$ with $a,b\ge0$. $\square$

*Marks: 26 / 26*

---

### Part E — Proof Analysis and Error Detection  (30 points)

**Your answer:**

#### E1 (14 points)

*Claim (false).* For all $n\ge1$, $\displaystyle\sum_{i=1}^{n} i=\frac{n^2+n+2}{2}$.

**Error 1 — the base case fails and is dismissed.** At $n=1$ the left side is $1$ while the formula gives
$\frac{1+1+2}{2}=2$. The "proof" acknowledges the mismatch and then writes "close enough — the formula
is approximately right." That is not a valid base case: an induction proof requires exact equality at
the base, and $2\neq1$. With a false base case the induction never starts.

**Error 2 — the claim itself is false.** $\sum_{i=1}^{n}i=\frac{n(n+1)}{2}$, not $\frac{n^2+n+2}{2}$;
the proposed right-hand side is exactly $1$ too large for every $n$. Testing $n=2$: LHS $=3$, RHS
$=\frac{4+2+2}{2}=4$.

**Error 3 — misreading the logic of the inductive step.** The algebra in the inductive step is in fact
correct: it verifies
$$\frac{k^2+k+2}{2}+(k+1)=\frac{(k+1)^2+(k+1)+2}{2}.$$
But this only proves the conditional $P(k)\to P(k+1)$; it does not prove $P(k)$. Because the base case
is false, the conditional is never triggered (there is no true instance to start from), so nothing
follows. A correct inductive step cannot rescue a false formula: here it merely propagates the constant
error of $1$ from $k$ to $k+1$.

#### E2 (16 points)

*Claim.* For all $n\ge1$, $2^n\ge n+1$.

**The structural error.** The induction hypothesis is stated as "assume $2^n\ge n+1$ for **all**
$n\ge1$." That assumes the entire statement being proved, for every $n$ at once — including
$n=k+1$, which is exactly what the step is supposed to establish. The argument is therefore circular:
it is not induction at all, but a restatement of the conclusion as a hypothesis.

In weak induction the hypothesis must be fixed at a single value: one assumes $P(k)$ for one arbitrary
but fixed $k$, and proves $P(k+1)$ from it. Quantifying the hypothesis over all $n$ turns the proof
into "if the theorem is true, then the theorem is true."

**Correction.** The claim is true and the algebra is sound; only the hypothesis statement needs repair.
The inductive step should read:

> *Induction hypothesis:* Let $k\ge1$ be arbitrary and assume $2^k\ge k+1$.
>
> *Inductive step:* Then $2^{k+1}=2\cdot2^k\ge2(k+1)=2k+2\ge k+2$, since $k\ge0$. Hence
> $2^{k+1}\ge(k+1)+1$.

With the base case $n=1$ ($2\ge2$) and this corrected hypothesis, the proof is valid.

*Marks: 30 / 30*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-20 |

**Feedback:**
All seven problems complete and correct, with weak/strong induction declared and every proof carrying
a labelled base case, hypothesis, step, and conclusion.

- **A1:** Both summation identities proved with the algebra shown fully; the factorisation in (a) and
  the perfect square in (b) are handled cleanly.
- **B1:** The divisibility step extracts $8^k=7m+1$ correctly, and the inequality in (b) justifies
  $k+1>2$ explicitly.
- **C1:** Values correct, closed form $3^n+2$ correctly conjectured via the shift $a_n-2$, and proved.
- **D1:** Strong induction handles the composite case by applying the hypothesis to a proper factor.
- **D2:** All three base cases $6,7,8$ present; the step correctly invokes $m=k-2\ge6$.
- **E1:** Base-case failure, falsity of the claim, and the insufficiency of a valid conditional step are
  all identified.
- **E2:** The circular "for all $n$" hypothesis is pinpointed and the repair to a fixed $k$ is given.
