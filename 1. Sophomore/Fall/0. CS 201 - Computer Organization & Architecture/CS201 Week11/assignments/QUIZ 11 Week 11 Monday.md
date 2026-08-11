# CS 201 · Quiz 11
## Administered: Monday, Week 11 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 10** — cache coherence, false sharing, NUMA, and the GPU.

**Instructions:** Closed notes. 10 minutes.

> **Unmarked, no weight.** Key below. Sit it closed-book first. **This is the last quiz of the
> course** — Quiz 11 covers Week 10, and Week 12's material is examined only on the final.

---

**Q1.** Give the four MESI states. Which two permit a write with no further action?

&nbsp;

&nbsp;

---

**Q2.** A single shared atomic counter did 64 M ops/s on one thread and 20 M on two. Why did adding a core make it slower?

&nbsp;

&nbsp;

---

**Q3.** Four separate per-thread counters, one per thread, cost 1.45× when packed together. What is this called, and why does it happen with no shared variable?

&nbsp;

&nbsp;

---

**Q4.** A parallel workload scaled to 3.90× on 4 threads and fell to 3.59× at 8. Why?

&nbsp;

&nbsp;

---

**Q5.** Distinguish cache coherence from memory consistency in one sentence each.

&nbsp;

&nbsp;

---

**Q6.** On a GPU you make branches *absent*; on a CPU you make them *predictable*. Why the opposite advice?

&nbsp;

&nbsp;

---

**Q7.** Vector add loses to the CPU on a GPU, but matrix multiply wins hugely. What one property explains it?

&nbsp;

&nbsp;

---

<div style="page-break-after: always;"></div>

---

## Answer Key — Mark Your Own

**Q1.** **Modified, Exclusive, Shared, Invalid.** **M and E** permit a write with no further action — both are sole copies. Writing an **S** line requires invalidating other copies first; an **I** line requires a fetch first.

---

**Q2.** **The counter's cache line must be the sole (M/E) copy to be written**, so every increment from a different core forces an invalidate of the others and a transfer of the line across the interconnect — hundreds of cycles per few-cycle atomic. The threads serialise on line ownership; the line **bounces**.

---

**Q3.** **False sharing.** The four counters share a **64-byte cache line** — the unit of coherence is the line, not the variable — so a write to counter 0 invalidates the line in the other cores' caches even though it changed none of *their* counters. Fixed by padding each to its own line.

---

**Q4.** **There are only 4 physical cores.** Threads 5–8 run on the hyperthreads, which share physical execution units; for compute-bound work the FPUs are already busy, so the extra threads add overhead without throughput. (Hyperthreading helps latency-bound work instead.)

---

**Q5.** **Coherence** guarantees all cores agree on the value of one location. **Consistency** governs the order in which writes to *different* locations become visible — and x86-64's TSO still permits store-load reordering.

---

**Q6.** **A GPU warp has no per-thread branch predictor and executes both branch paths serially** (warp divergence), so divergent branches waste throughput and the goal is to avoid them. **A CPU has a predictor that handles a taken/not-taken pattern for ~1 cycle**, so a *predictable* branch is nearly free. Same goal (cheap branches), opposite hardware, opposite technique.

---

**Q7.** **Arithmetic intensity** — flops per byte moved. Vector add does ~0.04 flop/byte and is memory/transfer-bound, so the PCIe copy makes the GPU lose. Matrix multiply's intensity grows with $n$, so its arithmetic dwarfs the transfer and the GPU's thousands of cores win.

---

### What to Do With Your Score

| If you missed | Reread |
|---|---|
| Q1, Q2 | L31 §2–§4 |
| Q3, Q4 | L32 §2 and §4 |
| Q5 | L31 §5 |
| Q6, Q7 | L33 §3 and §4 |

**This is the course's last quiz.** Week 11's material (profiling, roofline, benchmarking) and Week 12's (frontiers) are examined only on the **final** — see the Week 12 revision guide when it appears.

---

*CS 201 · Week 11 · Quiz 11 · covers Week 10 · ungraded*
