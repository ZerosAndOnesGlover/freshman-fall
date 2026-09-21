# MATH 141 · Calculus I
## Week 10 Overview and Instructor Notes

**Topic:** Indefinite Integrals and the Net Change Theorem · The Substitution Rule · Definite Substitution and Symmetry · Integration by Parts
**Lectures:** Monday 30 Nov / Tuesday 1 Dec / Wednesday 2 December 2026, 11:00
**Lab:** Friday 4 December 2026, 15:00–16:50 (Lab 10)
**Quiz:** Monday 30 November 2026, 11:00–11:15 (covers Week 9 — the Fundamental Theorem of Calculus)
**Problem Set 10:** Released Wednesday 2 December 2026, 12:00 · due Wednesday 9 December 2026, 11:00

---

## Learning Objectives

By the end of Week 10, students will be able to:

1. Formalize and apply the Net Change Theorem in physical contexts
2. Apply the Substitution Rule to indefinite integrals, recognizing common patterns
3. Apply the Substitution Rule to definite integrals using limit conversion
4. State and prove the symmetry theorems for even and odd functions
5. Use symmetry to evaluate or simplify integrals over symmetric intervals
6. Apply Integration by Parts using the LIATE heuristic to guide factor choice
7. Handle repeated Integration by Parts, including the tabular method
8. Recognize and solve "circular" integrals using the algebraic solve-for-$I$ technique
9. Select the appropriate technique (substitution, parts, symmetry, or combination) for a given integral

---

## File Index

```
MATH141 Week10/
├── Week 10 Overview.md
├── lectures/
│   ├── Lecture 01 Substitution.md
│   ├── Lecture 02 Substitution Definite Symmetry.md
│   └── Lecture 03 Integration by Parts.md
├── assignments/
│   └── Problem Set 10.md
├── lab/
│   └── LAB 10 Substitution Parts Tabular.md
├── quiz/
│   └── QUIZ 10 With Answer Key.md
├── resources/
│   └── Week 10 Reference Sheet.md
└── solutions_instructor/
    ├── LAB 10 Solutions.md
    └── PS 10 Solutions Instructor Only.md
```

---

## Pacing Notes

**Monday (Substitution):** After Quiz 10, open with the Net Change Theorem as a quick, satisfying restatement of FTC Part 2 in physical terms — this should feel like a "free win" before the new material. The core of the lecture is pattern recognition (Section 6) — spend real time here, since this is the skill students will lean on all semester. Do Examples 2–8 at a brisk but complete pace; the "solve for leftover $x$" technique (Example 8) is subtler and deserves emphasis, since it appears again in Week 8's trig substitution.

**Tuesday (Definite Substitution + Symmetry):** Lead with the two-methods comparison (Section 1) and make the case explicitly for why Method 2 (limit conversion) is preferred going forward — this saves real time on every subsequent problem. The symmetry proof (Section 3) is an excellent payoff moment: this is the exact result promised (and left unproved) in Problem Set 6, Problem F3 — call this out explicitly, since seeing a "promise kept" from a prior week reinforces the cumulative structure of the course. Example 6 (the odd-function integral $x^2\sin x$ over $[-\pi,\pi]$) is a great "wow" moment — evaluating a nontrivial-looking integral in one line.

**Friday (Lab):** Part 1's pattern-recognition drill is the highest-value activity of the lab — resist the urge to skip it for time. Part 4 (tabular method) previews the following day's integration-by-parts lecture; give a brief 5–10 minute framing of the by-parts formula at the start of lab so Part 4 lands correctly, since the full lecture treatment doesn't occur until Wednesday.

**Wednesday (Integration by Parts):** The formula derivation (Section 2) is quick, but LIATE deserves real discussion — it's a heuristic, not a theorem, and students benefit from understanding WHY it tends to work (Section 4's intuition) rather than memorizing it as an arbitrary acronym. The "circular" integral technique (Section 7) is one of the most elegant arguments in the course — do Example 6 completely and let students appreciate the algebra.

---

## Common Student Errors — Week 10

1. **Forgetting to convert $dx$ correctly in substitution**, especially when the derivative introduces a constant multiple (e.g., $u=5x$ requires $dx=du/5$, not $dx=du$).

2. **Mixing $x$ and $u$ in the same expression** after starting a substitution — every instance of $x$ must be replaced; leftover $x$'s (unless deliberately solved for, as in the "leftover $x$" technique) indicate an error.

3. **Forgetting to convert limits of integration** when substituting in a definite integral, OR converting limits AND THEN also substituting back to $x$ (double-work, and a common source of sign errors).

4. **Misapplying symmetry** — students sometimes claim a function is even or odd without checking algebraically ($f(-x)$ must be computed and compared to $f(x)$, not just "eyeballed").

5. **Choosing $u$ and $dv$ against LIATE without reason**, leading to a MORE complicated integral after applying the by-parts formula. Encourage students to abandon and retry if the new integral looks harder, rather than persisting.

6. **Giving up on "circular" integrals** rather than recognizing the reappearance of the original integral and solving algebraically — this feels unfamiliar the first time and needs explicit modeling.
