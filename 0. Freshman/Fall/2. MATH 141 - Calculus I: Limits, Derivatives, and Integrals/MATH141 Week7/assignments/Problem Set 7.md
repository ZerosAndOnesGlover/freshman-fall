# MATH 141 — Calculus I
## Problem Set 7
### Topic: L'Hôpital's Rule, Curve Sketching, Applied Optimization
**Released:** Wednesday, Week 7 | **Due:** Wednesday, Week 6 (start of class)

---

## Part A — L'Hôpital's Rule: Basic Forms (3 pts each)

**A1.** Evaluate using L'Hôpital's Rule. Verify the indeterminate form before applying.

- (a) $\displaystyle\lim_{x\to0}\frac{\sin 3x}{x}$ (verify against the Week 1 special trig limit method)
- (b) $\displaystyle\lim_{x\to1}\frac{\ln x}{x-1}$
- (c) $\displaystyle\lim_{x\to\infty}\frac{5x^2+3x}{2x^2-1}$ (verify against the Week 1 algebraic method — divide by highest power)
- (d) $\displaystyle\lim_{x\to0}\frac{e^x-e^{-x}}{\sin x}$
- (e) $\displaystyle\lim_{x\to\pi/2}\frac{\cos x}{x-\pi/2}$
- (f) $\displaystyle\lim_{x\to\infty}\frac{\ln(\ln x)}{\ln x}$

**A2.** Some of these require applying L'Hôpital's Rule more than once. Evaluate:

- (a) $\displaystyle\lim_{x\to0}\frac{x-\sin x}{x^3}$
- (b) $\displaystyle\lim_{x\to0}\frac{e^x-1-x-x^2/2}{x^3}$
- (c) $\displaystyle\lim_{x\to\infty}\frac{x^3}{e^{2x}}$

---

## Part B — Other Indeterminate Forms (4 pts each)

**B1.** Convert to $0/0$ or $\infty/\infty$, then apply L'Hôpital's Rule:

- (a) $\displaystyle\lim_{x\to0^+}\sqrt{x}\ln x$ *(form $0\cdot\infty$)*
- (b) $\displaystyle\lim_{x\to\infty}xe^{-x}$ *(form $0\cdot\infty$)*
- (c) $\displaystyle\lim_{x\to0}\left(\frac{1}{x}-\csc x\right)$ *(form $\infty-\infty$)*
- (d) $\displaystyle\lim_{x\to1^+}\left(\frac{1}{\ln x}-\frac{1}{x-1}\right)$ *(form $\infty-\infty$)*

**B2.** Use logarithms to handle these exponential indeterminate forms:

- (a) $\displaystyle\lim_{x\to0^+}(1+2x)^{1/x}$ *(form $1^\infty$)*
- (b) $\displaystyle\lim_{x\to\infty}x^{1/\ln x}$ *(form $\infty^0$)*
- (c) $\displaystyle\lim_{x\to0^+}(\sin x)^x$ *(form $0^0$)*
- (d) $\displaystyle\lim_{x\to\infty}\left(1-\frac{3}{x}\right)^{2x}$ *(form $1^\infty$)*

**B3.** Explain why L'Hôpital's Rule cannot be directly applied to $\displaystyle\lim_{x\to\infty}\frac{x+\cos x}{x}$ in a way that terminates usefully. Solve this limit correctly using an alternative method, and explain the general lesson.

---

## Part C — Complete Curve Sketching (10 pts each)

For each function, perform the FULL curve sketching analysis: domain, intercepts, symmetry, all asymptotes, intervals of increase/decrease, classified local extrema, intervals of concavity, inflection points. State each result clearly (you do not need to submit an actual hand-drawn graph, but your written analysis should be complete enough that someone else could sketch it accurately from your work).

**C1.** $f(x) = \dfrac{2x^2}{x^2-1}$

**C2.** $f(x) = x^4 - 2x^2 + 1$

**C3.** $f(x) = \dfrac{x^2+1}{x}$ *(has a slant asymptote)*

**C4.** $f(x) = x^2 e^{-x}$

**C5.** $f(x) = \ln(x^2+1)$

---

## Part D — Applied Optimization (7 pts each)

For each problem, follow the full 8-step strategy: set up variables, write objective and constraint, reduce to one variable, state domain, differentiate, find and verify critical numbers, answer the question with correct units and physical interpretation.

**D1.** A rectangular box (with a square base and open top) must have volume $32{,}000\ \text{cm}^3$. Find the dimensions that minimize the amount of material used.

**D2.** A rectangle is inscribed in the ellipse $\dfrac{x^2}{16}+\dfrac{y^2}{9}=1$ with sides parallel to the axes. Find the dimensions of the rectangle with maximum area.

**D3.** A piece of wire $20$ m long is cut into two pieces. One piece is bent into a square, the other into an equilateral triangle. How should the wire be cut to (a) maximize and (b) minimize the total enclosed area? *(For (a), consider the boundary case carefully — the answer may involve using all the wire for one shape.)*

**D4.** Find the dimensions of the right circular cylinder of maximum volume that can be inscribed in a sphere of radius $R$.

**D5.** A retailer sells $x$ units of a product per month at price $p(x) = 200 - 0.5x$ dollars. The cost to produce $x$ units is $C(x) = 3000 + 40x$. Find the production level $x$ that maximizes profit, and compute the maximum profit.

**D6.** A window is in the shape of a rectangle topped by a semicircle. The perimeter of the entire window (including the diameter of the semicircle, which is NOT part of the perimeter since it's internal) is $10$ m. Find the dimensions that maximize the area of the window admitting the most light.

---

## Part E — Conceptual and Proof (5 pts each)

**E1.** State precisely what conditions must be verified before applying L'Hôpital's Rule. Give an example (different from the lecture) where blindly applying the rule without checking the indeterminate form gives an incorrect answer.

**E2.** Explain the logical connection between L'Hôpital's Rule and the Mean Value Theorem discussed in Week 6. Specifically, describe how Cauchy's Generalized MVT is used in the proof.

**E3.** In an optimization problem, why is it not sufficient to simply find where $f'(x)=0$ and declare that the answer? Describe the additional verification step(s) required, referencing specific tests from Week 4.

---

## Grading Summary

| Part | Points | Focus |
|------|--------|-------|
| A (6+3 problems) | 27 | L'Hôpital's Rule — basic forms |
| B (3+4+1 problems) | 33 | Other indeterminate forms |
| C (5 × 10) | 50 | Full curve sketching synthesis |
| D (6 × 7) | 42 | Applied optimization |
| E (3 × 5) | 15 | Conceptual understanding |
| **Total** | **167** | |
