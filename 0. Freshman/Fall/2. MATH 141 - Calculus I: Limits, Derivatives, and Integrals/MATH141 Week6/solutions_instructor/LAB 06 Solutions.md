# MATH 141 · Week 6
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

## Part 3 — f and f′ Side by Side

**3.1** $f'(x)=4x^3-12x^2+8x=4x(x-1)(x-2)$. Critical numbers $0, 1, 2$.

| Interval | Sign of f′ | f |
|---|---|---|
| $(-\infty,0)$ | − | decreasing |
| $(0,1)$ | + | increasing |
| $(1,2)$ | − | decreasing |
| $(2,\infty)$ | + | increasing |

Local minima at $x=0$ ($f=0$) and $x=2$ ($f=0$); local maximum at $x=1$ ($f=1$).

**3.2** $f'=(x+2)(x-1)^2$. Critical numbers $-2, 1$. $f'<0$ on $(-\infty,-2)$ and $f'>0$ on $(-2,1)$ and
$(1,\infty)$: local minimum at $x=-2$; **no extremum at $x=1$** (f′ touches 0 without changing sign —
the squared factor). Any two such $f$ differ by a constant (Corollary 2).

---

## Part 4 — L'Hôpital Numerically

*(Values computed in Python 3.14.)*

| h | (eʰ−1−h)/h² |
|---|---|
| 0.1 | 0.517092 |
| 0.01 | 0.501671 |
| 0.001 | 0.500167 |
| 0.0001 | 0.500017 |

Limit $\tfrac12$: two applications give $e^h/2\to\tfrac12$.

| x | ln x/√x |
|---|---|
| 10 | 0.728141 |
| 10² | 0.460517 |
| 10⁴ | 0.092103 |
| 10⁶ | 0.013816 |

Limit 0 (L'Hôpital: $2/\sqrt{x}\to0$): $\sqrt{x}$ grows faster than $\ln x$. Note the value *rises* at
first — the limit only shows for large $x$.

**4c.** $1+\cos x$ oscillates between 0 and 2 forever, so $\lim f'/g'$ does not exist and the rule gives
no information; the graph of $(x+\sin x)/x$ visibly settles to 1.

---

## Part 5 — Root Counting via Rolle's Theorem

Rolle: if f(a) = f(b) and f is continuous on [a,b], differentiable on (a,b), then f′(c) = 0 for some
c in (a,b).

**The counting argument:** between any two roots of f there is a root of f′. So if f′ has at most k
roots, f has at most k+1. Combined with the IVT (which supplies *existence* from sign changes),
this brackets the root count exactly.

For f(x) = x⁵ + 3x + 1: f′(x) = 5x⁴ + 3 ≥ 3 > 0, so f′ is never zero and f has **at most one** root.
f(−1) = −3 < 0 and f(0) = 1 > 0, so by the IVT there is a root in (−1, 0). Hence **exactly one** real
root.

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
