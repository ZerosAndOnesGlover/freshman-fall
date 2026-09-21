# MATH 151 · Discrete Mathematics for Computer Science
## Quiz 3 — Proof Techniques
### Administered: Monday 12 October 2026, 13:00–13:15 (first 15 minutes of class) · Week 3

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

---

**Instructions:** Closed notes. 15 minutes. Write complete proofs in mathematical prose.

**Total: 20 points**

---

### Problem 1 (5 points)

Prove **directly**: if $a \mid b$ and $a \mid c$, then $a \mid (2b + 3c)$.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

### Problem 2 (5 points)

Prove **by contrapositive**: for any integer $n$, if $n^2$ is even then $n$ is even.

State the contrapositive explicitly before proving it.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

### Problem 3 (5 points)

Prove **by contradiction**: $\sqrt{5}$ is irrational.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

---

### Problem 4 (5 points)

The following proof contains **exactly one error**. Identify the error precisely (quote the problematic line) and explain why it is wrong. Then state whether the claim is actually true or false.

**Claim:** If $n$ is an integer and $n^2$ is divisible by 4, then $n$ is divisible by 4.

**"Proof" by contrapositive:** We prove: if $n$ is not divisible by 4, then $n^2$ is not divisible by 4.

Assume $4 \nmid n$. By the division algorithm, $n = 4q + r$ for $r \in \{1, 2, 3\}$.

*Case $r = 1$:* $n^2 = (4q+1)^2 = 16q^2 + 8q + 1 = 4(4q^2+2q) + 1$. So $4 \nmid n^2$. ✓

*Case $r = 2$:* $n^2 = (4q+2)^2 = 16q^2 + 16q + 4 = 4(4q^2 + 4q + 1)$. Since $4q^2+4q+1$ is odd, $n^2$ is divisible by 4 but not by 8, so $4 \nmid n^2$. ✓

*Case $r = 3$:* $n^2 = (4q+3)^2 = 16q^2 + 24q + 9 = 4(4q^2+6q+2)+1$. So $4 \nmid n^2$. ✓

In all cases $4 \nmid n^2$, so by contrapositive the claim holds. ∎

**Error:**

&nbsp;

&nbsp;

&nbsp;

**Is the original claim true or false?**

&nbsp;

---

*End of Quiz 3*
