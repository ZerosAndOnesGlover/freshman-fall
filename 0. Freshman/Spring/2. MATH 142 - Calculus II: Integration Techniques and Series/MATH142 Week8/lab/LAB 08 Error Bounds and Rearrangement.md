# MATH 142 · Calculus II
## Lab 08: Error Bounds, and Rearranging a Series to Any Sum You Like
### Week 8 Lab Session

**Date:** Wednesday 24 March 2027 · 15:00–16:50 · Lab section (Week 9) — covers Week 8 (Lectures 1–3)

---

**Duration:** 2 hours
**Format:** Individual or pairs (pairs submit separate reports)
**Graded on:** completion + correctness — **100 points**
**Tools required:** Python 3 with `mpmath` — only the calls in Lab 02's SymPy box and Lab 03's mpmath box

---

## Overview

The alternating harmonic series

$$1-\frac12+\frac13-\frac14+\cdots = \ln 2$$

converges **only because of cancellation** — its absolute values give the divergent harmonic series. This lab explores what that fragility costs and what it permits.

**Part A** measures the Leibniz error bound and finds it is honest but loose by a consistent factor.
**Part B** exploits that fragility: you will rearrange these very terms to sum to $\pi$.
**Part C** repairs the slowness, raising the order from 1 to 2 with one line of arithmetic.

---

## Part A — The Leibniz Error Bound (25 pts)

**A1 (10 pts).** Compute $s_N$ for $N = 10,\ 20,\ 50,\ 100,\ 200,\ 400$.

Tabulate $s_N$, the true error $|{\ln2}-s_N|$, and the Leibniz bound $b_{N+1}=\frac{1}{N+1}$.

**Confirm the bound holds at every $N$.**

**A2 (8 pts).** Add a column of $\dfrac{\text{true error}}{\text{bound}}$.

It approaches a simple constant. **Report it**, and explain geometrically why — recall that the sum lies **between** $s_N$ and $s_{N+1}$.

**A3 (7 pts).** How many terms does the Leibniz bound guarantee are needed for

- (a) 3 correct decimal places?
- (b) 6 correct decimal places?

Comment on whether direct summation is a sensible way to compute $\ln2$.

---

## Part B — Rearranging to Any Target (30 pts)

The positive terms $1,\frac13,\frac15,\ldots$ sum to $+\infty$; the negative terms $-\frac12,-\frac14,\ldots$ sum to $-\infty$. **Riemann's theorem exploits exactly this.**

**B1 (12 pts).** Implement the greedy rearrangement:

```python
def rearrange(target, nterms):
    s, p, q, used = mp.mpf(0), 1, 2, 0     # p odd (positives), q even (negatives)
    while used < nterms:
        while s <= target and used < nterms:
            s += mp.mpf(1)/p;  p += 2;  used += 1
        while s > target and used < nterms:
            s -= mp.mpf(1)/q;  q += 2;  used += 1
    return s
```

Run it with `nterms = 300000` for the targets

$$T = \ln 2,\quad 1,\quad \pi,\quad 0,\quad -2$$

**Report the partial sum reached in each case.**

**B2 (8 pts).** For the target $T=\pi$, record the running total at each **crossing** (each time the algorithm switches between adding positives and negatives) for the first eight crossings.

Describe what the sequence of crossings is doing, and explain why the overshoot shrinks.

**B3 (10 pts).**

- (a) Explain why each inner `while` loop is guaranteed to terminate.
- (b) Explain why the partial sums converge to $T$, referring to the size of the last term used at each crossing.
- (c) **The same terms, in their natural order, sum to $\ln2$.** In two or three sentences, say precisely which property of addition fails here — and why it is not a paradox.
- (d) Would this construction work on $\sum\frac{(-1)^{n+1}}{n^2}$? Explain.

---

## Part C — Making It Fast (25 pts)

Since $\ln2$ lies **between** $s_N$ and $s_{N+1}$, the midpoint should be better than either.

**C1 (10 pts).** Define $\widetilde S_N = \dfrac{s_N+s_{N+1}}{2}$ and tabulate $|\ln2-\widetilde S_N|$ alongside the raw error, for $N = 10,\ 20,\ 50,\ 100,\ 200,\ 400$.

**C2 (10 pts).** Add a column of error ratios **on doubling $N$** for the averaged estimate.

- (a) What is the ratio?
- (b) Hence what is the order of the averaged method, and what was the order of the raw one?

**C3 (5 pts).** Compare with Lab 7 Part C, where averaging the Integral Test bounds raised the order from 1 to 3.

Here it goes from 1 to 2. **Both improvements came from a two-sided bracket. Why is this one weaker?**

---

## Part D — Reflection (20 pts)

**D1 (10 pts).** Part B rearranged a convergent series to a different sum; Part C averaged consecutive partial sums to accelerate it. **Both exploit the same structural fact about alternating series.** State it, and explain how one use is destructive and the other constructive.

**D2 (10 pts).** Across eight labs:

| Lab | Verdict |
|---|---|
| 0 | numerics won |
| 3 | numerics could not answer at all |
| 6 | numerics superb, because exact analysis predicted it |
| 7 | numerics failed; an exact theorem repaired it |
| **8** | **?** |

Fill in the entry.

*In your answer, address this: in Part B the computation produced a **correct** number for each target — $\pi$, $0$, $-2$ — and yet "the sum of the series" is $\ln 2$. **What exactly did the computation compute?***

---

## What to Submit

1. The Leibniz bound table with the ratio column (Part A)
2. Your rearrangement code, the five targets, and the crossing trace (Part B)
3. The averaged-error table with orders (Part C)
4. Parts D1 and D2

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A | 25 | The error bound, and why it is loose by a factor |
| B | 30 | Riemann rearrangement, implemented and explained |
| C | 25 | Raising the order from 1 to 2 |
| D | 20 | What the computation actually computed |
| **Total** | **100** | |

---

*The same 300,000 numbers, added in different orders, gave $\pi$ and $\ln 2$ and $-2$. Nothing went wrong. Infinite addition is not addition, and this lab is what that sentence means.*
