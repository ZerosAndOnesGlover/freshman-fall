# CS 201 · Computer Organization & Architecture
## Week 5 · Lecture 3 of 3
### SIMD, and the Law That Limits Everything

*“The first characteristic of interest is the fraction of the computational load which is associated with data management housekeeping. This fraction has been very nearly constant for about ten years, and accounts for 40% of the executed instructions in production runs.”* — Gene Amdahl, "Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities" (1967) — the paper behind Amdahl's law

---

**Reading:** CS:APP §5.9–5.10, §1.9.1 · **Previous:** L17, prediction and out-of-order execution

**Coursework:** 📝 **PS 4** due today 17:00 · 📊 **Quiz 6** Mon of Week 6 · 🔬 **Lab 5** Tue of Week 6 15:00–16:50 · 📝 **PS 6** released Wed of Week 6, due Fri of Week 7 17:00

---

## 1. One Instruction, Many Data

Pipelining and out-of-order execution extract parallelism the hardware *finds*. **SIMD is parallelism you declare.**

A 256-bit AVX2 register holds eight `float`s or four `double`s. One `vmulps` multiplies all eight pairs at once.

| Extension | Width | `float`s | Year |
|---|---|---|---|
| SSE2 | 128-bit | 4 | 2001 |
| **AVX2** | **256-bit** | **8** | 2013 |
| AVX-512 | 512-bit | 16 | 2016 |

**This machine has AVX2 and not AVX-512** *(verified from `/proc/cpuinfo`)* — so eight `float` lanes is the ceiling here.

---

## 2. Writing It

Three ways, in increasing order of effort and control.

**Auto-vectorisation** — the compiler does it. `-O3` or `-O2 -ftree-vectorize`, plus `-mavx2` to permit the instructions. Free, and fragile: a loop-carried dependency, an unknown trip count, possible pointer aliasing, or a function call in the body will all silently prevent it.

**Intrinsics** — you write the vector operations, the compiler allocates registers:

```c
#include <immintrin.h>
__m256 one = _mm256_set1_ps(1.0f);
for (long i = 0; i < N; i += 8) {
    __m256 va = _mm256_load_ps(a + i);
    __m256 vb = _mm256_load_ps(b + i);
    _mm256_store_ps(c + i, _mm256_add_ps(_mm256_mul_ps(va, vb), one));
}
```

**Hand-written assembly** — almost never worth it now.

**Note `_mm256_load_ps` requires 32-byte alignment**, which is why the arrays come from `aligned_alloc(32, …)`. The unaligned form is `_mm256_loadu_ps` — this is L12's `movaps`/`movups` distinction, one level up.

---

## 3. Measured: 4.5×, and Then 1.07×

The loop above, `c[i] = a[i]*b[i] + 1.0f`, scalar against AVX2, at several array sizes:

| $N$ | bytes/array | scalar → AVX2 |
|---:|---:|---:|
| $2^{12}$ | 16 KiB | **4.51×** |
| $2^{14}$ | 64 KiB | **4.53×** |
| $2^{16}$ | 256 KiB | 2.78× |
| $2^{18}$ | 1 MiB | 2.65× |
| $2^{20}$ | 4 MiB | 1.37× |
| $2^{22}$ | 16 MiB | **1.07×** |

*(All measured; results verified bit-identical between the two versions at every size.)*

**Eight lanes, and the speedup falls from 4.5× to essentially nothing.** The instructions are the same in every row. The only thing that changed is how much data they touch.

**Why.** Three arrays at $N = 2^{22}$ is 48 MiB — eight times the 6 MiB L3. **The loop is waiting for DRAM**, and it does not matter how fast the arithmetic is. At $N = 2^{12}$ everything fits in L1, the memory system keeps up, and the vector units become the limit.

> **This is the week's connection to Week 4, and it is the single most useful idea in performance
> work.** A program is limited by *one* resource at a time. **SIMD only helps if that resource is
> compute.** Vectorising a memory-bound loop is effort spent on the wrong bottleneck — you will
> measure 1.07× and conclude, wrongly, that SIMD is overrated.
>
> Week 11 gives this a name and a diagram: **the roofline model.** You have now measured both roofs.

**And 4.5×, not 8×.** Eight lanes rarely give eight times, because the loop still needs two loads and a store per iteration, and there are only so many load/store ports. **The arithmetic stopped being the bottleneck and something else took over** — which is what always happens.

---

## 4. When Vectorisation Fails

| Blocker | Why | Fix |
|---|---|---|
| **Loop-carried dependency** | `a[i] = a[i-1] + x` — lane $i$ needs lane $i-1$ | Restructure, or accept it |
| **Aliasing** | The compiler cannot prove `a` and `c` do not overlap | `restrict`, or copy |
| **Branches in the body** | Lanes would need to diverge | Masked operations, or hoist the branch |
| **Non-contiguous access** | Gather/scatter is far slower than a contiguous load | Change the layout — AoS to SoA (Week 4) |
| **Function calls** | Cannot vectorise across a call | Inline it |
| **Reductions** | `sum += a[i]` is a dependency chain | Vector accumulator, then a horizontal sum |

**The reduction case connects back to Week 1.** Vectorising `sum += a[i]` means summing in a different order — which changes the answer, because floating-point addition is not associative. **The compiler will not do it without `-ffast-math`**, and you now know exactly what that flag gives away.

---

## 5. Amdahl's Law

Every technique in this week has a ceiling, and this is it.

If a fraction $p$ of a program can be sped up by a factor $s$, the overall speedup is

$$S = \frac{1}{(1-p) + \dfrac{p}{s}}$$

**As $s \to \infty$, $S \to \dfrac{1}{1-p}$.** The serial part is a hard wall.

| Fraction parallelised | Max speedup, infinite resources |
|---:|---:|
| 50% | 2× |
| 90% | 10× |
| 95% | 20× |
| **99%** | **100×** |
| 99.9% | 1000× |

**Read the 90% row carefully.** A program that is 90% parallel can never exceed 10×, **no matter how many cores you buy.** Not "in practice" — ever.

### Applied to this lecture

Suppose a program spends 40% of its time in a loop you vectorise at 4.5×:

$$S = \frac{1}{0.6 + \frac{0.4}{4.5}} = \frac{1}{0.6 + 0.089} = \mathbf{1.45\times}$$

**A 4.5× improvement on 40% of the runtime is a 45% improvement overall.** This is the most common disappointment in optimisation, and it is arithmetic, not bad luck.

> **The corollary is the reason Week 11 exists: optimise the biggest fraction first.** Making a 5%
> component infinitely fast gains you 5.3%. Profile before you choose, or you will do excellent work
> on something that does not matter.

**Gustafson's objection** is worth knowing. Amdahl assumes a *fixed problem size*. In practice, more capable machines are used on *larger* problems, and the serial fraction often shrinks as the problem grows. Both laws are correct; they answer different questions. **Amdahl: "how much faster for this problem?" Gustafson: "how much bigger a problem in the same time?"**

---

## 6. What to Take Away

1. **SIMD is declared parallelism**; AVX2 is 256 bits — eight `float`s. No AVX-512 here.
2. **Intrinsics are the practical middle ground**, and alignment matters.
3. **4.51× in cache, 1.07× out of it** — identical instructions, different bottleneck.
4. **SIMD only helps compute-bound code.** Establish the bottleneck first.
5. **8 lanes gave 4.5×**, because load/store ports became the limit.
6. **Vectorising a reduction changes the answer**, which is why it needs `-ffast-math`.
7. **Amdahl: $S = 1/((1-p) + p/s)$.** 90% parallel caps at 10×, forever.
8. **A 4.5× win on 40% of runtime is 1.45× overall.**

---

## Exercises

1. AVX2 is 256 bits. How many `double`s, `int`s, `short`s and `char`s fit in one register?
2. §3 measures 4.51× from an 8-lane instruction set. Give two reasons the factor is not 8.
3. A program spends 70% of its time in a vectorisable loop. You achieve 6× on it. Compute the overall speedup, then the speedup if you had achieved 100×.
4. Using Amdahl, find the parallel fraction needed for a 50× speedup on 64 cores. Comment on how achievable that is.
5. `sum += a[i]` will not auto-vectorise without `-ffast-math`. Explain the exact objection, and describe how you would vectorise it by hand while controlling the error.
6. The AVX speedup fell from 4.53× at 64 KiB to 1.37× at 4 MiB. Using Week 4's numbers, predict where the crossover sits and say which cache boundary it corresponds to.

---

*Midterm 1 is this week — Weeks 0–4, 75 minutes. See the revision guide in `resources/`.*
*Next week: virtual memory.*
