# CS 101 — Week 6
## LAB 6 Solutions — INSTRUCTOR ONLY

> **All code below was executed and all stated outputs are real.** Where a benchmark appears,
> the absolute timings are machine-specific — grade the *ratios* and the conclusions, never the
> raw milliseconds.

---

## Part 1 — Theoretical Analysis

| Function | Big-O | Reasoning | Recurrence |
|---|---|---|---|
| **A** | **Θ(n)** | Single loop, O(1) body | — |
| **B** | **Θ(n²)** | Nested loops, inner bound independent of outer ⇒ multiply | — |
| **C** | **Θ(log n)** | `i *= 2` — counter is *multiplied*, so it reaches n in log₂n steps | — |
| **D** | **Θ(n log n)** | Timsort; Θ(n) on already-sorted input (adaptive) | — |
| **E** | **Θ(2ⁿ)** | Two recursive calls, each on n−1 | T(n) = 2T(n−1) + O(1) |
| **F** | **Θ(φⁿ)**, φ≈1.618 | Two calls on n−1 and n−2 — overlapping subproblems | T(n) = T(n−1) + T(n−2) + O(1) |
| **G** | **O(n²)** worst, **O(1)** best | Nested loop; returns early on the first duplicate | — |
| **H** | **Θ(n log n)** | Master Theorem case 2: a=2, b=2, f(n)=n, n^(log₂2)=n | T(n) = 2T(n/2) + n |

**Points that separate a good answer from a passing one:**

- **C is the only sublinear function.** The distinguishing feature is multiplication of the counter,
  not the `while`.
- **E vs. F.** Both are exponential but with *different bases*: E branches on n−1 twice giving 2ⁿ,
  F on n−1 and n−2 giving φⁿ. Students who write "both O(2ⁿ)" have an upper bound that is correct
  but not tight for F.
- **G must be stated with best and worst cases.** It is the only function here whose cost depends
  on the *data* rather than just n. `O(n²)` alone is an incomplete answer.
- **D is a trap for students who write Θ(n).** `sorted` is not free.

---

## Part 2–3 — Empirical Measurement and Exponent Estimation

Fitting log t = k·log n + c over four doubling sizes; **k is the empirical exponent**.

| Function | Measured doubling ratios | Fitted k | Theory |
|---|---|---|---|
| A | 1.72, 2.06, 1.97 | **0.946** | 1 |
| B | 4.74, 4.41, 3.95 | **2.123** | 2 |
| G (no duplicates — worst case) | 4.24, 4.05, 4.11 | **2.045** | 2 |
| D | 2.18, 2.53, 2.46 | **1.263** | 1 + log correction |

Raw timings:

```
func_a   n=  200,000   10.368 ms      func_b   n=  300     4.191 ms
         n=  400,000   17.871 ms               n=  600    19.854 ms
         n=  800,000   36.861 ms               n= 1200    87.464 ms
         n=1,600,000   72.488 ms               n= 2400   345.065 ms

func_g   n=    500      3.855 ms      func_d   n=100,000   20.499 ms
         n=  1,000     16.330 ms               n=200,000   44.705 ms
         n=  2,000     66.215 ms               n=400,000  113.170 ms
         n=  4,000    272.362 ms               n=800,000  278.661 ms
```

**How to read these:**

- **A gives k = 0.946, not 1.000.** This is *not* evidence against Θ(n) — it is measurement noise
  plus fixed overhead. At the smallest size a constant startup cost is a larger fraction of the
  total, which flattens the fitted line. The doubling ratios (1.72, 2.06, 1.97) straddle 2, which
  is the more robust read. **Expect k within ±0.1 of theory and treat anything closer as luck.**
- **B and G both land near 2.0**, confirming quadratic. G was measured on input with **no
  duplicates**, forcing the worst case; a student who benchmarks G on random data with repeats will
  measure something close to Θ(1) and conclude the function is constant-time. That is the single
  most instructive mistake available in this lab — **the benchmark must construct the worst case
  deliberately.**
- **D gives k = 1.263, visibly above 1.** The log factor in n log n behaves like a slowly growing
  exponent: over this range, log₂n runs from ~17 to ~20, so t ∝ n·log n looks like n^1.06 in
  theory. The measured 1.26 exceeds even that, because sorting 800,000 floats starts to miss cache.
  **This is why Θ(n) and Θ(n log n) cannot be reliably separated empirically** — the log factor is
  within the noise of ordinary measurement, which is a genuine limitation worth stating.

### `func_c` — logarithmic

| n | `func_c(n)` | log₂ n |
|---|---|---|
| 1,000 | 10 | 10.0 |
| 1,000,000 | 20 | 19.9 |
| 10⁹ | 30 | 29.9 |
| 10¹² | 40 | 39.9 |

The return value **is** ⌈log₂ n⌉. Multiplying n by 1000 adds ~10 to the count. Note this cannot be
timed meaningfully — 40 iterations is below the clock's resolution — so the *return value* is the
measurement. Reward students who realise that counting operations beats timing them when the
operation count is small.

### `func_e` and `func_f` — exponential, by call count

| n | `func_e` calls | `func_f` calls |
|---|---|---|
| 5 | 31 | 15 |
| 10 | 1,023 | 177 |
| 15 | 32,767 | 1,973 |
| 20 | **1,048,575** | **21,891** |

- **`func_e` makes exactly 2ⁿ − 1 calls.** Check: 2²⁰ − 1 = 1,048,575 ✓. The recurrence
  C(n) = 2C(n−1) + 1 with C(1) = 1 unrolls to 2ⁿ − 1.
- **`func_f` makes 2·fib(n+1) − 1 calls**: fib(21) = 10,946, and 2(10,946) − 1 = 21,891 ✓.

The ratio between them at n = 20 is nearly **48×**, and it widens with n — a concrete demonstration
that φⁿ and 2ⁿ are *not* the same growth rate even though both are "exponential".

### `func_h` — the Master Theorem case

| n | Return value | Calls | n·log₂n |
|---|---|---|---|
| 16 | 80 | 31 | 64 |
| 64 | 448 | 127 | 384 |
| 256 | 2,304 | 511 | 2,048 |
| 1,024 | 11,264 | 2,047 | 10,240 |

The return value is exactly **n(log₂ n + 1)** — check 1024 × 11 = 11,264 ✓ — confirming
T(n) = 2T(n/2) + n solves to Θ(n log n). The **call count is 2n − 1** (2·1024 − 1 = 2,047 ✓),
because the recursion tree is a complete binary tree with n leaves.

This function is the cleanest illustration in the course of Master Theorem **case 2**: the critical
exponent n^(log_b a) = n^(log₂2) = n matches f(n) = n, so every level costs the same Θ(n) and there
are log n levels.

---

## Part 5 — Formal Big-O Proofs

`func_b` executes its inner statement exactly n² times, so a proof for it is immediate with c = 1,
n₀ = 0. The instructive case is a polynomial with lower-order terms — use this as the model:

> **Claim.** 3n² + 100n + 7 is O(n²).
> **Proof.** Take n₀ = 1. For all n ≥ 1 we have n ≤ n² and 1 ≤ n², so
> 3n² + 100n + 7 ≤ 3n² + 100n² + 7n² = 110n².
> Hence c = 110, n₀ = 1 witnesses the definition. ∎

**Grade the structure, not the constants.** Any valid (c, n₀) pair proves the claim — c = 110 with
n₀ = 1 and c = 4 with n₀ = 101 are equally correct. What must be present:

1. The definition **stated** before it is used.
2. **Explicit** c and n₀, not "for large enough n".
3. An inequality chain that actually establishes f(n) ≤ c·g(n), with each step justified.

A proof that ends "therefore it is O(n²)" without exhibiting constants has asserted the conclusion,
not proved it. Conversely, students who note that the same argument proves O(n³) — and that this is
*true but weaker* — have understood that Big-O is an upper bound and deserve credit.

---

## Marking Scheme

The lab is checkoff-graded against the criteria on the handout. Within each part:

- **Method (≈60%).** Correct approach, required loop/structure type actually used, edge cases
  considered, invariants stated where the handout asks for them.
- **Result (≈40%).** Code runs, produces the specified output, and the written answers are correct.

**Carry-through.** A wrong helper that is then used correctly downstream costs marks once.

**Watch for the two failure modes that matter:**
1. Code that produces the right answer for the sample input and is wrong in general — always run
   the edge cases listed under each exercise.
2. Written answers that restate the observation instead of explaining it. "0.1 + 0.2 isn't 0.3
   because floats are imprecise" earns nothing; the answer must reach binary representation.

---

*CS 101 · Week 6 · Lab Solutions · Instructor Copy · © CSE Department*
