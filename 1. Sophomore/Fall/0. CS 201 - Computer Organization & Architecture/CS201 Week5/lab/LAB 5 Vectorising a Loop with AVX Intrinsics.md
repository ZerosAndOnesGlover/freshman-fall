# CS 201 · Week 5 · Lab 5
## Vectorising a Loop with AVX Intrinsics

---

**When:** **Tuesday of Week 6**, 15:00–16:50, BH 210 — *after* Week 5's three lectures
**Covers:** Week 5 · **Assessment:** unmarked, checked off by the TA
**You need:** `gcc` with `-mavx2`, `objdump`. Check first:

```bash
grep -o -m1 avx2 /proc/cpuinfo        # must print avx2
```

---

## What This Lab Is For

To vectorise a loop by hand, measure a real speedup — and then watch that speedup **evaporate** when you make the arrays bigger, without changing a single instruction.

**Part 4 is the point of the lab.** Everything before it is setup.

---

## Part 1 — Break a Dependency Chain (20 min)

Before SIMD, the cheaper parallelism.

```c
/* one chain */                        /* four chains */
double a = 0;                          double b0=0,b1=0,b2=0,b3=0;
for (long i = 0; i < N; i++)           for (long i = 0; i < N; i += 4)
    a += 1.0;                              { b0+=1.0; b1+=1.0; b2+=1.0; b3+=1.0; }
```

$N = 2 \times 10^8$, `gcc -O1`:

```
1 chain,  200000000 adds   0.4768 s   2.38 ns/add
4 chains, 200000000 adds   0.1191 s   0.60 ns/add
speedup 4.00x  (same number of additions)
```

*(Verified — reproducible to two decimals.)*

**Identical arithmetic. 4.00× apart.**

**Answer:**

1. Why is the single chain slower, in terms of latency against throughput?
2. Try **eight** chains. Predict first, then measure. What limits it?
3. `-O1` is used deliberately here. Rebuild the single-chain version at `-O2` and explain what happens to the measurement.

**✅ CHECKPOINT 1** — both timings, the 8-chain result, and your explanation.

---

## Part 2 — Establish the Clock (10 min)

You will quote cycles later, so measure the clock rather than trusting the label.

```c
long n = 2000000000L; long a = 0;
__asm__ volatile("1:\n\t add $1,%0\n\t sub $1,%1\n\t jne 1b"
                 : "+r"(a), "+r"(n) :: "cc");
```

Dependent integer `add` is 1 cycle on any x86-64 since ~2006, so iterations ≈ cycles.

```
2e9 iterations in 0.6230 s  =>  ~3.21 GHz
```

*(Verified.)* Cross-check against `grep MHz /proc/cpuinfo` **while the loop runs** — the governor is `powersave` and idle cores sit at 400 MHz, so a reading taken at rest is meaningless.

**✅ CHECKPOINT 2** — your measured clock and the `/proc/cpuinfo` cross-check.

---

## Part 3 — Vectorise by Hand (35 min)

```c
#include <immintrin.h>

/* scalar reference */
void scalar(void) {
    for (long i = 0; i < N; i++) c[i] = a[i]*b[i] + 1.0f;
}

/* AVX2: eight floats per iteration */
void avx2(void) {
    __m256 one = _mm256_set1_ps(1.0f);
    for (long i = 0; i < N; i += 8) {
        __m256 va = _mm256_load_ps(a + i);
        __m256 vb = _mm256_load_ps(b + i);
        _mm256_store_ps(c + i, _mm256_add_ps(_mm256_mul_ps(va, vb), one));
    }
}
```

**Allocate with `aligned_alloc(32, …)`** — `_mm256_load_ps` requires 32-byte alignment and faults otherwise. This is L12's `movaps` rule one level up. *(`_mm256_loadu_ps` is the unaligned form.)*

```bash
gcc -O2 -mavx2 -o avx avx.c
```

### 3.1 Verify before you time

**Check `c[]` is bit-identical between the two versions.** A vectorised loop that computes the wrong thing is fast and useless, and boundary handling when $N$ is not a multiple of 8 is the usual culprit.

### 3.2 Confirm the instructions

```bash
objdump -d --no-show-raw-insn -M intel avx | grep -E "vmulps|vaddps|mulss|addss" | head
```

**`v...ps` is a 256-bit packed operation; `...ss` is scalar.** If you see no `v` forms, your intrinsics did not survive — check `-mavx2`.

### 3.3 Suppress the compiler's own vectoriser

The scalar reference is marked:

```c
__attribute__((optimize("no-tree-vectorize")))
```

**Remove it and re-measure.** GCC will vectorise the scalar loop itself, and your hand-written version's advantage will largely disappear.

> This is worth doing before you conclude anything about intrinsics. **Most loops that benefit from
> SIMD get it from the compiler for free.** Intrinsics are for the cases where it cannot — and
> knowing which case you are in requires looking.

**✅ CHECKPOINT 3** — identical outputs, `vmulps` in the disassembly, and the auto-vectorised comparison.

---

## Part 4 — Watch the Speedup Disappear (30 min)

Now the part that matters. **Change only $N$.**

| $N$ | bytes/array | speedup |
|---:|---:|---:|
| $2^{12}$ | 16 KiB | **4.51×** |
| $2^{14}$ | 64 KiB | **4.53×** |
| $2^{16}$ | 256 KiB | 2.78× |
| $2^{18}$ | 1 MiB | 2.65× |
| $2^{20}$ | 4 MiB | 1.37× |
| $2^{22}$ | 16 MiB | **1.07×** |

*(All verified; outputs bit-identical at every size.)*

**Identical instructions. Identical work per element. The speedup falls from 4.5× to nothing.**

**Answer, using Week 4's numbers:**

1. Three arrays at $N = 2^{22}$ is 48 MiB. Against which cache does that matter, and what is the loop waiting for?
2. At $N = 2^{12}$ the three arrays total 48 KiB. Which level holds them, and what has become the bottleneck instead?
3. **Where is the crossover**, and which cache boundary does it correspond to?
4. AVX2 is **eight** lanes but the best speedup was **4.5×**. Give two reasons.

> **The general statement, which Week 11 will name the roofline model:** a program is limited by one
> resource at a time. **SIMD only helps if that resource is compute.** Vectorising a memory-bound
> loop is effort spent on the wrong bottleneck — and you would measure 1.07× and wrongly conclude
> that SIMD is overrated.

**✅ CHECKPOINT 4** — your size sweep and all four answers.

---

## Part 5 — Optional: A Reduction

```c
float sum = 0;
for (long i = 0; i < N; i++) sum += a[i];
```

**This will not auto-vectorise**, even at `-O3 -mavx2`. Confirm with `-fopt-info-vec-missed`:

```bash
gcc -O3 -mavx2 -fopt-info-vec-missed -c reduce.c 2>&1 | grep -i reduc
```

**Why:** vectorising a sum means adding in a different order, and floating-point addition is **not associative** (Week 1 L06). The compiler will not silently change your answer.

Add `-ffast-math` and watch it vectorise. **Then compare the two results** — they will differ.

Now do it by hand: keep a `__m256` accumulator, then a horizontal sum at the end. **You are making the same reordering the compiler refused to make — the difference is that you chose it.**

---

## Before You Leave

| Task | Command |
|---|---|
| Check for AVX2 | `grep -o -m1 avx2 /proc/cpuinfo` |
| Compile with AVX2 | `gcc -O2 -mavx2 …` |
| Find vector instructions | `objdump -d -M intel prog \| grep vmulps` |
| Why a loop did not vectorise | `gcc -O3 -fopt-info-vec-missed` |
| Aligned allocation | `aligned_alloc(32, n*sizeof(float))` |

**The habit:** before vectorising anything, find out whether the loop is compute-bound. If it is not, you are about to spend an afternoon for 7%.

---

*CS 201 · Week 5 · Lab 5*
