# MATH 141 Week 1
## LAB 01 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed, not estimated.** Students working in Desmos rather
> than Python will see the same behaviour but fewer digits — grade the *reasoning and the observed
> trend*, not agreement to the last decimal place.

---

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

## Part 2 — Discontinuities

| Type | Example | Behaviour |
|---|---|---|
| **Removable** | (x²−1)/(x−1) at x=1 | Limit exists (=2) but f(1) is undefined. A single point is missing; redefining f(1)=2 repairs it |
| **Jump** | sign(x) at 0 | One-sided limits exist and **differ**; no redefinition can repair it |
| **Infinite** | 1/x² at 0 | Function grows without bound; the limit does not exist (even as ±∞ it is not a real limit) |
| **Floor** ⌊x⌋ | at every integer | Jump of 1 at each integer; right-continuous everywhere, left-discontinuous at integers |

The floor function is the useful one: it is discontinuous at **infinitely many** points yet
continuous on every open interval between them. Students should note it is **right**-continuous —
lim(x→n⁺)⌊x⌋ = n = ⌊n⌋, while the left limit is n−1.

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

## Part 4 — Bisection

f(x) = x³ − x − 2 on [1,2]: f(1) = **−2**, f(2) = **4**. Opposite signs, f continuous, so the
**Intermediate Value Theorem** guarantees a root in between.

| Iteration | Bracket | Width |
|---|---|---|
| 1 | [1.500000000, 2.000000000] | 5.00 × 10⁻¹ |
| 2 | [1.500000000, 1.750000000] | 2.50 × 10⁻¹ |
| 3 | [1.500000000, 1.625000000] | 1.25 × 10⁻¹ |
| 5 | [1.500000000, 1.531250000] | 3.12 × 10⁻² |
| 10 | [1.520507812, 1.521484375] | 9.77 × 10⁻⁴ |
| 12 | [1.521240234, 1.521484375] | 2.44 × 10⁻⁴ |

Root ≈ **1.521362305**, with f ≈ −1.0 × 10⁻⁴.

**The width halves every step**: after n steps it is (b−a)/2ⁿ, so reaching tolerance ε needs
**n ≥ log₂((b−a)/ε)** iterations — about 3.3 steps per decimal digit. That predictability is
bisection's selling point; Newton's method is faster but can diverge, while bisection **cannot
fail** once a sign change is bracketed.

Note the IVT guarantees *existence*, never uniqueness. A student who claims "exactly one root" from
the IVT alone has over-concluded — here it happens to be true, but that needs a separate argument
(f′ = 3x² − 1 > 0 on [1,2], so f is strictly increasing).

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
