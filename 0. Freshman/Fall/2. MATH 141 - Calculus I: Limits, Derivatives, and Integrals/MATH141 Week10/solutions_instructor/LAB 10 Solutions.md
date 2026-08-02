# MATH 141 — Week 10
## LAB 10 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed, not estimated.** Students working in Desmos rather
> than Python will see the same behaviour but fewer digits — grade the *reasoning and the observed
> trend*, not agreement to the last decimal place.

---

## Part 1 — Substitution Pattern Recognition

The pattern to teach: look for a composite f(g(x)) whose **inner derivative g′(x) is present as a
factor** (up to a constant).

| Integral | u | du |
|---|---|---|
| ∫ 2x·e^(x²) dx | x² | 2x dx |
| ∫ x/(1+x²) dx | 1+x² | 2x dx — supply the 1/2 |
| ∫ sin(x)cos(x) dx | sin x | cos x dx (or u = cos x; both work) |
| ∫ (ln x)/x dx | ln x | dx/x |
| ∫ tan x dx | cos x | −sin x dx |

**The diagnostic for a bad choice:** the substitution leaves an x that cannot be eliminated. That
means the derivative factor was not really present, and a different u — or a different technique —
is needed.

---

## Part 2 — Verifying Substitution Numerically

The two required checks:

1. **Change the limits.** For a definite integral, either convert the limits to u, or convert back
   to x before evaluating. **Substituting x-limits into a u-expression is the single most common
   substitution error** and produces a plausible wrong number.
2. **Differentiate the answer.** The fastest verification of any antiderivative is to differentiate
   it and compare with the integrand — numerically if not symbolically.

---

## Part 3 — Symmetry

Verified by numerical integration (midpoint, n = 200,000):

| Integral | Computed | Rule |
|---|---|---|
| ∫₋₂² x³ dx | **0.0000000000** | odd ⇒ 0 |
| ∫₋₁¹ x·cos x dx | **0.0000000000** | odd × even = odd ⇒ 0 |
| ∫₋₂² x² dx | 5.3333333332 | even ⇒ 2∫₀² = 5.3333333333 |

**The rules require the interval to be symmetric about 0**, and the student must *state which
symmetry applies and why*:

- f odd (f(−x) = −f(x)) ⇒ ∫₋ₐᵃ f = 0
- f even (f(−x) = f(x)) ⇒ ∫₋ₐᵃ f = 2∫₀ᵃ f

Asserting symmetry without checking f(−x) earns no method marks. Note **odd × even = odd** and
**odd × odd = even** — the parity algebra is worth tabulating, since x·cos x being odd is not
obvious at a glance.

---

## Part 4 — The Tabular Method

For ∫ x³eˣ dx, differentiate the polynomial column to zero and integrate the exponential column,
alternating signs:

| Sign | u (differentiate) | dv (integrate) |
|---|---|---|
| + | x³ | eˣ |
| − | 3x² | eˣ |
| + | 6x | eˣ |
| − | 6 | eˣ |
| + | 0 | eˣ |

Reading down the diagonals:

$$\int x^3 e^x\,dx = e^x\left(x^3 - 3x^2 + 6x - 6\right) + C$$

**Verified numerically on [0,1]:**

```
antiderivative  F(1) - F(0) = 0.5634363431
midpoint sum                = 0.5634363431
```

Exact agreement to 10 decimal places. ✓

The tabular method works when **one factor differentiates to zero in finitely many steps** — a
polynomial — and the other integrates indefinitely. It is not a new theorem, just repeated
integration by parts with the bookkeeping made visible.

---

## Part 5 — The "Solve for I" Technique

For ∫ eˣ sin x dx, two applications of integration by parts return the original integral:

$$I = e^x\sin x - e^x\cos x - I \quad\Longrightarrow\quad 2I = e^x(\sin x - \cos x)$$

$$\int e^x \sin x\,dx = \frac{e^x(\sin x - \cos x)}{2} + C$$

**Verified on [0, π]:**

```
closed form  = 12.0703463164
numeric      = 12.0703463166
```

✓ (The 10th-digit difference is the numerical integrator's truncation error, not an algebra error.)

The technique is worth naming explicitly: when the integral **reappears** after repeated parts, do
not despair and do not keep going — treat it as an algebraic unknown and solve. Students who apply
parts a third time and loop forever have missed the move, and it is the only place in the course
where the answer comes from algebra rather than from calculus.

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

*MATH 141 · Week 10 · Lab Solutions · Instructor Copy · © CSE Department*
