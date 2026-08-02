# MATH 141 · Calculus I
## Lab 08 (Friday, Week 8)
### Riemann Sums, Convergence, and Sample-Point Independence

**Duration:** 2 hours | **Tools:** Desmos, Python
**Submission:** Written report due Monday, Week 9
**Total: 100 points**

> **No antiderivatives in this lab.** The Fundamental Theorem arrives in Week 9. Every exact value
> here comes from a Riemann-sum limit or from geometry, because the point of this lab is to see what
> the definite integral *is* before you learn the shortcut for computing it.

---

## Lab Objectives

1. Visualise Riemann sums as rectangles and watch them converge
2. Compare the convergence rates of left, right, and midpoint sums numerically
3. Establish experimentally that the limit does not depend on the sample points
4. Use the comparison property to bracket an integral you cannot evaluate
5. Build a numerical integrator and measure its accuracy against its cost

---

## Part 1 — Watching Riemann Sums Converge (25 pts)

### Exercise 1.1 — Visualising Rectangles

For $f(x) = x^2$ on $[0,1]$, whose exact area is $\tfrac13$ (derived in Monday's lecture).

**1a.** *(3)* Sketch the right-endpoint rectangles for $n=4$ and shade the region. Does the
approximation overestimate or underestimate? Justify from the fact that $f$ is increasing.

**1b.** *(2)* Increase to $n=10$, then $n=50$. Describe how the fit improves.

**1c.** *(6)* Complete the table using $R_n = \dfrac{(n+1)(2n+1)}{6n^2}$:

| $n$ | $R_n$ | Error ($R_n - 1/3$) |
|-----|-------|---------------------|
| 4 | | |
| 10 | | |
| 50 | | |
| 100 | | |
| 1000 | | |

**1d.** *(4)* As $n$ **doubles**, by what factor does the error fall? What order of convergence does
that indicate? Compare with the forward-vs-central difference finding from Lab 3.

---

### Exercise 1.2 — Comparing Left, Right, and Midpoint

**1e.** *(3)* Derive the closed form for $L_n$ on this same function and interval.
*(It differs from $R_n$ in one predictable way.)*

**1f.** *(4)* Derive the closed form for $M_n$. The midpoints are
$\bar x_i = \dfrac{2i-1}{2n}$, and you will need $\sum_{i=1}^{n}(2i-1)^2 = \dfrac{n(4n^2-1)}{3}$.

**1g.** *(3)* Complete the comparison at $n=10$:

| Method | Value | Error |
|--------|-------|-------|
| $L_{10}$ | | |
| $R_{10}$ | | |
| $M_{10}$ | | |

---

## Part 2 — Sample-Point Independence (25 pts)

The definition of $\int_a^b f$ allows the sample point $x_i^*$ to be **anywhere** in its subinterval.
This part tests that claim experimentally.

**2a.** *(6)* Write a function `riemann(f, a, b, n, rule)` where `rule` selects `"left"`, `"right"`,
`"mid"`, or `"random"` (a uniformly random point in each subinterval).

**2b.** *(6)* For $f(x)=x^2$ on $[0,1]$, tabulate all four rules at $n = 10, 100, 10^4, 10^6$.
Run the random rule three times at each $n$ and report all three values.

**2c.** *(5)* At $n=10$ the four rules disagree substantially. At $n=10^6$ they agree to how many
decimal places? State the number.

**2d.** *(4)* The random rule gives a *different* answer every run. Does it still converge? What
does your table show happening to the spread between runs as $n$ grows?

**2e.** *(4)* Explain what your data demonstrates about the **definition** of the definite integral —
specifically, why the definition would be broken if these four sequences had different limits.

---

## Part 3 — Bounding an Integral You Cannot Evaluate (20 pts)

Consider $\displaystyle\int_0^2 \frac{dx}{1+x^3}$, which has no elementary antiderivative you can
write down at this stage.

**3a.** *(4)* Find the maximum and minimum of the integrand on $[0,2]$, showing that it is monotone
there. Apply the comparison property to bracket the integral.

**3b.** *(5)* Use your `riemann` function with $n=10^6$ to estimate the true value. Where does it sit
inside your bracket?

**3c.** *(6)* Split $[0,2]$ into 2, then 4, then 8 equal subintervals, and apply the comparison
property **on each piece separately**, summing the bounds. Tabulate how the bracket width shrinks.

**3d.** *(5)* Your Part 3c procedure is doing something you have already seen. Identify it, and
explain the connection in three sentences.

---

## Part 4 — Building a Numerical Integrator (25 pts)

### Exercise 4.1 — Midpoint Rule

```python
def midpoint_rule(f, a, b, n):
    """Approximate the integral of f from a to b with n midpoint rectangles."""
    delta_x = (b - a) / n
    total = 0.0
    for i in range(n):
        midpoint = a + (i + 0.5) * delta_x
        total += f(midpoint) * delta_x
    return total
```

**4a.** *(4)* Trace this by hand for $f(x)=x^2$, $a=0$, $b=1$, $n=2$. Check against your $M_n$ formula
from 1f.

**4b.** *(5)* Run it for $f(x) = e^{-x^2}$ on $[-2,2]$ with $n=1000$. The true value is
approximately $1.7642$ — report your error.

**4c.** *(6)* Tabulate the error for $n = 10, 10^2, 10^3, 10^4, 10^5$. Confirm the $O(1/n^2)$ rate
you found in Part 1, and note the $n$ beyond which floating-point noise stops the improvement.

**4d.** *(5)* Write pseudocode for an **adaptive** version: double $n$ until consecutive estimates
differ by less than a tolerance $\varepsilon$. What goes wrong if $\varepsilon$ is set below the
noise floor you found in 4c?

**4e.** *(5)* $e^{-x^2}$ has no elementary antiderivative, so no amount of Week 9 technique will give
you an exact answer for 4b. Discuss what that means for the relationship between the exact and the
numerical approach — and which problems each one owns.

---

## Lab Report Requirements

1. All completed tables (Parts 1–4)
2. A Desmos screenshot of the rectangles from 1a
3. Your `riemann` implementation and its output
4. Answers to all written questions

**Reflection (5 pts, 6–8 sentences):** Before this lab the definite integral may have felt like a
definition to memorise. After watching four different sampling rules converge to the same number,
what do you now think the definition is actually asserting? Where would you reach for a numerical
integrator in practice, and where would you not?

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — Riemann sum convergence | 25 |
| Part 2 — Sample-point independence | 25 |
| Part 3 — Bounding by comparison | 20 |
| Part 4 — Numerical integrator | 25 |
| Reflection | 5 |
| **Total** | **100** |

---

*MATH 141 · Week 8 · Lab 08 · © CSE Department*
