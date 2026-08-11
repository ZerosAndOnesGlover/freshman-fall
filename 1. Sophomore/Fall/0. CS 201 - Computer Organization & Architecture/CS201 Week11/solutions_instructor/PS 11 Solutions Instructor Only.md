# CS 201 · Problem Set 11 — Solutions
## Instructor Only

---

> **Not for distribution.** All figures measured on the lab image (i5-8250U, GCC 13.3). **Q3 is a
> report — the marked artefact is the *method shown at every step*, not the final speedup number.**

---

## Q1 (18) — The Method

### (a) [4]

**Measure** (`time`/stopwatch) → **Profile** (gprof, `perf`, callgrind) → **Diagnose** (cachegrind, disassembly) → **Bound** (Amdahl) → **Fix and re-measure**. Half a mark per step-with-tool; the diagnose and bound steps are the ones students omit.

### (b) [4]

> *"We should forget about small efficiencies, say about 97% of the time: premature optimization is
> the root of all evil. Yet we should not pass up our opportunities in that critical 3%."*

**[2]** The famous first clause warns against optimising by guesswork on code that does not matter. **[2] The second clause licenses — indeed demands — optimising the critical 3% once you have *found* it by measurement.** The quote is not anti-optimisation; it is anti-*premature* (i.e. un-measured) optimisation.

### (c) [4]

**Sampling:** periodically interrupts and records the PC. **Low overhead (few %), statistical, sees the whole program.** **Instrumenting:** inserts code at every entry/exit. **Exact counts, high overhead (20–50×), perturbs the measurement.** Sampling for production and for realistic timing; instrumenting when you need exact call counts and can tolerate the slowdown.

### (d) [3]

**`-O2` inlines `cheap`/`expensive` into `main`, erasing the boundaries the profiler attributes time to** — so everything is charged to `main`. **`-O2 -fno-inline`** restores the boundaries, at the cost of some realism (the shipped build *does* inline).

### (e) [3]

**`__mcount_internal` is gprof's own instrumentation** — the counting code inserted at each call. Its appearance at ~11% (with `mcount`, ~20% total) demonstrates that **an instrumenting profiler perturbs what it measures**: a fifth of the "work" in the profile is the profiler itself. *(Verified: 156M + 126M of ~1.38G instructions.)*

---

## Q2 (20) — The Roofline

### (a) [6] — 2 each

| Op | flops | bytes (double) | intensity | bound |
|---|---:|---:|---:|---|
| Vector add `c=a+b` | 1 | 24 | **0.042** | memory |
| SAXPY `y=a*x+y` | 2 | 24 | **0.083** | memory |
| Dot product | 2 | 16 | **0.125** | memory |

*(All well below any modern ridge point — all memory-bound.)*

### (b) [4]

Roofline: **flat roof = peak compute (GFLOP/s)**; **slanted roof = peak bandwidth (performance = intensity × bandwidth)**; **ridge = their intersection**; left of ridge **memory-bound** (fix: reduce bytes moved / improve locality), right **compute-bound** (fix: reduce flops / vectorise / more cores).

### (c) [4]

Matmul: **$2n^3$ flops** over **$\sim 3n^2$ words = $24n^2$ bytes**, so intensity $\sim \dfrac{2n^3}{24n^2} = \dfrac{n}{12}$ — **grows linearly with $n$**. A large matmul crosses the ridge and becomes compute-bound; vector add's intensity is a constant 0.042 regardless of size, so it is *always* memory-bound.

### (d) [6]

**[3] LLd rate = D1 rate = 50% means every L1 miss also missed L2 and L3 and went to DRAM** — the lower caches caught nothing, because the column stride outran them. **[2] Same signature as Week 4's naive transpose.** **[1]** The fix (loop reorder → streaming access) **reduces bytes moved from DRAM, not flops** — a memory-bound fix, moving the program along the roofline's slanted roof.

---

## Q3 (40) — Your 10× Speedup

**Marked on method, not on the number.** A student who reaches 10× with no diagnosis scores far below one who reaches 6× with a complete, evidenced report. The reference solution uses the Lab 11 matmul.

| Part | Marks | What earns them |
|---|---:|---|
| (a) Baseline | 6 | Correctness check + median-of-several timing with range |
| (b) Profile | 8 | Hotspot identified with evidence; inlining handled if it hid the boundary |
| (c) Diagnose | 8 | cachegrind/disassembly showing *why*; placed on the roofline |
| (d) Bound | 6 | Amdahl computed *before* the fix; decision justified |
| (e) Fix + re-measure | 8 | Change shown, correctness preserved, new time + re-profile |
| (f) Reflect | 4 | Bottleneck moved as predicted; next target and its ceiling |

**Reference figures (matmul, verified):**

- Baseline naive `ijk` `-O2`: 5.52 s.
- Diagnosis: D1/LLd both 50.1% → memory-bound, under the slanted roof.
- Fix (`ikj`): 0.74 s, **7.45×**, D1/LLd → 8.3%.
- Plus flags (`-O3 -march=native`): 0.58 s from a 16.12 s `-O0` baseline = **27.8×**.

> **Two failure modes to penalise:** (1) a speedup with no correctness check — a fast wrong answer;
> (2) a "diagnosis" that is a guess, not a measurement. **Both forfeit most of the relevant part's
> marks**, because the whole point of the week is that the method, not the intuition, produces the
> speedup.
>
> **Reward** a student whose Amdahl bound in (d) correctly predicted a *disappointing* result and who
> then chose a different target — that is the method working.

---

## Q4 (22) — Benchmark Honestly

### (a) [6]

**[3]** `-O2` folds `for(i) s+=i` to a constant; `objdump` shows `movabs rdx,0x…` = the answer, and the loop is absent. **[3]** Fix: make `n` unknown at compile time (`argc`, a `volatile`, a separate TU), disassemble to show the loop restored. **Prevented: constant folding / dead-code elimination.** *(Verified — Week 0.)*

### (b) [6] — 1 for each (i)/(ii)

1. **Measured the page cache, not the device** — the data was resident in DRAM. Fix: `O_DIRECT`, or state you meant the cache.
2. **Measured fast arithmetic on zeros** — the test values decayed out of the denormal range within a few thousand iterations. Fix: an array that *stays* denormal for the whole loop (Week 1's corrected version gave 34×).
3. **Measured a DRAM-bound workload where the TLB was not the bottleneck** — huge pages fix translation, and translation was not what it was waiting for. Fix: a cache-resident, page-spanning access pattern where the TLB *is* the limit.

### (c) [5]

Three of: **CPU governor / turbo state** (cold first run, thermal throttling); **other load on a shared machine**; **cache/TLB warm-up**; **ASLR-dependent layout effects**. **[report]** warm up, run many times, **report median and range** (or a percentile), state the machine's state (governor, load) or pin it. **A single number has no error bar.**

### (d) [5]

**Any earlier result with its independent model.** Best examples: the harmonic-sum **absorption index derived as $2^{21}$ and measured as $2^{21}$** (Week 1); the **cache cliffs matching `lscpu -C`** (Week 4); the **131 071 faults matching 131 072 pages** (Week 6); the **relative branch target computed by hand and confirmed by `objdump`** (Week 0). **The cross-check makes it trustworthy because agreement between an independent prediction and a measurement is very unlikely by chance** — a bare number could be an artefact of the measurement itself, but a number that matches a model computed a different way is corroborated.

---

## Mark Summary

| | |
|---|---:|
| Q1 | 18 |
| Q2 | 20 |
| Q3 | 40 |
| Q4 | 22 |
| **Total** | **100** |

**Where the class loses marks, in order:**

1. **Q3(c)/(d)** — skipping diagnose and bound, jumping straight from profile to a guessed fix.
2. **Q3(a)/(e)** — no correctness check; a fast wrong answer.
3. **Q4(d)** — restating a number without naming the independent model.
4. **Q2(d)** — not connecting the equal miss rates to "every miss reached DRAM".
5. **Q1(b)** — quoting only the famous half of Knuth.

**The whole point of the assignment:** the method produces the speedup, not the intuition. Grade the method.

---

*CS 201 · Week 11 · PS 11 Solutions · Instructor Only*
