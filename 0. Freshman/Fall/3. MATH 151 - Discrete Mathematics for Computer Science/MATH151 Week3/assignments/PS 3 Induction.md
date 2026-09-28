# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 3 — Mathematical Induction
### Released: Friday 16 October 2026, 14:00 (after the Friday lecture) | Due: Friday 23 October 2026, 17:00 (Week 4)

---

**Instructions:**
- Every induction proof must include: (1) a clearly labeled base case, (2) a clearly stated induction hypothesis, (3) a clearly labeled inductive step, (4) a conclusion sentence.
- State at the outset whether you are using weak or strong induction.
- Show all algebra. Do not skip steps.
- Write in complete mathematical prose.
- Submit as a single PDF.

**Expected time:** about 3 hours. **Scoring:** 100 points total.

---

## Part A — Weak Induction: Summation Formulas (14 points)

**A1.** (14 pts) Prove each formula by weak induction.

**(a)** For all $n \geq 1$:
$$\sum_{i=1}^{n} i(i+1) = \frac{n(n+1)(n+2)}{3}$$

**(b)** For all $n \geq 1$:
$$\sum_{i=1}^{n} \frac{1}{i(i+1)} = \frac{n}{n+1}$$

---

## Part B — Weak Induction: Inequalities and Divisibility (16 points)

**B1.** (16 pts) Prove by weak induction.

**(a)** For all $n \geq 0$: $7 \mid (8^n - 1)$.

**(b)** For all $n \geq 4$: $n! > 2^n$.

---

## Part C — Weak Induction: Recursive Sequences and Algorithms (14 points)

**C1.** (14 pts) Let the sequence $\{a_n\}$ be defined by $a_1 = 5$ and $a_n = 3a_{n-1} - 4$ for $n \geq 2$.

**(a)** Compute $a_1, a_2, a_3, a_4$.
**(b)** Conjecture a closed-form formula for $a_n$.
**(c)** Prove your conjecture by weak induction.

---

## Part D — Strong Induction (26 points)

**D1.** (12 pts) Prove by strong induction: every integer $n \geq 2$ has a prime divisor.

*(This is slightly different from prime factorization — prove just that at least one prime divides n.)*

---

**D2.** (14 pts) Prove by strong induction: every integer $n \geq 6$ can be expressed as $n = 3a + 4b$ for some non-negative integers $a$ and $b$.

*Hint:* Base cases are $n = 6, 7, 8$. For the inductive step, consider $n - 3$.

---

## Part E — Proof Analysis and Error Detection (30 points)

**E1.** (14 pts) The following is a "proof" by induction of a false statement. Identify every error precisely.

**False Claim:** For all $n \geq 1$, $\sum_{i=1}^{n} i = \frac{n^2 + n + 2}{2}$.

**"Proof":**
*Base case* ($n = 1$): $\sum_{i=1}^{1} i = 1$. The formula gives $\frac{1 + 1 + 2}{2} = 2$. Close enough — the formula is approximately right. ✓

*Inductive step*: Assume $\sum_{i=1}^{k} i = \frac{k^2+k+2}{2}$.
Then:
$$\sum_{i=1}^{k+1} i = \frac{k^2+k+2}{2} + (k+1) = \frac{k^2+k+2 + 2k+2}{2} = \frac{k^2+3k+4}{2} = \frac{(k+1)^2+(k+1)+2}{2}$$
This equals the formula at $n = k+1$. ✓

Therefore, by induction, the formula holds for all $n \geq 1$. ∎

---

**E2.** (16 pts) The following induction proof has a subtle structural error. Find it.

**Claim:** For all $n \geq 1$, $2^n \geq n + 1$.

**"Proof":**
*Base case* ($n = 1$): $2^1 = 2 \geq 2 = 1 + 1$. ✓

*Inductive step*: Assume $2^n \geq n + 1$ for all $n \geq 1$ (i.e., assume P(n) is true for all n). We show $2^{n+1} \geq n + 2$.
$$2^{n+1} = 2 \cdot 2^n \geq 2(n+1) = 2n + 2 \geq n + 2$$
since $n \geq 0$. ✓

Therefore, for all $n \geq 1$, $2^n \geq n+1$. ∎

*(Hint: The claim is actually TRUE and the algebra is correct — so what is the structural error in how the IH is stated?)*

---
