# CS 201 · Week 10 · Lab 10
## Parallel Reduction and False Sharing

---

**When:** **Tuesday of Week 11**, 15:00–16:50, BH 210 — *after* Week 10's three lectures
**Covers:** Week 10 · **Assessment:** unmarked, checked off by the TA
**You need:** `gcc` with `-pthread`, `lscpu`, `nproc`. No GPU required — see below.

---

## Before You Start: No GPU

The curriculum's Lab 10 is a CUDA parallel reduction. **The lab machines have no GPU** — `nvidia-smi` and `nvcc` are both absent *(verified)*.

**So this lab does the reduction on the CPU, and the CUDA version is written alongside as a reading exercise.** The *structure* — partition the data, reduce each partition privately, combine the partials — is identical on both; only the launch syntax differs. **Part 5 shows the CUDA mapping so you can read a GPU reduction, which is what the exam and CS 202 expect; the CPU version is what you compile and measure here.**

Everything measured in this lab is on the CPU. The GPU figures in the lectures are cited.

---

## Part 1 — Know Your Cores (10 min)

```bash
nproc
lscpu | grep -E "^CPU\(s\)|Thread|Core|NUMA"
```

On the lab machine:

```
CPU(s):              8
Thread(s) per core:  2
Core(s) per socket:  4
NUMA node(s):        1
```

*(Verified.)*

**Answer:**

1. The machine reports 8 CPUs. **How many can do independent arithmetic at the same time?** Explain the difference between the two numbers.
2. There is one NUMA node. What would change about this lab on a two-socket machine?

**✅ CHECKPOINT 1** — the topology and your two answers.

---

## Part 2 — Parallel Reduction That Scales (25 min)

Sum `sqrt(k)` for `k` in `[0, N)` — real floating-point work, no sharing. Each thread sums a private range into its own slot; the main thread combines the slots at the end.

```c
static double parts[64];
void *work(void *a) {
    long id = *(long*)a, chunk = N / nthreads;
    double s = 0;
    for (long k = id*chunk; k < (id+1)*chunk; k++) s += sqrt((double)k);
    parts[id] = s;                    /* write once, at the end */
    return NULL;
}
```

Run at 1, 2, 4, 8 threads:

| threads | time | speedup | efficiency |
|---:|---:|---:|---:|
| 1 | 0.184 s | 1.00× | 100% |
| 2 | 0.097 s | 1.90× | 95% |
| **4** | 0.047 s | **3.90×** | **97%** |
| 8 | 0.051 s | 3.59× | 45% |

*(Verified.)*

**Answer:**

1. Scaling is near-perfect to 4 threads and then **reverses** — 8 threads are slower than 4. Explain, using your Part 1 answer.
2. This is a **reduction with private partials**, not a shared accumulator. Why does that design scale when a single shared counter (Part 4) does not?
3. Efficiency is 97% at 4 threads, not 100%. Name one source of the missing 3%.

**✅ CHECKPOINT 2** — your scaling table and three answers.

---

## Part 3 — The Contended Version (20 min)

Now do it *wrong*: all threads increment **one shared atomic counter**.

```c
static atomic_long shared = 0;
void *inc(void *a) { for (long k = 0; k < N/nthreads; k++) atomic_fetch_add(&shared, 1); return NULL; }
```

| threads | time | throughput |
|---:|---:|---:|
| **1** | 6.23 s | **64.2 M ops/s** |
| 2 | 20.19 s | 19.8 M ops/s |
| 4 | 20.53 s | 19.5 M ops/s |
| 8 | 18.77 s | 21.3 M ops/s |

*(Verified.)*

**Read the throughput column.** One thread: 64 million ops/s. Two threads: **fewer than 20 million between them.**

**Answer:**

1. **Adding a second core made the program three times slower.** Explain in terms of MESI: what state must the counter's line be in to write it, and what happens on every increment from a different core?
2. This is called cache-line bouncing. Why does no faster atomic instruction fix it?
3. Rewrite `inc` to scale, and say how many cross-core line transfers your version does in the hot loop.

**✅ CHECKPOINT 3** — the contention table and three answers.

---

## Part 4 — False Sharing (25 min)

The subtle one: **no shared variable, and it still bounces.**

```c
struct { volatile long v; }               packed[4];  /* 8 bytes each — 24 apart, ONE line */
struct { volatile long v; char pad[56]; } padded[4];  /* 64 bytes each — separate lines */
```

Four threads, each incrementing **its own** counter, pinned to the four physical cores:

```
packed addrs span 24 bytes  -> SAME 64B line
padded addrs span 192 bytes -> 3 lines apart

packed  (false sharing): 0.84 s
padded  (no sharing):    0.46 s
false sharing cost: 1.45x slower
```

*(Verified.)*

### 4.1 Confirm they share a line

Print `&packed[i].v` for each `i`. **The four addresses are 8 bytes apart — all within one 64-byte line.** Do the same for `padded`: 64 bytes apart.

### 4.2 Explain and fix

**Answer:**

1. No thread touches another's counter. **Why does `packed` still bounce a cache line between cores?**
2. The fix is 56 bytes of padding per counter. What C11 feature expresses "put this on its own cache line" cleanly?
3. This machine shows 1.45×. **Why would the same code show 5–10× on a 32-core server?**
4. Which earlier week's unit (Week 4) is the thing that makes false sharing possible at all?

> **`perf c2c` is the tool that finds this** by reporting lines that bounce between cores — but it
> needs the perf permissions this machine lacks (Week 4). **The address-printing in 4.1 is the
> unprivileged way to spot it**: hot per-thread data within 64 bytes is a red flag.

**✅ CHECKPOINT 4** — the addresses, the two timings, and four answers.

---

## Part 5 — Read a GPU Reduction (15 min, no compilation)

You cannot run this here, but you must be able to **read** it. The same reduction as Part 2, in CUDA:

```cuda
__global__ void reduce(const float *in, float *out, int n) {
    __shared__ float sdata[256];
    int tid = threadIdx.x;
    int i   = blockIdx.x * blockDim.x + threadIdx.x;
    sdata[tid] = (i < n) ? in[i] : 0.0f;        // each thread loads one element
    __syncthreads();
    for (int s = blockDim.x/2; s > 0; s >>= 1) { // tree reduction within the block
        if (tid < s) sdata[tid] += sdata[tid + s];
        __syncthreads();
    }
    if (tid == 0) out[blockIdx.x] = sdata[0];    // one partial per block
}
```

**Map it onto what you did on the CPU:**

1. Which line corresponds to your `parts[id] = s` — the per-partition partial result?
2. Part 2's threads were independent. **These threads call `__syncthreads()`. Why does the GPU version need a barrier the CPU version did not?**
3. The `if (tid < s)` line means half the threads are idle each iteration. Relate this to **warp divergence** from L33. Is this a case where it is unavoidable?
4. `sdata[tid] += sdata[tid + s]` reads adjacent elements. Why does that access pattern matter on a GPU (L33 §3)?

**✅ CHECKPOINT 5** — your four answers mapping the GPU code to the CPU version.

---

## Before You Leave

| Task | Command / idea |
|---|---|
| Core topology | `lscpu`, `nproc` |
| Pin a thread to a core | `pthread_setaffinity_np` with a `cpu_set_t` |
| Spot false sharing (no perf) | print `&hot_per_thread_data`; flag anything within 64 bytes |
| Spot it (with perf) | `perf c2c record` / `report` — needs privileges |
| Put data on its own line | `alignas(64)` (C11) or `char pad[...]` |
| The scaling design | partition → private partials → combine once |

**The habit:** **the multi-core bottleneck is almost always a cache line moving between cores, not the arithmetic.** Before parallelising, ask what the threads share — including what they share *by accident* through a 64-byte line.

---

*CS 201 · Week 10 · Lab 10*
