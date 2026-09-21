# MATH 141 · Calculus I
## Week 1 Overview and Instructor Notes

**Topic:** Limits — Intuition, the ε-δ Definition, Infinite Limits and Limits at Infinity
**Lectures:** Monday 28 Sep / Tuesday 29 Sep / Wednesday 30 September 2026, 11:00  
**Lab:** Friday 2 October 2026, 15:00–16:50 (Lab 01)  
**Quiz:** Monday 28 September 2026, 11:00–11:15 (covers Week 0 — functions, algebra, trigonometry, exponentials/logarithms)
**Problem Set 1:** Released Wednesday 30 September 2026, 12:00 · due Wednesday 7 October 2026, 11:00

---

## Learning Objectives

By the end of Week 1, students will be able to:

1. Evaluate limits algebraically using factoring, rationalization, and the limit laws
2. Evaluate one-sided limits for piecewise functions
3. Apply the Squeeze Theorem to limits involving oscillating factors
4. Use the two special trigonometric limits to evaluate related expressions
5. Write a complete ε-δ proof for linear and simple quadratic limits
6. Apply the three-part definition of continuity and classify discontinuities
7. State and apply the Intermediate Value Theorem
8. Use bisection to locate roots numerically

---

## Week 1 File Index

```
MATH141 Week1/
├── Week 1 Overview.md
├── lectures/
│   ├── Lecture 01 Limits Intuition.md
│   ├── Lecture 02 Epsilon Delta.md
│   └── Lecture 03 Infinite Limits and Limits at Infinity.md
├── assignments/
│   └── Problem Set 1.md
├── lab/
│   └── LAB 01 Limits Numerical Graphical.md
├── quiz/
│   └── QUIZ 01 With Answer Key.md
├── resources/
│   └── Week 1 Reference Sheet.md
└── solutions_instructor/
    ├── LAB 01 Solutions.md
    └── PS 1 Solutions Instructor Only.md
```

---

## Pacing and Emphasis Notes

**Monday (Lecture 1):** After Quiz 01, spend ~10 min on key corrections before starting limits. The intuitive limit concept should feel natural by end of class. Emphasize: limits don't care about the value at the point. The $\sin(1/x)$ example is important — introduce it verbally, don't rush it.

**Tuesday (Lecture 2):** The ε-δ definition is the hardest single concept of the week. Do not skip the game-theoretic interpretation — it is the best pedagogical entry point. Work Example 1 (linear) and Example 2 (quadratic) in full on the board; students should copy every line. Assign the exercises as part of in-class discussion time if available.

**Friday (Lab 01):** Parts 1 and 2 are the most important. The catastrophic cancellation exercise (1.2) should prompt genuine surprise — this is often the first time students see that their calculator can lie. Part 4 (bisection) connects directly to CS students' background.

**Wednesday (Lecture 3):** Continuity should feel natural after limits. Spend the most time on IVT — its proof (requiring completeness of ℝ) is profound. The fixed-point corollary is worth a few minutes for CS students (fixed-point iteration is foundational in numerical computing and functional programming).

---

## Common Student Errors: Week 1

1. **Forgetting the $0 < |x-a|$ condition in ε-δ:** Students write $|x-a|<\delta$ without the strict inequality $0<$. Stress: the limit is about *approaching*, never *reaching*.

2. **Confusing limit DNE with limit = undefined:** $\lim_{x\to 0}(1/x)$ is "DNE (infinite)" not "undefined." These are precise different statements.

3. **Applying direct substitution to indeterminate forms:** A significant fraction of students will write $\lim_{x\to 1}\frac{x^2-1}{x-1} = \frac{0}{0}$ and conclude the limit doesn't exist. Correct this immediately.

4. **IVT applied without checking continuity:** Students often forget to verify the function is continuous on $[a,b]$ before applying IVT. Build the habit of stating hypotheses first.

5. **Mixing up ε and δ roles:** In ε-δ proofs, students sometimes write "choose ε = ..." — ε is given by the skeptic, δ is chosen by the prover.
