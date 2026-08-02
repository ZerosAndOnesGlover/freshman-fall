# MATH 141 — Calculus I
## Week 3 Overview and Instructor Notes

**Topic:** The Derivative — Definition, the Derivative as a Function, and Differentiability
**Lectures:** Monday / Tuesday / Wednesday
**Lab:** Friday
**Quiz:** Monday (covers Week 2 — continuity, types of discontinuity, the IVT)
**Problem Set 3:** Released Wednesday, due following Wednesday

---

## Learning Objectives

By the end of Week 3, students will be able to:

1. Compute derivatives from the limit definition for polynomial, rational, and radical functions
2. Interpret the derivative geometrically (slope of tangent) and physically (instantaneous rate of change)
3. Apply the power, constant multiple, sum, product, and quotient rules fluently
4. Derive and apply derivatives of all six trigonometric functions
5. Apply the chain rule to composite functions including nested compositions
6. Differentiate exponential functions $e^x$ and $a^x$
7. Identify and explain points of non-differentiability (corners, cusps, discontinuities)
8. Compute second and higher-order derivatives
9. Write equations of tangent and normal lines

---

## File Index

```
MATH141 Week3/
├── Week 3 Overview.md
├── lectures/
│   ├── Lecture 01 Derivative Definition.md
│   ├── Lecture 02 The Derivative as a Function.md
│   └── Lecture 03 Differentiability and Continuity.md
├── assignments/
│   └── Problem Set 3.md
├── lab/
│   └── LAB 03 Derivative Exploration.md
├── quiz/
│   └── QUIZ 03 With Answer Key.md
├── resources/
│   └── Week 3 Reference Sheet.md
└── solutions_instructor/
    ├── LAB 03 Solutions.md
    └── PS 3 Solutions Instructor Only.md
```

---

## Pacing Notes

**Monday:** After Quiz 03 corrections (~8 min), spend the full lecture on the definition. Do all four worked examples on the board — especially the square root (rationalizing) and the reciprocal (common denominator). The physical interpretation (velocity/acceleration) lands well with CS students. End with the differentiability failure modes — the corner example visually sets up the non-intuitive fact that continuity ≠ differentiability.

**Tuesday:** Move efficiently. Power rule is fast. Spend the most time on the product rule proof — the algebraic trick of adding and subtracting $f(x+h)g(x)$ is elegant and worth dwelling on. Derive $(\sin x)' = \cos x$ in full — this is the payoff from Week 1's special trig limits. The derivation should feel earned.

**Friday (Lab):** Parts 1 and 2 (secant convergence and reading the derivative from a graph) are the conceptual core. Part 4 (numerical differentiation) is the CS bridge — catastrophic cancellation recurs from Lab 1; the forward-vs-central difference order-of-accuracy result is directly applicable to numerical methods courses. Part 5 (the number $e$) numerically motivates what is otherwise a mysterious definition.

**Wednesday:** The chain rule is the most important lecture of the week. Spend the first 10 minutes on the proof sketch and the Leibniz notation intuition ($dy/du \cdot du/dx$). Then work nested compositions carefully. Emphasize: the chain rule is backpropagation — this is not a metaphor, it is literally the same computation.

---

## Common Student Errors — Week 3

1. **Forgetting the chain rule** on composite functions. The most common error all semester. Whenever the argument of a function is not bare $x$, the chain rule is required. Drill this.

2. **Product rule sign errors.** $(fg)' = f'g + fg'$, not $f'g'$. Have students say it out loud: "first times derivative of second, plus second times derivative of first."

3. **Quotient rule subtraction order.** It is $f'g - fg'$, not $fg' - f'g$. The numerator is NOT symmetric. Mnemonic: "Lo d-Hi minus Hi d-Lo."

4. **Treating $dy/dx$ as a fraction** before the chain rule is established. It is a limit, not a ratio. The chain rule gives it fraction-like behavior, but only because of how limits work.

5. **Computing $f'(a)$ instead of $f'(x)$.** In the definition, students sometimes fix a number throughout and get a constant. Make clear: when we want the derivative *function*, $a$ (or $x$) remains a variable.
