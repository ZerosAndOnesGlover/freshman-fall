# MATH 141 · Calculus I
## Lab 10 (Friday, Week 10)
### Substitution Pattern Recognition, Symmetry, and the Tabular Method for Integration by Parts

**Duration:** 2 hours | **Tools:** Desmos, Python (optional)
**Submission:** Written report due Monday, Week 8

---

## Lab Objectives

1. Build fluency in recognizing substitution patterns quickly
2. Verify substitution results numerically and graphically
3. Confirm symmetry shortcuts using Desmos visualizations
4. Learn and apply the tabular method for repeated integration by parts
5. Explore the "solve for $I$" technique with a numerical sanity check

---

## Part 1 — Substitution Pattern Recognition Drill (25 min)

For each integral, do NOT fully solve it — just identify the substitution $u=g(x)$ you would use, and verify that $du$ (up to a constant) appears elsewhere in the integrand. This drill builds the pattern-recognition speed that makes substitution feel automatic rather than laborious.

| # | Integral | Your choice of $u$ | Does $du$ appear (up to constant)? |
|---|----------|---------------------|--------------------------------------|
| 1 | $\int x^4\sin(x^5)\,dx$ | | |
| 2 | $\int \dfrac{e^{\sqrt x}}{\sqrt x}\,dx$ | | |
| 3 | $\int \tan^5x\sec^2x\,dx$ | | |
| 4 | $\int \dfrac{x^2}{(x^3+1)^5}\,dx$ | | |
| 5 | $\int \cos x\, e^{\sin x}\,dx$ | | |
| 6 | $\int \dfrac{1}{x(\ln x)^3}\,dx$ | | |
| 7 | $\int \sqrt{\tan x}\sec^2x\,dx$ | | |
| 8 | $\int \dfrac{\arctan x}{1+x^2}\,dx$ | | |

**Question 1a:** After completing the table, pick THREE of these and fully solve them (indefinite integral).

**Question 1b:** For entries where you struggled to identify $u$, what made the pattern harder to spot? Was it a "hidden" derivative relationship, or a less common function combination?

---

## Part 2 — Verifying Substitution Numerically (25 min)

### Exercise 2.1

Consider $\displaystyle\int_0^2 x(x^2+1)^2\,dx$ (Problem Set B1).

**Question 2a:** Solve this using substitution (limit-conversion method).

**Question 2b:** Verify numerically using a midpoint Riemann sum with $n=1000$ subintervals (you may estimate mentally using the formula, or use Python/a calculator if available):

$$M_{1000} = \Delta x \sum_{i=1}^{1000} f(\bar x_i), \quad f(x) = x(x^2+1)^2$$

Do the exact (substitution-based) and numerical (Riemann sum) answers agree to at least 3 decimal places?

### Exercise 2.2 — Graphical Verification

**Question 2c:** In Desmos, graph $f(x) = x(x^2+1)^2$ on $[0,2]$ and shade the region under the curve (Desmos supports this via an inequality or the built-in integral tool `\int_0^2 x(x^2+1)^2 dx`).

**Question 2d:** Does Desmos's computed value match your hand computation from Question 2a?

---

## Part 3 — Symmetry Visualization (25 min)

### Exercise 3.1 — Seeing Odd Symmetry Cancel

In Desmos, graph $f(x) = x^3 - 4x$ on $[-3,3]$.

**Question 3a:** Is this function even, odd, or neither? Verify algebraically.

**Question 3b:** Using Desmos's shading/area tools, visually confirm that the signed area from $-3$ to $0$ is the exact negative of the signed area from $0$ to $3$. Take a screenshot showing both shaded regions.

**Question 3c:** What is $\displaystyle\int_{-3}^3(x^3-4x)\,dx$? State the answer immediately using symmetry, then confirm with Desmos's integral tool.

### Exercise 3.2 — Seeing Even Symmetry Double

Graph $g(x) = x^4 - 5x^2 + 4$ on $[-2.5, 2.5]$.

**Question 3d:** Confirm this is even. Using Desmos, compute $\displaystyle\int_0^{2.5}g(x)\,dx$ and $\displaystyle\int_{-2.5}^{2.5}g(x)\,dx$ — verify the second is exactly double the first.

**Question 3e:** Find all $x$-intercepts of $g(x)$ (factor if possible: this is a quadratic in $x^2$). Does the symmetry of the ROOTS match the symmetry of the function?

---

## Part 4 — The Tabular Method for Repeated Integration by Parts (30 min)

When integration by parts must be applied multiple times (as in $\int x^3e^x\,dx$ or $\int x^2\cos x\,dx$), the **tabular method** organizes the work far more efficiently than repeated formula application.

### The Method

To integrate $\displaystyle\int P(x)\cdot f(x)\,dx$ where $P(x)$ is a polynomial (eventually reaches zero after repeated differentiation) and $f(x)$ is easy to integrate repeatedly:

1. Make a two-column table. Left column: $P(x)$ and its successive derivatives (down to 0). Right column: $f(x)$ and its successive antiderivatives (same number of rows).
2. Alternate signs starting with $+$: $+,-,+,-,\ldots$
3. Multiply diagonally (each left entry times the NEXT row's right entry), applying the alternating signs, and sum all products.

### Worked Example — Tabular Method for $\int x^3e^x\,dx$

| Sign | $P(x)$ and derivatives | $f(x)$ and antiderivatives |
|------|--------------------------|------------------------------|
| $+$ | $x^3$ | $e^x$ |
| $-$ | $3x^2$ | $e^x$ |
| $+$ | $6x$ | $e^x$ |
| $-$ | $6$ | $e^x$ |
| $+$ | $0$ | $e^x$ |

Multiply diagonally (each row's LEFT entry times the NEXT row's RIGHT entry), with alternating signs:

$$\int x^3e^x\,dx = +x^3e^x - 3x^2e^x+6xe^x-6e^x+C$$

$$= e^x(x^3-3x^2+6x-6)+C$$

**Question 4a:** Verify this by differentiating the answer and confirming you recover $x^3e^x$.

**Question 4b:** Use the tabular method to evaluate $\displaystyle\int x^2\cos x\,dx$. Build the full table (note: derivatives of $\cos x$ cycle through $\cos x\to-\sin x\to-\cos x\to\sin x\to\cos x\ldots$, but you only need to go until the polynomial column reaches 0).

**Question 4c:** Use the tabular method to redo $\displaystyle\int x^2e^{-x}\,dx$ from the problem set. Confirm your tabular-method answer matches your by-hand-formula answer from Problem Set Part E2.

**Question 4d:** Why does the tabular method work? *(Hint: each row of the table represents one application of integration by parts; the alternating signs come from the "$-\int v\,du$" term flipping sign each time. Try to explicitly connect one or two rows of the table to the formula $\int u\,dv=uv-\int v\,du$.)*

---

## Part 5 — Numerical Sanity Check for the "Solve for I" Technique (15 min)

### Exercise 5.1

Recall the result from Wednesday's lecture: $\displaystyle\int e^x\sin x\,dx = \dfrac{e^x(\sin x-\cos x)}{2}+C$.

**Question 5a:** Differentiate the right-hand side and confirm it equals $e^x\sin x$ (this checks the algebra of the "solve for $I$" derivation independent of any numerical evaluation).

**Question 5b:** Now evaluate the definite integral $\displaystyle\int_0^{\pi} e^x\sin x\,dx$ using the antiderivative formula.

**Question 5c:** Estimate the same definite integral using a midpoint Riemann sum with $n=8$ subintervals (by hand or with a calculator). Does it approximately match your exact answer from 5b?

---

## Lab Report Requirements

Include:
1. Completed pattern-recognition table from Part 1, plus 3 fully worked solutions
2. Numerical and graphical verification from Part 2, with Desmos screenshots
3. Symmetry visualizations from Part 3, with Desmos screenshots and written justification
4. All tabular method computations from Part 4
5. The verification and numerical check from Part 5
6. **Reflection** (6–8 sentences): Compare the mental process of solving an integral via substitution vs. via integration by parts. How do you now decide, when first looking at an unfamiliar integral, which technique (or combination) to try first? What visual or structural cues do you look for?

**Grading:**

| Section | Points |
|---------|--------|
| Part 1 — Pattern recognition | 20 |
| Part 2 — Substitution verification | 20 |
| Part 3 — Symmetry visualization | 20 |
| Part 4 — Tabular method | 25 |
| Part 5 — Solve-for-I check | 10 |
| Reflection | 5 |
| **Total** | **100** |
