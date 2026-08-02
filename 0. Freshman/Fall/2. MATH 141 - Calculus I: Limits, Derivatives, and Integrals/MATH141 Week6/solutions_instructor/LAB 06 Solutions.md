# MATH 141 — Week 6
## LAB 06 Solutions — INSTRUCTOR ONLY

> **Every numerical value below was computed, not estimated.** Students working in Desmos rather
> than Python will see the same behaviour but fewer digits — grade the *reasoning and the observed
> trend*, not agreement to the last decimal place.

---

## Part 1 — Every EVT Hypothesis Matters

The Extreme Value Theorem: a function **continuous** on a **closed, bounded** interval attains an
absolute maximum and minimum. Break any one hypothesis and the conclusion fails:

| Broken hypothesis | Counterexample | What fails |
|---|---|---|
| Continuity | f(x) = 1/x on [−1,1] (undefined at 0) | Unbounded; no max or min |
| Closed interval | f(x) = x on **(0,1)** | Infimum 0 and supremum 1 are never attained |
| Bounded interval | f(x) = x on [0,∞) | No maximum |

The open-interval case is the most instructive: f(x) = x on (0,1) is continuous and bounded, gets
arbitrarily close to 1, and **never reaches it**. "Bounded" and "attains its bound" are different
statements, and that distinction is the whole content of the EVT.

---

## Part 2 — The Mean Value Theorem

**2.1** MVT: if f is continuous on [a,b] and differentiable on (a,b), there exists c in (a,b) with
f′(c) = (f(b) − f(a))/(b − a).

For f(x) = x² on [0,3]: average slope = (9 − 0)/3 = **3**, and f′(c) = 2c = 3 gives **c = 1.5**.
Geometrically, the tangent at x = 1.5 is parallel to the secant joining (0,0) and (3,9).

**2.2 MVT and average velocity.** If you travel 120 miles in 2 hours, your average speed is 60 mph,
and the MVT guarantees that at some instant your **instantaneous** speed was exactly 60. This is the
mathematical basis of average-speed traffic enforcement, and it is the most convincing motivation
available for the theorem.

**The hypotheses must be checked.** f(x) = |x| on [−1,1] has average slope 0 but **no** point where
f′ = 0 — it is not differentiable at 0. A student who applies the MVT without verifying
differentiability has assumed the conclusion.

---

## Part 3 — f, f′, f″ Side by Side

| f | f′ | f″ |
|---|---|---|
| increasing | positive | — |
| local max | crosses 0 downward | negative |
| local min | crosses 0 upward | positive |
| concave up | increasing | positive |
| inflection point | local extremum | **crosses** zero |

**The inflection point requires f″ to change sign, not merely to vanish.** f(x) = x⁴ has f″(0) = 0
and no inflection there. This is the exact analogue of "f′ = 0 does not imply an extremum".

**3.2 Reverse engineering** — given f′, reconstruct the shape of f — is the harder and more valuable
direction, and is the skill Part 4 of Lab 6 (accumulation functions) formalises.

---

## Part 4 — When the Second-Derivative Test Fails

Three functions with **f′(0) = f″(0) = 0** and three different behaviours:

| f | Behaviour at 0 |
|---|---|
| x⁴ | **local minimum** |
| −x⁴ | **local maximum** |
| x³ | **neither** — inflection with horizontal tangent |

**f″(c) = 0 is therefore completely inconclusive.** The test says nothing, and a student who
concludes "no extremum" from it has made a real error. The fallback is the **first-derivative sign
test**: examine the sign of f′ on either side of the critical point. For x⁴, f′ = 4x³ goes − to +,
so it is a minimum; for x³, f′ = 3x² is ≥ 0 on both sides, so no extremum.

---

## Part 5 — Root Counting via Rolle's Theorem

Rolle: if f(a) = f(b) and f is continuous on [a,b], differentiable on (a,b), then f′(c) = 0 for some
c in (a,b).

**The counting argument:** between any two roots of f there is a root of f′. So if f′ has at most k
roots, f has at most k+1. Combined with the IVT (which supplies *existence* from sign changes),
this brackets the root count exactly.

For f(x) = x³ − x − 2: f′ = 3x² − 1 has two roots (±1/√3), so f has **at most three** roots. Testing
signs shows exactly one sign change, so f has **exactly one** real root — the 1.5213… found by
bisection in Lab 1.

This pairing is the point of the exercise: **IVT gives existence, Rolle gives uniqueness.** Neither
alone is enough.

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

*MATH 141 · Week 6 · Lab Solutions · Instructor Copy · © CSE Department*
