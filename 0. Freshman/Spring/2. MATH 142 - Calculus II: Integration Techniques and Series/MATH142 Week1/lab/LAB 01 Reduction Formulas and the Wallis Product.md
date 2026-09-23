# MATH 142 · Calculus II
## Lab 01: Reduction Formulas and the Wallis Product
### Week 1 Lab Session

**Date:** Wednesday 3 February 2027 · 15:00–16:50 · Lab section (Week 2) — covers Week 1 (Lectures 1–3)

---

**Duration:** 2 hours
**Format:** Individual or pairs (pairs submit separate reports)
**Graded on:** completion + correctness — **100 points**
**Tools required:** Python 3. Use `fractions.Fraction` for Parts A and D — **not** floating point.
`Fraction(a, b)` is the exact rational $a/b$; `+ - * /` on Fractions stay exact. That is all of it you need.

---

## Overview

Lecture 2 derived the reduction formula

$$I_n = \int_0^{\pi/2}\sin^n x\,dx = \frac{n-1}{n}\,I_{n-2}, \qquad I_0 = \frac\pi2,\quad I_1 = 1$$

and observed that it is **a recurrence relation** — a recursive algorithm with two base cases, reducing $n$ by 2 per call.

This lab implements it, and then uses it to reach a formula for $\pi$ that John Wallis found in **1656**, thirty years before Newton published the calculus:

$$\frac{\pi}{2} = \frac{2}{1}\cdot\frac{2}{3}\cdot\frac{4}{3}\cdot\frac{4}{5}\cdot\frac{6}{5}\cdot\frac{6}{7}\cdots$$

**The lab's real question is the same as Lab 0's:** how fast does it converge, and is that good enough to be useful? The answer this week is *no*, emphatically — and understanding why a beautiful formula can be computationally worthless is worth more than the formula.

---

## Part A — Implement the Recursion (25 pts)

Notice from the lecture that $I_n$ is a **rational number** when $n$ is odd and a **rational multiple of $\pi$** when $n$ is even. So represent $I_n$ exactly as a pair: a `Fraction` coefficient, and a flag for whether $\pi$ is present.

**A1 (12 pts).** Write a function returning $I_n$ in exact form.

```python
from fractions import Fraction

def I(n):
    """Return (coeff, has_pi) with  I_n = coeff * (pi if has_pi else 1)."""
    if n == 0: return (Fraction(1, 2), True)    # pi/2
    if n == 1: return (Fraction(1), False)      # 1
    c, hp = I(n - 2)
    return (c * Fraction(n - 1, n), hp)
```

Reproduce this table and confirm every entry:

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $I_n$ | $\tfrac\pi2$ | $1$ | $\tfrac\pi4$ | $\tfrac23$ | $\tfrac{3\pi}{16}$ | $\tfrac8{15}$ | $\tfrac{5\pi}{32}$ | $\tfrac{16}{35}$ | $\tfrac{35\pi}{256}$ |

**A2 (7 pts).** Explain why the parity of $n$ determines whether $\pi$ appears. Refer to the recursion's base cases.

**A3 (6 pts).** How many recursive calls does `I(n)` make, as a function of $n$? Give the exact count and the asymptotic order.

*If you have met recurrences in CS 101, say which standard shape this is.*

---

## Part B — The Wallis Product (25 pts)

Define the partial product

$$W_n = \prod_{k=1}^{n}\frac{(2k)(2k)}{(2k-1)(2k+1)} = \frac{2\cdot2}{1\cdot3}\cdot\frac{4\cdot4}{3\cdot5}\cdots\frac{(2n)(2n)}{(2n-1)(2n+1)}$$

**B1 (10 pts).** Compute $W_n$ in floating point for $n \in \{1,2,4,8,16,32,64,128,256,512,1024\}$ and tabulate it against $\pi/2 = 1.5707963267948966$.

**B2 (8 pts).** Add a column of absolute errors $|W_n - \pi/2|$, and a column of **consecutive error ratios** — as in Lab 0, the ratio is the point.

**B3 (7 pts).** Add a final column: $n\cdot|W_n - \pi/2|$. Report what this column appears to converge to, and identify the constant.

*It is a familiar number divided by something small. State it exactly if you can.*

---

## Part C — How Bad Is It? (25 pts)

**C1 (8 pts).** From your ratio column, state the order of convergence of the Wallis product — i.e. the $p$ for which the error behaves like $C n^{-p}$. Justify from your data.

**C2 (9 pts).** Using your measured constant from B3, estimate how many factors $n$ would be needed to compute $\pi$ to **10 correct decimal places**.

Comment on whether this is a practical way to compute $\pi$.

**C3 (8 pts).** Compare directly with Lab 0. There, Simpson's rule reached 10 decimal places on $\int_0^1 e^{-x^2}dx$ with $n = 128$.

Both are "compute a number by taking a limit". In a table, contrast the two on: order of convergence, work for 10 digits, and the ratio between them. Then say in one sentence what property of a numerical method actually determines whether it is usable.

---

## Part D — Why It Works: The Squeeze (15 pts)

Wallis' product is not an unrelated fact — **it falls out of the recursion in Part A**.

**D1 (5 pts).** On $[0,\pi/2]$ we have $0\le\sin x\le 1$, so $\sin^{n+1}x \le \sin^n x$. Deduce that

$$I_{2n+1}\;\le\;I_{2n}\;\le\;I_{2n-1}$$

**D2 (6 pts).** Using your exact values from Part A, verify numerically that

$$W_n \;=\; \frac{\pi}{2}\cdot\frac{I_{2n+1}}{I_{2n}}$$

for $n = 1, 2, 4, 8$. Report the two sides to at least 12 digits.

**D3 (4 pts).** Compute the ratio $I_{2n}/I_{2n+1}$ for $n$ up to 8 and observe that it tends to 1.

Combine with D2 to explain why $W_n \to \pi/2$ — that is, sketch the proof of Wallis' product.

---

## Part E — Reflection (10 pts)

**E1 (5 pts).** Part A computes $I_n$ **exactly** with rational arithmetic; Part B computes $W_n$ in floating point and converges slowly. Yet D2 shows they are the same quantity rearranged.

Explain how an exact formula and a slowly-converging approximation can be the same mathematics.

**E2 (5 pts).** Wallis found this in 1656 without calculus, and it was a celebrated result. Today it is useless for computing $\pi$.

In two or three sentences, say what it *is* still good for — why a mathematician would still care about a formula that no one would ever run.

---

## What to Submit

1. Your `I(n)` implementation and the reproduced exact table (Part A)
2. The $W_n$ table with errors, ratios, and $n\cdot$error (Part B)
3. Your order, your estimate for 10 digits, and the comparison table (Part C)
4. The squeeze verification and your sketch proof (Part D)
5. Parts E1 and E2

**Report the numbers you actually computed.** As in Lab 0, an unexpected result is a finding to investigate, not a mistake to conceal.

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A | 25 | Exact recursion; parity; call count |
| B | 25 | Wallis product; errors, ratios, scaled error |
| C | 25 | Order of convergence; practicality; contrast with Lab 0 |
| D | 15 | The squeeze, and why the product converges to $\pi/2$ |
| E | 10 | Interpretation |
| **Total** | **100** | |

---

*A formula can be exact, elegant, historically important, and completely impractical — all at once. Part C is where you find out which of those matter to a computation.*
