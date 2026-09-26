# MATH 141 · Calculus I
## Lab 06
### Visualizing Extrema, the Mean Value Theorem, and L'Hôpital's Rule

**Date:** Friday 6 November 2026 · 15:00–16:50 · Lab Section (Week 6) — covers Week 6 (Lectures 01–03)  
**Duration:** 2 hours | **Tools:** Desmos, and Python using only CS 101 Weeks 0–3 (`for` over a list, `math`)
**Expected time:** the session itself (7 questions), plus at most 30 minutes to tidy your answers
**Submission:** Written report due Monday 9 November 2026, 17:00 (Week 7)

> *Revised 2026-09-21.* The old Part 3 (reading $f''$ for concavity) and Part 4 (when the Second
> Derivative Test fails) used Week 7 material. Part 3 now uses $f$ and $f'$ only, and Part 4 checks
> L'Hôpital's Rule numerically.
>
> *Revised 2026-09-26.* Cut from five parts and about 25 questions to 7. Part 3 still asked for each
> critical number to be classified as a local max or min. That is the First Derivative Test (Week 7), so
> Part 3 now asks only where $f$ increases and decreases (MVT Corollary 3). Part 4 used Problem Set 6's own
> limits and now uses a different one. Part 5 (root counting and pseudocode) repeated Problem Set 6,
> Problem 3, and was removed.

---

## Lab Objectives

1. See why every hypothesis of the Extreme Value Theorem matters
2. See the Mean Value Theorem geometrically: a tangent parallel to a secant
3. Read where $f$ increases and decreases from the sign of $f'$
4. Check a L'Hôpital limit numerically, and see where the rule does not apply

---

## Part 1 — The Extreme Value Theorem (15 min)

### Question 1 (15 points)

Graph each in Desmos and say whether it has an absolute maximum on the given set. If it has none, name the
hypothesis of the EVT that fails.

**(a)** $f(x) = x$ for $0 \le x < 1$ and $f(1) = 0$. Type `y = x {0 <= x < 1}` and the point `(1, 0)`.

**(b)** $f(x) = x$ on the open interval $(0, 1)$: `y = x {0 < x < 1}`. What is the least upper bound of its
values, and is it attained?

**(c)** $f(x) = x$ on $[0, \infty)$.

---

## Part 2 — The Mean Value Theorem (35 min)

### Question 2 (15 points)

Let $f(x) = x^3 - x$ on $[-1, 2]$. Compute the secant slope $m = \dfrac{f(2)-f(-1)}{2-(-1)}$ and graph $f$ and
the secant line. Solve $f'(c) = m$ for $c$ in $(-1, 2)$. Add the tangent line $y = f(c) + f'(c)(x-c)$ for each
such $c$, and check it is parallel to the secant. How many values of $c$ are there?

### Question 3 (15 points)

A ball's height is $h(t) = -4.9t^2 + 20t + 1$ metres for $0 \le t \le 3$ seconds. Compute the average velocity
over $[0, 3]$, and find the time $c$ at which the instantaneous velocity equals it. Graph $h$, the secant and
the tangent at $t = c$. What does the MVT say about the ball's motion at that moment?

---

## Part 3 — $f$ and $f'$ Side by Side (30 min)

### Question 4 (15 points)

Let $f(x) = x^4 - 4x^3 + 4x^2$. Compute $f'(x)$ by hand and factor it. Graph $f$ and $f'$ in different
colours, and fill in the table using MVT Corollary 3 (Lecture 02):

| Interval | Sign of $f'$ | $f$ increasing or decreasing? |
|----------|--------------|-------------------------------|
| | | |
| | | |
| | | |
| | | |

### Question 5 (10 points)

You are given only $f'(x) = (x+2)(x-1)^2$. Without finding $f$, find its critical numbers and the
intervals where $f$ increases and decreases. Many functions have this derivative: by MVT Corollary 2, how
are any two of them related?

---

## Part 4 — L'Hôpital's Rule Numerically (25 min)

### Question 6 (15 points)

Use a `for` loop over `[0.1, 0.01, 0.001]` to print $\dfrac{1-\cos x}{x^2}$. What value does it approach?
Confirm it with L'Hôpital's Rule, applied twice. Then try `1e-8`. What goes wrong, and why? (Lab 01 met
the same problem.)

### Question 7 (15 points)

$\displaystyle\lim_{x\to\infty}\frac{x+\sin x}{x}$ has the form $\infty/\infty$. Graph $\dfrac{x+\sin x}{x}$ and
$1+\cos x$ (the ratio of the derivatives) for $0 < x \le 100$. What does each do as $x$ grows? Explain why
L'Hôpital's Rule gives no answer here, even though the original limit exists, and find that limit another
way.

---

## Lab Report Requirements

Include your program and output, Desmos screenshots or links for Questions 1–4 and 7, the table from
Question 4, and answers to Questions 1–7.

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — EVT hypotheses | 15 |
| Part 2 — MVT visualization | 30 |
| Part 3 — $f$ and $f'$ side by side | 25 |
| Part 4 — L'Hôpital numerically | 30 |
| **Total** | **100** |
