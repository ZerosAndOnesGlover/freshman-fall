# MATH 141 · Week 1
## LAB 01 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed, not estimated.** Students working in Desmos rather
> than Python will see the same behaviour but fewer digits — grade the *reasoning and the observed
> trend*, not agreement to the last decimal place.

---

> Lab sat Friday 2 October 2026. Revised 2026-09-21: Parts 2 (discontinuities) and 4 (bisection) removed —
> both need Week 2. Part numbers are kept so they match the handout.

## Part 1 — When Numerical Tables Lie

**1.1 A deceptive table.** The standard construction evaluates a function at points where it looks
convergent while the true limit differs — e.g. sin(π/x) sampled at x = 1, 1/2, 1/3, … gives 0 every
time, suggesting a limit of 0, when in fact the limit as x → 0 **does not exist** (the function
oscillates through every value in [−1,1] infinitely often).

**The lesson: a table samples countably many points; a limit is a statement about all of them.** No
finite table can *prove* a limit. It can only suggest one, or refute one.

**1.2 Round-off error — the important exercise.**

f(x) = (√(x+1) − 1)/x, whose exact limit as x → 0 is **0.5**:

| x | computed f(x) |
|---|---|
| 10⁻¹ | 0.488088481701516 |
| 10⁻⁴ | 0.499987500623966 |
| 10⁻⁸ | 0.499999996961265 |
| 10⁻¹² | 0.500044450291171 |
| 10⁻¹⁴ | 0.488498130835069 |
| 10⁻¹⁵ | 0.444089209850063 |
| 10⁻¹⁶ | **0.000000000000000** |

The values improve to about x = 10⁻⁸ and then **get worse**, collapsing to exactly 0.

**Why: catastrophic cancellation.** For tiny x, √(x+1) and 1 agree to nearly all 16 significant
digits a `double` carries. Subtracting them annihilates the leading digits and leaves only
round-off noise, which is then divided by a tiny x — amplifying the error enormously. At x = 10⁻¹⁶,
√(x+1) rounds to exactly 1.0 and the numerator is 0.

**The fix is algebraic, not numerical.** Multiply by the conjugate:

$$\frac{\sqrt{x+1}-1}{x} = \frac{x}{x\left(\sqrt{x+1}+1\right)} = \frac{1}{\sqrt{x+1}+1}$$

which involves no subtraction of nearly equal quantities. Verified:

| x | stable form |
|---|---|
| 10⁻¹² | 0.499999999999875 |
| 10⁻¹⁵ | 0.500000000000000 |
| 10⁻¹⁶ | 0.500000000000000 |

**This is the single most important idea in the lab**, and it connects directly to CS: the same
algebra that finds the limit by hand also makes the computation numerically stable. Students who
conclude "computers are unreliable" have missed it — the computer is reliable, the *expression*
was ill-conditioned.

---

## Part 3 — The Special Trigonometric Limits

| x | sin(x)/x | (1 − cos x)/x² |
|---|---|---|
| 1 | 0.841470984808 | 0.459697694132 |
| 0.1 | 0.998334166468 | 0.499583472197 |
| 0.01 | 0.999983333417 | 0.499995833347 |
| 0.001 | 0.999999833333 | 0.499999958326 |
| 10⁻⁵ | 0.999999999983 | 0.500000041370 |

**Limits: 1 and 1/2.**

Note the second column at x = 10⁻⁵ reads 0.500000041 — *worse* than at x = 10⁻³. Same cancellation
problem as Part 1: 1 − cos x subtracts nearly equal quantities. The stable form uses the identity
1 − cos x = 2sin²(x/2).

> **The degrees trap.** In degree mode, sin(1°)/1 = **0.01745**, not 1 — because sin(1°) = sin(π/180
> radians). Every calculus result for trigonometric functions assumes **radians**, and a student
> whose whole table reads ≈0.01745 has their calculator in the wrong mode. Check this first when a
> table looks systematically wrong.

**3.2 Geometric verification.** The squeeze cos x ≤ sin(x)/x ≤ 1 on (0, π/2) comes from comparing
the areas of the inner triangle, the sector, and the outer triangle. Both bounds → 1, so the middle
does too.

---

## Part 5 — ε–δ Intuition

The deliverable is that students find a **δ that works for a given ε**, and understand the order of
quantifiers: for **every** ε > 0 there **exists** δ > 0. A student who picks ε in terms of δ has the
logic backwards and earns no method marks however tidy the algebra.

For a linear function the relationship is exact: |f(x) − L| < ε with f(x) = mx + c requires
δ = ε/|m|. Starting there before attempting quadratics is the right scaffolding.

---

## Marking Scheme

- **Method (≈60%).** Correct technique named, hypotheses checked where a theorem requires them,
  symbolic setup before numerical evaluation, and a stated reason for each observed behaviour.
- **Execution (≈40%).** Correct arithmetic, sensible precision, correct plot or table, and a
  conclusion that actually follows from the data.

**Carry-through.** Penalise a wrong value once; award downstream marks if the student reasons
correctly from their own error.

**The specific failure to watch for in a computational lab:** reporting *what* the computer printed
without explaining *why*. "The table approaches 0.5" is an observation; "the table approaches 0.5
because the conjugate cancels the removable factor" is the answer. A lab report that is a
transcript earns the execution marks only.

---

*MATH 141 · Week 1 · Lab Solutions · Instructor Copy · © CSE Department*
