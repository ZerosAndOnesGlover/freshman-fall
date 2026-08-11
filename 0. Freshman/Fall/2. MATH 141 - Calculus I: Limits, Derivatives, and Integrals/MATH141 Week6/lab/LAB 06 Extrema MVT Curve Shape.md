# MATH 141 · Calculus I
## Lab 06 (Friday, Week 6)
### Visualizing Extrema, the Mean Value Theorem, and Curve Shape

**Duration:** 2 hours | **Tools:** Desmos, Python (optional)
**Submission:** Written report due Monday, Week 7

---

## Lab Objectives

1. Visualize the Extreme Value Theorem and see why its hypotheses matter
2. See the Mean Value Theorem geometrically — the parallel secant/tangent lines
3. Explore the relationship between $f$, $f'$, and $f''$ graphically, side by side
4. Discover why the Second Derivative Test can fail
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

## Part 3 — Three Graphs Side by Side: $f$, $f'$, $f''$ (35 min)

This is the most important conceptual exercise of the week: training your eye to read the relationships between a function and its derivatives.

### Exercise 3.1

Consider $f(x) = x^4 - 4x^3 + 4x^2$.

**Step 1:** Compute $f'(x)$ and $f''(x)$ by hand.

**Step 2:** In Desmos, graph all three functions $f$, $f'$, $f''$ using different colors, all on the same axes (or use Desmos's graph-folder feature to organize them).

**Question 3a:** Identify every $x$-value where $f'(x) = 0$ from the graph. At each such point, check: is $f$ increasing or decreasing on either side? Does this match a local max, local min, or neither?

**Question 3b:** Identify every $x$-value where $f''(x) = 0$. At each, check: does the concavity of $f$ actually change there? (Sometimes $f''=0$ does NOT mean an inflection point — verify this carefully.)

**Question 3c:** Fill in this synthesis table:

| $x$-value | $f'(x)$ sign change? | $f''(x)$ sign change? | Classification |
|-----------|----------------------|------------------------|-----------------|
| | | | |
| | | | |
| | | | |

### Exercise 3.2 — Reverse Engineering

You are given ONLY the graph of $f'(x) = (x+2)(x-1)^2$ (no formula for $f$ itself).

**Question 3d:** Without finding $f(x)$, determine:
- All critical numbers of $f$
- Intervals where $f$ is increasing/decreasing
- Classification of each critical point (local max/min/neither)

**Question 3e:** Now compute $f''(x)$ from $f'(x)$ and determine concavity intervals and inflection points — still without ever finding $f(x)$ itself.

**Question 3f:** Sketch what $f(x)$ might look like, using only this derivative information. (Many different functions $f$ could have this $f'$ — they'd all differ by a vertical shift, per MVT Corollary 2 from Tuesday's lecture. Your sketch just needs the correct *shape*.)

---

## Part 4 — When the Second Derivative Test Fails (20 min)

### Exercise 4.1 — Three Functions, Same $f'(0)=f''(0)=0$

Consider three functions:
$$f_1(x) = x^4 \qquad f_2(x) = -x^4 \qquad f_3(x) = x^3$$

**Question 4a:** Verify for all three that $f'(0) = 0$ and $f''(0) = 0$ (so the Second Derivative Test gives no information).

**Question 4b:** Graph all three in Desmos near $x=0$. Classify the behavior at $x=0$ for each: local min, local max, or neither (inflection with horizontal tangent)?

**Question 4c:** Use the First Derivative Test on each to confirm your graphical classification algebraically.

**Question 4d:** This exercise demonstrates that $f''(c)=0$ is truly inconclusive — it is consistent with a local min, local max, OR neither. Write a one-paragraph explanation of why the Second Derivative Test has this gap, referring to the geometric meaning of $f''$.

---

## Part 5 — Numerical Root Counting via Rolle's Theorem (15 min)

### Exercise 5.1 — Automated Reasoning

Rolle's Theorem, used contrapositively, gives a root-counting technique: if $f'(x) \neq 0$ everywhere on an interval, $f$ has **at most one** root there (since two roots would force $f'=0$ somewhere between them by Rolle's Theorem).

**Question 5a:** Consider $f(x) = x^5 + 3x + 1$. Compute $f'(x)$. Show algebraically that $f'(x) > 0$ for all $x$ (hence never zero).

**Question 5b:** Using the IVT (Week 2) and the sign of $f(0)$ and evaluate $f$ at convenient points, show $f$ has at least one root.

**Question 5c:** Combine 5a and 5b via Rolle's Theorem logic to conclude $f$ has **exactly one** real root.

**Question 5d:** In Desmos, graph $f(x) = x^5+3x+1$ and visually confirm there is exactly one $x$-intercept.

**Question 5e (Pseudocode):** Write pseudocode for a function `count_roots_via_derivative(f, f_prime, a, b)` that:
1. Checks if `f_prime` changes sign on `[a,b]` (using many sample points)
2. If `f_prime` never changes sign, concludes "at most one root" in `[a,b]`
3. Uses the bisection method (Lab 1) to actually locate the root if `f(a)` and `f(b)` have opposite signs

---

## Lab Report Requirements

Include:
1. Answers to all questions
2. Desmos screenshots for Parts 1, 2, and 3
3. The synthesis table from Exercise 3.1
4. Your sketch from Exercise 3.2
5. Pseudocode from Exercise 5.5
6. **Reflection** (6–8 sentences): How has visualizing $f$, $f'$, and $f''$ together changed the way you think about a function's graph? What is the most useful "reading" skill you developed today — being able to go from $f'$ back to properties of $f$, or forward from $f$ to properties of $f'$ and $f''$?

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — EVT hypotheses | 15 |
| Part 2 — MVT visualization | 25 |
| Part 3 — Three graphs synthesis | 30 |
| Part 4 — Second Derivative Test failure | 15 |
| Part 5 — Root counting | 10 |
| Reflection | 5 |
| **Total** | **100** |
