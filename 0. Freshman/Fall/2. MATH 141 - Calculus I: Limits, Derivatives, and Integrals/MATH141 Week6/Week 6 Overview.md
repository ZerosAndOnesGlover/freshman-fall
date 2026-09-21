# MATH 141 · Calculus I
## Week 6 Overview and Instructor Notes

**Topic:** Extrema · Rolle's Theorem · The Mean Value Theorem · L'Hôpital's Rule
**Lectures:** Monday 2 / Tuesday 3 / Wednesday 4 November 2026, 11:00
**Lab:** Friday 6 November 2026, 15:00–16:50 (Lab 06)
**Quiz:** Monday 2 November 2026, 11:00–11:15 (Quiz 06, covers Week 5 — implicit differentiation, logs, inverse trig, related rates)
**Problem Set 6:** Released Wednesday 4 November 2026, 12:00 · due Wednesday 11 November 2026, 11:00

---

## Learning Objectives

By the end of Week 6, students will be able to:

1. Distinguish absolute vs local extrema precisely using formal definitions
2. State and apply the Extreme Value Theorem, understanding why each hypothesis is necessary
3. Find critical numbers and apply the Closed Interval Method
4. State and prove Rolle's Theorem from the EVT and Fermat's Theorem
5. State and prove the Mean Value Theorem from Rolle's Theorem
6. Apply the MVT corollaries — especially the I/D Test and the "+C" foundation for integration
7. Evaluate limits of indeterminate forms with L'Hôpital's Rule, converting $0\cdot\infty$, $\infty-\infty$ and
   $1^\infty$ forms first

*(Concavity, the Second Derivative Test and curve sketching are Week 7.)*

---

## File Index

```
MATH141 Week6/
├── Week 6 Overview.md
├── lectures/
│   ├── Lecture 01 Extrema.md
│   ├── Lecture 02 MVT.md
│   └── Lecture 03 LHopital.md
├── assignments/
│   └── Problem Set 6.md
├── lab/
│   └── LAB 06 Extrema MVT Curve Shape.md
├── quiz/
│   └── QUIZ 06 With Answer Key.md
├── resources/
│   └── Week 6 Reference Sheet.md
└── solutions_instructor/
    ├── LAB 06 Solutions.md
    └── PS 6 Solutions Instructor Only.md
```

---

## Pacing Notes

**Monday (Extrema):** After Quiz 06, spend real time on the precise definitions — local vs absolute is a frequent point of confusion. The three EVT counterexamples (discontinuity, open interval, unboundedness) should each get a quick sketch on the board. Fermat's Theorem proof is short and elegant — do it in full. The $x^3$ counterexample to the converse is essential and should be memorable.

**Tuesday (Rolle's/MVT):** This is a proof-heavy lecture — budget time accordingly. The Rolle's Theorem proof (via EVT + Fermat) should be done carefully since it's a template for the MVT proof. The MVT proof via the auxiliary function $g(x)$ is one of the most elegant arguments in the course — the trick of "tilting" the function to reduce to Rolle's Theorem is a technique students will see again (e.g., Taylor's theorem in Week 12). Corollary 2 deserves emphasis: it is the entire justification for "+C" in indefinite integrals, which students will take on faith otherwise starting Week 9, when FTC Part 2 lets them use *any* antiderivative.

**Friday (Lab):** Part 3 (reading $f$ from $f'$) is the conceptual core — it rehearses MVT Corollary 3 before Week 7 adds $f''$. Part 4 checks Wednesday's L'Hôpital limits numerically. Part 2's physical MVT example (ball height/velocity) tends to land well.

**Wednesday (L'Hôpital's Rule):** Insist that students name the indeterminate form before every application. The $1^\infty$ case (take logs, then exponentiate) is where most marks are lost. Close with the growth-rate hierarchy — it is the CS connection students will use in algorithm analysis.

---

## Common Student Errors — Week 6

1. **Confusing local and absolute extrema**, especially at endpoints of a closed interval (endpoints can be absolute extrema without being "local" in the strict open-interval-neighborhood sense — some texts include endpoints in local extrema definitions; be consistent with Stewart's convention).

2. **Assuming $f'(c)=0$ automatically means an extremum.** This is the single most common error of the week. Constant refrain: always check the sign of $f'$ on each side (Corollary 3).

3. **Forgetting to check both hypotheses of Rolle's/MVT** before applying them — especially differentiability (not just continuity). The $x^{2/3}$ example is a good one to drill on this.

4. **Applying L'Hôpital's Rule to a form that is not indeterminate** — e.g. to $\frac{x+1}{x}$ as $x\to0$. Check the form before each application.

5. **Forgetting to exponentiate in $1^\infty$ problems.** Finding $\ln y\to L$ and reporting $L$ instead of $e^L$.
