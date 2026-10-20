---
assessment: Lab 2
course: MATH 151
component: Labs
possible: 100
score: 100
status: graded
started: 2026-10-19
submitted: 2026-10-19
graded: 2026-10-19
source: "LAB 2 Proof Workshop.md"
---

# MATH 151 · Lab 2
## Answer Sheet

**Assessment:** `LAB 2 Proof Workshop.md`
**Points available:** 100 (graded on completion and effort)

> Write your answers under each heading. When you are done, set `status: submitted` in the
> frontmatter above.

---

## Section 1 — Technique Identification

**(1.1)** $6\mid n\Rightarrow 3\mid n$.
- $P$: "$6\mid n$"; $Q$: "$3\mid n$".
- Contrapositive: if $3\nmid n$, then $6\nmid n$.
- Contradiction assumption: $6\mid n$ and $3\nmid n$.
- **Direct.** From $n=6k$ we get $n=3(2k)$ in one line; the other techniques only add work.

**(1.2)** $5\mid n^2\Rightarrow 5\mid n$.
- $P$: "$5\mid n^2$"; $Q$: "$5\mid n$".
- Contrapositive: if $5\nmid n$, then $5\nmid n^2$.
- Contradiction assumption: $5\mid n^2$ and $5\nmid n$.
- **Contrapositive.** Assuming $5\nmid n$ gives the concrete form $n=5q+r$ with $r\in\{1,2,3,4\}$,
  which can be squared directly; assuming $5\mid n^2$ gives only $n^2=5k$, which is hard to use.

**(1.3)** $a+b$ odd $\Rightarrow$ exactly one of $a,b$ is even.
- $P$: "$a+b$ is odd"; $Q$: "exactly one of $a,b$ is even".
- Contrapositive: if $a$ and $b$ have the same parity, then $a+b$ is even.
- Contradiction assumption: $a+b$ is odd and ($a,b$ both even or $a,b$ both odd).
- **Contrapositive.** The negation of $Q$ splits cleanly into the two parity cases; the direct
  hypothesis "$a+b$ is odd" is hard to decompose without already knowing the parities.

**(1.4)** $\sqrt{11}$ is irrational.
- Not an implication; the claim is $C$: "$\sqrt{11}\notin\mathbb{Q}$".
- Contrapositive: not applicable (there is no $P\to Q$ to contrapose).
- Contradiction assumption: $\sqrt{11}=p/q$ in lowest terms.
- **Contradiction.** The standard irrationality argument has no implication to contrapose; assuming a
  lowest-terms fraction is exactly what creates the usable equation $p^2=11q^2$.

**(1.5)** $xy>0\Rightarrow$ ($x,y$ both positive or both negative).
- $P$: "$xy>0$"; $Q$: "$x,y$ have the same sign".
- Contrapositive: if $x$ and $y$ do not have the same sign, then $xy\le0$.
- Contradiction assumption: $xy>0$ and $x,y$ do not have the same sign.
- **Contrapositive.** The negation of $Q$ (opposite signs, or one of them zero) makes the sign of
  $xy$ immediate; from $xy>0$ alone the case analysis is awkward.

**(1.6)** $4\mid(n^2-1)\Rightarrow n$ is odd.
- $P$: "$4\mid(n^2-1)$"; $Q$: "$n$ is odd".
- Contrapositive: if $n$ is even, then $4\nmid(n^2-1)$.
- Contradiction assumption: $4\mid(n^2-1)$ and $n$ is even.
- **Contrapositive.** With $n=2k$ we get $n^2-1=4k^2-1\equiv3\pmod4$ at once.

**(1.7)** No integer $n<10$ satisfies $n\equiv2\pmod4$ and $n\equiv0\pmod6$, except $n=6$.
- This is not a universal implication; it is a claim about the finitely many integers $n<10$.
- Contrapositive: not a single implication, so a single contrapositive does not apply.
- Contradiction assumption: $n<10$ satisfies both congruences and $n\neq6$.
- **Direct exhaustive check.** There are only ten cases; imposing one congruence leaves a short list
  to test against the other. (This is a finite claim, not a generic $P\to Q$.)

---

## Section 2 — Proof Writing from Scratch

### Exercise 2.1 — Direct Proofs

**(a)** *Claim.* If $n$ is odd, then $8\mid(n^2-1)$.

**Proof (direct).** Assume $n$ is odd, so $n=2k+1$ for some $k\in\mathbb{Z}$. Then
$$n^2-1=(2k+1)^2-1=4k^2+4k=4k(k+1).$$
The integers $k$ and $k+1$ are consecutive, so one of them is even; hence $k(k+1)=2m$ for some
$m\in\mathbb{Z}$. Therefore
$$n^2-1=4\cdot2m=8m,$$
and since $m\in\mathbb{Z}$, $8\mid(n^2-1)$. $\square$

**(b)** *Claim.* The sum of any three consecutive integers is divisible by $3$.

**Proof (direct).** Let the integers be $n,n+1,n+2$ with $n\in\mathbb{Z}$. Their sum is
$$n+(n+1)+(n+2)=3n+3=3(n+1).$$
Since $n+1\in\mathbb{Z}$, the sum is divisible by $3$. $\square$

**(c)** *Claim.* If $a\mid b$, then $a\mid(b^2-b)$.

**Proof (direct).** Assume $a\mid b$, so $b=ka$ for some $k\in\mathbb{Z}$. Then
$$b^2-b=b(b-1)=(ka)(ka-1)=a\big(k(ka-1)\big).$$
Since $k(ka-1)\in\mathbb{Z}$, we conclude $a\mid(b^2-b)$. $\square$

### Exercise 2.2 — Contrapositive Proofs

**(a)** *Claim.* For any integer $n$, if $n^2-1$ is even, then $n$ is odd.

**Contrapositive:** if $n$ is even, then $n^2-1$ is odd.

**Proof (contrapositive).** Assume $n$ is even, so $n=2k$. Then
$$n^2-1=4k^2-1=4k^2-2+1=2(2k^2-1)+1.$$
Since $2k^2-1\in\mathbb{Z}$, $n^2-1$ is odd. By contrapositive, if $n^2-1$ is even then $n$ is odd.
$\square$

**(b)** *Claim.* For any integers $a,b$, if $a^2+b^2$ is odd, then $a+b$ is odd.

**Contrapositive:** if $a+b$ is even, then $a^2+b^2$ is even.

**Proof (contrapositive).** Assume $a+b$ is even. Then $a$ and $b$ have the same parity.

- *Case 1: both even.* Write $a=2j$, $b=2k$. Then
  $$a^2+b^2=4j^2+4k^2=2(2j^2+2k^2),$$
  which is even.
- *Case 2: both odd.* Write $a=2j+1$, $b=2k+1$. Then
  $$a^2+b^2=(4j^2+4j+1)+(4k^2+4k+1)=2(2j^2+2j+2k^2+2k+1),$$
  which is even.

In both cases $a^2+b^2$ is even. By contrapositive, if $a^2+b^2$ is odd then $a+b$ is odd. $\square$

### Exercise 2.3 — Proof by Contradiction

**(a)** *Claim.* $\sqrt{13}$ is irrational.

**Proof (contradiction).** Suppose $\sqrt{13}=p/q$ in lowest terms, with $p,q\in\mathbb{Z}^+$ and
$\gcd(p,q)=1$. Squaring gives $p^2=13q^2$, so $13\mid p^2$. Since $13$ is prime, $13\mid p$; write
$p=13k$. Then $169k^2=13q^2$, so $q^2=13k^2$, hence $13\mid q^2$ and therefore $13\mid q$. Thus $13$
divides both $p$ and $q$, contradicting $\gcd(p,q)=1$. So $\sqrt{13}$ is irrational. $\square$

**(b)** *Claim.* There is no greatest odd integer.

**Proof (contradiction).** Suppose, for contradiction, that $N$ is the greatest odd integer. Since $N$
is odd, $N=2k+1$ for some $k\in\mathbb{Z}$, so
$$N+2=2k+3=2(k+1)+1$$
is also odd. And $N+2>N$. This contradicts the maximality of $N$ among odd integers. Hence no greatest
odd integer exists. $\square$

---

## Section 3 — Proof Critique and Repair

### Flawed Proof 3.1

**Claim.** If $4\mid n^2$, then $4\mid n$.

**Errors.**
1. "Then $n=2\sqrt{k}$": nothing justifies that $\sqrt{k}$ is an integer — $n^2=4k$ gives $n=2\sqrt{k}$,
   and $\sqrt{k}$ may be irrational.
2. "Thus $n=2m$, which means $4\mid n$": $n=2m$ means only $2\mid n$. The step to $4\mid n$ is the
   conclusion, assumed rather than proved — the argument is circular.

**The claim is false:** $n=2$ gives $n^2=4$ and $4\mid4$, but $4\nmid2$.

**Correct statement.** If $4\mid n^2$, then $n$ is even.

**Proof (contrapositive).** If $n$ is odd, write $n=2k+1$. Then
$$n^2=4k^2+4k+1=4(k^2+k)+1\equiv1\pmod4,$$
so $4\nmid n^2$. By contrapositive, $4\mid n^2$ implies $n$ is even. $\square$

### Flawed Proof 3.2

**Claim.** For any integer $n$, if $n$ is odd, then $n^2+n+1$ is odd.

**Errors.** None. Each step is valid: $n$ odd implies $n^2$ odd; odd $+$ odd $=$ even, so $n^2+n$ is
even; even $+1$ is odd. The proof is **correct and not repairable — it needs no repair.**

### Flawed Proof 3.3

**Claim.** If $a\mid b$ and $b\mid a$, then $a=b$.

**Errors.**
1. "Dividing by $b$" requires $b\neq0$, and the proof never handles $b=0$.
2. From $jk=1$ with $j,k\in\mathbb{Z}$ the proof concludes $j=k=1$, ignoring $j=k=-1$.
3. With $j=k=-1$ we get $b=-a$, so $a=b$ fails in general.

**The claim is false:** $a=3$, $b=-3$ gives $3\mid(-3)$ and $(-3)\mid3$, but $3\neq-3$.

**Corrected claim.** If $a\mid b$ and $b\mid a$, then $a=\pm b$.

**Proof.** Assume $a\mid b$ and $b\mid a$, so $b=ja$ and $a=kb$ for some $j,k\in\mathbb{Z}$.

- If $b=0$, then $a=kb=0$, so $a=b=0$ and $a=\pm b$ holds.
- If $b\neq0$, substitute: $b=j(kb)=jkb$, and dividing by $b$ gives $jk=1$. Since $j,k\in\mathbb{Z}$,
  either $j=k=1$ (so $b=a$) or $j=k=-1$ (so $b=-a$). In both cases $a=\pm b$. $\square$

### Flawed Proof 3.4

**Claim.** For any real $x$, if $x^2=x$, then $x=1$.

**Errors.** "Dividing both sides by $x$" is invalid when $x=0$. The hypothesis $x^2=x$ is satisfied by
$x=0$ as well, so the claim is false.

**Correct proof.** Assume $x^2=x$. Then $x^2-x=0$, so $x(x-1)=0$. By the zero-product property,
$x=0$ or $x=1$. Hence the solutions are $x\in\{0,1\}$. $\square$

### Flawed Proof 3.5

**Claim.** $\sqrt2+\sqrt2=\sqrt4=2$, so $\sqrt2$ is rational.

**What is wrong.** The premise $\sqrt2+\sqrt2=\sqrt4$ is false. In fact $\sqrt2+\sqrt2=2\sqrt2\approx
2.828$, whereas $\sqrt4=2$. The error is treating the square root as if it distributed over addition:
$\sqrt a+\sqrt b\neq\sqrt{a+b}$ whenever $a,b>0$. (It does distribute over multiplication,
$\sqrt a\sqrt b=\sqrt{ab}$, which is what makes the mistake tempting.) So the argument is invalid, and
its conclusion is false as well: $\sqrt2$ is irrational.

---

## Section 4 — Extension: Proof Gallery

**Gallery 1.** *There are infinitely many integers $n$ with $n^2+1$ not prime.*

Work modulo $5$. If $n\equiv2\pmod5$, then $n^2+1\equiv4+1\equiv0\pmod5$, so $5\mid(n^2+1)$. For
$n>2$ we also have $n^2+1>5$, so $n^2+1$ has a divisor $5$ strictly between $1$ and itself, hence is
composite. The integers $n=2,7,12,17,\dots$ (i.e. $n\equiv2\pmod5$) are infinitely many. $\square$

**Gallery 2.** *For any prime $p>2$, $8\mid(p^2-1)$.*

Every prime $p>2$ is odd, so $p=2k+1$. Then
$$p^2-1=(2k+1)^2-1=4k^2+4k=4k(k+1).$$
Since $k$ and $k+1$ are consecutive, one is even: $k(k+1)=2m$. Hence $p^2-1=8m$. $\square$

**Gallery 3.** *$\log_2 6$ is irrational.*

Suppose, for contradiction, that $\log_2 6=p/q$ with $p,q\in\mathbb{Z}^+$. Then $2^{p/q}=6$, so
$2^p=6^q=2^q3^q$, hence $2^{p-q}=3^q$.

- If $p>q$, the left side is a power of $2$ and the right side a power of $3$; by unique
  factorisation both must equal $1$, forcing $q=0$ and therefore $6=1$, a contradiction.
- If $p<q$, then $1=2^{q-p}3^q\ge2$, a contradiction.
- If $p=q$, then $1=3^q$, impossible for $q\ge1$.

All cases contradict, so $\log_2 6$ is irrational. $\square$

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-19 |

**Feedback:**
Completed and checked off. All checkoff items met: Section 1 done for all seven problems with
justification; Exercise 2.1(a) proved with the $k(k+1)$-even step shown; contrapositive proofs for
2.2(a) and 2.2(b) complete; $\sqrt{13}$ irrationality complete; all five flawed proofs critiqued and
repaired, including correctly identifying 3.2 as valid; gallery problems solved.
