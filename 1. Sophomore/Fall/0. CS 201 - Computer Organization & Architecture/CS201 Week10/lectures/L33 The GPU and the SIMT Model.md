# CS 201 · Computer Organization & Architecture
## Week 10 · Lecture 3 of 3
### The GPU and the SIMT Model

*“Think of it! With VLSI we can pack 100 ENIACS in 1 sq. cm.”* — Alan Perlis, "Epigrams on Programming" (1982), #109

---

**Reading:** Patterson & Hennessy §6.6, CUDA C Programming Guide §1–3 · **Previous:** L32, false sharing and NUMA

**Coursework:** 📝 **PS 9** due today 17:00 · 📊 **Quiz 11** Mon of Week 11 · 🔬 **Lab 10** Tue of Week 11 15:00–16:50 · 📝 **PS 11** released Wed of Week 11, due Fri of Week 12 17:00

---

## A Note on Hardware

**The lab machines have no GPU** — `nvidia-smi` is absent and there is no `nvcc` *(verified)*. So this lecture is conceptual, and **Lab 10 runs its parallel reduction on the CPU with the CUDA mapping documented alongside**, which is how you should read every code figure here: as the *shape* of a GPU program, verified against a CPU reference, not as something compiled on this machine. Where a number appears, it is cited from published figures and says so.

---

## 1. A Different Answer to the Same Question

Week 5 (SIMD), the first half of this week (multi-core), and now the GPU are three answers to one question: **how do you do many operations at once?**

| Approach | Parallelism | Best for |
|---|---|---|
| **SIMD** (Week 5) | One core, 8 lanes, one instruction | Tight numeric loops |
| **Multi-core** (L31–32) | A few powerful cores, independent instructions | General parallel work |
| **GPU** | **Thousands** of weak cores, one instruction across all | Massive data parallelism |

**A CPU is optimised for latency** — finish one thread's work as fast as possible, with big caches, deep out-of-order execution and branch prediction (Weeks 4–5) spent on making a single stream fast.

**A GPU is optimised for throughput** — finish an enormous amount of work per unit time, and it does not care how long any one item takes. It spends its transistors on *arithmetic units* instead of caches and control logic: a modern GPU has thousands of simple cores where a CPU has a handful of complex ones.

> **This is the post-Moore specialisation of Week 0 §L03 made concrete.** When you cannot make one
> core much faster, you build a different machine for the workloads that are massively parallel — and
> matrix multiply, the core of every neural network, is exactly that workload.

---

## 2. SIMT: Single Instruction, Multiple Threads

The GPU's execution model is **SIMT**, and it sits between SIMD and multi-threading.

- Threads are grouped into **warps** of 32 (NVIDIA) or 64 (AMD).
- **All threads in a warp execute the same instruction at the same time**, each on its own data — like SIMD lanes.
- But each thread has its own registers and its own program counter conceptually, so they are *programmed* as independent threads.

**The CUDA hierarchy:**

```
grid                   the whole launch
 └─ blocks             scheduled onto the GPU's multiprocessors
     └─ warps          32 threads, executed in lockstep
         └─ threads    one data element each
```

You write code for **one thread** and launch millions of them:

```cuda
__global__ void add(float *c, const float *a, const float *b, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;   // this thread's element
    if (i < n) c[i] = a[i] + b[i];
}
// launch: add<<<blocks, threads_per_block>>>(c, a, b, n);
```

**Every thread runs the same body; `threadIdx` tells it which element it owns.** This is the whole programming model, and it is why the GPU suits array operations so naturally — one thread per element.

---

## 3. The Two Things That Wreck GPU Performance

### Warp divergence

All 32 threads in a warp share one instruction stream. **A branch that sends some threads one way and some the other cannot run both at once** — the warp executes *both* paths, with the inactive threads masked off in each.

```cuda
if (threadIdx.x % 2 == 0) heavy_A();   // half the warp idles during A
else                       heavy_B();   // the other half idles during B
```

**A divergent branch can halve throughput, or worse.** The lesson is the opposite of a CPU's: on a CPU you make branches *predictable* (Week 5); on a GPU you try to make them *absent*, or at least uniform across a warp. This is Week 5's branch lecture with a completely different conclusion, because the hardware is completely different.

### Uncoalesced memory access

The GPU's memory system is built for warps that read **contiguous** addresses — thread 0 reads element 0, thread 1 element 1, and the hardware services all 32 in **one** wide transaction.

**If the accesses are scattered, it needs up to 32 separate transactions** — Week 4's cache-line lesson at GPU scale. `data[threadIdx.x]` coalesces; `data[threadIdx.x * stride]` does not. **Memory-access pattern is the single biggest determinant of GPU performance**, exactly as it was for the CPU cache — the same lesson, larger stakes.

---

## 4. The Cost of Getting There

The GPU is across the PCIe bus, and that is its Achilles' heel.

```
CPU DRAM  ──── PCIe (~16 GB/s, and a real latency) ────  GPU DRAM
```

**Data must be copied to the GPU, computed on, and copied back.** For the computation to pay, it must do enough arithmetic to dwarf the transfer:

$$\text{worth it if } \frac{\text{compute time}}{\text{transfer time}} \gg 1$$

**This is Week 5's roofline / operational-intensity idea in a new setting.** Adding two vectors (`c[i] = a[i] + b[i]`) does **one** flop per **three** memory words moved — it is hopelessly transfer-bound, and doing it on the GPU is *slower* than the CPU once the copy is counted. **Matrix multiply does $O(n^3)$ work on $O(n^2)$ data** — the arithmetic dwarfs the transfer, and that is why GPUs dominate deep learning and not vector addition.

> **The rule is the same one the whole course has taught: know your bottleneck.** A GPU is a compute
> machine on the far side of a slow pipe. It wins only when the compute-to-data ratio is high enough
> to hide the pipe — which is exactly the compute-bound-versus-memory-bound distinction Week 5's AVX
> sweep measured, now with a PCIe bus in the middle.

---

## 5. Where GPUs Win, and Where They Do Not

| Wins | Loses |
|---|---|
| Matrix multiply, convolution (deep learning) | Pointer-chasing, irregular structures |
| Dense linear algebra | Heavily branchy, divergent code |
| Image and video processing | Small problems (transfer dominates) |
| Monte Carlo, N-body simulation | Latency-sensitive, serial tasks |
| Anything with high arithmetic intensity and regular access | Anything with a hard serial dependency |

**The winning workloads are all high arithmetic intensity, regular access, and little divergence** — and they are exactly the workloads that drove the specialisation. **The GPU did not create deep learning; deep learning's shape — dense matrix multiplies — happened to match a machine built for graphics, and the field reorganised around the hardware it could get.** Week 12 returns to this as the general story of domain-specific architecture.

---

## 6. What to Take Away

1. **CPU optimises latency; GPU optimises throughput.** Few complex cores versus thousands of simple ones.
2. **SIMT: warps of 32 threads in lockstep**, programmed as independent threads, one per data element.
3. **The CUDA hierarchy is grid → block → warp → thread.**
4. **Warp divergence** runs both branch paths — on a GPU you *remove* branches, the opposite of Week 5.
5. **Uncoalesced access** costs up to 32× — Week 4's cache line at GPU scale.
6. **The PCIe transfer must be dwarfed by compute** — vector add loses, matrix multiply wins.
7. **GPUs win on high arithmetic intensity and regular access, and lose on everything serial or irregular.**

---

## Exercises

1. A CPU has 4 fast cores; a GPU has 2000 slow ones. For which of these does the GPU win, and why: (a) summing a billion floats, (b) walking a linked list, (c) multiplying two 4096×4096 matrices, (d) parsing a JSON file?
2. A warp of 32 threads hits `if (threadIdx.x < 16) A(); else B();`. How many "passes" does the warp take through the code, and what are the idle threads doing?
3. `data[threadIdx.x]` coalesces into one transaction; `data[threadIdx.x * 8]` does not. Explain, relating it to the 64-byte cache line of Week 4.
4. Vector add is transfer-bound on a GPU. Compute its arithmetic intensity (flops per byte moved) and explain why matrix multiply's is far higher.
5. On a CPU you make branches predictable; on a GPU you make them absent. Explain why the same goal (fast branches) leads to opposite advice.
6. A team ports a pointer-chasing graph algorithm to a GPU and it runs *slower*. Give two reasons from this lecture.

---

*Next: Midterm 2, covering Weeks 5–9. Then Week 11 — performance engineering, where all of this becomes a method.*
