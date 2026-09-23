# MATH 142 · Calculus II
## Lab 03: The $p$-Test, and the Limits of Numerical Evidence
### Week 3 Lab Session

**Date:** Wednesday 17 February 2027 · 15:00–16:50 · Lab section (Week 4) — covers Week 3 (Lectures 1–3)

---

**Duration:** 2 hours
**Format:** Individual or pairs (pairs submit separate reports)
**Graded on:** completion + correctness — **100 points**
**Tools required:** Python 3 with `mpmath` (`pip install mpmath`) — you will need exponents beyond `float` range

> **mpmath — every call the MATH 142 labs use, in one place.** No course has taught it; this is all you
> need, here and in Labs 4–12.
>
> ```python
> import mpmath as mp
> mp.mp.dps = 30                  # work to 30 significant digits (set before computing)
> mp.mpf(1) / 3                   # a high-precision number; arithmetic on mpf stays high-precision
> mp.log, mp.exp, mp.sqrt, mp.sin, mp.pi, mp.e    # the usual functions and constants
> mp.quad(f, [a, b])              # a numerical integral; mp.inf allowed as an endpoint
> mp.euler                        # the Euler–Mascheroni constant (Lab 7)
> mp.ellipe(m)                    # the complete elliptic integral E(m) (Lab 5)
> ```
>
> Wherever a lab says "numerical quadrature", your own Simpson's rule from Lab 00 is equally acceptable.

---

## Overview

Labs 0, 1 and 2 each compared a numerical method against an exact one. **This lab is the sharpest version of that comparison, and the conclusion is the strongest.**

Monday's $p$-test says

$$\int_1^\infty\frac{dx}{x^p}\ \text{converges} \iff p>1$$

That is a clean, exact, one-line criterion. **This lab asks whether you could have discovered it numerically** — by computing $\int_1^T x^{-p}dx$ for large $T$ and watching.

The answer is **no**, and not by a small margin. You will find that at $T=10^6$ the *convergent* case looks smaller than the divergent one, and that at $T=10^{100}$ — a googol, vastly more than the number of atoms in the observable universe — a convergent integral has still reached only 90% of its limit.

**Numerical evidence cannot decide convergence.** That is the lab.

---

## The Exact Formula

Everything rests on one closed form, which you should derive before computing anything:

$$F(T,p) := \int_1^T x^{-p}\,dx = \begin{cases}\dfrac{1-T^{1-p}}{p-1} & p\neq1\\[10pt] \ln T & p=1\end{cases}$$

```python
import mpmath as mp
mp.mp.dps = 20

def F(T, p):
    T, p = mp.mpf(T), mp.mpf(p)
    return mp.log(T) if p == 1 else (1 - T**(1-p))/(p-1)
```

**Use `mpmath`, not floats.** $10^{100}$ is fine for a float, but you will want more precision than 15 digits in Part D.

---

## Part A — Derive and Verify (20 pts)

**A1 (8 pts).** Derive $F(T,p)$ by hand for $p\neq1$ and for $p=1$. Show the antiderivative in each case.

**A2 (6 pts).** Verify your implementation against three exactly-known values:

| | | exact |
|---|---|---|
| $F(T,2)$ as $T\to\infty$ | | $1$ |
| $F(T,\tfrac32)$ as $T\to\infty$ | | $2$ |
| $F(10^6, 1)$ | | $\ln(10^6) = 6\ln10$ |

**A3 (6 pts).** From the formula, state the limit $\lim_{T\to\infty}F(T,p)$ for each of $p = 0.5,\ 0.99,\ 1,\ 1.01,\ 1.5,\ 2$. Which converge, and to what?

*Do this from the formula, before you compute the table. You are about to see numbers that contradict your intuition, and you need the right answer written down first.*

---

## Part B — The Table (25 pts)

**B1 (18 pts).** Compute $F(T,p)$ for

$$T \in \{10,\ 10^2,\ 10^3,\ 10^4,\ 10^6,\ 10^{10},\ 10^{20},\ 10^{50},\ 10^{100}\}$$
$$p \in \{0.5,\ 0.99,\ 1,\ 1.01,\ 1.5,\ 2\}$$

Present it as a table with $T$ down the side and $p$ across.

**B2 (7 pts).** Mark clearly on your table which columns converge and which diverge, using your Part A3 answers — **not** the appearance of the numbers.

---

## Part C — What the Table Shows (30 pts)

**C1 (10 pts).** Look at the row $T = 10^6$. Report the values for $p=0.99$, $p=1$, and $p=1.01$.

- (a) Which of the three is **largest**? Which is **smallest**?
- (b) Which of the three **converges**?
- (c) State plainly what is wrong with the following reasoning:

> *"I computed the integral out to a million. The $p=1.01$ case gave the smallest value and was still
> growing slowly, just like the other two. All three look the same, so they must behave the same."*

**C2 (8 pts).** The $p=1.01$ column converges to $100$.

- (a) What fraction of its limit has it reached at $T=10^6$?
- (b) Find, from the formula, the value of $T$ at which it reaches **90%** of its limit. Show the algebra.
- (c) Comment on whether that $T$ is reachable by computation.

**C3 (6 pts).** Contrast with the $p=2$ column, which converges to 1.

At what $T$ does it reach 90% of *its* limit? Why is this case so different from $p=1.01$, when both converge?

**C4 (6 pts).** Now compare two **divergent** columns, $p=0.5$ and $p=1$.

Both diverge, but they look completely different in the table. Describe how each grows (give the functional form from the formula), and explain why one divergence is numerically obvious and the other is essentially invisible.

---

## Part D — A Pair That Cannot Be Separated by Powers (15 pts)

Lecture 3 §7(d) claimed that

$$\int_2^\infty\frac{dx}{x\ln x}\quad\text{diverges} \qquad\text{while}\qquad \int_2^\infty\frac{dx}{x(\ln x)^2}\quad\text{converges to }\frac{1}{\ln2}$$

**D1 (5 pts).** Prove both, by the substitution $u=\ln x$. *(Each is two lines.)*

**D2 (6 pts).** Compute both partial integrals numerically at $T = 10^2,\ 10^6,\ 10^{20},\ 10^{100}$.

Report the values and comment: at $T=10^{100}$, how close is the convergent one to $\frac1{\ln2}\approx1.4427$, and how large is the divergent one?

**D3 (4 pts).** Explain why **no** comparison with a power $x^{-q}$ can decide either of these.

*Hint: consider what happens for $q=1$ and for $q = 1+\epsilon$ with any $\epsilon>0$.*

---

## Part E — Reflection (10 pts)

**E1 (5 pts).** Labs 0, 1 and 2 each contrasted an exact method with a numerical one:

| Lab | Numerical result | Exact result |
|---|---|---|
| 0 | Simpson: 10 digits from 128 points | — |
| 1 | Wallis: 10 digits needs $8\times10^9$ factors | the product is exactly $\pi/2$ |
| 2 | — | $\frac{22}{7}-\pi$, proving an inequality |
| 3 | **?** | the $p$-test, one line |

Fill in the missing entry for Lab 3, then rank the four labs by **how badly numerics loses**, and justify your ranking in two or three sentences.

**E2 (5 pts).** In Lab 0 numerics was excellent — ten digits from 128 evaluations. In this lab it is useless.

**What is different about the question being asked?** Answer in terms of what a finite computation can and cannot establish.

---

## What to Submit

1. Your derivation of $F(T,p)$ and the verification (Part A)
2. The full table (Part B)
3. Your answers to C1–C4, with the algebra in C2(b) shown
4. The two proofs and the numerical comparison (Part D)
5. Parts E1 and E2

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A | 20 | Deriving the closed form; stating the limits first |
| B | 25 | The table |
| C | 30 | Reading it correctly against intuition |
| D | 15 | A pair no power can separate |
| E | 10 | What a finite computation can establish |
| **Total** | **100** | |

---

*Every lab so far has ended with a number. This one ends with a limitation — and knowing the boundary of a method is worth as much as knowing the method.*
