---
assessment: Quiz 3
course: MATH 151
component: Quizzes
possible: 20
score: 20
status: graded
started: 2026-10-20
submitted: 2026-10-20
graded: 2026-10-20
source: "QUIZ 3 Proof Techniques.md"
---

# MATH 151 · Quiz 3
## Answer Sheet

**Assessment:** `QUIZ 3 Proof Techniques.md`
**Points available:** 20

---

### Problem 1 — Direct Proof (5 points)

*Claim.* If $a\mid b$ and $a\mid c$, then $a\mid(2b+3c)$.

**Proof (direct).** Assume $a\mid b$ and $a\mid c$. By definition of divisibility there exist integers
$j,k$ such that $b=ja$ and $c=ka$. Then
$$2b+3c=2(ja)+3(ka)=(2j+3k)a.$$
Since $2j+3k\in\mathbb{Z}$, this exhibits $2b+3c$ as an integer multiple of $a$, so
$a\mid(2b+3c)$. $\square$

---

### Problem 2 — Proof by Contrapositive (5 points)

*Claim.* For any integer $n$, if $n^2$ is even then $n$ is even.

**Contrapositive.** If $n$ is odd, then $n^2$ is odd.

**Proof (contrapositive).** We prove the contrapositive. Assume $n$ is odd, so $n=2k+1$ for some
$k\in\mathbb{Z}$. Then
$$n^2=(2k+1)^2=4k^2+4k+1=2(2k^2+2k)+1.$$
Since $2k^2+2k\in\mathbb{Z}$, $n^2$ is odd. By contrapositive, if $n^2$ is even then $n$ is even.
$\square$

---

### Problem 3 — Proof by Contradiction (5 points)

*Claim.* $\sqrt5$ is irrational.

**Proof (contradiction).** Suppose, for contradiction, that $\sqrt5$ is rational. Write $\sqrt5=p/q$
with $p,q\in\mathbb{Z}$, $q\neq0$, and $\gcd(p,q)=1$ (lowest terms). Squaring gives
$5=p^2/q^2$, so
$$p^2=5q^2.$$
Thus $5\mid p^2$. Since $5$ is prime, $5\mid p$; write $p=5m$ for some $m\in\mathbb{Z}$. Substituting,
$$(5m)^2=5q^2\implies25m^2=5q^2\implies q^2=5m^2.$$
Hence $5\mid q^2$, and since $5$ is prime, $5\mid q$. But then $5$ divides both $p$ and $q$,
contradicting $\gcd(p,q)=1$. Therefore $\sqrt5$ is irrational. $\square$

---

### Problem 4 — Error Detection (5 points)

**The error** is in the case $r=2$, in the sentence:

> "$n^2=(4q+2)^2=16q^2+16q+4=4(4q^2+4q+1)$. Since $4q^2+4q+1$ is odd, $n^2$ is divisible by $4$ but not
> by $8$, so $4\nmid n^2$."

**Why it is wrong.** The computation $n^2=4(4q^2+4q+1)$ *shows* $4\mid n^2$. The final inference
reverses this: "divisible by $4$ but not by $8$" still means $4\mid n^2$, not $4\nmid n^2$. Being
divisible by $4$ and not by $8$ is entirely compatible with being divisible by $4$. So this case does
not support the contrapositive; in fact it refutes it.

**Is the original claim true or false?** **FALSE.** Counterexample: $n=2$. Then $4\nmid2$, yet
$n^2=4$ and $4\mid4$. The true statement is: if $4\mid n^2$, then $2\mid n$ (that is, $n$ is even), not
that $4\mid n$.

---

## Grading Summary

*Filled in by the grader.*

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-10-20 |

**Feedback:**
All four problems correct. Problem 1 exhibits $2b+3c=(2j+3k)a$ and cites the definition. Problem 2
states the contrapositive explicitly before proving it and produces the required
$2(\,\cdot\,)+1$ form. Problem 3 gives the full lowest-terms argument, including primality of $5$ at both
stages. Problem 4 quotes the exact faulty sentence, explains that the displayed factorisation proves
$4\mid n^2$, and correctly identifies the claim as false with counterexample $n=2$.
