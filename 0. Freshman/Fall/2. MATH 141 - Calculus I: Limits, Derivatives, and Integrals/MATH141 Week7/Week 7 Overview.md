# MATH 141 · Calculus I
## Week 7 Overview and Instructor Notes

**Topic:** Shape of a Graph · Curve Sketching Synthesis · Applied Optimization
**Lectures:** Monday 9 Nov / Tuesday 10 Nov / Wednesday 11 November 2026, 11:00
**Lab:** Friday 13 November 2026, 15:00–16:50 (Lab 07)
**Quiz:** Monday 9 November 2026, 11:00–11:15 (covers Week 6 — extrema, Rolle's Theorem, the MVT, L'Hôpital's Rule)
**Problem Set 7:** Released Wednesday 11 November 2026, 12:00 · due Wednesday 18 November 2026, 11:00

---

## Learning Objectives

By the end of Week 7, students will be able to:

1. Use the Increasing/Decreasing Test and the First Derivative Test to classify critical numbers
2. Determine concavity and inflection points, and apply the Second Derivative Test (knowing when it is inconclusive)
3. Use L'Hôpital's Rule (Week 6) to find the asymptotic behaviour needed in curve sketching
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

**Monday (Shape of a Graph):** After Quiz 07, build directly on Week 6's MVT Corollary 3 — the Increasing/Decreasing Test is already proved. Spend the new time on concavity and the Second Derivative Test, and show $x^4$, $-x^4$, $x^3$ side by side so students see why $f''(c)=0$ is inconclusive.

**Tuesday (Curve Sketching):** This lecture is synthesis, not new theory — pacing can be brisk on individual techniques (all previously covered) but should slow down on the worked examples, since students need to see the *complete* checklist executed fluently, start to finish, more than once. Do at least two of the three worked examples fully on the board. The slant asymptote technique (Section 3) is the one genuinely new piece of content this lecture — don't rush it.

**Friday (Lab):** Part 1 (growth rate hierarchies) revisits Week 6's L'Hôpital lecture with visual/numerical evidence — very effective for building intuition about "why" the abstract limit theorems matter. Part 3's numerical optimizer (grid search) is a nice moment to explicitly connect to gradient descent / numerical methods students may see later — call this out explicitly if time allows.

**Wednesday (Applied Optimization):** The most important lecture of the week for many students, since it is the most commonly tested skill in later courses (economics, physics, engineering). Insist on the full 8-step structure every time — sloppy setup is the primary source of errors here, not the calculus itself. The Snell's Law exercise (in the exercise set) is an excellent capstone if time allows — it shows calculus deriving a physical law from a "least time" principle, foreshadowing the calculus of variations.

---

## Common Student Errors — Week 7

1. **Reading $f''(c)=0$ as "inflection point".** Concavity must actually change sign at $c$ — $x^4$ has $f''(0)=0$ and no inflection.

2. **Reading an inconclusive Second Derivative Test as "no extremum".** Fall back to the First Derivative Test (Problem Set 7, D1).

3. **Carrying L'Hôpital errors into asymptote work** — applying the rule to a form that is not indeterminate. State the form before each application.

4. **In curve sketching, confusing domain exclusions with vertical asymptotes.** A rational function may have a hole (removable discontinuity, Week 2) rather than a true vertical asymptote at an excluded point — always check whether the numerator also vanishes there.

5. **In optimization, forgetting to verify the critical point is actually the desired extremum.** Finding $f'(x)=0$ is necessary but not sufficient — the Second Derivative Test, First Derivative Test, or Closed Interval Method must be explicitly applied and stated.

6. **In optimization, using the wrong domain.** Physical constraints (lengths must be positive, angles must be in a valid range) often restrict the mathematical domain — forgetting this can lead to nonsensical "optimal" answers (e.g., negative side lengths).
