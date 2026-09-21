# MATH 141 · Calculus I
## Week 3 Overview and Instructor Notes

**Topic:** The Derivative — Definition, the Derivative as a Function, and Differentiability
**Lectures:** Monday 12 Oct / Tuesday 13 Oct / Wednesday 14 October 2026, 11:00
**Lab:** Friday 16 October 2026, 15:00–16:50 (Lab 03)
**Quiz:** Monday 12 October 2026, 11:00–11:15 (covers Week 2 — continuity, types of discontinuity, the IVT)
**Problem Set 3:** Released Wednesday 14 October 2026, 12:00 · due Wednesday 21 October 2026, 11:00

---

## Learning Objectives

By the end of Week 3, students will be able to:

1. Compute derivatives from the limit definition for polynomial, rational, and radical functions
2. Interpret the derivative geometrically (slope of tangent) and physically (instantaneous rate of change)
3. Treat the derivative as a function, and estimate it numerically with forward and central differences
4. Write the equation of a tangent line
5. Identify and explain points of non-differentiability (corners, cusps, discontinuities)
6. Prove that differentiability implies continuity, and show the converse fails

The differentiation rules, the chain rule and higher derivatives are **Week 4**. *(Objectives corrected
2026-09-21 to match the three lectures actually given this week.)*

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

**Monday 12 Oct (Lecture 01):** After Quiz 03 (~15 min), the definition. Do the worked examples on the board — especially
the square root (rationalizing) and the reciprocal (common denominator). Velocity lands well with CS students.

**Tuesday 13 Oct (Lecture 02):** The derivative as a function: build $f'$ point by point, read it from a graph, and
estimate it numerically. Forward vs central differences is the CS bridge.

**Wednesday 14 Oct (Lecture 03):** Differentiability and continuity: corners, cusps, vertical tangents, and the proof
that differentiable ⇒ continuous. Problem Set 3 is released after this lecture.

**Friday 16 Oct (Lab):** Secant convergence and reading the derivative from a graph are the conceptual core; the numerical
part repeats Lecture 02's forward-vs-central result by measurement. Everything is from the definition.

---

## Common Student Errors — Week 3

1. **Computing $f'(a)$ instead of $f'(x)$.** Students fix a number throughout the definition and get a constant.
   When the derivative *function* is wanted, $x$ stays a variable.

2. **Cancelling $h$ too early.** $\frac{f(x+h)-f(x)}{h}$ must be simplified until the factor $h$ cancels; setting $h = 0$
   before that gives $0/0$.

3. **"Continuous, so differentiable."** $|x|$ is the counterexample to keep in mind.

