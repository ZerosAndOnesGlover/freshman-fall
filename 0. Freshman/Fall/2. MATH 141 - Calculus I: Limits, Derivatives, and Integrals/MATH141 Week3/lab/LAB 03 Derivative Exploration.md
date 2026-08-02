# MATH 141 — Calculus I
## Lab 03 (Friday, Week 3)
### The Derivative: Numerical Exploration, Graphical Interpretation, and Rule Verification

**Duration:** 2 hours | **Tools:** Desmos, Python (optional)
**Submission:** Written report due Monday, Week 3

---

## Lab Objectives

1. Experience the derivative as a limit of slopes of secant lines
2. Understand graphically what differentiability looks like (and what failure looks like)
3. Verify differentiation rules numerically
4. Build intuition for the relationship between a function's graph and its derivative's graph
5. Apply numerical differentiation and understand its limitations

---

## Part 1 — Secant Lines Converging to the Tangent (25 min)

### Exercise 1.1 — Watching the Limit Happen

Consider $f(x) = x^2$ and the point $a = 2$.

The slope of the secant through $(2, f(2))$ and $(2+h, f(2+h))$ is:

$$m(h) = \frac{f(2+h)-f(2)}{h} = \frac{(2+h)^2 - 4}{h}$$

**Step 1:** Fill in the table:

| $h$ | $f(2+h)$ | $m(h)$ |
|-----|----------|--------|
| $1$ | | |
| $0.5$ | | |
| $0.1$ | | |
| $0.01$ | | |
| $0.001$ | | |
| $-0.1$ | | |
| $-0.01$ | | |
| $-0.001$ | | |

**Question 1a:** What value does $m(h)$ approach? This is $f'(2)$. Confirm with the formula $f'(x)=2x$.

**Step 2:** In Desmos, graph:
- $f(x) = x^2$
- The secant line: $y = f(2) + m(h)(x-2)$ where $h$ is a slider from $-2$ to $2$
- The tangent line: $y = 4 + 4(x-2)$

**Question 1b:** Drag the $h$ slider toward 0. Describe what happens to the secant line geometrically.

**Question 1c:** At what value of $h$ does the secant line become indistinguishable (visually) from the tangent line on the screen? What does this tell you about the numerical meaning of "close enough"?

---

### Exercise 1.2 — The Derivative Function from Slopes

Still using $f(x) = x^2$.

**Question 1d:** Compute the slope of the tangent line at each point:

| $a$ | Tangent slope $f'(a) = 2a$ |
|-----|--------------------------|
| $-2$ | |
| $-1$ | |
| $0$ | |
| $1$ | |
| $2$ | |
| $3$ | |

**Question 1e:** Plot these points $(a, f'(a))$ on a separate graph. What function do they trace out?

**Question 1f:** In Desmos, graph $f(x)=x^2$ and $f'(x)=2x$ on the same axes. Describe the relationship:
- Where is $f$ increasing? What sign does $f'$ have there?
- Where is $f$ decreasing? What sign does $f'$ have there?
- Where is $f$ at its minimum? What is $f'$ there?

---

## Part 2 — Reading the Derivative from a Graph (20 min)

In Desmos, graph $f(x) = x^3 - 3x$.

**Question 2a:** Without computing, identify visually the approximate $x$-values where:
- $f'(x) > 0$ (function increasing)
- $f'(x) < 0$ (function decreasing)
- $f'(x) = 0$ (function has horizontal tangent)

**Question 2b:** Now compute $f'(x)$ using the power and sum rules. Solve $f'(x)=0$ exactly.

**Question 2c:** Graph both $f(x)$ and $f'(x)$ in Desmos. Do the zero crossings of $f'$ correspond to the turning points of $f$? Verify.

**Question 2d:** Graph $f''(x)$ as well. Describe the relationship between:
- Where $f''(x) > 0$ and the shape of $f$ (concave up or down?)
- Where $f''(x) = 0$ and what happens to $f$

**Question 2e:** Sketch (by hand) what the graph of $f'$ would look like for the function shown below, given only its graph. You should be able to identify:
- Where $f' = 0$
- Where $f' > 0$ vs $f' < 0$
- Roughly how steep $f'$ is

```
        f(x)
   *
  / \
 /   \       /
/     \     /
        \ /
         *
```
*(A curve that rises, peaks, falls to a valley, then rises again)*

---

## Part 3 — Non-Differentiable Points (20 min)

### Exercise 3.1 — Corners

Graph $f(x) = |x|$ in Desmos.

**Question 3a:** Compute the left-hand and right-hand limits of the difference quotient at $x=0$:

$$\lim_{h\to0^-}\frac{|h|-0}{h} \qquad \text{and} \qquad \lim_{h\to0^+}\frac{|h|-0}{h}$$

**Question 3b:** What do these two limits tell you about differentiability at $x=0$?

**Question 3c:** Graph $f(x)=|x|$ in Desmos and add the secant-line slider from Exercise 1.1. What happens visually as $h\to0^-$ versus $h\to0^+$?

### Exercise 3.2 — Cusps

Graph $f(x) = x^{2/3}$ in Desmos.

**Question 3d:** Compute $\displaystyle\lim_{h\to0}\frac{(0+h)^{2/3}-0}{h} = \lim_{h\to0}h^{-1/3}$. What is this limit?

**Question 3e:** What does the graph look like at $x=0$? Is this consistent with your limit calculation?

### Exercise 3.3 — A Subtler Case

Consider:
$$f(x) = \begin{cases} x^2 & x\leq 1 \\ 2x-1 & x>1 \end{cases}$$

**Question 3f:** Is $f$ continuous at $x=1$? Check the three conditions.

**Question 3g:** Compute the left and right derivatives at $x=1$:
$$\lim_{h\to0^-}\frac{f(1+h)-f(1)}{h} \qquad \lim_{h\to0^+}\frac{f(1+h)-f(1)}{h}$$

**Question 3h:** Is $f$ differentiable at $x=1$? Graph $f$ and describe the geometric feature at $x=1$.

---

## Part 4 — Numerical Differentiation and Its Limits (25 min)

Computers can't take limits symbolically (unless using CAS tools). They approximate derivatives using finite differences.

### Exercise 4.1 — Forward vs Central Differences

The **forward difference** approximation: $f'(x) \approx \dfrac{f(x+h)-f(x)}{h}$

The **central difference** approximation: $f'(x) \approx \dfrac{f(x+h)-f(x-h)}{2h}$

Use $f(x) = \sin(x)$ and approximate $f'(\pi/4) = \cos(\pi/4) = \dfrac{\sqrt{2}}{2} \approx 0.70711$.

Fill in the table (use a calculator):

| $h$ | Forward diff. | Error (forward) | Central diff. | Error (central) |
|-----|--------------|----------------|--------------|----------------|
| $0.1$ | | | | |
| $0.01$ | | | | |
| $0.001$ | | | | |
| $0.0001$ | | | | |
| $0.00001$ | | | | |

**Question 4a:** Which approximation is more accurate for the same $h$? By roughly what factor?

**Question 4b:** For the forward difference, as $h$ decreases by a factor of 10, the error decreases by a factor of approximately ___. For the central difference, by a factor of approximately ___. What does this tell you about the order of accuracy of each method?

**Question 4c:** At very small $h$ (e.g., $h = 10^{-15}$), what happens to the accuracy? Why? (Think about the catastrophic cancellation issue from Lab 1.)

**Question 4d:** What is the optimal $h$ to use in practice for the forward difference? (There is a tradeoff between truncation error which decreases with $h$, and round-off error which increases with small $h$.)

> **CS Connection:** The central difference formula has error $O(h^2)$ — it's a second-order method. The forward difference has error $O(h)$ — first order. In numerical computing, higher-order methods are almost always preferred because they achieve the same accuracy with less computational work. The same principle drives the difference between Euler's method (first-order) and Runge-Kutta (fourth-order) for solving differential equations.

---

### Exercise 4.2 — Verifying the Product Rule Numerically

Let $f(x) = x^2$ and $g(x) = \sin x$. The product is $p(x) = x^2\sin x$.

At $x = 1$:
- $f(1) = 1$, $f'(1) = 2$
- $g(1) = \sin(1)$, $g'(1) = \cos(1)$
- Product rule predicts: $p'(1) = f'(1)g(1) + f(1)g'(1) = 2\sin(1) + \cos(1)$

**Question 4e:** Compute $2\sin(1)+\cos(1)$ numerically.

**Question 4f:** Verify this using the central difference formula with $h = 0.001$:
$$p'(1) \approx \frac{(1.001)^2\sin(1.001) - (0.999)^2\sin(0.999)}{0.002}$$

**Question 4g:** Do they agree to 3+ decimal places? What does this confirm?

---

## Part 5 — The Derivative of $e^x$ (15 min)

The number $e$ is defined so that $\dfrac{d}{dx}[e^x] = e^x$. Let's see this numerically.

**Question 5a:** The derivative of $a^x$ at $x=0$ is:
$$\lim_{h\to0}\frac{a^h-1}{h}$$

Fill in this table for $a = 2$, $a = e \approx 2.71828$, $a = 3$:

| $h$ | $\dfrac{2^h-1}{h}$ | $\dfrac{e^h-1}{h}$ | $\dfrac{3^h-1}{h}$ |
|-----|-------------------|-------------------|-------------------|
| $0.1$ | | | |
| $0.01$ | | | |
| $0.001$ | | | |
| $0.0001$ | | | |

**Question 5b:** What value does each column approach? For which base does $\lim_{h\to0}\frac{a^h-1}{h} = 1$?

**Question 5c:** This means $\dfrac{d}{dx}[e^x]\big|_{x=0} = 1$. Using the chain rule generalization, show that $\dfrac{d}{dx}[e^x] = e^x$ everywhere by computing $\dfrac{d}{dx}[e^x]$ via the limit definition:

$$\frac{d}{dx}[e^x] = \lim_{h\to0}\frac{e^{x+h}-e^x}{h} = e^x\lim_{h\to0}\frac{e^h-1}{h}$$

What does your table tell you about the remaining limit?

---

## Lab Report Requirements

Include:
1. All completed tables
2. Answers to all questions (labeled)
3. Desmos screenshots for Parts 1 and 2
4. Reflection (5–8 sentences): Before this lab, how did you think about the derivative? How has your understanding of it as a limit of slopes changed? What was most surprising?

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — Secant convergence | 20 |
| Part 2 — Reading derivatives from graphs | 20 |
| Part 3 — Non-differentiable points | 20 |
| Part 4 — Numerical differentiation | 25 |
| Part 5 — The number $e$ | 10 |
| Reflection | 5 |
| **Total** | **100** |
