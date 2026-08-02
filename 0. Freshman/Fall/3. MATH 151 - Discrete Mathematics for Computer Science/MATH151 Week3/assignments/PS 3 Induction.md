# MATH 151 · Discrete Mathematics for Computer Science
## Problem Set 3 — Mathematical Induction
### Released: Friday, Week 3 | Due: Friday, Week 4 (11:59 PM)

---

**Instructions:**
- Every induction proof must include: (1) a clearly labeled base case, (2) a clearly stated induction hypothesis, (3) a clearly labeled inductive step, (4) a conclusion sentence.
- State at the outset whether you are using weak or strong induction.
- Show all algebra. Do not skip steps.
- Write in complete mathematical prose.
- Submit as a single PDF.

**Scoring:** 100 points total.

---

## Part A — Weak Induction: Summation Formulas (24 points)

**A1.** (4 pts each) Prove each formula by weak induction.

**(a)** For all $n \geq 1$:
$$\sum_{i=1}^{n} i(i+1) = \frac{n(n+1)(n+2)}{3}$$

**(b)** For all $n \geq 0$:
$$\sum_{i=0}^{n} 3^i = \frac{3^{n+1} - 1}{2}$$

**(c)** For all $n \geq 1$:
$$\sum_{i=1}^{n} \frac{1}{i(i+1)} = \frac{n}{n+1}$$

**(d)** For all $n \geq 1$:
$$\left(\sum_{i=1}^{n} i\right)^2 = \sum_{i=1}^{n} i^3$$

*(Hint: You may use the formula $\sum_{i=1}^{n} i = n(n+1)/2$ without proof, and $\sum_{i=1}^{n} i^3 = [n(n+1)/2]^2$ is what you are proving — so express everything carefully.)*

**(e)** For all $n \geq 1$:
$$\prod_{i=1}^{n} \left(1 - \frac{1}{(i+1)^2}\right) = \frac{n+2}{2(n+1)}$$

**(f)** For all $n \geq 1$:
$$\sum_{i=1}^{n} \frac{i}{2^i} = 2 - \frac{n+2}{2^n}$$

---

## Part B — Weak Induction: Inequalities and Divisibility (24 points)

**B1.** (4 pts each) Prove by weak induction.

**(a)** For all $n \geq 1$: $3^n \geq 2n + 1$.

**(b)** For all $n \geq 0$: $7 \mid (8^n - 1)$.

**(c)** For all $n \geq 1$: $n! \geq 2^{n-1}$.

**(d)** For all $n \geq 4$: $n! > 2^n$.

**(e)** For all $n \geq 1$: $(1 + x)^n \geq 1 + nx$ for any fixed $x \geq -1$. (Bernoulli's Inequality)

**(f)** For all $n \geq 0$: $9 \mid (4^n + 6n - 1)$.

---

## Part C — Weak Induction: Recursive Sequences and Algorithms (16 points)

**C1.** (6 pts) Let the sequence $\{a_n\}$ be defined by $a_1 = 5$ and $a_n = 3a_{n-1} - 4$ for $n \geq 2$.

**(a)** Compute $a_1, a_2, a_3, a_4$.
**(b)** Conjecture a closed-form formula for $a_n$.
**(c)** Prove your conjecture by weak induction.

---

**C2.** (6 pts) Prove by induction that the following recursive algorithm correctly computes $\sum_{i=1}^{n} i^2$:

```python
def sum_of_squares(n):
    if n == 0:
        return 0
    else:
        return sum_of_squares(n - 1) + n * n
```

**Claim:** `sum_of_squares(n)` returns $\frac{n(n+1)(2n+1)}{6}$ for all $n \geq 0$.

---

**C3.** (4 pts) The Towers of Hanoi puzzle with n disks requires a minimum of $2^n - 1$ moves. Prove this by induction.

The recursive structure: to move n disks from peg A to peg C (using peg B as auxiliary):
1. Move n−1 disks from A to B: requires $T(n-1)$ moves.
2. Move the largest disk from A to C: 1 move.
3. Move n−1 disks from B to C: requires $T(n-1)$ moves.

So $T(n) = 2T(n-1) + 1$ with $T(0) = 0$.

Prove: $T(n) = 2^n - 1$ for all $n \geq 0$.

---

## Part D — Strong Induction (24 points)

**D1.** (6 pts) Prove by strong induction: every integer $n \geq 2$ has a prime divisor.

*(This is slightly different from prime factorization — prove just that at least one prime divides n.)*

---

**D2.** (6 pts) The sequence $\{L_n\}$ (Lucas numbers) is defined by $L_1 = 1$, $L_2 = 3$, and $L_n = L_{n-1} + L_{n-2}$ for $n \geq 3$.

**(a)** Compute $L_1$ through $L_6$.
**(b)** Prove by strong induction: $L_n < 2^n$ for all $n \geq 1$.

---

**D3.** (6 pts) Prove by strong induction: every integer $n \geq 6$ can be expressed as $n = 3a + 4b$ for some non-negative integers $a$ and $b$.

*Hint:* Base cases are $n = 6, 7, 8$. For the inductive step, consider $n - 3$.

---

**D4.** (6 pts) Prove by strong induction that the following recursive algorithm correctly computes $\lfloor \log_2 n \rfloor$ (the floor of the base-2 logarithm) for all $n \geq 1$:

```python
def floor_log2(n):
    if n == 1:
        return 0
    else:
        return 1 + floor_log2(n // 2)
```

**Claim:** `floor_log2(n)` returns $\lfloor \log_2 n \rfloor$ for all $n \geq 1$.

*Hint:* For $n \geq 2$, note that $n // 2 = \lfloor n/2 \rfloor$ and $1 \leq \lfloor n/2 \rfloor < n$. Use the identity $\lfloor \log_2 n \rfloor = 1 + \lfloor \log_2 \lfloor n/2 \rfloor \rfloor$.*

---

## Part E — Proof Analysis and Error Detection (12 points)

**E1.** (4 pts) The following is a "proof" by induction of a false statement. Identify every error precisely.

**False Claim:** For all $n \geq 1$, $\sum_{i=1}^{n} i = \frac{n^2 + n + 2}{2}$.

**"Proof":**
*Base case* ($n = 1$): $\sum_{i=1}^{1} i = 1$. The formula gives $\frac{1 + 1 + 2}{2} = 2$. Close enough — the formula is approximately right. ✓

*Inductive step*: Assume $\sum_{i=1}^{k} i = \frac{k^2+k+2}{2}$.
Then:
$$\sum_{i=1}^{k+1} i = \frac{k^2+k+2}{2} + (k+1) = \frac{k^2+k+2 + 2k+2}{2} = \frac{k^2+3k+4}{2} = \frac{(k+1)^2+(k+1)+2}{2}$$
This equals the formula at $n = k+1$. ✓

Therefore, by induction, the formula holds for all $n \geq 1$. ∎

---

**E2.** (4 pts) The following induction proof has a subtle structural error. Find it.

**Claim:** For all $n \geq 1$, $2^n \geq n + 1$.

**"Proof":**
*Base case* ($n = 1$): $2^1 = 2 \geq 2 = 1 + 1$. ✓

*Inductive step*: Assume $2^n \geq n + 1$ for all $n \geq 1$ (i.e., assume P(n) is true for all n). We show $2^{n+1} \geq n + 2$.
$$2^{n+1} = 2 \cdot 2^n \geq 2(n+1) = 2n + 2 \geq n + 2$$
since $n \geq 0$. ✓

Therefore, for all $n \geq 1$, $2^n \geq n+1$. ∎

*(Hint: The claim is actually TRUE and the algebra is correct — so what is the structural error in how the IH is stated?)*

---

**E3.** (4 pts) Determine whether the following claim is true or false. If true, prove it. If false, find the smallest counterexample and explain why induction would fail.

**Claim:** For all $n \geq 0$, $n^2 - n + 41$ is prime.

---

## Bonus (8 points — optional)

**Bonus 1.** (4 pts) Prove by induction: for all $n \geq 1$,
$$\sum_{i=1}^{n} \frac{1}{\sqrt{i}} \geq \sqrt{n}$$

*(Hint: For the inductive step, you need to show $\sqrt{k} + \frac{1}{\sqrt{k+1}} \geq \sqrt{k+1}$. Manipulate this carefully — multiply through by $\sqrt{k+1}$ and use the AM-GM inequality or direct algebra.)*

**Bonus 2.** (4 pts) A **tiling** of a $2^n \times 2^n$ chessboard (with one square removed) by L-shaped trominoes (pieces covering 3 squares in an L-shape) is always possible for any $n \geq 1$ regardless of which square is removed.

Prove this by induction on $n$.

*Hint:* For the inductive step, divide the $2^{k+1} \times 2^{k+1}$ board into four $2^k \times 2^k$ quadrants. Place one tromino at the center covering one square from each of the three quadrants that do NOT contain the removed square. Then apply the IH to each quadrant.*
