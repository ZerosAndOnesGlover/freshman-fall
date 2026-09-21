# MATH 151 · Week 3
## PS3 Solutions — INSTRUCTOR ONLY

---

## Part A — Summation Formulas

### A1(a): $\sum_{i=1}^{n} i(i+1) = \frac{n(n+1)(n+2)}{3}$

**Base case** ($n=1$): LHS = $1 \cdot 2 = 2$. RHS = $\frac{1\cdot2\cdot3}{3} = 2$. ✓

**IH:** Assume $\sum_{i=1}^{k} i(i+1) = \frac{k(k+1)(k+2)}{3}$.

**Step:**
$$\sum_{i=1}^{k+1} i(i+1) = \frac{k(k+1)(k+2)}{3} + (k+1)(k+2)$$
$$= (k+1)(k+2)\left(\frac{k}{3} + 1\right) = (k+1)(k+2)\cdot\frac{k+3}{3} = \frac{(k+1)(k+2)(k+3)}{3}$$

This is $\frac{(k+1)((k+1)+1)((k+1)+2)}{3}$. ✓ ∎

---

### A1(b): $\sum_{i=0}^{n} 3^i = \frac{3^{n+1}-1}{2}$

**Base case** ($n=0$): LHS = $3^0 = 1$. RHS = $\frac{3-1}{2} = 1$. ✓

**IH:** Assume $\sum_{i=0}^{k} 3^i = \frac{3^{k+1}-1}{2}$.

**Step:**
$$\sum_{i=0}^{k+1} 3^i = \frac{3^{k+1}-1}{2} + 3^{k+1} = \frac{3^{k+1}-1 + 2\cdot3^{k+1}}{2} = \frac{3\cdot3^{k+1}-1}{2} = \frac{3^{k+2}-1}{2}$$ ✓ ∎

---

### A1(c): $\sum_{i=1}^{n} \frac{1}{i(i+1)} = \frac{n}{n+1}$

**Base case** ($n=1$): LHS = $\frac{1}{1\cdot2} = \frac{1}{2}$. RHS = $\frac{1}{2}$. ✓

**IH:** Assume $\sum_{i=1}^{k} \frac{1}{i(i+1)} = \frac{k}{k+1}$.

**Step:**
$$\sum_{i=1}^{k+1} \frac{1}{i(i+1)} = \frac{k}{k+1} + \frac{1}{(k+1)(k+2)} = \frac{k(k+2) + 1}{(k+1)(k+2)} = \frac{k^2+2k+1}{(k+1)(k+2)} = \frac{(k+1)^2}{(k+1)(k+2)} = \frac{k+1}{k+2}$$ ✓ ∎

---

### A1(d): $\left(\sum_{i=1}^{n} i\right)^2 = \sum_{i=1}^{n} i^3$

We prove this equals $\left[\frac{n(n+1)}{2}\right]^2$.

**Base case** ($n=1$): LHS = $(1)^2 = 1$. RHS = $1^3 = 1$. ✓

**IH:** Assume $\sum_{i=1}^{k} i^3 = \left[\frac{k(k+1)}{2}\right]^2$.

**Step:**
$$\sum_{i=1}^{k+1} i^3 = \left[\frac{k(k+1)}{2}\right]^2 + (k+1)^3 = (k+1)^2\left[\frac{k^2}{4} + (k+1)\right]$$
$$= (k+1)^2 \cdot \frac{k^2 + 4k + 4}{4} = (k+1)^2 \cdot \frac{(k+2)^2}{4} = \left[\frac{(k+1)(k+2)}{2}\right]^2$$ ✓ ∎

---

### A1(e): $\prod_{i=1}^{n}\left(1 - \frac{1}{(i+1)^2}\right) = \frac{n+2}{2(n+1)}$

**Base case** ($n=1$): LHS = $1 - \frac{1}{4} = \frac{3}{4}$. RHS = $\frac{3}{2\cdot2} = \frac{3}{4}$. ✓

**IH:** Assume $\prod_{i=1}^{k}\left(1-\frac{1}{(i+1)^2}\right) = \frac{k+2}{2(k+1)}$.

**Step:**
$$\prod_{i=1}^{k+1}\left(1-\frac{1}{(i+1)^2}\right) = \frac{k+2}{2(k+1)} \cdot \left(1 - \frac{1}{(k+2)^2}\right)$$
$$= \frac{k+2}{2(k+1)} \cdot \frac{(k+2)^2-1}{(k+2)^2} = \frac{k+2}{2(k+1)} \cdot \frac{(k+1)(k+3)}{(k+2)^2}$$
$$= \frac{(k+3)}{2(k+2)} = \frac{(k+1)+2}{2((k+1)+1)}$$ ✓ ∎

---

### A1(f): $\sum_{i=1}^{n} \frac{i}{2^i} = 2 - \frac{n+2}{2^n}$

**Base case** ($n=1$): LHS = $\frac{1}{2}$. RHS = $2 - \frac{3}{2} = \frac{1}{2}$. ✓

**IH:** Assume $\sum_{i=1}^{k} \frac{i}{2^i} = 2 - \frac{k+2}{2^k}$.

**Step:**
$$\sum_{i=1}^{k+1} \frac{i}{2^i} = 2 - \frac{k+2}{2^k} + \frac{k+1}{2^{k+1}}$$
$$= 2 + \frac{-(k+2)\cdot2 + (k+1)}{2^{k+1}} = 2 + \frac{-2k-4+k+1}{2^{k+1}} = 2 + \frac{-k-3}{2^{k+1}} = 2 - \frac{k+3}{2^{k+1}}$$

This equals $2 - \frac{(k+1)+2}{2^{k+1}}$. ✓ ∎

---

## Part B — Inequalities and Divisibility

### B1(a): $3^n \geq 2n+1$ for $n \geq 1$

**Base case** ($n=1$): $3 \geq 3$. ✓

**IH:** Assume $3^k \geq 2k+1$.

$$3^{k+1} = 3\cdot3^k \geq 3(2k+1) = 6k+3 \geq 2k+3 = 2(k+1)+1$$

The last inequality: $6k+3 \geq 2k+3$ iff $4k \geq 0$, true for $k \geq 1$. ✓ ∎

---

### B1(b): $7 \mid (8^n - 1)$

**Base case** ($n=0$): $8^0-1=0=7\cdot0$. ✓

**IH:** Assume $7 \mid (8^k-1)$, i.e., $8^k = 7m+1$.

$$8^{k+1}-1 = 8\cdot8^k - 1 = 8(7m+1)-1 = 56m+7 = 7(8m+1)$$

Since $8m+1\in\mathbb{Z}$, $7\mid(8^{k+1}-1)$. ✓ ∎

---

### B1(c): $n! \geq 2^{n-1}$

**Base case** ($n=1$): $1! = 1 \geq 1 = 2^0$. ✓

**IH:** Assume $k! \geq 2^{k-1}$.

$(k+1)! = (k+1)\cdot k! \geq (k+1)\cdot2^{k-1} \geq 2\cdot2^{k-1} = 2^k$

since $k+1 \geq 2$ for $k \geq 1$. ✓ ∎

---

### B1(d): $n! > 2^n$ for $n \geq 4$

**Base case** ($n=4$): $4! = 24 > 16 = 2^4$. ✓

**IH:** Assume $k! > 2^k$ for some $k \geq 4$.

$(k+1)! = (k+1)\cdot k! > (k+1)\cdot2^k > 2\cdot2^k = 2^{k+1}$

since $k+1 \geq 5 > 2$. ✓ ∎

---

### B1(e): Bernoulli's Inequality — proved in Lecture 10, see that solution.

---

### B1(f): $9 \mid (4^n + 6n - 1)$

**Base case** ($n=0$): $4^0 + 0 - 1 = 0 = 9\cdot0$. ✓

**IH:** Assume $9 \mid (4^k + 6k - 1)$, so $4^k + 6k - 1 = 9m$.

$$4^{k+1} + 6(k+1) - 1 = 4\cdot4^k + 6k + 5$$
$$= 4(9m - 6k + 1) + 6k + 5 \quad\text{[from IH: }4^k = 9m - 6k + 1\text{]}$$
$$= 36m - 24k + 4 + 6k + 5 = 36m - 18k + 9 = 9(4m - 2k + 1)$$

Since $4m-2k+1\in\mathbb{Z}$, $9\mid(4^{k+1}+6(k+1)-1)$. ✓ ∎

---

## Part C — Recursive Sequences and Algorithms

### C1: $a_1 = 5$, $a_n = 3a_{n-1} - 4$

**(a)** $a_1=5$, $a_2=3(5)-4=11$, $a_3=3(11)-4=29$, $a_4=3(29)-4=83$.

**(b)** Notice $a_n - 2 = 3(a_{n-1}-2)$ (check: $a_n-2 = 3a_{n-1}-6 = 3(a_{n-1}-2)$). So $a_n - 2$ is a geometric sequence with ratio 3 and first term $a_1-2=3$. Thus $a_n - 2 = 3\cdot3^{n-1} = 3^n$, giving **$a_n = 3^n + 2$**.

**Verify:** $a_1=3+2=5$ ✓, $a_2=9+2=11$ ✓, $a_3=27+2=29$ ✓, $a_4=81+2=83$ ✓.

**(c) Proof by induction.**

**Base case** ($n=1$): $a_1 = 5 = 3^1+2$. ✓

**IH:** Assume $a_k = 3^k + 2$.

$$a_{k+1} = 3a_k - 4 = 3(3^k+2) - 4 = 3^{k+1} + 6 - 4 = 3^{k+1}+2$$ ✓ ∎

---

### C2: sum_of_squares correctness

**Claim:** `sum_of_squares(n)` returns $\frac{n(n+1)(2n+1)}{6}$ for all $n \geq 0$.

**Proof** by induction on $n$.

**Base case** ($n=0$): `sum_of_squares(0)` returns $0 = \frac{0\cdot1\cdot1}{6}$. ✓

**IH:** Assume `sum_of_squares(k)` returns $\frac{k(k+1)(2k+1)}{6}$.

`sum_of_squares(k+1)` executes the else branch, computing `sum_of_squares(k) + (k+1)*(k+1)`.

By IH, `sum_of_squares(k)` returns $\frac{k(k+1)(2k+1)}{6}$.

So `sum_of_squares(k+1)` returns:
$$\frac{k(k+1)(2k+1)}{6} + (k+1)^2 = (k+1)\left[\frac{k(2k+1)}{6} + (k+1)\right]$$
$$= (k+1)\cdot\frac{k(2k+1)+6(k+1)}{6} = (k+1)\cdot\frac{2k^2+7k+6}{6} = (k+1)\cdot\frac{(k+2)(2k+3)}{6}$$
$$= \frac{(k+1)(k+2)(2k+3)}{6} = \frac{(k+1)((k+1)+1)(2(k+1)+1)}{6}$$ ✓ ∎

---

### C3: Towers of Hanoi — $T(n) = 2^n - 1$

**Proof** by induction.

**Base case** ($n=0$): $T(0) = 0 = 2^0-1 = 0$. ✓

**IH:** Assume $T(k) = 2^k - 1$.

$$T(k+1) = 2T(k) + 1 = 2(2^k-1)+1 = 2^{k+1}-2+1 = 2^{k+1}-1$$ ✓ ∎

---

## Part D — Strong Induction

### D1: Every $n \geq 2$ has a prime divisor.

**Proof** by strong induction.

**Base case** ($n=2$): 2 is prime and $2\mid2$. ✓

**IH:** Assume every integer $m$ with $2\leq m\leq k$ has a prime divisor.

Consider $k+1$.

*Case 1:* $k+1$ is prime. Then $k+1\mid k+1$, so $k+1$ is its own prime divisor. ✓

*Case 2:* $k+1$ is composite. Then $k+1=ab$ for integers $a,b$ with $2\leq a < k+1$. By IH applied to $a$ (since $2\leq a\leq k$), $a$ has a prime divisor $p$. Then $p\mid a$ and $a\mid(k+1)$, so $p\mid(k+1)$. ✓

By strong induction, every $n\geq2$ has a prime divisor. ∎

---

### D2: $L_n < 2^n$

**(a)** $L_1=1, L_2=3, L_3=4, L_4=7, L_5=11, L_6=18$.

**(b) Proof** by strong induction.

**Base cases:**
- $n=1$: $L_1=1<2=2^1$. ✓
- $n=2$: $L_2=3<4=2^2$. ✓

**IH:** Assume $L_m < 2^m$ for all $m$ with $1\leq m\leq k$, where $k\geq2$.

$$L_{k+1} = L_k + L_{k-1} < 2^k + 2^{k-1} = 2^{k-1}(2+1) = 3\cdot2^{k-1} < 4\cdot2^{k-1} = 2^{k+1}$$ ✓ ∎

---

### D3: Every $n\geq6$ is $3a+4b$

**Base cases:**
- $n=6$: $6=3(2)+4(0)$. ✓
- $n=7$: $7=3(1)+4(1)$. ✓
- $n=8$: $8=3(0)+4(2)$. ✓

**IH:** Assume every integer $m$ with $6\leq m\leq k$ (for $k\geq8$) can be expressed as $3a+4b$.

Consider $k+1$. Since $k\geq8$, $k+1-3=k-2\geq6$. By IH applied to $m=k-2$: $k-2=3a+4b$ for some $a,b\geq0$.

Then $k+1 = (k-2)+3 = 3a+4b+3 = 3(a+1)+4b$, with $a+1\geq1\geq0$. ✓ ∎

---

### D4: floor_log2 correctness

**Claim:** `floor_log2(n)` returns $\lfloor\log_2 n\rfloor$ for all $n\geq1$.

**Proof** by strong induction on $n$.

**Base case** ($n=1$): `floor_log2(1)` returns $0 = \lfloor\log_2 1\rfloor$. ✓

**IH:** Assume `floor_log2(m)` returns $\lfloor\log_2 m\rfloor$ for all $m$ with $1\leq m\leq k$.

Consider `floor_log2(k+1)`. Since $k+1\geq2$, the else branch executes with `n//2` $= \lfloor(k+1)/2\rfloor$.

Let $m = \lfloor(k+1)/2\rfloor$. Since $k+1\geq2$: $m = \lfloor(k+1)/2\rfloor \geq1$ and $m \leq k$ (since $(k+1)/2 < k+1$ for $k\geq1$, and $m\leq k$).

By IH, `floor_log2(m)` returns $\lfloor\log_2 m\rfloor$.

The function returns $1 + \lfloor\log_2 m\rfloor = 1 + \lfloor\log_2\lfloor(k+1)/2\rfloor\rfloor$.

We must verify this equals $\lfloor\log_2(k+1)\rfloor$.

For any $n\geq2$: $\lfloor\log_2 n\rfloor = 1 + \lfloor\log_2\lfloor n/2\rfloor\rfloor$.

**Proof of this identity:** Let $n\geq2$ and write $2^j\leq n < 2^{j+1}$ (so $\lfloor\log_2 n\rfloor = j$). Then $2^{j-1}\leq n/2 < 2^j$, so $\lfloor\log_2(n/2)\rfloor = j-1$. Since $\lfloor\log_2\lfloor n/2\rfloor\rfloor = \lfloor\log_2(n/2)\rfloor$ (this follows from floor properties, acceptable to cite), $\lfloor\log_2 n\rfloor = j = 1+(j-1) = 1+\lfloor\log_2\lfloor n/2\rfloor\rfloor$. ✓

Therefore `floor_log2(k+1)` returns $\lfloor\log_2(k+1)\rfloor$. ✓ ∎

---

## Part E — Proof Analysis

### E1: Errors in the false claim

**Error 1 (fatal):** The base case fails. The student computes $\frac{1+1+2}{2}=2\neq1$ and explicitly acknowledges this, then says "close enough." A false base case means the entire induction collapses — the theorem is not established.

**Error 2 (conceptual):** The correct value is $\sum_{i=1}^{1}i=1$, not 2. The formula is wrong.

**What this illustrates:** A valid inductive step for a false formula is entirely possible. The inductive step proves: IF the formula holds for $k$, THEN it holds for $k+1$. If it doesn't hold for the base case, this conditional is vacuously useless — it never fires. The step and base case together are both required. The formula $\frac{n^2+n+2}{2}$ is exactly 1 more than the correct formula $\frac{n^2+n}{2} = \frac{n(n+1)}{2}$; the inductive step preserves this constant error, which is why the step "works" — but the formula is wrong throughout.

---

### E2: Structural error in IH statement

**The error:** The IH is stated as "assume $2^n \geq n+1$ for **all** $n \geq 1$." This is circular — it assumes the entire conclusion for all $n$ simultaneously, then derives it for $n+1$. In standard weak induction, the IH must be stated for a **fixed, specific k**: "assume $2^k \geq k+1$ for some specific $k \geq 1$."

**The claim is TRUE** and the algebra is correct. The proof can be repaired by replacing the IH statement:

*Correct IH:* "Let $k \geq 1$ be arbitrary. Assume $2^k \geq k+1$."

This is a standard error where a student writes "for all n" in the IH instead of "for a fixed k." It is circular reasoning disguised as induction.

---

### E3: $n^2 - n + 41$

**Claim is FALSE.**

The formula produces primes for $n = 0, 1, 2, \ldots, 40$, but:

$n = 41$: $41^2 - 41 + 41 = 41^2 = 1681$, which is not prime ($1681 = 41^2$).

Also $n = 40$: $40^2 - 40 + 41 = 1600 - 40 + 41 = 1601$. Is 1601 prime? $\sqrt{1601}\approx40$. Check divisibility by primes up to 40: not divisible by 2,3,5,7,11,13,17,19,23,29,31,37. Yes, 1601 is prime. So the first counterexample is $n=41$.

**Why induction would fail:** If you attempted to prove "P(k) → P(k+1)" where P(n) = "$n^2-n+41$ is prime," you would immediately find that P(41) is false. The inductive step would fail because P(40) is true but P(41) is false — the implication P(40)→P(41) is F.
