# CS 201 · Lab 11 — Solutions and TA Notes
## Instructor Only

---

> **Unmarked.** Five checkpoints. All figures verified on the lab image. **This is the capstone lab
> and the template for half of Project 2 — protect the full method, do not let it become "run
> gprof".**

---

## Before the Session

**`perf` is unavailable** (`perf_event_paranoid = 4`). Say so, and say what the substitutes are: gprof for sampling + call counts, callgrind/cachegrind for exact analysis. **The method is what transfers, not the tool** — a student who can profile-diagnose-bound-fix-remeasure with gprof can do it with `perf` in five minutes.

**The pedagogical arc:** Part 1 makes them guess wrong; Part 2 shows the profiler correcting them; Part 3 makes them compute the ceiling before working; Part 4 is a real optimisation with a real diagnosis; Part 5 is the honesty check. **Every step is a step they will skip in Project 2 unless it is drilled here.**

---

## Timing

| Part | Budget | Reality |
|---|---|---|
| 1 — measure + guess | 10 min | 10 min |
| 2 — profile | 20 min | 20 min |
| 3 — Amdahl bound | 10 min | 10 min |
| 4 — **the real optimisation** | 35 min | **Protect this** |
| 5 — a benchmark that lies | 15 min | 15 min |

---

## Part 1

**Make them write the guess down.** Most will pick `cheap` (twice the calls) or hedge. The value of Part 2 is proportional to how committed the wrong guess was.

**✅ CHECKPOINT 1**

---

## Part 2

*(Verified: `expensive` 94.44%, `cheap` 0.00%, with 2M/4M call counts. The `-O2` build shows 100% `main`.)*

1. **The guess was wrong**; **time-per-call × calls** is what matters, not calls alone. `expensive`'s 50-iteration `sqrt` loop dwarfs `cheap`'s single multiply.
2. **`-O2` inlined both functions into `main`**; `-fno-inline` restores boundaries at a small realism cost.
3. **`mcount`/`__mcount_internal` is gprof's instrumentation** (~20% of the callgrind profile) — proof that **instrumenting profilers perturb their own measurement**. Connect to Week 0.

**✅ CHECKPOINT 2**

---

## Part 3

*(Reference: 16.7× ceiling if `expensive` → 0; 1.89× if halved; `cheap` ceiling = 1/(1−0) ≈ 1.00×, i.e. essentially nothing.)*

**This is the step students most want to skip, and the one that saves the most wasted effort.** Make them state, from the numbers, that `cheap` is *never* worth touching (0% → 0% payoff) and that `expensive` is worth attacking but capped at 16.7×.

**✅ CHECKPOINT 3**

---

## Part 4 — the important one

### 4.1

*(Verified: `ijk` 5.52 s, `ikj` 0.74 s, **7.45×**, identical result.)*

### 4.2

*(Verified: `ijk` D1/LLd 50.1%/50.1%; `ikj` 8.3%/8.3%.)*

1. **LLd = D1 means every L1 miss went to DRAM** — L2/L3 caught nothing, exactly Week 4's transpose signature.
2. `ijk` strides B by a column: **1 useful double per 64-byte line (1/8 used)**. `ikj` streams B and C in row order: **8 of 8 doubles used**. Hence the ~6× drop in miss rate.
3. **Memory-bound, under the slanted roof; the fix reduces bytes moved, not flops.**

### 4.3

*(Verified ladder: 16.12 → 5.27 → 4.14 → 2.82 → 0.58 s.)*

4. **Flags and layout are multiplicative** — the flags make each iteration's arithmetic faster (vectorisation, unrolling), the layout makes the data arrive faster; they attack different resources, so the gains compose.
5. **Flags first** (free, and the compiler does work you would otherwise do by hand), **then profile, then fix the algorithm/layout** where the roofline points. Hand-tuning before `-O3` duplicates the compiler's effort.

> **The take-home is the ladder read as leverage:** free flags first, then measured, targeted
> structural change. This is exactly the Project 2 optimisation rubric.

**✅ CHECKPOINT 4**

---

## Part 5

*(Verified: `-O2` folds the sum loop to a `movabs` constant, 0.0000 s — Week 0.)*

1. **The loop was constant-folded away**; `main` contains `movabs` of the answer and no loop.
2. Fixes: `volatile`, value from `argc`, separate TU. Disassembly must show the loop back. **Prevented: dead-code elimination / constant folding.**
3. Checklist violated: **"Did the compiler delete it?"** Another always-ask: **"Is the result consumed?"** or **"Does it match theory?"**

**✅ CHECKPOINT 5**

---

## What Success Looks Like

1. Guess wrong, then let the profiler correct them — internalising "measure, don't guess".
2. Compute an Amdahl ceiling *before* optimising, and decline work that is not worth it.
3. **Diagnose a hotspot as memory- or compute-bound with cachegrind and the roofline.**
4. Achieve and *prove* a speedup — correctness preserved, re-profiled.
5. Recognise and fix a lying benchmark.

**This lab is the whole course's method in one sitting.** If a student leaves able to run the loop — measure, profile, diagnose, bound, fix, re-measure — the machine-organisation half of the degree has done its job.

---

*CS 201 · Week 11 · Lab 11 Solutions · Instructor Only*
