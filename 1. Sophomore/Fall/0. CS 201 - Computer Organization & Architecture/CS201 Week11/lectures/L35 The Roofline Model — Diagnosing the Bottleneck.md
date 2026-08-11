# CS 201 · Computer Organization & Architecture
## Week 11 · Lecture 2 of 3
### The Roofline Model — Diagnosing the Bottleneck

---

**Reading:** CS:APP §5.5–5.9, §6.6 · **Previous:** L34, measure first

---

## 1. Every Hotspot Is One of Two Things

L34's method reaches step 3: the profile named the hotspot, and now you must find out *why* it is slow. **There are only two fundamental answers**, and the whole course has been circling them:

- **Compute-bound** — the arithmetic units are the limit. More flops per second is the only way to go faster.
- **Memory-bound** — the memory system is the limit. The processor is waiting for data, and faster arithmetic changes nothing.

**You have measured both without the name.** Week 5's AVX sweep: 4.51× in cache (compute-bound) collapsing to 1.07× out of cache (memory-bound). Week 4's transpose: the speedup came from DRAM misses, not L1. **The roofline model is the diagram that unifies all of it.**

---

## 2. Arithmetic Intensity Is the Key Number

The single quantity that decides which bound you hit:

$$\text{arithmetic intensity} = \frac{\text{floating-point operations}}{\text{bytes moved from memory}} \quad\left[\frac{\text{flop}}{\text{byte}}\right]$$

**Low intensity → memory-bound. High intensity → compute-bound.** The whole model is reading this one number against the hardware.

| Operation | Flops | Bytes | Intensity |
|---|---:|---:|---:|
| Vector add `c=a+b` | 1 | 24 (2 loads + 1 store, double) | **0.04** |
| SAXPY `y=a·x+y` | 2 | 24 | 0.08 |
| Dot product | 2 | 16 | 0.125 |
| **Matrix multiply** | $2n^3$ | $\sim 3n^2 \times 8$ | **$\sim n/12$ — grows with $n$** |

**Vector add moves 24 bytes to do 1 flop — it is hopelessly memory-bound**, which is exactly why Week 10 said it loses on a GPU. **Matrix multiply's intensity grows with the problem size**, so a big matmul is compute-bound — which is why GPUs and this whole week's optimisations pay off on it.

---

## 3. The Roofline

Plot achievable performance (flop/s) against arithmetic intensity (flop/byte), both log scale:

```
 performance
 (GFLOP/s)
    │              ┌──────────────── peak compute (flat roof)
    │            ╱
    │          ╱   ← the slanted roof = peak memory bandwidth
    │        ╱          (performance = intensity × bandwidth)
    │      ╱
    │    ╱
    └──────────────────────────────── arithmetic intensity (flop/byte)
          ↑ridge
     memory-bound │ compute-bound
```

**Two ceilings, and your program lives under the lower one:**

- **The slanted roof** is memory bandwidth: at low intensity, performance = intensity × bandwidth, so you are limited by how fast bytes arrive.
- **The flat roof** is peak compute: past the ridge, more intensity buys nothing because the ALUs are saturated.
- **The ridge point** is where they meet — the intensity at which a program *could* become compute-bound.

**The diagnosis is a glance:** find your program's intensity on the x-axis, and whether it sits under the slanted roof (memory-bound — reduce bytes moved) or the flat roof (compute-bound — reduce flops or vectorise).

> **The roofline turns "why is it slow?" into a measurement.** Compute the intensity, read the roof
> you are under, and the *kind* of fix follows — you do not vectorise a memory-bound loop (Week 5's
> 1.07×) or restructure the memory access of a compute-bound one. **This is the diagnosis that
> prevents optimising the wrong thing.**

---

## 4. Measured: 7.45× From Changing the Bound

A 1024×1024 `double` matrix multiply, naive versus one loop reorder — **identical arithmetic, identical result**:

```c
/* ijk: inner loop strides DOWN a column of B */         /* ikj: inner loop STREAMS rows of B and C */
for i: for j: for k:  C[i][j] += A[i][k]*B[k][j];        for i: for k: for j:  C[i][j] += A[i][k]*B[k][j];
```

```
naive ijk : 5.521 s
ikj       : 0.741 s   (7.45x)
```

*(Measured.)* **A 7.45× speedup from swapping two loop indices.** Cachegrind says exactly why:

| | D1 miss rate | LLd miss rate |
|---|---:|---:|
| naive `ijk` | 50.1% | **50.1%** |
| `ikj` | 8.3% | **8.3%** |

*(Measured.)*

**The naive version misses L1 half the time, and every one of those misses goes to DRAM** — its LLd rate equals its D1 rate, exactly Week 4's transpose signature. **It strides down a column of B, one useful `double` per 64-byte line.** The `ikj` version streams rows of B and C in memory order, so 8 of every 8 doubles in a line are used and the miss rate collapses to 8%.

**This is a memory-bound problem made less memory-bound by reducing bytes moved** — the roofline's slanted-roof fix. **The arithmetic never changed; the access pattern did.** Big-O is identical; the constant is 7×.

---

## 5. The Optimisation Ladder, Measured

The same matrix multiply, showing where each *kind* of optimisation lives:

| Version | Time | vs naive `-O0` |
|---|---:|---:|
| naive `ijk`, `-O0` | 16.12 s | 1.0× |
| naive `ijk`, `-O2` | 5.27 s | 3.1× |
| naive `ijk`, `-O3` | 4.14 s | 3.9× |
| naive `ijk`, `-O3 -march=native` | 2.82 s | 5.7× |
| **`ikj`, `-O3 -march=native`** | **0.58 s** | **27.8×** |

*(All measured.)*

**Read the ladder as a hierarchy of leverage:**

**Compiler flags gave ~5.7×** — free, and the first thing to try. `-O3` unrolls and vectorises; `-march=native` lets it use this CPU's AVX2 (Week 5).

**The algorithm/layout change gave the rest — the jump from 2.82 s to 0.58 s is another ~5×**, on top of the flags. **The layout fix and the compiler are multiplicative, not competing**, and together they turn 16 seconds into half a second.

> **The order matters and it is the practical rule:** turn on the optimiser first (free), then profile,
> then fix the algorithm and data layout where the profile and the roofline point. **Hand-tuning
> before `-O3` is wasted effort the compiler would have done; hand-tuning the wrong function is wasted
> effort Amdahl warned you about.** Measurement orders the work.

---

## 6. What to Take Away

1. **Every hotspot is compute-bound or memory-bound** — the two roofs.
2. **Arithmetic intensity (flop/byte) decides which.** Vector add is 0.04; matrix multiply grows with $n$.
3. **The roofline diagnoses at a glance:** under the slanted roof, cut bytes moved; under the flat roof, cut flops or vectorise.
4. **A loop reorder gave 7.45×** by dropping the last-level miss rate from 50% to 8% — a memory-bound fix.
5. **Flags then layout: 16 s → 2.8 s → 0.58 s**, and the two are multiplicative.
6. **Turn on the optimiser first, then profile, then fix where the roofline points.**

---

## Exercises

1. Compute the arithmetic intensity of SAXPY (`y[i] = a*x[i] + y[i]`) in `double`. Is it compute- or memory-bound? Which roof is it under?
2. The naive matmul had LLd rate = D1 rate = 50%. What does the equality tell you, and which Week-4 result has the same signature?
3. `ikj` streams B and C in memory order; `ijk` strides B by a column. Compute the bytes-per-useful-double for each, and relate to the 50%→8% miss-rate drop.
4. `-O3 -march=native` gave 5.7× on the naive version with no source change. Name two things the flags did (Weeks 5, 4).
5. A program's hotspot has intensity 0.1 flop/byte on a machine with a ridge at 8 flop/byte. Is vectorising it worth doing? What would help instead?
6. The flag speedup and the layout speedup multiplied to 27.8×. Explain why they compose rather than overlap.

---

*Next: L36 — the pitfalls of benchmarking, and how to measure honestly.*
