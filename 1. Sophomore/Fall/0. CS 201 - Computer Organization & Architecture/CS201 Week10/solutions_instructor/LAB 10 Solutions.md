# CS 201 · Lab 10 — Solutions and TA Notes
## Instructor Only

---

> **Unmarked.** Five checkpoints. CPU figures verified on the lab image; **the GPU part is a reading
> exercise — no compilation, no GPU.**

---

## Before the Session

**Say the GPU situation plainly.** No `nvcc`, no `nvidia-smi` *(verified)*. The lab does the reduction on the CPU and reads the CUDA version in Part 5. **The structure is identical — partition, private partials, combine — and that is the transferable content.** The exam and CS 202 expect students to *read* a GPU reduction, which Part 5 delivers; they do not need to have run one.

**Midterm 2 is this evening.** Expect a distracted room; Parts 3 and 4 (contention, false sharing) are the ones to protect, since they are also Q1/Q3 of the paper.

---

## Timing

| Part | Budget | Reality |
|---|---|---|
| 1 — topology | 10 min | 5 min |
| 2 — scaling | 25 min | 20 min |
| 3 — contention | 20 min | 20 min |
| 4 — **false sharing** | 25 min | **Protect this** |
| 5 — GPU reading | 15 min | 15 min |

---

## Part 1

*(Verified: 8 CPUs, 2 threads/core, 4 cores, 1 NUMA node.)*

1. **Four** can do independent arithmetic at once — the physical cores. The "8" counts hyperthreads, which share each core's execution units.
2. On two sockets there would be two NUMA nodes, and Part 2's array placement would matter (first-touch); remote accesses would cost ~1.5–2×.

**✅ CHECKPOINT 1**

---

## Part 2

*(Verified table: 3.90× at 4 threads (97%), 3.59× at 8 (45%).)*

1. **Scaling reverses past 4 threads because there are 4 physical cores**; threads 5–8 contend for shared execution units on the hyperthreads and add overhead without throughput.
2. **Private partials mean no shared writes in the hot loop** — each thread touches only its own memory, so no cache line bounces. A shared accumulator (Part 3) serialises on one line.
3. Any of: thread create/join overhead, load imbalance, shared-LLC/bandwidth contention, the serial combine.

**✅ CHECKPOINT 2**

---

## Part 3

*(Verified: 64.2 M ops/s at 1 thread, ~20 M at 2+.)*

**Let the throughput column land before explaining.** "Adding a core made it 3× slower" is the sentence to put on the board.

1. **To write the counter the line must be M (sole, dirty copy).** Every increment from a different core forces an invalidate of the others and a transfer of the line — hundreds of cycles of interconnect latency per few-cycle atomic. The threads serialise on line ownership.
2. **No faster atomic helps** — the cost is the line transfer, not the instruction.
3. Per-thread partials, combined once; **zero cross-core transfers in the hot loop** if the accumulator is a register/thread-local (not a per-thread array slot that itself shares a line).

**✅ CHECKPOINT 3**

---

## Part 4 — the important one

*(Verified: packed span 24 B / same line; padded span 192 B; 0.84 s vs 0.46 s = 1.45×.)*

### 4.1

Students must **print the addresses** and see the four packed counters 8 bytes apart within one 64-byte line. This is the unprivileged substitute for `perf c2c`, which needs the perf permissions the machine lacks.

### 4.2

1. **The 64-byte line is the unit of coherence, not the variable.** A write to `packed[0]` invalidates the whole line, including `packed[1..3]` in other cores' caches.
2. `alignas(64)` on each counter.
3. **Larger on 32 cores** — more writers contending for one bouncing line; the effect grows with core count, which is why 4-core-clean code collapses at 32.
4. **Week 4's cache line.**

> **The pedagogical arc of Parts 3–4:** Part 3 is contention you can *see* (shared variable); Part 4
> is contention you cannot (separate variables, shared line). Students who leave understanding that
> the second exists — and that it is invisible in the source — have the week's main lesson.

**✅ CHECKPOINT 4**

---

## Part 5 — GPU reading

**Answers:**

1. `if (tid == 0) out[blockIdx.x] = sdata[0]` — the per-block partial, corresponding to `parts[id] = s`.
2. **The threads in a block cooperate through shared memory** (`sdata`), so they must synchronise before reading what their neighbours wrote; the CPU threads were fully independent and combined only at the end, needing no barrier mid-loop.
3. `if (tid < s)` idles half the threads each iteration — **warp divergence**, but here it is **largely unavoidable and standard** for a tree reduction; the divergence is coarse (whole halves of the warp) and the alternative algorithms trade it for other costs.
4. `sdata[tid] += sdata[tid + s]` on **shared memory**; the coalescing/ bank-conflict concern is the shared-memory analogue of Week 4's line — adjacent access is what the hardware serves efficiently.

> Accept reasonable answers; the point is that they can *map* GPU code to the CPU reduction they
> wrote, not that they know CUDA idioms cold.

**✅ CHECKPOINT 5**

---

## What Success Looks Like

1. Distinguish physical cores from hyperthreads and predict where scaling stops.
2. Explain negative scaling of a shared counter via MESI.
3. **Recognise false sharing from addresses alone, and fix it with alignment.**
4. Read a GPU reduction and map it onto the CPU version.

Item 3 is the one that separates this from "threads are good". It is Q3 of the problem set and Q1 of the midterm's descendant topics.

---

*CS 201 · Week 10 · Lab 10 Solutions · Instructor Only*
