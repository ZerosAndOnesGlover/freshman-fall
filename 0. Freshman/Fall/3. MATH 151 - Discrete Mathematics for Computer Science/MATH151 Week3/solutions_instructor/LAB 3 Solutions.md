# MATH 151 · Week 3
## LAB3 Solutions — INSTRUCTOR ONLY

---

## Section 1 Solutions

### Exercise 1.1 — Verify or Refute

**(a)** Gauss's formula: **TRUE** for all tested n. Both sides equal n(n+1)/2 for every n ≥ 1.

**(b)** $2^n > n^2$:
- n=1: 2 > 1. **TRUE.**
- n=2: 4 > 4? No — equal, not greater. **FALSE.**
- n=3: 8 > 9? No. **FALSE.**
- n=4: 16 > 16? No — equal again. **FALSE.**
- n=5: 32 > 25. **TRUE.**
- n=6: 64 > 36. **TRUE.** Remains true for all n ≥ 5.

First counterexample (where it fails): n = 2. The claim as stated ("for all n ≥ 1") is FALSE. The correct statement is "for all n ≥ 5."

**(c)** $n^2 - n + 41$ prime:
- TRUE for n = 0 through 40.
- FALSE at n = 41: $41^2 - 41 + 41 = 41^2 = 1681 = 41 \times 41$, not prime.
First counterexample: n = 41.

**(d)** $7 \mid (3^n + 4^n)$:
- n=1: 3+4=7. ✓
- n=2: 9+16=25. 25 mod 7 = 4. FALSE.
First counterexample: n = 2. The claim is FALSE.

**(e)** Every n ≥ 8 expressible as 3a+5b:
- n=8: 3+5=8 ✓. n=9: 3·3=9 ✓. n=10: 5·2=10 ✓. ... TRUE for all n=8 through 30 (and all n ≥ 8).

---

### Exercise 1.2 — Inductive Step Verification

**claim_a (Gauss):** No failures. Inductive step holds for all k tested.

**claim_b ($2^n > n^2$):**
- With predicate defined for all n ≥ 1:
  - P(1) = True (2>1), P(2) = False (4≯4). So the step from k=1 to k+1=2 would require: "P(1) true implies P(2) true" — but P(2) is false. Step FAILS at k=1.
  - P(2) = False, so the step from k=2 is vacuous (False implies anything).
  - P(3) = False, P(4) = False. Steps vacuous.
  - P(5) = True, P(6) = True. Step holds.
  - The inductive step holds from k=5 onward.

**Answer to the question:** Yes, a claim can be true for all large n even when the inductive step fails at small k. Induction from n=1 simply doesn't apply — the starting point is wrong. The correct proof uses base case n=5 and shows the step holds for k ≥ 5.

**claim_c ($n^2-n+41$ prime):**
`verify_inductive_step` will find a failure at k=40: P(40)=True but P(41)=False. So the inductive step fails.

---

## Section 2 Solutions

### Exercise 2.1 — Geometric Sum

**Proof.** By weak mathematical induction on n.

**Base case (n=0):** LHS = $\sum_{i=0}^{0} 2^i = 2^0 = 1$. RHS = $2^{0+1}-1 = 2-1 = 1$. Equal. ✓

**Inductive step:** Let k ≥ 0 be arbitrary.
IH: Assume $\sum_{i=0}^{k} 2^i = 2^{k+1} - 1$.
Goal: Show $\sum_{i=0}^{k+1} 2^i = 2^{k+2} - 1$.

$$\sum_{i=0}^{k+1} 2^i = \left(\sum_{i=0}^{k} 2^i\right) + 2^{k+1} = (2^{k+1}-1) + 2^{k+1} \quad\text{[by IH]}$$
$$= 2\cdot2^{k+1} - 1 = 2^{k+2} - 1$$

This is the formula at $n=k+1$. ✓

By the Principle of Mathematical Induction, $\sum_{i=0}^{n} 2^i = 2^{n+1}-1$ for all $n \geq 0$. ∎

---

### Exercise 2.2 — Inequality $2^n \geq n+1$

**Proof.** By weak mathematical induction on n.

**Base case (n=1):** $2^1 = 2 \geq 2 = 1+1$. ✓

**Inductive step:** Let k ≥ 1 be a **fixed, specific** integer.
IH: Assume $2^k \geq k+1$. [Note: this is for the specific k, not for all n.]
Goal: Show $2^{k+1} \geq (k+1)+1 = k+2$.

$$2^{k+1} = 2\cdot2^k \geq 2(k+1) = 2k+2 \geq k+2 \quad\text{[by IH; and }2k+2\geq k+2\text{ since }k\geq1\text{]}$$

Therefore $2^{k+1} \geq k+2$. ✓

By the Principle of Mathematical Induction, $2^n \geq n+1$ for all $n \geq 1$. ∎

*Note on IH statement:* The IH says "assume $2^k \geq k+1$" for a fixed k, NOT "assume $2^n \geq n+1$ for all n ≥ 1." The latter assumes the entire conclusion and is circular (see E2 in PS3).

---

### Exercise 2.3 — Divisibility: $6 \mid (n^3 + 5n)$

**Proof.** By weak mathematical induction on n.

**Base case (n=0):** $0^3 + 5(0) = 0 = 6\cdot0$. So $6 \mid 0$. ✓

**Inductive step:** Let k ≥ 0. Assume $6 \mid (k^3 + 5k)$, i.e., $k^3 + 5k = 6m$ for some $m\in\mathbb{Z}$.

$$(k+1)^3 + 5(k+1) = k^3 + 3k^2 + 3k + 1 + 5k + 5$$
$$= (k^3 + 5k) + 3k^2 + 3k + 6$$
$$= 6m + 3k(k+1) + 6 \quad\text{[by IH]}$$

Since k and k+1 are consecutive integers, one is even, so $k(k+1) = 2t$ for some $t\in\mathbb{Z}$.

$$= 6m + 3(2t) + 6 = 6m + 6t + 6 = 6(m+t+1)$$

Since $m+t+1\in\mathbb{Z}$, $6\mid((k+1)^3+5(k+1))$. ✓ ∎

---

### Exercise 2.4 — Recursive Sequence $b_1=2$, $b_n=2b_{n-1}+3$

**(a)** $b_1=2$, $b_2=2(2)+3=7$, $b_3=2(7)+3=17$, $b_4=2(17)+3=37$, $b_5=2(37)+3=77$.

**(b)** Pattern: 2, 7, 17, 37, 77. Differences: 5, 10, 20, 40 — doubling. Consider $b_n + 3$: values are 5, 10, 20, 40, 80. These are $5\cdot2^{n-1}$. So $b_n = 5\cdot2^{n-1} - 3$.

**Verify:** $b_1 = 5\cdot1-3=2$ ✓. $b_2 = 5\cdot2-3=7$ ✓. $b_3=5\cdot4-3=17$ ✓.

**(c) Proof.**

**Base case** ($n=1$): $5\cdot2^0-3=5-3=2=b_1$. ✓

**IH:** Assume $b_k = 5\cdot2^{k-1}-3$.

$$b_{k+1} = 2b_k+3 = 2(5\cdot2^{k-1}-3)+3 = 5\cdot2^k - 6 + 3 = 5\cdot2^k - 3$$ ✓ ∎

---

### Exercise 2.5 — Prime Factorization (Strong Induction)

**Proof.** By strong mathematical induction on n.

**Base case** ($n=2$): 2 is prime, so $2$ itself is a prime factorization (single factor). ✓

**Inductive step:** Let k ≥ 2. Assume every integer m with $2 \leq m \leq k$ is either prime or a product of primes. [Strong IH]

Consider k+1.

*Case 1: k+1 is prime.* Then k+1 is already a prime factorization. ✓

*Case 2: k+1 is composite.* Then $k+1 = ab$ for integers $a, b$ with $2 \leq a \leq b < k+1$.

Since $2 \leq a \leq k$ and $2 \leq b \leq k$, the Strong IH applies to both.

By IH, $a = p_1p_2\cdots p_r$ and $b = q_1q_2\cdots q_s$ for primes $p_i, q_j$.

Therefore $k+1 = ab = p_1p_2\cdots p_r q_1q_2\cdots q_s$, a product of primes. ✓

By strong induction, every integer $n \geq 2$ is prime or a product of primes. ∎

---

## Section 3 — Bug Solutions

### Bug 3.1

**Error:** The base case is missing entirely. The student proves only the inductive step.

Without a base case, the induction gives: "IF the formula holds for some starting k, THEN it holds for k+1, k+2, …" But we never establish that it holds anywhere. The implication chain has no anchor.

**The claim IS true** (Gauss's formula). The fix: add base case n=1: LHS = 1, RHS = 1(2)/2 = 1. ✓

Additionally: the proof starts "from the right side" (RHS of P(k+1)) and arrives at the LHS. This is valid if done carefully (showing equality), but many graders prefer starting from LHS. Accept either direction if logically sound.

---

### Bug 3.2

**The proof appears correct — check the algebra carefully.**

$(k+1)^3 - (k+1) = k^3 + 3k^2 + 3k + 1 - k - 1 = k^3 + 3k^2 + 2k$.

Then $k^3 + 3k^2 + 2k = (k^3-k) + 3k^2 + 3k = (k^3-k) + 3k(k+1)$.

By IH, $3\mid(k^3-k)$. Also $3\mid 3k(k+1)$. Therefore $3\mid((k+1)^3-(k+1))$.

The proof is actually **CORRECT**. The student used a slightly different algebraic path from the solution above, but both are valid.

The "subtle error" question here is a trick — sometimes a proof has no error. Award full marks for students who verify the algebra is correct and state the proof is valid.

*If assigning as a trick problem, note this explicitly in grading.*

---

### Bug 3.3

**Multiple errors:**

**Error 1 (fatal — base case):** The student computes n=1: $1+1=2$, which is even. Acknowledges the claim seems false. The base case FAILS. The claim is false.

**Error 2 (conceptual — using failed base case):** The student proceeds with the inductive step even though the base case fails. Without a true base case, induction proves nothing.

**Error 3 (the inductive step is valid for the wrong reasons):** The step shows "odd + even = odd," which is a valid inference. If P(k) were true (k²+k is odd), then P(k+1) would be true. But P(k) is never true — k²+k = k(k+1) is always even (product of consecutive integers). So the IH is always false, and the step is vacuously true without being useful.

**The claim is FALSE.** $n^2+n = n(n+1)$ is always even for any integer n (consecutive integers always include one even). So the formula is never odd.

**Full explanation:** The proof has a valid inductive step for a false premise. This is analogous to the horse paradox at the level of the IH — the hypothesis is never actually true, making the implication vacuously true. The conclusion "by induction, the claim holds" is invalid because no base case was established.

---

### Bug 3.4

**Is $5 \mid (4^n + 6^n)$?**

n=1: 4+6=10. $5\mid10$. ✓
n=2: 16+36=52. $52/5=10.4$. $5\nmid52$. FALSE.

The claim is **FALSE**. Counterexample: n=2.

**Why the student got stuck:** The approach $4^{k+1}+6^{k+1} = 4(4^k+6^k)+2\cdot6^k$ gives $5\mid4(4^k+6^k)$ by IH, but $5\nmid2\cdot6^k$ in general ($6^k \equiv 1^k = 1 \pmod{5}$, so $2\cdot6^k\equiv2\pmod5$). The inductive step cannot be completed because the claim is false.

**Correct analysis:** $4\equiv-1\pmod5$ and $6\equiv1\pmod5$. So $4^n+6^n \equiv (-1)^n + 1^n \pmod5$. For odd n: $(-1)+1=0\equiv0\pmod5$ — divisible. For even n: $1+1=2\pmod5$ — not divisible. So the claim holds only for odd n, not all n.

---

## Section 4 — Python Expected Outputs

```
check_induction([1], gauss, 100):
  {'base_ok': True, 'step_ok': True, 'first_failure': None,
   'message': 'Both base case(s) and inductive step verified for n up to 100'}

check_induction([1], exp_gt_sq, 20):
  {'base_ok': True, 'step_ok': False, 'first_failure': 1,
   'message': 'INDUCTIVE STEP FAILS: P(1) is True but P(2) is False'}
  (P(1): 2>1 True; P(2): 4>4 False)

check_induction([5], exp_gt_sq, 50):
  {'base_ok': True, 'step_ok': True, 'first_failure': None,
   'message': 'Both base case(s) and inductive step verified for n up to 50'}

check_induction([1], odd_claim, 20):
  {'base_ok': False, 'step_ok': None, 'first_failure': 1,
   'message': 'BASE CASE FAILS at n=1'}
  (1²+1=2, which is even, not odd)

check_induction([0], div7, 30):
  {'base_ok': True, 'step_ok': True, 'first_failure': None,
   'message': 'Both base case(s) and inductive step verified for n up to 30'}
```

**Interpretations:**

- Test 1: Gauss's formula is confirmed — both base case and step hold up to n=100. This strongly suggests (but does not prove) the formula is correct. The induction proof completes the argument.

- Test 2: With base n=1, the claim $2^n > n^2$ fails at the inductive step from n=1 to n=2. This means we cannot prove the claim starting from n=1.

- Test 3: Starting from n=5, both base case and step hold up to n=50. This is consistent with the correct theorem: $2^n > n^2$ for all $n \geq 5$.

- Test 4: The base case fails at n=1 (1²+1=2 is even). The tool correctly reports this without checking the inductive step. The claim $n^2+n$ is odd is false — we need not proceed.

- Test 5: $7\mid(8^n-1)$ holds for all n=0..30, with both base case and step verified. Ready to write the induction proof.
