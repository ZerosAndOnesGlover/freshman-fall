# CS 201 · Problem Set 10
## Parallelism, Coherence, and the GPU

---

**Released:** Week 10, Wednesday · **Due:** Week 11, Friday 17:00
**Total: 100 points** · Submit one PDF plus a `.zip` of source, `PS10_{LastName}_{StudentID}.pdf`

> Q1 and Q4 are analysis; Q2 and Q3 want measurements from your own machine. **The GPU questions
> (Q5) are conceptual — no GPU is required or expected.**

---

### Q1: Coherence (22 points)

**(a) [6]** Give the four MESI states and, for each, say who else may hold the line and whether this cache may write it without further action.

**(b) [4]** Two cores hold `x` in **S**. Core 0 writes `x`, then Core 1 reads `x`, then Core 1 writes `x`. Give the MESI state of each core's line after every step.

**(c) [4]** A single shared atomic counter measured **64 M ops/s on one thread and ~20 M across two** *(reference)*. Explain why aggregate throughput *fell*, in terms of what must be true of the line's state to write it.

**(d) [4]** A colleague proposes to fix (c) with a faster atomic instruction. Explain why that cannot work, and give the design that does.

**(e) [4]** Distinguish **coherence** from **consistency**. Give the store-load example and explain why `r1 == 0 && r2 == 0` can occur on x86-64 despite coherence.

---

### Q2: Scaling, Measured (20 points)

Build the `sqrt`-reduction from Lab 10 Part 2 — private partials, no sharing.

**(a) [6]** Report time, speedup and efficiency at 1, 2, 4, 8 threads. Reference *(verified)*: 3.90× at 4 threads (97%), 3.59× at 8 (45%).

**(b) [5]** Scaling **reverses** past the physical core count. Explain, distinguishing physical cores from hyperthreads, and say what kind of workload hyperthreading *does* help.

**(c) [4]** Efficiency at 4 threads is 97%, not 100%. Name two sources of the missing few percent.

**(d) [5]** Apply Amdahl's Law: if this workload were 98% parallel, what is the maximum speedup on infinite cores? On 4 cores? Compare with your measured 4-thread figure and comment.

---

### Q3: False Sharing (22 points)

Build the packed-vs-padded counter benchmark from Lab 10 Part 4, four threads pinned to the four physical cores.

**(a) [6]** Print the addresses of the four packed counters and the four padded counters. Show that the packed set shares a 64-byte line and the padded set does not.

**(b) [6]** Report both timings. Reference *(verified)*: **0.84 s packed vs 0.46 s padded — 1.45×.** Explain why the packed version is slower when no thread touches another's counter.

**(c) [4]** Fix it with `alignas(64)` (or padding) and confirm the speedup returns. State how many bytes of padding each counter needs and why.

**(d) [6]** The measured cost here is 1.45×. **Predict, with reasoning, whether it would be larger or smaller on a 32-core server**, and explain why false sharing is "the classic reason a program that scaled to 4 cores collapses at 32".

---

### Q4: The Design (16 points)

**(a) [6]** Rewrite this contended counter as a scalable design. State how many cross-core cache-line transfers your version performs per thread during the hot loop.

```c
atomic_long total = 0;
void *count_events(void *ranges) {
    for (each event in my range) atomic_fetch_add(&total, 1);
    return NULL;
}
```

**(b) [4]** Your fix uses per-thread partials combined at the end. Name the two earlier ideas in this course it generalises (one from Week 5, one the general pattern).

**(c) [3]** A large array is initialised by one thread, then processed by 16 threads across 2 NUMA nodes, and runs slower than expected. Diagnose it and give the fix.

**(d) [3]** State the "first touch" rule and why it makes the bug in (c) happen.

---

### Q5: The GPU (20 points)

**(a) [4]** A CPU has 4 fast cores; a GPU has 2000 slow ones. For each workload, say which wins and why: summing a billion floats; walking a linked list; multiplying two 4096×4096 matrices; parsing JSON.

**(b) [4]** Explain **SIMT** and the warp. How does it differ from both SIMD (Week 5) and independent multi-threading (L31)?

**(c) [4]** A warp hits `if (threadIdx.x < 16) A(); else B();`. Explain **warp divergence** and its cost. Why is the GPU advice ("remove branches") the opposite of the CPU advice from Week 5 ("make branches predictable")?

**(d) [4]** `data[threadIdx.x]` coalesces into one memory transaction; `data[threadIdx.x * 8]` does not. Explain, and relate it to the 64-byte cache line of Week 4.

**(e) [4]** Vector add (`c[i] = a[i] + b[i]`) is *slower* on a GPU than a CPU once the PCIe transfer is counted, but matrix multiply is far faster. Explain using **arithmetic intensity** (flops per byte moved), and connect it to Week 5's roofline idea.

---

## Marks

| | |
|---|---:|
| Q1 Coherence | 22 |
| Q2 Scaling, Measured | 20 |
| Q3 False Sharing | 22 |
| Q4 The Design | 16 |
| Q5 The GPU | 20 |
| **Total** | **100** |

---

*CS 201 · Week 10 · Problem Set 10*
