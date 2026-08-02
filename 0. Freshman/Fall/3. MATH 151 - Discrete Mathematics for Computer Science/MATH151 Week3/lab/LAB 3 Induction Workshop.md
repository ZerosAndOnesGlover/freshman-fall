# MATH 151 · Discrete Mathematics for Computer Science
## Lab 3 — Induction Workshop: Writing, Debugging, and Verifying Proofs
### Wednesday, Week 3 | Duration: 2 hours

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

Write complete proofs. Use the template from the resources folder. Label every section.

---

### Exercise 2.1 — Summation

Prove by weak induction:

$$\sum_{i=0}^{n} 2^i = 2^{n+1} - 1 \quad \text{for all } n \geq 0$$

Show every line of algebra in the inductive step. Identify exactly where the IH is applied.

---

### Exercise 2.2 — Inequality

Prove by weak induction:

$$2^n \geq n + 1 \quad \text{for all } n \geq 1$$

*After the proof:* Check whether your IH statement is of the form "for some fixed k" (correct) or "for all n" (wrong). See PS3 Problem E2.

---

### Exercise 2.3 — Divisibility

Prove by weak induction:

$$6 \mid (n^3 + 5n) \quad \text{for all } n \geq 0$$

*Hint:* $n^3 + 5n = n^3 - n + 6n = (n-1)n(n+1) + 6n$. The product of three consecutive integers is divisible by 6.

---

### Exercise 2.4 — Recursive Sequence

The sequence $\{b_n\}$ is defined by $b_1 = 2$, $b_n = 2b_{n-1} + 3$ for $n \geq 2$.

**(a)** Compute $b_1$ through $b_5$.

**(b)** Conjecture a closed form. *(Hint: compute $b_n + c$ for some constant $c$ to make the recurrence homogeneous.)*

**(c)** Prove your conjecture by weak induction.

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

### Bug 3.4

**Claim:** For all $n \geq 1$, $5 \mid (4^n + 6^n)$.

**"Proof":**
*Base case* ($n = 1$): $4 + 6 = 10 = 5 \cdot 2$. ✓

*Inductive step:* Assume $5 \mid (4^k + 6^k)$.

$$4^{k+1} + 6^{k+1} = 4 \cdot 4^k + 6 \cdot 6^k$$

Hmm, I want to use the fact that $4^k + 6^k \equiv 0 \pmod{5}$, i.e., $6^k \equiv -4^k \pmod{5}$.

$$= 4 \cdot 4^k + 6 \cdot 6^k = 4 \cdot 4^k + 6(-4^k) + 6 \cdot 4^k \cdot \text{[something]}$$

I can't make this work. Let me try differently:

$$4^{k+1} + 6^{k+1} = 4(4^k + 6^k) + (6-4) \cdot 6^k = 4(4^k + 6^k) + 2 \cdot 6^k$$

By IH, $5 \mid 4(4^k + 6^k)$. But $5 \mid 2 \cdot 6^k$? Not obviously. The proof is stuck. ✓(?)

**The student got stuck. Is the claim true or false? If true, find and write a correct proof. If false, find a counterexample.**

---

## Section 4 — Python: Induction Verifier Extension (15 min)

Extend `predicate_tools.py` with an induction checker.

```python
def check_induction(base_cases, predicate, n_max):
    """
    Verifies:
    1. All base cases hold.
    2. For each k from max(base_cases) to n_max-1:
       if predicate(k) then predicate(k+1).
    3. Reports the first failure at either stage.
    
    Args:
        base_cases: list of integers (e.g. [0] or [1, 2])
        predicate: function int -> bool
        n_max: check up to this value
    
    Returns: dict with keys 'base_ok', 'step_ok', 'first_failure', 'message'
    """
    # Check base cases
    for b in base_cases:
        if not predicate(b):
            return {
                'base_ok': False,
                'step_ok': None,
                'first_failure': b,
                'message': f"BASE CASE FAILS at n={b}"
            }
    
    # Check inductive step
    start = max(base_cases)
    for k in range(start, n_max):
        if predicate(k) and not predicate(k + 1):
            return {
                'base_ok': True,
                'step_ok': False,
                'first_failure': k,
                'message': f"INDUCTIVE STEP FAILS: P({k}) is True but P({k+1}) is False"
            }
    
    return {
        'base_ok': True,
        'step_ok': True,
        'first_failure': None,
        'message': f"Both base case(s) and inductive step verified for n up to {n_max}"
    }
```

**Task:** Add to `predicate_tools.py`. Test on:

```python
# Test 1: Gauss's formula (should pass)
gauss = lambda n: sum(range(1, n+1)) == n*(n+1)//2
print(check_induction([1], gauss, 100))

# Test 2: 2^n > n^2 with base n=1 (should fail inductive step early)
exp_gt_sq = lambda n: 2**n > n**2
print(check_induction([1], exp_gt_sq, 20))

# Test 3: 2^n > n^2 with base n=5 (should pass from n=5 onward)
print(check_induction([5], exp_gt_sq, 50))

# Test 4: False claim n^2+n is odd (base case should fail)
odd_claim = lambda n: (n**2 + n) % 2 == 1
print(check_induction([1], odd_claim, 20))

# Test 5: 7 | (8^n - 1)
div7 = lambda n: (8**n - 1) % 7 == 0
print(check_induction([0], div7, 30))
```

For each test, interpret the output: what does the tool tell you about the claim?

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

*Save `predicate_tools.py` with the new function — it will be extended in Lab 4.*
