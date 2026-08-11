# MATH 141 · Calculus I
## Lab 00: Graphical Exploration of Functions
### Week 0 Lab Session

---

**Duration:** 2 hours  
**Lab session:** Friday of Week 0
**Format:** Individual or pairs (pairs must submit separate lab reports)  
**Graded on:** Completion + correctness of written responses (not graded during Week 0: this is the orientation lab)  
**Tools Required:** Python 3 with `matplotlib` and `numpy` (instructions below), or [Desmos](https://www.desmos.com) (free, browser-based)

---

## Overview

Mathematics without visualization is half-blind. This lab trains you to move fluidly between algebraic formulas and their visual representations: a skill that will be essential for understanding limits, derivatives, and integrals throughout this course.

You will:
1. Plot and explore families of functions
2. Observe transformation rules visually
3. Investigate average rates of change graphically
4. Build intuition for what happens "near a point", the foundation of limits

---

## Setup

### Option A: Python (Recommended for CSE Students)

```bash
# Install if needed (run in terminal)
pip install matplotlib numpy

# Start Python
python3
```

```python
# Template — paste this at the top of every Python session
import numpy as np
import matplotlib.pyplot as plt

# Create x values from -5 to 5 with 1000 points
x = np.linspace(-5, 5, 1000)

# Plot a function
plt.figure(figsize=(8, 6))
plt.plot(x, x**2, label='f(x) = x²', color='blue')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(True, alpha=0.3)
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Graph of f(x) = x²')
plt.show()
```

### Option B: Desmos

Go to [desmos.com/calculator](https://www.desmos.com/calculator). Type functions directly. Use sliders for parameters.

---

## Part 1: Function Families (30 minutes)

### Activity 1.1: Power Functions

Plot the following on the same axes for $x \in [-2, 2]$:
$$f_1(x) = x, \quad f_2(x) = x^2, \quad f_3(x) = x^3, \quad f_4(x) = x^4, \quad f_5(x) = x^5$$

```python
x = np.linspace(-2, 2, 1000)
functions = [x, x**2, x**3, x**4, x**5]
labels = ['x', 'x²', 'x³', 'x⁴', 'x⁵']

plt.figure(figsize=(10, 7))
for f, label in zip(functions, labels):
    plt.plot(x, f, label=f'f(x) = {label}')
plt.ylim(-3, 3)
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(0, color='black', linewidth=0.8)
plt.grid(True, alpha=0.3)
plt.legend()
plt.title('Power Functions')
plt.show()
```

**Written Questions 1.1:**

a. What pattern do you notice between even-power functions vs odd-power functions?

b. All the graphs pass through which specific points? Explain algebraically why this must be true for all $x^n$.

c. For $x \in (0, 1)$, which function is largest? For $x > 1$, which is largest? Explain why.

d. Compare the "flatness" of each function near $x = 0$. Which is flattest? What does this suggest about their derivatives at $x = 0$?

---

### Activity 1.2: Exponential vs Polynomial Growth

```python
x = np.linspace(0, 10, 1000)

plt.figure(figsize=(10, 7))
plt.plot(x, x**2, label='x²', linewidth=2)
plt.plot(x, x**3, label='x³', linewidth=2)
plt.plot(x, 2**x, label='2ˣ', linewidth=2)
plt.plot(x, np.e**x, label='eˣ', linewidth=2)
plt.ylim(0, 10000)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)
plt.title('Polynomial vs Exponential Growth')
plt.show()

# Now try logarithmic scale
plt.figure(figsize=(10, 7))
plt.semilogy(x, x**2, label='x²')
plt.semilogy(x, x**3, label='x³')
plt.semilogy(x, 2**x, label='2ˣ')
plt.semilogy(x, np.e**x, label='eˣ')
plt.grid(True, alpha=0.3)
plt.legend()
plt.title('Same Functions on Logarithmic Scale')
plt.show()
```

**Written Questions 1.2:**

a. At approximately what value of $x$ does $2^x$ overtake $x^3$? Verify algebraically by solving $2^x = x^3$ approximately (use trial and error with logarithms).

b. On the logarithmic-scale plot, which functions appear as straight lines? Why? (Hint: if $\ln(f(x))$ is linear in $x$, what does that tell you about $f$?)

c. Based on the graphs, explain in your own words what it means for an exponential function to "dominate" a polynomial for large $x$.

---

### Activity 1.3: Logarithmic Functions

```python
x = np.linspace(0.01, 10, 1000)  # Avoid x=0

plt.figure(figsize=(10, 7))
plt.plot(x, np.log(x), label='ln(x)', linewidth=2)
plt.plot(x, np.log2(x), label='log₂(x)', linewidth=2)
plt.plot(x, np.log10(x), label='log₁₀(x)', linewidth=2)
plt.plot(x, np.sqrt(x), label='√x', linewidth=2, linestyle='--')
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(0, color='black', linewidth=0.8)
plt.ylim(-4, 4)
plt.grid(True, alpha=0.3)
plt.legend()
plt.title('Logarithmic Functions')
plt.show()
```

**Written Questions 1.3:**

a. All three logarithm graphs have the same shape. What geometric transformation relates $\ln x$ to $\log_2 x$? Verify using the change of base formula.

b. Compare $\ln x$ and $\sqrt{x}$ for large $x$. Which grows faster? What does this suggest about the "slowness" of logarithmic growth?

c. As $x \to 0^+$, what happens to $\ln x$? What does this mean for the domain of $\ln$?

---

## Part 2: Transformations (30 minutes)

### Activity 2.1: Systematic Transformations

Start with $f(x) = x^2$. Use Desmos or Python to observe each transformation:

```python
x = np.linspace(-5, 5, 1000)
base = x**2

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
transformations = [
    (base, 'f(x) = x²', 'baseline'),
    (base + 2, 'f(x) + 2', 'vertical shift up 2'),
    ((x-2)**2, 'f(x-2)', 'horizontal shift right 2'),
    (2*base, '2·f(x)', 'vertical stretch by 2'),
    ((2*x)**2, 'f(2x)', 'horizontal compression'),
    (-base, '-f(x)', 'reflection over x-axis'),
]

for ax, (func, label, desc) in zip(axes.flatten(), transformations):
    ax.plot(x, func, color='blue', linewidth=2)
    ax.plot(x, base, color='gray', linewidth=1, linestyle='--', alpha=0.5, label='original')
    ax.set_ylim(-10, 20)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True, alpha=0.3)
    ax.set_title(f'{label}\n({desc})')
    ax.legend()

plt.tight_layout()
plt.show()
```

**Written Questions 2.1:**

a. The graph of $f(x-2)$ shifts the parabola to the **right** even though we subtracted 2. Explain precisely why this is — trace through what $x$ value makes $x - 2 = 0$, and what that means geometrically.

b. Compare $2f(x)$ (vertical stretch) and $f(2x)$ (horizontal compression). They look different but are both "making the graph skinnier." Explain the difference precisely using the formulas.

c. What is the vertex of the parabola $y = 3(x-4)^2 + 1$? Without graphing, describe all transformations applied to $y = x^2$ to produce this parabola.

---

### Activity 2.2: Absolute Value and Piecewise

```python
x = np.linspace(-4, 4, 1000)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# |x|
axes[0].plot(x, np.abs(x), color='blue', linewidth=2)
axes[0].set_title('f(x) = |x|')
axes[0].grid(True, alpha=0.3)
axes[0].axhline(0, color='black', linewidth=0.5)

# |x²  - 4|
axes[1].plot(x, np.abs(x**2 - 4), color='red', linewidth=2)
axes[1].plot(x, x**2 - 4, color='gray', linewidth=1, linestyle='--', alpha=0.5, label='x²-4')
axes[1].set_title('f(x) = |x² - 4|')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
axes[1].axhline(0, color='black', linewidth=0.5)

# Floor function
axes[2].plot(x, np.floor(x), color='green', linewidth=2, drawstyle='steps-post')
axes[2].set_title('f(x) = ⌊x⌋ (floor function)')
axes[2].grid(True, alpha=0.3)
axes[2].axhline(0, color='black', linewidth=0.5)

plt.tight_layout()
plt.show()
```

**Written Questions 2.2:**

a. $|x^2 - 4|$ is the "folded" version of $x^2 - 4$. Describe the folding rule: which parts of the original graph stay the same, and which get reflected?

b. The floor function $\lfloor x \rfloor$ has **jump discontinuities** at every integer. Note the open and closed dots at each jump. Describe precisely: is $\lfloor 2 \rfloor = 2$ or undefined? What is $\lim_{x \to 2^-} \lfloor x \rfloor$ vs $\lim_{x \to 2^+} \lfloor x \rfloor$? (Informal use of limits — we formalize next week.)

c. Is the floor function one-to-one? Does it have an inverse? Explain.

---

## Part 3: Average Rate of Change and the Approach to Calculus (45 minutes)

### Activity 3.1: Secant Lines

This is the most important activity in Lab 00.

```python
import matplotlib.pyplot as plt
import numpy as np

def f(x):
    return x**2

x_plot = np.linspace(-1, 4, 1000)
x_fixed = 1.0  # The point we're approaching

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Secant lines with decreasing h
h_values = [2.0, 1.0, 0.5]
colors = ['red', 'orange', 'green']

for ax, h, color in zip(axes, h_values, colors):
    x_h = x_fixed + h
    slope = (f(x_h) - f(x_fixed)) / h
    
    # Plot function
    ax.plot(x_plot, f(x_plot), 'b-', linewidth=2, label='f(x) = x²')
    
    # Plot secant line
    x_line = np.linspace(x_fixed - 0.5, x_h + 0.5, 100)
    y_line = f(x_fixed) + slope * (x_line - x_fixed)
    ax.plot(x_line, y_line, color=color, linewidth=2, 
            label=f'Secant (h={h})\nSlope = {slope:.3f}')
    
    # Mark the two points
    ax.plot(x_fixed, f(x_fixed), 'ko', markersize=8)
    ax.plot(x_h, f(x_h), 'o', color=color, markersize=8)
    
    ax.set_xlim(-0.5, 4)
    ax.set_ylim(-0.5, 12)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title(f'h = {h}')

plt.suptitle('Secant Lines Approaching x=1 — f(x) = x²', fontsize=14)
plt.tight_layout()
plt.show()
```

**Written Questions 3.1:**

a. Fill in this table by computing the average rate of change $\dfrac{f(1+h) - f(1)}{h}$ algebraically:

| $h$ | $f(1+h)$ | $\dfrac{f(1+h)-f(1)}{h}$ |
|-----|----------|--------------------------|
| $1.0$ | | |
| $0.5$ | | |
| $0.1$ | | |
| $0.01$ | | |
| $0.001$ | | |

b. What value does the average rate of change appear to approach? 

c. Prove it algebraically: simplify $\dfrac{(1+h)^2 - 1}{h}$ and find its value as $h \to 0$.

d. Visually, what does the secant line "become" as $h \to 0$?

---

### Activity 3.2: Exploring Different Functions

Repeat the secant line analysis for $g(x) = x^3$ at the point $x = 2$.

```python
def g(x):
    return x**3

x_fixed = 2.0
h_values = [0.5, 0.1, 0.01]

print("Secant slopes for g(x) = x³ at x = 2:")
print(f"{'h':>10} {'(g(2+h) - g(2))/h':>25}")
print("-" * 40)
for h in h_values:
    slope = (g(x_fixed + h) - g(x_fixed)) / h
    print(f"{h:>10.4f} {slope:>25.10f}")
```

**Written Questions 3.2:**

a. What value does the slope appear to approach?

b. Verify algebraically: expand $(2+h)^3$ and simplify $\dfrac{(2+h)^3 - 8}{h}$.

c. What is the pattern? The derivative of $x^2$ at $x = 1$ is $2$. The derivative of $x^3$ at $x = 2$ is (your answer). Can you guess a general formula for the derivative of $x^n$ at $x = a$?

---

### Activity 3.3: The Derivative of $e^x$ — A Surprise

```python
def expf(x):
    return np.exp(x)

x_fixed = 0.0
h_values = [1.0, 0.5, 0.1, 0.01, 0.001, 0.0001]

print("Secant slopes for f(x) = eˣ at x = 0:")
print(f"{'h':>10} {'slope':>20} {'f(0)':>15}")
print("-" * 50)
for h in h_values:
    slope = (expf(x_fixed + h) - expf(x_fixed)) / h
    print(f"{h:>10.6f} {slope:>20.15f} {expf(x_fixed):>15.10f}")
```

**Written Questions 3.3:**

a. What value does the slope of $e^x$ at $x = 0$ approach? How does it compare to $f(0) = e^0$?

b. This is the remarkable property of $e^x$: its derivative equals itself. Verify this numerically at $x = 1$ and $x = 2$ by computing the secant slopes.

c. What base $a$ makes the derivative of $a^x$ at $x = 0$ equal exactly to $1$? You just found it numerically. (Answer: $e$.)

---

## Part 4: Investigations (15 minutes)

### Activity 4.1: The Mystery of $|x|$ at $x = 0$

```python
x_fixed = 0.0
h_values = [0.5, 0.1, 0.01, -0.01, -0.1, -0.5]

print("Secant slopes for f(x) = |x| at x = 0:")
print(f"{'h':>10} {'slope':>15}")
print("-" * 30)
for h in h_values:
    slope = (abs(x_fixed + h) - abs(x_fixed)) / h
    print(f"{h:>10.4f} {slope:>15.6f}")
```

**Written Questions 4.1:**

a. What happens to the slope for positive $h$ vs negative $h$?

b. Does the secant slope approach a single value as $h \to 0$? What does this mean for the derivative of $|x|$ at $x = 0$?

c. Look at the graph of $|x|$ at $x = 0$. What feature of the graph corresponds to your numerical finding?

---

## Lab Report

Submit a PDF document containing:

1. **All graphs** produced (screenshots or saved images)
2. **All written responses** to questions
3. **Complete Python code** used (or Desmos links)
4. **Reflection** (half page): What surprised you most in this lab? What questions arose that you don't yet know how to answer?

---

## Quick Reference: Python Plotting Commands

```python
# Multiple plots on one figure
plt.figure(figsize=(10, 6))
plt.plot(x, y1, label='first', color='blue', linewidth=2)
plt.plot(x, y2, label='second', color='red', linestyle='--')
plt.scatter([x0], [y0], color='black', s=100, zorder=5)  # Single point
plt.xlabel('x'); plt.ylabel('y')
plt.title('My Plot')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(-3, 3); plt.ylim(-2, 5)
plt.savefig('my_plot.png', dpi=150)
plt.show()

# Subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].plot(x, y)  # top-left
axes[0, 1].plot(x, z)  # top-right
# etc.

# Handling undefined values (division by zero)
with np.errstate(divide='ignore', invalid='ignore'):
    y = 1 / (x - 2)  # Will give inf at x=2
y[np.abs(y) > 100] = np.nan  # Replace large values with NaN (not plotted)
```

---

*Lab 00 is not graded — it is calibration. Do it anyway. The students who skip Week 0 lab are recognizable by Week 4.*
