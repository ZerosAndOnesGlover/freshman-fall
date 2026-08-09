# MATH 141 · Calculus I
## Problem Set 6
### Topic: Extrema, Rolle's Theorem, Mean Value Theorem, Shape of a Graph
**Released:** Wednesday, Week 6 · **Due:** Wednesday, Week 7 (start of class)

---

## Part A — Absolute Extrema (4 pts each)

**A1.** Find all critical numbers:

- (a) $f(x) = x^3 - 6x^2 + 9x + 2$
- (b) $g(x) = \dfrac{x-1}{x^2+3}$
- (c) $h(x) = x^{1/3}(x+4)$
- (d) $k(x) = 2\cos x + x$ on $[0, 2\pi]$

**A2.** Use the Closed Interval Method to find the absolute maximum and minimum values:

- (a) $f(x) = x^3 - 3x + 1$ on $[-2, 3]$
- (b) $f(x) = \dfrac{x}{x^2+4}$ on $[0, 4]$
- (c) $f(x) = x - 2\sin x$ on $[0, 2\pi]$

**A3.** A continuous function on $[0,5]$ has $f(0)=4$, $f(5)=4$, and critical numbers only at $x=2$ and $x=4$, where $f(2)=9$ and $f(4)=1$. Determine the absolute max and min values on $[0,5]$, and state which theorem guarantees these values are actually attained.

---

## Part B — Rolle's Theorem and MVT (5 pts each)

**B1.** For each function, verify whether Rolle's Theorem applies on the given interval. If it applies, find all values of $c$. If not, explain which hypothesis fails.

- (a) $f(x) = x^2 - 2x$ on $[0,2]$
- (b) $f(x) = 1 - x^{2/3}$ on $[-1,1]$
- (c) $f(x) = \tan x$ on $[0, \pi]$

**B2.** For each function, verify the MVT applies on the given interval and find all values of $c$.

- (a) $f(x) = x^3 + x - 1$ on $[0,2]$
- (b) $f(x) = \sqrt{x+1}$ on $[0,3]$

**B3.** Use Rolle's Theorem to show that $f(x) = x^5 + 2x - 3$ has exactly one real root.

**B4.** Two towns A and B are connected by a mountain road 45 km long. A cyclist covers the distance in exactly 1.5 hours. Prove, using the MVT, that at some instant the cyclist's speed was exactly 30 km/h. State the theorem's hypotheses and verify they apply to this physical scenario.

**B5.** Use the MVT to prove that for all $x, y \in \mathbb{R}$ with $x < y$:
$$|\sin y - \sin x| \leq |y - x|$$

*(Hint: apply MVT to $f(t) = \sin t$ on $[x,y]$, and use $|\cos c| \leq 1$.)*

---

## Part C — Shape of a Graph (5 pts each)

For each function: find intervals of increase/decrease, classify all local extrema (state which test you used), find intervals of concavity, and find all inflection points.

**C1.** $f(x) = x^3 - 3x^2 - 9x + 5$

**C2.** $f(x) = 3x^4 - 4x^3$

**C3.** $f(x) = \dfrac{x^2}{x^2+3}$

**C4.** $f(x) = xe^{-x^2}$

**C5.** $f(x) = x - 2\sin x$ on $[0, 2\pi]$

---

## Part D — Second Derivative Test (4 pts each)

**D1.** Use the Second Derivative Test to classify all critical points. If the test is inconclusive at any point, use the First Derivative Test instead.

- (a) $f(x) = x^4 - 4x^2$
- (b) $f(x) = x^5$
- (c) $f(x) = x^3 - 3x^2 + 3x - 1$

**D2.** Construct a function $f(x)$ such that $f'(0) = 0$, $f''(0) = 0$, but $f$ has a local minimum at $x=0$. Verify your example works by computing derivatives directly.

---

## Part E — Curve Construction and Sketching (6 pts each)

**E1.** Sketch a possible graph of a function $f$ satisfying all of the following simultaneously:
- $f$ is continuous on $\mathbb{R}$
- $f'(x) > 0$ for $x < -1$ and $x > 3$; $f'(x) < 0$ for $-1 < x < 3$
- $f''(x) < 0$ for $x < 1$; $f''(x) > 0$ for $x > 1$
- $f(-1) = 4$, $f(3) = -2$, $f(1) = 1$

Label all local extrema and the inflection point on your sketch.

**E2.** A function $g$ satisfies $g'(x) = (x-1)^2(x-3)$.

- (a) Find all critical numbers of $g$.
- (b) Determine intervals of increase/decrease.
- (c) Classify each critical point using the First Derivative Test.
- (d) Find $g''(x)$ and determine concavity intervals.

*(Note: you are not given $g(x)$ explicitly — work entirely from $g'(x)$.)*

**E3.** Perform a complete analysis (domain, symmetry, intercepts if easy, increase/decrease, extrema, concavity, inflection points, asymptotes) of:
$$f(x) = \frac{x^2 - 1}{x^2 + 1}$$

---

## Part F — Conceptual and Proof (6 pts each)

**F1.** A student says: "If $f'(c) = 0$, then $f$ has a local extremum at $c$." Give a specific counterexample and explain, using the definitions from Monday's lecture, exactly why the counterexample fails to be a local extremum.

**F2.** Prove: if $f$ is differentiable on $\mathbb{R}$, $f'(x) \geq 0$ for all $x$, and $f'(x) = 0$ at only finitely many points, then $f$ is strictly increasing on $\mathbb{R}$ (not just non-decreasing).

*(Hint: use the MVT on any interval $[a,b]$ and account for the finitely many zero points.)*

**F3.** Explain the logical relationship between Rolle's Theorem and the Mean Value Theorem. Is Rolle's Theorem a special case of the MVT, or is the MVT proved using Rolle's Theorem, or both? Justify with reference to the proofs given in lecture.

**F4 (Bonus — 4 pts).** Prove using the MVT that $e^x \geq 1 + x$ for all $x \geq 0$.

*(Hint: Let $f(t) = e^t - 1 - t$. Show $f(0)=0$ and analyze $f'(t)$.)*

---

## Grading Summary

| Part | Points | Focus |
|------|--------|-------|
| A (3 problems, various) | 25 | Absolute extrema |
| B (5 problems, various) | 27 | Rolle's Theorem, MVT |
| C (5 × 5) | 25 | Shape of graph (comprehensive) |
| D (2 problems) | 12 | Second Derivative Test |
| E (3 problems) | 18 | Curve construction/sketching |
| F (3 × 6 + bonus 4) | 18 + 4 | Conceptual/proof |
| **Total** | **125 + 4 bonus** | |
