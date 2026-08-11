# CS 201 · Week 10 · Reading Guide
## Multi-Core, Coherence, and the GPU

---

**Set reading:** Patterson & Hennessy, *Computer Organization and Design*, **§5.10** (coherence) and **§6.1–6.7** (parallel processors and the GPU). CS:APP has no coherence chapter — this is where the RISC-V book earns its place on the reading list.
**Also:** the CUDA C Programming Guide, **§1–3**, read for the model not the API.
**Optional:** Sorin, Hill & Wood, *A Primer on Memory Consistency and Cache Coherence* (free) — the definitive treatment.

---

## Why the Textbook Changes This Week

**CS:APP is a single-core book.** It covers caches (Chapter 6) beautifully and stops at one core. **Coherence, consistency and the GPU are Patterson & Hennessy's territory**, and this is the week to read the other book.

**Read P&H §5.10 for coherence and §6 for parallelism**, and take the memory-consistency material from L31 §5 — both textbooks treat it lightly, and it is the part that makes concurrency genuinely hard.

---

## Section by Section (Patterson & Hennessy)

| § | Topic | What to take from it |
|---|---|---|
| **5.10** | **Cache coherence** | MESI (the book may use MSI/MESI variants), the snooping protocol, invalidation |
| **6.1** | Introduction | The multicore/throughput motivation — Week 0's power wall, revisited |
| **6.2** | The difficulty of parallelism | **Amdahl again**, and why parallel programming is hard |
| **6.3** | SISD, MIMD, SIMD, SPMD | The taxonomy. SIMD is Week 5; this places it |
| **6.4** | Hardware multithreading | **Hyperthreading** — why 8 "CPUs" are 4 cores (Lab 10 Part 2) |
| **6.5** | Multicore and shared memory | The coherence problem at scale |
| **6.6** | **GPUs** | SIMT, warps, the memory model — L33 |
| **6.7** | Clusters and message passing | Beyond one machine; background for now |

---

## Questions to Read Against

**On §5.10 — coherence**

1. State the coherence invariant: what must be true of every core's view of a single location?
2. Trace MESI for: two cores share `x` (both S); Core 0 writes; Core 1 reads; Core 1 writes. Give every state.
3. Why is a *read*-heavy shared workload cheap under MESI but a *write*-heavy one expensive? Which state permits cheap sharing?
4. A single shared counter scaled *negatively* (Lab 10 Part 3). Explain from the protocol, not from "contention".

**On §6.2, §6.4 — the ceilings**

5. Restate Amdahl's Law from Week 5. For a 95%-parallel program, the maximum speedup and the speedup on 8 cores?
6. §6.4 covers hardware multithreading. Why did the `sqrt` workload (Lab 10 Part 2) get *slower* at 8 threads on a 4-core machine, and what workload would benefit instead?

**On §6.6 — the GPU**

7. Explain SIMT and the warp. How does a warp differ from a SIMD vector, and from independent threads?
8. What is warp divergence, and why does it make GPU branch advice the *opposite* of CPU branch advice (Week 5)?
9. Coalesced vs uncoalesced access — relate it to Week 4's cache line. Which access pattern does a GPU want from a warp?
10. Vector add loses to the CPU on a GPU; matrix multiply wins hugely. Explain with arithmetic intensity and Week 5's roofline.

**Beyond the textbooks**

11. Distinguish coherence from consistency. Why can `r1==0 && r2==0` happen on x86-64 in the store-load example?
12. False sharing (Lab 10 Part 4) involves no shared variable. Explain how it happens and why the fix is padding.

> **Question 11 is the hard one and the one worth the most.** Coherence is a hardware guarantee;
> consistency is a contract you must program to. Most concurrency bugs that survive testing are
> consistency bugs.

---

## Reading Against the Machine

```bash
# 1. Your topology — physical cores vs threads
lscpu | grep -E "Core|Thread|NUMA" ; nproc

# 2. Scaling: the sqrt reduction (Lab 10 Part 2) at 1,2,4,8 threads
#    Predict where it stops scaling BEFORE running it.

# 3. False sharing: packed vs padded counters (Lab 10 Part 4)
#    Print the addresses and confirm the packed set shares a 64-byte line.
```

**Item 3 is the measurement of the week**, and it is invisible without printing the addresses. *(Verified: 1.45× on this 4-core machine; larger on more cores.)*

**Two honesty checks the hardware forces:**
- **No GPU** — `nvcc`/`nvidia-smi` absent — so §6.6 and L33 are conceptual and Lab 10 does the reduction on the CPU. The GPU figures in the lectures are cited.
- **One NUMA node** — so §6.5's NUMA effects cannot be measured here and those figures are cited too.

---

## Terminology You Should Own by Week 11

| | | |
|---|---|---|
| cache coherence | MESI / MSI | snooping |
| invalidate | cache-line bouncing | Modified/Exclusive/Shared/Invalid |
| memory consistency | sequential consistency | TSO |
| store-load reordering | memory fence | C11 memory order |
| false sharing | `alignas` | `perf c2c` |
| NUMA | first touch | remote access |
| hyperthreading / SMT | physical vs logical core | strong/weak scaling |
| GPU / SIMT | warp | warp divergence |
| coalesced access | arithmetic intensity | CUDA grid/block/thread |

---

## If You Want More

**Sorin, Hill & Wood, *A Primer on Memory Consistency and Cache Coherence*** (free, Morgan & Claypool) is *the* reference. **Read the first two chapters** — coherence and the consistency-vs-coherence distinction — which is L31 done rigorously.

**Preshing on Programming** (blog) has the clearest writing anywhere on memory ordering, fences and lock-free programming. **"Memory Reordering Caught in the Act"** demonstrates the store-load reordering of Q11 with runnable code — worth doing on your own machine.

**The CUDA Programming Guide** is the primary source for L33. **Read §1–3 for the model**; the rest is API reference you consult when writing GPU code, which is CS 331 (AI) and beyond.

**Herb Sutter's "The Free Lunch Is Over"** (2005) is the essay that named the shift this whole week is about — the end of automatic single-thread speedups and the turn to explicit parallelism. Short, and still the best statement of why Week 10 exists.

---

*CS 201 · Week 10 · Reading Guide*
