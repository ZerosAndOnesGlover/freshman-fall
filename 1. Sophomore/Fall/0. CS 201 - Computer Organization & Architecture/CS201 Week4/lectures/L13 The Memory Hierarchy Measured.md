# CS 201 · Computer Organization & Architecture
## Week 4 · Lecture 1 of 3
### The Memory Hierarchy, Measured

---

**Reading:** CS:APP §6.1–6.3 · **Previous:** L12, alignment and recursion

---

## 1. The Problem the Hierarchy Solves

You want memory that is large, fast and cheap. **You may have two.**

| | Fast | Large |
|---|---|---|
| SRAM (cache) | ✅ | ✗ — six transistors per bit |
| DRAM (main memory) | ✗ | ✅ — one transistor and a capacitor |

The hierarchy is the engineering answer: a small fast thing in front of a large slow thing, arranged so that **most accesses are served by the fast one.** Whether that works depends entirely on your access pattern — which is why this is a programming topic and not a hardware topic.

---

## 2. What It Actually Costs on This Machine

Not a textbook table. A **pointer chase** — each load's address comes from the previous load, so the CPU cannot prefetch or overlap — over working sets from 4 KiB to 32 MiB:

| Working set | ns/access | ≈ cycles @ 3.4 GHz | Served by |
|---:|---:|---:|---|
| 4 KiB | 1.22 | 4.1 | **L1d** |
| 8 KiB | 1.22 | 4.1 | L1d |
| 16 KiB | 1.19 | 4.0 | L1d |
| **32 KiB** | **1.22** | **4.1** | L1d — *exactly its size* |
| 64 KiB | 2.50 | 8.5 | spilling into L2 |
| 128 KiB | 3.40 | 11.6 | **L2** |
| **256 KiB** | **5.67** | 19.3 | L2 — *exactly its size* |
| 512 KiB | 9.27 | 31.5 | L3 |
| 1 MiB | 12.12 | 41.2 | **L3** |
| 2 MiB | 14.83 | 50.4 | L3 |
| 4 MiB | 30.39 | 103 | L3, under pressure |
| **8 MiB** | **81.81** | 278 | **DRAM** — *past the 6 MiB L3* |
| 32 MiB | 128.94 | 438 | DRAM |

*(All measured on the lab machine.)*

**Read the flat regions and the cliffs.** The number is constant at 1.22 ns up to **32 KiB**, then rises. It settles again around **128–256 KiB**. It rises hard past **6 MiB**. Compare with the actual geometry from `lscpu -C`:

```
L1d  32K   8-way   64B lines
L2  256K   4-way   64B lines
L3    6M  12-way   64B lines
```

**The cliffs are at 32 KiB, 256 KiB and 6 MiB. The hardware told us its own cache sizes.** You did not have to look them up; the stopwatch found them.

And the cycle counts — **4, 12, 41, 438** — land almost exactly on the canonical figures in every architecture textbook (4, 12, 40, 200+). **This is one of the few places where the round numbers you were taught are simply true.**

---

## 3. The One Number That Matters

$$\frac{438}{4.1} \approx \mathbf{107\times}$$

**A DRAM access costs about a hundred L1 hits.** Everything in this week, and most of Week 11, follows from that ratio.

Put it in instruction terms: while one DRAM access completes, the CPU could have retired **hundreds** of arithmetic instructions. **For most real programs the processor is not computing. It is waiting.**

> **This is why Week 0's von Neumann bottleneck was not a historical footnote.** The gap between
> processor speed and memory speed has widened every year since 1980. The hierarchy is not an
> optimisation; it is the only reason a modern CPU is not idle almost all the time.

---

## 4. The Cost Is Not Per Byte — It Is Per Line

Memory does not move in bytes. It moves in **cache lines of 64 bytes**, at every level.

Measure it directly. Walk 256 MiB of `int`s, touching every $s$-th element:

| stride (ints) | bytes | ns per access |
|---:|---:|---:|
| 1 | 4 | **0.85** |
| 2 | 8 | 1.18 |
| 4 | 16 | 2.30 |
| 8 | 32 | 5.94 |
| **16** | **64** | **11.06** |
| 32 | 128 | 18.32 |
| 64 | 256 | 19.42 |

*(Measured.)*

**The cost per access rises steadily until stride 16 — which is 64 bytes, exactly one cache line — and then flattens.**

The reason is that up to that point **every stride fetches the same number of lines.** At stride 1 you use all 16 `int`s in each line; at stride 16 you use one and discard fifteen. The line was fetched either way. **You paid the same and got 1/16 of the value.**

> **So the useful question is never "how many bytes do I read?" It is "how many distinct 64-byte lines
> do I touch, and how much of each do I use?"** Restating a performance problem that way is most of
> solving it.

---

## 5. Two Kinds of Locality

The hierarchy works only if your accesses cluster. There are exactly two ways they can.

**Temporal locality** — you access the same location again, soon. A loop counter, an accumulator, a hot lookup table. The hardware exploits this by *keeping* recently used lines.

**Spatial locality** — you access a location near one you just used. Walking an array, reading struct fields. The hardware exploits this by *fetching a whole line* when you touch one byte of it.

**These are the only two levers you have.** Every cache optimisation in this course is one of:

- make the working set smaller, so it fits in a faster level *(temporal)*;
- reorder accesses so nearby data is used together *(spatial)*;
- change the layout so the data that is used together *is* nearby *(spatial)*.

---

## 6. Thirty Times, From Swapping Two Lines

```c
for (int i = 0; i < N; i++)          for (int j = 0; j < N; j++)
    for (int j = 0; j < N; j++)          for (int i = 0; i < N; i++)
        s += m[i*N + j];                     s += m[i*N + j];
```

Same array, same $N^2$ additions, **same answer**. On a 4096×4096 `int` matrix:

```
row-major (i,j)   0.0086 s   sum=16777216
col-major (j,i)   0.3099 s   sum=16777216
ratio             35.98x
```

*(Measured. A second run gave 28.71× — the effect is large and somewhat variable, never small.)*

**Why.** C stores arrays **row-major**: `m[i][j]` and `m[i][j+1]` are adjacent. The left loop walks memory sequentially, using all 16 `int`s of every line it fetches. The right loop strides by `N*4 = 16 384` bytes, **touching one `int` per line and then abandoning it** — and by the time it comes back to that row, the line is long gone.

**Nothing in the C says which is faster.** The instruction counts are identical; the disassembly is nearly identical. The difference is entirely in which addresses are touched in which order.

> **This is the moment the course changes.** Until now, "what does this compile to?" answered your
> performance questions. From here, the compiler's output is the same and the *data* decides. Week 11
> is three hours of consequences.

---

## 7. What to Take Away

1. **Fast, large, cheap — pick two.** The hierarchy is the compromise.
2. **On this machine: 4, 12, 41, 438 cycles** for L1, L2, L3, DRAM. Measured, and matching the canonical numbers.
3. **DRAM costs ~107 L1 hits.** Most programs are waiting, not computing.
4. **Memory moves in 64-byte lines.** Count lines touched, not bytes read.
5. **Temporal and spatial locality are the only two levers.**
6. **Loop order alone was worth ~30×** on identical work.

---

## Exercises

1. The pointer chase deliberately makes each load depend on the previous one. What would a *sequential* walk measure instead, and why would it not reveal the cache sizes as cleanly?
2. From the table in §2, estimate the size of L2 without being told it. What feature of the data are you reading?
3. At stride 32 the cost per access was 18.32 ns and at stride 64 it was 19.42 ns — nearly the same. Explain why it stops growing.
4. A `struct` has a 4-byte field you read constantly and 120 bytes you rarely touch. You have an array of 100 000 of them. Describe the layout change that would help, and estimate the reduction in lines touched.
5. The column-major loop is ~30× slower. Would padding the row length from 4096 to 4097 `int`s help, hurt, or do nothing? Predict, then say what you would measure to check.

---

*Next: L14 — how a cache actually decides where a line goes.*
