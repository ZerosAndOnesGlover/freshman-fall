# MATH 141 · Calculus I
## Week 6 Reference Sheet
### Extrema · Rolle's Theorem · MVT · L'Hôpital's Rule

---

## Extrema — Definitions

| Term | Definition |
|------|-----------|
| Absolute max at $c$ | $f(c) \geq f(x)$ for ALL $x$ in domain |
| Absolute min at $c$ | $f(c) \leq f(x)$ for ALL $x$ in domain |
| Local max at $c$ | $f(c) \geq f(x)$ for $x$ NEAR $c$ |
| Local min at $c$ | $f(c) \leq f(x)$ for $x$ NEAR $c$ |
| Critical number | $c$ in domain where $f'(c)=0$ OR $f'(c)$ undefined |

---

## The Big Three Theorems

### Extreme Value Theorem (EVT)
$f$ continuous on $[a,b]$ $\implies$ $f$ attains an absolute max AND absolute min on $[a,b]$.
*(Requires: continuity + closed + bounded interval — all three necessary.)*

### Fermat's Theorem
$f$ has local extremum at $c$, and $f'(c)$ exists $\implies$ $f'(c)=0$.
*(Converse FALSE: $f'(c)=0$ does not guarantee an extremum — e.g., $f(x)=x^3$ at $x=0$.)*

### Rolle's Theorem
$f$ continuous on $[a,b]$, differentiable on $(a,b)$, $f(a)=f(b)$ $\implies$ $\exists\,c\in(a,b): f'(c)=0$.

### Mean Value Theorem (MVT)
$f$ continuous on $[a,b]$, differentiable on $(a,b)$ $\implies$ $\exists\,c\in(a,b): f'(c)=\dfrac{f(b)-f(a)}{b-a}$.
*(Rolle's Theorem is the special case $f(a)=f(b)$.)*

---

## Closed Interval Method (finding absolute extrema on $[a,b]$)

1. Find critical numbers in $(a,b)$
2. Evaluate $f$ at each critical number
3. Evaluate $f$ at both endpoints
4. Largest value = absolute max; smallest = absolute min

---

## MVT Corollaries (the theoretical foundation of curve sketching)

| Corollary | Statement |
|-----------|-----------|
| 1 | $f'(x)=0$ on interval $\implies$ $f$ constant there |
| 2 | $f'=g'$ on interval $\implies$ $f-g=$ constant (foundation of $+C$ in integration!) |
| 3 (I/D Test) | $f'>0 \implies f$ increasing; $f'<0 \implies f$ decreasing |

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

## Common Errors

| ❌ Wrong | ✅ Right |
|---------|---------|
| $f'(c)=0 \implies$ extremum at $c$ | Check that $f'$ changes sign (MVT Corollary 3); $x^3$ at $0$ is the counterexample |
| Using EVT on an open interval | EVT requires CLOSED, bounded interval |
| Forgetting to check endpoints in Closed Interval Method | Endpoints are always candidates |
| Apply L'Hôpital to a non-indeterminate limit | Always check form is $0/0$ or $\infty/\infty$ first |
| Apply quotient rule instead of L'Hôpital | Differentiate numerator and denominator separately |
| Assume $0^0$ form always equals 1 | Must actually compute the limit — it's genuinely indeterminate |

---

## Week 6 Schedule

| Day | Event | Topic |
|-----|-------|-------|
| Monday | **Quiz 06** + Lecture 1 | Extrema, EVT, Fermat's Theorem, Closed Interval Method |
| Tuesday | Lecture 2 | Rolle's Theorem, Mean Value Theorem, corollaries |
| Wednesday | Lecture 3 + **PS 6 released** (12:00) (12:00) | L'Hôpital's Rule, all indeterminate forms |
| Friday | **Lab 06** (15:00) | EVT hypotheses, MVT visualization, reading $f$ from $f'$, L'Hôpital numerically |

**Next week:** Shape of a graph (First and Second Derivative Tests, concavity), curve sketching, applied optimization.
