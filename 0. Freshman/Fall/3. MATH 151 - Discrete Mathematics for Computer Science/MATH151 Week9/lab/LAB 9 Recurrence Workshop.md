# MATH 151 — Discrete Mathematics for Computer Science
## Lab 9 — Recurrence Workshop: Modelling, Solving, Verifying
### Wednesday, Week 9 | Duration: 2 hours

---

**Bring:** laptop with Python 3. Work in pairs; both submit.

**Theme:** every closed form in this lab is **checked against iteration**. That habit — derive, then
verify numerically — is the single most valuable thing you will take from this week, and it catches
sign errors that no amount of re-reading will.

---

## Section 1 — Modelling (30 min)

For each scenario, write the recurrence **and** its initial conditions, then compute the first six
values by hand.

### Exercise 1.1
Length-$n$ bit strings with no two consecutive 1s.

**Recurrence:** ________________  **Initial conditions:** ________________

### Exercise 1.2
The number of regions $n$ lines in general position divide the plane into.

### Exercise 1.3
A staircase of $n$ steps, climbed 1 or 2 steps at a time. How many distinct ways?

### Exercise 1.4
A country issues 3¢ and 5¢ stamps. Ways to make $n$ cents **where order matters**.

*(Careful with the initial conditions on this one — several are zero.)*

---

## Section 2 — Solving by Hand (30 min)

Solve each, then **verify against three iterated values**.

### Exercise 2.1
$a_n = 7a_{n-1}-12a_{n-2}$, $a_0=2$, $a_1=5$.

### Exercise 2.2
$a_n = 4a_{n-1}-4a_{n-2}$, $a_0=1$, $a_1=6$. Which case applies?

### Exercise 2.3
$a_n = 3a_{n-1}+2$, $a_0=4$. Solve twice — once by iteration, once by characteristic equation.

---

## Section 3 — Python: Iterate, Solve, Compare (40 min)

### Exercise 3.1 — A Verification Harness

```python
def iterate(rec, initial, N):
    """rec(a, n) returns a_n given the list a of previous terms."""
    a = list(initial)
    while len(a) < N:
        a.append(rec(a, len(a)))
    return a

def check(closed, seq):
    """Report the first index where a closed form disagrees with the sequence."""
    for n, v in enumerate(seq):
        if closed(n) != v:
            return f"MISMATCH at n={n}: closed={closed(n)}, actual={v}"
    return f"OK for n = 0..{len(seq)-1}"
```

**Task:** use this to verify all three of your Section 2 answers. Paste the output. *(6 pts)*

### Exercise 3.2 — Binet's Formula and Floating Point

```python
from math import sqrt
phi, psi = (1+sqrt(5))/2, (1-sqrt(5))/2
binet = lambda n: (phi**n - psi**n) / sqrt(5)
```

1. Tabulate `binet(n)` against the integer $F_n$ for $n = 0, \ldots, 80$.
2. **Find the first $n$ where `round(binet(n))` differs from $F_n$.** Explain what went wrong — the
   mathematics is exact, so the failure is not mathematical.
3. Verify that for $n \geq 1$, $F_n$ is the nearest integer to $\varphi^n/\sqrt5$ — that is, that
   dropping the $\psi^n$ term entirely still rounds correctly.

### Exercise 3.3 — Naive vs Memoised Fibonacci

```python
def fib_naive(n):
    return n if n < 2 else fib_naive(n-1) + fib_naive(n-2)
```

1. Instrument it to count calls. Tabulate the count for $n = 5, 10, 15, 20, 25, 30$.
2. Confirm the call count itself satisfies a recurrence, and identify it.
3. Write a memoised version and compare both time and call count at $n=30$.
4. State the complexity of each and connect it to Lecture 9.2's $\Theta(\varphi^n)$.

### Exercise 3.4 — Power Series by Formal Division

```python
from fractions import Fraction as Fr

def series(num, den, N):
    """Coefficients of num/den as a formal power series. Lists are coefficient lists."""
    a = []
    for n in range(N):
        s = num[n] if n < len(num) else Fr(0)
        for k in range(1, min(n, len(den)-1) + 1):
            s -= den[k] * a[n-k]
        a.append(s / den[0])
    return a
```

Use it to confirm:

| Function | Expected coefficients |
|---|---|
| $1/(1-x)$ | all 1s |
| $1/(1-2x)$ | powers of 2 |
| $1/(1-x)^2$ | $1,2,3,4,\ldots$ |
| $x/(1-x-x^2)$ | Fibonacci |
| $(1-x)/(1-5x+6x^2)$ | your C-part answer |

**Why `Fraction` and not `float`?** Answer this in one sentence in your write-up.

---

## Section 4 — Generating Functions by Hand (15 min)

### Exercise 4.1
Write the generating function for making $n$ cents from 1¢, 2¢, and 5¢ coins. Compute the
coefficient of $x^{10}$ with your Exercise 3.4 code, then **verify by listing every combination**.

### Exercise 4.2
Write the generating function for choosing $n$ objects from four types with at most 3 of each, and
find the coefficient of $x^5$. Verify by brute-force enumeration.

---

## Section 5 — Reflection (5 min)

1. In Exercise 3.2 the mathematics is exact but the computation fails at some point. What does this
   tell you about using closed forms numerically?

2. Exercise 3.3's naive Fibonacci recomputes the same subproblems. Estimate how many times $F_5$ is
   computed during `fib_naive(30)`, and say what memoisation actually changes.

3. Generating functions and the characteristic equation solve the same recurrences. Give one reason
   you might prefer each.

---

## Checkoff Criteria

Show your TA:

- [ ] Section 1: all four recurrences with correct initial conditions
- [ ] Section 2: all three solved and verified against iteration
- [ ] Exercise 3.1: harness working, all three Section 2 answers reported OK
- [ ] Exercise 3.2: the breakdown point of Binet's formula found and explained
- [ ] Exercise 3.3: call counts tabulated, recurrence identified, memoised version compared
- [ ] Exercise 3.4: all five series confirmed
- [ ] Section 4: both coefficients verified two ways
