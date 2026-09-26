# MATH 141 · Lab 04
## Rules, Chains, and Motion

**Duration:** 2 hours · **20 points**
**Date:** Friday 23 October 2026 · 15:00–16:50 · Lab Section (Week 4) — covers Week 4 (Lectures 01–03)
**Tools:** Desmos, and Python using only CS 101 Weeks 0–3: `def`, `for` over a list, and `math`
**Expected time:** the session itself (6 questions), plus at most 30 minutes to tidy your answers

---

## Overview

Three activities: check a differentiation rule numerically, watch the chain rule multiply rates, and
analyse a motion problem with graphs. Reuse your Lab 03 program: its `central(a, h)` function is the
only tool you need.

```python
import math

def f(x):
    return x**2 * math.sin(x)

def central(a, h):
    return (f(a + h) - f(a - h)) / (2 * h)

for h in [1e-2, 1e-4, 1e-6]:
    print(h, central(1, h))
```

---

## Part 1: Checking a Rule Numerically (3 pts)

### Question 1 (3 points)

Differentiate $f(x)=x^2\sin x$ by the product rule, and evaluate $f'(1)$ with `math.sin(1)` and
`math.cos(1)`. Run the program above. Does the central difference agree with your answer, and to how
many digits at $h = 10^{-6}$?

---

## Part 2: The Chain Rule, Seen (7 pts)

### Question 2 (3 points)

For $F(u)=u^5$ and $u=g(x)=x^2+1$, compute $\frac{dF}{du}$ at $u=g(1)$, $\frac{du}{dx}$ at $x=1$, and their
product. Check the product against `central(1, 1e-6)` with `f` changed to `(x**2 + 1)**5`. Explain in
one sentence why the rates multiply.

### Question 3 (4 points)

Let $f(x)=\sqrt{1+\sin(x^2)}$. Name its three layers from the outside in, then differentiate it with the
chain rule. Check your formula at $x=1$ with `central(1, 1e-6)`.

---

## Part 3: A Motion Analysis (10 pts)

A particle has position $s(t)=t^3-9t^2+24t$ metres on $0\le t\le5$.

### Question 4 (3 points)

Find $v(t)$ and $a(t)$ by hand, and factor $v$. Then write a `for` loop over `[0, 1, 2, 3, 4, 5]` that
prints $t$, $s(t)$, $v(t)$ and $a(t)$, and record the table.

### Question 5 (4 points)

In Desmos, graph $s$, $v$ and $a$ with $x$ as $t$ and the restriction `{0 <= x <= 5}`. Where $v = 0$, what
does the graph of $s$ do? Where $a = 0$, what does the graph of $v$ do? On which time intervals is the
particle speeding up, and why?

### Question 6 (3 points)

Find the displacement and the total distance over $[0, 5]$. Justify from the factored form of $v$ why
they differ.

---

## Deliverables

Your program and tables, the derivatives worked by hand, one Desmos screenshot or link for Question 5,
and written answers to Questions 1–6.

## Grading

| Part | Points |
|---|---|
| 1 — a rule checked numerically | 3 |
| 2 — chain rule decomposition and verification | 7 |
| 3 — motion analysis with justification | 10 |
| **Total** | **20** |

---

*Revised 2026-09-26: the lab repeated Problem Set 4. Its functions were PS 4's product and quotient drills
and its motion problem was PS 4 Part C, word for word. It now uses different functions, and its motion
problem is also not the Wednesday lecture's example. The floating-point question was cut, since Lab 03
Question 9 already asks it. 11 items became 6 questions.*

---

*MATH 141 · Week 4 · Lab 04 · © CSE Department*
