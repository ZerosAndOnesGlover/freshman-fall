# CS 201 · Computer Organization & Architecture
## Week 10 · Lecture 2 of 3
### False Sharing, NUMA, and Writing Code That Scales

---

**Reading:** CS:APP §6.6, Patterson & Hennessy §5.10, §6.5 · **Previous:** L31, MESI

---

## 1. The Sharing You Did Not Know You Had

L31's shared counter was *obviously* shared — every thread wrote the same variable. **False sharing is the same pathology with no shared variable at all.**

```c

struct { long v; } counter[4];        /* one per thread, no sharing... right? */
```

Four separate counters, one per thread. No thread touches another's. **And yet** — because MESI works on **64-byte cache lines**, not on variables — all four 8-byte counters land in the same line:

```
packed[0..3] span 24 bytes -> SAME 64-byte line
```

*(Verified — four `long`s at 24 bytes apart are one cache line.)*

**So when thread 0 writes `counter[0]`, it invalidates the line in thread 1's cache — which holds `counter[1]`.** The threads share nothing logically and everything physically. Every write bounces the line, exactly as if they had shared one variable.

---

## 2. Measured, and Fixed with 56 Bytes of Padding

The same four counters, packed into one line versus padded onto four separate lines:

```c
struct { volatile long v; }              packed[4];   /* 24 bytes apart — 1 line */
struct { volatile long v; char pad[56]; } padded[4];  /* 64 bytes apart — 4 lines */
```

```
packed addrs span 24 bytes  -> SAME 64B line
padded addrs span 192 bytes -> 3 lines apart

packed  (false sharing): 0.84 s
padded  (no sharing):    0.46 s
false sharing cost: 1.45x slower
```

*(Measured, 4 threads pinned to the 4 physical cores.)*

**A 1.45× slowdown from a struct layout, fixed by 56 bytes of padding.** The computation is identical; only the addresses changed.

> **On this 4-core mobile chip the effect is 1.45×. On a 32- or 64-core server it is routinely 5–10×**,
> because more cores means more invalidations contending for the one bouncing line. **False sharing is
> the classic reason a program that scaled fine to 4 cores collapses at 32** — and it is invisible in
> the source, invisible in the algorithm, and invisible in Big-O. It lives entirely in the 64-byte
> line, which is Week 4's unit reappearing to bite a program Week 4 never considered.

**How to find it:** `perf c2c` (cache-to-cache) reports lines that bounce between cores, naming the source lines involved. **How to fix it:** pad hot per-thread data to a cache line (`alignas(64)` in C11), or give each thread genuinely separate allocations.

---

## 3. NUMA: Not All Memory Is Equidistant

On a single-socket machine, every core reaches DRAM at the same cost. **On a multi-socket machine it does not.**

```
   Socket 0                    Socket 1
   ┌─────────┐   interconnect  ┌─────────┐
   │ cores   │◀───────────────▶│ cores   │
   │ + DRAM0 │                 │ + DRAM1 │
   └─────────┘                 └─────────┘
```

Each socket has its own memory controller and its own attached DRAM. **A core reading its *local* DRAM is fast; reading the *other* socket's DRAM goes across the interconnect** and costs perhaps 1.5–2× the latency. This is **Non-Uniform Memory Access**.

**The lab machine is single-socket** — one NUMA node, `NUMA node0 CPU(s): 0-7` *(verified)* — so this cannot be measured here, and the figures are cited. But the principle governs every server you will deploy on:

**The rule is "first touch".** Linux allocates a page on the NUMA node of the core that *first writes* it, not the core that called `malloc`. So the thread that initialises data should be the thread that later uses it. **A common bug: one thread initialises a large array (all pages land on its node), then a pool of threads processes it (half of them now make remote accesses).** The fix is to parallelise the *initialisation* with the same partitioning as the computation.

> **NUMA is Week 4's memory hierarchy with one more level, and the same lesson: locality is
> everything, and the hardware places data by rules you must know.** `numactl` and `numastat`
> control and report it; CS 202 next semester goes into the kernel side.

---

## 4. The Ceiling: Amdahl, Measured

Even with no false sharing and perfect locality, parallelism has a hard ceiling — Week 5's Amdahl's Law, now with threads instead of vector lanes.

An embarrassingly parallel workload (each thread sums `sqrt(k)` over a private range, no sharing at all):

| threads | time | speedup | efficiency |
|---:|---:|---:|---:|
| 1 | 0.184 s | 1.00× | 100% |
| 2 | 0.097 s | 1.90× | 95% |
| **4** | 0.047 s | **3.90×** | **97%** |
| 8 | 0.051 s | **3.59×** | **45%** |

*(Measured.)*

**Near-perfect scaling to 4 threads — 3.90× on 4 cores — and then it *reverses*.** Eight threads are *slower* than four.

**Why: there are four physical cores.** Threads 5–8 run on the same cores' hyperthreads (SMT), which share the physical execution units. **For compute-bound work there is nothing to share** — the FPUs are already busy — so the extra threads add scheduling overhead and contention without adding throughput. **Hyperthreading helps latency-bound work (one thread stalls on memory while the other computes); it does little for compute-bound work.**

> **Two ceilings, both real.** Amdahl caps you at $1/(1-p)$ no matter how many cores; and *physical*
> cores, not logical threads, are what deliver compute throughput. **A machine reporting "8 CPUs" has
> 4 that can do independent arithmetic at once.** Knowing the difference is the gap between a
> benchmark that scales and one that mysteriously plateaus at 4.

---

## 5. How to Write Multi-Core Code That Scales

The whole week reduces to four rules, and they are all about *not sharing*:

| Rule | Because |
|---|---|
| **Share nothing you can avoid sharing** | Every shared write is an invalidate (L31) |
| **Give each thread its own cache line** for hot data | Or false sharing bounces it (§2) |
| **Reduce, don't contend** | Per-thread partial results combined at the end beat one shared accumulator — Week 5's multiple-accumulators idea, across cores |
| **Respect locality: physical cores and NUMA nodes** | Logical threads and remote memory do not deliver what they appear to (§3–§4) |

**The design pattern is always the same: partition the work, give each partition private state, and combine at the very end.** The atomic counter of L31 becomes an array of per-thread counters summed once at the finish — no sharing during the hot loop, one cheap combine after. **This is map-reduce at the level of a single machine, and it is why it scales when a shared counter does not.**

---

## 6. What to Take Away

1. **False sharing is contention with no shared variable** — the 64-byte line is the unit, not the variable.
2. **Four per-thread counters in one line cost 1.45× here, and 5–10× on a big server.** Fixed by padding to a line.
3. **`perf c2c` finds it; `alignas(64)` fixes it.**
4. **NUMA makes remote memory 1.5–2× slower**; "first touch" places a page on the writing core's node.
5. **Amdahl caps parallel speedup**, and **physical cores, not threads, deliver compute throughput** — 8 threads were slower than 4 here.
6. **Scale by not sharing:** partition, give each partition private state, combine once at the end.

---

## Exercises

1. Four `long` counters are 24 bytes apart and share a line. How much padding makes each its own line here, and what C11 feature expresses it cleanly?
2. False sharing cost 1.45× on 4 cores. Explain why the same code would cost *more* on 32 cores, not less.
3. A program initialises a 4 GB array in one thread, then processes it with 16 threads across 2 sockets. Explain the NUMA bug and the fix.
4. The `sqrt` workload scaled to 3.90× at 4 threads and *fell* to 3.59× at 8. Explain, distinguishing physical cores from hyperthreads.
5. Give a workload where hyperthreading *does* help, and say why it differs from the `sqrt` case.
6. Rewrite L31's single shared atomic counter as a scalable design, and say how many cache-line transfers your version does per thread during the hot loop.

---

*Next: L33 — the GPU, a different answer to the same parallelism question.*
