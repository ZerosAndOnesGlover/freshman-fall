# MATH 151 — Generating Functions Reference
## Week 9: Generating Functions

---

## Definition

$$G(x) = \sum_{n=0}^{\infty} a_n x^n = a_0 + a_1x + a_2x^2 + \cdots$$

**The sequence is the coefficients.** $x$ is a bookkeeping device.

**"Formal" power series:** we never substitute a value for $x$ and never ask about convergence. Every
operation is defined by its effect on coefficients. This is why $\frac{1}{1-x}$ is a perfectly good
generating function even though the series diverges for $|x| \ge 1$.

---

## The Catalogue

| Generating function | Coefficients $a_n$ |
|---|---|
| $\dfrac{1}{1-x}$ | $1, 1, 1, 1, \ldots$ |
| $\dfrac{1}{1-cx}$ | $c^n$ |
| $\dfrac{1}{(1-x)^2}$ | $n+1$ &nbsp; ($1,2,3,4,\ldots$) |
| $\dfrac{1}{(1-x)^k}$ | $\binom{n+k-1}{k-1}$ |
| $\dfrac{x}{1-x-x^2}$ | Fibonacci $F_n$ |
| $(1+x)^m$ | $\binom mn$ |
| $\dfrac{1-x^{m+1}}{1-x}$ | $1$ for $n\le m$, else $0$ |
| $e^x$ *(exponential GF)* | $1/n!$ |

**All verified by formal division:**

| Function | First eight coefficients |
|---|---|
| $1/(1-x)$ | 1, 1, 1, 1, 1, 1, 1, 1 |
| $1/(1-2x)$ | 1, 2, 4, 8, 16, 32, 64, 128 |
| $1/(1-3x)$ | 1, 3, 9, 27, 81, 243, … |
| $1/(1-x)^2$ | 1, 2, 3, 4, 5, 6, 7, 8 |
| $x/(1-x-x^2)$ | 0, 1, 1, 2, 3, 5, 8, 13 |
| $(1-x)/(1-5x+6x^2)$ | 1, 4, 14, 46, 146, 454, 1394, 4246 |
| $(2+5x)/(1-x-2x^2)$ | 2, 7, 11, 25, 47, 97, 191, 385 |

---

## Solving a Recurrence

1. Let $G(x)=\sum a_nx^n$.
2. Multiply the recurrence by $x^n$; sum over all $n$ where it holds.
3. Express each shifted sum via $G(x)$: $\sum_{n\ge k}a_{n-1}x^n = x\,G(x) - (\text{missing terms})$.
4. Solve algebraically for $G(x)$.
5. Expand — by formal division or partial fractions — to recover $a_n$.

### Worked: Fibonacci

$$G(x)-x = xG(x)+x^2G(x) \;\Longrightarrow\; G(x)=\frac{x}{1-x-x^2}$$

**The denominator is the reversed characteristic polynomial.** $1-x-x^2$ reversed is $-x^2-x+1$,
i.e. $r^2-r-1$ up to sign. The characteristic-equation method and generating functions are the same
mathematics; partial fractions on $x/(1-x-x^2)$ reproduces Binet's formula exactly.

---

## Multiplication = Convolution = Independent Choice

$$\left(\sum a_nx^n\right)\left(\sum b_nx^n\right)=\sum_n\left(\sum_{k=0}^{n}a_kb_{n-k}\right)x^n$$

The inner sum is "take some from the first pile, the rest from the second". **So one factor per
independent choice.**

### Making change

Ways to make $n$ cents from 1¢, 5¢, 10¢:

$$\frac{1}{1-x}\cdot\frac{1}{1-x^5}\cdot\frac{1}{1-x^{10}}$$

Verified: the coefficient of $x^{25}$ is **12**, confirmed by listing all 12 combinations.

For 1¢, 2¢, 5¢ the coefficient of $x^{10}$ is **10** — likewise confirmed by enumeration.

### One factor per restriction

| Restriction on a type | Factor |
|---|---|
| Any number | $\dfrac{1}{1-x}$ |
| At most $m$ | $1+x+\cdots+x^m = \dfrac{1-x^{m+1}}{1-x}$ |
| At least $k$ | $\dfrac{x^k}{1-x}$ |
| An even number | $\dfrac{1}{1-x^2}$ |
| Exactly 0 or 1 | $1+x$ |
| In multiples of $d$ | $\dfrac{1}{1-x^d}$ |

Verified: choosing from four types with at most 3 of each is $(1+x+x^2+x^3)^4$, whose coefficient of
$x^5$ is **40** — confirmed by brute-force enumeration.

---

## Catalan Numbers

$$C_n=\frac{1}{n+1}\binom{2n}{n}, \qquad C(x)=\frac{1-\sqrt{1-4x}}{2x}$$

arising from $C_n=\sum_{k=0}^{n-1}C_kC_{n-1-k}$ — a convolution, hence a product.

$C_0..C_8 = 1, 1, 2, 5, 14, 42, 132, 429, 1430$ *(verified)*.

Counts binary trees with $n$ nodes, balanced bracket strings of length $2n$, and polygon
triangulations.

---

## Computing Coefficients Exactly

```python
from fractions import Fraction as Fr

def series(num, den, N):
    a = []
    for n in range(N):
        s = num[n] if n < len(num) else Fr(0)
        for k in range(1, min(n, len(den)-1) + 1):
            s -= den[k] * a[n-k]
        a.append(s / den[0])
    return a
```

**Use `Fraction`, not `float`.** Formal power series coefficients are exact rationals; floating point
introduces rounding that accumulates through the recursion and silently corrupts later coefficients.

---

## Common Errors

| ❌ | ✅ |
|---|---|
| Worrying whether the series converges | It is *formal* — convergence never arises |
| Forgetting the missing terms when shifting | $\sum_{n\ge2}a_{n-1}x^n = x(G(x)-a_0)$ |
| Adding factors for independent choices | **Multiply** — addition models alternatives, not combinations |
| Using floats for coefficients | Use `Fraction` |
| Expecting a closed form always | Sometimes the generating function *is* the answer |

---

*MATH 151 · Week 9 · Reference · © CSE Department*
