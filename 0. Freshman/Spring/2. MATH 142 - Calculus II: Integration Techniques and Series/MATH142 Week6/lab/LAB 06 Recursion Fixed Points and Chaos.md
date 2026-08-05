# MATH 142 · Calculus II
## Lab 06: Recursion, Fixed Points, and Chaos
### Week 6 Lab Session

---

**Duration:** 2 hours
**Format:** Individual or pairs (pairs submit separate reports)
**Graded on:** completion + correctness — **100 points**
**Tools required:** Python 3 with `mpmath` (you will need far more than 15 digits)

---

## Overview

A recursive sequence $a_{n+1}=g(a_n)$ **is a loop**. This lab is about a single question with a startlingly precise answer:

> **Given the rule $g$, how fast does the loop converge — and does it converge at all?**

Lecture 3 claimed the answer is governed by one number: $g'$ at the fixed point. This lab measures that claim in three regimes.

- **Part A–B:** $g'(L)=0$ — **quadratic** convergence, digits doubling every step.
- **Part C:** $0<|g'(L)|<1$ — **linear** convergence, a constant factor per step.
- **Part D:** $|g'(L)|>1$ — **no convergence at all**, and something much stranger.

**Set `mp.mp.dps = 60`.** Part B reaches 48 correct digits in six steps and `float` will not show it.

---

## Part A — The Babylonian Method (20 pts)

To compute $\sqrt2$, iterate

$$a_{n+1} = \frac12\left(a_n+\frac{2}{a_n}\right),\qquad a_0 = 1$$

This is roughly 3,700 years old and is essentially what your computer's `sqrt` still does.

**A1 (6 pts).** Find the fixed points of $g(x)=\frac12\left(x+\frac2x\right)$ by solving $L=g(L)$. Which one does the iteration approach from $a_0=1$?

**A2 (8 pts).** Compute $g'(x)$ by hand and evaluate it at the positive fixed point.

**Report the exact value.** What does Lecture 3 §5 predict from it?

**A3 (6 pts).** Explain, from the fixed point criterion, why this iteration should converge **quadratically** rather than linearly.

---

## Part B — Measuring Quadratic Convergence (25 pts)

**B1 (10 pts).** Run the iteration from $a_0=1$ for 7 steps at 60-digit precision. Tabulate $a_n$ and the error $|a_n-\sqrt2|$.

**B2 (8 pts).** Add a column of $\dfrac{e_n}{e_{n-1}^2}$.

It converges to a constant. **Report it, and identify it exactly** — it is a simple expression in $\sqrt2$.

**B3 (7 pts).** Add a column giving the **number of correct decimal digits** at each step (i.e. $\lfloor-\log_{10}e_n\rfloor$).

- (a) Describe the pattern.
- (b) How many steps would be needed for 1000 correct digits? Justify from the pattern, not by running it.
- (c) Compare with Lab 1's Wallis product, which needed about $8\times10^9$ factors for 10 digits.

---

## Part C — Linear Convergence, for Contrast (20 pts)

Here is a different iteration with the same fixed point $\sqrt2$:

$$a_{n+1} = a_n - \frac{a_n^2-2}{4}, \qquad a_0=1$$

**C1 (6 pts).** Verify that $\sqrt2$ is a fixed point. Compute $g'(x)$ and evaluate at $\sqrt2$, **exactly**.

**C2 (8 pts).** Run it for 9 steps. Tabulate the error and the **ratio of consecutive errors** $\dfrac{e_{n-1}}{e_n}$.

Report the constant the ratio approaches, and check it against $\dfrac{1}{|g'(\sqrt2)|}$.

**C3 (6 pts).** Both iterations converge to $\sqrt2$ and both use only arithmetic.

- (a) Roughly how many steps does each need for 12 correct digits?
- (b) **What single feature of $g$ accounts for the difference?**

---

## Part D — When the Fixed Point Repels: The Logistic Map (25 pts)

Now a rule where $|g'|>1$. The **logistic map** models a population with limited resources:

$$x_{n+1} = r\,x_n(1-x_n), \qquad x_0 = 0.5,\quad 0<r\le4$$

**D1 (6 pts).** Show that the non-zero fixed point is $x^\ast = 1-\dfrac1r$, and that

$$g'(x^\ast) = 2-r$$

**D2 (7 pts).** From the criterion $|g'(x^\ast)|<1$, determine the exact range of $r$ for which the fixed point is **stable**.

**D3 (12 pts).** For $r = 2.5,\ 3.2,\ 3.5,\ 3.55,\ 3.9$: iterate 2000 times to discard the transient, then print the next 8 values.

For each $r$, report whether the orbit settles to a **single value**, a **repeating cycle** (state its length), or **neither**.

Then answer:

- (a) At which of your $r$ values is the fixed point stable, and does that match D2?
- (b) What happens at $r=3.2$, just past the stability threshold?
- (c) Describe the pattern as $r$ increases through your values.
- (d) At $r=3.9$ the orbit never repeats. **Note that the rule is a deterministic quadratic with no randomness in it whatsoever.** Comment in two or three sentences on what that implies about predicting such a system.

---

## Part E — Reflection (10 pts)

**E1 (5 pts).** Lecture 3 said convergence speed is governed by $g'(L)$. Your three parts tested $g'(L)=0$, $0<|g'(L)|<1$, and $|g'(L)|>1$.

Summarise in a small table: the value of $g'(L)$, the behaviour, and the evidence from your data.

**E2 (5 pts).** Across six labs, the relationship between exact and numerical methods has varied. Where does this lab sit?

*In particular: Part B produced 48 correct digits of an irrational number in six steps of arithmetic. Does that count as a numerical method winning, or as an exact method?*

---

## What to Submit

1. Fixed points and derivatives, by hand (Parts A, C1, D1)
2. The quadratic convergence table with the ratio and digit columns (Part B)
3. The linear convergence table with its ratio (Part C)
4. Your logistic map orbits and answers (Part D)
5. Parts E1 and E2

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A | 20 | Fixed point and derivative, by hand |
| B | 25 | Measuring quadratic convergence |
| C | 20 | Linear convergence, for contrast |
| D | 25 | Instability, period doubling, chaos |
| E | 10 | The unifying criterion |
| **Total** | **100** | |

---

*Three iterations, one criterion, and outcomes ranging from 48 digits in six steps to a system nobody can predict. All of it is one derivative.*
