# MATH 141 · Week 7
## LAB 07 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed, not estimated.** Grade the *reasoning*, not agreement to the
> last decimal place.

*(Revised 2026-09-26 to match the 6-question version of the lab.)*

---

## Part 1 — Growth Rate Hierarchies

**Q1 (20).** Slowest to fastest: $\ln x$, $x$, $x^2$, $e^x$.

| x | ln x / x | x² / eˣ |
|---|---|---|
| 10 | 0.2302585 | 4.54 × 10⁻³ |
| 20 | 0.1497866 | 8.24 × 10⁻⁷ |
| 50 | 0.0782405 | 4.82 × 10⁻¹⁹ |

L'Hôpital: $\frac{\ln x}{x} \to \frac{1/x}{1} \to 0$; $\frac{x^2}{e^x} \to \frac{2x}{e^x} \to \frac{2}{e^x} \to 0$ (twice).
$O(\log n)$: binary search (CS 101 Lecture 16). $O(n^2)$: selection or insertion sort (Lecture 17).

*A student who extends the loop to $x = 1000$ gets `OverflowError` from `math.exp(1000)`. Accept a remark
on it; don't require it.*

---

## Part 2 — Curve Sketching

**Q2 (10).** Domain $(0, \infty)$. $x\ln x = \dfrac{\ln x}{1/x}$, form $-\infty/\infty$; L'Hôpital gives
$\dfrac{1/x}{-1/x^2} = -x \to 0$. So $\lim_{x\to0^+} x\ln x = 0$. As $x \to \infty$, $x\ln x \to \infty$.

**Q3 (20).** $g'(x) = \ln x + 1$, zero at $x = 1/e \approx 0.368$. Decreasing on $(0, 1/e)$, increasing on
$(1/e, \infty)$. $g''(x) = 1/x > 0$, so concave up everywhere, with no inflection points. By either test,
$x = 1/e$ is a local minimum, and the absolute minimum is $g(1/e) = -1/e \approx -0.3679$.

---

## Part 3 — Optimization

**Q4 (25).** $C(x) = 5000\sqrt{x^2 + 25} + 3000(10 - x)$.

$C'(x) = \dfrac{5000x}{\sqrt{x^2+25}} - 3000 = 0 \Rightarrow 5x = 3\sqrt{x^2+25} \Rightarrow 16x^2 = 225
\Rightarrow x = 3.75$ km.

$C(0) = \$55{,}000$, $C(3.75) = \$50{,}000$, $C(10) = \$55{,}902$. The minimum is **\$50,000**, with the cable
coming ashore 3.75 km from $P$.

**Q5 (15).**

| n | best x | V(best x) |
|---|---|---|
| 10 | 1.8 | 127.008 |
| 100 | 1.98 | 127.990368 |
| 10000 | 1.9998 | 127.99999904 |

The error in $x$ is at most one step, $6/n$. For $n = 10000$ the step is $0.0006$, and $2$ is not a whole
number of steps from $0$ ($2/0.0006 = 3333.3\ldots$), so the grid has no point at $2$. Rounding in
`a + i * step` also means the printed $x$ is not always exactly a grid multiple.

**Q6 (10).** Calculus gives the **exact** optimum, a proof that it is optimal, and a formula that works for
every version of the problem. Grid search needs many evaluations for a few digits: each extra digit costs
10 times the work. It also cannot prove it has found the best point, and can miss a narrow peak between
grid points. Grid search is still practical when $f$ has no formula (a simulation or a measurement), when
$f'$ is hard to find or solve, or when a rough answer is enough.

---

## Marking Scheme

- **Method (≈60%).** Hand analysis before the Desmos check, endpoint comparison in Q4, and a reason for
  each observation.
- **Execution (≈40%).** Correct values, and conclusions that follow from them.

---

*MATH 141 · Week 7 · Lab Solutions · Instructor Copy · © CSE Department*
