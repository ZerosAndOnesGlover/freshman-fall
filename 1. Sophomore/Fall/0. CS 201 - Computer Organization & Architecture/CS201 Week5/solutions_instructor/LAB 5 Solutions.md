# CS 201 · Lab 5 — Solutions and TA Notes
## Instructor Only

---

> **Unmarked.** Four checkpoints. All figures measured on the lab image.
>
> **Midterm 1 is this evening.** Expect a distracted room. **Part 4 is the only part that must
> happen**; if the session is going badly, run Parts 1 and 4 and let them go.

---

## Timing

| Part | Budget | Reality |
|---|---|---|
| 1 — dependency chains | 20 min | 15 min. Satisfying and fast |
| 2 — clock | 10 min | 10 min |
| 3 — vectorise by hand | 35 min | **Runs long.** Intrinsic syntax trips people |
| 4 — watch it disappear | 30 min | **Protect this** |

---

## Part 1

```
1 chain,  0.4768 s   2.38 ns/add
4 chains, 0.1191 s   0.60 ns/add
speedup 4.00x
```

*(Verified.)* **Exactly 4.00×, reproducibly.** Worth pausing on — students expect measurement noise, and this one lands on the integer.

**Answers:**

1. The single chain is limited by **latency**: each `addsd` must finish before the next begins. The four chains are limited by **throughput**: independent operations issue while others are in flight. Same instruction, two different limits.
2. **Eight chains: 7.25×** *(verified — 0.4920 s against 0.0679 s).* **Not 8×.** The limit has moved from dependency latency to **FP add throughput and issue width** — roughly two FP adds per cycle on this core.
3. At `-O2` GCC recognises the single chain as `a = N * 1.0` and computes it directly. **The measurement disappears** — Week 0's Lab Part 4 again. This is why `-O1` is specified.

> **Point 3 catches people every term.** Someone will rebuild at `-O2`, see 0.0000 s, and conclude
> their machine is fast.

**✅ CHECKPOINT 1**

---

## Part 2

```
2e9 dependent add/sub/jne iterations in 0.6230 s  =>  ~3.21 GHz
```

*(Verified.)* `/proc/cpuinfo` during the run shows ~3399 MHz on the active cores; **at idle, cores read 400 MHz** under the `powersave` governor.

**The lesson to state explicitly:** every "cycles" figure in Weeks 4 and 5 depends on a clock, and a clock read at idle describes a state your benchmark never ran in. **Measure it, or state the assumption.**

**✅ CHECKPOINT 2**

---

## Part 3

**Common failures, in order of frequency:**

| Symptom | Cause |
|---|---|
| `SIGSEGV` on the first `_mm256_load_ps` | `malloc` instead of `aligned_alloc(32, …)` |
| `error: unknown type name '__m256'` | Missing `#include <immintrin.h>` |
| `illegal instruction` | Missing `-mavx2`, or genuinely old hardware |
| Wrong results at the array end | $N$ not a multiple of 8, no scalar tail |
| No speedup at all | The scalar reference got auto-vectorised — see 3.3 |

**3.2** — `vmulps` / `vaddps` are the 256-bit packed forms; `mulss` / `addss` are scalar. If only the `ss` forms appear, the intrinsics did not survive.

**3.3 is the honest part.** With `no-tree-vectorize` removed, GCC vectorises the scalar loop itself and the hand-written advantage largely vanishes.

> **Say this plainly:** most loops that benefit from SIMD get it from the compiler for free.
> Intrinsics are for the cases it cannot handle — and identifying those cases requires
> `-fopt-info-vec-missed`, not intuition. **A student who leaves believing intrinsics are routinely
> necessary has learned the wrong thing.**

**✅ CHECKPOINT 3**

---

## Part 4 — the important one

| $N$ | KiB/array | speedup |
|---:|---:|---:|
| $2^{12}$ | 16 | **4.51×** |
| $2^{14}$ | 64 | **4.53×** |
| $2^{16}$ | 256 | 2.78× |
| $2^{18}$ | 1024 | 2.65× |
| $2^{20}$ | 4096 | 1.37× |
| $2^{22}$ | 16384 | **1.07×** |

*(All verified; outputs bit-identical at every size.)*

**Answers:**

1. **48 MiB against a 6 MiB L3.** The loop is waiting for **DRAM bandwidth**. The arithmetic units are idle, so widening them changes nothing.
2. **48 KiB — L1 and L2.** The memory system keeps up, and the **vector units** become the limit.
3. **Crossover between $2^{18}$ and $2^{20}$** — three arrays of 1 MiB is 3 MiB (inside L3, 2.65×); three of 4 MiB is 12 MiB (outside it, 1.37×). **The 6 MiB L3 boundary.**
4. **8 lanes, 4.5×:** two loads and a store per iteration saturate the load/store ports before the ALUs; and loop overhead does not vectorise.

> **The framing to leave them with:** *a program is limited by one resource at a time.* They have now
> measured the same instructions being compute-bound and memory-bound. **Week 11 draws the roofline;
> this is the data it is drawn from.**

**✅ CHECKPOINT 4**

---

## Part 5 — optional

Without `-ffast-math`: **0** vector adds. With it: **4**. *(Verified.)*

The compiler will not reorder a floating-point reduction because addition is not associative. **Adding the flag grants that globally** — including to any compensated summation in the program, which Week 1's Lab 1 measured being silently deleted.

**The hand-written version makes the same reordering deliberately**, which is the difference worth drawing out: not that the flag is wrong, but that it is a global grant where the programmer's version is a local, bounded choice.

---

## What Success Looks Like

1. Break a dependency chain and predict roughly what it buys.
2. Write, build and verify an AVX2 intrinsic loop.
3. Check that the compiler had not already done it.
4. **Say whether a loop is compute-bound or memory-bound before optimising it.**

Item 4 is the one Week 11 assumes.

---

*CS 201 · Week 5 · Lab 5 Solutions · Instructor Only*
