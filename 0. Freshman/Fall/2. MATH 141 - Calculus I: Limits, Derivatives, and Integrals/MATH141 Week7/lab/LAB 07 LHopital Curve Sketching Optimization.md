# MATH 141 — Calculus I
## Lab 07 (Friday, Week 7)
### L'Hôpital's Rule Verification, Curve Sketching Practice, and Optimization Design

**Duration:** 2 hours | **Tools:** Desmos, Python (optional)
**Submission:** Written report due Monday, Week 6

---

## Lab Objectives

1. Verify L'Hôpital's Rule numerically and understand growth rate hierarchies visually
2. Practice the complete curve sketching checklist on unfamiliar functions
3. Solve a real optimization problem and visualize why the critical point is optimal
4. Build a numerical optimizer and compare it against calculus-based exact solutions

---

## Part 1 — Growth Rate Hierarchies (25 min)

### Exercise 1.1 — Racing Functions to Infinity

In Desmos, graph the following four functions together on the same axes for $x \in [0, 20]$:
- $f_1(x) = \ln x$
- $f_2(x) = x$
- $f_3(x) = x^2$
- $f_4(x) = e^x$ (you may need to restrict the $y$-range to see the others!)

**Question 1a:** Rank these four functions from slowest-growing to fastest-growing based on the graph.

**Question 1b:** Now compute the ratios and confirm using L'Hôpital's Rule (on paper):

$$\lim_{x\to\infty}\frac{\ln x}{x} = ? \qquad \lim_{x\to\infty}\frac{x}{x^2} = ? \qquad \lim_{x\to\infty}\frac{x^2}{e^x} = ?$$

**Question 1c:** Numerically evaluate $\dfrac{\ln x}{x}$, $\dfrac{x}{x^2}$, and $\dfrac{x^2}{e^x}$ at $x = 10, 100, 1000, 10000$. Do the ratios approach the values predicted by L'Hôpital's Rule?

| $x$ | $\ln x / x$ | $x/x^2$ | $x^2/e^x$ |
|-----|------------|---------|-----------|
| 10 | | | |
| 100 | | | |
| 1000 | | | |
| 10000 | | | |

**Question 1d:** This ranking is exactly the algorithm complexity hierarchy. Match each function to a familiar algorithm:
- $O(\log n)$: ___________________
- $O(n)$: ___________________
- $O(n^2)$: ___________________
- $O(2^n)$ (or similar exponential): ___________________

---

### Exercise 1.2 — Verifying $1^\infty$ Numerically

We proved $\displaystyle\lim_{x\to\infty}\left(1+\frac1x\right)^x = e$ using L'Hôpital's Rule.

**Question 1e:** Fill in the table:

| $x$ | $(1+1/x)^x$ |
|-----|-------------|
| 10 | |
| 100 | |
| 1000 | |
| 100000 | |
| 10000000 | |

**Question 1f:** How many correct decimal digits of $e \approx 2.718281828...$ do you get at $x = 10^7$? What does this suggest about the *rate* of convergence of this particular limit (fast or slow)?

**Question 1g:** In Desmos, graph $y = (1+1/x)^x$ for $x > 0$ and confirm it approaches $e$ as $x \to \infty$. Also observe: is the function monotonically increasing toward $e$, or does it overshoot?

---

## Part 2 — Curve Sketching Practice with Instant Feedback (40 min)

For each function below: **first** perform the calculus analysis by hand (domain, asymptotes, increase/decrease, concavity), predict what the graph looks like, **then** check in Desmos. Note any discrepancies and figure out what went wrong in your analysis if there is a mismatch.

### Exercise 2.1

$$f(x) = \frac{x}{x^2+1}$$

**Question 2a:** Complete the analysis. Predict: is this function bounded? What is its range?

**Question 2b:** Check in Desmos. Find the exact maximum and minimum values (these should be local AND absolute, since the function has no other extrema).

### Exercise 2.2

$$g(x) = x\ln x$$

**Question 2c:** What is the domain? (Careful — this is not all of $\mathbb{R}$.)

**Question 2d:** Complete the analysis: find $g'(x)$, critical numbers, concavity. Predict behavior as $x \to 0^+$ (this requires the $0\cdot\infty$ technique from Lecture 1!).

**Question 2e:** Check in Desmos. Is there a genuine minimum? What is it?

### Exercise 2.3

$$h(x) = \frac{e^x}{x}$$

**Question 2f:** Domain? Vertical asymptote behavior — compute both one-sided limits at the excluded point.

**Question 2g:** Find critical numbers and classify. Complete the full analysis.

**Question 2h:** Check in Desmos. This function has an interesting "valley" shape on the positive side — does your calculus prediction match?

---

## Part 3 — Optimization: Design and Verify (35 min)

### Exercise 3.1 — The Minimum Cost Pipeline

An underwater cable must connect a station on shore to a platform 5 km offshore (perpendicular distance). The nearest point on shore to the platform is point $P$. The station is 10 km down the shore from $P$. Laying cable underwater costs $\$5000$/km; laying cable on land costs $\$3000$/km.

**Question 3a:** Let $x$ = distance from $P$ to the point where the cable comes ashore. Set up the total cost function $C(x)$.

**Question 3b:** Differentiate, find the critical number, and verify it's a minimum.

**Question 3c:** In Desmos, graph $C(x)$ for $x \in [0, 10]$. Visually confirm the minimum occurs where your calculus predicts.

**Question 3d:** What is the minimum total cost?

### Exercise 3.2 — Numerical Optimization Comparison

**Question 3e:** For the box problem from Lecture 3 ($V(x) = x(12-2x)^2$, domain $(0,6)$), write Python pseudocode (or actual Python if available) implementing a simple numerical optimizer:

```python
def find_max_numerically(f, a, b, n_points=10000):
    """
    Evaluate f at n_points evenly spaced points in [a,b].
    Return the x-value giving the maximum f(x).
    """
    best_x = a
    best_val = f(a)
    step = (b - a) / n_points
    for i in range(n_points + 1):
        x = a + i * step
        val = f(x)
        if val > best_val:
            best_val = val
            best_x = x
    return best_x, best_val
```

**Question 3f:** Run this (mentally, or in Python if available) on $V(x) = x(12-2x)^2$ over $(0,6)$. Does it converge to $x=2$ (the exact calculus answer)? How does the accuracy depend on `n_points`?

**Question 3g:** What are the tradeoffs between this "brute force" numerical approach and the calculus-based exact approach? When would you prefer one over the other in a real engineering context?

> **CS Connection:** This is a **grid search** — the simplest possible optimization algorithm, and the direct numerical analog of everything you did by hand this week. It is also extremely inefficient compared to calculus-informed methods (gradient descent, Newton's method) which use derivative information to converge far faster. This is the core motivation behind why ML training uses gradients rather than brute-force search over parameter space.

---

## Part 4 — Design Your Own Optimization Problem (15 min)

**Question 4a:** Working with a partner, design an original applied optimization problem (not from the lecture or textbook). It should involve:
- A clear real-world context
- A geometric or algebraic constraint
- A well-defined objective function

Write the full problem statement, then solve it completely (objective function, constraint, differentiation, verification).

**Question 4b:** Verify your answer using Desmos by graphing the objective function over its domain and visually confirming the extremum location.

---

## Lab Report Requirements

Include:
1. Completed tables from Part 1
2. Full written analysis for all three functions in Part 2, with Desmos screenshots
3. Complete solution to Exercise 3.1 with Desmos screenshot
4. Your Python/pseudocode results from Exercise 3.2, with discussion of tradeoffs
5. Your original optimization problem and full solution from Part 4
6. **Reflection** (6–8 sentences): Compare the "exact" calculus approach to optimization with the "numerical/brute-force" approach from Exercise 3.2. What does calculus give you that brute-force search does not? In what situations might brute-force still be preferable?

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — Growth rate hierarchies | 20 |
| Part 2 — Curve sketching practice | 30 |
| Part 3 — Optimization design/verify | 30 |
| Part 4 — Original problem | 15 |
| Reflection | 5 |
| **Total** | **100** |
