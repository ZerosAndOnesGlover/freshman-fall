# MATH 141 · Calculus I
## Week 8 Overview and Instructor Notes

**Topic:** Riemann Sums · The Definite Integral · Properties of the Definite Integral
**Lectures:** Monday 16 Nov / Tuesday 17 Nov / Wednesday 18 November 2026, 11:00
**Lab:** Friday 20 November 2026, 15:00–16:50 (Lab 08)
**Quiz:** Monday 16 November 2026, 11:00–11:15 (covers Week 7 — shape of a graph, curve sketching, applied optimization)
**Problem Set 8:** Released Wednesday 18 November 2026, 12:00 · due Wednesday 25 November 2026, 11:00

---

## A Pivotal Week

This week marks the transition from **differential calculus** (Weeks 1–7) to **integral calculus** (Weeks 8–12). Its job is to build the definite integral honestly — as a limit of Riemann sums — and to establish its properties, including the Mean Value Theorem for Integrals.

That MVT for Integrals is the single piece of machinery Week 9 needs to prove the Fundamental Theorem. Everything here is groundwork: the payoff lands next week, and students should be told so, because the definition-and-properties work of this week is otherwise easy to mistake for bookkeeping.

---

## Learning Objectives

By the end of Week 8, students will be able to:

1. Use sigma notation and summation formulas to compute finite sums exactly
2. Construct left, right, and midpoint Riemann sums for a given function and partition
3. Compute exact areas as limits of Riemann sums for simple polynomial functions
4. State the formal definition of the definite integral as a limit of Riemann sums
5. Apply the algebraic and comparison properties of definite integrals
6. Compute the average value of a function and apply the Mean Value Theorem for Integrals
7. Explain why the definite integral is well defined — why the limit does not depend on the sample points
8. Use the comparison property to bound an integral without evaluating it
9. Explain what the definite integral of a sign-changing function measures, and why it is not the geometric area

---

## File Index

```
MATH141 Week8/
├── Week 8 Overview.md
├── lectures/
│   ├── Lecture 01 Riemann Sums.md
│   ├── Lecture 02 Definite Integral.md
│   └── Lecture 03 Properties of the Definite Integral.md
├── assignments/
│   └── Problem Set 8.md
├── lab/
│   └── LAB 08 Riemann Sums and Convergence.md
├── quiz/
│   └── QUIZ 08 With Answer Key.md
├── resources/
│   └── Week 8 Reference Sheet.md
└── solutions_instructor/
    ├── LAB 08 Solutions.md
    └── PS 8 Solutions Instructor Only.md
```

---

## Pacing Notes

**Monday (Riemann Sums):** After Quiz 08, spend real time motivating WHY we need a new tool — the area problem cannot be solved by elementary geometry for curved regions. The exact computation of $\int_0^1 x^2\,dx = 1/3$ via the Riemann sum limit (Section 6) is the centerpiece of this lecture and should be done slowly and completely on the board — it is many students' first fully rigorous "from scratch" computation of an exact area, and it should feel like a genuine achievement. The distance problem (Section 8) is a good structural parallel to draw out explicitly, since it foreshadows the FTC connection between velocity and position.

**Tuesday (Definite Integral):** This lecture is more about consolidating definitions and properties than deriving new results — pace can be brisk on the properties (Section 3) since they follow intuitively from sums, but slow down for the Mean Value Theorem for Integrals, since its parallel structure to the ordinary MVT (Week 6) is worth drawing out explicitly, and since it is the engine of next week's FTC proof. The average-value-as-expected-value connection (CS section) is valuable for students with probability/statistics background.

**Friday (Lab):** Part 1's convergence-rate comparison (left/right/midpoint) directly parallels Lab 3's forward/central-difference comparison — make this connection explicit if students don't draw it themselves; both are $O(h)$ versus $O(h^2)$ for the same reason. **Part 2 is the conceptual core**: watching four sampling rules — including a random one — converge to the same number is the only convincing way to show that sample-point independence is a real claim and not a technicality in the definition. Give it the full 25 minutes. Part 4's $e^{-x^2}$ is a deliberate teaser for Week 9: it has no elementary antiderivative, so no amount of technique will ever evaluate it exactly.

**Wednesday (Properties of the Definite Integral):** Linearity and additivity go quickly — students accept them from the sum definition. Spend the time instead on the two properties that carry weight next week: the **comparison property** (which lets you bound an integral you cannot evaluate) and the **Mean Value Theorem for Integrals**. Close by stating, without proof, what Week 9 will establish: that this whole apparatus collapses into "antidifferentiate and subtract." Ending the week on that promise is what makes Monday's FTC lecture land.

---

## Common Student Errors — Week 8

1. **Treating the definite integral as geometric area unconditionally.** $\int_a^b f$ is *signed* area: regions below the axis subtract. The diagnostic is $\int_{-1}^{1}x\,dx = 0$ while the region plainly has area 1. This is Problem D2 on the problem set — assign it.

2. **Off-by-one in the sample points.** $R_n$ sums $i=1..n$; $L_n$ sums $i=0..n-1$. This is the commonest arithmetic error in Part A and it is worth writing both index ranges on the board side by side.

3. **Reading $\int_b^a f = -\int_a^b f$ as a theorem.** It is a definition — Riemann sums are constructed assuming $a<b$. Students who think it was proved cannot say why any other convention was unavailable. Problem D3 targets this directly.

4. **Applying the comparison property without establishing the extremes.** Evaluating the integrand at the two endpoints is not the same as finding its maximum and minimum on the interval. It happens to work in B3 because the integrand is monotone there — which is exactly what the student must argue.

5. **Reaching for an antiderivative.** Some students will have seen the FTC elsewhere and will evaluate C1 in one line. Say explicitly when assigning the set that Part C must be done from the definition and that antiderivative solutions score zero. The point of the week is to earn the shortcut, not to use it.

---

*MATH 141 · Week 8 · Overview · © CSE Department*
