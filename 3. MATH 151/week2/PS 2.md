---
assessment: PS 2
course: MATH 151
component: Problem Sets
possible: 100
score: 100
status: graded
started: 2026-10-19
submitted: 2026-10-19
graded: 2026-10-19
source: "PS 2 Proof Techniques.md"
---

# MATH 151 · PS 2
## Answer Sheet

**Assessment:** `PS 2 Proof Techniques.md`
**Points available:** 100

> Write your answers under each heading. Leave the **Marks** lines alone — they are filled
> in during grading. When you are done, set `status: submitted` in the frontmatter above.

---

### Part A — Direct Proof  (36 points)

**Your answer:**

#### A1 (24 points)

**(a)** *Claim.* If $n$ is an odd integer, then $n+1$ is even.

**Proof (direct).** Assume $n$ is odd. By definition, $n=2k+1$ for some $k\in\mathbb{Z}$. Then
$$n+1=(2k+1)+1=2k+2=2(k+1).$$
Since $k+1\in\mathbb{Z}$, $n+1$ is even. $\square$

**(b)** *Claim.* If $a\mid b$ and $a\mid c$, then $a\mid(3b-2c)$.

**Proof (direct).** Assume $a\mid b$ and $a\mid c$. Then $b=ja$ and $c=ka$ for some $j,k\in\mathbb{Z}$.
Hence
$$3b-2c=3(ja)-2(ka)=(3j-2k)a.$$
Since $3j-2k\in\mathbb{Z}$, we have $a\mid(3b-2c)$. $\square$

**(c)** *Claim.* For every integer $n$, $n^2+n$ is even.

**Proof (direct, by cases on the parity of $n$).** Note $n^2+n=n(n+1)$.

- If $n$ is even, then $n=2k$, so $n(n+1)=2k(n+1)=2\big(k(n+1)\big)$, which is even.
- If $n$ is odd, then $n+1$ is even, say $n+1=2k$, so $n(n+1)=n\cdot2k=2(nk)$, which is even.

In both cases $n^2+n$ is even. $\square$

#### A2 (12 points)

**Your answer:**

**The error.** The flawed proof concludes "hence $4\mid n$" from the fact that $n=2m$. But $n=2m$ only
establishes $2\mid n$, not $4\mid n$; the final step assumes the very conclusion it is meant to prove.
The earlier step "then $n^2$ is even, so $n$ is even" is valid, but it is not enough.

**The claim is false.** Take $n=2$: then $n^2=4=4\cdot1$, so $4\mid n^2$, yet $4\nmid2$.

**Correct claim and proof.** The true statement is: if $4\mid n^2$, then $n$ is even (that is, $2\mid n$).

**Proof (contrapositive).** We prove: if $n$ is odd, then $4\nmid n^2$. Assume $n=2k+1$. Then
$$n^2=(2k+1)^2=4k^2+4k+1=4(k^2+k)+1,$$
which leaves remainder $1$ on division by $4$; hence $4\nmid n^2$. By contrapositive, if $4\mid n^2$ then
$n$ is even. $\square$

*Marks: 36 / 36*

---

### Part B — Proof by Contrapositive  (18 points)

**Your answer:**

**(a)** *Claim.* For any integer $n$, if $n^2$ is odd, then $n$ is odd.

**Contrapositive:** if $n$ is even, then $n^2$ is even.

**Proof.** We prove the contrapositive. Assume $n$ is even, so $n=2k$ for some $k\in\mathbb{Z}$. Then
$$n^2=(2k)^2=4k^2=2(2k^2),$$
and $2k^2\in\mathbb{Z}$, so $n^2$ is even. Therefore, by contrapositive, if $n^2$ is odd then $n$ is
odd. $\square$

**(b)** *Claim.* For any real numbers $x$ and $y$, if $x+y$ is irrational, then $x$ is irrational or $y$
is irrational.

**Contrapositive:** if $x$ and $y$ are both rational, then $x+y$ is rational.

**Proof.** We prove the contrapositive. Assume $x,y\in\mathbb{Q}$, so $x=p/q$ and $y=m/n$ with
$p,q,m,n\in\mathbb{Z}$ and $q,n\neq0$. Then
$$x+y=\frac{p}{q}+\frac{m}{n}=\frac{pn+qm}{qn}.$$
Here $pn+qm\in\mathbb{Z}$ and $qn\neq0$, so $x+y\in\mathbb{Q}$. By contrapositive, if $x+y$ is
irrational then at least one of $x,y$ is irrational. $\square$

*Marks: 18 / 18*

---

### Part C — Proof by Contradiction  (32 points)

**Your answer:**

#### C1 (18 points)

**(a)** *Claim.* $\sqrt7$ is irrational.

**Proof (contradiction).** Suppose, for contradiction, that $\sqrt7$ is rational. Write
$\sqrt7=p/q$ with $p,q\in\mathbb{Z}^+$, $q\neq0$, and $\gcd(p,q)=1$ (lowest terms). Squaring gives
$7=p^2/q^2$, so
$$p^2=7q^2.$$
Thus $7\mid p^2$. Since $7$ is prime, it follows that $7\mid p$; write $p=7k$. Then
$49k^2=7q^2$, so $q^2=7k^2$. Hence $7\mid q^2$, and again since $7$ is prime, $7\mid q$. But now $7$
divides both $p$ and $q$, contradicting $\gcd(p,q)=1$. Therefore $\sqrt7$ is irrational. $\square$

**(b)** *Claim.* If $n$ is an integer and $n^2$ is divisible by $5$, then $n$ is divisible by $5$.

**Choice of technique.** I use the **contrapositive** rather than contradiction. The negation of the
claim, "$5\mid n^2$ and $5\nmid n$", does not give a convenient form for $n^2$, whereas assuming
$5\nmid n$ lets us write $n=5q+r$ with $r\in\{1,2,3,4\}$ and compute directly. (The proof could be
recast as a contradiction, but the contrapositive is cleaner.)

**Proof (contrapositive).** We prove: if $5\nmid n$, then $5\nmid n^2$. Assume $5\nmid n$; by the
division algorithm, $n=5q+r$ with $r\in\{1,2,3,4\}$. Then

- $r=1$: $n^2=25q^2+10q+1=5(5q^2+2q)+1\equiv1\pmod 5$;
- $r=2$: $n^2=25q^2+20q+4=5(5q^2+4q)+4\equiv4\pmod 5$;
- $r=3$: $n^2=25q^2+30q+9=5(5q^2+6q+1)+4\equiv4\pmod 5$;
- $r=4$: $n^2=25q^2+40q+16=5(5q^2+8q+3)+1\equiv1\pmod 5$.

In every case $n^2\not\equiv0\pmod 5$, so $5\nmid n^2$. By contrapositive, $5\mid n^2$ implies
$5\mid n$. $\square$

#### C2 (14 points)

**Your answer:**

**Where the proof fails.** From $p=2k$ and $k^2=q^2$ the proof infers $q=k$ (taking $q>0$) and then
computes $\gcd(p,q)=\gcd(2k,k)=k$. This is a contradiction with $\gcd(p,q)=1$ **only when $k>1$**. When
$k=1$ there is no contradiction: then $p=2$ and $q=1$, and $\sqrt4=2/1=2$, which is rational. So the
argument fails exactly at the point where it needs $k>1$ but has not ruled out $k=1$.

**Why the analogous $\sqrt2$ argument has no such problem.** For $\sqrt2$, the argument shows $p$ and
$q$ are both even, so $p=2j$ and $q=2m$ with $j,m$ integers, and $\sqrt2=j/m$ is a representation in
*smaller* terms. That can be repeated forever — an infinite descent — which is impossible for positive
integers. There is no pair $(p,q)$ at which the descent bottoms out. For $\sqrt4$ the descent *does*
bottom out at the valid representation $2/1$, so no contradiction is reached; indeed $\sqrt4$ is
rational. The irrationality proof only works when no finite representation exists.

*Marks: 32 / 32*

---

### Part D — Mixed and Applied  (14 points)

**Your answer:**

**(a)** *Claim.* If $a\mid(b+c)$, then $a\mid b$ or $a\mid c$. — **FALSE.**

**Counterexample:** $a=3$, $b=1$, $c=2$. Then $b+c=3$ and $3\mid3$, but $3\nmid1$ and $3\nmid2$. A
divisor of a sum need not divide either summand.

**(b)** *Claim.* If $a\mid bc$, then $a\mid b$ or $a\mid c$. — **FALSE.**

**Counterexample:** $a=4$, $b=6$, $c=2$. Then $bc=12$ and $4\mid12$, but $4\nmid6$ and $4\nmid2$. The
statement becomes true when $a$ is prime (Euclid's lemma, Week 12): the failure here is that $4$ is
composite and shares a factor with each of $6$ and $2$ without dividing either.

*Marks: 14 / 14*

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 100 / 100 |
| **Percent** | 100% |
| **Graded** | 2026-10-19 |

**Feedback:**
All six problems complete and correct, in mathematical prose.

- **A1:** All three direct proofs valid; the parity cases in (c) are exhaustive, and the key step
  $k(k+1)$ even is justified.
- **A2:** The circular final step is identified precisely, the claim is correctly disproved with
  $n=2$, and the true statement ($4\mid n^2\Rightarrow n$ even) is proved by contrapositive.
- **B1:** Both contrapositives stated before being proved and proved correctly.
- **C1:** $\sqrt7$ irrationality complete; for (b) the technique choice is justified and the four
  residue cases are correct.
- **C2:** The failure at $k=1$ is pinpointed, and the contrast with the infinite descent for $\sqrt2$
  is explained.
- **D1:** Both false statements disproved with explicit counterexamples, with the primality contrast
  noted.
