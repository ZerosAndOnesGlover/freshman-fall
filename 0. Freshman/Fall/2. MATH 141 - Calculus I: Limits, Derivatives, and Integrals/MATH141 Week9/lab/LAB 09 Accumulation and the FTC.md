# MATH 141 · Lab 09
## Accumulation Functions and the FTC Numerically

**Date:** Friday 27 November 2026 · 15:00–16:50 · Lab Section (Week 9) — covers Week 9 (Lectures 01–03)
**Duration:** 2 hours · **20 points**

> *Revised 2026-09-21.* 1A used to ask for Simpson's rule, which no lecture or handout gives. It now reuses
> the Lab 08 midpoint rule, which reaches the same ten decimal places at $n=100\,000$.

---

## Part 1: Building an Accumulation Function (6 pts)

Let $F(x)=\displaystyle\int_0^x e^{-t^2}\,dt$ — the function from Problem Set 9, Part D.

**1A.** Bring your `midpoint_rule(f, a, b, n)` from Lab 08 Exercise 4.1 (it is repeated below) and check it
on $\displaystyle\int_0^1 x^2\,dx=\tfrac13$ with $n=1000$. Use $n=100\,000$ for everything below. *(2 pts)*

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

**1B.** Tabulate $F(x)$ for $x=0,0.5,1,1.5,2,3$ to ten decimal places. *(1 pt)*

**1C.** $F$ is increasing and bounded above. Estimate its limit as $x\to\infty$ by evaluating at
$x=3,4,5,6$, and compare with $\dfrac{\sqrt\pi}{2}$. *(1 pt)*

**1D.** Verify FTC 1 numerically: compute $\dfrac{F(x+h)-F(x-h)}{2h}$ with $h=10^{-5}$ at
$x=0.5,1,2$ and compare each with $e^{-x^2}$. Report the agreement to as many digits as you get.
*(2 pts)*

---

## Part 2: Shape From the Derivative Alone (5 pts)

Using **only** $F'(x)=e^{-x^2}$ and $F''(x)=-2xe^{-x^2}$ — no table of values:

**2A.** Predict where $F$ increases, where it is concave up, and where it has an inflection point.
*(2 pts)*

**2B.** Now plot $F$ from your Part 1 data and confirm every prediction. *(2 pts)*

**2C.** State in one sentence what you have just demonstrated about a function with no elementary
formula. *(1 pt)*

---

## Part 3: Displacement Versus Distance (5 pts)

A particle has $v(t)=t^2-4$ m/s on $[0,4]$.

**3A.** Compute $\displaystyle\int_0^4 v\,dt$ numerically. *(1 pt)*

**3B.** Compute $\displaystyle\int_0^4 \lvert v\rvert\,dt$ numerically. *(1 pt)*

**3C.** Find the sign change of $v$, split the interval there, and compute the two pieces separately.
Confirm that they sum to your 3B answer and *differ* to your 3A answer. *(2 pts)*

**3D.** Plot position $s(t)=\int_0^t v$ alongside cumulative distance
$d(t)=\int_0^t\lvert v\rvert$. Describe in two sentences where and why the curves separate. *(1 pt)*

---

## Part 4: The Chain Rule Form (4 pts)

Let $G(x)=\displaystyle\int_{x^2}^{x^3}\sin t\,dt$.

**4A.** Evaluate $G$ numerically at $x=1.3$ using `midpoint_rule`. *(1 pt)*

**4B.** Estimate $G'(1.3)$ by central difference. *(1 pt)*

**4C.** Compute $3x^2\sin(x^3)-2x\sin(x^2)$ at $x=1.3$ and compare. Report the agreement. *(1 pt)*

**4D.** Repeat 4B–4C at $x=0.7$ and $x=2.0$. Does the formula hold at all three points? *(1 pt)*

---

## Deliverables

Your code, all tables, both plots, and written answers to 2C and 3D.

## Grading

| Part | Points |
|---|---|
| 1 — integrator, table, limit, FTC 1 verified | 6 |
| 2 — shape predicted from the derivative, then confirmed | 5 |
| 3 — displacement and distance computed and distinguished | 5 |
| 4 — chain-rule form verified at three points | 4 |
| **Total** | **20** |

---

*MATH 141 · Week 9 · Lab 09 · © CSE Department*
