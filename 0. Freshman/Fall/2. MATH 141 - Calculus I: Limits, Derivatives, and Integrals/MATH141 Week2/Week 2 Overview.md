# MATH 141 · Week 2 Overview
## Continuity and the Intermediate Value Theorem

---

## This Week

Week 1 made "approaches" precise. This week uses that precision to define **continuity**, classify
the ways it can fail, and prove the first genuinely non-obvious theorem of the course.

| Day | Lecture | Topic |
|---|---|---|
| Monday | 1 | Continuity: The Three-Part Definition |
| Tuesday | 2 | Classifying Discontinuities |
| Wednesday | 3 | The Intermediate Value Theorem |
| — | Lab 02 | Continuity, Discontinuity, and Bisection |

**Quiz 02** at the start of Monday's lecture, covering Week 1.
**Problem Set 2** due Wednesday of Week 3.

---

## Learning Objectives

1. State and apply the three-part definition of continuity at a point
2. Classify a discontinuity as removable, jump, infinite, or essential
3. Repair a removable discontinuity by continuous extension
4. State the IVT with its hypotheses, and apply it to prove a root exists
5. Implement bisection and compute the number of steps needed for a given accuracy
6. Explain why the IVT is false over $\mathbb{Q}$, and what that says about $\mathbb{R}$

---

## Key Results

| | |
|---|---|
| Continuity at $a$ | $f(a)$ defined; $\lim_{x\to a}f$ exists; the two agree |
| Removable | Limit exists but $\ne f(a)$ — **repairable** |
| Jump | One-sided limits exist, differ |
| Infinite | A one-sided limit is $\pm\infty$ |
| Essential | A one-sided limit fails for any other reason |
| Rational $\frac pq$ with $q(a)=0$ | $p(a)\ne0$ ⟹ infinite; $p(a)=0$ ⟹ factor and re-check |
| **IVT** | Continuous on $[a,b]$, $N$ between $f(a),f(b)$ ⟹ some $c$ with $f(c)=N$ |
| Bolzano | Opposite signs ⟹ a root |
| Bisection | $n\ge\log_2\!\big((b-a)/\varepsilon\big)$, **rounded up** |

---

## Common Errors

| Error | Correction |
|---|---|
| Cancelling without noting $x\ne a$ | Legitimate, because the limit never evaluates *at* $a$ |
| Calling every $\tfrac00$ removable | Factor first — $\tfrac{x-1}{(x-1)^2}$ is infinite |
| Assuming the IVT locates the root | It gives **existence only** |
| Thinking the converse of the IVT holds | $\sin(1/x)$ takes all values and is discontinuous |
| Rounding the bisection count down | Always **up** |

---

## Connections

**Back:** Week 1's ε-δ definition is what makes continuity provable rather than pictorial.

**Forward:** Week 3 shows differentiability implies continuity but not conversely. The IVT proves the
MVT (Week 6) and the MVT for integrals (Week 8). Bisection reappears in MATH 341 as the guaranteed —
if slow — root finder.

---

*MATH 141 · Week 2 · © CSE Department*
