# MATH 151 — Week 3
## Quiz 3 Solutions — INSTRUCTOR ONLY

---

### Problem 1 — Direct Proof (5 points)

**Claim:** If $a \mid b$ and $a \mid c$, then $a \mid (2b + 3c)$.

**Proof.**
Assume $a \mid b$ and $a \mid c$.
By definition of divisibility, there exist integers $j$ and $k$ such that $b = ja$ and $c = ka$.
Then:
$$2b + 3c = 2(ja) + 3(ka) = (2j + 3k)a$$
Since $2j + 3k \in \mathbb{Z}$, we have $a \mid (2b + 3c)$. ∎

*Grading: 1 pt for assuming a|b and a|c. 1 pt for writing b=ja, c=ka. 2 pts for correct algebra. 1 pt for conclusion citing definition.*

---

### Problem 2 — Proof by Contrapositive (5 points)

**Claim:** If $n^2$ is even then $n$ is even.

**Contrapositive:** If $n$ is odd then $n^2$ is odd.

**Proof.**
We prove the contrapositive: if $n$ is odd, then $n^2$ is odd.

Assume $n$ is odd. By definition, $n = 2k+1$ for some $k \in \mathbb{Z}$.
Then:
$$n^2 = (2k+1)^2 = 4k^2 + 4k + 1 = 2(2k^2 + 2k) + 1$$
Since $2k^2 + 2k \in \mathbb{Z}$, $n^2$ is odd.

Therefore, by contrapositive, if $n^2$ is even then $n$ is even. ∎

*Grading: 1 pt for stating contrapositive. 1 pt for assuming n odd → n = 2k+1. 2 pts for correct algebra showing n² = 2(…)+1. 1 pt for conclusion invoking contrapositive.*

---

### Problem 3 — Proof by Contradiction (5 points)

**Claim:** $\sqrt{5}$ is irrational.

**Proof.**
Suppose, for contradiction, that $\sqrt{5}$ is rational.
Then $\sqrt{5} = p/q$ for integers $p$, $q$ with $q \neq 0$ and $\gcd(p,q) = 1$.
Squaring: $5 = p^2/q^2$, so $p^2 = 5q^2$.

Thus $5 \mid p^2$. Since 5 is prime and $5 \mid p^2$, we have $5 \mid p$.
Write $p = 5m$ for some integer $m$.

Substituting: $(5m)^2 = 5q^2$, so $25m^2 = 5q^2$, so $q^2 = 5m^2$.
Thus $5 \mid q^2$, so $5 \mid q$.

Both $5 \mid p$ and $5 \mid q$ contradict $\gcd(p,q) = 1$.
Therefore $\sqrt{5}$ is irrational. ∎

*Grading: 1 pt for contradiction assumption with lowest terms. 1 pt for p²=5q² and concluding 5|p. 1 pt for substituting p=5m and concluding 5|q. 1 pt for identifying the contradiction. 1 pt for conclusion.*

---

### Problem 4 — Error Detection (5 points)

**The error is in Case r = 2:**

The student writes: "we can conclude $n^2 = 4(4q^2+4q+1)$, and since $4q^2+4q+1$ is odd, $n^2$ is divisible by 4 but not 8. Therefore $4 \nmid n^2$."

This is **wrong**. The computation shows $n^2 = 4(4q^2+4q+1)$, which means $4 \mid n^2$ — directly contradicting the claim that $4 \nmid n^2$. The student then makes a false deduction: "$n^2$ is divisible by 4 but not 8, therefore $4 \nmid n^2$." Being divisible by 4 but not by 8 does NOT mean $4 \nmid n^2$ — it means exactly $4 \mid n^2$.

**The claim is FALSE.**

Counterexample: $n = 2$. Then $4 \nmid 2$, but $n^2 = 4$, and $4 \mid 4$. So $4 \mid n^2$ but $4 \nmid n$.

The correct statement (which is provable) is: if $4 \mid n^2$, then $2 \mid n$ (n is even). But $4 \mid n^2$ does NOT imply $4 \mid n$.

*Grading: 2 pts for quoting the exact problematic sentence in Case r=2. 2 pts for correct explanation of why it's wrong (showed 4|n² then claimed 4∤n²). 1 pt for correctly stating the claim is FALSE with counterexample n=2.*

*Common student error: saying "the base case is missing" — this is not what is asked; the problem says "exactly one error" and the base case is not shown (but the error is in Case 2).*

---

### Grade Distribution

| Score | Interpretation |
|---|---|
| 18–20 | Mastered direct, contrapositive, contradiction |
| 14–17 | Good foundation; review algebra precision |
| 10–13 | Re-read Lectures 2.1–2.3; redo PS2 |
| < 10 | Schedule office hours before Week 4 |
