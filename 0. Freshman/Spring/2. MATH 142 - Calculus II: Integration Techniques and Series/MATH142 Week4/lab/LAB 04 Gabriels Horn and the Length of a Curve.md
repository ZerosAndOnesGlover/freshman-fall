# MATH 142 · Calculus II
## Lab 04: Gabriel's Horn, and the Length of a Curve
### Week 4 Lab Session

---

**Duration:** 2 hours
**Format:** Individual or pairs (pairs submit separate reports)
**Graded on:** completion + correctness — **100 points**
**Tools required:** Python 3 with `mpmath` and `sympy`

---

## Overview

This lab has two halves, and each combines this week's geometry with an earlier week's analysis.

**Part A–C: Gabriel's Horn.** Rotate $y=\tfrac1x$ for $x\ge1$ about the $x$-axis. The resulting solid has **finite volume and infinite surface area** — which sounds impossible, and is not. Deciding both facts uses Week 3's $p$-test and comparison test; the apparent paradox has a resolution, and finding it is the point.

**Part D: the length of a curve.** Lecture 3 derived arc length by replacing a curve with an inscribed polygon. This half **measures how fast the polygon converges**, and finds — unlike Labs 1 and 3 — that the answer is very satisfactory.

---

## Part A — The Horn's Volume and Surface (25 pts)

Let $H$ be the solid obtained by rotating $y=\dfrac1x$, $x\ge1$, about the $x$-axis.

**A1 (8 pts).** Write down the improper integral for the **volume** of $H$, evaluate it, and state which test from Week 3 guarantees convergence.

**A2 (10 pts).** Write down the improper integral for the **surface area** of $H$.

Then prove it **diverges**, using a **direct comparison** from Week 3. *(Hint: what is the smallest that $\sqrt{1+x^{-4}}$ can be?)*

State clearly which comparison function you used and why the comparison points the correct way.

**A3 (7 pts).** Verify both symbolically with `sympy`. Report exactly what it returns for each.

---

## Part B — Truncating the Horn (25 pts)

Let $H_T$ be the horn cut off at $x=T$.

**B1 (10 pts).** Derive closed forms for $V(T)$ and, if you can, for $S(T)$. *(The volume has a simple closed form. The surface does not — compute it numerically.)*

Tabulate both for $T = 10,\ 10^2,\ 10^3,\ 10^4,\ 10^6$.

**B2 (8 pts).** Add a column with $2\pi\ln T$ — the lower bound from your A2 comparison — and a column with the ratio $S(T)/(2\pi\ln T)$.

What does the ratio appear to approach? Explain why that is the value you should expect, in terms of the factor $\sqrt{1+x^{-4}}$.

**B3 (7 pts).** From your table:

- (a) How close is $V(T)$ to its limit at $T=10^6$?
- (b) How large is $S(T)$ at $T=10^6$?
- (c) **Which of these two is the numerically obvious one?** Relate your answer to Lab 3's finding about logarithmic divergence.

---

## Part C — The Painter's Paradox (15 pts)

Here is the puzzle, stated the way it is usually stated:

> *The horn holds exactly $\pi$ cubic units of paint. So pour $\pi$ units of paint into it, and the
> inside surface is now covered. But the inside surface has infinite area, and no finite amount of
> paint can cover an infinite area. Contradiction.*

**C1 (8 pts).** **Resolve it.** The argument contains a specific false step; identify it and say precisely why it is false.

*Think about what "covering a surface with paint" means physically, and what quantity it actually requires.*

**C2 (7 pts).** Make the resolution quantitative.

Suppose you coat the inside with a layer of paint of **constant thickness $d$**.

- (a) At what value of $x$ does the horn's radius drop below $d$?
- (b) What does that mean for the layer beyond that point?
- (c) Hence explain why "filling the horn" and "painting its surface" are **not** the same operation, and why only one of them requires finite volume.

---

## Part D — How Fast Does a Polygon Become a Curve? (25 pts)

Lecture 3 defined arc length as a limit of inscribed polygons. Take $y=x^2$ on $[0,1]$, whose exact length is

$$L = \frac{\sqrt5}{2}+\frac{\operatorname{arcsinh}2}{4} = 1.4789428575445975\ldots$$

Define $L_n$ = the length of the inscribed polygon with $n$ equal steps in $x$:

$$L_n = \sum_{i=0}^{n-1}\sqrt{(x_{i+1}-x_i)^2+\big(x_{i+1}^2-x_i^2\big)^2}, \qquad x_i = \frac in$$

**D1 (8 pts).** Implement $L_n$ and tabulate it for $n=2,4,8,\ldots,512$, alongside the **signed** error $L - L_n$.

**D2 (7 pts).** Add a column of consecutive error ratios. State the **order of convergence** and justify it from your data, as in Labs 0 and 3.

**D3 (5 pts).** Add a column of $n^2\times(\text{error})$. Report the constant it approaches.

**D4 (5 pts).** Every error in your table has the **same sign**.

- (a) Which sign, and therefore does $L_n$ over- or under-estimate?
- (b) Give a one-line geometric reason why this must be so for **every** curve and every $n$, not just this example.

---

## Part E — Reflection (10 pts)

**E1 (5 pts).** Across four labs, numerics has fared very differently:

| Lab | Verdict |
|---|---|
| 0 | numerics won — 10 digits from 128 points |
| 1 | numerics worked, $6\times10^7$ times too slowly |
| 2 | numerics gave the value but not the proof |
| 3 | numerics could not answer at all |
| **4** | **?** |

Fill in the entry for **Part D** of this lab, and say which earlier lab it most resembles.

**E2 (5 pts).** Part A proved two things about an object nobody can build, using integrals over an infinite interval. Part D measured something you could check with a ruler.

**Which half of this lab could have been done numerically alone, and which could not?** Answer in one or two sentences, referring to the kind of statement each half establishes.

---

## What to Submit

1. Both improper integrals, evaluated, with the tests named (Part A)
2. The truncation table with the bound and ratio (Part B)
3. Your resolution of the paradox, qualitative and quantitative (Part C)
4. The polygon table with errors, ratios, scaled errors, and signs (Part D)
5. Parts E1 and E2

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A | 25 | Both improper integrals; comparison done correctly |
| B | 25 | Truncation, the logarithmic bound, and what is visible |
| C | 15 | Resolving the paradox, and making it quantitative |
| D | 25 | Order of convergence of the inscribed polygon |
| E | 10 | What each half establishes |
| **Total** | **100** | |

---

*A solid with finite volume and infinite surface is not a contradiction. It is a statement that two different integrals of the same curve land on opposite sides of the $p=1$ threshold — which is exactly what Week 3 was about.*
