# MATH 142 · Calculus II
## Lab 11: Slope Fields, Euler's Method, and Runge–Kutta
### Week 11 Lab Session

---

**Duration:** 2 hours
**Format:** Individual or pairs (pairs submit separate reports)
**Graded on:** completion + correctness — **100 points**
**Tools required:** Python 3 with `mpmath`; `matplotlib` for Part A

---

## Overview

Most differential equations cannot be solved in closed form — the same situation as most integrals, and the response is the same: **step forward numerically, and analyse the error.**

**This lab measures the order of three methods**, on a problem whose exact solution you know so the error can be computed honestly. The result should look familiar: **the same order analysis you did in Lab 0, in Week 0, on Simpson's rule.**

Then it turns the methods on an equation that has no solution at all.

---

## Part A — Slope Fields (15 pts)

**A1 (9 pts).** Plot the slope field of $\dfrac{dy}{dx}=y-x$ on $[-2,3]\times[-2,5]$.

Overlay the solution curves through $(0,2)$, $(0,1)$ and $(0,0)$.

**A2 (6 pts).** The exact solution through $(0,2)$ is $y=e^x+x+1$. *(You may verify this by substitution.)*

- (a) Confirm your plotted curve matches.
- (b) One of your three curves is a straight line. **Which initial condition gives it, and why does the slope field make that obvious?**

---

## Part B — Euler's Method and Its Order (30 pts)

Test problem: $\;y'=y-x$, $\;y(0)=2$, exact solution $y=e^x+x+1$, so $y(1)=e+2=4.71828182845905\ldots$

**B1 (12 pts).** Implement Euler's method

$$y_{n+1}=y_n+h\,f(x_n,y_n)$$

and compute $y(1)$ using $n = 10,\ 20,\ 40,\ 80,\ 160,\ 320$ steps. Tabulate the value and the error.

**B2 (10 pts).** Add a column of **error ratios on doubling $n$**.

- (a) What does the ratio approach?
- (b) Hence what is the **order** of Euler's method?

**B3 (8 pts).** From your data, estimate how many steps Euler would need for an error below $10^{-10}$.

Comment on whether that is practical.

---

## Part C — Two Better Methods (35 pts)

**C1 (12 pts).** Implement **improved Euler** (Heun's method), which averages the slope at the start and at the predicted endpoint:

$$k_1 = f(x_n,y_n),\qquad k_2 = f(x_n+h,\ y_n+hk_1),\qquad y_{n+1}=y_n+\frac h2(k_1+k_2)$$

Repeat the table of Part B, including the ratio column. **State its order.**

**C2 (13 pts).** Implement **RK4**:

$$k_1=f(x_n,y_n),\quad k_2=f\!\left(x_n+\tfrac h2,y_n+\tfrac h2k_1\right),\quad k_3=f\!\left(x_n+\tfrac h2,y_n+\tfrac h2k_2\right),\quad k_4=f(x_n+h,y_n+hk_3)$$

$$y_{n+1}=y_n+\frac h6\left(k_1+2k_2+2k_3+k_4\right)$$

Repeat the table. **State its order.**

**C3 (10 pts).** Build a summary comparison at $n=320$:

| method | error at $n=320$ | order | evaluations of $f$ per step |
|---|---|---|---|

- (a) By what factor does RK4 beat Euler?
- (b) **RK4 uses four function evaluations per step against Euler's one.** Is that a good trade? Justify with your numbers.
- (c) **Where have you seen the ratio 16 before in this course?**

---

## Part D — An Equation With No Solution Formula (20 pts)

$$\frac{dy}{dx}=x^2+y^2,\qquad y(0)=0$$

**D1 (6 pts).** Show it is neither separable nor linear. Confirm that `sympy`'s `dsolve` fails on it, and report what it does.

**D2 (8 pts).** Use RK4 to estimate $y(1)$ with $n=10,\ 100,\ 1000$ steps.

**Report the values and state how many digits you believe are correct**, justifying from the agreement between successive refinements.

**D3 (6 pts).** You have produced a number for a quantity that has no formula.

In two or three sentences, relate this to Week 0's opening claim about $\int e^{-x^2}dx$ — **what is the same, and what is different?**

*(Consider: in Week 10 the integral got a series. Does this equation?)*

---

## What to Submit

1. The slope field plot with three solution curves (Part A)
2. Euler's table with ratios and your order (Part B)
3. Both improved tables and the comparison (Part C)
4. The Riccati results and your reflection (Part D)

---

## Marking Summary

| Part | Points | Focus |
|---|---|---|
| A | 15 | Slope fields; reading behaviour without solving |
| B | 30 | Euler's method, measured order 1 |
| C | 35 | RK2 and RK4, orders 2 and 4 |
| D | 20 | An equation with no closed form |
| **Total** | **100** | |

---

*This is the eleventh lab, and the eleventh time you have measured an order of convergence. That number has decided every question of practicality in this course.*
