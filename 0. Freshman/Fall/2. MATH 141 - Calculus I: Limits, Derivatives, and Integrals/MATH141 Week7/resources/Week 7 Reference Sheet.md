# MATH 141 — Calculus I
## Week 7 Reference Sheet
### L'Hôpital's Rule · Curve Sketching · Applied Optimization

---

## L'Hôpital's Rule

**Applies only to** $\dfrac{0}{0}$ or $\dfrac{\infty}{\infty}$ forms:

$$\lim_{x\to a}\frac{f(x)}{g(x)} = \lim_{x\to a}\frac{f'(x)}{g'(x)}$$

*(Differentiate numerator and denominator SEPARATELY — this is NOT the quotient rule.)*

**Can be reapplied** if the new limit is still indeterminate.

**Always verify the indeterminate form FIRST** — applying the rule to a non-indeterminate limit gives a wrong answer.

### Converting Other Indeterminate Forms

| Form | Strategy |
|------|----------|
| $0\cdot\infty$ | Rewrite as $\dfrac{f}{1/g}$ or $\dfrac{g}{1/f}$ → $0/0$ or $\infty/\infty$ |
| $\infty-\infty$ | Combine into a single fraction (common denominator) → $0/0$ |
| $0^0$, $1^\infty$, $\infty^0$ | Take $\ln$ of both sides → exponent becomes $0\cdot\infty$ product → solve → exponentiate with $e$ |

**Key limit proved via L'Hôpital:** $\displaystyle\lim_{x\to\infty}\left(1+\dfrac1x\right)^x = e$

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
| Apply L'Hôpital to a non-indeterminate limit | Always check form is $0/0$ or $\infty/\infty$ first |
| Apply quotient rule instead of L'Hôpital | Differentiate numerator and denominator separately |
| Forget to verify max/min in optimization | Always apply 2nd/1st Derivative Test after finding critical points |
| Skip domain restrictions in optimization | Physical constraints (positivity) restrict the domain |
| Assume $0^0$ form always equals 1 | Must actually compute the limit — it's genuinely indeterminate |

---

## Week 7 Schedule

| Day | Event | Topic |
|-----|-------|-------|
| Monday | **Quiz 07** + Lecture 1 | L'Hôpital's Rule, all indeterminate forms |
| Tuesday | Lecture 2 | Complete curve sketching synthesis, slant asymptotes |
| Friday | **Lab 07** | Growth hierarchies, curve sketching practice, optimization design |
| Wednesday | Lecture 3 + **PS5 Released** | Applied optimization: full worked examples |

**Next week:** Introduction to Integral Calculus — Riemann Sums and the Definite Integral.
