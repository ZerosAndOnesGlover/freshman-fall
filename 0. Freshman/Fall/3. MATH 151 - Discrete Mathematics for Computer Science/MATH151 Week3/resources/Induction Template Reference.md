# MATH 151 · Induction Template Reference
## Week 3: Weak and Strong Mathematical Induction

---

## Weak Induction — Full Template

```
Theorem. P(n) holds for all n ≥ n₀.

Proof. By (weak) mathematical induction on n.

Base case (n = n₀):
  [Compute both sides of P(n₀) explicitly.]
  [Show they are equal / the inequality holds / divisibility holds.]
  Therefore P(n₀) holds. ✓

Inductive step:
  Let k ≥ n₀ be an arbitrary integer.
  Induction Hypothesis: Assume P(k), i.e., [write P(k) explicitly].
  Goal: Prove P(k+1), i.e., [write P(k+1) explicitly].

  [Begin with the expression in P(k+1) that involves a sum/product/recurrence.]
  [Separate it so that P(k) applies to part of it.]
    = [expression involving the P(k) part] + [remaining terms]
    = [apply IH to replace the P(k) part]       [by IH]
    = [algebraic simplification]
    = [right-hand side of P(k+1)]
  
  Therefore P(k+1) holds. ✓

By the Principle of Mathematical Induction, P(n) holds for all n ≥ n₀. ∎
```

---

## Strong Induction — Full Template

```
Theorem. P(n) holds for all n ≥ n₀.

Proof. By strong mathematical induction on n.

Base case(s):
  [Verify P(n₀), P(n₀+1), ..., P(n₀+j) directly.]
  [The number of base cases = the maximum lookback in the inductive step.]

Inductive step:
  Let k ≥ n₀+j be an arbitrary integer.
  Strong Induction Hypothesis: Assume P(m) holds for all m with n₀ ≤ m ≤ k.
  Goal: Prove P(k+1).

  [Express P(k+1) in terms of P(m) for some m ≤ k.]
  [Identify which values of m are needed — verify n₀ ≤ m ≤ k.]
  [Apply the Strong IH to those values of m.]
  [Complete the derivation.]
  
  Therefore P(k+1) holds. ✓

By the Principle of Strong Mathematical Induction, P(n) holds for all n ≥ n₀. ∎
```

---

## Checklist Before Submitting Any Induction Proof

**Base case:**
- [ ] Is the base case at the correct starting value n₀?
- [ ] Did I verify both sides separately and show they are equal (not just write "LHS = RHS" without computing)?
- [ ] Is the base case complete for strong induction (enough base cases for the lookback)?

**Inductive hypothesis:**
- [ ] Is the IH stated for a fixed, arbitrary k (not "for all n")?
- [ ] Did I write out P(k) explicitly (not just "assume the formula works for k")?
- [ ] Did I write out P(k+1) explicitly as a goal?

**Inductive step:**
- [ ] Did I start from P(k+1) and work toward showing it holds?
- [ ] Did I explicitly apply the IH (and label where)?
- [ ] Is every algebraic step correct?
- [ ] For strong induction: did I verify that all values m used in the IH satisfy n₀ ≤ m ≤ k?

**Conclusion:**
- [ ] Did I state "By the Principle of Mathematical Induction, P(n) holds for all n ≥ n₀"?

---

## Common Inductive Step Techniques

### For Summation Claims: $\sum_{i=n_0}^{n} f(i) = g(n)$

```
∑_{i=n₀}^{k+1} f(i) = (∑_{i=n₀}^{k} f(i)) + f(k+1)
                     = g(k) + f(k+1)            [by IH]
                     = [algebra]
                     = g(k+1)
```

### For Product Claims: $\prod_{i=n_0}^{n} f(i) = g(n)$

```
∏_{i=n₀}^{k+1} f(i) = (∏_{i=n₀}^{k} f(i)) · f(k+1)
                     = g(k) · f(k+1)            [by IH]
                     = [algebra]
                     = g(k+1)
```

### For Recurrence Claims: $a_n = [closed form]$

```
a_{k+1} = [recurrence applied]             [definition]
         = [expression in a_k, a_{k-1}, ...]
         = [IH applied]                     [by IH (one or more times)]
         = [algebra]
         = [closed form at k+1]
```

### For Divisibility Claims: $d \mid f(n)$

```
f(k+1) = [express in terms of f(k) and other terms]
        = [f(k)] · [something] + [remaining]
        
Since d | f(k) [IH], we have d | [f(k)] · [something].
[Show d | remaining separately.]
Therefore d | f(k+1).
```

### For Inequality Claims: $f(n) ≥ g(n)$ or $f(n) > g(n)$

```
f(k+1) = [express in terms of f(k)]
        ≥ [or >] [some expression involving f(k)]
        ≥ [or >] [apply IH to replace f(k) with g(k)]   [by IH, since f(k) ≥ g(k)]
        ≥ [or >] g(k+1)                                  [show remaining inequality]
```

*Caution: when multiplying by a quantity, verify its sign. Multiplying by a negative flips the inequality.*

---

## Weak vs Strong Induction Decision Guide

| Ask yourself | If YES → |
|---|---|
| Does P(k+1) depend only on P(k)? | Weak induction |
| Does P(k+1) depend on P(k) AND P(k-1)? | Strong induction, 2 base cases |
| Does the recursive step jump to arbitrary smaller values? | Strong induction |
| Are you proving "every n has some property" where a proof for n uses arbitrary smaller values? | Strong induction |
| Is the recurrence $a_n = f(a_{n-1})$ only? | Weak induction |
| Is the recurrence $a_n = f(a_{n-1}, a_{n-2})$? | Strong induction, 2 base cases |

---

## Named Induction Theorems to Know

| Theorem | Type | Base Cases | IH Used At |
|---|---|---|---|
| $\sum i = n(n+1)/2$ | Weak | n=1 | k |
| $\sum i^2 = n(n+1)(2n+1)/6$ | Weak | n=1 | k |
| $\sum r^i = (r^{n+1}-1)/(r-1)$ | Weak | n=0 | k |
| $2^n > n$ | Weak | n=1 | k |
| $n! \geq 2^{n-1}$ | Weak | n=1 | k |
| $d \mid (a^n - b^n)$ | Weak | n=1 | k |
| Bernoulli: $(1+x)^n \geq 1+nx$ | Weak | n=1 | k |
| $F_n < 2^n$ | Strong | n=1,2 | k and k-1 |
| Every $n \geq 2$ has prime factor | Strong | n=2 | arbitrary m < k+1 |
| Postage: $n = 3a+5b$ for $n \geq 8$ | Strong | n=8,9,10 | k-2 |
