# MATH 141 · Calculus I
## Lab 06
### Visualizing Extrema, the Mean Value Theorem, and L'Hôpital's Rule

**Date:** Friday 6 November 2026 · 15:00–16:50 · Lab Section (Week 6) — covers Week 6 (Lectures 01–03)  
**Duration:** 2 hours | **Tools:** Desmos, Python (optional)
**Submission:** Written report due Monday 9 November 2026, 17:00 (Week 7)

> *Revised 2026-09-21.* The old Part 3 (reading $f''$ for concavity) and Part 4 (when the Second
> Derivative Test fails) used Week 7 material. Part 3 now uses $f$ and $f'$ only, and Part 4 checks
> L'Hôpital's Rule numerically.

---

## Lab Objectives

1. Visualize the Extreme Value Theorem and see why its hypotheses matter
2. See the Mean Value Theorem geometrically — the parallel secant/tangent lines
3. Read increasing/decreasing and local extrema from the graphs of $f$ and $f'$ side by side
4. Check L'Hôpital's Rule numerically
5. Build a numerical root-counting tool using Rolle's Theorem logic

---

## Part 1 — The Extreme Value Theorem: Why Every Hypothesis Matters (20 min)

### Exercise 1.1 — Breaking Continuity

In Desmos, graph:
$$f(x) = \begin{cases} x & 0 \leq x < 1 \\ 0 & x = 1 \end{cases}$$

(You can approximate this with a piecewise function in Desmos using curly braces syntax.)

**Question 1a:** Does this function have an absolute maximum on $[0,1]$? Explain using the graph.

**Question 1b:** Which hypothesis of the EVT fails? Where exactly does the failure occur?

### Exercise 1.2 — Breaking the Closed Interval

Graph $f(x) = x$ on the **open** interval $(0,1)$ (in Desmos, restrict the domain using `{0<x<1}`).

**Question 1c:** Does this function attain a maximum value on $(0,1)$? What is the supremum (least upper bound)? Is it attained?

**Question 1d:** Now change to the closed interval $[0,1]$. Does the EVT now guarantee a maximum? What is it?

### Exercise 1.3 — Breaking Boundedness

Graph $f(x) = x$ on $[0, \infty)$.

**Question 1e:** Is this function continuous on a "closed" set? Does it have an absolute maximum? Why does the EVT not apply here?

---

## Part 2 — The Mean Value Theorem: Geometric Visualization (30 min)

### Exercise 2.1 — Finding the Parallel Tangent

Consider $f(x) = x^3 - x$ on $[-1, 2]$.

**Step 1:** In Desmos, graph $f(x)$.

**Step 2:** Compute the secant line slope: $m = \dfrac{f(2)-f(-1)}{2-(-1)}$.

**Step 3:** Graph the secant line through $(-1, f(-1))$ and $(2, f(2))$.

**Question 2a:** Solve $f'(c) = m$ for $c \in (-1, 2)$ algebraically.

**Question 2b:** Add the tangent line at $x = c$ to Desmos: $y = f(c) + f'(c)(x-c)$. Verify visually that this tangent line is **parallel** to the secant line (same slope).

**Question 2c:** Are there multiple values of $c$ satisfying the MVT conclusion for this function on this interval? If so, find all of them and add all corresponding tangent lines to your graph.

### Exercise 2.2 — MVT and Average Velocity

A ball is thrown, and its height (in meters) is $h(t) = -4.9t^2 + 20t + 1$ for $t \in [0, 3]$ (seconds).

**Question 2d:** Compute the average velocity over $[0,3]$: $\dfrac{h(3)-h(0)}{3-0}$.

**Question 2e:** Find the time $c$ at which the instantaneous velocity $h'(c)$ equals this average velocity.

**Question 2f:** In Desmos, graph $h(t)$, the secant line, and the tangent line at $t=c$. Interpret physically: at time $c$, what is special about the ball's motion?

**Question 2g:** Graph the velocity function $v(t) = h'(t)$ separately. Mark the point $(c, v(c))$ and the horizontal line $y = \text{average velocity}$. Confirm they intersect at $t=c$.

---

## Part 3 — $f$ and $f'$ Side by Side (25 min)

### Exercise 3.1

Consider $f(x) = x^4 - 4x^3 + 4x^2$.

**Step 1:** Compute $f'(x)$ by hand and factor it.

**Step 2:** In Desmos, graph $f$ and $f'$ in different colours on the same axes.

**Question 3a:** Identify every $x$-value where $f'(x) = 0$. At each, is $f$ increasing or decreasing on
either side? Is it a local max, a local min, or neither?

**Question 3b:** Fill in this table:

| Interval | Sign of $f'$ | $f$ increasing or decreasing? |
|----------|--------------|-------------------------------|
| | | |
| | | |
| | | |
| | | |

### Exercise 3.2 — Reading $f$ from $f'$

You are given ONLY $f'(x) = (x+2)(x-1)^2$ (no formula for $f$ itself).

**Question 3c:** Without finding $f(x)$, determine all critical numbers of $f$, the intervals where $f$ is
increasing or decreasing (MVT Corollary 3), and the classification of each critical number.

**Question 3d:** Many functions have this $f'$. By MVT Corollary 2, how are any two of them related?

---

## Part 4 — L'Hôpital's Rule Numerically (20 min)

**Question 4a:** Tabulate $\dfrac{e^h-1-h}{h^2}$ for $h = 0.1, 0.01, 0.001, 0.0001$. What value does it
approach? Confirm with L'Hôpital's Rule (applied twice).

**Question 4b:** Tabulate $\dfrac{\ln x}{\sqrt{x}}$ for $x = 10, 10^2, 10^4, 10^6$. What does it approach?
Confirm with L'Hôpital's Rule. What does this say about which of $\ln x$ and $\sqrt{x}$ grows faster?

**Question 4c:** In Desmos, graph $\dfrac{x+\sin x}{x}$ and $1+\cos x$ for $x$ up to 100. Use the picture to
explain why L'Hôpital's Rule cannot be used on the first, even though its limit exists.

---

## Part 5 — Numerical Root Counting via Rolle's Theorem (20 min)

### Exercise 5.1 — Automated Reasoning

Rolle's Theorem, used contrapositively, gives a root-counting technique: if $f'(x) \neq 0$ everywhere on an interval, $f$ has **at most one** root there (since two roots would force $f'=0$ somewhere between them by Rolle's Theorem).

**Question 5a:** Consider $f(x) = x^5 + 3x + 1$. Compute $f'(x)$. Show algebraically that $f'(x) > 0$ for all $x$ (hence never zero).

**Question 5b:** Using the IVT (Week 2) and the sign of $f(0)$ and evaluate $f$ at convenient points, show $f$ has at least one root.

**Question 5c:** Combine 5a and 5b via Rolle's Theorem logic to conclude $f$ has **exactly one** real root.

**Question 5d:** In Desmos, graph $f(x) = x^5+3x+1$ and visually confirm there is exactly one $x$-intercept.

**Question 5e (Pseudocode):** Write pseudocode for a function `count_roots_via_derivative(f, f_prime, a, b)` that:
1. Checks if `f_prime` changes sign on `[a,b]` (using many sample points)
2. If `f_prime` never changes sign, concludes "at most one root" in `[a,b]`
3. Uses the bisection method (Lab 02) to actually locate the root if `f(a)` and `f(b)` have opposite signs

---

## Lab Report Requirements

Include:
1. Answers to all questions
2. Desmos screenshots for Parts 1, 2, 3 and 4
3. The tables from Exercise 3.1 and Part 4
4. Pseudocode from Question 5e
5. **Reflection** (5–6 sentences): What is the most useful "reading" skill you developed today — going
   from $f'$ back to properties of $f$, or seeing a theorem's hypotheses fail in a picture?

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — EVT hypotheses | 15 |
| Part 2 — MVT visualization | 25 |
| Part 3 — $f$ and $f'$ side by side | 20 |
| Part 4 — L'Hôpital numerically | 20 |
| Part 5 — Root counting | 15 |
| Reflection | 5 |
| **Total** | **100** |
