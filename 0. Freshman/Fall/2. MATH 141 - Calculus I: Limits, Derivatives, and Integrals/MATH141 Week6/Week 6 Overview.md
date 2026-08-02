# MATH 141 — Calculus I
## Week 6 Overview and Instructor Notes

**Topic:** Extrema · Rolle's Theorem · The Mean Value Theorem · L'Hôpital's Rule
**Lectures:** Monday / Tuesday / Wednesday
**Lab:** Friday
**Quiz:** Monday (covers Week 5 — implicit differentiation, logs, inverse trig, related rates)
**Problem Set 6:** Released Wednesday, due following Wednesday

---

## Learning Objectives

By the end of Week 6, students will be able to:

1. Distinguish absolute vs local extrema precisely using formal definitions
2. State and apply the Extreme Value Theorem, understanding why each hypothesis is necessary
3. Find critical numbers and apply the Closed Interval Method
4. State and prove Rolle's Theorem from the EVT and Fermat's Theorem
5. State and prove the Mean Value Theorem from Rolle's Theorem
6. Apply the MVT corollaries — especially the I/D Test and the "+C" foundation for integration
7. Use the First Derivative Test and Second Derivative Test to classify critical points
8. Determine intervals of concavity and locate inflection points
9. Perform a complete qualitative analysis of a function's graph from its derivatives

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

**Friday (Lab):** Part 3 (three graphs side by side) is the conceptual core of the entire week — the ability to move fluently between $f$, $f'$, $f''$ is the single most transferable skill from this unit. Give this part the most time. Part 2's physical MVT example (ball height/velocity) tends to land well.

**Wednesday (Shape of a Graph):** This lecture synthesizes everything. The full curve analysis examples should be done completely on the board — don't skip steps. Emphasize the procedure as a repeatable checklist (given in the resource sheet). The CS connection to convexity in ML optimization is a good closer for students with that background.

---

## Common Student Errors — Week 6

1. **Confusing local and absolute extrema**, especially at endpoints of a closed interval (endpoints can be absolute extrema without being "local" in the strict open-interval-neighborhood sense — some texts include endpoints in local extrema definitions; be consistent with Stewart's convention).

2. **Assuming $f'(c)=0$ automatically means an extremum.** This is the single most common error of the week. Constant refrain: always verify via First or Second Derivative Test.

3. **Forgetting to check both hypotheses of Rolle's/MVT** before applying them — especially differentiability (not just continuity). The $x^{2/3}$ example is a good one to drill on this.

4. **Second Derivative Test misapplication when $f''(c)=0$.** Students often report "no conclusion" as if the point is definitely not an extremum, rather than correctly falling back to the First Derivative Test.

5. **Inflection point without verifying sign change.** Just finding $f''(c)=0$ is not sufficient — must confirm concavity actually changes sign around $c$ (see Example: $f(x)=x^4$ has $f''(0)=0$ but no inflection point there, since $f''(x)=12x^2\geq0$ never goes negative).
