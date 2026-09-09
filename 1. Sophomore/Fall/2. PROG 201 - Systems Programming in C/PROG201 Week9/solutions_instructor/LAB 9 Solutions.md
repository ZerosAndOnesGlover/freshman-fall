# PROG 201 · Lab 9 Solutions
## Roofline Analysis — Instructor Only

---

**Do not distribute.** Part B turns on students producing a wrong bandwidth number and noticing it from a kernel above the roof. Telling them the answer removes the lab.

**Machine these numbers came from:** Intel i5-8250U (4 cores / 8 threads, 32 KiB L1d, 256 KiB L2, 6 MiB L3), Linux 7.0.0-30-generic, gcc 13.3.0. **Every student's numbers will differ**; mark the shape, the ratios and the reasoning.

> **`perf` does not work on these machines.** `kernel.perf_event_paranoid` is **4**, which refuses
> even `perf stat -e task-clock` on your own process. Lowering it needs root and is a real security
> decision on a shared machine. The week is built on Callgrind and a hand-written sampler instead,
> and [[PROG 201 Scheduling Notes]] §18 records it. **If a student asks whether they can just use
> `perf` at home: yes, and they should — the lab's Part B is the same either way.**

---

## 1. The Two TODOs

The kernels, the timing, `KEEP`, and `main` are provided.

```c
static double bandwidth(size_t bytes, int reps)
{
    double *a = aligned_alloc(64, bytes);
    memset(a, 1, bytes);
    size_t n = bytes / sizeof *a;
    double best = 0;
    for (int r = 0; r < reps; r++) {
        /* EIGHT accumulators, not one.  A single `s += a[i]` is a dependency
         * chain and measures add latency rather than memory bandwidth --
         * which is the mistake this file was written with, and it read 6.3
         * GB/s on a machine that does 14. */
        double s0=0,s1=0,s2=0,s3=0,s4=0,s5=0,s6=0,s7=0;
        double t0 = now();
        for (size_t i = 0; i + 7 < n; i += 8) {
            s0 += a[i]; s1 += a[i+1]; s2 += a[i+2]; s3 += a[i+3];
            s4 += a[i+4]; s5 += a[i+5]; s6 += a[i+6]; s7 += a[i+7];
        }
        double dt = now() - t0;
        double gbs = bytes / dt / 1e9;
        if (gbs > best) best = gbs;
        KEEP(s0); KEEP(s1); KEEP(s2); KEEP(s3);
        KEEP(s4); KEEP(s5); KEEP(s6); KEEP(s7);
    }
    free(a);
    return best;
}

static double flops(long iters, int reps)
{
    double best = 0;
    for (int r = 0; r < reps; r++) {
        double a0=1,a1=2,a2=3,a3=4,a4=5,a5=6,a6=7,a7=8;
        const double k = 1.0000001;
        double t0 = now();
        for (long i = 0; i < iters; i++) {
            a0 = a0*k + 1.0; a1 = a1*k + 1.0; a2 = a2*k + 1.0; a3 = a3*k + 1.0;
            a4 = a4*k + 1.0; a5 = a5*k + 1.0; a6 = a6*k + 1.0; a7 = a7*k + 1.0;
        }
        double dt = now() - t0;
        double gf = iters * 8.0 * 2.0 / dt / 1e9;      /* 8 FMAs = 16 flops */
        if (gf > best) best = gf;
        KEEP(a0); KEEP(a1); KEEP(a2); KEEP(a3);
        KEEP(a4); KEEP(a5); KEEP(a6); KEEP(a7);
    }
    return best;
}```

Builds clean under `gcc -Wall -Wextra -O2 -g -march=native -o roof roof.c -lm`.

---

## 2. Where Students Get Stuck

| # | Symptom | Cause | What to say |
| --- | --- | --- | --- |
| 1 | Bandwidth in the thousands of GB/s | `KEEP` omitted; the loop is gone | `objdump`. Part D(a) early |
| 2 | Bandwidth ≈ 6 GB/s, and a kernel above 100% | **one accumulator** — this is the lab | Point at the >100% row, say nothing else |
| 3 | Arithmetic peak ≈ 2 GFLOP/s | one accumulator again, in TODO 2 | Same cause, second place. Q5 |
| 4 | Ceilings fine, kernels all ~5% | built without `-march=native`, so no FMA | The Makefile has it; check they used `make` |
| 5 | Latency table has no steps | buffer too small, or the chase is sequential | It must be a shuffled cycle, and reach 256 MiB |
| 6 | "My ridge point is 3.1" | bandwidth wrong (see 2), peak right | The ratio is the tell |

**Symptom 2 is the session.** Do not diagnose it — ask which row of the kernel table is impossible, and let them work back from there. A student who finds it themselves has learned the lab's actual lesson, which is not about bandwidth.

---

## 3. Reference Output

**Part A — the hierarchy:**

```
         8 KiB         1.49 ns      L1d  (32 KiB)
        32 KiB         1.53
       128 KiB         3.13         L2   (256 KiB)
       256 KiB         4.40
         1 MiB        11.84         L3   (6 MiB)
         4 MiB        16.00
        16 MiB       107.68         DRAM
        64 MiB       141.94
       256 MiB       141.44
```

**L1 to DRAM: 95×.**

**Part A — the stride:**

```
    stride   bytes   ns/element
         1       4         1.09
         2       8         1.08
         4      16         2.01
         8      32         4.15
        16      64         6.33
        32     128        14.52
        64     256        14.50
```

**Part B — the ceilings:**

| | GB/s |
| --- | --- |
| one accumulator (the wrong version) | **6.28** |
| eight accumulators | **13.71** |

arithmetic peak **13.50 GFLOP/s**, ridge point **0.98 flops/byte**.

**Part C — the kernels:**

```
  kernel                 AI      GFLOP/s         GB/s  % of roof
  sum (1 acc)         0.125         0.77         6.17        45%
  axpy                0.083         1.13        13.55        99%
  copy                0.000         0.00        10.78          -
  poly(deg 16)        4.000         2.47         0.62        18%
  poly4(deg 16)       4.000         7.14         1.79        53%
  poly(deg 64)       16.000         2.59         0.16        19%
  poly4(deg 64)      16.000         7.08         0.44        52%
```

**With the wrong 6.28 GB/s ceiling, `axpy` reads 222% and `sum` reads 98%** — and the 222% is what should send them back.

**Part D(b):**

| | 64 MiB | 16 KiB |
| --- | --- | --- |
| `-O2` | 8.37 GB/s | 9.68 GB/s |
| `-O3` | **14.53 GB/s** | **46.28 GB/s** |

---

## 4. Answers

**Q1 — the hierarchy.**

Four plateaus at roughly 1.5 / 3–4 / 12–16 / 140 ns, changing at **32 KiB, 256 KiB and ~6 MiB** — which `lscpu` reports as L1d, L2 and L3. **Ratio L1 to DRAM ≈ 95×.**

Accept any machine's numbers; the marks are for the steps landing on the reported cache sizes and for computing the ratio.

**Q2 — one accumulator against eight.**

**6.28 GB/s against 13.71.** A single `s += a[i]` is a **dependency chain**: each addition waits for the previous one's result, so the loop runs at one add per FP-add latency (about 4 cycles) regardless of how fast memory is. It measures **floating-point add latency**, not bandwidth.

Eight independent accumulators let the machine keep eight additions in flight, so the loop becomes limited by the thing you meant to measure.

**Full marks require "it is measuring latency, not bandwidth"** in some form. "It's slower because of the dependency" is [3 of 5] — push for what the number then *is*.

**Q3 — where the stride table flattens.**

At **stride 32, i.e. 128 bytes**, not 64. The cache line is 64 bytes, so from stride 16 onward every access is already a separate line — but up to about 128 bytes the **hardware prefetcher** still recognises the pattern and fetches ahead, so some of the latency is hidden. Past that it stops trying and every access pays a full miss, which is why 32 and 64 are identical at 14.5 ns.

A student who says "the cache line is 128 bytes" has the wrong answer for a plausible reason; send them to `getconf LEVEL1_DCACHE_LINESIZE`, which says 64.

**Q4 — `axpy` at 99%.**

**Two that would help:** move less data — use `float` instead of `double` and halve the bytes; or **fuse** it with the loop that produced or consumes the array, so the data is touched once instead of twice. Accept also non-temporal stores, which skip the read-for-ownership of `b`.

**One that would not:** anything that makes the *arithmetic* faster — vectorising it further, using FMA, unrolling. It is at the memory roof, and the arithmetic is already free.

**Q5 — `poly` against `poly4`.**

An FMA has a **latency** of about 4 cycles and a **throughput** of about 2 per cycle. A single dependency chain issues one FMA every 4 cycles and leaves seven eighths of the capacity idle; four independent chains keep four in flight and get about 3× more. Same flops, same bytes, same arithmetic intensity — **the roofline cannot see the difference.**

**Q6 — roofline against profiler.** Two sentences, and any correct pair:

- The roofline tells you **what the machine could do for this algorithm**, so it tells you whether a hot loop is worth optimising at all and which resource to attack. A profiler cannot: it says where the time went, not whether that was reasonable.
- A profiler tells you **which code is hot**, which the roofline has no idea about — it is a model of a kernel you have already chosen.

**Q7 — removing `KEEP`.**

Bandwidth in the hundreds or thousands of GB/s, or a division by a zero elapsed time. `objdump` shows the loop body gone entirely.

Why an impossible number is more useful: **because you notice it.** A benchmark that is wrong by 2× reports a plausible figure and gets believed; one that is wrong by 1000× cannot be. The general defence is to have a model of what the answer should be — which is what the roofline provides.

**Q8 — `-O3` against the ceiling.**

The `-O3` 64 MiB figure (**14.53 GB/s**) is essentially the measured bandwidth ceiling (13.71 — the small excess is run-to-run variation and the L3 fraction of a 64 MiB buffer). **So `-O3` is at the memory roof and `-O2` was not**, and the reason is exactly Q2's: the scalar loop is a single dependency chain, and **the vectoriser's first act is to split the reduction into several accumulators.**

The 16 KiB gap is much larger (4.8× against 1.74×) because at that size there is no memory bottleneck to hide behind — the loop is purely compute, so the full width of the SIMD unit shows up.

---

## 5. Checkoff

The four boxes are in the lab sheet. In practice:

- **The second box is the lab.** Insist on seeing both numbers and the >100% row. A student who went straight to eight accumulators because a friend told them has not done Part B.
- **The roofline sketch on paper**, with all seven points and the ridge. It takes two minutes and it is the thing they will remember in a year.
- Q5's two FMA numbers should be looked up, not guessed — Agner Fog's tables, or the Intel optimisation manual.

**Timing.** Setup 5, Part A 20, Part B 35, Part C 25, Part D 15 — 100 against 110. **Part D(a) can be demonstrated from the front** if the room is behind, but Part D(b)'s four numbers should be theirs, because Q8 is the best question on the sheet.

---

*PROG 201 · Week 9 · Lab 9 Solutions · Instructor Only · © CSE Department*
