# CS 201 · Problem Set 10 — Solutions
## Instructor Only

---

> **Not for distribution.** CPU figures measured on the lab image (i5-8250U, 4 cores / 8 threads,
> single NUMA node). **GPU and NUMA figures are cited — no GPU and one socket on this machine.**

---

## Q1 (22) — Coherence

### (a) [6] — 1 each

| State | Others hold it? | Writable without action? |
|---|---|---|
| **M** — Modified | No | **Yes** (dirty, sole copy) |
| **E** — Exclusive | No | **Yes** (clean, sole copy) |
| **S** — Shared | Maybe | **No** — must invalidate others first |
| **I** — Invalid | — | **No** — must fetch first |

### (b) [4]

| Step | Core 0 | Core 1 |
|---|---|---|
| start | S | S |
| Core 0 writes | **M** | **I** *(invalidated)* |
| Core 1 reads | **S** *(downgraded)* | **S** *(fetched from C0)* |
| Core 1 writes | **I** *(invalidated)* | **M** |

### (c) [4]

**To write the counter, a core's line must be in M or E — the sole copy.** Every increment on a different core forces an **invalidate** of all other copies and a **transfer** of the line to the writer. With one thread the line stays local; with two, it **bounces between cores on every increment**, and the interconnect latency (hundreds of cycles) dwarfs the atomic op (a few). Aggregate throughput falls because the threads are serialised on line ownership.

### (d) [4]

**A faster atomic cannot help — the cost is the line transfer, not the operation.** No instruction avoids the invalidate-and-fetch of a contended line. **The fix is to stop sharing:** per-thread partial counts, combined once at the end, so the hot loop touches only thread-local lines.

### (e) [4]

**Coherence** guarantees all cores agree on the value of *one* location; **consistency** governs the order in which writes to *different* locations become visible. Example: `x=1; r1=y` on Core 0 and `y=1; r2=x` on Core 1 can yield `r1==0 && r2==0` on x86-64, because each core's **store can be buffered** and made visible after its own later load (store-load reordering, permitted under TSO). Coherence is not violated — each location is individually consistent — but cross-location ordering is not guaranteed.

---

## Q2 (20) — Scaling, Measured

### (a) [6]

| threads | time | speedup | efficiency |
|---:|---:|---:|---:|
| 1 | 0.184 s | 1.00× | 100% |
| 2 | 0.097 s | 1.90× | 95% |
| 4 | 0.047 s | 3.90× | 97% |
| 8 | 0.051 s | 3.59× | 45% |

*(Verified.)*

### (b) [5]

**There are 4 physical cores; threads 5–8 run on hyperthreads that share physical execution units.** For compute-bound work the FPUs are already saturated, so extra threads add scheduling overhead without throughput — hence the *reversal*. **Hyperthreading helps latency-bound work**: when one thread stalls on a memory access (Week 4), its sibling can use the idle execution units.

### (c) [4]

Any two: **thread creation/join overhead**; **imperfect load balance** (N not divisible by thread count); **shared last-level cache and memory-bandwidth contention**; **the serial combine step** (Amdahl).

### (d) [5]

$$S_\infty = \frac{1}{1-0.98} = \mathbf{50\times}; \qquad S_4 = \frac{1}{0.02 + \frac{0.98}{4}} = \frac{1}{0.265} = \mathbf{3.77\times}$$

**Measured 3.90× exceeds the 98%-model's 3.77×**, which tells you this workload is *more* than 98% parallel — consistent with its being embarrassingly parallel with only a tiny serial combine. Accept any answer that computes both and compares sensibly.

---

## Q3 (22) — False Sharing

### (a) [6]

*(Verified.)* Packed: four counters 8 bytes apart, spanning 24 bytes — **one 64-byte line**. Padded: 64 bytes apart, spanning 192 — **four separate lines**. Award for showing the addresses and the span, not just asserting.

### (b) [6]

**0.84 s packed vs 0.46 s padded — 1.45×** *(verified)*. **The packed counters share a cache line, so MESI treats a write to any one as a write to the whole line**: thread 0's increment invalidates the line in the caches of threads 1–3, even though it changed none of their counters. The line bounces exactly as if the variable were shared. **The unit of coherence is the 64-byte line, not the variable.**

### (c) [4]

`alignas(64)` on each counter (or 56 bytes of trailing padding) puts each on its own line. **Each `long` needs to be padded from 8 to 64 bytes** so that no two counters share a line — the padding is one cache line minus the counter's own size.

### (d) [6]

**Larger on 32 cores.** More cores writing the same line means more invalidations per unit time contending for a single line that can only be owned by one core at once — the bouncing rate rises with core count. **A program with false sharing scales to 4 cores because the contention is mild, then collapses at 32** because the one bouncing line becomes a hard serialisation point that every core fights over. **The bug is invisible in the source and in Big-O; it lives entirely in the 64-byte line.**

---

## Q4 (16) — The Design

### (a) [6]

```c
static long partial[NTHREADS];   /* ideally each alignas(64) to avoid false sharing */
void *count_events(void *arg) {
    long id = ((args*)arg)->id, local = 0;
    for (each event in my range) local++;    /* thread-local, in a register */
    partial[id] = local;                     /* one write at the end */
    return NULL;
}
/* main: total = sum of partial[] */
```

**Cross-core transfers per thread in the hot loop: zero.** `local` lives in a register; nothing shared is touched until the single write at the end. *(Award full only if the answer states "zero" and keeps the accumulation thread-local — a per-thread slot updated every iteration still false-shares if the slots share a line.)*

### (b) [4]

**Week 5's multiple accumulators** (breaking a dependency/contention chain into independent ones) and **the general partition-private-combine / map-reduce pattern.**

### (c) [3]

**NUMA first-touch bug:** the initialising thread's node gets all the pages, so half the processing threads (on the other socket) make **remote** memory accesses at ~1.5–2× latency. **Fix: parallelise the initialisation with the same partitioning as the computation**, so each thread first-touches the pages it will later process.

### (d) [3]

**First touch:** Linux allocates a physical page on the NUMA node of the core that *first writes* it, not the one that called `malloc`. So a single-threaded initialisation places every page on one node, stranding the other socket's threads with remote accesses.

---

## Q5 (20) — The GPU

### (a) [4] — 1 each

- **Sum a billion floats:** GPU — regular, massively parallel, high throughput. *(Borderline if transfer-bound; accept with that caveat.)*
- **Walk a linked list:** CPU — pointer-chasing is serial and irregular; the GPU's parallelism is useless.
- **4096×4096 matrix multiply:** GPU — $O(n^3)$ work on $O(n^2)$ data, high arithmetic intensity.
- **Parse JSON:** CPU — branchy, serial, irregular.

### (b) [4]

**SIMT: threads grouped into warps of 32 that execute one instruction in lockstep, each on its own data.** Unlike **SIMD** (one thread, explicit vector lanes) it is *programmed* as independent threads with their own indices; unlike **independent multi-threading** (L31) the threads in a warp are not independent — they share one instruction stream and diverging costs performance.

### (c) [4]

**Warp divergence:** when threads in a warp take different branch paths, the warp executes **both** paths serially, masking off the inactive threads in each — so a divergent branch can halve throughput. **On a CPU you make branches predictable** (the predictor handles a taken/not-taken pattern cheaply); **on a GPU there is no per-thread predictor and both paths run**, so you make branches *absent or uniform across the warp*. Same goal, opposite technique, because the hardware is opposite.

### (d) [4]

**Coalescing:** the memory system services a warp reading contiguous addresses in one wide transaction. `data[threadIdx.x]` gives consecutive addresses → one transaction; `data[threadIdx.x * 8]` scatters them → up to 32 transactions. **This is Week 4's 64-byte cache line at GPU scale** — using a whole wide fetch versus one useful element per fetch.

### (e) [4]

**Vector add does 1 flop per 3 words moved (2 loads + 1 store) — arithmetic intensity ~0.08 flop/byte**, so it is transfer-bound, and the PCIe copy makes the GPU lose to the CPU. **Matrix multiply does $O(n^3)$ flops on $O(n^2)$ data — intensity grows with $n$**, so the arithmetic dwarfs the transfer and the GPU wins hugely. **This is Week 5's roofline: below a threshold intensity you are bandwidth-bound and more compute units do nothing.**

---

## Mark Summary

| | |
|---|---:|
| Q1 | 22 |
| Q2 | 20 |
| Q3 | 22 |
| Q4 | 16 |
| Q5 | 20 |
| **Total** | **100** |

**Where the class loses marks, in order:**

1. **Q4(a)** — a per-thread slot updated every iteration that itself false-shares; the fix must keep the accumulator thread-local (a register), not merely per-thread.
2. **Q1(c)** — "the atomic is slow" instead of "the line transfer is slow".
3. **Q3(d)** — predicting false sharing gets *better* on more cores.
4. **Q2(b)** — not distinguishing physical cores from hyperthreads.
5. **Q5(c)** — not noticing the GPU branch advice is the *opposite* of the CPU's.

---

*CS 201 · Week 10 · PS 10 Solutions · Instructor Only*
