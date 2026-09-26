# MATH 141 · Calculus I
## Lab 00: Graphical Exploration of Functions
### Week 0 Lab Session

---

**Duration:** 2 hours  
**Date:** Friday 25 September 2026 · 15:00–16:50 · Lab Section (Week 0) — covers Lectures 00–03
**Format:** Individual or pairs (pairs must submit separate lab reports)  
**Graded on:** Completion + correctness of written responses (not graded during Week 0: this is the orientation lab)  
**Tools:** [Desmos](https://www.desmos.com/calculator) (free, in the browser) for every graph. The Python REPL as a calculator, using only what CS 101 has taught by today: arithmetic, `**` and variables (CS 101 Lecture 02).
**Expected time:** the session itself (12 questions), plus at most 30 minutes to tidy your answers.

---

## Overview

Mathematics without visualization is half-blind. This lab trains you to move fluidly between algebraic formulas and their visual representations: a skill that will be essential for understanding limits, derivatives, and integrals throughout this course.

You will:
1. Plot and compare families of functions
2. Watch transformations happen with sliders
3. Compute average rates of change and watch them settle on a single number — the idea the whole course is built on

---

## Setup (10 minutes)

### Desmos in five minutes

Open [desmos.com/calculator](https://www.desmos.com/calculator). Everything is typed into the list on the left.

| To do this | Type or click |
|---|---|
| Graph a function | `y = x^2`, or name it: `f(x) = x^2` |
| Use a named function | `y = f(x - 2)`, or `f(3)` to see its value |
| Exponents, roots, logs | `x^3`, `2^x`, `e^x`, `sqrt(x)`, `ln(x)`, `abs(x)` |
| A slider | Type an expression with a new letter, e.g. `y = a(x - h)^2 + k`, then click **add slider** for each letter. Click the slider's limits to change its range |
| Restrict the domain | `y = x^2 {0 < x < 2}` |
| Plot a point | `(1, f(1))` |
| Special points | Click on a curve. Grey dots appear at intercepts and intersections; click one to see its coordinates |
| Change the window | Scroll or pinch to zoom, or click the **wrench** icon (top right) and type the x and y limits |
| Hide a curve | Click its coloured circle |
| Save your work | Take a screenshot, or use **Share** to copy a link |

### The Python REPL as a calculator

Open a terminal and type `python3`. At the `>>>` prompt, arithmetic works as in CS 101 Lecture 02:

```python
>>> 2**10
1024
>>> h = 0.1
>>> ((1 + h)**2 - 1) / h
2.100000000000002
```

Press the **up arrow** to recall a line, edit it, and press Enter again. The stray `…0000000002` at the end
is the computer rounding; CS 101 explains why in Week 1. Round to four decimal places in your tables.

---

## Part 1: Function Families (30 minutes)

### Activity 1.1: Power Functions

In Desmos, graph $y = x$, $y = x^2$, $y = x^3$, $y = x^4$ and $y = x^5$. Set the window to $-2 \le x \le 2$, $-3 \le y \le 3$.

**Q1.** What pattern separates the even powers from the odd powers? Describe it using symmetry.

**Q2.** Which points do all five graphs pass through? Explain algebraically why every $x^n$ must pass through them.

**Q3.** For $0 < x < 1$, which of the five is largest? For $x > 1$, which is largest? Explain why the order flips at $x = 1$.

### Activity 1.2: Exponential vs Polynomial Growth

Graph $y = x^3$ and $y = 2^x$. Set the window to $0 \le x \le 12$, $0 \le y \le 5000$.

**Q4.** Click the curves to find where they cross. Beyond which value of $x$ does $2^x$ stay above $x^3$ for good? Check in the REPL by comparing `2**10` with `10**3`, and `2**9` with `9**3`.

**Q5.** Type `ln(100)`, `sqrt(100)`, `ln(10000)` and `sqrt(10000)` into Desmos. Which grows faster for large $x$, $\ln x$ or $\sqrt{x}$? What does that say about how slowly logarithms grow?

---

## Part 2: Transformations (25 minutes)

### Activity 2.1: Sliders

Type `y = a(x - h)^2 + k` and add sliders for $a$, $h$ and $k$. Also graph $y = x^2$ as a reference.

**Q6.** Set $a = 1$ and $k = 0$, then move $h$ to $2$. Which way does the parabola move? Explain why subtracting 2 moves it to the **right**: which value of $x$ makes $x - 2 = 0$, and what does that mean for the graph?

**Q7.** Without graphing, give the vertex of $y = 3(x-4)^2 + 1$ and list the transformations that turn $y = x^2$ into it. Then set the sliders to check.

### Activity 2.2: Absolute Value

Graph $y = x^2 - 4$ and $y = |x^2 - 4|$.

**Q8.** Describe the "folding" rule: which parts of $y = x^2 - 4$ stay the same in $y = |x^2 - 4|$, and which are reflected? Why?

---

## Part 3: Average Rate of Change and the Approach to Calculus (45 minutes)

This is the most important part of Lab 00. It uses Lecture 03 §5, the average rate of change.

### Activity 3.1: Secant Lines for $f(x) = x^2$ at $x = 1$

In Desmos, type these four lines. Add a slider for $h$ and set its range from $0.001$ to $2$.

```
f(x) = x^2
(1, f(1))
(1 + h, f(1 + h))
y = f(1) + (f(1 + h) - f(1))/h * (x - 1)
```

The last line is the **secant line** through the two points. Drag $h$ towards $0$ and watch it.

**Q9.** Fill in the table. Use the REPL for the arithmetic: set `h = 1`, then type `(1 + h)**2` and
`((1 + h)**2 - 1) / h`. Change `h` and repeat with the up arrow.

| $h$ | $f(1+h)$ | $\dfrac{f(1+h)-f(1)}{h}$ |
|-----|----------|--------------------------|
| $1$ | | |
| $0.5$ | | |
| $0.1$ | | |
| $0.01$ | | |
| $0.001$ | | |

**Q10.** What value does the slope approach? Prove it: simplify $\dfrac{(1+h)^2 - 1}{h}$ by hand until no $h$ is left in the denominator, then put $h = 0$.

**Q11.** As you drag $h$ towards $0$, what does the secant line turn into? Describe it in one or two sentences.

### Activity 3.2: The Same Idea for $g(x) = x^3$ at $x = 2$

**Q12.** In the REPL, compute `((2 + h)**3 - 8) / h` for $h = 0.5$, $0.1$ and $0.01$. What value do the slopes approach? Check it by hand: expand $(2+h)^3$, simplify $\dfrac{(2+h)^3 - 8}{h}$, and put $h = 0$.

---

## Lab Report

Write your answers to Q1–Q12 in your answer sheet. Include:

1. **One screenshot or Desmos link per part** (three in total)
2. **Your completed Q9 table** and the REPL lines you typed for Q9 and Q12
3. **The hand working** for Q7, Q10 and Q12

---

*Revised 2026-09-26: the lab no longer needs `numpy` or `matplotlib`, which no course has taught. All graphs
are drawn in Desmos, and the only Python is REPL arithmetic from CS 101 Lecture 02. The logarithm family,
the floor function (it needed one-sided limits, a Week 1 idea) and the reflection were removed so the lab
fits its two hours.*

*Lab 00 is not graded — it is calibration. Do it anyway. The students who skip Week 0 lab are recognizable by Week 4.*
