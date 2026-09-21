# MATH 141 · Calculus I
## Week 7 Reference Sheet
### Shape of a Graph · Curve Sketching · Applied Optimization

---

## First Derivative Test

At critical number $c$:

| Sign change of $f'$ at $c$ | Conclusion |
|------------------------------|-----------|
| $+ \to -$ | Local maximum |
| $- \to +$ | Local minimum |
| No change | Not an extremum |

---

## Concavity and the Second Derivative

| Sign of $f''$ | Concavity |
|---------------|-----------|
| $f''(x)>0$ | Concave up (⌣) |
| $f''(x)<0$ | Concave down (⌢) |

**Inflection point:** concavity changes. Necessary (not sufficient) condition: $f''(c)=0$ or undefined.

---

## Second Derivative Test

At a critical number $c$ where $f'(c)=0$:

| $f''(c)$ | Conclusion |
|----------|-----------|
| $>0$ | Local minimum |
| $<0$ | Local maximum |
| $=0$ | **Inconclusive** — use First Derivative Test |

---

## Complete Curve Analysis Checklist

1. Domain
2. $f'(x)$: critical numbers, increase/decrease intervals
3. Classify critical points (First or Second Derivative Test)
4. $f''(x)$: concavity intervals, inflection points
5. Asymptotes (vertical, horizontal — Week 1 techniques)
6. Sketch

---

## Curve Sketching — The 8-Step Checklist

| Step | What to find |
|------|--------------|
| A. Domain | All $x$ where $f$ is defined |
| B. Intercepts | $f(0)$; solve $f(x)=0$ |
| C. Symmetry | Even ($f(-x)=f(x)$), odd ($f(-x)=-f(x)$), or periodic |
| D. Asymptotes | Vertical (denominator zero), horizontal (limits at $\pm\infty$), slant (deg num = deg denom + 1) |
| E. Increase/Decrease | Sign of $f'(x)$ |
| F. Local Extrema | First or Second Derivative Test |
| G. Concavity/Inflection | Sign of $f''(x)$ |
| H. Sketch | Combine everything |

**Slant asymptote:** for $f(x)=P(x)/Q(x)$ with $\deg P = \deg Q+1$, do polynomial long division:
$$f(x) = (\text{linear part}) + \frac{\text{remainder}}{Q(x)}$$
The linear part is the slant asymptote.

---

## Applied Optimization — The 8-Step Strategy

1. Understand the problem — identify objective and constraint(s)
2. Draw a diagram; label variables
3. Write the objective function
4. Use constraint(s) to reduce to ONE variable
5. Determine the domain (physical restrictions: lengths $>0$, etc.)
6. Differentiate; find critical numbers
7. **Verify** max or min (First/Second Derivative Test or Closed Interval Method)
8. Answer the original question with correct units

> ⚠️ Step 7 is not optional. Finding $f'(x)=0$ alone does not prove you have a maximum or minimum.

### Common Objective/Constraint Pairs

| Objective | Constraint |
|-----------|-----------|
| Maximize area/volume | Fixed perimeter/surface area/material |
| Minimize material/cost | Fixed volume/capacity |
| Minimize distance | Point on a given curve |
| Maximize profit | $\text{Profit} = \text{Revenue} - \text{Cost}$ |
| Minimize time | $\text{Time} = \text{distance}/\text{speed}$, possibly across media |

---

## Growth Rate Hierarchy (proved via L'Hôpital)

$$\ln x \ll x^\epsilon \ll x \ll x\ln x \ll x^2 \ll \cdots \ll 2^x \ll x! \ll x^x$$

(as $x\to\infty$; $\epsilon>0$ small)

Directly underlies Big-O complexity comparisons: $O(\log n) < O(n) < O(n\log n) < O(n^2) < O(2^n)$.

---

## Common Errors

| ❌ Wrong | ✅ Right |
|---------|---------|
| $f''(c)=0 \implies$ inflection point | Must verify concavity actually changes |
| Assuming Second Derivative Test always works | It's silent when $f''(c)=0$ |
| Forget to verify max/min in optimization | Always apply 2nd/1st Derivative Test after finding critical points |
| Skip domain restrictions in optimization | Physical constraints (positivity) restrict the domain |

---

## Week 7 Schedule

| Day | Event | Topic |
|-----|-------|-------|
| Monday | **Quiz 07** + Lecture 1 | I/D Test, First Derivative Test, concavity, Second Derivative Test |
| Tuesday | Lecture 2 | Complete curve sketching synthesis, slant asymptotes |
| Wednesday | Lecture 3 + **PS 7 released** (12:00) (12:00) | Applied optimization: full worked examples |
| Friday | **Lab 07** (15:00) | Growth hierarchies, curve sketching practice, optimization |

**Next week:** Introduction to Integral Calculus — Riemann Sums and the Definite Integral.
