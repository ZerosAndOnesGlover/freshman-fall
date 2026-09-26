# MATH 141 · Lab 02
## Continuity, Discontinuity, and Bisection

**Duration:** 2 hours · **20 points**
**Date:** Friday 9 October 2026 · 15:00–16:50 · Lab Section (Week 2) — covers Week 2 (Lectures 01–03)
**Tools:** Desmos, and Python using only CS 101 Weeks 0–2: arithmetic, `math`, `if`/`else`, `while`
(CS 101 Lecture 08) and `for` over a list (Lecture 09, this morning). No functions are needed.
**Expected time:** the session itself (7 questions), plus at most 30 minutes to tidy your answers.

---

## Python for Today

Programs longer than one line are easier in a file. Save the code as `lab02.py` and run it from the
terminal with `python3 lab02.py` (CS 101 Lecture 02). Start the file with `import math` if it uses `math`.

A `for` loop over a list, as in CS 101 Lecture 09, prints a table in three lines:

```python
for x in [0.9, 0.99, 0.999, 1.001, 1.01, 1.1]:
    print(x, (x**2 - 1) / (x - 1))
```

---

## Part 1: Seeing the Types (5 pts)

### Question 1 (2 points)

Graph each function in Desmos near the given point and classify the discontinuity (removable, jump,
infinite or essential). Say which part of the three-part definition fails.

| | Function | Point |
|---|---|---|
| 1A | $\dfrac{x^2-1}{x-1}$ | $x=1$ |
| 1B | $\dfrac1x$ | $x=0$ |
| 1C | $f(x)=x$ for $x<0$, $x+1$ for $x\ge0$ (type `y = x {x < 0}` and `y = x + 1 {x >= 0}`) | $x=0$ |

### Question 2 (3 points)

For $\sin(1/x)$ at $x = 0$, evaluate at $x=\dfrac{2}{k\pi}$ for $k=1,3,5,7,9,11$:

```python
for k in [1, 3, 5, 7, 9, 11]:
    x = 2 / (k * math.pi)
    print(x, math.sin(1 / x))
```

Record the table. What happens to $x$, what happens to $\sin(1/x)$, and what type of discontinuity is this?

---

## Part 2: Repairing a Discontinuity (5 pts)

### Question 3 (2 points)

For $f(x)=\dfrac{x^3-8}{x-2}$, adapt the `for` loop above to tabulate values at
$x = 1.9, 1.99, 1.999, 2.001, 2.01, 2.1$, and conjecture the limit as $x \to 2$.

### Question 4 (3 points)

Factor $x^3 - 8$ to confirm your conjecture, and write the continuous extension of $f$ explicitly. Then
explain why cancelling $x - 2$ is legitimate inside the limit even though it is invalid at $x=2$.

---

## Part 3: Bisection in Code (10 pts)

Lecture 03 §4 describes bisection. Here you run it on $f(x) = x^3 - 2x - 5$ over $[2, 3]$, a different
function from the problem set's.

### Question 5 (4 points)

Copy this program, fill in the blank, and run it. It performs 8 bisection steps.

```python
a = 2.0
b = 3.0
step = 0
while step < 8:
    m = (a + b) / 2
    fa = a**3 - 2*a - 5
    fm = m**3 - 2*m - 5
    print(step + 1, a, b, m, fm)
    if ________________:        # the root is in [a, m] when ...
        b = m
    else:
        a = m
    step = step + 1
```

Explain your condition using the IVT, and record the eight lines of output.

### Question 6 (3 points)

Change the loop so it runs `while b - a > 1e-6` instead of 8 times, keeping the `step` counter. Report
the root (the final midpoint) to 6 decimal places and the number of steps it took.

### Question 7 (3 points)

Lecture 03 says bisection on an interval of width 1 needs $n \geq \log_2(1/\varepsilon)$ steps. Run your
Question 6 program with tolerances `1e-4`, `1e-6` and `1e-10`. Do the step counts match the formula?

---

## Deliverables

Your tables, program, output, and written answers to Questions 1–7.

## Grading

| Part | Points |
|---|---|
| 1 — types classified with evidence | 5 |
| 2 — repair, with the cancellation justified | 5 |
| 3 — working bisection, with step counts checked | 10 |
| **Total** | **20** |

---

*Revised 2026-09-26: the lab now uses only Week 0–2 Python (the bisection is a `while` loop with no
function definitions, which are CS 101 Week 3). It was cut from 16 items to 7 questions: the four
hand-made tables are now one Desmos question and one loop, and Part 4 (the IVT over the rationals) is
covered by Problem Set 2, Problem 8. The bisection function differs from the problem set's, so the lab
no longer repeats it.*

---

*MATH 141 · Week 2 · Lab 02 · © CSE Department*
