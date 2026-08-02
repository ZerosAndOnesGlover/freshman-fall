# MATH 151 — Common Summation Formulas
## Week 3 Reference Sheet

---

## Standard Closed-Form Summation Formulas

All formulas hold for integers n ≥ 1 unless otherwise noted. All are provable by weak induction.

---

### Arithmetic Sums

| Formula | Closed Form | Notes |
|---|---|---|
| $\displaystyle\sum_{i=1}^{n} 1$ | $n$ | Count |
| $\displaystyle\sum_{i=1}^{n} i$ | $\dfrac{n(n+1)}{2}$ | Gauss's formula |
| $\displaystyle\sum_{i=1}^{n} i^2$ | $\dfrac{n(n+1)(2n+1)}{6}$ | Sum of squares |
| $\displaystyle\sum_{i=1}^{n} i^3$ | $\left[\dfrac{n(n+1)}{2}\right]^2$ | Sum of cubes = (Gauss)² |
| $\displaystyle\sum_{i=1}^{n} (2i-1)$ | $n^2$ | Sum of first n odd numbers |
| $\displaystyle\sum_{i=1}^{n} i(i+1)$ | $\dfrac{n(n+1)(n+2)}{3}$ | |

---

### Geometric Sums

| Formula | Closed Form | Condition |
|---|---|---|
| $\displaystyle\sum_{i=0}^{n} r^i$ | $\dfrac{r^{n+1}-1}{r-1}$ | $r \neq 1$, $n \geq 0$ |
| $\displaystyle\sum_{i=0}^{n} 2^i$ | $2^{n+1} - 1$ | $n \geq 0$ |
| $\displaystyle\sum_{i=0}^{n} 3^i$ | $\dfrac{3^{n+1}-1}{2}$ | $n \geq 0$ |
| $\displaystyle\sum_{i=1}^{n} 2^i$ | $2^{n+1} - 2$ | $n \geq 1$ |

---

### Telescoping Sums

These collapse to a simple expression because consecutive terms cancel:

| Formula | Closed Form | Key Identity Used |
|---|---|---|
| $\displaystyle\sum_{i=1}^{n} \dfrac{1}{i(i+1)}$ | $\dfrac{n}{n+1}$ | $\dfrac{1}{i(i+1)} = \dfrac{1}{i} - \dfrac{1}{i+1}$ |
| $\displaystyle\sum_{i=1}^{n} (a_{i+1} - a_i)$ | $a_{n+1} - a_1$ | General telescoping |
| $\displaystyle\sum_{i=1}^{n} \dfrac{1}{\sqrt{i}+\sqrt{i+1}}$ | $\sqrt{n+1} - 1$ | Rationalize denominator |

**Telescoping technique:** If $f(i) = g(i+1) - g(i)$, then $\sum_{i=1}^{n} f(i) = g(n+1) - g(1)$.

---

### Product Formulas

| Formula | Closed Form | Notes |
|---|---|---|
| $\displaystyle\prod_{i=1}^{n} i$ | $n!$ | Factorial |
| $\displaystyle\prod_{i=2}^{n} \left(1 - \dfrac{1}{i^2}\right)$ | $\dfrac{n+1}{2n}$ | |
| $\displaystyle\prod_{i=1}^{n} \left(1 - \dfrac{1}{(i+1)^2}\right)$ | $\dfrac{n+2}{2(n+1)}$ | |

---

### Useful Inequalities (all provable by induction)

| Inequality | Holds For | Notes |
|---|---|---|
| $2^n > n$ | $n \geq 1$ | |
| $2^n \geq n+1$ | $n \geq 1$ | |
| $2^n > n^2$ | $n \geq 5$ | Fails for $n = 1,2,3,4$ |
| $2^n \geq n^2$ | $n \geq 4$ | |
| $n! > 2^n$ | $n \geq 4$ | |
| $n! \geq 2^{n-1}$ | $n \geq 1$ | |
| $3^n \geq 2n+1$ | $n \geq 1$ | |
| $(1+x)^n \geq 1+nx$ | $n \geq 1$, $x \geq -1$ | Bernoulli |

---

### Divisibility Results (all provable by induction)

| Claim | Holds For |
|---|---|
| $2 \mid n(n+1)$ | $n \geq 0$ |
| $3 \mid n(n+1)(n+2)$ | $n \geq 0$ |
| $6 \mid n(n+1)(n+2)$ | $n \geq 0$ |
| $6 \mid (n^3 - n)$ | $n \geq 0$ |
| $3 \mid (4^n - 1)$ | $n \geq 0$ |
| $7 \mid (8^n - 1)$ | $n \geq 0$ |
| $5 \mid (4^n - 4)$ | $n \geq 1$ |
| $(a-b) \mid (a^n - b^n)$ | $n \geq 1$, $a,b \in \mathbb{Z}$ |

---

## Fibonacci Sequence Reference

$F_1 = 1,\ F_2 = 1,\ F_n = F_{n-1} + F_{n-2}$ for $n \geq 3$.

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $F_n$ | 1 | 1 | 2 | 3 | 5 | 8 | 13 | 21 | 34 | 55 |

**Known inductive results about Fibonacci:**
- $F_n < 2^n$ for all $n \geq 1$
- $F_n \leq 2^{n-1}$ for all $n \geq 1$
- $F_{2n} = F_n(2F_{n+1} - F_n)$
- $\gcd(F_m, F_n) = F_{\gcd(m,n)}$ (Fibonacci GCD theorem — proved later)
- Binet's formula: $F_n = \dfrac{\phi^n - \psi^n}{\sqrt{5}}$ where $\phi = \frac{1+\sqrt{5}}{2}$, $\psi = \frac{1-\sqrt{5}}{2}$

---

## Induction Proof Strategy by Claim Type

| Claim looks like | Strategy |
|---|---|
| $\sum f(i) = g(n)$ | Peel off last term: $\sum_{i}^{k+1} = \sum_{i}^{k} + f(k+1)$ |
| $\prod f(i) = g(n)$ | Peel off last factor: $\prod_{i}^{k+1} = \prod_{i}^{k} \cdot f(k+1)$ |
| $d \mid h(n)$ | Express $h(k+1)$ as $[\text{multiple of } h(k)] + [\text{other term divisible by } d]$ |
| $f(n) \geq g(n)$ | Write $f(k+1)$ in terms of $f(k)$; use IH; bound remaining term |
| $a_n = \text{closed form}$ | Substitute recurrence, apply IH, simplify |
| Property of $F_n$ | Usually need 2 base cases; use $F_{k+1} = F_k + F_{k-1}$ |
| Every $n$ has property X | Strong induction — handle prime/composite cases separately |
