# MATH 141 — Calculus I
## Lab 05 (Friday, Week 5)
### Implicit Curves, Logarithmic Derivatives, and Related Rates Simulation

**Duration:** 2 hours | **Tools:** Desmos, Python (optional)
**Submission:** Written report due Monday, Week 4

---

## Lab Objectives

1. Visualize implicitly defined curves and their tangent lines
2. Verify implicit derivatives graphically and numerically
3. Explore the logarithm function and its derivative $1/x$ geometrically
4. Build and simulate a related rates scenario numerically
5. Discover the relationship between $e^x$ and $\ln x$ through their derivatives

---

## Part 1 — Implicit Curves in Desmos (25 min)

Desmos can plot implicit curves directly. Type the equation as-is (e.g., `x^2 + y^2 = 25`).

### Exercise 1.1 — The Circle

Graph $x^2 + y^2 = 25$ in Desmos.

**Question 1a:** We showed $\dfrac{dy}{dx} = -\dfrac{x}{y}$. At the point $(3, 4)$:
- Compute $dy/dx$ numerically.
- Add the tangent line $y - 4 = -\frac{3}{4}(x-3)$ to Desmos.
- Confirm visually it is tangent to the circle at $(3, 4)$.

**Question 1b:** At what points on the circle is $dy/dx$ undefined? Explain geometrically.

**Question 1c:** At what points is $dy/dx = 1$? Find them algebraically (solve $-x/y = 1$) and verify on the graph.

---

### Exercise 1.2 — The Folium of Descartes

Graph $x^3 + y^3 = 6xy$ in Desmos. This is a beautiful curve with a loop.

**Question 1d:** We found $\dfrac{dy}{dx} = \dfrac{2y - x^2}{y^2 - 2x}$. 

At the point $(2, 2)$: Verify this point lies on the curve. Compute $dy/dx$ there. Add the tangent line to Desmos.

**Question 1e:** Find all points where the tangent is horizontal (numerically from the graph, then verify algebraically by setting $2y - x^2 = 0$ and substituting back).

**Question 1f:** Where is $dy/dx$ undefined on this curve? What is happening geometrically at those points?

---

### Exercise 1.3 — Lemniscate of Bernoulli

Graph $(x^2 + y^2)^2 = 4(x^2 - y^2)$ in Desmos (a figure-eight curve).

**Question 1g:** Describe the shape. How many $x$-intercepts does it have? $y$-intercepts?

**Question 1h:** Use implicit differentiation to find $dy/dx$. Show your work step by step.

**Question 1i:** At the point $(1, 1)$ — verify it lies on the curve — find the tangent line and add it to Desmos.

---

## Part 2 — The Logarithm Function and its Derivative (20 min)

### Exercise 2.1 — Geometric Meaning of $(\ln x)' = 1/x$

In Desmos, graph:
1. $y = \ln x$
2. $y = 1/x$

**Question 2a:** At $x = 1$: what is $\ln 1$? What is the slope of $y=\ln x$ there? What does $1/x$ give at $x=1$? Are these consistent?

**Question 2b:** At $x = 2$: what is the slope of $y = \ln x$? Verify using the central difference with $h = 0.001$:
$$\text{slope} \approx \frac{\ln(2.001) - \ln(1.999)}{0.002}$$

**Question 2c:** At $x = 0.5$: repeat the verification. Is the slope greater or less than 1? Does $y = 1/x$ give the same answer?

**Question 2d:** For what values of $x$ is $\ln x$ increasing? Decreasing? What does the derivative $1/x$ tell you about this?

**Question 2e:** Add $y = \ln|x|$ to Desmos. What is the domain? Graph $y = 1/x$ and observe it matches the slope of $y = \ln|x|$ on both sides of $x = 0$.

---

### Exercise 2.2 — The Number $e$ via the Derivative

The number $e$ is uniquely characterized by $\dfrac{d}{dx}[e^x]\big|_{x=0} = 1$, equivalently $\lim_{h\to0}\dfrac{e^h-1}{h} = 1$.

**Question 2f:** In Desmos, graph $y = a^x$ for various values of $a$ using a slider. Also graph the tangent line to $y = a^x$ at $x = 0$.

At $x = 0$, the slope of $y = a^x$ is $\lim_{h\to0}\dfrac{a^h - 1}{h} = \ln a$.

- For $a = 2$: slope at $x=0$ is $\ln 2 \approx ?$
- For $a = e$: slope at $x=0$ is $\ln e = ?$
- For $a = 3$: slope at $x=0$ is $\ln 3 \approx ?$

**Question 2g:** What value of $a$ makes the slope of $y = a^x$ at $x=0$ exactly equal to 1? Use Desmos to find it numerically, then confirm it is $e$.

---

## Part 3 — Related Rates Simulation (35 min)

### Exercise 3.1 — The Sliding Ladder (Numerical Simulation)

The ladder from Lecture 3: 10 m ladder, bottom sliding away at $v_x = 2$ m/s.

**Position at time $t$:** $x(t) = x_0 + 2t$ (bottom moves right), $y(t) = \sqrt{100 - x(t)^2}$ (top constrained to wall).

**Question 3a:** Using $x_0 = 0$ (start with ladder vertical), fill in the table:

| $t$ (s) | $x(t)$ | $y(t)$ | $dy/dt$ (numerical) |
|---------|--------|--------|---------------------|
| 0 | 0 | 10 | |
| 0.5 | 1 | | |
| 1.0 | 2 | | |
| 1.5 | 3 | | |
| 2.0 | 4 | | |
| 2.5 | 5 | | |
| 3.0 | 6 | | |
| 3.5 | 7 | | |
| 4.0 | 8 | | |
| 4.25 | 8.5 | | |

For the numerical $dy/dt$ column, use: $\dfrac{y(t+0.01) - y(t-0.01)}{0.02}$

**Question 3b:** From the implicit relation $\dfrac{dy}{dt} = -\dfrac{x}{y}\cdot\dfrac{dx}{dt}$, compute the exact $dy/dt$ at each row. Do the numerical and exact values agree?

**Question 3c:** What happens to $dy/dt$ as $x \to 10$ (ladder almost flat)? Why does this make physical sense? What does it imply about the mathematical model near $x = 10$?

**Question 3d:** In Desmos, plot $dy/dt$ vs $x$ for $x \in [0, 10)$. Describe the behavior.

---

### Exercise 3.2 — The Expanding Balloon

A balloon inflates so $r(t) = \sqrt{t}$ cm for $t > 0$ (in seconds).

**Question 3e:** Find $V(t)$ — express volume as a function of $t$.

**Question 3f:** Compute $dV/dt$ two ways:
- (i) Differentiate $V(t)$ directly with respect to $t$
- (ii) Use the related rates formula $\dfrac{dV}{dt} = 4\pi r^2\dfrac{dr}{dt}$, substituting $r = \sqrt{t}$ and $\dfrac{dr}{dt} = \dfrac{1}{2\sqrt{t}}$

**Question 3g:** Do both methods give the same answer? They should — explain why they must.

**Question 3h:** At $t = 4$ seconds: what is the radius? What is $dV/dt$? How does the rate of volume growth compare to $t = 1$?

---

### Exercise 3.3 — Design Your Own Related Rates Problem

**Question 3i:** Invent a related rates scenario involving one of the following:
- A cone being filled with liquid
- A shadow cast by a moving light source
- Two objects moving toward/away from each other

Write out:
1. The physical setup (a few sentences + diagram)
2. The equation relating the variables
3. The rates given and the rate to find
4. The full solution

Exchange with a partner and check each other's work.

---

## Part 4 — Inverse Trig Derivatives Numerically (20 min)

### Exercise 4.1 — Verifying $(\arctan x)' = 1/(1+x^2)$

**Question 4a:** At $x = 1$, the derivative should be $\dfrac{1}{1+1^2} = \dfrac{1}{2}$.

Verify numerically: $\dfrac{\arctan(1.001) - \arctan(0.999)}{0.002} \approx ?$

**Question 4b:** Fill in the table:

| $x$ | $\dfrac{1}{1+x^2}$ | Numerical derivative of $\arctan x$ | Match? |
|----|-------------------|-------------------------------------|--------|
| $0$ | | | |
| $0.5$ | | | |
| $1$ | | | |
| $2$ | | | |
| $5$ | | | |
| $10$ | | | |

**Question 4c:** In Desmos, graph $y = \arctan x$ and $y = \dfrac{1}{1+x^2}$ on separate axes (or use different colors). Describe how the derivative function reflects the behavior of $\arctan x$ — where is $\arctan x$ steepest? Where is $1/(1+x^2)$ largest?

**Question 4d:** What is $\lim_{x\to\infty}\arctan x$? What does this imply about $(\arctan x)'$ for large $x$? Does the formula $1/(1+x^2)$ confirm this?

---

## Lab Report Requirements

Include:
1. Completed tables from Parts 1, 3, and 4
2. Answers to all questions with clear labels
3. Desmos screenshots for Parts 1 and 2 (showing curves, tangent lines, and derivative functions)
4. Your original related rates problem from Exercise 3.3 with full solution
5. **Reflection** (5–8 sentences): What is the most geometrically surprising result from today's lab? How does the visual behavior of implicit curves connect to what implicit differentiation computes algebraically?

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — Implicit curves | 25 |
| Part 2 — Logarithm derivative | 20 |
| Part 3 — Related rates simulation | 30 |
| Part 4 — Inverse trig verification | 15 |
| Reflection | 10 |
| **Total** | **100** |
