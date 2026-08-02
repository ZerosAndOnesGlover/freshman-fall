# MATH 141 · Week 0
## LAB 00 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed, not estimated.** Students working in Desmos rather
> than Python will see the same behaviour but fewer digits — grade the *reasoning and the observed
> trend*, not agreement to the last decimal place.

---

## Part 1 — Function Families

**1.1 Power functions.** Expected observations: even powers are symmetric about the *y*-axis and
non-negative; odd powers are symmetric about the origin. All pass through (1,1) and (0,0). On
(0,1) *higher* powers lie **below** lower ones; on (1,∞) the order reverses. That crossover at
x = 1 is the point students should articulate.

**1.2 Exponential vs. polynomial.** For x below roughly 1.0 and again between about 2 and 4,
`x**2` exceeds `2**x` — but beyond the final crossing the exponential wins permanently and by an
unbounded margin. At x = 50, `x²/eˣ ≈ 4.8 × 10⁻¹⁹`.

The point is not that exponentials are "bigger" but that **eventually** they dominate every
polynomial. A student who tests only x ≤ 3 will draw the opposite conclusion, which is exactly why
the activity specifies a wide window.

**1.3 Logarithms.** `ln x` grows without bound but *slower than any positive power of x*:
x/ln x rises 4.34 → 21.7 → 145 → 1086 as x goes 10 → 10⁴. Domain is x > 0, vertical asymptote at
x = 0, and ln x is negative on (0,1).

---

## Part 2 — Transformations

The standard results, and the one that reverses intuition:

| Change | Effect |
|---|---|
| f(x) + c | shift **up** by c |
| f(x + c) | shift **left** by c — *opposite* to the sign |
| c·f(x) | vertical stretch by c |
| f(cx) | horizontal **compression** by c — again inverted |
| −f(x) | reflect in the x-axis |
| f(−x) | reflect in the y-axis |

**Inside the parentheses, everything is backwards.** The reason is worth stating: f(x + 3) at
x = −3 gives f(0), so the graph reaches its old x = 0 behaviour three units *earlier*.

`|f(x)|` reflects everything below the axis upward; `f(|x|)` discards the left half and mirrors
the right half. These are different operations and students routinely conflate them.

---

## Part 3 — Secant Lines and the Approach to Calculus

**3.1** For f(x) = x² at x = 3, secant slope = (f(3+h) − f(3))/h:

| h | Secant slope |
|---|---|
| 1 | 7.0000000000 |
| 0.1 | 6.1000000000 |
| 0.01 | 6.0100000000 |
| 0.001 | 6.0010000000 |
| 10⁻⁶ | 6.0000010009 |

Algebraically the slope is exactly **6 + h**, which is why the digits march so cleanly. The limit is
**6**, and f′(x) = 2x gives 2(3) = 6 ✓. Ask students to derive 6 + h symbolically — that
cancellation *is* the derivative computation, done before they have the word for it.

The h = 10⁻⁶ row shows 6.0000010009 rather than 6.000001 exactly: floating-point error is already
visible, and Lab 1 pursues it.

**3.3 The e^x surprise.** The limit (eʰ − 1)/h:

| h | (eʰ − 1)/h |
|---|---|
| 1 | 1.7182818285 |
| 0.1 | 1.0517091808 |
| 0.01 | 1.0050167084 |
| 0.001 | 1.0005001667 |
| 10⁻⁶ | 1.0000005000 |

**The limit is 1**, so (eˣ)′ = eˣ · 1 = eˣ: the function is its own derivative. This is the
*defining* property of e, and the activity's job is to make it an observation before it is a rule.
Try 2ˣ and 3ˣ for contrast — their limits are ln 2 ≈ 0.693 and ln 3 ≈ 1.099, bracketing 1, which is
where e "lives".

---

## Part 4 — The Mystery of |x| at 0

Left-hand secant slopes are **−1**, right-hand are **+1**, for every h. They never approach a
common value, so the two-sided limit does not exist and **|x| is not differentiable at 0** — despite
being perfectly continuous there.

**Continuity does not imply differentiability.** The graph has a *corner*: no single tangent line
exists, because the slope jumps. Differentiability is the strictly stronger condition, and this is
the cleanest counterexample in the course. (The converse *does* hold: differentiable ⇒ continuous.)

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

*MATH 141 · Week 0 · Lab Solutions · Instructor Copy · © CSE Department*
