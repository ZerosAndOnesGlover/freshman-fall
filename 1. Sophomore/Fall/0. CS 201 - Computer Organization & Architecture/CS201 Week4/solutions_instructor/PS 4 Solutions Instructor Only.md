# CS 201 · Problem Set 4 — Solutions
## Instructor Only

---

> **Not for distribution.** All figures measured on the lab image (i5-8250U, GCC 13.3.0, Valgrind
> 3.22). **Student machines will differ** — mark the method and the reasoning, not agreement with
> these numbers.

---

## Q1 (16) — Cache Geometry

### (a) [4]

| | $S$ | $E$ | $B$ | $S \times E \times B$ |
|---|---:|---:|---:|---|
| L1d | 64 | 8 | 64 | $= 32\,768$ = 32 KiB ✓ |
| L2 | 1024 | 4 | 64 | $= 262\,144$ = 256 KiB ✓ |
| L3 | 8192 | 12 | 64 | $= 6\,291\,456$ = 6 MiB ✓ |

### (b) [4]

**offset** = $\log_2 64$ = **6 bits** · **set index** = $\log_2 64$ = **6 bits** · **tag** = remaining 52.

For `0x7fff8a3c40`:

- offset = low 6 bits of `0x40` = `0x00` → **0**
- set index = $\lfloor \texttt{0x7fff8a3c40}/64 \rfloor \bmod 64$. $\texttt{0x7fff8a3c40} = 549\,754\,662\,464$; $/64 = 8\,589\,916\,601$; $\bmod\ 64 = \mathbf{57}$
- tag = $\lfloor 8\,589\,916\,601 / 64 \rfloor = 134\,217\,446$

> Accept the bit-slicing method shown in any form. The marks are for the 6/6/52 split, not arithmetic.

### (c) [4]

$$S \times B = 64 \times 64 = \mathbf{4096 \text{ bytes}}$$

Any stride that is a multiple of 4096 maps to the same set every time. In `double`s that is a row length of $4096/8 = \mathbf{512}$ — which is exactly why `double A[512][512]` is the standard pathological example.

### (d) [4] — 1 each

1. **Compulsory.** Never referenced before; must be fetched once.
2. **Conflict.** 8 KiB of data in a 32 KiB cache — capacity is ample — but the 32 KiB separation maps both arrays to identical sets, and direct-mapped means one line per set.
3. **Compulsory.** Each line is touched once and never reused; there is nothing to keep.
4. **Capacity.** 10 MiB exceeds the 6 MiB L3, and random order defeats reuse.

---

## Q2 (20) — Finding the Cliffs

### (a) [6]

| KiB | ns | KiB | ns |
|---:|---:|---:|---:|
| 4 | 1.22 | 512 | 9.27 |
| 8 | 1.22 | 1024 | 12.12 |
| 16 | 1.19 | 2048 | 14.83 |
| **32** | **1.22** | 4096 | 30.39 |
| 64 | 2.50 | **8192** | **81.81** |
| 128 | 3.40 | 16384 | 113.54 |
| 256 | 5.67 | 32768 | 128.94 |

*(Verified.)*

**Cliffs:** flat at 1.22 ns through **32 KiB**, then rising → **L1d = 32 KiB** ✓. Settles near 3.40 ns around 128 KiB and departs after **256 KiB** → **L2 = 256 KiB** ✓. Rises sharply past **4–8 MiB** → **L3 = 6 MiB** ✓.

**All three match Q1(a) exactly.**

### (b) [4]

At 3.4 GHz (0.294 ns/cycle):

| Level | ns | cycles | canonical |
|---|---:|---:|---:|
| L1 | 1.22 | **4.1** | 4 |
| L2 | 3.40 | **11.6** | 12 |
| L3 | 12.12 | **41.2** | 40 |
| DRAM | 128.94 | **438** | 200+ |

> **The agreement is unusually good** and worth remarking on in class — students are used to textbook
> round numbers being approximations. Accept any stated clock; require the student to *state* it.

### (c) [4]

$$\frac{438}{4.1} \approx \mathbf{107}$$

**One DRAM access costs about 107 L1 hits.** For a program whose working set exceeds L3, the processor spends the overwhelming majority of its cycles waiting rather than computing — so **reducing memory traffic beats reducing instruction count**, often by two orders of magnitude.

### (d) [6]

| KiB | random | sequential |
|---:|---:|---:|
| 4 | 1.22 | 1.39 |
| 32 | 1.22 | 1.19 |
| 256 | 5.67 | 1.21 |
| 2048 | 14.83 | 1.33 |
| 8192 | 81.81 | 1.52 |
| 32768 | 128.94 | **1.55** |

*(Verified.)* **At 32 MiB, sequential is 83× faster on the identical working set.**

**[3] Mechanism:** the **hardware prefetcher** detects a constant stride and issues loads ahead of demand, so the line is already resident when the program asks. Latency is fully hidden; the loop becomes bandwidth-limited rather than latency-limited. A random cycle gives it nothing to predict, and each load must complete before the next address is even known.

**[3] Why the rest still matters** — any of:

- **Prefetching hides latency, not bandwidth.** Once you saturate the memory bus, more prefetching does not help; the transpose in Q3 is bandwidth-bound and blocking still gives 3.29×.
- **Only regular patterns are predictable.** Linked lists, trees, hash tables and graph traversals — a large share of real workloads — get nothing.
- **Prefetching fetches whole lines.** The column-major loop uses 1 of 8 doubles per line; a prefetcher that correctly anticipates a wasteful pattern still wastes 7/8 of the bandwidth.

> **Full marks require engaging with the tension.** A student who just describes prefetching has
> answered half the question.

---

## Q3 (34) — The Transpose

### (a) [8]

Standard implementations; 4 for each being correct, with an elementwise check against `naive` for every $b$.

> **Require the correctness check.** A blocked transpose with a boundary bug is easy to write and
> gives plausible timings.

### (b) [6]

```
naive            0.0608 s   (1.00x)
blocked b=8      0.0250 s   (2.43x)
blocked b=16     0.0230 s   (2.65x)
blocked b=32     0.0185 s   (3.29x)
blocked b=64     0.0170 s   (3.58x)
```

*(Verified.)*

### (c) [6]

Two $b \times b$ `double` tiles: $2 b^2 \times 8$ bytes $\le 32\,768$, so $b \le \sqrt{2048} \approx \mathbf{45}$.

**Measured optimum is 64 — larger than the derivation allows.** Any of these accounts for it, and one is required:

- The tile need not be fully resident; only the $b$ **lines** currently in play must be, which is a far weaker constraint.
- L2 (256 KiB) catches the overflow at ~12 cycles, which is cheap relative to the DRAM trips being avoided.
- $b = 64$ `double`s is 512 bytes = exactly 8 cache lines per row, which aligns tile rows to line boundaries.

> A student who derives ~45, measures 64, and *notices the discrepancy* gets full marks even with an
> incomplete explanation. One who reports 64 and claims the derivation predicted it has not checked.

### (d) [8]

| | D refs | D1 miss rate | LLd miss rate |
|---|---:|---:|---:|
| naive | 12 636 013 | 41.5% | **41.5%** |
| blocked $b=32$ | 12 636 160 | **42.5%** | **13.5%** |

*(Verified.)*

**[4]** **D1 misses rose** (5 244 694 → 5 375 708) while **LLd misses fell 3.07×** (5 244 472 → 1 705 595).

**[4] The explanation must distinguish where a miss is served.** An L1 miss caught by L2 costs ~12 cycles; one that reaches DRAM costs ~438 — **36× more**, and both are counted identically in "D1 miss rate". Blocking traded a small number of extra L1 misses (cheap, served by L2/L3) for a threefold reduction in DRAM trips (expensive). 3.07× fewer DRAM accesses → 3.29× faster.

### (e) [6]

**[3]** LLd misses are within 0.005% of D1 misses, so **essentially every L1 miss also missed L2 and L3 and went to DRAM.** L2 and L3 contributed nothing — the access stride exceeded what any of them could span.

**[3]** **Aim the optimisation at the level that is actually missing.** The naive version's problem was never L1; it was that nothing below L1 was helping. Blocking's job was to bring L2 and L3 into play, and the LLd rate is the measurement that shows it worked.

---

## Q4 (16) — The Control

### (a) [4]

naive **0.0035 s**, blocked $b=32$ **0.0026 s** — **1.35×**. *(Verified.)*

### (b) [4]

LLd misses **66 989** and **66 993**. *(Verified.)* A difference of 4 in ~67 000 — 0.006%.

### (c) [4]

**Compulsory (cold) misses.** Each of the two 2 MiB matrices must be brought in from memory **once**; there is no prior state to reuse. **No reordering can avoid a first touch** — the only ways to reduce them are to touch less data or to overlap the fetch with computation (prefetching), neither of which is a loop transformation.

### (d) [4]

**The rebuttal must contain the conditional structure**, not just a defence of blocking.

Blocking reduces **capacity** misses by shrinking the inner loop's working set below the cache size. At $N = 512$ both matrices already fit in the 6 MiB L3, so **there were no capacity misses at the last level to remove** — the LLd count is compulsory misses only, and it is identical in both versions.

**This is precisely what makes the $N = 2048$ result credible.** An intervention that improved things everywhere, under all conditions, would be suspicious — it would suggest the measurement rather than the mechanism was doing the work. **An intervention that helps exactly when its stated mechanism applies, and does nothing when it does not, is evidence the mechanism is real.**

**The general principle:** an optimisation is a claim about a *specific* bottleneck. Its value is conditional on that bottleneck being present, and a competent engineer establishes the condition before applying the technique.

> This is the best question on the problem set. **Award generously for the conditional reasoning**,
> even if expressed loosely.

---

## Q5 (14) — Layout

### (a) [5]

`sizeof(struct particle)` = **88** bytes *(verified: 6×8 = 48, `int id` at offset 48, `char name[32]` at 52, total 84, padded to 88 for 8-byte alignment)*.

**AoS:** the step touches 48 useful bytes out of every 88, but lines are fetched whole:
$$\frac{10^6 \times 88}{64} = \mathbf{1\,375\,000 \text{ lines}}$$

**SoA:** six separate `double` arrays, all fully used:
$$\frac{10^6 \times 6 \times 8}{64} = \mathbf{750\,000 \text{ lines}}$$

**Ratio ≈ 1.83×.** *(Verified.)*

> Accept a student who also notes that AoS wastes the `name` field entirely — 32 of 88 bytes fetched
> and never read.

### (b) [4]

Any one, argued:

- **A single particle is no longer one object.** Passing "particle 5" to a function means passing six array references and an index.
- **Insertion and deletion touch six arrays**, and a bug that updates five of them is now possible.
- **Poor locality for the opposite access pattern** — code that touches all fields of one particle now strides across six arrays.
- **It fights the type system**; the compiler can no longer check that you are handling one coherent object.

### (c) [5]

**[2] The stride.** Successive column accesses are one row apart: $512 \times 8 = \mathbf{4096}$ bytes. Since $S \times B = 64 \times 64 = 4096$, every access has the **same set index** — all 512 rows compete for one 8-way set.

**[3] The fix does not work, and the explanation is the marked part.**

*(Verified.)*

| | D1 miss rate | LLd miss rate | wall clock |
|---|---:|---:|---:|
| `[512][512]` | 95.0% | 0.6% | 0.1324 s |
| `[512][513]` | 93.7% | 0.6% | **0.1347 s** |

**Padding moved the miss rate by 1.3 points and made the program marginally slower.**

**Why.** The dominant cost is **spatial locality, not conflict**: column traversal takes **one useful `double` from each 64-byte line**, so 7/8 of every fetch is discarded regardless of which set it lands in. And `LLd = 0.6%` says those misses are being served by **L3 at ~41 cycles**, not DRAM at ~438 — the whole 2 MiB array is resident, so each miss is cheap and there are simply a lot of them.

**The principle:** padding addresses conflict misses; blocking addresses capacity misses; nothing addresses compulsory misses. **Diagnose which kind dominates before choosing.** Applying a correct technique to the wrong miss type measures nothing — which is exactly what happens here.

> **Students who report that padding helped have not measured it.** Ask for their numbers. This
> question exists specifically to break the habit of applying remembered fixes without diagnosis.

---

## Mark Summary

| | |
|---|---:|
| Q1 | 16 |
| Q2 | 20 |
| Q3 | 34 |
| Q4 | 16 |
| Q5 | 14 |
| **Total** | **100** |

**Where the class loses marks, in order:**

1. **Q3(d)** — explaining the speedup as "fewer cache misses" without noticing D1 went *up*.
2. **Q5(c)** — reporting that padding helped, having assumed rather than measured.
3. **Q4(d)** — defending blocking instead of explaining why a null result is evidence.
4. **Q2(d)** — describing prefetching without addressing why the rest of the week matters.
5. **Q3(c)** — claiming the derived tile size matches the measured optimum when it does not.

Items 1 and 2 are the same error — **assuming the mechanism instead of measuring it** — and are worth fifteen minutes in the Week 5 review, since Midterm 1 covers this week.

---

*CS 201 · Week 4 · PS 4 Solutions · Instructor Only*
