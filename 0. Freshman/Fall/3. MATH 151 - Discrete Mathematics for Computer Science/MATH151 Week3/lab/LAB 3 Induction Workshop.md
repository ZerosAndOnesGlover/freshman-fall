# MATH 151 · Discrete Mathematics for Computer Science
## Lab 3 — Induction Workshop: Writing, Debugging, and Verifying Proofs
### Wednesday 21 October 2026, 15:00–16:50 · Week 4 | Duration: 2 hours | Covers Week 3 (all three lectures)

---

**Lab Objectives:**
1. Write complete weak and strong induction proofs from scratch
2. Debug broken induction proofs — identify exactly where and why they fail
3. Computationally verify inductive claims before proving them
4. Distinguish between weak and strong induction needs
5. Connect induction to recursive algorithm correctness

**Materials:** Pencil, paper, laptop with Python 3.

---

## Section 1 — Computational Verification Before Proof (25 min)

Before proving an inductive claim, always verify it computationally for small cases. This catches false conjectures before you waste time on a proof, and builds intuition for the inductive step.

### Exercise 1.1 — Verify or Refute

For each claim, write a Python function that checks it for n = 0 through 30. Report whether it holds for all tested values, and if not, find the smallest counterexample.

```python
def verify_claim(predicate, n_max, start=0):
    """
    Tests predicate(n) for n from start to n_max.
    Returns (True, None) if all pass, or (False, first_n_failing).
    """
    for n in range(start, n_max + 1):
        if not predicate(n):
            return False, n
    return True, None
```

Test each claim:

**(a)** $\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$ for all $n \geq 1$.
```python
def claim_a(n):
    lhs = sum(range(1, n+1))
    rhs = n * (n + 1) // 2
    return lhs == rhs
```

**(b)** $2^n > n^2$ for all $n \geq 1$.
```python
def claim_b(n):
    return 2**n > n**2
```
*(Find the exact range where this holds. What is the smallest n where it first becomes true and stays true?)*

**(c)** $n^2 - n + 41$ is prime for all $n \geq 0$.
```python
def is_prime(k):
    if k < 2: return False
    for i in range(2, int(k**0.5) + 1):
        if k % i == 0: return False
    return True

def claim_c(n):
    return is_prime(n**2 - n + 41)
```

**(d)** $7 \mid (3^n + 4^n)$ for all $n \geq 1$. *(True or false?)*
```python
def claim_d(n):
    return (3**n + 4**n) % 7 == 0
```

**(e)** Every integer $n \geq 8$ can be expressed as $3a + 5b$ for non-negative integers $a, b$.
```python
def claim_e(n):
    for a in range(n // 3 + 1):
        for b in range(n // 5 + 1):
            if 3*a + 5*b == n:
                return True
    return False
```

For each claim: state whether it is true for all tested n, and if false, give the first counterexample with the actual computed value.

---

### Exercise 1.2 — Building the Inductive Step Computationally

The inductive step says: if P(k) holds, then P(k+1) holds. We can verify this computationally for small k.

Write a function that checks: given that P(k) is true, does P(k+1) follow from it?

```python
def verify_inductive_step(predicate, k_max, start=1):
    """
    For each k from start to k_max:
    checks that if predicate(k) is True, then predicate(k+1) is True.
    Reports any k where the implication fails.
    """
    failures = []
    for k in range(start, k_max):
        if predicate(k) and not predicate(k+1):
            failures.append(k)
    return failures
```

Apply this to:
- `claim_a` (sum formula) — should find no failures
- `claim_b` ($2^n > n^2$) — what do you find? Why does the inductive step fail for some k even though the claim eventually becomes true?
- `claim_c` ($n^2 - n + 41$ prime) — find where the inductive step first fails

For claim_b, explain: can a claim be true for all large n even when the inductive step fails at some small k?

---

## Section 2 — Writing Proofs from Scratch (45 min)

*(Revised 2026-09-26: cut from five proofs to three, and from four broken proofs to three, to fit the session.
Section 4 used to return a dict (dictionaries are CS 101 Week 8) and extend `predicate_tools.py`, which Lab 1 no
longer builds; it now returns a tuple. Exercise numbers are unchanged.)*

Write complete proofs. Use the template from the resources folder. Label every section.

---

### Exercise 2.1 — Summation

Prove by weak induction:

$$\sum_{i=0}^{n} 2^i = 2^{n+1} - 1 \quad \text{for all } n \geq 0$$

Show every line of algebra in the inductive step. Identify exactly where the IH is applied.

---

### Exercise 2.3 — Divisibility

Prove by weak induction:

$$6 \mid (n^3 + 5n) \quad \text{for all } n \geq 0$$

*Hint:* $n^3 + 5n = n^3 - n + 6n = (n-1)n(n+1) + 6n$. The product of three consecutive integers is divisible by 6.

---

### Exercise 2.5 — Strong Induction

Prove by strong induction: every integer $n \geq 2$ is either prime or a product of exactly two or more primes.

*(This restates the prime factorization existence theorem — write a complete, clean proof.)*

---

## Section 3 — Debugging Broken Proofs (30 min)

For each broken proof: (i) identify the precise error, (ii) state whether the claim itself is true or false, (iii) either write a correct proof or produce a counterexample.

---

### Bug 3.1

**Claim:** For all $n \geq 1$, $\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$.

**"Proof":**
*Inductive step:* Assume $\sum_{i=1}^{k} i = \frac{k(k+1)}{2}$.

We want to show $\sum_{i=1}^{k+1} i = \frac{(k+1)(k+2)}{2}$.

Starting from the right side:
$$\frac{(k+1)(k+2)}{2} = \frac{k^2+3k+2}{2} = \frac{k^2+k}{2} + \frac{2k+2}{2} = \frac{k(k+1)}{2} + (k+1)$$

By IH, $\frac{k(k+1)}{2} = \sum_{i=1}^{k} i$. Therefore:
$$\frac{(k+1)(k+2)}{2} = \sum_{i=1}^{k} i + (k+1) = \sum_{i=1}^{k+1} i. \quad ✓$$

*Base case:* ...*(student ran out of time and didn't write the base case)*. ∎

**What is wrong?**

---

### Bug 3.2

**Claim:** For all $n \geq 0$, $3 \mid (n^3 - n)$.

**"Proof":**
*Base case* ($n = 0$): $0^3 - 0 = 0 = 3 \cdot 0$. ✓

*Inductive step:* Assume $3 \mid (k^3 - k)$. We show $3 \mid ((k+1)^3 - (k+1))$.

$$(k+1)^3 - (k+1) = k^3 + 3k^2 + 3k + 1 - k - 1 = k^3 + 3k^2 + 2k$$

By IH, $3 \mid (k^3 - k)$, i.e., $k^3 - k = 3m$, so $k^3 = 3m + k$.

Substituting: $k^3 + 3k^2 + 2k = (3m + k) + 3k^2 + 2k = 3m + 3k^2 + 3k = 3(m + k^2 + k)$.

Since $m + k^2 + k \in \mathbb{Z}$, we have $3 \mid ((k+1)^3 - (k+1))$. ✓ ∎

**Find the error.** *(Hint: the error is subtle — check the algebra.)*

---

### Bug 3.3

**Claim:** For all $n \geq 1$, $n^2 + n$ is odd.

**"Proof":**
*Base case* ($n = 1$): $1 + 1 = 2$... hmm, 2 is even. But let's try $n = 3$: $9 + 3 = 12$. Still even. The claim seems false, but let me try to make the induction work anyway.

*Inductive step:* Assume $k^2 + k$ is odd.

$(k+1)^2 + (k+1) = k^2 + 2k + 1 + k + 1 = (k^2 + k) + 2k + 2 = (k^2 + k) + 2(k+1)$.

Since $2(k+1)$ is even and we assumed $k^2 + k$ is odd, odd + even = odd. ✓

So the inductive step works! Therefore by induction, $n^2 + n$ is odd for all $n \geq 1$. ∎

**Identify all errors and explain fully what has gone wrong.**

---

## Section 4 — Python: An Induction Checker (15 min)

Add this function to the same file as Exercise 1.1. It returns a **tuple**, as CS 101 Lecture 10 §4.2 does
for multiple return values: `(base_ok, step_ok, first_failure)`.

```python
def check_induction(base, predicate, n_max):
    """Check the base case, then 'P(k) implies P(k+1)' for k = base .. n_max - 1.
    Returns (base_ok, step_ok, first_failure); first_failure is None if nothing failed."""
    if not predicate(base):
        return False, None, base
    for k in range(base, n_max):
        if predicate(k) and not predicate(k + 1):
            return True, False, k
    return True, True, None
```

Test it:

```python
gauss = lambda n: sum(range(1, n + 1)) == n * (n + 1) // 2
print(check_induction(1, gauss, 100))

exp_gt_sq = lambda n: 2**n > n**2
print(check_induction(1, exp_gt_sq, 20))
print(check_induction(5, exp_gt_sq, 50))

odd_claim = lambda n: (n**2 + n) % 2 == 1
print(check_induction(1, odd_claim, 20))
```

For each test, say what the tuple tells you about the claim. Why can a finite check like this support an
induction proof but never replace it?

---

## Checkoff Criteria

Show your TA:

- [ ] Exercise 1.1: all five claims verified/refuted with correct output
- [ ] Exercise 1.2: `verify_inductive_step` run on claim_b with explanation of why step fails for small k
- [ ] Exercise 2.1: complete proof of geometric sum with base case and IH labeled
- [ ] Exercise 2.3: complete divisibility proof
- [ ] Bug 3.1: error identified and correct proof written
- [ ] Bug 3.3: all errors identified and explained (this one has multiple)
- [ ] Section 4: `check_induction` function running, Test 1 and Test 4 output interpreted

---

