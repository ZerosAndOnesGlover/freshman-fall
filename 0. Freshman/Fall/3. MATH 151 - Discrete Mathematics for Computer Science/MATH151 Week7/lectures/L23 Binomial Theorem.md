# MATH 151 · Discrete Mathematics for Computer Science
## Lecture 23 (L23) — The Binomial Theorem and Pascal's Triangle
### Friday, Week 7

**Date:** Friday 13 November 2026 · 13:00–13:50 · Week 7

---

> **Core Question:** What is the algebraic expansion of $(x+y)^n$, and what does it reveal about the deep structure connecting algebra and counting?

---

## 1. The Binomial Theorem

**Theorem (Binomial Theorem).** For any non-negative integer $n$:
$$(x+y)^n = \sum_{k=0}^{n} \binom{n}{k} x^{n-k}y^k$$

**Expanded form:**
$$(x+y)^n = \binom{n}{0}x^n + \binom{n}{1}x^{n-1}y + \binom{n}{2}x^{n-2}y^2 + \cdots + \binom{n}{n}y^n$$

### Why This Connects to Counting

When you expand $(x+y)^n = (x+y)(x+y)\cdots(x+y)$ ($n$ factors), each term in the fully expanded polynomial arises from choosing, for EACH of the $n$ factors, either the $x$ or the $y$. A term $x^{n-k}y^k$ arises whenever you choose $y$ from exactly $k$ of the $n$ factors (and $x$ from the remaining $n-k$).

**The number of ways to choose WHICH $k$ factors contribute the $y$** is exactly $\binom{n}{k}$ — a combination (order doesn't matter, no repetition) of size $k$ chosen from $n$ factors.

This is why the coefficient of $x^{n-k}y^k$ is $\binom{n}{k}$ — **the Binomial Theorem is literally a counting statement in algebraic disguise.**

### Worked Example 1

Expand $(x+y)^4$.

$$(x+y)^4 = \binom{4}{0}x^4+\binom{4}{1}x^3y+\binom{4}{2}x^2y^2+\binom{4}{3}xy^3+\binom{4}{4}y^4$$
$$= x^4+4x^3y+6x^2y^2+4xy^3+y^4$$

### Worked Example 2 — Finding a Specific Coefficient

Find the coefficient of $x^5y^3$ in the expansion of $(x+y)^8$.

**Solution.** We need $n=8$, and the term $x^{n-k}y^k$ with $n-k=5, k=3$ (consistent: $5+3=8$ ✓).

Coefficient $=\binom{8}{3}=\frac{8!}{3!5!}=56$.

### Worked Example 3 — A Trickier Binomial

Find the coefficient of $x^3$ in $(2x-3)^5$.

**Solution.** Write $(2x-3)^5 = (2x+(-3))^5 = \sum_{k=0}^5\binom{5}{k}(2x)^{5-k}(-3)^k$.

We need $x^3$, so $5-k=3$, giving $k=2$.

Term: $\binom{5}{2}(2x)^3(-3)^2 = 10\times8x^3\times9 = 720x^3$.

Coefficient: **720**.

---

## 2. Pascal's Triangle

Pascal's Triangle is the visual arrangement of binomial coefficients:

```
n=0:                1
n=1:               1  1
n=2:              1  2  1
n=3:             1  3  3  1
n=4:            1  4  6  4  1
n=5:           1 5  10 10  5  1
n=6:          1 6 15 20 15  6  1
```

Row $n$ contains $\binom{n}{0},\binom{n}{1},\ldots,\binom{n}{n}$.

**Construction rule:** each interior entry is the sum of the two entries diagonally above it — this is EXACTLY Pascal's Rule, proved combinatorially on Thursday:
$$\binom{n}{r} = \binom{n-1}{r-1}+\binom{n-1}{r}$$

**Connection to Week 6:** the Hasse diagram of $(\mathcal{P}(\{1,2,3\}),\subseteq)$ (Lab 6, Exercise 3.2) has exactly 1, 3, 3, 1 elements at each level — row 3 of Pascal's Triangle. In general, the number of size-$k$ subsets of an $n$-element set, arranged by level in the subset-inclusion Hasse diagram, gives exactly row $n$ of Pascal's Triangle.

---

## 3. Combinatorial Identities via the Binomial Theorem

### Identity 1: Row Sum $= 2^n$

Set $x=y=1$ in the Binomial Theorem:
$$(1+1)^n = \sum_{k=0}^n\binom{n}{k}1^{n-k}1^k = \sum_{k=0}^n\binom{n}{k}$$
$$2^n = \sum_{k=0}^n\binom{n}{k}$$

**This confirms the "total subsets" fact from Week 4** ($|\mathcal{P}(A)|=2^n$) via a completely different route — algebraic substitution rather than induction. Two independent proofs of the same fact, from two different areas of mathematics, is a hallmark of deep mathematical structure.

### Identity 2: Alternating Sum $= 0$

Set $x=1, y=-1$:
$$(1-1)^n = \sum_{k=0}^n\binom{n}{k}1^{n-k}(-1)^k$$
$$0^n = \sum_{k=0}^n(-1)^k\binom{n}{k}$$

For $n\geq1$: $0 = \binom{n}{0}-\binom{n}{1}+\binom{n}{2}-\cdots\pm\binom{n}{n}$.

**Interpretation:** the number of EVEN-sized subsets of an $n$-set equals the number of ODD-sized subsets (for $n\geq1$) — each equal to $2^{n-1}$. (This resolves Week 4's Lecture 14, Exercise 5!)

### Identity 3: The Hockey Stick Identity

$$\sum_{i=r}^{n}\binom{i}{r} = \binom{n+1}{r+1}$$

**Combinatorial proof:** Consider choosing a subset of size $r+1$ from $\{1,2,\ldots,n+1\}$. Classify by the LARGEST element chosen, say it's $i+1$ (so $i$ ranges from $r$ to $n$). Given the largest element is $i+1$, the remaining $r$ elements must come from $\{1,\ldots,i\}$: $\binom{i}{r}$ ways. Summing over all valid $i$ (Addition Rule, since these cases are mutually exclusive by largest-element value) gives the total count $\binom{n+1}{r+1}$ two ways — proving the identity. ∎

---

## 4. The Vandermonde Identity (More Advanced — Optional Enrichment)

$$\binom{m+n}{r} = \sum_{k=0}^{r}\binom{m}{k}\binom{n}{r-k}$$

**Combinatorial proof.** Suppose we choose $r$ people from a group of $m+n$ people, consisting of $m$ men and $n$ women. The LHS directly counts this: $\binom{m+n}{r}$.

Alternatively, classify by how many of the $r$ chosen are men ($k$) versus women ($r-k$): for each $k$ from 0 to $r$, choose $k$ men from $m$ ($\binom{m}{k}$ ways) and $r-k$ women from $n$ ($\binom{n}{r-k}$ ways), by the Multiplication Rule giving $\binom{m}{k}\binom{n}{r-k}$ for that specific $k$. Summing over all $k$ (Addition Rule, mutually exclusive cases) gives the RHS.

Since both sides count the same thing, they are equal. ∎

---

## 5. Generalization — The Multinomial Theorem (Brief Mention)

The Binomial Theorem generalizes to sums of more than 2 terms:

$$(x_1+x_2+\cdots+x_m)^n = \sum \binom{n}{k_1,k_2,\ldots,k_m}x_1^{k_1}x_2^{k_2}\cdots x_m^{k_m}$$

where the sum ranges over all non-negative integers $k_1,\ldots,k_m$ with $k_1+\cdots+k_m=n$, and

$$\binom{n}{k_1,k_2,\ldots,k_m} = \frac{n!}{k_1!k_2!\cdots k_m!}$$

is the **multinomial coefficient** — exactly the "arrangements with indistinguishable objects" formula from Thursday's lecture (Section 9), now appearing as the coefficient in a multi-term expansion.

---

## 6. Binomial Coefficients in Computer Science

**Dynamic programming — Pascal's Triangle as a DP table:** Computing $\binom{n}{r}$ via the recurrence $\binom{n}{r}=\binom{n-1}{r-1}+\binom{n-1}{r}$ (with base cases $\binom{n}{0}=\binom{n}{n}=1$) is a textbook dynamic programming algorithm, avoiding the numerical overflow issues of computing large factorials directly.

```python
def binomial_dp(n, r):
    """Compute C(n,r) via Pascal's Rule (dynamic programming)."""
    C = [[0]*(r+1) for _ in range(n+1)]
    for i in range(n+1):
        C[i][0] = 1
        for j in range(1, min(i,r)+1):
            if j == i:
                C[i][j] = 1
            else:
                C[i][j] = C[i-1][j-1] + C[i-1][j]
    return C[n][r]
```

**Probability (MATH 251 preview):** the Binomial Distribution — probability of exactly $k$ successes in $n$ independent trials with success probability $p$ — is $\binom{n}{k}p^k(1-p)^{n-k}$, directly built from the Binomial Theorem's structure.

**Error-correcting codes:** binomial coefficients count the number of ways bit-errors can occur in a codeword, directly informing the design and analysis of Hamming codes and other error-correction schemes (CS 341).

**Algorithm analysis:** the number of comparisons in certain divide-and-conquer algorithms, and the size of certain recursive search trees, are expressed via binomial coefficients.

---

## 7. Summary

```
Binomial Theorem:
  (x+y)^n = Σ C(n,k) x^(n-k) y^k

Pascal's Triangle:
  Row n = C(n,0), C(n,1), ..., C(n,n)
  Recurrence: C(n,r) = C(n-1,r-1) + C(n-1,r)

Key identities (all provable by substitution or combinatorial argument):
  Σ C(n,k) = 2^n                        (x=y=1)
  Σ (-1)^k C(n,k) = 0  (n≥1)             (x=1,y=-1)
  Σ_{i=r}^{n} C(i,r) = C(n+1,r+1)        (Hockey Stick)
  C(m+n,r) = Σ C(m,k)C(n,r-k)            (Vandermonde)

Multinomial Theorem: generalizes to sums of m terms
  Coefficient of x₁^k₁⋯x_m^k_m is n!/(k₁!⋯k_m!)
```

---

## 8. End-of-Lecture Exercises

1. Expand $(x+y)^5$ completely using the Binomial Theorem.

2. Find the coefficient of $x^4y^6$ in $(x+y)^{10}$.

3. Find the coefficient of $x^3$ in $(3x-2)^6$.

4. Using the Binomial Theorem with a clever substitution, prove: $\sum_{k=0}^{n}\binom{n}{k}2^k = 3^n$.
   *(Hint: what values of $x,y$ give you a $2^k$ inside the sum?)*

5. Verify Pascal's Rule algebraically: show $\binom{n-1}{r-1}+\binom{n-1}{r}=\binom{n}{r}$ using the factorial formula (not the combinatorial argument). Show every algebraic step.

6. Give a combinatorial proof (count the same thing two ways) of: $\binom{n}{k}=\binom{n}{n-k}$. *(This is the Symmetry property — prove it via a bijection/counting argument, not just algebra.)*

7. Row 10 of Pascal's Triangle is: 1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1. Verify: does the row sum to $2^{10}=1024$? Does the alternating sum equal 0?

8. **Challenge:** Use the Hockey Stick Identity to compute $\binom{3}{3}+\binom{4}{3}+\binom{5}{3}+\binom{6}{3}+\binom{7}{3}$ without adding the five terms directly — verify your shortcut answer by also computing the direct sum.

---

*Week 7 complete. Week 8: Advanced Counting — the Pigeonhole Principle and Inclusion–Exclusion. The identity $\sum_k(-1)^k\binom nk = 0$ proved above is exactly what makes inclusion–exclusion's alternating signs work.*
