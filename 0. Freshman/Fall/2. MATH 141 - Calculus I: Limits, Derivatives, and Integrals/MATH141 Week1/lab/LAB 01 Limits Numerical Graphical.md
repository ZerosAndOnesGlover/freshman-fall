# MATH 141 · Calculus I
## Lab 01
### Numerical and Graphical Investigation of Limits

**Date:** Friday 2 October 2026 · 15:00–16:50 · Lab Section (Week 1) — covers Week 1 (Lectures 01–03)  
**Duration:** 2 hours | **Submission:** End of lab session + written report due Monday 5 October 2026, 11:00  
**Tools:** Desmos (desmos.com), Python (optional), pen and paper for proofs

---

## Lab Objectives

By the end of this lab you will:
1. Distinguish between limits that can be evaluated by substitution and those that cannot
2. Understand the limitations of numerical tables for limit estimation
3. Verify the two special trigonometric limits numerically and geometrically
4. Build intuition for the ε-δ definition

*(Revised 2026-09-21: the discontinuity-types and bisection parts need Week 2 — continuity and the IVT —
and were removed; they now belong to Lab 02.)*

---

## Part 1 — When Numerical Tables Lie (30 min)

One of the most important lessons in calculus: **numerical evidence is suggestive, not conclusive.** This part demonstrates that dramatically.

### Exercise 1.1 — A Deceptive Table

Consider $f(x) = \sin\!\left(\dfrac{\pi}{x}\right)$.

Fill in the table:

| $x$ | $f(x) = \sin(\pi/x)$ |
|-----|----------------------|
| 1 | |
| 0.5 | |
| 0.1 | |
| 0.01 | |
| 0.001 | |
| 0.0001 | |

**Question 1a:** Based on the table, what would you guess $\lim_{x \to 0} \sin(\pi/x)$ equals?

**Question 1b:** Now compute $f(2/n)$ for integer values $n = 1, 2, 3, 4, 5$. What do you observe?

**Question 1c:** Explain in one paragraph why $\lim_{x \to 0} \sin(\pi/x)$ does not exist, even though some tables might suggest a value. What is happening geometrically?

**Question 1d:** Graph $f(x) = \sin(\pi/x)$ on Desmos for $x \in [-0.5, 0.5]$. Describe what you see near $x = 0$.

---

### Exercise 1.2 — Round-Off Error in Limits

Consider $g(x) = \dfrac{\sqrt{1+x} - 1}{x}$.

The true limit is $\lim_{x \to 0} g(x) = \dfrac{1}{2}$ (you'll prove this in Problem Set 1 using rationalization).

Fill in the table using a calculator:

| $x$ | $g(x)$ (calculator) | $g(x)$ (rationalized form) |
|-----|--------------------|-----------------------------|
| $0.1$ | | |
| $0.01$ | | |
| $0.001$ | | |
| $0.0001$ | | |
| $0.00001$ | | |
| $0.000001$ | | |
| $0.0000001$ | | |

The rationalized form is $g(x) = \dfrac{1}{\sqrt{1+x}+1}$ (derive this yourself first).

**Question 1e:** At what point does the calculator column start behaving unexpectedly? Why does this happen? (Think about floating-point precision — the difference of two nearly-equal numbers.)

**Question 1f:** Which form — the original or rationalized — is more numerically stable as $x \to 0$? Why?

> **CS Connection:** This exercise demonstrates **catastrophic cancellation** — a critical concept in numerical computing. When two nearly-equal floating-point numbers are subtracted, significant digits are lost. The rationalized form avoids this by eliminating the subtraction. This is why numerical analysts always seek algebraically equivalent forms that avoid subtracting nearly-equal quantities.

---

## Part 3 — Verifying the Special Trigonometric Limits (20 min)

### Exercise 3.1 — Numerical Verification

Fill in the table for $f(x) = \dfrac{\sin x}{x}$ (with $x$ in radians):

| $x$ | $\sin x$ | $\sin x / x$ |
|-----|----------|--------------|
| $1.0$ | | |
| $0.5$ | | |
| $0.1$ | | |
| $0.01$ | | |
| $0.001$ | | |
| $-0.1$ | | |
| $-0.01$ | | |

**Question 3a:** What value does $\dfrac{\sin x}{x}$ appear to approach as $x \to 0$?

**Question 3b:** Graph $\dfrac{\sin x}{x}$ on Desmos. Note that Desmos will show a filled dot at $x = 0$ — why is this misleading? (Desmos is computing a limit, not $f(0)$.)

### Exercise 3.2 — Geometric Verification

On paper (or using Desmos geometry tools), draw a unit circle with a small angle $\theta > 0$.

Mark:
- Point $A = (1, 0)$
- Point $P = (\cos\theta, \sin\theta)$ on the circle
- Point $T = (1, \tan\theta)$ where the tangent line at $A$ meets the line $OP$

Compute and compare the three areas:
- Triangle $OAP$: area $= \dfrac{1}{2}\cos\theta\sin\theta$
- Circular sector $OAP$: area $= \dfrac{1}{2}\theta$
- Triangle $OAT$: area $= \dfrac{1}{2}\tan\theta$

**Question 3c:** Write the inequality chain relating these three areas.

**Question 3d:** Divide through by $\dfrac{1}{2}\sin\theta$ and take the reciprocal to get $\cos\theta \leq \dfrac{\sin\theta}{\theta} \leq \dfrac{1}{\cos\theta}$.

**Question 3e:** Apply the Squeeze Theorem to conclude $\lim_{\theta \to 0^+} \dfrac{\sin\theta}{\theta} = 1$.

---

## Part 5 — Open Investigation: Building Intuition for ε-δ (20 min)

### Exercise 5.1 — Interactive Epsilon-Delta

In Desmos, graph $f(x) = 2x + 1$ and the horizontal lines $y = 5 - \varepsilon$ and $y = 5 + \varepsilon$.

Set $\varepsilon = 0.5$ using a Desmos slider.

**Question 5a:** By inspecting the graph, estimate the largest $\delta$ such that when $|x - 2| < \delta$, we have $|f(x) - 5| < 0.5$.

**Question 5b:** Now find the exact $\delta$ algebraically from $\varepsilon = 0.5$. Does it match your graphical estimate?

**Question 5c:** Decrease $\varepsilon$ to $0.1$, then $0.01$, then $0.001$. What is the pattern relating $\varepsilon$ and $\delta$?

**Question 5d:** Now try $f(x) = x^2$ and the limit $\lim_{x \to 2} x^2 = 4$. With $\varepsilon = 0.5$, graphically estimate $\delta$. Then check against the algebraic result $\delta = \min(1, \varepsilon/5)$ from Tuesday's lecture.

---

## Lab Report Requirements

Submit a typed or handwritten report containing:

1. **Completed tables** from Parts 1 and 3
2. **Written answers** to all Questions (label each clearly)
3. **Desmos screenshot** for Exercise 3.2
4. **Reflection paragraph** (5–8 sentences): What was the most surprising thing you discovered in this lab? What does it tell you about the relationship between numerical evidence and mathematical proof?

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — Deceptive tables | 35 |
| Part 3 — Trig limits | 35 |
| Part 5 — ε-δ exploration | 20 |
| Reflection | 10 |
| **Total** | **100** |
