# MATH 141 · Calculus I
## Lab 01
### Numerical and Graphical Investigation of Limits

**Date:** Friday 2 October 2026 · 15:00–16:50 · Lab Section (Week 1) — covers Week 1 (Lectures 01–03)  
**Duration:** 2 hours | **Submission:** End of lab session + written report due Monday 5 October 2026, 11:00  
**Tools:** Desmos (see the Lab 00 table) and the Python REPL, using only CS 101 Weeks 0–1: arithmetic,
variables and the `math` module (CS 101 Lecture 06, this morning). No loops or functions are needed.
**Expected time:** the session itself (11 questions), plus at most 30 minutes to tidy your answers.

---

## Lab Objectives

By the end of this lab you will:
1. Understand why a table of values can suggest a limit but never prove one
2. See floating-point round-off spoil a limit, and fix it with algebra
3. Check $\lim_{x\to 0} \frac{\sin x}{x} = 1$ numerically
4. Build intuition for the ε-δ definition with Desmos sliders

---

## Python for Today

Everything is one line at a time at the `>>>` prompt. Use the up arrow to repeat a line with a new `x`.

```python
>>> import math
>>> x = 0.1
>>> math.sin(math.pi / x)
-1.2246467991473533e-15
>>> (math.sqrt(1 + x) - 1) / x
0.4880884817015163
```

- `1e-8` means $1 \times 10^{-8}$, and Python prints very small or large results the same way:
  `-1.22e-15` is $-0.00000000000000122$, which is zero apart from round-off.
- `math.sin` and `math.cos` work in **radians**, which is what calculus needs.

---

## Part 1 — When Numerical Tables Lie (40 min)

### Exercise 1.1 — A Deceptive Table

Let $f(x) = \sin\!\left(\dfrac{\pi}{x}\right)$. Compute it at $x = 1$, $0.1$, $0.01$ and $0.001$.

| $x$ | $f(x) = \sin(\pi/x)$ |
|-----|----------------------|
| 1 | |
| 0.1 | |
| 0.01 | |
| 0.001 | |

### Question 1 (9 points)

Based only on the table, what would you guess $\lim_{x \to 0} \sin(\pi/x)$ is?

### Question 2 (9 points)

Now compute $f$ at $x = 2/401$ and at $x = 2/403$. Both are within $0.005$ of $0$. What do you get, and what does that do to your guess?

### Question 3 (9 points)

Graph $y = \sin(\pi/x)$ in Desmos for $-0.5 \le x \le 0.5$. Describe what happens near $x = 0$, and explain in a few sentences why $\lim_{x \to 0} \sin(\pi/x)$ does not exist.

### Exercise 1.2 — Round-Off Error

Let $g(x) = \dfrac{\sqrt{1+x} - 1}{x}$. Its limit as $x \to 0$ is $\dfrac{1}{2}$ (Problem Set 1, Problem 1(b), shows the same method).

First, rationalize by hand to show $g(x) = \dfrac{1}{\sqrt{1+x}+1}$ for $x \neq 0$. Then fill in the table using `(math.sqrt(1 + x) - 1) / x` and `1 / (math.sqrt(1 + x) + 1)`.

| $x$ | original form | rationalized form |
|-----|---------------|-------------------|
| `1e-4` | | |
| `1e-8` | | |
| `1e-12` | | |
| `1e-15` | | |

### Question 4 (9 points)

Where does the original form start to go wrong? Explain why, using what CS 101 Lecture 04 §4 says about floating-point numbers: what happens when you subtract two nearly equal numbers?

### Question 5 (9 points)

Which form is more trustworthy as $x \to 0$, and why? What does this say about the algebra you do to find a limit?

---

## Part 2 — The Limit of $\frac{\sin x}{x}$ (30 min)

Fill in the table with `math.sin(x) / x`.

| $x$ | $\sin x / x$ |
|-----|--------------|
| $0.5$ | |
| $0.1$ | |
| $0.01$ | |
| $-0.1$ | |

### Question 6 (8 points)

What value does $\dfrac{\sin x}{x}$ appear to approach as $x \to 0$? Why do $x = 0.1$ and $x = -0.1$ give the same value?

### Question 7 (8 points)

Graph $y = \sin(x)/x$ in Desmos. It draws an unbroken curve through $x = 0$. Now type `sin(0)/0` into Desmos. What does it say, and why is the unbroken picture misleading?

### Question 8 (9 points)

Lecture 02 §4 proves $\cos x \leq \dfrac{\sin x}{x} \leq \dfrac{1}{\cos x}$ for small $x > 0$. Compute `math.cos(0.1)` and `1 / math.cos(0.1)`, and check the chain at $x = 0.1$ against your table. Then explain in two sentences how the Squeeze Theorem turns this chain into $\lim_{x\to 0^+} \frac{\sin x}{x} = 1$.

---

## Part 3 — Building Intuition for ε-δ (30 min)

In Desmos, graph $f(x) = 2x + 1$ and the lines $y = 5 - e$ and $y = 5 + e$, with a slider for $e$ (Desmos has no ε key; $e$ plays its role). Also graph the vertical lines $x = 2 - d$ and $x = 2 + d$ with a slider for $d$ (this is δ).

### Question 9 (10 points)

Set $e = 0.5$. Move $d$ to find the largest $\delta$ for which every $x$ with $|x - 2| < \delta$ has $|f(x) - 5| < 0.5$. Then find the exact $\delta$ algebraically. Do they agree?

### Question 10 (10 points)

Repeat with $e = 0.1$ and $e = 0.01$. What rule gives $\delta$ from $\varepsilon$ for this function, and why?

### Question 11 (10 points)

Change $f$ to $f(x) = x^2$ and the lines to $y = 4 \pm e$, for $\lim_{x \to 2} x^2 = 4$. With $e = 0.5$, estimate the largest $\delta$ from the graph. Compare it with $\delta = \min(1, \varepsilon/5)$ from Lecture 02 Example 2. Is the lecture's $\delta$ larger or smaller than the largest possible one, and does that matter for the proof?

---

## Lab Report Requirements

Write your answers under Questions 1–11 in your answer sheet. Include:

1. **The three completed tables**, and the hand rationalization before the Exercise 1.2 table
2. **One Desmos screenshot or link** for Question 3 and one for Part 3

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — Deceptive tables and round-off (Questions 1–5) | 45 |
| Part 2 — $\sin x / x$ (Questions 6–8) | 25 |
| Part 3 — ε-δ exploration (Questions 9–11) | 30 |
| **Total** | **100** |

---

*Revised 2026-09-21: the discontinuity-types and bisection parts need Week 2 (continuity and the IVT) and were
removed. Revised 2026-09-26: the lab now uses only Week 0–1 Python and Desmos, and was cut from 15 questions,
five long tables, a geometric construction and a reflection to 11 questions and three short tables, so it
fits the session.*
