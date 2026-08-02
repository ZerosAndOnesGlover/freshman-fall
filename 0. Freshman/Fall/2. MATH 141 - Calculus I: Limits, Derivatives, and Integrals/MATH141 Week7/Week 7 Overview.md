# MATH 141 — Calculus I
## Week 7 Overview and Instructor Notes

**Topic:** Shape of a Graph · Curve Sketching Synthesis · Applied Optimization
**Lectures:** Monday / Tuesday / Wednesday
**Lab:** Friday
**Quiz:** Monday (covers Week 6 — extrema, Rolle's Theorem, the MVT, L'Hôpital's Rule)
**Problem Set 7:** Released Wednesday, due following Wednesday

---

## Learning Objectives

By the end of Week 7, students will be able to:

1. Recognize $0/0$ and $\infty/\infty$ indeterminate forms and apply L'Hôpital's Rule correctly
2. Convert $0\cdot\infty$, $\infty-\infty$, $0^0$, $1^\infty$, $\infty^0$ forms into L'Hôpital-applicable forms
3. Reapply L'Hôpital's Rule when necessary and recognize when it fails to terminate
4. Perform a complete 8-step curve sketching analysis on rational, exponential, and logarithmic functions
5. Identify and compute slant (oblique) asymptotes via polynomial division
6. Set up and solve applied optimization problems using the full 8-step strategy
7. Correctly reduce two-variable constrained problems to single-variable optimization
8. Verify optimality using appropriate tests, not just critical point identification

---

## File Index

```
MATH141 Week7/
├── Week 7 Overview.md
├── lectures/
│   ├── Lecture 01 Shape of Graph.md
│   ├── Lecture 02 Curve Sketching.md
│   └── Lecture 03 Applied Optimization.md
├── assignments/
│   └── Problem Set 7.md
├── lab/
│   └── LAB 07 LHopital Curve Sketching Optimization.md
├── quiz/
│   └── QUIZ 07 With Answer Key.md
├── resources/
│   └── Week 7 Reference Sheet.md
└── solutions_instructor/
    ├── LAB 07 Solutions.md
    └── PS 7 Solutions Instructor Only.md
```

---

## Pacing Notes

**Monday (L'Hôpital's Rule):** After Quiz 07, open by revisiting the unsolved $0/0$ limits from Week 1 to motivate the need for a new tool. The Cauchy MVT proof sketch connects directly back to last week — spend a few minutes making this link explicit, since it demonstrates the payoff of the "abstract" MVT machinery. Budget significant time for the indeterminate form conversions (Section 6) — these are where most computational errors occur. The growth rate hierarchy (Section 8) is an excellent bridge to CS-background students; consider opening or closing with it.

**Tuesday (Curve Sketching):** This lecture is synthesis, not new theory — pacing can be brisk on individual techniques (all previously covered) but should slow down on the worked examples, since students need to see the *complete* checklist executed fluently, start to finish, more than once. Do at least two of the three worked examples fully on the board. The slant asymptote technique (Section 3) is the one genuinely new piece of content this lecture — don't rush it.

**Friday (Lab):** Part 1 (growth rate hierarchies) reinforces Monday's lecture with visual/numerical evidence — very effective for building intuition about "why" the abstract limit theorems matter. Part 3's numerical optimizer (grid search) is a nice moment to explicitly connect to gradient descent / numerical methods students may see later — call this out explicitly if time allows.

**Wednesday (Applied Optimization):** The most important lecture of the week for many students, since it is the most commonly tested skill in later courses (economics, physics, engineering). Insist on the full 8-step structure every time — sloppy setup is the primary source of errors here, not the calculus itself. The Snell's Law exercise (in the exercise set) is an excellent capstone if time allows — it shows calculus deriving a physical law from a "least time" principle, foreshadowing the calculus of variations.

---

## Common Student Errors — Week 7

1. **Applying L'Hôpital's Rule without checking the indeterminate form.** This is the single most common error. Drill: state the form explicitly ("this is $0/0$") before applying the rule.

2. **Confusing L'Hôpital's Rule with the Quotient Rule.** Students sometimes compute $(f/g)'$ instead of $f'/g'$. These are entirely different operations.

3. **Stopping after one application when the result is still indeterminate.** Reapply until the form is no longer indeterminate (or recognize the rule isn't converging, as in Part B3 of the problem set).

4. **In curve sketching, confusing domain exclusions with vertical asymptotes.** A rational function may have a hole (removable discontinuity, Week 2) rather than a true vertical asymptote at an excluded point — always check whether the numerator also vanishes there.

5. **In optimization, forgetting to verify the critical point is actually the desired extremum.** Finding $f'(x)=0$ is necessary but not sufficient — the Second Derivative Test, First Derivative Test, or Closed Interval Method must be explicitly applied and stated.

6. **In optimization, using the wrong domain.** Physical constraints (lengths must be positive, angles must be in a valid range) often restrict the mathematical domain — forgetting this can lead to nonsensical "optimal" answers (e.g., negative side lengths).
