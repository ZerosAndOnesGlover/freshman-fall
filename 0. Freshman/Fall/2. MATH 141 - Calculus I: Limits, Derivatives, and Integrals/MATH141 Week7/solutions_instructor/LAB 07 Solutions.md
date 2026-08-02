# MATH 141 · Week 7
## LAB 07 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed, not estimated.** Students working in Desmos rather
> than Python will see the same behaviour but fewer digits — grade the *reasoning and the observed
> trend*, not agreement to the last decimal place.

---

## Part 1 — Growth Rate Hierarchies

The hierarchy, slowest to fastest:

$$\ln x \;\ll\; x^{0.5} \;\ll\; x \;\ll\; x^2 \;\ll\; e^x \;\ll\; x!$$

| x | ln x | x^0.5 | x/ln x |
|---|---|---|---|
| 10 | 2.303 | 3.162 | 4.343 |
| 100 | 4.605 | 10.000 | 21.715 |
| 1,000 | 6.908 | 31.623 | 144.765 |
| 10,000 | 9.210 | 100.000 | 1085.736 |

x/ln x diverging confirms **ln x grows slower than any positive power of x**.

Exponential dominance, via x²/eˣ:

| x | x²/eˣ |
|---|---|
| 5 | 1.68 × 10⁻¹ |
| 10 | 4.54 × 10⁻³ |
| 20 | 8.24 × 10⁻⁷ |
| 50 | **4.82 × 10⁻¹⁹** |

Each ratio is an ∞/∞ form; L'Hôpital applied twice gives 2/eˣ → 0.

> **L'Hôpital's Rule applies only to 0/0 and ∞/∞.** Using it on 2/0 or 0/5 produces nonsense. Other
> indeterminate forms (0·∞, ∞−∞, 1^∞) must be **algebraically converted first** — and each
> application requires rechecking that the new limit is still indeterminate.
>
> It is **not** the quotient rule: L'Hôpital replaces f/g with f′/g′, differentiating numerator and
> denominator *separately*.

**1.2 The 1^∞ form.** (1 + 1/n)ⁿ:

| n | value |
|---|---|
| 10 | 2.5937424601 |
| 100 | 2.7048138294 |
| 10⁴ | 2.7181459268 |
| 10⁷ | 2.7182816941 |

→ **e = 2.7182818285**. The standard technique is to take logs: ln y = n·ln(1 + 1/n), which is an
∞·0 form, rewritten as ln(1+1/n)/(1/n) — now 0/0, so L'Hôpital applies and gives 1, hence y → e¹.

`1^∞` is indeterminate precisely because the base approaches 1 *from above* while the exponent
grows; which effect wins depends on the rates.

---

## Part 2 — Curve Sketching

The required checklist, in order:

1. **Domain** and any excluded points
2. **Intercepts**
3. **Symmetry** — even, odd, or neither
4. **Asymptotes** — vertical (denominator zeros), horizontal (limit at ±∞), oblique (when the
   numerator's degree exceeds the denominator's by exactly 1)
5. **f′**: critical points, increasing/decreasing intervals
6. **f″**: concavity, inflection points
7. Assemble, then **check against a plot**

The plot is the *verification*, not the method. A student who plots first and annotates afterwards
has done the exercise backwards and should be told so — the point is to predict, then confirm.

---

## Part 3 — Optimization

**3.1 Minimum-cost pipeline.** The standard setup: minimise a cost function over a feasible domain,
typically C(x) = a·√(x²+h²) + b·(L−x). Setting C′ = 0 gives the interior critical point.

**Three things a complete answer must include:**

1. The **feasible domain** stated explicitly (here 0 ≤ x ≤ L) — a physical problem has bounds.
2. **Endpoint evaluation.** The optimum may sit at an endpoint, and a single interior critical point
   is not automatically the answer.
3. A **justification of max vs. min** — first-derivative sign test or the second-derivative test —
   not merely "I set the derivative to zero".

**3.2 Numerical comparison.** Golden-section search or ternary search converges to the same optimum
without derivatives. The comparison worth drawing: the analytic method gives an **exact** answer and
requires a differentiable closed form; the numerical method needs only evaluations and works on
functions with no closed form at all. Neither dominates.

---

## Part 4 — Design Your Own

Grade the **modelling**, not the arithmetic: is there a genuine constraint that eliminates one
variable? Is the objective function correctly derived from the geometry or economics? Is the domain
stated? A problem whose "constraint" does not actually constrain anything is the commonest failure.

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

*MATH 141 · Week 7 · Lab Solutions · Instructor Copy · © CSE Department*
