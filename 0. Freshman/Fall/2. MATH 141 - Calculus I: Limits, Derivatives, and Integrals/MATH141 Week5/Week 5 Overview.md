# MATH 141 · Calculus I
## Week 5 Overview and Instructor Notes

**Topic:** Implicit Differentiation · Logarithmic Derivatives · Inverse Trig · Related Rates
**Lectures:** Monday / Tuesday / Wednesday
**Lab:** Friday
**Quiz:** Monday (covers Week 4 — differentiation rules, the chain rule, higher derivatives and rates)
**Problem Set 5:** Released Wednesday, due following Wednesday

---

## Learning Objectives

By the end of Week 5, students will be able to:

1. Differentiate implicitly defined curves using the chain rule
2. Find equations of tangent lines to implicit curves
3. Compute second derivatives implicitly
4. Differentiate $\ln x$, $\ln|x|$, $\ln(g(x))$, and $\log_a x$
5. Apply logarithmic differentiation to functions of the form $[f(x)]^{g(x)}$
6. Derive and apply all six inverse trig derivatives
7. Identify and set up related rates problems from geometric descriptions
8. Differentiate both sides of a geometric equation with respect to time
9. Correctly use similar triangles and other geometric constraints to reduce variable count

---

## File Index

```
MATH141 Week5/
├── Week 5 Overview.md
├── lectures/
│   ├── Lecture 01 Implicit Differentiation.md
│   ├── Lecture 02 Log Differentiation Inverse Trig.md
│   └── Lecture 03 Related Rates.md
├── assignments/
│   └── Problem Set 5.md
├── lab/
│   └── LAB 05 Implicit Logarithms Related Rates.md
├── quiz/
│   └── QUIZ 05 With Answer Key.md
├── resources/
│   └── Week 5 Reference Sheet.md
└── solutions_instructor/
    ├── LAB 05 Solutions.md
    └── PS 5 Solutions Instructor Only.md
```

---

## Pacing Notes

**Monday (Implicit Differentiation):** After Quiz 05, open with the circle $x^2+y^2=25$ — it's instantly intuitive. Then the Folium of Descartes to show a more complex curve. Do Example 3 ($\sin(xy) = y^2 - x$) slowly — product rule inside implicit differentiation confuses students. End with the implicit second derivative (Example 4) to show the method extends. Preview: inverse trig derivatives are derived by this exact method.

**Tuesday (Logs + Inverse Trig):** Derive $(\ln x)' = 1/x$ cleanly via implicit differentiation — it takes 3 lines and students should see it come from first principles, not be handed as a formula. Logarithmic differentiation on $x^x$ is the payoff — it visually shows why the power rule fails when the exponent is variable. For inverse trig: derive $\arcsin$ and $\arctan$ in class; assign $\arccos$, $\text{arcsec}$ as exercises. The paired identities ($\arcsin + \arccos = \pi/2$, etc.) connect everything.

**Wednesday (Related Rates):** This is where many students hit their first wall. The hardest part is setup, not calculus. Enforce the diagram requirement — students who skip it almost always set up the wrong equation. Work the conical tank (Example 3) especially carefully: the similar-triangles step to eliminate one variable is the key technique. Spend the last 10 minutes on a student-solved example (have them set it up while you circulate).

---

## Common Student Errors — Week 5

1. **Not applying chain rule on $y$ terms.** Writing $d/dx[y^2] = 2y$ instead of $2y\cdot y'$. This is the most common error in implicit differentiation. Drill: every $y$-term gets a $\cdot y'$ factor.

2. **Substituting numerical values before differentiating in related rates.** Non-negotiable: values only go in after $dy/dt$ or $dr/dt$ terms are visible in the equation.

3. **Forgetting the chain rule on $\ln(g(x))$.** Writing $(\ln(x^2+1))' = 1/(x^2+1)$ instead of $2x/(x^2+1)$. Emphasize: the chain rule applies to logarithms just as it does to everything else.

4. **Wrong sign on $\arccos$ derivative.** Students often remember $1/\sqrt{1-x^2}$ but forget the negative sign for $\arccos$.

5. **Not reducing to one variable before differentiating in related rates.** Setting up $dV/dt$ with both $r$ and $h$ for a cone without using similar triangles first to eliminate $r$ in terms of $h$.
