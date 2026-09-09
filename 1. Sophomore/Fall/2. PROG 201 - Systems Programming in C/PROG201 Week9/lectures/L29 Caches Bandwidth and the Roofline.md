# PROG 201 · Systems Programming in C
## Week 9 · Lecture 2 of 3
### Caches, Bandwidth, and the Roofline

---

**Reading:** CS:APP Ch. 6 · Williams, Waterman & Patterson, *Roofline: An Insightful Visual Performance Model* (CACM 2009) · Drepper, *What Every Programmer Should Know About Memory* §3 · **Previous:** L28 · **Next:** L30 — optimising without fooling yourself

---

## 1. The Hierarchy, Measured

CS 201 gave you the memory hierarchy as a diagram. Here it is as numbers from this machine, produced by chasing a randomly shuffled pointer cycle through a buffer of increasing size — dependent loads, so each one is a full latency:

| working set | ns per access | |
| --- | --- | --- |
| 8 KiB | **1.49** | L1d (32 KiB) |
| 32 KiB | 1.53 | still L1 |
| 128 KiB | 3.13 | L2 (256 KiB) |
| 256 KiB | 4.40 | edge of L2 |
| 1 MiB | 11.84 | L3 (6 MiB) |
| 4 MiB | 16.00 | still L3 |
| **16 MiB** | **107.68** | **DRAM** |
| 64 MiB | 141.94 | DRAM |
| 256 MiB | 141.44 | DRAM |

**Ninety-five times from L1 to DRAM**, and the steps land on the documented cache sizes without being told where they are. This is the single most useful table in performance work: **it is not one memory, it is four, and they differ by two orders of magnitude.**

---

## 2. The Cache Line, Measured

Scan 64 MiB of `int`, touching one element every *stride*:

| stride | bytes apart | ns per element touched |
| --- | --- | --- |
| 1 | 4 | **1.09** |
| 2 | 8 | 1.08 |
| 4 | 16 | 2.01 |
| 8 | 32 | 4.15 |
| **16** | **64** | **6.33** |
| 32 | 128 | 14.52 |
| 64 | 256 | 14.50 |

Read it as a story. At stride 1 you get sixteen `int`s out of every 64-byte line, so each line's cost is amortised sixteen ways. As the stride grows you use less of each line, and the cost per *element* rises in proportion. **At stride 16 you are using one `int` per line and throwing away 60 bytes.**

And then it stops rising: stride 32 and 64 are the same, at 14.5 ns. **The hardware prefetcher has given up** — it fetches adjacent lines while the stride is small enough to look sequential, and beyond 128 bytes it stops trying, so every access is a full miss and there is nothing left to lose.

**The practical consequence is the one thing to take from this lecture:** an array-of-structs where you touch one field is a stride, and turning it into a struct-of-arrays turns 14.5 ns per element into 1.1.

---

## 3. Cachegrind Counts What You Cannot See

`perf`'s hardware counters are unavailable (L28 §3), but Valgrind simulates the cache in software:

```
$ valgrind --tool=cachegrind --cache-sim=yes ./work
==  I refs:        218,178,289
==  D refs:         44,051,858  (42,039,549 rd + 2,012,309 wr)
==  D1  misses:      2,751,768
==  D1  miss rate:         6.2%
==  LL  miss rate:         1.0%
```

**A 6.2% D1 miss rate on a program that walks an `int` array sequentially — and 6.2% is exactly 1/16.** Sixteen `int`s fit in a 64-byte line, the first touch misses and the next fifteen hit. The simulator and the arithmetic agree, which is how you know you have understood the number rather than merely read it.

Cachegrind's limits are worth stating: it simulates **one** cache model, knows nothing about prefetching, hardware or otherwise, and is 20–100× slow. **Its miss *counts* are a model; its miss *ratios* are usually right**, and for finding which loop is thrashing that is enough.

---

## 4. The Two Ceilings

Every computation is bounded by two things: how fast the machine can do arithmetic, and how fast it can move data. Measure both.

**Bandwidth** — stream a buffer far larger than the last-level cache:

```
memory bandwidth      13.71 GB/s   (256 MiB streaming read)
```

**Arithmetic peak** — independent fused multiply-adds, touching no memory:

```
arithmetic peak       13.50 GFLOP/s (independent FMAs, no memory)
```

Divide one by the other and you get the machine's **ridge point**:

```
ridge point            0.98 flops/byte
```

**Below 0.98 flops per byte a computation cannot be anything but memory-bound on this machine.** Above it, it has a chance of being compute-bound. That single number tells you, before you write anything, which half of the problem you are in.

---

## 5. Arithmetic Intensity and the Roofline

**Arithmetic intensity** is flops performed divided by bytes moved to and from DRAM. It is a property of the *algorithm*, not the machine:

| kernel | flops | bytes | AI |
| --- | --- | --- | --- |
| `b[i] = a[i]` | 0 | 16 | 0 |
| `s += a[i]` | 1 | 8 | 0.125 |
| `b[i] = k*a[i] + b[i]` | 2 | 24 | 0.083 |
| degree-16 polynomial per element | 32 | 8 | 4.0 |

The **roofline** is the upper bound that follows:

```
    attainable GFLOP/s  =  min( peak GFLOP/s,  AI × bandwidth )
```

Plot it with AI on the x-axis and GFLOP/s on the y-axis, both logarithmic, and you get a slanted line (the bandwidth limit) meeting a horizontal one (the arithmetic limit) at the ridge point. Every kernel is a point under that roof, and **how far under, and in which region, is the whole diagnosis.**

---

## 6. The Kernels

Same machine, 256 MiB arrays, ceilings from §4:

| kernel | AI | GFLOP/s | GB/s | % of its roof |
| --- | --- | --- | --- | --- |
| `sum`, one accumulator | 0.125 | 0.77 | 6.17 | **45%** |
| `axpy` | 0.083 | 1.13 | 13.55 | **99%** |
| `copy` | 0 | — | 10.78 | — |
| `poly(deg 16)`, one chain | 4.0 | 2.47 | 0.62 | **18%** |
| `poly(deg 16)`, four chains | 4.0 | **7.14** | 1.79 | **53%** |
| `poly(deg 64)`, one chain | 16.0 | 2.59 | 0.16 | 19% |
| `poly(deg 64)`, four chains | 16.0 | **7.08** | 0.44 | 52% |

Three readings, in increasing order of usefulness:

**`axpy` at 99% is finished.** It is memory-bound, it is achieving the memory bandwidth the machine has, and no amount of cleverness inside the loop will help. **The only thing that helps a kernel at its roof is moving less data** — a different data type, a different layout, or fusing it with the loop before it.

**`poly` at 18% is not finished**, and the roofline says it is compute-bound, so the problem is inside the arithmetic.

**And the two `poly` rows at identical arithmetic intensity differ by 2.9×**, which the roofline model cannot explain at all.

---

## 7. Why a Kernel Misses Its Roof

```c
for (int d = 0; d < deg; d++) p = p * x + d;        /* one chain: 2.47 GFLOP/s */
```

Every iteration needs the previous iteration's `p`. An FMA has a **latency of about 4 cycles** and a **throughput of two per cycle**, so a single dependent chain runs at one FMA per 4 cycles and leaves seven eighths of the arithmetic units idle.

```c
p0 = p0*x0 + d;  p1 = p1*x1 + d;                    /* four chains: 7.14 GFLOP/s */
p2 = p2*x2 + d;  p3 = p3*x3 + d;
```

Four independent chains keep four FMAs in flight, and the rate nearly triples with **no change to the arithmetic intensity and no change to the number of flops.**

**This is the roofline's honest limitation, and knowing it is what stops the model being a cargo cult.** It bounds you from above using two machine numbers and one algorithm number. It does not know about:

- **dependency chains** — §7, and the commonest cause of missing the roof;
- **instruction-level parallelism** and how many execution ports you have;
- **prefetching**, and therefore access *order* — §2's stride table is invisible to it;
- **vectorisation** — a scalar loop's roof should really be one eighth of the AVX peak;
- **latency-bound memory access**, which is §8.

**A point far below the roof is a question, not an answer.** The model tells you which ceiling to look at; finding out why you are not near it is the work.

---

## 8. The Mistake This Lecture Was Written With

The first version of the measurement program reported:

```
memory bandwidth       6.28 GB/s
```

and then a kernel achieving **13.55 GB/s** — 222% of a roof, which is impossible and therefore a bug in the measurement rather than a discovery.

The bandwidth ceiling had been measured with

```c
for (size_t i = 0; i < n; i++) s += a[i];       /* ONE accumulator */
```

which is **exactly the dependency chain from §7**. A single-accumulator reduction is bounded by floating-point add latency, not by memory, and it reads 6.28 GB/s on a machine that does 13.71. With eight accumulators:

```
memory bandwidth      13.71 GB/s
```

and every kernel drops below 100%, where it belongs.

**Two lessons, and the second is the one to keep.** A roofline point above the roof is always a measurement error — the model is an upper bound, so exceeding it means one of the three inputs is wrong. And **the same mistake appears twice in this lecture**: once as a bug in the ceiling and once as the `sum (1 acc)` kernel sitting at 45%. Once you have seen a dependency chain cost you a factor of two in a benchmark, you start seeing it in the code you are optimising.

---

## Summary

- The hierarchy, measured: **L1 1.49 ns, L2 3.13, L3 11.84, DRAM 141.94** — a factor of **95**, with the steps landing on the documented cache sizes.
- **Stride 1 costs 1.09 ns per element and stride 16 costs 6.33**, because 16 `int`s share a 64-byte line. Beyond 128 bytes it flattens at 14.5 — **the prefetcher has stopped trying.**
- Cachegrind measured a **6.2% D1 miss rate** on a sequential `int` scan, which is exactly **1/16**.
- **Two ceilings, measured: 13.71 GB/s and 13.50 GFLOP/s, giving a ridge point of 0.98 flops/byte.** Below that intensity, memory-bound; above it, possibly compute-bound.
- **Roofline: attainable = min(peak, AI × bandwidth).** `axpy` hit **99%** of its roof and is finished; `poly` hit **18%** and is not.
- **Two kernels at identical arithmetic intensity differed by 2.9×** because one had a single dependency chain and the other had four. The roofline cannot see that, or prefetching, or vectorisation.
- **A point above the roof is a measurement bug** — as this lecture's own first bandwidth number was, for exactly the reason the `poly` rows demonstrate.

---

## Exercises

1. Reproduce §1's table on your machine and compare the step positions with `lscpu | grep -i cache`. Do they agree?
2. Add a *sequential* pointer chase to §1 (each element points at the next). Why is it flat, and what does that tell you about the prefetcher?
3. Extend §2's stride table to 4,096 bytes. Where is the next step, and what does it correspond to? *(Hint: `getconf PAGESIZE`, and think about the TLB.)*
4. Turn an array-of-structs into a struct-of-arrays for a workload that touches one field, and predict the speedup from §2's table before measuring.
5. Compute the arithmetic intensity of a naive *n*×*n* matrix multiply, and of a tiled one. Plot both on your roofline. Which region is each in?
6. Take `poly` to eight and sixteen independent chains. Where does it stop helping, and what does that number correspond to?
7. Measure your machine's bandwidth with 1, 2, 4 and 8 accumulators. Reproduce §8's bug deliberately, then say how you would have caught it without knowing the answer.

---

*PROG 201 · Week 9 · L29 · © CSE Department*
