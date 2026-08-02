# MATH 141 — Week 3
## LAB 03 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed, not estimated.** Students working in Desmos rather
> than Python will see the same behaviour but fewer digits — grade the *reasoning and the observed
> trend*, not agreement to the last decimal place.

---

## Part 1 — Secant Lines Converging to the Tangent

For f(x) = x² at x = 3 the secant slope is exactly **6 + h**, converging to 6 = f′(3). See Lab 0
Part 3 for the full table; the point here is that the *symbolic* cancellation and the *numerical*
trend are the same fact.

**1.2** Computing the slope at many x-values and plotting produces the graph of f′ — the derivative
as a **function**, not a number. This is the conceptual step of the week: f′(a) is a number, f′(x)
is a function, and confusing them is the commonest error in tangent-line problems.

---

## Part 2 — Reading the Derivative from a Graph

The correspondences students must state:

| On f | On f′ |
|---|---|
| increasing | f′ > 0 (above the axis) |
| decreasing | f′ < 0 |
| local max or min | f′ **crosses** zero |
| horizontal inflection | f′ **touches** zero without crossing |
| steepest ascent | f′ at a local maximum |
| concave up | f′ increasing |

The distinction between *crossing* and *touching* zero is what separates an extremum from a
saddle — and is exactly why the first-derivative **sign** test works where "f′ = 0" alone does not.

---

## Part 3 — Non-Differentiable Points

| Case | Example | Why differentiability fails |
|---|---|---|
| **Corner** | \|x\| at 0 | One-sided slopes −1 and +1; both exist, they differ |
| **Cusp** | x^(2/3) at 0 | Slopes → −∞ and +∞ |
| **Vertical tangent** | x^(1/3) at 0 | Slope → +∞ from both sides |
| **Discontinuity** | any jump | Differentiability implies continuity, so this fails first |

The subtler case is **x² sin(1/x)** (with f(0) = 0), which *is* differentiable at 0 with f′(0) = 0
— the x² factor squeezes the oscillation — yet f′ is **not continuous** at 0. This shows
"differentiable" does not imply "continuously differentiable", and is worth showing to strong
students.

---

## Part 4 — Numerical Differentiation and Its Limits

f = sin at x = 1, exact f′ = cos(1) = 0.540302305868140.

| h | Forward error | Central error | Fwd ratio | Ctr ratio |
|---|---|---|---|---|
| 10⁻¹ | 4.294 × 10⁻² | 9.001 × 10⁻⁴ | — | — |
| 10⁻² | 4.216 × 10⁻³ | 9.005 × 10⁻⁶ | 10.2 | **100.0** |
| 10⁻³ | 4.208 × 10⁻⁴ | 9.005 × 10⁻⁸ | 10.0 | **100.0** |
| 10⁻⁴ | 4.207 × 10⁻⁵ | 9.004 × 10⁻¹⁰ | 10.0 | **100.0** |
| 10⁻⁵ | 4.207 × 10⁻⁶ | 1.114 × 10⁻¹¹ | 10.0 | 80.8 |
| 10⁻⁶ | 4.207 × 10⁻⁷ | 2.772 × 10⁻¹¹ | 10.0 | **0.4** |
| 10⁻⁸ | 2.970 × 10⁻⁹ | 2.581 × 10⁻⁹ | 141.7 | 0.0 |
| 10⁻¹⁰ | 5.848 × 10⁻⁸ | 5.848 × 10⁻⁸ | 0.1 | 0.0 |

**Two findings, both required in the report:**

1. **Forward difference is O(h); central difference is O(h²).** Dividing h by 10 divides the forward
   error by 10 and the central error by **100** — visible in the ratio columns, and exactly what
   Taylor expansion predicts. The central formula's O(h) term cancels by symmetry.

2. **Smaller h stops helping and starts hurting.** The central error bottoms out near
   **h = 10⁻⁵** at about 1.1 × 10⁻¹¹, then *rises*. Below that, round-off in the numerator
   f(1+h) − f(1−h) — subtracting nearly equal quantities again — dominates the shrinking truncation
   error. The optimum trades the two off and sits near ε^(1/3) ≈ 6 × 10⁻⁶ for the central formula,
   ε^(1/2) ≈ 10⁻⁸ for the forward one.

By h = 10⁻¹⁰ both methods have the *same* error, because both are pure noise.

> **The lesson: "take h as small as possible" is wrong.** There is an optimal step size, and it is
> nowhere near machine epsilon. Students who report only that "smaller h is more accurate" have
> stopped measuring too early — insist on the full range down to 10⁻¹⁰.

**4.2 Product rule.** Verify (fg)′ = f′g + fg′ numerically at several points; the mismatch with the
plausible-looking f′g′ should be immediate and large.

---

## Part 5 — The Derivative of eˣ

lim(h→0)(eʰ − 1)/h = **1**, so (eˣ)′ = eˣ. For contrast, the same limit for 2ˣ gives
ln 2 ≈ 0.6931 and for 3ˣ gives ln 3 ≈ 1.0986 — so the base whose limit is exactly 1 lies between 2
and 3. **That base is the definition of e.**

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

*MATH 141 · Week 3 · Lab Solutions · Instructor Copy · © CSE Department*
