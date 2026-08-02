# MATH 141 · Calculus I
## Week 6 Reference Sheet
### Extrema · Rolle's Theorem · MVT · Shape of a Graph

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

## Common Errors

| ❌ Wrong | ✅ Right |
|---------|---------|
| $f'(c)=0 \implies$ extremum at $c$ | Must check sign change (First Deriv. Test) |
| $f''(c)=0 \implies$ inflection point | Must verify concavity actually changes |
| Using EVT on an open interval | EVT requires CLOSED, bounded interval |
| Forgetting to check endpoints in Closed Interval Method | Endpoints are always candidates |
| Assuming Second Derivative Test always works | It's silent when $f''(c)=0$ |

---

## Week 6 Schedule

| Day | Event | Topic |
|-----|-------|-------|
| Monday | **Quiz 06** + Lecture 1 | Extrema, EVT, Fermat's Theorem, Closed Interval Method |
| Tuesday | Lecture 2 | Rolle's Theorem, Mean Value Theorem, corollaries |
| Friday | **Lab 06** | EVT hypotheses, MVT visualization, $f/f'/f''$ synthesis |
| Wednesday | Lecture 3 + **PS4 Released** | I/D Test, concavity, First & Second Derivative Tests |

**Next week:** Curve sketching synthesis, L'Hôpital's Rule, applied optimization problems.
